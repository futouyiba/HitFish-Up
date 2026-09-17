#!/usr/bin/env python3
"""人机共创回路：把你**手工改过**的 .drawio 与"我发射的基线"逐 cell 对差，
产出一份结构化改动清单。

为什么需要它：改图时"我说你改"这条路是**有损**的 —— 你说"这个框往右一点"，
我得猜是哪个框、往右多少。而你在 draw.io 里拖一下，落到磁盘上就是一段**精确的
坐标变化**。这个脚本把那段变化翻译成我能直接执行的清单。

回路（三个文件，别混）：

    generated/fcf-system-map.drawio   ← 构建产物，**永远不要手改**（一重建就没了）
    working/baseline.drawio           ← 快照：创建 working 时那份基线（对差的参照系）
    working/edited.drawio             ← **你在这里改**（draw.io Desktop 打开它）

改完保存，跑 `roundtrip.py diff`，我就知道你动了什么。

    python3 build/roundtrip.py init     # 建/刷新工作副本（会拒绝覆盖已有改动）
    python3 build/roundtrip.py status   # 一句话：改了几处、要不要重开工作副本
    python3 build/roundtrip.py diff     # 结构化改动清单
    python3 build/roundtrip.py diff --json
    python3 build/roundtrip.py open     # 怎么打开 working/edited.drawio
    python3 build/roundtrip.py reset --force   # 丢掉改动，回到新基线

对差是**按 cell 语义**比的，不是文本 diff —— draw.io 保存时会把整份文件重写
（属性顺序、viewport 的 dx/dy 都会变），文本 diff 全是噪声。
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import sys
import urllib.parse
import zlib
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                       # fcf-system-map/
WORK = ROOT / "working"
BASELINE = WORK / "baseline.drawio"
EDITED = WORK / "edited.drawio"
MANIFEST = WORK / "manifest.json"
GENERATED = ROOT / "generated" / "fcf-system-map.drawio"
# 稳定页 id（与 graph.json 的 mxfile/diagram 一致）—— get_page/set_page 用它定位。
PAGE_ID = "fcf-canonical-system-map"

# 改动分类。这一栏决定"该改哪个源文件"，是整份清单的用处所在。
CLASS_OF = {
    "added": "semantic", "removed": "semantic", "relabeled": "semantic",
    "reparented": "semantic", "reconnected": "semantic", "rerouted": "semantic",
    "moved": "geometric", "resized": "geometric",
    "restyled": "cosmetic", "visibility": "cosmetic",
}
WHERE = {
    "relabeled": "graph.json 的 label",
    "added": "graph.json 的 nodes + layout.json 的包纳树",
    "removed": "graph.json 的 nodes + layout.json 的包纳树",
    "reparented": "graph.json 的 parent",
    "reconnected": "graph.json 的 edges",
    "rerouted": "graph.json 的 edges（exit/entry/route/lane）",
    "moved": "layout.json（声明式）或 overrides 层（一次性）",
    "resized": "layout.json 的 w/h 或容器的 even/fill",
    "restyled": "多半是 scope lens 或手改样式，需人工判",
    "visibility": "views.json 的 expansion 或 layout.json 的 when",
    "page": "构建器里由版面算出的页宽页高（一般不用手改）",
}

# cell id → graph.json 的 label。报告里报 id 不如报名字 ——
# "removed R2.C1.F5" 你得回去查，"removed 忽略因子（六角形）" 一眼就懂。
_LABELS = None


def labels() -> dict:
    global _LABELS
    if _LABELS is None:
        try:
            g = json.loads((ROOT / "graph.json").read_text(encoding="utf-8"))
            _LABELS = {n["id"]: n.get("label", "") for n in g["nodes"]}
        except Exception:
            _LABELS = {}
    return _LABELS


def name_of(cid: str) -> str:
    lb = labels().get(cid)
    return "%s（%s）" % (cid, lb) if lb else cid

# mxGraphModel 上纯视口/开关类属性：你平移一下画布它就变，但对内容毫无意义。
# 不排掉的话，每次 diff 都会被这些噪声淹没。
MODEL_NOISE = {"dx", "dy", "grid", "gridSize", "guides", "tooltips", "connect",
               "arrows", "fold", "pageScale", "math", "shadow", "page"}


# --------------------------------------------------------------- 读 .drawio --

def _inflate(body: str) -> str:
    """draw.io 的压缩页：XML → encodeURIComponent → raw deflate → base64。
    三步逆着来。（与官方 MCP `pages.js` 的 decompressDiagram 同一套。）"""
    raw = base64.b64decode(body)
    return urllib.parse.unquote(zlib.decompress(raw, -15).decode("utf-8"))


def pages_of(path: Path):
    """[(page_id, page_name, mxGraphModel Element|None)]，自动解压。

    `<diagram>` 的载荷有两种形态，都要认：
      * **子元素**：`<diagram><mxGraphModel>…</mxGraphModel></diagram>`（未压缩）
      * **文本 base64**：`<diagram>eNq…</diagram>`（draw.io 默认存的压缩页）
    只看 `d.text` 会漏掉第一种 —— 元素在前时 `text` 只剩缩进空白。
    """
    root = ET.parse(str(path)).getroot()
    if root.tag == "mxGraphModel":                 # 裸模型文件（没有 mxfile 壳）
        return [(None, None, root)]
    out = []
    for d in root.iter("diagram"):
        model = None
        for c in d:
            if c.tag == "mxGraphModel":
                model = c
                break
        if model is None:
            body = (d.text or "").strip()
            if body.startswith("<"):
                model = ET.fromstring(body)
            elif body:
                model = ET.fromstring(_inflate(body))
        out.append((d.get("id"), d.get("name"), model))
    return out


def pick_page(path: Path, page: str | None = None):
    pages = pages_of(path)
    if not pages:
        sys.exit("error: %s 里没有 <diagram>" % path)
    if page is None:
        for pid, _, model in pages:
            if pid == PAGE_ID:
                return pid, model
        return pages[0][0], pages[0][2]
    for pid, name, model in pages:
        if page in (pid, name):
            return pid, model
    if page.isdigit() and int(page) < len(pages):
        return pages[int(page)][0], pages[int(page)][2]
    sys.exit("error: %s 里没有页 %r（有：%s）"
             % (path, page, [p[0] for p in pages]))


def parse_style(style: str) -> dict:
    """样式串 → dict。draw.io 保存时**会重排键序**，按串比会产生假差异。"""
    out = {}
    for part in (style or "").split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            out[k] = v
        else:
            out[part] = "1"          # 裸 flag，如 dashed
    return out


def _num(v):
    if v is None:
        return None
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except (TypeError, ValueError):
        return v


def _cell(cid, mx, value, parent) -> dict:
    geo, pts = {}, []
    g = mx.find("mxGeometry")
    if g is not None:
        for k in ("x", "y", "width", "height"):
            geo[k] = _num(g.get(k))
        # 途经点可能放在**多个** <Array as="points"> 里（draw.io 拖动线段时自己
        # 怎么放不确定），所以全收，不只取第一个 —— 少收一个 Array 就等于漏报一次拖动。
        for arr in g.findall("Array"):
            pts.extend([_num(p.get("x")), _num(p.get("y"))]
                       for p in arr.findall("mxPoint"))
    return {
        "id": cid, "value": value or "",
        "style": mx.get("style") or "", "styleMap": parse_style(mx.get("style") or ""),
        "parent": parent or "",
        "vertex": mx.get("vertex") == "1", "edge": mx.get("edge") == "1",
        "visible": mx.get("visible") != "0",
        "source": mx.get("source") or "", "target": mx.get("target") or "",
        "geo": geo, "points": pts or None,
    }


def cells_of(model) -> dict:
    """{cell_id: cell}。UserObject 包着的 cell（带 link 的那些）id 在包装层上，
    要单独收 —— 直接 iter('mxCell') 会把它们漏掉或误判。"""
    out, inner = {}, set()
    for uo in model.iter("UserObject"):
        m = uo.find("mxCell")
        if m is None:
            continue
        inner.add(id(m))
        cid = uo.get("id")
        if cid:
            out[cid] = _cell(cid, m, uo.get("label"), m.get("parent"))
    for mx in model.iter("mxCell"):
        if id(mx) in inner:
            continue
        cid = mx.get("id")
        if not cid or cid in ("0", "1"):
            continue
        out[cid] = _cell(cid, mx, mx.get("value"), mx.get("parent"))
    return out


# -------------------------------------------------------------------- 对差 --

def looks_autogenerated(cid: str) -> bool:
    """draw.io 新画的方块会给随机 id。我们的语义 id 是 R2.C1.A1 这种。
    分不清的话，"你新加了一个框"会被误读成"你改了一个已有节点"。"""
    if not cid:
        return True
    if "/" in cid:                              # 贴边壳 C:W:xxx
        return False
    head = cid.split(".")[0]
    return not (head and head.replace("_", "").isalnum()
                and head[:1].isupper() and len(head) <= 14)


def abs_xy(cells: dict, cid: str) -> list:
    """沿父链累加 → 绝对页面坐标。

    .drawio 里子 cell 的 x/y 是**相对父容器**的，所以直接报局部坐标会误导：
    "R2.F.CORE 移到了 [156, -11]" 里的 -11 只是它在自己贴边壳里的偏移，
    不是页面上往上了 11。对差要给人看，就得换算成绝对坐标。
    """
    x = y = 0
    cur, seen = cid, set()
    while cur and cur in cells and cur not in seen:
        seen.add(cur)
        g = cells[cur]["geo"]
        x += g.get("x") or 0
        y += g.get("y") or 0
        cur = cells[cur]["parent"]
    return [x, y]


def diff_cells(base: dict, edit: dict) -> list:
    changes = []
    for cid in sorted(set(base) | set(edit)):
        b, e = base.get(cid), edit.get(cid)
        if b is None:
            changes.append({"id": cid, "kind": "added", "cls": "semantic",
                            "detail": {"label": e["value"], "parent": e["parent"],
                                       "vertex": e["vertex"], "edge": e["edge"],
                                       "autogenerated_id": looks_autogenerated(cid)}})
            continue
        if e is None:
            changes.append({"id": cid, "kind": "removed", "cls": "semantic",
                            "detail": {"label": b["value"], "parent": b["parent"],
                                       "vertex": b["vertex"], "edge": b["edge"]}})
            continue

        def add(kind, detail):
            changes.append({"id": cid, "kind": kind, "cls": CLASS_OF[kind],
                            "detail": detail})

        if b["value"] != e["value"]:
            add("relabeled", {"from": b["value"], "to": e["value"]})
        if b["parent"] != e["parent"]:
            add("reparented", {"from": b["parent"], "to": e["parent"]})
        if b["source"] != e["source"] or b["target"] != e["target"]:
            add("reconnected", {"from": [b["source"], b["target"]],
                                "to": [e["source"], e["target"]]})
        if b["visible"] != e["visible"]:
            add("visibility", {"from": b["visible"], "to": e["visible"]})
        if b["points"] != e["points"]:
            add("rerouted", {"from": b["points"], "to": e["points"]})

        # 样式：比 dict、只报真正变了的键，而不是整串（键序会被 draw.io 重排）
        sk = {k for k in set(b["styleMap"]) | set(e["styleMap"])
              if b["styleMap"].get(k) != e["styleMap"].get(k)}
        if sk:
            add("restyled", {k: [b["styleMap"].get(k), e["styleMap"].get(k)]
                             for k in sorted(sk)})

        bgeo, egeo = b["geo"], e["geo"]
        dx = [bgeo.get("x"), egeo.get("x")]
        dy = [bgeo.get("y"), egeo.get("y")]
        if dx[0] != dx[1] or dy[0] != dy[1]:
            delta = [None if None in dx else dx[1] - dx[0],
                     None if None in dy else dy[1] - dy[0]]
            add("moved", {"abs_from": abs_xy(base, cid), "abs_to": abs_xy(edit, cid),
                          "delta": delta,
                          "local_from": [dx[0], dy[0]], "local_to": [dx[1], dy[1]]})
        dw = [bgeo.get("width"), egeo.get("width")]
        dh = [bgeo.get("height"), egeo.get("height")]
        if dw[0] != dw[1] or dh[0] != dh[1]:
            add("resized", {"from": [dw[0], dh[0]], "to": [dw[1], dh[1]],
                            "delta": [None if None in dw else dw[1] - dw[0],
                                      None if None in dh else dh[1] - dh[0]]})
    return changes


def diff_models(bm, em) -> list:
    """模型级差异（页宽页高等）。视口类属性已被排除。"""
    out = []
    if bm is None or em is None:
        return out
    keys = (set(bm.attrib) | set(em.attrib)) - MODEL_NOISE
    for k in sorted(keys):
        if bm.get(k) != em.get(k):
            out.append({"id": "(model)", "kind": "page", "cls": "geometric",
                        "detail": {k: [bm.get(k), em.get(k)]}})
    return out


def diff_files(baseline: Path, edited: Path, page=None):
    bpid, bm = pick_page(baseline, page)
    epid, em = pick_page(edited, page)
    bc, ec = cells_of(bm), cells_of(em)
    return {"baseline_page": bpid, "edited_page": epid,
            "baseline_cells": len(bc), "edited_cells": len(ec),
            "model": diff_models(bm, em),
            "changes": diff_cells(bc, ec)}


# ------------------------------------------------------------------ 报告 --

def render(report: dict) -> str:
    ch = report["model"] + report["changes"]
    if not ch:
        return ("没有差异 —— working/edited.drawio 与基线逐 cell 一致。\n"
                "（要么你还没改，要么改完没保存。）")
    by_cls = {"semantic": [], "geometric": [], "cosmetic": []}
    for c in ch:
        by_cls[c["cls"]].append(c)
    L = []
    L.append("基线 %d cell → 改动后 %d cell，共 **%d** 处差异："
             % (report["baseline_cells"], report["edited_cells"], len(ch)))
    for cls, title, hint in (
            ("semantic", "语义改动（要落进 graph.json / layout.json 的结构）",
             "→ 我按这个改源文件"),
            ("geometric", "几何改动（位置 / 尺寸）",
             "→ 声明式地块改 layout.json；一次性手摆改 overrides 层"),
            ("cosmetic", "样式 / 可见性（多半是 lens 或临时试色）",
             "→ 先确认是不是有意的")):
        if not by_cls[cls]:
            continue
        L.append("")
        L.append("## %s —— %d 处" % (title, len(by_cls[cls])))
        L.append("_%s_" % hint)
        for c in sorted(by_cls[cls], key=lambda x: (x["kind"], x["id"])):
            L.append("  %-11s %-34s %s"
                     % (c["kind"], name_of(c["id"]), _short(c)))
    L.append("")
    L.append("落点提示：" + "；".join(
        sorted({WHERE.get(c["kind"], "?") for c in ch})))
    return "\n".join(L)


def _short(c) -> str:
    d, k = c["detail"], c["kind"]
    if k == "relabeled":
        return "%r → %r" % (d["from"], d["to"])
    if k == "moved":
        return "绝对 %s → %s  (Δ%s)" % (d["abs_from"], d["abs_to"], d["delta"])
    if k == "resized":
        return "%s → %s  (Δ%s)" % (d["from"], d["to"], d["delta"])
    if k == "added":
        return "%r  父=%s%s" % (d["label"], d["parent"],
                                "  ⚠ id 像是 draw.io 自动生成的，需要给它一个语义 id"
                                if d["autogenerated_id"] else "")
    if k == "removed":
        return "父=%s  原文字=%r" % (d["parent"], d["label"])
    if k == "restyled":
        return ", ".join("%s %s→%s" % (a, b[0], b[1]) for a, b in d.items())
    if k == "reparented":
        return "%s → %s" % (d["from"], d["to"])
    if k == "rerouted":
        return "%s → %s" % (d["from"], d["to"])
    if k == "reconnected":
        return "%s → %s" % (d["from"], d["to"])
    if k == "visibility":
        return "%s → %s" % (d["from"], d["to"])
    return json.dumps(d, ensure_ascii=False)[:90]


# ------------------------------------------------------------------ 仓库 --

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else "-"


def head_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "-"


def cmd_init(force: bool):
    if not GENERATED.exists():
        sys.exit("error: %s 不存在 —— 先跑 python3 build/build_diagram.py" % GENERATED)
    if EDITED.exists() and not force:
        # 不轻易覆盖：working/edited.drawio 里可能是你正在做的手工改动。
        r = diff_files(BASELINE, EDITED) if BASELINE.exists() else None
        n = len(r["changes"]) + len(r["model"]) if r else "?"
        sys.exit("working/edited.drawio 已存在（与基线差 %s 处）。\n"
                 "  想保留你的改动 → 什么都别做，直接跑 diff。\n"
                 "  确认要丢掉重来 → 加 --force" % n)
    WORK.mkdir(exist_ok=True)
    data = GENERATED.read_bytes()
    BASELINE.write_bytes(data)          # 同一个字节：参照系 = 我发射的基线
    EDITED.write_bytes(data)
    MANIFEST.write_text(json.dumps({
        "page": PAGE_ID,
        "baseline_sha256": sha(BASELINE),
        "source_sha256": sha(GENERATED),
        "snapshot_commit": head_commit(),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("工作副本已就绪：")
    print("  参照系  working/baseline.drawio  (%s)" % sha(BASELINE))
    print("  改这个  working/edited.drawio")
    print("  快照自  %s @ %s" % (sha(GENERATED), head_commit()))
    print("\n下一步：python3 build/roundtrip.py open")


def cmd_status():
    if not EDITED.exists():
        print("还没有工作副本 —— 跑 python3 build/roundtrip.py init")
        return
    if not BASELINE.exists():
        print("缺 working/baseline.drawio —— 跑 init 重建（会丢改动，或加 --force）")
        return
    r = diff_files(BASELINE, EDITED)
    n = len(r["changes"]) + len(r["model"])
    print("working/edited.drawio：%d 处改动（语义 %d / 几何 %d / 样式 %d）"
          % (n,
             sum(1 for c in r["changes"] if c["cls"] == "semantic"),
             sum(1 for c in r["changes"] + r["model"] if c["cls"] == "geometric"),
             sum(1 for c in r["changes"] if c["cls"] == "cosmetic")))
    if MANIFEST.exists():
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if m.get("source_sha256") != sha(GENERATED):
            print("⚠ 快照之后 generated/ 已经变过（%s → %s）—— 重开工作副本才能"
                  "对到最新基线：init --force" % (m.get("source_sha256"), sha(GENERATED)))
    if n == 0:
        print("（与基线一致；改完记得在 draw.io 里保存）")


def cmd_diff(as_json: bool, page=None):
    if not EDITED.exists():
        sys.exit("还没有 working/edited.drawio —— 先跑 init")
    r = diff_files(BASELINE, EDITED, page)
    print(json.dumps(r, ensure_ascii=False, indent=2) if as_json else render(r))


def cmd_open():
    p = EDITED.resolve()
    print("改这个文件：%s" % p)
    print()
    print("draw.io Desktop（推荐，本地文件原生）：")
    print("  open -a draw.io \"%s\"" % p)
    print()
    print("浏览器（app.diagrams.net，官方在线编辑器）：")
    print("  https://app.diagrams.net/  →  Open from → Device → 选上面那个文件")
    print()
    print("⚠ 存回**同一个路径**（Save / Cmd-S）。若在浏览器里用 Save as 存到别处，")
    print("  回路就断了。也别去改 generated/fcf-system-map.drawio —— 那是构建产物。")
    print("  改完跑：python3 build/roundtrip.py diff")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_init = sub.add_parser("init", help="建/刷新工作副本")
    p_init.add_argument("--force", action="store_true", help="覆盖已有改动")
    sub.add_parser("status", help="一句话状态")
    p_diff = sub.add_parser("diff", help="结构化改动清单")
    p_diff.add_argument("--json", action="store_true")
    p_diff.add_argument("--page", default=None)
    sub.add_parser("open", help="怎么打开工作副本")
    p_reset = sub.add_parser("reset", help="丢掉改动、回到新基线")
    p_reset.add_argument("--force", action="store_true", required=True,
                         help="必须显式确认（会丢改动）")
    a = ap.parse_args()
    if a.cmd == "init":
        cmd_init(a.force)
    elif a.cmd == "status":
        cmd_status()
    elif a.cmd == "diff":
        cmd_diff(a.json, a.page)
    elif a.cmd == "open":
        cmd_open()
    elif a.cmd == "reset":
        cmd_init(True)


if __name__ == "__main__":
    main()

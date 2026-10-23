#!/usr/bin/env python3
"""roundtrip.py 的回归测试：确认对差「该抓的抓得住、该忽略的忽略掉」。

为什么值得单独测：这个脚本的用途是我**据此改源文件**。漏报一处，你的手工改动就
白做了；误报（把 draw.io 保存时的噪声当成改动）会淹没真信号，让我去改一堆没动过
的地方。两边都会毁掉回路，所以两种情况都在这里锁住。

⚠️ **测试不许硬编码 cell id。** 图上的 id 会随设计改名（类别头节点退场、
`R2.C1.K` 改叫 `R2.C1.F1.FIT`……），写死 id 的测试会跟着碎 —— 而那是测试的问题、
不是被测对象的问题。所以下面一律**按特征挑**被测的 cell，把挑中的 id 记下来再断言。

用自己的临时文件，**不碰 working/** —— 那里面可能是你正在做的手工改动。

    python3 build/test_roundtrip.py
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from roundtrip import diff_files, parse_style  # noqa: E402

SRC = HERE.parent / "generated" / "fcf-system-map.drawio"
fails = []
# mutate() 按特征挑出来的 id，main() 据此断言。
PICK = {}


def check(cond, msg):
    if not cond:
        fails.append(msg)
    return cond


def mutate(src: Path, dst: Path) -> None:
    """伪造一份「人工在 draw.io 里改过、并被 draw.io 整体重写」的文件。"""
    tree = ET.parse(str(src))
    root = tree.getroot()
    # 必须取**同一棵树**里的 model —— 另起一次 parse 会把改动写进另一个对象。
    diagram = next(root.iter("diagram"))
    model = next(c for c in diagram if c.tag == "mxGraphModel")

    # 噪声 1：画布平移（draw.io 会把视口写进 dx/dy）—— 必须被忽略
    model.set("dx", "4821")
    model.set("dy", "1777")

    # ── 按特征挑被测 cell（见模块 docstring）──────────────────────────
    verts = [mx for mx in model.iter("mxCell")
             if mx.get("vertex") == "1" and mx.get("id") not in (None, "0", "1")
             and mx.find("mxGeometry") is not None]
    labeled = [mx for mx in verts if (mx.get("value") or "").strip()]
    # 挑**嵌套**的 cell（父不是图层）—— 顶层的局部坐标恰好等于绝对坐标，
    # 拿它测"报的是不是绝对坐标"测不出东西。
    nested = [mx for mx in labeled if (mx.get("parent") or "").startswith("C:")]
    pool = nested or labeled
    check(len(pool) >= 5, "带文字且嵌套的 cell 少于 5 个，测试样本不够")
    if len(pool) < 5:
        return
    pick_move, pick_resize, pick_relabel, pick_remove, pick_restyle = pool[:5]
    PICK.update(move=pick_move.get("id"), resize=pick_resize.get("id"),
                relabel=pick_relabel.get("id"), remove=pick_remove.get("id"),
                restyle=pick_restyle.get("id"))

    edges = [mx for mx in model.iter("mxCell")
             if mx.get("edge") == "1" and mx.get("id")]
    withpts = [e for e in edges
               if e.find("mxGeometry") is not None
               and e.find("mxGeometry").find("Array") is not None
               and e.find("mxGeometry").find("Array").findall("mxPoint")]
    simple = [e for e in edges if e not in withpts]
    check(bool(withpts) and bool(simple), "找不到足够的边来做拖动/噪声测试")
    if not (withpts and simple):
        return
    PICK.update(drag=withpts[0].get("id"), noise=simple[0].get("id"))

    def geo(mx):
        return mx.find("mxGeometry")

    # ── 真改动 ──────────────────────────────────────────────────────
    g = geo(pick_move)                      # 移动
    g.set("x", str(int(g.get("x")) + 37))
    g.set("y", str(int(g.get("y")) - 11))

    g = geo(pick_resize)                    # 拉大
    g.set("width", str(int(g.get("width")) + 100))
    g.set("height", str(int(g.get("height")) + 20))

    pick_relabel.set("value", "我改过的名字")   # 改文字（普通 cell 在 value 上）

    for parent in model.iter():             # 删一个
        if pick_remove in list(parent):
            parent.remove(pick_remove)
            break

    newmx = ET.SubElement(model.find("root"), "mxCell")   # 新画一个（自动 id）
    newmx.set("id", "k7QmZ3vRt9")
    newmx.set("value", "我新加的一个框")
    newmx.set("style", "rounded=1;whiteSpace=wrap;html=1;")
    newmx.set("vertex", "1")
    newmx.set("parent", "Layer:Main")
    ng = ET.SubElement(newmx, "mxGeometry")
    for k, v in (("x", "900"), ("y", "2400"), ("width", "160"), ("height", "44")):
        ng.set(k, v)
    ng.set("as", "geometry")

    drag = geo(withpts[0]).find("Array")    # 拖一条边（改已有 Array 的点）
    for el, (x, y) in zip(drag.findall("mxPoint"), ((30, 700), (30, 1500))):
        el.set("x", str(x))
        el.set("y", str(y))

    sm = parse_style(pick_restyle.get("style"))          # 改样式 + 键序重排
    sm["fillColor"] = "#ff0000"
    pick_restyle.set("style",
                     ";".join("%s=%s" % (k, v) for k, v in reversed(list(sm.items()))) + ";")

    sm = parse_style(simple[0].get("style"))             # 噪声 2：只重排键序，不该被报
    simple[0].set("style",
                  ";".join("%s=%s" % (k, v) for k, v in reversed(list(sm.items()))) + ";")

    ET.indent(tree, space="  ")
    tree.write(str(dst), encoding="utf-8", xml_declaration=True)


def main():
    if not SRC.exists():
        sys.exit("error: 先跑 python3 build/build_diagram.py")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        base, edited = td / "base.drawio", td / "edited.drawio"
        shutil.copy(SRC, base)
        mutate(SRC, edited)

        r = diff_files(base, edited)
        got = {(c["id"], c["kind"]) for c in r["changes"]}

        expect = {
            (PICK["move"], "moved"),
            (PICK["resize"], "resized"),
            (PICK["relabel"], "relabeled"),
            (PICK["remove"], "removed"),
            ("k7QmZ3vRt9", "added"),
            (PICK["drag"], "rerouted"),
            (PICK["restyle"], "restyled"),
        }
        for pair in sorted(expect - got):
            fails.append("漏报：%s %s" % pair)
        for pair in sorted(got - expect):
            fails.append("误报：%s %s" % pair)
        check(("(model)", "page") not in got, "模型级差异被混进了 cell 差异")

        # 噪声必须一字不报
        check(not any(c["id"] == PICK["noise"] for c in r["changes"]),
              "误报：只重排 style 键序被当成了改动（%s；draw.io 保存必然这样做）"
              % PICK["noise"])
        check(not any(c["kind"] == "visibility" for c in r["changes"]),
              "误报：出现无中生有的 visibility 变化")

        # 认得出 draw.io 自动生成的 id（否则"新加"会被误读成"改了已有节点"）
        added = [c for c in r["changes"] if c["kind"] == "added"]
        check(added and added[0]["detail"]["autogenerated_id"],
              "新画的方块没被识别为自动 id")

        # 移动要报**绝对**坐标（局部坐标对着页面看不出来）
        moved = [c for c in r["changes"] if c["kind"] == "moved"][0]
        check(moved["detail"]["abs_from"] != moved["detail"]["local_from"],
              "moved 报的是局部坐标，不是绝对坐标")

        # 确定性：同样的两份输入必须同结果
        check(json.dumps(diff_files(base, edited), sort_keys=True, ensure_ascii=False)
              == json.dumps(r, sort_keys=True, ensure_ascii=False),
              "对差结果不是确定性的")

    if fails:
        print("TEST: FAIL (%d)" % len(fails))
        for f in fails:
            print("  - " + f)
        sys.exit(1)
    print("TEST: PASS")
    print("  该抓的：moved / resized / relabeled / removed / added / rerouted / restyled / page")
    print("  该忽略的：画布 dx/dy 位移、未改动边的 style 键序重排")
    print("  被测 cell 按特征挑：%s" % json.dumps(PICK, ensure_ascii=False))


if __name__ == "__main__":
    main()

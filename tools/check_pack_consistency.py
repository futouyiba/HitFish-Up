#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_pack_consistency — 审阅包内部一致性巡检（**候选发现器，不是证明器**）。

用途
    本族的审阅包是**多份文档并置**（`OPEN-ITEMS` / `contract-cards` / `consolidated` /
    `figma-current` / `README`）。实测反复出现的失效模式只有一种形态：

        **同一条「射程 / 边界 / 限定 / 状态」被正确写在 A 处，又被在 B 处重新附加、收窄、
        或干脆写成相反的读数 —— 而两处各自读起来都对。**

    2026-09-21 两轮独立复审在 PR #7 上报出的 6 条 finding，**6/6 全是这一形态**
    （ADJ-12 补档案规则 / Species Role UI 状态 / 卡8 未冻结 / §3 vs §6 覆盖缺口 /
    typed-value guard 射程 /「丢弃未保存的改动」射程）。

判据（本项目 Owner 确认过的口径）
    **凡一条「射程／边界／限定／状态」在包内多处出现的，逐处取字节比一遍 ——
    要么逐字同形，要么显式标「已作废」，二者必居其一。**

★★ 实测的覆盖面（**别把本脚本当保障**）────────────────────────────────────
    用**修复前的真实包**（`fa96900`）做回归，结果是**只有 C2 会红**：

        C1（主题极性）在真实包上报 **0** —— 它**抓不到那 6 条 finding**。
        原因：C1 的判据是**状态词**（已裁/未裁…），而那 6 条相抵是**内容/射程**型
        （「补档案规则**仍在**」vs「**不自动**建 Profile」）—— 两句里**一个状态词都没有**。
        C1 只能覆盖「同一主题一处在说已裁、另一处在说未裁」这一子类（本族确有，但 ≠ 主类）。

    ⇒ **C2（计数）与 C3（跨容器引用）是能红的**；**C1 弱**，留着只作补充线索。
    ⇒ **主类（射程/限定被重新附加或收窄）目前仍只能人工逐处对—— 这是本工具的已知缺口。**

⚠️ 本脚本做的是**启发式候选发现**，不是语义证明：
    · 它按「主题 token 共现 + 极性相反」找候选，**会漏**（措辞完全不同的相抵它找不到）；
    · 它排除带「留痕/作废/更正」盾的块（那类是有意保留的旧说法）；
    · **它报出来的每一条都要人回原文核**；它报 0 条**不等于**包内一致。

三项检查
    C1 主题极性相抵 —— 同一主题在 ≥2 个块里既有「已闭」极性又有「未闭」极性
    C2 计数相抵     —— 「N 项已裁 / 零项待裁」这类计数声明 vs 显式登记的开项数
    C3 引用可解析   —— 包内/说明里引用的仓内路径是否真的存在

自检（**非空转**；不通过则退 2、什么都不做）
    隔离临时夹具，**两个方向都测**（「该红的会不会红」＋「不该红的会不会红」）：
      ① 同主题 · 极性相反          ⇒ 必须红
      ② 同主题 · 极性相同          ⇒ 必须绿
      ③ 带留痕盾的相反极性          ⇒ 必须绿（有意保留的旧说法不是缺陷）
      ④ 引用不存在的路径            ⇒ 必须红
      ⑤ 引用存在的路径              ⇒ 必须绿
      ⑥ 真实 C2 缺陷 + 四个登记标记  ⇒ 必须红；裸零项主张/留痕/同块说明必须绿

用法
    python3 tools/check_pack_consistency.py --pack docs/review/ui-component-contract-r2
    python3 tools/check_pack_consistency.py --pack <dir> --repo . --json

输出约定
    --json 的 stdout 为单个 JSON 对象；自检、错误与边界提示写 stderr。
    status=completed / exit_code=0 只表示扫描完成（即使有候选）；不是一致性证明。
    status=error / exit_code=2 表示参数、自检或输入失败；checks=null，不能当干净。
    checks 包含 c1 候选、c2 声明/开项块计数/候选、c3 路径/缺失引用。
    --help 仍输出帮助。C2 按块计数，不做自然语言语义判断或开项身份去重。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

# ── 极性标记 ────────────────────────────────────────────────────────────────
CLOSED = [u"已裁", u"已闭", u"已落", u"已冻结", u"CLOSED", u"已对齐", u"已收敛",
          u"已实现", u"已改", u"已澄清", u"已同步"]
OPEN = [u"未裁", u"未决", u"待裁", u"待设计", u"待做", u"OPEN", u"仍开",
        u"未冻结", u"尚未", u"仍未", u"未落页", u"未闭合"]

# ── 留痕盾：这些块是**有意保留的旧说法**，不算相抵 ─────────────────────────
SHIELD = [u"已作废", u"此前", u"一度", u"不再是", u"原写", u"旧注", u"~~", u"更正",
          u"留痕", u"先前写", u"本行曾", u"曾写", u"那条是错的"]

# ── 主题 token（**只收具体标识**；不收泛词、不收文件名）─────────────────────
# 第一版把「反引号里任意 2–40 字」都当主题 ⇒ `Role` / `SET` / `CLEAR` / 文件名全进来，
# 一个段落带上五个 ADJ 编号就被当成五个主题 ⇒ **38 个候选、几乎全是噪声**。
# ⇒ 收紧：只收 (a) 编号型主题；(b) **形如代码标识符**的反引号串。
NUM_SUBJ = re.compile(r"ADJ-\d+|CXR7-[A-Z]+-\d+|GPT-R2-\d+|A?[①②]-?卡\d+|卡\d+|§\d+(?:[.\-–]\d+)*")
IDENT_SUBJ = re.compile(r"`([A-Za-z_][A-Za-z0-9_]*[A-Za-z0-9])`|`([A-Z][A-Za-z0-9_]+)`")
FILEISH = re.compile(r"\.(md|py|mjs|ts|json|xlsx|csv)$", re.I)
GENERIC = set(u"role set clear add absent inherit core secondary ignored value op null "
              u"name id key tier bucket species profile source template patch ledger".split())


def _is_ident(tok):
    if FILEISH.search(tok) or tok.lower() in GENERIC or len(tok) < 4:
        return False
    # 必须「像代码标识符」：含下划线 / 内部大写 / 全大写
    return ("_" in tok) or re.search(r"[a-z][A-Z]", tok) or tok.isupper()


def subjects(text: str):
    out = set(NUM_SUBJ.findall(text))
    for m in IDENT_SUBJ.finditer(text):
        tok = m.group(1) or m.group(2)
        if _is_ident(tok):
            out.add(tok)
    return out


SENT_SPLIT = re.compile(u"(?<=[。；！？])|\n")


def sentences(blk: str):
    for s in SENT_SPLIT.split(blk):
        s = s.strip()
        if len(s) >= 8:
            yield s


def polarity(text: str):
    c = [k for k in CLOSED if k in text]
    o = [k for k in OPEN if k in text]
    return (bool(c), bool(o), c, o)


def shielded(text: str) -> bool:
    return any(x in text for x in SHIELD)


def iter_blocks(path: str):
    """把 md 切成块：空行分段；表格行各自成块（表内一格一句，最易相抵）。"""
    cur, ln = [], 1
    with open(path, encoding="utf-8") as source:
        for i, line in enumerate(source, 1):
            t = line.rstrip("\n")
            if t.strip() == "" or t.lstrip().startswith("|"):
                if cur:
                    yield ln, "\n".join(cur)
                    cur = []
                if t.lstrip().startswith("|"):
                    yield i, t
            else:
                if not cur:
                    ln = i
                cur.append(t)
    if cur:
        yield ln, "\n".join(cur)


# ── C1 ─────────────────────────────────────────────────────────────────────
def check_c1(files):
    """句子级：同一句里既有**具体主题**又有**极性词**才计入；
    再按主题汇总，**同一主题出现两种极性**才报。"""
    by_subj = {}
    for f in files:
        for ln, blk in iter_blocks(f):
            for sent in sentences(blk):
                if shielded(sent):
                    continue
                subs = subjects(sent)
                if not subs or len(subs) > 3:      # >3 个主题 ⇒ 那是枚举句，不是关于某一条的陈述
                    continue
                c, o, ck, ok = polarity(sent)
                if not (c or o):
                    continue
                for sub in subs:
                    by_subj.setdefault(sub, []).append((os.path.basename(f), ln, c, o, ck, ok, sent))
    hits = []
    for sub, rows in sorted(by_subj.items()):
        if len(rows) < 2:
            continue
        if any(r[2] for r in rows) and any(r[3] for r in rows):
            hits.append((sub, rows))
    return hits


# ── C2 ─────────────────────────────────────────────────────────────────────
COUNT_CLAIM = re.compile(u"([零一二三四五六七八九十百\\d]+)\\s*项已裁")
# ★ 第一版把「影响『零项待裁』的读数」这类**引用**也当成主张 ⇒ 假阳性。
#   修法：主张必须**不在引号内**。
QUOTED = re.compile(u"[「『][^」』]{0,60}(零项待裁|项已裁)[^」』]{0,60}[」』]")
ZERO_CLAIM = re.compile(u"零项待裁")
REG_MARK = re.compile(u"未冻结|未裁|未决|待裁")


def _reg_marks(blk):
    """★ 「零项待裁」这个词**自身含「待裁」** ⇒ 直接拿 OPEN 词表去判「有没有登记开项」
    会把裸主张误判成「已登记」⇒ 真阳性被关掉（实测：REAL-DEFECT 自检维当场变红）。
    ⇒ 判之前先把「零项待裁」抹掉。"""
    return REG_MARK.search(blk.replace(u"零项待裁", u""))


def check_c2(files):
    claims, regs = [], 0
    for f in files:
        txt = Path(f).read_text(encoding="utf-8")
        for m in COUNT_CLAIM.finditer(txt):
            if QUOTED.search(m.group(0)):
                continue
            claims.append((os.path.basename(f), m.group(0)))
        for ln, blk in iter_blocks(f):
            if (ZERO_CLAIM.search(blk) and not shielded(blk) and not QUOTED.search(blk)
                    and not _reg_marks(blk)):        # 同句并陈「另有一处未冻结」⇒ 不是裸主张
                claims.append((os.path.basename(f) + ":%d" % ln, u"零项待裁"))
            if _reg_marks(blk) and not shielded(blk):
                regs += 1
    # 「零项待裁」与显式开项登记不能并存（仅作候选）
    bad = [c for c in claims if ZERO_CLAIM.search(c[1])] if regs else []
    return claims, regs, bad


# ── C3 ─────────────────────────────────────────────────────────────────────
PATH_RE = re.compile(r"(?:^|[\s`（(])((?:docs|tools|src|scripts|tests)/[A-Za-z0-9_./\-]+\.(?:md|py|mjs|ts))")


def check_c3(files, repos):
    """★ 第一版只收一个 repo ⇒ 把**别仓**的路径（编辑器仓 `src/...`、`docs/gaps.md`）全报成
    「不存在」⇒ 假阳性。修法：`--repo` 可重复，**只有所有给定仓都找不到**才报。"""
    seen, miss = set(), []
    for f in files:
        for m in PATH_RE.finditer(Path(f).read_text(encoding="utf-8")):
            p = m.group(1)
            if p in seen:
                continue
            seen.add(p)
            if not any(os.path.exists(os.path.join(r, p)) for r in repos):
                miss.append((os.path.basename(f), p))
    return sorted(seen), miss


# ── 自检 ───────────────────────────────────────────────────────────────────
def selftest():
    """所有文件与仓根都来自本次隔离夹具，不借用待扫描仓的内容。"""
    res = {}
    try:
        with tempfile.TemporaryDirectory(prefix="pack-consistency-") as tmp:
            root = Path(tmp)

            def fixture(name, text):
                path = root / name
                path.write_text(text, encoding="utf-8")
                return str(path)

            a = fixture("opposite.md", "`WidgetFoo` 的射程已裁，只到 ADD。\n\n`WidgetFoo` 仍未裁，待设计。\n")
            res["opposite-polarity-must-flag"] = len(check_c1([a])) >= 1
            b = fixture("same.md", "`WidgetFoo` 已裁。\n\n`WidgetFoo` 也已裁。\n")
            res["same-polarity-must-pass"] = len(check_c1([b])) == 0
            c = fixture("shielded.md", "`WidgetFoo` 已裁。\n\n本行曾写「`WidgetFoo` 未裁」，已作废，保留作留痕。\n")
            res["shielded-must-pass"] = len(check_c1([c])) == 0

            repo = root / "repo"
            (repo / "docs").mkdir(parents=True)
            (repo / "docs" / "exists.md").write_text("fixture", encoding="utf-8")
            d = fixture("missing.md", "见 `docs/nope/nope.md`。\n")
            _, miss = check_c3([d], [str(repo)])
            res["missing-path-must-flag"] = len(miss) >= 1
            e = fixture("existing.md", "见 `docs/exists.md`。\n")
            _, miss = check_c3([e], [str(repo)])
            res["existing-path-must-pass"] = len(miss) == 0

            # PR #7 真实缺陷的逐字摘录，保留作为回归。
            claim = fixture("claim.md", "## 2. Owner 裁决状态 —— **十三项已裁，零项待裁**\n")
            reg = fixture("real.md", "  ⇒ **该子情形按「未冻结」读**：实现**不得默认它已冻结，也不得静默选一种**\n")
            _, _, bad = check_c2([claim, reg])
            res["REAL-DEFECT-must-flag"] = len(bad) >= 1
            _, regs, bad = check_c2([claim])
            res["zero-claim-must-pass"] = regs == 0 and not bad
            for marker in ("待裁", "未裁", "未决", "未冻结"):
                reg = fixture("marker.md", "| ADJ-12 | %s |\n" % marker)
                _, regs, bad = check_c2([claim, reg])
                res[marker + "-must-flag"] = regs == 1 and len(bad) == 1
                reg = fixture("marker.md", "| ADJ-12 | %s，已作废 |\n" % marker)
                _, regs, bad = check_c2([claim, reg])
                res[marker + "-shielded-must-pass"] = regs == 0 and not bad
                reg = fixture("marker.md", "零项待裁，另有 ADJ-12 %s。\n" % marker)
                _, regs, bad = check_c2([reg])
                res[marker + "-qualified-must-pass"] = regs == 1 and not bad
    except Exception as ex:  # noqa: BLE001
        res["exception"] = "FAIL: %r" % ex
    return res


BOUNDARY = "候选发现器：每条结果须回原文核对；报 0 条不等于包内一致，C1 内容/射程型矛盾仍需人工检查。"


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    json_mode = "--json" in argv
    ap = ArgumentParser(description=__doc__, allow_abbrev=False)
    ap.add_argument("--pack", required=True)
    ap.add_argument("--repo", action="append", default=[])
    ap.add_argument("--json", action="store_true", help="stdout 输出单个 JSON 对象；诊断写 stderr")
    result = {"status": "error", "exit_code": 2, "pack": None, "files": [],
              "selftest": {}, "checks": None, "error": None, "boundary": BOUNDARY}
    try:
        a = ap.parse_args(argv)
        result["pack"] = a.pack
        repos = [os.path.abspath(r) for r in (a.repo or ["."])]
        st = result["selftest"] = selftest()
        for k, v in st.items():
            print("SELFTEST %-32s -> %s" % (k, "PASS" if v is True else v), file=sys.stderr)
        if not st or not all(v is True for v in st.values()):
            raise ValueError("SELFTEST FAILED —— 检查器不能区分「一致」与「相抵」；停止扫描")
        files = sorted(os.path.join(a.pack, f) for f in os.listdir(a.pack) if f.endswith(".md"))
        if not files:
            raise ValueError("没匹配到 md —— 那是「没能检查」，不是「干净」")
        result["files"] = files
        c1 = check_c1(files)
        claims, regs, bad = check_c2(files)
        seen, miss = check_c3(files, repos)
        result.update(status="completed", exit_code=0, checks={
            "c1": {"candidates": c1},
            "c2": {"claims": claims, "open_blocks": regs, "candidates": bad},
            "c3": {"paths": seen, "missing": miss},
        })
    except (OSError, UnicodeError, ValueError) as ex:
        result["error"] = str(ex)
        print("ERROR: " + str(ex), file=sys.stderr)

    print(BOUNDARY, file=sys.stderr)
    if json_mode:
        print(json.dumps(result, ensure_ascii=False))
    elif result["status"] == "completed":
        print_report(result)
    return result["exit_code"]


def print_report(result):
    print("\n扫描 %d 个文件：%s\n" % (len(result["files"]), result["pack"]))
    checks = result["checks"]
    c1 = checks["c1"]["candidates"]
    print("=== C1 主题极性相抵：%d 个候选 ===" % len(c1))
    for s, rows in c1:
        print("  ● 主题 %s" % s)
        for fn, ln, c, o, ck, ok, blk in rows[:4]:
            print("      %s:%d  [%s%s]  %s" % (fn, ln, "".join(ck), "".join(ok), blk.replace("\n", " ")[:110]))

    claims, regs, bad = (checks["c2"][key] for key in ("claims", "open_blocks", "candidates"))
    print("\n=== C2 计数相抵：%d 条计数声明，%d 处开项登记 ===" % (len(claims), regs))
    for c in claims:
        print("      %s  →  %s" % tuple(c))
    if bad:
        print("  ● ★ 计数声明与开项登记并存 ⇒ 候选相抵：%s" % bad)

    seen, miss = checks["c3"]["paths"], checks["c3"]["missing"]
    print("\n=== C3 引用可解析：%d 条仓内路径，%d 条不存在 ===" % (len(seen), len(miss)))
    for fn, p in miss:
        print("      ● %s 引  %s  —— 仓内不存在" % (fn, p))


if __name__ == "__main__":
    sys.exit(main())

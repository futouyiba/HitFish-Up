#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""需求文档卫生检查 —— 结构折损 + 流程标记。

用法：
    python3 check_doc_hygiene.py --prefix "某页面前缀"     # 检查标题以该前缀开头的页
    python3 check_doc_hygiene.py --prefix "..." --json
    python3 check_doc_hygiene.py --self-test               # 只跑自检，不联网

退出码：0 = 全部干净；1 = 有发现；2 = **没能真正检查**（取不到 token / 网络失败 / 一页都没匹配到）。

设计要点（这几条都是被真实事故逼出来的，别删）：
  1. **本仓是公开仓，所以脚本里不含任何内网 URL / 页面 id。** 页面前缀是运行时参数。
  2. **判「页面写坏了」要看结构，不要看某个字符序列的计数。**
     实测过：粗体区间内含代码段时，markdown 回读会出现四个连续星号，而**块级完全正常**、
     渲染也正常 —— 那是序列化假象。真正的损坏是：标题被吞、整节折成一行、
     `<table>` 与 `</table>` 不配平、单元格尖括号被转义成标签形。
  3. **本脚本自带 --self-test，默认先跑它，且自检断言的是「命中了哪条判据」而不是「命中了几类」。**
     一个「永远绿」的检查比没有检查更糟；而只断言「变红」不断言「红对理由」，
     仍会被假证明骗过去（曾经有人把语法错误注入进去，测试红了但红的理由完全不对）。
     断言判据名，才能保证**每一条判据都被单独证伪过**。
  4. **失败必须 fail-closed。** 一页都没匹配到 ≠ 干净 —— 那通常意味着前缀拼错或页面被改名。

已知局限（当启发式看，不要当判据）：
  - 流程标记里 `canonical` 只匹配「canonical 见 / canonical：/ canonical 归属」这类**指向权威**的用法；
    `Canonical output` 这类技术术语不报。中文语料里误报与漏报都可能存在，
    所以它给的是**线索清单**，最终判断仍要人看。
  - 「页内历史隔断」只认**标题**里出现历史词，正文里正常提到「旧版」不会报。
  - **围栏配平用「行首 ``` / ~~~ 的行数奇偶」判定**：若某页的**代码块内容本身**有一行以 ``` 开头
    （例如正在演示围栏写法），会算成奇数 → 报一次假的「围栏不配平」，并把该页降级为原文逐行检查
    （围栏内合法的 mermaid `<br>` 可能被一并报出）。**这个取舍是刻意保留的**：
    静默漏检远比吵一次严重，而降级的代价只是多一条线索。
  - 诊断信息（含自检 banner）一律写 **stderr**，`stdout` 只放发现；所以 `--json` 的 stdout 是纯 JSON，
    **不必再加 `--skip-self-test`**。
"""

import argparse
import json
import os
import re
import sys
import urllib.request

NOTION_VERSION = "2026-03-11"
DESKTOP_CONFIG = os.path.expanduser(
    "~/Library/Application Support/Claude-3p/claude_desktop_config.json"
)

CAT_STRUCT = "结构"
CAT_MARK = "标记"

PROCESS_MARKERS = [
    # 拉丁词一律大小写不敏感：实际写法常是全大写（Status：WORKING / NEXT）
    ("Working", re.compile(r"(?<![A-Za-z])Working(?![A-Za-z])", re.I)),
    ("pending", re.compile(r"(?<![A-Za-z])pending(?![A-Za-z])", re.I)),
    ("Open Question", re.compile(r"Open\s+Question", re.I)),
    ("待裁", re.compile(r"待裁")),
    ("待定", re.compile(r"待定")),
    ("待确认", re.compile(r"待确认")),
    # 日期可能在词前或词后（「（2026-09-17 Owner 裁决）」和「Owner 裁决 2026-09-17」都有），
    # 所以只认「Owner 裁决」本身，不强求日期位置
    ("Owner 裁决", re.compile(r"Owner\s*裁决")),
    # 指向权威的用法才算流程标记；Canonical output / CanonicalStructureType 不报
    ("canonical 指向权威", re.compile(r"[Cc]anonical\s*(见|：|归属)")),
]

# 页内历史隔断：只在**标题**里认，正文提到「旧版」不算
HISTORY_HEADING = re.compile(r"^\s*#{1,6}\s.*(Historical|Superseded|Deprecated|废弃|已废|旧版|存档)")

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def split_fences(md):
    """返回 (outside_lines, raw_lines, balanced)。

    围栏内的 `<br>` 是合法写法（mermaid 用它换行），不能当折损。
    **围栏数不配平时返回 balanced=False** —— 那时剥离结果不可信，调用方必须改用 raw，
    否则一处错位会把该点之后的整页当成围栏内内容跳过，行级判据全部失效且不报异常。
    """
    raw = md.split("\n")
    fences = sum(1 for line in raw if FENCE_RE.match(line))
    balanced = fences % 2 == 0
    if not balanced:
        return list(raw), raw, False
    out, infence = [], False
    for line in raw:
        if FENCE_RE.match(line):
            infence = not infence
            out.append("")
            continue
        out.append("" if infence else line)
    return out, raw, True


def check_page(md):
    """返回 findings：每条是 (类别, 判据名, 行号, 摘录)。

    判据名要唯一到「一条判据一个名字」——自检就是按它做证伪的。
    """
    findings = []
    outside, raw, balanced = split_fences(md)

    # 1) 围栏配平
    if not balanced:
        findings.append((CAT_STRUCT, "围栏不配平", 0,
                         "围栏（``` / ~~~）数量为奇数；已降级用原文逐行检查，但结构需人工确认"))

    # 2) 表标签配平（用剥离后的视图：围栏里的 <table> 是示例文本，不算表格结构）
    n_open = sum(l.count("<table") for l in outside)
    n_close = sum(l.count("</table>") for l in outside)
    if n_open != n_close:
        findings.append((CAT_STRUCT, "表标签不配平", 0,
                         "<table> %d / </table> %d" % (n_open, n_close)))

    for i, line in enumerate(outside, 1):
        # 3) 标题被吞：标题行里混进了折行或表格
        if re.match(r"^#{1,6}\s", line) and ("<br>" in line or "<table" in line):
            findings.append((CAT_STRUCT, "标题被吞", i,
                             "标题行里混进 <br>/<table>：%s" % line[:70]))
        # 4) 非代码块内的折行
        if "<br>" in line:
            findings.append((CAT_STRUCT, "代码块外折行", i, line[:70]))
        # 5) 尖括号转义 —— 只认「标签形」：\<td\> / \</td\> / \<table\>
        #    正文里的比较运算符转义（如「0 \< 阈值」）是**合法用法**，不报。
        if re.search(r"\\</?[A-Za-z]", line):
            findings.append((CAT_STRUCT, "标签形转义", i, line[:70]))
        # 6) 页内历史隔断：只在标题里认
        if HISTORY_HEADING.match(line):
            findings.append((CAT_MARK, "页内历史隔断", i, line[:70]))
        # 7) 流程标记
        for label, pat in PROCESS_MARKERS:
            if pat.search(line):
                findings.append((CAT_MARK, "流程标记：" + label, i, line[:70]))
    return findings


# ── 判据清单（自检与真实检查共用同一份真相） ────────────────────────────────

JUDGEMENTS = [
    "围栏不配平", "表标签不配平", "标题被吞", "代码块外折行", "标签形转义",
    "页内历史隔断",
] + ["流程标记：" + label for label, _ in PROCESS_MARKERS]


def token():
    """取凭据。**取不到时抛异常，不要 sys.exit** —— 否则退出码会是 1（＝「有发现」），
    而真相是一个字都没读。调用方统一把它归到退出码 2（「没能检查」）。"""
    t = os.environ.get("NOTION_TOKEN")
    if t:
        return t.strip()
    try:
        with open(DESKTOP_CONFIG) as f:
            return json.load(f)["mcpServers"]["notionApi"]["env"]["NOTION_TOKEN"].strip()
    except Exception as e:
        raise RuntimeError("取不到 token（设 NOTION_TOKEN，或确认本机 Claude 配置可读）：%s" % e)


def api(path, tok, body=None, method="GET"):
    req = urllib.request.Request(
        "https://api.notion.com/v1" + path,
        data=json.dumps(body).encode() if body else None,
        headers={
            "Authorization": "Bearer " + tok,
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        method=method,
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def title_of(page):
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(s.get("plain_text", "") for s in prop.get("title", []))
    return ""


def pages_with_prefix(tok, prefix):
    found, cursor = [], None
    while True:
        body = {"query": prefix, "page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        res = api("/search", tok, body, "POST")
        for p in res["results"]:
            if p.get("object") == "page" and title_of(p).startswith(prefix):
                found.append((p["id"].replace("-", ""), title_of(p)))
        if not res.get("has_more"):
            return found
        cursor = res.get("next_cursor")


# ── 自检：证明每一条判据都能被单独证伪 ──────────────────────────────────────

# (描述, 样本, 期望命中的**判据名**集合)
SELF_TEST_CASES = [
    # —— 好样本：都不该报 ——
    ("干净样本", "## 1. 标题\n正文 `code` 与 **粗体**。\n<table><tr><td>x</td></tr></table>\n", set()),
    ("技术术语不报：Canonical output", "## 1. 标题\nCanonical output = Foo。\n", set()),
    ("mermaid 内的 <br> 不报", "## 1. 标题\n```mermaid\nA[\"x<br>y\"] --> B\n```\n", set()),
    ("合法转义：比较运算符不报", "## 1. 标题\n水温 = 0 \\< 阈值 0.05；排序 CG-01 \\> CG-02。\n", set()),
    ("正文提到旧版但标题干净：不报", "## 1. 标题\n这段说明旧版行为已废弃。\n", set()),
    # —— 坏样本：每条判据单独一条，互不搭车 ——
    ("围栏不配平", "## 1. 标题\n```\n未闭合\n", {"围栏不配平"}),
    ("表标签不配平", "## 1. 标题\n<table><tr><td>x</td></tr>\n", {"表标签不配平"}),
    ("标题被吞（仅表格）", "## 1. 标题<table>\n</table>\n", {"标题被吞"}),
    ("标题被吞（仅折行）", "## 1. 标题<br>正文\n", {"标题被吞", "代码块外折行"}),
    ("代码块外折行（非标题行）", "## 1. 标题\n正文<br>续行\n", {"代码块外折行"}),
    ("标签形转义", "## 1. 标题\n正文 \\<td\\>x\\</td\\>\n", {"标签形转义"}),
    ("页内历史隔断", "## Historical｜旧版存档\n正文\n", {"页内历史隔断"}),
    ("流程标记 Working", "## 1. 标题\n**Status：WORKING / NEXT。**\n", {"流程标记：Working"}),
    ("流程标记 pending", "## 1. 标题\n状态 Pending 中。\n", {"流程标记：pending"}),
    ("流程标记 Open Question", "## 1. 标题\nOpen Question：这条怎么定？\n", {"流程标记：Open Question"}),
    ("流程标记 待裁", "## 1. 标题\n这条待裁。\n", {"流程标记：待裁"}),
    ("流程标记 待定", "## 1. 标题\n口径待定。\n", {"流程标记：待定"}),
    ("流程标记 待确认", "## 1. 标题\n数据待确认。\n", {"流程标记：待确认"}),
    ("流程标记 Owner 裁决", "## 1. 标题\n（2026-09-17 Owner 裁决）\n", {"流程标记：Owner 裁决"}),
    ("流程标记 canonical 见", "## 1. 标题\ncanonical 见开发需求 §3.3。\n", {"流程标记：canonical 指向权威"}),
]


def self_test(verbose=True, stream=None):
    stream = stream or sys.stdout
    failures = []
    for desc, sample, want in SELF_TEST_CASES:
        got = {j for _, j, _, _ in check_page(sample)}
        if got != want:
            failures.append((desc, sorted(want), sorted(got)))
        if verbose:
            print("  %-32s 期望 %-28s 实得 %s"
                  % (desc, ",".join(sorted(want)) or "（无）", ",".join(sorted(got)) or "（无）"), file=stream)
    # 覆盖面断言：每条判据都必须有至少一个「只命中它」的样本
    covered = {j for _, _, want in SELF_TEST_CASES for j in want}
    uncovered = [j for j in JUDGEMENTS if j not in covered]
    if uncovered:
        failures.append(("判据无单独样本", "全部判据都要被覆盖", "未覆盖：%s" % uncovered))
    if failures:
        print("\n❌ 自检未通过：", file=stream)
        for d, w, g in failures:
            print("   %s：期望 %s，实得 %s" % (d, w, g), file=stream)
        return 1
    print("\n✅ 自检通过：%d 个坏样本按**判据名**逐条命中，%d 个好样本未报，%d 条判据全部被覆盖。"
          % (sum(1 for _, _, w in SELF_TEST_CASES if w),
             sum(1 for _, _, w in SELF_TEST_CASES if not w),
             len(JUDGEMENTS)), file=stream)
    return 0


# ── 主流程 ──────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="需求文档卫生检查（结构折损 + 流程标记）")
    ap.add_argument("--prefix", help="只检查标题以此开头的页面")
    ap.add_argument("--self-test", action="store_true", help="只跑自检，不联网")
    ap.add_argument("--skip-self-test", action="store_true", help="跳过自检直接检查")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    # 默认先自检：证明这个检查真的会红，再拿它判别人
    if not args.skip_self_test:
        if self_test(verbose=False, stream=sys.stderr):
            # 诊断信息一律走 stderr：否则 --json 的 stdout 就不是纯 JSON 了
            print("自检未通过，拒绝执行检查（一个不会红的检查没有意义）。", file=sys.stderr)
            return 2
        print("自检通过，继续。\n", file=sys.stderr)

    if not args.prefix:
        ap.error("需要 --prefix（本仓是公开仓，不把内网页面前缀写进脚本）")

    try:
        tok = token()
        pages = pages_with_prefix(tok, args.prefix)
    except Exception as e:
        print("检查未能执行（凭据 / 网络 / API 失败）：%s" % e)
        return 2

    # **一页都没匹配到不是「干净」**：通常是前缀拼错或页面被改名。fail-closed。
    if not pages:
        print("检查未能执行：没有标题以 %r 开头的页面。"
              "（前缀拼错、或页面被改名/移出可见范围都会这样。这**不是**「全部干净」。）" % args.prefix)
        return 2

    report, total = [], 0
    for pid, title in sorted(pages, key=lambda x: x[1]):
        # 逐页读取失败也归到「没能检查」（退出码 2）：漏读一页就不是一次完整的检查，
        # 而默认的未捕获异常退出码是 1，会被读成「有发现」——那会让下游去没读到的页上找并不存在的违规。
        try:
            md = json.load(urllib.request.urlopen(urllib.request.Request(
                "https://api.notion.com/v1/pages/%s/markdown?include_transcript=false" % pid,
                headers={"Authorization": "Bearer " + tok, "Notion-Version": NOTION_VERSION},
            ), timeout=120))["markdown"]
        except Exception as e:
            print("检查未能执行：读取页面失败（%s）：%s" % (title, e))
            return 2
        f = check_page(md)
        total += len(f)
        report.append({"title": title, "findings": f})
        if not args.json:
            flag = "  " if not f else "⚠ "
            print("%s%s  —— %d 处" % (flag, title, len(f)))
            for cat, judge, ln, msg in f:
                print("      [%s] L%d %s：%s" % (cat, ln, judge, msg))

    if args.json:
        print(json.dumps({"pages": report, "total": total}, ensure_ascii=False, indent=2))
    else:
        print("\n合计 %d 处（已检查 %d 页）。" % (total, len(pages)))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

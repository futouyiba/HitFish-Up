#!/usr/bin/env python3
"""FCF 总图 · 大块拓扑对齐草图 v1 (alignment sketch, throwaway).

NOT the canonical map: discussion artifact for aligning the top-level
module topology. v1 changes per alignment round 1:

  * ③ 玩家策略与操作数据 occupies its own vertical band between ② and ④
    (right-offset horizontally only);
  * data vs process distinct styles: parallelogram = 配置/数据,
    cube = 派生数据(环境场, per directive), rounded rect = 过程/模块,
    gray dashed = 范围外;
  * 派生环境场 sits directly below 烘焙 (slightly right), styled as a cube;
  * D.B(钓场投鱼配置) → D.A / D.C edges carry query semantics instead of
    "纽带": 钓场ID+时段/天气常量表 查询环境上下文; 习性ID(Engagement Mode)
    查询 fish env affinity(= 鱼的习性配置记录);
  * each module row is a top-level collapse unit — click the row label to
    fold/unfold; folded rows hide their member blocks AND every edge
    touching them (arrow removal). 范围外 is not collapsible.

Deterministic; regenerate: python3 align_topology.py
"""

from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 1560, 1420

GRAY_FILL, GRAY_STROKE, GRAY_FONT = "#f5f5f5", "#a6a6a6", "#8f8f8f"

# id, kind(data|process|cube|ghost), label, caption, x, y, w, h
BLOCKS = [
    # ① 数据 (top row) — parallelogram data style
    ("D.A", "data", "环境上下文", "", 100, 100, 300, 100),
    ("D.B", "data", "钓场投鱼配置", "", 480, 100, 330, 100),
    ("D.C", "data", "鱼的习性配置", "", 890, 100, 300, 100),
    # ② 烘焙 (process) → 派生环境场 (cube data, below bake, slightly right)
    ("BAKE", "process", "烘焙", "", 240, 290, 340, 90),
    ("FIELD", "cube", "派生环境场", "derived environment field", 340, 430, 320, 100),
    # ③ 玩家策略与操作数据 — own band, right-offset; data + derived cue data
    ("PLAYER", "data", "玩家策略与操作数据", "钓具 / 钓组 · 姿态", 1100, 520, 360, 100),
    ("CUE", "data", "Cue 吸引元素", "", 1150, 660, 280, 70),
    # ④ 响应 (process)
    ("RESP", "process", "响应模块", "(适配系数 — 逻辑暂不展开)", 640, 770, 320, 90),
    # ⑤ 圆桌抽鱼 (process container + 4 sub-blocks)
    ("TABLE", "process", "圆桌抽鱼", "", 440, 930, 760, 45),
    ("T1", "process", "品质抽取调整", "Engagement Mode", 460, 990, 170, 90),
    ("T2", "process", "圆桌权重表 Building", "组件", 645, 990, 170, 90),
    ("T3", "process", "硬保底", "", 830, 990, 160, 90),
    ("T4", "process", "动态权重调整", "", 1005, 990, 175, 90),
    # ⑥ 抽鱼和生成 (process; short extension of ⑤)
    ("DRAW", "process", "抽鱼和生成", "鱼种 · 品质 · 大小 · 重量 | fish condition 透传",
     560, 1180, 480, 100),
    # 范围外 (ghost, NOT collapsible)
    ("FISHAI", "ghost", "运行 Fish AI(刺鱼 / 博鱼)", "超出中鱼范畴 · 最简略,无折叠",
     640, 1330, 340, 70),
]

# from, to, label, style-key
EDGES = [
    ("D.B", "D.A", "钓场ID + 时段/天气 常量表(外部驱动)→ 查询", "QUERY"),
    ("D.B", "D.C", "习性ID(Engagement Mode)→ 查询 fish env affinity(= 习性配置记录)", "QUERY"),
    ("D.A", "BAKE", "", "FEED"),
    ("D.B", "BAKE", "", "FEED"),
    ("D.C", "BAKE", "", "FEED"),
    ("BAKE", "FIELD", "", "FLOW"),
    ("PLAYER", "CUE", "", "FLOW"),
    ("FIELD", "RESP", "", "FLOW"),
    ("CUE", "RESP", "", "FLOW"),
    ("RESP", "TABLE", "", "FLOW"),
    ("TABLE", "DRAW", "", "FLOW"),
    ("DRAW", "FISHAI", "", "GHOST"),
]

# top-level collapse units: row label, label y, member block ids
ROWS = [
    ("R1", "① 数据", 70, ["D.A", "D.B", "D.C"]),
    ("R2", "② 烘焙", 270, ["BAKE", "FIELD"]),
    ("R3", "③ 玩家策略与操作数据", 480, ["PLAYER", "CUE"]),
    ("R4", "④ 响应", 750, ["RESP"]),
    ("R5", "⑤ 圆桌抽鱼", 910, ["TABLE", "T1", "T2", "T3", "T4"]),
    ("R6", "⑥ 抽鱼和生成(⑤ 的短延伸)", 1160, ["DRAW"]),
]
NON_COLLAPSIBLE_LABEL = ("范围外", 1310)

SEPARATORS = [250, 480, 730, 910, 1150, 1300]

LEGEND = [
    ("data", "数据 / 配置"),
    ("cube", "派生数据(环境场)"),
    ("process", "过程 / 模块"),
    ("ghost", "范围外"),
]

KIND_STYLE = {
    "data": ("shape=parallelogram;perimeter=parallelogramPerimeter;size=16;", "#dae8fc", "#6c8ebf"),
    "cube": ("shape=cube;size=18;", "#dae8fc", "#6c8ebf"),
    "process": ("rounded=1;", "#ffe6cc", "#d79b00"),
    "ghost": ("rounded=1;dashed=1;", GRAY_FILL, GRAY_STROKE),
}

EDGE_STYLES = {
    "QUERY": "endArrow=open;dashed=1;dashPattern=1 3;strokeColor=#7f8fa6;strokeWidth=1.5;"
             "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=10;fontColor=#555555;",
    "FEED": "endArrow=block;dashed=1;strokeColor=#d79b00;strokeWidth=1.5;"
            "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;",
    "FLOW": "endArrow=block;strokeColor=#666666;strokeWidth=2;"
            "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;",
    "GHOST": "endArrow=block;dashed=1;strokeColor=#a6a6a6;strokeWidth=1.5;"
             "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;",
}


def xesc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def label_html(label, caption):
    if not caption:
        return label
    return "%s<br><font style='font-size:9px;color:#555555'>%s</font>" % (label, caption)


def action_link(payload):
    return "data:action/json," + json.dumps(payload, separators=(",", ":"))


def row_fold_cells(members, edges):
    """Member blocks + every edge touching a member (arrow removal on fold)."""
    memberset = set(members)
    cells = list(members)
    for i, (src, tgt, _, _) in enumerate(edges):
        if src in memberset or tgt in memberset:
            cells.append("E%d" % i)
    return cells


def main():
    by_id = {b[0]: b for b in BLOCKS}
    out = []
    a = out.append
    a('<?xml version="1.0" encoding="UTF-8"?>\n')
    a('<mxfile host="fcf-align-sketch" agent="align_topology.py" version="26.0.0" type="device">\n')
    a('  <diagram id="fcf-align-topology-v1" name="FCF 总图拓扑对齐 v1">\n')
    a('    <mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" '
      'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" '
      'pageHeight="%d" math="0" shadow="0">\n' % (PAGE_W, PAGE_H))
    a('      <root>\n')
    a('        <mxCell id="0" />\n')
    a('        <mxCell id="1" parent="0" />\n')

    a('        <mxCell id="TITLE" value="FCF 总图 · 大块拓扑对齐草图 v1 — 只对齐结构(非 canonical;对齐后落回 fcf-system-map 重画)" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=14;fontStyle=1;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="14" width="860" height="30" as="geometry" />\n        </mxCell>\n')
    a('        <mxCell id="HINT" value="点击各行 ①..⑥ 行标 = 折叠 / 展开该行:行内块与所连箭头一起隐藏(范围外不可折叠)" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#666666;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="42" width="640" height="22" as="geometry" />\n        </mxCell>\n')

    # legend (top right)
    lx = 1180
    for i, (kind, text) in enumerate(LEGEND):
        y = 16 + i * 34
        base, fill, stroke = KIND_STYLE[kind]
        style = base + ("fontSize=10;fillColor=%s;strokeColor=%s;fontColor=#333333;" % (fill, stroke))
        if kind == "ghost":
            style += "dashed=1;"
        a('        <mxCell id="LEG%d" value="%s" style="%s" vertex="1" parent="1">\n'
          % (i, xesc(text), xesc(style)) +
          '            <mxGeometry x="%d" y="%d" width="150" height="28" as="geometry" />\n'
          % (lx, y) + '        </mxCell>\n')

    for y in SEPARATORS:
        a('        <mxCell id="SEP%d" style="endArrow=none;strokeColor=#e0e0e0;dashed=1;" '
          'edge="1" parent="1">\n' % y +
          '            <mxGeometry relative="1" as="geometry">\n'
          '                <mxPoint x="40" y="%d" as="sourcePoint" />\n' % y +
          '                <mxPoint x="%d" y="%d" as="targetPoint" />\n' % (PAGE_W - 40, y) +
          '            </mxGeometry>\n        </mxCell>\n')

    # row labels = collapse toggles (UserObject + custom action)
    for rid, text, y, members in ROWS:
        cells = row_fold_cells(members, EDGES)
        link = action_link({"actions": [{"toggle": {"cells": cells}}]})
        a('        <UserObject label="%s" link="%s" id="%s">\n'
          % (xesc(text + "  ⇕"), xesc(link), xesc("RL:" + rid)) +
          '          <mxCell style="text;html=1;align=left;verticalAlign=middle;fontSize=12;'
          'fontStyle=1;fontColor=#4477aa;" vertex="1" parent="1">\n'
          '            <mxGeometry x="40" y="%d" width="330" height="24" as="geometry" />\n' % y +
          '          </mxCell>\n        </UserObject>\n')
    name, y = NON_COLLAPSIBLE_LABEL
    a('        <mxCell id="RL:NONE" value="%s" style="text;html=1;align=left;verticalAlign=middle;'
      'fontSize=12;fontStyle=1;fontColor=#999999;" vertex="1" parent="1">\n' % xesc(name) +
      '            <mxGeometry x="40" y="%d" width="200" height="24" as="geometry" />\n' % y +
      '        </mxCell>\n')

    for bid, kind, label, caption, x, y, w, h in BLOCKS:
        base, fill, stroke = KIND_STYLE[kind]
        style = base + ("fontSize=12;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
                        % (fill, stroke))
        if kind == "ghost":
            style += "fontColor=%s;" % GRAY_FONT
        if bid == "TABLE":
            style += "verticalAlign=top;align=center;spacingTop=2;fontStyle=1;"
        a('        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">\n'
          % (xesc(bid), xesc(label_html(label, caption)), xesc(style)) +
          '            <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" />\n'
          % (x, y, w, h) +
          '        </mxCell>\n')

    for i, (src, tgt, lab, kind) in enumerate(EDGES):
        exit_hint = entry_hint = ""
        if (src, tgt) == ("FIELD", "RESP"):
            exit_hint = "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
        elif (src, tgt) == ("CUE", "RESP"):
            exit_hint = "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
        a('        <mxCell id="E%d" value="%s" style="%s%s" edge="1" parent="1" source="%s" target="%s">\n'
          % (i, xesc(lab), xesc(EDGE_STYLES[kind]), xesc(exit_hint), xesc(src), xesc(tgt)) +
          '            <mxGeometry relative="1" as="geometry" />\n'
          '        </mxCell>\n')

    a('      </root>\n')
    a('    </mxGraphModel>\n')
    a('  </diagram>\n')
    a('</mxfile>\n')
    path = HERE / "align-topology-v1.drawio"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(out))
    print("wrote %s (%d blocks, %d edges, %d collapsible rows)" % (path, len(BLOCKS), len(EDGES), len(ROWS)))


if __name__ == "__main__":
    main()

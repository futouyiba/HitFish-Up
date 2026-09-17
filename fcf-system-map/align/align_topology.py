#!/usr/bin/env python3
"""FCF 总图 · 中层框架对齐草图 v2 (alignment sketch, throwaway).

NOT the canonical map. Aligned to the Notion authority
「中鱼机制 0.3.4｜逻辑框架升级（中间对齐骨架）」§2.1–§2.3 + §4.0–§4.7.

v2 corrections over v1 (v1 had two semantic errors, exposed by reading the
authority rather than by re-testing draw.io):

  * v1 drew 派生环境场 --FLOW--> 响应模块.  WRONG. Authority §2.2 / §3.1.2:
    Response does NOT consume the final EnvironmentWeight.  Env side and fish
    side are two parallel branches that merge ONCE, at 4.5.  The only DEF->4.4
    edge is dotted and carries 「必要关系事实 / Anchor」 only.
  * v1 was missing 4.0 场景投鱼表读取, 4.1 Engagement Mode Routing, and the
    Runtime Exposure / Environment Assembly step.

v2 shows TWO partitions of the same chain side by side:
  * left column  = 第一性原理的四道(五道)语义边界 — Gameplay 因果
  * center/right = 0.3.4 的工程实现 (模块 4.0–4.7 与它们之间的数据 Contract)
That they partition differently is the point: 语义边界 != 工程实现边界.

Deterministic; regenerate: python3 align_topology.py
"""

from __future__ import annotations
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 1440, 1580

GRAY_FILL, GRAY_STROKE, GRAY_FONT = "#f5f5f5", "#a6a6a6", "#8f8f8f"

KIND_STYLE = {
    "config":  ("shape=parallelogram;perimeter=parallelogramPerimeter;size=16;", "#ffe6cc", "#d79b00"),
    "data":    ("shape=parallelogram;perimeter=parallelogramPerimeter;size=16;", "#dae8fc", "#6c8ebf"),
    "cube":    ("shape=cube;size=18;", "#dae8fc", "#6c8ebf"),
    "process": ("rounded=1;", "#ffe6cc", "#d79b00"),
    "ghost":   ("rounded=1;dashed=1;", GRAY_FILL, GRAY_STROKE),
}

# block id, kind, label, caption, x, y, w, h
BLOCKS = [
    # ---- 输入:配置 / 事实 -------------------------------------------------
    ("IN.STOCK",   "config", "钓场投鱼配置", "FishStock：鱼种 × 品质 投放项", 140, 80, 300, 84),
    ("IN.ENV",     "data",   "世界与环境事实", "季节 · 水温 · 时段 · 天气史 · 地形 · 结构", 500, 80, 300, 84),
    ("IN.SPECIES", "config", "鱼的习性配置", "Species / FishQuality / EngagementMode", 900, 80, 320, 84),

    # ---- 4.0 – 4.2 慢计算 -------------------------------------------------
    ("M40", "process", "4.0 场景投鱼表读取", "候选初始化 + 基础权重", 500, 220, 300, 84),
    ("M41", "process", "4.1 Engagement Mode Routing", "Mode 身份 + EngagementModeShare", 500, 350, 300, 84),
    ("M42", "process", "4.2 DEF 烘焙 / 慢计算", "环境侧与鱼侧共用规则基础设施，语义分离", 500, 480, 300, 84),
    ("E42", "cube", "环境侧 Artifact", "Presence · SpatialSuitability · baked Exposure", 900, 430, 320, 88),
    ("C42", "cube", "Fish Condition 快照", "Activity · FeedingMotivation · FeedingPreferenceProfile", 900, 560, 320, 88),

    # ---- 4.3 呈现解析 ------------------------------------------------------
    ("IN.PLAYER", "data", "玩家操作 + 饵", "姿态颗粒 · 饵静态属性", 140, 700, 300, 84),
    ("M43", "process", "4.3 姿态与饵刺激解析", "玩家与饵 → 标准刺激通道", 500, 700, 300, 84),
    ("D43", "data", "Presentation Signals", "速度 · 动作 · 声音 · 震动 · 光 · 轮廓 · 气味", 900, 700, 320, 84),

    # ---- ④ 环境暴露组装 / 鱼响应(两条并行支路,只在 4.5 汇合) --------------
    ("A44", "process", "Runtime 暴露 / 环境组装", "EXPOSURE / ACCESS 结算点", 900, 850, 320, 84),
    ("EW",  "cube", "EnvironmentWeight", "环境侧最终量", 900, 975, 280, 80),
    ("M44", "process", "4.4 Meaning / Response Resolver", "MEANING + RESPONSE 结算点", 900, 1120, 320, 84),
    ("R44", "data", "Response Result", "Meaning / ResponseGrade / ResponseWeight", 900, 1245, 320, 84),

    # ---- ⑤ 聚合与抽鱼 ------------------------------------------------------
    ("M45", "process", "4.5 SelectionWeight 聚合", "Env × Response — 只汇合一次", 500, 1160, 300, 84),
    ("D45", "data", "Selection Pool", "SelectionWeight[] + NONE", 140, 1160, 300, 84),

    # ---- ⑥ 生成 ------------------------------------------------------------
    ("M46",    "ghost", "4.6 圆桌抽奖 / 4.7 生成交接", "复用既有底盘；本版不动随机内核", 500, 1330, 300, 84),
    ("FISHAI", "ghost", "Fish AI / 下游玩法", "中鱼统计系统到此结束", 500, 1460, 300, 74),
]

# from, to, label, style-key
EDGES = [
    ("IN.STOCK", "M40", "", "FEED"),
    ("IN.ENV", "M42", "", "FEED"),
    ("IN.SPECIES", "M41", "", "FEED"),

    ("M40", "M41", "品质基础候选", "FLOW"),
    ("M41", "M42", "品质 × 习性模式组合候选", "FLOW"),
    ("M42", "E42", "", "FLOW"),
    ("M42", "C42", "", "FLOW"),

    ("IN.PLAYER", "M43", "", "FLOW"),
    ("M43", "D43", "", "FLOW"),
    ("D43", "A44", "", "FLOW"),
    ("E42", "A44", "", "FLOW"),
    ("A44", "EW", "", "FLOW"),

    ("D43", "M44", "呈现", "FLOW"),
    ("C42", "M44", "鱼侧动态参数", "FLOW"),
    ("E42", "M44", "必要关系事实 / Anchor — 不是最终 EnvironmentWeight", "ANCHOR"),
    ("M44", "R44", "", "FLOW"),

    ("EW", "M45", "", "FLOW"),
    ("R44", "M45", "", "FLOW"),
    ("M45", "D45", "", "FLOW"),
    ("D45", "M46", "", "FLOW"),
    ("M46", "FISHAI", "", "GHOST"),
]

# 第一性原理:四道(五道)语义边界 —— 左栏,独立于工程模块切分
SEAMS = [
    ("SEAM1", "① Presence / Spatial", "鱼在哪里？这里有多少有效机会？", 40, 400, "#4a6fa5"),
    ("SEAM2", "② Exposure / Access", "当前呈现够不够得到这些鱼？", 40, 820, "#5b8c5a"),
    ("SEAM3", "③ Meaning", "鱼把呈现理解成什么？", 40, 1060, "#b58b2f"),
    ("SEAM4", "④ Response", "已感知后愿不愿开始互动？", 40, 1240, "#a5563f"),
    ("SEAM5", "⑤ Selection", "这些机会里抽中谁？", 40, 1400, "#7a5c8f"),
]

# 工程分层背景带
LAYERS = [
    ("LAY.SLOW", "① 预计算 / 慢计算", 200, 400, "#fdf6ec"),
    ("LAY.RT",   "② 实时 Runtime",   660, 700, "#eef7ee"),
    ("LAY.SEL",  "③ Selection / 服务端", 1140, 260, "#f3eefa"),
]

EDGE_STYLES = {
    "FEED": "endArrow=block;dashed=1;strokeColor=#d79b00;strokeWidth=1.5;"
            "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;",
    "FLOW": "endArrow=block;strokeColor=#666666;strokeWidth=2;"
            "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=10;fontColor=#555555;",
    "ANCHOR": "endArrow=open;dashed=1;dashPattern=1 3;strokeColor=#b03a2e;strokeWidth=1.5;"
              "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=10;fontColor=#b03a2e;",
    "GHOST": "endArrow=block;dashed=1;strokeColor=#a6a6a6;strokeWidth=1.5;"
             "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;",
}

LEGEND = [
    ("config", "配置 / 权威(可编辑)"),
    ("data", "事实 / 数据"),
    ("cube", "派生数据产物(Artifact)"),
    ("process", "过程 / 计算模块"),
    ("ghost", "复用既有底盘 / 范围外"),
]

# 逐边路由提示(纯视觉;确保两条支路在 4.5 汇合而不穿过彼此)
HINTS = {
    ("IN.STOCK", "M40"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("IN.ENV", "M42"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("IN.SPECIES", "M41"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;",
    ("M40", "M41"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("M41", "M42"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("M42", "E42"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("M42", "C42"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("IN.PLAYER", "M43"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("M43", "D43"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("D43", "A44"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("E42", "A44"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("A44", "EW"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("D43", "M44"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.25;entryDx=0;entryDy=0;",
    ("C42", "M44"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("E42", "M44"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("M44", "R44"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("EW", "M45"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.25;entryDx=0;entryDy=0;",
    ("R44", "M45"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.75;entryDx=0;entryDy=0;",
    ("M45", "D45"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;",
    ("D45", "M46"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("M46", "FISHAI"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
}


def xesc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def label_html(label, caption):
    if not caption:
        return label
    return "%s<br><font style='font-size:9px;color:#555555'>%s</font>" % (label, caption)


def main():
    out = []
    a = out.append
    a('<?xml version="1.0" encoding="UTF-8"?>\n')
    a('<mxfile host="fcf-align-sketch" agent="align_topology.py" version="26.0.0" type="device">\n')
    a('  <diagram id="fcf-align-midlevel-v2" name="FCF 中层框架对齐 v2">\n')
    a('    <mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" '
      'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" '
      'pageHeight="%d" math="0" shadow="0">\n' % (PAGE_W, PAGE_H))
    a('      <root>\n')
    a('        <mxCell id="0" />\n')
    a('        <mxCell id="1" parent="0" />\n')

    # 工程分层背景带(最底层)
    for lid, lname, ly, lh, lfill in LAYERS:
        a('        <mxCell id="%s" value="%s" style="rounded=0;dashed=1;dashPattern=8 8;'
          'fillColor=%s;strokeColor=#dddddd;verticalAlign=top;align=left;spacingLeft=8;'
          'spacingTop=4;fontSize=11;fontColor=#999999;" vertex="1" parent="1">\n'
          % (xesc(lid), xesc(lname), xesc(lfill)) +
          '            <mxGeometry x="270" y="%d" width="%d" height="%d" as="geometry" />\n'
          % (ly, PAGE_W - 300, lh) + '        </mxCell>\n')

    a('        <mxCell id="TITLE" value="FCF 总图 · 中层框架对齐草图 v2 — 对齐 Notion Authority《中鱼机制 0.3.4｜逻辑框架升级（中间对齐骨架）》§2.2 模块 Contract + §2.1.1 语义边界" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=14;fontStyle=1;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="16" width="1100" height="28" as="geometry" />\n        </mxCell>\n')
    a('        <mxCell id="HINT" value="左栏 = 第一性原理的四道判断(语义边界),它切分这条链的方式与工程模块不同; 红色虚线 = 环境侧只向 Response 传「必要关系事实」,最终 EnvironmentWeight 不进入 Response —— 两条支路只在 4.5 汇合一次。" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#666666;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="42" width="1180" height="28" as="geometry" />\n        </mxCell>\n')

    # 语义边界(左栏)
    for sid, sname, sq, sx, sy, scol in SEAMS:
        a('        <mxCell id="%s" value="%s&#10;%s" style="rounded=1;dashed=1;'
          'fillColor=none;strokeColor=%s;strokeWidth=2;verticalAlign=middle;align=center;'
          'fontSize=11;fontColor=%s;fontStyle=1;" vertex="1" parent="1">\n'
          % (xesc(sid), xesc(sname), xesc(sq), xesc(scol), xesc(scol)) +
          '            <mxGeometry x="%d" y="%d" width="196" height="100" as="geometry" />\n'
          % (sx, sy) + '        </mxCell>\n')

    # 图例(左中部空白区)
    for i, (kind, text) in enumerate(LEGEND):
        base, fill, stroke = KIND_STYLE[kind]
        style = base + ("fontSize=10;fillColor=%s;strokeColor=%s;fontColor=#333333;" % (fill, stroke))
        if kind == "ghost":
            style += "dashed=1;"
        a('        <mxCell id="LEG%d" value="%s" style="%s" vertex="1" parent="1">\n'
          % (i, xesc(text), xesc(style)) +
          '            <mxGeometry x="40" y="%d" width="196" height="30" as="geometry" />\n'
          % (170 + i * 38) + '        </mxCell>\n')

    # 模块 / 数据
    for bid, kind, label, caption, x, y, w, h in BLOCKS:
        base, fill, stroke = KIND_STYLE[kind]
        style = base + ("fontSize=12;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
                        % (fill, stroke))
        if kind == "ghost":
            style += "fontColor=%s;" % GRAY_FONT
        a('        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">\n'
          % (xesc(bid), xesc(label_html(label, caption)), xesc(style)) +
          '            <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" />\n'
          % (x, y, w, h) + '        </mxCell>\n')

    for i, (src, tgt, lab, kind) in enumerate(EDGES):
        hint = HINTS.get((src, tgt), "")
        a('        <mxCell id="E%d" value="%s" style="%s%s" edge="1" parent="1" source="%s" target="%s">\n'
          % (i, xesc(lab), xesc(EDGE_STYLES[kind]), xesc(hint), xesc(src), xesc(tgt)) +
          '            <mxGeometry relative="1" as="geometry" />\n'
          '        </mxCell>\n')

    a('      </root>\n')
    a('    </mxGraphModel>\n')
    a('  </diagram>\n')
    a('</mxfile>\n')
    path = HERE / "align-midlevel-v2.drawio"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(out))
    print("wrote %s (%d blocks, %d edges, %d seams, %d layers)"
          % (path, len(BLOCKS), len(EDGES), len(SEAMS), len(LAYERS)))


if __name__ == "__main__":
    main()

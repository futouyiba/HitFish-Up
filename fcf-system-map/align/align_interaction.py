#!/usr/bin/env python3
"""FCF 总图 · 压缩阶梯 × Interaction 下钻 对齐草图 v4 (throwaway).

Two panels, per the agreed framing:

  A. 压缩阶梯 (compression ladder) — 中鱼升级 is the substrate; each lower
     level is a *projection* with strictly smaller scope. FCF v1 is compression
     1 (not read this round), Simplified V0 compression 2, 0.3.4 smaller again,
     0.3.4.0-B the current-version projection.

  B. Interaction 内部拓扑 + 四层分离 + operator admission — the drill-down
     where player-strategy differences are actually produced.

Authorities read this round:
  * 中鱼升级｜Mechanism Topology V2：Spatial × Response 深入下钻 (v2)
  * 中鱼升级｜Behavioral Regime × Largemouth Bass：Spatial–Response 中层逻辑样板 (v8)
  * 中鱼0.3.4.0-B｜开发需求 R0 / 固定模板分层烘焙 / Authoring & Resolve Contract R0

Deterministic; regenerate: python3 align_interaction.py
"""

from __future__ import annotations
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 1680, 1620

GRAY_FILL, GRAY_STROKE, GRAY_FONT = "#f5f5f5", "#a6a6a6", "#8f8f8f"

KIND_STYLE = {
    "ladder":  ("rounded=1;", "#dae8fc", "#6c8ebf"),
    "ladderB": ("rounded=1;strokeWidth=3;", "#fff2cc", "#d79b00"),
    "src":     ("shape=parallelogram;perimeter=parallelogramPerimeter;size=16;", "#e1d5e7", "#9673a6"),
    "proc":    ("rounded=1;", "#d5e8d4", "#82b366"),
    "mode":    ("rounded=1;", "#fff2cc", "#d6b656"),
    "agg":     ("rounded=1;strokeWidth=3;", "#ffe6cc", "#d79b00"),
    "layer":   ("rounded=1;", "#dae8fc", "#6c8ebf"),
    "op":      ("rounded=0;", "#f5f5f5", "#999999"),
    "ghost":   ("rounded=1;dashed=1;", GRAY_FILL, GRAY_STROKE),
}

# id, kind, label, caption, x, y, w, h
BLOCKS = [
    # ---- A. 压缩阶梯 ------------------------------------------------------
    ("L0", "ladder", "中鱼升级", "第一性 / 总体范围 · WHO / WHEN / RESOLVE · q = Σ_r L_r × C_r", 80, 110, 520, 76),
    ("L1", "ladder", "FCF v1", "压缩 1（范围更小）· 本轮不读", 620, 110, 400, 76),
    ("L2", "ladder", "Simplified V0", "压缩 2 · 4.0–4.7 模块链 · Engagement Mode / 4 语义边界", 1040, 110, 400, 76),
    ("L3", "ladder", "0.3.4", "更小 · Bake DSL 与 Fixed Template 两条并行方案", 1040, 210, 400, 68),
    ("L4", "ladderB", "0.3.4.0-B", "当前版本投影 · Fixed Template Bake · AggregationRole 开关 · 无 DSL", 1040, 296, 400, 68),
    ("NAP", "ghost", "本轮未读", "FCF v1 骨架未读，压缩 1 与 2 之间的差异待补", 620, 210, 400, 68),

    # ---- B. Interaction 内部拓扑 -----------------------------------------
    ("SRC", "src", "Visual / Chemical / Mechanical Source", "呈现源（三通道并列）", 120, 450, 340, 76),
    ("PROP", "proc", "Fish-agnostic Propagation", "传播语境：距离 · 光照 · 浑浊 · 遮挡 · 流场", 120, 556, 340, 76),
    ("SIG", "src", "Receiver-local Signals", "到达受体的信号（Source ≠ Evidence）", 120, 662, 340, 76),
    ("EV", "src", "Perceptual Evidence[]", "+ FishSensoryCapability → 各通道 Evidence", 120, 768, 340, 76),
    ("INTERP", "proc", "Semantic Interpretation", "Target / Intrusion / Novelty\n（低证据 → hypothesis 更 broad，而不是先乘低 detection）", 120, 874, 340, 86),

    ("MFEED", "mode", "Feeding Mode", "Target Relation × Motivation\n× TaskAffordance → C_feed", 560, 874, 300, 86),
    ("MDEF", "mode", "Defense Mode", "Guarding ∧ InsideScope\n∧ ThreatRelevant → C_defense", 900, 874, 300, 86),
    ("MINV", "ghost", "Investigation Mode", "V0 不 admission：\n不能独立闭合到 SpawnCommit 兼容响应", 1240, 874, 320, 86),

    ("AGG", "agg", "Cross-Mode Aggregator", "operator 必须由 route relation 决定\nA ▷ B（PrimaryWithFallback）", 120, 1010, 1080, 86),
    ("CRET", "proc", "captureRetention  C", "", 120, 1130, 1080, 66),

    # ---- C. 四层分离 ------------------------------------------------------
    ("F1", "layer", "① Behavior Enabled", "该行为在当前 presentation-independent 行为语境中是否存在", 120, 1250, 520, 62),
    ("F2", "layer", "② Mode Applicability", "Applicable | NotApplicable(reason) | Unknown(reason)", 120, 1322, 520, 62),
    ("F3", "layer", "③ TaskAffordance", "Feasible | Constrained | Infeasible(reason) | Unknown", 120, 1394, 520, 62),
    ("F4", "layer", "④ Response", "完整求解后保留多少 Native Supply → C_mode", 120, 1466, 520, 62),
    ("FRULE", "op", "NotApplicable → 才可 fallback　|　Applicable + C=0 → 不得 fallback\nUnknown → fail closed　|　Infeasible 是 Applicable route 的 Task 结果，不撤销 Applicability",
     "", 120, 1540, 520, 56),

    # ---- D. operator admission -------------------------------------------
    ("OP_T", "op", "Operator Admission｜先定语义关系，再定算子", "q = L×C 是合法 retention join；TemperatureCoeff×DOCoeff×StructureCoeff 没有默认语义资格", 700, 1250, 900, 56),
    ("OP1", "op", "高度重叠的完整 alternative routes  →  max", "避免重复计同一 response population", 700, 1320, 900, 44),
    ("OP2", "op", "Primary 失败后才进入 Fallback  →  C = C_P + (1−C_P)·C_F", "残差形式；max(C_feed,C_defense) 已明确拒绝", 700, 1370, 900, 44),
    ("OP3", "op", "稳定互斥 mixture / regime  →  Σ π_m C_m", "必须有可识别 partition", 700, 1420, 900, 44),
    ("OP4", "op", "真实集合 union  →  μ(∪A_m)/μ(Ω)", "必须处理 overlap；不默认 independent Noisy-OR", 700, 1470, 900, 44),
    ("OP5", "op", "Hard prerequisite  →  typed Gate　|　Capacity vs Demand  →  Compare→Affordance", "反模式：让高分补偿 hard impossible；SpeedCoeff×TurnCoeff×EnergyCoeff", 700, 1520, 900, 44),
    ("OP6", "op", "多个 viability constraints  →  Joint bottleneck resolver　|　Support aggregation  →  Reduce by μT", "反模式：Temp×DO×Flow 默认乘法；Join 前分别平均 L/C", 700, 1570, 900, 44),
]

EDGES = [
    ("SRC", "PROP", "", "FLOW"),
    ("PROP", "SIG", "", "FLOW"),
    ("SIG", "EV", "", "FLOW"),
    ("EV", "INTERP", "", "FLOW"),
    ("INTERP", "MFEED", "", "FLOW"),
    ("INTERP", "MDEF", "", "FLOW"),
    ("INTERP", "MINV", "", "OPT"),
    ("MFEED", "AGG", "", "FLOW"),
    ("MDEF", "AGG", "", "FLOW"),
    ("MINV", "AGG", "", "OPT"),
    ("AGG", "CRET", "", "FLOW"),
    ("L0", "L1", "压缩 1", "LADDER"),
    ("L1", "L2", "压缩 2", "LADDER"),
    ("L2", "L3", "", "LADDER"),
    ("L3", "L4", "", "LADDER"),
    ("L1", "NAP", "", "OPT"),
]

EDGE_STYLES = {
    "FLOW":   "endArrow=block;strokeColor=#555555;strokeWidth=2;edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=10;fontColor=#444444;",
    "OPT":    "endArrow=block;dashed=1;strokeColor=#999999;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=10;fontColor=#777777;",
    "LADDER": "endArrow=block;strokeColor=#6c8ebf;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=10;fontColor=#5a7fa8;",
}

HINTS = {
    ("SRC", "PROP"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("PROP", "SIG"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("SIG", "EV"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("EV", "INTERP"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("INTERP", "MFEED"): "exitX=1;exitY=0.25;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("INTERP", "MDEF"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("INTERP", "MINV"): "exitX=1;exitY=0.75;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("MFEED", "AGG"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.25;entryY=0;entryDx=0;entryDy=0;",
    ("MDEF", "AGG"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.55;entryY=0;entryDx=0;entryDy=0;",
    ("MINV", "AGG"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.85;entryY=0;entryDx=0;entryDy=0;",
    ("AGG", "CRET"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("L0", "L1"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("L1", "L2"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("L2", "L3"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("L3", "L4"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("L1", "NAP"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
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
    a('<mxfile host="fcf-align-sketch" agent="align_interaction.py" version="26.0.0" type="device">\n')
    a('  <diagram id="fcf-align-interaction-v4" name="FCF 压缩阶梯 × Interaction 下钻 v4">\n')
    a('    <mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" '
      'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" '
      'pageHeight="%d" math="0" shadow="0">\n' % (PAGE_W, PAGE_H))
    a('      <root>\n')
    a('        <mxCell id="0" />\n')
    a('        <mxCell id="1" parent="0" />\n')

    a('        <mxCell id="TITLE" value="FCF 总图 · 压缩阶梯 × Interaction 下钻 v4 — 依据「中鱼升级｜」Mechanism Topology V2 + 中层逻辑样板 v8，与 0.3.4.0-B 三页" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=14;fontStyle=1;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="14" width="1300" height="28" as="geometry" />\n        </mxCell>\n')
    a('        <mxCell id="HINT" value="上排 = 压缩阶梯：中鱼升级是本体，每一层是范围更小的投影（v1 本轮未读）。下排 = Interaction 下钻：真正产生“玩家策略差异”的地方。橙色粗框 = 当前版本投影 0.3.4.0-B 落点。" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#666666;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="40" width="1300" height="26" as="geometry" />\n        </mxCell>\n')

    a('        <mxCell id="A_T" value="A. 压缩阶梯｜每一层是范围更小的投影" style="text;html=1;align=left;verticalAlign=middle;fontSize=12;fontStyle=1;fontColor=#4477aa;" vertex="1" parent="1">\n'
      '            <mxGeometry x="80" y="84" width="600" height="22" as="geometry" />\n        </mxCell>\n')
    a('        <mxCell id="B_T" value="B. Interaction 内部拓扑｜Source → Evidence → Interpretation → Modes → Aggregator" style="text;html=1;align=left;verticalAlign=middle;fontSize=12;fontStyle=1;fontColor=#4477aa;" vertex="1" parent="1">\n'
      '            <mxGeometry x="120" y="422" width="900" height="22" as="geometry" />\n        </mxCell>\n')
    a('        <mxCell id="C_T" value="C. 四层分离（不得混淆）" style="text;html=1;align=left;verticalAlign=middle;fontSize=12;fontStyle=1;fontColor=#4477aa;" vertex="1" parent="1">\n'
      '            <mxGeometry x="120" y="1222" width="400" height="22" as="geometry" />\n        </mxCell>\n')

    for bid, kind, label, caption, x, y, w, h in BLOCKS:
        base, fill, stroke = KIND_STYLE[kind]
        style = base + ("fontSize=12;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;"
                        % (fill, stroke))
        if kind == "ghost":
            style += "fontColor=%s;" % GRAY_FONT
        if kind == "op":
            style += "fontSize=10;fontColor=#444444;align=left;spacingLeft=10;"
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
    path = HERE / "align-interaction-v4.drawio"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(out))
    print("wrote %s (%d blocks, %d edges)" % (path, len(BLOCKS), len(EDGES)))


if __name__ == "__main__":
    main()

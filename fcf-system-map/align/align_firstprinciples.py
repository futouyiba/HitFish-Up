#!/usr/bin/env python3
"""FCF 总图 · 第一性原理主干对齐草图 v3 (alignment sketch, throwaway).

Re-based from the 「中鱼升级｜」 design branch (Mainline First-Principles /
Causal Heritage) rather than from FCF Simplified V0 / 0.3.4.

Authorities read:
  * 中鱼升级｜Overall System Model：从 World State 到 Fish Spawn Commit (v20)
  * 中鱼升级｜Behavioral Regime × Largemouth Bass：Spatial–Response 中层逻辑样板 (v8)

Why v3 replaces v2's spine:
  v2 used Simplified V0's 4.0–4.7 module chain as the spine. That chain is a
  *projection* of this branch, not the substrate. The first-principles spine is
  WHO / WHEN / RESOLVE with the mid-level kernel  q = Σ_r L_r × C_r, where
  L = Native Supply (Spatial) and C = captureRetention (Interaction) must Join
  on the same support BEFORE reducing.  It also carries the "semantic waist"
  (Readiness / ResolvedFunctionalContext / ActualPresentation) that V0's module
  chain compresses away.

Deterministic; regenerate: python3 align_firstprinciples.py
"""

from __future__ import annotations
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 1520, 1760

GRAY_FILL, GRAY_STROKE, GRAY_FONT = "#f5f5f5", "#a6a6a6", "#8f8f8f"

KIND_STYLE = {
    "fact":    ("shape=parallelogram;perimeter=parallelogramPerimeter;size=16;", "#dae8fc", "#6c8ebf"),
    "def":     ("shape=parallelogram;perimeter=parallelogramPerimeter;size=16;", "#e1d5e7", "#9673a6"),
    "waist":   ("rounded=1;", "#fff2cc", "#d6b656"),
    "resolve": ("rounded=1;", "#d5e8d4", "#82b366"),
    "bind":    ("rounded=1;", "#ffe6cc", "#d79b00"),
    "commit":  ("rounded=1;strokeWidth=3;", "#d5e8d4", "#2d6a4f"),
    "ghost":   ("rounded=1;dashed=1;", GRAY_FILL, GRAY_STROKE),
    "plane":   ("rounded=1;dashed=1;dashPattern=6 6;", "#f8f8f8", "#aaaaaa"),
}

# id, kind, label, caption, x, y, w, h
BLOCKS = [
    # ---- 因果输入 ---------------------------------------------------------
    ("W",  "fact", "World / Ecology / History", "authoritative facts + admitted history", 140, 110, 300, 84),
    ("F",  "def",  "Fish Definition", "Species / Cohort 稳定定义（≠ 当前状态）", 500, 110, 280, 84),
    ("A",  "fact", "Player Action + Skill + Equipment", "玩家 command（≠ 水下实际发生）", 840, 110, 300, 84),
    ("RC", "plane", "Consumable Resource", "独立窄 Domain：quantity / lineage / 资源结算\n不拥有 Spawn Opportunity", 1200, 110, 260, 100),

    # ---- 语义腰（三个容易被压丢的 semantic waist） ------------------------
    ("RD", "waist", "Readiness / Behavioral Context", "ResolvedBehavioralContext · 与当前呈现无关", 140, 280, 300, 84),
    ("FC", "waist", "Functional Context Resolver", "ResolvedFunctionalContext · task-independent 能力的\n单一 derived semantic authority", 500, 280, 280, 84),
    ("PR", "waist", "Presentation Realization", "ActualPresentation · 经装备/技能/物理后的实际呈现", 840, 280, 300, 84),

    # ---- WHEN：species-agnostic 的评价票 ---------------------------------
    ("OPP", "resolve", "Opportunity Formation", "LogicalOpportunity · species-agnostic WHEN\n定义本票评价哪段 support / measure", 840, 440, 300, 94),

    # ---- WHO 的两条支路 ---------------------------------------------------
    ("SP", "resolve", "Spatial Resolver", "Native Supply  L_i,j   · WHERE · 与呈现无关", 140, 440, 300, 94),
    ("IN", "resolve", "Interaction Resolver", "captureRetention  C_i,j  · 给定 presence 后\n对 ActualPresentation 的条件响应保留", 500, 440, 300, 94),

    # ---- 中层 Kernel：same-support Join ----------------------------------
    ("CAND", "bind", "Candidate Resolver — 同 support Join Before Reduce",
     "q_species,j = Σ_r  L_r,j × C_r,j        先在同一 identity / support 上组合，再按 Opportunity measure reduce\n"
     "→ W_i^opp / NativeCandidateSnapshot", 380, 620, 640, 110),
    ("REG", "waist", "Behavioral Regime 轴（条件性 materialize）",
     "presentation-independent 上游行为语义（如 NestGuarding）· 不是跨域 Owner\n"
     "仅当必须保存 L_r ↔ C_r 相关性时才活到 Join；Join 后通常死亡", 1080, 620, 380, 110),

    # ---- RESOLVE ----------------------------------------------------------
    ("POL", "bind", "Candidate Pre-Roll Gameplay Policy", "显式玩法规则；不改写 Native truth", 380, 790, 640, 76),
    ("ROLL", "resolve", "Canonical TrueRoll", "只消费 complete effective surface", 380, 910, 640, 76),

    ("TN", "ghost", "Accepted TrueNone", "正常 no-spawn（≠ 缺数据）", 140, 1050, 300, 84),
    ("FB", "ghost", "Fallback Runtime State", "只消费合法 accepted post-policy outcome\n+ credited time；不消费 incomplete", 140, 1180, 300, 94),
    ("SEL", "resolve", "Authoritative Selected Candidate", "", 760, 1050, 300, 84),
    ("INST", "resolve", "Spawn Instance Realization", "selection-neutral 具体化；不得因生成困难重开候选竞争", 760, 1180, 300, 94),

    ("REP", "resolve", "Replay / Settlement", "ordering / acceptance / replay / commit authority", 500, 1330, 400, 80),
    ("COMMIT", "commit", "Fish Spawn Commit", "中鱼系统成功边界 — Probe / Bite / Hook / Fight 不得回溯重算本次 WHO", 440, 1460, 520, 92),

    ("DOWN", "ghost", "Downstream interaction / outcome producers", "范围外：追击 / 咬口 / 接触 / 博鱼", 500, 1600, 400, 74),
]

# from, to, label, style-key
EDGES = [
    ("W", "RD", "", "FACT"),
    ("W", "FC", "", "FACT"),
    ("W", "SP", "", "FACT"),
    ("W", "PR", "", "FACT"),
    ("F", "RD", "", "FACT"),
    ("F", "FC", "", "FACT"),
    ("F", "SP", "", "FACT"),
    ("F", "IN", "", "FACT"),
    ("A", "PR", "", "FACT"),

    ("PR", "OPP", "ActualPresentation", "FLOW"),
    ("PR", "IN", "", "FLOW"),
    ("RD", "IN", "", "FLOW"),
    ("FC", "IN", "", "FLOW"),
    ("FC", "SP", "where applicable", "OPT"),

    ("SP", "CAND", "L  (Native Supply)", "FLOW"),
    ("IN", "CAND", "C  (captureRetention)", "FLOW"),
    ("OPP", "CAND", "本票的 support / measure", "FLOW"),

    ("CAND", "POL", "NativeCandidateSnapshot / W", "FLOW"),
    ("POL", "ROLL", "effective resolution surface", "FLOW"),

    ("ROLL", "TN", "Accepted TrueNone", "OPT"),
    ("ROLL", "SEL", "Selected Candidate", "FLOW"),
    ("TN", "FB", "", "OPT"),
    ("SEL", "INST", "", "FLOW"),
    ("FB", "REP", "（尾部保护后可进入）", "OPT"),
    ("INST", "REP", "ValidSpawnProposal", "FLOW"),
    ("REP", "COMMIT", "", "FLOW"),
    ("COMMIT", "DOWN", "", "GHOST"),

    ("RC", "SP", "", "PLANE"),
    ("RC", "IN", "", "PLANE"),
]

# 十条跨域宪法（只列对画图有约束力的）
CONSTITUTION = [
    ("Zero Competing Authority", "一个 Concept 恰好一个 Semantic Owner"),
    ("Player Command ≠ ActualPresentation", "玩家输入须经装备/技能/物理 realizable 后才被消费"),
    ("WHO ≠ WHEN", "鱼偏好 / 动机不得偷偷增加 Opportunity Supply"),
    ("Opportunity Species-Agnostic", "形成与评价 support 先于 fish-specific response"),
    ("Join Before Reduce", "L 与 C 必须在相同 identity / support 上组合，再按 measure reduce"),
    ("Unknown ≠ Zero", "缺数据 = ResolutionIncomplete，不等于 TrueNone"),
    ("Current ≠ Future State", "Event@t 只改变 causally-later state，禁止 same-epoch 回填"),
    ("Native Truth ≠ Gameplay Policy", "Guarantee / Fallback / Quest 不得伪装成自然原因"),
    ("Irreversible Boundaries Forward-Only", "Opportunity / Selection / Commit 一旦接受，下游不得重开上游竞争"),
    ("Production Preserves Semantics", "Bake Once = Semantic Consequence Once"),
]

INVARIANTS = [
    ("Behavior Enabled", "该行为在 presentation-independent 行为语境中是否存在"),
    ("Mode Applicability", "当前 Presentation 是否真的实例化了这个 Mode 的关系"),
    ("TaskAffordance", "行为理由成立后，具体动作做不做得到"),
    ("Response", "完整求解后有多少 Native Supply 被保留为有效响应"),
]

EDGE_STYLES = {
    "FACT":  "endArrow=block;strokeColor=#6c8ebf;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;",
    "FLOW":  "endArrow=block;strokeColor=#555555;strokeWidth=2;edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=10;fontColor=#444444;",
    "OPT":   "endArrow=block;dashed=1;strokeColor=#999999;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontSize=10;fontColor=#777777;",
    "PLANE": "endArrow=open;dashed=1;dashPattern=1 4;strokeColor=#bbbbbb;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;",
    "GHOST": "endArrow=block;dashed=1;strokeColor=#a6a6a6;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;",
}

LEGEND = [
    ("fact", "上游事实 / 输入"),
    ("def", "稳定定义（≠ 当前状态）"),
    ("waist", "语义腰 / 条件性轴"),
    ("resolve", "Resolver / 结算"),
    ("commit", "成功边界"),
    ("ghost", "非成功支路 / 范围外"),
]

HINTS = {
    ("W", "RD"): "exitX=0.25;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("W", "FC"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.25;entryY=0;entryDx=0;entryDy=0;",
    ("W", "SP"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("W", "PR"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("F", "IN"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.75;entryY=0;entryDx=0;entryDy=0;",
    ("A", "PR"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.75;entryY=0;entryDx=0;entryDy=0;",
    ("PR", "OPP"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("PR", "IN"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.25;entryDx=0;entryDy=0;",
    ("FC", "SP"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.25;entryDx=0;entryDy=0;",
    ("SP", "CAND"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.15;entryY=0;entryDx=0;entryDy=0;",
    ("IN", "CAND"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("OPP", "CAND"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.85;entryY=0;entryDx=0;entryDy=0;",
    ("CAND", "POL"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("POL", "ROLL"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("ROLL", "TN"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;",
    ("ROLL", "SEL"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("TN", "FB"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("SEL", "INST"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("FB", "REP"): "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
    ("INST", "REP"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;",
    ("REP", "COMMIT"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("COMMIT", "DOWN"): "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
    ("RC", "SP"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.75;entryDx=0;entryDy=0;",
    ("RC", "IN"): "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;",
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
    a('<mxfile host="fcf-align-sketch" agent="align_firstprinciples.py" version="26.0.0" type="device">\n')
    a('  <diagram id="fcf-align-firstprinciples-v3" name="FCF 第一性原理主干 v3">\n')
    a('    <mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" '
      'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" '
      'pageHeight="%d" math="0" shadow="0">\n' % (PAGE_W, PAGE_H))
    a('      <root>\n')
    a('        <mxCell id="0" />\n')
    a('        <mxCell id="1" parent="0" />\n')

    a('        <mxCell id="TITLE" value="FCF 总图 · 第一性原理主干 v3 — 依据「中鱼升级｜」分支（Mainline First-Principles / Causal Heritage）Overall System Model v20 + 中层逻辑样板 v8" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=14;fontStyle=1;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="16" width="1200" height="28" as="geometry" />\n        </mxCell>\n')
    a('        <mxCell id="HINT" value="主干 = WHO / WHEN / RESOLVE 三问；中层 Kernel = q = Σ_r L_r × C_r（同 support 先 Join 再 Reduce）。青色 = 三个 semantic waist；绿色 = Resolver；深绿粗框 = 成功边界 Fish Spawn Commit。" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#666666;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="44" width="1200" height="28" as="geometry" />\n        </mxCell>\n')

    # 十条宪法（右侧栏）
    a('        <mxCell id="CONST_T" value="Cross-domain Constitution｜十条跨域不变量" style="text;html=1;align=left;verticalAlign=top;fontSize=12;fontStyle=1;fontColor=#333333;" vertex="1" parent="1">\n'
      '            <mxGeometry x="1080" y="240" width="400" height="24" as="geometry" />\n        </mxCell>\n')
    for i, (name, desc) in enumerate(CONSTITUTION):
        a('        <mxCell id="CONST%d" value="%s&#10;%s" style="text;html=1;align=left;verticalAlign=top;fontSize=9;fontColor=#555555;" vertex="1" parent="1">\n'
          % (i, xesc("<b>%d. %s</b>" % (i + 1, name)), xesc(desc)) +
          '            <mxGeometry x="1080" y="%d" width="400" height="38" as="geometry" />\n'
          % (270 + i * 42) + '        </mxCell>\n')

    # Interaction 四层（左下角说明）
    a('        <mxCell id="INV_T" value="Interaction 四层分离（不得混淆）" style="text;html=1;align=left;verticalAlign=top;fontSize=11;fontStyle=1;fontColor=#333333;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="870" width="300" height="22" as="geometry" />\n        </mxCell>\n')
    for i, (name, desc) in enumerate(INVARIANTS):
        a('        <mxCell id="INV%d" value="%s → %s" style="text;html=1;align=left;verticalAlign=top;fontSize=9;fontColor=#555555;" vertex="1" parent="1">\n'
          % (i, xesc("<b>%s</b>" % name), xesc(desc)) +
          '            <mxGeometry x="60" y="%d" width="300" height="34" as="geometry" />\n'
          % (896 + i * 40) + '        </mxCell>\n')

    # 图例（右上）
    for i, (kind, text) in enumerate(LEGEND):
        base, fill, stroke = KIND_STYLE[kind]
        style = base + ("fontSize=10;fillColor=%s;strokeColor=%s;fontColor=#333333;" % (fill, stroke))
        if kind == "ghost":
            style += "dashed=1;"
        a('        <mxCell id="LEG%d" value="%s" style="%s" vertex="1" parent="1">\n'
          % (i, xesc(text), xesc(style)) +
          '            <mxGeometry x="1200" y="%d" width="220" height="28" as="geometry" />\n'
          % (100 + i * 36) + '        </mxCell>\n')

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
    path = HERE / "align-firstprinciples-v3.drawio"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(out))
    print("wrote %s (%d blocks, %d edges, %d invariants listed)"
          % (path, len(BLOCKS), len(EDGES), len(CONSTITUTION)))


if __name__ == "__main__":
    main()

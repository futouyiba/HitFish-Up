#!/usr/bin/env python3
"""七行分层展开模型 v2 — 对齐草图（throwaway，非 canonical）。

依据 Design Owner 2026-09-17 的修订：
  行1  L0 直接用三块（环境上下文 / 钓场投鱼配置 / 鱼的习性配置），外层是一个
       **不可折叠的 section**，让人一眼看到数据的三个重要来源；L1 再展开各自的细节。
  行2  L0 封面大块「烘焙」→ L1 五条计算通道（各分 核心/次要/排除）→ L2 通道一细展开。
  行3  **去掉原来的 L1**；L0 = 玩家策略与操作数据 · Cue 吸引元素，L1 = 钓具/钓组/姿态 ·
       呈现刺激通道。
  行4  **去掉原来的 L1**；把原 L2 的三个标题提为 L1：四层分离 / 两条完整模式 / 跨模式聚合。
  行5  宽条 + 四子块；L1 = 四块各自的细分。
  行6  抽鱼和生成；L1 = 抽出内容 + 参数透传。
  行7  运行 Fish AI；L1 = 刺鱼 / 博鱼。

布局策略（方案一 + 横向展开）：
  * 每行是一条固定高度的「行带」；行带边界永不移动。
  * 展开 = 往右侧延伸（横向），**不向下长**，因此下面的行永不被推动。
  * 行1 的行带常显三块；行2/5 折叠态用「封面块」填住行带。
"""

from __future__ import annotations
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 2260, 1800

KIND = {
    "section": ("rounded=1;dashed=1;strokeWidth=2;", "#f7f7f7", "#888888"),
    "cover":   ("rounded=1;strokeWidth=3;", "#ffe6cc", "#d79b00"),
    "mod":     ("rounded=1;", "#ffe6cc", "#d79b00"),
    "data":    ("shape=parallelogram;perimeter=parallelogramPerimeter;size=18;", "#dae8fc", "#6c8ebf"),
    "cube":    ("shape=cube;size=20;", "#dae8fc", "#6c8ebf"),
    "l1":      ("rounded=1;", "#fff7e6", "#d79b00"),
    "core":    ("rounded=1;strokeWidth=2;", "#d5e8d4", "#2d6a4f"),
    "sec":     ("rounded=1;dashed=1;", "#fff2cc", "#d6b656"),
    "skip":    ("rounded=1;dashed=1;", "#f5f5f5", "#aaaaaa"),
    "gate":    ("rhombus;whiteSpace=wrap;html=1;", "#f8cecc", "#b85450"),
    "note":    ("text;html=1;align=left;verticalAlign=top;fontSize=10;fontColor=#777777;", "#ffffff", "#ffffff"),
    "outside": ("rounded=1;dashed=1;", "#f5f5f5", "#a6a6a6"),
}

B, E = [], []


def b(id, kind, label, cap, x, y, w, h):
    B.append((id, kind, label, cap, x, y, w, h))


def e(a, c, label=""):
    E.append((a, c, label))


# 行带 y 与高度（行带边界固定；展开只向右）
ROW = {
    "R1": (110, 270), "R2": (420, 300), "R3": (760, 195), "R4": (995, 235),
    "R5": (1270, 230), "R6": (1540, 110), "R7": (1690, 110),
}


# ── 行带底纹 ──────────────────────────────────────────────────────────────
for rid, (ry, rh) in ROW.items():
    b("BAND." + rid, "section", "", "", 60, ry - 20, PAGE_W - 120, rh)

# ── 行1：常显的 section + 三块 ────────────────────────────────────────────
ry, rh = ROW["R1"]
b("R1.SEC", "section", "一、数据｜不可折叠的 section：数据的三个重要来源常显",
  "", 80, ry, 420, rh - 30)
b("D.CONTEXT", "data", "环境上下文", "季节 · 天气史 · 地形 · 结构", 100, ry + 42, 260, 58)
b("D.STOCK", "data", "钓场投鱼配置", "鱼种 × 品质 投放项 · 基础机会强度", 100, ry + 110, 260, 58)
b("D.HABIT", "data", "鱼的习性配置", "温度 / 水层 / 结构亲和 · 时段习性", 100, ry + 178, 260, 58)
b("R1.L1", "note", "L1（点任一数据块展开）", "", 560, ry - 26, 340, 20)
for i, (t, c) in enumerate([
        ("时间轴：时段 / 历史天气序列", "同一根轴，两种处理"),
        ("条件组：结构 · 水温 · 觅食水层 · 时段", "水温=计算型；其余=查表型"),
        ("投放项 / 基础机会强度 / 背景鱼标记", "含环境系数下限"),
        ("温度 · 觅食水层 · 结构亲和 · 时段 · 中鱼习性模式", "鱼的静态习性组件")]):
    b("R1.L1.%d" % i, "l1", t, c, 560, ry + 30 + i * 44, 460, 38)

# ── 行2：封面 → 通道 → 通道一细展开 ──────────────────────────────────────
ry, rh = ROW["R2"]
b("R2.COVER", "cover", "二、烘焙", "L0 折叠态 · 封面块填住行带", 80, ry, 300, 150)
b("BAKE", "mod", "烘焙", "L1 · 模块本体", 420, ry, 150, 50)
b("DEF", "cube", "派生环境场", "输出 · 行2 与行4 之间的交接数据", 420, ry + 66, 200, 60)
e("R2.COVER", "BAKE", "")

CH = [("1 空间分布权重", "环境侧"), ("2 活性 Activity", "鱼侧"),
      ("3 进食动机", "鱼侧"), ("4 警戒度", "鱼侧·后续"), ("5 动态进食偏好", "鱼侧")]
for i, (t, c) in enumerate(CH):
    b("R2.C%d" % i, "mod", t, c, 680, ry + i * 48, 150, 42)
    b("R2.C%d.core" % i, "core", "核心因子", "", 840, ry + i * 48, 100, 42)
    b("R2.C%d.sec" % i, "sec", "次要因子", "", 950, ry + i * 48, 100, 42)
    b("R2.C%d.skip" % i, "skip", "排除", "", 1060, ry + i * 48, 80, 42)

b("R2.L2.T", "note", "L2（展开通道 1）", "", 1180, ry - 26, 300, 20)
b("R2.HAB", "mod", "鱼的栖息地动态偏好", "与其它因子一起参与计算", 1180, ry, 250, 44)
b("R2.CORE", "core", "核心因子（方块 · 三角）", "按中鱼习性模式配置", 1180, ry + 56, 250, 44)
b("R2.SEC2", "sec", "次要因子（六边形 · 圆）", "", 1180, ry + 112, 250, 44)
b("R2.SKIP2", "skip", "不计算（六角形）", "", 1180, ry + 168, 250, 44)
b("R2.GATE", "gate", "门控", "核心因子先过门控", 1470, ry + 56, 110, 50)
b("R2.PASS", "mod", "满足 → 核心路径结算", "", 1610, ry + 40, 220, 40)
b("R2.FAIL", "mod", "不满足 → 失败路径 / 背景鱼下限", "", 1610, ry + 96, 220, 40)
b("R2.VAL", "data", "该通道的值", "", 1860, ry + 68, 150, 40)
for a_, c_ in [("R2.HAB", "R2.GATE"), ("R2.CORE", "R2.GATE"), ("R2.GATE", "R2.PASS"),
               ("R2.GATE", "R2.FAIL"), ("R2.PASS", "R2.VAL"), ("R2.FAIL", "R2.VAL")]:
    e(a_, c_)

# ── 行3 ──────────────────────────────────────────────────────────────────
ry, rh = ROW["R3"]
b("PLAYER", "data", "玩家策略与操作数据", "钓具 / 钓组 · 姿态", 80, ry, 260, 60)
b("CUE", "data", "Cue 吸引元素", "L0", 80, ry + 80, 260, 60)
b("R3.L1.T", "note", "L1（去掉原 L1，直接给细节）", "", 400, ry - 26, 340, 20)
b("R3.A", "l1", "钓具 / 钓组 · 姿态颗粒", "", 400, ry, 320, 50)
b("R3.B", "l1", "呈现刺激通道", "速度 · 轨迹动作 · 声音 · 震动 · 光闪烁 · 轮廓 · 气味", 400, ry + 70, 420, 60)

# ── 行4 ──────────────────────────────────────────────────────────────────
ry, rh = ROW["R4"]
b("RESP", "mod", "响应模块", "L0 · 两路输入：派生环境场 + Cue", 80, ry, 300, 60)
b("R4.L1.T", "note", "L1（原 L2 的三个标题提上来）", "", 420, ry - 26, 340, 20)
b("R4.A", "l1", "四层分离", "行为使能 → 模式适用性 → 任务可负担性 → 响应", 420, ry, 480, 50)
b("R4.B", "l1", "两条完整模式", "摄食：目标关系 × 动机 × 任务｜防御：护巢 ∧ 在范围内 ∧ 威胁相关",
  420, ry + 66, 480, 60)
b("R4.C", "l1", "跨模式聚合", "算子由路由关系决定", 420, ry + 140, 480, 50)

# ── 行5 ──────────────────────────────────────────────────────────────────
ry, rh = ROW["R5"]
b("TABLE", "mod", "圆桌抽鱼", "L0 · 宽条", 80, ry, 300, 42)
b("R5.L1.T", "note", "L1（四块各自细分）", "", 420, ry - 26, 300, 20)
T5 = [("品质抽取调整", "中鱼习性模式带来的品质份额调整"),
      ("圆桌权重表构建", "权重池：空间分布权重 × 适配系数 → SelectionWeight 行 + NONE"),
      ("硬保底", "尾部保护 · 独立控制层，不污染生态语义"),
      ("动态权重调整", "动态因子注入")]
for i, (t, c) in enumerate(T5):
    b("R5.T%d" % i, "l1", t, c, 420 + i * 440, ry, 410, 56)

# ── 行6 / 行7 ────────────────────────────────────────────────────────────
ry, rh = ROW["R6"]
b("DRAW", "mod", "抽鱼和生成", "L0", 80, ry, 300, 60)
b("R6.L1", "l1", "抽出鱼种 / 品质 / 大小 / 重量 ＋ 鱼侧动态参数透传（活性等）", "",
  420, ry, 620, 50)
ry, rh = ROW["R7"]
b("FISHAI", "outside", "运行 Fish AI", "L0 · 范围外", 80, ry, 300, 60)
b("R7.L1", "l1", "刺鱼 / 博鱼", "最简略", 420, ry, 400, 50)


def xesc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def html(label, cap):
    if not cap:
        return label
    return "%s<br><font style='font-size:9px;color:#555555'>%s</font>" % (label, cap)


def main():
    out = []
    a = out.append
    a('<?xml version="1.0" encoding="UTF-8"?>\n')
    a('<mxfile host="align" agent="expand_model_v2.py" version="26.0.0" type="device">\n')
    a('  <diagram id="expand-v2" name="七行分层展开模型 v2">\n')
    a('    <mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" '
      'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" pageHeight="%d" '
      'math="0" shadow="0">\n' % (PAGE_W, PAGE_H))
    a('      <root>\n        <mxCell id="0" />\n        <mxCell id="1" parent="0" />\n')

    a('        <mxCell id="TITLE" value="七行分层展开模型 v2 — 对齐草图（非 canonical）" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=14;fontStyle=1;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="16" width="800" height="28" as="geometry" />\n        </mxCell>\n')
    a('        <mxCell id="HINT" value="横向展开：每行是一条固定高度的行带（灰色虚线框），展开只向右延伸，因此下面的行永不被推动。行1 的 section 不可折叠、三块常显。行2 折叠态用封面块填住行带。" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#666666;" vertex="1" parent="1">\n'
      '            <mxGeometry x="60" y="42" width="1500" height="24" as="geometry" />\n        </mxCell>\n')

    for bid, kind, label, cap, x, y, w, h in B:
        base, fill, stroke = KIND[kind]
        style = base + ("whiteSpace=wrap;html=1;" if kind != "note" else "") + \
                "fontSize=12;fontColor=#000000;fillColor=%s;strokeColor=%s;" % (fill, stroke)
        if kind == "note":
            style = base
        if kind == "cover":
            style += "fontSize=20;fontStyle=1;"
        if kind == "section":
            style += "verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;fontSize=11;fontColor=#888888;"
        a('        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">\n'
          % (xesc(bid), xesc(html(label, cap)), xesc(style)) +
          '            <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" />\n' % (x, y, w, h) +
          '        </mxCell>\n')

    for i, (src, tgt, lab) in enumerate(E):
        s = ("rounded=1;html=1;edgeStyle=orthogonalEdgeStyle;fontSize=10;fontColor=#555555;"
             "strokeColor=#777777;strokeWidth=1.5;endArrow=block;")
        a('        <mxCell id="E%d" value="%s" style="%s" edge="1" parent="1" source="%s" target="%s">\n'
          % (i, xesc(lab), xesc(s), xesc(src), xesc(tgt)) +
          '            <mxGeometry relative="1" as="geometry" />\n        </mxCell>\n')

    a('      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')
    p = HERE / "expand-model-v2.drawio"
    p.write_text("".join(out), encoding="utf-8")
    print("wrote %s (%d blocks, %d edges)" % (p, len(B), len(E)))


if __name__ == "__main__":
    main()

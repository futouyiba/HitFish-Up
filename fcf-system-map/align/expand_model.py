#!/usr/bin/env python3
"""行 2「烘焙」的三层展开模型 — 对齐草图（throwaway，非 canonical）。

Design Owner 2026-09-17 给出的规格：
  L0  一个大块「烘焙」；输入 = 第一行数据；输出 = 派生环境场
  L1  展开后呈现若干「计算通道」，每条通道分 核心因子计算 / 次要因子计算 / 排除因子忽略，
      并得到该通道的值。通道：空间分布权重 / 活性 / 进食动机 / 警戒度 / 动态进食偏好
  L2  把「空间分布权重」通道再展开：按中鱼习性模式配置，把因子分成核心 / 次要 / 不计算，
      其中「鱼的栖息地动态偏好」与其它因子一起参与计算；核心因子先过门控，
      通过走一条路、不通过走另一条路（见 0.3.4.0-B）。

三块面板并排，直接对照「每一层看到什么」。同时用一条竖向标注表示
「派生环境场」位于行 2 与行 4 之间（是模块二与模块四之间的交接数据）。
"""

from __future__ import annotations
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 1340, 1560

KIND = {
    "cover":  ("rounded=1;strokeWidth=3;", "#ffe6cc", "#d79b00"),
    "mod":    ("rounded=1;", "#ffe6cc", "#d79b00"),
    "data":   ("shape=parallelogram;perimeter=parallelogramPerimeter;size=18;", "#dae8fc", "#6c8ebf"),
    "cube":   ("shape=cube;size=20;", "#dae8fc", "#6c8ebf"),
    "core":   ("rounded=1;strokeWidth=2;", "#d5e8d4", "#2d6a4f"),
    "sec":    ("rounded=1;dashed=1;", "#fff2cc", "#d6b656"),
    "skip":   ("rounded=1;dashed=1;", "#f5f5f5", "#aaaaaa"),
    "gate":   ("rhombus;whiteSpace=wrap;html=1;", "#f8cecc", "#b85450"),
    "chan":   ("rounded=0;", "#f0f0f0", "#999999"),
}

B = []          # id, kind, label, caption, x, y, w, h
E = []          # from, to, label


def b(id, kind, label, caption, x, y, w, h):
    B.append((id, kind, label, caption, x, y, w, h))


def e(a, c, label=""):
    E.append((a, c, label))


# ───────────────────────── 面板 A：L0 折叠态 ─────────────────────────
b("A.T", "skip", "L0｜折叠态", "一个大封面块，填住整条行带（解决“折叠后显得空”）", 60, 80, 620, 46)

b("A.R1", "data", "一、数据", "三块（此处略）", 60, 150, 300, 54)
b("A.BAKE", "cover", "二、烘焙", "折叠态：占据整条行带 · 字号放大", 60, 224, 300, 150)
b("A.DEF", "cube", "派生环境场", "位于行 2 与行 4 之间 · 模块二与模块四的交接数据", 60, 400, 300, 80)
b("A.R4", "mod", "四、响应", "", 60, 506, 300, 54)

e("A.R1", "A.BAKE", "输入")
e("A.BAKE", "A.DEF", "输出")
e("A.DEF", "A.R4", "交接")

# ───────────────────────── 面板 B：L1 通道态 ─────────────────────────
b("B.T", "skip", "L1｜展开一次", "烘焙 → 若干计算通道；每条通道分 核心 / 次要 / 排除，得到该通道的值", 700, 80, 600, 46)

b("B.BAKE", "mod", "烘焙", "模块本体", 700, 150, 170, 50)
b("B.DEF", "cube", "派生环境场", "输出", 900, 150, 190, 50)
e("B.BAKE", "B.DEF", "")

CH = [("空间分布权重", "环境侧"), ("活性 Activity", "鱼侧"),
      ("进食动机", "鱼侧"), ("警戒度", "鱼侧·后续"), ("动态进食偏好", "鱼侧")]
y = 224
for i, (name, side) in enumerate(CH, 1):
    cid = "B.C%d" % i
    b(cid, "chan", "%d  %s" % (i, name), side, 700, y, 170, 42)
    b(cid + ".core", "core", "核心因子", "", 890, y, 110, 42)
    b(cid + ".sec", "sec", "次要因子", "", 1010, y, 110, 42)
    b(cid + ".skip", "skip", "排除", "", 1130, y, 90, 42)
    e("B.BAKE", cid, "" if i > 1 else "分通道")
    y += 50

b("B.NOTE", "skip", "每条通道各自得到自己的值",
  "0.3.4.0-B：CORE 进 Core 聚合 / SECONDARY 进有界聚合 / EXCLUDED 完全不消费",
  700, y + 12, 620, 46)

# ───────────────────────── 面板 C：L2 通道 1 细展开 ─────────────────────────
b("C.T", "skip", "L2｜把「空间分布权重」通道再展开",
  "按中鱼习性模式配置，因子分成 核心 / 次要 / 不计算；核心因子先过门控", 60, 620, 700, 46)

b("C.CORE", "core", "核心因子（例：方块 · 三角）", "按中鱼习性模式配置", 60, 700, 300, 52)
b("C.SEC", "sec", "次要因子（例：六边形 · 圆）", "", 60, 762, 300, 52)
b("C.SKIP", "skip", "不计算（例：六角形）", "", 60, 824, 300, 52)
b("C.HAB", "mod", "鱼的栖息地动态偏好", "与其它因子一起参与计算", 60, 886, 300, 52)

b("C.GATE", "gate", "门控", "核心因子先过门控", 440, 700, 140, 62)
b("C.PASS", "mod", "满足 → 核心路径结算", "", 620, 690, 240, 50)
b("C.FAIL", "mod", "不满足 → 失败路径 / 背景鱼下限", "", 620, 756, 240, 50)
b("C.OUT", "data", "该通道的值", "", 920, 722, 170, 50)

e("C.CORE", "C.GATE", "")
e("C.HAB", "C.GATE", "")
e("C.GATE", "C.PASS", "通过")
e("C.GATE", "C.FAIL", "不通过")
e("C.PASS", "C.OUT", "")
e("C.FAIL", "C.OUT", "")


def xesc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def html(label, cap):
    return label + ("<br><font style='font-size:9px;color:#555555'>%s</font>" % cap if cap else "")


def main():
    out = []
    a = out.append
    a('<?xml version="1.0" encoding="UTF-8"?>\n')
    a('<mxfile host="align" agent="expand_model.py" version="26.0.0" type="device">\n')
    a('  <diagram id="expand-model" name="行 2 三层展开模型">\n')
    a('    <mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" '
      'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" pageHeight="%d" '
      'math="0" shadow="0">\n' % (PAGE_W, PAGE_H))
    a('      <root>\n        <mxCell id="0" />\n        <mxCell id="1" parent="0" />\n')

    a('        <mxCell id="TITLE" value="行 2「烘焙」三层展开模型 — 对齐草图（非 canonical）" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=14;fontStyle=1;" vertex="1" parent="1">\n'
      '            <mxGeometry x="40" y="16" width="900" height="28" as="geometry" />\n        </mxCell>\n')
    a('        <mxCell id="HINT" value="三块面板对照「每一层看到什么」。L0 用大封面块填住行带（解决折叠后显得空的问题），展开只切换可见性——行带边界与其它行的位置永不变动。" '
      'style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#666666;" vertex="1" parent="1">\n'
      '            <mxGeometry x="40" y="40" width="1100" height="24" as="geometry" />\n        </mxCell>\n')

    for bid, kind, label, cap, x, y, w, h in B:
        if w == 0:
            continue
        base, fill, stroke = KIND[kind]
        style = base + "whiteSpace=wrap;html=1;fontSize=12;fontColor=#000000;fillColor=%s;strokeColor=%s;" % (fill, stroke)
        if kind == "cover":
            style += "fontSize=20;fontStyle=1;"
        if kind == "skip" and bid.endswith(".T"):
            style += "fontSize=12;fontStyle=1;fontColor=#4477aa;"
        a('        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">\n'
          % (xesc(bid), xesc(html(label, cap)), xesc(style)) +
          '            <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" />\n' % (x, y, w, h) +
          '        </mxCell>\n')

    for i, (src, tgt, lab) in enumerate(E):
        s = "rounded=1;html=1;edgeStyle=orthogonalEdgeStyle;fontSize=10;fontColor=#555555;strokeColor=#777777;strokeWidth=1.5;endArrow=block;"
        a('        <mxCell id="E%d" value="%s" style="%s" edge="1" parent="1" source="%s" target="%s">\n'
          % (i, xesc(lab), xesc(s), xesc(src), xesc(tgt)) +
          '            <mxGeometry relative="1" as="geometry" />\n        </mxCell>\n')

    a('      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')
    p = HERE / "expand-model-row2.drawio"
    p.write_text("".join(out), encoding="utf-8")
    print("wrote %s (%d blocks, %d edges)" % (p, len([x for x in B if x[6]]), len(E)))


if __name__ == "__main__":
    main()

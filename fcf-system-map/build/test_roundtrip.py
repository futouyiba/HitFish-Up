#!/usr/bin/env python3
"""roundtrip.py 的回归测试：确认对差「该抓的抓得住、该忽略的忽略掉」。

为什么值得单独测：这个脚本的用途是我**据此改源文件**。漏报一处，你的手工改动就
白做了；误报（把 draw.io 保存时的噪声当成改动）会淹没真信号，让我去改一堆没动过
的地方。两边都会毁掉回路，所以两种情况都在这里锁住。

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
from roundtrip import diff_files, pages_of, parse_style  # noqa: E402

SRC = HERE.parent / "generated" / "fcf-system-map.drawio"
fails = []
# 测试里"按特征挑出来"的那两条边，id 在 mutate() 里填，main() 里断言。
DRAG_ID = [None]
NOISE_ID = [None]


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

    def cell(cid):
        for uo in model.iter("UserObject"):
            if uo.get("id") == cid:
                return uo, uo.find("mxCell")
        for mx in model.iter("mxCell"):
            if mx.get("id") == cid:
                return mx, mx
        raise KeyError(cid)

    def geo(cid):
        return cell(cid)[1].find("mxGeometry")

    g = geo("R2.F.CORE")                     # 移动
    g.set("x", str(int(g.get("x")) + 37))
    g.set("y", str(int(g.get("y")) - 11))
    g = geo("R2.C1.A1")                      # 拉大
    g.set("width", str(int(g.get("width")) + 100))
    g.set("height", str(int(g.get("height")) + 20))

    holder, _ = cell("R2.C1.V")              # 改文字（普通 cell 在 value 上）
    holder.set("value", "通道返回值")

    uo, _ = cell("R2.C1.F5")                 # 删一个
    for parent in model.iter():
        if uo in list(parent):
            parent.remove(uo)
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

    edges = [mx for mx in model.iter("mxCell")
             if mx.get("edge") == "1" and mx.get("id")]
    # 不写死边 id —— 边会随设计改名，测试不该跟着碎。按特征挑：
    #   * 有途经点的边（走廊绕行的那几条）→ 用来测"拖动线段"
    #   * 没有途经点的简单边          → 用来测"只重排 style 键序不该被报"
    withpts = [e for e in edges
               if e.find("mxGeometry") is not None
               and e.find("mxGeometry").find("Array") is not None
               and e.find("mxGeometry").find("Array").findall("mxPoint")]
    simple = [e for e in edges if e not in withpts]
    check(withpts and simple, "找不到足够的边来做拖动/噪声测试")
    if not (withpts and simple):
        return
    drag = withpts[0].find("mxGeometry").find("Array")
    for el, (x, y) in zip(drag.findall("mxPoint"), ((30, 700), (30, 1500))):
        el.set("x", str(x))
        el.set("y", str(y))
    noise_edge = simple[0]

    mx, _ = cell("R2.C1.F1")                 # 改样式 + 键序重排
    sm = parse_style(mx.get("style"))
    sm["fillColor"] = "#ff0000"
    mx.set("style", ";".join("%s=%s" % (k, v) for k, v in reversed(list(sm.items()))) + ";")

    x = noise_edge                           # 噪声 2：只重排键序，不该被报
    sm = parse_style(x.get("style"))
    x.set("style", ";".join("%s=%s" % (k, v) for k, v in reversed(list(sm.items()))) + ";")
    NOISE_ID[0] = x.get("id")
    DRAG_ID[0] = withpts[0].get("id")

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
        model_changes = {(c["id"], c["kind"]) for c in r["model"]}

        expect = {
            ("R2.F.CORE", "moved"),
            ("R2.C1.A1", "resized"),
            ("R2.C1.V", "relabeled"),
            ("R2.C1.F5", "removed"),
            ("k7QmZ3vRt9", "added"),
            (DRAG_ID[0], "rerouted"),
            ("R2.C1.F1", "restyled"),
        }
        for pair in sorted(expect - got):
            fails.append("漏报：%s %s" % pair)
        for pair in sorted(got - expect):
            fails.append("误报：%s %s" % pair)
        check(("(model)", "page") not in got, "模型级差异被混进了 cell 差异")

        # 噪声必须一字不报
        check(not any(c["id"] == NOISE_ID[0] for c in r["changes"]),
              "误报：只重排 style 键序被当成了改动（%s；draw.io 保存必然这样做）"
              % NOISE_ID[0])
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

        # 字节级确定性：同样的两份输入必须逐字节同结果
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


if __name__ == "__main__":
    main()

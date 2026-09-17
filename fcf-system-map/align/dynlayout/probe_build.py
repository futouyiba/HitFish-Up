#!/usr/bin/env python3
"""THROWAWAY probe builder for the dynamic-layout (approach 2) experiment.

Emits probe .drawio files with real drawio containers so the pinned official
viewer can be asked, empirically, whether the layout engine reflows anything.

Not part of the canonical pipeline. Does not touch graph.json / the skeleton.

    python3 probe_build.py            # -> probe.drawio, probe-layers.drawio
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The seven rows, as collapsible containers would be. Deliberately given
# OVERLAPPING y so a stack layout, if it ever runs, has visible work to do.
ROWS = [
    ("R1", "行一 数据"),
    ("R2", "行二 烘焙"),
    ("R3", "行三 玩家策略"),
    ("R4", "行四 响应"),
    ("R5", "行五 圆桌抽鱼"),
]
ROW_H = 100
ROW_W = 400


def xesc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def action_link(payload):
    return "data:action/json," + json.dumps(payload, separators=(",", ":"))


def vertex(cid, value, style, x, y, w, h, parent, link=None, visible=True):
    vis = "" if visible else ' visible="0"'
    geo = ('<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/>'
           % (x, y, w, h))
    if link:
        return ('<UserObject label="%s" link="%s" id="%s">'
                '<mxCell style="%s" vertex="1" parent="%s"%s>%s</mxCell>'
                '</UserObject>' % (xesc(value), xesc(link), xesc(cid),
                                   xesc(style), xesc(parent), vis, geo))
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s"%s>%s'
            '</mxCell>' % (xesc(cid), xesc(value), xesc(style), xesc(parent),
                           vis, geo))


ROW_STYLE = ("swimlane;html=1;horizontal=0;collapsible=1;startSize=24;"
             "fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;")
CHILD_STYLE = ("rounded=1;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;"
               "fontSize=11;")
PLAIN_STYLE = ("rounded=0;html=1;fillColor=#fafafa;strokeColor=#cccccc;")
STACK_STYLE = ("rounded=0;html=1;fillColor=#fafafa;strokeColor=#999999;"
               "childLayout=stackLayout;resizeParent=1;resizeParentMax=0;"
               "horizontalStack=0;stackSpacing=10;stackBorder=10;")
BTN_STYLE = ("rounded=1;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
             "fontSize=11;")


def body_rows(prefix, ox, row_h, y_start, parent, extra_style=""):
    """A stack of 5 collapsible row containers, each with 2 content children."""
    out = []
    for i, (rid, label) in enumerate(ROWS):
        cid = prefix + rid
        out.append(vertex(cid, label, ROW_STYLE + extra_style,
                          ox, y_start, ROW_W, row_h, parent))
        out.append(vertex(cid + "a", label + " · 子块A", CHILD_STYLE,
                          ox + 10, y_start + 30, 180, 50, cid))
        out.append(vertex(cid + "b", label + " · 子块B", CHILD_STYLE,
                          ox + 210, y_start + 30, 180, 50, cid))
    return "".join(out)


def build_probe(with_layers=False):
    out = []
    a = out.append
    layers = []
    a('<?xml version="1.0" encoding="UTF-8"?>')
    a('<mxfile host="probe" agent="probe_build.py" version="26.0.0" type="device">')
    a('<diagram id="dynlayout-probe" name="probe">')
    a('<mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" '
      'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
      'pageWidth="1700" pageHeight="1560" math="0" shadow="0">')
    a('<root>')
    a('<mxCell id="0"/>')
    a('<mxCell id="1" parent="0"/>')
    a('<mxCell id="Layer:Controls" value="Controls" parent="0"/>')
    a('<mxCell id="Layer:Main" value="Main" parent="0"/>')

    # ---- A. stack container with 5 collapsible rows, all at the same y ------
    # If the layout engine runs (at load or on any change), these become
    # 60 / 170 / 280 / ... If it never runs they all stay at y=60.
    a(vertex("OUTER", "OUTER (childLayout=stackLayout)", STACK_STYLE,
             60, 60, 420, 560, "Layer:Main"))
    a(body_rows("", 70, ROW_H, 70, "OUTER"))

    # ---- B. control: same shape, NO childLayout -----------------------------
    a(vertex("PLAIN", "PLAIN (no childLayout)", PLAIN_STYLE,
             560, 60, 420, 560, "Layer:Main"))
    a(body_rows("P", 570, ROW_H, 70, "PLAIN"))

    # ---- C. control: cells outside any layout owner -------------------------
    a(vertex("SIB", "SIB (sibling below OUTER, outside any stack)",
             PLAIN_STYLE, 60, 660, 420, 60, "Layer:Main"))
    a(vertex("EAST", "EAST (unrelated)", PLAIN_STYLE,
             1050, 60, 300, 120, "Layer:Main"))

    # ---- D. trigger buttons (custom actions reachable by click) -------------
    btns = [
        ("BTN:TOGGLE_R2a", "toggle R2 内容 (visibility)",
         {"actions": [{"toggle": {"cells": ["R2a", "R2b"]}}]}),
        ("BTN:HIDE_R2a", "hide R2 内容 (visibility)",
         {"actions": [{"hide": {"cells": ["R2a", "R2b"]}}]}),
        ("BTN:HIDE_ROW_R3", "hide 整行 R3 (row itself, transient=0)",
         {"actions": [{"hide": {"cells": ["R3"], "transient": False}}]}),
        ("BTN:SHOW_ROW_R3", "show 整行 R3",
         {"actions": [{"show": {"cells": ["R3"], "transient": False}}]}),
        ("BTN:TOGGLE_ROW_R3", "toggle 整行 R3",
         {"actions": [{"toggle": {"cells": ["R3"], "transient": False}}]}),
        ("BTN:COLLAPSE_R3", "style collapsed=1 on R3",
         {"actions": [{"style": {"key": "collapsed", "value": "1",
                                 "cells": ["R3"], "transient": False}}]}),
        ("BTN:EXPAND_R3", "style collapsed=0 on R3",
         {"actions": [{"style": {"key": "collapsed", "value": "0",
                                 "cells": ["R3"], "transient": False}}]}),
        ("BTN:STYLE_R2", "style R2 fillColor (style change)",
         {"actions": [{"style": {"key": "fillColor", "value": "#ff0000",
                                 "cells": ["R2"], "transient": False}}]}),
        ("BTN:VIEWBOX_R3R5", "viewbox R3..R5 (pans, no move)",
         {"actions": [{"viewbox": {"cells": ["R3", "R4", "R5"]}}]}),
    ]
    for i, (cid, label, payload) in enumerate(btns):
        a(vertex(cid, label, BTN_STYLE, 60 + (i % 2) * 430,
                 780 + (i // 2) * 46, 400, 36, "Layer:Controls",
                 link=action_link(payload)))

    if with_layers:
        # ---- E. pre-baked multi-state layers (the "no engine" alternative) ---
        # StateA = all rows collapsed-band; StateB = row 2 expanded.
        # Same ids reused with a suffix so both states can coexist.
        a('<mxCell id="Layer:StateA" value="StateA" parent="0"/>')
        a('<mxCell id="Layer:StateB" value="StateB" parent="0"/>')
        layers.append("StateA")
        layers.append("StateB")
        for cid, label, payload in [
            ("BTN:STATE_A", "→ StateA (全收起)",
             {"actions": [{"hide": {"layers": ["Layer:StateB"]}},
                          {"show": {"layers": ["Layer:StateA"]}}]}),
            ("BTN:STATE_B", "→ StateB (行二展开)",
             {"actions": [{"hide": {"layers": ["Layer:StateA"]}},
                          {"show": {"layers": ["Layer:StateB"]}}]}),
        ]:
            a(vertex(cid, label, BTN_STYLE, 940, 780 + len(layers) * 0,
                     400, 36, "Layer:Controls", link=action_link(payload)))
        # StateA geometry: every row band y = 60,120,180,240,300 (h=50)
        rowsA = [(r[0], r[1], 60 + i * 60, 50) for i, r in enumerate(ROWS)]
        # StateB geometry: row2 expanded (h=120) so rows below shift down
        rowsB = [("R1", "行一 数据", 60, 50), ("R2", "行二 烘焙", 120, 120),
                 ("R3", "行三 玩家策略", 250, 50), ("R4", "行四 响应", 310, 50),
                 ("R5", "行五 圆桌抽鱼", 370, 50)]
        for state, rows, vis in (("StateA", rowsA, True),
                                 ("StateB", rowsB, False)):
            for rid, label, y, h in rows:
                a(vertex("%s:%s" % (state, rid), label, PLAIN_STYLE,
                         1100, y, 260, h, "Layer:%s" % state))
                a(vertex("%s:%sa" % (state, rid), label + " · A", CHILD_STYLE,
                         1110, y + 26, 110, 20, "Layer:%s" % state))
                a(vertex("%s:%sb" % (state, rid), label + " · B", CHILD_STYLE,
                         1230, y + 26, 110, 20, "Layer:%s" % state))

    a('</root>')
    a('</mxGraphModel>')
    a('</diagram>')
    a('</mxfile>')
    return "".join(out)


def build_tc():
    """Variant C: the title bar and the content block are SEPARATE stack
    children, interleaved (T1,C1,T2,C2,...). The title is never hidden, so it
    stays clickable; clicking it toggles only its own content block and the
    stack packs the rest up/down."""
    T_STYLE = ("rounded=1;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
               "fontSize=12;fontStyle=1;")
    C_STYLE = ("rounded=1;html=1;fillColor=#f5f5f5;strokeColor=#b3b3b3;"
               "fontSize=11;")
    S_STYLE = ("rounded=0;html=1;fillColor=#fafafa;strokeColor=#999999;"
               "childLayout=stackLayout;resizeParent=1;resizeParentMax=0;"
               "horizontalStack=0;stackSpacing=6;stackBorder=8;")
    out = []
    a = out.append
    a('<?xml version="1.0" encoding="UTF-8"?>')
    a('<mxfile host="probe" agent="probe_build.py" version="26.0.0" type="device">')
    a('<diagram id="dynlayout-tc" name="tc">')
    a('<mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" '
      'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
      'pageWidth="1700" pageHeight="1560" math="0" shadow="0">')
    a('<root><mxCell id="0"/><mxCell id="1" parent="0"/>')
    a('<mxCell id="Layer:Controls" value="Controls" parent="0"/>')
    a('<mxCell id="Layer:Main" value="Main" parent="0"/>')
    a(vertex("OUTER2", "OUTER2 (interleaved T/C stack)", S_STYLE,
             60, 60, 440, 640, "Layer:Main"))
    y = 60
    for i, (rid, label) in enumerate(ROWS):
        t, c = "T%d" % (i + 1), "C%d" % (i + 1)
        a(vertex(t, label, T_STYLE, 70, y, 420, 28, "OUTER2",
                 link=action_link({"actions": [{"toggle": {
                     "cells": [c], "transient": False}}]})))
        a(vertex(c, label + " · 内容块", C_STYLE, 70, y + 34, 420, 72, "OUTER2"))
        a(vertex(c + "a", label + " · 子块A", CHILD_STYLE, 80, y + 60, 190, 40, c))
        a(vertex(c + "b", label + " · 子块B", CHILD_STYLE, 290, y + 60, 190, 40, c))
    a('</root></mxGraphModel></diagram></mxfile>')
    return "".join(out)


def main():
    for name, fn in (("probe.drawio", lambda: build_probe(False)),
                     ("probe-layers.drawio", lambda: build_probe(True)),
                     ("probe-tc.drawio", build_tc)):
        p = HERE / name
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(fn())
        print("wrote %s (%d bytes)" % (p, p.stat().st_size))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""THROWAWAY probe for the container-layout landing: P1..P5.

Answers the mechanical questions the emitter design depends on, in the REAL
pinned viewer, before any of it is written into the canonical builder.

  P1  does `movable=0` exclude a child from the stack (keeps its own coords,
      does not count toward the parent's height) while still travelling with
      the parent?
  P2  do negative parent-relative coordinates render (and can an edge reach
      such a cell)?
  P3  is a HORIZONTAL container's height really never recomputed?
  P4  horizontal-inside-vertical: is it byte-stable over repeated cycles?
  P5  does `marginLeft` on a vertical container indent children and preserve
      `H = 2*border + sum(h) + spacing*(n-1)`?

Not part of the canonical pipeline.

    python3 probe_nest_build.py      # -> probe-nest.drawio
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

B = 10          # stackBorder
SP = 10         # stackSpacing


def xesc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def action_link(payload):
    return "data:action/json," + json.dumps(payload, separators=(",", ":"))


def cell(cid, value, style, x, y, w, h, parent, link=None, visible=True):
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


def edge(eid, parent, src, tgt):
    st = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=1.5;")
    return ('<mxCell id="%s" value="" style="%s" edge="1" parent="%s" '
            'source="%s" target="%s"><mxGeometry relative="1" as="geometry"/>'
            '</mxCell>' % (eid, st, parent, src, tgt))


def box_style(axis, extra=""):
    return ("rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fontSize=9;"
            "childLayout=stackLayout;resizeParent=1;resizeParentMax=0;"
            "horizontalStack=%d;stackSpacing=%d;stackBorder=%d;strokeWidth=1;"
            "fillColor=#fafafa;strokeColor=#999999;%s"
            % (1 if axis == "h" else 0, SP, B, extra))


LEAF = ("rounded=0;html=1;fontSize=9;fillColor=#dae8fc;strokeColor=#6c8ebf;")
PIN = LEAF + "movable=0;"


def build():
    out = []
    a = out.append
    a('<?xml version="1.0" encoding="UTF-8"?>')
    a('<mxfile host="probe" agent="probe_nest_build.py" version="26.0.0" type="device">')
    a('<diagram id="nest-probe" name="nest">')
    a('<mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" '
      'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
      'pageWidth="1700" pageHeight="1560" math="0" shadow="0">')
    a('<root><mxCell id="0"/><mxCell id="1" parent="0"/>')
    a('<mxCell id="Layer:Controls" value="Controls" parent="0"/>')
    a('<mxCell id="Layer:Main" value="Main" parent="0"/>')

    # ---- S1 / P1 + P2 : movable=0 lateral pin, at NEGATIVE local x ---------
    # emitted box height = 2*10 + (40+10+40) + 10 = 110  (pin must not count)
    a(cell("P1BOX", "P1BOX (v)", box_style("v"), 300, 60, 300, 110,
           "Layer:Main"))
    a(cell("P1A", "P1A", LEAF, 10, 10, 280, 40, "P1BOX"))
    a(cell("P1B", "P1B", LEAF, 10, 60, 280, 40, "P1BOX"))
    a(cell("P1PIN", "P1PIN (movable=0, x=-230)", PIN, -230, 10, 200, 40,
           "P1BOX"))
    a(cell("P1FAR", "P1FAR (edge target)", LEAF, 30, 260, 200, 40,
           "Layer:Main"))
    a(edge("E:P1PIN", "Layer:Main", "P1PIN", "P1FAR"))

    # ---- S2 / P3 + P4 : horizontal inside vertical -------------------------
    # P3H height is DECLARED (130); P3TAIL sits after it inside P3OUT.
    a(cell("P3OUT", "P3OUT (v)", box_style("v"), 900, 60, 560, 200,
           "Layer:Main"))
    a(cell("P3H", "P3H (h)", box_style("h"), 10, 10, 540, 130, "P3OUT"))
    a(cell("P3L", "P3L (v)", box_style("v"), 10, 10, 240, 110, "P3H"))
    a(cell("P3L1", "P3L1", LEAF, 10, 10, 220, 30, "P3L"))
    a(cell("P3L2", "P3L2", LEAF, 10, 50, 220, 30, "P3L"))
    a(cell("P3R", "P3R (v)", box_style("v"), 260, 10, 240, 110, "P3H"))
    a(cell("P3R1", "P3R1", LEAF, 10, 10, 220, 30, "P3R"))
    a(cell("P3R2", "P3R2", LEAF, 10, 50, 220, 30, "P3R", visible=False))
    a(cell("P3R3", "P3R3", LEAF, 10, 90, 220, 30, "P3R", visible=False))
    a(cell("P3TAIL", "P3TAIL (after the h-container)", LEAF, 10, 150, 540, 40,
           "P3OUT"))

    # ---- S3 / P5 : marginLeft on a vertical container ----------------------
    # first child x must become B + marginLeft = 90; width = 400 - 20 - 80 = 300
    # height = 2*10 + (30+10+30+10+30) + 10 = 130
    a(cell("P5BOX", "P5BOX (v, marginLeft=80)",
           box_style("v", "marginLeft=80;"), 60, 500, 400, 130, "Layer:Main"))
    a(cell("P5A", "P5A", LEAF, 90, 10, 300, 30, "P5BOX"))
    a(cell("P5B", "P5B", LEAF, 90, 50, 300, 30, "P5BOX"))
    a(cell("P5C", "P5C", LEAF, 90, 90, 300, 30, "P5BOX"))

    # ---- S4 / P6 : does hiding a container cascade to its descendants? -----
    a(cell("P6BOX", "P6BOX (v)", box_style("v"), 1500, 60, 280, 70,
           "Layer:Main"))
    a(cell("P6GRP", "P6GRP (v)", box_style("v"), 10, 10, 260, 50, "P6BOX"))
    a(cell("P6X", "P6X (grandchild)", LEAF, 10, 10, 240, 30, "P6GRP"))

    # ---- controls ----------------------------------------------------------
    btns = [
        ("BTN:SHOW_P3R23", "show P3R2+P3R3",
         {"actions": [{"show": {"cells": ["P3R2", "P3R3"],
                                "transient": False}}]}),
        ("BTN:HIDE_P3R23", "hide P3R2+P3R3",
         {"actions": [{"hide": {"cells": ["P3R2", "P3R3"],
                                "transient": False}}]}),
        ("BTN:HIDE_P6BOX", "hide P6BOX (container id only)",
         {"actions": [{"hide": {"cells": ["P6BOX"], "transient": False}}]}),
        ("BTN:SHOW_P6BOX", "show P6BOX",
         {"actions": [{"show": {"cells": ["P6BOX"], "transient": False}}]}),
    ]
    for i, (cid, label, payload) in enumerate(btns):
        a(cell(cid, label,
               "rounded=1;html=1;fontSize=9;fillColor=#d5e8d4;"
               "strokeColor=#82b366;", 60, 700 + i * 34, 300, 28,
               "Layer:Controls", link=action_link(payload)))

    a('</root></mxGraphModel></diagram></mxfile>')
    return "".join(out)


def main():
    p = HERE / "probe-nest.drawio"
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(build())
    print("wrote %s (%d bytes)" % (p, p.stat().st_size))
    return 0


if __name__ == "__main__":
    sys.exit(main())

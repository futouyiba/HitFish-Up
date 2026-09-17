#!/usr/bin/env python3
"""THROWAWAY demo builder: 3-level nested containers with progressive drill-down.

    L1: 2 containers, side by side       (A, B)
      L2: 2 x 3 = 6 containers           (each L1 holds 3)
        L3: 2 x 3 x 3 = 18 containers    (each L2 holds 3)
          54 content blocks              (each L3 holds 3)

The two L1 trees are placed as independent columns rather than as siblings of
one shared root stack: a single column of 27 stacked rows is ~2213px tall, which
on a normal panel fits at ~0.36x and is illegible, while two columns bring the
fully-expanded box to ~720x1099 and fit at ~0.72x.  Each column still shows the
vertical reflow in full.  (The "a stack reflows its siblings" case, including a
root stack, is covered separately by probe.drawio.)

Every container is a real drawio container with `childLayout=stackLayout`, and
its children are emitted in this order:

    [ header cell (always visible, carries the toggle) , content child, ... ]

The header is a CHILD rather than the container's own title on purpose: a stack
only re-sizes its parent while it has at least one laid-out child, so a
container whose children are all hidden would keep a stale height and leave a
gap.  With the header as a permanent visible child, a collapsed container
shrinks to exactly header + 2*border — no gap at any level.

Geometry is emitted already equal to the layout fixed point for the initial
(all-collapsed) state, so nothing jumps on the first click.

Not part of the canonical pipeline: nothing under fcf-system-map/{graph,scopes,
views,contracts}.json, skeleton.baseline.json or generated/ is touched.

    python3 demo_build.py          # -> demo-nested.drawio
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

B = 5             # stackBorder, every container
SP = 5            # stackSpacing, every container
HDR_H = 18        # header height
LEAF_H = 20       # leaf height
ROOT_W = 340
L1_X = (60, 450)      # the two independent top-level columns
L1_Y = 60

BODY = {1: ("#dae8fc", "#6c8ebf"), 2: ("#d5e8d4", "#82b366"),
        3: ("#ffe6cc", "#d79b00")}
HDR = {1: "#6c8ebf", 2: "#82b366", 3: "#d79b00"}
LEAF_FILL, LEAF_STROKE = "#f5f5f5", "#a6a6a6"

COLLAPSED = 2 * B + HDR_H                       # container showing only its header


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


def body_style(level):
    fill, stroke = BODY[level]
    return ("rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fontSize=9;"
            "childLayout=stackLayout;resizeParent=1;resizeParentMax=0;"
            "horizontalStack=0;stackSpacing=%d;stackBorder=%d;strokeWidth=1;"
            "fillColor=%s;strokeColor=%s;" % (SP, B, fill, stroke))


def hdr_style(level):
    c = HDR[level]
    return ("rounded=0;whiteSpace=wrap;html=1;fontSize=10;fontStyle=1;"
            "fontColor=#ffffff;fillColor=%s;strokeColor=%s;" % (c, c))


LEAF_STYLE = ("rounded=0;html=1;fontSize=9;fillColor=%s;strokeColor=%s;"
              % (LEAF_FILL, LEAF_STROKE))


# ---------------------------------------------------------------- geometry ----
# Mirrors mxStackLayout.execute for horizontalStack=0 exactly:
#   child i  y     = B + sum(child_h[0..i-1]) + SP * i      (relative to parent)
#   parent   h     = 2*B + sum(child_h) + SP * (n - 1)
#   child    width = parent_w - 2*B                         (engine's `fill`)
# All heights below are integers, so every emitted coordinate is exact.
def ys_of(heights):
    ys, y = [], B
    for h in heights:
        ys.append(y)
        y += h + SP
    return ys


def h_of(heights):
    return 2 * B + sum(heights) + SP * (len(heights) - 1)


def build():
    out = []
    a = out.append

    # ---------------- id scheme -------------------------------------------
    l1_ids = ["L1-" + x for x in "AB"]
    l2_ids = ["L2-%s%d" % (x, i) for x in "AB" for i in (1, 2, 3)]
    l3_ids = ["L3-%s%d%d" % (x, i, j) for x in "AB" for i in (1, 2, 3)
              for j in (1, 2, 3)]
    leaf_ids = ["%s%d%d%d" % (x, i, j, k) for x in "AB" for i in (1, 2, 3)
                for j in (1, 2, 3) for k in (1, 2, 3)]

    children_of = {}
    for x in "AB":
        children_of["L1-" + x] = ["L2-%s%d" % (x, i) for i in (1, 2, 3)]
    for x in "AB":
        for i in (1, 2, 3):
            children_of["L2-%s%d" % (x, i)] = [
                "L3-%s%d%d" % (x, i, j) for j in (1, 2, 3)]
            for j in (1, 2, 3):
                children_of["L3-%s%d%d" % (x, i, j)] = [
                    "%s%d%d%d" % (x, i, j, k) for k in (1, 2, 3)]

    # widths: each level loses 2*B (children fill the parent's inner width)
    w_root = ROOT_W
    w_l1 = w_root - 2 * B
    w_l2 = w_l1 - 2 * B
    w_l3 = w_l2 - 2 * B
    w_leaf = w_l3 - 2 * B
    w_of = {"L1": w_l1, "L2": w_l2, "L3": w_l3}

    # ---------------- document --------------------------------------------
    a('<?xml version="1.0" encoding="UTF-8"?>')
    a('<mxfile host="demo" agent="demo_build.py" version="26.0.0" type="device">')
    a('<diagram id="nested-demo" name="nested">')
    a('<mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" '
      'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
      'pageWidth="1700" pageHeight="1560" math="0" shadow="0">')
    a('<root><mxCell id="0"/><mxCell id="1" parent="0"/>')
    a('<mxCell id="Layer:Controls" value="Controls" parent="0"/>')
    a('<mxCell id="Layer:Main" value="Main" parent="0"/>')

    # The two L1 trees are placed side by side as INDEPENDENT columns rather
    # than as siblings of one shared root stack.  Reason: a single column of
    # 27 stacked rows is ~2213px tall, which on a normal panel fits at ~0.36x
    # and is unreadable; two columns bring the fully-expanded box to ~720x1099
    # and fit at ~0.72x.  Each column still demonstrates the vertical reflow.
    # (The "root stack reflows its two children" case is covered by probe.drawio.)
    for n, x in enumerate("AB"):
        cid = "L1-" + x
        kids = children_of[cid]
        a(cell(cid, "", body_style(1), L1_X[n], L1_Y, w_l1, COLLAPSED,
               "Layer:Main"))
        a(cell("H:" + cid, "L1-%s　▸ 点开看 L2（3 个）" % x, hdr_style(1),
               L1_X[n] + B, L1_Y + B, w_l2, HDR_H, cid,
               link=action_link({"actions": [
                   {"toggle": {"cells": kids, "transient": False}}]})))
        l2_ys = ys_of([HDR_H] + [COLLAPSED] * 3)
        for m, (i, kid) in enumerate(zip((1, 2, 3), kids)):
            k3 = children_of[kid]
            a(cell(kid, "", body_style(2), B, l2_ys[m + 1], w_l2, COLLAPSED,
                   cid, visible=False))
            a(cell("H:" + kid, "L2-%s%d　▸ 点开看 L3（3 个）" % (x, i),
                   hdr_style(2), B, B, w_l3, HDR_H, kid,
                   link=action_link({"actions": [
                       {"toggle": {"cells": k3, "transient": False}}]})))
            l3_ys = ys_of([HDR_H] + [COLLAPSED] * 3)
            for p, (j, k3id) in enumerate(zip((1, 2, 3), k3)):
                leaves = children_of[k3id]
                a(cell(k3id, "", body_style(3), B, l3_ys[p + 1], w_l3,
                       COLLAPSED, kid, visible=False))
                a(cell("H:" + k3id, "L3-%s%d%d　▸ 点开看叶片（3 片）"
                       % (x, i, j), hdr_style(3), B, B, w_leaf, HDR_H, k3id,
                       link=action_link({"actions": [
                           {"toggle": {"cells": leaves, "transient": False}}]})))
                leaf_ys = ys_of([HDR_H] + [LEAF_H] * 3)
                for q, (k, lid) in enumerate(zip((1, 2, 3), leaves)):
                    a(cell(lid, "叶片 %s%d%d%d" % (x, i, j, k), LEAF_STYLE,
                           B, leaf_ys[q + 1], w_leaf, LEAF_H, k3id,
                           visible=False))

    a('</root></mxGraphModel></diagram></mxfile>')
    return "".join(out), {"l1": l1_ids, "l2": l2_ids, "l3": l3_ids,
                          "leaf": leaf_ids}


def main():
    xml, ids = build()
    p = HERE / "demo-nested.drawio"
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    print("wrote %s (%d bytes)" % (p, p.stat().st_size))
    print("  L1 %d / L2 %d / L3 %d / leaves %d"
          % (len(ids["l1"]), len(ids["l2"]), len(ids["l3"]), len(ids["leaf"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())

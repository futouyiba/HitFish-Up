#!/usr/bin/env python3
"""FCF Canonical System Map — deterministic draw.io builder (Production Pilot v0.1).

Inputs (semantic source, hand/AI-editable):
    graph.json     nodes (stable IDs, hierarchy, lanes) + explicit semantic edges
    scopes.json    lens scopes (OVERALL / 0.3.4.0) with ACTIVE/BOUNDARY/OUT classes
    views.json     view presets (expansion granularity + optional scope lens)
    contracts.json thin diagram-node -> authority links (validated only)

Output (build artifact, never hand-edit):
    generated/fcf-system-map.drawio

Design invariants (Production Pilot v0.1):
  * ONE cell per semantic node, ever. Scope coloring is a native `style`
    custom-action pass on those same cells — no duplicated instances, no
    scope x view layer multiplication (`::-suffixed` copies are banned).
  * Three orthogonal dimensions:
      Hierarchy  — semantic parent grouping; collapsible subtrees toggle cell
                   visibility (native `toggle`/`hide`/`show` actions).
      Scope      — per-node ACTIVE/BOUNDARY/OUT class; applied only as
                   fillColor/strokeColor/fontColor/dashed style changes.
                   OUT nodes are grayed, never hidden.
      View       — expansion presets; buttons that change visibility never
                   change styles and vice versa.
  * Deterministic: fixed constants, fixed emission order, no timestamps,
    uuids or randomness. Same sources -> byte-identical output.
  * Only native draw.io mechanisms: layers (controls/main), custom-action
    links (`data:action/json,{...}`) verified against the pinned official
    viewer (see spike/README.md for the verified action vocabulary).

Regenerate:
    python3 build/build_diagram.py
Validate:
    python3 build/validate.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# ---------------------------------------------------------------- layout ----
# Fixed-capacity lane grid. Anchored lanes position slots relative to their
# anchor node's top-left. Renaming never moves anything; appending to a lane
# takes the next slot; inserting mid-lane shifts later siblings one slot
# (documented rule).
NODE_W, NODE_H, STAGE_W = 260, 66, 220
# 7-row 整体框架 layout: `main` stacks the root + seven row labels; each row
# lane lays its blocks out horizontally (dx) on that row's own y.
LANES = {
    "main": {"x": 40, "w": 280, "anchor": None, "y0": 150, "dy": 0, "bandGap": 26, "tagH": 30},
    "r1a":     {"x": 400,  "w": 270, "anchor": "R1", "y0": 72, "dy": 70, "cap": 3},
    "r1b":     {"x": 700,  "w": 470, "anchor": "R1", "y0": 58, "dy": 46, "h": 42, "cap": 4},
    "r2cover": {"x": 40,   "w": 280, "anchor": "R2", "y0": 0,  "dx": 0, "h": 480},
    "r2io":    {"x": 400,  "w": 210, "anchor": "R2", "y0": 60, "dx": 0, "h": 64},
    "r2chG":   {"x": 660,  "w": 220, "anchor": "R2", "y0": 56, "dx": 232, "h": 224, "cap": 5},
    "r2chK":   {"follow": "r2chG", "x0": 8,  "y0": 44,  "w": 204, "h": 40},
    "r2chS":   {"follow": "r2chG", "x0": 8,  "y0": 88,  "w": 204, "h": 40},
    "r2chX":   {"follow": "r2chG", "x0": 8,  "y0": 132, "w": 204, "h": 40},
    "r2chV":   {"follow": "r2chG", "x0": 8,  "y0": 176, "w": 204, "h": 40},
    "r2l2":    {"x": 660,  "w": 250, "anchor": "R2", "y0": 310, "dy": 56, "h": 50, "cap": 4},
    "r2gate":  {"x": 950,  "w": 110, "anchor": "R2", "y0": 368, "dx": 0, "h": 50},
    "r2out":   {"x": 1090, "w": 220, "anchor": "R2", "y0": 348, "dy": 56, "h": 50, "cap": 2},
    "r2val":   {"x": 1350, "w": 150, "anchor": "R2", "y0": 376, "dx": 0, "h": 42},
    "r3cover": {"x": 40,   "w": 280, "anchor": "R3", "y0": 0, "dx": 0, "h": 190},
    "r3def":   {"x": 400,  "w": 260, "anchor": "R3", "y0": 44, "dx": 0, "h": 92},
    "r3l0":    {"x": 740,  "w": 270, "anchor": "R3", "y0": 40, "dy": 78, "cap": 2},
    "r3l1":    {"x": 1060, "w": 430, "anchor": "R3", "y0": 40, "dy": 72, "cap": 2},
    "r4cover": {"x": 40,   "w": 280, "anchor": "R4", "y0": 0, "dx": 0, "h": 180},
    "r4l0":    {"x": 400,  "w": 300, "anchor": "R4", "y0": 40, "dx": 0, "h": 60},
    "r4l1":    {"x": 740,  "w": 480, "anchor": "R4", "y0": 40, "dy": 68, "cap": 3},
    "r5cover": {"x": 40,   "w": 280, "anchor": "R5", "y0": 0, "dx": 0, "h": 180},
    "r5bar":   {"x": 400,  "w": 1120, "anchor": "R5", "y0": 40, "dx": 0, "h": 42},
    "r5t":     {"x": 420,  "w": 270, "anchor": "R5", "y0": 96, "dx": 286, "cap": 4},
    "r6cover": {"x": 40,   "w": 280, "anchor": "R6", "y0": 0, "dx": 0, "h": 140},
    "r6l0":    {"x": 400,  "w": 300, "anchor": "R6", "y0": 40, "dx": 0, "h": 60},
    "r6l1":    {"x": 740,  "w": 620, "anchor": "R6", "y0": 40, "dx": 0, "h": 50},
    "r7l0":    {"x": 400,  "w": 300, "anchor": "R7", "y0": 40, "dx": 0, "h": 60},
    "r7l1":    {"x": 740,  "w": 400, "anchor": "R7", "y0": 40, "dx": 0, "h": 50},
}
PAGE_W, PAGE_H = 1820, 2400

GRAY_FILL, GRAY_STROKE, GRAY_FONT = "#f5f5f5", "#a6a6a6", "#8f8f8f"

# 形状 / 配色按节点的 kind 字段决定（回到 v1 的图例）：
#   数据 / 配置   -> 平行四边形
#   派生数据      -> 立方体（派生环境场的专用图例）
#   过程 / 模块   -> 圆角矩形
#   范围外        -> 灰色虚线圆角矩形
KIND_STYLE = {
    "data":    ("shape=parallelogram;perimeter=parallelogramPerimeter;size=18;", "#dae8fc", "#6c8ebf"),
    "cube":    ("shape=cube;size=20;", "#dae8fc", "#6c8ebf"),
    "process": ("rounded=1;", "#ffe6cc", "#d79b00"),
    "l1":      ("rounded=1;", "#fff7e6", "#d79b00"),
    "cover":   ("rounded=1;strokeWidth=3;", "#ffe6cc", "#d79b00"),
    "core":    ("rounded=1;strokeWidth=2;", "#d5e8d4", "#2d6a4f"),
    "sec":     ("rounded=1;dashed=1;", "#fff2cc", "#d6b656"),
    "skip":    ("rounded=1;dashed=1;", "#f5f5f5", "#aaaaaa"),
    "gate":    ("rhombus;whiteSpace=wrap;html=1;", "#f8cecc", "#b85450"),
    "outside": ("rounded=1;dashed=1;", "#f5f5f5", "#a6a6a6"),
    "group":   ("rounded=1;dashed=1;strokeWidth=1;", "#fcfcfc", "#bbbbbb"),
    "gtitle":  ("rounded=0;", "#eeeeee", "#999999"),
}
ROW_STYLE = ("rounded=1;strokeWidth=2;", "#ffffff", "#4477aa")   # 行标题
DEFAULT_KIND = "process"

ANCHOR_STYLE = "endArrow=none;dashed=1;dashPattern=1 3;strokeColor=#b3b3b3;strokeWidth=1;edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;jettySize=auto;orthogonalLoop=1;"
EDGE_BASE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;jettySize=auto;orthogonalLoop=1;strokeWidth=1.5;"
)
EDGE_TYPES = {
    "DATA_FLOW": {"dashed": "", "arrow": "block", "dashPattern": ""},
    "CONTROL_OR_SELECTION": {"dashed": "dashed=1;", "arrow": "block", "dashPattern": ""},
    "REFERENCE_OR_CONFIG": {"dashed": "dashed=1;", "arrow": "open", "dashPattern": "dashPattern=1 4;"},
    "RETENTION": {"dashed": "", "arrow": "block", "dashPattern": "", "color": "#2d6a4f"},
    "ANCHOR": {"dashed": "dashed=1;", "arrow": "open", "dashPattern": "dashPattern=1 3;", "color": "#b03a2e"},
}

DIRS = {
    "N": (0.5, 0), "S": (0.5, 1), "E": (1, 0.5), "W": (0, 0.5),
}

LENS_EDGE_GRAY = "#a6a6a6"


def xesc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def style_of(kind):
    return KIND_STYLE.get(kind, KIND_STYLE[DEFAULT_KIND])


def node_style(kind):
    base, fill, stroke = style_of(kind)
    extra = ""
    if kind == "group":
        extra = "verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;fontSize=11;fontColor=#888888;"
    elif kind == "gtitle":
        extra = "fontSize=11;fontColor=#555555;fontStyle=1;"
    return (base + "whiteSpace=wrap;html=1;fontSize=12;fontColor=#000000;"
            "fillColor=%s;strokeColor=%s;%s" % (fill, stroke, extra))


def action_link(payload):
    return "data:action/json," + json.dumps(payload, separators=(",", ":"))


# ---------------------------------------------------------------- loading ----

def load_sources(root):
    src = {}
    for name in ("graph", "scopes", "views", "contracts"):
        with open(root / ("%s.json" % name), "r", encoding="utf-8") as f:
            src[name] = json.load(f)
    return src


# ---------------------------------------------------------------- layout ----

def layout(nodes, edges):
    ids = [n["id"] for n in nodes]
    by_id = {n["id"]: n for n in nodes}
    pos, lane_cursor, row_bands, lane_positions = {}, {}, {}, {}
    # main lane first (row nodes live there), then row lanes in definition order
    for lane in ["main"] + [l for l in LANES if l != "main"]:
        spec = LANES[lane]
        i = 0
        cursor_y = spec.get("y0", 0) if lane == "main" else 0
        for n in nodes:
            if n.get("lane") != lane:
                continue
            if lane == "main" and n.get("parent") is not None:
                # 行：按累积 band 高度定位；行带边界固定，展开不会推动它。
                # 行节点自身只有一条窄标签，但它向后推进整个 band 的高度。
                y = cursor_y
                cursor_y += n.get("band", 160) + spec.get("bandGap", 26)
                pos[n["id"]] = (spec["x"], y, spec["w"], spec.get("tagH", 28))
                row_bands[n["id"]] = (y, n.get("band", 160))
                i += 1
                continue
            if "follow" in spec:
                src = spec["follow"]
                if src not in lane_positions or i >= len(lane_positions[src]):
                    sys.exit("error: lane %s follows %s but has no slot %d"
                             % (lane, src, i))
                bx, by = lane_positions[src][i]
                x, y = bx + spec.get("x0", 0), by + spec.get("y0", 0)
                pos[n["id"]] = (x, y, spec["w"], spec.get("h", NODE_H))
                lane_positions.setdefault(lane, []).append((x, y))
                i += 1
                continue
            if "dx" in spec:
                # horizontal lane: blocks sit side by side on the anchor's row
                # (dx may be 0 — a single wide bar spanning the row)
                if spec["anchor"] not in pos:
                    sys.exit("error: lane %s anchors on %s which is not laid out yet"
                             % (lane, spec["anchor"]))
                x = spec["x"] + i * spec["dx"]
                y = pos[spec["anchor"]][1] + spec["y0"]
            elif spec["anchor"] is None:
                x, y = spec["x"], cursor_y
                cursor_y += (54 if n.get("parent") is None else NODE_H) + spec.get("bandGap", 26)
            else:
                if spec["anchor"] not in pos:
                    sys.exit("error: lane %s anchors on %s which is not laid out yet"
                             % (lane, spec["anchor"]))
                x = spec["x"]
                y = pos[spec["anchor"]][1] + spec["y0"] + i * spec["dy"]
            pos[n["id"]] = (x, y, spec["w"], spec.get("h", NODE_H))
            lane_positions.setdefault(lane, []).append((x, y))
            i += 1
        cap = spec.get("cap")
        if cap is not None and i > cap:
            sys.exit("error: 行 %s 已超出其声明容量 %d（当前 %d 个方块）。"
                     "该行已满 —— 扩容是一次需要重新规划布局的事件，"
                     "请调整 LANES 里的 cap / 页宽后重新冻结骨架，而不是让方块挤在一起。"
                     % (lane, cap, i))
        lane_cursor[lane] = i

    # 按「容量」而非「当前用量」校验行宽：预留的位置必须真的在页内
    for lane, spec in LANES.items():
        if "dx" not in spec or not spec.get("cap"):
            continue
        right = spec["x"] + (spec["cap"] - 1) * spec["dx"] + spec["w"]
        if right > PAGE_W:
            sys.exit("error: 行 %s 的容量 %d 需要宽度到 x=%d，超出页宽 %d。"
                     "要么缩小 dx，要么加宽 PAGE_W。" % (lane, spec["cap"], right, PAGE_W))

    # 页高按行带累积结果算（确定性），随后再做越界检查
    global PAGE_H
    bottom = max((pos[nid][1] + row_bands[nid][1] if nid in row_bands else y + h)
                 for nid, (x, y, w, h) in pos.items())
    PAGE_H = int(bottom + 220)

    for nid, (x, y, w, h) in pos.items():
        if x + w > PAGE_W or y + h > PAGE_H or x < 0 or y < 0:
            sys.exit("error: node %s lands outside the page canvas: %r" % (nid, pos[nid]))

    # structural (hierarchy) edges, deterministic order: node array order
    root_ids = {n["id"] for n in nodes if n.get("parent") is None}
    structural = []
    for n in nodes:
        p = n.get("parent")
        if p is None or p in root_ids:
            # 根节点 -> 行 的包含关系由行的纵向顺序表达，不画线（否则是一条贯穿全图的竖线）
            continue
        structural.append({"from": p, "to": n["id"],
                           "id": "EX:%s->%s" % (p, n["id"])})
    # semantic edges keep source order with stable ids
    semantic = []
    for e in edges:
        semantic.append({"from": e["from"], "to": e["to"], "type": e["type"],
                         "exit": e.get("exit"), "entry": e.get("entry"),
                         "id": "E:%s->%s" % (e["from"], e["to"])})
    return pos, structural, semantic, row_bands


def page_height(pos, row_bands):
    """页高按内容算（仍确定性）：最后一条行带底部 + 图例区。"""
    bottom = 0
    for nid, (x, y, w, h) in pos.items():
        if nid in row_bands:
            bottom = max(bottom, y + row_bands[nid][1])
        else:
            bottom = max(bottom, y + h)
    return int(bottom + 220)


def descendants(nid, nodes):
    by_parent = {}
    for n in nodes:
        by_parent.setdefault(n.get("parent"), []).append(n["id"])
    out, stack = [], [nid]
    while stack:
        cur = stack.pop()
        for child in by_parent.get(cur, []):
            out.append(child)
            stack.append(child)
    return out


# ------------------------------------------------------- scope lens data ----

def lens_of(scopes):
    """Returns (scope_by_id, lens_scope) where lens_scope is the scope entry
    with lens=true, or None."""
    scope_by_id = {s["id"]: s for s in scopes["scopes"]}
    lensed = [s for s in scopes["scopes"] if s.get("lens")]
    return scope_by_id, (lensed[0] if lensed else None)


def row_content_cells(nid, nodes, semantic, structural):
    """行的「内容」= 后代中除封面块以外的全部 cell，加上它们之间的边。
    封面块是折叠态的对立面，两者互斥，故不算在内容里。"""
    cover = cover_of(nid, nodes)
    desc = set(descendants(nid, nodes))
    if cover:
        desc.discard(cover)
    cells = sorted(desc)
    for e in semantic:
        if e["from"] in desc or e["to"] in desc:
            cells.append(e["id"])
    for e in structural:
        if e["from"] in desc or e["to"] in desc:
            cells.append(e["id"])
    return sorted(set(cells))


def cover_of(nid, nodes):
    for n in nodes:
        if n.get("parent") == nid and n.get("kind") == "cover":
            return n["id"]
    return None


def subtree_cells(nid, nodes, semantic, structural):
    """All cell ids hidden together when `nid` collapses: descendant vertex
    cells + every edge (structural or semantic) touching a descendant."""
    desc = set(descendants(nid, nodes))
    cells = sorted(desc)
    for e in semantic:
        if e["from"] in desc or e["to"] in desc:
            cells.append(e["id"])
    for e in structural:
        if e["from"] in desc or e["to"] in desc:
            cells.append(e["id"])
    return cells


def class_of(node_id, assignment):
    for cls, members in assignment.items():
        if node_id in members:
            return cls
    return None


def lens_actions(scope, nodes, kinds, structural, semantic, mode):
    """Style + opacity actions for a scope lens.

    mode='apply' -> colour the three classes AND dim out-of-scope cells
    mode='clear' -> neutral colours AND full opacity

    Opacity uses the native viewer action {"opacity": {"value": v, "cells": [...]}}.
    Dimming rather than hiding is deliberate: out-of-scope elements stay legible as
    context and the geometry never moves, so spatial memory survives the switch.
    """
    assignment = scope["assignment"]
    op = scope.get("opacity", {})
    acts = []

    def style(key, value, cells):
        cells = sorted(set(cells))
        if cells:
            acts.append({"style": {"key": key, "value": value,
                                   "cells": cells, "transient": False}})

    def set_opacity(value, cells):
        cells = sorted(set(cells))
        if cells:
            acts.append({"opacity": {"value": value, "cells": cells}})

    by_class = {c: sorted(assignment.get(c, [])) for c in ("ACTIVE", "BOUNDARY", "OUT")}
    all_nodes = [n["id"] for n in nodes]
    all_edges = [e["id"] for e in semantic] + [e["id"] for e in structural]

    gray_edges, dash_edges = [], []
    for e in semantic:
        tcls = class_of(e["to"], assignment)
        scls = class_of(e["from"], assignment)
        if tcls == "OUT":
            gray_edges.append(e["id"])
        elif scls == "BOUNDARY" and tcls == "ACTIVE":
            dash_edges.append(e["id"])

    if mode == "clear":
        for cls in ("OUT", "BOUNDARY"):
            for nid in by_class[cls]:
                _, fill, stroke = style_of(kinds.get(nid, DEFAULT_KIND))
                style("fillColor", fill, [nid])
                style("strokeColor", stroke, [nid])
                style("fontColor", "#000000", [nid])
        style("dashed", "0", by_class["BOUNDARY"])
        style("strokeWidth", "1", by_class["BOUNDARY"])
        by_eid = {e["id"]: e for e in semantic}
        for eid in gray_edges:
            _, fill, stroke = style_of(kinds.get(by_eid[eid]["from"], DEFAULT_KIND))
            style("strokeColor", stroke, [eid])
        style("dashed", "0", dash_edges)
        set_opacity(1, all_nodes + all_edges)
        return acts

    style("fillColor", GRAY_FILL, by_class["OUT"])
    style("strokeColor", GRAY_STROKE, by_class["OUT"])
    style("fontColor", GRAY_FONT, by_class["OUT"])
    style("dashed", "1", by_class["BOUNDARY"])
    style("strokeWidth", "2", by_class["BOUNDARY"])
    style("strokeColor", LENS_EDGE_GRAY, gray_edges)
    style("dashed", "1", dash_edges)

    set_opacity(op.get("ACTIVE", 1.0), by_class["ACTIVE"])
    set_opacity(op.get("BOUNDARY", 0.75), by_class["BOUNDARY"])
    set_opacity(op.get("OUT", 0.30), by_class["OUT"])
    set_opacity(op.get("BOUNDARY", 0.75), dash_edges)
    set_opacity(op.get("OUT", 0.30), gray_edges)
    return acts


# ---------------------------------------------------------------- easing ----

def view_button_payload(view, scope_by_id, nodes, kinds, semantic, structural, collapsible_cells):
    acts = []
    lens_id = view.get("scopeLens", "keep")
    if lens_id == "clear":
        for s in scope_by_id.values():
            if s.get("lens"):
                acts.extend(lens_actions(s, nodes, kinds, structural, semantic, "clear"))
    elif lens_id not in (None, "keep"):
        acts.extend(lens_actions(scope_by_id[lens_id], nodes, kinds, structural, semantic, "apply"))
    exp = view.get("expansion") or {}
    for key in ("collapse", "expand"):
        for nid in exp.get(key, []):
            if nid not in collapsible_cells:
                sys.exit("error: view %s tries to %s %r, which is not a "
                         "collapsible node in graph.json" % (view["id"], key, nid))
    for nid in exp.get("collapse", []):
        acts.append({"hide": {"cells": collapsible_cells[nid]}})
    for nid in exp.get("expand", []):
        acts.append({"show": {"cells": collapsible_cells[nid]}})
    return {"actions": acts}


# ---------------------------------------------------------------- emit ----

def vertex(cid, value, style, x, y, w, h, layer, link=None, visible=True):
    vis = "" if visible else ' visible="0"'
    geo = ('            <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" />\n'
           % (x, y, w, h))
    if link:
        return ('        <UserObject label="%s" link="%s" id="%s">\n'
                '          <mxCell style="%s" vertex="1" parent="%s"%s>\n%s'
                '          </mxCell>\n        </UserObject>\n'
                % (xesc(value), xesc(link), xesc(cid), xesc(style), xesc(layer), vis, geo))
    return ('        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s"%s>\n%s'
            '        </mxCell>\n'
            % (xesc(cid), xesc(value), xesc(style), xesc(layer), vis, geo))


def edge(eid, estyle, layer, src, tgt, visible=True, value=""):
    vis = "" if visible else ' visible="0"'
    return ('        <mxCell id="%s" value="%s" style="%s" edge="1" parent="%s" source="%s" target="%s"%s>\n'
            '            <mxGeometry relative="1" as="geometry" />\n'
            '        </mxCell>\n'
            % (xesc(eid), xesc(value), xesc(estyle), xesc(layer), xesc(src), xesc(tgt), vis))


def text_cell(cid, value, style, x, y, w, h):
    return vertex(cid, value, style, x, y, w, h, "Layer:Controls")


def emit(graph, scopes, views, pos, structural, semantic, collapsible_cells, default_view):
    kinds = {n["id"]: n.get("kind", DEFAULT_KIND) for n in graph["nodes"]}
    out = []
    a = out.append
    a('<?xml version="1.0" encoding="UTF-8"?>\n')
    a('<mxfile host="fcf-system-map" agent="build_diagram.py" version="26.0.0" type="device">\n')
    a('  <diagram id="fcf-canonical-system-map" name="FCF System Map">\n')
    a('    <mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" '
      'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" '
      'pageHeight="%d" math="0" shadow="0">\n' % (PAGE_W, PAGE_H))
    a('      <root>\n')
    a('        <mxCell id="0" />\n')
    a('        <mxCell id="1" parent="0" />\n')
    a('        <mxCell id="Layer:Controls" value="Controls" parent="0" />\n')
    a('        <mxCell id="Layer:Main" value="System Map" parent="0" />\n')

    # ---- controls（全部中文；英文仅作副标题） ---------------------------
    a(text_cell("CTRL:TITLE",
                "中鱼机制总图｜FCF Canonical System Map",
                "text;html=1;align=left;verticalAlign=middle;fontSize=16;fontStyle=1;",
                700, 56, 640, 30))
    a(text_cell("CTRL:HINT",
                "本图停在『整体框架』级别：只表达流向、模块边界与输入输出边界，不表达具体参数如何算出下一层。"
                "七大层自上而下；点击行标题可折叠整行（行内方块与所连箭头一起隐藏）。",
                "text;html=1;align=left;verticalAlign=top;fontSize=10;fontColor=#666666;",
                80, 92, 1080, 28))

    for i, v in enumerate(views["views"]):
        payload = view_button_payload(v, {s["id"]: s for s in scopes["scopes"]},
                                      graph["nodes"], kinds, semantic, structural,
                                      collapsible_cells)
        is_default = v["id"] == default_view
        x, y, w, h = 80 + i * 190, 54, 175, 34
        extra = "strokeWidth=2;fontStyle=1;" if is_default else "strokeWidth=1;"
        fill, stroke = ("#dae8fc", "#6c8ebf") if is_default else ("#d5e8d4", "#82b366")
        a(vertex("BTN:VIEW:%s" % v["id"], v["label"],
                 "rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=%s;strokeColor=%s;%s"
                 % (fill, stroke, extra),
                 x, y, w, h, "Layer:Controls",
                 link=action_link(payload)))

    # 图例：Scope 三态（右下侧栏，避开各行方块）
    legend = [
        ("LEG:DATA", "数据 / 配置",
         "shape=parallelogram;perimeter=parallelogramPerimeter;size=18;", "#dae8fc", "#6c8ebf"),
        ("LEG:CUBE", "派生数据（环境场）", "shape=cube;size=20;", "#dae8fc", "#6c8ebf"),
        ("LEG:PROC", "过程 / 模块", "rounded=1;", "#ffe6cc", "#d79b00"),
        ("LEG:OUT2", "范围外", "rounded=1;dashed=1;", GRAY_FILL, GRAY_STROKE),
    ]
    ly = PAGE_H - 128
    lx = 340
    for cid, label, base, fill, stroke in legend:
        a(vertex(cid, label,
                 base + "whiteSpace=wrap;html=1;fontSize=11;fontColor=#333333;"
                 "fillColor=%s;strokeColor=%s;" % (fill, stroke),
                 lx, ly, 250, 34, "Layer:Controls"))
        lx += 260
    a(text_cell("LEG:EDGES",
                "——▶  数据 / 权重流向　　– –▶  选择 · 控制　　┄┄  层属查询（非因果主张）",
                "text;html=1;align=left;verticalAlign=middle;fontSize=10;fontColor=#666666;",
                350, ly + 48, 900, 30))

    # ---- nodes (single instance each) ------------------------------------
    # Initial visibility is the DEFAULT VIEW applied at build time: every
    # collapsible row starts collapsed, then the default view's expansion spec
    # is baked in. A reader opening the file sees exactly the default view.
    default_spec = next(v for v in views["views"] if v["id"] == default_view)
    default_exp = default_spec.get("expansion") or {}
    initially_hidden = set()
    for row in [n["id"] for n in graph["nodes"] if n.get("band")]:
        cover = cover_of(row, graph["nodes"])
        content = row_content_cells(row, graph["nodes"], semantic, structural)
        if not cover:
            continue          # 没有封面 = 这行不可折叠（行1 常显 section、行7 范围外）
        if row in default_exp.get("expand", []):
            initially_hidden.add(cover)          # 展开态：封面藏起，内容可见
        else:
            initially_hidden.update(content)     # 折叠态：内容藏起，封面可见
    for row in default_exp.get("collapse", []):
        cover = cover_of(row, graph["nodes"])
        if cover:
            initially_hidden.add(cover)
    for n in graph["nodes"]:
        nid = n["id"]
        x, yy, w, h = pos[nid]
        kind = n.get("kind", DEFAULT_KIND)
        style = node_style(kind) + ("strokeWidth=2;" if n.get("collapsible") else "")
        link = None
        value = n["label"]
        if n.get("caption"):
            value += ("<br><font style='font-size:9px;color:#555555'>%s</font>"
                      % n["caption"])
        if n.get("collapsible"):
            # 行标签 = 折叠（显示封面、隐藏内容）
            link = action_link({"actions": [{"show": {"cells": [cover_of(nid, graph["nodes"])] if cover_of(nid, graph["nodes"]) else []}},
                                            {"hide": {"cells": row_content_cells(nid, graph["nodes"], semantic, structural)}}]})
        elif n.get("kind") == "cover":
            # 封面 = 展开（隐藏封面、显示内容）
            row = n["parent"]
            link = action_link({"actions": [{"hide": {"cells": [nid]}},
                                            {"show": {"cells": row_content_cells(row, graph["nodes"], semantic, structural)}}]})
        a(vertex(nid, value, style, x, yy, w, h, "Layer:Main", link=link,
                 visible=nid not in initially_hidden))

    # ---- edges: structural (faint) then semantic (typed) -----------------
    for e in structural:
        a(edge(e["id"], ANCHOR_STYLE, "Layer:Main", e["from"], e["to"],
               visible=e["id"] not in initially_hidden))
    for e in semantic:
        kind = kinds.get(e["from"], DEFAULT_KIND)
        _, fill, stroke = style_of(kind)
        t = EDGE_TYPES[e["type"]]
        stroke = t.get("color", stroke)
        style = (EDGE_BASE + t["dashed"] + t["dashPattern"] +
                 "endArrow=%s;strokeColor=%s;" % (t["arrow"], stroke))
        if e.get("label"):
            style += "fontSize=10;fontColor=%s;" % stroke
        for key, val in (("exit", e.get("exit")), ("entry", e.get("entry"))):
            if val:
                fx, fy = DIRS[val]
                style += "%sX=%s;%sY=%s;%sDx=0;%sDy=0;" % (
                    "exit" if key == "exit" else "entry", fx,
                    "exit" if key == "exit" else "entry", fy,
                    "exit" if key == "exit" else "entry",
                    "exit" if key == "exit" else "entry")
        a(edge(e["id"], style, "Layer:Main", e["from"], e["to"],
               visible=e["id"] not in initially_hidden, value=e.get("label", "")))

    a('      </root>\n')
    a('    </mxGraphModel>\n')
    a('  </diagram>\n')
    a('</mxfile>\n')
    return "".join(out)


# ---------------------------------------------------------------- main ----

def build(root):
    src = load_sources(root)
    graph, scopes, views = src["graph"], src["scopes"], src["views"]

    pos, structural, semantic, row_bands = layout(graph["nodes"], graph["edges"])
    collapsible_cells = {
        n["id"]: subtree_cells(n["id"], graph["nodes"], semantic, structural)
        for n in graph["nodes"] if n.get("collapsible")
    }
    default_view = views["defaultView"]
    xml = emit(graph, scopes, views, pos, structural, semantic,
               collapsible_cells, default_view)
    out_path = root / "generated" / "fcf-system-map.drawio"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    digest = hashlib.sha256(xml.encode("utf-8")).hexdigest()
    n_cells = len(graph["nodes"]) + len(structural) + len(semantic)
    print("wrote %s: %d nodes, %d structural + %d semantic edges, %d cells total, "
          "sha256=%s" % (out_path, len(graph["nodes"]), len(structural),
                         len(semantic), n_cells, digest[:16]))
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(ROOT),
                    help="fcf-system-map root directory (contains the four source JSONs)")
    ap.add_argument("--out", default=None,
                    help="override output path (default <root>/generated/fcf-system-map.drawio)")
    args = ap.parse_args()
    root = Path(args.root)
    if args.out:
        src = load_sources(root)
        graph, scopes, views = src["graph"], src["scopes"], src["views"]
        pos, structural, semantic, row_bands = layout(graph["nodes"], graph["edges"])
        collapsible_cells = {
            n["id"]: subtree_cells(n["id"], graph["nodes"], semantic, structural)
            for n in graph["nodes"] if n.get("collapsible")
        }
        xml = emit(graph, scopes, views, pos, structural, semantic,
                   collapsible_cells, views["defaultView"])
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(xml)
        print("wrote %s" % args.out)
    else:
        build(root)


if __name__ == "__main__":
    main()

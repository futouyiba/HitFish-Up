#!/usr/bin/env python3
"""FCF Canonical System Map — deterministic draw.io builder (Production Pilot v0.1).

Inputs (semantic source, hand/AI-editable):
    graph.json     nodes (stable IDs, hierarchy, lanes) + explicit semantic edges
    layout.json    版面：容器包纳树（C: 前缀的容器 + graph.json 节点作叶子）
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
      Hierarchy  — 版面容器（layout.json）互相包纳，由 draw.io 的布局引擎在
                   每次编辑事务后重排：展开一层，下面的层自动让位。
      Scope      — per-node ACTIVE/BOUNDARY/OUT class; applied only as
                   fillColor/strokeColor/fontColor/dashed style changes.
                   OUT nodes are grayed, never hidden.
      View       — expansion presets; buttons that change visibility never
                   change styles and vice versa.
  * 版面硬规则：引擎永不重算**水平**容器的高度，所以重排只能沿「垂直容器的连续链」
    向上传播 —— 水平容器只装不可再展开的叶子，高度发射时钉死。见
    align/dynlayout/REPORT-dynamic-layout.md 的探针 P3。
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
    "core":    ("rounded=1;strokeWidth=2;", "#d5e8d4", "#2d6a4f"),
    "sec":     ("rounded=1;dashed=1;", "#fff2cc", "#d6b656"),
    "skip":    ("rounded=1;dashed=1;", "#f5f5f5", "#aaaaaa"),
    "gate":    ("rhombus;whiteSpace=wrap;html=1;", "#f8cecc", "#b85450"),
    "outside": ("rounded=1;dashed=1;", "#f5f5f5", "#a6a6a6"),
    "group":   ("rounded=1;dashed=1;strokeWidth=1;", "#fcfcfc", "#bbbbbb"),
    "gtitle":  ("rounded=0;", "#eeeeee", "#999999"),
}
DEFAULT_KIND = "process"
# 版面容器只画一条很淡的虚线边，提示包纳关系；不留底色，避免盖住方块。
CONTAINER_STROKE = "#e3e3e3"
# 标题条（行标题 / 分组标题）：左对齐加粗，压低体量，便于一眼看出这是可点的把手。
TITLE_FILL, TITLE_STROKE = "#f2f6fa", "#7d9bb8"
TITLE_EXTRA = ("align=left;spacingLeft=12;verticalAlign=middle;fontSize=13;"
               "fontStyle=1;")

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


def node_style(kind, role=None):
    if role == "title":
        return ("rounded=0;whiteSpace=wrap;html=1;fontColor=#1f3a52;"
                "fillColor=%s;strokeColor=%s;strokeWidth=2;%s"
                % (TITLE_FILL, TITLE_STROKE, TITLE_EXTRA))
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
# 版面来自 layout.json 的「包纳树」：内部节点是容器（C: 前缀，带 childLayout），
# 叶子是 graph.json 的节点。几何必须与 mxStackLayout 的首轮结果逐像素一致，
# 否则首次点击时整批行会跳（见 align/dynlayout/REPORT-dynamic-layout.md）。
#
# 硬规则（探针 P3 实测）：布局引擎永不重算**水平**容器的高度，所以重排只能沿
# 「垂直容器的连续链」向上传播 —— 水平容器只装不可再展开的叶子，高度发射时钉死。

LEAF_W = {
    "data": 260, "l1": 250, "process": 260, "cube": 260, "outside": 260,
    "group": 300, "core": 190, "sec": 190, "skip": 190, "gate": 130,
}
DEFAULT_LEAF_W = 240
ROOT_X, ROOT_Y = 40, 150


def load_layout(root):
    with open(root / "layout.json", "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_layout(lay, nodes):
    """把 layout.json 的 ref 展开成实树，并校验「每个节点恰好出现一次」。"""
    by_id = {n["id"]: n for n in nodes}
    containers = lay["containers"]

    def build(spec, cid, parent):
        kids = []
        for ch in spec.get("children", []):
            if "node" in ch:
                if ch["node"] not in by_id:
                    sys.exit("error: layout.json 引用了 graph.json 里没有的节点 %r"
                             % ch["node"])
                kids.append({"kind": "leaf", "id": ch["node"], "spec": ch,
                             "parent": cid})
            elif "ref" in ch:
                if ch["ref"] not in containers:
                    sys.exit("error: layout.json 引用了未定义的容器 %r" % ch["ref"])
                sub = build(containers[ch["ref"]], ch["ref"], cid)
                sub["spec"] = ch
                kids.append(sub)
            else:
                sys.exit("error: layout.json 的子项既非 node 也非 ref: %r" % (ch,))
        return {"kind": "container", "id": cid, "axis": spec.get("axis", "v"),
                "indent": spec.get("indent", 0), "spec": spec,
                "children": kids, "parent": parent}

    root = build(lay["root"], "C:ROOT", None)
    seen = {}

    def count(n):
        if n["kind"] == "leaf":
            seen[n["id"]] = seen.get(n["id"], 0) + 1
        for c in n.get("children", []):
            count(c)
    count(root)
    dup = sorted(k for k, v in seen.items() if v > 1)
    miss = sorted(n["id"] for n in nodes if n["id"] not in seen)
    if dup or miss:
        sys.exit("error: layout.json 覆盖不全 —— 重复 %r / 缺失 %r" % (dup, miss))
    return root


def layout_ctx(lay, graph, views, root):
    """可见性 + 尺寸上下文。

    容器的折叠态由 default view 决定：它的**标题节点**出现在 expansion.expand 里
    就是展开态，否则折叠态。子项的 `when` 与之匹配时才在初态可见。
    """
    spec = next(v for v in views["views"] if v["id"] == views["defaultView"])
    expanded = set((spec.get("expansion") or {}).get("expand", []))

    by_cid = {}

    def index(n):
        by_cid[n["id"]] = n
        for c in n.get("children", []):
            index(c)
    index(root)

    def state_of(cid):
        container = by_cid.get(cid)
        if container is None:
            return None
        for c in container.get("children", []):
            if c["kind"] == "leaf" and c["spec"].get("role") == "title":
                return "expanded" if c["id"] in expanded else "collapsed"
        return None

    def visible(child):
        when = child["spec"].get("when")
        if when is None:
            return True
        return when == state_of(child["parent"])

    return {
        "border": lay["border"], "spacing": lay["spacing"],
        "titleH": lay["titleH"], "leafH": lay["leafH"],
        "kinds": {n["id"]: n.get("kind", DEFAULT_KIND) for n in graph["nodes"]},
        "visible": visible, "state_of": state_of, "expanded": expanded,
        "leaf_w": {},
    }


def natural_w(node, ctx):
    if node["kind"] == "leaf":
        kind = ctx["kinds"].get(node["id"], DEFAULT_KIND)
        return (node["spec"].get("w") or LEAF_W.get(kind, DEFAULT_LEAF_W))
    b, sp = ctx["border"], ctx["spacing"]
    laid = [c for c in node.get("children", [])
            if ctx["visible"](c) and not c["spec"].get("pin")]
    if not laid:
        return 2 * b + node["indent"]
    if node["axis"] == "h":
        return (2 * b + node["indent"] + sum(natural_w(c, ctx) for c in laid)
                + sp * (len(laid) - 1))
    return 2 * b + node["indent"] + max(natural_w(c, ctx) for c in laid)


def measure(node, forced_w, ctx):
    """自底向上算尺寸、自顶向下落局部坐标（相对父容器左上角）。

    容器的高度/宽度只由**初态可见**的子块决定（发射出来的几何就是布局引擎的
    首轮不动点）。初态不可见的子块照样要发出去（带 visible="0"），所以也得给
    它们一组坐标 —— 顺排在可见内容之后，仅供存储，引擎在它们变可见时会重排。
    """
    b, sp = ctx["border"], ctx["spacing"]
    if node["kind"] == "leaf":
        kind = ctx["kinds"].get(node["id"], DEFAULT_KIND)
        node["_w"] = (forced_w or node["spec"].get("w")
                      or LEAF_W.get(kind, DEFAULT_LEAF_W))
        node["_h"] = (node["spec"].get("h")
                      or (ctx["titleH"] if node["spec"].get("role") == "title"
                          else ctx["leafH"].get(kind, 44)))
        return
    kids = [c for c in node["children"] if not c["spec"].get("pin")]
    vis = [c for c in kids if ctx["visible"](c)]
    hid = [c for c in kids if not ctx["visible"](c)]
    ind = node["indent"]
    if node["axis"] == "h":
        # 水平容器：子块保留自己的宽度；容器宽向上汇总，高发射时钉死。
        # 引擎会给**叶子**子块按 fill 拉平高度（容器子块则用自己的内容高度，
        # 见探针 P3），所以叶子的发射高度必须写成容器内高，否则首次点击会跳。
        off = ind + b
        for c in vis:
            measure(c, None, ctx)
            c["_x"], c["_y"] = off, b
            off += c["_w"] + sp
        node["_w"] = ((off - sp) + b) if vis else (2 * b + ind)
        node["_h"] = 2 * b + max([c["_h"] for c in vis] or [0])
        for c in vis:
            if c["kind"] == "leaf":
                c["_h"] = node["_h"] - 2 * b
        tail = off
        for c in hid:
            measure(c, None, ctx)
            c["_x"], c["_y"] = tail, b + node["_h"]
            tail += c["_w"] + sp
    else:
        node["_w"] = forced_w or natural_w(node, ctx)
        inner = node["_w"] - 2 * b - ind
        y = b
        for c in vis:
            # 垂直容器把子块宽度撑满；但水平子容器会按自己的内容重算宽度。
            wide = (c["kind"] == "container" and c["axis"] == "h")
            measure(c, None if wide else inner, ctx)
            c["_x"], c["_y"] = ind + b, y
            y += c["_h"] + sp
        node["_h"] = ((y - sp) + b) if vis else (2 * b)
        tail = node["_h"] + b
        for c in hid:
            wide = (c["kind"] == "container" and c["axis"] == "h")
            measure(c, None if wide else inner, ctx)
            c["_x"], c["_y"] = ind + b, tail
            tail += c["_h"] + sp
    # 侧钉（movable=0）：不进栈、不计入父高，坐标由声明给定。
    for c in node.get("children", []):
        if c["spec"].get("pin"):
            measure(c, c["spec"].get("w"), ctx)
            c["_x"], c["_y"] = c["spec"]["pin"]


def layout(lay, graph, views):
    """递归版面 → 发射计划。坐标是**父相对**的（mxGeometry 语义）。"""
    root = resolve_layout(lay, graph["nodes"])
    ctx = layout_ctx(lay, graph, views, root)
    measure(root, None, ctx)
    root["_x"], root["_y"] = ROOT_X, ROOT_Y

    order, parent_of = [], {}

    def walk(n):
        order.append(n["id"])
        for c in n.get("children", []):
            parent_of[c["id"]] = n["id"]
            walk(c)
    walk(root)

    # 结构边：仍是「父节点 → 子节点」的语义层级（与版面树无关），保持原样
    nodes = graph["nodes"]
    root_ids = {n["id"] for n in nodes if n.get("parent") is None}
    structural = []
    for n in nodes:
        p = n.get("parent")
        if p is None or p in root_ids:
            continue
        structural.append({"from": p, "to": n["id"],
                           "id": "EX:%s->%s" % (p, n["id"])})
    semantic = []
    for e in graph["edges"]:
        semantic.append({"from": e["from"], "to": e["to"], "type": e["type"],
                         "exit": e.get("exit"), "entry": e.get("entry"),
                         "id": "E:%s->%s" % (e["from"], e["to"])})

    by_cid = {}

    def index(n):
        by_cid[n["id"]] = n
        for c in n.get("children", []):
            index(c)
    index(root)

    titles = {n["id"] for n in by_cid.values()
              if n["kind"] == "leaf" and n["spec"].get("role") == "title"}
    page_w = int(ROOT_X + root["_w"] + 120)
    page_h = int(ROOT_Y + root["_h"] + 220)
    return {"root": root, "by_cid": by_cid, "order": order,
            "parent_of": parent_of, "ctx": ctx, "titles": titles,
            "page_w": page_w, "page_h": page_h}, structural, semantic


def subtree_node_ids(node):
    """版面树里某个节点下面的全部 graph.json 节点 id（含自身若是叶子）。"""
    out = set()

    def walk(n):
        if n["kind"] == "leaf":
            out.add(n["id"])
        for c in n.get("children", []):
            walk(c)
    walk(node)
    return out


def edges_touching(ids, structural, semantic):
    out = []
    for e in semantic + structural:
        if e["from"] in ids or e["to"] in ids:
            out.append(e["id"])
    return sorted(out)


def container_toggles(plan, structural, semantic):
    """每个可折叠容器要 toggle 的 cell 列表，键 = 它的**标题节点 id**
    （与 views.json 的 expansion 对齐）。

    折叠态 = 只留标题条（Design Owner 2026-09-17 的决定：不再有「占满整条行带」
    的封面块）。所以只需要一条 `toggle` 动作作用在这组内容 cell 上 —— 隐藏一个
    容器 id 会级联到它的子孙（探针 P6），而 toggle 动词本身双向可用，一个链接
    展开/收起都管。边不是容器的子孙，必须显式列进来。
    """
    toggles = {}
    for node in plan["by_cid"].values():
        if node["kind"] != "container":
            continue
        title = None
        for c in node.get("children", []):
            if c["kind"] == "leaf" and c["spec"].get("role") == "title":
                title = c
        if title is None:
            continue
        cells = []
        for c in node.get("children", []):
            if c is title or c["spec"].get("pin") or not c["spec"].get("when"):
                continue
            cells.append(c["id"])
            cells.extend(edges_touching(subtree_node_ids(c),
                                        structural, semantic))
        if cells:
            toggles[title["id"]] = sorted(set(cells))
    return toggles


def class_of(node_id, assignment):
    for cls, members in assignment.items():
        if node_id in members:
            return cls
    return None


def lens_actions(scope, nodes, kinds, structural, semantic, mode, titles=()):
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
                if nid in titles:
                    fill, stroke = TITLE_FILL, TITLE_STROKE
                else:
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

def view_button_payload(view, scope_by_id, nodes, kinds, semantic, structural,
                        toggles, titles=()):
    acts = []
    lens_id = view.get("scopeLens", "keep")
    if lens_id == "clear":
        for s in scope_by_id.values():
            if s.get("lens"):
                acts.extend(lens_actions(s, nodes, kinds, structural, semantic,
                                         "clear", titles))
    elif lens_id not in (None, "keep"):
        acts.extend(lens_actions(scope_by_id[lens_id], nodes, kinds, structural,
                                 semantic, "apply", titles))
    exp = view.get("expansion") or {}
    for key in ("collapse", "expand"):
        for nid in exp.get(key, []):
            if nid not in toggles:
                sys.exit("error: view %s tries to %s %r, which is not a "
                         "collapsible node in layout.json" % (view["id"], key, nid))
    for nid in exp.get("collapse", []):
        acts.append({"hide": {"cells": toggles[nid]}})
    for nid in exp.get("expand", []):
        acts.append({"show": {"cells": toggles[nid]}})
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


def emit(graph, scopes, views, plan, structural, semantic, default_view):
    kinds = {n["id"]: n.get("kind", DEFAULT_KIND) for n in graph["nodes"]}
    gby = {n["id"]: n for n in graph["nodes"]}
    toggles = container_toggles(plan, structural, semantic)
    ctx = plan["ctx"]
    PAGE_W, PAGE_H = plan["page_w"], plan["page_h"]
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
                "七大层自上而下；每行是一个容器，点标题条上的 ⇕ 收起／展开 —— 收起时只留标题条，"
                "下方的行自动上移；展开时整行恢复、下方的行下移。层内再展开同样会让位。",
                "text;html=1;align=left;verticalAlign=top;fontSize=10;fontColor=#666666;",
                80, 92, 1080, 28))

    for i, v in enumerate(views["views"]):
        payload = view_button_payload(v, {s["id"]: s for s in scopes["scopes"]},
                                      graph["nodes"], kinds, semantic, structural,
                                      toggles, plan["titles"])
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

    # ---- nodes: 容器 + 叶子，按版面树 DFS 顺序（父先于子） -----------------
    hidden_nodes, hidden_edges = set(), set()
    for node in plan["by_cid"].values():
        for c in node.get("children", []):
            if not ctx["visible"](c):
                hidden_nodes |= subtree_node_ids(c)
    hidden_edges = set(edges_touching(hidden_nodes, structural, semantic))

    for cid in plan["order"]:
        n = plan["by_cid"][cid]
        parent = plan["parent_of"].get(cid, "Layer:Main")
        x, y, w, h = n["_x"], n["_y"], n["_w"], n["_h"]
        if n["kind"] == "container":
            indent = ("marginLeft=%d;" % n["indent"]) if n["indent"] else ""
            style = ("rounded=0;html=1;fillColor=none;strokeColor=%s;"
                     "childLayout=stackLayout;resizeParent=1;resizeParentMax=0;"
                     "horizontalStack=%d;stackSpacing=%d;stackBorder=%d;%s"
                     % (CONTAINER_STROKE, 1 if n["axis"] == "h" else 0,
                        ctx["spacing"], ctx["border"], indent))
            a(vertex(cid, "", style, x, y, w, h, parent))
            continue
        gn = gby[n["id"]]
        kind = gn.get("kind", DEFAULT_KIND)
        style = node_style(kind, n["spec"].get("role"))
        if n["spec"].get("pin"):
            style += "movable=0;"
        value = gn["label"]
        if n["id"] in toggles:
            value = "⇕ " + value      # 折叠把手：⇕ = 可收起 / 展开
        if gn.get("caption"):
            value += ("<br><font style='font-size:9px;color:#555555'>%s</font>"
                      % gn["caption"])
        link = None
        if n["id"] in toggles:
            link = action_link({"actions": [
                {"toggle": {"cells": toggles[n["id"]], "transient": False}}]})
        a(vertex(n["id"], value, style, x, y, w, h, parent, link=link,
                 visible=n["id"] not in hidden_nodes))

    # ---- edges: structural (faint) then semantic (typed) -----------------
    for e in structural:
        a(edge(e["id"], ANCHOR_STYLE, "Layer:Main", e["from"], e["to"],
               visible=e["id"] not in hidden_edges))
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
               visible=e["id"] not in hidden_edges, value=e.get("label", "")))

    a('      </root>\n')
    a('    </mxGraphModel>\n')
    a('  </diagram>\n')
    a('</mxfile>\n')
    return "".join(out)


# ---------------------------------------------------------------- main ----

def build(root):
    src = load_sources(root)
    graph, scopes, views = src["graph"], src["scopes"], src["views"]

    plan, structural, semantic = layout(load_layout(root), graph, views)
    xml = emit(graph, scopes, views, plan, structural, semantic,
               views["defaultView"])
    out_path = root / "generated" / "fcf-system-map.drawio"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    digest = hashlib.sha256(xml.encode("utf-8")).hexdigest()
    n_cont = sum(1 for n in plan["by_cid"].values() if n["kind"] == "container")
    n_cells = len(graph["nodes"]) + n_cont + len(structural) + len(semantic)
    print("wrote %s: %d nodes + %d containers, %d structural + %d semantic edges, "
          "%d cells total, sha256=%s" % (out_path, len(graph["nodes"]), n_cont,
                                         len(structural), len(semantic), n_cells,
                                         digest[:16]))
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(ROOT),
                    help="fcf-system-map root directory (contains the source JSONs)")
    ap.add_argument("--out", default=None,
                    help="override output path (default <root>/generated/fcf-system-map.drawio)")
    args = ap.parse_args()
    root = Path(args.root)
    if args.out:
        src = load_sources(root)
        graph, scopes, views = src["graph"], src["scopes"], src["views"]
        plan, structural, semantic = layout(load_layout(root), graph, views)
        xml = emit(graph, scopes, views, plan, structural, semantic,
                   views["defaultView"])
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(xml)
        print("wrote %s" % args.out)
    else:
        build(root)


if __name__ == "__main__":
    main()

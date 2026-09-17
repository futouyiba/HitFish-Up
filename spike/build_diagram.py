#!/usr/bin/env python3
"""FCF Canonical System Map — draw.io spike builder (deterministic, AI-only).

Inputs:  graph.json (nodes + hierarchy) and scopes.json (views + scope rules).
Output:  an uncompressed .drawio file built only from native draw.io mechanisms:

  * native layers for view scoping (layer visibility + Layers panel);
  * native custom actions (``data:action/json`` links) for interactive view
    switching and expand/collapse in the diagrams.net viewer;
  * stable cell ids derived from node ids (view-specific gray duplicates get
    a ``::<view>`` suffix).

The .drawio file is a build artifact: never hand-edit it. Edit the source JSON
and regenerate::

    python3 build_diagram.py
    python3 build_diagram.py --graph g.json --scopes s.json --out o.drawio

Determinism: no timestamps, no uuids, no randomness, fixed layout grid, fixed
attribute and emission order. Same inputs -> byte-identical output.

The custom-action link format used here was verified against the shipped
viewer source (viewer.diagrams.net ``viewer-static.min.js``)::

    data:action/json,{"actions":[
      {"show":   {"cells": ["<cell-or-layer-id>", ...]}},
      {"hide":   {"cells": [...]}}
    ]}

Referencing a *layer cell* id in show/hide flips only that layer's own
visibility flag, which composes orthogonally with per-cell collapse flags.
``toggle`` flips each listed cell's own visibility independently (edges must
be listed explicitly).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Fixed layout constants — "append-stable fixed-capacity grid".
#
#  * root sits at a fixed slot; every root child owns a fixed-width region;
#  * deeper children occupy fixed slots indexed by their position among
#    siblings (SLOT_DX apart, LEVEL_DY below the parent);
#  * therefore: renaming a node moves nothing; APPENDING a child adds a new
#    slot and moves nothing else; inserting between siblings shifts the later
#    siblings by one slot (documented rule, not attempted to be avoided).
#  * region capacity: REGION_W / SLOT_DX = 5 child slots per branch.
# --------------------------------------------------------------------------
ROOT_X, ROOT_Y, ROOT_W, NODE_H = 2350, 40, 260, 50
MARGIN_X, REGION_W = 80, 1200
SLOT_DX, LEVEL_DY, HEADER_DX = 240, 160, 40
GROUP_W, LEAF_W = 260, 200
BTN_X0, BTN_Y, BTN_W, BTN_H, BTN_DX = 80, 40, 150, 40, 170
TITLE_X, TITLE_W = 450, 900
HINT_Y = 96

GRAY_FILL, GRAY_STROKE, GRAY_FONT = "#f5f5f5", "#a6a6a6", "#8f8f8f"

BRANCH_COLORS = {
    "SPATIAL": ("#dae8fc", "#6c8ebf"),
    "CONDITION": ("#fff2cc", "#d6b656"),
    "RESPONSE": ("#d5e8d4", "#82b366"),
    "SELECTION": ("#e1d5e7", "#9673a6"),
}
ROOT_COLOR = ("#ffe6cc", "#d79b00")

EDGE_TMPL = (
    "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;"
    "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
    "jettySize=auto;orthogonalLoop=1;strokeColor=%s;strokeWidth=1.5;"
)


def xesc(s):
    """XML-escape an attribute value."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def branch_color(node_id):
    return BRANCH_COLORS.get(node_id.split(".")[0], ROOT_COLOR)


def node_style(node_id, gray=False):
    if gray:
        fill, stroke, font = GRAY_FILL, GRAY_STROKE, GRAY_FONT
    else:
        fill, stroke = branch_color(node_id)
        font = "#000000"
    return (
        "rounded=1;whiteSpace=wrap;html=1;fontSize=12;fontColor=%s;"
        "fillColor=%s;strokeColor=%s;" % (font, fill, stroke)
    )


def edge_style(target_node_id, gray=False):
    stroke = GRAY_STROKE if gray else branch_color(target_node_id)[1]
    return EDGE_TMPL % stroke


def action_link(payload):
    return "data:action/json," + json.dumps(payload, separators=(",", ":"))


# --------------------------------------------------------------------------
# Loading / validation
# --------------------------------------------------------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(graph, scopes):
    nodes = graph["nodes"]
    ids = [n["id"] for n in nodes]
    if len(ids) != len(set(ids)):
        sys.exit("error: duplicate node ids in graph.json")
    idset = set(ids)
    for n in nodes:
        p = n.get("parent")
        if p is not None and p not in idset:
            sys.exit("error: node %s references unknown parent %s" % (n["id"], p))
    layer_keys = set(scopes["layers"])
    for v in scopes["views"]:
        if v["layer"] not in layer_keys:
            sys.exit("error: view %s references unknown layer %s" % (v["id"], v["layer"]))
    defaults = [v for v in scopes["views"] if v.get("default")]
    if len(defaults) > 1:
        sys.exit("error: more than one default view")
    for r in scopes["rules"]:
        if not ({"id", "prefix"} & set(r["match"])):
            sys.exit("error: rule match must contain 'id' or 'prefix': %r" % (r,))
        for mode in r["views"].values():
            if mode is not None and mode not in ("normal", "gray"):
                sys.exit("error: unsupported mode %r in rule for %r" % (mode, r["match"]))


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

def layout(nodes):
    """Deterministic slot layout. Returns {node_id: (x, y, w, h)} and kids map."""
    kids, roots = {}, []
    for n in nodes:
        p = n.get("parent")
        if p is None:
            roots.append(n)
        else:
            kids.setdefault(p, []).append(n)

    pos = {}

    def place(n, x, y, depth):
        w = ROOT_W if depth == 0 else (GROUP_W if depth == 1 else LEAF_W)
        pos[n["id"]] = (x, y, w, NODE_H)
        for j, c in enumerate(kids.get(n["id"], [])):
            if depth == 0:
                # root children own fixed regions on the region grid
                place(c, MARGIN_X + j * REGION_W + HEADER_DX, y + LEVEL_DY, 1)
            else:
                place(c, x + j * SLOT_DX, y + LEVEL_DY, depth + 1)
        if depth >= 1 and len(kids.get(n["id"], [])) * SLOT_DX > REGION_W:
            sys.stderr.write(
                "warning: %s has more children than its region fits (%d slots)\n"
                % (n["id"], REGION_W // SLOT_DX)
            )

    for i, r in enumerate(roots):
        place(r, ROOT_X + i * REGION_W, ROOT_Y, 0)
    return pos, kids


def descendants(nid, kids):
    out = []
    for c in kids.get(nid, []):
        out.append(c["id"])
        out.extend(descendants(c["id"], kids))
    return out


# --------------------------------------------------------------------------
# Scope resolution / instance materialization
# --------------------------------------------------------------------------

def rule_matches(match, node_id):
    if "id" in match:
        return node_id == match["id"]
    return node_id.startswith(match["prefix"])


def resolve_views(node_id, scopes):
    """Returns {view_id: mode} for the views the node appears in."""
    rule = next((r for r in scopes["rules"] if rule_matches(r["match"], node_id)), None)
    spec = rule["views"] if rule else scopes.get("default_rule", {"views": {"*": "normal"}})["views"]
    out = {}
    for v in scopes["views"]:
        mode = spec.get(v["id"], spec.get("*"))
        if mode is not None:
            out[v["id"]] = mode
    return out


def build_instances(nodes, scopes):
    """One cell per (node, view it appears in). Nodes whose mode is 'normal'
    in every view get a single instance on the base layer and keep their bare
    node id as cell id (the stable-ID anchor)."""
    views = scopes["views"]
    default_view = next((v["id"] for v in views if v.get("default")), views[0]["id"])
    view_layer = {v["id"]: v["layer"] for v in views}

    cells = {}          # cell_id -> {node, view, gray, layer_key}
    node_map = {}       # node_id -> {view_id: (cell_id, mode)}

    for n in nodes:
        vm = resolve_views(n["id"], scopes)
        cmap = {}
        if set(vm.values()) == {"normal"} and len(vm) == len(views):
            cells[n["id"]] = {"node": n, "view": None, "gray": False, "layer": "base"}
            cmap = {vid: (n["id"], "normal") for vid in vm}
        else:
            for vid, mode in vm.items():
                cid = (
                    n["id"]
                    if (vid == default_view and mode == "normal")
                    else n["id"] + "::" + vid
                )
                cells[cid] = {"node": n, "view": vid, "gray": mode == "gray", "layer": view_layer[vid]}
                cmap[vid] = (cid, mode)
        node_map[n["id"]] = cmap

    return cells, node_map, default_view


def build_edges(nodes, scopes, node_map, cells, default_view):
    """Hierarchy edges as instances matching their endpoints' per-view cells."""
    view_layer = {v["id"]: v["layer"] for v in scopes["views"]}
    edges = {}  # cell_id -> {src, tgt, layer_key, gray, style}
    for n in nodes:
        p = n.get("parent")
        if p is None:
            continue
        emitted = set()
        for v in scopes["views"]:
            vid = v["id"]
            if vid not in node_map[n["id"]] or vid not in node_map[p]:
                continue
            src, _ = node_map[p][vid]
            tgt, mode = node_map[n["id"]][vid]
            if (src, tgt) in emitted:
                continue
            emitted.add((src, tgt))
            both_base = (
                cells[src]["layer"] == "base" and cells[tgt]["layer"] == "base"
            )
            if both_base:
                eid, layer = "E:%s->%s" % (p, n["id"]), "base"
            elif vid == default_view:
                eid, layer = "E:%s->%s" % (p, n["id"]), view_layer[vid]
            else:
                eid, layer = "E:%s->%s::%s" % (p, n["id"], vid), view_layer[vid]
            gray = mode == "gray"
            edges[eid] = {
                "src": src,
                "tgt": tgt,
                "layer": layer,
                "gray": gray,
                "style": edge_style(tgt.split("::")[0], gray),
            }
    return edges


# --------------------------------------------------------------------------
# XML emission
# --------------------------------------------------------------------------

def vertex_xml(cid, cell, pos, layer_id, label=None, link=None, style_extra=""):
    n = cell["node"]
    x, y, w, h = pos[n["id"]]
    style = node_style(n["id"], cell["gray"]) + style_extra
    label = n["label"] if label is None else label
    geo = (
        '            <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" />\n'
        % (x, y, w, h)
    )
    if link:
        return (
            '        <UserObject label="%s" link="%s" id="%s">\n'
            "          <mxCell style=\"%s\" vertex=\"1\" parent=\"%s\">\n"
            "%s"
            "          </mxCell>\n"
            "        </UserObject>\n" % (xesc(label), xesc(link), xesc(cid), xesc(style), xesc(layer_id), geo)
        )
    return (
        '        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">\n'
        "%s"
        "        </mxCell>\n" % (xesc(cid), xesc(label), xesc(style), xesc(layer_id), geo)
    )


def edge_xml(eid, e, layer_id):
    return (
        '        <mxCell id="%s" style="%s" edge="1" parent="%s" source="%s" target="%s">\n'
        '            <mxGeometry relative="1" as="geometry" />\n'
        "        </mxCell>\n"
        % (xesc(eid), xesc(e["style"]), xesc(layer_id), xesc(e["src"]), xesc(e["tgt"]))
    )


def text_cell_xml(cid, value, style, x, y, w, h):
    return (
        '        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">\n'
        '            <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" />\n'
        "        </mxCell>\n"
        % (xesc(cid), xesc(value), xesc(style), "Layer:Controls", x, y, w, h)
    )


def emit(graph, scopes, cells, edges, node_map, pos, kids, default_view):
    layer_ids = {k: m["id"] for k, m in scopes["layers"].items()}
    visible_keys = {"controls", "base"} | {v["layer"] for v in scopes["views"] if v["id"] == default_view}

    # collapse payloads for collapsible nodes (all instances of the subtree:
    # vertices + their edges, across all views)
    collapse_links = {}
    for n in graph["nodes"]:
        if not n.get("collapsible"):
            continue
        ids = []
        for d in descendants(n["id"], kids):
            ids.extend(cid for cid, _ in node_map[d].values())
            ids.extend(eid for eid, e in edges.items() if e["tgt"].split("::")[0] == d)
        ids = list(dict.fromkeys(ids))
        collapse_links[n["id"]] = action_link({"actions": [{"toggle": {"cells": ids}}]})

    out = []
    a = out.append
    a('<?xml version="1.0" encoding="UTF-8"?>\n')
    a('<mxfile host="fcf-spike" agent="build_diagram.py" version="26.0.0" type="device">\n')
    a('  <diagram id="fcf-spike-map-001" name="FCF System Map">\n')
    a(
        '    <mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" '
        'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2400" '
        'pageHeight="1200" math="0" shadow="0">\n'
    )
    a("      <root>\n")
    a('        <mxCell id="0" />\n')
    a('        <mxCell id="1" parent="0" />\n')

    # layers (order: controls, base, then one per view)
    for key in ["controls", "base"] + [v["layer"] for v in scopes["views"]]:
        meta = scopes["layers"][key]
        vis = "" if key in visible_keys else ' visible="0"'
        a(
            '        <mxCell id="%s" value="%s" parent="0"%s />\n'
            % (xesc(meta["id"]), xesc(meta["label"]), vis)
        )

    # control cells
    a(
        text_cell_xml(
            "CTRL:TITLE",
            "FCF Canonical System Map — Spike (AI-generated from graph.json; do not hand-edit)",
            "text;html=1;align=left;verticalAlign=middle;fontSize=15;fontStyle=1;",
            TITLE_X,
            BTN_Y,
            TITLE_W,
            BTN_H,
        )
    )
    a(
        text_cell_xml(
            "CTRL:HINT",
            "Views: click a view button. Expand/collapse: click the Spatial Opportunity box. "
            "Runs on native draw.io custom actions in the diagrams.net viewer.",
            "text;html=1;align=left;verticalAlign=top;fontSize=10;fontColor=#666666;",
            BTN_X0,
            HINT_Y,
            700,
            30,
        )
    )
    BTN_STYLES = {
        v["id"]: ("#dae8fc", "#6c8ebf") if v["id"] == default_view else ("#d5e8d4", "#82b366")
        for v in scopes["views"]
    }
    for i, v in enumerate(scopes["views"]):
        others = [layer_ids[vv["layer"]] for vv in scopes["views"] if vv["id"] != v["id"]]
        own = layer_ids[v["layer"]]
        link = action_link(
            {"actions": [{"hide": {"cells": others}}, {"show": {"cells": [own]}}]}
        )
        fill, stroke = BTN_STYLES[v["id"]]
        style_extra = (
            "fillColor=%s;strokeColor=%s;strokeWidth=2;fontStyle=1;" % (fill, stroke)
            if v["id"] == default_view
            else "fillColor=%s;strokeColor=%s;" % (fill, stroke)
        )
        geo = (
            BTN_X0 + i * BTN_DX,
            BTN_Y,
            BTN_W,
            BTN_H,
        )
        a(
            '        <UserObject label="%s" link="%s" id="%s">\n'
            '          <mxCell style="rounded=1;whiteSpace=wrap;html=1;fontSize=13;%s" vertex="1" parent="Layer:Controls">\n'
            '            <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" />\n'
            "          </mxCell>\n"
            "        </UserObject>\n"
            % (
                xesc(v["label"]),
                xesc(link),
                xesc("BTN:VIEW:%s" % v["id"]),
                xesc(style_extra),
                geo[0],
                geo[1],
                geo[2],
                geo[3],
            )
        )

    # node instances (emission order: nodes array order, then views order;
    # single-instance nodes map to the same cell id in every view -> dedupe)
    for n in graph["nodes"]:
        cmap = node_map[n["id"]]
        for cid in dict.fromkeys(c for c, _ in cmap.values()):
            cell = cells[cid]
            link = collapse_links.get(n["id"])
            label = None
            style_extra = ""
            if link:
                label = (
                    "%s<br><font style='font-size:9px;color:#555555'>click to expand / collapse</font>"
                    % n["label"]
                )
                style_extra = "strokeWidth=2;"
            a(vertex_xml(cid, cell, pos, layer_ids[cell["layer"]], label=label, link=link, style_extra=style_extra))

    # edge instances
    for eid, e in edges.items():
        a(edge_xml(eid, e, layer_ids[e["layer"]]))

    a("      </root>\n")
    a("    </mxGraphModel>\n")
    a("  </diagram>\n")
    a("</mxfile>\n")
    return "".join(out)


# --------------------------------------------------------------------------

def main():
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--graph", default=str(here / "graph.json"))
    ap.add_argument("--scopes", default=str(here / "scopes.json"))
    ap.add_argument("--out", default=str(here / "fcf-spike.drawio"))
    args = ap.parse_args()

    graph = load_json(args.graph)
    scopes = load_json(args.scopes)
    validate(graph, scopes)

    pos, kids = layout(graph["nodes"])
    cells, node_map, default_view = build_instances(graph["nodes"], scopes)
    edges = build_edges(graph["nodes"], scopes, node_map, cells, default_view)

    xml = emit(graph, scopes, cells, edges, node_map, pos, kids, default_view)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)

    digest = hashlib.sha256(xml.encode("utf-8")).hexdigest()
    print(
        "wrote %s: %d nodes -> %d vertex cells, %d edge cells, %d layers "
        "(default view: %s) sha256=%s"
        % (
            args.out,
            len(graph["nodes"]),
            len(cells),
            len(edges),
            len(scopes["layers"]),
            default_view,
            digest[:16],
        )
    )


if __name__ == "__main__":
    main()

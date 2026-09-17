#!/usr/bin/env python3
"""FCF Canonical System Map — build validation (Production Pilot v0.1).

Covers Production Pilot validation items 1-6 statically; items 7-10 are
runtime viewer checks (see build/viewer-harness.html and README.md).

Checks:
  1.  all stable IDs unique (and syntactically safe: no '::', '->', ':',
      no reserved prefixes)                              [spec item 1]
  2.  all edge endpoints exist                           [spec item 2]
  3.  scope assignments / views / contracts reference existing nodes
                                                         [spec item 3]
  4.  parent links exist and are acyclic                 [spec item 4]
  5.  same-source consecutive builds are byte-stable, and the committed
      generated/fcf-system-map.drawio is up to date      [spec item 5]
  6.  renaming a display label does not change any stable cell ID or
      geometry                                           [spec item 6]
  +  schema sanity: edge types, scope classes, view lenses, contract refs,
     lane names, collapsible targets, single-instance guarantee.
"""

import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BUILDER = HERE / "build_diagram.py"

RESERVED_PREFIXES = ("E:", "EX:", "BTN:", "CTRL:", "LEG:", "Layer:")
ID_RE = re.compile(r"^[A-Z][A-Z0-9_]*(\.[A-Z0-9_]+)*$")
EDGE_TYPES = {"DATA_FLOW", "CONTROL_OR_SELECTION", "REFERENCE_OR_CONFIG",
              "RETENTION", "ANCHOR"}
CLASSES = {"ACTIVE", "BOUNDARY", "OUT"}

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
    return cond


def load(name):
    with open(ROOT / name, "r", encoding="utf-8") as f:
        return json.load(f)


def run_builder(out_path):
    r = subprocess.run([sys.executable, str(BUILDER), "--out", str(out_path)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        failures.append("builder failed: %s" % r.stderr.strip())
        return False
    return True


def cells_of(drawio_path):
    """{cell_id: (label, parent, geometry)} for the generated file."""
    root = ET.parse(str(drawio_path)).getroot()
    out = {}
    for mx in root.iter("mxCell"):
        cid = mx.get("id")
        if cid in (None, "0", "1"):
            continue
        geo = mx.find("mxGeometry")
        g = None
        if geo is not None:
            g = tuple((k, geo.get(k)) for k in ("x", "y", "width", "height", "relative")
                      if geo.get(k) is not None)
        out[cid] = (mx.get("value"), mx.get("parent"), g)
    for uo in root.iter("UserObject"):
        mx = uo.find("mxCell")
        geo = mx.find("mxGeometry")
        g = tuple((k, geo.get(k)) for k in ("x", "y", "width", "height", "relative")
                  if geo.get(k) is not None)
        out[uo.get("id")] = (uo.get("label"), mx.get("parent"), g)
    return out


def main():
    graph, scopes, views, contracts = (load("graph.json"), load("scopes.json"),
                                       load("views.json"), load("contracts.json"))
    nodes = graph["nodes"]
    ids = [n["id"] for n in nodes]
    idset = set(ids)

    # -- 1. unique + syntactically safe stable IDs -------------------------
    check(len(ids) == len(idset), "duplicate node ids: %s" % sorted(i for i in ids if ids.count(i) > 1))
    for nid in ids:
        check(bool(ID_RE.match(nid)), "id violates naming scheme: %r" % nid)
        check(not any(nid.startswith(p) for p in RESERVED_PREFIXES),
              "id uses reserved prefix: %r" % nid)
        check("::" not in nid and "->" not in nid, "id contains reserved separator: %r" % nid)

    # -- label language: every cell must carry Chinese (Design Owner rule) ---
    CJK = re.compile(u"[一-鿿]")
    for n in nodes:
        check(bool(CJK.search(n.get("label", ""))),
              "%s: label has no Chinese — every cell must have a Chinese label (%r)"
              % (n["id"], n.get("label")))

    # -- 4. parents exist, no cycles ---------------------------------------
    by_id = {n["id"]: n for n in nodes}
    for n in nodes:
        p = n.get("parent")
        if p is not None:
            check(p in idset, "%s: unknown parent %r" % (n["id"], p))
    for nid in ids:
        seen, cur = set(), nid
        while cur is not None:
            check(cur not in seen, "parent cycle at %r" % nid)
            if cur in seen:
                break
            seen.add(cur)
            cur = by_id.get(cur, {}).get("parent")

    # -- lanes --------------------------------------------------------------
    for n in nodes:
        check(n.get("lane") in ("main", "r1", "r2", "r3", "r4", "r5", "r6", "r7"),
              "%s: unknown lane %r" % (n["id"], n.get("lane")))
    for n in nodes:
        if n.get("collapsible"):
            check(any(c.get("parent") == n["id"] for c in nodes),
                  "%s marked collapsible but has no children" % n["id"])

    # -- 2. edge endpoints + types ------------------------------------------
    seen_pairs = set()
    for e in graph["edges"]:
        check(e["from"] in idset, "edge from unknown node %r" % e["from"])
        check(e["to"] in idset, "edge to unknown node %r" % e["to"])
        check(e["type"] in EDGE_TYPES, "edge %r->%r illegal type %r" % (e["from"], e["to"], e["type"]))
        pair = (e["from"], e["to"])
        check(pair not in seen_pairs, "duplicate edge pair %r" % (pair,))
        seen_pairs.add(pair)
    # structural hierarchy must not duplicate a semantic edge between same pair
    for n in nodes:
        p = n.get("parent")
        if p is not None:
            check((p, n["id"]) not in seen_pairs,
                  "hierarchy pair %r->%r also declared as semantic edge" % (p, n["id"]))

    # -- 3. scope assignments reference existing nodes, exactly once --------
    for s in scopes["scopes"]:
        if s.get("lens"):
            assignment = s.get("assignment", {})
            classified = [nid for members in assignment.values() for nid in members]
            check(sorted(classified) == sorted(ids),
                  "scope %s: classification mismatch (missing=%s extra=%s)"
                  % (s["id"], sorted(set(ids) - set(classified)),
                     sorted(set(classified) - set(ids))))
            overlap = {nid for nid in classified if classified.count(nid) > 1}
            check(not overlap, "scope %s: nodes in multiple classes: %s" % (s["id"], sorted(overlap)))
            for cls, members in assignment.items():
                check(cls in CLASSES, "scope %s: illegal class %r" % (s["id"], cls))
                for nid in members:
                    check(nid in idset, "scope %s: unknown node %r" % (s["id"], nid))

    # -- views ----------------------------------------------------------------
    view_ids = [v["id"] for v in views["views"]]
    check(len(view_ids) == len(set(view_ids)), "duplicate view ids")
    check(views["defaultView"] in view_ids, "defaultView %r not among views" % views["defaultView"])
    lensed_ids = {s["id"] for s in scopes["scopes"] if s.get("lens")}
    all_scope_ids = {s["id"] for s in scopes["scopes"]}
    for v in views["views"]:
        lens = v.get("scopeLens", "keep")
        check(lens in ("clear", "keep") or lens in lensed_ids,
              "view %s: scopeLens %r is not a lens scope" % (v["id"], lens))
        check(lens not in all_scope_ids or lens in lensed_ids,
              "view %s: scopeLens %r points at a non-lens scope" % (v["id"], lens))
        exp = v.get("expansion") or {}
        for key in ("collapse", "expand"):
            for nid in exp.get(key, []):
                check(nid in idset, "view %s: %s target %r unknown" % (v["id"], key, nid))
                check(by_id.get(nid, {}).get("collapsible"),
                      "view %s: %s target %r is not collapsible" % (v["id"], key, nid))

    # -- contracts -------------------------------------------------------------
    statuses = {"linked", "pending"}
    for c in contracts["contracts"]:
        check(c["semanticId"] in idset, "contract for unknown node %r" % c["semanticId"])
        check(c["status"] in statuses, "contract %r illegal status %r" % (c["semanticId"], c["status"]))
        ref = c.get("authorityRef")
        check(ref is None or ref.startswith("https://"),
              "contract %r authorityRef must be https or null" % c["semanticId"])

    # -- page containment: EVERY vertex (nodes AND controls) must fit the page --
    # 构建器只对主图节点做越界检查；控件（标题/按钮/图例）是硬编码坐标，
    # 之前漏检过——这里对最终产物做一次全量检查。
    _root = ET.parse(str(ROOT / "generated" / "fcf-system-map.drawio")).getroot()
    _model = _root.find(".//mxGraphModel")
    if _model is not None:
        pw, ph = int(_model.get("pageWidth")), int(_model.get("pageHeight"))
        for mx in _root.iter("mxCell"):
            geo = mx.find("mxGeometry")
            if geo is None or mx.get("vertex") != "1":
                continue
            try:
                gx, gy = int(geo.get("x")), int(geo.get("y"))
                gw, gh = int(geo.get("width")), int(geo.get("height"))
            except (TypeError, ValueError):
                continue
            if gx + gw > pw or gy + gh > ph or gx < 0 or gy < 0:
                failures.append("%s overflows the page: (%d,%d)+%dx%d vs page %dx%d"
                                % (mx.get("id"), gx, gy, gw, gh, pw, ph))

    # -- 5. determinism + freshness of the committed artifact ------------------
    if not failures:
        with tempfile.TemporaryDirectory() as td:
            a, b = Path(td) / "a.drawio", Path(td) / "b.drawio"
            if run_builder(a) and run_builder(b):
                check(a.read_bytes() == b.read_bytes(),
                      "consecutive builds differ (non-deterministic output)")
                committed = (ROOT / "generated" / "fcf-system-map.drawio")
                check(committed.exists(), "generated/fcf-system-map.drawio missing")
                if committed.exists():
                    check(committed.read_bytes() == a.read_bytes(),
                          "generated/fcf-system-map.drawio is stale — rebuild and commit")

                # -- 6. rename does not move stable IDs or geometry ----------
                g2 = json.loads(json.dumps(graph))
                for n in g2["nodes"]:
                    n["label"] = n["label"] + " (renamed)"
                # rename every label, rebuild in an isolated temp root, compare
                tmp_root = Path(td) / "root"
                tmp_root.mkdir(parents=True)
                for fname in ("graph.json", "scopes.json", "views.json", "contracts.json"):
                    srcj = g2 if fname == "graph.json" else load(fname)
                    (tmp_root / fname).write_text(
                        json.dumps(srcj, ensure_ascii=False, indent=2), encoding="utf-8")
                (tmp_root / "build").symlink_to(HERE, target_is_directory=True)
                r = subprocess.run(
                    [sys.executable, str(tmp_root / "build" / "build_diagram.py"),
                     "--root", str(tmp_root), "--out", str(Path(td) / "renamed.drawio")],
                    capture_output=True, text=True)
                if r.returncode != 0:
                    failures.append("renamed build failed: %s" % r.stderr.strip())
                else:
                    base, ren = cells_of(a), cells_of(Path(td) / "renamed.drawio")
                    check(set(base) == set(ren),
                          "rename changed cell ID set: %s"
                          % sorted(set(base) ^ set(ren)))
                    diff = [cid for cid in base
                            if cid in ren and base[cid][2] != ren[cid][2]]
                    check(not diff, "rename moved geometry for %s" % diff)
                    semantic_cells = [cid for cid in base if not cid.startswith(
                        ("E:", "EX:", "BTN:", "CTRL:", "LEG:", "Layer:"))]
                    label_diff = [cid for cid in semantic_cells
                                  if cid in ren and base[cid][0] == ren[cid][0]]
                    check(not label_diff,
                          "rename did not propagate to labels: %s" % label_diff)

    # ---------------------------------------------------------------- report
    stable_count = len(ids)
    if failures:
        print("VALIDATION: FAIL (%d)" % len(failures))
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("VALIDATION: PASS")
    print("  stable IDs:            %d (unique, syntax-safe)" % stable_count)
    root_ids = {n["id"] for n in nodes if n.get("parent") is None}
    drawn_structural = [n for n in nodes if n.get("parent") and n["parent"] not in root_ids]
    print("  edges:                 %d semantic + %d structural (root->row edges not drawn), endpoints ok"
          % (len(graph["edges"]), len(drawn_structural)))
    print("  views:                 %s (default %s)"
          % (", ".join(view_ids), views["defaultView"]))
    lensed = [s for s in scopes["scopes"] if s.get("lens")]
    if lensed:
        s = lensed[0]
        a = s["assignment"]
        print("  scope lens:            %s — %d ACTIVE / %d BOUNDARY / %d OUT, all nodes classified once"
              % (s["id"], len(a.get("ACTIVE", [])), len(a.get("BOUNDARY", [])), len(a.get("OUT", []))))
    declared = [s["id"] for s in scopes["scopes"] if s.get("status") == "DECLARED-UNASSIGNED"]
    if declared:
        print("  ladder declared, unassigned: %s" % ", ".join(declared))
    print("  contracts:             %d entries (refs valid)"
          % len(contracts["contracts"]))
    print("  determinism:           consecutive builds byte-identical; committed artifact fresh")
    print("  rename stability:      cell ID set and geometry invariant under label rename")


if __name__ == "__main__":
    main()

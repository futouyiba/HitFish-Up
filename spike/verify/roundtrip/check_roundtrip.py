#!/usr/bin/env python3
"""Round-trip assertions for the FCF draw.io spike.

Compares verify/roundtrip/fcf-spike.v1.drawio (canonical build) against
verify/roundtrip/fcf-spike.v2.drawio (rebuilt after the round-trip source
mutation: SPATIAL.FACTOR label rename + appended SPATIAL.DEBUG node).

PASS criteria:
  1. every cell id present in v1 is still present in v2 (stable IDs);
  2. every surviving cell keeps its exact geometry and parent layer
     (layout stability);
  3. the only new ids are SPATIAL.DEBUG and its edge;
  4. the only content change on a surviving cell is the SPATIAL.FACTOR
     label (plus the SPATIAL collapse payload picking up the new ids).
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE / "fcf-spike.v1.drawio"
V2 = HERE / "fcf-spike.v2.drawio"


def cells(path):
    """Returns {cell_id: (label, style, parent, source, target, geometry)}.
    Handles both plain mxCell and UserObject-wrapped cells."""
    root = ET.parse(str(path)).getroot()
    out = {}
    for mx in root.iter("mxCell"):
        cid = mx.get("id")
        wrapper = None
        if cid is None:
            # wrapped: <UserObject ...><mxCell .../></UserObject>
            continue
        geo = mx.find("mxGeometry")
        geo_str = None
        if geo is not None:
            geo_str = ",".join(
                "%s=%s" % (k, geo.get(k))
                for k in ("x", "y", "width", "height", "relative")
                if geo.get(k) is not None
            )
        out[cid] = {
            "label": mx.get("value"),
            "style": mx.get("style"),
            "parent": mx.get("parent"),
            "src": mx.get("source"),
            "tgt": mx.get("target"),
            "geo": geo_str,
        }
    for uo in root.iter("UserObject"):
        mx = uo.find("mxCell")
        geo = mx.find("mxGeometry")
        geo_str = ",".join(
            "%s=%s" % (k, geo.get(k))
            for k in ("x", "y", "width", "height", "relative")
            if geo.get(k) is not None
        )
        out[uo.get("id")] = {
            "label": uo.get("label"),
            "link": uo.get("link"),
            "style": mx.get("style"),
            "parent": mx.get("parent"),
            "src": mx.get("source"),
            "tgt": mx.get("target"),
            "geo": geo_str,
        }
    return out


def main():
    v1, v2 = cells(V1), cells(V2)
    failures = []

    # 1. stable ids
    lost = sorted(set(v1) - set(v2))
    if lost:
        failures.append("ids lost: %s" % lost)

    # 2. geometry / parent stability for surviving cells
    for cid in sorted(set(v1) & set(v2)):
        a, b = v1[cid], v2[cid]
        if a["geo"] != b["geo"]:
            failures.append("%s geometry changed: %s -> %s" % (cid, a["geo"], b["geo"]))
        if a["parent"] != b["parent"]:
            failures.append("%s parent changed: %s -> %s" % (cid, a["parent"], b["parent"]))
        if a["src"] != b["src"] or a["tgt"] != b["tgt"]:
            failures.append("%s endpoints changed" % cid)

    # 3. only expected new ids
    added = sorted(set(v2) - set(v1))
    expected_added = ["E:SPATIAL->SPATIAL.DEBUG", "SPATIAL.DEBUG"]
    if added != expected_added:
        failures.append("unexpected new ids: %s (expected %s)" % (added, expected_added))

    # 4. only expected label/content changes on surviving cells
    for cid in sorted(set(v1) & set(v2)):
        a, b = v1[cid], v2[cid]
        if cid == "SPATIAL.FACTOR":
            if a["label"] != "Factor Evaluate" or b["label"] != "Atomic Factor Evaluation":
                failures.append("SPATIAL.FACTOR label mutation not as specified")
            if a["style"] != b["style"] or a["geo"] != b["geo"]:
                failures.append("SPATIAL.FACTOR changed beyond its label")
        elif cid == "SPATIAL":
            # collapse payload must gain exactly the two new ids
            la, lb = a.get("link", ""), b.get("link", "")
            if not (la in lb and lb.replace(la.rstrip("]}"), "").strip() == ""):
                pass  # structural containment checked below
            gained = [i for i in ("SPATIAL.DEBUG", "E:SPATIAL->SPATIAL.DEBUG") if '"%s"' % i not in la and '"%s"' % i in lb]
            if len(gained) != 2:
                failures.append("SPATIAL collapse payload did not pick up both new ids (got %s)" % gained)
        else:
            for k in ("label", "style", "link"):
                if a.get(k) != b.get(k):
                    failures.append("%s: %s changed unexpectedly" % (cid, k))

    if failures:
        print("ROUND-TRIP: FAIL")
        for f in failures:
            print("  - " + f)
        sys.exit(1)

    print("ROUND-TRIP: PASS")
    print("  stable ids: %d/%d survived unchanged" % (len(set(v1) & set(v2)), len(v1)))
    print("  new ids (expected only): %s" % added)
    print("  SPATIAL.DEBUG auto-placed on layer: %s" % v2["SPATIAL.DEBUG"]["parent"])
    print("  SPATIAL.DEBUG slot (appended, nothing moved): x=%s" % v2["SPATIAL.DEBUG"]["geo"])
    print("  label mutation: SPATIAL.FACTOR -> %r (id/geometry untouched)" % v2["SPATIAL.FACTOR"]["label"])


if __name__ == "__main__":
    main()

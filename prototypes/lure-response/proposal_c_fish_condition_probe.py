"""Proposal C working probe: Fish Condition block resolution.

Implements the resolution rules in
docs/proposals/lure-response-proposal-c-fish-condition-production-contract.md:
baseline + authorized overlay, expiry -> Unknown, no stale values.

Run: python3 -I prototypes/lure-response/proposal_c_fish_condition_probe.py
"""

from __future__ import annotations

import math

RESOLVED = "Resolved"
UNKNOWN = "Unknown"
NOT_CONFIGURED = "NotConfigured"
INVALID = "InvalidInput"

AUTHORIZED = {"wariness"}


def _valid_number(v, lo=None, hi=None) -> bool:
    if not isinstance(v, (int, float)) or not math.isfinite(v):
        return False
    if lo is not None and v < lo:
        return False
    if hi is not None and v > hi:
        return False
    return True


def _covers(validity, now) -> bool:
    return validity[0] <= now <= validity[1]


def resolve(block, now, overlay=None):
    """Return {condition: (status, value)}."""
    out = {}
    if not block.get("version") or not _covers(block["validity"], now):
        return {name: (UNKNOWN, None) for name in block["conditions"]}

    for name, item in block["conditions"].items():
        status = item.get("status", RESOLVED)
        value = item.get("value")
        if status != RESOLVED or item.get("sourceRef") is None:
            out[name] = (UNKNOWN, None)
            continue
        out[name] = (RESOLVED, value)

    if overlay is None:
        return out

    name = overlay["condition"]
    if name not in AUTHORIZED:
        out[name] = (INVALID, None)
        return out
    if name not in out:
        return out
    if not _covers(overlay["validity"], now):
        return out  # expired overlay: fall back to baseline
    delta = overlay.get("delta", 0.0)
    if not _valid_number(delta):
        out[name] = (INVALID, None)
        return out
    status, base = out[name]
    if status != RESOLVED:
        return out
    merged = base + delta
    if not _valid_number(merged, 0.0, 1.0):
        out[name] = (INVALID, None)
    else:
        out[name] = (RESOLVED, merged)
    return out


def main() -> None:
    now = 10.0
    block = {
        "version": "v1",
        "validity": (0.0, 20.0),
        "conditions": {
            "activity": {"value": 1.2, "status": RESOLVED, "sourceRef": "bake:1"},
            "feedingMotivation": {"value": 0.5, "status": RESOLVED, "sourceRef": "bake:1"},
            "wariness": {"value": 0.3, "status": RESOLVED, "sourceRef": "bake:1"},
        },
    }

    print("baseline:", resolve(block, now))
    expired_block = dict(block, validity=(0.0, 5.0))
    print("expired block:", resolve(expired_block, now))

    missing_source = {
        **block,
        "conditions": {**block["conditions"], "activity": {"value": 1.2, "status": RESOLVED}},
    }
    print("missing source:", resolve(missing_source, now))

    good_overlay = {"condition": "wariness", "delta": 0.2, "validity": (5.0, 15.0)}
    print("authorized overlay:", resolve(block, now, good_overlay))

    bad_overlay = {"condition": "activity", "delta": 0.2, "validity": (5.0, 15.0)}
    print("unauthorized overlay:", resolve(block, now, bad_overlay))

    stale_overlay = {"condition": "wariness", "delta": 0.2, "validity": (0.0, 5.0)}
    print("stale overlay:", resolve(block, now, stale_overlay))

    overflow_overlay = {"condition": "wariness", "delta": 0.9, "validity": (5.0, 15.0)}
    print("overflow overlay:", resolve(block, now, overflow_overlay))

    r = resolve(block, now)
    assert r["activity"] == (RESOLVED, 1.2)
    assert r["wariness"] == (RESOLVED, 0.3)

    assert resolve(expired_block, now)["activity"] == (UNKNOWN, None)
    assert resolve(missing_source, now)["activity"] == (UNKNOWN, None)

    merged = resolve(block, now, good_overlay)
    assert merged["wariness"] == (RESOLVED, 0.5)
    assert merged["activity"] == (RESOLVED, 1.2)

    assert resolve(block, now, bad_overlay)["activity"] == (INVALID, None)
    assert resolve(block, now, stale_overlay)["wariness"] == (RESOLVED, 0.3)
    assert resolve(block, now, overflow_overlay)["wariness"] == (INVALID, None)

    # Expired block must not reuse last values.
    assert resolve(dict(block, validity=(0.0, 20.0)), 25.0)["wariness"] == (UNKNOWN, None)

    print("Fish Condition resolution probe passed")


if __name__ == "__main__":
    main()

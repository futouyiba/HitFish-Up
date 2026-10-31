"""Proposal C working probe: end-to-end response chain.

Toy implementation of docs/proposals/lure-response-proposal-c-response-algorithm-v1.md.
Checks status propagation, sibling max with provenance, interval support handling,
Reject composition, cast-snapshot selection and the single L×C multiply.

2026-10-30 direction: no latent bearing; closing cost is K_close * q^2 * activity
with no angle average (K_close rescaled from 0.76 to 0.19 on the same cost scale).

Run: python3 -I prototypes/lure-response/proposal_c_end_to_end_probe.py
"""

from __future__ import annotations

import math

M0, M1 = 0.0, 0.40
K_CLOSE = 0.19  # no-theta rescale: was 0.76 under bearing averaging (x 1/4)
TRIGGER_BUDGET = 0.10
K_WARY = 1.0

RESOLVED = "Resolved"
UNKNOWN = "Unknown"
NOT_CONFIGURED = "NotConfigured"
RI = "ResolutionIncomplete"
REJECT = "Reject"
INVALID = "InvalidInput"


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def threshold(m: float) -> float:
    base = 0.60 - 0.40 * m
    if m > 0.80:
        base -= 0.50 * (m - 0.80)
    return base


def _finite(x) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(x)


def activity_multiplier(activity):
    if activity in (UNKNOWN, NOT_CONFIGURED):
        return RI, None
    if not _finite(activity) or activity < 0:
        return INVALID, None
    return RESOLVED, float(activity)


def conditional_c(food, trigger, activity, q, risk, motivation) -> float:
    cost = K_CLOSE * q * q * activity
    margin = food + trigger - cost - risk - threshold(motivation)
    if not math.isfinite(margin):
        return None
    return clamp01((margin - M0) / (M1 - M0))


def normalize_support(support):
    """value | (lo, hi) | status -> (status, value)."""
    if isinstance(support, tuple):
        lo, hi = support
        if lo == hi:
            return RESOLVED, float(lo)
        return RI, None
    if support == REJECT:
        return REJECT, 0.0
    if support in (UNKNOWN, NOT_CONFIGURED):
        return RI, None
    if support == INVALID:
        return INVALID, None
    if not _finite(support) or not 0.0 <= support <= 1.0:
        return INVALID, None
    return RESOLVED, float(support)


def prey_response(support, state, food, activity, q, risk, motivation):
    """Return (status, C_prey or None)."""
    status, value = normalize_support(support)
    if status != RESOLVED:
        return status, value
    if state == REJECT:
        return REJECT, 0.0
    if state in (UNKNOWN, NOT_CONFIGURED):
        return RI, None
    if not _finite(state) or not 0.0 <= state <= 1.0:
        return INVALID, None
    for item in (food, q, risk, motivation):
        if not _finite(item):
            return INVALID, None
    act_status, mult = activity_multiplier(activity)
    if act_status != RESOLVED:
        return act_status, None
    trigger = TRIGGER_BUDGET * state
    c = conditional_c(food, trigger, mult, q, risk, motivation)
    if c is None:
        return INVALID, None
    return RESOLVED, value * c


def compose(results):
    """results: {family: (status, value)} -> (status, C_feed, skipped{family: status})."""
    resolved = [v for s, v in results.values() if s == RESOLVED]
    rejected = [v for s, v in results.values() if s == REJECT]
    skipped = {f: s for f, (s, _) in results.items()
               if s in (RI, UNKNOWN, NOT_CONFIGURED)}
    if any(s == INVALID for s, _ in results.values()):
        return INVALID, None, skipped
    if not resolved and rejected:
        return REJECT, 0.0, skipped
    if not resolved and not rejected:
        return RI, None, skipped
    return RESOLVED, max(resolved + rejected), skipped


def cast_entry(cast_fc, cast_id, group, mode):
    """Mirror the algorithm's snapshot selection."""
    if not cast_fc:
        return None
    if cast_fc.get("castId") != cast_id:
        return None
    if not cast_fc.get("blockVersion") or not cast_fc.get("formedAt"):
        return None
    return cast_fc.get("entries", {}).get((group, mode))


def join(c_feed, L, skipped):
    if c_feed is None or L is None:
        return RI, None, skipped
    if L in (UNKNOWN, NOT_CONFIGURED):
        return RI, None, skipped
    if L == INVALID:
        return INVALID, None, skipped
    if not _finite(L) or L < 0:
        return INVALID, None, skipped
    return RESOLVED, L * c_feed, skipped


def main() -> None:
    print("end-to-end scenarios")
    base = dict(food=0.70, activity=1.0, q=0.40, risk=0.0, motivation=0.5)

    s1 = prey_response(1.0, 0.80, **base)
    print("happy path:", s1)

    s2 = prey_response(1.0, 0.80, food=0.70, activity=UNKNOWN, q=0.40, risk=0.0, motivation=0.5)
    print("unknown activity:", s2)

    s3 = prey_response(REJECT, 0.80, **base)
    print("reject family:", s3)

    s4 = prey_response(UNKNOWN, 0.80, **base)
    print("unknown support:", s4)

    s5 = prey_response((0.40, 0.75), 0.80, **base)
    print("interval support:", s5)

    s6 = prey_response((0.50, 0.50), 0.80, **base)
    print("degenerate interval:", s6)

    s7 = prey_response(1.0, 0.80, food=float("nan"), activity=1.0, q=0.40, risk=0.0, motivation=0.5)
    print("nan food:", s7)
    s8 = prey_response(1.0, 0.80, food=0.70, activity=-1.0, q=0.40, risk=0.0, motivation=0.5)
    print("negative activity:", s8)

    comp1 = compose({"baitfish": (RESOLVED, 0.80), "crayfish": (RI, None)})
    comp2 = compose({"baitfish": (RESOLVED, 0.45), "crayfish": (RESOLVED, 0.30)})
    comp3 = compose({"baitfish": (REJECT, 0.0), "crayfish": (RESOLVED, 0.30)})
    comp4 = compose({"baitfish": (REJECT, 0.0), "crayfish": (UNKNOWN, None)})
    comp5 = compose({"baitfish": (RI, None), "crayfish": (UNKNOWN, None)})
    comp6 = compose({"baitfish": (RESOLVED, 0.45), "crayfish": (INVALID, None)})
    print("sibling max with unresolved:", comp1)
    print("sibling max two resolved:", comp2)
    print("reject plus resolved:", comp3)
    print("reject plus unknown:", comp4)
    print("none resolved:", comp5)
    print("invalid sibling:", comp6)

    print("join ok:", join(0.80, 0.50, {}))
    print("join missing L:", join(0.80, None, {}))

    snapshot = {
        "castId": "cast-1",
        "formedAt": 10.0,
        "blockVersion": "v1",
        "entries": {("cg-1", "mode-stalk"): {"activity": 1.0}},
    }
    print("snapshot ok:", cast_entry(snapshot, "cast-1", "cg-1", "mode-stalk"))
    print("snapshot wrong cast:", cast_entry(snapshot, "cast-2", "cg-1", "mode-stalk"))
    print("snapshot missing entry:", cast_entry(snapshot, "cast-1", "cg-2", "mode-stalk"))

    # assertions
    assert s1[0] == RESOLVED and 0 < s1[1] <= 1
    assert s2 == (RI, None)
    assert s3 == (REJECT, 0.0)
    assert s4 == (RI, None)
    assert s5 == (RI, None)          # non-degenerate interval is not evaluated
    assert s6[0] == RESOLVED         # degenerate interval is scalar
    assert s7 == (INVALID, None)
    assert s8 == (INVALID, None)
    assert comp1 == (RESOLVED, 0.80, {"crayfish": RI})
    assert comp2 == (RESOLVED, 0.45, {})
    assert comp3 == (RESOLVED, 0.30, {})
    assert comp4 == (REJECT, 0.0, {"crayfish": UNKNOWN})
    assert comp5 == (RI, None, {"baitfish": RI, "crayfish": UNKNOWN})
    assert comp6[0] == INVALID
    assert join(0.80, 0.50, {}) == (RESOLVED, 0.40, {})
    assert join(0.80, None, {}) == (RI, None, {})
    assert join(0.80, INVALID, {}) == (INVALID, None, {})
    assert cast_entry(snapshot, "cast-1", "cg-1", "mode-stalk") is not None
    assert cast_entry(snapshot, "cast-2", "cg-1", "mode-stalk") is None
    assert cast_entry(snapshot, "cast-1", "cg-2", "mode-stalk") is None

    # single multiply: q is exactly L × C, no second factor
    _, q_val, _ = join(0.6, 0.5, {})
    assert abs(q_val - 0.30) < 1e-12

    print("End-to-end response probe passed")


if __name__ == "__main__":
    main()

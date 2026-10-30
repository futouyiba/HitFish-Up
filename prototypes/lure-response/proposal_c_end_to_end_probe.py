"""Proposal C working probe: end-to-end response chain.

Toy implementation of docs/proposals/lure-response-proposal-c-response-algorithm-v1.md.
Checks status propagation, sibling bounds, Reject handling and the single L×C multiply.

2026-10-30 direction: no latent bearing. The first version assumes the fish is
chasing the lure, so closing cost is K_close * q^2 * activity with no angle
average.

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


def prey_response(support, state, food, activity, q, risk, motivation):
    """Return (status, C_f or None)."""
    if support == REJECT:
        return REJECT, 0.0
    if support in (UNKNOWN, NOT_CONFIGURED):
        return RI, (0.0, 1.0)
    if not _finite(support) or not 0.0 <= support <= 1.0:
        return INVALID, (0.0, 1.0)
    if state == REJECT:
        return REJECT, 0.0
    if state in (UNKNOWN, NOT_CONFIGURED):
        return RI, (0.0, 1.0)
    if not _finite(state) or not 0.0 <= state <= 1.0:
        return INVALID, (0.0, 1.0)
    for value in (food, q, risk, motivation):
        if not _finite(value):
            return INVALID, (0.0, 1.0)
    status, mult = activity_multiplier(activity)
    if status != RESOLVED:
        return status, (0.0, 1.0)
    trigger = TRIGGER_BUDGET * state
    c = conditional_c(food, trigger, mult, q, risk, motivation)
    if c is None:
        return INVALID, (0.0, 1.0)
    return RESOLVED, support * c


def prey_interval(support_lo, support_hi, state, food, activity, q, risk, motivation):
    """Interval support: compute C with support=1, then scale the bounds."""
    status, c = prey_response(1.0, state, food, activity, q, risk, motivation)
    if status != RESOLVED:
        return status, c
    return RI, (support_lo * c, support_hi * c)


def compose(siblings):
    """siblings: list of (status, value).

    2026-10-30 direction: same-target sibling interpretations take a plain max.
    Reject contributes 0; unresolved families are skipped and reported in
    provenance; InvalidInput still blocks; no resolved family -> RI.
    """
    resolved = []
    skipped = []
    invalid = False
    for status, value in siblings:
        if status == RESOLVED:
            resolved.append(value)
        elif status == REJECT:
            resolved.append(0.0)
        elif status == INVALID:
            invalid = True
        elif status in (RI, UNKNOWN, NOT_CONFIGURED):
            skipped.append(status)
    if invalid:
        return INVALID, None, skipped
    if not resolved:
        return RI, None, skipped
    return RESOLVED, max(resolved), skipped


def join(c_feed, L):
    if c_feed is None or L is None:
        return RI, None
    if L in (UNKNOWN, NOT_CONFIGURED):
        return RI, None
    if L == INVALID:
        return INVALID, None
    if not _finite(L) or L < 0:
        return INVALID, None
    return RESOLVED, L * c_feed


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

    s5 = prey_response(1.0, 0.80, food=float("nan"), activity=1.0, q=0.40, risk=0.0, motivation=0.5)
    print("nan food:", s5)
    s6 = prey_response(1.0, 0.80, food=0.70, activity=-1.0, q=0.40, risk=0.0, motivation=0.5)
    print("negative activity:", s6)
    s7 = prey_response(1.0, float("nan"), **base)
    print("nan state:", s7)

    comp1 = compose([(RESOLVED, 0.80), (RI, None)])
    comp2 = compose([(RESOLVED, 0.45), (RI, None)])
    comp3 = compose([(RESOLVED, 0.45), (INVALID, None)])
    comp4 = compose([(RI, None), (UNKNOWN, None)])
    print("sibling max with unresolved:", comp1)
    print("sibling max two resolved/unresolved:", comp2)
    print("sibling invalid:", comp3)
    print("sibling none resolved:", comp4)

    print("join ok:", join(0.80, 0.50))
    print("join missing L:", join(0.80, None))

    # assertions
    status, c = s1
    assert status == RESOLVED and 0 < c <= 1
    assert s2 == (RI, (0.0, 1.0))
    assert s3 == (REJECT, 0.0)
    assert s4 == (RI, (0.0, 1.0))
    assert s5 == (INVALID, (0.0, 1.0))
    assert s6 == (INVALID, (0.0, 1.0))
    assert s7 == (INVALID, (0.0, 1.0))
    assert comp1 == (RESOLVED, 0.80, [RI])
    assert comp2 == (RESOLVED, 0.45, [RI])
    assert comp3[0] == INVALID
    assert comp4[0] == RI
    assert join(0.80, 0.50) == (RESOLVED, 0.40)
    assert join(0.80, None) == (RI, None)
    assert join(0.80, INVALID) == (INVALID, None)

    # single multiply: q is exactly L × C, no second factor
    _, q_val = join(0.6, 0.5)
    assert abs(q_val - 0.30) < 1e-12

    print("End-to-end response probe passed")


if __name__ == "__main__":
    main()

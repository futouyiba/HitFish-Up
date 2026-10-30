"""Proposal C working probe: end-to-end response chain.

Toy implementation of docs/proposals/lure-response-proposal-c-response-algorithm-v1.md.
Checks status propagation, sibling bounds, Reject handling and the single L×C multiply.

Run: python3 -I prototypes/lure-response/proposal_c_end_to_end_probe.py
"""

from __future__ import annotations

import math

M0, M1 = 0.0, 0.40
K_CLOSE = 0.76
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


def activity_multiplier(activity):
    """activity is a resolved multiplier or a non-numeric status."""
    if not isinstance(activity, (int, float)) or not math.isfinite(activity) or activity < 0:
        return None
    return float(activity)


def conditional_c(food, trigger, activity, q, risk, motivation, n=720) -> float:
    total = 0.0
    th = threshold(motivation)
    for i in range(n):
        theta = 2.0 * math.pi * (i + 0.5) / n
        cost = K_CLOSE * max(0.0, q * math.cos(theta)) ** 2 * activity
        margin = food + trigger - cost - risk - th
        total += clamp01((margin - M0) / (M1 - M0))
    return total / n


def prey_response(support, state, food, activity, q, risk, motivation):
    """Return (status, C_f or None)."""
    if support == REJECT:
        return RESOLVED, 0.0
    if support in (UNKNOWN, NOT_CONFIGURED):
        return RI, None
    if not isinstance(support, (int, float)) or not 0.0 <= support <= 1.0:
        return INVALID, None
    if state == REJECT:
        return RESOLVED, 0.0
    if state in (UNKNOWN, NOT_CONFIGURED):
        return RI, None
    mult = activity_multiplier(activity)
    if mult is None:
        return RI, None
    trigger = TRIGGER_BUDGET * state
    c = conditional_c(food, trigger, mult, q, risk, motivation)
    return RESOLVED, support * c


def compose(siblings):
    """siblings: list of (status, interval). Return (status, C_feed or bounds)."""
    bounds = []
    for status, value in siblings:
        if status == RESOLVED:
            bounds.append((value, value))
        elif status == RI:
            lo, hi = value
            bounds.append((lo, hi))
        else:
            return RI, None
    lo = max(b[0] for b in bounds)
    hi = max(b[1] for b in bounds)
    if lo == hi:
        return RESOLVED, lo
    return RI, (lo, hi)


def join(c_feed, L):
    if c_feed is None or L is None:
        return RI, None
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

    comp1 = compose([(RESOLVED, 0.80), (RI, (0.20, 0.60))])
    comp2 = compose([(RESOLVED, 0.45), (RI, (0.10, 0.90))])
    print("sibling converged:", comp1)
    print("sibling open:", comp2)

    print("join ok:", join(0.80, 0.50))
    print("join missing L:", join(0.80, None))

    # assertions
    status, c = s1
    assert status == RESOLVED and 0 < c <= 1
    assert s2 == (RI, None)
    assert s3 == (RESOLVED, 0.0)
    assert s4 == (RI, None)
    assert comp1 == (RESOLVED, 0.80)
    assert comp2[0] == RI and comp2[1] == (0.45, 0.90)
    assert join(0.80, 0.50) == (RESOLVED, 0.40)
    assert join(0.80, None) == (RI, None)

    # single multiply: q is exactly L × C, no second factor
    _, q_val = join(0.6, 0.5)
    assert abs(q_val - 0.30) < 1e-12

    print("End-to-end response probe passed")


if __name__ == "__main__":
    main()

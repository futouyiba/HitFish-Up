"""Proposal C working probe: opportunity support and per-time yield.

Toy model, not production. Purpose: check whether adding a minimal L (dwell-based)
plus encounter rate produces the strategy trade-offs that Response C alone missed
(fast search vs slow finesse; direct vs stealth).

Run: python3 -I prototypes/lure-response/proposal_c_opportunity_support_probe.py
"""

from __future__ import annotations

import math

M0, M1 = 0.0, 0.40
K_CLOSE = 0.76
DWELL_UNITS = 0.80  # L = D / (D + q): smooth dwell decay as speed rises
Q_CAP = 1.00        # encounter rate saturates: R = q / (1 + q / Q_CAP)
K_WARY = 1.0


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def threshold(motivation: float) -> float:
    base = 0.60 - 0.40 * motivation
    if motivation > 0.80:
        base -= 0.50 * (motivation - 0.80)
    return base


def conditional_response(food, trigger, q, activity, risk, motivation) -> float:
    total = 0.0
    n = 720
    th = threshold(motivation)
    for i in range(n):
        theta = 2.0 * math.pi * (i + 0.5) / n
        cost = K_CLOSE * max(0.0, q * math.cos(theta)) ** 2 * activity
        margin = food + trigger - cost - risk - th
        total += clamp01((margin - M0) / (M1 - M0))
    return total / n


def support(q: float) -> float:
    """L: smooth dwell-based opportunity support per grain."""
    return DWELL_UNITS / (DWELL_UNITS + max(q, 0.0))


def encounter_rate(q: float) -> float:
    """R: distinct opportunity grains per unit time, saturating with speed."""
    return q / (1.0 + q / Q_CAP)


def yield_rate(food, trigger, q, activity, risk, motivation, coverage=1.0) -> float:
    """Relative per-time yield: encounter rate × per-grain L × per-grain C."""
    return coverage * encounter_rate(q) * support(q) * conditional_response(food, trigger, q, activity, risk, motivation)


def best_q(food, trigger, activity, risk, motivation, coverage=1.0):
    best = (None, -1.0)
    q = 0.20
    while q <= 2.0001:
        y = yield_rate(food, trigger, q, activity, risk, motivation, coverage)
        if y > best[1]:
            best = (round(q, 3), round(y, 4))
        q += 0.01
    return best


def main() -> None:
    food, trigger, risk, motivation = 0.70, 0.0, 0.0, 0.50
    print("activity\tbest_q\tbest_yield\tY(0.45)\tY(0.90)\tY(1.50)")
    rows = {}
    for activity in (0.8, 1.0, 1.6):
        bq, by = best_q(food, trigger, activity, risk, motivation)
        y45 = yield_rate(food, trigger, 0.45, activity, risk, motivation)
        y90 = yield_rate(food, trigger, 0.90, activity, risk, motivation)
        y15 = yield_rate(food, trigger, 1.50, activity, risk, motivation)
        rows[activity] = (bq, by, y45, y90, y15)
        print(f"{activity:.1f}\t{bq}\t{by}\t{y45:.3f}\t{y90:.3f}\t{y15:.3f}")

    # Lower multiplier = higher activity. High activity sustains a faster optimum.
    assert rows[0.8][0] > rows[1.6][0]
    # At the low-activity end, slow beats fast; at the high-activity end, fast can catch up.
    assert rows[0.8][2] > rows[0.8][3]

    print("\nwariness\tstealth_cov\tY_direct(0.9)\tY_stealth(0.9)")
    for wariness in (0.1, 0.4, 0.8):
        direct = yield_rate(food, trigger, 0.90, 1.0, K_WARY * wariness * 0.50, motivation)
        stealth = yield_rate(food, trigger, 0.90, 1.0, K_WARY * wariness * 0.10, motivation, coverage=0.55)
        print(f"{wariness:.1f}\t0.55\t\t{direct:.3f}\t\t{stealth:.3f}")

    # At high wariness, stealth wins; at low wariness, direct can win if stealth loses coverage.
    low_direct = yield_rate(food, trigger, 0.90, 1.0, K_WARY * 0.1 * 0.50, motivation)
    low_stealth = yield_rate(food, trigger, 0.90, 1.0, K_WARY * 0.1 * 0.10, motivation, coverage=0.55)
    high_direct = yield_rate(food, trigger, 0.90, 1.0, K_WARY * 0.8 * 0.50, motivation)
    high_stealth = yield_rate(food, trigger, 0.90, 1.0, K_WARY * 0.8 * 0.10, motivation, coverage=0.55)
    assert low_direct > low_stealth
    assert high_stealth > high_direct

    print("Opportunity support probe passed")


if __name__ == "__main__":
    main()

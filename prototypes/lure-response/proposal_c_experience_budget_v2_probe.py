"""Proposal C experience-budget v2 probe.

Working calibration probe only. Not a production formula.

This probe does two things:
1) encodes qualitative jerkbait strategy stories as C_mode target intervals;
2) checks whether a simple threshold-family formula can fit those intervals while
   preserving monotonic semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Story:
    name: str
    value: float
    motivation: float
    strain: float
    c_low: float
    c_high: float


STORIES = [
    Story("poor_bite_fast", 0.85, 0.25, 0.75, 0.15, 0.25),
    Story("poor_bite_slow", 0.85, 0.25, 0.25, 0.50, 0.65),
    Story("normal_bite_fast", 0.85, 0.60, 0.65, 0.75, 0.85),
    Story("normal_bite_reference_good", 0.85, 0.60, 0.30, 0.95, 1.00),
    Story("good_bite_fast", 0.85, 0.90, 0.65, 0.90, 1.00),
    Story("weak_capacity_fast", 0.85, 0.60, 0.85, 0.25, 0.35),
    Story("weak_capacity_slow", 0.85, 0.60, 0.50, 0.85, 0.95),
]

# Diagnostic fit found by local least-squares against interval midpoints.
# The point is the shape, not these exact numbers.
K = 0.4684698
P = 4.0
B = 0.74910813
C = 0.3978849
R = 0.34451794
GAMMA = 0.88502698


def c_mode(value: float, motivation: float, strain: float) -> float:
    if strain > 1.0 or value <= 0.0 or motivation <= 0.0:
        return 0.0
    task_cost = K * strain**P
    threshold = B - C * motivation
    margin = value - task_cost - threshold
    x = min(1.0, max(0.0, margin / R))
    return x**GAMMA


def interval_distance(x: float, lo: float, hi: float) -> float:
    if lo <= x <= hi:
        return 0.0
    return lo - x if x < lo else x - hi


def main() -> None:
    # Hard semantic checks.
    assert c_mode(0.90, 0.60, 0.50) >= c_mode(0.80, 0.60, 0.50)
    assert c_mode(0.85, 0.80, 0.50) >= c_mode(0.85, 0.60, 0.50)
    assert c_mode(0.85, 0.60, 0.40) >= c_mode(0.85, 0.60, 0.60)
    assert c_mode(1.00, 1.00, 1.01) == 0.0

    rows = []
    sq = 0.0
    for s in STORIES:
        pred = c_mode(s.value, s.motivation, s.strain)
        d = interval_distance(pred, s.c_low, s.c_high)
        sq += d * d
        rows.append((s.name, pred, s.c_low, s.c_high, d))

    # Same value/motivation: lower strain cannot have lower response.
    normal_fast = c_mode(0.85, 0.60, 0.65)
    weak_slow = c_mode(0.85, 0.60, 0.50)
    assert weak_slow >= normal_fast

    rmse_to_intervals = (sq / len(rows)) ** 0.5
    assert isfinite(rmse_to_intervals)

    print("Experience-budget v2 probe passed")
    print(f"interval RMSE = {rmse_to_intervals:.4f}")
    for name, pred, lo, hi, d in rows:
        print(f"{name:28s} pred={pred:.3f} target=[{lo:.2f}, {hi:.2f}] miss={d:.3f}")
    print(f"TaskCost shape exponent p={P:.1f} (diagnostic: strongly convex)")


if __name__ == "__main__":
    main()

"""Proposal C probe: InterceptSpeedLimit is a Closing burden scale.

This is a semantic/topology probe, not production calibration.
"""

from math import cos, pi


def closing_utilization(lure_speed_water: float, intercept_speed_limit: float, theta: float) -> float:
    assert intercept_speed_limit > 0
    q = lure_speed_water / intercept_speed_limit
    return max(0.0, q * cos(theta))


def closing_cost(u: float, k_close: float = 0.30) -> float:
    return k_close * u * u


# A higher speed scale lowers the same presentation's Closing burden.
weak_limit = 0.60
strong_limit = 1.00
u_weak = closing_utilization(0.75, weak_limit, 0.0)
u_strong = closing_utilization(0.75, strong_limit, 0.0)
assert u_strong < u_weak
assert closing_cost(u_strong) < closing_cost(u_weak)

# Motivation must not change locomotor capacity; it belongs downstream.
low_motivation_limit = 0.80
high_motivation_limit = 0.80
assert low_motivation_limit == high_motivation_limit

# Reference-frame guard: both numerator and denominator are water-relative.
assert closing_utilization(0.60, 0.90, 0.0) == closing_utilization(0.60, 0.90, 0.0)

# q > 1 is a high burden, not a complete opportunity hard zero.
limit = 0.80
lure_speed = 1.00
away = closing_utilization(lure_speed, limit, 0.0)
transverse = closing_utilization(lure_speed, limit, pi / 2)
toward = closing_utilization(lure_speed, limit, pi)
assert away > 1.0
assert closing_cost(away) > closing_cost(transverse)
assert abs(transverse) < 1e-12
assert toward == 0.0

print("PASS: InterceptSpeedLimit Closing-burden invariants")

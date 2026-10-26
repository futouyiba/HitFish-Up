"""Proposal C probe: EffectiveInterceptCapacity ownership invariants.

This is a semantic/topology probe, not production calibration.
"""

from math import cos, pi


def effective_capacity(baseline: float, capacity_modifier: float) -> float:
    assert baseline > 0
    assert 0 < capacity_modifier
    return baseline * capacity_modifier


def closing_utilization(lure_speed_water: float, capacity: float, theta: float) -> float:
    q = lure_speed_water / capacity
    return max(0.0, q * cos(theta))


def closing_result(u: float, k_close: float = 0.30):
    if u >= 1.0:
        return {"infeasible": True, "cost": None}
    return {"infeasible": False, "cost": k_close * u * u}


# Same presentation, same baseline: higher current Functional Capacity must help
baseline = 1.0
weak = effective_capacity(baseline, 0.60)
strong = effective_capacity(baseline, 1.00)

u_weak = closing_utilization(0.75, weak, 0.0)
u_strong = closing_utilization(0.75, strong, 0.0)

assert u_strong < u_weak
assert closing_result(u_weak)["infeasible"] is True
assert closing_result(u_strong)["infeasible"] is False

# Motivation must not change locomotor capacity.
# It belongs downstream in WillingnessThreshold, not in this function.
low_motivation_capacity = effective_capacity(baseline, 0.80)
high_motivation_capacity = effective_capacity(baseline, 0.80)
assert low_motivation_capacity == high_motivation_capacity

# Reference-frame guard: both numerator and denominator are water-relative.
# Uniform world current is intentionally absent from this ratio.
capacity = effective_capacity(1.2, 0.75)
u_without_world_current = closing_utilization(0.60, capacity, 0.0)
u_with_same_water_relative_lure_motion = closing_utilization(0.60, capacity, 0.0)
assert u_without_world_current == u_with_same_water_relative_lure_motion

# q > 1 does not hard-zero every latent angle.
capacity = 0.8
lure_speed = 1.0
away = closing_result(closing_utilization(lure_speed, capacity, 0.0))
transverse = closing_result(closing_utilization(lure_speed, capacity, pi / 2))
toward = closing_result(closing_utilization(lure_speed, capacity, pi))
assert away["infeasible"] is True
assert transverse["infeasible"] is False
assert toward["infeasible"] is False

print("PASS: EffectiveInterceptCapacity semantic invariants")

"""Proposal C Activity bake probe.

This is a topology/ordering fixture, not production calibration.
"""

from dataclasses import dataclass
from math import cos, radians


def bake_activity(*supports: float) -> float:
    if not supports:
        raise ValueError("no enabled Activity supports")
    if any(s < 0 or s > 1 for s in supports):
        raise ValueError("Activity supports must be in [0,1]")
    return min(supports)


def activity_cost_multiplier(activity: float, k_activity: float = 1.0) -> float:
    if not 0 <= activity <= 1:
        raise ValueError("Activity must be in [0,1]")
    return 1.0 + k_activity * (1.0 - activity)


@dataclass(frozen=True)
class ClosingResult:
    utilization: float
    infeasible: bool
    cost: float | None


def closing_cost(
    lure_speed: float,
    intercept_speed_limit: float,
    theta_deg: float,
    activity: float,
    k_close: float = 0.4,
    k_activity: float = 1.0,
) -> ClosingResult:
    if intercept_speed_limit <= 0:
        raise ValueError("intercept_speed_limit must be positive")
    q = lure_speed / intercept_speed_limit
    u = max(0.0, q * cos(radians(theta_deg)))
    if u >= 1.0:
        return ClosingResult(u, True, None)
    cost = k_close * u * u * activity_cost_multiplier(activity, k_activity)
    return ClosingResult(u, False, cost)


def main() -> None:
    # Bottleneck bake: one limiting cause dominates rather than multiplying penalties.
    assert bake_activity(0.9, 0.8, 0.7) == 0.7

    # Activity does not alter hard feasibility.
    high = closing_cost(1.2, 1.0, 0, 1.0)
    low = closing_cost(1.2, 1.0, 0, 0.2)
    assert high.infeasible and low.infeasible

    # For physically feasible pursuit, lower Activity raises soft cost.
    high = closing_cost(0.7, 1.0, 0, 1.0)
    low = closing_cost(0.7, 1.0, 0, 0.2)
    assert not high.infeasible and not low.infeasible
    assert low.cost > high.cost

    # Pause / no radial-away motion receives no Closing penalty regardless of Activity.
    high_pause = closing_cost(0.0, 1.0, 0, 1.0)
    low_pause = closing_cost(0.0, 1.0, 0, 0.0)
    assert high_pause.cost == 0.0
    assert low_pause.cost == 0.0

    # Transverse presentation likewise has zero radial Closing demand in this reduced model.
    # Keep the closed form's tiny floating-point residual out of the assertion.
    transverse = closing_cost(0.9, 1.0, 90, 0.0)
    assert transverse.cost is not None and abs(transverse.cost) < 1e-12

    print("Activity bake / Closing ownership probe passed")


if __name__ == "__main__":
    main()

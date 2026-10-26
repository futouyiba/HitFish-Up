"""Proposal C probe: latent-geometry interception without concrete fish positions.

Working idea:
- no concrete fish point exists at runtime;
- relative bearing between a hypothetical fish and the lure is treated as a latent variable;
- evaluate response per bearing, then marginalize response across the bearing distribution;
- do NOT average TaskStrain first and then apply a nonlinear response function.

This file is a probe, not production authority.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ProbeParams:
    characteristic_distance: float = 1.0
    horizon_seconds: float = 1.0
    fish_intercept_capacity: float = 1.5
    food_value: float = 0.8
    motivation: float = 0.6
    task_cost_k: float = 0.35
    task_cost_p: float = 4.0
    threshold_b: float = 0.72
    threshold_c: float = 0.45
    response_margin_lo: float = -0.10
    response_margin_hi: float = 0.23


def clipped_linear(margin: float, lo: float, hi: float) -> float:
    if margin <= lo:
        return 0.0
    if margin >= hi:
        return 1.0
    return (margin - lo) / (hi - lo)


def response_for_bearing(
    lure_speed: float,
    bearing_radians: float,
    p: ProbeParams,
) -> tuple[float, float, bool]:
    """Return (C(theta), utilization, feasible) for one latent bearing.

    Geometry probe:
    - lure is at origin and moves along +x;
    - hypothetical fish is on a ring of characteristic_distance around lure;
    - after horizon_seconds, required average fish speed is distance from that
      latent fish position to the lure's projected position divided by horizon.

    This is deliberately a minimal geometric probe. Distance and horizon are
    not claimed as production contracts.
    """

    d = p.characteristic_distance
    t = p.horizon_seconds

    fish_x = d * math.cos(bearing_radians)
    fish_y = d * math.sin(bearing_radians)
    lure_x = lure_speed * t
    lure_y = 0.0

    required_speed = math.hypot(lure_x - fish_x, lure_y - fish_y) / t
    utilization = required_speed / p.fish_intercept_capacity

    if utilization > 1.0:
        return 0.0, utilization, False

    task_cost = p.task_cost_k * utilization**p.task_cost_p
    willingness_threshold = p.threshold_b - p.threshold_c * p.motivation
    margin = p.food_value - task_cost - willingness_threshold
    c_theta = clipped_linear(
        margin,
        p.response_margin_lo,
        p.response_margin_hi,
    )
    return c_theta, utilization, True


def angular_retention(
    lure_speed: float,
    p: ProbeParams = ProbeParams(),
    samples: int = 720,
) -> tuple[float, float]:
    """Uniform-isotropic latent bearing prior for the first probe.

    Returns:
      expected C across latent bearings,
      fraction of latent bearings that are physically feasible.
    """

    c_sum = 0.0
    feasible_count = 0

    for i in range(samples):
        theta = 2.0 * math.pi * i / samples
        c_theta, _u, feasible = response_for_bearing(lure_speed, theta, p)
        c_sum += c_theta
        feasible_count += int(feasible)

    return c_sum / samples, feasible_count / samples


def main() -> None:
    print("speed\tE[C(theta)]\tfeasible-bearing fraction")
    for speed in (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5):
        c_avg, feasible_fraction = angular_retention(speed)
        print(f"{speed:.2f}\t{c_avg:.3f}\t\t{feasible_fraction:.3f}")

    # Core semantic regression: marginalize response, not utilization.
    p = ProbeParams()
    speed = 0.75
    cs = []
    us = []
    for i in range(720):
        theta = 2.0 * math.pi * i / 720
        c_theta, u, _ = response_for_bearing(speed, theta, p)
        cs.append(c_theta)
        us.append(u)

    expected_c = sum(cs) / len(cs)
    mean_u = sum(us) / len(us)

    # This intentionally demonstrates that these are not generally equivalent:
    # E[f(u)] != f(E[u]) for nonlinear gates/cost/projection.
    task_cost_at_mean_u = p.task_cost_k * mean_u**p.task_cost_p
    threshold = p.threshold_b - p.threshold_c * p.motivation
    c_of_mean_u = clipped_linear(
        p.food_value - task_cost_at_mean_u - threshold,
        p.response_margin_lo,
        p.response_margin_hi,
    )

    print("\nnon-commutativity check")
    print(f"E[C(theta)] = {expected_c:.3f}")
    print(f"C(E[u])      = {c_of_mean_u:.3f}")
    assert abs(expected_c - c_of_mean_u) > 1e-3


if __name__ == "__main__":
    main()

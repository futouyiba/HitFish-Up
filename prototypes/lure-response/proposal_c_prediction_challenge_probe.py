"""Working probe for Proposal C prediction challenge.

Purpose:
- Do not infer exact fish turning demand from lure trajectory curvature when no fish point exists.
- Represent a recent sudden direction change as a transient prediction/reacquisition challenge.
- Keep this separate from positive prey-state trigger semantics and from latent-angle Closing.

Not production calibration.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class TurnEvent:
    time_s: float
    delta_heading_deg: float


def turn_event_strength(delta_heading_deg: float) -> float:
    """Bounded geometry-only event strength. 0° -> 0, 90° -> .5, 180° -> 1."""
    delta = math.radians(abs(delta_heading_deg) % 360.0)
    if delta > math.pi:
        delta = 2.0 * math.pi - delta
    return 0.5 * (1.0 - math.cos(delta))


def prediction_challenge(events: list[TurnEvent], now_s: float, recovery_time_s: float) -> float:
    """Working transient state: strongest unresolved recent redirection.

    Exponential decay is only a topology probe. recovery_time_s is deliberately
    left uncalibrated. Repeated turns maintain challenge by refreshing the state;
    they do not sum without bound.
    """
    if recovery_time_s <= 0:
        raise ValueError("recovery_time_s must be > 0")
    candidates = []
    for event in events:
        if event.time_s > now_s:
            continue
        age = now_s - event.time_s
        candidates.append(turn_event_strength(event.delta_heading_deg) * math.exp(-age / recovery_time_s))
    return max(candidates, default=0.0)


def _assert_close(a: float, b: float, eps: float = 1e-9) -> None:
    assert abs(a - b) <= eps, (a, b)


def run_probe() -> None:
    _assert_close(turn_event_strength(0), 0.0)
    _assert_close(turn_event_strength(90), 0.5)
    _assert_close(turn_event_strength(180), 1.0)

    tau = 0.6
    single = [TurnEvent(0.0, 90.0)]
    p0 = prediction_challenge(single, 0.0, tau)
    p06 = prediction_challenge(single, 0.6, tau)
    assert p06 < p0

    repeated = [TurnEvent(0.0, 90.0), TurnEvent(0.4, 90.0), TurnEvent(0.8, 90.0)]
    assert prediction_challenge(repeated, 0.9, tau) > prediction_challenge(single, 0.9, tau)

    # A straight fast retrieve has no prediction challenge merely because it is fast.
    _assert_close(prediction_challenge([], 1.0, tau), 0.0)

    print("prediction challenge probe passed")


if __name__ == "__main__":
    run_probe()

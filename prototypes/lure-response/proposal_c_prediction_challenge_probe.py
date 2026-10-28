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
    """Working `max_recent`: strongest unresolved recent redirection.

    Exponential decay is only a topology probe. recovery_time_s is deliberately
    left uncalibrated. This keeps the current review entry's `max_recent`
    aggregation: a new turn only replaces the state when its decayed strength
    exceeds the current maximum, so sustained turning never accumulates beyond
    the latest event. That limit is recorded by the regression control below.
    Changing it is a semantic change that needs Owner approval, not a
    probe-local edit.
    """
    if recovery_time_s <= 0:
        raise ValueError("recovery_time_s must be > 0")
    candidates = []
    for event in events:
        if event.time_s > now_s:
            continue
        age = now_s - event.time_s
        candidates.append(
            turn_event_strength(event.delta_heading_deg)
            * math.exp(-age / recovery_time_s)
        )
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
    # The `max_recent` topology must keep single-event decay intact.
    _assert_close(p06, 0.5 * math.exp(-0.6 / tau))

    repeated = [TurnEvent(0.0, 90.0), TurnEvent(0.4, 90.0), TurnEvent(0.8, 90.0)]
    assert prediction_challenge(repeated, 0.9, tau) > prediction_challenge(single, 0.9, tau)

    # Regression control for the known `max_recent` underestimation: sustained
    # turning collapses to the same value as its single latest event. This
    # records current behavior explicitly, so an unapproved additive refresh
    # fails here instead of passing silently. If sustained turns are meant to
    # accumulate, the review entry must change first with Owner approval.
    latest_only = [TurnEvent(0.8, 90.0)]
    repeated_state = prediction_challenge(repeated, 0.9, tau)
    latest_state = prediction_challenge(latest_only, 0.9, tau)
    _assert_close(repeated_state, latest_state)
    assert repeated_state <= 1.0

    # Same limit under many sustained turns: the state stays at the latest
    # event's strength (0.5 here), rather than accumulating toward 1.0.
    many = [TurnEvent(0.1 * i, 90.0) for i in range(20)]
    _assert_close(prediction_challenge(many, many[-1].time_s, tau), 0.5)

    # A straight fast retrieve has no prediction challenge merely because it is fast.
    _assert_close(prediction_challenge([], 1.0, tau), 0.0)

    print("prediction challenge probe passed")


if __name__ == "__main__":
    run_probe()

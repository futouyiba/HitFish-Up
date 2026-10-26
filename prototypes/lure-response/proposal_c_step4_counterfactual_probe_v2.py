"""Proposal C Step-4 counterfactual probe v2.

Refinements:
- recent pause remains a candidate mechanism; this probe does not reject it.
- roll may route to valuation as a cue and/or to TaskDemand through actual
  capture-geometry consequences. Raw roll angle is not itself a generic penalty.
- TaskDemand is compressed into task semantics rather than one field per raw input.

All numeric thresholds are arbitrary topology probes, not biological calibration.
"""

from dataclasses import dataclass
from enum import Enum


class Affordance(str, Enum):
    FEASIBLE = "Feasible"
    CONSTRAINED = "Constrained"
    INFEASIBLE = "Infeasible"
    UNKNOWN = "Unknown"


@dataclass(frozen=True)
class FunctionalCapacity:
    comfortable_intercept: float
    hard_intercept: float
    comfortable_maneuver: float
    hard_maneuver: float


@dataclass(frozen=True)
class Presentation:
    prey_support: float = 0.90
    distance: float = 4.0
    relative_speed: float = 0.0
    lateral_offset: float = 0.0
    vertical_offset: float = 0.0
    capture_orientation_demand: float = 0.0
    roll_deg: float = 0.0
    sinking: bool = False
    recent_move_then_pause: bool = False
    pause_age: float | None = None


def resolve_task_demand(p: Presentation):
    """Illustrative semantic compression, not a production equation."""
    intercept = max(0.0, p.distance / 10.0 + p.relative_speed)
    maneuver = (
        abs(p.lateral_offset) / 5.0
        + abs(p.vertical_offset) / 5.0
        + p.capture_orientation_demand
    )
    return {"intercept": intercept, "maneuver": maneuver}


def _axis(value, comfortable, hard):
    if value <= comfortable:
        return Affordance.FEASIBLE
    if value <= hard:
        return Affordance.CONSTRAINED
    return Affordance.INFEASIBLE


def resolve_task_affordance(capacity: FunctionalCapacity, demand):
    axes = (
        _axis(demand["intercept"], capacity.comfortable_intercept, capacity.hard_intercept),
        _axis(demand["maneuver"], capacity.comfortable_maneuver, capacity.hard_maneuver),
    )
    if Affordance.INFEASIBLE in axes:
        return Affordance.INFEASIBLE
    if Affordance.CONSTRAINED in axes:
        return Affordance.CONSTRAINED
    return Affordance.FEASIBLE


def valuation_candidates(p: Presentation):
    candidates = []
    if p.sinking and abs(p.roll_deg) >= 60:
        candidates.append("imbalance_like_vulnerability")
    if p.recent_move_then_pause:
        candidates.append("temporal_attention_or_trigger")
    return candidates


def evaluate(p: Presentation, capacity: FunctionalCapacity):
    demand = resolve_task_demand(p)
    return {
        "prey_support": p.prey_support,
        "task_demand": demand,
        "task_affordance": resolve_task_affordance(capacity, demand),
        "valuation_candidates": valuation_candidates(p),
        "feeding_motivation_delta": 0.0,
    }


def run_counterfactuals():
    capacity = FunctionalCapacity(
        comfortable_intercept=0.55,
        hard_intercept=0.75,
        comfortable_maneuver=0.20,
        hard_maneuver=0.40,
    )

    # Q1: relative motion changes intercept demand without a fast-lure penalty scalar.
    q1 = [
        evaluate(Presentation(relative_speed=v), capacity)
        for v in (0.10, 0.25, 0.50)
    ]
    assert [x["task_affordance"] for x in q1] == [
        Affordance.FEASIBLE,
        Affordance.CONSTRAINED,
        Affordance.INFEASIBLE,
    ]

    # Q2: identical current physics does NOT prove recent-pause has no effect.
    # It only proves any effect needs a separate temporal mechanism rather than
    # being silently hidden in current TaskDemand.
    q2_recent = evaluate(
        Presentation(relative_speed=0.0, recent_move_then_pause=True, pause_age=0.20),
        capacity,
    )
    q2_long = evaluate(
        Presentation(relative_speed=0.0, recent_move_then_pause=False, pause_age=5.0),
        capacity,
    )
    assert q2_recent["task_demand"] == q2_long["task_demand"]
    assert q2_recent["task_affordance"] == q2_long["task_affordance"]
    assert "temporal_attention_or_trigger" in q2_recent["valuation_candidates"]
    assert "temporal_attention_or_trigger" not in q2_long["valuation_candidates"]

    # Q3a: cue-only roll. If actual capture geometry is held identical,
    # TaskDemand stays identical and the difference is valuation-only.
    q3_normal = evaluate(Presentation(relative_speed=0.05, sinking=True, roll_deg=0), capacity)
    q3_cue_only = evaluate(Presentation(relative_speed=0.05, sinking=True, roll_deg=75), capacity)
    assert q3_normal["task_demand"] == q3_cue_only["task_demand"]
    assert "imbalance_like_vulnerability" not in q3_normal["valuation_candidates"]
    assert "imbalance_like_vulnerability" in q3_cue_only["valuation_candidates"]

    # Q3b: physically consequential roll. The raw angle is not the demand;
    # an actual capture-geometry consequence is.
    q3_physical = evaluate(
        Presentation(
            relative_speed=0.05,
            sinking=True,
            roll_deg=75,
            capture_orientation_demand=0.30,
        ),
        capacity,
    )
    assert q3_physical["task_demand"] != q3_cue_only["task_demand"]
    assert q3_physical["task_affordance"] == Affordance.CONSTRAINED
    assert "imbalance_like_vulnerability" in q3_physical["valuation_candidates"]

    return {
        "Q1": [x["task_affordance"].value for x in q1],
        "Q2": "same current TaskDemand, temporal mechanism remains candidate",
        "Q3a": "cue-only roll changes valuation candidate, not TaskDemand",
        "Q3b": "physical capture-geometry consequence may also change TaskDemand",
    }


if __name__ == "__main__":
    result = run_counterfactuals()
    for key, value in result.items():
        print(f"{key}: {value}")

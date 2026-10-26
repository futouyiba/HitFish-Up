"""Proposal C Step-4 counterfactual probe.

Scope:
- Fish: largemouth bass
- Prey interpretation: small baitfish
- Hold prey support and fish internal state constant
- Test only routing semantics for Q1/Q2/Q3

This is a design probe, not biological calibration and not a production formula.
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
    comfortable_closing: float
    hard_closing_limit: float


@dataclass(frozen=True)
class Presentation:
    prey_support: float
    target_speed: float
    distance: float
    sinking_speed: float = 0.0
    roll_deg: float = 0.0
    recent_move_then_pause: bool = False
    pause_age: float | None = None


def resolve_task_demand(p: Presentation):
    """Minimal illustrative demand packet; values are arbitrary probe units."""
    return {
        "closing": p.target_speed,
        "distance": p.distance,
        "sinking": abs(p.sinking_speed),
    }


def resolve_task_affordance(capacity: FunctionalCapacity, demand):
    closing = demand["closing"]
    if closing <= capacity.comfortable_closing:
        return Affordance.FEASIBLE
    if closing <= capacity.hard_closing_limit:
        return Affordance.CONSTRAINED
    return Affordance.INFEASIBLE


def interpret_vulnerability_candidate(p: Presentation):
    """Route an imbalance-like cue to valuation candidate only; no bonus implied."""
    if p.sinking_speed < 0 and abs(p.roll_deg) >= 60:
        return "candidate_vulnerable"
    return "none"


def evaluate(p: Presentation, capacity: FunctionalCapacity):
    demand = resolve_task_demand(p)
    return {
        "prey_support": p.prey_support,
        "task_demand": demand,
        "task_affordance": resolve_task_affordance(capacity, demand),
        "vulnerability_interpretation": interpret_vulnerability_candidate(p),
        "temporal_history": (
            "recent_move_then_pause" if p.recent_move_then_pause else "none"
        ),
        # Step-3 presentation history does not create fish internal motivation.
        "feeding_motivation_delta": 0.0,
        # No independent pause bonus is admitted by default.
        "temporal_valuation_delta": 0.0,
    }


def run_counterfactuals():
    capacity = FunctionalCapacity(
        comfortable_closing=0.15,
        hard_closing_limit=0.30,
    )

    # Q1: velocity reversal / escalation.
    q1_inputs = [
        Presentation(0.90, target_speed=0.10, distance=4.0),
        Presentation(0.90, target_speed=0.22, distance=4.0),
        Presentation(0.90, target_speed=0.40, distance=4.0),
    ]
    q1 = [evaluate(p, capacity) for p in q1_inputs]
    assert [x["task_affordance"] for x in q1] == [
        Affordance.FEASIBLE,
        Affordance.CONSTRAINED,
        Affordance.INFEASIBLE,
    ]
    assert all(x["prey_support"] == 0.90 for x in q1)
    assert all(x["feeding_motivation_delta"] == 0.0 for x in q1)

    # Q2: newly paused vs long-paused; current physics held identical.
    q2_recent = Presentation(
        0.90,
        target_speed=0.0,
        distance=4.0,
        recent_move_then_pause=True,
        pause_age=0.20,
    )
    q2_long = Presentation(
        0.90,
        target_speed=0.0,
        distance=4.0,
        recent_move_then_pause=False,
        pause_age=5.0,
    )
    q2a, q2b = evaluate(q2_recent, capacity), evaluate(q2_long, capacity)
    assert q2a["task_demand"] == q2b["task_demand"]
    assert q2a["task_affordance"] == q2b["task_affordance"]
    assert q2a["temporal_valuation_delta"] == q2b["temporal_valuation_delta"] == 0.0
    assert q2a["feeding_motivation_delta"] == q2b["feeding_motivation_delta"] == 0.0

    # Q3: same sinking mechanics, posture differs.
    q3_normal = Presentation(
        0.90,
        target_speed=0.05,
        distance=4.0,
        sinking_speed=-0.05,
        roll_deg=0,
    )
    q3_rolled = Presentation(
        0.90,
        target_speed=0.05,
        distance=4.0,
        sinking_speed=-0.05,
        roll_deg=75,
    )
    q3a, q3b = evaluate(q3_normal, capacity), evaluate(q3_rolled, capacity)
    assert q3a["task_demand"] == q3b["task_demand"]
    assert q3a["task_affordance"] == q3b["task_affordance"]
    assert q3a["vulnerability_interpretation"] == "none"
    assert q3b["vulnerability_interpretation"] == "candidate_vulnerable"
    assert q3a["feeding_motivation_delta"] == q3b["feeding_motivation_delta"] == 0.0

    return {
        "Q1": [x["task_affordance"].value for x in q1],
        "Q2": "no independent temporal effect admitted",
        "Q3": "same task demand; roll routes only to valuation candidate",
    }


if __name__ == "__main__":
    result = run_counterfactuals()
    for key, value in result.items():
        print(f"{key}: {value}")

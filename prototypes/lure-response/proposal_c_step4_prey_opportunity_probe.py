"""Proposal C Step-4 prey opportunity interpretation probe.

The point of this probe is structural:
- fishing-domain prey stories such as escaping / struggling / vulnerable-like are admitted as
  semantic interpretations;
- they do not collapse into one flat OpportunityState;
- fish-relative opportunity depends on both prey-side semantics and current TaskAffordance.

All numeric thresholds are arbitrary topology probes, not biological calibration.
"""

from dataclasses import dataclass
from enum import Enum


class Affordance(str, Enum):
    FEASIBLE = "Feasible"
    CONSTRAINED = "Constrained"
    INFEASIBLE = "Infeasible"


@dataclass(frozen=True)
class Capacity:
    comfortable_intercept: float
    hard_intercept: float
    comfortable_maneuver: float
    hard_maneuver: float


@dataclass(frozen=True)
class Presentation:
    prey_support: float = 0.90
    relative_speed: float = 0.0
    distance: float = 3.0
    lateral_offset: float = 0.0
    vertical_offset: float = 0.0
    orientation_demand: float = 0.0
    erratic_escape: bool = False
    surface_struggle: bool = False
    sinking: bool = False
    roll_deg: float = 0.0


def resolve_prey_semantics(p: Presentation):
    behavior = []
    condition = []

    if p.erratic_escape:
        behavior.append("escaping_like")
    if p.surface_struggle:
        behavior.append("struggling_like")
    if p.sinking and abs(p.roll_deg) >= 60:
        condition.append("vulnerable_like")

    return {
        "behavior_motifs": behavior,
        "condition_cues": condition,
    }


def resolve_task_demand(p: Presentation):
    return {
        "intercept": p.distance / 10.0 + max(0.0, p.relative_speed),
        "maneuver": (
            abs(p.lateral_offset) / 5.0
            + abs(p.vertical_offset) / 5.0
            + p.orientation_demand
        ),
    }


def _axis(value, comfortable, hard):
    if value <= comfortable:
        return Affordance.FEASIBLE
    if value <= hard:
        return Affordance.CONSTRAINED
    return Affordance.INFEASIBLE


def resolve_task_affordance(c: Capacity, d):
    axes = [
        _axis(d["intercept"], c.comfortable_intercept, c.hard_intercept),
        _axis(d["maneuver"], c.comfortable_maneuver, c.hard_maneuver),
    ]
    if Affordance.INFEASIBLE in axes:
        return Affordance.INFEASIBLE
    if Affordance.CONSTRAINED in axes:
        return Affordance.CONSTRAINED
    return Affordance.FEASIBLE


def opportunity_packet(p: Presentation, c: Capacity):
    semantic = resolve_prey_semantics(p)
    demand = resolve_task_demand(p)
    affordance = resolve_task_affordance(c, demand)

    # Important: this is a typed packet, not a scalar or flat enum.
    return {
        "prey_support": p.prey_support,
        "prey_semantics": semantic,
        "task_demand": demand,
        "task_affordance": affordance,
        "opportunity_bonus": None,
    }


def run_probe():
    c = Capacity(
        comfortable_intercept=0.55,
        hard_intercept=0.75,
        comfortable_maneuver=0.20,
        hard_maneuver=0.40,
    )

    # A/B: same escaping-like story, different fish-relative opportunity.
    escaping_easy = opportunity_packet(
        Presentation(relative_speed=0.10, distance=2.0, erratic_escape=True), c
    )
    escaping_hard = opportunity_packet(
        Presentation(relative_speed=0.50, distance=4.0, erratic_escape=True), c
    )
    assert escaping_easy["prey_semantics"] == escaping_hard["prey_semantics"]
    assert escaping_easy["task_affordance"] == Affordance.FEASIBLE
    assert escaping_hard["task_affordance"] == Affordance.INFEASIBLE

    # C/D: same vulnerable-like cue, different geometry / affordance.
    vuln_easy = opportunity_packet(
        Presentation(
            relative_speed=0.05, distance=2.0, sinking=True, roll_deg=75
        ),
        c,
    )
    vuln_hard = opportunity_packet(
        Presentation(
            relative_speed=0.40, distance=5.0, sinking=True, roll_deg=75
        ),
        c,
    )
    assert vuln_easy["prey_semantics"] == vuln_hard["prey_semantics"]
    assert vuln_easy["task_affordance"] == Affordance.FEASIBLE
    assert vuln_hard["task_affordance"] == Affordance.INFEASIBLE

    # E: semantic facets can coexist, proving a single flat prey-state enum is lossy.
    coexist = opportunity_packet(
        Presentation(
            relative_speed=0.05,
            distance=2.0,
            sinking=True,
            roll_deg=75,
            surface_struggle=True,
        ),
        c,
    )
    assert "struggling_like" in coexist["prey_semantics"]["behavior_motifs"]
    assert "vulnerable_like" in coexist["prey_semantics"]["condition_cues"]

    # F: the interpretation packet must not manufacture a generic opportunity bonus.
    for packet in (escaping_easy, escaping_hard, vuln_easy, vuln_hard, coexist):
        assert packet["opportunity_bonus"] is None

    return {
        "A/B": "same escaping-like semantic; Feasible vs Infeasible",
        "C/D": "same vulnerable-like semantic; Feasible vs Infeasible",
        "E": "struggling-like and vulnerable-like can coexist",
        "F": "no generic opportunity bonus generated",
    }


if __name__ == "__main__":
    result = run_probe()
    print("Step-4 prey opportunity probe passed")
    for key, value in result.items():
        print(f"{key}: {value}")

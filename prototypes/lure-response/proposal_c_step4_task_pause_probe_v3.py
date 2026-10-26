"""Proposal C Step-4 task-demand and pause-mechanism probe v3.

Purpose:
1) Test whether maneuver/capture-geometry demand can create a ranking reversal
   while intercept demand is held constant.
2) Decompose "recent move then pause" into distinct candidate causal routes
   instead of a universal pause bonus.

All numbers are arbitrary topology probes, not biological calibration.
"""

from dataclasses import dataclass
from enum import Enum


class Affordance(str, Enum):
    FEASIBLE = "Feasible"
    CONSTRAINED = "Constrained"
    INFEASIBLE = "Infeasible"
    UNKNOWN = "Unknown"


@dataclass(frozen=True)
class Capacity:
    comfortable_intercept: float = 0.55
    hard_intercept: float = 0.75
    comfortable_maneuver: float = 0.20
    hard_maneuver: float = 0.40


@dataclass(frozen=True)
class TaskDemand:
    intercept: float
    maneuver: float


@dataclass(frozen=True)
class PauseHistory:
    prior_salient_motion: bool
    pause_age: float
    trajectory_changed_at_pause: bool
    favorable_geometry_horizon: float
    cadence_pattern_id: str | None = None


@dataclass(frozen=True)
class MechanismConfig:
    attention_continuity: bool = False
    prediction_break: bool = False
    attack_window: bool = False
    cadence_trigger: bool = False


def axis(value: float, comfortable: float, hard: float) -> Affordance:
    if value <= comfortable:
        return Affordance.FEASIBLE
    if value <= hard:
        return Affordance.CONSTRAINED
    return Affordance.INFEASIBLE


def resolve_affordance(cap: Capacity, demand: TaskDemand):
    intercept = axis(demand.intercept, cap.comfortable_intercept, cap.hard_intercept)
    maneuver = axis(demand.maneuver, cap.comfortable_maneuver, cap.hard_maneuver)
    if Affordance.INFEASIBLE in (intercept, maneuver):
        overall = Affordance.INFEASIBLE
    elif Affordance.CONSTRAINED in (intercept, maneuver):
        overall = Affordance.CONSTRAINED
    else:
        overall = Affordance.FEASIBLE
    return {"intercept": intercept, "maneuver": maneuver, "overall": overall}


def evaluate_pause(history: PauseHistory, cfg: MechanismConfig):
    """Return typed causal routes. No scalar bonus is produced."""
    out = {
        "perception_attention_memory": "NotConfigured",
        "prediction_state": "NotConfigured",
        "attack_window": "NotConfigured",
        "cadence_valuation": "NotConfigured",
        "feeding_motivation_delta": 0.0,
    }

    if cfg.attention_continuity:
        out["perception_attention_memory"] = (
            "RecentSalientHistory"
            if history.prior_salient_motion and history.pause_age <= 1.0
            else "NoRecentSalientHistory"
        )

    if cfg.prediction_break:
        out["prediction_state"] = (
            "TrajectoryBreak"
            if history.trajectory_changed_at_pause
            else "NoTrajectoryBreak"
        )

    if cfg.attack_window:
        out["attack_window"] = {
            "favorable_geometry_horizon": history.favorable_geometry_horizon
        }

    if cfg.cadence_trigger:
        out["cadence_valuation"] = (
            f"CandidatePattern:{history.cadence_pattern_id}"
            if history.cadence_pattern_id
            else "NoConfiguredPattern"
        )

    return out


def run():
    cap = Capacity()

    # M1: Hold intercept constant, vary only maneuver demand.
    demands = [
        TaskDemand(intercept=0.50, maneuver=0.10),
        TaskDemand(intercept=0.50, maneuver=0.30),
        TaskDemand(intercept=0.50, maneuver=0.50),
    ]
    m1 = [resolve_affordance(cap, d) for d in demands]
    assert [x["intercept"] for x in m1] == [Affordance.FEASIBLE] * 3
    assert [x["overall"] for x in m1] == [
        Affordance.FEASIBLE,
        Affordance.CONSTRAINED,
        Affordance.INFEASIBLE,
    ]

    # P0: With no mechanism configured, recent-vs-long pause must not create a hidden bonus.
    recent = PauseHistory(True, 0.20, True, 1.20, "move-stop")
    long = PauseHistory(False, 5.00, False, 1.20, None)
    p0a = evaluate_pause(recent, MechanismConfig())
    p0b = evaluate_pause(long, MechanismConfig())
    assert p0a == p0b

    # P1 attention continuity is a Perception/history route.
    p1a = evaluate_pause(recent, MechanismConfig(attention_continuity=True))
    p1b = evaluate_pause(long, MechanismConfig(attention_continuity=True))
    assert p1a["perception_attention_memory"] == "RecentSalientHistory"
    assert p1b["perception_attention_memory"] == "NoRecentSalientHistory"
    assert p1a["feeding_motivation_delta"] == p1b["feeding_motivation_delta"] == 0.0

    # P2 trajectory break is a transient prediction/task-state route.
    p2a = evaluate_pause(recent, MechanismConfig(prediction_break=True))
    p2b = evaluate_pause(long, MechanismConfig(prediction_break=True))
    assert p2a["prediction_state"] == "TrajectoryBreak"
    assert p2b["prediction_state"] == "NoTrajectoryBreak"

    # P3 attack-window effect is exposure/horizon, not an instantaneous valuation bonus.
    same_history_short = PauseHistory(True, 0.20, True, 0.25, "move-stop")
    same_history_long = PauseHistory(True, 0.20, True, 1.50, "move-stop")
    p3a = evaluate_pause(same_history_short, MechanismConfig(attack_window=True))
    p3b = evaluate_pause(same_history_long, MechanismConfig(attack_window=True))
    assert p3a["attack_window"]["favorable_geometry_horizon"] < p3b["attack_window"]["favorable_geometry_horizon"]
    assert p3a["feeding_motivation_delta"] == p3b["feeding_motivation_delta"] == 0.0

    # P4 cadence is the only route here allowed to remain a valuation candidate,
    # and only when an explicit pattern is configured.
    p4a = evaluate_pause(recent, MechanismConfig(cadence_trigger=True))
    p4b = evaluate_pause(long, MechanismConfig(cadence_trigger=True))
    assert p4a["cadence_valuation"] == "CandidatePattern:move-stop"
    assert p4b["cadence_valuation"] == "NoConfiguredPattern"

    return {
        "M1": [x["overall"].value for x in m1],
        "P0": "no hidden pause bonus",
        "P1": "attention routes to perception/history",
        "P2": "trajectory break routes to transient prediction/task state",
        "P3": "attack-window routes to exposure/horizon",
        "P4": "cadence remains explicit valuation candidate only",
    }


if __name__ == "__main__":
    for k, v in run().items():
        print(f"{k}: {v}")

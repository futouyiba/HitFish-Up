"""Proposal C Complete Feeding Response Mode closure probe.

Purpose:
- separate target/food value from fish-side motivation and task affordance;
- test whether an additional presentation-state valuation layer is mandatory;
- preserve Unknown / Unsupported / Infeasible distinctions.

All numeric mappings are topology probes only, not production calibration.
"""

from dataclasses import dataclass
from enum import Enum


class Resolution(str, Enum):
    RESOLVED = "Resolved"
    UNKNOWN = "Unknown"
    UNSUPPORTED = "Unsupported"


class Affordance(str, Enum):
    FEASIBLE = "Feasible"
    CONSTRAINED = "Constrained"
    INFEASIBLE = "Infeasible"
    UNKNOWN = "Unknown"


@dataclass(frozen=True)
class ModeInput:
    target_resolution: Resolution
    perception_resolution: Resolution
    task_affordance: Affordance
    feeding_motivation: float | None
    target_value: float | None
    state_valuation_delta: float | None = None


def close_feeding_mode(x: ModeInput):
    # Resolution and mode validity are not numeric penalties.
    if x.target_resolution == Resolution.UNKNOWN or x.perception_resolution == Resolution.UNKNOWN:
        return {"status": "ResolutionIncomplete", "rollable": False}

    if x.target_resolution == Resolution.UNSUPPORTED or x.perception_resolution == Resolution.UNSUPPORTED:
        return {"status": "ModeInvalid", "rollable": False}

    if x.task_affordance == Affordance.UNKNOWN or x.feeding_motivation is None or x.target_value is None:
        return {"status": "ResolutionIncomplete", "rollable": False}

    # Physical inability is not low willingness.
    if x.task_affordance == Affordance.INFEASIBLE:
        return {
            "status": "TaskInfeasible",
            "rollable": False,
            "target_value": x.target_value,
            "feeding_motivation": x.feeding_motivation,
        }

    # Working probe only. This is not a proposed production aggregation formula.
    affordance_factor = 1.0 if x.task_affordance == Affordance.FEASIBLE else 0.6
    admitted_state_delta = 0.0 if x.state_valuation_delta is None else x.state_valuation_delta
    drive = max(0.0, x.target_value + admitted_state_delta) * x.feeding_motivation

    return {
        "status": "Complete",
        "rollable": True,
        "target_value": x.target_value,
        "feeding_motivation": x.feeding_motivation,
        "task_affordance": x.task_affordance.value,
        "state_valuation_delta": admitted_state_delta,
        "drive_probe": drive,
        "response_proxy": drive * affordance_factor,
    }


def run_counterfactuals():
    base = dict(
        target_resolution=Resolution.RESOLVED,
        perception_resolution=Resolution.RESOLVED,
        task_affordance=Affordance.FEASIBLE,
        feeding_motivation=0.70,
        target_value=0.80,
    )

    baseline = close_feeding_mode(ModeInput(**base))

    # A: target / food value has independent downstream meaning.
    lower_value = close_feeding_mode(ModeInput(**{**base, "target_value": 0.30}))
    assert baseline["response_proxy"] > lower_value["response_proxy"]

    # B: fish-side feeding motivation has independent downstream meaning.
    lower_motivation = close_feeding_mode(ModeInput(**{**base, "feeding_motivation": 0.20}))
    assert baseline["response_proxy"] > lower_motivation["response_proxy"]

    # C: task affordance remains distinct from value and willingness.
    constrained = close_feeding_mode(ModeInput(**{**base, "task_affordance": Affordance.CONSTRAINED}))
    assert baseline["response_proxy"] > constrained["response_proxy"]

    infeasible = close_feeding_mode(ModeInput(**{**base, "task_affordance": Affordance.INFEASIBLE}))
    assert infeasible["status"] == "TaskInfeasible"
    assert not infeasible["rollable"]

    # D: unresolved facts are not neutral coefficients or zero response.
    unresolved = close_feeding_mode(ModeInput(**{**base, "target_resolution": Resolution.UNKNOWN}))
    assert unresolved["status"] == "ResolutionIncomplete"
    assert not unresolved["rollable"]

    # E: no presentation-state valuation is required for the mode to close.
    explicit_zero = close_feeding_mode(ModeInput(**base, state_valuation_delta=0.0))
    assert explicit_zero["response_proxy"] == baseline["response_proxy"]

    # F: if a state valuation mechanism is admitted later, it can be inserted
    # explicitly without changing target, motivation, or task ownership.
    admitted_modifier = close_feeding_mode(ModeInput(**base, state_valuation_delta=0.20))
    assert admitted_modifier["response_proxy"] > baseline["response_proxy"]

    return ["A-target-value", "B-motivation", "C-affordance", "D-unknown", "E-no-state-valuation-required", "F-optional-state-valuation"]


if __name__ == "__main__":
    print("Complete Feeding Response closure probe passed:", " ".join(run_counterfactuals()))

"""Proposal C Complete Feeding Response Mode closure probe.

Purpose:
- separate target/food value from fish-side motivation and task affordance;
- test whether an additional presentation-state valuation layer is mandatory;
- model Closing hard feasibility through species × size cohort → InterceptSpeedLimit;
- apply Activity only as soft cost after physically-feasible Closing;
- preserve Unknown / zero / Disabled / NotApplicable distinctions.

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


class InputState(str, Enum):
    KNOWN = "Known"
    UNKNOWN = "Unknown"
    DISABLED = "Disabled"
    NOT_APPLICABLE = "NotApplicable"


@dataclass(frozen=True)
class ClosingInput:
    demand: float | None
    intercept_speed_limit: float | None
    state: InputState = InputState.KNOWN


def resolve_closing(closing: ClosingInput, activity: float | None, activity_state: InputState = InputState.KNOWN):
    """Resolve hard Closing feasibility, then optional Activity soft cost.

    InterceptSpeedLimit is keyed by species × size cohort outside this probe.
    Activity never changes the hard limit and is never multiplied into it.
    """
    if closing.state in (InputState.UNKNOWN, InputState.DISABLED, InputState.NOT_APPLICABLE):
        return {
            "affordance": Affordance.UNKNOWN,
            "closing_cost": None,
            "activity_cost": None,
            "closing_state": closing.state.value,
        }
    if closing.demand is None or closing.intercept_speed_limit is None:
        return {
            "affordance": Affordance.UNKNOWN,
            "closing_cost": None,
            "activity_cost": None,
            "closing_state": closing.state.value,
        }
    if closing.demand > closing.intercept_speed_limit:
        return {
            "affordance": Affordance.INFEASIBLE,
            "closing_cost": None,
            "activity_cost": None,
            "closing_state": closing.state.value,
        }

    activity_cost = None
    if activity_state == InputState.KNOWN:
        if activity is None:
            return {"affordance": Affordance.UNKNOWN, "closing_cost": None, "activity_cost": None, "closing_state": closing.state.value}
        activity_cost = max(0.0, 1.0 - activity)
    elif activity_state in (InputState.DISABLED, InputState.NOT_APPLICABLE):
        activity_cost = 0.0
    else:
        return {"affordance": Affordance.UNKNOWN, "closing_cost": None, "activity_cost": None, "closing_state": closing.state.value}

    utilization = closing.demand / closing.intercept_speed_limit
    closing_cost = utilization + activity_cost
    affordance = Affordance.CONSTRAINED if utilization >= 0.8 else Affordance.FEASIBLE
    return {"affordance": affordance, "closing_cost": closing_cost, "activity_cost": activity_cost}


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

    # Physical inability is not low willingness. This probe uses the resolved
    # affordance supplied by resolve_closing; Activity cannot create Infeasible.
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
    base_closing = resolve_closing(
        ClosingInput(demand=0.50, intercept_speed_limit=0.80),
        activity=0.70,
    )
    assert base_closing["affordance"] == Affordance.FEASIBLE

    low_activity = resolve_closing(
        ClosingInput(demand=0.50, intercept_speed_limit=0.80),
        activity=0.20,
    )
    assert low_activity["affordance"] == Affordance.FEASIBLE
    assert low_activity["closing_cost"] > base_closing["closing_cost"]

    # Activity does not change the hard feasibility boundary.
    over_limit = resolve_closing(
        ClosingInput(demand=0.90, intercept_speed_limit=0.80),
        activity=1.00,
    )
    assert over_limit["affordance"] == Affordance.INFEASIBLE

    # Unknown, Disabled, and NotApplicable remain distinct from known zero.
    unknown_activity = resolve_closing(
        ClosingInput(demand=0.50, intercept_speed_limit=0.80),
        activity=None,
        activity_state=InputState.UNKNOWN,
    )
    assert unknown_activity["affordance"] == Affordance.UNKNOWN
    disabled_activity = resolve_closing(
        ClosingInput(demand=0.50, intercept_speed_limit=0.80),
        activity=None,
        activity_state=InputState.DISABLED,
    )
    not_applicable_activity = resolve_closing(
        ClosingInput(demand=0.50, intercept_speed_limit=0.80),
        activity=None,
        activity_state=InputState.NOT_APPLICABLE,
    )
    assert disabled_activity["activity_cost"] == 0.0
    assert not_applicable_activity["activity_cost"] == 0.0

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

    return ["A-closing-limit", "B-activity-soft-cost", "C-activity-does-not-change-hard-feasibility", "D-unknown-disabled-not-applicable", "E-target-value", "F-motivation", "G-affordance", "H-unknown", "I-no-state-valuation-required", "J-optional-state-valuation"]


if __name__ == "__main__":
    print("Complete Feeding Response closure probe passed:", " ".join(run_counterfactuals()))

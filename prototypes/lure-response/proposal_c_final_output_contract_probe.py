"""Proposal C final output contract probe.

Topology probe only. Numeric mappings are illustrative and are not production formulas.
Validates:
- categorical status + continuous strength
- Unknown != resolved zero
- affordance / motivation / target validity boundaries
- max only among resolved explicit alternative siblings
- incomplete required alternatives block final C_mode
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class Resolution(str, Enum):
    COMPLETE = "Complete"
    INCOMPLETE = "Incomplete"


class Affordance(str, Enum):
    FEASIBLE = "Feasible"
    CONSTRAINED = "Constrained"
    INFEASIBLE = "Infeasible"
    UNKNOWN = "Unknown"


class ModeStatus(str, Enum):
    RESOLUTION_INCOMPLETE = "ResolutionIncomplete"
    RESOLVED_NONRESPONSIVE = "ResolvedNonResponsive"
    RESOLVED_RESPONSIVE = "ResolvedResponsive"


@dataclass(frozen=True)
class FeedingModeInput:
    mode_id: str
    resolution: Resolution
    target_valid: Optional[bool]
    target_value: Optional[float]
    motivation: Optional[float]
    affordance: Affordance
    optional_state_modifier: Optional[float] = None
    sibling_group: str = "feeding"
    alternative: bool = True


@dataclass(frozen=True)
class FeedingModeOutput:
    mode_id: str
    status: ModeStatus
    strength: Optional[float]
    reasons: Tuple[str, ...]


def affordance_factor(a: Affordance) -> Optional[float]:
    return {
        Affordance.FEASIBLE: 1.0,
        Affordance.CONSTRAINED: 0.45,
        Affordance.INFEASIBLE: 0.0,
    }.get(a)


def evaluate_mode(x: FeedingModeInput) -> FeedingModeOutput:
    if x.resolution is Resolution.INCOMPLETE:
        return FeedingModeOutput(
            x.mode_id,
            ModeStatus.RESOLUTION_INCOMPLETE,
            None,
            ("resolution_incomplete",),
        )

    if (
        x.target_valid is None
        or x.target_value is None
        or x.motivation is None
        or x.affordance is Affordance.UNKNOWN
    ):
        return FeedingModeOutput(
            x.mode_id,
            ModeStatus.RESOLUTION_INCOMPLETE,
            None,
            ("required_input_unknown",),
        )

    if not x.target_valid:
        return FeedingModeOutput(
            x.mode_id,
            ModeStatus.RESOLVED_NONRESPONSIVE,
            0.0,
            ("target_invalid_for_mode",),
        )

    af = affordance_factor(x.affordance)
    if af == 0.0:
        return FeedingModeOutput(
            x.mode_id,
            ModeStatus.RESOLVED_NONRESPONSIVE,
            0.0,
            ("task_infeasible",),
        )

    modifier = 1.0 if x.optional_state_modifier is None else x.optional_state_modifier
    raw = (
        max(0.0, x.target_value)
        * max(0.0, x.motivation)
        * af
        * max(0.0, modifier)
    )

    # Bounded topology-only proxy. Not a production aggregation formula.
    strength = raw / (1.0 + raw)

    if strength == 0.0:
        return FeedingModeOutput(
            x.mode_id,
            ModeStatus.RESOLVED_NONRESPONSIVE,
            0.0,
            ("resolved_zero_drive",),
        )

    return FeedingModeOutput(
        x.mode_id,
        ModeStatus.RESOLVED_RESPONSIVE,
        strength,
        ("resolved",),
    )


def aggregate_alternative_siblings(outputs, inputs):
    groups = {i.sibling_group for i in inputs}
    assert len(groups) == 1
    assert all(i.alternative for i in inputs)

    # This fixture models a contract where every required alternative in the
    # sibling set must be resolved before the set may produce final C_mode.
    if any(o.status is ModeStatus.RESOLUTION_INCOMPLETE for o in outputs):
        return {"status": "ResolutionIncomplete", "C_mode": None}

    responsive = [
        o for o in outputs if o.status is ModeStatus.RESOLVED_RESPONSIVE
    ]
    if not responsive:
        return {"status": "ResolvedNonResponsive", "C_mode": 0.0}

    winner = max(responsive, key=lambda o: o.strength)
    return {
        "status": "ResolvedResponsive",
        "C_mode": winner.strength,
        "winner": winner.mode_id,
    }


def run_probe():
    base = dict(
        resolution=Resolution.COMPLETE,
        target_valid=True,
        target_value=1.0,
        motivation=0.8,
        affordance=Affordance.FEASIBLE,
    )

    feasible = evaluate_mode(FeedingModeInput("feasible", **base))
    constrained = evaluate_mode(
        FeedingModeInput("constrained", **{**base, "affordance": Affordance.CONSTRAINED})
    )
    infeasible = evaluate_mode(
        FeedingModeInput("infeasible", **{**base, "affordance": Affordance.INFEASIBLE})
    )
    unknown = evaluate_mode(
        FeedingModeInput(
            "unknown",
            resolution=Resolution.COMPLETE,
            target_valid=True,
            target_value=1.0,
            motivation=None,
            affordance=Affordance.FEASIBLE,
        )
    )
    zero_drive = evaluate_mode(
        FeedingModeInput("zero_drive", **{**base, "motivation": 0.0})
    )

    assert feasible.status is ModeStatus.RESOLVED_RESPONSIVE
    assert constrained.status is ModeStatus.RESOLVED_RESPONSIVE
    assert feasible.strength > constrained.strength > 0
    assert infeasible.status is ModeStatus.RESOLVED_NONRESPONSIVE
    assert infeasible.strength == 0.0
    assert unknown.status is ModeStatus.RESOLUTION_INCOMPLETE
    assert unknown.strength is None
    assert zero_drive.status is ModeStatus.RESOLVED_NONRESPONSIVE
    assert zero_drive.strength == 0.0

    # Unknown must never collapse into a resolved zero.
    assert unknown.strength is None and zero_drive.strength == 0.0

    baitfish = FeedingModeInput(
        "baitfish",
        **base,
        sibling_group="feeding_alt",
        alternative=True,
    )
    crayfish = FeedingModeInput(
        "crayfish",
        **{**base, "target_value": 0.7},
        sibling_group="feeding_alt",
        alternative=True,
    )
    baitfish_out = evaluate_mode(baitfish)
    crayfish_out = evaluate_mode(crayfish)
    aggregated = aggregate_alternative_siblings(
        [baitfish_out, crayfish_out], [baitfish, crayfish]
    )
    assert aggregated["winner"] == "baitfish"

    unresolved_alt = FeedingModeInput(
        "unknown_alt",
        resolution=Resolution.COMPLETE,
        target_valid=True,
        target_value=None,
        motivation=0.8,
        affordance=Affordance.FEASIBLE,
        sibling_group="feeding_alt",
        alternative=True,
    )
    unresolved_alt_out = evaluate_mode(unresolved_alt)
    blocked = aggregate_alternative_siblings(
        [baitfish_out, unresolved_alt_out], [baitfish, unresolved_alt]
    )
    assert blocked["status"] == "ResolutionIncomplete"
    assert blocked["C_mode"] is None

    return {
        "status_contract": "categorical + continuous",
        "unknown": "ResolutionIncomplete / no scalar",
        "resolved_zero": "ResolvedNonResponsive / C_mode=0",
        "sibling_max": "only resolved explicit alternatives",
        "incomplete_set": "blocks final C_mode",
    }


if __name__ == "__main__":
    result = run_probe()
    print("Proposal-C final output contract passed")
    for key, value in result.items():
        print(f"{key}: {value}")

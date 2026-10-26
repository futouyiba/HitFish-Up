"""Proposal C Step-4 valuation admission probe.

Purpose:
- attack cadence-motif and imbalance/vulnerability as independent Feeding-mode valuation mechanisms;
- require residual effect after controlling prey support, perception/history,
  TaskDemand/Affordance, dwell/support, and fish-side motivation;
- forbid silent valuation bonuses without mechanism scope and provenance.

This is a topology/admission probe, not biological calibration and not production logic.
"""

from dataclasses import dataclass
from enum import Enum


class Admission(str, Enum):
    ADMITTED = "Admitted"
    CANDIDATE = "CandidateUnresolved"
    REJECTED = "Rejected"


@dataclass(frozen=True)
class ControlledContext:
    prey_support: float = 0.90
    perception_support: float = 0.80
    intercept_demand: float = 0.40
    maneuver_demand: float = 0.20
    temporal_dwell_support: float = 0.70
    feeding_motivation: float = 0.80


@dataclass(frozen=True)
class ValuationCandidate:
    name: str
    mechanism_scope: str
    evidence_independent_of_existing_routes: bool
    controlled_residual_reversal: bool
    player_learnable: bool
    provenance: str | None


def same_controls(a: ControlledContext, b: ControlledContext):
    return a == b


def admission(candidate: ValuationCandidate):
    # No anonymous bonus: a route must have semantic scope and provenance.
    if not candidate.mechanism_scope or not candidate.provenance:
        return Admission.REJECTED

    # Independent valuation DOF is admitted only if it survives a controlled
    # residual test and buys learnable ranking power beyond existing owners.
    if (
        candidate.evidence_independent_of_existing_routes
        and candidate.controlled_residual_reversal
        and candidate.player_learnable
    ):
        return Admission.ADMITTED

    return Admission.CANDIDATE


def run_admission_attack():
    baseline = ControlledContext()
    assert same_controls(baseline, ControlledContext())

    # Cadence: practice evidence suggests motif/cadence may matter, but current
    # evidence does not isolate a residual effect after attention, TaskDemand,
    # dwell/support, and motivation are controlled.
    cadence = ValuationCandidate(
        name="cadence_motif",
        mechanism_scope="feeding-mode valuation",
        evidence_independent_of_existing_routes=True,
        controlled_residual_reversal=False,
        player_learnable=True,
        provenance="angler-practice hypothesis; controlled residual evidence pending",
    )
    assert admission(cadence) == Admission.CANDIDATE

    # Vulnerability: general predator-prey literature supports vulnerability as
    # a plausible ecological concept, but this does not yet demonstrate that
    # largemouth bass interpret a lure imbalance cue as vulnerable prey after
    # physical capture geometry and other routes are held fixed.
    vulnerability = ValuationCandidate(
        name="imbalance_like_vulnerability",
        mechanism_scope="target / feeding-mode valuation",
        evidence_independent_of_existing_routes=True,
        controlled_residual_reversal=False,
        player_learnable=True,
        provenance="general predator-prey evidence; LMB-lure residual evidence pending",
    )
    assert admission(vulnerability) == Admission.CANDIDATE

    # A silent state bonus without a named mechanism/provenance is rejected even
    # if someone supplies an apparent tuning delta.
    silent_bonus = ValuationCandidate(
        name="generic_state_bonus",
        mechanism_scope="",
        evidence_independent_of_existing_routes=True,
        controlled_residual_reversal=True,
        player_learnable=True,
        provenance=None,
    )
    assert admission(silent_bonus) == Admission.REJECTED

    # Topology proof: if a future controlled holdout demonstrates a residual,
    # reproducible and learnable reversal, the candidate can be admitted without
    # changing the rest of the contract.
    cadence_validated = ValuationCandidate(
        **{**cadence.__dict__, "controlled_residual_reversal": True}
    )
    vulnerability_validated = ValuationCandidate(
        **{**vulnerability.__dict__, "controlled_residual_reversal": True}
    )
    assert admission(cadence_validated) == Admission.ADMITTED
    assert admission(vulnerability_validated) == Admission.ADMITTED

    return {
        "cadence_motif": admission(cadence).value,
        "imbalance_like_vulnerability": admission(vulnerability).value,
        "generic_state_bonus": admission(silent_bonus).value,
    }


if __name__ == "__main__":
    result = run_admission_attack()
    print("Step-4 valuation admission probe passed:")
    for key, value in result.items():
        print(f"  {key}: {value}")

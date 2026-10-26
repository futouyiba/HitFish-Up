"""Proposal C Step-4 pause dependency / cadence admission probe.

This probe is about ownership and admission discipline, not effect-size calibration.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ControlledState:
    prey_support: float
    task_demand: tuple
    task_affordance: str
    perception_current: str
    attention_history: str
    favorable_geometry_horizon: float
    feeding_motivation: str
    temporal_motif: str | None


@dataclass(frozen=True)
class CadenceEvidence:
    validated_independent_ranking: bool = False
    effect_scope: str | None = None
    provenance: str | None = None


def dependency_audit():
    return {
        "attention_continuity": {
            "owner": "Perception/history",
            "new_scalar_needed": False,
            "reason": "derived from prior perceptual salience + bounded history",
        },
        "prediction_break": {
            "owner": "Transient task/prediction state",
            "new_scalar_needed": False,
            "reason": "derived from trajectory transition; do not duplicate current motion demand",
        },
        "favorable_dwell": {
            "owner": "Temporal support/exposure",
            "new_scalar_needed": False,
            "reason": "duration of favorable state should be represented on time/support, not as pause bonus",
        },
        "cadence_motif": {
            "owner": "Valuation candidate",
            "new_scalar_needed": None,
            "reason": "only residual route after current physics, perception/history and dwell are controlled",
        },
    }


def resolve_cadence_valuation(state: ControlledState, evidence: CadenceEvidence):
    if state.temporal_motif is None:
        return {"status": "NoMotif", "ranking_effect": None}

    if not evidence.validated_independent_ranking:
        return {
            "status": "CandidateUnresolved",
            "motif": state.temporal_motif,
            "ranking_effect": None,
        }

    return {
        "status": "ResolvedByValidatedRule",
        "motif": state.temporal_motif,
        "effect_scope": evidence.effect_scope,
        "ranking_effect": "rule-owned",
        "provenance": evidence.provenance,
    }


def run():
    audit = dependency_audit()
    assert audit["attention_continuity"]["new_scalar_needed"] is False
    assert audit["prediction_break"]["new_scalar_needed"] is False
    assert audit["favorable_dwell"]["new_scalar_needed"] is False
    assert audit["cadence_motif"]["new_scalar_needed"] is None

    common = dict(
        prey_support=0.90,
        task_demand=(0.40, 0.10),
        task_affordance="Feasible",
        perception_current="Detected",
        attention_history="RecentSalientHistory",
        favorable_geometry_horizon=1.00,
        feeding_motivation="High",
    )
    a = ControlledState(**common, temporal_motif="jerk-jerk-pause")
    b = ControlledState(**common, temporal_motif="steady-then-pause")

    # V1: motif differs, but no independent evidence => no ranking is fabricated.
    unresolved = CadenceEvidence()
    va = resolve_cadence_valuation(a, unresolved)
    vb = resolve_cadence_valuation(b, unresolved)
    assert va["status"] == vb["status"] == "CandidateUnresolved"
    assert va["ranking_effect"] is None and vb["ranking_effect"] is None

    # V2: admission requires explicit validated evidence, not a motif name.
    validated = CadenceEvidence(
        validated_independent_ranking=True,
        effect_scope="largemouth_bass/cold_water/jerkbait",
        provenance="future controlled validation",
    )
    va2 = resolve_cadence_valuation(a, validated)
    assert va2["status"] == "ResolvedByValidatedRule"
    assert va2["ranking_effect"] == "rule-owned"

    return {
        "dependency_audit": "attention/prediction/dwell compile into existing owners; no new scalar",
        "cadence_without_validation": "CandidateUnresolved; no fabricated ranking",
        "cadence_admission_gate": "requires independent controlled ranking evidence + scoped provenance",
    }


if __name__ == "__main__":
    for k, v in run().items():
        print(f"{k}: {v}")

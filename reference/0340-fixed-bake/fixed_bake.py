"""0.3.4.0-B Fixed Bake (中鱼因子聚合逻辑化) — Executable Reference.

STATUS: REFERENCE / VALIDATION ONLY — NOT the production implementation.

Purpose (task: 0.3.4.0 Fixed Bake / Executable Reference x Implementation
Readiness Validation): prove, by one real vertical implementation, which parts of
the Current 0.3.4.0-B Fixed Bake contract are uniquely implementable, and surface
the parts that are not. Nothing here is promoted; every behaviour below is
traceable to a Current Notion page (see docs/implementation-readiness.md §1).

Authority read 2026-09-18 (Notion, FCF tree):
  - 中鱼0.3.4.0-B｜中鱼因子聚合逻辑化（Fixed Template Bake）        (branch root)
  - 中鱼0.3.4.0-B｜开发需求                                          CANONICAL for
    Role/Gate semantics (§3.3, §4.5) and aggregation formulas (§3.4, §7 goldens)
  - 0.3.4.0-B｜Bake Runtime Algorithm & Authoring Contract            (W4B Current Spine)
  - 0.3.4.0-B｜Bake Authoring Schema & Validator Contract             (W4B Current)
  - 0.3.4.0-B｜Authoring & Resolve Contract                           (W4B Current)
  - 0.3.4.0-B｜Bass NORMAL Fixed Template Vertical Slice              (P0 golden fixtures)
  - Checkpoint｜0.3.4.0-B Main Agent Control §25.6 / §26               (owner rulings)

SUPERSEDED premises — deliberately NOT implemented (see docs/implementation-gap.md):
  * `GatePolicy` field / HARD_EXCLUDE|TRACE_RESIDUAL|LOW_RESIDUAL
      -> DELETED 2026-09-17. Gate is automatic for CORE; no policy field.
  * Gate "Failure Cap" `min(RawEnvCoeff, min(failedGateCaps))`
      -> replaced by the gate-failure BRANCH: background -> envCoeffMin, else -> 0.
  * `ConditionRole = CORE|SECONDARY|OFF`
      -> `AggregationRole = CORE|SECONDARY|IGNORED` (OFF/EXCLUDED = migration aliases).
  * `SecondaryLoss = min((1/6)*Σ -ln(fit), 0.5*-ln(0.60))`
      -> `SecondaryFactor = 1 - (1 - SecondaryProduct)/4` (range [0.75, 1.0]).
  * output name `SpatialOpportunityIntensity`
      -> `SpatialDistributionWeight` (= BaseOpportunityIntensity x FinalEnvCoeff).
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any, Dict, List, Mapping, Optional, Sequence

# --------------------------------------------------------------------------- #
# Contract tokens
# --------------------------------------------------------------------------- #

CORE = "CORE"
SECONDARY = "SECONDARY"
IGNORED = "IGNORED"

#: legacy tokens accepted on read only; never written (Main Control §26.4 #8)
_MIGRATION_IGNORED_ALIASES = frozenset({"OFF", "EXCLUDED"})

#: a serialized gatePolicy key is legacy; only "absent" or explicit NONE is inert
_INERT_GATE_POLICY = (None, "NONE")

#: the four fixed P0 condition slots, in canonical (system) order. Order is a
#: presentation/iteration order only -- aggregation is commutative (see §3.4).
CONDITION_KEYS = ("TEMPERATURE", "STRUCTURE", "FEEDING_LAYER", "TIME_PERIOD")

#: conditions whose gate criterion is "lookup coefficient is exactly 0"
_DISCRETE_CONDITIONS = frozenset({"STRUCTURE", "FEEDING_LAYER", "TIME_PERIOD"})

FACTOR_SEMANTIC_IDS = {
    "TEMPERATURE": "TEMPERATURE_SUITABILITY",
    "STRUCTURE": "STRUCTURE_FIT",
    "FEEDING_LAYER": "FEEDING_LAYER_FIT",
    "TIME_PERIOD": "TIME_PERIOD_OPPORTUNITY_FIT",
}

#: 开发需求 §4.6 / Schema §5.1: background floor range is (0, 0.30]
ENV_COEFF_MIN_UPPER = 0.30

#: gate-failure branch labels (trace only)
BRANCH_BACKGROUND_FLOOR = "BACKGROUND_ENVCOEFFMIN"
BRANCH_NON_BACKGROUND = "NON_BACKGROUND_ZERO"


class BakeConfigError(ValueError):
    """Config / input is not legal under the Current 0.3.4.0-B contract."""


# --------------------------------------------------------------------------- #
# Temperature curve  (开发需求 §4.3)
# --------------------------------------------------------------------------- #

def point_fit(temperature: float, profile: Mapping[str, Any]) -> float:
    """TemperatureFit = PointFit(representativeTemp).

    偏好区内 = 1.00；可接受区间外 = 0.00；过渡段 LINEAR = u，SMOOTHSTEP = u^2(3-2u).

    Degenerate bands (accept_min == fav_min, or fav_max == accept_max) are legal
    under the stated hard constraint and are unreachable inside this branch order:
    if the band is empty the point is already classified by the checks above, so
    the `u` division is never evaluated with a zero span. (GAP-008)
    """
    a_min = profile["temp_accept_min"]
    a_max = profile["temp_accept_max"]
    f_min = profile["temp_fav_min"]
    f_max = profile["temp_fav_max"]

    if temperature < a_min or temperature > a_max:
        return 0.0
    if f_min <= temperature <= f_max:
        return 1.0

    if temperature < f_min:
        span = f_min - a_min
        u = (temperature - a_min) / span
    else:
        span = a_max - f_max
        u = (a_max - temperature) / span

    u = min(1.0, max(0.0, u))  # defensive only; u is in [0,1] by construction
    shape = profile["falloff_shape"]
    if shape == "LINEAR":
        return u
    if shape == "SMOOTHSTEP":
        return u * u * (3.0 - 2.0 * u)
    raise BakeConfigError("falloff_shape must be LINEAR or SMOOTHSTEP, got %r" % (shape,))


# --------------------------------------------------------------------------- #
# Inputs / resolve
# --------------------------------------------------------------------------- #

def _binding_rows(subject: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    rows = subject.get("resolvedSpatialOpportunityBindings")
    if not isinstance(rows, list):
        raise BakeConfigError("subject.resolvedSpatialOpportunityBindings must be a list")
    out: Dict[str, Mapping[str, Any]] = {}
    for row in rows:
        key = row.get("conditionKey")
        if key not in CONDITION_KEYS:
            raise BakeConfigError("unknown conditionKey %r" % (key,))
        if key in out:
            raise BakeConfigError("duplicate binding for %s" % key)
        out[key] = row
    return out


def role_of(key: str, row: Mapping[str, Any]) -> str:
    """Resolve AggregationRole for one binding row.

    Missing-vs-ignored: an *explicit* `null` or an explicit token resolves to
    IGNORED (Bass Vertical Slice §5 renders `"aggregationRole": null` = IGNORED).
    A *missing* binding row is a resolve error, not an ignore -- 开发需求 §4.5
    guardrail 2: "忽略 = 作者显式决定 ... 后者仍是错误".
    See GAP-003: authority is split on whether `null` alone is explicit enough.

    A legacy `gatePolicy` key is handled per GAP-004 (two Current clauses disagree):
    an inert value is read through, any other is rejected.
    """
    if "gatePolicy" in row and row["gatePolicy"] not in _INERT_GATE_POLICY:
        raise BakeConfigError(
            "%s: legacy gatePolicy=%r present. The Current contract has no GatePolicy "
            "field (gate is automatic for CORE); lift the intent explicitly to CORE or "
            "SECONDARY -- silent coercion is forbidden." % (key, row["gatePolicy"]))
    token = row.get("aggregationRole")
    if token is None or token == IGNORED or token in _MIGRATION_IGNORED_ALIASES:
        return IGNORED
    if token in (CORE, SECONDARY):
        return token
    raise BakeConfigError("%s: unknown aggregationRole %r" % (key, token))


def validate(subject: Mapping[str, Any], seed: Mapping[str, Any]) -> None:
    """Minimal main-chain validation (Schema & Validator §5 / 开发需求 §8).

    Only the invariants the main chain actually consumes. Validator ownership of
    authored file content is out of scope for this reference.
    """
    _binding_rows(subject)  # raises on unknown / duplicate / missing list

    if not seed.get("fishPondRef"):
        raise BakeConfigError("seed.fishPondRef is required (Schema §5)")
    if seed.get("fishQualityRef") != subject.get("fishQualityRef"):
        raise BakeConfigError(
            "seed.fishQualityRef must equal subject.fishQualityRef (Schema §5)")

    base = seed.get("baseOpportunityIntensity")
    if not isinstance(base, (int, float)) or isinstance(base, bool):
        raise BakeConfigError("seed.baseOpportunityIntensity must be a number")
    if base != base or base < 0:  # NaN or negative
        raise BakeConfigError("seed.baseOpportunityIntensity must be finite and >= 0")

    is_bg = seed.get("isBackgroundFish")
    if not isinstance(is_bg, bool):
        raise BakeConfigError("seed.isBackgroundFish must be an explicit bool (Schema §7)")

    floor = seed.get("envCoeffMin")
    if is_bg:
        if floor is None:
            raise BakeConfigError("background fish must declare envCoeffMin (开发需求 §4.7)")
        if not (0.0 < floor <= ENV_COEFF_MIN_UPPER):
            raise BakeConfigError("envCoeffMin must be in (0, %.2f], got %r"
                                  % (ENV_COEFF_MIN_UPPER, floor))
    elif floor is not None:
        raise BakeConfigError("non-background fish must not author envCoeffMin (Schema §5)")


# --------------------------------------------------------------------------- #
# Component evaluators  (finite registry; 4 P0 slots only)
# --------------------------------------------------------------------------- #

def _profile_for(profiles: Mapping[str, Any], key: str) -> Any:
    if key not in profiles:
        raise BakeConfigError("missing required profile for active condition %s" % key)
    return profiles[key]


def evaluate_fit(key: str, profiles: Mapping[str, Any],
                 condition_group: Mapping[str, Any]) -> Any:
    """fact + profile -> FactorFit. No Gate consequence, no Floor, no Base."""
    if key == "TEMPERATURE":
        profile = _profile_for(profiles, key)
        rng = condition_group["waterTemperatureRange"]
        representative = (rng[0] + rng[1]) / 2.0
        return point_fit(representative, profile), rng

    if key == "STRUCTURE":
        profile = _profile_for(profiles, key)
        structure_type = condition_group["structureType"]
        table = profile["structure_affinity"]
        if structure_type not in table:
            raise BakeConfigError("structure_affinity has no entry for %r" % (structure_type,))
        return table[structure_type], structure_type

    if key == "FEEDING_LAYER":
        profile = _profile_for(profiles, key)
        layers = condition_group["feedingEcologyLayers"]
        if not layers:
            raise BakeConfigError(
                "feedingEcologyLayers is empty; max() over an empty layer set is "
                "undefined by the Current contract (GAP-006)")
        affinities = [
            {"SURFACE": profile["foraging_surface_affinity"],
             "MIDDLE": profile["foraging_middle_affinity"],
             "BOTTOM": profile["foraging_bottom_affinity"]}[layer]
            for layer in layers
        ]
        return max(affinities), list(layers)

    if key == "TIME_PERIOD":
        profile = _profile_for(profiles, key)
        period = condition_group["timePeriod"]
        table = profile["time_period_activity_coefficient"]
        if period not in table:
            raise BakeConfigError("time_period table has no entry for %r" % (period,))
        return table[period], period

    raise BakeConfigError("no evaluator registered for %s" % key)


def gate_failed(key: str, fit: float, profiles: Mapping[str, Any]) -> Optional[bool]:
    """Gate criterion -- fixed per condition kind, no author control (开发需求 §3.3).

    Returns None when the condition carries no gate (SECONDARY / IGNORED).
    """
    if key in _DISCRETE_CONDITIONS:
        return fit == 0.0
    if key == "TEMPERATURE":
        profile = _profile_for(profiles, key)
        return fit < profile["temp_threshold"]
    return None


# --------------------------------------------------------------------------- #
# Fixed Bake Template Program  (系统拥有; author controls nothing here)
# --------------------------------------------------------------------------- #

def evaluate(subject: Mapping[str, Any], seed: Mapping[str, Any],
             condition_group: Mapping[str, Any]) -> Dict[str, Any]:
    """Resolved subject + resolved seed + ConditionGroup -> weight + Trace.

    Returns the SpatialDistributionWeight together with a structured Trace that
    explains where it came from (开发需求 §3.5 / Authoring & Resolve §4).
    """
    validate(subject, seed)
    rows = _binding_rows(subject)
    profiles = subject["resolvedComponentProfiles"]
    roles = {key: role_of(key, rows[key]) for key in CONDITION_KEYS if key in rows}

    factor_results: List[Dict[str, Any]] = []
    gate_results: List[Dict[str, Any]] = []
    fits: Dict[str, float] = {}

    for key in CONDITION_KEYS:
        if key not in roles:
            raise BakeConfigError(
                "no binding row for %s; missing != ignored (开发需求 §4.5)" % key)
        role = roles[key]
        if role == IGNORED:
            gate_results.append({
                "conditionKey": key,
                "aggregationRole": role,
                "gateEvaluated": False,
                "passed": None,
                "criterion": "ignored: evaluator not run, no gate",
            })
            continue

        fit, raw_inputs = evaluate_fit(key, profiles, condition_group)
        fits[key] = fit
        passed = None
        criterion = "no gate (SECONDARY)"
        if role == CORE:
            passed = not gate_failed(key, fit, profiles)
            criterion = ("lookup coefficient == 0" if key in _DISCRETE_CONDITIONS
                         else "PointFit(representativeTemp) < temp_threshold")
            gate_results.append({
                "conditionKey": key, "aggregationRole": role, "gateEvaluated": True,
                "passed": passed, "criterion": criterion, "fit": fit,
            })
        else:
            gate_results.append({
                "conditionKey": key, "aggregationRole": role, "gateEvaluated": False,
                "passed": None, "criterion": criterion, "fit": fit,
            })

        factor_results.append({
            "conditionKey": key,
            "factorSemanticId": FACTOR_SEMANTIC_IDS[key],
            "aggregationRole": role,
            "rawInputs": raw_inputs,
            "rawFit": fit,
            # Current contract applies NO >=0.05 soft clamp to applied fit; the two
            # are equal by construction and kept separate only for trace fidelity.
            "appliedFit": fit,
            "loss": (-math.log(fit)) if fit > 0 else None,
        })

    failed = [g["conditionKey"] for g in gate_results
              if g["gateEvaluated"] and not g["passed"]]

    core_product: Optional[float] = None
    secondary_product: Optional[float] = None
    secondary_factor: Optional[float] = None
    raw_env_coeff: Optional[float] = None
    core_loss: Optional[float] = None
    background_floor_applied = False
    branch: Optional[Dict[str, Any]] = None

    if failed:
        # Gate failure is a path boundary: the aggregate is NOT applied (§3.4).
        if seed["isBackgroundFish"]:
            final_env_coeff = seed["envCoeffMin"]
            name = BRANCH_BACKGROUND_FLOOR
        else:
            final_env_coeff = 0.0
            name = BRANCH_NON_BACKGROUND
        branch = {"applied": True, "branch": name, "failedConditions": failed}
    else:
        core_fits = [fits[k] for k in CONDITION_KEYS if roles.get(k) == CORE]
        secondary_fits = [fits[k] for k in CONDITION_KEYS if roles.get(k) == SECONDARY]
        core_product = _product(core_fits)
        secondary_product = _product(secondary_fits)
        secondary_factor = 1.0 - (1.0 - secondary_product) / 4.0
        raw_env_coeff = core_product * secondary_factor
        core_loss = None if any(f <= 0.0 for f in core_fits) else -sum(
            math.log(f) for f in core_fits)
        if seed["isBackgroundFish"]:
            final_env_coeff = max(raw_env_coeff, seed["envCoeffMin"])
            background_floor_applied = final_env_coeff > raw_env_coeff
        else:
            final_env_coeff = raw_env_coeff

    return {
        "subjectIdentity": subject["fishQualityRef"],
        "baseOpportunityIntensity": seed["baseOpportunityIntensity"],
        "isBackgroundFish": seed["isBackgroundFish"],
        "envCoeffMin": seed.get("envCoeffMin"),
        "conditionGroup": dict(condition_group),
        "gateResults": gate_results,
        "factorResults": factor_results,
        "coreProduct": core_product,
        "secondaryProduct": secondary_product,
        "secondaryFactor": secondary_factor,
        "coreLoss": core_loss,
        # superseded keys, retained only so the Trace shape matches Schema §3.8;
        # always None under the post-2026-09-17 aggregation (see GAP-001)
        "secondaryLossRaw": None,
        "secondaryLossApplied": None,
        "rawEnvCoeff": raw_env_coeff,
        "gateFailureBranch": branch,
        "backgroundFloorApplied": background_floor_applied,
        "finalEnvCoeff": final_env_coeff,
        "spatialDistributionWeight": seed["baseOpportunityIntensity"] * final_env_coeff,
    }


def _product(values: Sequence[float]) -> float:
    """Empty product is the multiplicative identity (GAP-007: not stated, only derivable)."""
    out = 1.0
    for value in values:
        out *= value
    return out


# --------------------------------------------------------------------------- #
# Demo: run the P0 Bass Q3 fixture and print one full Trace
# --------------------------------------------------------------------------- #

def _main(argv: Sequence[str]) -> int:
    """Print one full Trace for the P0 Bass fixture (or a given fixture file)."""
    path = argv[1] if len(argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "fixtures", "bass_q3.json")
    with open(path, "r", encoding="utf-8") as handle:
        raw = json.load(handle)
    profiles = raw["componentProfiles"]
    seed = raw["seed"]
    case = json.loads(json.dumps(raw["cases"][0]))
    seed.update(case.get("seedOverride", {}))
    subject = dict(raw["subject"])
    subject["resolvedComponentProfiles"] = profiles
    trace = evaluate(subject, seed, case["conditionGroup"])
    print(json.dumps(trace, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(_main(sys.argv))

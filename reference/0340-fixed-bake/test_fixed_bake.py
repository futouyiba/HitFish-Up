"""Semantic + property tests for the 0.3.4.0-B Fixed Bake executable reference.

REFERENCE / VALIDATION. These tests verify the *contract*, not coverage: each one
names the authority clause it checks. Cases that the Current authority does not
define are marked GAP-xxx and assert only the reference's current behaviour --
those assertions are characterisation, not contract.
"""

from __future__ import annotations

import copy
import json
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fixed_bake as fb  # noqa: E402

FIXTURE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "fixtures", "bass_q3.json")


def load_fixture():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as handle:
        raw = json.load(handle)
    profiles = raw.pop("componentProfiles")
    subject = raw["subject"]
    subject["resolvedComponentProfiles"] = copy.deepcopy(profiles)
    return profiles, subject, raw["seed"], raw["cases"]


PROFILES, BASE_SUBJECT, BASE_SEED, CASES = load_fixture()


def build_subject(roles, profiles=None, omit=()):
    """Build a ResolvedSpatialOpportunitySubject. `roles[key] = None` -> explicit null."""
    rows = []
    for key in fb.CONDITION_KEYS:
        if key in omit:
            continue
        rows.append({"conditionKey": key,
                     "aggregationRole": roles.get(key, fb.IGNORED)})
    return {
        "type": "ResolvedSpatialOpportunitySubject",
        "fishQualityRef": {"speciesId": "LARGEMOUTH_BASS", "fishQualityId": "Q3"},
        "resolvedComponentProfiles": copy.deepcopy(profiles or PROFILES),
        "resolvedSpatialOpportunityBindings": rows,
    }


def build_seed(base=1.0, background=False, env_coeff_min=None):
    seed = {
        "type": "ResolvedOpportunitySeed",
        "fishPondRef": "TEST_POND",
        "fishQualityRef": {"speciesId": "LARGEMOUTH_BASS", "fishQualityId": "Q3"},
        "baseOpportunityIntensity": base,
        "isBackgroundFish": background,
    }
    if env_coeff_min is not None:
        seed["envCoeffMin"] = env_coeff_min
    return seed


def cg(structure="GRASS_EDGE", temperature=(25, 27), layers=("MIDDLE",), period="MORNING"):
    return {"structureType": structure, "waterTemperatureRange": list(temperature),
            "feedingEcologyLayers": list(layers), "timePeriod": period}


BASS_CORE_ROLES = {"TEMPERATURE": fb.CORE, "STRUCTURE": fb.CORE,
                   "FEEDING_LAYER": fb.SECONDARY, "TIME_PERIOD": fb.IGNORED}


class TestFixtureGoldens(unittest.TestCase):
    """The P0 vertical-slice goldens, recomputed independently from 开发需求 §3.4 / §7."""

    def test_all_fixture_cases(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                seed = dict(BASE_SEED)
                seed.update(case.get("seedOverride", {}))
                trace = fb.evaluate(copy.deepcopy(BASE_SUBJECT), seed, case["conditionGroup"])
                expect = case["expect"]
                raw = trace["rawEnvCoeff"]
                if expect["rawEnvCoeff"] is None:
                    self.assertIsNone(raw, "gate failure must not apply the aggregate")
                else:
                    self.assertAlmostEqual(raw, expect["rawEnvCoeff"], places=12)
                self.assertAlmostEqual(trace["finalEnvCoeff"], expect["finalEnvCoeff"], places=12)
                self.assertAlmostEqual(trace["spatialDistributionWeight"], expect["weight"], places=12)
                failed = bool([g for g in trace["gateResults"] if g["passed"] is False])
                self.assertEqual(failed, expect["gateFailed"])


class TestSemanticCases(unittest.TestCase):
    """Task §十 semantic cases, re-expressed against the Current contract."""

    def test_case01_neutral(self):
        """All ordinary fits = 1 -> no environmental loss at all."""
        subject = build_subject({"TEMPERATURE": fb.CORE, "STRUCTURE": fb.CORE,
                                 "FEEDING_LAYER": fb.SECONDARY, "TIME_PERIOD": fb.SECONDARY},
                                profiles=dict(PROFILES,
                                              TIME_PERIOD={"time_period_activity_coefficient":
                                                           {"MORNING": 1.0}}))
        trace = fb.evaluate(subject, build_seed(), cg())
        self.assertAlmostEqual(trace["finalEnvCoeff"], 1.0, places=12)

    def test_case02_single_core_loss(self):
        """One CORE below 1: CoreProduct is that fit itself."""
        trace = fb.evaluate(build_subject(dict(BASS_CORE_ROLES, FEEDING_LAYER=fb.IGNORED)),
                            build_seed(), cg(structure="OPEN"))  # 0.25
        self.assertAlmostEqual(trace["coreProduct"], 0.25, places=12)
        self.assertAlmostEqual(trace["finalEnvCoeff"], 0.25, places=12)

    def test_case03_multiple_core_no_order_dependence(self):
        """Two CORE factors multiply; result is independent of binding order."""
        subject = build_subject(BASS_CORE_ROLES)
        group = cg(structure="DROPOFF", temperature=(15, 15), layers=("BOTTOM",))
        forward = fb.evaluate(subject, build_seed(), group)
        reversed_subject = copy.deepcopy(subject)
        reversed_subject["resolvedSpatialOpportunityBindings"].reverse()
        backward = fb.evaluate(reversed_subject, build_seed(), group)
        self.assertAlmostEqual(forward["finalEnvCoeff"], backward["finalEnvCoeff"], places=15)
        self.assertAlmostEqual(forward["finalEnvCoeff"], 0.3190909090909091, places=12)

    def test_case04_secondary_weak_loss(self):
        """One SECONDARY at 0.60 moves the result at most to 0.90, never to 0.60."""
        single = fb.evaluate(build_subject(dict(BASS_CORE_ROLES, FEEDING_LAYER=fb.IGNORED)),
                             build_seed(), cg(layers=("BOTTOM",)))
        with_secondary = fb.evaluate(build_subject(BASS_CORE_ROLES), build_seed(), cg(layers=("BOTTOM",)))
        self.assertAlmostEqual(single["finalEnvCoeff"], 1.0, places=12)
        self.assertAlmostEqual(with_secondary["secondaryFactor"], 0.90, places=12)
        self.assertAlmostEqual(with_secondary["finalEnvCoeff"], 0.90, places=12)

    def test_case05_secondary_accumulation_is_bounded(self):
        """More SECONDARY conditions accumulate but can never cut more than 25%."""
        profiles = dict(PROFILES, TIME_PERIOD={
            "time_period_activity_coefficient": {"MORNING": 0.60}})
        three = build_subject({"TEMPERATURE": fb.CORE, "STRUCTURE": fb.CORE,
                               "FEEDING_LAYER": fb.SECONDARY, "TIME_PERIOD": fb.SECONDARY},
                              profiles=profiles)
        trace = fb.evaluate(three, build_seed(), cg(layers=("BOTTOM",), period="MORNING"))
        # SecondaryProduct = 0.6 * 0.6 = 0.36 -> SecondaryFactor = 1 - 0.64/4 = 0.84
        self.assertAlmostEqual(trace["secondaryFactor"], 0.84, places=12)
        self.assertGreaterEqual(trace["secondaryFactor"], 0.75 - 1e-12)

    def test_case05b_secondary_saturates_at_floor(self):
        """Even absurdly bad SECONDARY fits bottom out at 0.75, never lower."""
        profiles = dict(PROFILES, TIME_PERIOD={
            "time_period_activity_coefficient": {"MORNING": 0.0}})
        subject = build_subject({"TEMPERATURE": fb.CORE, "STRUCTURE": fb.CORE,
                                 "FEEDING_LAYER": fb.SECONDARY, "TIME_PERIOD": fb.SECONDARY},
                                profiles=profiles)
        trace = fb.evaluate(subject, build_seed(), cg(layers=("BOTTOM",), period="MORNING"))
        self.assertAlmostEqual(trace["secondaryFactor"], 0.75, places=12)

    def test_case06_gate_hard_exclude(self):
        """Discrete gate: authoring exactly 0 excludes the fish (non-background -> 0)."""
        profiles = dict(PROFILES, STRUCTURE={"structure_affinity": {"OPEN": 0.0}})
        trace = fb.evaluate(build_subject(BASS_CORE_ROLES, profiles=profiles),
                            build_seed(), cg(structure="OPEN"))
        self.assertEqual(trace["finalEnvCoeff"], 0.0)
        self.assertEqual(trace["gateFailureBranch"]["branch"], fb.BRANCH_NON_BACKGROUND)

    def test_case07_residual_gate_is_not_a_third_tier(self):
        """A near-zero-but-nonzero discrete coefficient is NOT a gate failure."""
        profiles = dict(PROFILES, STRUCTURE={"structure_affinity": {"OPEN": 0.02}})
        trace = fb.evaluate(build_subject(BASS_CORE_ROLES, profiles=profiles),
                            build_seed(), cg(structure="OPEN"))
        self.assertIsNone(trace["gateFailureBranch"])
        self.assertAlmostEqual(trace["coreProduct"], 0.02, places=12)

    def test_case08_gate_never_raises_the_result(self):
        """Counterfactual: the same fits with the gate forced open are never lower.

        3C sits inside the [2, 24] ramp, so TemperatureFit = 1/22 = 0.045 < 0.05 --
        i.e. a genuinely failing gate whose fit is not 0. This is the case that
        distinguishes the Current failure-branch from the superseded failure-cap.
        """
        group = cg(temperature=(3, 3))
        gated = fb.evaluate(build_subject(BASS_CORE_ROLES),
                            build_seed(background=True, env_coeff_min=0.1), group)
        open_profiles = dict(PROFILES, TEMPERATURE=dict(PROFILES["TEMPERATURE"], temp_threshold=0.0))
        opened = fb.evaluate(build_subject(BASS_CORE_ROLES, profiles=open_profiles),
                             build_seed(background=True, env_coeff_min=0.1), group)
        self.assertTrue(gated["gateFailureBranch"]["applied"])
        self.assertIsNone(opened["gateFailureBranch"])
        self.assertLessEqual(gated["finalEnvCoeff"], opened["finalEnvCoeff"] + 1e-12)

    def test_case09_multiple_failed_gates_collapse_to_one_branch(self):
        """Several failed CORE gates do not combine -- the branch is single-valued."""
        profiles = dict(PROFILES, STRUCTURE={"structure_affinity": {"OPEN": 0.0}})
        trace = fb.evaluate(build_subject(BASS_CORE_ROLES, profiles=profiles),
                            build_seed(background=True, env_coeff_min=0.1),
                            cg(structure="OPEN", temperature=(36, 36)))
        self.assertEqual(sorted(trace["gateFailureBranch"]["failedConditions"]),
                         ["STRUCTURE", "TEMPERATURE"])
        self.assertEqual(trace["finalEnvCoeff"], 0.1)

    def test_case10_background_floor_without_gate_failure(self):
        trace = fb.evaluate(build_subject(BASS_CORE_ROLES),
                            build_seed(background=True, env_coeff_min=0.1),
                            cg(structure="OPEN", temperature=(5, 5), layers=("SURFACE",)))
        self.assertFalse(bool(trace["gateFailureBranch"]))
        self.assertTrue(trace["backgroundFloorApplied"])
        self.assertAlmostEqual(trace["rawEnvCoeff"], 0.03068181818181818, places=12)
        self.assertEqual(trace["finalEnvCoeff"], 0.1)

    def test_case11_gate_failure_outranks_background_floor(self):
        """On gate failure the floor is not applied as a max(); the branch value is used."""
        trace = fb.evaluate(build_subject(BASS_CORE_ROLES),
                            build_seed(background=True, env_coeff_min=0.1),
                            cg(temperature=(36, 36)))
        self.assertTrue(trace["gateFailureBranch"]["applied"])
        self.assertFalse(trace["backgroundFloorApplied"])
        self.assertEqual(trace["finalEnvCoeff"], 0.1)
        self.assertIsNone(trace["rawEnvCoeff"])

    def test_case12_base_opportunity_scales_the_output(self):
        """Same EnvCoeff, different Base -> SpatialDistributionWeight scales linearly."""
        subject = build_subject(BASS_CORE_ROLES)
        one = fb.evaluate(subject, build_seed(base=1.0), cg(structure="DROPOFF", temperature=(15, 15)))
        four = fb.evaluate(subject, build_seed(base=4.0), cg(structure="DROPOFF", temperature=(15, 15)))
        self.assertAlmostEqual(one["finalEnvCoeff"], four["finalEnvCoeff"], places=15)
        self.assertAlmostEqual(four["spatialDistributionWeight"],
                               4.0 * one["spatialDistributionWeight"], places=12)

    def test_case12b_zero_base_never_creates_weight(self):
        trace = fb.evaluate(build_subject(BASS_CORE_ROLES),
                            build_seed(base=0.0, background=True, env_coeff_min=0.1),
                            cg(structure="OPEN", temperature=(5, 5), layers=("SURFACE",)))
        self.assertEqual(trace["finalEnvCoeff"], 0.1)
        self.assertEqual(trace["spatialDistributionWeight"], 0.0)

    def test_case13_out_of_range_authored_fit(self):
        """GAP-005 characterisation: authority does not define runtime handling of an
        out-of-range authored value. The reference deliberately does NOT clamp and does
        NOT invent a default; it lets the value through. NOT a contract assertion."""
        profiles = dict(PROFILES, STRUCTURE={"structure_affinity": {"OPEN": 1.5}})
        trace = fb.evaluate(build_subject(BASS_CORE_ROLES, profiles=profiles),
                            build_seed(), cg(structure="OPEN"))
        self.assertAlmostEqual(trace["coreProduct"], 1.5, places=12)  # > 1 -- undefined by contract

    def test_case14_missing_binding_row_is_an_error_not_an_ignore(self):
        """开发需求 §4.5 guardrail 2: 'missing' and 'ignored' are different things."""
        subject = build_subject(BASS_CORE_ROLES)
        subject["resolvedSpatialOpportunityBindings"] = [
            r for r in subject["resolvedSpatialOpportunityBindings"]
            if r["conditionKey"] != "TEMPERATURE"]
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(subject, build_seed(), cg())

    def test_case14b_missing_active_profile_is_an_error(self):
        profiles = dict(PROFILES)
        del profiles["STRUCTURE"]
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(build_subject(BASS_CORE_ROLES, profiles=profiles), build_seed(), cg())

    def test_case14c_ignored_condition_needs_no_profile(self):
        """Bass Slice §3.5: an IGNORED slot must not force a fabricated profile."""
        subject = build_subject(BASS_CORE_ROLES)  # TIME_PERIOD omitted from profiles
        trace = fb.evaluate(subject, build_seed(), cg())
        self.assertNotIn("TIME_PERIOD", [f["conditionKey"] for f in trace["factorResults"]])
        period_gate = [g for g in trace["gateResults"] if g["conditionKey"] == "TIME_PERIOD"][0]
        self.assertEqual(period_gate["aggregationRole"], fb.IGNORED)
        self.assertFalse(period_gate["gateEvaluated"])
        self.assertNotIn("fit", period_gate)

    def test_case15_trace_explains_the_result(self):
        """Every stage difference is visible in the Trace (开发需求 §3.5, Authoring §4)."""
        trace = fb.evaluate(build_subject(BASS_CORE_ROLES), build_seed(),
                            cg(structure="DROPOFF", temperature=(15, 15), layers=("BOTTOM",)))
        for key in ("subjectIdentity", "baseOpportunityIntensity", "conditionGroup",
                    "gateResults", "factorResults", "coreProduct", "secondaryProduct",
                    "secondaryFactor", "rawEnvCoeff", "gateFailureBranch",
                    "backgroundFloorApplied", "finalEnvCoeff", "spatialDistributionWeight"):
            self.assertIn(key, trace)
        by_key = {f["conditionKey"]: f for f in trace["factorResults"]}
        self.assertAlmostEqual(by_key["TEMPERATURE"]["rawFit"], 13 / 22, places=12)
        self.assertAlmostEqual(by_key["STRUCTURE"]["rawFit"], 0.60, places=12)
        self.assertAlmostEqual(trace["coreProduct"], 13 / 22 * 0.60, places=12)
        self.assertAlmostEqual(trace["secondaryFactor"], 0.90, places=12)
        self.assertAlmostEqual(trace["finalEnvCoeff"], 0.3190909090909091, places=12)


class TestMigrationAndLegacy(unittest.TestCase):
    """W5 migration rules: legacy tokens are read, never silently coerced."""

    def test_legacy_off_without_gate_is_ignored(self):
        subject = build_subject(BASS_CORE_ROLES)
        for row in subject["resolvedSpatialOpportunityBindings"]:
            if row["conditionKey"] == "TIME_PERIOD":
                row["aggregationRole"] = "EXCLUDED"
        trace = fb.evaluate(subject, build_seed(), cg())
        self.assertNotIn("TIME_PERIOD", [f["conditionKey"] for f in trace["factorResults"]])

    def test_legacy_off_with_gate_policy_is_rejected_not_coerced(self):
        """Schema §5.1: OFF + non-NONE GatePolicy requires an explicit content decision."""
        subject = build_subject(BASS_CORE_ROLES)
        for row in subject["resolvedSpatialOpportunityBindings"]:
            if row["conditionKey"] == "TIME_PERIOD":
                row["aggregationRole"] = "OFF"
                row["gatePolicy"] = "TRACE_RESIDUAL"
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(subject, build_seed(), cg())

    def test_legacy_off_with_none_gate_policy_normalises_to_ignored(self):
        subject = build_subject(BASS_CORE_ROLES)
        for row in subject["resolvedSpatialOpportunityBindings"]:
            if row["conditionKey"] == "TIME_PERIOD":
                row["aggregationRole"] = "OFF"
                row["gatePolicy"] = "NONE"
        trace = fb.evaluate(subject, build_seed(), cg())
        self.assertAlmostEqual(trace["finalEnvCoeff"], 1.0, places=12)


class TestValidation(unittest.TestCase):
    def test_background_requires_floor(self):
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(build_subject(BASS_CORE_ROLES), build_seed(background=True), cg())

    def test_non_background_must_not_author_floor(self):
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(build_subject(BASS_CORE_ROLES),
                        build_seed(background=False, env_coeff_min=0.1), cg())

    def test_floor_upper_bound(self):
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(build_subject(BASS_CORE_ROLES),
                        build_seed(background=True, env_coeff_min=0.31), cg())

    def test_seed_quality_must_match_subject(self):
        seed = build_seed()
        seed["fishQualityRef"] = {"speciesId": "LARGEMOUTH_BASS", "fishQualityId": "Q4"}
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(build_subject(BASS_CORE_ROLES), seed, cg())

    def test_negative_base_rejected(self):
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(build_subject(BASS_CORE_ROLES), build_seed(base=-1.0), cg())

    def test_duplicate_binding_rejected(self):
        subject = build_subject(BASS_CORE_ROLES)
        subject["resolvedSpatialOpportunityBindings"].append(
            {"conditionKey": "TEMPERATURE", "aggregationRole": "CORE"})
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(subject, build_seed(), cg())

    def test_empty_layer_set_is_undefined(self):
        """GAP-006: max() over an empty layer set is not defined by the contract."""
        with self.assertRaises(fb.BakeConfigError):
            fb.evaluate(build_subject(BASS_CORE_ROLES), build_seed(), cg(layers=()))


class TestPropertyInvariants(unittest.TestCase):
    """Invariants derived from the contract; the task §十八 list, corrected where
    the Current contract differs from the superseded failure-cap model."""

    def _random_case(self, rng):
        return cg(
            structure=rng.choice(["GRASS_EDGE", "DROPOFF", "ROCK", "OPEN", "COMPLEX_WOOD"]),
            temperature=(rng.uniform(0, 40), rng.uniform(0, 40)),
            layers=rng.sample(["SURFACE", "MIDDLE", "BOTTOM"], rng.randint(1, 3)),
        )

    def test_p1_determinism(self):
        rng = random.Random(20260918)
        subject = build_subject(BASS_CORE_ROLES)
        for _ in range(200):
            group = self._random_case(rng)
            is_background = rng.random() < 0.5
            seed = build_seed(background=is_background,
                              env_coeff_min=rng.uniform(0.01, 0.30) if is_background else None)
            a = fb.evaluate(copy.deepcopy(subject), dict(seed), group)
            b = fb.evaluate(copy.deepcopy(subject), dict(seed), group)
            self.assertEqual(a, b)

    def test_p2_env_coeff_is_bounded(self):
        rng = random.Random(7)
        for _ in range(300):
            trace = fb.evaluate(build_subject(BASS_CORE_ROLES), build_seed(),
                                self._random_case(rng))
            self.assertGreaterEqual(trace["finalEnvCoeff"], 0.0)
            self.assertLessEqual(trace["finalEnvCoeff"], 1.0)

    def test_p3_background_result_never_below_floor(self):
        rng = random.Random(11)
        for _ in range(300):
            trace = fb.evaluate(build_subject(BASS_CORE_ROLES),
                                build_seed(background=True, env_coeff_min=0.12),
                                self._random_case(rng))
            self.assertGreaterEqual(trace["finalEnvCoeff"], 0.12 - 1e-12)

    def test_p4_worsening_a_core_fit_never_raises_the_result(self):
        """Holds in both regions: within the passing region (product), and across the
        gate threshold (the failure branch is bounded by the floor, see GAP-006)."""
        rng = random.Random(3)
        subject = build_subject(BASS_CORE_ROLES)
        for _ in range(200):
            lo, hi = sorted((rng.uniform(0, 20), rng.uniform(0, 20)))
            good = fb.evaluate(subject, build_seed(), cg(temperature=(hi, hi)))
            worse = fb.evaluate(subject, build_seed(), cg(temperature=(lo, lo)))
            self.assertLessEqual(worse["finalEnvCoeff"], good["finalEnvCoeff"] + 1e-12)

    def test_p5_extra_secondary_factor_never_raises_the_result(self):
        profiles = dict(PROFILES, TIME_PERIOD={
            "time_period_activity_coefficient": {"MORNING": 0.75}})
        without = fb.evaluate(build_subject(BASS_CORE_ROLES), build_seed(), cg())
        with_extra = fb.evaluate(
            build_subject({"TEMPERATURE": fb.CORE, "STRUCTURE": fb.CORE,
                           "FEEDING_LAYER": fb.SECONDARY, "TIME_PERIOD": fb.SECONDARY},
                          profiles=profiles), build_seed(), cg(period="MORNING"))
        self.assertLessEqual(with_extra["finalEnvCoeff"], without["finalEnvCoeff"] + 1e-12)

    def test_p6_binding_order_does_not_change_the_result(self):
        rng = random.Random(101)
        for _ in range(100):
            group = self._random_case(rng)
            subject = build_subject(BASS_CORE_ROLES)
            baseline = fb.evaluate(subject, build_seed(), group)
            shuffled = copy.deepcopy(subject)
            rng.shuffle(shuffled["resolvedSpatialOpportunityBindings"])
            self.assertEqual(fb.evaluate(shuffled, build_seed(), group), baseline)

    def test_p7_secondary_factor_range_is_exactly_75_to_100(self):
        rng = random.Random(55)
        profiles = dict(PROFILES, TIME_PERIOD={
            "time_period_activity_coefficient": {"MORNING": rng.random()}})
        for value in (0.0, 0.05, 0.25, 0.6, 1.0):
            profiles["TIME_PERIOD"] = {"time_period_activity_coefficient": {"MORNING": value}}
            subject = build_subject({"TEMPERATURE": fb.CORE, "STRUCTURE": fb.CORE,
                                     "FEEDING_LAYER": fb.SECONDARY, "TIME_PERIOD": fb.SECONDARY},
                                    profiles=profiles)
            trace = fb.evaluate(subject, build_seed(), cg(layers=("BOTTOM",), period="MORNING"))
            self.assertGreaterEqual(trace["secondaryFactor"], 0.75 - 1e-12)
            self.assertLessEqual(trace["secondaryFactor"], 1.0 + 1e-12)

    def test_p8_no_core_bindings_yields_multiplicative_identity(self):
        """GAP-007: authority never states the empty-Core convention; it is only the
        standard product identity. Characterisation, not contract."""
        profiles = dict(PROFILES, TIME_PERIOD={
            "time_period_activity_coefficient": {"MORNING": 0.75}})
        subject = build_subject({"TEMPERATURE": fb.SECONDARY, "STRUCTURE": fb.SECONDARY,
                                 "FEEDING_LAYER": fb.SECONDARY, "TIME_PERIOD": fb.SECONDARY},
                                profiles=profiles)
        trace = fb.evaluate(subject, build_seed(), cg(period="MORNING"))
        self.assertAlmostEqual(trace["coreProduct"], 1.0, places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)

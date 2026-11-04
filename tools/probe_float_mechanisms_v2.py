#!/usr/bin/env python3
"""Explicit gameplay hypotheses; no species facts or production probabilities."""
import argparse
import json
import math
from pathlib import Path
import unittest


def check(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError("finite nonnegative value required")
    return value


def relation(signatures, profile):
    labels = {profile.get(s, "NEUTRAL") for s in set(signatures)}
    if labels - {"POSITIVE", "NEUTRAL", "AVOID"}:
        raise ValueError("unknown relation")
    return "AVOID" if "AVOID" in labels else "POSITIVE" if "POSITIVE" in labels else "NEUTRAL"


def physical(edible_mass, binder, t):
    check(edible_mass)
    check(t)
    # Presets are authored experimental treatments, not measured material laws.
    release, loss, bottom = {"open": (0.6, 0.12, 0.35), "bound": (0.06, 0.02, 0.9)}[binder]
    available = edible_mass * release * (math.exp(-release * t) - math.exp(-loss * t)) / (loss - release)
    return {"bottom": available * bottom, "suspended": available * (1 - bottom),
            "stored": edible_mass * math.exp(-release * t),
            "lost": edible_mass - available - edible_mass * math.exp(-release * t)}


def response(hook_food, hook_utilization, hook_signatures, background_signatures,
             free_objects, preference, cue_profile, hook_profile, layer="bottom",
             max_size=2, background_gain=0.5):
    h = check(hook_food)
    u = check(hook_utilization)
    gain = check(background_gain)
    if h > 1 or u > 1:
        raise ValueError("fixture food/utilization outside domain")
    bg = relation(background_signatures, cue_profile)
    hk = relation(hook_signatures, hook_profile)
    acceptance = {"POSITIVE": 1.0, "NEUTRAL": 0.8, "AVOID": 0.3}[hk]
    context = {"POSITIVE": 1 + gain, "NEUTRAL": 1.0, "AVOID": 0.7}[bg]
    free = 0.0
    for obj in free_objects:
        mass, size = check(obj["mass"]), check(obj["size"])
        value = check(preference[obj["target"]])
        if value > 1:
            raise ValueError("preference outside domain")
        if not obj.get("rejected", False) and obj["layer"] == layer and size <= max_size:
            free += mass * value
    return {"hook_label": hk, "background_label": bg, "processable_free_value": free,
            "trial_response": h * u * acceptance * context / (1 + free)}


def report():
    prefs = {"grain": 1, "animal": 0.2}
    cue = {"garlic": "POSITIVE", "curd": "NEUTRAL", "other": "AVOID"}
    hook = {"garlic": "AVOID", "curd": "POSITIVE"}
    cases = {}
    for name, hs, bs, mass, size, layer in (
        ("no_background", ["curd"], [], 0, 1, "bottom"),
        ("cue_only", ["curd"], ["garlic"], 0, 1, "bottom"),
        ("cue_and_free", ["curd"], ["garlic"], 1, 1, "bottom"),
        ("free_only", ["curd"], [], 1, 1, "bottom"),
        ("hook_avoid_background_positive", ["garlic"], ["garlic"], 0, 1, "bottom"),
        ("unusable_free", ["curd"], [], 1, 4, "bottom"),
        ("wrong_layer_free", ["curd"], [], 1, 1, "suspended")):
        cases[name] = response(0.6, 0.8, hs, bs,
            [{"mass": mass, "size": size, "layer": layer, "target": "grain"}], prefs, cue, hook)
    timelines = []
    for state in ("open", "bound"):
        # Binder replaces food in the same one-unit batch.
        edible = 0.8 if state == "open" else 0.6
        for t in (1, 5, 20, 60):
            p = physical(edible, state, t)
            timelines.append({"state": state, "time": t, "edible_input": edible, **p,
                              "bottom_free_penalty": 1 / (1 + p["bottom"])})
    return {"status": "UNADMITTED_GAMEPLAY_HYPOTHESES_NOT_BIOLOGY", "cases": cases,
            "physical_treatments": timelines}


class Tests(unittest.TestCase):
    def test_separate_causes(self):
        c = report()["cases"]
        self.assertGreater(c["cue_only"]["trial_response"], c["no_background"]["trial_response"])
        self.assertLess(c["free_only"]["trial_response"], c["no_background"]["trial_response"])
        self.assertLess(c["hook_avoid_background_positive"]["trial_response"], c["cue_only"]["trial_response"])
        self.assertEqual(c["unusable_free"]["trial_response"], c["no_background"]["trial_response"])
        self.assertEqual(c["wrong_layer_free"]["trial_response"], c["no_background"]["trial_response"])

    def test_ablation_and_duplicate_signature(self):
        args = (0.6, 0.8, ["curd"], ["garlic"], [], {}, {"garlic": "POSITIVE"}, {})
        a = response(*args)
        b = response(0.6, 0.8, ["curd"], ["garlic", "garlic"], [], {}, {"garlic": "POSITIVE"}, {})
        self.assertEqual(a, b)
        self.assertAlmostEqual(response(*args, background_gain=0)["trial_response"], 0.6 * 0.8 * 0.8)
        self.assertEqual(response(0, *args[1:])["trial_response"], 0)

    def test_physical_conservation(self):
        for row in report()["physical_treatments"]:
            self.assertAlmostEqual(sum(row[k] for k in ("bottom", "suspended", "stored", "lost")), row["edible_input"])
            self.assertTrue(all(row[k] >= 0 for k in ("bottom", "suspended", "stored", "lost")))
        self.assertEqual(physical(0.8, "open", 0)["bottom"], 0)

    def test_rejected_free_object_does_not_compete(self):
        obj = {"mass": 1, "size": 1, "layer": "bottom", "target": "grain", "rejected": True}
        args = (0.6, 0.8, [], [])
        no_free = response(*args, [], {"grain": 1}, {}, {})
        rejected = response(*args, [obj], {"grain": 1}, {}, {})
        accepted = response(*args, [{**obj, "rejected": False}], {"grain": 1}, {}, {})
        self.assertEqual(no_free, rejected)
        self.assertLess(accepted["trial_response"], rejected["trial_response"])

    def test_split_free_invariant(self):
        obj = {"mass": 1, "size": 1, "layer": "bottom", "target": "grain"}
        a = response(0.6, 1, [], [], [obj], {"grain": 1}, {}, {})
        b = response(0.6, 1, [], [], [{**obj, "mass": 0.5}] * 2, {"grain": 1}, {}, {})
        self.assertEqual(a, b)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    text = json.dumps(report(), ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.write_text(text)
    else:
        print(text)

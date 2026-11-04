#!/usr/bin/env python3
"""Finite-session strategy experiment. Metrics are not catches or probabilities."""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("float_strategy", ROOT / "tools/probe_float_strategy.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
FIXTURE = ROOT / "docs/groundbait-recipe/fixtures/float-strategy-v1.json"


def session(fixture, recipe_name, hook_name, schedule, duration, step=0.25, operator="global", release=0.2):
    base.nonnegative(duration)
    base.nonnegative(step)
    if not duration or not step or step > duration:
        raise ValueError("invalid integration interval")
    events = []
    for index, (time, mass) in enumerate(schedule):
        base.nonnegative(time)
        base.nonnegative(mass)
        if time >= duration:
            raise ValueError("deposit outside fishing interval")
        events.append(base.deposit(str(index), time, mass, release=release))
    state = base.Field("room1:cell1:bottom", fixture["rates"])
    mix = base.recipe(fixture["recipes"][recipe_name], fixture["ingredients"])
    times = {0.0, duration, *(e["time"] for e in events)}
    i = 1
    while i * step < duration:
        times.add(i * step)
        i += 1
    pending = sorted(events, key=lambda event: (event["time"], event["id"]))
    hooks = {name: base.hook_value(profile, fixture["hooks"][hook_name], operator)
             for name, profile in fixture["fish"].items()}
    values = {name: base.food(mix["targets"], profile["preference"], operator)
              for name, profile in fixture["fish"].items()}
    integrals = dict.fromkeys(hooks, 0.0)
    previous = None
    for time in sorted(times):
        while pending and pending[0]["time"] <= time:
            state.apply(pending.pop(0))
        state.advance(time)
        available = sum(lot["available"] for lot in state.lots.values())
        current = {name: base.trial_response(hook, available * values[name], 0)
                   for name, hook in hooks.items()}
        if previous is not None:
            old_time, old_values = previous
            for name in hooks:
                integrals[name] += (time - old_time) * (old_values[name] + current[name]) / 2
        previous = time, current
    return {"recipe": recipe_name, "hook": hook_name, "schedule": schedule,
            "duration": duration, "release": release, "operator": operator,
            "deposited_mass": sum(mass for _, mass in schedule),
            "response_integrals": integrals}


def pareto(rows, target, nuisance):
    result = []
    for index, row in enumerate(rows):
        a = (row["response_integrals"][target], -row["response_integrals"][nuisance], -row["deposited_mass"])
        dominated = False
        for other_index, other in enumerate(rows):
            if index == other_index:
                continue
            b = (other["response_integrals"][target], -other["response_integrals"][nuisance], -other["deposited_mass"])
            if all(y >= x for x, y in zip(a, b)) and any(y > x for x, y in zip(a, b)):
                dominated = True
                break
        if not dominated:
            result.append(index)
    return result


def report(fixture, step=0.25):
    schedules = {"none": [], "small_once": [[0, 2]], "large_once": [[0, 12]],
                 "split_same_budget": [[0, 4], [20, 4], [40, 4]],
                 "late": [[30, 2]]}
    rows = []
    for duration in (20, 60, 120):
        for recipe_name in fixture["recipes"]:
            for hook_name in ("grain_small", "animal_small", "oversize"):
                for name, schedule in schedules.items():
                    if any(t >= duration for t, _ in schedule):
                        continue
                    for release in (0.04, 0.6):
                        row = session(fixture, recipe_name, hook_name, schedule, duration, step, release=release)
                        row["plan"] = name
                        rows.append(row)
    fronts = {}
    for duration in (20, 60, 120):
        indices = [i for i, r in enumerate(rows) if r["duration"] == duration]
        subset = [rows[i] for i in indices]
        fronts[str(duration)] = [indices[i] for i in pareto(subset, "generalist", "specialist")]
    return {"status": "WORKING_FIXTURE_NOT_CATCH_FORECAST", "fixture_version": fixture["version"],
            "step": step, "target": "generalist", "nuisance": "specialist", "rows": rows,
            "pareto_row_indices": fronts}


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = json.loads(FIXTURE.read_text())

    def test_no_feed_reference(self):
        r = session(self.f, "grain_focus", "grain_small", [], 60)
        for name, p in self.f["fish"].items():
            self.assertAlmostEqual(r["response_integrals"][name], 60 * base.hook_value(p, self.f["hooks"]["grain_small"], "global"))

    def test_nuisance_filter_not_background_rescue(self):
        r = session(self.f, "mixed", "oversize", [[0, 12]], 60)
        self.assertEqual(r["response_integrals"]["specialist"], 0)
        self.assertGreater(r["response_integrals"]["generalist"], 0)
        r = session(self.f, "mixed", "rejected", [[0, 12]], 60)
        self.assertEqual(set(r["response_integrals"].values()), {0})

    def test_equal_budget_and_timing(self):
        a = session(self.f, "mixed", "grain_small", [[0, 12]], 60)
        b = session(self.f, "mixed", "grain_small", [[0, 4], [20, 4], [40, 4]], 60)
        self.assertEqual(a["deposited_mass"], b["deposited_mass"])
        self.assertNotEqual(a["response_integrals"], b["response_integrals"])

    def test_integration_convergence(self):
        for plan in ([[0, 12]], [[0, 4], [20, 4], [40, 4]]):
            a = session(self.f, "mixed", "grain_small", plan, 60, 0.25)
            b = session(self.f, "mixed", "grain_small", plan, 60, 0.125)
            for name in a["response_integrals"]:
                self.assertLess(abs(a["response_integrals"][name] - b["response_integrals"][name]), 0.01)

    def test_partition_deposit_invariance(self):
        a = session(self.f, "mixed", "grain_small", [[0, 2]], 60)
        b = session(self.f, "mixed", "grain_small", [[0, 1], [0, 1]], 60)
        for name in a["response_integrals"]:
            self.assertAlmostEqual(a["response_integrals"][name], b["response_integrals"][name])

    def test_cost_negative_control_and_pareto(self):
        rows = []
        for target, nuisance, cost in ((10, 3, 2), (9, 4, 3), (10, 3, 0), (12, 4, 2)):
            rows.append({"response_integrals": {"t": target, "n": nuisance}, "deposited_mass": cost})
        self.assertEqual(pareto(rows, "t", "n"), [2, 3])
        for duration in (0, -1):
            with self.assertRaises(ValueError):
                session(self.f, "mixed", "grain_small", [], duration)
        with self.assertRaises(ValueError):
            session(self.f, "mixed", "grain_small", [[60, 2]], 60)

    def test_inputs_unchanged(self):
        old = deepcopy(self.f)
        session(self.f, "mixed", "grain_small", [[0, 2]], 20)
        self.assertEqual(old, self.f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    data = report(json.loads(FIXTURE.read_text()))
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"
    if args.report:
        args.report.write_text(text)
    else:
        print(text)

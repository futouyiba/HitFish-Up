#!/usr/bin/env python3
"""Unified working experiment; response integrals are not catch forecasts."""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


base = module("probe_float_strategy")
v2 = module("probe_float_mechanisms_v2")
cue = module("probe_float_cue_windows")
FIXTURE = ROOT / "docs/groundbait-recipe/fixtures/float-integrated-v3.json"


class Experiment:
    def __init__(self, config, scope="room:A", lifetime="fixed"):
        if lifetime not in ("fixed", "serial_units"):
            raise ValueError("unknown lifetime hypothesis")
        self.config = deepcopy(config)
        self.scope = scope
        self.lifetime = lifetime
        self.field = base.Field(scope, {"recovery": 0, "pressure_per_mass": 0})
        self.events = {}
        self.sources = []
        self.objects = {}
        self.cost = {"solid": 0.0, "cue_dose": 0.0, "operations": 0}

    def apply(self, event):
        staged = deepcopy(self)
        changed = staged._apply(event)
        if changed:
            self.__dict__.update(staged.__dict__)
        return changed

    def _apply(self, event):
        if event["scope"] != self.scope:
            raise ValueError("scope mismatch")
        if event["id"] in self.events:
            if self.events[event["id"]] != event:
                raise ValueError("conflicting repeated event")
            return False
        base.nonnegative(event["at"])
        units = event["units"]
        if isinstance(units, bool) or not isinstance(units, int) or not 1 <= units <= 8:
            raise ValueError("standard applications require 1..8 integer units")
        if event["at"] < self.field.time:
            raise ValueError("late event needs checkpoint replay")
        if event["layer"] not in ("bottom", "suspended"):
            raise ValueError("unknown layer")
        if not isinstance(event["actor"], str):
            raise ValueError("invalid actor")
        treatment = self.config["treatments"][event["treatment"]]
        recipe = self.config["recipes"][event["recipe"]]
        signatures = recipe["signatures"]
        edible = units * (1 - treatment["binder_mass"]) if recipe["food"] else 0
        self.field.advance(event["at"])
        for target, fraction in recipe["food"].items():
            key = event["id"] + ":" + target
            mass = edible * fraction
            self.field.apply(dict(id=key, scope=self.scope, time=event["at"], type="deposit",
                                  mass=mass, release=treatment["release"], loss=treatment["loss"],
                                  value=1, actor=event["actor"]))
            self.objects[key] = {"target": target, "size": 1, "layer": event["layer"],
                                 "place": event["place"], "bottom_share": treatment["bottom_share"]}
        if signatures:
            duration = treatment["cue_duration"] * (units if self.lifetime == "serial_units" else 1)
            self.sources.append(dict(id=event["id"], at=event["at"], delay=treatment["cue_delay"],
                                     duration=duration, place=event["place"] + ":" + event["layer"],
                                     signatures=signatures, cost=units * recipe["cue_dose"], actor=event["actor"]))
        self.cost["solid"] += units if recipe["food"] else 0
        self.cost["cue_dose"] += units * recipe["cue_dose"]
        self.cost["operations"] += 1
        self.events[event["id"]] = deepcopy(event)
        return True

    def evaluate(self, time, hook_name, operator="global", place="A", gain=0.5):
        self.field.advance(time)
        hook = self.config["hooks"][hook_name]
        signatures = cue.active(self.sources, time, place + ":" + hook["layer"])
        result = {}
        for name, fish in self.config["fish"].items():
            objects = []
            for key, lot in self.field.lots.items():
                obj = self.objects[key]
                if obj["place"] != place:
                    continue
                share = obj["bottom_share"] if obj["layer"] == "bottom" else 1 - obj["bottom_share"]
                objects.append({"target": obj["target"], "size": obj["size"],
                                "layer": obj["layer"], "mass": lot["available"] * share})
            h = base.food(hook["food"], fish["preference"], operator)
            u = 0 if hook["rejected"] or hook["size"] > fish["max_size"] else 0.8
            # Each target's mass is valued once by response(), not pre-saturated by lot.
            row = v2.response(h, u, hook["signatures"], signatures, objects,
                              fish["preference"], fish["background"], fish["hook"],
                              layer=hook["layer"], max_size=fish["max_size"], background_gain=gain)
            result[name] = row["trial_response"]
        return result

    def save(self):
        return deepcopy(dict(version=self.config["version"], config=self.config, scope=self.scope,
                             lifetime=self.lifetime, field=self.field.save(), events=self.events,
                             sources=self.sources, objects=self.objects, cost=self.cost))

    @classmethod
    def load(cls, snapshot, version):
        if snapshot["version"] != version:
            raise ValueError("mechanism version mismatch")
        result = cls(snapshot["config"], snapshot["scope"], snapshot["lifetime"])
        result.field = base.Field.load(snapshot["field"])
        for key in ("events", "sources", "objects", "cost"):
            setattr(result, key, deepcopy(snapshot[key]))
        return result


def event(key, at=0, recipe="grain", units=1, treatment="open", layer="bottom", place="A"):
    return dict(id=key, at=at, scope="room:A", actor="player", recipe=recipe,
                units=units, treatment=treatment, layer=layer, place=place)


def session(config, events, horizon=30, hook="small_grain", lifetime="fixed", operator="global", step=0.25, gain=0.5):
    base.nonnegative(horizon)
    base.nonnegative(step)
    if not horizon or not step:
        raise ValueError("positive duration/step required")
    state = Experiment(config, lifetime=lifetime)
    ordered = sorted(events, key=lambda e: (e["at"], e["id"]))
    # Validate atomically on a disposable instance before numerical integration.
    validation = Experiment(config, lifetime=lifetime)
    for e in ordered:
        if e["at"] >= horizon:
            raise ValueError("event outside session")
        validation.apply(e)
    boundaries = {0.0, horizon}
    boundaries.update(e["at"] for e in ordered)
    for src in validation.sources:
        start = src["at"] + src["delay"]
        boundaries.update(t for t in (start, start + src["duration"]) if 0 < t < horizon)
    totals = dict.fromkeys(config["fish"], 0.0)
    boundaries = sorted(boundaries)
    index = 0
    for lo, hi in zip(boundaries, boundaries[1:]):
        while index < len(ordered) and ordered[index]["at"] <= lo:
            state.apply(ordered[index])
            index += 1
        # Midpoint quadrature never samples the wrong side of a categorical jump.
        count = max(1, int((hi - lo) / step) + 1)
        dt = (hi - lo) / count
        for n in range(count):
            values = state.evaluate(lo + (n + 0.5) * dt, hook, operator, gain=gain)
            for name, value in values.items():
                totals[name] += value * dt
        state.field.advance(hi)
    return dict(horizon=horizon, hook=hook, lifetime=lifetime, operator=operator,
                cost=state.cost, integrals=totals)


def report(config):
    rows = []
    for horizon in (10, 30, 60):
        for lifetime in ("fixed", "serial_units"):
            for treatment in ("open", "bound"):
                for recipe in config["recipes"]:
                    for units in (1, 3):
                        for hook in ("small_grain", "large_grain", "animal"):
                            for operator in ("max", "noisy_or", "global"):
                                e = event("a", recipe=recipe, units=units, treatment=treatment)
                                row = session(config, [e], horizon, hook, lifetime, operator)
                                rows.append(dict(recipe=recipe, units=units, treatment=treatment, **row))
    controls = {}
    for name, events in {"none": [], "one": [event("a")],
                         "three_once": [event("a", units=3)],
                         "split_three": [event("a"), event("b", 10), event("c", 20)],
                         "wrong_place": [event("a", place="B")],
                         "wrong_layer": [event("a", layer="suspended")]}.items():
        controls[name] = session(config, events)
    dominance = []
    for lifetime in ("fixed", "serial_units"):
        for treatment in ("open", "bound"):
            for operator in ("max", "noisy_or", "global"):
                subset = [r for r in rows if r["lifetime"] == lifetime and r["treatment"] == treatment and r["operator"] == operator]
                comparisons = 0
                failures = 0
                for full in subset:
                    if full["recipe"] != "grain":
                        continue
                    pure = next(r for r in subset if r["recipe"] == "cue_only" and all(r[k] == full[k] for k in ("horizon", "hook", "units")))
                    comparisons += 1
                    if pure["integrals"]["target"] + 1e-10 < full["integrals"]["target"]:
                        failures += 1
                dominance.append(dict(lifetime=lifetime, treatment=treatment, operator=operator,
                                      comparisons=comparisons, target_pure_cue_counterexamples=failures))
    return dict(status="WORKING_NOT_PRODUCTION_OR_SPECIES_FACT", fixture_version=config["version"],
                rows=rows, controls=controls, dominance=dominance,
                interpretation="serial_units is an unadmitted quantity-to-lifetime hypothesis, not intensity")


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = json.loads(FIXTURE.read_text())

    def test_duplicate_and_conflict_atomic(self):
        s = Experiment(self.c)
        e = event("a")
        s.apply(e)
        before = s.save()
        self.assertFalse(s.apply(e))
        with self.assertRaises(ValueError):
            s.apply({**e, "units": 3})
        self.assertEqual(s.save(), before)
        with self.assertRaises(ValueError):
            s.apply(event("bad", at=5, units=0))
        self.assertEqual(s.save(), before)
        missing = event("bad", at=5)
        del missing["place"]
        for bad in (missing, event("bad", at=5, place=7)):
            with self.assertRaises((KeyError, TypeError, ValueError)):
                s.apply(bad)
            self.assertEqual(s.save(), before)
        self.assertTrue(s.apply(event("valid", at=2)))

    def test_restore_shared_state_and_version(self):
        a = Experiment(self.c)
        a.apply(event("a"))
        a.evaluate(5, "small_grain")
        snap = a.save()
        b = Experiment.load(json.loads(json.dumps(snap)), self.c["version"])
        self.assertEqual(a.evaluate(20, "small_grain"), b.evaluate(20, "small_grain"))
        self.assertEqual(a.save(), b.save())
        self.assertFalse(b.apply(event("a")))
        with self.assertRaises(ValueError):
            Experiment.load(snap, "wrong")

    def test_pure_cue_dominance_and_fixed_amount(self):
        for units in (1, 3):
            pure = session(self.c, [event("a", recipe="cue_only", units=units)])
            full = session(self.c, [event("a", units=units)])
            self.assertGreater(pure["integrals"]["target"], full["integrals"]["target"])
        a = session(self.c, [event("a")])
        b = session(self.c, [event("a", units=3)])
        self.assertGreater(a["integrals"]["target"], b["integrals"]["target"])
        self.assertLess(a["cost"]["solid"], b["cost"]["solid"])

    def test_lifetime_ablation(self):
        a = session(self.c, [event("a", recipe="cue_only")])
        b = session(self.c, [event("a", recipe="cue_only", units=3)])
        extended = session(self.c, [event("a", recipe="cue_only", units=3)], lifetime="serial_units")
        self.assertEqual(a["integrals"], b["integrals"])
        self.assertGreater(extended["integrals"]["target"], b["integrals"]["target"])
        zero = session(self.c, [event("a", recipe="cue_only")], gain=0)
        none = session(self.c, [], gain=0)
        for name in zero["integrals"]:
            self.assertAlmostEqual(zero["integrals"][name], none["integrals"][name], places=12)

    def test_jump_integration_and_convergence(self):
        pure = session(self.c, [event("a", recipe="cue_only")], horizon=30, step=5)
        h = base.food({"grain": 1}, self.c["fish"]["target"]["preference"], "global") * 0.8
        self.assertAlmostEqual(pure["integrals"]["target"], h * (30 + 0.5 * 10))
        for treatment in ("open", "bound"):
            a = session(self.c, [event("a", treatment=treatment)], step=0.125)
            b = session(self.c, [event("a", treatment=treatment)], step=0.0625)
            self.assertLess(abs(a["integrals"]["target"] - b["integrals"]["target"]), 0.001)

    def test_hook_and_place_isolation(self):
        self.assertEqual(session(self.c, [event("a")], hook="reject")["integrals"], {"target": 0, "nuisance": 0})
        for e in (event("a", place="B"), event("a", layer="suspended")):
            actual, expected = session(self.c, [e])["integrals"], session(self.c, [])["integrals"]
            for name in actual:
                self.assertAlmostEqual(actual[name], expected[name], places=12)
        self.assertEqual(session(self.c, [event("a")], hook="large_grain")["integrals"]["nuisance"], 0)

    def test_mass_conservation_and_cost(self):
        s = Experiment(self.c)
        s.apply(event("a", units=3))
        s.field.advance(30)
        row = s.field.row(0)
        self.assertAlmostEqual(row["stored"] + row["available"] + row["lost"] + row["consumed"], row["deposited"])
        self.assertEqual(s.cost, {"solid": 3, "cue_dose": 3, "operations": 1})
        self.assertEqual(s.field.pressure, 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    payload = report(json.loads(FIXTURE.read_text()))
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    if args.report:
        args.report.write_text(text)
    else:
        print(text)

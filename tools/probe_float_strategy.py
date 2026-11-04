#!/usr/bin/env python3
"""Float design experiment, not a production Response implementation."""
import argparse
from copy import deepcopy
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "docs/groundbait-recipe/fixtures/float-strategy-v1.json"


def nonnegative(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
        raise ValueError("expected finite nonnegative number")
    return value


def food(targets, preferences, operator):
    if set(targets) - set(preferences):
        raise ValueError("missing target preference")
    values = [nonnegative(preferences[t]) * nonnegative(x) / (1 + x) for t, x in sorted(targets.items())]
    if any(p > 1 for p in preferences.values()):
        raise ValueError("preference outside fixture domain")
    if operator == "max":
        return max(values, default=0)
    if operator == "noisy_or":
        return 1 - math.prod(1 - r for r in values)
    if operator == "global":
        total = sum(values)
        return total / (1 + total)
    raise ValueError("unknown experimental operator")


def recipe(slots, ingredients):
    totals, signatures = {}, set()
    total_mass = 0.0
    edible_mass = 0.0
    for ingredient_id, amount in slots:
        item = ingredients[ingredient_id]
        amount = nonnegative(amount)
        if item.get("unit", "solid_mass") == "cue_dose":
            if item["targets"] or item["edible_fraction"]:
                raise ValueError("cue dose cannot add food mass")
            if amount > 0:
                signatures.update(item["signatures"])
            continue
        total_mass += amount
        edible = nonnegative(item["edible_fraction"])
        if edible > 1:
            raise ValueError("edible fraction outside domain")
        edible_mass += amount * edible
        for target, share in item["targets"].items():
            totals[target] = totals.get(target, 0) + amount * edible * nonnegative(share)
        if amount > 0:
            signatures.update(item["signatures"])
    if total_mass == 0:
        raise ValueError("empty recipe")
    return {"targets": {k: v / total_mass for k, v in totals.items()},
            "signatures": sorted(signatures), "edible_fraction": edible_mass / total_mass}


def flavor(signatures, relations):
    values = {relations.get(s, "NEUTRAL") for s in set(signatures)}
    if values - {"AVOID", "POSITIVE", "NEUTRAL"}:
        raise ValueError("unknown relation")
    return "AVOID" if "AVOID" in values else "POSITIVE" if "POSITIVE" in values else "NEUTRAL"


def utilization(actions, size, layer):
    nonnegative(size)
    unique = {}
    for action in actions:
        key = action["id"]
        if key in unique and action != unique[key]:
            raise ValueError("conflicting duplicate action")
        unique[key] = action
    feasible = [a for a in unique.values() if a["layer"] == layer and a["min"] <= size <= a["max"]]
    weights = [nonnegative(a["weight"]) for a in feasible]
    for a in feasible:
        if not 0 <= nonnegative(a["success"]) <= 1:
            raise ValueError("invalid success")
    denom = sum(weights)
    return sum(w * a["success"] for w, a in zip(weights, feasible)) / denom if denom else 0.0


def hook_value(profile, hook, operator):
    if not hook["legal"] or hook["rejected"]:
        return 0.0
    return food(hook["targets"], profile["preference"], operator) * utilization(profile["actions"], hook["size"], hook["layer"])


def trial_response(hook, valued_mass, pressure, beta=6.0, gamma=0.5):
    nonnegative(hook)
    nonnegative(valued_mass)
    nonnegative(pressure)
    nonnegative(beta)
    nonnegative(gamma)
    return hook * (1 + beta * valued_mass / (1 + valued_mass)) / (1 + gamma * valued_mass) * math.exp(-pressure)


class Field:
    def __init__(self, scope, rates):
        self.scope = scope
        self.rates = rates
        self.time = 0.0
        self.lots = {}
        self.seen = set()
        self.pressure = 0.0
        self.consumed = 0.0
        self.lost = 0.0
        self.deposited = 0.0

    def advance(self, now):
        dt = nonnegative(now - self.time)
        self.pressure *= math.exp(-self.rates["recovery"] * dt)
        for lot in self.lots.values():
            d, a, r, loss = lot["stored"], lot["available"], lot["release"], lot["loss"]
            er, el = math.exp(-r * dt), math.exp(-loss * dt)
            if r == loss:
                release_to_a = r * d * dt * el
            else:
                delta = abs(loss - r)
                release_to_a = r * d * math.exp(-min(r, loss) * dt) * (-math.expm1(-delta * dt)) / delta
            nd, na = d * er, a * el + release_to_a
            self.lost += d + a - nd - na
            lot["stored"], lot["available"] = nd, na
        self.time = now

    def apply(self, event):
        if event["scope"] != self.scope:
            raise ValueError("scope mismatch")
        if event["id"] in self.seen:
            return False
        if event["time"] < self.time:
            raise ValueError("late event needs replay, not clamping")
        kind = event["type"]
        nonnegative(event["time"])
        if kind == "deposit":
            for key in ("mass", "release", "loss", "value"):
                nonnegative(event[key])
            if not isinstance(event["actor"], str):
                raise ValueError("invalid actor")
        elif kind == "ingest":
            nonnegative(event["mass"])
        else:
            raise ValueError("unknown event type")
        self.advance(event["time"])
        if kind == "deposit":
            mass = nonnegative(event["mass"])
            release = nonnegative(event["release"])
            loss = nonnegative(event["loss"])
            value = nonnegative(event["value"])
            self.lots[event["id"]] = {"stored": mass, "available": 0.0, "release": release,
                                       "loss": loss, "value": value, "actor": event["actor"]}
            self.deposited += mass
        elif event["type"] == "ingest":
            available = sum(l["available"] for l in self.lots.values())
            eaten = min(available, nonnegative(event["mass"]))
            for lot in self.lots.values():
                if available:
                    lot["available"] *= 1 - eaten / available
            self.consumed += eaten
            self.pressure += self.rates["pressure_per_mass"] * eaten
        else:
            raise ValueError("unknown event type")
        self.seen.add(event["id"])
        return True

    def row(self, hook):
        available = sum(l["available"] for l in self.lots.values())
        valued = sum(l["available"] * l["value"] for l in self.lots.values())
        stored = sum(l["stored"] for l in self.lots.values())
        return {"time": self.time, "stored": stored, "available": available,
                "lost": self.lost, "consumed": self.consumed, "pressure": self.pressure,
                "deposited": self.deposited, "trial_response": trial_response(hook, valued, self.pressure)}

    def save(self):
        return deepcopy({"scope": self.scope, "rates": self.rates, "time": self.time,
                "lots": self.lots, "seen": sorted(self.seen), "pressure": self.pressure,
                "consumed": self.consumed, "lost": self.lost, "deposited": self.deposited})

    @classmethod
    def load(cls, snapshot):
        state = cls(snapshot["scope"], snapshot["rates"])
        for key in ("time", "lots", "pressure", "consumed", "lost", "deposited"):
            setattr(state, key, deepcopy(snapshot[key]))
        state.seen = set(snapshot["seen"])
        return state


def deposit(event_id, time, mass, release=0.2, actor="A", scope="room1:cell1:bottom", value=1.0):
    return dict(id=event_id, time=time, mass=mass, release=release, loss=0.03,
                type="deposit", scope=scope, actor=actor, value=value)


def run_time(events, times, rates, hook=0.4):
    state = Field("room1:cell1:bottom", rates)
    pending = sorted(events, key=lambda e: (e["time"], e["id"]))
    rows = []
    for now in times:
        while pending and pending[0]["time"] <= now:
            state.apply(pending.pop(0))
        state.advance(now)
        rows.append(state.row(hook))
    return rows


def report(fixture):
    operators = ["max", "noisy_or", "global"]
    mixes = {name: recipe(slots, fixture["ingredients"]) for name, slots in fixture["recipes"].items()}
    food_rows = [{"fish_profile": name, "recipe": recipe_name,
                  **{op: food(mix["targets"], profile["preference"], op) for op in operators}}
                 for name, profile in fixture["fish"].items() for recipe_name, mix in mixes.items()]
    hook_rows = []
    for name, profile in fixture["fish"].items():
        for hook_name, hook in fixture["hooks"].items():
            h = hook_value(profile, hook, "global")
            hook_rows.append({"fish_profile": name, "hook": hook_name, "hook_value": h,
                              "no_background": trial_response(h, 0, 0),
                              "moderate": trial_response(h, 1, 0), "excess": trial_response(h, 20, 0)})
    times = fixture["sample_times"]
    scenarios = {
        "none": [], "moderate": [deposit("d1", 0, 2)],
        "repeated": [deposit(f"d{i}", i * 5, 2) for i in range(7)],
        "excess": [deposit("d1", 0, 30)],
        "fast": [deposit("d1", 0, 2, release=0.6)],
        "slow": [deposit("d1", 0, 2, release=0.04)],
        "confirmed_ingestion": [deposit("d1", 0, 2),
            {"id": "eat1", "time": 10, "mass": 0.5, "scope": "room1:cell1:bottom", "type": "ingest"}],
        "second_player": [deposit("d1", 0, 2), deposit("d2", 10, 2, actor="B")],
    }
    combinations = []
    for fish_name, profile in fixture["fish"].items():
        for recipe_name, mix in mixes.items():
            background = food(mix["targets"], profile["preference"], "global")
            for hook_name in ("grain_small", "animal_small", "oversize"):
                h = hook_value(profile, fixture["hooks"][hook_name], "global")
                combinations.append({"fish_profile": fish_name, "recipe": recipe_name,
                                     "hook": hook_name, "valued_background": 2 * background,
                                     "trial_response": trial_response(h, 2 * background, 0)})
    hypothetical_flavor = []
    for label, relations in (("assume_garlic_positive", {"garlic": "POSITIVE", "curd": "NEUTRAL"}),
                             ("assume_curd_positive", {"garlic": "NEUTRAL", "curd": "POSITIVE"})):
        for background in ([], ["garlic"], ["curd"]):
            for hook_signature in ("garlic", "curd"):
                hypothetical_flavor.append({"hypothesis_not_species_fact": label,
                    "background": background, "hook": hook_signature,
                    "background_label": flavor(background, relations),
                    "hook_label": flavor([hook_signature], relations),
                    "union_label": flavor(background + [hook_signature], relations)})
    return {"status": "WORKING_FIXTURE_NOT_PRODUCTION", "fixture_version": fixture["version"],
            "food": food_rows, "hooks": hook_rows, "combinations": combinations,
            "hypothetical_garlic_curd": hypothetical_flavor,
            "time": {n: run_time(e, times, fixture["rates"]) for n, e in scenarios.items()}}


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = json.loads(FIXTURE.read_text())

    def test_split_recipe(self):
        a = recipe([["grain", 1]], self.f["ingredients"])
        b = recipe([["grain", 0.5], ["grain", 0.5]], self.f["ingredients"])
        self.assertEqual(a, b)
        for op in ("max", "noisy_or", "global"):
            self.assertEqual(food(a["targets"], self.f["fish"]["specialist"]["preference"], op),
                             food(b["targets"], self.f["fish"]["specialist"]["preference"], op))

    def test_budget_tradeoff(self):
        rows = report(self.f)["food"]
        for op in ("max", "noisy_or", "global"):
            lookup = {(r["fish_profile"], r["recipe"]): r[op] for r in rows}
            self.assertGreater(lookup["specialist", "grain_focus"], lookup["specialist", "mixed"])
        lookup = {(r["fish_profile"], r["recipe"]): r for r in rows}
        self.assertGreater(lookup["generalist", "mixed"]["global"], lookup["generalist", "grain_focus"]["global"])
        self.assertLess(lookup["generalist", "mixed"]["max"], lookup["generalist", "grain_focus"]["max"])

    def test_target_taxonomy_attack(self):
        original = food({"x": 1}, {"x": 1}, "global")
        cloned = food({"x": 0.5, "y": 0.5}, {"x": 1, "y": 1}, "global")
        self.assertGreater(cloned, original)

    def test_trace_flavor_without_intensity(self):
        self.assertEqual(flavor(["grain", "grain"], {"grain": "POSITIVE"}), "POSITIVE")
        self.assertEqual(flavor(["unknown"], {}), "NEUTRAL")
        self.assertEqual(flavor(["grain", "garlic"], {"grain": "POSITIVE", "garlic": "AVOID"}), "AVOID")
        a = recipe([["grain", 1], ["cue_garlic", 0.001]], self.f["ingredients"])
        self.assertIn("garlic", a["signatures"])
        self.assertEqual(self.f["ingredients"]["cue_garlic"]["edible_fraction"], 0)

    def test_actions_and_size(self):
        profile = self.f["fish"]["specialist"]
        actions = profile["actions"]
        self.assertEqual(utilization(actions, 4, "bottom"), utilization(actions + actions, 4, "bottom"))
        self.assertEqual(utilization(actions, 4, "surface"), 0)
        self.assertEqual(utilization(actions, 4, "bottom"), 0)
        self.assertGreater(utilization(self.f["fish"]["generalist"]["actions"], 4, "bottom"), 0)

    def test_weak_hook_not_rescued(self):
        p = self.f["fish"]["specialist"]
        for key in ("oversize", "rejected", "empty"):
            h = hook_value(p, self.f["hooks"][key], "global")
            self.assertEqual(trial_response(h, 100, 0), 0)

    def test_hump_and_no_fake_satiety(self):
        self.assertGreater(trial_response(0.4, 1, 0), trial_response(0.4, 0, 0))
        self.assertGreater(trial_response(0.4, 1, 0), trial_response(0.4, 20, 0))
        s = Field("room1:cell1:bottom", self.f["rates"])
        s.apply(deposit("a", 0, 100))
        s.advance(60)
        self.assertEqual(s.pressure, 0)

    def test_conservation_and_time_semigroup(self):
        for release in (0.03, 0.2, 0.6):
            a = Field("room1:cell1:bottom", self.f["rates"])
            a.apply(deposit("a", 0, 2, release=release))
            b = Field.load(json.loads(json.dumps(a.save())))
            a.advance(60)
            for i in range(1, 61):
                b.advance(i)
            for key in ("stored", "available", "lost", "consumed"):
                self.assertAlmostEqual(a.row(0.4)[key], b.row(0.4)[key], places=11)
            row = a.row(0.4)
            self.assertAlmostEqual(row["stored"] + row["available"] + row["lost"] + row["consumed"], row["deposited"])

    def test_ingestion_recovery_and_relogin(self):
        a = Field("room1:cell1:bottom", self.f["rates"])
        a.apply(deposit("a", 0, 2))
        eat = {"id": "eat", "time": 10, "type": "ingest", "mass": 0.5, "scope": a.scope}
        a.apply(eat)
        pressure = a.pressure
        b = Field.load(json.loads(json.dumps(a.save())))
        self.assertFalse(b.apply(eat))
        a.advance(80)
        b.advance(80)
        self.assertEqual(a.save(), b.save())
        self.assertLess(b.pressure, pressure)
        row = b.row(0.4)
        self.assertAlmostEqual(sum(row[k] for k in ("stored", "available", "lost", "consumed")), row["deposited"])

    def test_shared_players_and_scope(self):
        a = Field("room1:cell1:bottom", self.f["rates"])
        first, second = deposit("a", 0, 2), deposit("b", 0, 2, actor="B")
        a.apply(first)
        a.apply(second)
        b = Field(a.scope, self.f["rates"])
        b.apply(second)
        b.apply(first)
        a.advance(10)
        b.advance(10)
        self.assertEqual(a.row(0.4), b.row(0.4))
        self.assertFalse(a.apply(second))
        with self.assertRaises(ValueError):
            a.apply(deposit("wrong", 11, 3, scope="room2:cell1:bottom"))
        with self.assertRaises(ValueError):
            a.advance(9)

    def test_bad_input(self):
        for value in (-1, math.inf, math.nan, True):
            with self.assertRaises(ValueError):
                trial_response(value, 1, 0)
        with self.assertRaises(ValueError):
            food({"missing": 1}, {}, "global")

    def test_time_rankings_and_negative_control(self):
        rows = report(self.f)["time"]
        at = lambda name, time: next(r for r in rows[name] if r["time"] == time)
        self.assertGreater(at("moderate", 10)["trial_response"], at("none", 10)["trial_response"])
        self.assertLess(at("excess", 10)["trial_response"], at("none", 10)["trial_response"])
        self.assertLess(at("repeated", 30)["trial_response"], at("moderate", 30)["trial_response"])
        self.assertGreater(at("fast", 5)["trial_response"], at("slow", 5)["trial_response"])
        self.assertLess(at("fast", 60)["trial_response"], at("slow", 60)["trial_response"])
        self.assertGreater(at("excess", 120)["trial_response"], at("excess", 10)["trial_response"])
        self.assertGreater(trial_response(0.4, 20, 0, gamma=0), trial_response(0.4, 1, 0, gamma=0))
        self.assertLessEqual(trial_response(0.4, 1, 0, beta=0), trial_response(0.4, 0, 0, beta=0))

    def test_slot_enumeration(self):
        optima = {}
        for name, profile in self.f["fish"].items():
            for op in ("max", "noisy_or", "global"):
                values = [food({"grain": n / 5, "animal": (4 - n) / 5}, profile["preference"], op) for n in range(5)]
                best = max(values)
                optima[name, op] = {n for n, value in enumerate(values) if abs(value - best) < 1e-12}
        for op in ("max", "noisy_or", "global"):
            self.assertEqual(optima["specialist", op], {4})
        self.assertEqual(optima["generalist", "max"], {0, 4})
        self.assertEqual(optima["generalist", "noisy_or"], {2})
        self.assertEqual(optima["generalist", "global"], {2})

    def test_food_monotonicity_and_bounds(self):
        for op in ("max", "noisy_or", "global"):
            last = -1
            for x in (0, 0.001, 0.1, 1, 10, 100):
                result = food({"grain": x, "animal": 0.2}, {"grain": 1, "animal": 0.5}, op)
                self.assertGreaterEqual(result, last)
                self.assertTrue(0 <= result <= 1)
                self.assertEqual(result, food({"animal": 0.2, "grain": x}, {"animal": 0.5, "grain": 1}, op))
                last = result
        with self.assertRaises(ValueError):
            food({"grain": 1}, {"grain": -1}, "global")

    def test_review_regressions(self):
        base = recipe([["grain", 1]], self.f["ingredients"])
        for dose in (0.001, 1, 20):
            mixed = recipe([["grain", 1], ["cue_garlic", dose]], self.f["ingredients"])
            self.assertEqual(mixed["targets"], base["targets"])
            self.assertEqual(mixed["edible_fraction"], base["edible_fraction"])
        r = math.nextafter(0.03, math.inf)
        a = Field("room1:cell1:bottom", self.f["rates"])
        a.apply(deposit("a", 0, 2, release=r))
        snapshot = a.save()
        b = Field.load(snapshot)
        a.advance(60)
        for t in range(1, 61):
            b.advance(t)
        expected = 2 * r * 60 * math.exp(-0.03 * 60)
        self.assertAlmostEqual(a.row(0.4)["available"], expected, places=12)
        self.assertAlmostEqual(a.row(0.4)["available"], b.row(0.4)["available"], places=12)
        self.assertEqual(snapshot["lots"]["a"]["stored"], 2)
        c = Field.load(snapshot)
        c.advance(60)
        self.assertEqual(a.row(0.4), c.row(0.4))
        for key in ("stored", "available", "lost", "consumed"):
            self.assertGreaterEqual(c.row(0.4)[key], -1e-12)
        state = Field("room1:cell1:bottom", self.f["rates"])
        state.apply(deposit("a", 0, 2))
        for bad in (deposit("bad", 10, -1),
                    {"id": "unknown", "time": 10, "type": "unknown", "scope": state.scope}):
            before = state.save()
            with self.assertRaises(ValueError):
                state.apply(bad)
            self.assertEqual(state.save(), before)
        state.apply(deposit("valid", 5, 1))
        self.assertEqual(state.time, 5)

    def test_structural_isolation(self):
        state = Field("room1:cell1:bottom", self.f["rates"])
        frozen = {"DEF": 0.8, "FishCondition": {"Activity": 1}, "L": 0.3}
        before = deepcopy(frozen)
        state.apply(deposit("a", 0, 30))
        state.advance(10)
        trial_response(0.4, state.row(0.4)["available"], 0)
        self.assertEqual(frozen, before)
        self.assertFalse(set(state.save()) & set(frozen))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    payload = report(json.loads(FIXTURE.read_text()))
    if args.report:
        args.report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

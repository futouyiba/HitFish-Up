#!/usr/bin/env python3
"""Categorical cue windows: experimental lifecycle, not chemical intensity."""
import argparse
import json
import math
from pathlib import Path
import unittest


def number(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0:
        raise ValueError("finite nonnegative number required")
    return x


def active(events, time, place):
    number(time)
    unique = {}
    for event in events:
        key = event["id"]
        if key in unique and unique[key] != event:
            raise ValueError("conflicting repeated source")
        for name in ("at", "delay", "duration", "cost"):
            number(event[name])
        if event["duration"] == 0 or event["cost"] == 0:
            raise ValueError("invalid standard application")
        unique[key] = event
    signatures = set()
    for event in unique.values():
        start = event["at"] + event["delay"]
        if event["place"] == place and start <= time < start + event["duration"]:
            signatures.update(event["signatures"])
    return sorted(signatures)


def source(key, at, delay=2, duration=10, place="bottom:A"):
    return {"id": key, "at": at, "delay": delay, "duration": duration,
            "place": place, "signatures": ["grain"], "cost": 1}


def evaluate(events, horizon=30, gain=0.5):
    number(horizon)
    number(gain)
    # The active set is constant between these boundaries, so integration is exact.
    boundaries = {0, horizon}
    for e in events:
        start = e["at"] + e["delay"]
        boundaries.update(t for t in (start, start + e["duration"]) if 0 < t < horizon)
    times = sorted(boundaries)
    rows = []
    integral = 0
    for lo, hi in zip(times, times[1:]):
        sigs = active(events, (lo + hi) / 2, "bottom:A")
        response = 0.4 * (1 + gain if "grain" in sigs else 1)
        integral += (hi - lo) * response
        rows.append({"from": lo, "until": hi, "signatures": sigs, "metric": response})
    unique = {e["id"]: e for e in events}
    return {"response_integral": integral, "application_cost": sum(e["cost"] for e in unique.values()), "intervals": rows}


def report():
    plans = {"none": [], "one": [source("a", 0)],
             "simultaneous_three": [source(str(i), 0) for i in range(3)],
             "overlap": [source("a", 0), source("b", 5)],
             "just_in_time": [source("a", 0), source("b", 10)],
             "wrong_place": [source("a", 0, place="surface:B")],
             "slow": [source("a", 0, delay=8, duration=18)]}
    return {"status": "UNADMITTED_CATEGORICAL_LIFETIME_FIXTURE", "horizon": 30,
            "plans": {name: evaluate(events) for name, events in plans.items()}}


class Tests(unittest.TestCase):
    def test_boundaries_and_place(self):
        e = source("a", 0)
        self.assertEqual(active([e], 1.999, e["place"]), [])
        self.assertEqual(active([e], 2, e["place"]), ["grain"])
        self.assertEqual(active([e], 12, e["place"]), [])
        self.assertEqual(active([e], 3, "other"), [])

    def test_same_time_no_amplitude_or_lifetime_reward(self):
        r = report()["plans"]
        self.assertEqual(r["one"]["response_integral"], r["simultaneous_three"]["response_integral"])
        self.assertEqual(r["simultaneous_three"]["application_cost"], 3)
        self.assertGreater(r["just_in_time"]["response_integral"], r["overlap"]["response_integral"])

    def test_relogin_and_duplicate(self):
        e = source("a", 0)
        self.assertEqual(active([e, e], 5, e["place"]), active(json.loads(json.dumps([e])), 5, e["place"]))
        with self.assertRaises(ValueError):
            active([e, {**e, "duration": 20}], 5, e["place"])

    def test_gain_ablation(self):
        self.assertEqual(evaluate([source("a", 0)], gain=0)["response_integral"], evaluate([], gain=0)["response_integral"])
        self.assertEqual(report()["plans"]["wrong_place"]["response_integral"], report()["plans"]["none"]["response_integral"])

    def test_standard_application_not_arbitrary_trace(self):
        with self.assertRaises(ValueError):
            active([{**source("a", 0), "cost": 0}], 3, "bottom:A")
        with self.assertRaises(ValueError):
            active([{**source("a", 0), "at": float("nan")}], 3, "bottom:A")


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

"""Independent recomputation of the 8 fixture goldens.

Deliberately does NOT import ``fixed_bake``. The formulas below are transcribed
by hand from the stated contract (开发需求 §3.4 / §4.3 / §3.3 / §3.5), so this
script and the reference implementation cannot fail in the same way for the same
shared misunderstanding: they agree only if both read the contract correctly.

Run:  python3 verify_goldens.py          (exit 0 = all 8 reproduced)
"""
import json
import os
import sys

FIXTURE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "fixtures", "bass_q3.json")

raw = json.load(open(FIXTURE_PATH))
PROFILES = raw["componentProfiles"]
CASES = raw["cases"]
SEED = raw["seed"]


def point_fit(t, p):
    """开发需求 §4.3 — piecewise linear/bezier temperature falloff."""
    a_min, a_max = p["temp_accept_min"], p["temp_accept_max"]
    f_min, f_max = p["temp_fav_min"], p["temp_fav_max"]
    if t < a_min or t > a_max:
        return 0.0
    if f_min <= t <= f_max:
        return 1.0
    if t < f_min:
        u = (t - a_min) / (f_min - a_min)
    else:
        u = (a_max - t) / (a_max - f_max)
    s = p["falloff_shape"]
    return u if s == "LINEAR" else u * u * (3 - 2 * u)


def fit(key, prof, cg):
    """开发需求 §3.2 / §4.3 — per-condition fit for the four components."""
    if key == "TEMPERATURE":
        lo, hi = cg["waterTemperatureRange"]
        return point_fit((lo + hi) / 2.0, prof["TEMPERATURE"])
    if key == "STRUCTURE":
        return prof["STRUCTURE"]["structure_affinity"][cg["structureType"]]
    if key == "FEEDING_LAYER":
        m = {"SURFACE": "foraging_surface_affinity",
             "MIDDLE": "foraging_middle_affinity",
             "BOTTOM": "foraging_bottom_affinity"}
        return max(prof["FEEDING_LAYER"][m[layer]]
                   for layer in cg["feedingEcologyLayers"])
    if key == "TIME_PERIOD":
        return prof["TIME_PERIOD"]["time_period_activity_coefficient"][cg["timePeriod"]]
    raise KeyError(key)


def gate_failed(key, v, prof):
    """开发需求 §3.3 — the gate fires only for CORE bindings."""
    if key in ("STRUCTURE", "FEEDING_LAYER", "TIME_PERIOD"):
        return v == 0.0
    if key == "TEMPERATURE":
        return v < prof["TEMPERATURE"]["temp_threshold"]
    return None


ROLES = {r["conditionKey"]: r["aggregationRole"]
         for r in raw["subject"]["resolvedSpatialOpportunityBindings"]}


def cmp(a, b):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) < 1e-12


def main():
    ok = 0
    for c in CASES:
        seed = dict(SEED)
        seed.update(c.get("seedOverride", {}))
        cg = c["conditionGroup"]
        fits = {k: fit(k, PROFILES, cg)
                for k, r in ROLES.items() if r in ("CORE", "SECONDARY")}
        failed = [k for k, r in ROLES.items()
                  if r == "CORE" and gate_failed(k, fits[k], PROFILES)]

        if failed:
            raw_env = None
            final = seed["envCoeffMin"] if seed["isBackgroundFish"] else 0.0
        else:
            core = 1.0
            for k, r in ROLES.items():
                if r == "CORE":
                    core *= fits[k]
            sec = 1.0
            for k, r in ROLES.items():
                if r == "SECONDARY":
                    sec *= fits[k]
            # §3.4 — secondary aggregation is the difference shrunk by 1/4.
            raw_env = core * (1.0 - (1.0 - sec) / 4.0)
            final = (max(raw_env, seed["envCoeffMin"])
                     if seed["isBackgroundFish"] else raw_env)

        weight = seed["baseOpportunityIntensity"] * final
        e = c["expect"]
        good = (cmp(raw_env, e["rawEnvCoeff"]) and cmp(final, e["finalEnvCoeff"])
                and cmp(weight, e["weight"])
                and (bool(failed) == e["gateFailed"]))
        ok += good
        print("%-18s raw=%-22r final=%-22r w=%-22r gate=%-5s %s"
              % (c["id"], raw_env, final, weight, bool(failed),
                 "OK" if good else "*** MISMATCH ***"))

    print("\n%d/%d goldens reproduced by an INDEPENDENT recomputation"
          % (ok, len(CASES)))
    return 0 if ok == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())

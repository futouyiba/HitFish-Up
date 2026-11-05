"""Proposal C working probe: Escape-like state description and fish-side trigger.

Layer split:
  prey side   -> StateMatchStrength in [0,1]: descriptive, shared across predators
  fish side   -> TriggerEvaluation_f: default equals StateMatchStrength in v1
  response    -> StateTriggerValue = TriggerBudget x TriggerEvaluation

Checks window filter, per-family applicability, max instead of sum, pause/alternation
ignored, typed statuses (NotConfigured, NotApplicable, Unknown, InvalidInput), and
that changing the predator does not alter the prey-side description.

Run: python3 -I prototypes/lure-response/proposal_c_escape_trigger_probe.py
"""

from __future__ import annotations

import math
import inspect
from dataclasses import dataclass, field

WINDOW = 0.50
TRIGGER_BUDGET = 0.10  # Working budget, unchanged by the layer split

# Working example: which event kinds each prey family consumes.
# An empty set means the family is configured but has no trigger valuation.
FAMILY_KINDS = {
    "baitfish": {"turn", "burst"},
    "crayfish": {"turn", "burst"},
    "frog": {"burst"},
    "bass_static": set(),
}


@dataclass(frozen=True)
class Event:
    time: float
    kind: str
    families: frozenset[str]
    strengths: dict[str, float] = field(default_factory=dict)


def _valid_strength(x) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(x) and 0.0 <= x <= 1.0


def state_match_strength(events, family: str, now: float, window: float = WINDOW):
    """Prey side: return (status, StateMatchStrength|None) for one prey family.

    Reads only presentation facts, events and the family's own state rules. Does not
    read the predator's diet, closing ability or motivation.
    """
    if family not in FAMILY_KINDS:
        return "NotConfigured", None
    if not FAMILY_KINDS[family]:
        return "NotApplicable", 0.0

    applicable = [
        e for e in events
        if 0.0 <= now - e.time <= window
        and e.kind in ("turn", "burst")
        and e.kind in FAMILY_KINDS[family]
        and family in e.families
    ]
    if not applicable:
        return "ResolvedNonResponsive", 0.0

    used = []
    for e in applicable:
        if family not in e.strengths:
            return "Missing", None
        value = e.strengths[family]
        if value is None:
            return "Unknown", None
        if not _valid_strength(value):
            return "InvalidInput", None
        used.append(float(value))

    return "ResolvedResponsive", max(used)


def trigger_evaluation(family: str, match_strength: float,
                       predator: str = "default", table=None):
    """Fish side: map an already explained state to a normalized trigger effect.

    `table` maps (predator, family) -> callable(match_strength) -> (status, value).
    No table entry, or no table at all, falls back to the shared default; a missing
    species entry is not NotConfigured. Any table here is a probe fixture, not an
    approved parameter set.
    """
    if table is not None:
        rule = table.get((predator, family))
        if rule is not None:
            status, value = rule(match_strength)
            if status != "Resolved":
                return status, None
            if not _valid_strength(value):
                return "InvalidInput", None
            return "Resolved", float(value)
    return "Resolved", match_strength


def trigger_value(events, family: str, now: float, predator: str = "default",
                  table=None) -> float:
    """Prey description -> fish-side evaluation -> StateTriggerValue.

    Missing and Unknown both propagate as ResolutionIncomplete; NotConfigured /
    InvalidInput stay unrollable.
    """
    status, strength = state_match_strength(events, family, now)
    if status in ("Missing", "Unknown"):
        raise ValueError(f"ResolutionIncomplete: trigger evidence is {status.lower()}")
    if status in ("NotConfigured", "InvalidInput"):
        raise ValueError(f"not rollable: {status}")
    eval_status, evaluated = trigger_evaluation(family, strength, predator, table)
    if eval_status != "Resolved":
        raise ValueError(f"not rollable: {eval_status}")
    return TRIGGER_BUDGET * evaluated


def main() -> None:
    now = 1.00
    a = [Event(0.90, "turn", frozenset({"baitfish"}), {"baitfish": 0.80})]
    b = a + [Event(0.95, "burst", frozenset({"baitfish"}), {"baitfish": 0.60})]
    c = [Event(0.30, "turn", frozenset({"baitfish"}), {"baitfish": 0.60}),
         Event(0.90, "turn", frozenset({"baitfish"}), {"baitfish": 0.60})]
    d = [Event(0.20, "turn", frozenset({"baitfish"}), {"baitfish": 0.90})]
    e = [Event(0.95, "pause", frozenset({"baitfish"}), {"baitfish": 0.90})]
    f = [Event(0.95, "alternation", frozenset({"baitfish"}), {"baitfish": 0.90})]
    h = [Event(0.90, "turn", frozenset({"crayfish"}), {"crayfish": 0.80})]
    missing = [Event(0.90, "turn", frozenset({"baitfish"}), {})]
    unresolved = [Event(0.90, "turn", frozenset({"baitfish"}), {"baitfish": None})]
    invalid = [Event(0.90, "turn", frozenset({"baitfish"}), {"baitfish": 1.40})]

    cases = [
        ("A single turn", a, "baitfish", "ResolvedResponsive", 0.80),
        ("B turn+burst max", b, "baitfish", "ResolvedResponsive", 0.80),
        ("C repeated turns", c, "baitfish", "ResolvedResponsive", 0.60),
        ("D outside window", d, "baitfish", "ResolvedNonResponsive", 0.0),
        ("E pause ignored", e, "baitfish", "ResolvedNonResponsive", 0.0),
        ("F alternation ignored", f, "baitfish", "ResolvedNonResponsive", 0.0),
        ("G no events", [], "baitfish", "ResolvedNonResponsive", 0.0),
        ("H other family only", h, "baitfish", "ResolvedNonResponsive", 0.0),
        ("J missing strength", missing, "baitfish", "Missing", None),
        ("J2 unresolved strength", unresolved, "baitfish", "Unknown", None),
        ("K no trigger valuation", a, "bass_static", "NotApplicable", 0.0),
        ("L out of range", invalid, "baitfish", "InvalidInput", None),
        ("M unknown family", a, "shrimp", "NotConfigured", None),
    ]

    print("case\tstatus\tStateMatchStrength")
    for name, events, family, want_status, want_value in cases:
        status, value = state_match_strength(events, family, now)
        shown = "-" if value is None else f"{value:.2f}"
        print(f"{name}\t{status}\t{shown}")
        assert (status, value) == (want_status, want_value), name

    # A vs B: adding a burst does not sum into the description.
    assert state_match_strength(b, "baitfish", now)[1] == 0.80

    # Same motion, different family: different intensity, not one shared number.
    mixed = [Event(0.90, "turn", frozenset({"baitfish", "crayfish"}),
                   {"baitfish": 0.80, "crayfish": 0.30})]
    assert state_match_strength(mixed, "baitfish", now)[1] == 0.80
    assert state_match_strength(mixed, "crayfish", now)[1] == 0.30

    # Frog consumes burst only; a turn alone produces no trigger for frog.
    frog_turn = [Event(0.90, "turn", frozenset({"frog"}), {"frog": 0.90})]
    frog_burst = [Event(0.90, "burst", frozenset({"frog"}), {"frog": 0.70})]
    assert state_match_strength(frog_turn, "frog", now) == ("ResolvedNonResponsive", 0.0)
    assert state_match_strength(frog_burst, "frog", now) == ("ResolvedResponsive", 0.70)

    # Unknown evidence must not be rolled as zero.
    try:
        trigger_value(missing, "baitfish", now)
        raise AssertionError("unknown trigger must not produce a value")
    except ValueError as exc:
        assert "ResolutionIncomplete" in str(exc)

    # Future-dated events are ignored, not read ahead.
    future = [Event(1.20, "turn", frozenset({"baitfish"}), {"baitfish": 0.90})]
    assert state_match_strength(future, "baitfish", now) == ("ResolvedNonResponsive", 0.0)

    # --- layer ownership ---
    # Structural guard: the prey description must not accept a predator at all.
    # If someone later adds fish-side input here, this assertion fails.
    assert set(inspect.signature(state_match_strength).parameters) == {
        "events", "family", "now", "window"
    }
    try:
        state_match_strength(a, "baitfish", now, predator="pike")
        raise AssertionError("prey description must not accept a predator")
    except TypeError:
        pass
    # The prey-side description does not depend on the predator.
    assert state_match_strength(a, "baitfish", now)[1] == 0.80
    # With no per-species configuration, every predator uses the shared default.
    for predator in ("bass", "pike", "catfish"):
        assert trigger_evaluation("baitfish", 0.80, predator) == ("Resolved", 0.80)
    # A configured fish-side rule may differ; this is a probe fixture, not a proposal.
    table = {("pike", "baitfish"): lambda s: ("Resolved", 0.5 * s)}
    assert trigger_evaluation("baitfish", 0.80, "bass", table) == ("Resolved", 0.80)
    assert trigger_evaluation("baitfish", 0.80, "pike", table) == ("Resolved", 0.40)
    # Fish-side output out of range is InvalidInput, not clamped.
    bad_table = {("pike", "baitfish"): lambda s: ("Resolved", 1.40)}
    assert trigger_evaluation("baitfish", 0.80, "pike", bad_table) == ("InvalidInput", None)

    # Default evaluation preserves the pre-split numbers.
    assert abs(trigger_value(a, "baitfish", now) - 0.08) < 1e-12

    # Branch isolation: prey A has an escape event, prey B does not.
    per_family = [Event(0.90, "turn", frozenset({"baitfish"}), {"baitfish": 0.80})]
    a_status, a_strength = state_match_strength(per_family, "baitfish", now)
    c_status, c_strength = state_match_strength(per_family, "crayfish", now)
    assert (a_status, a_strength) == ("ResolvedResponsive", 0.80)
    assert (c_status, c_strength) == ("ResolvedNonResponsive", 0.0)
    assert trigger_evaluation("crayfish", c_strength)[1] == 0.0

    print("Escape-like state description and fish-side trigger probe passed")


if __name__ == "__main__":
    main()

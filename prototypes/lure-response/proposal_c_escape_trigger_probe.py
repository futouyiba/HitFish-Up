"""Proposal C working probe: Escape-like trigger v1.

Checks window filter, per-family applicability, max instead of sum, pause/alternation
ignored, and typed statuses: NotConfigured, NotApplicable, Unknown, InvalidInput.

Run: python3 -I prototypes/lure-response/proposal_c_escape_trigger_probe.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

WINDOW = 0.50

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


def trigger_intensity(events, family: str, now: float, window: float = WINDOW):
    """Return (status, intensity|None) for one prey family."""
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
            return "Unknown", None
        value = e.strengths[family]
        if not _valid_strength(value):
            return "InvalidInput", None
        used.append(float(value))

    return "ResolvedResponsive", max(used)


def trigger_value(events, family: str, now: float) -> float:
    """Map Unknown to ResolutionIncomplete; other non-numeric statuses stay unrollable."""
    status, value = trigger_intensity(events, family, now)
    if status == "Unknown":
        raise ValueError("ResolutionIncomplete: trigger evidence is unknown")
    if status in ("NotConfigured", "InvalidInput"):
        raise ValueError(f"not rollable: {status}")
    return value


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
        ("J missing strength", missing, "baitfish", "Unknown", None),
        ("K no trigger valuation", a, "bass_static", "NotApplicable", 0.0),
        ("L out of range", invalid, "baitfish", "InvalidInput", None),
        ("M unknown family", a, "shrimp", "NotConfigured", None),
    ]

    print("case\tstatus\tintensity")
    for name, events, family, want_status, want_value in cases:
        status, value = trigger_intensity(events, family, now)
        shown = "-" if value is None else f"{value:.2f}"
        print(f"{name}\t{status}\t{shown}")
        assert (status, value) == (want_status, want_value), name

    # A vs B: adding a burst does not sum into the trigger.
    assert trigger_intensity(b, "baitfish", now)[1] == 0.80

    # Same motion, different family: different intensity, not one shared number.
    mixed = [Event(0.90, "turn", frozenset({"baitfish", "crayfish"}),
                   {"baitfish": 0.80, "crayfish": 0.30})]
    assert trigger_intensity(mixed, "baitfish", now)[1] == 0.80
    assert trigger_intensity(mixed, "crayfish", now)[1] == 0.30

    # Frog consumes burst only; a turn alone produces no trigger for frog.
    frog_turn = [Event(0.90, "turn", frozenset({"frog"}), {"frog": 0.90})]
    frog_burst = [Event(0.90, "burst", frozenset({"frog"}), {"frog": 0.70})]
    assert trigger_intensity(frog_turn, "frog", now) == ("ResolvedNonResponsive", 0.0)
    assert trigger_intensity(frog_burst, "frog", now) == ("ResolvedResponsive", 0.70)

    # Unknown evidence must not be rolled as zero.
    try:
        trigger_value(missing, "baitfish", now)
        raise AssertionError("unknown trigger must not produce a value")
    except ValueError as exc:
        assert "ResolutionIncomplete" in str(exc)

    # Future-dated events are ignored, not read ahead.
    future = [Event(1.20, "turn", frozenset({"baitfish"}), {"baitfish": 0.90})]
    assert trigger_intensity(future, "baitfish", now) == ("ResolvedNonResponsive", 0.0)

    print("Escape-like trigger probe passed")


if __name__ == "__main__":
    main()

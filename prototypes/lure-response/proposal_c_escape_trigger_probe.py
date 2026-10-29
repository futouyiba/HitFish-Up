"""Proposal C working probe: Escape-like trigger admission.

Checks the v1 rules in docs/proposals/lure-response-proposal-c-escape-trigger-v1.md:
window filter, per-family applicability, max instead of sum, pause/alternation ignored,
NotConfigured propagation.

Run: python3 -I prototypes/lure-response/proposal_c_escape_trigger_probe.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

WINDOW = 0.50

# Working example: which event kinds each prey family consumes.
FAMILY_KINDS = {
    "baitfish": {"turn", "burst"},
    "crayfish": {"turn", "burst"},
    "frog": {"burst"},
}


@dataclass(frozen=True)
class Event:
    time: float
    kind: str
    strengths: dict[str, float] = field(default_factory=dict)


def trigger_intensity(events, family: str, now: float, window: float = WINDOW):
    if family not in FAMILY_KINDS:
        return "NotConfigured", None
    used = [
        e.strengths[family]
        for e in events
        if 0.0 <= now - e.time <= window
        and e.kind in ("turn", "burst")
        and e.kind in FAMILY_KINDS[family]
        and family in e.strengths
    ]
    if not used:
        return "ResolvedNonResponsive", 0.0
    return "ResolvedResponsive", max(used)


def main() -> None:
    now = 1.00
    a = [Event(0.90, "turn", {"baitfish": 0.80})]
    b = a + [Event(0.95, "burst", {"baitfish": 0.60})]
    c = [Event(0.30, "turn", {"baitfish": 0.60}), Event(0.90, "turn", {"baitfish": 0.60})]
    d = [Event(0.20, "turn", {"baitfish": 0.90})]
    e = [Event(0.95, "pause", {"baitfish": 0.90})]
    f = [Event(0.95, "alternation", {"baitfish": 0.90})]
    h = [Event(0.90, "turn", {"crayfish": 0.80})]

    cases = [
        ("A single turn", a, "baitfish", 0.80),
        ("B turn+burst max", b, "baitfish", 0.80),
        ("C repeated turns", c, "baitfish", 0.60),
        ("D outside window", d, "baitfish", 0.0),
        ("E pause ignored", e, "baitfish", 0.0),
        ("F alternation ignored", f, "baitfish", 0.0),
        ("G no events", [], "baitfish", 0.0),
        ("H other family only", h, "baitfish", 0.0),
    ]

    print("case\tstatus\tintensity")
    for name, events, family, expect in cases:
        status, value = trigger_intensity(events, family, now)
        actual = 0.0 if value is None else value
        print(f"{name}\t{status}\t{actual:.2f}")
        assert value == expect, name

    # A vs B: adding a burst does not sum into the trigger.
    assert trigger_intensity(b, "baitfish", now)[1] == 0.80

    # Same motion, different family: different intensity, not one shared number.
    mixed = [Event(0.90, "turn", {"baitfish": 0.80, "crayfish": 0.30})]
    assert trigger_intensity(mixed, "baitfish", now)[1] == 0.80
    assert trigger_intensity(mixed, "crayfish", now)[1] == 0.30

    # Frog consumes burst only; a turn alone produces no trigger for frog.
    frog_turn = [Event(0.90, "turn", {"frog": 0.90})]
    frog_burst = [Event(0.90, "burst", {"frog": 0.70})]
    assert trigger_intensity(frog_turn, "frog", now) == ("ResolvedNonResponsive", 0.0)
    assert trigger_intensity(frog_burst, "frog", now) == ("ResolvedResponsive", 0.70)

    # Unknown family: not silently zero.
    assert trigger_intensity(a, "shrimp", now) == ("NotConfigured", None)

    # Future-dated events are ignored, not read ahead.
    future = [Event(1.20, "turn", {"baitfish": 0.90})]
    assert trigger_intensity(future, "baitfish", now) == ("ResolvedNonResponsive", 0.0)

    print("Escape-like trigger probe passed")


if __name__ == "__main__":
    main()

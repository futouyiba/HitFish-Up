"""Proposal C Step-4: test whether Prey Opportunity Interpretation is a real production object.

The probe compares two downstream paths:
1) consume constituent semantics directly;
2) first wrap the same constituents in a Prey Opportunity packet, then consume it.

If both paths have identical decision power, the packet is a projection / explain view,
not an independently authoritative production object.

All rules are illustrative topology probes, not production behavior.
"""

from dataclasses import dataclass
from enum import Enum


class Affordance(str, Enum):
    FEASIBLE = "Feasible"
    CONSTRAINED = "Constrained"
    INFEASIBLE = "Infeasible"


@dataclass(frozen=True)
class Inputs:
    behavior: frozenset[str]
    condition: frozenset[str]
    affordance: Affordance
    dwell: str
    motivation: str


def direct_decision(x: Inputs):
    """Illustrative Complete-Mode consumer using constituent fields directly."""
    if x.affordance == Affordance.INFEASIBLE:
        mode = "observe_or_track"
    elif "escaping_like" in x.behavior and x.affordance == Affordance.FEASIBLE:
        mode = "pursuit_or_intercept"
    elif "struggling_like" in x.behavior and x.affordance != Affordance.INFEASIBLE:
        mode = "close_strike_window"
    else:
        mode = "generic_feeding_evaluation"

    explain = []
    if "vulnerable_like" in x.condition:
        explain.append("vulnerable_like")
    if x.dwell == "favorable":
        explain.append("favorable_dwell")

    return {
        "mode": mode,
        "explain": tuple(explain),
        "motivation": x.motivation,
    }


def build_opportunity_projection(x: Inputs):
    """No new fact or score is introduced here; this is only a grouped view."""
    return {
        "prey_semantics": {
            "behavior": tuple(sorted(x.behavior)),
            "condition": tuple(sorted(x.condition)),
        },
        "task_affordance": x.affordance.value,
        "temporal_context": {"dwell": x.dwell},
        "motivation": x.motivation,
    }


def packet_decision(packet):
    return direct_decision(
        Inputs(
            behavior=frozenset(packet["prey_semantics"]["behavior"]),
            condition=frozenset(packet["prey_semantics"]["condition"]),
            affordance=Affordance(packet["task_affordance"]),
            dwell=packet["temporal_context"]["dwell"],
            motivation=packet["motivation"],
        )
    )


def run_probe():
    cases = [
        # same escaping semantic, feasible capture
        Inputs(frozenset({"escaping_like"}), frozenset(), Affordance.FEASIBLE, "neutral", "ready"),
        # same escaping semantic, infeasible capture
        Inputs(frozenset({"escaping_like"}), frozenset(), Affordance.INFEASIBLE, "neutral", "ready"),
        # multiple semantics coexist
        Inputs(
            frozenset({"struggling_like"}),
            frozenset({"vulnerable_like"}),
            Affordance.FEASIBLE,
            "favorable",
            "ready",
        ),
        # vulnerable semantic does not override low motivation or affordance
        Inputs(frozenset(), frozenset({"vulnerable_like"}), Affordance.CONSTRAINED, "neutral", "low"),
    ]

    direct = [direct_decision(c) for c in cases]
    through_packet = [packet_decision(build_opportunity_projection(c)) for c in cases]

    # Core consumer-equivalence test: packet adds no new decision power.
    assert direct == through_packet

    # Escaping semantic alone does not determine opportunity quality / response mode.
    assert direct[0]["mode"] == "pursuit_or_intercept"
    assert direct[1]["mode"] == "observe_or_track"

    # Sparse semantics may coexist and remain explainable without a flat enum.
    assert direct[2]["explain"] == ("vulnerable_like", "favorable_dwell")

    # Vulnerability remains semantic; it does not silently rewrite motivation.
    assert direct[3]["motivation"] == "low"

    return {
        "consumer_equivalence": True,
        "production_object_admission": "not justified",
        "recommended_role": "projection_or_explain_view",
    }


if __name__ == "__main__":
    result = run_probe()
    print("Opportunity consumer probe passed:", result)

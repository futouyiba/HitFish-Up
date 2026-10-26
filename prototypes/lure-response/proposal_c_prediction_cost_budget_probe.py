"""Working probe for Proposal C PredictionChallenge effect-size budget.

This file tests topology and relative budget only. Values are not production calibration.
"""

from math import cos, exp, pi

TRIGGER_BUDGET = 0.12
PREDICTION_BUDGET = 0.10
RECOVERY_TAU_S = 0.60


def turn_strength(deg: float) -> float:
    rad = deg * pi / 180.0
    return (1.0 - cos(rad)) / 2.0


def prediction_challenge(turn_deg: float, age_s: float) -> float:
    return turn_strength(turn_deg) * exp(-age_s / RECOVERY_TAU_S)


def row(name: str, turn_deg: float, age_s: float, trigger_intensity: float):
    p = 0.0 if turn_deg == 0 else prediction_challenge(turn_deg, age_s)
    trigger = TRIGGER_BUDGET * trigger_intensity
    prediction_cost = PREDICTION_BUDGET * p
    return {
        "case": name,
        "P": p,
        "trigger": trigger,
        "prediction_cost": prediction_cost,
        "net_state_delta": trigger - prediction_cost,
    }


CASES = [
    row("straight", 0, 10.0, 0.0),
    row("single moderate dart now", 90, 0.0, 0.85),
    row("single moderate dart 0.5s ago", 90, 0.5, 0.85),
    row("single hard dart now", 150, 0.0, 1.0),
    row("single hard dart 0.5s ago", 150, 0.5, 1.0),
]


if __name__ == "__main__":
    for c in CASES:
        print(
            f"{c['case']:<31} "
            f"P={c['P']:.3f} "
            f"trigger={c['trigger']:.3f} "
            f"pred_cost={c['prediction_cost']:.3f} "
            f"net={c['net_state_delta']:+.3f}"
        )

    # Structural guards: prediction is a correction, not an independent veto.
    moderate = CASES[1]
    hard = CASES[3]
    assert moderate["net_state_delta"] > 0
    assert hard["net_state_delta"] > 0
    assert hard["net_state_delta"] < moderate["net_state_delta"]
    assert PREDICTION_BUDGET <= TRIGGER_BUDGET

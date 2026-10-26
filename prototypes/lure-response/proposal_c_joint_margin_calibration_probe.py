"""Proposal C joint DecisionMargin calibration seed probe.

Candidate / Working probe only. Not production tuning.
"""

PREFERRED = 1.00
GOOD = 0.70
MARGINAL = 0.40
POOR = 0.00
K_MOT = 0.40


def willingness_threshold(motivation: float) -> float:
    if not 0.0 <= motivation <= 1.0:
        raise ValueError("motivation must be in [0,1]")
    return MARGINAL + K_MOT * (0.5 - motivation)


def decision_margin(food_value: float, motivation: float, *, trigger: float = 0.0, cost: float = 0.0) -> float:
    return food_value + trigger - cost - willingness_threshold(motivation)


def approx(a: float, b: float, eps: float = 1e-9) -> bool:
    return abs(a - b) <= eps


def run_regression() -> None:
    # Threshold ladder.
    expected_thresholds = {
        0.00: 0.60,
        0.25: 0.50,
        0.50: 0.40,
        0.75: 0.30,
        1.00: 0.20,
    }
    for motivation, expected in expected_thresholds.items():
        actual = willingness_threshold(motivation)
        assert approx(actual, expected), (motivation, actual, expected)

    # A: Preferred remains healthy under low motivation + moderate burden.
    assert decision_margin(PREFERRED, 0.25, cost=0.15) > 0.30

    # B: Good remains usable under reference motivation + moderate burden.
    assert decision_margin(GOOD, 0.50, cost=0.15) > 0.0

    # C: Marginal is weak under reference motivation + moderate burden.
    assert decision_margin(MARGINAL, 0.50, cost=0.15) < 0.0

    # D: Same Marginal flips under higher motivation, low burden and ordinary trigger.
    assert decision_margin(MARGINAL, 0.75, trigger=0.10, cost=0.05) > 0.0

    # E: Poor is not rescued by maximum motivation + upper trigger alone.
    assert decision_margin(POOR, 1.00, trigger=0.15, cost=0.0) < 0.0

    # F: Poor can cross only when another legal prey-specific positive adjustment exists.
    poor_adjusted_food_value = POOR + 0.10
    assert decision_margin(poor_adjusted_food_value, 1.00, trigger=0.15, cost=0.0) > 0.0

    # Additional guards.
    assert decision_margin(GOOD, 0.00, cost=0.0) > 0.0
    assert decision_margin(MARGINAL, 0.00, cost=0.0) < 0.0
    assert decision_margin(MARGINAL, 1.00, cost=0.0) > 0.0


if __name__ == "__main__":
    run_regression()
    print("Proposal C joint margin calibration seed: PASS")

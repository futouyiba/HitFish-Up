"""Proposal C DecisionMargin -> response projection probe.

Candidate calibration helper only. Not production behavior.
"""

M0 = 0.0
M1 = 0.30


def response_projection(margin: float) -> float:
    if M1 <= M0:
        raise ValueError("M1 must be > M0")
    return max(0.0, min(1.0, (margin - M0) / (M1 - M0)))


def assert_close(actual: float, expected: float, eps: float = 1e-9) -> None:
    if abs(actual - expected) > eps:
        raise AssertionError((actual, expected))


REGRESSION_POINTS = {
    -0.10: 0.0,
    0.00: 0.0,
    0.05: 1.0 / 6.0,
    0.10: 1.0 / 3.0,
    0.15: 0.5,
    0.20: 2.0 / 3.0,
    0.30: 1.0,
    0.50: 1.0,
}

for margin, expected in REGRESSION_POINTS.items():
    assert_close(response_projection(margin), expected)

# Joint calibration seed examples.
PREFERRED = 1.00
GOOD = 0.70
MARGINAL = 0.40
POOR = 0.00
K_MOT = 0.40


def threshold(motivation: float) -> float:
    return MARGINAL + K_MOT * (0.5 - motivation)


def margin(food_value: float, motivation: float, trigger: float = 0.0, cost: float = 0.0) -> float:
    return food_value + trigger - cost - threshold(motivation)


CASES = {
    "preferred_reference_zero_burden": (PREFERRED, 0.5, 0.0, 0.0, 1.0),
    "good_reference_zero_burden": (GOOD, 0.5, 0.0, 0.0, 1.0),
    "good_ordinary_burden": (GOOD, 0.5, 0.0, 0.15, 0.5),
    "marginal_reference": (MARGINAL, 0.5, 0.0, 0.0, 0.0),
    "marginal_favorable": (MARGINAL, 0.75, 0.10, 0.05, 0.5),
    "poor_max_mot_trigger": (POOR, 1.0, 0.15, 0.0, 0.0),
}

for name, (fv, mot, trig, cost, expected_c) in CASES.items():
    m = margin(fv, mot, trig, cost)
    c = response_projection(m)
    assert_close(c, expected_c)
    print(f"{name}: margin={m:.3f}, C={c:.3f}")

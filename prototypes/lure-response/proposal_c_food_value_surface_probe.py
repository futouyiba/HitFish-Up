"""Proposal C food-value response-surface probe.

Working topology probe only. Numbers are not production calibration.
"""

RELATION_VALUE = {
    "Preferred": 1.00,
    "Good": 0.80,
    "Marginal": 0.55,
    "Poor": 0.35,
    "Reject": 0.00,
}


def response(value: float, motivation: float, strain: float) -> float:
    if value <= 0 or motivation <= 0 or strain > 1:
        return 0.0
    task_cost = 0.33 * strain ** 4.0
    threshold = 0.72 - 0.45 * motivation
    margin = value - task_cost - threshold
    return max(0.0, min(1.0, margin / 0.38))


def run() -> None:
    # Hard semantic boundary.
    for m in (0.25, 0.60, 0.95):
        for s in (0.15, 0.55, 0.80):
            assert response(RELATION_VALUE["Reject"], m, s) == 0.0

    # Ordered target relation must remain monotone under same context.
    ordered = ["Reject", "Poor", "Marginal", "Good", "Preferred"]
    for m in (0.25, 0.60, 0.90):
        for s in (0.25, 0.55, 0.80):
            xs = [response(RELATION_VALUE[k], m, s) for k in ordered]
            assert xs == sorted(xs)

    # Poor is not a hard semantic zero: only an extreme favorable context revives it slightly.
    poor_best = response(RELATION_VALUE["Poor"], 0.95, 0.15)
    poor_normal = response(RELATION_VALUE["Poor"], 0.60, 0.25)
    assert 0.05 <= poor_best <= 0.25
    assert poor_normal == 0.0

    # Marginal requires either better motivation or easier task.
    marginal_bad = response(RELATION_VALUE["Marginal"], 0.25, 0.25)
    marginal_normal = response(RELATION_VALUE["Marginal"], 0.60, 0.25)
    marginal_good = response(RELATION_VALUE["Marginal"], 0.90, 0.25)
    assert marginal_bad == 0.0
    assert 0.10 <= marginal_normal <= 0.40
    assert marginal_good > marginal_normal

    # Good remains useful in normal conditions and can be degraded by high task strain.
    assert response(RELATION_VALUE["Good"], 0.60, 0.25) >= 0.75
    assert response(RELATION_VALUE["Good"], 0.60, 0.80) < response(RELATION_VALUE["Good"], 0.60, 0.25)

    print("Food-value surface probe passed")


if __name__ == "__main__":
    run()

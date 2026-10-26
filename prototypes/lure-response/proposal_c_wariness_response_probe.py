"""Proposal C wariness response topology probe.

Working fixture only. Numbers are not production parameters.
"""


def risk_cost(wariness: float, suspicion: float, k_wary: float = 0.12) -> float:
    assert 0.0 <= wariness <= 1.0
    assert 0.0 <= suspicion <= 1.0
    assert k_wary >= 0.0
    return k_wary * wariness * suspicion


def margin(food: float, trigger: float, closing: float, prediction: float,
           threshold: float, wariness: float, suspicion: float,
           k_wary: float = 0.12) -> float:
    return (
        food
        + trigger
        - closing
        - prediction
        - risk_cost(wariness, suspicion, k_wary)
        - threshold
    )


def main() -> None:
    base = dict(food=0.80, trigger=0.10, closing=0.08, prediction=0.03, threshold=0.45)
    cases = [
        ("low wary, low suspicion", 0.20, 0.15),
        ("high wary, low suspicion", 0.85, 0.15),
        ("low wary, high suspicion", 0.20, 0.85),
        ("high wary, high suspicion", 0.85, 0.85),
        ("high wary, zero suspicion", 0.85, 0.00),
    ]

    print("case\tW\tS\tRiskCost\tMargin")
    for name, w, s in cases:
        rc = risk_cost(w, s)
        m = margin(**base, wariness=w, suspicion=s)
        print(f"{name}\t{w:.2f}\t{s:.2f}\t{rc:.3f}\t{m:.3f}")

    # Acceptance guards.
    assert risk_cost(0.9, 0.0) == 0.0
    assert risk_cost(0.0, 0.9) == 0.0
    assert risk_cost(0.8, 0.8) > risk_cost(0.2, 0.8)
    assert risk_cost(0.8, 0.8) > risk_cost(0.8, 0.2)

    # Wariness is soft only: a strong positive state can still yield a positive margin.
    assert margin(0.8, 0.2, 0.02, 0.01, 0.35, 1.0, 1.0) > 0.0


if __name__ == "__main__":
    main()

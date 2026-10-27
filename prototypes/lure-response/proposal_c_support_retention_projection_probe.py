"""Proposal C probe: prey support -> response retention projection.

Working-only. Tests whether a non-linear projection is justified.
"""


def identity(s: float) -> float:
    return s


def soft_gate(s: float, h: float = 0.35) -> float:
    if s <= 0:
        return 0.0
    return (s * s) / (s * s + h * h)


def sqrt_boost(s: float) -> float:
    return s ** 0.5


def retained_response(support: float, c_conditional: float, projection=identity) -> float:
    return projection(support) * c_conditional


if __name__ == "__main__":
    supports = [0.1, 0.2, 0.4, 0.6, 0.8, 0.9]
    c_conditional = 0.8
    print("support identity soft_gate sqrt_boost")
    for s in supports:
        print(
            f"{s:.2f} "
            f"{retained_response(s,c_conditional,identity):.3f} "
            f"{retained_response(s,c_conditional,soft_gate):.3f} "
            f"{retained_response(s,c_conditional,sqrt_boost):.3f}"
        )

    # Core topology checks.
    assert retained_response(0.0, 1.0) == 0.0
    assert retained_response(1.0, 0.7) == 0.7
    assert retained_response(0.4, 0.8) < retained_response(0.9, 0.8)
    print("support retention projection probe passed")

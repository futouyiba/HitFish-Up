import math

Q_REF = {
    "HighClosing": 0.45,
    "GeneralClosing": 0.65,
    "LowClosing": 0.90,
}

K_CLOSE = 0.08 * 4.0 / (Q_REF["GeneralClosing"] ** 2)


def hard_share_isotropic_2d(q: float) -> float:
    if q <= 1.0:
        return 0.0
    return math.acos(1.0 / q) / math.pi


def mean_soft_cost_when_q_le_1(q: float) -> float:
    assert q <= 1.0
    return K_CLOSE * q * q / 4.0


def q_for(archetype: str, speed_multiple_of_vref: float) -> float:
    return Q_REF[archetype] * speed_multiple_of_vref


def main() -> None:
    assert abs(K_CLOSE - 0.757396449704142) < 1e-12

    # Normal steady separation.
    assert mean_soft_cost_when_q_le_1(Q_REF["HighClosing"]) < 0.04
    assert abs(mean_soft_cost_when_q_le_1(Q_REF["GeneralClosing"]) - 0.08) < 1e-12
    assert 0.15 < mean_soft_cost_when_q_le_1(Q_REF["LowClosing"]) < 0.16

    # Slow remains feasible for all three profiles.
    for archetype in Q_REF:
        assert q_for(archetype, 0.5) < 0.5

    # Fast search: LowClosing crosses hard-feasibility boundary,
    # GeneralClosing is near it, HighClosing remains soft-cost dominated.
    assert q_for("HighClosing", 1.5) < 0.7
    assert 0.95 < q_for("GeneralClosing", 1.5) < 1.0
    assert q_for("LowClosing", 1.5) > 1.0
    assert 0.23 < hard_share_isotropic_2d(q_for("LowClosing", 1.5)) < 0.24

    # Burst: General and Low have angle-local hard infeasibility;
    # High remains under q=1.
    assert q_for("HighClosing", 2.0) < 1.0
    assert 0.22 < hard_share_isotropic_2d(q_for("GeneralClosing", 2.0)) < 0.23
    assert 0.31 < hard_share_isotropic_2d(q_for("LowClosing", 2.0)) < 0.32

    print("K_CLOSE", round(K_CLOSE, 6))
    for speed_label, multiplier in [
        ("Slow", 0.5),
        ("Normal", 1.0),
        ("Fast", 1.5),
        ("Burst", 2.0),
    ]:
        print(speed_label)
        for archetype in Q_REF:
            q = q_for(archetype, multiplier)
            print(
                archetype,
                "q=", round(q, 3),
                "hard_share=", round(hard_share_isotropic_2d(q), 3),
            )


if __name__ == "__main__":
    main()

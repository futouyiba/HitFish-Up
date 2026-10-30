"""Proposal C probe: favorable dwell ownership.

Goal: show that longer favorable dwell can increase cumulative encounter/attack
opportunity without changing instantaneous Feeding response C.

Illustrative only. The exposure formula below is NOT a production contract.
"""

from math import exp


def cumulative_opportunity(instant_c: float, duration_s: float, opportunity_rate_per_s: float = 1.0) -> float:
    """Illustrative hazard-style exposure projection, not production math."""
    return 1.0 - exp(-opportunity_rate_per_s * instant_c * duration_s)


def main() -> None:
    instant_c = 0.60

    short_dwell = 0.20
    long_dwell = 1.20

    # Controlled case: current prey interpretation, FoodValue, Trigger,
    # Closing, Prediction and Motivation are identical.
    c_short = instant_c
    c_long = instant_c

    assert c_short == c_long

    p_short = cumulative_opportunity(c_short, short_dwell)
    p_long = cumulative_opportunity(c_long, long_dwell)

    assert p_long > p_short

    print(f"instant C: short={c_short:.3f}, long={c_long:.3f}")
    print(f"illustrative cumulative exposure: short={p_short:.3f}, long={p_long:.3f}")
    print("PASS: dwell changes exposure, not instantaneous Feeding response")


if __name__ == "__main__":
    main()

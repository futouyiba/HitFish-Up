"""Proposal C Step 4/5 probe: feeding response aggregation topology.

Working hypothesis only. Numbers are topology fixtures, not production calibration.

Question attacked:
Should Food Value and Feeding Motivation be multiplied into one symmetric Drive,
or should Motivation alter the willingness-to-act threshold while Food Value and
Task Cost remain decision quantities?
"""

from dataclasses import dataclass


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


@dataclass(frozen=True)
class FeedingInput:
    food_value: float
    motivation: float
    task_strain: float
    resolved: bool = True
    mode_valid: bool = True


def task_cost(strain: float) -> float:
    # Working shaping only: low strain is cheap; cost rises toward the capacity edge.
    return 0.45 * (strain ** 1.6)


def willingness_threshold(motivation: float) -> float:
    # Working shaping only: high motivation lowers the reservation threshold.
    return 0.90 - 0.80 * motivation


def response_curve(margin: float) -> float:
    # Working shaping only: below threshold => no response; then a bounded ramp.
    return clamp01(margin / 0.45)


def resolve_threshold_model(x: FeedingInput):
    if not x.resolved:
        return ("ResolutionIncomplete", None)
    if not x.mode_valid:
        return ("ResolvedNonResponsive", 0.0)
    if x.task_strain > 1.0:
        return ("ResolvedNonResponsive", 0.0)
    if x.food_value <= 0.0 or x.motivation <= 0.0:
        return ("ResolvedNonResponsive", 0.0)

    margin = (
        x.food_value
        - task_cost(x.task_strain)
        - willingness_threshold(x.motivation)
    )
    c = response_curve(margin)
    if c <= 0.0:
        return ("ResolvedNonResponsive", 0.0)
    return ("ResolvedResponsive", c)


def naive_product_drive(food_value: float, motivation: float) -> float:
    return food_value * motivation


def run_probe() -> None:
    # A. Symmetry attack: product-drive aliases semantically different situations.
    assert naive_product_drive(1.0, 0.4) == naive_product_drive(0.4, 1.0)

    a = resolve_threshold_model(FeedingInput(1.0, 0.4, 0.4))[1]
    b = resolve_threshold_model(FeedingInput(0.4, 1.0, 0.4))[1]
    assert a != b

    # B. Motivation broadens the set of opportunities worth acting on.
    low_m = resolve_threshold_model(FeedingInput(0.8, 0.3, 0.6))[1]
    high_m = resolve_threshold_model(FeedingInput(0.8, 0.9, 0.6))[1]
    assert low_m == 0.0
    assert high_m > 0.0

    # C. Food value remains monotonic when motivation and task strain are fixed.
    c1 = resolve_threshold_model(FeedingInput(0.6, 0.9, 0.4))[1]
    c2 = resolve_threshold_model(FeedingInput(0.8, 0.9, 0.4))[1]
    assert 0.0 <= c1 < c2

    # D. Task strain remains monotonic when value and motivation are fixed.
    d1 = resolve_threshold_model(FeedingInput(0.8, 0.6, 0.2))[1]
    d2 = resolve_threshold_model(FeedingInput(0.8, 0.6, 0.8))[1]
    assert d1 > d2 >= 0.0

    # E. Infeasible is a hard gate, not a large soft cost that can be compensated.
    status, c = resolve_threshold_model(FeedingInput(1.0, 1.0, 1.01))
    assert status == "ResolvedNonResponsive" and c == 0.0

    # F. Unknown remains non-rollable rather than becoming zero.
    status, c = resolve_threshold_model(
        FeedingInput(1.0, 1.0, 0.0, resolved=False)
    )
    assert status == "ResolutionIncomplete" and c is None

    print("Feeding response threshold probe passed: A B C D E F")


if __name__ == "__main__":
    run_probe()

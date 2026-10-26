"""Working probe for Proposal C prey-support -> feeding-mode contribution.

This probe does not freeze production numbers. It demonstrates topology:
- prey support is evidence strength, not a normalized identity probability;
- evidence strength is projected to an interpretation-retention R;
- fish-side response is computed conditionally on a prey interpretation;
- R attenuates that conditional response after projection;
- alternative prey interpretations of one physical lure default to max composition.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Support:
    status: str  # known | unknown | no_match
    value: Optional[float] = None


def recognition_projection(s: float) -> float:
    """Probe-only monotone mapping. Identity here is deliberate simplicity, not a production claim."""
    return max(0.0, min(1.0, s))


def conditional_response(food_value: float, trigger: float, task_cost: float, threshold: float) -> float:
    margin = food_value + trigger - task_cost - threshold
    return max(0.0, min(1.0, margin / 0.38))


def prey_mode_contribution(
    support: Support,
    *,
    food_value: float,
    trigger: float,
    task_cost: float,
    threshold: float,
) -> Optional[float]:
    if support.status == "unknown":
        return None
    if support.status == "no_match":
        return 0.0
    assert support.value is not None
    r = recognition_projection(support.value)
    c_if_recognized = conditional_response(food_value, trigger, task_cost, threshold)
    return r * c_if_recognized


def compose_alternative_prey_modes(*values: Optional[float]) -> Optional[float]:
    if any(v is None for v in values):
        return None
    return max(v for v in values if v is not None)


def main() -> None:
    baitfish = prey_mode_contribution(
        Support("known", 0.90), food_value=0.80, trigger=0.12, task_cost=0.08, threshold=0.45
    )
    crayfish = prey_mode_contribution(
        Support("known", 0.75), food_value=0.55, trigger=0.00, task_cost=0.05, threshold=0.45
    )
    assert baitfish is not None and crayfish is not None
    assert baitfish > crayfish

    # Supports are not probabilities and need not sum to 1.
    assert 0.90 + 0.75 > 1.0

    # Same conditional response, different interpretation evidence -> different mode contribution.
    weak = prey_mode_contribution(
        Support("known", 0.40), food_value=0.80, trigger=0.0, task_cost=0.05, threshold=0.40
    )
    strong = prey_mode_contribution(
        Support("known", 0.90), food_value=0.80, trigger=0.0, task_cost=0.05, threshold=0.40
    )
    assert weak is not None and strong is not None and strong > weak

    # NoMatch is a distinct resolved zero; Unknown remains unresolved.
    assert prey_mode_contribution(
        Support("no_match"), food_value=1.0, trigger=0.15, task_cost=0.0, threshold=0.2
    ) == 0.0
    assert prey_mode_contribution(
        Support("unknown"), food_value=1.0, trigger=0.15, task_cost=0.0, threshold=0.2
    ) is None

    # Alternative readings of one physical feeding opportunity do not sum or union by default.
    composed = compose_alternative_prey_modes(baitfish, crayfish)
    assert composed == max(baitfish, crayfish)
    assert composed <= 1.0

    print("prey-support bridge probe passed")
    print(f"baitfish={baitfish:.3f}, crayfish={crayfish:.3f}, composed={composed:.3f}")


if __name__ == "__main__":
    main()

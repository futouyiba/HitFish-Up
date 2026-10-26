"""Proposal C: State Trigger ownership probe.

Working probe only. Shows that adding StateTriggerValue on the target/state side
is numerically equivalent to subtracting it from a threshold in a simple linear
margin, but differs semantically and in scope once multiple prey interpretations
share one fish-level Motivation state.
"""

from dataclasses import dataclass


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def willingness_threshold(motivation: float) -> float:
    # Working nonlinear example; not production calibration.
    return 0.65 - 0.45 * (motivation ** 1.5)


def response(food_value: float, state_trigger: float, task_cost: float, motivation: float,
             width: float = 0.35) -> float:
    margin = food_value + state_trigger - task_cost - willingness_threshold(motivation)
    return clamp01(margin / width)


def leaked_response(food_value: float, fish_global_trigger: float, task_cost: float,
                    motivation: float, width: float = 0.35) -> float:
    # Deliberately unsafe ownership example: trigger incorrectly lowers a fish-global threshold.
    margin = food_value - task_cost - (willingness_threshold(motivation) - fish_global_trigger)
    return clamp01(margin / width)


if __name__ == "__main__":
    motivation = 0.60
    task_cost = 0.08
    prey = {
        "baitfish_escape_valid": (0.55, 0.12),
        "crayfish_no_trigger": (0.55, 0.00),
    }

    print("prey-local target/state ownership")
    for name, (fv, trig) in prey.items():
        print(name, f"{response(fv, trig, task_cost, motivation):.3f}")

    print("\nunsafe fish-global threshold ownership")
    global_trigger = 0.12
    for name, (fv, _trig) in prey.items():
        print(name, f"{leaked_response(fv, global_trigger, task_cost, motivation):.3f}")

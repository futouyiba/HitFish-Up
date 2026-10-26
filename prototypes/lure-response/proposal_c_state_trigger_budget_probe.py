"""Working probe: constrain StateTriggerValue budget against FoodValue tiers.

Not production calibration.
"""

FOOD = {
    "Preferred": 1.00,
    "Good": 0.80,
    "Marginal": 0.55,
    "Poor": 0.35,
}


def response(food_value: float, motivation: float, task_strain: float, trigger: float) -> float:
    task_cost = 0.33 * task_strain**4
    threshold = 0.72 - 0.45 * motivation
    margin = food_value + trigger - task_cost - threshold
    return max(0.0, min(1.0, margin / 0.38))


def table(trigger: float):
    cases = [(0.25, 0.55), (0.60, 0.55), (0.90, 0.55)]
    return {
        name: [round(response(v, m, s, trigger), 3) for m, s in cases]
        for name, v in FOOD.items()
    }


if __name__ == "__main__":
    for trigger in (0.00, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30):
        print(f"trigger={trigger:.2f}")
        for relation, values in table(trigger).items():
            print(f"  {relation:9s}: poor_bite={values[0]:.3f} normal={values[1]:.3f} good_bite={values[2]:.3f}")

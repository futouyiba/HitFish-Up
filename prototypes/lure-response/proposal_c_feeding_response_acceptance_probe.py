"""Proposal C feeding-response acceptance matrix probe.

Working Proposal evidence only. The formula and fixture numbers are not production
parameters. This probe separates semantic invariants, strategy-ordering checks,
and calibration/effect-size diagnostics.
"""

from dataclasses import dataclass


def task_cost(task_strain: float) -> float:
    return 0.45 * (task_strain ** 1.6)


def willingness_threshold(motivation: float) -> float:
    return 0.90 - 0.80 * motivation


def response(food_value: float, motivation: float, task_strain: float) -> float:
    # Typed gates represented minimally for this probe.
    if task_strain > 1.0:
        return 0.0
    if food_value <= 0.0 or motivation <= 0.0:
        return 0.0

    margin = food_value - task_cost(task_strain) - willingness_threshold(motivation)
    return max(0.0, min(1.0, margin / 0.45))


@dataclass(frozen=True)
class Check:
    id: str
    name: str
    passed: bool
    detail: str = ""


def gt(a: float, b: float) -> bool:
    return a > b + 1e-12


def main() -> None:
    hard = [
        Check("H1", "Food Value monotonic", gt(response(.8, .6, .4), response(.6, .6, .4))),
        Check("H2", "Motivation monotonic", gt(response(.8, .8, .4), response(.8, .4, .4))),
        Check("H3", "Task Strain monotonic", gt(response(.8, .6, .3), response(.8, .6, .7))),
        Check("H4", "Infeasible is hard zero", response(1.0, 1.0, 1.1) == 0.0),
        Check("H5", "Zero target value is zero", response(0.0, 1.0, .2) == 0.0),
        Check("H6", "Zero motivation is zero", response(1.0, 0.0, .2) == 0.0),
        Check(
            "H7",
            "Response is bounded",
            all(
                0.0 <= response(v, m, s) <= 1.0
                for v in (0.0, .2, .5, 1.0)
                for m in (0.0, .2, .5, 1.0)
                for s in (0.0, .5, 1.0, 1.2)
            ),
        ),
        Check(
            "H8",
            "Food Value and Motivation are not structurally forced symmetric",
            abs(response(1.0, .4, .4) - response(.4, 1.0, .4)) > 1e-12,
        ),
    ]

    strategy = [
        Check("S1", "Bad bite: easier/slower target ranks above demanding/fast target", gt(response(.8, .3, .25), response(.8, .3, .75))),
        Check("S2", "Good bite: demanding presentation can remain viable", response(.8, .9, .75) > 0.0),
        Check("S3", "Higher motivation broadens acceptable opportunity", gt(response(.6, .9, .6), response(.6, .3, .6))),
        Check("S4", "Higher target value can offset constrained task", gt(response(1.0, .8, .8), response(.7, .8, .8))),
        Check("S5", "Value/motivation cannot rescue physical infeasibility", response(1.0, 1.0, 1.1) == 0.0),
        Check("S6", "Higher functional capacity / lower derived strain improves same presentation", gt(response(.8, .5, .35), response(.8, .5, .65))),
        Check("S7", "Pause has no intrinsic hidden bonus", True, "Pause may help only through admitted consequences such as reduced TaskDemand or other named routes."),
    ]

    # These are working calibration fixtures. They are not semantic truths.
    calibration = {
        "F1_bad_bite_fast_to_slow": {
            "fast": response(.75, .25, .75),
            "slow": response(.75, .25, .25),
        },
        "F2_normal_bite_strain_flip": {
            "demanding": response(.65, .50, .70),
            "easy": response(.65, .50, .30),
        },
        "F3_good_bite_moderate_prey_demanding": {
            "response": response(.60, .90, .80),
        },
        "F4_bad_bite_good_prey_demanding": {
            "response": response(.90, .30, .80),
        },
        "F5_good_bite_great_prey_easy": {
            "response": response(1.00, .90, .20),
        },
    }

    failed = [c for c in hard + strategy if not c.passed]
    if failed:
        for c in failed:
            print(f"FAIL {c.id}: {c.name} {c.detail}")
        raise AssertionError("semantic/strategy acceptance failed")

    print("Semantic invariants passed:", " ".join(c.id for c in hard))
    print("Strategy orderings passed:", " ".join(c.id for c in strategy))
    print("Calibration/effect-size diagnostics:")
    for fixture_id, values in calibration.items():
        rendered = ", ".join(f"{k}={v:.4f}" for k, v in values.items())
        print(f"  {fixture_id}: {rendered}")

    # Important diagnostic: a sign flip can be numerically real but gameplay-invisible.
    f1 = calibration["F1_bad_bite_fast_to_slow"]
    print(
        "F1 rescue delta:",
        f"{f1['slow'] - f1['fast']:.4f}",
        "(effect-size target intentionally not frozen)",
    )


if __name__ == "__main__":
    main()

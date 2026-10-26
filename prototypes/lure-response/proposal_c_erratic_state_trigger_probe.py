import math


def state_trigger_value(erratic_intensity: float, trigger_cap: float = 0.45, trigger_gain: float = 3.0) -> float:
    """Working saturating positive valuation for prey-conditioned escape/erratic state.

    Not a production curve. This probe only tests whether a monotone saturating trigger
    plus a convex handling cost can create a middle optimum without a hand-authored
    bell-shaped 'erratic bonus'.
    """
    e = max(0.0, min(1.0, erratic_intensity))
    return trigger_cap * (1.0 - math.exp(-trigger_gain * e))


def handling_cost(erratic_intensity: float, cost_scale: float = 0.5, exponent: float = 3.0) -> float:
    e = max(0.0, min(1.0, erratic_intensity))
    return cost_scale * (e ** exponent)


def net_margin_delta(erratic_intensity: float) -> float:
    return state_trigger_value(erratic_intensity) - handling_cost(erratic_intensity)


def main() -> None:
    print("e\ttrigger\thandling_cost\tnet_delta")
    for i in range(11):
        e = i / 10.0
        print(f"{e:.1f}\t{state_trigger_value(e):.3f}\t{handling_cost(e):.3f}\t{net_margin_delta(e):.3f}")

    print("\nCanonical fixtures")
    for name, e in {
        "mechanical_straight": 0.00,
        "moderate_darting": 0.45,
        "extreme_erratic": 0.95,
    }.items():
        print(name, {
            "erratic_intensity": e,
            "trigger": round(state_trigger_value(e), 3),
            "handling_cost": round(handling_cost(e), 3),
            "net_delta": round(net_margin_delta(e), 3),
        })


if __name__ == "__main__":
    main()

"""Map Proposal C captureRetention into current Candidate/TrueRoll metrics.

Working reference simulator only. Fixture numbers are deliberately normalized and
are not production calibration. Uses Current TrueRoll semantic form:
    p_i = W_i / max(N, F), F = sum(W)
with lambda opportunities per second.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Fixture:
    name: str
    target_supply: float
    background_mass: float
    N: float
    opportunity_rate: float = 1.0
    bycatch_handling_seconds: float = 5.0


def metrics(fx: Fixture, capture_retention: float) -> dict[str, float]:
    wt = fx.target_supply * capture_retention
    wb = fx.background_mass
    F = wt + wb
    denom = max(fx.N, F)

    p_target = wt / denom if denom > 0 else 0.0
    p_background = wb / denom if denom > 0 else 0.0
    p_any = F / denom if denom > 0 else 0.0
    purity = wt / F if F > 0 else 0.0

    active_roll_time = float("inf") if p_target <= 0 else 1.0 / (fx.opportunity_rate * p_target)

    # Simple renewal fixture: each opportunity costs 1/lambda active seconds.
    # A bycatch commit adds handling/reset delay before the next opportunity.
    # This is diagnostic only, not a production Catch Cycle model.
    if p_target <= 0:
        wall_clock = float("inf")
    else:
        active_step = 1.0 / fx.opportunity_rate
        wall_clock = (active_step + p_background * fx.bycatch_handling_seconds) / p_target

    return {
        "C": capture_retention,
        "W_target": wt,
        "F": F,
        "p_target": p_target,
        "p_any": p_any,
        "purity": purity,
        "target_active_roll_s": active_roll_time,
        "target_wall_clock_s": wall_clock,
    }


def show(fx: Fixture) -> None:
    print(f"\n[{fx.name}] target_supply={fx.target_supply}, background={fx.background_mass}, N={fx.N}")
    print("C    Wt    F     p_target purity p_any  active_s wall_s")
    for c in (0.10, 0.20, 0.40, 0.60, 0.80, 1.00):
        m = metrics(fx, c)
        print(
            f"{m['C']:.2f} "
            f"{m['W_target']:5.1f} "
            f"{m['F']:5.1f} "
            f"{m['p_target']:.3f}   "
            f"{m['purity']:.3f}  "
            f"{m['p_any']:.3f} "
            f"{m['target_active_roll_s']:8.2f} "
            f"{m['target_wall_clock_s']:7.2f}"
        )


def main() -> None:
    # F < N throughout: target C changes absolute target rate, purity and total
    # throughput, while background absolute probability stays fixed.
    show(Fixture("underfilled", target_supply=40.0, background_mass=50.0, N=100.0))

    # Crosses F=N as C increases: after saturation, candidates compete for fixed
    # total spawn throughput and target improvement becomes zero-sum composition.
    show(Fixture("crosses-saturation", target_supply=40.0, background_mass=80.0, N=100.0))


if __name__ == "__main__":
    main()

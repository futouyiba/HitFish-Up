from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import sqrt


# Canonical calibration working basket from Candidate Weight Calibration Current v8:
# T2 target reference response = 1.0, target active-roll anchor = 30 s,
# any-fish anchor = 12 s, purity = 40% under the normalized λ=1/s fixture.
# A convenient equivalent mass representation is target=40, background=60, N=1200.
TARGET_NATIVE_AT_C1 = 40.0
BACKGROUND_MASS = 60.0
N = 1200.0
LAMBDA = 1.0
REFERENCE_TARGET_TIME = 30.0


@dataclass(frozen=True)
class Story:
    name: str
    target_time_s: float
    motivation: float
    task_strain: float
    food_value: float = 1.0


STORIES = [
    Story("poor_bite_fast", 150.0, 0.30, 0.65),
    Story("poor_bite_slow", 60.0, 0.30, 0.25),
    Story("normal_bite_fast", 45.0, 0.60, 0.65),
    Story("normal_reference_good", 30.0, 0.60, 0.25),
    Story("good_bite_fast", 35.0, 0.90, 0.65),
    Story("weak_capacity_fast", 120.0, 0.60, 0.90),
    Story("weak_capacity_slow", 40.0, 0.60, 0.50),
]


def backsolve_c_from_target_time(target_time_s: float) -> float:
    # In this underfilled reference basket:
    # T_target = N / (λ * W_target) = 1200 / (40*C) = 30/C.
    return REFERENCE_TARGET_TIME / target_time_s


def candidate_metrics(c: float) -> dict[str, float]:
    w_target = TARGET_NATIVE_AT_C1 * c
    total = BACKGROUND_MASS + w_target
    denom = max(N, total)
    p_target = w_target / denom
    purity = w_target / total if total > 0 else 0.0
    p_any = total / denom
    return {
        "c": c,
        "w_target": w_target,
        "p_target": p_target,
        "purity": purity,
        "p_any": p_any,
        "target_active_roll_time": 1.0 / (LAMBDA * p_target) if p_target > 0 else float("inf"),
        "any_fish_active_roll_time": 1.0 / (LAMBDA * p_any) if p_any > 0 else float("inf"),
    }


def assert_story_consistency(stories: list[Story]) -> None:
    # If FoodValue and Motivation are the same, lower TaskStrain must not be assigned
    # a lower target C. Otherwise the experience targets themselves violate the
    # current monotonic TaskStrain invariant before any formula is fitted.
    rows = [(s, backsolve_c_from_target_time(s.target_time_s)) for s in stories]
    for a, ca in rows:
        for b, cb in rows:
            if a.name >= b.name:
                continue
            if a.food_value == b.food_value and a.motivation == b.motivation:
                if a.task_strain < b.task_strain and ca + 1e-9 < cb:
                    raise AssertionError(
                        f"experience targets conflict with TaskStrain monotonicity: {a.name} vs {b.name}"
                    )
                if b.task_strain < a.task_strain and cb + 1e-9 < ca:
                    raise AssertionError(
                        f"experience targets conflict with TaskStrain monotonicity: {b.name} vs {a.name}"
                    )


def response_model(params: tuple[float, float, float, float, float, float], story: Story) -> float:
    # Working structure only:
    # TaskCost = k * S^p
    # Threshold = b - c*M
    # x = clamp((V - TaskCost - Threshold) / r, 0, 1)
    # C = x^gamma
    k, p, b, c, r, gamma = params
    margin = story.food_value - k * story.task_strain**p - (b - c * story.motivation)
    x = min(1.0, max(0.0, margin / r))
    return x**gamma


def coarse_fit(stories: list[Story]) -> tuple[float, tuple[float, ...], list[tuple[str, float, float]]]:
    target = {s.name: backsolve_c_from_target_time(s.target_time_s) for s in stories}
    best = None
    for params in product(
        [0.35, 0.40, 0.45, 0.50, 0.55],  # task-cost scale k
        [1.0, 1.2, 1.4, 1.6],              # task-cost exponent p
        [0.65, 0.75, 0.85, 0.95],          # threshold intercept b
        [0.45, 0.55, 0.65, 0.75],          # motivation threshold relief c
        [0.40, 0.50, 0.60, 0.70],          # response width r
        [0.8, 1.0, 1.2, 1.4],              # response gamma
    ):
        residuals = [response_model(params, s) - target[s.name] for s in stories]
        rmse = sqrt(sum(e * e for e in residuals) / len(residuals))
        if best is None or rmse < best[0]:
            best = (rmse, params)

    assert best is not None
    rmse, params = best
    detail = [(s.name, response_model(params, s), target[s.name]) for s in stories]
    return rmse, params, detail


def main() -> None:
    assert_story_consistency(STORIES)

    print("Experience targets -> backsolved C")
    for story in STORIES:
        c = backsolve_c_from_target_time(story.target_time_s)
        m = candidate_metrics(c)
        print(
            f"{story.name:26s} T={story.target_time_s:6.1f}s  C={c:6.3f}  "
            f"purity={m['purity']:.3f}  anyT={m['any_fish_active_roll_time']:.2f}s"
        )

    rmse, params, detail = coarse_fit(STORIES)
    print("\nBest coarse threshold fit")
    print("params(k,p,b,c,r,gamma)=", params)
    print("RMSE=", round(rmse, 4))
    for name, predicted, target in detail:
        print(f"{name:26s} predicted={predicted:6.3f} target={target:6.3f} residual={predicted-target:+.3f}")

    # This is deliberately not an acceptance threshold for production.
    # It only records whether the current simple surface can approximate the
    # experience budget without changing the budget to flatter the formula.
    print("\nExperience backsolve probe completed")


if __name__ == "__main__":
    main()

from __future__ import annotations

import math

# Working experience-budget cases. These are calibration fixtures, not production truth.
CASES = [
    ("bad_fast", -0.0482421875, (0.15, 0.25)),
    ("bad_slow", 0.0611328125, (0.50, 0.65)),
    ("normal_fast", 0.1575228125, (0.75, 0.85)),
    ("normal_ref", 0.4147478125, (0.95, 1.00)),
    ("good_fast", 0.2925228125, (0.90, 1.00)),
    ("weak_fast", 0.0372978125, (0.25, 0.35)),
    ("weak_slow", 0.1981250000, (0.85, 0.95)),
]


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def linear_projection(margin: float, low: float = -0.10, high: float = 0.23) -> float:
    return clamp01((margin - low) / (high - low))


def sigmoid_projection(margin: float, midpoint: float = 0.065, scale: float = 0.065) -> float:
    return 1.0 / (1.0 + math.exp(-(margin - midpoint) / scale))


def bucket_projection(margin: float) -> float:
    # Illustrative only: discrete DecisionStrength -> numeric projection.
    if margin < -0.08:
        return 0.0
    if margin < 0.02:
        return 0.20
    if margin < 0.10:
        return 0.50
    if margin < 0.22:
        return 0.80
    return 1.0


def center(bounds: tuple[float, float]) -> float:
    return sum(bounds) / 2.0


def rmse(projector) -> float:
    err = 0.0
    for _, margin, bounds in CASES:
        err += (projector(margin) - center(bounds)) ** 2
    return math.sqrt(err / len(CASES))


def main() -> None:
    assert linear_projection(-1.0) == 0.0
    assert linear_projection(1.0) == 1.0
    assert sigmoid_projection(-1.0) > 0.0  # important semantic difference
    assert sigmoid_projection(1.0) < 1.0

    print("case\tmargin\ttarget\tlinear\tsigmoid\tbucket")
    for name, margin, bounds in CASES:
        print(
            f"{name}\t{margin:.3f}\t{bounds[0]:.2f}-{bounds[1]:.2f}\t"
            f"{linear_projection(margin):.3f}\t"
            f"{sigmoid_projection(margin):.3f}\t"
            f"{bucket_projection(margin):.3f}"
        )

    print(f"linear_rmse={rmse(linear_projection):.4f}")
    print(f"sigmoid_rmse={rmse(sigmoid_projection):.4f}")
    print(f"bucket_rmse={rmse(bucket_projection):.4f}")

    # Structural checks: all projections are monotone in margin.
    xs = [i / 100.0 for i in range(-100, 101)]
    for projector in (linear_projection, sigmoid_projection, bucket_projection):
        ys = [projector(x) for x in xs]
        assert all(b >= a for a, b in zip(ys, ys[1:]))

    print("Response projection probe passed")


if __name__ == "__main__":
    main()

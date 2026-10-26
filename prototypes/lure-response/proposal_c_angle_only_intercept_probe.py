import math
import numpy as np


def closing_utilization(theta: float, q: float) -> float:
    """Working reduced intercept model.

    theta: angle between lure motion and the radial direction from latent fish to lure.
           theta=0 means lure moving directly away from fish.
           theta=pi means lure moving toward fish.
    q: lure speed / fish intercept capacity.
    """
    return max(0.0, q * math.cos(theta))


def task_cost(u: float, k: float = 0.35, p: float = 4.0) -> float:
    if u > 1.0:
        return math.inf
    return k * (u ** p)


def response_from_closing(
    u: float,
    base_margin: float = 0.32,
    projection_width: float = 0.33,
) -> float:
    if u > 1.0:
        return 0.0
    margin = base_margin - task_cost(u)
    return max(0.0, min(1.0, margin / projection_width))


def expected_response(q: float, samples: int = 3600):
    thetas = np.linspace(-math.pi, math.pi, samples, endpoint=False)
    us = np.array([closing_utilization(float(theta), q) for theta in thetas])
    cs = np.array([response_from_closing(float(u)) for u in us])
    feasible = float(np.mean(us <= 1.0))
    return float(np.mean(cs)), feasible, float(np.mean(us))


def main():
    print("q=lure_speed/intercept_capacity, E[C], feasible_angle_share, E[u_close]")
    for q in [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
        c, feasible, u = expected_response(q)
        print(f"{q:>4.2f}  {c:>6.3f}  {feasible:>6.3f}  {u:>6.3f}")

    # Semantic assertions.
    assert closing_utilization(0.0, 0.8) == 0.8
    assert abs(closing_utilization(math.pi / 2, 0.8)) < 1e-12
    assert closing_utilization(math.pi, 0.8) == 0.0

    # Slower presentation should not reduce angle-averaged response.
    c_slow = expected_response(0.5)[0]
    c_fast = expected_response(1.25)[0]
    assert c_slow > c_fast

    # q > 1 only makes some away-facing angles infeasible; it does not mean
    # every latent angle is infeasible.
    assert 0.0 < expected_response(1.25)[1] < 1.0

    print("angle-only intercept probe passed")


if __name__ == "__main__":
    main()

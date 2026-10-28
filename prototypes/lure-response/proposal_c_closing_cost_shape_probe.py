import math


def u_close(q: float, theta: float) -> float:
    return max(0.0, q * math.cos(theta))


def closing_cost(u: float, k_close: float = 1.0, power: int = 2) -> float:
    # Soft Closing: `u_close >= 1 -> hard infeasible` is withdrawn, so cost
    # keeps its power-law shape past the structural speed scale. A margin clamp
    # may still drive the response to zero; that is not an angle-local gate.
    return k_close * (u ** power)


def angle_response(q: float, theta: float, k_close: float = 1.0, power: int = 2) -> float:
    # Probe-only response: margin = 1 - cost, clipped.
    return max(0.0, min(1.0, 1.0 - closing_cost(u_close(q, theta), k_close, power)))


def angle_average_response(
    q: float, power: int, k_close: float = 1.0, samples: int = 7200
) -> float:
    total = 0.0
    for i in range(samples):
        theta = -math.pi + (2 * math.pi) * (i + 0.5) / samples
        total += angle_response(q, theta, k_close, power)
    return total / samples


def radial_overload_share(q: float, samples: int = 7200) -> float:
    """Diagnostic only: share of bearings above the structural speed scale."""
    overloaded = 0
    for i in range(samples):
        theta = -math.pi + (2 * math.pi) * (i + 0.5) / samples
        if u_close(q, theta) >= 1.0:
            overloaded += 1
    return overloaded / samples


if __name__ == "__main__":
    qs = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    for q in qs:
        vals = {p: angle_average_response(q, p) for p in (1, 2, 4)}
        print(q, radial_overload_share(q), vals)

    # The old `u_close >= 1 -> hard infeasible` rule is withdrawn. Cost stays
    # finite and keeps its power-law shape above the structural speed scale.
    assert closing_cost(1.0, 1.0, 2) == 1.0
    assert closing_cost(1.5, 1.0, 2) == 2.25
    assert closing_cost(2.0, 1.0, 2) == 4.0

    # With a sub-unit K_close fixture, a bearing past u_close == 1 still gets a
    # nonzero response. The withdrawn hard gate would have forced it to zero.
    # The 0.25 is a shape fixture here, not a production anchor.
    assert abs(angle_response(1.5, 0.0, k_close=0.25, power=2) - 0.4375) < 1e-12
    assert angle_response(1.5, 0.0, k_close=0.25, power=2) > 0.0

    # Whole-mode response is not zero merely because q > 1.
    assert angle_average_response(1.5, 2) > 0.0

    # Convex forms are more permissive at low utilization than linear.
    assert angle_average_response(0.5, 2) > angle_average_response(0.5, 1)
    assert angle_average_response(0.5, 4) > angle_average_response(0.5, 2)

    # A stronger retrieve lowers the average response. The overload share is a
    # diagnostic, not a feasibility gate.
    assert angle_average_response(2.0, 2) < angle_average_response(1.5, 2)
    assert radial_overload_share(2.0) > radial_overload_share(1.5) > 0.0

    # Higher powers buy limited additional separation in the q > 1 regime,
    # entirely through the soft cost shape.
    d24 = abs(angle_average_response(1.5, 2) - angle_average_response(1.5, 4))
    assert d24 < 0.1

    print("PASS")

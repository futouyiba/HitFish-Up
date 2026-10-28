import math


def u_close(q: float, theta: float) -> float:
    return max(0.0, q * math.cos(theta))


def closing_cost(u: float, k_close: float = 1.0, power: int = 2):
    if u >= 1.0:
        return None  # angle-local hard infeasible
    return k_close * (u ** power)


def angle_average_response(q: float, power: int, samples: int = 7200) -> float:
    # Probe-only response: margin = 1 - cost, clipped; infeasible angle -> 0.
    total = 0.0
    for i in range(samples):
        theta = -math.pi + (2 * math.pi) * (i + 0.5) / samples
        u = u_close(q, theta)
        cost = closing_cost(u, 1.0, power)
        c = 0.0 if cost is None else max(0.0, min(1.0, 1.0 - cost))
        total += c
    return total / samples


def feasible_share(q: float, samples: int = 7200) -> float:
    ok = 0
    for i in range(samples):
        theta = -math.pi + (2 * math.pi) * (i + 0.5) / samples
        if u_close(q, theta) < 1.0:
            ok += 1
    return ok / samples


if __name__ == "__main__":
    qs = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    for q in qs:
        vals = {p: angle_average_response(q, p) for p in (1, 2, 4)}
        fs = feasible_share(q)
        print(q, fs, vals)

    # q > 1 must not imply whole-mode zero.
    assert feasible_share(1.5) > 0.7
    assert angle_average_response(1.5, 2) > 0.0

    # Convex forms are more permissive at low utilization than linear.
    assert angle_average_response(0.5, 2) > angle_average_response(0.5, 1)
    assert angle_average_response(0.5, 4) > angle_average_response(0.5, 2)

    # With angle-local hard zero already present, higher powers buy limited
    # additional separation in the q > 1 regime compared with adding a new
    # semantic boundary.
    d24 = abs(angle_average_response(1.5, 2) - angle_average_response(1.5, 4))
    assert d24 < 0.1

    print("PASS")

"""Proposal C probe: soft closing cost shape without a latent bearing.

2026-10-30 direction: the first version assumes the fish is chasing the lure,
so closing cost is K_close * q^2 * activity with no angle average.

What this probe can prove:
- cost stays finite above the structural speed scale (the old q >= 1 hard gate
  is withdrawn);
- response falls monotonically as the speed ratio rises;
- cost is linear in the activity multiplier;
- higher convex powers buy limited extra separation at low utilisation.

What it cannot prove: production K_close, real pursuit geometry.

Run: python3 -I prototypes/lure-response/proposal_c_closing_cost_shape_probe.py
"""


def closing_cost(q: float, k_close: float = 1.0, power: int = 2, activity: float = 1.0) -> float:
    return k_close * max(0.0, q) ** power * activity


def response(q: float, k_close: float = 1.0, power: int = 2, activity: float = 1.0) -> float:
    """Shape fixture: margin = 1 - cost, clipped to [0, 1]."""
    return max(0.0, min(1.0, 1.0 - closing_cost(q, k_close, power, activity)))


if __name__ == "__main__":
    qs = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    for q in qs:
        print(q, {p: round(response(q, 1.0, p), 4) for p in (1, 2, 4)})

    # The old `u_close >= 1 -> hard infeasible` rule is withdrawn. Cost stays
    # finite and keeps its power-law shape past the structural speed scale; a
    # margin clamp may still drive response to zero, but that is not a gate.
    assert closing_cost(1.0, 1.0, 2) == 1.0
    assert closing_cost(1.5, 1.0, 2) == 2.25
    assert closing_cost(2.0, 1.0, 2) == 4.0

    # Response decreases monotonically with the speed ratio.
    for power in (1, 2, 4):
        values = [response(q, 0.76, power) for q in qs]
        assert all(a >= b for a, b in zip(values, values[1:]))

    # Convex forms are more permissive at low utilisation than linear.
    assert response(0.5, 1.0, 2) > response(0.5, 1.0, 1)
    assert response(0.5, 1.0, 4) > response(0.5, 1.0, 2)

    # With a sub-unit K_close fixture, q > 1 still yields non-zero response.
    assert response(1.5, 0.25, 2) > 0.0
    assert response(1.5, 0.25, 2) == 1.0 - 0.25 * 2.25

    # Cost scales linearly with the activity multiplier.
    assert closing_cost(0.8, 0.76, 2, 2.0) == 2.0 * closing_cost(0.8, 0.76, 2, 1.0)

    print("PASS")

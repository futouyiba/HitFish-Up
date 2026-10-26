"""Proposal C latent bearing prior probe.

Candidate regression helper only. Not production calibration.
"""

from __future__ import annotations

import math


def expected_u2_isotropic_2d(q: float) -> float:
    """For q <= 1, E[max(0, q cos(theta))^2], theta~U(0,2pi)."""
    if not 0 <= q <= 1:
        raise ValueError("closed-form helper here is for 0 <= q <= 1")
    return q * q / 4.0


def expected_u2_isotropic_3d(q: float) -> float:
    """For q <= 1, E[max(0, q mu)^2], mu~U(-1,1)."""
    if not 0 <= q <= 1:
        raise ValueError("closed-form helper here is for 0 <= q <= 1")
    return q * q / 6.0


def hard_fraction_isotropic_2d(q: float) -> float:
    if q <= 1:
        return 0.0
    return math.acos(1.0 / q) / math.pi


def hard_fraction_isotropic_3d(q: float) -> float:
    if q <= 1:
        return 0.0
    return (1.0 - 1.0 / q) / 2.0


def main() -> None:
    for q in (0.25, 0.5, 0.75, 1.0):
        e2 = expected_u2_isotropic_2d(q)
        e3 = expected_u2_isotropic_3d(q)
        ratio = e2 / e3 if e3 else float("nan")
        print(f"q={q:.2f} E[u^2]_2d={e2:.6f} E[u^2]_3d={e3:.6f} ratio={ratio:.3f}")
        assert math.isclose(ratio, 1.5, rel_tol=1e-12)

    for q in (1.1, 1.5, 2.0, 3.0):
        h2 = hard_fraction_isotropic_2d(q)
        h3 = hard_fraction_isotropic_3d(q)
        print(f"q={q:.2f} hard_2d={h2:.6f} hard_3d={h3:.6f}")
        assert 0.0 < h2 < 0.5
        assert 0.0 < h3 < 0.5

    # The dimensionality choice materially changes the Closing statistics.
    assert not math.isclose(
        expected_u2_isotropic_2d(0.8), expected_u2_isotropic_3d(0.8)
    )


if __name__ == "__main__":
    main()

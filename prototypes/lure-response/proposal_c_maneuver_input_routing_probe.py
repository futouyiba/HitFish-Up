"""Proposal C maneuver-input routing probe.

Purpose
-------
Demonstrate which ActualPresentation motion features are clean inputs to the
current geometry-free Maneuver proxy.

This is a design probe, not production code.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    name: str
    speed_mps: float
    curvature_per_m: float

    @property
    def omega_traj_rad_s(self) -> float:
        # For a smooth 3-D trajectory, heading angular speed is v * curvature.
        return self.speed_mps * self.curvature_per_m


CASES = [
    Case("straight_slow", 0.4, 0.0),
    Case("straight_fast", 1.0, 0.0),
    Case("gentle_turn_slow", 0.4, 0.5),
    Case("gentle_turn_fast", 1.0, 0.5),
    Case("sharp_turn_slow", 0.4, 2.0),
    Case("sharp_turn_fast", 1.0, 2.0),
]


def main() -> None:
    expected = {
        "straight_slow": 0.0,
        "straight_fast": 0.0,
        "gentle_turn_slow": 0.2,
        "gentle_turn_fast": 0.5,
        "sharp_turn_slow": 0.8,
        "sharp_turn_fast": 2.0,
    }

    for case in CASES:
        actual = case.omega_traj_rad_s
        target = expected[case.name]
        assert abs(actual - target) < 1e-9, (case.name, actual, target)
        print(f"{case.name:24s} omega_traj={actual:.3f} rad/s")

    # Guardrails: raw straight-line speed alone is not Maneuver demand.
    assert CASES[0].omega_traj_rad_s == CASES[1].omega_traj_rad_s == 0.0
    # Same curvature at higher speed implies faster trajectory-direction change.
    assert CASES[3].omega_traj_rad_s > CASES[2].omega_traj_rad_s
    # Same speed with tighter curvature implies faster trajectory-direction change.
    assert CASES[5].omega_traj_rad_s > CASES[3].omega_traj_rad_s

    print("Maneuver input-routing probe passed")


if __name__ == "__main__":
    main()

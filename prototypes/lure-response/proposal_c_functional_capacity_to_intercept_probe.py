"""Topology probe for FunctionalCapacity -> EffectiveInterceptCapacity.

Probe only. Values are illustrative and not production calibration.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    name: str
    baseline: float
    retention: float
    lure_speed: float


def effective_capacity(baseline: float, retention: float) -> float:
    return baseline * retention


def q(case: Case) -> float:
    cap = effective_capacity(case.baseline, case.retention)
    return float("inf") if cap <= 0 else case.lure_speed / cap


def main() -> None:
    cases = [
        Case("normal", baseline=2.0, retention=1.0, lure_speed=1.0),
        Case("moderate impairment", baseline=2.0, retention=0.7, lure_speed=1.0),
        Case("strong impairment", baseline=2.0, retention=0.4, lure_speed=1.0),
        Case("zero capacity", baseline=2.0, retention=0.0, lure_speed=1.0),
    ]

    for c in cases:
        print(
            c.name,
            "effective_capacity=", round(effective_capacity(c.baseline, c.retention), 3),
            "q=", round(q(c), 3) if q(c) != float("inf") else "inf",
        )

    # Invariants of the proposed scale semantics.
    assert effective_capacity(2.0, 1.0) == 2.0
    assert effective_capacity(2.0, 0.5) == 1.0
    assert effective_capacity(2.0, 0.0) == 0.0
    assert q(cases[0]) < q(cases[1]) < q(cases[2]) < q(cases[3])


if __name__ == "__main__":
    main()

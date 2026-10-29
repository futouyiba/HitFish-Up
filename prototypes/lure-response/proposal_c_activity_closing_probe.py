"""Proposal C probe: Activity affects soft Closing cost, not speed capacity."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    name: str
    lure_speed: float
    intercept_speed_limit: float
    cos_theta: float
    activity: float


K_CLOSE = 0.30
K_ACTIVITY = 1.00


def evaluate(case: Case):
    q = case.lure_speed / case.intercept_speed_limit
    u_close = max(0.0, q * case.cos_theta)
    activity_multiplier = 1.0 + K_ACTIVITY * (1.0 - case.activity)
    closing_cost = K_CLOSE * (u_close ** 2) * activity_multiplier
    return {
        "name": case.name,
        "u_close": u_close,
        "high_burden": u_close >= 1.0,
        "closing_cost": closing_cost,
    }


CASES = [
    Case("fast-away high activity", 0.8, 1.0, 1.0, 1.0),
    Case("fast-away low activity", 0.8, 1.0, 1.0, 0.2),
    Case("pause high activity", 0.0, 1.0, 1.0, 1.0),
    Case("pause low activity", 0.0, 1.0, 1.0, 0.2),
    Case("toward fish low activity", 0.8, 1.0, -1.0, 0.2),
    Case("over-limit high activity", 1.2, 1.0, 1.0, 1.0),
    Case("over-limit low activity", 1.2, 1.0, 1.0, 0.2),
]


if __name__ == "__main__":
    results = [evaluate(c) for c in CASES]
    for r in results:
        print(r)

    by_name = {r["name"]: r for r in results}

    assert by_name["fast-away low activity"]["closing_cost"] > by_name["fast-away high activity"]["closing_cost"]
    assert by_name["pause high activity"]["closing_cost"] == 0.0
    assert by_name["pause low activity"]["closing_cost"] == 0.0
    assert by_name["toward fish low activity"]["closing_cost"] == 0.0
    assert by_name["over-limit high activity"]["high_burden"] is True
    assert by_name["over-limit low activity"]["high_burden"] is True
    assert by_name["over-limit low activity"]["closing_cost"] > by_name["over-limit high activity"]["closing_cost"]

    print("PASS: Activity changes soft pursuit cost only; u_close >= 1 is not a hard zero.")

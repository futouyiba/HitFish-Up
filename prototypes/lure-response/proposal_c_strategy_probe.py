"""Proposal C working probe: three strategy orderings.

Not production calibration. Numbers are Working seeds from the design package:
  threshold(M), M0=0 / M1=0.40, K_close=0.19 (no-theta scale), TriggerBudget=0.10,
  K_wary=1.0 (probe).

2026-10-30 direction: no latent bearing. First version assumes the fish is
chasing the lure, so closing cost is K_close * q^2 * activity with no angle
average. Results differ from the earlier per-bearing tables.

Run: python3 -I prototypes/lure-response/proposal_c_strategy_probe.py
"""

from __future__ import annotations

M0 = 0.0
M1 = 0.40
K_CLOSE = 0.19  # no-theta rescale: was 0.76 under bearing averaging (x 1/4)
TRIGGER_BUDGET = 0.10
K_WARY = 1.0


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def threshold(motivation: float) -> float:
    base = 0.60 - 0.40 * motivation
    if motivation > 0.80:
        base -= 0.50 * (motivation - 0.80)
    return base


def closing_cost(q: float, activity_mult: float) -> float:
    return K_CLOSE * q * q * activity_mult


def response(food: float, trigger: float, q: float, activity_mult: float,
             risk: float, motivation: float) -> float:
    margin = food + trigger - closing_cost(q, activity_mult) - risk - threshold(motivation)
    return clamp01((margin - M0) / (M1 - M0))


def case_a() -> None:
    print("== Case A: fast search vs slow finesse ==")
    food, trigger, risk, motivation = 0.70, 0.0, 0.0, 0.50
    print("activity\tq=0.45(slow)\tq=0.90(fast)")
    rows = {}
    for activity in (0.8, 1.0, 1.3, 1.6):
        slow = response(food, trigger, 0.45, activity, risk, motivation)
        fast = response(food, trigger, 0.90, activity, risk, motivation)
        rows[activity] = (slow, fast)
        print(f"{activity:.2f}\t\t{slow:.3f}\t\t{fast:.3f}")

    # ClosingLoad ~ 0: activity must not change response.
    for activity in (0.8, 1.6):
        c = response(food, trigger, 0.0, activity, risk, motivation)
        print(f"q=0 activity={activity:.1f} -> C={c:.3f}")
    assert abs(response(food, trigger, 0.0, 0.8, risk, motivation)
               - response(food, trigger, 0.0, 1.6, risk, motivation)) < 1e-12

    # Without angle averaging the fast presentation carries the full radial cost.
    assert rows[0.8][1] < rows[0.8][0]
    assert rows[1.6][1] < rows[1.6][0]
    assert rows[1.6][1] <= rows[0.8][1] + 1e-12  # lower activity, no better


def case_b() -> None:
    print("== Case B: ordinary vs reaction bite ==")
    food, risk, activity = 0.70, 0.02, 1.0
    print("motivation\tT=0,q=0.4\tT=0.10,q=0.4\tT=0.10,q=0.9")
    for motivation in (0.9, 0.7, 0.5, 0.3, 0.2):
        ordinary = response(food, 0.0, 0.40, activity, risk, motivation)
        reaction = response(food, TRIGGER_BUDGET, 0.40, activity, risk, motivation)
        reaction_fast = response(food, TRIGGER_BUDGET, 0.90, activity, risk, motivation)
        print(f"{motivation:.1f}\t\t{ordinary:.3f}\t\t{reaction:.3f}\t\t{reaction_fast:.3f}")

    high = response(food, 0.0, 0.40, activity, risk, 0.9)
    low = response(food, 0.0, 0.40, activity, risk, 0.2)
    low_reaction = response(food, TRIGGER_BUDGET, 0.40, activity, risk, 0.2)
    low_reaction_fast = response(food, TRIGGER_BUDGET, 0.90, activity, risk, 0.2)

    assert high > 0.80            # ordinary good target is enough at high motivation
    assert low < 0.50             # ordinary presentation weakens at low motivation
    assert low_reaction > low     # legal trigger helps
    assert low_reaction_fast < low_reaction  # trigger does not erase its own cost
    assert low_reaction_fast < high           # trigger is not a fixed optimum


def case_c() -> None:
    print("== Case C: direct vs stealth under wariness ==")
    food, trigger, q, activity, motivation = 0.70, 0.0, 0.40, 1.0, 0.50
    print("wariness\tdirect(E=0.50)\tstealth(E=0.10)")
    for wariness in (0.1, 0.2, 0.4, 0.6, 0.8, 1.0):
        direct = response(food, trigger, q, activity, K_WARY * wariness * 0.50, motivation)
        stealth = response(food, trigger, q, activity, K_WARY * wariness * 0.10, motivation)
        print(f"{wariness:.1f}\t\t{direct:.3f}\t\t{stealth:.3f}")

    assert response(food, trigger, q, activity, K_WARY * 0.1 * 0.50, motivation) > 0.30
    assert response(food, trigger, q, activity, K_WARY * 0.8 * 0.50, motivation) < 0.10
    assert (response(food, trigger, q, activity, K_WARY * 0.8 * 0.10, motivation)
            > response(food, trigger, q, activity, K_WARY * 0.8 * 0.50, motivation))


def sweeps() -> None:
    print("== Sensitivity sweeps ==")
    food, risk, motivation = 0.70, 0.0, 0.50

    print("K_close\tslow\tfast\tfast/slow")
    for k in (0.12, 0.19, 0.30):
        globals()["K_CLOSE"] = k
        slow = response(food, 0.0, 0.45, 1.0, risk, motivation)
        fast = response(food, 0.0, 0.90, 1.0, risk, motivation)
        ratio = fast / slow if slow > 0 else 0.0
        print(f"{k:.2f}\t{slow:.3f}\t{fast:.3f}\t{ratio:.2f}")
    globals()["K_CLOSE"] = 0.19

    print("M1\tfood=0.70,M=0.5,ordinary")
    for m1 in (0.30, 0.40, 0.50):
        globals()["M1"] = m1
        print(f"{m1:.2f}\t{response(food, 0.0, 0.0, 1.0, risk, motivation):.3f}")
    globals()["M1"] = 0.40

    print("trigger\tM=0.2,q=0.4\tM=0.2,q=0.9")
    for t in (0.05, 0.10, 0.15):
        print(f"{t:.2f}\t{response(food, t, 0.40, 1.0, 0.02, 0.2):.3f}\t\t"
              f"{response(food, t, 0.90, 1.0, 0.02, 0.2):.3f}")


def main() -> None:
    case_a()
    case_b()
    case_c()
    sweeps()
    print("Strategy probe passed")


if __name__ == "__main__":
    main()

"""Proposal C end-to-end ordering probe.

Working diagnostic only. It checks two topology claims:
1. latent-angle response must be projected before expectation;
2. prey-support values are not probability weights and must not be silently normalized.
"""


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def project(margin, m0=0.0, m1=0.2):
    return clamp((margin - m0) / (m1 - m0))


def response_for_angle(base_margin, task_cost):
    return project(base_margin - task_cost)


def main():
    # Half the latent angles are easy, half are effectively impossible.
    base_margin = 0.18
    costs = [0.0, 0.30]

    correct = sum(response_for_angle(base_margin, c) for c in costs) / len(costs)
    wrong = project(base_margin - sum(costs) / len(costs))

    assert abs(correct - 0.45) < 1e-9
    assert abs(wrong - 0.15) < 1e-9
    assert correct != wrong

    # Prey supports are evidence strengths, not a probability distribution.
    prey_support = {"baitfish": 0.90, "crayfish": 0.75}
    assert sum(prey_support.values()) > 1.0

    print("Proposal C end-to-end ordering probe passed")
    print(f"project-then-average = {correct:.3f}")
    print(f"average-cost-then-project = {wrong:.3f}")
    print(f"prey-support sum = {sum(prey_support.values()):.2f} (not a probability simplex)")


if __name__ == "__main__":
    main()

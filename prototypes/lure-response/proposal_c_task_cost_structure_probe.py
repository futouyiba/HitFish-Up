"""Proposal C task-cost structure probe.

Working hypothesis:
- each task axis is normalized as utilization = demand / capacity;
- any axis > 1 is hard infeasible;
- within feasible space, peak utilization dominates cost;
- secondary simultaneous load may add a bounded surcharge.

All constants are calibration hypotheses, not biological constants.
"""

def task_cost_max_only(ui, um, k=0.33, p=4.0):
    if max(ui, um) > 1.0:
        return None
    return k * max(ui, um) ** p


def task_cost_axis_aware(ui, um, k=0.33, p=4.0, rho=0.25):
    if max(ui, um) > 1.0:
        return None
    ci, cm = ui ** p, um ** p
    return k * (max(ci, cm) + rho * min(ci, cm))


def run_probe():
    assert task_cost_axis_aware(1.01, 0.1) is None
    assert task_cost_axis_aware(0.1, 1.01) is None
    assert task_cost_axis_aware(0.3, 0.1) < task_cost_axis_aware(0.6, 0.1)
    assert task_cost_axis_aware(0.95, 0.1) > 5 * task_cost_axis_aware(0.6, 0.1)
    assert task_cost_max_only(0.6, 0.1) == task_cost_max_only(0.6, 0.6)
    assert task_cost_axis_aware(0.6, 0.6) > task_cost_axis_aware(0.6, 0.1)
    assert task_cost_axis_aware(0.8, 0.6) > task_cost_axis_aware(0.8, 0.1)
    base = task_cost_axis_aware(0.8, 0.1)
    combined = task_cost_axis_aware(0.8, 0.6)
    assert combined < base * 1.25
    return {
        "easy_straight": task_cost_axis_aware(0.3, 0.1),
        "moderate_straight": task_cost_axis_aware(0.6, 0.1),
        "moderate_plus_turn": task_cost_axis_aware(0.6, 0.6),
        "hard_straight": task_cost_axis_aware(0.8, 0.1),
        "hard_plus_maneuver": task_cost_axis_aware(0.8, 0.6),
        "near_limit_straight": task_cost_axis_aware(0.95, 0.1),
        "near_limit_both": task_cost_axis_aware(0.95, 0.9),
    }


if __name__ == "__main__":
    out = run_probe()
    print("Task-cost structure probe passed")
    for key, value in out.items():
        print(f"{key}: {value:.4f}")

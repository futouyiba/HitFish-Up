"""Proposal C: secondary task-axis penalty admission probe.

Purpose:
- test whether a second task axis deserves an independent penalty term;
- keep compound-task effects small unless controlled experience fixtures justify more.

All numbers are working calibration hypotheses, not production values.
"""


def task_cost(ui, um, k=0.35, p=4.0, rho=0.0):
    if ui > 1 or um > 1:
        return None
    a, b = ui ** p, um ** p
    return k * (max(a, b) + rho * min(a, b))


def response(ui, um, rho, value=0.8, motivation=0.6,
             k=0.35, p=4.0, threshold_b=0.85, threshold_c=0.45,
             margin_lo=-0.10, margin_hi=0.23):
    cost = task_cost(ui, um, k, p, rho)
    if cost is None:
        return 0.0
    margin = value - cost - (threshold_b - threshold_c * motivation)
    return max(0.0, min(1.0, (margin - margin_lo) / (margin_hi - margin_lo)))


def run_probe():
    rows = {}
    for rho in (0.0, 0.10, 0.25, 0.50, 1.0):
        rows[rho] = {
            "moderate_straight": response(0.60, 0.10, rho),
            "moderate_turn": response(0.60, 0.60, rho),
            "moderate_vertical": response(0.60, 0.50, rho),
            "hard_straight": response(0.85, 0.10, rho),
            "hard_compound": response(0.85, 0.80, rho),
        }

    # Current experience stories do not identify rho; rho=0 is therefore the
    # minimum-complexity production hypothesis until compound-task fixtures exist.
    assert rows[0.0]["moderate_straight"] == rows[0.0]["moderate_turn"]
    assert rows[0.10]["moderate_turn"] < rows[0.10]["moderate_straight"]
    assert rows[0.25]["hard_compound"] < rows[0.25]["hard_straight"]
    assert rows[1.0]["hard_compound"] <= rows[0.50]["hard_compound"]

    return rows


if __name__ == "__main__":
    rows = run_probe()
    print("Secondary-axis penalty probe passed")
    for rho, values in rows.items():
        print(rho, {k: round(v, 3) for k, v in values.items()})

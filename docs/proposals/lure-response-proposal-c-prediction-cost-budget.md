# Proposal C｜PredictionChallenge 的作用预算

状态：Working Hypothesis。不是 Current，不是生产参数。

## 结论

第一版把 `PredictionChallenge` 定位成**小幅、暂态的修正项**，而不是第二套 `TaskCost`。

推荐 Working 结构：

```text
PredictionCost = K_pred × PredictionChallenge
```

其中 `PredictionChallenge ∈ [0,1]`，`K_pred` 的第一版 Working 预算约为 `0.08～0.12` 的 Decision-Margin 尺度。

这个范围与当前 State Trigger 的 `0.10～0.15` Working 预算同量级但略弱。含义是：

- 一次 prey-appropriate 的中等 dart 通常仍应净正向；
- 一次很急的突然变向会明显削薄 trigger 收益，但不应自动变成负收益；
- 高频、极端乱窜如果最终变差，应由 Prediction + Closing + favorable-window 等真实后果共同造成，而不是由 Prediction 单独处罚到负值。

## 为什么 Prediction 不能成为大 penalty

当前已经准入：突然变向可以作为 prey-conditioned escape/distress 状态证据，提高 `StateTriggerValue`。

如果同时允许 PredictionCost 比 Trigger 更强，那么同一事实会形成：

```text
突然变向
→ 正向 Trigger
→ 更强的负向 Prediction penalty
→ 净结果稳定变差
```

这会使“dart / zig-zag 能触发攻击”的策略故事失去实际权力。

因此第一版应满足一个简单预算护栏：

```text
K_pred <= TriggerBudget
```

这不是长期数学不变量，而是当前缺少更强证据时的复杂度护栏。

## Working probe

示例仅验证结构：

```text
TriggerBudget = 0.12
PredictionBudget = 0.10
recovery tau = 0.60 s
```

PredictionChallenge 采用上一页的 Working event model：

```text
TurnStrength(Δψ) = (1 - cosΔψ) / 2
P(t) = TurnStrength × exp(-age / tau)
```

结果：

| case | P | Trigger | PredictionCost | 净状态变化 |
|---|---:|---:|---:|---:|
| straight | 0.000 | 0.000 | 0.000 | 0.000 |
| 90° dart，刚发生 | 0.500 | 0.102 | 0.050 | +0.052 |
| 90° dart，0.5s前 | 0.217 | 0.102 | 0.022 | +0.080 |
| 150° hard dart，刚发生 | 0.933 | 0.120 | 0.093 | +0.027 |
| 150° hard dart，0.5s前 | 0.405 | 0.120 | 0.041 | +0.079 |

这些数字不是生产 calibration。

它们只证明一件事：Prediction 可以让“越猛烈的突然变向”边际收益变小，同时不必强迫所有 erratic action 变成负收益。

## 与 pause 的关系

如果转向后进入 pause：

- Closing burden 可能下降；
- `PredictionChallenge` 随时间自然衰减；
- favorable dwell 可能增加。

因此不再增加独立的 `PredictionResetBonus`。

如果 pause 期间又发生新的真实方向事件，则按新事件重新评价，而不是机械清零。

## 与 cadence 的关系

当前 event model 使用“近期最强 turn event + 时间衰减”作为最小表达。

连续 zig-zag 的作用是不断刷新 `PredictionChallenge`，而不是额外叠加一个 `CadencePenalty`。

若未来发现：在相同近期最强 turn、相同 Closing 与 temporal support 下，连续多次反向仍有独立的可感知负效应，才准入 event accumulation / frequency semantic。

目前没有这份反例，因此不增加第二个频率惩罚自由度。

## 当前边界

- `PredictionChallenge`：Working admitted transient semantic。
- `PredictionCost = K_pred × P`：Working numeric hypothesis。
- `K_pred ≈ 0.08～0.12`：effect-size probe budget，不是生产参数。
- `tau_recover`：尚未 calibration。
- 通用 `ManeuverCost(ω_traj / turn_capacity)`：撤回作为第一版 numeric core。
- `PredictionChallenge > 1` 或任意阈值 hard-zero：不准入。

可执行 probe：`../../prototypes/lure-response/proposal_c_prediction_cost_budget_probe.py`。

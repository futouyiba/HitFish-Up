# Proposal C｜Decision Margin 联合标定首轮种子

状态：Working Calibration Seed / Candidate。不是 Current，不是生产参数。

## 1. 目的

本页不单独拍 `Good / Marginal / K_mot / Trigger` 的数值，而是给出一组可联合验证的首轮 calibration seed，用来检查当前 DecisionMargin 拓扑是否能同时产生：

- Preferred 稳定高价值；
- Good 在正常鱼情下稳定可用；
- Marginal 随 Motivation / Trigger / burden 发生明确翻转；
- Poor 常态下仍明显困难；
- Reject 始终 hard zero。

当前 Working：

```text
DecisionMargin
= CurrentFoodValue
+ StateTriggerValue
- ClosingCost
- PredictionCost
- RiskCost
- WillingnessThreshold(M)
```

FoodValue gauge：

```text
Preferred = 1.00
Poor      = 0.00
Reject    = hard semantic boundary
```

Motivation threshold：

```text
WillingnessThreshold(M)
= MarginalAnchor + K_mot × (0.5 - M)
```

## 2. 首轮 calibration seed

建议先用：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00

K_mot = 0.40

ordinary StateTrigger ≈ 0.10
upper Working trigger guardrail ≈ 0.15
```

这些值只用于受控 probe，不是 production calibration。

## 3. Motivation 对阈值的影响

用：

```text
MarginalAnchor = 0.40
K_mot = 0.40
```

得到：

| Feeding Motivation M | WillingnessThreshold |
|---:|---:|
| 0.00 | 0.60 |
| 0.25 | 0.50 |
| 0.50 | 0.40 |
| 0.75 | 0.30 |
| 1.00 | 0.20 |

因此在 `Trigger=0, Costs=0` 时：

| Relation | M=0.00 | M=0.25 | M=0.50 | M=0.75 | M=1.00 |
|---|---:|---:|---:|---:|---:|
| Preferred 1.00 | +0.40 | +0.50 | +0.60 | +0.70 | +0.80 |
| Good 0.70 | +0.10 | +0.20 | +0.30 | +0.40 | +0.50 |
| Marginal 0.40 | -0.20 | -0.10 | 0.00 | +0.10 | +0.20 |
| Poor 0.00 | -0.60 | -0.50 | -0.40 | -0.30 | -0.20 |

这组 seed 购买了几个期望行为：

- Good 即使在很低 Motivation 下，零 burden 时仍保留正 margin；
- Marginal 正好围绕 Motivation 中点发生过阈值翻转；
- Motivation 从参考值升到极高，只给 Marginal 增加 `+0.20`，不会吞掉整个 FoodValue 标尺；
- Poor 即使在 M=1、零 burden、无 Trigger 时仍为 `-0.20`，不会被普通高鱼情单独救活。

## 4. 与 Trigger 的关系

若 ordinary Trigger 约为：

```text
+0.10
```

则：

```text
Marginal + M=0.50 + ordinary Trigger
→ margin = +0.10
```

可以明确越线。

但：

```text
Poor + M=1.00 + ordinary Trigger
→ margin = -0.10
```

仍不足以成为响应目标。

即使使用当前 Working upper guardrail：

```text
Poor + M=1.00 + Trigger 0.15
→ margin = -0.05
```

仍不会单靠 Motivation + Trigger 越线。

若未来希望 Poor 在极端条件下偶发响应，应由额外合法有利项共同完成，例如：

- 正向 SizePreferenceAdjustment；
- 正向 DietaryShiftDelta；
- 特别低的 task burden；
- 或经单独 admission 的更强 prey-state evidence。

不要通过无限扩大 `K_mot` 或 generic Trigger 来救 Poor。

## 5. 最小受控篮子

首轮建议至少检查以下案例。

### A. Preferred，低 Motivation，moderate burden

示例：

```text
FoodValue = 1.00
M = 0.25
TotalSoftCost = 0.15
Trigger = 0

Threshold = 0.50
Margin = 1.00 - 0.15 - 0.50 = +0.35
```

预期：仍然明显 responsive。

### B. Good，参考 Motivation，moderate burden

```text
FoodValue = 0.70
M = 0.50
TotalSoftCost = 0.15
Trigger = 0

Margin = 0.70 - 0.15 - 0.40 = +0.15
```

预期：稳定可用，但弱于 Preferred。

### C. Marginal，参考 Motivation，moderate burden

```text
FoodValue = 0.40
M = 0.50
TotalSoftCost = 0.15
Trigger = 0

Margin = -0.15
```

预期：偏弱 / 不响应。

### D. 同一 Marginal，高 Motivation + 低 burden + ordinary Trigger

```text
FoodValue = 0.40
M = 0.75
TotalSoftCost = 0.05
Trigger = 0.10

Threshold = 0.30
Margin = 0.40 + 0.10 - 0.05 - 0.30 = +0.15
```

预期：发生明确策略翻转。

### E. Poor，极高 Motivation + 零 burden + upper Trigger

```text
FoodValue = 0.00
M = 1.00
TotalSoftCost = 0
Trigger = 0.15

Threshold = 0.20
Margin = -0.05
```

预期：仍不过线。

这保证 Poor 不会被普通状态因素轻易抬成主力目标。

### F. Poor，加合法 prey-specific 正向偏移

例如只作为结构测试：

```text
BaseDietAffinity = 0.00
SizePreferenceAdjustment + DietaryShiftDelta = +0.10
M = 1.00
Trigger = 0.15
Cost = 0

CurrentFoodValue = 0.10
Threshold = 0.20
Margin = +0.05
```

预期：极端组合下可以出现很弱的非零响应。

这里的 `+0.10` 不是 production DietaryShift / Size 参数，只证明 topology 允许 Poor 在多个合法因素共同支持时偶发越线。

### G. Reject

无论 M / Trigger / Cost：

```text
Reject → C = 0
```

不进入上述连续计算。

## 6. 为什么这组 seed 比等距四档更好

若简单采用：

```text
1.00 / 0.67 / 0.33 / 0.00
```

并不能说明 Motivation / Trigger 应有多大预算。

当前 seed：

```text
1.00 / 0.70 / 0.40 / 0.00
```

使：

```text
Preferred - Good = 0.30
Good - Marginal = 0.30
Marginal - Poor = 0.40
```

这不是为了数学对称，而是刻意给 `Poor` 更大的保护区，同时允许 Marginal 在 `0.10–0.20` 量级的状态变化下发生翻转。

如果未来 probe 表明：

- Good 太容易被 burden 打掉，优先检查 `g`、cost budget 或 Response projection；
- Marginal 太容易被 Trigger 抬升，优先检查 `m` 与 Trigger budget；
- Poor 太容易响应，优先检查 `m`、`K_mot`、正向 adjustment / trigger admission，而不是直接加 hard gate。

## 7. 不在本轮冻结的内容

本页不冻结：

- production `Good / Marginal` anchors；
- production `K_mot`；
- Trigger 最终幅度；
- Closing / Prediction / Risk 各自 cost budget；
- DecisionMargin → response coefficient 的 projection anchors；
- SizePreference / DietaryShift 的最终幅度；
- bite-rate / candidate-rate 目标。

这些需要后续用完整受控 basket 和体验目标联合反推。

## 8. 当前推荐

在没有更强 calibration evidence 前，后续 probe 可把：

```text
Good = 0.70
Marginal = 0.40
K_mot = 0.40
ordinary Trigger = 0.10
upper Trigger guardrail = 0.15
```

作为统一的 **Working calibration seed**，避免不同文档各自使用不同临时数字。

任何实际生产数值都需要重新经过 joint calibration，不因本页能产生合理案例而自动晋升。

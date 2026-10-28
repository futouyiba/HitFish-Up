# Proposal C｜Combined Burden Stress Test

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

ClosingCost、PredictionCost、RiskCost 可以在 DecisionMargin 中相加，因为它们回答不同问题：

```text
ClosingCost
→ 追赶 / closing 的任务负担

PredictionCost
→ 突然轨迹变化导致的预测困难

RiskCost
→ 当前 presentation 的可疑 / 风险抑制
```

第一版不增加通用 `TotalBurdenCap`。多个独立负担同时很高时，Good target 被压到 0 可以是正确结果。

真正需要的 guardrail 是：

> ordinary / 常见组合负担不能让 Good target 大面积、常态化归零。

因此联合标定必须看 combined burden，而不是分别看三个 cost 的单项上限。

## 2. 当前联合标尺

Working calibration seed：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00

WillingnessThreshold(reference Motivation) = 0.40
Response full anchor M1 = 0.40
```

在无 Trigger、reference Motivation 下：

```text
Margin = FoodValue - 0.40 - TotalSoftBurden

TotalSoftBurden
= ClosingCost
+ PredictionCost
+ RiskCost
```

## 3. Stress baskets

以下数值只用于检查模型行为，不是 production 参数。

| Basket | Closing | Prediction | Risk | Total burden |
|---|---:|---:|---:|---:|
| Light | 0.04 | 0.02 | 0.02 | 0.08 |
| Ordinary | 0.08 | 0.05 | 0.05 | 0.18 |
| Heavy | 0.15 | 0.10 | 0.10 | 0.35 |
| Severe | 0.22 | 0.12 | 0.12 | 0.46 |

按当前 projection：

```text
C = clamp(Margin / 0.40, 0, 1)
```

得到：

| Basket | Preferred C | Good C | Marginal C |
|---|---:|---:|---:|
| Light | 1.00 | 0.55 | 0 |
| Ordinary | 1.00 | 0.30 | 0 |
| Heavy | 0.625 | 0 | 0 |
| Severe | 0.35 | 0 | 0 |

这组行为符合当前 relation 语义：

- Preferred 对 light / ordinary burden 有明显鲁棒性；
- Good 在 ordinary burden 下仍可用，但明显下降；
- Good 在多个较强不利因素同时存在时可以归零；
- Preferred 在 heavy / severe burden 下仍保留一定 response；
- Marginal 在 reference Motivation、无 Trigger 时本来就在阈值边缘，因此普通 burden 会使其归零，需靠高 Motivation、低 burden 或合法 Trigger 翻转。

## 4. 不建立 TotalBurdenCap

拒绝：

```text
TotalSoftBurden = min(Closing + Prediction + Risk, 0.25)
```

或其它统一硬 cap。

原因：

- 会让多个真实独立负担无法继续叠加；
- 极端 high closing + high risk 本来就应明显抑制 Feeding response；
- cap 会把不同策略场景压成相同结果；
- 之后难以判断某个单项 cost 是否过大。

如果 ordinary case 过度归零，应回头调整单项 effect-size，而不是用末端 cap 遮盖问题。

## 5. Joint budget guardrail

当前 Working 建议把普通组合的目标区间理解为：

```text
ordinary combined burden ≈ 0.12 ～ 0.20
```

这不是生产硬范围，而是 calibration guardrail。

在 reference Motivation、无 Trigger 下，Good 的基础 margin 是：

```text
Good - threshold
= 0.70 - 0.40
= 0.30
```

当前 `M1=0.40` 下：

```text
combined burden = 0.12
→ Good margin = 0.18
→ C = 0.45

combined burden = 0.18
→ Good margin = 0.12
→ C = 0.30

combined burden = 0.20
→ Good margin = 0.10
→ C = 0.25
```

如果普通 gameplay 的 combined burden 经常达到 `>= 0.30`，Good 会常态化归零，说明至少一个 cost 的普通 effect-size 过大或 feature ownership 重复计权。

## 6. 单项 budget 的含义

当前已有 Prediction Working budget 约：

```text
PredictionCost ≈ 0.08 ～ 0.12   # 较强 challenge 的工作上沿
```

这不能被误解为“普通 Prediction 每次都约 0.10”。

同理后续 `K_close / K_wary` 的 production calibration 必须区分：

```text
ordinary value
strong value
near-maximum value
```

不能把每个 family 的 working upper guardrail 同时作为常见输入。否则三个合法但偏高的上沿一叠，会制造系统性过抑制。

## 7. Activity 的位置

Activity 通过 Closing 路径放大主动追赶成本，因此：

```text
Activity low
→ ClosingCost higher
```

它不作为第四项独立 soft cost 再相加。

否则同一“主动追赶更吃力”的后果会被重复结算。

Activity 具体公式由其当前 owner 维护；本页只固定 combined-burden 的消费边界。

## 8. Trigger / Motivation 是合法对冲，不是补锅

StateTrigger 与高 FeedingMotivation 可以在语义上对冲 soft burden：

```text
FoodValue
+ Trigger
- soft burden
- WillingnessThreshold
→ Margin
```

例如 Marginal 在 ordinary burden 下可以为 0，但高 Motivation + 合法 Trigger 可能重新越线。这是预期策略故事。

但不允许通过无来源的 Trigger 或放大 Motivation 来掩盖普通 burden calibration 过高。

## 9. 回归指标

后续 simulation 至少记录：

```text
combined_burden_distribution
burden_by_component
P(Good C=0)
P(Good C>0.3)
P(Preferred C=0)
component_contribution_share
```

并按：

- fish species / cohort；
- presentation family；
- Motivation band；
- Wariness band；
- lure speed / trajectory regime

分层查看。

如果普通场景中 `P(Good C=0)` 很高，需要优先检查：

1. Feature Ownership 是否重复；
2. Closing ordinary cost 是否过高；
3. Prediction upper guardrail 是否被当成常态值；
4. RiskCost 是否因 SuspicionLoad 或 K_wary 过宽而常态化。

## 10. 当前 OPEN

- `K_close` 的生产标定与 ordinary ClosingCost 分布；
- `K_wary` 的生产标定与 ordinary RiskCost 分布；
- Activity 对 ClosingCost 的 effect-size；
- 完整 latent-bearing integration 后 Closing burden 的真实分布；
- 实际 presentation telemetry / simulation basket；
- ordinary combined burden `0.12～0.20` 是否需要调整。

本页冻结“不加 TotalBurdenCap、以 ordinary combined burden 做联合 guardrail”的原则，并同步当前 `M1=0.40` Working projection；不声明 production calibration 已完成。

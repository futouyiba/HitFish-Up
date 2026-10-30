# Proposal C｜Feeding Motivation → Willingness Threshold

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

Proposal C 不再沿用旧候选模型中的：

```text
FeedingMotivation × FoodValue / incentive
```

当前 Feeding Motivation 只改变“鱼愿意为一次摄食机会接受多低的净价值”，因此进入 `DecisionMargin` 的方式是移动 `WillingnessThreshold`：

```text
DecisionMargin(θ)
= FoodValue
+ StateTriggerValue
- ClosingCost(θ)
- PredictionCost
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

首版推荐一个中心化、单调、线性的 projection：

```text
M ∈ [0, 1]
M_ref = 0.5

WillingnessThreshold(M)
= T_ref + K_mot × (M_ref - M)
```

其中：

- `M` 不是咬口概率；
- `M=0.5` 是 Response 约定的参考摄食意愿；
- `M>0.5` 降低阈值，更容易出手；
- `M<0.5` 提高阈值，更挑剔；
- `K_mot > 0` 控制 Motivation 能移动阈值的总幅度。

首版不再额外使用 sigmoid、幂次或 Motivation 乘数。

## 2. 与 FoodValue 标尺对齐

当前 Working 的 FoodValue relation scale 已固定：

```text
Preferred = 1.0
Good      = g
Marginal  = m
Poor      = 0.0

1 > g > m > 0
Reject    = hard semantic boundary
```

`Marginal` 的定义本身就是“在正常鱼情附近、对其它负担较敏感的阈值目标”。因此第一版推荐直接把参考阈值锚在 `Marginal`：

```text
T_ref = m
```

于是：

```text
M = 0.5
StateTrigger = 0
Costs = 0
```

时：

```text
Preferred margin = 1 - m
Good margin      = g - m
Marginal margin  = 0
Poor margin      = -m
```

这不是最终 bite-rate 标定，而是把 relation class 与 Motivation threshold 的语义原点对齐。

## 3. 为什么不再让 Motivation 乘 FoodValue

若使用：

```text
FoodValue × Motivation
```

会带来三个问题：

1. Motivation 越低，Preferred 与 Poor 的绝对差异也被一起压缩；
2. “食物本身值多少钱”与“当前愿不愿意出手”再次纠缠；
3. DietaryShift / BaseDietAffinity 与 Motivation 更难分别标定。

阈值模型保留两个独立问题：

```text
FoodValue
→ 这口食物本身值不值得

FeedingMotivation
→ 当前最低愿意接受多差的净交易
```

因此同一个 Marginal prey 可以在高 Motivation 时越线，在低 Motivation 时掉到线下，而它的 FoodValue 本身没有变化。

## 4. `M=0` / `M=1` 不是硬语义

`M=0` 不自动表示“绝不摄食”；`M=1` 也不表示“必定攻击”。

它们只是 Feeding Motivation 轴的两个极端端点。

是否响应仍取决于：

```text
FoodValue
+ StateTriggerValue
- ClosingCost
- PredictionCost
- RiskCost
- threshold
```

因此：

- 高 Motivation 不能复活 `Reject`；
- 高 Motivation 不能绕过 angle-local hard infeasible；
- 低 Motivation 不撤销 prey support 或 prey interpretation；
- Unknown Motivation 不能默认成 `0.5`。

## 5. `K_mot` 的标定目标

当前不冻结 `K_mot` 数值。

它必须由受控体验篮子反推，至少满足：

### 5.1 Marginal 必须能发生鱼情翻转

固定 prey、Trigger、Closing、Prediction、Risk：

```text
Marginal + low Motivation
→ 明显偏弱 / 可能不响应

Marginal + high Motivation
→ 能明显进入响应区
```

如果 Motivation 无法改变 Marginal 的状态，它对玩家策略没有购买足够表达能力。

### 5.2 Good 不应因轻微低 Motivation 就普遍失效

`Good` 是稳定正常目标。

因此 Moderate Motivation 波动可以改变响应强度，但不应让所有 Good prey 轻易变成近似不可食。

### 5.3 Poor 不应被普通高 Motivation 普遍抬成主力目标

`Poor` 仍应保持低连续价值。

允许：

```text
very high Motivation
+ extremely low burden
+ 合法 Trigger（若存在）
→ Poor 偶发越线
```

但不允许普通的 Motivation 提升使 Poor 系统性接近 Good。

### 5.4 Preferred 在低 Motivation 时仍保留“高食物价值”身份

低 Motivation 可以让鱼更挑剔，但不应通过一个过大的 `K_mot` 抹掉 Preferred 与其它 relation 的结构差异。

## 6. 与 StateTrigger 的预算关系

当前 StateTrigger Working budget 约为 Decision-Margin 标尺上的 `0.10–0.15`，尚未 production calibration。

因此后续联合标定必须检查：

```text
Motivation swing
Trigger budget
Good - Marginal gap
Marginal - Poor gap
```

四者不能各自独立拍值。

例如若：

```text
Good - Marginal
```

比普通 Trigger 还小很多，则 Marginal 很容易被任意 Trigger 普遍提升成 Good-like 行为，relation 档位失去意义。

同样，如果 `K_mot` 的半幅已经跨越大部分 `[Poor, Preferred]` 标尺，Motivation 会吞掉 FoodValue 的职责。

## 7. 与 Bake 的接口

Response 只消费已解析的：

```text
FeedingMotivation M
```

不重读：

- Period；
- 近期摄食历史；
- 温度；
- 氧气；
- Activity；
- Wariness；
- DietaryShift cause。

这些 cause 是否以及如何生成 Feeding Motivation，属于 Fish Condition / Bake 上游。

仓内旧候选 `docs/proposals/lure-feeding-motivation.md` 曾提出：

```text
species/cohort reference
+ period effect
+ recent consumption load
→ H
```

这仍可作为上游设计证据，但其中 `H × incentive` 的 Response 数学不再属于当前 Proposal C Working 路线。

若上游最终输出的 Feeding Motivation 标尺不是 `[0,1]` 且 `0.5=reference`，必须提供显式 adapter；Response 不得自行猜测或重新归一化。

## 8. Unknown / Disabled / NotApplicable

必须保持：

```text
Unknown
≠ 0
≠ 0.5
```

- `Unknown`：ResolutionIncomplete，不输出最终 Feeding scalar；
- `Disabled`：若某 Phase 明确禁用 Motivation 动态，需要该 Phase 的显式规则，不通过缺值表达；
- `NotApplicable`：若某非 Feeding mode 不消费 Feeding Motivation，由对应 mode contract 决定；
- 已知 `M=0.5`：只是已解析的参考状态。

## 9. 首版数学

在 relation anchors 与 Response projection 完成联合标定前，首版保留：

```text
T_ref = MarginalAnchor

WillingnessThreshold(M)
= MarginalAnchor
+ K_mot × (0.5 - M)
```

因此：

```text
DecisionMargin(θ)
= CurrentFoodValue
+ StateTriggerValue
- ClosingCost(θ)
- PredictionCost
- RiskCost
- MarginalAnchor
- K_mot × (0.5 - M)
```

注意：这仍是 Working calibration topology，不是生产数值。

## 10. 当前 OPEN

- `Good` / `Marginal` 的最终 numeric anchors；
- `K_mot` 的 production 值；
- Feeding Motivation Bake 是否采用 `[0,1], 0.5=reference` 的同一标尺，还是需要 adapter；
- Response projection 的 `M0/M1`（projection anchors，注意不要与 Feeding Motivation 的 `M` 混淆）；
- Poor 在最大 Motivation、零 burden、无 Trigger 时是否允许刚好进入非零响应区；
- 上游近期消费、Period 等 cause 的最终生产 reducer。

本页只闭合 Feeding Motivation 在 Response 中的职责、标尺接口与首版 projection 形状，不冻结上游 Bake 算法或最终体验数值。

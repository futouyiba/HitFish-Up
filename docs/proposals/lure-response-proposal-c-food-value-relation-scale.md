# Proposal C｜FoodValue Relation Scale

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`Preferred / Good / Marginal / Poor` 是 `BaseDietAffinity` 的 authoring relation class；Bake 后投影到同一条连续 FoodValue 标尺。

第一版冻结**标尺语义与 gauge**，不冻结 `Good / Marginal` 的最终生产数值：

```text
Preferred = 1.0   # 连续标尺上端参考
Good      = g     # 0 < m < g < 1
Marginal  = m
Poor      = 0.0   # 连续标尺下端参考
Reject    = hard semantic boundary，不进入连续标尺
```

`Poor = 0` 不代表 response = 0。Response 仍由完整 DecisionMargin 决定；高 FeedingMotivation、低任务成本或合法 StateTrigger 仍可让 Poor 在极有利条件下越过门槛。

`Reject` 与 `Poor` 必须保持结构区别：

```text
Poor
→ continuous FoodValue = 0
→ 仍进入 DecisionMargin

Reject
→ ResolvedNonResponsive / C = 0
→ 不允许 Motivation / Trigger / DietaryShift 救活
```

## 2. 为什么必须固定标尺

当前解释模型：

```text
DecisionMargin
= FoodValue
+ StateTriggerValue
- ClosingCost
- PredictionCost
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

若 FoodValue 全部加一个常数，同时 WillingnessThreshold 也加同一常数，DecisionMargin 不变。因此仅声明“Preferred > Good > Marginal > Poor”不足以形成可标定模型。

第一版用：

```text
Preferred = 1
Poor = 0
```

固定 FoodValue 的 offset 与跨度。之后 Trigger、Cost、Motivation threshold 的预算都以这一单位比较。

这不是说真实鱼类食物价值天然处在 0..1；这是生产模型的内部 reference scale。

## 3. 四档分别购买什么行为

### Preferred

参考上下文、参考 prey size 下的主力 Feeding target。

预期：

- 普通 FeedingMotivation 下，合理 presentation 应较容易进入 responsive 区；
- 不依赖异常强 StateTrigger 才能成立；
- 一般 soft burden 可以降低响应，但不应轻易把它变成长期无效目标。

### Good

稳定、正常可选的 Feeding target。

预期：

- 普通 Motivation + 合理 presentation 应有可观响应；
- 相比 Preferred，对 Closing / Prediction / Risk burden 更敏感；
- 不应表现成“需要极特殊条件才能吃”。

### Marginal

边缘 Feeding target。

预期：

- 普通条件下经常处于阈值附近或阈值下方；
- 高 Motivation、较低任务成本、较低风险或合法 Trigger 可以使它进入响应区；
- 它是当前模型中最重要的“策略翻转”档。

### Poor

低连续食物价值，但仍属于 Feeding target。

预期：

- 常态下多为弱响应或不响应；
- 只有非常有利的 Motivation / Trigger / task-burden 组合才偶发越过阈值；
- 不承担 hard exclusion。

### Reject

明确不属于当前 species / cohort 的 Feeding target。

它不是连续标尺的最低一档，而是独立语义边界。

## 4. Good / Marginal 不应预设等距

第一版拒绝直接冻结：

```text
Preferred = 1.00
Good      = 0.67
Marginal  = 0.33
Poor      = 0.00
```

或其它等距方案。

原因：relation class 的目的不是视觉均匀，而是购买不同的阈值行为。

最终 `g`、`m` 应通过受控 response basket 反推，使：

```text
Preferred
→ reference-good presentation 在正常 Motivation 下接近高响应区

Good
→ 普通条件稳定可用，但明显弱于 Preferred

Marginal
→ 条件变化能产生“过阈值 / 不过阈值”的策略翻转

Poor
→ 只有极有利条件才偶发响应
```

因此只冻结：

```text
1 > g > m > 0
```

不冻结实际间距。

## 5. 与 FeedingMotivation 的关系

FoodValue 回答：

> 这类 prey 对当前鱼来说有多值得吃？

FeedingMotivation 回答：

> 当前鱼愿意接受多低价值 / 多高代价的 Feeding target？

因此：

```text
FoodValue
→ prey-specific value axis

FeedingMotivation
→ global willingness threshold
```

不允许用 Motivation 重新缩放 FoodValue：

```text
FoodValue *= FeedingMotivation   # reject
```

否则 Good / Marginal / Poor 的可解释边界会消失。

## 6. 与 DietaryShift 的关系

当前：

```text
CurrentFoodValue(prey)
= BaseDietAffinity(prey)
+ SizePreferenceAdjustment(prey)
+ DietaryShiftDelta(prey)
```

`DietaryShiftDelta` 使用与 FoodValue 同一 Decision-Margin 单位，但必须满足：

- 不拥有 common-mode freedom；共同升降全部 prey 的需求归 FeedingMotivation；
- 不允许把 Reject 救活；
- 最终 CurrentFoodValue 的合法 clamp / extrapolation 边界仍需 calibration 后冻结。

在生产 anchor 未标定前，不先规定 `DietaryShift = ±0.1` 等最终幅度。

## 7. 与 StateTrigger 的关系

StateTrigger 是当前 prey/state 局部的额外攻击价值，不属于 BaseDietAffinity。

已有 Working budget 约为 Decision-Margin 标尺的 `0.10–0.15`，目前只是 guardrail，不是生产参数。

Relation anchor calibration 必须检查：

- Trigger 可以帮助 Marginal 越线；
- Trigger 可以增强 Good；
- Trigger 默认不应把 Poor 普遍变成主目标；
- Reject 无论 Trigger 多高都保持 0。

若未来 `Good - Marginal` 的档差比合法 Trigger budget 还小，应检查是否导致 relation class 失去意义，而不是直接扩大 Trigger。

## 8. 标定方式

不要单独拟合 relation anchors。应与 Motivation threshold、Trigger budget、Closing / Prediction / Risk costs 联合做小型 basket calibration。

至少需要以下 controlled cases：

```text
A. Preferred + normal Motivation + low burden
B. Good + normal Motivation + moderate burden
C. Marginal + normal Motivation + moderate burden
D. Marginal + high Motivation / low burden
E. Poor + normal conditions
F. Poor + exceptional favorable conditions
G. Reject + any conditions
```

验收目标：

- A 高响应；
- B 可观但低于 A；
- C 常在边缘；
- D 相比 C 有明确跨阈值机会；
- E 弱或 0；
- F 可以偶发非零，但不能普遍追平 Good；
- G 永远 0。

## 9. 外部生态证据的使用边界

鱼类 prey choice 同时受 prey profitability、捕获 / handling cost、predator size、prey size、饱腹程度与 prey availability 等影响。外部食谱或胃含物比例不能直接等同于本项目的 FoodValue anchor。

因此外部资料只帮助判断 relation class 排序与是否需要 species/cohort override；最终连续 anchor 仍由项目 response calibration 决定。

## 10. 当前 OPEN

- `Good = g` 的 production anchor；
- `Marginal = m` 的 production anchor；
- FeedingMotivation → WillingnessThreshold 的生产范围；
- CurrentFoodValue 经 SizePreference / DietaryShift 调整后的 clamp / extrapolation 规则；
- Trigger / Risk / Prediction / Closing 的最终 budget；
- relation class 是否需要在 Editor 中显示连续 resolved value，还是只显示档位与 Explain。

本页冻结 relation scale 的语义、`Preferred=1 / Poor=0` 的 gauge 与 Reject 边界，不冻结最终 calibration 数值。

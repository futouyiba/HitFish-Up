# Proposal C｜DecisionMargin 可补偿性契约

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

Proposal C 第一版继续采用加性 DecisionMargin：

```text
DecisionMargin(theta)
= FoodValue
+ StateTriggerValue
- ClosingCost(theta)
- PredictionCost
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

但该公式不是“所有因素都换成一个数再相加”。它只允许**可补偿的 soft evidence / soft burden**进入。

所有不可补偿语义必须在进入 Margin 前通过 typed state / hard semantic boundary 处理。

## 2. 为什么加法可以成立

Margin 回答的是：

> 在当前 prey interpretation 下，正向摄食价值与触发证据，扣除当前行动负担、预测困难、风险以及行动门槛后，还剩多少净决策余量？

因此进入 Margin 的各项都使用同一 working gauge：`decision-margin units`。

加法表达的是一种明确机制：

```text
更高 FoodValue
可以补偿一部分 Closing / Prediction / Risk

更强 StateTrigger
可以帮助边缘目标跨线

更低 Motivation
可以通过提高 Threshold 抵消这些正向证据
```

这是第一版需要的策略语义，而不是物理量之间的直接相加。

## 3. 什么可以进入 Margin

### Positive soft evidence

```text
FoodValue
StateTriggerValue
```

它们可以提高出手余量。

### Negative soft burden

```text
ClosingCost
PredictionCost
RiskCost
```

它们可以压低出手余量，但默认允许被足够高的价值 / trigger / Motivation 条件部分补偿。

### Decision threshold

```text
WillingnessThreshold(FeedingMotivation)
```

Motivation 不作为另一项正向“奖励”，而是移动行动门槛。

## 4. 什么不能进入 Margin

以下语义不能通过“给一个很大的 cost”模拟：

### Reject

```text
TargetRelation = Reject
→ typed resolved zero
```

不能写成：

```text
RejectCost = 999
```

因为 Reject 的语义是“不属于合法 Feeding target”，不是“非常不划算”。

### ResolutionIncomplete

```text
required input Unknown / NotConfigured
→ ResolutionIncomplete
→ no scalar Margin
```

不能把 Unknown 变成 `0`、均值或惩罚项。

### Future true hard interception infeasibility

若未来获得合法 encounter geometry / reaction-window contract，并能证明某 case 物理上没有攻击窗口，则：

```text
HardInterceptionInfeasible
→ typed zero for that branch
```

不能仅通过一个超大 ClosingCost 冒充 hard semantic boundary。

当前 Proposal C 没有足够几何信息，所以第一版没有该 hard gate。

## 5. 可补偿性不是无限补偿

“soft”不表示成本必须有 cap。

例如：

```text
ClosingCost
= K_close × u_close^2 × ActivityCostMultiplier
```

可以随着 `u_close` 增大而持续增加，因此极高 Closing burden 仍可自然把 Margin 压到负值。

区别在于：

```text
soft burden
→ 通过完整 Margin 决定结果

hard semantic zero
→ 不进入普通 Margin
```

第一版不增加 `TotalBurdenCap`。

## 6. 为什么不乘法聚合

不采用：

```text
ResponseDrive
= FoodValue
  × Motivation
  × ClosingFactor
  × PredictionFactor
  × RiskFactor
```

因为这会导致：

- 任一低值都可能把其它 cause 近似抹掉；
- Motivation 又退回“全局倍率”，失去 threshold 语义；
- 难以表达 Marginal 在强 Trigger / 高 Motivation 下翻转；
- 多个 penalty 连乘会系统性产生过强衰减；
- 每个 factor 的数值尺度难以独立解释。

加性 Margin 更直接表达“证据与负担的竞争”。

## 7. 为什么不把所有正向项先乘起来

不采用：

```text
AttackValue
= FoodValue × StateTrigger
```

因为 `StateTrigger=0` 是“当前没有额外 trigger”，不应把正常 FoodValue 归零。

同样不采用：

```text
FoodValue × Motivation
```

因为 Motivation 低并不改变目标本身的 FoodValue。

因此：

```text
FoodValue + Trigger - Threshold
```

比乘法更符合当前 owner 划分。

## 8. 进入同一 Margin 的准入条件

任何新 numeric term 在加入 DecisionMargin 前必须同时满足：

1. **独立问题**：它回答的不是已有 term 已经回答的问题；
2. **独立 cause**：不是同一 raw fact 的同义重复处罚 / 奖励；
3. **soft compensable**：设计语义允许它被其它合法证据部分对冲；
4. **同一 gauge**：可以被标定为 decision-margin units；
5. **有 residual strategy effect**：控制其它项后仍有稳定、可学习的策略差异；
6. **不是 hard state**：Reject / Unknown / true infeasibility 必须走 typed semantics。

不满足这些条件，不应新增匿名 `Bonus` / `Penalty`。

## 9. 当前算法顺序

对每个 prey interpretation、每个 latent bearing：

```text
1. resolve typed prerequisites
   - support status
   - TargetRelation
   - required inputs

2. if hard semantic zero
   → resolved zero

3. compute soft terms
   FoodValue
   StateTriggerValue
   ClosingCost(theta)
   PredictionCost
   RiskCost
   WillingnessThreshold

4. DecisionMargin(theta)

5. ResponseProjection(Margin)
   → C_conditional(theta)

6. integrate latent bearing

7. multiply calibrated prey support

8. sibling interpretation composition
```

这个顺序防止 hard state 被数值补偿，也防止 support / sibling composition 侵入 fish-side conditional decision。

## 10. Calibration implication

由于各 soft term 共用同一 margin gauge，production calibration 不能逐项独立完成后直接拼接。

至少要联合观察：

```text
FoodValue class
× Motivation band
× Trigger regime
× Closing regime
× Prediction regime
× Wariness/Suspicion regime
```

重点不是每项“看起来合理”，而是组合后保持目标策略排序。

第一版已知 guardrail：普通 combined burden 不应让 Good 大面积常态归零；Preferred 应比 Good 对同样 burden 更鲁棒；Marginal 应能在有利组合下翻转；Poor 只在极端有利条件下出现弱响应；Reject 永不复活。

## 11. 当前 Working Closure

第一版保留：

```text
additive soft DecisionMargin
+ typed non-compensable boundaries
+ clipped ResponseProjection
```

不引入：

```text
multiplicative drive
anonymous total burden cap
hard states encoded as giant numeric penalties
extra generic bonus/penalty terms
```

后续若出现无法由 additive margin 复现的稳定 strategy ordering，再以具体反例重开 aggregation topology，而不是先增加自由参数。

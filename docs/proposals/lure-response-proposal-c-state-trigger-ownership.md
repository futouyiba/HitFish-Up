# Proposal C：State Trigger Value 的 ownership 裁决

> Status: Working Contract
>
> Scope: Feeding Response / prey-conditioned state valuation

## 结论

`StateTriggerValue` 应归属于**当前 prey interpretation + 当前呈现状态**，不应归属于鱼级的 `Motivation / WillingnessThreshold`。

推荐写法：

```text
AttackValue = FoodValue + StateTriggerValue
DecisionMargin = AttackValue - TaskCost - WillingnessThreshold(Motivation)
```

实现时可以不必强制保存独立 `AttackValue` 字段；它首先是 Explain / conceptual seam。若没有独立生命周期、缓存或 authoring 需求，数值实现可以直接保持：

```text
DecisionMargin
= FoodValue
+ StateTriggerValue
- TaskCost
- WillingnessThreshold(Motivation)
```

## 为什么不把 Trigger 放到 Motivation 阈值侧

在当前线性 margin 里：

```text
FoodValue + Trigger - TaskCost - Threshold
```

和：

```text
FoodValue - TaskCost - (Threshold - Trigger)
```

数学上可以等价。

但 ownership 不等价。

`Motivation / WillingnessThreshold` 是鱼在当前状态下的**全局摄食意愿 / 挑食程度**。同一条鱼面对不同 prey interpretation 时，这个状态可以共享。

`StateTriggerValue` 则来自：

```text
某个 prey interpretation
+ 当前该 prey 的 escape / distressed / struggling state
```

因此它必须是 prey-local / mode-local 的。

如果错误地把 Trigger 写进鱼级阈值，就会出现串味：

```text
baitfish 的 escape trigger 成立
→ fish-global threshold 被降低
→ 同时把没有 escape trigger 的 crayfish path 也抬高
```

这是错误的因果传播。

Working probe 使用相同 FoodValue / TaskCost / Motivation，只让 baitfish path 拥有 `StateTriggerValue=0.12`：

```text
正确 prey-local ownership：
baitfish  ≈ 0.426
crayfish  ≈ 0.083

错误 fish-global threshold ownership：
baitfish  ≈ 0.426
crayfish  ≈ 0.426
```

第二种结果把 baitfish 的状态价值泄漏给了另一个 prey interpretation。

## 语义分工

### FoodValue

回答：

> 这个目标本身值不值得吃？

主要由 Target Relation / diet / prey value 决定。

### StateTriggerValue

回答：

> 按当前 prey interpretation 理解时，它现在这个状态是否特别容易触发攻击？

例如：

- baitfish 的 sudden dart / escape-like state；
- crayfish 的 backward escape burst；
- frog 的 surface struggle。

它不是通用 `ErraticBonus`，也不允许跨 prey path 自动共享。

### WillingnessThreshold(Motivation)

回答：

> 这条鱼当前整体有多愿意为一次摄食机会出手？

它可以影响多个 prey / mode，但不应被某个具体 prey 的局部状态反向改写。

## `AttackValue` 是否需要成为正式中间对象

当前不建议因为公式可读性就强制新增 runtime object。

`AttackValue = FoodValue + StateTriggerValue` 的主要价值是：

- Explain / debug 更清楚；
- 明确 target-side value 与 fish-side willingness 的边界；
- 防止后续把 Trigger 错塞进 Motivation。

只有未来出现以下独立需求，才考虑把 `AttackValue` admission 为正式中间结构：

1. 多种 prey-state valuation 需要先在目标侧聚合；
2. 该值需要独立缓存或跨多个 response mode 复用；
3. authoring / telemetry 需要直接观察“目标当前攻击价值”；
4. consumer 需要在不重新展开 FoodValue 和 StateTriggerValue 的情况下消费它。

在此之前，保留 conceptual seam 即可。

## Hard boundaries

以下规则不因 ownership 调整而改变：

```text
Reject
→ hard zero
→ Trigger 不可救活

Hard Infeasible
→ hard zero
→ Trigger 不可救活

ResolutionIncomplete
→ no scalar
```

`StateTriggerValue` 仍应遵守既有 Working budget：它只能显著改变边缘决策，不应跨越一个完整 FoodValue 档位并长期压倒 Target Relation。

## 当前主链

```text
Target Relation
→ FoodValue

Prey-conditioned current state
→ StateTriggerValue

FoodValue + StateTriggerValue
→ target-side Attack Value（conceptual seam）

species × size cohort → InterceptSpeedLimit
+ task consequence
→ Closing feasibility
→ Activity-aware soft Closing cost
→ TaskCost

Fish Condition / Feeding Motivation
→ WillingnessThreshold

AttackValue - TaskCost - Threshold
→ DecisionMargin
→ Response Projection
→ C_mode
```

## 当前裁决

- `StateTriggerValue`：prey-local / mode-local target-state ownership。
- `WillingnessThreshold`：fish-level motivation ownership。
- `AttackValue`：Working conceptual seam，不强制 runtime materialization。
- “Trigger lowers global Motivation threshold”：Rejected。

# Proposal C｜FoodValue 生产拓扑

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

FoodValue 第一版不应由多个匿名 multiplier 连乘，也不应让 `Preferred / Good / Marginal / Poor` 同时既作为手填主值、又再叠 size fit 与 Dietary Shift。

建议把职责拆成：

```text
BaseDietAffinity(prey family)
+ SizePreferenceAdjustment(prey size)
+ DietaryShiftDelta(prey family)
→ CurrentFoodValue
→ optional label projection
```

其中：

- `BaseDietAffinity` 表达该鱼种 / cohort 在参考上下文下，对某 prey family 的基础食性价值；
- `SizePreferenceAdjustment` 只表达“在可食范围内，当前猎物尺寸相对偏好尺寸的软变化”；
- `DietaryShiftDelta` 只表达上下文造成的食物之间相对偏转；
- `Preferred / Good / Marginal / Poor` 默认作为连续 FoodValue 的解释标签，而不是第二套独立 authoring 数值；
- `Reject` 保持独立 hard semantic boundary，不等于 `FoodValue=0`。

## 2. 为什么不建议乘法堆叠

不建议：

```text
FoodValue
= BasePreference
× SizeFit
× DietaryShiftMultiplier
```

问题：

1. 三个量的 authoring 标尺很难解释；
2. 多个中等减益会形成无证据的复利；
3. `DietaryShiftMultiplier` 如果对所有食物共同升降，会和 FeedingMotivation 重叠；
4. BasePreference 如果已经包含典型 prey size，再乘一份 size fit 可能重复计权。

因此第一版优先在一个共同 value scale 上合成具名 contribution。

## 3. BaseDietAffinity 的职责

`BaseDietAffinity(prey)` 回答：

> 在参考 Fish Condition、参考 prey size 下，这类 prey 对当前鱼种 / cohort 本来有多大食物价值？

它不表达：

- 当前整体有多想吃；
- 当前警惕程度；
- 拟饵呈现是否像该 prey；
- 当前 prey state 是否额外诱发攻击；
- 当前目标是否追得上。

这些分别由 FeedingMotivation、Wariness、prey support / state interpretation、StateTrigger、Closing 承接。

## 4. SizePreferenceAdjustment

尺寸处理分两层。

### 4.1 PreySizeFeasibility

如果项目未来有权威规则能确认某尺寸在物理 / 摄食方式上不可接受，应使用独立 hard boundary：

```text
PreySizeFeasibility = Infeasible
→ 当前 prey feeding path resolved zero
```

不能把它伪装成 `Reject`，因为：

```text
Reject = 食性语义拒绝
Size Infeasible = 尺寸 / 摄食方式不可行
```

首版若没有权威 hard feasibility 数据，不要凭经验制造阈值。

### 4.2 可食范围内的软尺寸偏好

在可食范围内：

```text
SizePreferenceAdjustment ≤ 0
```

参考最适尺寸处：

```text
SizePreferenceAdjustment = 0
```

偏离最适尺寸只扣减，不额外把 FoodValue 提到基础偏好之上。这样 `BaseDietAffinity` 的含义稳定：它是“参考适宜尺寸下”的基础值。

当前不冻结具体曲线。允许未来从 `prey_length / fish_length` 或其它权威尺寸关系生成；不先采用旧 probe 的 log-Gaussian 为生产规则。

## 5. DietaryShiftDelta

当前约束：

```text
DietaryShiftDelta(prey)
```

只允许改变 prey families 之间的相对 FoodValue。

禁止拥有 common-mode freedom：

```text
所有 prey 同时 +0.2
```

这会和 FeedingMotivation 无法区分。

推荐第一版对 shift 做中心化约束，例如：

```text
weighted_mean(DietaryShiftDelta) = 0
```

或未来指定 reference prey family。具体权重仍 OPEN。

`DietaryShiftDelta` 不能救活基础 `Reject`。

## 6. CurrentFoodValue

对于非 Reject、尺寸可行且必要输入已解析的 prey：

```text
CurrentFoodValue
= clamp(
    BaseDietAffinity
    + SizePreferenceAdjustment
    + DietaryShiftDelta,
    V_min,
    V_max
  )
```

这是 Working topology，不冻结 `V_min / V_max` 或各 contribution 的生产预算。

重点是：

- BaseDietAffinity 给参考点；
- size 只做相对该参考点的软惩罚；
- DietaryShift 做相对食性偏转；
- FeedingMotivation 不进入 FoodValue；
- StateTrigger 不进入 FoodValue。

## 7. Preferred / Good / Marginal / Poor

第一版建议将四档视为解释 / authoring presentation label：

```text
continuous CurrentFoodValue
→ Preferred / Good / Marginal / Poor label
```

而不是：

```text
作者手填 Good
→ 映射 0.8
→ 再乘 size fit
→ 再叠 Dietary Shift
```

如果编辑器需要人类友好的离散输入，可以允许作者填 class，但 Bake 必须将其解析成唯一连续 anchor，运行时只消费连续 FoodValue；不能同时保留两套独立真值。

`Reject` 例外：它不是最低档连续值，而是 typed hard boundary。

## 8. 与 FeedingMotivation 的边界

必须保持：

```text
FoodValue
→ 这个 prey 值不值得吃

FeedingMotivation
→ 当前整体愿不愿意为食物出手
```

因此：

- 某 prey 因 Dietary Shift 相对变好，FoodValue 上升；
- 当前所有 prey 都更容易被接受，优先由 FeedingMotivation / WillingnessThreshold 表达；
- 不允许用 Dietary Shift 同时抬所有 FoodValue 模拟“好鱼口”。

## 9. 与 prey support / StateTrigger 的边界

FoodValue 不表达“像不像 prey”。

```text
prey support
→ 这个解释有多少证据
```

FoodValue 只在该 prey interpretation 已被支持后评价其食物价值。

StateTrigger 也不并入 FoodValue：

```text
FoodValue
+ StateTriggerValue
→ attack-side positive value
```

这样基础偏好与当前猎物状态的额外诱发不会混成一份难以解释的 authoring 数值。

## 10. Unknown 与 hard boundaries

```text
BaseDietAffinity = Unknown
→ FoodValue ResolutionIncomplete
```

```text
required SizePreference input = Unknown
→ FoodValue ResolutionIncomplete
```

```text
DietaryShift required but Unknown
→ FoodValue ResolutionIncomplete
```

不能补默认 0，除非 profile 明确声明该 shift 维度 Disabled / NotApplicable。

```text
TargetRelation = Reject
→ resolved zero feeding path
```

Reject 不进入普通连续合成。

## 11. 当前 OPEN

仍未闭合：

- BaseDietAffinity 的 production anchor；
- `Preferred / Good / Marginal / Poor` 的连续区间；
- size preference 的真实输入量与曲线；
- 是否需要独立 PreySizeFeasibility hard gate；
- DietaryShift 中心化权重；
- species / cohort 是否共享同一 FoodValue scale；
- FoodValue contribution 的最大允许 shift budget；
- editor authoring 用 class 还是连续值，或 class authoring + Bake anchor。

本页只闭合职责与生产拓扑，不从旧 probe 示例值晋升生产参数。

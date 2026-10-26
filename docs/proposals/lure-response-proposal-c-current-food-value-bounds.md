# Proposal C｜CurrentFoodValue Bound Contract

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

第一版将完整 `CurrentFoodValue` 的合法连续区间固定为：

```text
CurrentFoodValue ∈ [0, 1]
```

这不是只约束 `BaseDietAffinity`，而是约束经过尺寸偏好和当前 Dietary Shift 修正后的最终 prey-specific FoodValue。

对于非 Reject、尺寸可行且必要输入已解析的 prey：

```text
RawFoodValue
= BaseDietAffinity
+ SizePreferenceAdjustment
+ DietaryShiftDelta

CurrentFoodValue
= clamp(RawFoodValue, 0, 1)
```

当前 FoodValue gauge 因此保持：

```text
0 = 连续 Feeding target 的最低可表达 food value
1 = 连续 Feeding target 的最高可表达 food value
Reject = 独立 hard semantic boundary，不在连续轴上
```

## 2. 为什么不允许 1.2 / -0.2 成为隐藏有效值

此前 relation scale 已固定：

```text
Preferred = 1.0
Poor      = 0.0
```

如果后续允许：

```text
Preferred + DietaryShift = 1.2
Poor + SizePenalty = -0.2
```

则 `[0,1]` 只剩 authoring 外观，而不再是 DecisionMargin 的真实标尺。

这会带来两个问题：

1. Trigger / Motivation / Closing / Risk 等 effect budget 无法再与 FoodValue 的固定跨度比较；
2. `Preferred=1 / Poor=0` 不再真正定义 gauge，后续 calibration 会重新出现整体尺度漂移。

因此第一版规定：

> 超出 `[0,1]` 的 RawFoodValue 不保留隐藏 residual；边界就是当前模型可表达的 prey-specific value 上下限。

## 3. 为什么仍采用 additive + clamp

第一版不采用按剩余 headroom / footroom 自动缩放的 bounded nonlinear adjustment，例如：

```text
positive_delta_effect = delta × (1 - current_value)
negative_delta_effect = delta × current_value
```

因为这样同一个 `DietaryShiftDelta=+0.10` 在不同 BaseDietAffinity 上会变成不同的 DecisionMargin 实际单位，破坏已经建立的共同 value scale。

当前选择保持：

```text
+0.10 FoodValue
```

在整个内部标尺上始终表示同一个 margin 单位；只在越过明确语义边界时发生饱和。

clamp 因此不是实现补丁，而是 FoodValue range contract 的一部分。

## 4. SizePreferenceAdjustment 的边界

当前 BaseDietAffinity 的定义是：

> 在参考上下文、参考适宜 prey size 下，这类 prey 的基础食物价值。

因此 SizePreference 第一版只允许做非正修正：

```text
SizePreferenceAdjustment <= 0
```

参考适宜尺寸：

```text
SizePreferenceAdjustment = 0
```

偏离适宜尺寸：

```text
SizePreferenceAdjustment < 0
```

它不能把 FoodValue 推到 BaseDietAffinity 之上。

若未来有权威证据表明某个“参考尺寸”只是中性点而不是最佳点，需要先改 BaseDietAffinity 的定义，再开放正向 size adjustment；不能在现有定义上直接加正 bonus。

### 4.1 不用负 FoodValue 表达尺寸不可行

如果某 prey size 具有明确物理 / 摄食方式 hard infeasible：

```text
PreySizeFeasibility = Infeasible
→ whole prey feeding path resolved zero
```

不能靠：

```text
SizePreferenceAdjustment = -999
```

来模拟 hard gate。

如果没有权威 hard feasibility 数据，维持 soft penalty，不凭经验制造 hard cutoff。

## 5. DietaryShiftDelta 的边界

Dietary Shift 仍表达当前上下文下 prey families 之间的相对偏转：

```text
DietaryShiftDelta(prey family)
```

它可以正也可以负，但必须继续满足：

- 不拥有 common-mode freedom；
- 不允许把 Reject 救活；
- 使用与 FoodValue / DecisionMargin 相同的数值单位；
- 最终结果受 `[0,1]` range contract 约束。

因此：

```text
Base = 0.70
DietaryShift = +0.10
→ 0.80
```

和：

```text
Base = 0.95
DietaryShift = +0.10
→ Raw = 1.05
→ Current = 1.00
```

都合法。

后一个 case 中超出的 `0.05` 不保留为隐藏价值，也不转移到 Trigger / Motivation。

## 6. 饱和的语义

### 上饱和

```text
CurrentFoodValue = 1
```

只表示：

> 当前 prey-specific food value 已达到本模型最高可表达值。

不表示：

- 必定攻击；
- C=1；
- 无视 Closing / Prediction / Risk；
- 无视低 FeedingMotivation。

这些仍通过 DecisionMargin 生效。

### 下饱和

```text
CurrentFoodValue = 0
```

仍然不同于 Reject。

它表示：

> 这是已承认的 Feeding target，但当前连续 food value 已到模型下限。

因此仍可进入 DecisionMargin；在极端有利 Motivation / Trigger / burden 组合下，理论上仍可能越线。

`Reject` 则始终绕过普通 projection，直接 whole-path zero。

## 7. 多个 adjustment 的合成

第一版仍允许：

```text
BaseDietAffinity
+ SizePreferenceAdjustment
+ DietaryShiftDelta
```

在 clamp 前做一次 additive composition。

这样 SizePreference 与 DietaryShift 在共同 DecisionMargin 单位中可比较，也避免因为先后顺序造成不同结果。

拒绝首版使用：

```text
clamp(Base + Size)
再 + DietaryShift
```

或：

```text
clamp(Base + DietaryShift)
再 + Size
```

因为中间 clamp 会让合成结果依赖计算顺序。

唯一合法第一版顺序：

```text
resolve all admitted contributions
→ sum once
→ clamp once
```

## 8. Dietary Shift 的中心化仍在 clamp 前定义

Dietary Shift 不得借饱和产生隐性的 common-mode。

若未来使用：

```text
weighted_mean(DietaryShiftDelta) = 0
```

这个约束作用于 **raw DietaryShiftDelta profile**，不是 clamp 后的 CurrentFoodValue 结果。

原因：若很多高 Base prey 在上边界饱和，clamp 后的平均实际变化可能不再为零；这属于边界压缩后的结果，不应反过来重定义 Dietary Shift profile。

如果生产数据中大量 profile 长期饱和，说明 anchor / shift budget 或 relation design 需要重标定，而不是做二次 renormalization。

## 9. 饱和率是必须监控的 calibration 指标

clamp 合法，但不能让它大量吞掉系统差异。

后续 simulation / telemetry 至少应记录：

```text
upper_saturation_rate
lower_saturation_rate
saturation_by_relation_class
saturation_by_species/cohort
saturation_by_dietary_shift_profile
```

Working guardrail：

> 如果大量正常 case 在上/下边界长期饱和，应优先检查 Base anchor、SizePreference budget、DietaryShift budget，而不是接受“clamp 反正能跑”。

当前不冻结具体可接受百分比。

## 10. 与现有 joint calibration 的关系

当前 Working seed：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00
```

因此：

- Preferred 的正向 DietaryShift 默认可能直接饱和，不产生超过1的额外 FoodValue；
- Poor 的负向 SizePreference / DietaryShift 默认可能直接饱和在0；
- 这两类饱和是边界语义允许的；
- 若它们在真实 production profile 中过于常见，说明 relation anchor 或 adjustment budget 设计需要复审。

不因为边界饱和而新增 `SuperPreferred` 或负 FoodValue 档。

## 11. Unknown / Disabled / hard boundaries

```text
BaseDietAffinity = Unknown
→ ResolutionIncomplete
```

```text
required SizePreference input = Unknown
→ ResolutionIncomplete
```

```text
required DietaryShift = Unknown
→ ResolutionIncomplete
```

Unknown 不进入 sum，也不能补0。

显式 Disabled / NotApplicable contribution 不参与 sum。

```text
TargetRelation = Reject
→ resolved whole-prey Feeding zero
```

```text
PreySizeFeasibility = Infeasible
→ resolved whole-prey Feeding zero
```

这两个 hard boundary 都不靠 clamp 实现。

## 12. 当前 OPEN

仍未闭合：

- SizePreferenceAdjustment 的生产曲线和最大 soft penalty；
- DietaryShiftDelta 的 production budget；
- DietaryShift 中心化权重；
- 是否需要 PreySizeFeasibility hard gate，以及其权威数据来源；
- production saturation-rate guardrail；
- 当前约200鱼种的实际 distribution 是否会导致边界大量饱和。

本页冻结 `[0,1]` 作为完整 CurrentFoodValue range、单次 additive composition + 单次 clamp、SizePreference 非正职责，以及 Reject / Size Infeasible 不靠 clamp 表达的边界。
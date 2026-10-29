# Proposal C｜Activity Bake Contract

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

本轮接受上游方向调整：`FunctionalCapacity` 不再作为 Proposal C 的必要动态输入。Fish Condition Bake 面向 Response 输出至少四个语义彼此独立的结果：

```text
Activity
FeedingMotivation
Wariness
DietaryShift
```

其中 `Activity` 只回答：

> 当前这类鱼在当前环境与时间上下文下，主动发起和维持运动行为有多容易。

它不是：

- 物种/体型决定的物理游动速度极限；
- 摄食意愿；
- 风险回避；
- 食物偏好；
- 总体“鱼情好坏”。

## 2. 与其它三个 Bake 输出的边界

| 输出 | 回答的问题 | Proposal C 当前消费位置 |
|---|---|---|
| Activity | 当前主动运动有多容易 | Closing 的 soft cost |
| FeedingMotivation | 当前有多愿意为了食物出手 | WillingnessThreshold |
| Wariness | 当前有多受风险/可疑线索抑制 | 独立 Wariness response path，尚待闭合 |
| DietaryShift | 当前食性相对基线如何偏转 | TargetRelation / FoodValue 上游 |

同一个原始原因可以同时影响多个 Bake 输出，但必须通过各自的 species/context-specific 解释分别得到结果。例如低温可以同时压低 Activity 和 FeedingMotivation，但不能因为 Activity 低就在 Feeding Response 内自动降低 Motivation。

## 3. Activity 标尺

第一版使用归一化 `[0,1]` 标尺：

```text
1.0 = 参考高活跃状态；不增加额外 pursuit soft cost
0.0 = 强低活跃状态；主动追赶明显不利，但不表示失去物理运动能力
```

中间值只表达相对活跃程度，不解释成概率。

特别注意：

```text
Activity = 0
≠ InterceptSpeedLimit = 0
```

低 Activity 的鱼仍可能攻击停顿、缓慢或朝鱼移动的目标。

## 4. 物理上限与 Activity 分离

物理追赶上限来自鱼种 / 体型配置：

```text
species + size cohort
→ InterceptSpeedLimit
```

若 response 前已有具体个体长度，可使用具体长度对应的速度上限；否则使用当前 `species × size cohort` 的代表长度所烘出的速度上限。

Activity 不修改该能力尺度。

第一版 Closing：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
u_close(theta) = max(0, q * cos(theta))

ClosingCost(theta)
= K_close * u_close(theta)^2
  * ActivityCostMultiplier(Activity)

`u_close >= 1` 表示高 Closing burden；没有独立 encounter-geometry / reaction-window contract 时，不直接输出 `C_conditional(theta)=0`。
```

Activity 只影响已经物理可行的追赶任务有多吃力。

## 5. 第一版 ActivityCostMultiplier

最小自由度 Working 候选：

```text
ActivityCostMultiplier(A)
= 1 + K_activity * (1 - A)
```

满足：

```text
A = 1 → multiplier = 1
A ↓   → pursuit soft cost 单调上升
u_close = 0 → ClosingCost = 0，无 Activity 惩罚
```

`K_activity` 尚未 calibration。

不采用：

```text
InterceptSpeedLimit *= Activity
```

因为这会把“当前不活跃”偷换成“当前物理极速下降”，并使 Activity 与已删除的 FunctionalCapacity 重新同义。

## 6. Bake 输入如何聚合

Activity 的 raw causes 可以包括但不限于：

- period / circadian activity tendency；
- temperature suitability 对主动运动的限制；
- dissolved oxygen 对主动运动的限制；
- 已准入的其它 species/context-specific activity cause。

本页不把这些 raw causes 的具体曲线定成 Current。

第一版 reducer 倾向把每条已准入原因解释成“在该原因约束下，当前最多支持多少 Activity”：

```text
A_period
A_temperature
A_oxygen
A_other...
```

然后：

```text
Activity = min(enabled resolved supports)
```

这是一版保守的 bottleneck reducer。它避免无证据地把多个中等减益连续相乘，例如 `0.8 * 0.8 * 0.8`。

如果未来受控案例证明多个原因存在稳定、可学习的累积抑制，再重新打开 reducer；当前不提前增加 weighted sum / product / generalized mean。

## 7. Unknown / Disabled / NotApplicable

必须区分：

```text
required Activity cause = Unknown
→ Activity = Unknown
→ 依赖 Activity 的 Closing resolution incomplete
```

不能把 Unknown 当 1 或 0。

显式未启用 / 不适用的 cause 不参加 `min`。

`min` 只聚合已声明属于本 Activity contract 的 sibling causes。

## 8. 代表长度与速度上限

代表长度优先级：

```text
若已有具体个体长度
→ 使用具体长度

否则
→ 使用 species × size cohort 的代表长度
```

cohort 代表长度优先取真实生成分布的中位数；没有生成分布时，才退化到 authoring reference / 区间中点。

推荐在 Bake 阶段直接得到：

```text
SpeciesCohortMotionProfile {
  representative_length,
  intercept_speed_limit
}
```

runtime Response 直接查 `intercept_speed_limit`，不必重复运行 size scaling。

如果同一 cohort 的尺寸跨度已经足以让常见拟饵速度跨过 hard-feasibility 边界，则一个代表长度不再合格。优先拆 cohort；必要时才考虑尺寸分布积分。

## 9. 与策略体验的关系

Activity 应购买的主要策略故事：

```text
低 Activity
+ 高速背离 presentation
→ Closing soft cost 显著提高

低 Activity
+ 慢速 / pause presentation
→ Closing burden 小，得到明显 rescue
```

但：

```text
低 Activity
≠ 自动低 FeedingMotivation
≠ 自动高 Wariness
≠ 自动改变 DietaryShift
```

因此玩家可以遇到例如：

- Activity 低但 FeedingMotivation 高：想吃，但更适合慢饵；
- Activity 高但 FeedingMotivation 低：游得动，但不太愿意为食物出手；
- Activity 高且 Wariness 高：有行动能力，但对可疑呈现谨慎。

这些组合正是保留四个 Bake 输出而不压成一个 FishCondition scalar 的价值。

## 10. Supersession

本页替代 Proposal C 中把 `FunctionalCapacity` 作为 Closing 动态能力输入的 Working 路线。

历史文档 `lure-response-proposal-c-functional-capacity-to-intercept.md` 保留用于推导考古，但不再代表当前 Proposal C 推荐结构。

当前链条改为：

```text
species × size cohort config
→ InterceptSpeedLimit
→ hard feasibility

Fish Condition Bake
→ Activity
→ Closing soft-cost multiplier

Fish Condition Bake
→ FeedingMotivation
→ WillingnessThreshold
```

## 11. 当前 OPEN

- `K_activity` calibration；
- Activity raw-cause 的具体 production curves；
- `min` reducer 是否经 controlled fixture 后仍成立；
- Activity 是否还应独立影响 Prediction recovery；首版默认不影响，避免扩散；
- species × size cohort 的 `intercept_speed_limit` 数据生产方法；
- cohort 尺寸跨度何时必须拆分的自动检查阈值。

# Proposal C｜Activity 与 Closing 的职责拆分

状态：Working Hypothesis / Candidate。不是 Current，不是生产参数。

## 1. 结论

删除 `FunctionalCapacity` 后，不把它原有的全部语义塞进 `Activity`。

第一版把静态追赶能力与动态活跃度拆开：

```text
Species / size cohort configuration
→ InterceptSpeedLimit
→ Closing burden / capability scale

Activity
→ ActivePursuitCostMultiplier
→ soft Closing cost
```

因此：

- `InterceptSpeedLimit` 回答“物理上是否追得上”；
- `Activity` 回答“当前状态下，主动追赶这件事有多费劲 / 多不自然”；
- `Feeding Motivation` 回答“值不值得为了食物出手”；
- `Wariness` 回答“面对风险 / 可疑呈现是否抑制出击”；
- `Dietary Shift` 改变当前食性评价，不改运动能力。

## 2. InterceptSpeedLimit 从哪里来

首版推荐在 Bake 阶段针对 `species × size cohort` 生成一个代表性的短时追赶速度上限：

```text
FishSpeciesConfig
├─ reference_length
├─ reference_intercept_speed
└─ size_scaling_rule

Species × SizeCohort
├─ representative_length
└─ baked_intercept_speed_limit
```

runtime 只读取当前候选 cohort 的 `baked_intercept_speed_limit`，不再即时重做生物学推导。

若 response 前已经存在权威具体个体长度，可以直接用个体长度求值；否则使用 cohort 代表长度。

## 3. 代表长度

优先级：

```text
1. 已有权威具体个体长度
2. 当前 species × cohort 的生成分布中位数
3. 若没有分布，使用该 cohort 的 authoring reference length
4. 最后才退化到 species reference length
```

不建议使用“整个鱼种平均长度”。同一鱼种的小个体与大个体应有不同能力尺度。

如果 cohort 只有 `[min_length, max_length]` 且明确按长度均匀生成，则中位数等于区间中点；如果生成分布定义在体重、等级或其它空间上，应先按真实生成规则求长度中位数，不应直接取长度区间中点。

### 3.1 何时一个代表长度不够

代表长度只是为了避免在 response 前额外采样隐藏个体。

若同一 cohort 内的尺寸跨度已经导致：

- `InterceptSpeedLimit` 明显跨档；或
- 同一 retrieve 在 cohort 内一部分可追、一部分不可追；或
- response ranking 对尺寸分布高度敏感；

则不应继续靠一个均值 / 中位数硬撑。优先：

1. 拆更细 cohort；
2. 若确有必要，再对 size distribution 做显式积分。

首版不为了精度提前引入 size micro-sampling。

## 4. Activity 不修改 hard speed limit

Activity 不是“剩余多少物理极速”。

不采用：

```text
EffectiveSpeedLimit = InterceptSpeedLimit × Activity
```

否则低 Activity 会把“当前不爱动”偷换成“物理上追不上”，并与 Feeding Motivation 的低响应效应混淆。

首版固定：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
u_close(theta) = max(0, q * cos(theta))

ClosingCost(theta)
= K_close * u_close(theta)^2 * ActivityCostMultiplier(A)

`u_close >= 1` 表示高 Closing burden；没有独立 encounter-geometry / reaction-window contract 时，不直接输出 `C_conditional(theta)=0`。
高 Closing burden 仍由完整 DecisionMargin 决定响应是否归零。
```

其中：

- `A` 为已 Bake 的 Activity，Working 假定归一化到 `[0,1]`；
- `A=1` 是 reference-active 状态，multiplier = 1；
- Activity 越低，主动追赶成本越高；
- `K_activity` 尚未标定；
- 此线性 multiplier 只是最小自由度 Working shape，不是生物学定律。

这样有一个重要性质：

```text
u_close ≈ 0
→ Activity 几乎不产生负面影响
```

因此低 Activity 的鱼仍可对停顿、慢速或迎面而来的目标产生响应；但高速背离目标会明显更差。

这正是“低活性鱼需要放慢、停顿、降低追赶要求”的策略故事。

## 6. Activity 与 Feeding Motivation 的边界

固定：

```text
Activity
→ pursuit execution cost

Feeding Motivation
→ willingness threshold
```

同一温度、时段、缺氧等上游原因可以同时影响两者，但 Bake 必须分别产出。

禁止：

- Activity 再修改 `WillingnessThreshold`；
- Feeding Motivation 再修改 `InterceptSpeedLimit` 或 ClosingCost；
- 因同一个 raw cause 已进入 Activity，又在 Response 层再追加一次环境 penalty。

因此可以出现合法组合：

```text
Activity 低 + Motivation 高
→ 很想吃，但不适合追很快的目标

Activity 高 + Motivation 低
→ 追得动，但不太值得出手
```

这正是保留两维的意义。

## 7. Wariness 与 Dietary Shift

`Wariness` 不进入本页 Closing math。它应影响风险 / 可疑目标的响应抑制，而不是把谨慎解释成游不动。

`Dietary Shift` 应修改当前 prey 的 Target Relation / FoodValue，不能改变 Closing feasibility。

四个 Bake 输出因此形成清晰职责：

```text
Activity          → 动作执行活跃度 / pursuit cost
Feeding Motivation→ 摄食意愿门槛
Wariness          → 风险抑制
Dietary Shift     → 当前食性偏转
```

## 8. Unknown 与 zero

`Activity = Unknown` 不是 0。若 Activity 是本 mode 的必要输入，则保持 `ResolutionIncomplete`。

`Activity = 0` 也不表示物理无法游动；它只表示当前处于极低执行活跃度。是否允许 A=0 仍产生有限 soft cost，由 `K_activity` 与生产标尺共同决定。

## 9. 当前缺口

仍未闭合：

- Activity 的 Bake 语义与 0/1 anchor；
- `K_activity`；
- `reference_intercept_speed` 的生产来源；
- size scaling rule；
- cohort representative length 的实际生产数据源；
- cohort 宽度何时必须拆分的验收阈值；
- 是否存在极端生理状态需要独立于 Activity 的 hard locomotor disable。若存在，应由具名状态另行 admission，而不是重新恢复宽泛 FunctionalCapacity。

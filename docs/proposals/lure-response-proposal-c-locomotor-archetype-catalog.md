# Proposal C｜Locomotor Archetype Catalog

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`LocomotorArchetype` 只服务于当前 Proposal C Closing 所实际消费的结构能力：

```text
ReferenceInterceptSpeed
SizeScalingRule
```

因此 archetype 的 admission 标准不是鱼类学分类，而是：

> 在相同体长、相同 lure-speed basket 下，是否会形成稳定、玩家可感知的 Closing 行为差异，并且这种差异不能只靠 species sparse override 更经济地表达。

按当前模型能力，第一版推荐只保留 **3 个基础 archetype**：

```text
HighClosing
GeneralClosing
LowClosing
```

这三个名称是生产 authoring profile，不是自然界正式生态分类。

首版不正式建立：

```text
BurstAmbushPredator
ManeuverOriented
SustainedCruiser
```

除非后续 runtime 增加了能真正消费这些差异的独立参数。

## 2. 为什么第一版只需要 3 类

当前 Closing 核心：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
u_close(theta) = max(0, q * directional_cosine(theta))
```

所以 locomotor profile 在当前 Response 中真正能改变的只有：

- 同一 lure speed 下的 `q`；
- ClosingCost 分布；
- angle-local hard-infeasible share。

如果两个所谓 archetype 最终只是拥有不同名称，但能被同一个 `ReferenceInterceptSpeed` 与同一个 size-scaling profile 完整表达，那么它们不应该拆成两个 archetype。

## 3. 三个基础 archetype 的行为语义

### HighClosing

用途：短时 Closing 能力明显高于项目常规鱼类基线的 species / cohort。

预期在 lure-speed basket 中：

```text
Slow
→ Closing burden 很低

Normal Steady
→ 低到普通 burden

Fast Search
→ 仍有较大比例 bearing 保持可行

Burst Peak
→ 开始出现明显 cost / 局部 hard-infeasible，
   但不应像 General / LowClosing 那样快速崩塌
```

这里不等于“高速巡游鱼”这一生态标签；只表达当前模型需要的 Closing 能力档位。

### GeneralClosing

项目 reference profile。

预期：

```text
Slow
→ 低 burden

Normal Steady
→ ordinary Closing burden

Fast Search
→ burden 明显抬升，部分条件可能接近能力边界

Burst Peak
→ 可出现较明显 angle-local hard-infeasible
```

`K_close` 的主要 reference calibration 应优先围绕该 archetype 的 Normal Steady basket。

### LowClosing

用途：当前模型下短时追赶明显弱于常规 baseline 的 species / cohort。

预期：

```text
Pause / Slow
→ 仍可形成合理 Feeding response

Normal Steady
→ burden 已明显高于 General

Fast Search
→ 较高 hard-infeasible share

Burst Peak
→ 大量 bearing 不可行
```

它不代表“鱼整体行动迟缓”；Activity 是另一条 Fish Condition 状态轴。

## 4. 为什么暂不设 BurstAmbushPredator

现实上，伏击型鱼可能具有很强短时爆发能力，但未必适合持续追逐。

然而当前模型没有：

```text
pursuit_horizon
burst_duration
acceleration_budget
sustained_vs_burst capacity
```

只有单一 `InterceptSpeedLimit`。

因此若现在增加：

```text
BurstAmbushPredator
```

最终仍只能映射到一个速度标量。它与 `HighClosing` 的数值区别只能靠人为另配一个 baseline，不能购买新的运行时语义。

第一版处理方式：

- 若某伏击 species 的短时 Closing 确实高，映射 `HighClosing`；
- 若只是略有差异，用 species override；
- 只有未来引入 pursuit horizon / burst duration 等独立机制后，再重新打开该 archetype。

## 5. 为什么暂不设 ManeuverOriented

当前 Proposal C 已明确：

```text
trajectory change
→ PredictionChallenge
→ PredictionCost
```

而且没有合法鱼点 / 朝向时，不引入 fish-turn-rate capacity。

因此“机动性强”不能再通过 LocomotorArchetype 给 Closing 一份 bonus，否则会把 maneuver 能力和直线 Closing 能力混在一起。

未来如果合法引入：

```text
TurnCapacity
AccelerationCapacity
```

再讨论是否需要独立 maneuver archetype。

## 6. Archetype 只给默认值，species / cohort 可 sparse override

建议 authoring：

```text
LocomotorArchetype
├─ default ReferenceInterceptSpeed profile
└─ default SizeScalingRule

Species
├─ archetype_id
├─ optional reference-speed override
└─ optional size-scaling override
```

Cohort 通常只通过 representative length 进入 size scaling；只有存在明确的 ontogenetic locomotor regime change，才允许 cohort 改 archetype 或 profile。

不能因为 juvenile / adult 名称不同就自动切 archetype。

## 7. Archetype admission / split rule

新增 locomotor archetype 至少满足：

1. 在 lure-speed basket 中形成稳定不同的 Closing ranking；
2. 差异不能只靠少量 species override 经济表达；
3. 差异对应当前 runtime 已消费的参数，而不是尚未实现的生态属性；
4. 加入后显著降低 widespread override rate；
5. 不与 Activity、Prediction、Wariness 等已有 owner 重复。

例如，如果大量伏击 species 都需要：

```text
Normal Steady ≈ General
Burst Peak 显著强于 General
```

但单一 `InterceptSpeedLimit` 无法同时表达这两个条件，正确动作不是立刻新增 archetype，而是承认 **当前 runtime representation 不够**。只有先增加 burst/sustained 维度，archetype split 才有意义。

## 8. Coverage test

拿到生产鱼种表后，应统计：

```text
species count per archetype
override rate per archetype
reference-speed override distribution
size-scaling override distribution
lure-speed basket response separation
```

重点诊断：

- 某 archetype 只有极少 species；
- 两个 archetype 的 resolved speed profile 几乎重合；
- 某 archetype 大量 species 都向同一方向 override；
- 大量 species 无法用三个 archetype + sparse override 表达。

出现这些情况时，应合并 / 重划 archetype，而不是继续堆 override。

## 9. 与真实 locomotion evidence 的关系

外部真实游泳能力资料用于：

```text
species evidence
→ locomotor ordering / plausible range
→ archetype assignment / override evidence
```

不能机械地：

```text
Ucrit / burst speed label
→ archetype name
```

尤其 `HighClosing / GeneralClosing / LowClosing` 是项目内部 Closing 行为档位，不宣称等价于某个实验 swimming-performance taxonomy。

## 10. 当前 OPEN

- 三个 archetype 的 production `ReferenceInterceptSpeed` anchor；
- 共用还是分 archetype 的 size-scaling exponent / profile；
- 约 200 production species 的真实覆盖与 override rate；
- 生产 lure-speed telemetry / basket 的绝对 m/s 分布；
- 2D / 3D bearing prior；
- 是否未来因 burst/sustained 差异增加第二个 locomotor runtime 维度。

本页冻结第一版 archetype 数量与职责边界，不冻结生产速度参数。
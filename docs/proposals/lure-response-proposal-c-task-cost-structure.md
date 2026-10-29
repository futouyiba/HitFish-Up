# Proposal C：TaskCost 结构收敛

> 状态：Working Hypothesis / probe-backed，不是生产冻结公式。

## Closing hard feasibility 与 soft cost 的分工

当前 baseline 不建立旧的 `FunctionalCapacity` 总对象，也不把 `InterceptSpeedLimit × Activity` 做成复合 hard gate。

```text
species × size cohort → InterceptSpeedLimit
+ Closing demand
→ Closing physically feasible / infeasible

Activity
→ soft Closing cost only when Closing is physically feasible
```

`InterceptSpeedLimit` 提供 Closing burden 的能力尺度，不单独证明完整 encounter feasibility；`Activity` 只负责 soft Closing cost。其它 task axis 只有在有独立物理语义和反事实证据时才可单独 admission。`Unknown` 不等于 zero、`Disabled` 或 `NotApplicable`。

## 结论

当前不建议直接把 physically-feasible task consequence 压成一个总标量后写死 `TaskCost = k × S^p`。

更稳的第一版结构是：

1. 先按任务轴分别计算能力利用率：

```text
u_intercept = InterceptDemand / InterceptCapacity
u_maneuver  = ManeuverDemand  / ManeuverCapacity
```

2. 只有在已经拥有独立的 physical task contract 时，才允许把某个 task axis 的超限标为 `Infeasible`。当前 `u_close > 1` 只表示径向 Closing burden 很高，不能单独把完整 feeding opportunity 判为 `Infeasible`；`FoodValue` / `Motivation` 也不能把真正已知的 physical infeasibility 补回来。

3. 在当前已准入的 soft Closing 区间内，成本由已确认的任务轴主导；第二轴只有在拥有独立物理语义、来源和反事实证据时才能 admission：

```text
axisCost(u) = u^p
TaskCost = k × [max(axisCost_i) + rho × min(axisCost_i)]
```

其中 `k / p / rho` 都只是标定参数。当前 probe 用 `k=0.33, p=4, rho=0.25` 只为验证拓扑，不是生物学常数。

## 为什么不只用 max(Strain)

如果只用：

```text
physically-feasible task consequence = max(u_intercept, u_maneuver)
TaskCost = k × physically-feasible task consequence^p
```

那么下面两种任务会被判成完全一样：

```text
直线追逐：       intercept=0.6, maneuver=0.1
追逐 + 大幅转向：intercept=0.6, maneuver=0.6
```

但第二种明显要求更多定位和机动。现有鱼类捕食运动学也支持定位、转向、制动与 prey capture 是独立的重要动作要求。

因此需要保留第二轴的独立贡献，但不应简单全额相加，否则容易把共享的运动负担重复结算。

## 当前 Working 形式

当前第一版只承认 Closing 的 soft burden。真正的 hard gate 保留给未来的 encounter geometry / reaction-window contract：

```text
u_close(theta) = max(0, q * cos(theta))
ClosingCost(theta) = K_close × u_close(theta)^2 × ActivityCostMultiplier(Activity)
```

`u_close > 1` 不自动输出 `Infeasible` 或 `C_mode = 0`。如果未来 admission 了另一个拥有独立物理 contract 的 task axis，它必须单独声明 hard-feasibility owner；不能因为采用 `rho` 就自动取得 hard-gate authority。

当前的第二轴 surcharge 保持 Deferred，不进入第一版 numeric core，直到它拥有独立玩家策略故事、数据来源、owner 和不重复计权的反事实证据。

## 当前 probe 行为

使用 Working 参数 `k=.33, p=4, rho=.25`：

| 场景 | Intercept | Maneuver | TaskCost |
|---|---:|---:|---:|
| easy straight | 0.30 | 0.10 | 0.0027 |
| moderate straight | 0.60 | 0.10 | 0.0428 |
| moderate + turn | 0.60 | 0.60 | 0.0535 |
| hard straight | 0.80 | 0.10 | 0.1352 |
| hard + maneuver | 0.80 | 0.60 | 0.1459 |
| near-limit straight | 0.95 | 0.10 | 0.2688 |
| near-limit both | 0.95 | 0.90 | 0.3229 |

这个形状满足当前希望的三件事：

- 中低负荷便宜；
- 接近能力边界时成本快速上升；
- 同样 peak load 下，额外高 maneuver 会更难，但不是再乘一次完整 penalty。

## 与生物学证据的边界

外部研究支持的是方向，而不是当前具体公式：

- 大口黑鲈捕食时需要 locomotor positioning、制动与口部相对目标的定位；
- 高速游动的能耗通常非线性增加；
- 转向可能带来独立运动成本。

这些证据足以支持“不能只看一个速度系数”和“接近能力极限时成本应明显上升”，但不足以证明 `p=4` 或 `rho=.25`。

## 验收约束

后续任何 TaskCost 形式至少要满足：

1. 当前已明确的 Closing 负担不因 `u_close > 1` 自动取得完整任务的 hard-gate authority；真正的 hard gate 需要独立 physical task contract；
2. 固定其它量，任一已准入利用率上升不能让 TaskCost 下降；
3. 中低利用率不应被过度惩罚；
4. 接近能力边界时成本应快速上升；
5. 同 peak utilization 下，额外显著 maneuver 只有在独立 owner 与反事实 admission 通过后才能增加成本；
6. 第二轴附加成本不能等价于再完整乘一遍 response penalty；
7. Activity 的 soft Closing cost 不能修改 `InterceptSpeedLimit`，也不能制造第二个 hard gate。

## 仍未冻结

- `InterceptDemand / Capacity` 的具体单位与标准化方式；
- `ManeuverDemand / Capacity` 的具体构成；
- encounter geometry / reaction-window contract 何时足以准入真正 hard feasibility；
- `p` 是否真需要接近 4；
- `rho` 是否值得成为生产参数，还是能由更底层的 task composition 自然导出；
- 两轴是否足够，还是后续反例要求第三个独立任务轴。

在 hard-feasibility contract 缺失时，`rho` 与多轴 TaskCost 保持 Deferred，不因本轮术语迁移升格。

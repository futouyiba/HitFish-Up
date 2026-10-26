# Proposal C：TaskCost 结构收敛

> 状态：Working Hypothesis / probe-backed，不是生产冻结公式。

## 结论

当前不建议直接把 `TaskStrain` 压成一个总标量后写死 `TaskCost = k × S^p`。

更稳的第一版结构是：

1. 先按任务轴分别计算能力利用率：

```text
u_intercept = InterceptDemand / InterceptCapacity
u_maneuver  = ManeuverDemand  / ManeuverCapacity
```

2. 任一轴 `u > 1` 时，任务为 `Infeasible`，直接 hard gate；FoodValue / Motivation 不得补偿。

3. 在可行区间内，成本由最吃紧的轴主导，同时允许第二轴提供有限 surcharge：

```text
axisCost(u) = u^p
TaskCost = k × [max(axisCost_i) + rho × min(axisCost_i)]
```

其中 `k / p / rho` 都只是标定参数。当前 probe 用 `k=0.33, p=4, rho=0.25` 只为验证拓扑，不是生物学常数。

## 为什么不只用 max(Strain)

如果只用：

```text
TaskStrain = max(u_intercept, u_maneuver)
TaskCost = k × TaskStrain^p
```

那么下面两种任务会被判成完全一样：

```text
直线追逐：       intercept=0.6, maneuver=0.1
追逐 + 大幅转向：intercept=0.6, maneuver=0.6
```

但第二种明显要求更多定位和机动。现有鱼类捕食运动学也支持定位、转向、制动与 prey capture 是独立的重要动作要求。

因此需要保留第二轴的独立贡献，但不应简单全额相加，否则容易把共享的运动负担重复结算。

## 当前 Working 形式

```text
Hard gate:
max(u_intercept, u_maneuver) > 1
→ Infeasible
→ C_mode = 0

Otherwise:
ci = u_intercept^p
cm = u_maneuver^p
TaskCost = k × [max(ci, cm) + rho × min(ci, cm)]
```

`rho` 的含义是：第二个同时存在的任务负担，只作为有限附加成本，而不是第二次完整惩罚。

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

1. 任一轴超过能力边界时 hard gate；
2. 固定其它量，任一利用率上升不能让 TaskCost 下降；
3. 中低利用率不应被过度惩罚；
4. 接近能力边界时成本应快速上升；
5. 同 peak utilization 下，额外显著 maneuver 可以增加成本；
6. 第二轴附加成本不能等价于再完整乘一遍 response penalty；
7. Functional Capacity 只通过 utilization 进入，不能在下游再因“弱鱼”重复惩罚。

## 仍未冻结

- `InterceptDemand / Capacity` 的具体单位与标准化方式；
- `ManeuverDemand / Capacity` 的具体构成；
- `p` 是否真需要接近 4；
- `rho` 是否值得成为生产参数，还是能由更底层的 task composition 自然导出；
- 两轴是否足够，还是后续反例要求第三个独立任务轴。

下一步应优先攻击 `rho`：寻找“同 peak utilization、不同第二轴负担”的玩家策略故事，判断第二轴 surcharge 是否真的购买了足够明显的玩法差异。

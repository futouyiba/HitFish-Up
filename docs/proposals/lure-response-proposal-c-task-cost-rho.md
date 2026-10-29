# Proposal C：第二任务轴惩罚 `rho` 的准入结论

> Status: Working Hypothesis / admission review
>
> Scope: Feeding Response / `TaskDemand -> TaskCost`

## 结论

当前**不应把 `rho` 作为已准入的生产参数**。

现有体验故事主要只约束一个综合 physically-feasible task consequence，没有形成“同样瓶颈轴、第二轴不同”的控制对照，因此无法从现有校准数据识别 `rho`。

第一版更干净的假设是：

```text
rho = 0
```

即：

```text
TaskCost = k * max(u_intercept^p, u_maneuver^p)
```

其中：

```text
u_intercept = InterceptDemand / InterceptCapacity
u_maneuver  = ManeuverDemand  / ManeuverCapacity
```

任一利用率 `> 1` 时直接判定 Task Infeasible，不允许由 FoodValue 或 Motivation 补偿。

## 为什么暂时不加第二轴惩罚

第二任务轴可能真实增加捕获难度。大口黑鲈捕获猎物确实需要 locomotor positioning、制动、朝向和 mouth-prey geometry；转向和复杂机动不是纯装饰。

但“这个物理事实存在”并不等于“生产模型现在就需要一个独立 `rho` 参数”。

当前还缺少这样的体验 fixture：

```text
FoodValue 相同
Motivation 相同
Intercept utilization 相同

A: Maneuver utilization 很低
B: Maneuver utilization 中等
C: Maneuver utilization 很高

并且明确规定 A / B / C 最终应该差多少。
```

没有这类控制案例，`rho` 只能靠直觉调，不能被现有体验预算独立识别。

## 灵敏度结果

Working probe 固定其他参数，只改变 `rho`：

| rho | moderate straight | moderate turn | hard straight | hard compound |
|---:|---:|---:|---:|---:|
| 0.00 | 0.832 | 0.832 | 0.416 | 0.416 |
| 0.10 | 0.832 | 0.818 | 0.416 | 0.373 |
| 0.25 | 0.832 | 0.798 | 0.416 | 0.307 |
| 0.50 | 0.832 | 0.764 | 0.416 | 0.199 |
| 1.00 | 0.832 | 0.695 | 0.416 | 0.000 |

这说明：

- 小 `rho` 只产生次级修正；
- 大 `rho` 会在高负担区迅速形成强惩罚；
- `rho=1` 很容易把两个本来分别可行的任务轴重新变成类似连乘式重罚。

因此如果未来 `rho` 被准入，也更像**小的 compound-task correction**，不应成为第二套主惩罚。

## 当前推荐 contract

第一版先保持：

```text
TaskCost = k * max(u_intercept^p, u_maneuver^p)
```

保留两个原始 axis utilization 用于：

- Explain / debug；
- Infeasible 判定；
- 未来 compound-task fixture；
- 后续验证 `rho` 是否购买独立表达能力。

不要因为暂时 `rho=0` 就把两个轴重新压成一个不可追溯的标量输入。

## `rho` 的准入门

只有出现并确认以下类型的体验需求，才重新打开 `rho`：

1. 相同 Intercept 难度下，大转向需要稳定且可感知地低于直线追击；
2. 相同 Intercept 难度下，明显垂直重定位需要独立降低 response；
3. 该差异不能由现有 Intercept / Maneuver task consequence 定义、Infeasible gate 或 Closing hard limit 主轴解释；
4. 差异幅度足以映射为玩家可感知的 target efficiency / purity / wait-time 变化。

在这之前，`rho` 保持 Deferred，而不是默认存在。

# Proposal C：无鱼实体点条件下的角度概率 Intercept

> Status: Working Hypothesis
>
> Scope: Feeding Response / TaskDemand / latent micro-geometry

## 结论

当前运行时没有“某条鱼的具体世界坐标”，只有拟饵的具体位置与呈现轨迹。

因此 Feeding Response 不应虚构一条鱼位于某个绝对距离 `D`，再执行完整几何截获。

第一版更合适的是：

1. 把鱼相对拟饵的**未知方位角** `theta` 视为潜变量；
2. 只从该角度解析当前呈现造成的局部 Closing / Intercept Demand；
3. 对不同 `theta` 下的 response 做概率期望；
4. 不在这一层引入自由的绝对距离分布 `p(D)`。

即：

```text
latent angle theta
→ Closing Utilization u_close(theta)
→ TaskCost / C(theta)
→ angle expectation
→ C_mode
```

## 为什么撤掉绝对距离 D

此前 probe 证明 `C_mode` 对假定距离高度敏感。例如在同一 working 参数下，慢速 retrieve 仅把 `D` 从 1m 改成 3m，就可能从强响应降到中低响应。

但当前系统并没有鱼的实体位置，也没有一个已承接的“鱼离饵几米”的运行时事实。

因此继续引入：

```text
D = 1.5m
```

或自由的：

```text
p(D)
```

都会把未建模的鱼微观位置、感知距离、是否进入交互范围等问题偷偷塞进 Feeding Decision。

这类绝对距离信息在没有明确 Owner 之前，不应成为 Response 的隐藏参数。

## Reduced Intercept

定义：

```text
q = lure_speed / intercept_capacity
```

令 `theta` 为拟饵运动方向与“潜在鱼 → 拟饵”径向方向的夹角：

- `theta = 0`：拟饵正背离潜在鱼；
- `theta = 90°`：拟饵横切；
- `theta = 180°`：拟饵朝潜在鱼运动。

第一版 Closing utilization：

```text
u_close(theta) = max(0, q * cos(theta))
```

含义：

- 背离鱼运动的径向速度分量增加 Closing Demand；
- 横切本身不在 Closing 轴上追加“追离距离”的负担；
- 朝鱼运动不需要鱼主动追回正在扩大的径向距离。

这不代表横切、高速迎面经过没有难度。它们的其他后果继续由各自 Owner 处理，例如：

- Maneuver / Capture-Geometry Demand；
- temporal support / favorable dwell；
- presentation history / prediction break；
- 未来若 admission 的其他独立 task semantic。

不要把所有 fast-retrieve 后果重新塞回 Intercept。

## 概率聚合

当前没有证据支持方向偏置时，可先使用无偏角度先验：

```text
p(theta) = Uniform(-pi, pi)
```

最终不是先求“平均 physically-feasible task consequence”，而是：

```text
C_mode = E_theta[C(theta)]
```

原因是 TaskAffordance 含有：

- `Infeasible` hard gate；
- convex TaskCost；
- clipped response projection。

这些都是非线性的。

例如：

```text
50% 的角度 C=1
50% 的角度 C=0
```

应得到：

```text
C_mode = 0.5
```

而不是先构造一个不存在的“平均鱼位置 / 平均 physically-feasible task consequence”再算 response。

## Working probe

`proposal_c_angle_only_intercept_probe.py` 暂用既有 Working TaskCost 与 response projection，仅检查角度结构。

示例：

| q = lure speed / capacity | angle-averaged C | feasible angle share |
|---:|---:|---:|
| 0.00 | 0.970 | 1.000 |
| 0.50 | 0.957 | 1.000 |
| 0.75 | 0.907 | 1.000 |
| 1.00 | 0.775 | 1.000 |
| 1.25 | 0.697 | 0.795 |
| 1.50 | 0.656 | 0.732 |
| 2.00 | 0.609 | 0.667 |

这些数字不是 production calibration。

它们只说明：

- `q > 1` 不等于“所有潜在鱼都追不上”；
- 只有一部分背离方向会首先跨入 Infeasible；
- 角度积分可以把“不同微观方位下部分可追、部分不可追”自然投影成 retention；
- Closing axis 单独不会负责所有高速呈现惩罚。

## Distance 的当前处理

此前探索过：

```text
x = D / (capacity * decision_horizon)
```

并验证不同 `p(x)` 会明显改变慢速 retrieve 的结果。

因此当前不 admission 一个自由的 radial prior。

更干净的第一版解释是：Feeding Response 在“目标已经进入当前 interaction / consideration 范围”的条件下工作，径向进入范围本身不在这里重新随机模拟。

如果未来系统明确提供并拥有以下任一契约，再重新打开 radial geometry：

1. 已定义的 reaction / consideration distance；
2. 已定义的 encounter neighborhood；
3. 可验证的 micro-position prior；
4. 一个不会与 Spatial supply 重复计权的 radial probability contract。

在这之前：

```text
latent theta: admitted as Working reduced geometry
absolute D / free p(D): deferred
```

## 与 Spatial 的边界

Spatial 仍回答：

> 这个饵点周围，本来有多少该鱼的 native supply。

这里的 angle integration 只回答：

> 在这些潜在鱼没有实体微观坐标的情况下，不同相对方位会让当前 presentation 对其中多少鱼更容易或更难响应。

因此角度积分必须归一化为 response retention，不能再次扩大或缩小 Spatial abundance 本身。

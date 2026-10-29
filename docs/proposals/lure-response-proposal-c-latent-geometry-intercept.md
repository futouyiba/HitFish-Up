# Proposal C：无具体鱼位置时的潜在几何截获模型

> Status: Working Hypothesis / geometry model probe
>
> Scope: Feeding Response / Intercept Demand

## 结论

当前运行时只有饵的具体位置/轨迹，不存在某条鱼的具体世界坐标。

因此不要虚构一条实例鱼，也不要把“拟饵速度”直接当成 `InterceptDemand`。

推荐把鱼相对拟饵的未知几何关系视为**潜变量**，在概率意义上边缘化：

```text
latent relative geometry g
→ InterceptDemand(g)
→ utilization(g)
→ TaskCost(g)
→ C_mode(g)
→ E_g[C_mode(g)]
```

最终的 `C_mode` 可以解释为：

> 在当前鱼种、鱼情和呈现条件下，对未知相对几何位置的潜在鱼群做平均后，有多少 native opportunity 被保留下来。

这和 Interaction 输出 `captureRetention` 的语义是相容的。

## 为什么不能先平均 physically-feasible task consequence

不要这样：

```text
E_g[physically_feasible_task_consequence(g)]
→ TaskCost
→ C_mode
```

原因是 Infeasible gate、凸 TaskCost 和截断 Response Projection 都是非线性的，一般有：

```text
E_g[f(physically_feasible_task_consequence(g))] != f(E_g[physically_feasible_task_consequence(g)])
```

如果先平均，可能把“部分方向完全追不上、部分方向很好追”的真实混合状态，伪造成一条中等难度的平均鱼。

正确顺序应是：

```text
每个 latent geometry 独立结算
→ 再平均最终 response / retention
```

## 最小角度模型

第一版只把相对方位 `theta` 作为潜变量。

设：

- `D`：Working characteristic encounter distance；
- `T`：Working interception horizon；
- `v_lure`：当前拟饵速度向量；
- `theta`：假想鱼相对拟饵运动方向的方位角；
- `Vcap`：鱼的 Intercept Capacity。

在最小 constant-velocity probe 中，假想鱼位于距拟饵 `D` 的环上。到 `T` 时刻，拟饵的预测位置为：

```text
p_lure(T) = v_lure * T
```

对应方位的假想鱼位置为：

```text
p_fish(theta) = D * [cos(theta), sin(theta)]
```

所需平均截获速度：

```text
Vreq(theta)
= |p_lure(T) - p_fish(theta)| / T
```

能力利用率：

```text
u_intercept(theta) = Vreq(theta) / Vcap
```

若：

```text
u_intercept(theta) > 1
```

则该潜在方位为 Task Infeasible，对应：

```text
C_mode(theta) = 0
```

否则进入既有 Working 链：

```text
u_intercept(theta)
→ TaskCost(theta)
→ DecisionMargin(theta)
→ C_mode(theta)
```

最终：

```text
C_mode = ∫ p(theta | context) * C_mode(theta) dtheta
```

## 第一版 prior

当前没有证据支持复杂微观鱼位分布，因此最小 probe 使用：

```text
p(theta) = Uniform(0, 2π)
```

这只是**默认各向同性 latent-geometry prior**，不是在说真实鱼一定均匀围着饵。

未来只有在有独立输入时，才允许引入方向性 prior，例如：

- 明确的流向导致鱼普遍迎流定向；
- 已有 Structure/Cover 模型能给出局部方向性；
- 某个 mode 本身定义了可靠的 approach-direction prior。

注意：不要为了得到 `p(theta)` 重新读取 Spatial Cause 并把鱼密度/结构偏好算第二次。Spatial 决定 native supply；这里的 latent prior 只解释**未知的微观相对几何**。

## Probe 结果

Working 参数下，仅改变拟饵速度，均匀积分 720 个方位：

| lure speed | E[C(theta)] | feasible-bearing fraction |
|---:|---:|---:|
| 0.00 | 1.000 | 1.000 |
| 0.25 | 0.969 | 1.000 |
| 0.50 | 0.799 | 1.000 |
| 0.75 | 0.585 | 0.651 |
| 1.00 | 0.493 | 0.540 |
| 1.25 | 0.421 | 0.460 |
| 1.50 | 0.357 | 0.393 |

这些数字不是 Production calibration。它们只说明概率化几何会自然产生：

- 速度提高时，可截获方位比例下降；
- 并非所有方向同时变难；
- pause/降速可以通过扩大 feasible geometry 的占比来提高总体 response；
- 不需要虚构某条实例鱼的坐标。

## Distance 仍是未闭合项

角度可以明确作为潜变量，但 `D` 现在仍不能悄悄固定成“真实鱼距离”。

有三个候选方向：

1. **characteristic encounter distance**：每个 species/mode 使用一个可标定的代表距离；
2. **latent distance distribution**：和角度一样，对 `D` 也边缘化；
3. **distance-free reduced model**：只保留方向/速度形成的无量纲 chase load。

当前不足以裁定三者。

第一版建议不要马上增加 `p(D)`，先用 characteristic `D` 做 sensitivity probe，判断最终 `C_mode` 对 `D` 是否高度敏感；如果高度敏感，才证明 distance distribution 值得成为正式模型对象。

## 当前 Working contract

```text
No concrete fish point
≠ no geometry effect

Unknown micro geometry
→ latent-variable marginalization
→ expected response / retention
```

因此 `InterceptDemand` 可以继续保留，但应明确是：

> 对潜在鱼-饵相对几何进行概率边缘化后的捕获任务解释，
> 而不是实例鱼 AI 的逐鱼追逐求解。

对应可执行 probe：

`prototypes/lure-response/proposal_c_latent_geometry_intercept_probe.py`

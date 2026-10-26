# Proposal C：Maneuver 输入归属与 hard-gate 修正

> Status: Working Hypothesis / design correction
>
> Scope: Feeding Response / `ActualPresentation -> Maneuver Challenge`

## 结论

第一版 Maneuver 不应继续承接所有“高速、横切、升降、roll、急停”等现象。

当前只准入一类在没有鱼具体位置时仍能稳定计算、且语义相对干净的输入：

```text
拟饵自身轨迹方向变化速度
```

Working 量：

\[
\omega_{traj}=v\kappa=\frac{\|v\times a\|}{\|v\|^2}
\]

其中：

- `v`：拟饵相对水体的瞬时速度；
- `κ`：三维轨迹曲率；
- `ω_traj`：拟饵速度方向每秒改变多少，单位 rad/s。

它同时表达：同样弯道走得越快越难处理；同样速度下弯得越急越难处理。

## 输入归属

| ActualPresentation 现象 | 当前归属 | 原因 |
|---|---|---|
| 直线水平高速 | Closing / Intercept | 高速本身不等于需要急转；是否背离潜在鱼由 latent angle 决定 |
| 横向穿越 | 不直接进 Maneuver | 无鱼距时无法从横向速度推出 predator 所需转角或 LOS angular rate |
| 稳定上升 / 下沉 | 垂直 closing / reposition，当前 Deferred | 匀速升降本身不是轨迹方向变化；鱼在上方还是下方未知 |
| 轨迹曲率 / 急转 | Maneuver candidate | 拟饵自身运动方向确实在快速改变 |
| 直线加速 / 减速 | Closing / transient prediction | 速度大小变化不等于转向 |
| pause | Closing / temporal support / prediction break | pause 不拥有匿名 Maneuver bonus |
| roll / body orientation | Deferred | 只有能证明稳定改变 strike geometry 时，才允许进入 TaskDemand；否则可能只是视觉/猎物状态线索 |

## 为什么不能把 `omega_traj / fish_turn_capacity > 1` 当 Infeasible

此前 Working TaskCost 曾暂时使用：

```text
任一 task-axis utilization > 1 -> Task Infeasible
```

这个规则对当前 Maneuver proxy **过强，需要修正**。

`omega_traj` 描述的是目标轨迹自身转得多快，不是 predator 为成功捕获所必须达到的最小转向速度。鱼可以：

- 切弯；
- 预测或偏置追击；
- 等待目标进入击口窗口；
- 不逐点复制猎物路径。

因此：

```text
u_intercept > 1
```

在语义完整的 Closing / Intercept 条件下仍可作为某个 latent geometry 下的 hard infeasible；

而：

```text
omega_traj / Omega_fish > 1
```

目前只能表示较高 Steering Challenge，不能证明物理上无法捕获。

这也得到鱼类 pursuit 文献的方向支持：predator 并不必然逐点复制 prey trajectory；鱼类可采用 pure/deviated pursuit 或直接朝预测截获点运动。这里引用只支持“目标轨迹速度并不等于 predator 必须匹配的轨迹”这一机制方向，不提供本提案的生产公式。

## 当前推荐结构

第一版把两个概念分开：

```text
Closing / Intercept
- latent angle conditioned
- 可以有明确 hard infeasible sector

Steering Challenge
- 读取 omega_traj
- 目前只允许 soft cost
- 不允许单独 hard-zero
```

因此此前：

```text
TaskCost = k * max(u_intercept^p, u_maneuver^p)
任一 u > 1 -> hard zero
```

不再作为当前推荐写法。

更准确的 Working 拓扑是：

```text
latent angle theta
+ lure relative-water velocity
+ fish intercept capacity
→ Closing / Intercept branch
→ per-angle hard feasibility + closing cost

lure trajectory angular rate omega_traj
+ fish steering capability / reference
→ Steering Challenge
→ bounded or otherwise soft maneuver cost

closing cost + steering cost
→ TaskCost composition
```

`Steering Challenge -> cost` 的具体函数尚未冻结；在获得 compound-task experience fixture 前，不新增 hard threshold。

## 需要保留的反例

1. **直线快 ≠ Maneuver 高**：`v` 很高但 `κ=0`，`omega_traj=0`。
2. **同曲率快走更难**：`κ` 相同，速度更高，`omega_traj` 更高。
3. **同速度急转更难**：速度相同，曲率更高，`omega_traj` 更高。
4. **稳定升降不等于转弯**：如果三维速度方向恒定，`omega_traj=0`；垂直追赶应由独立语义承接。
5. **目标转得比鱼快仍不等于必然捕获失败**：没有 predator-relative geometry 时，禁止由该比值单独 hard-zero。

对应 executable probe：

`prototypes/lure-response/proposal_c_maneuver_input_routing_probe.py`

## 未闭合

- Steering Challenge 应如何映射为 soft Maneuver Cost；
- 是否需要区分 yaw / pitch capacity；
- 垂直 relative geometry 是否值得单独概率化；
- roll / body-axis orientation 是否能通过独立反事实验收进入 Capture-Geometry Demand；
- Steering Challenge 与 Closing Cost 最终是 `max`、小 correction，还是其他 operator。

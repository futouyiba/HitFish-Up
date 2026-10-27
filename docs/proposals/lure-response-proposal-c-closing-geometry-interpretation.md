# Proposal C｜Closing Geometry Interpretation

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

当前第一版使用：

```text
q = lure_speed_horizontal_relative_to_water / InterceptSpeedLimit
u_close(theta) = max(0, q * cos(theta))
```

`u_close` 只表达：

> 拟饵沿潜在鱼→拟饵视线方向继续远离时，径向分离速度相对于鱼短时截获速度尺度的比例。

它是 **RadialSeparationLoad** 的输入，不是完整 interception feasibility。

本次修正：

```text
u_close >= 1
```

**不再直接产生 hard-zero。**

第一版统一改为 soft Closing burden：

```text
ClosingCost(theta)
= K_close
  * u_close(theta)^2
  * ActivityCostMultiplier(Activity)
```

随后照常进入 `DecisionMargin(theta)` 与 response projection。

真正的 hard interception zero 只有未来拿到合法 encounter geometry / reaction-window contract 后才允许恢复。

## 2. 为什么 `max(0, q cosθ)` 仍成立

若只关心拟饵相对潜在鱼的瞬时径向分离速度：

```text
v_radial = v_lure * cos(theta)
```

当：

```text
cos(theta) > 0
```

拟饵正在沿视线方向远离鱼，鱼必须补偿这部分径向分离，才能阻止距离继续拉大。

当：

```text
cos(theta) = 0
```

拟饵纯横切，瞬时一阶径向距离不增加。

当：

```text
cos(theta) < 0
```

拟饵正在朝鱼方向接近，当前运动本身不制造继续远离负担。

因此：

```text
max(0, q cosθ)
```

作为径向分离 proxy 成立。

## 3. 它不等于完整 interception problem

当前没有合法事实描述：

- fish-lure 初始距离；
- 鱼的真实朝向；
- strike reach；
- reaction latency；
- 目标交会点；
- 鱼为了横切截获需要游多远；
- 加速度 / 转向能力；
- pursuit horizon；
- presentation 离开有效 interaction region 的剩余时间。

所以不能从 `u_close` 推出完整追击是否物理可行。

尤其：

```text
cosθ = 0
→ u_close = 0
```

只表示当前没有额外径向逃离负担，不表示鱼无需运动。

## 4. 为什么撤掉 `u_close >= 1 → hard-zero`

`u_close >= 1` 最多说明：

> 目标当前径向远离速度达到或超过鱼的短时截获速度尺度，鱼无法靠持续同向游动让两者径向距离停止增加。

但它不能推出：

> 当前 interaction 已经不可能发生。

反例：鱼与拟饵已经非常接近。即使拟饵开始以高于鱼持续追赶能力的速度远离，鱼仍可能在目标离开 strike / interaction window 前完成攻击。

要裁 hard-zero，至少还需要类似：

```text
current_gap
strike_reach
reaction_latency
time_to_exit_interaction_region
```

当前这些量没有合法 owner。因此把 `u_close >= 1` 直接设成 `C=0`，会把“无法持续追上”错误升级成“当前无法攻击”。

## 5. 第一版 soft Closing

第一版冻结：

```text
q
= lure_speed_horizontal_relative_to_water
  / InterceptSpeedLimit

u_close(theta)
= max(0, q * cos(theta))

ClosingCost(theta)
= K_close
  * u_close(theta)^2
  * ActivityCostMultiplier(Activity)
```

`ClosingCost` 可以大于 1；它是 `DecisionMargin` 中的 cost，不是概率。

因此高 `u_close` 仍会强烈压低响应，但不会绕过 FoodValue、Motivation、Trigger 等其它合法输入直接判死。

例如高速度在普通条件下完全可能通过：

```text
DecisionMargin <= 0
→ C = 0
```

得到数值上的零响应。这里的零来自完整决策链，而不是一个缺少 encounter geometry 的伪物理 hard gate。

## 6. InterceptSpeedLimit 的语义同步收窄

`InterceptSpeedLimit` 仍可以表示鱼的结构性短时截获速度能力尺度，并继续用于 species × size calibration。

但在当前第一版中：

```text
lure radial speed > InterceptSpeedLimit
```

不等价于：

```text
interaction impossible
```

因此 `InterceptSpeedLimit` 是 Closing load 的能力尺度，而不是单独足够的 encounter feasibility gate。

如果未来觉得名称会持续误导，可以在 production schema 评审时考虑改名为：

```text
ReferenceInterceptSpeed
```

或其它不暗示单变量 hard gate 的名称。当前不因命名问题提前改 schema。

## 7. 与 Opportunity 的边界

职责切分：

```text
Candidate / Spatial / Opportunity
→ 鱼与 presentation 是否处在可发生 interaction 的局部机会范围
→ exposure / residency / encounter window
```

```text
Closing
→ 当前 lure motion 正在多强地把这个机会带离潜在鱼
```

如果未来 Opportunity Owner 能输出标准化 encounter geometry，例如：

```text
current_gap
interaction_radius
remaining_exposure_window
```

再讨论真正的 interception hard gate。

在此之前 Closing 不自行假设距离或 reaction window。

## 8. 不新增横向速度 penalty

撤掉 hard-zero 不意味着要补：

```text
v_tangential = v_lure * sin(theta)
ClosingCost += K_tangent * |v_tangential|
```

仍然不建议这样做，因为：

- 没有鱼点时，横向速度并不唯一对应需要鱼横移的距离；
- 会把 Prediction / maneuver 与 Closing 再次混合；
- `K_tangent` 会成为新的自由参数；
- 容易对高速横切 presentation 重复处罚。

只有未来拿到真实 encounter geometry / pursuit horizon 后，才应整体升级到二维 interception model。

## 9. Explain / regression

Explain 至少输出：

```text
radial_separation_ratio
bearing
closing_cost
```

不再输出：

```text
hard_radial_escape_infeasible
```

第一版需要新增 regression case：

1. `u_close < 1`：普通 soft burden；
2. `u_close ≈ 1`：连续过渡，不出现不连续 hard cliff；
3. `u_close > 1`：高 burden，但仍由完整 DecisionMargin 决定是否归零；
4. 高 Motivation / Preferred / strong Trigger 能否在部分高 `u_close` case 中保留小幅响应；
5. ordinary Good target 在高 `u_close` 下是否自然降为 0。

## 10. 对既有 Working calibration 的影响

此前文档中关于：

```text
q > 1
→ hard-infeasible bearing share
```

的统计不再代表第一版运行时 hard-zero 比例。

这些数值最多保留为：

> bearing 上 `radial_separation_ratio > 1` 的占比。

它仍可作为速度压力诊断指标，但不能直接当作 response hard-zero share。

因此：

- `HighClosing / GeneralClosing / LowClosing` 的 Working `q_ref` 可以继续作为分档 seed；
- `K_close` 需要在新的纯 soft 模型下重新跑完整 response basket；
- Fast / Burst 的旧 hard-infeasible 叙述必须按 soft Closing 重新解释。

## 11. 升级条件

只有满足以下任一条件，才重新讨论 hard interception gate：

1. 系统能合法取得真实/局部 fish-lure encounter geometry；
2. Opportunity Owner 输出标准化 encounter radius / distance distribution；
3. 有明确 reaction latency / strike reach / time-to-exit contract；
4. controlled fixtures 证明纯 soft radial proxy 无法复现关键玩家策略排序。

升级时应整体替换为新的 interception contract，不在当前公式上继续追加匿名 hard threshold。

## 12. 当前判定

第一版当前 Working 裁定：

- `max(0, q cosθ)` 保留，作为径向分离 load proxy；
- Closing 改为纯 soft burden；
- `u_close >= 1 → C=0` 撤回；
- `InterceptSpeedLimit` 不再单独充当 encounter hard gate；
- 真正 hard interception zero 等合法 encounter geometry / reaction-window owner；
- 不新增 tangential penalty。

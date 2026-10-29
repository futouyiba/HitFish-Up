# Proposal C｜Effective Intercept Capacity 语义闭合

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`intercept_capacity` 第一版不定义成“物种最高游速”。

它表示：

> 当前这条鱼在本次短时追赶语境下，用于阻止目标径向间距继续拉大的**有效 Closing 能力**。

它是 Response 侧消费的有效能力尺度，单位可以保持 m/s，但不等于资料表里的 burst speed、critical speed 或 cruising speed。

## 2. 为什么不能直接用最高游速

鱼类游泳性能至少区分持续游速、burst performance、加速和转向；捕食过程也会根据流场与捕获动作改变运动学。把一个“最高游速”直接拿来做 Closing gate，会把不同时间尺度和不同测试口径混在一起。

本项目当前又没有具体鱼点、起始距离与追赶时长，因此也没有条件显式解一个完整的 acceleration + distance + pursuit horizon 模型。

所以第一版不伪造这些缺失状态，而是把它们压成一个可校准的短时有效能力。

## 3. Working ownership

最小结构：

```text
LocomotorBaseline(species, size/stage)
        ↓
InterceptSpeedLimit
```

其中：

- `LocomotorBaseline` 表示该鱼种与体型/成长阶段的短时追赶能力基线；
- `InterceptSpeedLimit` 是 Closing 使用的能力尺度，不是单变量的完整 encounter feasibility proof；
- `Activity` 不修改 `InterceptSpeedLimit`，只调制 soft Closing cost。

本页不再建立旧的 `FunctionalCapacity` 总对象。环境和生理因素若要改变硬能力边界，必须通过一个单独命名、拥有独立 Contract 的 capability modifier 接入；不能把通用 Activity 复用为第二个 hard gate。

## 4. 与 Motivation 的边界

`InterceptSpeedLimit` 与 Feeding Motivation 必须分开。

```text
InterceptSpeedLimit
→ Closing 能力尺度
→ Closing feasibility / soft Closing cost

Feeding Motivation
→ 愿不愿意为这个目标出手
→ WillingnessThreshold
```

同一条鱼可以：

- Closing 能力高、Motivation 低：追得上，但不太愿意出手；
- Closing 能力低、Motivation 高：很想吃，但在缺少 encounter geometry 的当前版本中，高径向负担仍通过 soft Closing cost 降低响应。

不得用 Motivation 提高 `InterceptSpeedLimit`，也不得因为 Activity 低再额外降低 `InterceptSpeedLimit`。

## 5. 环境与生理因素只结算一次

若温度、低氧、疲劳、疾病等需要改变硬能力边界，必须先由上游写入具名的 capability modifier Contract。当前没有这样的生产 Contract，因此 Closing 不额外读取这些原因做第二次能力惩罚。

合法的当前链路是：

```text
species / size cohort
→ InterceptSpeedLimit
→ q
→ ClosingCost

Activity
→ Closing soft-cost multiplier
```

不能把同一个环境或生理原因同时写入能力上限和 Closing cost。

## 6. 参考系

`InterceptSpeedLimit` 与 lure speed 必须使用同一参考系。

第一版推荐都使用**相对水体**的速度语义：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
```

理由：能力基线描述鱼相对水体主动产生的推进能力；若分子使用世界速度、分母使用相对水体能力，水流会被错误混入 Closing utilization。

环境流对鱼实际捕获动作的额外影响，如果未来需要，应先明确它是否已经进入具名的 capability modifier 或其它独立机制，不能悄悄同时进入两边。

## 7. acceleration 如何处理

当前没有鱼点、起始距离与追赶 horizon，因此第一版不新增显式 acceleration state。

这不等于认为 acceleration 不重要。它的作用暂时由 `InterceptSpeedLimit` 的校准口径吸收：

> 这是短时捕食语境下的有效 Closing 能力，而不是稳态极速。

若未来获得合法的 reaction distance / encounter geometry / response horizon contract，再重新检查是否应拆成：

```text
burst speed
+ acceleration
+ response horizon
→ explicit intercept feasibility
```

在那之前不提前制造一套无法校验的运动学模型。

## 8. 和 ClosingCost 的接口

当前 Working：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
u_close(θ) = max(0, q cosθ)

ClosingCost(θ)
= K_close × u_close(θ)^2
  × ActivityCostMultiplier(Activity)
```

在没有 encounter geometry / reaction-window Contract 时，`u_close ≥ 1` 只表示径向分离负担高，不单独输出 `C=0`。能力变化只有一条直接路径：

```text
InterceptSpeedLimit↑
→ q↓
→ u_close↓
→ ClosingCost↓
```

Activity 只改变可行 Closing 的 soft cost，不改变 `InterceptSpeedLimit`。不得再加“强鱼 bonus”或“弱鱼 penalty”。

## 9. 仍未闭合

- `LocomotorBaseline` 的生产数据来源；
- 体长、成长阶段与 species baseline 的生成方法；
- `InterceptSpeedLimit` 的生产映射与 calibration；
- 是否需要 fish-quality / individual variation；
- `K_close` calibration；
- 若未来出现 reaction distance / response horizon authority，是否拆出 acceleration 和真正的 interception feasibility。

这些仍是缺口，不用假数字补齐。

## 10. 当前裁决

Working admitted：

```text
InterceptSpeedLimit
= 当前短时追赶语境下的有效 Closing 能力尺度
```

明确拒绝：

- 直接把资料表 `maximum speed` 当 production capacity；
- 把 Ucrit、burst speed、cruising speed 当成同一个量；
- Motivation 或 Activity 修改 `InterceptSpeedLimit`；
- 没有 encounter geometry 时，把 `u_close ≥ 1` 直接当作完整攻击机会的 hard zero；
- 在没有距离与时间尺度时伪造完整加速追击模型。

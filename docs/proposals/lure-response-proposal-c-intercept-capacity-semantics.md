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
        ×
CapacityStateModifier(FunctionalCapacity)
        ↓
EffectiveInterceptCapacity
```

其中：

- `LocomotorBaseline` 表示该鱼种与体型/成长阶段的短时追赶能力基线；
- `FunctionalCapacity` 表示当前鱼在环境与生理条件下“能做到多少”；
- `CapacityStateModifier` 是从 FunctionalCapacity 到实际能力尺度的映射；
- `EffectiveInterceptCapacity` 是 Closing 模块唯一消费的能力结果。

当前不冻结 `CapacityStateModifier` 为恒等、线性或其它曲线。若上游 FunctionalCapacity 的标尺尚未定义，不能直接假设 `capacity = baseline × FunctionalCapacity`。

## 4. 与 Motivation 的边界

FunctionalCapacity 与 Feeding Motivation 必须分开。

```text
FunctionalCapacity
→ 能不能追得上 / 做得到
→ EffectiveInterceptCapacity

Feeding Motivation
→ 愿不愿意为这个目标出手
→ WillingnessThreshold
```

同一条鱼可以：

- 能力高、Motivation 低：追得上，但不太愿意出手；
- 能力低、Motivation 高：很想吃，但部分 Closing angle 仍可能物理不可行。

不得用 Motivation 提高 intercept capacity，也不得因为 FunctionalCapacity 低再额外提高 willingness threshold，除非未来有独立机制证据。

## 5. 环境与生理因素只结算一次

若温度、低氧、疲劳、疾病等已经由上游 Fish Condition 编译进 FunctionalCapacity，则 Closing 不得再次读取这些因素做第二次能力惩罚。

合法链路是：

```text
environment / physiology
→ FunctionalCapacity
→ EffectiveInterceptCapacity
→ q
→ ClosingCost / angle-local infeasible
```

不合法：

```text
temperature
→ FunctionalCapacity↓
→ capacity↓

同时：
temperature
→ ClosingCost 再乘一次 penalty
```

这会 double count。

## 6. 参考系

`EffectiveInterceptCapacity` 与 lure speed 必须使用同一参考系。

第一版推荐都使用**相对水体**的速度语义：

```text
q = lure_speed_relative_to_water / EffectiveInterceptCapacity
```

理由：能力基线描述鱼相对水体主动产生的推进能力；若分子使用世界速度、分母使用相对水体能力，水流会被错误混入 Closing utilization。

环境流对鱼实际捕获动作的额外影响，如果未来需要，应先明确它是否已经进入 FunctionalCapacity 或其它独立机制，不能悄悄同时进入两边。

## 7. acceleration 如何处理

当前没有鱼点、起始距离与追赶 horizon，因此第一版不新增显式 acceleration state。

这不等于认为 acceleration 不重要。它的作用暂时由 `EffectiveInterceptCapacity` 的校准口径吸收：

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
q = lure_speed_relative_to_water / EffectiveInterceptCapacity
u_close(θ) = max(0, q cosθ)

if u_close(θ) >= 1:
    C_conditional(θ) = 0
else:
    ClosingCost(θ) = K_close × u_close(θ)^2
```

因此能力变化只有一条直接路径：

```text
FunctionalCapacity↑
→ EffectiveInterceptCapacity↑
→ q↓
→ u_close↓
→ ClosingCost↓ / infeasible angle 减少
```

不得再加“强鱼 bonus”或“弱鱼 penalty”。

## 9. 仍未闭合

- `LocomotorBaseline` 的生产数据来源；
- 体长、成长阶段与 species baseline 的生成方法；
- FunctionalCapacity 的量纲与标尺；
- `CapacityStateModifier` 的生产映射；
- 是否需要 fish-quality / individual variation；
- `K_close` calibration；
- 若未来出现 reaction distance / response horizon authority，是否拆出 acceleration。

这些仍是缺口，不用假数字补齐。

## 10. 当前裁决

Working admitted：

```text
EffectiveInterceptCapacity
= 当前短时追赶语境下的有效径向 Closing 能力
```

明确拒绝：

- 直接把资料表 `maximum speed` 当 production capacity；
- 把 Ucrit、burst speed、cruising speed 当成同一个量；
- Motivation 修改 locomotor capacity；
- FunctionalCapacity 已影响 capacity 后再按同一原因重复惩罚 Closing；
- 在没有距离与时间尺度时伪造完整加速追击模型。

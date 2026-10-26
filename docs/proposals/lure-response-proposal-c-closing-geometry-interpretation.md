# Proposal C｜Closing Geometry Interpretation

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

当前：

```text
u_close(theta) = max(0, q * cos(theta))
```

其中：

```text
q = lure_speed_horizontal_relative_to_water / InterceptSpeedLimit
```

几何上可以解释为：

> 拟饵沿鱼到拟饵视线方向继续远离时，对鱼造成的**径向分离速度占能力边界的比例**。

它不是完整的 interception 求解，也不表达鱼到拟饵之间的实际距离、横向交会距离、反应延迟或加速度过程。

因此第一版必须把它正式命名/解释为：

```text
RadialSeparationLoad
```

或继续保留 `ClosingCost` 名称，但文档必须明确其含义是“由当前运动造成的额外追赶负担”，不是“追上拟饵的全部运动代价”。

## 2. 为什么 `max(0, q cosθ)` 几何上成立

若只关心拟饵相对潜在鱼的瞬时径向分离速度：

```text
v_radial = v_lure * cos(theta)
```

当：

```text
cos(theta) > 0
```

拟饵正在沿视线方向远离鱼，鱼必须至少补偿这部分径向分离速度，才能避免距离继续拉大。

当：

```text
cos(theta) = 0
```

拟饵纯横切，瞬时一阶径向距离不增加。

当：

```text
cos(theta) < 0
```

拟饵正在朝鱼方向接近，当前运动本身不制造“继续远离”的追赶负担。

因此：

```text
max(0, q cosθ)
```

作为**径向分离负担 proxy** 是一致的。

## 3. 它不等于完整 interception problem

缺少真实鱼点后，我们不知道：

- fish-lure 初始距离；
- 鱼的真实朝向；
- 目标交会点；
- 鱼为了横切截获需要游多远；
- 反应延迟；
- 加速度 / 转向能力；
- pursuit horizon。

所以不能宣称：

```text
u_close
= total interception effort
```

尤其横切 case：

```text
cosθ = 0
→ u_close = 0
```

只意味着“拟饵没有在径向上继续逃离”。

它不意味着鱼无需运动。

## 4. 为什么第一版仍可接受

Proposal C 当前没有真实鱼点，也明确禁止采样虚构鱼点。

如果为了补横切距离而新增：

```text
assumed encounter radius
assumed starting distance
assumed reaction point
```

就会重新制造一组不可验证的隐藏几何参数。

第一版更稳妥的职责切分是：

```text
Candidate / Spatial / Opportunity
→ 决定鱼与当前 presentation 是否处在可发生交互的有效局部范围

Closing
→ 只计算当前 lure motion 是否正在把这个可交互目标快速带离鱼
```

因此横切 `ClosingCost≈0` 的语义是：

> 在已经进入有效交互范围这一前提下，横切运动本身没有额外增加径向逃离负担。

不是“鱼不需要游”。

## 5. Hard infeasible 的语义也要同步收窄

当前：

```text
if u_close(theta) >= 1:
    C_conditional(theta) = 0
```

应解释为：

> 当前拟饵沿潜在鱼→拟饵方向的远离速度，已经达到或超过鱼的短时截获速度边界，因此该 bearing 下鱼无法阻止距离继续拉大。

它不是对完整三角拦截问题的严格物理解。

如果未来有真实局部几何，应替换成真正 interception feasibility，而不是继续堆 proxy。

## 6. 不能因此新增横向速度 penalty

不建议把：

```text
v_tangential = v_lure * sin(theta)
```

再直接加入：

```text
ClosingCost += K_tangent * |v_tangential|
```

原因：

- 没有鱼点时，横向速度并不唯一对应需要鱼横移的距离；
- 会把 Prediction / maneuver 与 Closing 再次混合；
- `K_tangent` 会成为新的自由参数；
- 容易把所有横切高速 presentation 无依据地重复处罚。

只有未来拿到真实 encounter geometry / pursuit horizon 后，才应升级到二维 interception model。

## 7. 与其它 owner 的关系

```text
speed magnitude + latent horizontal bearing
→ RadialSeparationLoad / ClosingCost
```

```text
sudden direction change
→ PredictionChallenge
```

```text
鱼是否位于能发生 interaction 的有效局部范围
→ Candidate / Spatial / Opportunity owner
```

```text
持续暴露时间 / encounter duration
→ Temporal Exposure / Opportunity owner
```

Closing 不重新承担这些职责。

## 8. 第一版公式保留

在上述语义收窄后，第一版继续使用：

```text
q = lure_speed_horizontal_relative_to_water / InterceptSpeedLimit

u_close(theta) = max(0, q * cos(theta))

if u_close(theta) >= 1:
    C_conditional(theta) = 0
else:
    ClosingCost(theta)
    = K_close
      * u_close(theta)^2
      * ActivityCostMultiplier(Activity)
```

但 Explain 应能明确输出：

```text
radial_separation_ratio
bearing
hard_radial_escape_infeasible
```

避免把它解释成完整 pursuit simulation。

## 9. 升级条件

只有满足以下任一条件，才建议替换第一版 proxy：

1. 系统能合法取得真实/局部 fish-lure encounter geometry；
2. Opportunity owner 输出标准化 encounter radius / distance distribution；
3. runtime 需要表达 pursuit horizon、加速度、持续追逐或真实横切截获；
4. controlled fixtures 证明径向 proxy 无法复现关键玩家策略排序。

升级时应整体替换为新的 interception contract，不在当前公式上继续追加 tangential / distance / acceleration 匿名 penalty。

## 10. 当前判定

本轮结论：

- `max(0, q cosθ)` 作为径向分离 proxy 成立；
- 它不是完整 interception 几何；
- 横切 `u=0` 只表示无额外径向逃离，不表示无需运动；
- 第一版保留公式，但收窄语义；
- 不新增 tangential penalty；
- 完整 interception 留给未来有合法 encounter geometry 时整体升级。

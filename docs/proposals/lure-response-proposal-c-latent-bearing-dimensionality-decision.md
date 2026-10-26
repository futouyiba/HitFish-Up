# Proposal C｜Latent Bearing Dimensionality Decision

状态：Working Decision / Candidate。不是 Current，不是生产参数。

## 1. 结论

Proposal C 第一版 Closing 采用：

```text
RelativeBearingPrior = Isotropic2D
θ ~ Uniform(0, 2π)
```

这里的 2D 指水平相对 bearing。它是 Proposal C 的显式建模约定，不是“真实鱼一定在同一水平面”的世界事实。

## 2. 为什么第一版选 Horizontal2D

当前 Response 不拥有鱼的实际位置，也不应重新计算鱼种空间分布、depth / water-layer suitability、habitat affinity 或 candidate abundance。

因此第一版 Closing 只回答一个更窄的问题：

> 在当前目标已经进入可响应的空间语境后，如果鱼相对拟饵的水平方位未知，当前拟饵水平运动对 closing 造成多大负担？

把 latent prior 扩成完整 3D 会重新引入垂直方向不确定性，并把一部分纵向空间关系折进 Closing。由于 Response 没有权威鱼点，也没有一份 Current Contract 授权它重新解释 depth / water-layer suitability，这会增加重复计权和不可解释性。

因此第一版明确选择较窄的职责：

```text
vertical spatial suitability / eligibility
→ upstream spatial / candidate owner

horizontal relative bearing uncertainty
→ Proposal C Closing
```

## 3. 这不是对现行空间系统的事实声明

本轮检查了：

- `docs/README.md`：只是导航，不定义机制；
- `docs/authority-model.md`：Owner 裁定和经审核合并的 Git Markdown 才能形成 Current Authority；
- 当前分支仓树和代码搜索：没有找到一篇 Current Contract 明确规定 Proposal C 应使用完整 3D relative direction。

因此本页不能声称“现行空间系统已经证明鱼与拟饵处于同一水平层”。

本页只做 Candidate 设计裁定：在现有 authority 缺口下，第一版 Response 不主动接管垂直几何。

若后续空间 Owner 明确输出 lure-relative 3D directional support，本裁定必须重新审视。

## 4. 第一版公式

```text
θ ~ Uniform(0, 2π)
q = lure_speed_horizontal_relative_to_water / InterceptSpeedLimit
u_close(θ) = max(0, q * cosθ)
```

若：

```text
u_close(θ) >= 1
```

则对应 bearing hard infeasible。

否则：

```text
ClosingCost(θ)
= K_close
  * u_close(θ)^2
  * ActivityCostMultiplier(Activity)
```

并保持：

```text
θ
→ hard feasibility / ClosingCost
→ DecisionMargin(θ)
→ C(θ)
→ Eθ[C(θ)]
```

## 5. 为什么这里使用水平 lure speed

既然 latent bearing 只积分水平相对方位，`q` 的 numerator 也必须与该几何口径一致。

第一版应使用：

```text
lure_speed_horizontal_relative_to_water
```

而不是完整 3D 速度模长。

否则会出现：拟饵主要垂直下沉 / 上升，却被当成水平逃离鱼，从而人为抬高 Closing burden。

垂直 presentation 的策略意义如果需要表达，应由合法的 vertical prey-state / depth / spatial path 承接，不能通过 2D Closing 偷算。

## 6. 与 3D 的数值差异

在 `q <= 1`、reference Activity 下：

```text
E[u_close^2] = q^2 / 4
```

因此后续 `K_close` calibration 必须按 2D 口径进行。

不得先按 3D 的：

```text
q^2 / 6
```

标定，再在实现中换成 2D。

当 `q > 1` 时，2D hard-infeasible bearing fraction：

```text
P_hard = arccos(1/q) / π
```

这成为第一版 Closing 的 calibration contract。

## 7. ExplicitDirectional 暂不开放

第一版：

```text
family = Isotropic
 dimensionality = Horizontal2D
```

不允许 Response 自己根据：

- structure orientation；
- bank direction；
- current direction；
- cover orientation；
- 玩家抛投方向；

生成 biased bearing prior。

只有上游合法 Owner 明确输出与 lure-relative bearing 相容的 directional support，才可以引入 `ExplicitDirectional`。

## 8. Explain / regression

第一版至少输出：

```text
bearing_prior = Isotropic2D
bearing_dimension = Horizontal2D
speed_basis = horizontal_relative_to_water
prior_provenance = ProposalC_ModelConvention
```

回归应固定：

- `E[u^2] = q^2/4` for `q<=1`；
- `P_hard = arccos(1/q)/π` for `q>1`；
- 垂直速度变化不能单独改变 2D Closing；
- 水平速度增加不能提升 response；
- 未知 prior 不静默 fallback，除非 Phase 明确启用本固定 convention。

## 9. 重新打开 3D 的条件

只有满足至少一项时重新审视 Full3D：

1. 上游空间 / Candidate Owner 提供可消费的 3D lure-relative fish directional distribution；
2. controlled fixtures 证明控制 depth / layer / horizontal bearing 后，垂直 relative geometry 仍产生独立、稳定、玩家可理解的 Closing 排序；
3. runtime 获得真实鱼点或合法的个体空间 distribution，而不是临时随机假鱼点。

在此之前，Full3D 不进入第一版。

## 10. 剩余缺口

仍未解决：

- 当前空间 / Candidate Current Owner 是否未来会正式承接 vertical eligibility 与 directional support；
- lure runtime 是否已有稳定的 `horizontal_relative_to_water` 速度事实；
- 未来若出现 vertical pursuit 玩法，归属 Spatial、Prey State 还是 Closing 的 owner 边界。

这些缺口不阻塞 Proposal C 第一版使用 `Isotropic2D` 作为显式 Candidate modeling convention。

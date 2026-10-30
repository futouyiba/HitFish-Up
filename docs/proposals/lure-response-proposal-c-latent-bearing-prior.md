# Proposal C｜Latent Bearing Prior

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

当前 Feeding Response 在没有具体鱼点时，仍需要对潜在鱼相对拟饵运动方向的 latent bearing 做积分：

```text
bearing hypothesis b
→ Closing feasibility / ClosingCost(b)
→ DecisionMargin(b)
→ C_conditional(b)
→ integrate over RelativeBearingPrior
```

但 `RelativeBearingPrior` 不能被省略，也不能把“未知”静默写成“各方向等概率”。

第一版把它提升为显式建模对象：

```text
RelativeBearingPrior
```

它表达：

> 在当前 response resolution 所允许的信息范围内，对潜在鱼相对拟饵运动方向的建模分布。

它不是实际鱼坐标，也不是随机生成一个假鱼点。

## 2. 为什么 prior 是必需的

当前 Closing 使用：

```text
u_close(b) = max(0, q * cos(b))
```

不同 bearing 会产生不同结果：

- 拟饵背离潜在鱼：Closing burden 大；
- 横切：径向分离 burden 小；
- 拟饵朝潜在鱼：Closing burden 为0；
- 高 q 时只有一部分 bearing hard infeasible。

因此：

```text
E_b[C(b)]
```

没有 prior 就没有唯一数值。

`Unknown bearing` 不是一个可直接平均的事实状态。

## 3. 不允许采样虚构鱼点

禁止：

```text
sample fake fish position
→ derive bearing
→ calculate response
```

原因：

- 系统没有该个体位置事实；
- 随机点会让一次 response resolution 产生无意义噪声；
- 后续很容易把采样结果误当世界状态；
- 多次 roll 可能因为隐藏几何采样而改变结果，难以 Explain / regression。

第一版只对 latent bearing 做确定性积分或离散求积。

## 4. 默认 prior 必须声明为模型约定

如果当前 resolution 没有合法方向证据，可以使用一个声明过的 isotropic prior 作为模型约定。

但必须明确：

```text
IsotropicPrior
≠ 观测到鱼均匀分布
```

它只表示：

> 在没有可消费方向信息时，模型不偏好某个 bearing。

如果上游未来提供合法的方向结构，例如明确的鱼群空间支持、结构边缘方向、流向相关驻位或其它 Current Owner 输出，可以替换 isotropic prior。

Response 不得自己从 structure / current / bank / cover 猜 prior。

## 5. 2D 与 3D 不能混写

当前还存在一个未闭合的维度问题。

### Isotropic 2D

如果纵向位置已经由其它空间系统独立约束，而这里只剩水平相对方位：

```text
θ ~ Uniform(0, 2π)
```

则是水平 bearing prior。

### Isotropic 3D

如果 latent direction 是完整三维方向：

```text
μ = cos(θ) ~ Uniform(-1, 1)
```

注意：三维各向同性不是 `θ ~ Uniform(0, π)`。

两种 prior 会给出不同 Closing 统计，不能互换。

当前仓内尚未找到一份 Current Contract 明确回答：Proposal C 的 Closing latent bearing 应只积分水平 bearing，还是完整 3D relative direction。因此本页不擅自冻结 2D / 3D。

## 6. 两种 isotropic prior 的差异不是小数值细节

只看 Closing utilization 的二次项：

```text
u = max(0, q * directional_cosine)
```

在不触发 hard infeasible 时：

```text
E[u²] = q² / 4    # isotropic 2D
E[u²] = q² / 6    # isotropic 3D
```

因此同一个 `K_close` 下，2D isotropic 的平均二次 Closing burden 比 3D isotropic 高 50%。

当 `q > 1` 时，hard-infeasible bearing fraction 也不同：

```text
2D: P_hard = arccos(1/q) / π
3D: P_hard = (1 - 1/q) / 2
```

所以 2D / 3D 必须在 calibration 前冻结，不能等到最后再换。

## 7. 第一版接口

推荐：

```text
RelativeBearingPrior {
  status
  dimensionality: Horizontal2D | Full3D
  family: Isotropic | ExplicitDirectional
  parameters
  provenance
}
```

第一版真正需要支持的最小集合可以只有：

```text
Isotropic2D
Isotropic3D
```

`ExplicitDirectional` 先保留接口，不在没有上游数据时提前实现复杂分布。

## 8. Unknown / Disabled / NotApplicable

```text
prior Unknown
→ ResolutionIncomplete
→ 不输出最终 Feeding scalar
```

不能：

```text
Unknown prior
→ fallback uniform silently
```

如果某个 Phase 明确声明使用固定 isotropic modeling convention，则该 convention 本身就是已解析 prior，不是 Unknown。

`Disabled` 不适用于正常 Closing path：只要 Closing 仍依赖 latent bearing，就必须有 prior。

## 9. 与空间系统的边界

RelativeBearingPrior 不负责：

- 鱼种空间分布权重；
- depth / water-layer suitability；
- habitat affinity；
- cover / structure preference；
- 真实鱼群密度；
- candidate abundance。

这些量若已经决定“鱼更可能在哪些空间区域”，不能在 Response 再偷算一次。

只有当空间 Owner 明确输出与本次 lure-relative bearing 相容的 directional support 时，才能被适配为 `ExplicitDirectional` prior。

## 10. 与 Explain / regression 的关系

Explain 至少应能输出：

```text
bearing_prior = Isotropic2D
```

或：

```text
bearing_prior = Isotropic3D
```

以及 prior 的 provenance。

这样同一个 lure presentation 在不同 prior contract 下得到不同 response 时，可以追溯原因，而不是表现成 Closing 参数漂移。

## 11. 当前 OPEN

P0：

- Closing latent bearing 到底应是 Horizontal2D 还是 Full3D；
- 对应空间 / Candidate Current Owner 是否已有可消费的方向信息。

P1：

- 若未来允许 ExplicitDirectional，谁拥有其 production contract；
- prior 是否随 structure / current / bank geometry 变化，以及怎样避免与 Spatial Distribution 重复计权；
- 数值积分采用解析积分、固定 quadrature 还是离散 bearing bins。

## 12. 当前 Working 裁定

在 dimensionality 未由项目空间语义闭合前：

- `RelativeBearingPrior` 作为必需 contract 已闭合；
- 不采样假鱼点；
- isotropic 只能作为显式模型 convention；
- 2D / 3D 暂不静默裁定；
- 完整 Feeding scalar 仍不能宣称 production-closed。

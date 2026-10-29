# Proposal C｜Closing Cost Shape

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 结论

第一版 Closing 采用径向分离 proxy 与简单凸 soft cost：

```text
u_close(θ) = max(0, q cosθ)
q = lure_speed_relative_to_water / InterceptSpeedLimit

ClosingCost(θ) = K_close · u_close(θ)^2
```

没有独立 encounter-geometry / reaction-window contract 时，`u_close >= 1` 仍是高 burden，不直接把 `C_conditional(θ)` 置零。

`u²` 是当前最小 Working 选择。它不是长期物理定律。

## 为什么不是线性

线性 cost 会从低 Closing 开始持续处罚，容易让正常速度也过早失去 response。

凸 cost 的语义更合适：

- 远离能力边界时，Closing 只是轻度负担；
- 接近能力尺度时，soft burden 快速抬升；
- 是否归零由完整 DecisionMargin 和未来合法的 encounter contract 共同决定。

这符合当前体验护栏：正常或较快 retrieve 在正常/好鱼口下仍可用，弱鱼口与高速度组合才显著恶化。

## 为什么当前不用更高次方

probe 比较了 `u`、`u²`、`u⁴`。一旦 `u>=1` 已经作为 angle-local hard-zero，q>1 区间的整体 response 主要由“有多少 latent angle 追不上”决定；二次与四次在整体结果上的差异明显缩小。

因此当前没有独立策略故事支持额外指数自由度。`u²` 比 `u⁴` 更容易解释，也更便于 calibration。

## hard infeasible 的作用域

`u_close(θ) >= 1` 只说明当前 latent angle 下，拟饵径向拉开速度达到或超过该鱼的 Closing 能力尺度。没有 encounter geometry 时，它仍是高 Closing burden，不直接产生 `C_conditional(θ)=0`。

不能推出：

```text
q >= 1 → whole feeding mode = 0
```

因为其它角度可能是横切或朝鱼运动。最终仍必须：

```text
θ → C_conditional(θ) → Eθ[C_conditional(θ)]
```

## Functional Capacity

`intercept_capacity` 是鱼侧能力输入。相同 presentation 下，更强的鱼得到更小 q，因此不能再额外按“强鱼/弱鱼身份”乘第二次能力 penalty。

## 仍未闭合

- `K_close` 的 production calibration；
- `intercept_capacity` 的 production 来源与尺度；
- `u_close=1` 边界是否采用严格 `>=1` 或带极小数值容差；
- uniform latent-angle prior 是否长期成立；
- 是否存在需要独立 consideration-distance owner 才能恢复的距离效应。

## 被拒绝 / 暂不采用

- whole-mode `q>1` hard-zero；
- 先平均 `u_close` 或 ClosingCost 再做 response projection；
- 为拟合效果直接选高次幂；
- 引入没有 owner 的绝对鱼距 D；
- Functional Capacity 已进入 q 后再按鱼身份重复处罚。

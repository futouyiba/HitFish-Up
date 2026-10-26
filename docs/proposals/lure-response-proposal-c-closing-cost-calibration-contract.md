# Proposal C｜Closing Cost Calibration Contract

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

当前不冻结单一 `K_close` 数值。

`ClosingCost` 的第一版拓扑保持：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
u_close(theta) = max(0, q * directional_cosine(theta))

if u_close(theta) >= 1:
    C_conditional(theta) = 0
else:
    ClosingCost(theta)
    = K_close * u_close(theta)^2 * ActivityCostMultiplier(Activity)
```

但 `K_close` 必须与以下三项联合标定：

```text
1. q 的真实 production 分布
2. RelativeBearingPrior 的 dimensionality / family
3. ActivityCostMultiplier 的生产范围
```

在这三项未闭合前，单独给 `K_close` 一个值属于无依据的数值冻结。

## 2. 为什么 K_close 不能脱离 q 标定

在 reference Activity（ActivityCostMultiplier=1）且 `q <= 1` 时，若 prior 为 isotropic：

```text
Isotropic2D:
E[u_close^2] = q^2 / 4

Isotropic3D:
E[u_close^2] = q^2 / 6
```

因此同一个 `K_close` 在 2D 与 3D 下得到的平均 soft Closing burden 相差 50%。

更重要的是，`q` 本身平方进入 cost。

例如若把 reference ordinary average Closing burden 暂定为约 `0.08`，则仅作敏感性说明：

```text
ordinary q = 0.5
→ K_close ≈ 1.28 (2D)
→ K_close ≈ 1.92 (3D)

ordinary q = 0.7
→ K_close ≈ 0.65 (2D)
→ K_close ≈ 0.98 (3D)
```

这组数字不是 production candidate，只证明 `K_close` 对 `q` 与 prior 很敏感。

因此不能先拍 `K_close=0.8`，再让 InterceptSpeedLimit 或 prior 去适配它。

## 3. K_close 的职责

`K_close` 只控制：

> 在 Closing utilization 已经由几何和能力算出之后，soft pursuit burden 进入 DecisionMargin 的尺度有多大。

它不承担：

- 修正错误的 InterceptSpeedLimit；
- 补偿错误的 lure speed reference frame；
- 补偿 2D / 3D prior 选择；
- 表达 Activity；Activity 只通过 `ActivityCostMultiplier` 进入；
- 表达 Prediction / Risk；这些有独立 owner；
- 表达 hard feasibility；`u_close >= 1` 已有独立局部 hard-zero。

## 4. 标定目标

应先建立 production / representative `q` basket，再反推 `K_close`。

至少分：

```text
low utilization
ordinary utilization
high-but-feasible utilization
near-boundary utilization
infeasible angles
```

第一版体验要求：

### Low utilization

轻松可追的目标只产生轻微 burden，不能因为存在运动就显著压低 Good / Preferred。

### Ordinary utilization

在正常 retrieve 与典型 fish capability 组合下，Closing 应成为普通 combined burden 的主要组成之一，但不能单独让 Good 大面积归零。

结合当前 combined-burden Working guardrail：

```text
ordinary total soft burden ≈ 0.12 ~ 0.20
```

Closing 的 ordinary contribution 可作为其中较大的一项，但不应默认独占整个预算。

### High-but-feasible utilization

接近能力上沿时，二次 cost 应明显抬升，使 fast presentation 对 Good / Marginal 更敏感。

### Near-boundary / infeasible

`u_close >= 1` 已由 angle-local hard-zero 承担。

不能靠把 `K_close` 调得极大来模拟 hard infeasible，否则 soft/hard 语义会混淆。

## 5. 与 latent bearing 的关系

当前 RelativeBearingPrior contract 仍有一个 OPEN：

```text
Horizontal2D
vs
Full3D
```

因此第一版 calibration 必须按 prior 明确记录：

```text
K_close@Isotropic2D
或
K_close@Isotropic3D
```

在 dimensionality 未裁定前，不允许跨 prior 复用同一 calibration 结论。

若未来启用 ExplicitDirectional prior，也需要重新验证 Closing burden distribution；不能假设 isotropic 标定自动成立。

## 6. 与 Activity 的关系

Response 只消费 Cowork / Fish Condition 上游提供的 `ActivityCostMultiplier(Activity)`。

本页不定义或修改 Activity 曲线。

必须保持：

```text
ClosingCost
= base geometric burden
× ActivityCostMultiplier
```

而不是：

```text
ClosingCost
+ separate ActivityPenalty
```

Activity 不应形成第四个独立 soft burden。

`K_close` 应优先在 reference Activity 下标定；之后再检查 Activity multiplier 是否把 ordinary cases 推入 heavy burden 区。

## 7. Production 标定顺序

建议顺序：

```text
A. 冻结 InterceptSpeedLimit 来源 / cohort scale
B. 收集或构造代表性 lure_speed_relative_to_water 分布
C. 得到 q distribution
D. 裁定 RelativeBearingPrior dimensionality
E. 在 reference Activity 下反推 K_close
F. 再接入 Activity multiplier 做 stress test
G. 与 Prediction / Risk 做 combined-burden regression
```

不能倒过来从一个任意 `K_close` 反推鱼速。

## 8. 必要 telemetry / probe

至少输出：

```text
q distribution
u_close distribution by latent bearing
hard-infeasible bearing share
ClosingCost distribution
ClosingCost share of total soft burden
Good C=0 rate by q bucket
Preferred C=0 rate by q bucket
```

并按：

```text
species/cohort
lure / presentation family
Activity band
prior dimensionality
```

切片检查。

## 9. 当前 OPEN

- production `q` 分布；
- InterceptSpeedLimit 的最终来源与 size scaling；
- RelativeBearingPrior 是 2D 还是 3D；
- ActivityCostMultiplier 的生产曲线与范围（由 Cowork / Fish Condition 侧闭合）；
- reference ordinary Closing burden 的最终目标；
- 最终 `K_close` production 数值。

本页冻结的是 `K_close` 的职责、依赖与标定顺序，不冻结最终系数。
# Proposal C｜Decision Margin → Response Projection

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

在当前 FoodValue / FeedingMotivation 联合标尺下，第一版继续采用 clipped linear projection，不引入 sigmoid、指数或额外 soft gate。

Working calibration seed：

```text
M0 = 0.00
M1 = 0.30

C(Margin)
= clamp((Margin - M0) / (M1 - M0), 0, 1)
= clamp(Margin / 0.30, 0, 1)
```

因此：

```text
Margin <= 0    → C = 0
Margin = 0.05  → C ≈ 0.17
Margin = 0.10  → C ≈ 0.33
Margin = 0.15  → C = 0.50
Margin = 0.20  → C ≈ 0.67
Margin = 0.30  → C = 1.00
Margin > 0.30  → C = 1.00
```

`M0/M1` 是 Response projection anchors，不是 FeedingMotivation 的 `M`，也不是生物学常数。

## 2. 为什么令 M0 = 0

当前 `DecisionMargin` 的语义已经是：

> 当前 prey-specific value 与 trigger，扣除 closing / prediction / risk burden 和 willingness threshold 后，还剩多少净决策余量。

因此 `Margin = 0` 正好是愿不愿意出手的决策边界。

第一版直接规定：

```text
Margin <= 0
→ ResolvedNonResponsive
→ C = 0
```

这使 `WillingnessThreshold` 真正成为阈值，而不是“阈值附近仍偷偷保留一截正响应”的软中心。

如果未来体验证据显示负 margin 仍需保留非零 Feeding response，应重新解释 DecisionMargin / threshold 的语义，而不是先把 `M0` 偷移到负值。

## 3. 为什么 M1 首轮取 0.30

当前联合 calibration seed：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00
K_mot     = 0.40
T_ref     = 0.40
```

因此在参考 Motivation、无 Trigger、无 Cost 时：

```text
Preferred margin = 0.60
Good margin      = 0.30
Marginal margin  = 0.00
Poor margin      = -0.40
```

选择 `M1 = 0.30` 会得到一个容易解释的 reference behavior：

```text
Preferred → C = 1
Good      → C = 1
Marginal  → C = 0
Poor      → C = 0
```

这不表示 Preferred 与 Good 永远一样。Good 只有在 reference-zero-burden 条件下达到满 retention；加入普通 Closing / Prediction / Risk burden 后会很快进入中段，而 Preferred 有更大的余量吸收这些 burden。

例如：

```text
Good + total soft cost 0.15
→ Margin = 0.15
→ C = 0.50

Preferred + total soft cost 0.15
→ Margin = 0.45
→ C = 1.00
```

因此 `M1=0.30` 保留了 Preferred 对 burden 的鲁棒性，而不是要求 reference-zero-burden 时两者就必须得到不同 C。

## 4. 与 Marginal 翻转的关系

当前 Marginal 被设计为策略翻转档。

在 reference Motivation 下：

```text
Marginal
→ Margin = 0
→ C = 0
```

若通过高 Motivation、低 burden 或合法 Trigger 得到：

```text
Margin = 0.10
→ C ≈ 0.33

Margin = 0.15
→ C = 0.50
```

因此 Marginal 一旦真正越过阈值，不只是得到几乎看不见的 epsilon response；中等有利组合可以形成可感知的恢复。

但普通 Trigger Working budget约 `0.10`、上沿约 `0.15`，单独 Trigger 也不会把 Marginal 自动推到 `C=1`。

## 5. 与 Poor 的关系

当前 joint seed 有一个重要保护：

```text
Poor
+ max Motivation (M=1)
+ Trigger 0.15
+ zero soft cost
→ Margin = -0.05
→ C = 0
```

因此 Poor 不会仅靠普通最大 Motivation + Trigger 被普遍救活。

若另有合法 prey-specific 正向项（例如 SizePreferenceAdjustment / DietaryShiftDelta）把 margin 推到略高于0，则 Poor 可以得到小到中等非零 response；这符合“极有利组合下偶发越线”的语义。

`Reject` 不走 projection：

```text
Reject
→ whole prey feeding response = 0
```

## 6. 为什么暂不使用 sigmoid

Sigmoid 会至少引入：

- center；
- slope；
- 是否允许负 margin 获得正 response；
- 两端永远不真正到0/1的处理。

当前没有证据购买这些自由度。

现有 relation / Motivation / Trigger / Cost 已经提供主要行为差异。Projection 第一版只需回答：

> 净 margin 从刚过线到充分过线时，response retention 如何增长？

clipped linear 已足够，而且容易从 controlled basket 反推。

## 7. 与 latent angle 的顺序

Projection 必须保持在 latent-angle 内执行：

```text
θ
→ hard closing feasibility
→ ClosingCost(θ)
→ DecisionMargin(θ)
→ C_conditional(θ)
→ Eθ[C_conditional(θ)]
```

禁止：

```text
Eθ[Margin]
→ Projection
```

因为 clipped linear 含有0和1两端 clipping，平均前后不等价；且 angle-local hard infeasible 必须保留为局部0。

## 8. C 的语义

`C` 是当前 Feeding response / retention strength，不直接解释成：

- 真实攻击概率；
- 每秒 bite probability；
- prey identity probability；
- 最终 Candidate probability。

后续仍有：

```text
prey support
× Eθ[C_conditional]
→ C_prey

alternative prey interpretations
→ Feeding composition

Interaction
→ captureRetention

Candidate Resolver
→ native candidate weight / roll
```

因此 projection 不需要单独承担最终 bite-rate calibration。

## 9. Working seed 的回归点

首轮应固定这些 probe 点：

```text
Margin -0.10 → C 0
Margin  0.00 → C 0
Margin  0.05 → C 1/6
Margin  0.10 → C 1/3
Margin  0.15 → C 1/2
Margin  0.20 → C 2/3
Margin  0.30 → C 1
Margin  0.50 → C 1
```

并联合检查：

- Good + ordinary burden 能落入中段；
- Preferred 对同样 burden 更鲁棒；
- Marginal favorable case 可从0翻到约0.3～0.6；
- Poor 不被普通 Motivation + Trigger 普遍救活；
- Reject 永远0；
- Unknown 必要输入不进入 projection。

## 10. 当前 OPEN

- `M1=0.30` 是否能在完整 latent-angle / prey-support / Candidate 联算中保持合理体验差；
- 最终是否需要把满 response anchor 从0.30微调到其它值；
- support × response 后是否造成过强衰减，需要由完整链路而不是 projection 单点判断；
- temporal exposure / opportunity integration 补齐后，瞬时 `C` 与累计中鱼效率的映射；
- Production telemetry / simulation target 尚未建立。

本页冻结第一版 projection topology、`M0=0` 的阈值语义，并提供 `M1=0.30` 的 Working calibration seed；不声明 production calibration 已完成。

# Proposal C｜Decision Margin → Response Projection

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

第一版继续采用 **clipped linear projection**，不引入 sigmoid、指数、幂函数或额外 soft gate。

本轮修正的是满响应锚，而不是曲线族：

```text
M0 = 0.00
M1 = 0.40

C(Margin)
= clamp((Margin - M0) / (M1 - M0), 0, 1)
= clamp(Margin / 0.40, 0, 1)
```

旧 Working seed `M1=0.30` 被本页 supersede。

新的参考点：

```text
Margin <= 0    → C = 0
Margin = 0.05  → C = 0.125
Margin = 0.10  → C = 0.25
Margin = 0.15  → C = 0.375
Margin = 0.20  → C = 0.50
Margin = 0.30  → C = 0.75
Margin = 0.40+ → C = 1.00
```

`M0/M1` 是 Response projection anchors，不是 FeedingMotivation 的 `M`，也不是生物学常数。

## 2. 为什么继续使用 clipped linear

当前 `DecisionMargin` 已经回答：

> 当前 prey-specific value 与 trigger，扣除 closing / prediction / risk burden 和 willingness threshold 后，还剩多少净决策余量。

因此：

```text
Margin <= 0
→ ResolvedNonResponsive
→ C = 0
```

这是明确的决策边界。

在 `Margin>0` 后，当前没有独立策略故事要求：

- 刚越线时额外迟钝；
- 中段突然陡升；
- 高段渐近但永不到 1；
- 某个额外中心点附近最敏感。

Sigmoid、指数或 power curve 都会为这些行为新增自由度。现阶段没有证据购买这些自由度，所以第一版继续保持线性。

如果未来 controlled fixtures 明确显示“同样的 margin 差在不同区间应产生不同 response sensitivity”，再重新打开曲线族。

## 3. 为什么撤回 M1 = 0.30

参考 Motivation、无 Trigger、无 soft burden 时：

```text
Preferred margin = 1.00 - 0.40 = 0.60
Good margin      = 0.70 - 0.40 = 0.30
Marginal margin  = 0.40 - 0.40 = 0.00
Poor margin      = 0.00 - 0.40 = -0.40
```

若 `M1=0.30`：

```text
Preferred → C = 1
Good      → C = 1
Marginal  → C = 0
Poor      → C = 0
```

这会让 Good 与 Preferred 在最干净的 reference 条件下完全饱和为同一结果。两档差异只有等 Closing / Prediction / Risk burden 出现后才重新展开。

这不是错误，但会浪费一部分 response dynamic range，并让 `Preferred > Good` 的结构差异过度依赖“是否刚好存在 burden”。

因此第一版把满响应锚上移到 `0.40`。

## 4. M1 = 0.40 的行为

参考 Motivation、无 Trigger、无 burden：

```text
Preferred margin = 0.60 → C = 1.00
Good margin      = 0.30 → C = 0.75
Marginal margin  = 0.00 → C = 0
Poor margin      = -0.40 → C = 0
```

这样保留了：

- Preferred 在理想条件下达到满响应；
- Good 在理想条件下很强，但仍有可见 headroom；
- Marginal 仍位于策略翻转边界；
- Poor 仍需要极端有利组合才可能越线；
- Reject 仍不进入 projection。

## 5. 对 soft burden 的敏感性

在 reference Motivation、无 Trigger 下：

| Total soft burden | Preferred C | Good C |
|---:|---:|---:|
| 0.00 | 1.00 | 0.75 |
| 0.08 | 1.00 | 0.55 |
| 0.18 | 1.00 | 0.30 |
| 0.35 | 0.625 | 0.00 |

因此：

- Preferred 对 ordinary burden 仍有明显鲁棒性；
- Good 在 light / ordinary burden 下不会立即归零，但会明显下降；
- heavy burden 可以把 Good 压到 0；
- Preferred 在 heavy burden 下仍保留响应。

这比 `M1=.30` 更充分利用 `[0,1]` response 范围，同时不改变 DecisionMargin 自身的 relation / threshold 语义。

## 6. 与 Marginal 翻转的关系

Marginal 在 reference Motivation、零 Trigger、零 burden 时仍然：

```text
Margin = 0
→ C = 0
```

若合法 Trigger 或高 Motivation 让它越线：

```text
Margin = 0.10 → C = 0.25
Margin = 0.15 → C = 0.375
Margin = 0.20 → C = 0.50
```

因此 Marginal 仍可以形成可感知 rescue，但不会因为单个 `0.10～0.15` Trigger 就快速接近满响应。

这更符合 StateTrigger 的职责：它可以改变边缘目标的策略可用性，但不应轻易抹平 relation class。

## 7. 与 Poor / Reject 的关系

Poor 的极端越线窗口由 FoodValue、Motivation tail relief、Trigger 与 soft burden共同决定。

如果最终只得到：

```text
Margin = 0.05
```

那么当前 projection 给：

```text
C = 0.125
```

它仍然是弱响应，不会因为刚刚跨线就得到过大的 retention。

`Reject` 不进入 projection：

```text
Reject
→ typed hard semantic zero
```

## 8. 为什么暂不使用 convex / concave power curve

可以写成：

```text
C = (Margin / M1)^gamma
```

但：

- `gamma > 1` 会额外压低刚越线和中段 response；
- `gamma < 1` 会额外放大刚越线 response；
- `gamma` 本身没有新的 owner，也没有独立可验证的策略故事。

当前关系档、Motivation threshold、Trigger 与 soft burden 已经决定主要策略差异。Projection 只负责把净 margin 映射到 retention strength，不应该再承担第二层隐含平衡。

## 9. latent bearing 顺序

Projection 必须在 latent bearing 内执行：

```text
theta
→ ClosingCost(theta)
→ DecisionMargin(theta)
→ C_conditional(theta)
→ E_theta[C_conditional(theta)]
```

禁止：

```text
E_theta[Margin]
→ Projection
```

因为 clipping 使二者不等价。

当前 Closing 已撤回 `u_close>=1 → hard-zero`；因此本页不再保留旧的 angle-local hard Closing gate 描述。真正的 hard interception gate 若未来获得合法 encounter geometry，再由对应 contract 单独定义。

## 10. C 的语义

`C` 是当前 Feeding response / retention strength，不直接解释成：

- 真实攻击概率；
- 每秒 bite probability；
- prey identity probability；
- 最终 Candidate probability。

后续仍有：

```text
calibrated prey support
× E_theta[C_conditional]
→ C_prey

alternative prey interpretations
→ Feeding composition

Interaction
→ captureRetention

Candidate Resolver
→ native candidate surface / roll
```

因此 projection 不承担最终 bite-rate calibration。

## 11. Working regression points

首轮固定：

```text
Margin -0.10 → C 0
Margin  0.00 → C 0
Margin  0.05 → C 0.125
Margin  0.10 → C 0.25
Margin  0.15 → C 0.375
Margin  0.20 → C 0.50
Margin  0.30 → C 0.75
Margin  0.40 → C 1.00
Margin  0.60 → C 1.00
```

联合检查：

- Preferred reference-clean case 达到 1；
- Good reference-clean case 保留约 0.75，而非直接饱和；
- Good + ordinary burden 保持非零但明显下降；
- Marginal favorable case 可以翻正，但单个 Trigger 不应接近满响应；
- Poor 极端越线仍只得到弱 response；
- Reject 永远 0；
- Unknown 必要输入不进入 projection。

## 12. 当前 OPEN

- `M1=0.40` 是否在真实 prey-support 分布与完整 Response basket 下保持合理 effect size；
- production telemetry 是否要求微调到 `0.35～0.45` 一类邻域；
- 是否存在真实 fixture 证明线性 sensitivity 不够，需要非线性 curve；
- `support × response` 后整体 attenuation 是否与 Candidate 体验预算匹配。

本页冻结第一版 projection topology、`M0=0` 的阈值语义，并把 Working 满响应锚从 `0.30` 更新为 `0.40`；不声明 production calibration 已完成。

# 方案 C｜Decision Margin → C_mode：Response Projection Working Closure

日期：2026-10-26  
状态：Working Closure，非 Current，非生产参数。

相关护栏：[`lure-response-proposal-c-anti-design-guardrails.md`](./lure-response-proposal-c-anti-design-guardrails.md)。其中集中记录本主线已被反例击穿、后续不应静默回退的反设计与重开条件。

## 1. 本轮问题

前面已经把 Feeding Response 的连续主干压缩成：

```text
Target Relation / Food Value
+ Feeding Motivation
+ TaskStrain
→ Decision Margin
```

本轮只问最后一跳：

```text
Decision Margin
→ C_mode
```

需要线性、sigmoid、分段档位，还是更复杂的 projection？

可执行 probe：`../../prototypes/lure-response/proposal_c_response_projection_probe.py`。

## 2. 比较原则

不追求单次拟合误差最低，而优先：

1. 满足现有 experience budget；
2. 保持单调；
3. 保留真正的 hard zero / hard one 边界；
4. 不引入没有独立玩法价值的自由度；
5. 方便策划理解、标定与回归测试。

## 3. 三类候选

### 3.1 截断线性

```text
C = clamp((Margin - M0) / (M1 - M0), 0, 1)
```

含义：

- Margin <= M0：已解析但不响应；
- M0～M1：响应强度线性增长；
- Margin >= M1：已足够有利，达到满 retention。

优点：参数少、可解释、可直接形成 exact zero / exact one。

### 3.2 Sigmoid

```text
C = sigmoid((Margin - midpoint) / scale)
```

优点：阈值附近平滑。

缺点：普通 sigmoid 对任意有限 Margin 都不真正等于 0 或 1；若还要另外 clamp / hard gate，就会重新引入边界参数。当前 experience budget 上，它只获得很小的拟合改善，没有购买新的策略语义。

### 3.3 Decision Strength 档位

例如：

```text
Reject / Weak / Marginal / Positive / Strong
→ 0 / .2 / .5 / .8 / 1
```

这与中层样板的 Working `Decision Strength` 语言兼容，但如果把它作为 Production numeric core，会把连续的 Motivation / TaskStrain 差异重新量化成台阶，并制造阈值跳变。

因此更适合作为 Explain / Debug projection，而不是当前默认 numeric owner。

## 4. Probe 结果

对当前 7 个 experience-budget case，用同一组 Decision Margin：

- 截断线性 working fit：RMSE 约 `0.061`；
- sigmoid working fit：RMSE 约 `0.054`；
- 简单五档 bucket 更差，并出现明显台阶误差。

sigmoid 的改善幅度很小，主要来自阈值附近平滑；它没有解决新的领域问题，也没有产生新的 ranking / reversal 能力。

因此当前没有足够理由为它增加参数和调试成本。

## 5. 当前推荐

第一版优先：

```text
DecisionMargin
→ clipped linear Response Projection
→ C_mode
```

即：

```text
C_mode = clamp((DecisionMargin - M0) / (M1 - M0), 0, 1)
```

其中 `M0 / M1` 不是物理常数，而是由 Reference Fishing Stories 的体验预算反推的 calibration anchors。

这不是说真实行为一定线性，而是：

> 在当前证据下，线性已经能表达需要的 strategy ordering / reversal；更复杂曲线尚未购买额外能力。

## 6. Decision Strength 的保留位置

中层样板中的：

```text
Strong | Positive | Marginal | Weak | Reject
```

仍然有价值，但建议作为从 continuous Decision Margin / C_mode 派生出的 Explain View，例如：

```text
C >= .85  → Strong
.55-.85   → Positive
.25-.55   → Marginal
0-.25     → Weak
C = 0     → Reject / NonResponsive（需结合 reason 区分）
```

具体阈值仍未冻结。

它不取得 numeric authority，也不反向决定 `C_mode`。

## 7. 一个重要边界

`ResolvedNonResponsive C=0` 与 `ResolutionIncomplete no scalar` 仍然完全不同。

截断线性产生的 0 只能表示：

```text
必要输入已经解析
+ Feeding mode 有效
+ Decision Margin 未越过响应阈值
→ ResolvedNonResponsive
```

Unknown 仍不得进入 projection。

## 8. 当前最小计算结构

现在 Proposal C 的 Feeding numeric hypothesis 可以进一步收成：

```text
Target Relation
→ FoodValue

FunctionalCapacity + presentation task facts
→ TaskStrain
→ convex TaskCost

Feeding Motivation
→ Willingness Threshold

FoodValue - TaskCost - Threshold
→ DecisionMargin

DecisionMargin
→ clipped linear projection
→ C_mode
```

再由 Interaction 内 mode composition 得到 `captureRetention C_i,j`。

## 9. 仍未冻结

- Target Relation 各档的 production numeric anchors；
- `TaskStrain → TaskCost` 的最终函数与参数；
- `Motivation → Threshold` 的最终函数与参数；
- `M0 / M1` 的 reference calibration；
- Feeding 之外的 Defense / Investigation 是否共享同一 projection family；
- Complete Modes 的 production aggregation operator。

当前只关闭一个问题：**没有证据要求把最后一跳做得比截断线性更复杂。**

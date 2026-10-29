# 方案 C｜Decision Margin → C_mode：Response Projection

日期：2026-10-26

相关护栏：[`../design-guardrails/lure-response.md`](../design-guardrails/lure-response.md)。其中集中记录本主线已被反例击穿、后续不应静默回退的反设计与重开条件。

## 1. 本轮问题

前面已经把 Feeding Response 的连续主干压缩成：

```text
Target Relation / Food Value
+ Feeding Motivation
+ Activity-aware soft Closing cost and other admitted task consequence
→ Decision Margin
```

本页只比较三种 `Decision Margin → C_mode` 候选：

1. 截断线性；
2. sigmoid；
3. `Decision Strength` 档位。

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

- 必须满足 `M0 < M1`；
- `Margin ≤ M0`：已解析但不响应，输出 `C_mode = 0`；
- `M0 < Margin < M1`：响应强度在线性区间内增长；
- `Margin ≥ M1`：达到满 retention。

`M0` 是非响应阈值，`M1` 是满 retention 的 calibration anchor。两者都是体验预算的标定参数，不是物理常数。

优点：参数少、可解释、可直接形成 exact zero / exact one。

### 3.2 Sigmoid

```text
C = sigmoid((Margin - midpoint) / scale)
```

优点：阈值附近平滑。

缺点：普通 sigmoid 对任意有限 Margin 都不真正等于 0 或 1；若还要另外 clamp / hard gate，就会重新引入边界参数。在这 7 个工作 fixture 上，sigmoid 的 RMSE 略低，但它只增加了 `midpoint` 和 `scale` 两个参数。当前没有证据表明这点局部改善值得增加这些参数及其调试成本。

### 3.3 Decision Strength 档位

例如：

```text
Reject / Weak / Marginal / Positive / Strong
→ 0 / .2 / .5 / .8 / 1
```

这与中层样板的 Working `Decision Strength` 语言兼容，但如果把它作为 Production numeric core，会把连续的 Motivation / Activity-soft-cost 差异重新量化成台阶，并制造阈值跳变。

因此更适合作为 Explain / Debug projection，而不是当前默认 numeric owner。

## 4. Probe 结果

Probe 使用 7 个人工 experience-budget case，并把每个目标区间的中点作为诊断目标。RMSE 只用于比较候选曲线，不代表生产拟合误差：

- 截断线性：`0.0614`；
- sigmoid：`0.0545`；
- 五档 bucket：`0.0916`。

sigmoid 的改善来自阈值附近的平滑。这个 probe 没有显示它带来新的策略排序或反转能力，因此当前没有理由为它增加 `midpoint`、`scale` 或额外边界参数。

## 5. 当前推荐

第一版优先：

```text
DecisionMargin
→ clipped linear Response Projection
→ C_mode
```

Projection 只接受已闭合的 `Decision Margin`：

```text
ResolutionIncomplete / Unknown
→ 不调用 projection，不输出 C_mode

ResolvedNonResponsive
→ 调用 projection，输出 C_mode = 0

ResolvedResponsive
→ 调用 projection，输出 0 < C_mode ≤ 1
```

`clamp` 处理的是已解析的数值范围，不负责把 Unknown 转换成 0。

即：

```text
C_mode = clamp((DecisionMargin - M0) / (M1 - M0), 0, 1)
```

其中 `M0 / M1` 不是物理常数，而是由 Reference Fishing Stories 的体验预算反推的 calibration anchors。关联验收矩阵中的 `clamp(Margin / 0.45, 0, 1)` 只是另一组验收 fixture 的临时归一化写法，不冻结本页的 `M0 / M1`，也不证明 `M1 - M0 = 0.45`。

这不是说真实行为一定线性，而是：

> 在当前证据下，线性已经能表达需要的 strategy ordering / reversal；更复杂曲线尚未购买额外能力。

## 6. Decision Strength 的保留位置

中层样板中的：

```text
Strong | Positive | Marginal | Weak | Reject
```

仍然有价值，但建议作为从 continuous Decision Margin / C_mode 派生出的 Explain View，例如：

```text
C_mode ≥ .85  → Strong
.55 ≤ C_mode < .85 → Positive
.25 ≤ C_mode < .55 → Marginal
0 < C_mode < .25 → Weak
C_mode = 0 → Reject / NonResponsive
```

这些阈值只用于说明 Explain View 的形状，不是当前配置。`C_mode = 0` 仍需结合输出 status 和 reason 区分已解析不响应、不可行和其他 hard gate。

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

## 8. 当前工作假设的计算链

以下只是当前研究链路，不是生产公式：

```text
Target Relation
→ FoodValue

species × size cohort → InterceptSpeedLimit
+ presentation task facts
→ Closing feasibility
→ Activity-aware soft Closing cost
→ TaskAffordance

Feeding Motivation
→ candidate Willingness Threshold

FoodValue - candidate TaskCost - candidate Threshold
→ DecisionMargin

DecisionMargin
→ clipped linear projection
→ C_mode
```

只有完整闭合的 mode 才能产生 `C_mode`。它随后按 Interaction 的 mode composition 规则进入 `captureRetention`。本页不重新定义该桥接。

## 9. 仍未冻结

- Target Relation 各档的 production numeric anchors；
- `TaskCost` 的 Working 结构与参数；它必须把 physically-feasible Closing 的 Activity soft cost 与其它已 admission 的 task consequence 分开表示；
- `Motivation → Threshold` 的最终函数与参数；
- `M0 / M1` 的 reference calibration；
- Feeding 之外的 Defense / Investigation 是否共享同一 projection family；
- Complete Modes 的 production aggregation operator；
- `C_mode` 在完整 Candidate / Roll 链中的最终生产接入位置。

本页只关闭一个 Working 选择：

> 在当前人工体验预算、单调性和 hard-boundary 要求下，先使用 clipped linear projection。现有证据没有要求把最后一跳做得更复杂。

这不是生产参数批准，也不是完整响应链路闭合。

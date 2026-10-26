# Proposal C：Prey Support → Response Retention 映射

> Status: Working Closure / production calibration unresolved
>
> Scope: prey interpretation support 到 feeding response contribution 的桥接

## 结论

第一版不引入额外的非线性 `RecognitionProjection`。直接复用 support 标尺：

```text
R = support
C_prey_mode = support × C_conditional
```

这里的乘法语义是：**猎物解释证据强度对该 interpretation 最终 feeding response contribution 的保留程度**。

它不是：

- prey identity probability；
- Bayesian posterior；
- 多 prey interpretation 的 mixture probability；
- FoodValue；
- 咬口概率。

因此 `support=0.7` 只表示：在当前 Working topology 下，这条 prey interpretation 以 0.7 的 retention 参与 response contribution。不能转述成“70% 概率它是一条小鱼”。

## 为什么不再加一条非线性 projection

support 本身已经是连续的“解释证据强度”。若再引入：

```text
support → soft gate / S curve / concave boost → R
```

就必须另外解释：

- 为什么 0.4 的证据应被额外压低；
- 为什么 0.8 的证据应被额外放大或压缩；
- 新曲线的阈值、斜率、饱和点分别购买了什么独立玩法能力。

当前没有这样的反例或体验需求。

Working probe 对比了：

- identity：`R=support`；
- soft gate：低证据额外压低；
- concave boost：低中证据额外放大。

后二者都会新增不可独立识别的自由度。当前无法从已有 strategy story 或 experience budget 证明它们更正确。

因此按最小自由度原则，第一版保留 identity。

## 重要边界

### 1. support 仍然不是概率

虽然数值区间同为 `[0,1]`，也虽然当前 identity 使：

```text
R = support
```

但语义没有因此改变。

数值标尺复用不等于概率解释。

### 2. 不需要新的生产对象

当前没有必要创建：

```text
RecognitionRetention
RecognitionProjectionPacket
```

等独立 runtime authority。

实现可以直接：

```text
C_prey_mode = support × C_conditional
```

Explain/debug 层再注明该乘法的 cause：`prey interpretation support retention`。

只有未来出现独立缓存、跨 mode 复用、authoring 或 telemetry 需求时，才考虑把它实体化。

### 3. support Unknown 不得乘成 0

```text
support = Unknown
```

不是：

```text
support = 0
```

因此 required prey interpretation support 未解析时，mode 保持 `ResolutionIncomplete`，不能执行 identity multiplication。

### 4. NoMatch 与 Reject 分离

```text
support = 0 / NoMatch
```

表示没有足够证据按该 prey interpretation 解释当前 presentation。

```text
Target Relation = Reject
```

表示即使目标已经被识别为该 prey，鱼仍不接受它作为 feeding target。

二者不能合并成一个 zero reason。

## 当前模式内计算顺序

对每个 prey interpretation：

```text
prey support s

FoodValue
+ StateTriggerValue
- TaskCost(theta)
- WillingnessThreshold(Motivation)
→ DecisionMargin(theta)
→ ResponseProjection
→ C_conditional(theta)
→ E_theta[C_conditional(theta)]
→ C_conditional

C_prey_mode = s × C_conditional
```

角度积分必须先于 support retention 的最终乘法。support 不参与 latent-angle distribution。

## 多 prey interpretation composition

同一物理拟饵的 baitfish / crayfish / frog 等 interpretation 默认属于 alternative sibling interpretations，而不是独立 feeding opportunities。

第一版：

```text
C_feed = max(C_prey_mode_1, C_prey_mode_2, ...)
```

不求和，不做 probability union，不把 support 归一化成 mixture probability。

未来只有在出现明确、可验证的 cross-interpretation synergy 时，才重新打开 composition operator。

## Reopen gate

只有出现以下任一证据，才重新考虑非线性 `R(support)`：

1. 低 support 即使乘以很高 `C_conditional`，仍系统性高估 response；
2. 高 support 被 identity 显著低估，导致强 prey interpretation 无法接近 reference-good；
3. strategy story 要求一个明确的 recognition threshold / saturation，而该能力无法由现有 prey support authoring 本身表达；
4. calibration across prey families 显示统一 identity 无法同时成立。

在这些证据出现前，identity 是默认 Working Closure。

## 当前状态

- `R=support`：Working Closure。
- support 作为概率：Rejected interpretation。
- 额外 soft gate / S curve：Deferred，无独立证据。
- 独立 Recognition runtime object：Deferred，无独立 lifecycle。
- production numeric calibration：仍需以后结合 full response experience budget 验证。

Reference probe：`prototypes/lure-response/proposal_c_support_retention_projection_probe.py`。

# Lure Response Design Guardrails

日期：2026-10-26  
状态：Working Guardrails，非 Current。

来源：这些护栏主要由 Proposal C 的反例、counterfactual probe、Candidate seam 对齐与体验标定推演形成。它们不取得 Current Authority；但在被新的 Owner 裁定或更强证据 supersede 前，用于防止后续 Lure Response 设计静默退回已知错误。

## 1. 不把所有输入做成匿名连乘

### 反设计

```text
C_mode = FoodCoeff × MotivationCoeff × TaskCoeff × StateBonus × ...
```

### 为什么拒绝

不同输入承担不同因果角色：

- Target / Food Value 回答“值不值得吃”；
- Feeding Motivation 回答“现在有多愿意为了食物出手”；
- ClosingCost 回答当前径向追赶负担；
- RiskCost 回答已解析风险 cue 在 Wariness 下的软抑制；
- `u_close >= 1` 不是单独的完整 encounter hard gate；真正 hard infeasibility 需要独立 encounter geometry / reaction-window contract；
- ResolvedNonResponsive 是已解析的终态，不是可被其它高系数补偿的小数。

统一连乘会把这些语义压成同一种折扣，并且维度越多，整体数值越容易无意义地下沉。

### 重开条件

只有新的实证或 counterfactual 能证明某两个变量确实属于同一种独立 retention 机制，而且乘法更符合排序与体验预算时，才允许局部乘法；不能据此恢复“所有东西统一连乘”。

## 2. 不使用万能 `stateBonus / pauseBonus / vulnerabilityCoeff`

### 反设计

```text
recent_move_then_pause → +20%
vulnerable_like       → ×1.3
```

### 为什么拒绝

同一个表象可能通过不同机制生效：

- pause 可以降低当前 TaskDemand；
- pause 可以延长 favorable dwell / exposure；
- recent motion 可以影响 attention / prediction history；
- vulnerable-like 可以是目标语义，但不自动等于独立数值增益。

匿名 bonus 会重复结算同一原因，也会把“语义识别”偷换成“已证明的独立 response effect”。

### 重开条件

只有在控制 Perception、TaskAffordance、temporal exposure、Target Value、Motivation 等现有 Owner 后，仍存在稳定、可复现、可学习的 residual ranking，才允许把某个 state semantic 晋升为独立 valuation 项。

## 3. 不把 `Prey Opportunity` 做成新的权威状态或分数

### 反设计

```text
PreyOpportunityState = Vulnerable / Escaping / Easy / ...
OpportunityScore
OpportunityBonus
```

### 为什么拒绝

`escaping-like / struggling-like / vulnerable-like` 可以同时成立；而“好不好抓”又是 fish-relative 的 TaskAffordance，不属于 prey 自身状态。

此前 consumer-equivalence probe 显示，下游可以直接由 constituent owners 得到同样决策，不需要新增一份 authoritative packet。额外持久化只会制造 stale state、双重 authoring 与 provenance 漂移。

### 当前保留

`Prey Opportunity Interpretation` 只作为 Projection / Explain View。

### 重开条件

至少需要出现以下之一：

- 多个独立下游都需要稳定的同一聚合契约；
- 推导成本高到必须缓存；
- 存在 constituent snapshot 无法重建的独立 lifecycle / expiry / revocation；
- 出现 constituent owners 无法表达的新决策语义。

## 4. 不把 `C_mode` 直接当 Candidate Weight 或再次乘到 Candidate 上

### 反设计

```text
Spatial Weight × C_mode
→ Candidate Weight
→ Candidate Weight × ResponseCoeff
```

或把同一个 Interaction response 伪装成 Pre-Roll Gameplay Policy 再乘一次。

### 为什么拒绝

Complete Modes 先在 Interaction 内聚合成 support-aligned `captureRetention C_i,j`，Candidate Resolver 再执行一次 Native Retention Join：

```text
q_i,j = L_i,j × C_i,j
```

同一 response 再乘一次就是重复结算，不是调参选择。

### 重开条件

只有 Current Candidate / Interaction authority 明确改变 ownership，或定义新的独立 gameplay cause，才允许新增下游变换；新 cause 必须有独立 provenance，不能只是重读 Interaction 的同一输入。

## 5. 不把 Unknown 当 0

### 反设计

```text
Unknown / missing input → C_mode = 0
```

### 为什么拒绝

`ResolutionIncomplete` 与“已经解析，明确不响应”语义不同：

```text
ResolutionIncomplete → no scalar / not rollable
ResolvedNonResponsive → C_mode = 0
```

把 Unknown 写成 0 会把数据缺失、未配置或解析失败伪装成自然不咬口，也会让下游错误继续 roll。

### 重开条件

只有上游语义被明确重新定义成“Unknown 即某个具体默认值”时才能改变；不能静默降级成 0。

## 6. 不把高 Closing burden 自动写成 Infeasible

### 反设计

```text
u_close >= 1 → TaskAffordance = Infeasible → C_mode = 0
```

### 为什么拒绝

`u_close` 只表示径向 Closing burden 高，不证明完整 encounter 已不可达。没有 current gap、strike reach、reaction latency 和 interaction-region exit window 时，不能把这个单一 proxy 当完整 hard gate。

```text
u_close >= 1 → soft Closing burden
```

真正 hard infeasibility 必须来自独立的 encounter geometry / reaction-window contract；已知 terminal non-response 才可输出：

```text
ResolvedNonResponsive → C_mode = 0
```

### 重开条件

只有合法 encounter geometry / reaction-window owner 明确当前任务不可达，才允许建立 geometry-qualified hard gate。

## 7. 不让 Food Value 与 Motivation 被公式结构强制对称

### 反设计

```text
Drive = FoodValue × Motivation
```

并把 Drive 当作两者唯一充分统计量。

### 为什么拒绝

该结构强迫：

```text
FoodValue=1.0, Motivation=0.4
==
FoodValue=0.4, Motivation=1.0
```

但“非常合口、当前没那么想吃”与“很想吃、目标只是一般”没有理由恒等。

当前 Working 更倾向让 Motivation 改变 reservation / willingness threshold，Food Value 保留独立语义。

### 重开条件

只有未来 evidence / calibration 明确支持这种对称性，并且不会破坏 Target Relation 的策略故事，才可重开。

## 8. 不把 `Poor` 和 `Reject` 合并为同一个 0

### 反设计

```text
Poor = 0
Reject = 0
```

### 为什么拒绝

`Poor` 是低价值 Target Relation，仍属于连续 Feeding decision；`Reject` 是明确语义硬边界。

当前 Working 语义：

- Poor：在极好 Motivation + 极低 TaskStrain 下可有少量响应；
- Reject：无论条件多好都不能复活。

把二者合并会丢掉“鱼口好时降低挑食程度”这条策略能力。

### 重开条件

若某个 species / target scope 的证据明确显示某类 Poor 关系实际上是 hard semantic exclusion，应把该关系重新分类为 Reject，而不是修改全局 Poor 语义。

## 9. 不先定 `ΔC_mode`，再宣称它等于“明显体验差异”

### 反设计

```text
ΔC_mode >= 0.2
→ 玩家一定明显感受到
```

### 为什么拒绝

`C_mode` 后面还会经过 Spatial supply、Candidate competition、TrueRoll、Opportunity cadence 与 Catch Cycle。同样的 `ΔC` 在不同 candidate-pool regime 中，会产生不同的 target rate、purity 与 wall-clock 差异。

当前标定方向应是：

```text
Reference Fishing Story
→ 玩家体验目标
→ target time / purity / efficiency budget
→ 反推 C_mode
→ 再反推 TaskCost / Motivation Threshold / projection
```

### 重开条件

只有在固定且明确的 Reference Scenario 内，可以把某个 `ΔC` 当作局部 shorthand；不能升级成跨场景 universal rule。

## 10. 不为了拟合略好就增加 ResponseCurve 复杂度

### 反设计

在 clipped linear 已满足策略排序和体验预算时，仅因为 sigmoid 的单次拟合误差略低，就引入 midpoint / scale / extra clamp 等参数。

### 为什么拒绝

当前比较中 sigmoid 只带来很小拟合改善，没有购买新的 ranking、reversal 或玩家策略能力；同时会让 exact zero / exact one 与标定解释变复杂。

当前 Working 默认：

```text
DecisionMargin
→ clipped linear Response Projection
→ C_mode
```

`Decision Strength` 档位保留为 Explain / Debug projection，不取得 numeric authority。

### 重开条件

若线性 projection 在新增、可信的 Reference Stories 上出现系统性残差，而且该残差不能通过上游 Value / TaskCost / Motivation Threshold 修正，再考虑 sigmoid、piecewise 或其它曲线。

## 11. 不用离散 Decision Strength 反向主导连续计算

### 反设计

```text
Margin
→ Weak / Marginal / Positive / Strong
→ 查表得到 C_mode
```

### 为什么拒绝

这会把连续的 Motivation / TaskStrain 差异重新切成台阶，并制造人为边界跳变。

当前建议：

```text
continuous Margin / C_mode
→ Explain projection
→ Weak / Marginal / Positive / Strong
```

### 重开条件

只有产品明确需要离散状态本身拥有 lifecycle、行为切换或独立 authoring 语义时才重开；不能只为了 UI 好讲就让它取得数值 authority。

## 12. 不把 Activity 与 InterceptSpeedLimit 重复或错误合并

### 反设计

```text
InterceptSpeedLimit × Activity
→ composite capacity
```

### 为什么拒绝

`species × size cohort → InterceptSpeedLimit` 提供 Closing 的能力尺度。Fish Condition Bake 输出的 `Activity` 只影响 soft Closing cost，不改变 `InterceptSpeedLimit`，也不等于 `FeedingMotivation`。

```text
Activity = soft Closing-cost multiplier
InterceptSpeedLimit = Closing capability scale
```

`Unknown`、zero、`Disabled` 和 `NotApplicable` 仍是不同状态，不能互相补值。

### 重开条件

只有 Owner 明确改变 Fish Condition Bake 输出或 hard-feasibility owner，并给出新的承接 Contract，才允许改变这条路由；不能用新的系数或 probe 结果静默恢复 `FunctionalCapacity`。

## 13. 不把 pause 标签本身当 Cause

### 反设计

```text
if paused: bonus += ...
```

### 为什么拒绝

pause 只是观测到的状态/事件标签。它真正可能购买的 consequence 已拆开：

- 降低 Intercept / Maneuver demand；
- 延长 favorable dwell / attack window；
- 形成 attention continuity / prediction break；
- cadence motif 若未来有独立 residual evidence，再单独 admission。

### 重开条件

只有“pause 这个标签本身”在控制上述具名机制后仍产生独立、稳定、可复现 response effect，才允许新增 pause-specific valuation。

## 14. 使用规则

新增 Feeding / Interaction 机制前，先问：

1. 这个新项是否只是已有 Cause 的改名或重复结算？
2. 控制现有 owners 后，它是否仍能产生独立 ranking / reversal？
3. 它购买的玩家策略能力是否值得新增 authoring、calibration 与 runtime 成本？

如果三问答不出来，默认不新增 DOF。

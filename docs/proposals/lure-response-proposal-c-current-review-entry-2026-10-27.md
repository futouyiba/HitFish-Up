# Proposal C｜Current Review Entry（2026-10-27）

状态：Working Review Entry / Candidate。不是 Current，不是生产参数。

用途：给其他 Agent / Reviewer 作为当前 Proposal C 的统一审阅入口。本文只保留当前仍成立的主链、最新 Working seed、已闭合边界和开放项。

> 若本文与更高 Authority 冲突，以 `docs/authority-model.md` 与已合并 Current Owner 为准。本文所在分支为 `docs/lure-response-joint-evaluation`。

## 1. 当前主链

```text
ActualPresentation
→ prey interpretation / support
→ prey-conditioned current state
→ fish-side evaluation
→ latent-bearing conditional response
→ prey-mode response
→ Feeding composition
→ Interaction composition
→ temporal opportunity
→ Candidate native retention
→ TrueRoll
```

核心分层基本成立，但仍有少数语义级接口和 production/calibration 缺口，不能把现有 Working seed 当作生产参数。

## 2. Feeding Decision

```text
DecisionMargin(theta)
= CurrentFoodValue
+ StateTriggerValue [Escape-like v1]
- ClosingCost(theta)
- RiskCost [0 when Risk cue is Disabled / NotConfigured]
- WillingnessThreshold(FeedingMotivation)
```

FoodValue：

```text
CurrentFoodValue
= clamp(
    BaseDietAffinity
    + SizePreferenceAdjustment
    + DietaryShiftDelta,
    0,
    1
  )
```

Working relation anchors：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00
Reject    = typed hard semantic boundary
```

最新 Working Motivation：

```text
WillingnessThreshold(M)
= 0.40 + 0.60 * (0.5 - M)
= 0.70 - 0.60M
```

StateTrigger Working budget：

```text
ordinary ≈ 0.10
upper guardrail ≈ 0.15
```

这些都是 Working calibration seed。

## 3. Poor 与 Reject：已闭合的 Working 区分

旧 `K_mot=0.40` 会导致 Poor 在所有合法条件下都无法跨线，行为上与 Reject 塌缩。

当前 Working 改为：

```text
K_mot = 0.60
```

因此：

```text
M = 1
→ threshold = 0.10
```

普通 Trigger：

```text
Poor + M=1 + Trigger=0.10 + Costs=0
→ Margin = 0
→ C = 0
```

强 Trigger：

```text
Poor + M=1 + Trigger=0.15 + Costs=0
→ Margin = 0.05
→ weak C > 0
```

Poor 只有在：

```text
M > 0.9167
+ upper-range legal Trigger
+ almost no negative burden
```

时才可能弱响应。

Reject 仍然是 typed hard zero，任何 Motivation / Trigger 都不能复活。

这个调整不改变 `M=0.5` 时的 reference threshold，因此 reference-Motivation 的旧 burden calibration 不需要重标。

详细 closure：`lure-response-proposal-c-poor-reject-separation.md`。

## 4. Closing：最新裁定

第一版只处理水平 latent bearing：

```text
theta ~ Uniform(0, 2pi)
```

```text
q
= horizontal lure speed relative to water
  / InterceptSpeedLimit

u_close(theta)
= max(0, q * cos(theta))
```

`u_close` 只表达径向分离负担，不是完整 interception feasibility。

当前：

```text
ClosingCost(theta)
= K_close
  * u_close(theta)^2
  * ActivityCostMultiplier(Activity)
```

旧规则：

```text
u_close >= 1
→ C_conditional = 0
```

已撤回。

原因是当前没有合法的：

```text
current fish-lure gap
strike reach
reaction latency
time-to-exit interaction region
```

所以 `u_close>1` 只能表示径向分离压力超过结构速度尺度，不能单独推出 interaction 已不可能。

真正 hard interception gate 只有未来拿到 encounter geometry / reaction-window contract 后才允许恢复。

## 5. Activity 与 InterceptSpeedLimit

```text
Species / size cohort
→ InterceptSpeedLimit
→ Closing capability scale

Activity
→ ActivePursuitCostMultiplier
→ soft Closing cost
```

Activity 不降低 `InterceptSpeedLimit`。

第一版 locomotor profiles：

```text
HighClosing
GeneralClosing
LowClosing
```

Working q anchors：

```text
HighClosing    q_ref = 0.45
GeneralClosing q_ref = 0.65
LowClosing     q_ref = 0.90
```

由于 Closing hard-zero 已撤回，Fast / Burst 需要按纯 soft Closing 重新跑完整 response basket；旧 hard-infeasible share 只保留为诊断统计。

## 6. Prediction：Deferred Research

第一版不把 `PredictionChallenge` 或 `PredictionCost` 放进 active DecisionMargin。旧 `TurnStrength + max_recent` 只保留为历史 probe / 研究证据，不是当前实现项。

只有在固定 FoodValue、AttackTrigger、Closing、Risk、Motivation 和 Opportunity `L` 后，只改变运动可预测性，仍得到稳定、可复现、玩家能理解且足以改变打法选择的独立排序时，才重新打开 Prediction。

## 7. Wariness / Suspicion

当前生产输入缺失时：

```text
Risk cue = Disabled / NotConfigured
RiskCost = 0
```

正式保留的后续输入方向只有 `TackleConspicuousness`。`EntryDisturbance` 不进入第一版正式输入方向；不能用 prey support、speed、turn count 或 SKU 名称代替风险 cue。

当 `TackleConspicuousness` 取得合法生产输入后，才走：

```text
TackleConspicuousness → SuspicionLoad
Wariness × SuspicionLoad → RiskCost
```

禁止：

```text
1 - prey_support → SuspicionLoad
high speed → SuspicionLoad
frequent turns → SuspicionLoad
```

## 8. Margin → Response

Working projection：

```text
C(Margin)
= clamp(Margin / 0.30, 0, 1)
```

必须：

```text
theta
→ local costs
→ Margin(theta)
→ C(theta)
→ integrate over theta
```

不能先平均 Margin 再投影。

## 9. prey support × response

每个 prey interpretation：

```text
C_prey
= prey_support
  * E_theta[C_conditional(theta)]
```

多个 sibling prey interpretations 当前倾向替代关系：

```text
C_feed
= max(C_baitfish, C_crayfish, ...)
```

只适用于同一 Feeding route 下声明为 sibling alternatives 的路径。

## 10. Temporal Opportunity

`L` 的正式 owner 是 Opportunity。Spatial 只提供位置、区域、几何、垂直层和有效空间窗口等事实。

```text
Spatial facts
→ Opportunity identity / duration / dedupe / reevaluation / reducer
→ native opportunity support L

q = L × C
```

空间覆盖、停留、穿越有效区域和垂直可交互窗口由 Opportunity 表达，不进入瞬时 `DecisionMargin`。Response 不创建 `ExposureRate`、搜索信息 bonus 或第二个时间乘数。

## 11. 当前真正仍开的 P0

本轮 Issue #152 已完成 Owner 裁定。剩余工作转入 Opportunity / Fish Condition / Bake 的实现与生产契约，不再重开 AttackTrigger、Risk 核对、Prediction 探索或策略 probe。

### P0｜Opportunity `L` production contract

需要在实现前明确：

- Spatial facts 到 Opportunity identity 的映射；
- duration、coverage、vertical eligibility、dedupe、reevaluation 和 reducer；
- tick-rate / replay / partition invariance；
- `q = L × C` 只乘一次。

这些是实现接口约束，不是 Response bonus 设计。

## 12. 当前 P1

### P1-A｜Horizontal2D 对 vertical-dominant presentation 的适用边界

当前 Closing 只读 horizontal speed。对：

```text
vertical jigging
rapid lift
rapid fall
vertical dart
```

可能低估逃离负担。

第一版至少需要明确 Horizontal2D 的 applicability；vertical-dominant presentation 不能静默宣称已被统一解决。

### P1-B｜Opportunity 与 Closing 的联合闭环

Closing 只表达当前运动如何改变已有 opportunity 的局部保留；Opportunity 负责 `L` 的空间、时间、覆盖和 identity 语义。实现前需要联合验证两者的接口，但不再把 Prediction 作为当前 P1。

### P1-C｜K_mot=0.60 的低 Motivation regression

Poor/Reject 已恢复区分，但必须检查：

```text
Good at M≈0.2–0.4
Preferred at very low M
```

是否被新的 Motivation swing 过度压低。

若 regression 不通过，应重新标定 `K_mot`，而不是回头修改 Poor / Reject 的 typed semantics。

## 13. 当前仍成立的结构边界

以下不应被 Reviewer 无反例地重新打开：

3. `Activity` 只影响 soft Closing cost；
4. `Reject` 与 `Poor` typed semantics 分离；
5. `Poor` 在极端有利条件下允许弱响应，`Reject` 永不复活；
6. `CurrentFoodValue` 完整连续域 `[0,1]`；
7. 第一版 `AttackTrigger` 只准入 `Escape-like`；`Injured / Struggling`、imbalance-like vulnerability 和 pause 保持未准入；
8. 第一版不含 Prediction；
9. 第一版 RelativeBearingPrior 使用显式 `Isotropic2D` modeling convention；
10. Closing 只解释径向分离负担，不冒充完整 interception simulation；
11. `u_close >= 1 → hard-zero` 已撤回；
12. Risk cue 未启用时 `RiskCost=0`；正式后续输入方向只有 `TackleConspicuousness`；
13. `L` 的 owner 是 Opportunity，Spatial 只提供事实；
14. 不新增探索 / 信息覆盖 bonus、CapacityModifier 或 EntryDisturbance；
15. temporal duration 不进入 `DecisionMargin`。

## 14. Reviewer 建议攻击点

优先攻击：

1. Opportunity `L` 的 identity、duration、coverage、dedupe、reevaluation 与 reducer contract；
2. `K_mot=0.60` 是否让低 Motivation 下 Good / Preferred 行为失真；
3. 纯 soft Closing 在 Fast / Burst 下是否仍能形成正确策略排序；
4. Horizontal2D 对哪些 presentation 必须标 NotApplicable / Incomplete；
5. prey support × response × temporal opportunity × Candidate 是否系统性过度衰减；
6. 哪些 OPEN 真正阻塞 production，哪些只是 calibration。

Reviewer 必须区分事实、Candidate、Working seed、建议；不能把缺少 owner 的内容补造成生产规则。

## 15. 深挖入口

- `lure-feeding-response-proposal-c.md`：实际呈现 → prey interpretation / state；
- `lure-response-proposal-c-current-food-value-bounds.md`：FoodValue 域；
- `lure-response-proposal-c-feeding-motivation-threshold.md`：Motivation topology；
- `lure-response-proposal-c-poor-reject-separation.md`：Poor / Reject 最新 Working closure；
- `lure-response-proposal-c-feature-ownership-matrix.md`：feature ownership；
- `lure-response-proposal-c-latent-bearing-prior.md`：bearing prior；
- `lure-response-proposal-c-latent-bearing-dimensionality-decision.md`：Horizontal2D decision；
- `lure-response-proposal-c-closing-geometry-interpretation.md`：最新 Closing 几何与 hard-zero 撤回；
- `lure-response-proposal-c-intercept-speed-production-contract.md`：InterceptSpeed production topology；
- `lure-response-proposal-c-reference-intercept-speed-working-anchors.md`：Working anchors，注意旧 hard-infeasible 解释已被最新 Closing decision supersede；
- `lure-response-proposal-c-combined-burden-stress-test.md`：联合 burden；
- `lure-response-proposal-c-temporal-exposure-opportunity.md`：Temporal Opportunity seam。

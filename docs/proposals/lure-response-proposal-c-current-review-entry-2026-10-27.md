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
+ StateTriggerValue
- ClosingCost(theta)
- PredictionCost
- RiskCost
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

## 6. Prediction

```text
sudden direction change
→ PredictionChallenge
→ PredictionCost
```

Working：

```text
TurnStrength(delta_psi)
= (1 - cos(delta_psi)) / 2

PredictionChallenge(t)
= max_recent[
    TurnStrength
    * exp(-age / tau_recover)
  ]

PredictionCost
= K_pred * PredictionChallenge
```

Prediction 不 hard-zero。Pause 只通过时间推进让 challenge 衰减，不加额外 PauseBonus。

## 7. Wariness / Suspicion

```text
RiskCost
= K_wary * Wariness * SuspicionLoad
```

SuspicionLoad 只能来自具名、独立拥有的风险 cue。

禁止：

```text
1 - prey_support → SuspicionLoad
high speed → SuspicionLoad
frequent turns → SuspicionLoad
```

除非未来有独立证据与 owner。

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

瞬时 `C(t)` 不是每秒 bite probability，也不是最终 candidate probability。

```text
instantaneous response C(t)
× temporal / local opportunity exposure
→ accumulated opportunity
→ Candidate retention
```

时间不进入 DecisionMargin，不加 DwellBonus / PauseBonus。

姿态颗粒方案沿用既有设计，不在本文重复。

Temporal Opportunity / exposure → Candidate 的正式 Current Owner 仍未落仓。

## 11. 当前真正仍开的 P0

### P0｜Unknown sibling 的 max aggregation

当前同时有：

```text
Unknown != 0
```

和：

```text
C_feed = max(sibling prey responses)
```

但尚未定义：

```text
resolved sibling = 0.45
unresolved sibling = Unknown
```

时能否输出最终 `0.45`。

推荐方向是 partial-resolution bounds：

```text
known_lower_bound
= max(resolved siblings)

possible_upper_bound
= max(
    known_lower_bound,
    unresolved siblings' allowed upper bounds
  )
```

只有 unresolved path 已不可能改变 winner，或上下界收敛时，才输出最终 scalar；否则保持 `ResolutionIncomplete`。

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

### P1-B｜Prediction 的 max_recent 是否低估持续 erratic movement

需要 regression：

```text
single turn
repeated moderate turns
alternating turns
turn → long pause
```

如果持续乱跳与单次转向长期同值，再考虑有限记忆 accumulation；当前不先加公式。

### P1-C｜Opportunity 与 Closing 的联合闭环

Closing 现在只表达“当前运动多强地把已有 opportunity 带走”。

因此：

```text
Opportunity geometry
↔ Closing
```

需要联合验证，而不是把 Opportunity 当成纯后处理。

### P1-D｜K_mot=0.60 的低 Motivation regression

Poor/Reject 已恢复区分，但必须检查：

```text
Good at M≈0.2–0.4
Preferred at very low M
```

是否被新的 Motivation swing 过度压低。

若 regression 不通过，应重新标定 `K_mot`，而不是回头修改 Poor / Reject 的 typed semantics。

## 13. 当前仍成立的结构边界

以下不应被 Reviewer 无反例地重新打开：

1. FoodValue 与 Motivation 分离；
2. FunctionalCapacity 删除；
3. Activity 只影响 soft Closing cost；
4. Reject 与 Poor typed semantics 分离；
5. Poor 在极端有利条件下允许弱响应，Reject 永不复活；
6. CurrentFoodValue 完整连续域 `[0,1]`；
7. sudden turn 可同时产生 Trigger 正效应与 Prediction 负效应；
8. 第一版 RelativeBearingPrior 使用显式 `Isotropic2D` modeling convention；
9. Closing 只解释径向分离负担，不冒充完整 interception simulation；
10. `u_close >= 1 → hard-zero` 已撤回；
11. high speed / low prey support / pause 不产生匿名 Suspicion 或 bonus；
12. combined soft burden 不加 runtime total cap；
13. temporal duration 不进入 DecisionMargin。

## 14. Reviewer 建议攻击点

优先攻击：

1. Unknown sibling 的 partial-resolution aggregation；
2. `K_mot=0.60` 是否让低 Motivation 下 Good / Preferred 行为失真；
3. 纯 soft Closing 在 Fast / Burst 下是否仍能形成正确策略排序；
4. Horizontal2D 对哪些 presentation 必须标 NotApplicable / Incomplete；
5. `max_recent` Prediction 是否低估持续 erratic pattern；
6. prey support × response × temporal opportunity × Candidate 是否系统性过度衰减；
7. 哪些 OPEN 真正阻塞 production，哪些只是 calibration。

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

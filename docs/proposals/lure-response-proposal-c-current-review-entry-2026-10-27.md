# Proposal C｜Current Review Entry（2026-10-27）

状态：Working Review Entry / Candidate。不是 Current，不是生产参数。

用途：给其他 Agent / Reviewer 作为当前 Proposal C 的统一审阅入口。本文承接 2026-10-26 版，并吸收 2026-10-27 对 Closing hard-zero 的修正。历史推演、已关闭问题和过时状态不在这里重复。

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

当前判断：核心分层基本成立，但仍有少数语义级问题没有完全闭合，不能把现有 Working seed 当作 production calibration。

## 2. Feeding Decision

核心式：

```text
DecisionMargin(theta)
= CurrentFoodValue
+ StateTriggerValue
- ClosingCost(theta)
- PredictionCost
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

当前 Working：

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

Motivation：

```text
WillingnessThreshold(M)
= 0.40 + 0.40 * (0.5 - M)
```

StateTrigger Working budget：

```text
ordinary ≈ 0.10
upper guardrail ≈ 0.15
```

这些均是 Working seed。

## 3. Closing：当前最新裁定

第一版只处理水平 latent bearing：

```text
theta ~ Uniform(0, 2pi)
```

使用：

```text
q
= horizontal lure speed relative to water
  / InterceptSpeedLimit

u_close(theta)
= max(0, q * cos(theta))
```

`u_close` 只表达径向分离负担，不是完整 interception feasibility。

当前最新 Working：

```text
ClosingCost(theta)
= K_close
  * u_close(theta)^2
  * ActivityCostMultiplier(Activity)
```

### 关键修正

旧规则：

```text
u_close >= 1
→ C_conditional = 0
```

已撤回。

原因：缺少：

```text
current fish-lure gap
strike reach
reaction latency
time-to-exit interaction region
```

所以“目标径向远离速度超过鱼的短时截获速度尺度”只能说明鱼无法持续阻止距离拉大，不能推出当前 interaction 已经不可能发生。

真正 hard interception gate 只有未来拿到合法 encounter geometry / reaction-window contract 后才允许恢复。

此前任何：

```text
q > 1
→ hard-infeasible bearing share
```

的统计不再代表第一版 hard-zero 比例，只可作为 `radial_separation_ratio > 1` 的诊断比例。

## 4. Activity 与 InterceptSpeedLimit

当前 Owner 边界仍成立：

```text
Species / size cohort
→ InterceptSpeedLimit
→ Closing capability scale

Activity
→ ActivePursuitCostMultiplier
→ soft Closing cost
```

Activity 不降低 `InterceptSpeedLimit`。

`InterceptSpeedLimit` 当前是结构性短时截获能力尺度，不再单独充当 encounter hard gate。

第一版 locomotor profiles：

```text
HighClosing
GeneralClosing
LowClosing
```

Working q anchors 仍保留为 calibration seed：

```text
HighClosing    q_ref = 0.45
GeneralClosing q_ref = 0.65
LowClosing     q_ref = 0.90
```

但 Fast / Burst 的旧 hard-infeasible 解释已失效，需要按纯 soft Closing 重新跑完整 response basket。

## 5. Prediction

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

## 6. Wariness / Suspicion

```text
RiskCost
= K_wary * Wariness * SuspicionLoad
```

SuspicionLoad 只能来自具名、独立拥有的风险 cue。禁止：

```text
1 - prey_support → SuspicionLoad
high speed → SuspicionLoad
frequent turns → SuspicionLoad
```

除非未来有独立证据与 owner。

## 7. Margin → Response

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

## 8. prey support × response

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

## 9. Temporal Opportunity

瞬时 `C(t)` 不是每秒 bite probability，也不是最终 candidate probability。

当前 seam：

```text
instantaneous response C(t)
× temporal / local opportunity exposure
→ accumulated opportunity
→ Candidate retention
```

时间不进入 DecisionMargin，不加 DwellBonus / PauseBonus。

姿态颗粒方案沿用既有设计，不在本文重复。

Temporal Opportunity / exposure → Candidate 的正式 Current Owner 仍未落仓。

## 10. 当前真正仍开的 P0

### P0-A｜Poor 与 Reject 的行为区分

当前 Working seed 下：

```text
Poor = 0
WillingnessThreshold(M=1) = 0.20
StateTrigger upper guardrail ≈ 0.15
```

即使最高 Motivation、最大 Trigger、无任何负 burden：

```text
Margin = 0 + 0.15 - 0.20 = -0.05
```

所以 Poor 在当前 Working 数值下永远 `C=0`。

这会让 Poor 与 Reject 在行为上塌成同一类，只剩 typed semantics 不同。

需要联合调整：

```text
Poor anchor
Motivation threshold range
StateTrigger budget
```

目标不是让 Poor 常规可用，而是至少保留“极端有利状态下可跨线”的连续语义。

### P0-B｜Unknown sibling 的 max aggregation

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

第一版需要正式定义 partial-resolution semantics。推荐方向是 lower/upper bound：

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

## 11. 当前 P1

### P1-A｜Horizontal2D 对 vertical-dominant presentation 的适用边界

当前 Closing 只读 horizontal speed。对：

```text
vertical jigging
rapid lift
rapid fall
vertical dart
```

可能低估逃离负担。

第一版至少需要明确：Horizontal2D 是 horizontal-dominant presentation 的 approximation；vertical-dominant presentation 不能静默宣称已被统一解决。

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

## 12. 当前仍成立的结构边界

以下不应被 Reviewer 无反例地重新打开：

1. FoodValue 与 Motivation 分离；
2. FunctionalCapacity 删除；
3. Activity 只影响 soft Closing cost；
4. Reject 与 Poor typed semantics 分离；
5. CurrentFoodValue 完整连续域 `[0,1]`；
6. sudden turn 可同时产生 Trigger 正效应与 Prediction 负效应；
7. 第一版 RelativeBearingPrior 使用显式 `Isotropic2D` modeling convention；
8. Closing 只解释径向分离负担，不冒充完整 interception simulation；
9. `u_close >= 1 → hard-zero` 已撤回；
10. high speed / low prey support / pause 不产生匿名 Suspicion 或 bonus；
11. combined soft burden 不加 runtime total cap；
12. temporal duration 不进入 DecisionMargin。

## 13. Reviewer 建议攻击点

优先攻击：

1. Poor 是否应该保留连续可响应语义，怎样最小改动恢复；
2. Unknown sibling 的 partial-resolution aggregation；
3. 纯 soft Closing 在 Fast / Burst 下是否仍能形成正确策略排序；
4. Horizontal2D 对哪些 presentation 必须标 NotApplicable / Incomplete；
5. `max_recent` Prediction 是否低估持续 erratic pattern；
6. prey support × response × temporal opportunity × Candidate 是否系统性过度衰减；
7. 哪些 OPEN 真正阻塞 production，哪些只是 calibration。

Reviewer 必须区分事实、Candidate、Working seed、建议；不能把缺少 owner 的内容补造成生产规则。

## 14. 深挖入口

- `lure-feeding-response-proposal-c.md`：实际呈现 → prey interpretation / state；
- `lure-response-proposal-c-current-food-value-bounds.md`：FoodValue 域；
- `lure-response-proposal-c-feeding-motivation-threshold.md`：Motivation；
- `lure-response-proposal-c-feature-ownership-matrix.md`：feature ownership；
- `lure-response-proposal-c-latent-bearing-prior.md`：bearing prior；
- `lure-response-proposal-c-latent-bearing-dimensionality-decision.md`：Horizontal2D decision；
- `lure-response-proposal-c-closing-geometry-interpretation.md`：最新 Closing 几何与 hard-zero 撤回；
- `lure-response-proposal-c-intercept-speed-production-contract.md`：InterceptSpeed production topology；
- `lure-response-proposal-c-reference-intercept-speed-working-anchors.md`：Working anchors，注意其中旧 hard-infeasible 解释已被最新 Closing decision supersede；
- `lure-response-proposal-c-combined-burden-stress-test.md`：联合 burden；
- `lure-response-proposal-c-temporal-exposure-opportunity.md`：Temporal Opportunity seam。

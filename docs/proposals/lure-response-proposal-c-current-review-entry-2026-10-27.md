# Proposal C｜Current Review Entry（2026-10-27）

状态：Working Review Entry / Candidate。不是 Current，不是生产参数。

用途：给其他 Agent / Reviewer 作为当前 Proposal C 的统一审阅入口。本文只保留当前仍成立的主链、最新 Working seed、已闭合边界和开放项。

> 若本文与更高 Authority 冲突，以 `docs/authority-model.md` 与已合并 Current Owner 为准。本文是 `futou-/exciting-payne-95a562` 分支的审阅入口；Proposal C 的 Working 文档保留在 `docs/lure-response-joint-evaluation` 分支。
>
> 2026-10-30 同步：第一版 `DecisionMargin` 按 Proposal C 当前 Working Closure 使用五项式；Prediction 为 `Deferred Research`，不进入第一版裕量。本页此前含 `PredictionCost` 的六项式是未同步旧口径。依据：PR [#130](https://github.com/futouyiba/HitFish-Up/pull/130) 提交 `5caf1f119ab6e5a5c595a4ba913e7962aa338ec3` 的 [`lure-response-proposal-c-feeding-response-working-closure.md`](https://github.com/futouyiba/HitFish-Up/blob/5caf1f119ab6e5a5c595a4ba913e7962aa338ec3/docs/proposals/lure-response-proposal-c-feeding-response-working-closure.md) §4–§5，以及 Proposal C open-decisions 的「已知未同步」条目。

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
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

`Prediction` 第一版为 `Deferred Research`，不进入上式；重开条件见 §6。

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

### 输入状态传播

`DecisionMargin` 只有在所有必需输入都已解析时才产生数值。输入状态按以下规则传播：

- `Reject` 直接产生 typed hard zero，不进入连续裕量计算；
- `NotConfigured` 或缺少必需 owner 的输入，产生 `ResolutionIncomplete`，不得静默填 0；
- `Unknown` 只有在该项已证明不会改变当前输出或上下界已经收敛时，才允许继续归约；否则保持 `ResolutionIncomplete`；
- `NoMatch` 表示适用规则已完成检查但没有命中，按该规则定义的数值结果处理，不能与 `Unknown` 或 `NotConfigured` 混用；
- 已解析的数值 0 才能进入公式并表示该项的真实零贡献。

因此，`StateTriggerValue`、`RiskCost` 和 `WillingnessThreshold` 的缺失状态必须先解决，才能输出 `DecisionMargin`。`CurrentFoodValue=0` 仍是合法的 Poor 输入；它不等于 `Reject`。

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

详细 closure：Proposal C Working 文档中的 `lure-response-proposal-c-poor-reject-separation.md`。该文件不在本分支复制；本页只保留其已纳入本入口的 Working 结论。

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

## 6. Prediction（Deferred Research）

第一版不进入 `DecisionMargin`，本节只保留研究材料。

重开条件：必须证明 Prediction 提供独立的策略价值。固定 FoodValue、AttackTrigger、Closing、Risk、Motivation 和 Opportunity `L`，只改变运动可预测性，仍能得到稳定、可复现、玩家能理解且足以改变打法选择的排序；只靠统计拟合改善不构成重开依据。

以下为待验证的研究形态，不是当前裕量项：

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

若重开，Prediction 不 hard-zero。Pause 只通过时间推进让 challenge 衰减，不加额外 PauseBonus。

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
= clamp((Margin - M0) / (M1 - M0), 0, 1)
```

本页不冻结 `M0 / M1` 的生产值。入口中的 Poor 示例只表达响应窗口，不提供数值投影的验收结果。Response projection probe 当前比较三类曲线的相对形状，使用的 `-0.10 / 0.23` 是独立 fixture，不是本页的生产 anchor。

`M0` 与 `M1` 是 calibration anchors，不是物理常数。只有已解析的 `DecisionMargin` 才能进入 projection：

```text
ResolutionIncomplete / Unknown
→ 不调用 projection，不输出 C

ResolvedNonResponsive
→ 输出 C = 0

ResolvedResponsive
→ 输出 0 < C <= 1
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

`prey_support` 的状态传播与 `DecisionMargin` 相同：已解析数值才可相乘；`Unknown`、`NotConfigured` 或尚未收敛的 sibling 支持度不能被强制转成 0。

多个 sibling prey interpretations 当前倾向替代关系：

```text
C_feed
= max(C_baitfish, C_crayfish, ...)
```

归约规则：

```text
known_lower_bound
= max(known resolved sibling responses)

possible_upper_bound
= max(
    known_lower_bound,
    unresolved siblings' allowed upper bounds
  )
```

只有当未解析路径不可能改变 winner，或上下界已经收敛时，才输出最终 scalar；否则输出 `ResolutionIncomplete`。`NoMatch` 只有在该 sibling 的适用规则已完整检查后，才可作为已解析的数值结果参与归约。

这只适用于同一 Feeding route 下声明为 sibling alternatives 的路径。

## 10. Temporal Opportunity

瞬时 `C(t)` 不是每秒 bite probability，也不是最终 candidate probability。

```text
instantaneous response C(t)
× temporal / local opportunity exposure
→ accumulated opportunity
→ Candidate retention
```

时间不进入 DecisionMargin，不加 DwellBonus / PauseBonus。

时间机会接口的最小状态契约：

- `C(t)` 是 `[0,1]` 的已解析瞬时响应；
- `exposure` 必须由 opportunity owner 提供，并明确时间窗口、局部机会范围和单位；
- `exposure` 未配置或无法解析时，输出 `ResolutionIncomplete`，不得当作零曝光；
- 已解析的零曝光才表示该窗口没有机会；
- 归约器必须说明按事件窗口还是采样时段累积，并保持同一窗口内的单位和归约方式一致；
- 归约结果进入 Candidate retention，不能在 Candidate 后段再次乘 Response。

姿态颗粒方案沿用既有设计，不在本文重复。Temporal Opportunity / exposure → Candidate 的正式 Current Owner 仍未落仓。

## 11. 当前 P0：Unknown sibling 的归约状态

当前同时有：

```text
Unknown != 0
```

和：

```text
C_feed = max(sibling prey responses)
```

本页将 partial-resolution bounds 记为 Working seam，不把它写成已冻结的 production aggregation contract：

```text
known_lower_bound
= max(known resolved sibling responses)

possible_upper_bound
= max(
    known_lower_bound,
    unresolved siblings' allowed upper bounds
  )
```

只有未解析路径不可能改变 winner，或上下界已经收敛时，才输出最终 scalar；否则保持 `ResolutionIncomplete`。该规则仍需要 Current Owner 收口。

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

### P1-B｜Prediction 的 max_recent 是否低估持续 erratic movement（Deferred Research）

若 Prediction 重开，需要 regression：

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
7. Prediction 保持 `Deferred Research`；若重开，sudden turn 可同时产生 Trigger 正效应与 Prediction 负效应；
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
5. Prediction 重开时，`max_recent` 是否低估持续 erratic pattern；
6. prey support × response × temporal opportunity × Candidate 是否系统性过度衰减；
7. 哪些 OPEN 真正阻塞 production，哪些只是 calibration。

Reviewer 必须区分事实、Candidate、Working seed、建议；不能把缺少 owner 的内容补造成生产规则。替代方案还必须指出它替换哪个归属方、消除了什么重复计权，以及对现有回归证据的影响。可复核的回归入口包括 [`proposal_c_prediction_challenge_probe.py`](../../prototypes/lure-response/proposal_c_prediction_challenge_probe.py)、[`proposal_c_response_projection_probe.py`](../../prototypes/lure-response/proposal_c_response_projection_probe.py)、[`proposal_c_closing_cost_shape_probe.py`](../../prototypes/lure-response/proposal_c_closing_cost_shape_probe.py) 和 [`proposal_c_support_retention_projection_probe.py`](../../prototypes/lure-response/proposal_c_support_retention_projection_probe.py)。

## 15. 可复核入口

本页只保留当前分支中可直接运行的 probe 入口。Proposal C 的 Working 文档留在其独立研究分支，不在本提交中复制。

- [`proposal_c_prediction_challenge_probe.py`](../../prototypes/lure-response/proposal_c_prediction_challenge_probe.py)：Prediction regression（Deferred Research）；
- [`proposal_c_response_projection_probe.py`](../../prototypes/lure-response/proposal_c_response_projection_probe.py)：Response projection；
- [`proposal_c_closing_cost_shape_probe.py`](../../prototypes/lure-response/proposal_c_closing_cost_shape_probe.py)：soft Closing shape；
- [`proposal_c_support_retention_projection_probe.py`](../../prototypes/lure-response/proposal_c_support_retention_projection_probe.py)：support × response retention。

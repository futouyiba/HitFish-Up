# Proposal C｜Current Review Entry（2026-10-26）

状态：Working Review Entry / Candidate。不是 Current，不是生产参数。

用途：给其他 Agent / Reviewer 作为当前 Proposal C 的统一审阅入口。本文只保留当前仍成立的主链、已闭合边界、Working calibration seed 与开放项；历史推演、已关闭问题和过时状态不在这里重复。

> 若本文与更高 Authority 冲突，以 `docs/authority-model.md` 与已合并 Current Owner 为准。本文所在分支为 `docs/lure-response-joint-evaluation`，当前分支基线见 Git history。

## 1. 当前结论

Proposal C 当前主链：

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

瞬时 Feeding Response 的核心公式已经基本闭合；主要剩余问题集中在 production source、参数标定、Temporal Opportunity 的正式 owner，以及全量鱼种覆盖。

---

## 2. 呈现与猎物解释

`ActualPresentation` 提供真实呈现事实，包括形态、轨迹、速度、停顿、转向、近底/水面状态等。不得用玩家输入指令直接冒充实际呈现。

同一 presentation 可同时支持多个 prey interpretation：

```text
baitfish support
crayfish support
frog support
...
```

这些 support：

- 不要求和为 1；
- 不等于 bite probability；
- 不等于 FoodValue；
- 不等于 Suspicion；
- sibling prey interpretations 是替代解释，不重复当作独立机会叠加。

prey-conditioned state 可包含 movement、low displacement、rise/fall、surface/near-bottom、move→pause、sudden redirection、burst、escape/distress 等。

Unknown / NotConfigured / NoMatch 必须区分。缺失数据不能静默按 0 处理。

---

## 3. FoodValue

当前拓扑：

```text
BaseDietAffinity(prey family)
+ SizePreferenceAdjustment(prey size)
+ DietaryShiftDelta(prey family)
→ RawFoodValue
→ clamp(0,1)
→ CurrentFoodValue
```

当前 Working relation anchors：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00
Reject    = typed hard semantic boundary
```

关键边界：

- `[0,1]` 是完整 `CurrentFoodValue` 的合法连续域；
- `Poor=0` 仍是合法连续 Feeding target；
- `Reject` 在连续轴外，不能被 Motivation / Trigger / DietaryShift 复活；
- `SizePreferenceAdjustment <= 0`；
- 所有合法 contribution 先求和，再 clamp 一次；
- 不做中间 clamp；
- DietaryShift 是相对 prey-family 偏移，不是 common appetite boost。

---

## 4. FeedingMotivation

FeedingMotivation 不再乘 FoodValue，而是改变行动门槛：

```text
WillingnessThreshold(M)
= T_ref + K_mot * (M_ref - M)

M_ref = 0.5
T_ref = MarginalAnchor = 0.40
K_mot = 0.40   # Working seed
```

所以在 reference Motivation 下：

```text
Preferred margin = +0.60
Good      margin = +0.30
Marginal  margin = 0
Poor      margin = -0.40
```

Motivation 是鱼的全局进食意愿，不是 prey-specific value，不是 bite probability。

---

## 5. StateTrigger

当前 prey/current-state 可提供额外正向攻击证据：

```text
sudden redirection
burst / escape-like state
→ StateTriggerValue
```

Working budget：

```text
ordinary trigger ≈ 0.10
upper guardrail ≈ 0.15
```

StateTrigger 不改 prey identity，不改 Motivation，也不能复活 Reject。

同一个 sudden turn 可合法双路：

```text
sudden turn
├→ prey-state evidence → StateTriggerValue (+)
└→ prediction disruption → PredictionCost (-)
```

因为两条路径回答不同问题。

---

## 6. Closing

当前第一版只处理**水平 latent bearing**。

```text
θ ~ Uniform(0, 2π)
```

使用：

```text
q
= horizontal lure speed relative to water
  / InterceptSpeedLimit

u_close(θ)
= max(0, q * cosθ)
```

`u_close` 的语义必须收窄为：

> 拟饵相对潜在鱼的径向远离速度，占鱼短时截获能力的比例。

它不是完整二维 interception simulation。

因此：

- `cosθ > 0`：目标正在远离，有 Closing burden；
- `cosθ = 0`：纯横切，当前不增加径向分离；
- `cosθ < 0`：目标正向潜在鱼接近，不增加追赶负担。

不能因为横切仍需要鱼移动，就补一个匿名 tangential penalty。初始 fish-lure distance、交会点、reaction latency 当前都没有合法数据 owner。

当前 Working：

```text
ClosingCost(θ)
= K_close
  * u_close(θ)^2
  * ActivityCostMultiplier(Activity)

`u_close >= 1` 表示高 Closing burden；没有独立 encounter-geometry / reaction-window contract 时，不直接输出 `C_conditional(θ)=0`。
```

hard-zero 只表示：

> 当前 bearing 下，拟饵的径向远离速度已达到或超过鱼的短时截获能力。

不是声明严格二维物理意义上整个追击绝对不可能。

---

## 7. Activity 与 InterceptSpeedLimit

Owner 已裁：`FunctionalCapacity` 删除；Activity 与结构速度能力分离。

```text
Species / size cohort
→ InterceptSpeedLimit
→ Closing burden / capability scale

Activity
→ ActivePursuitCostMultiplier
→ soft Closing cost
```

Activity 不降低 `InterceptSpeedLimit`，避免同一低活性同时：

1. 降低硬能力边界；
2. 抬高 soft Closing cost。

Activity 文档修改由其它执行线处理；本 Review Entry 只登记接口边界，不重写 Activity 方案。

---

## 8. InterceptSpeedLimit production topology

推荐：

```text
FishSpeciesConfig
├─ ReferenceLength
├─ ReferenceInterceptSpeed
└─ SizeScalingRule

Species × SizeCohort
├─ RepresentativeLength
└─ BakedInterceptSpeedLimit
```

Working scaling topology：

```text
InterceptSpeedLimit(L)
= ReferenceInterceptSpeed
  * (L / ReferenceLength)^alpha
```

`alpha` 不是 production-closed。

RepresentativeLength 优先级：

```text
1. response 前已合法存在的 individual length
2. cohort generation distribution median
3. generation contract representative length
4. authored cohort midpoint/reference
5. species-wide fallback
```

不得为了 Response 临时随机“假鱼长度”。如果 cohort 内 variation 足以改变 feasibility / ranking，优先 split cohort，而不是 runtime 对长度分布再积分。

---

## 9. Locomotor archetype 与 Working anchors

第一版只保留三个生产 authoring profile：

```text
HighClosing
GeneralClosing
LowClosing
```

不正式设：

```text
BurstAmbushPredator
ManeuverOriented
SustainedCruiser
```

因为当前 runtime 只有单一 `InterceptSpeedLimit`，没有 burst duration、pursuit horizon、turn capacity 等独立维度。

以 Normal Steady reference lure speed 的中位数记为：

```text
V_ref
```

当前 Working target q：

```text
HighClosing    q_ref = 0.45
GeneralClosing q_ref = 0.65
LowClosing     q_ref = 0.90
```

等价于：

```text
HighClosing    ReferenceInterceptSpeed ≈ 2.22 * V_ref
GeneralClosing ReferenceInterceptSpeed ≈ 1.54 * V_ref
LowClosing     ReferenceInterceptSpeed ≈ 1.11 * V_ref
```

这些是 calibration seed，不是现实鱼类“真实最高游速”。

在 Isotropic2D、reference Activity 下，如果目标：

```text
GeneralClosing × Normal Steady
→ average Closing burden ≈ 0.08
```

则 Working：

```text
K_close ≈ 0.76
```

对应 Normal Steady 平均 soft Closing burden 约：

```text
High    ≈ 0.038
General ≈ 0.080
Low     ≈ 0.153
```

仍不是 production 参数。

---

## 10. Prediction

当前 generic ManeuverCost 已撤回。

```text
sudden direction change
→ PredictionChallenge
→ PredictionCost
```

Working shape：

```text
TurnStrength(Δψ)
= (1 - cosΔψ) / 2

PredictionChallenge(t)
= max_recent[
    TurnStrength
    * exp(-age / τ_recover)
  ]

PredictionCost
= K_pred * PredictionChallenge
```

Prediction 不 hard-zero。Pause 通过时间推进让 PredictionChallenge 自然衰减，不加 `PauseBonus / PredictionResetBonus`。

---

## 11. Wariness / Suspicion

Wariness 不作为第二套 Motivation/global threshold。

```text
Wariness × SuspicionLoad
→ RiskCost
```

Working：

```text
RiskCost
= K_wary * Wariness * SuspicionLoad
```

首版允许 SuspicionLoad 消费有独立 authority 的 named cue，例如：

```text
TackleConspicuousness
EntryDisturbance
...
```

禁止：

```text
SuspicionLoad = 1 - prey_support
```

也禁止仅因高速、频繁转向、低 prey support 就自动判“不自然/可疑”。

Fishing pressure 优先作为 Wariness 的上游原因，不同时默认抬高 SuspicionLoad，避免近似平方放大。

---

## 12. DecisionMargin

当前核心式：

```text
DecisionMargin(θ)
= CurrentFoodValue
+ StateTriggerValue
- ClosingCost(θ)
- PredictionCost
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

不同作用必须保持不同 owner；不能因为某 raw feature “看起来重要”就在多个 coefficient 中重复结算同一个效果。

---

## 13. Margin → Feeding Response

当前 Working projection：

```text
C(Margin)
= clamp(Margin / 0.30, 0, 1)
```

因此：

```text
Margin <= 0    → C = 0
0.05           → ~0.17
0.10           → ~0.33
0.15           → 0.50
0.20           → ~0.67
0.30+          → 1
```

`DecisionMargin = 0` 就是 response decision boundary。

不另设隐藏 onset offset。

projection 必须在 latent bearing 内做：

```text
θ
→ local feasibility / costs
→ Margin(θ)
→ C(θ)
→ integrate over θ
```

不能先平均 Margin 再 projection。

---

## 14. prey support × response

每个 prey interpretation：

```text
C_prey
= prey_support
  * Eθ[C_conditional(θ)]
```

多个 sibling prey interpretations 当前倾向替代关系：

```text
C_feed
= max(C_baitfish, C_crayfish, ...)
```

只适用于声明为同一 Feeding route 的 sibling alternatives；不能把所有 Interaction mode 都 universal max。

---

## 15. Combined burden budget

当前 soft negative terms：

```text
ClosingCost
PredictionCost
RiskCost
```

可加法进入 DecisionMargin，但必须联合标定。

Working stress baskets：

```text
Light:
Closing   0.04
Prediction 0.02
Risk      0.02
Total     0.08

Ordinary:
Closing   0.08
Prediction 0.05
Risk      0.05
Total     0.18

Heavy:
Closing   0.15
Prediction 0.10
Risk      0.10
Total     0.35
```

Working guardrail：

```text
ordinary combined soft burden ≈ 0.12 ~ 0.20
```

不要加 runtime `TotalBurdenCap`。如果 normal case 经常被打到 0，应检查各 term calibration 或重复 ownership，而不是用 cap 隐藏问题。

Activity 是 Closing 内部 multiplier，不是第四个独立 burden。

---

## 16. Temporal Opportunity

瞬时 `C` 不是：

- 每秒 bite probability；
- 最终 candidate probability；
- 累计中鱼率。

时间维度不进入 DecisionMargin，不加 DwellBonus / PauseBonus。

当前职责边界：

```text
instantaneous response C(t)
× temporal / local opportunity exposure
→ accumulated opportunity
→ Candidate retention
```

姿态颗粒的具体方案已经单独讨论并沿用既有设计，不在本文重复定义。

当前仓内仍缺一份已合并 Current Owner 明确拥有 Temporal Opportunity / exposure → candidate reducer。Proposal C 只能定义接口，不能把缺口静默吞进 Feeding Response。

---

## 17. Candidate join

Response 最终只产生 native contribution：

```text
q_i,j = L_i,j * C_i,j
→ Opportunity Reduce
→ W_i^opp
→ NativeCandidateSnapshot
→ optional Pre-Roll Gameplay Policy
→ TrueRoll
```

不得在 Candidate 后段再乘一次 Response，避免 double multiplication。

Typed status：

```text
ResolutionIncomplete
ResolvedNonResponsive  C=0
ResolvedResponsive     0<C<=1
Reject                  hard semantic zero
```

Unknown 不等于 0。

---

## 18. 当前已经闭合的结构边界

以下目前不应被 Review Agent 当作 OPEN 再从零重设计：

1. FoodValue 与 Motivation 分离；
2. FunctionalCapacity 删除；
3. Activity 只改 soft Closing cost，不改硬速度上限；
4. Reject 与 Poor 分离；
5. CurrentFoodValue 完整域为 `[0,1]`；
6. sudden turn 的 Trigger / Prediction 双路允许，但不能再加 generic Erratic bonus/penalty；
7. RelativeBearingPrior 第一版采用显式 `Isotropic2D` modeling convention；
8. Closing 只解释径向远离造成的额外追赶负担，不冒充完整 interception simulation；
9. feature ownership matrix 禁止 high speed→Suspicion、low support→Suspicion、pause→额外 bonus 等重复结算；
10. combined soft burden 不加 runtime total cap；
11. temporal duration 不进入 DecisionMargin。

Reviewer 若要推翻这些，应给出明确反例或显示其破坏了现有链条的哪个 invariant。

---

## 19. 当前仍开放的问题

### 结构 / Owner 缺口

- Temporal Opportunity / exposure → Candidate 的正式 Current Owner；
- Feeding / Defense / Investigation 的 Interaction composition；
- ExplicitDirectional bearing prior 若未来启用，由谁提供 production directional support；
- SuspicionLoad 的生产 cue owner。

### production source

- 约 200 鱼种的 BaseDietAffinity / DietArchetype coverage；
- SizePreference production curve；
- DietaryShift production budget / centering；
- InterceptSpeedLimit 真实绝对 m/s source；
- size scaling profile / exponent；
- lure family × regime 的 horizontal water-relative speed telemetry；
- Suspicion cue 标准化输入。

### calibration

- `K_close` production value；
- `K_pred`、`τ_recover`；
- `K_wary`；
- final Good / Marginal anchors；
- response projection `M1` production calibration；
- StateTrigger final budget；
- prey support × response 的整链分布；
- saturation / zero-rate guardrails。

---

## 20. Reviewer 建议任务

如果让外部 Agent 审这套方案，建议不要重新设计整个 FCF，而是按以下问题攻击：

1. 当前各变量是否职责重叠或漏项？
2. 是否仍有同一 raw feature 被重复结算？
3. Closing 的径向分离近似在哪些玩家操作下会产生错误排序？
4. Isotropic2D 在没有具体鱼点时是否是可接受的第一版 modeling convention？
5. Working anchors / burden budget 是否会让大量正常 Good target 长期饱和或长期归零？
6. prey support × response × temporal opportunity × Candidate 是否存在系统性过度衰减？
7. 哪些 OPEN 是阻塞 production 的 P0，哪些只是可后补的 calibration？
8. 是否存在不需要新增 runtime state 就能显著简化整个链条的方案？

要求 Reviewer：

- 区分事实、Candidate、Working seed、建议；
- 不把历史已关闭缺口重新当 Current OPEN；
- 不修改 Activity 文档；
- 不把缺少 owner 的内容凭空补成生产规则；
- 若提出替代公式，必须说明替代了哪个现有 owner、避免了什么重复计权，以及对现有 regression basket 的影响。

---

## 21. 深挖入口

本页是统一入口；需要审具体子问题时再下钻：

- `lure-feeding-response-proposal-c.md`：实际呈现 → prey interpretation / prey-conditioned state；
- `lure-response-proposal-c-feature-ownership-matrix.md`：raw feature ownership；
- `lure-response-proposal-c-current-food-value-bounds.md`：FoodValue 合法域；
- `lure-response-proposal-c-feeding-motivation-threshold.md`：Motivation → threshold；
- `lure-response-proposal-c-latent-bearing-prior.md`：latent bearing contract；
- `lure-response-proposal-c-latent-bearing-dimensionality-decision.md`：2D decision；
- `lure-response-proposal-c-closing-geometry-interpretation.md`：Closing 几何语义；
- `lure-response-proposal-c-intercept-speed-production-contract.md`：InterceptSpeedLimit production topology；
- `lure-response-proposal-c-reference-intercept-speed-working-anchors.md`：Working speed anchors；
- `lure-response-proposal-c-locomotor-archetype-catalog.md`：locomotor archetypes；
- `lure-response-proposal-c-combined-burden-stress-test.md`：联合 burden；
- `lure-response-proposal-c-temporal-exposure-opportunity.md`：Temporal Opportunity interface；
- `lure-response-proposal-c-adversarial-review-2026-10-26.md`：历史整链攻击报告，仅作 evidence；其中已关闭的 P0/P1 不应继续视为当前缺口。

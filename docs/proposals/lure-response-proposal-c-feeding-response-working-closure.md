# Proposal C｜Feeding Response Working Closure

状态：Working Closure / Candidate。不是 Current，也不是生产参数。

本页只承接 Proposal C 的 Candidate Delta。当前 RESPONSE Authority 仍由 `fcf-system-map/contracts.json` 指向外部中层样板 v8。远端对齐边界见 `lure-response-proposal-c-remote-alignment-audit-2026-10-26.md`。

## 1. 主链

```text
ActualPresentation
→ prey support
→ prey-conditioned current state
→ FoodValue / StateTrigger / Activity-aware Closing / Prediction / FeedingMotivation
→ latent-angle conditional response
→ prey-mode response
→ Feeding composition
→ Interaction composition
→ captureRetention
→ Candidate native retention join
```

Candidate 只消费 Interaction 聚合后的 `captureRetention C_i,j`。Response 不在 Candidate 侧再次计算或相乘。

## 2. Prey interpretation

### Prey support

每个 prey interpretation 都有一项支持强度。它表示当前呈现有多少依据可以按该猎物理解：

```text
baitfish: 0.90
crayfish: 0.75
frog: 0
```

support 有以下边界：

- 不要求各 prey support 之和为 1；
- 不强制选择唯一 prey identity；
- 不是 prey probability、FoodValue 或咬口概率；
- `Unknown`、`NotConfigured` 与 `NoMatch` 分开处理。

### Prey-conditioned current state

每种 prey interpretation 分别解释当前状态和过程，例如移动、低位移、上升、下落、surface、near-bottom、move→pause、sudden redirection、burst、escape-like 或 distressed-like evidence。状态解释不能直接附加匿名 response multiplier。

## 3. Feeding decision

### FoodValue

`FoodValue` 表示按当前 prey interpretation 判断目标是否值得吃。Working 分类为：

```text
Preferred > Good > Marginal > Poor > Reject
```

`Reject` 是 hard semantic boundary，不是普通低分。`Target Relation = Reject` 时，整个 prey feeding mode resolved zero。Trigger 和高 FeedingMotivation 都不能恢复它。

### StateTriggerValue

`StateTriggerValue` 表示当前 prey state 是否额外容易触发攻击。第一版只准入 `Escape-like`；`Injured / Struggling` 与 imbalance-like vulnerability 保持 `CandidateUnresolved`。Pause 本身不进入 Trigger。

首版通用正向证据只保留：

- sudden redirection event；
- burst / sudden acceleration event。

左右交替、时序不规则等先作为 prey-state pattern 的解释证据，不直接加分。

```text
AttackValue = FoodValue + StateTriggerValue
```

`AttackValue` 是解释对象，不要求成为独立 runtime object。State Trigger 属于 prey + current state local value，不修改 fish-global Motivation threshold。

### FeedingMotivation

```text
FeedingMotivation
→ WillingnessThreshold
```

低 Motivation 提高门槛，高 Motivation 降低门槛。Motivation 不改写 prey identity，也不被某个 prey-local trigger 反向修改。

## 4. Closing 与 Prediction

### 4.1 Closing / Intercept

系统没有权威鱼点，只有拟饵位置，因此首版不虚构鱼的世界坐标，也不指定米制鱼距 `D`。

物理追赶上限由 `species × size cohort` 配置或 Bake 产出的 `InterceptSpeedLimit` 提供。若 response 前已有权威具体个体长度，使用该个体对应的上限；否则使用当前 cohort 代表长度所烘出的上限。

```text
species × size cohort
→ InterceptSpeedLimit
→ Closing burden / capability scale

Fish Condition Bake
→ Activity
→ Closing soft-cost multiplier
```

`Activity` 不修改 `InterceptSpeedLimit`，也不与它相乘：

```text
Activity = 0
≠ InterceptSpeedLimit = 0
```

能力与拟饵速度使用同一参考系。首版采用相对水体速度：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
u_close(θ) = max(0, q * cosθ)
```

Closing Working closure：

```text
ClosingCost(θ)
= K_close × u_close(θ)^2
  × ActivityCostMultiplier(Activity)
```

第一版不把 `u_close >= 1` 直接变成 hard-zero。当前 `u_close` 只表示径向分离负担，不是完整 interception feasibility。没有合法的 current gap、strike reach、reaction latency 和 interaction-region exit window 时，高 `u_close` 仍由完整 `DecisionMargin` 与 response projection 决定是否得到数值 0。真正的 hard interception gate 只有在未来取得 encounter geometry / reaction-window contract 后才允许恢复。

Activity soft-cost 候选：

```text
ActivityCostMultiplier(A)
= 1 + K_activity × (1 - A)
```

`A=1` 不增加额外 pursuit soft cost。Activity 越低，主动追赶的 soft cost 越高。`u_close=0` 时 `ClosingCost=0`，不产生匿名 Activity 惩罚。`K_close` 与 `K_activity` 尚未 production calibration。

Closing 的含义：

- 拟饵正背离潜在鱼时 Closing Demand 最大；
- 横切不自动产生径向 closing burden；
- 朝鱼运动时 Closing Demand 可为 0；
- `u_close` 越高时 soft burden 越高，但不绕过完整 DecisionMargin 直接判死；
- `Activity` 只影响 Closing 的 soft cost，不改变 `InterceptSpeedLimit`；
- Prediction 第一版不进入 active numeric core；
- Risk cue 未启用时 `RiskCost = 0`；
- 真正的 hard interception gate 需要 encounter geometry / reaction-window contract。

`q >= 1` 不会让整个 mode hard-zero，因为其它角度仍可能可行。首版优先 `u_close²`，这是 Working shape，不是长期物理定律。没有 reaction distance 与 pursuit horizon 时，首版不显式拆 acceleration；其影响暂由短时 `InterceptSpeedLimit` 的口径吸收。

### Prediction

Prediction 第一版 Deferred，不进入 active numeric core。旧的 turn-event / `max_recent` 方案只保留为研究证据，不进入当前 DecisionMargin。

## 5. Decision Margin 与 projection

```text
DecisionMargin(θ)
= FoodValue
+ StateTriggerValue
- ClosingCost(θ)
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

高 `u_close` 的 latent angle 仍按 soft Closing burden 进入 `DecisionMargin`。只有未来已有 geometry-qualified hard-feasibility contract 且已知当前任务不可达时，才可在该 contract 规定的范围内输出 `C_conditional(θ)=0`。其它角度使用 Working projection：

```text
C_conditional(θ)
= ResponseProjection(DecisionMargin(θ))

C = clamp((Margin - M0) / (M1 - M0), 0, 1)
```

`M0 / M1` 是 calibration anchors，不是物理常数。

latent-angle 的固定顺序是：

```text
θ
→ u_close(θ)
→ ClosingCost(θ)
→ DecisionMargin(θ)
→ C_conditional(θ)
→ Eθ[C_conditional(θ)]
```

当前不在 Closing 层对 `u_close >= 1` 设置 hard-zero。不能先平均 `u_close` 或 `ClosingCost`，再做 nonlinear projection。否则会把不同 bearing 的负担压成不存在的“平均鱼”。

## 6. Prey response 与 Feeding composition

首版的 prey response 为：

```text
C_prey
= support_prey × Eθ[C_conditional,p(θ)]
```

这里复用 support 的 0～1 尺度作为 response-retention strength，不把 support 解释成 prey identity probability。当前不增加 `RecognitionProjection`、soft gate 或 S-curve。Unknown support 不得当 0 相乘，应保持 `ResolutionIncomplete`。`NoMatch` 与 `FoodValue=Reject` 也不是同一状态。

同一个 physical lure 同时支持 baitfish、crayfish、frog 等解释时，默认它们是同一次 feeding opportunity 的 alternative sibling interpretations：

```text
C_feed = max(C_baitfish, C_crayfish, C_frog, ...)
```

只有在这些 interpretation 明确属于同一 physical target 的替代解释时才使用该 `max`。首版不默认求和、概率 union 或 support 归一化后的 mixture average。独立 synergy 需要单独 admission。

## 7. Typed status 与硬边界

### ResolutionIncomplete

必要输入未解析：

```text
no scalar
not rollable
```

### ResolvedNonResponsive

必要语义已解析，但 response 为 0：

```text
C_mode = 0
```

### ResolvedResponsive

```text
0 < C_mode ≤ 1
```

### Reject

```text
Target Relation = Reject
→ whole prey feeding mode resolved zero
```

Trigger 和高 Motivation 不能救活 Reject。

### Closing hard gate

当前不设置 Closing hard gate。`u_close` 只进入 soft Closing cost。未来只有在取得 encounter geometry / reaction-window contract 后，才可定义 hard interception gate。

## 8. Pause、dwell 与 cadence

Pause 不获得匿名 `PauseBonus`。它只通过已有路径产生后果：

- lure speed 下降，Closing Demand 降低；
- 没有新的 abrupt redirection，Prediction 不产生 active cost；
- prey-conditioned process interpretation 改变，只有在有独立证据时才改变 StateTriggerValue。

不增加 `PredictionResetBonus`。`burst → pause` 也不整体增加一次 Trigger。

`favorable dwell` 不进入 Feeding `DecisionMargin`，也不新增 `DwellBonus` 或 `PauseDurationCoeff`。如果两个状态的 FoodValue、Trigger、Closing、Risk、Motivation 都相同，只是有利状态持续时间不同，那么瞬时 Feeding response `C` 相同。

更长 dwell 的优势属于：

```text
resolved response state
× Opportunity support L
→ cumulative opportunity
```

当前 `L` 由 Opportunity owner 承接。Feeding 不接管 temporal exposure、空间覆盖或 duration integration。

首版不准入独立 `CadenceValue`、`CadenceBonus` 或 `CadencePenalty`。只有在其它量完全相同、唯一稳定变化是 temporal motif，且仍产生可复现、可解释、玩家可学习的 ranking difference 时，才重新打开 cadence scalar。当前 cadence 只保留为事件历史 / Explain feature。

## 9. Feeding、Interaction 与 Candidate

Feeding 产生 `C_feed`，它是 Interaction 内部的 complete-mode contribution。Interaction 按声明的 routing relation 与 Defense、Investigation 等其它 Complete Modes 聚合，得到：

```text
CaptureResponsePacket
└─ captureRetention C_i,j
```

跨 family operator 不在本页统一设为 `max`：

- overlapping alternatives 可用 `max`；
- primary-with-fallback 不是 `max`；
- exclusive mixture / set union 需要各自合法 operator。

Candidate Resolver 只消费聚合后的 `C_i,j`：

```text
q_i,j = L_i,j × C_i,j
```

Interaction response 只结算一次。禁止 `L × C → W → W × C`，也不把 native response 伪装成 Pre-Roll Gameplay MassTransform。

## 10. Effect-size 护栏

当前证据只支持方向与体验预算，不支持 production anchors。

- State Trigger 的 Working budget 约为 `0.10～0.15` 的 Decision-Margin 尺度。它可以帮助 Marginal、增强 Good，但不能普遍把 Poor 抬成主力，也不能救活 Reject。
- Prediction 第一版不进入 active numeric core；
- `RiskCost` 在 Risk cue Disabled / NotConfigured 时为 0；

需要保持的体验排序：

- poor bite + fast retrieve 明显差；
- poor bite + slow / pause 有显著 rescue；
- normal bite 下 normal-fast 仍有竞争力；
- good bite 下 faster retrieve 可以接近 reference-good；
- moderate prey-appropriate darting 优于机械直线；
- 极端高速乱窜可以因 Closing 或 Opportunity consequences 变差，不靠匿名 erratic penalty 或 Prediction 强制实现；
- 同一 presentation 下，不同 `InterceptSpeedLimit` 的鱼只通过物理可行性和 Closing cost 产生响应差异。

## 11. 不得恢复的路线

- `Drive = FoodValue × Motivation` 作为默认核心；
- 匿名 `PauseBonus`；
- `PauseDurationCoeff`、`DwellBonus` 或 `PredictionResetBonus`；
- 通用 `ErraticBonus`；
- `CadenceValue`、通用 `CadenceBonus` 或 `CadencePenalty`；
- 具体鱼世界坐标或未经授权的米制鱼距 `D`；
- 资料表 maximum speed 直接充当 `InterceptSpeedLimit`；
- 把 burst speed、critical speed、cruising speed 当成同一个量；
- 把 Activity 乘进 `InterceptSpeedLimit`，或用 Activity 产生 hard feasibility；
- Motivation 修改 locomotor capacity；
- 同一环境或生理原因已进入 Activity 后，再在 Closing 重复处罚；
- 没有 reaction distance / pursuit horizon 时伪造完整 acceleration pursuit；
- 把 prey support 当 prey probability、归一化 mixture 或 binary admission gate；
- 仅凭 `u_close >= 1` 直接产生 hard-zero；
- whole-mode `q>1` hard-zero；
- 先平均 `u_close` / `ClosingCost` 再做 response projection；
- 为拟合效果直接使用高次 Closing 幂；
- 用 `ω_traj / fish_turn_capacity` 作为通用 ManeuverCost；
- Maneuver utilization >1 就 whole-mode hard zero；
- 任意 PredictionChallenge threshold 直接 hard-zero；
- 为补 temporal exposure 缺口而提高 Feeding `C`；
- Candidate Resolver 逐 mode 解释 Feeding / Defense 语义；
- Interaction response 在 Candidate 侧二次相乘。

## 12. 尚未闭合

以下项目仍是 OPEN / Working：

- FoodValue production anchors；
- FeedingMotivation → WillingnessThreshold production mapping；
- `K_close` / `K_activity` production calibration；
- species × size cohort 的 `InterceptSpeedLimit` 数据来源、代表长度、生成方法与 cohort 拆分阈值；
- Activity raw-cause 曲线与 `min` reducer 的 controlled validation；
- 是否需要 fish-quality / individual variation；
- latent-angle prior 的生产定义；
- 若未来获得 reaction distance / pursuit horizon authority，是否拆出 acceleration；
- `PredictionChallenge`、`τ_recover`、`K_pred` 和旧 prediction probe 不进入当前 OPEN；
- `M0 / M1`；
- State Trigger production budget；
- support × conditional response 的 production calibration；
- prey-family-specific escape / distress state rules；
- Opportunity `L` production contract；
- Feeding / Defense / Investigation 的最终 route graph 与 operators；
- runtime hot-path struct / representation；
- production calibration 与自动回归阈值。

Cadence scalar 不在默认 OPEN 列表中。只有满足 residual admission gate 才重新打开。

## 13. 证据文档

窄主题文档保留证据与回归说明，不自动覆盖本页：

- `lure-response-proposal-c-food-value-surface.md`
- `lure-response-proposal-c-feeding-response-threshold.md`
- `lure-response-proposal-c-response-projection.md`
- `lure-response-proposal-c-task-cost-structure.md`
- `lure-response-proposal-c-task-cost-rho.md`
- `lure-response-proposal-c-angle-only-intercept.md`
- `lure-response-proposal-c-closing-cost-shape.md`
- `lure-response-proposal-c-intercept-capacity-semantics.md`（旧能力路线证据）
- `lure-response-proposal-c-maneuver-input-routing.md`（历史 Working；通用 ManeuverCost 已替代）
- `lure-response-proposal-c-prediction-challenge.md`
- `lure-response-proposal-c-prediction-cost-budget.md`
- `lure-response-proposal-c-favorable-dwell-ownership.md`
- `lure-response-proposal-c-cadence-residual-admission.md`
- `lure-response-proposal-c-erratic-state-trigger.md`
- `lure-response-proposal-c-escape-feature-routing.md`
- `lure-response-proposal-c-state-trigger-budget.md`
- `lure-response-proposal-c-state-trigger-ownership.md`
- `lure-response-proposal-c-end-to-end-ordering.md`
- `lure-response-proposal-c-prey-support-bridge.md`
- `lure-response-proposal-c-support-retention-projection.md`
- `lure-response-proposal-c-candidate-bridge-closure.md`

清理前 Proposal C 全文仍在 archive，用于历史查阅，不回流为当前规则。

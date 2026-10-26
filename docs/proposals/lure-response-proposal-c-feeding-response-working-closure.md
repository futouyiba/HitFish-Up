# Proposal C｜Feeding Response Working Closure

状态：Working Closure / Candidate。不是 Current，不是生产参数。

对齐基线：

- 最新已检查 `main`：`cd74d363d0478d7c7aecfeb7320ff0419b1b6fd0`
- 当前 RESPONSE Authority 仍由 `fcf-system-map/contracts.json` 指向外部中层样板 v8；本页只承接 Proposal C 的 Candidate Delta。
- 远端对齐与清理检查见 `lure-response-proposal-c-remote-alignment-audit-2026-10-26.md`。

## 1. 当前主线

```text
ActualPresentation
→ prey support
→ prey-conditioned current state
→ fish-side value / closing / prediction / motivation evaluation
→ latent-angle conditional response
→ prey-mode response
→ Feeding composition
→ Interaction composition
→ captureRetention
→ Candidate native retention join
```

本页只收当前仍承重的 Working 结论。窄主题 probe / 文档继续保留证据与回归说明。

## 2. Prey interpretation

### 2.1 Prey support

第2步输出每个 prey interpretation 的支持强度，例如：

```text
baitfish: 0.90
crayfish: 0.75
frog: 0
```

语义是“当前呈现有多少依据可以按该猎物理解”。必须保持：

- 不要求不同 prey support 之和为1；
- 不强制选唯一 prey identity；
- support 不是 prey probability、FoodValue 或咬口概率；
- Unknown / NotConfigured / NoMatch 分开。

### 2.2 Prey-conditioned current state

按每种 prey interpretation 解释当前状态与过程，例如移动、低位移、上升、下落、surface、near-bottom、move→pause、sudden redirection、burst、escape-like / distressed-like state evidence。

状态解释不能直接贴匿名 response multiplier。

## 3. Feeding Decision

### FoodValue

回答：如果把当前目标按这种 prey 理解，这条鱼觉得它值不值得吃？

Working class：

```text
Preferred > Good > Marginal > Poor > Reject
```

`Reject` 是 hard semantic boundary，不是普通低数值。

### StateTriggerValue

回答：这个 prey 当前状态是否额外容易触发攻击？

当前只准入 prey-conditioned 的 escape / erratic / distress 类状态价值。它不是通用 `ErraticBonus`。

第一版通用正向证据只保留 sudden redirection event 与 burst / sudden acceleration event。左右交替、时序不规则等先作为 prey-state pattern 的解释证据，不默认直接加分。

State Trigger 属于 prey + current state local value，不修改 fish-global Motivation threshold。

解释上可写：

```text
AttackValue = FoodValue + StateTriggerValue
```

`AttackValue` 当前不需要成为独立 production object。

### Feeding Motivation

回答：这条鱼现在总体有多愿意出手？

```text
Motivation
→ WillingnessThreshold
```

低 Motivation 提高门槛，高 Motivation 降低门槛。Motivation 不改写 prey identity，也不被某一 prey-local trigger 反向修改。

## 4. Closing 与 Prediction

### 4.1 Closing / Intercept

系统没有具体鱼点，只有拟饵具体位置，因此不虚构鱼的世界坐标。

用 latent relative angle `θ` 表示潜在鱼相对拟饵运动方向的未知微观方位：

```text
q = lure_speed / intercept_capacity
u_close(θ) = max(0, q * cosθ)
```

第一版 Closing Working closure：

```text
if u_close(θ) >= 1:
    C_conditional(θ) = 0
else:
    ClosingCost(θ) = K_close × u_close(θ)^2
```

含义：

- 拟饵正背离潜在鱼时 Closing Demand 最大；
- 横切不自动形成径向 closing burden；
- 朝鱼运动时 Closing Demand 可为0；
- 中低 utilization 只产生较轻 cost；
- 接近能力边界时 cost 快速抬升；
- 明确超过 Closing capacity 时，只把对应 latent angle 判为 hard infeasible。

`q >= 1` 不能推出 whole mode hard-zero，因为其它角度仍可能可行。最终仍按 `θ → C(θ) → Eθ[C(θ)]` 聚合。

当前优先 `u²`，不是长期物理定律。probe 比较表明，一旦 `u>=1` 已经 angle-local hard-zero，继续从二次升到四次主要增加拟合自由度，没有购买新的策略语义。

绝对鱼距 `D` 当前不准入首版。随便假设 1m / 3m / 5m 会产生玩法级差异，而系统没有权威个体距离事实。

Functional Capacity 已通过 `intercept_capacity` 进入 q；不得再按“强鱼 / 弱鱼身份”重复处罚。

### 4.2 Prediction Challenge

通用 `ManeuverCost(ω_traj / fish_turn_capacity)` 已撤回作为第一版 numeric core。没有具体鱼点、鱼朝向和截获路径时，拟饵自身转向角速度不能推出鱼必须以同样速度转弯。

当前更窄的 Working semantic：

```text
sudden direction-change event
→ existing attack prediction temporarily degrades
→ PredictionChallenge
→ soft PredictionCost
```

Working probe：

```text
TurnStrength(Δψ) = (1 - cosΔψ) / 2
P(t) = max_recent[TurnStrength × exp(-age / τ_recover)]
```

PredictionChallenge 是暂态，只允许 soft cost，不产生 hard infeasible。连续 zig-zag 首版只通过不断刷新近期 challenge 生效，不另叠 CadencePenalty。

当前 effect-size Working：

```text
PredictionCost = K_pred × PredictionChallenge
K_pred ≈ 0.08～0.12
```

护栏：`K_pred` 默认不强于 Working TriggerBudget。中等 prey-appropriate dart 不应仅因 Prediction 反转成负收益。

## 5. 折线运动的双路径

同一次 sudden redirection / darting 可以同时产生：

```text
trajectory event
├→ prey-conditioned escape/distress interpretation
│  → StateTriggerValue (+)
└→ prediction disruption
   → PredictionChallenge
   → PredictionCost (-)
```

两条链回答不同问题，不属于重复计权。

不手工设计“中等 erratic 最好”的钟形 bonus。Trigger、Prediction、Closing 等真实路径共同决定最终排序。

## 6. Decision Margin 与 Projection

当前 Working numeric topology：

```text
DecisionMargin(θ)
= FoodValue
+ StateTriggerValue
- ClosingCost(θ)
- PredictionCost
- WillingnessThreshold(Motivation)
```

对 Closing infeasible 的 latent angle，不进入普通 margin，而是直接得到 `C_conditional(θ)=0`。

其它角度再做：

```text
C_conditional(θ)
= ResponseProjection(DecisionMargin(θ))
```

第一版 projection 倾向 clipped linear：

```text
C = clamp((Margin - M0) / (M1 - M0), 0, 1)
```

`M0 / M1` 是 calibration anchors，不是物理常数。

## 7. latent angle 的平均顺序

硬 topology：

```text
θ
→ u_close(θ)
→ [hard infeasible or ClosingCost(θ)]
→ DecisionMargin(θ)
→ C_conditional(θ)
→ Eθ[C_conditional(θ)]
```

不能先平均 `u_close` 或 ClosingCost 再做 nonlinear projection。否则会把部分角度 hard-zero、部分角度高响应的混合压成不存在的“平均鱼”。

## 8. Prey support 如何进入 response

第一版最小结构：

```text
C_prey
= support_prey × Eθ[C_conditional,p(θ)]
```

这里复用 support 的 0～1 尺度作为 response-retention strength，不把它解释成 prey identity probability。

当前不增加额外 `RecognitionProjection` / soft gate / S-curve。Unknown support 不得当0相乘；保持 `ResolutionIncomplete`。

`NoMatch` 与 `FoodValue=Reject` 语义不同。

## 9. 多 prey interpretation 的 Feeding composition

同一个物理拟饵同时支持 baitfish / crayfish / frog 等解释时，默认是同一次 feeding opportunity 的 alternative sibling interpretations。

第一版：

```text
C_feed = max(C_baitfish, C_crayfish, C_frog, ...)
```

前提是这些 siblings 明确声明为同一 physical target 的替代解释。

不默认求和、概率 union 或 support 归一化后的 mixture average。跨 prey interpretation 的独立 synergy 若未来成立，需要单独 admission。

## 10. Typed status 与 hard boundaries

### ResolutionIncomplete

必要输入未解析：

```text
no scalar
not rollable
```

### ResolvedNonResponsive

所有必要语义已解析但 response 为0：

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

Trigger 与高 Motivation 都不能救活 Reject。

### Closing Infeasible

只对对应 latent angle 局部置零。PredictionChallenge 不拥有 hard-zero authority。

## 11. Pause、dwell 与 cadence

Pause 不获得匿名 `PauseBonus`。它只通过已有因果路径产生后果：

- lure speed 下降 → Closing Demand 降低；
- 没有新的 abrupt redirection → PredictionChallenge 自然衰减；
- prey-conditioned process interpretation 改变 → 若有独立证据则改变 StateTriggerValue。

不增加 `PredictionResetBonus`；`burst → pause` 不能整体再增加一次 Trigger。

### Favorable dwell

`favorable dwell` 不进入 Feeding `DecisionMargin`，也不新增 `DwellBonus` / `PauseDurationCoeff`。

若两个状态当前 FoodValue、Trigger、Closing、Prediction、Motivation 都相同，只是有利状态已经持续的时长不同，则它们的**瞬时 Feeding response `C` 相同**。

更长 dwell 的优势属于：

```text
resolved response state
× temporal exposure / opportunity support
→ cumulative opportunity
```

当前 `main` 没找到已承接 temporal exposure integration 的 Current Markdown Contract。这是明确缺口：Feeding 不接管，后续由 Opportunity / temporal exposure 的合法 Owner 承接。

### Cadence motif

第一版不准入独立 `CadenceValue` / `CadenceBonus` / `CadencePenalty`。

当前已有更具体的 owner 承接其大部分可解释效果：StateTrigger、Prediction、Closing、attention/history、temporal exposure。

只有在这些量全部相同、唯一稳定变化是 temporal motif，且仍产生可复现、可解释、玩家可学习的 ranking difference 时，才重新打开 cadence scalar。当前 cadence 只保留为事件历史 / Explain feature。

## 12. Feeding → Interaction → Candidate

Feeding 内得到 `C_feed`。它仍是 Interaction 内部 complete-mode contribution。

Interaction 负责和 Defense / Investigation 等其他 Complete Modes 按声明的 routing relation 聚合，得到 support-aligned：

```text
CaptureResponsePacket
└─ captureRetention C_i,j
```

跨 family operator 不由本页统一设成 max。已知规则：overlapping alternatives 可用 max；primary-with-fallback 不是 max；exclusive mixture / set union 需要各自合法 operator。

Candidate Resolver 只消费聚合后的 `C_i,j`：

```text
q_i,j = L_i,j × C_i,j
```

Interaction response 只结算一次。禁止 `L × C → W → W × C`，也不得把 native response 再伪装成 Pre-Roll Gameplay MassTransform。

## 13. 当前 effect-size 护栏

当前证据只支持方向与体验预算，不支持 production anchors。

State Trigger 的 Working budget 倾向约 `0.10～0.15` 的 Decision-Margin 尺度：能明显帮助 Marginal、增强 Good，但不能把 Poor 普遍抬成主力，也不能救活 Reject。

Prediction Cost 的 Working budget 倾向约 `0.08～0.12`：默认不强于 State Trigger；中等 dart 不因 Prediction alone 反转成负收益；hard turn 可以削薄即时 Trigger；极端动作的负面结果由多条真实路径共同形成。

Closing 的形状先冻结为 `K_close × u_close²` + angle-local hard infeasible；`K_close` 尚未 calibration。

需要保持的体验排序：

- poor bite + fast retrieve 明显差；
- poor bite + slow/pause 有显著 rescue；
- normal bite 下 normal-fast 仍有竞争力；
- good bite 下 faster retrieve 可以接近 reference-good；
- moderate prey-appropriate darting 明显优于机械直线；
- 极端高速乱窜可以因 Closing / Prediction / temporal consequences 重新变差，但不是由匿名 erratic penalty 强制实现；
- 同 presentation 下 Functional Capacity 更强的鱼，不应因 identity 再被重复惩罚。

## 14. 已拒绝 / 已撤回

当前不应静默恢复：

- `Drive = FoodValue × Motivation` 作为默认核心；
- 匿名 `PauseBonus`；
- `PauseDurationCoeff` / `DwellBonus`；
- `PredictionResetBonus`；
- 通用 `ErraticBonus`；
- `CadenceValue` / 通用 `CadenceBonus` / `CadencePenalty`；
- 具体鱼世界坐标；
- 随便指定米制鱼距 `D`；
- prey support 当 prey probability；
- prey support 归一化成 mixture；
- support 只做 binary admission gate；
- whole-mode `q>1` hard-zero；
- 先平均 `u_close` / ClosingCost 再做 response projection；
- 为拟合效果直接采用高次 Closing 幂；
- `ω_traj / fish_turn_capacity` 直接作为通用 ManeuverCost；
- Maneuver utilization >1 就 whole-mode hard zero；
- 任意 PredictionChallenge threshold 直接 hard-zero；
- 为补 temporal exposure 缺口而提高 Feeding `C`；
- Candidate Resolver 逐 mode 解释 Feeding / Defense 语义；
- Interaction response 在 Candidate 侧二次相乘。

## 15. 尚未闭合

以下仍是 OPEN / Working：

- FoodValue production anchors；
- Motivation → Threshold production mapping；
- `K_close` 与 `intercept_capacity` production calibration；
- latent-angle prior 的生产定义；
- PredictionChallenge 的 production event extraction；
- `τ_recover` 与 `K_pred` production calibration；
- `M0 / M1`；
- State Trigger production budget；
- support × conditional response 的 production calibration；
- prey-family-specific escape/distress state rules；
- Opportunity / temporal exposure 的 Current Owner 与 cumulative operator；
- Feeding / Defense / Investigation 的最终 route graph 与 operators；
- runtime hot-path struct / representation；
- production calibration 与自动回归阈值。

Cadence scalar 已从默认 OPEN 列表移除；只有满足 residual admission gate 才重新打开。

## 16. 证据文档

窄主题文档继续承担证据与回归说明，包括：

- `lure-response-proposal-c-food-value-surface.md`
- `lure-response-proposal-c-feeding-response-threshold.md`
- `lure-response-proposal-c-response-projection.md`
- `lure-response-proposal-c-task-cost-structure.md`
- `lure-response-proposal-c-task-cost-rho.md`
- `lure-response-proposal-c-angle-only-intercept.md`
- `lure-response-proposal-c-closing-cost-shape.md`
- `lure-response-proposal-c-maneuver-input-routing.md`（历史 Working，其中通用 ManeuverCost 已被后续工作替代）
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

清理前 Proposal C 全文继续保存在 archive，用于考古，不回流成当前规则。

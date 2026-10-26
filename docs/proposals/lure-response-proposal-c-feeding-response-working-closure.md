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

本页只收当前仍承重的 Working 结论。窄主题 probe / 文档继续保留证据，不把历史推导重新塞回总入口。

## 2. 类型与状态先于鱼侧价值

### 2.1 Prey support

第2步输出每个 prey interpretation 的支持强度，例如：

```text
baitfish: 0.90
crayfish: 0.75
frog: 0
```

语义是“当前呈现有多少依据可以按该猎物理解”。

必须保持：

- 不要求不同 prey support 之和为1；
- 不强制选唯一 prey identity；
- support 不是 prey probability；
- support 不是 FoodValue；
- support 不是咬口概率；
- Unknown / NotConfigured / NoMatch 分开。

### 2.2 Prey-conditioned current state

按每种 prey interpretation 解释当前状态和过程，例如：

- 移动 / 低位移；
- 上升 / 下落；
- surface / near-bottom；
- move→pause；
- sudden redirection；
- burst；
- escape-like / distressed-like state evidence。

状态解释不能直接贴匿名 response multiplier。

## 3. Feeding Decision 的当前 Working 核心

对一个已解析的 prey interpretation，先在“假定该 prey interpretation 成立”的条件下算鱼侧响应。

### 3.1 Food Value

回答：

> 如果把当前目标按这种 prey 理解，这条鱼觉得它值不值得吃？

Working class：

```text
Preferred > Good > Marginal > Poor > Reject
```

`Reject` 是 hard semantic boundary，不是普通低数值。

### 3.2 State Trigger Value

回答：

> 这个 prey 当前状态是否额外容易触发攻击？

当前只正式准入 prey-conditioned 的 escape / erratic / distress 类状态价值。

它不是通用 `ErraticBonus`。

第一版通用正向证据只保留：

- sudden redirection event；
- burst / sudden acceleration event。

左右交替、时序不规则等更适合作为 prey-state pattern 的解释可信度，不默认直接加分。

`burst → pause` 不作为整体 bonus；pause 的作用由 Closing、Prediction 和 prey-state 等各自承接。

State Trigger 属于 prey + current state local value，不修改 fish-global Motivation threshold。

解释上可以写：

```text
AttackValue = FoodValue + StateTriggerValue
```

`AttackValue` 目前不需要成为独立 production object。

### 3.3 Feeding Motivation

回答：

> 这条鱼现在总体有多愿意出手？

当前 Working 表达：

```text
Motivation
→ WillingnessThreshold
```

低 Motivation 提高出手门槛，高 Motivation 降低门槛。

Motivation 不改写 prey identity，也不被某一 prey-local trigger 反向修改。

## 4. Capture / Prediction 侧

### 4.1 Closing / Intercept

当前系统没有具体鱼点，只有拟饵的具体位置。因此不虚构某条鱼的世界坐标。

用 latent relative angle `θ` 表示潜在鱼相对拟饵运动方向的未知微观方位。

第一版 reduced Closing proxy：

```text
q = lure_speed / intercept_capacity
u_close(θ) = max(0, q * cosθ)
```

含义：

- 拟饵正背离潜在鱼时 Closing Demand 最大；
- 横切不自动形成径向 closing burden；
- 朝鱼运动时 Closing Demand 可为0。

绝对鱼距 `D` 当前不准入首版 Intercept。之前灵敏度检查表明，随便假设 1m / 3m / 5m 会产生玩法级差异，而系统没有权威个体距离事实。

Closing 可以在特定 `θ` 下 hard infeasible；该角度的 conditional response 为0。部分角度 infeasible 不等于 whole mode hard-zero。

### 4.2 Prediction Challenge

通用 `ManeuverCost(ω_traj / fish_turn_capacity)` 已撤回作为第一版 numeric core。

原因：没有具体鱼点、鱼朝向和截获路径时，拟饵自身转向角速度不能推出鱼必须以同样速度转弯。规则圆周也可能转得很快却高度可预测。

当前更窄的 Working semantic 是：

```text
sudden direction-change event
→ existing attack prediction temporarily degrades
→ PredictionChallenge
→ soft PredictionCost
```

Working event proxy：

```text
TurnStrength(Δψ) = (1 - cosΔψ) / 2
P(t) = max_recent[TurnStrength × exp(-age / τ_recover)]
```

这只是 topology probe，不是生产公式。

PredictionChallenge：

- 是暂态；
- 只允许 soft cost；
- 不产生 hard infeasible；
- 连续 zig-zag 首版只通过不断刷新近期 challenge 生效，不另叠 `CadencePenalty`。

如果未来 controlled fixture 证明：在相同近期最大 turn、相同 Closing 与 temporal exposure 下，多次反向仍有独立负效应，再准入 event accumulation / frequency semantic。

### 4.3 Prediction effect-size

当前 Working：

```text
PredictionCost = K_pred × PredictionChallenge
```

其中 `K_pred` 的 probe budget 约为 `0.08～0.12` 的 Decision-Margin 尺度。

它被刻意限制为小修正项：

- 一次 prey-appropriate 的中等 dart 通常仍应净正向；
- 急转可以明显削薄 Trigger 收益；
- 极端高速乱窜是否最终变差，应由 Prediction、Closing 和其它真实后果共同形成；
- Prediction 不单独把所有 erratic action 判成坏动作。

当前护栏：

```text
K_pred <= Working TriggerBudget
```

这是当前复杂度护栏，不是长期物理定律。

## 5. 折线运动的双路径

同一次 sudden redirection / darting 可以同时产生两个不同后果：

```text
trajectory event
    ├→ prey-conditioned escape/distress interpretation
    │      → StateTriggerValue (+)
    │
    └→ prediction disruption
           → PredictionChallenge
           → PredictionCost (-)
```

这不是重复计权，因为两条链回答不同问题。

不手工设计“中等 erratic 最好”的钟形 bonus。当前 Working 解释是：

- Trigger 随 prey-appropriate escape state 增强后饱和；
- Prediction 让突然转向的即时收益变薄；
- Closing 等其它真实后果继续保留独立因果权力；
- 最终是否形成中间最优，由这些路径共同决定。

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

再做：

```text
C_conditional(θ)
= ResponseProjection(DecisionMargin(θ))
```

第一版 projection 倾向 clipped linear：

```text
C = clamp((Margin - M0) / (M1 - M0), 0, 1)
```

当前 sigmoid 只带来很小拟合改善，没有购买新的策略语义。

`M0 / M1` 仍是 calibration anchors，不是物理常数。

## 7. latent angle 的平均顺序

这是硬 topology 约束。

正确：

```text
θ
→ ClosingCost(θ)
→ DecisionMargin(θ)
→ C_conditional(θ)
→ Eθ[C_conditional(θ)]
```

PredictionCost、FoodValue、StateTriggerValue、MotivationThreshold 若在该微观角度分布上不变，可以在每个 `θ` 的 margin 中复用同一值，但不能先把 Closing 非线性结果平均掉。

错误：

```text
Eθ[ClosingCost]
→ one average Margin
→ one C
```

因为中间存在 angle-local hard infeasible、非线性 cost 与截断 projection。先平均会制造不存在的“平均鱼”。

## 8. Prey support 如何进入 response

第一版最小结构：

```text
C_prey
= support_prey × Eθ[C_conditional,p(θ)]
```

这里复用 support 的 0～1 尺度作为 response-retention strength。

重要：

> `support=0.7` 不表示“70%概率它是这种猎物”。

这里只表示这套 interpretation 以0.7的解释强度贡献其条件响应。

当前不增加额外 `RecognitionProjection` / soft gate / S-curve。若未来反例证明 support 的线性 retention 失真，再准入新的 `R(support)`。

Unknown support 不得当0相乘；它保持 `ResolutionIncomplete`。

`NoMatch` 与 `FoodValue=Reject` 语义不同。

## 9. 多 prey interpretation 的 Feeding composition

同一个物理拟饵同时支持 baitfish / crayfish / frog 等解释时，默认是**同一次 feeding opportunity 的 alternative sibling interpretations**，不是多份独立 opportunity。

第一版默认：

```text
C_feed = max(C_baitfish, C_crayfish, C_frog, ...)
```

前提：这些 siblings 已明确声明为同一 physical target 的替代解释。

不默认：

- 求和；
- 概率 union；
- support 归一化后做 mixture average。

若未来证明跨 prey interpretation 存在独立 synergy，需要单独 admission；不能默默从 max 改成增益聚合。

## 10. typed status / hard boundaries

### ResolutionIncomplete

必要输入未解析时：

```text
no scalar
not rollable
```

不得补成0或1。

### ResolvedNonResponsive

所有必要语义已解析，但 response 为0：

```text
C_mode = 0
```

这是合法 native zero。

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

只对对应 latent angle 局部置零；不因为部分角度 infeasible 就默认 whole mode hard zero。

PredictionChallenge 不拥有 hard-zero authority。

## 11. pause / dwell / cadence 去重

pause 不获得匿名 `PauseBonus`。

它可以通过：

- lure speed 下降 → Closing Demand 降低；
- 没有新的 abrupt redirection → `PredictionChallenge` 随时间自然衰减；
- prey-conditioned process interpretation 改变 → 若有独立证据则改变 StateTriggerValue。

不再增加独立 `PredictionResetBonus`。

`burst → pause` 不能整体再增加一次 State Trigger。

### Favorable dwell

`favorable dwell` 不进入 Feeding `DecisionMargin`，也不新增 `DwellBonus` / `PauseDurationCoeff`。

受控条件下，如果两个状态当前的 FoodValue、Trigger、Closing、Prediction、Motivation 都相同，只是有利状态已经持续的时长不同，则它们的**瞬时 Feeding response `C` 相同**。

更长 dwell 的优势属于：

```text
resolved response state
× temporal exposure / opportunity support
→ cumulative opportunity
```

不是：

```text
longer dwell
→ fish-side instantaneous value increases
```

当前仓内 `main` 没找到已承接 temporal support / exposure integration 的 Current Markdown Contract。因此这是明确缺口：Feeding 不接管，后续需要由 Opportunity / temporal exposure 的合法 Owner 承接。

Duration 仍可作为上游事实进入已存在的语义，例如 PredictionChallenge 的恢复时间、prey-specific process state 或 attention history；但不变成通用 duration bonus。

Cadence motif 仍未完全闭合。当前也不增加通用 `CadencePenalty`。未来若要准入 cadence residual effect，必须在 current speed / Closing、Prediction、StateTrigger、attention、total temporal exposure、Motivation 都相同后仍产生稳定 ranking difference。

## 12. Feeding → Interaction → Candidate

Feeding 内得到：

```text
C_feed
```

它仍是 Interaction 内部 complete-mode contribution。

Interaction 负责和 Defense / Investigation 等其他 Complete Modes 按声明的 routing relation 聚合，得到 support-aligned：

```text
CaptureResponsePacket
└─ captureRetention C_i,j
```

跨 family 的 operator 不由本页统一设成 max。

既有规则仍是：

- overlapping alternatives 可用 max；
- primary-with-fallback 不是 max；
- exclusive mixture / set union 需要各自合法 operator。

Candidate Resolver 只消费聚合后的 `C_i,j`：

```text
q_i,j = L_i,j × C_i,j
```

Interaction response 只结算一次。禁止：

```text
L × C
→ W
→ W × C
```

也不得把 native response 再伪装成 Pre-Roll Gameplay MassTransform。

## 13. 当前 Working effect-size 护栏

当前证据只支持方向与体验预算，不支持 production anchors。

### State Trigger

Working budget 倾向约 `0.10～0.15` 的 Decision-Margin 尺度，目标是：

- 能明显帮助 Marginal 跨门槛；
- 能增强 Good；
- 不能把 Poor 普遍抬成主力；
- 不能救活 Reject。

### Prediction Cost

Working budget 倾向约 `0.08～0.12`：

- 默认不强于 State Trigger；
- 中等 dart 不因 Prediction alone 反转成负收益；
- hard turn 可以显著削薄即时 Trigger；
- 极端动作的负面结果由多条真实路径共同形成。

以上均不是生产数值。

### Reference fishing stories

需要保持：

- poor bite + fast retrieve 明显差；
- poor bite + slow/pause 有显著 rescue；
- normal bite 下 normal-fast 仍有竞争力；
- good bite 下 faster retrieve 可以接近 reference-good；
- moderate prey-appropriate darting 能明显优于机械直线；
- 极端高速乱窜可以因 Closing / Prediction / temporal consequences 重新变差，但不是由匿名 erratic penalty 强制实现；
- 同 presentation 下 Functional Capacity 更强的鱼，不应因 identity 再被重复惩罚。

## 14. 已拒绝 / 已撤回的结构

当前不应静默恢复：

- `Drive = FoodValue × Motivation` 作为默认核心；
- 匿名 `PauseBonus`；
- `PauseDurationCoeff` / `DwellBonus`；
- `PredictionResetBonus`；
- 通用 `ErraticBonus`；
- 通用 `CadencePenalty`；
- 具体鱼世界坐标；
- 随便指定米制鱼距 `D`；
- `prey support` 当 prey probability；
- `prey support` 归一化成 mixture；
- support 只做 binary admission gate；
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
- ClosingCost production function；
- PredictionChallenge 的 production event extraction；
- `τ_recover` 与 `K_pred` production calibration；
- `M0 / M1`；
- State Trigger production budget；
- support × conditional response 的 production calibration；
- prey-family-specific escape/distress state rules；
- Opportunity / temporal exposure 的 Current Owner 与 cumulative operator；
- cadence motif 是否仍需要独立 semantic；
- Feeding / Defense / Investigation 的最终 route graph 与 operators；
- runtime hot-path struct / representation；
- production calibration 与自动回归阈值。

## 16. 证据文档

本页是当前 Working 归并入口。窄主题文档继续承担证据与回归说明，不因本页建立而删除，包括：

- `lure-response-proposal-c-food-value-surface.md`
- `lure-response-proposal-c-feeding-response-threshold.md`
- `lure-response-proposal-c-response-projection.md`
- `lure-response-proposal-c-task-cost-structure.md`
- `lure-response-proposal-c-task-cost-rho.md`
- `lure-response-proposal-c-angle-only-intercept.md`
- `lure-response-proposal-c-maneuver-input-routing.md`（历史 Working，关于通用 ManeuverCost 的部分已被后续 PredictionChallenge 工作替代）
- `lure-response-proposal-c-prediction-challenge.md`
- `lure-response-proposal-c-prediction-cost-budget.md`
- `lure-response-proposal-c-favorable-dwell-ownership.md`
- `lure-response-proposal-c-erratic-state-trigger.md`
- `lure-response-proposal-c-escape-feature-routing.md`
- `lure-response-proposal-c-state-trigger-budget.md`
- `lure-response-proposal-c-state-trigger-ownership.md`
- `lure-response-proposal-c-end-to-end-ordering.md`
- `lure-response-proposal-c-prey-support-bridge.md`
- `lure-response-proposal-c-support-retention-projection.md`
- `lure-response-proposal-c-candidate-bridge-closure.md`

清理前 Proposal C 全文继续保存在 archive，用于考古，不回流成当前规则。
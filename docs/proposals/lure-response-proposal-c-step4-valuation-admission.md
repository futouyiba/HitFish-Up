# 方案 C｜Step 4 Valuation Admission Attack

日期：2026-10-26  
状态：Working Probe，非 Current，非生产参数。

## 1. 问题

经过前面的 dependency / double-count audit，pause / state 相关效应已经优先路由到既有 owner：

- attention continuity → Perception / bounded history；
- trajectory / prediction break → transient task / prediction state；
- favorable dwell / attack window → temporal support / exposure；
- capture geometry consequence → TaskDemand / TaskAffordance。

因此真正还值得竞争“独立 Feeding-mode Valuation 自由度”的候选只剩两类：

1. temporal cadence motif；
2. imbalance-like vulnerability interpretation。

这轮目标不是证明它们无效，而是判断它们目前是否已经买到了足够独立的表达能力，可以获得独立 valuation DOF。

可执行 probe：`../../prototypes/lure-response/proposal_c_step4_valuation_admission_probe.py`。

## 2. Admission gate

独立 Valuation mechanism 至少同时满足：

1. **Named semantic scope**：不是匿名 `stateBonus`；
2. **Provenance**：知道这条机制为什么存在、证据来自哪里；
3. **Existing-route independence**：不能只是 Perception / TaskDemand / dwell / Motivation 的重复投影；
4. **Controlled residual reversal**：控制其它 owner 后，仍能稳定产生 ranking difference；
5. **Player-learnable**：差异能形成玩家可学习、可利用的策略，而不是不可解释噪声。

不满足时可以保留 Candidate，但不能获得独立 coefficient / scalar freedom。

## 3. Cadence motif

### 当前证据

钓鱼实践材料大量认为 cadence、jerk-pause、walk-pause、停顿时长有时会改变咬口。这说明 temporal motif 是合理候选。

但这些材料通常没有控制：

- 当前速度；
- 注意是否已被前序运动刷新；
- trajectory prediction 是否被打断；
- 停在 favorable attack geometry 的时间；
- fish-side motivation。

因此目前不能证明：

```text
same prey support
+ same perception/history support
+ same TaskDemand / TaskAffordance
+ same dwell/support
+ same Feeding Motivation
+ different cadence motif
→ stable residual valuation reversal
```

### 当前裁决

`CandidateUnresolved`

不能 admission：

- `PauseBonus`；
- `CadenceCoeff`；
- `recent_move_then_pause` 通用加成。

未来只有在 controlled holdout 中证明 residual effect，才允许 cadence motif 晋升为独立 Feeding-mode Valuation。

## 4. Imbalance-like vulnerability

### 当前证据

一般 predator-prey ecology 支持“受伤或防御能力下降的 prey 可能更容易被捕食”这一方向，但综述也指出，捕食者主动偏好 wounded / vulnerable prey 这一常见假设实际上被正式测试得并不充分。

对当前 Proposal C 更关键的是：这些证据没有证明大口黑鲈会把某种路亚的 roll / imbalance cue 稳定解释为 vulnerable prey。

而且物理后果必须先拆走：

```text
roll / imbalance
├─ actual trajectory / strike-geometry consequence
│  → Maneuver / Capture-Geometry Demand
│
└─ cue-only interpretation
   → vulnerability Candidate
```

只有第二条才有资格参与本轮 valuation admission。

### 当前裁决

`CandidateUnresolved`

不能 admission：

- `VulnerabilityBonus`；
- `InjuredPreyCoeff`；
- `roll -> injured -> easier -> +response`。

需要的未来 holdout 是：物理轨迹、capture geometry、prey support、Perception、TaskDemand、dwell、Motivation 均保持一致，仅改变可被鱼感知的 vulnerability cue，并观察是否出现稳定、可复现、玩家可学习的 ranking reversal。

## 5. 当前 Step 4 最小结构

```text
ActualPresentation / prey interpretation
        ↓
Perception / Target Interpretation
        ↓
ResolvedTaskDemand
├─ Intercept / Closing Demand
└─ Maneuver / Capture-Geometry Demand
        ↓
TaskAffordance

同时：
Fish-side Feeding Motivation
+ Target value
+ [optional admitted valuation mechanisms]
        ↓
Feeding-mode Valuation
```

目前 `[optional admitted valuation mechanisms]` 可以为空。

这很重要：Step 4 不需要为了结构对称而强行拥有一个 state valuation scalar。

## 6. 当前 admission 状态

| 候选 | 当前状态 | 原因 |
|---|---|---|
| Intercept / Closing Demand | Admitted Working | 能独立购买 feasibility reversal |
| Maneuver / Capture-Geometry Demand | Admitted Working | intercept 固定时仍能独立改变 Affordance |
| attention continuity | Existing owner | Perception / bounded history |
| prediction break | Existing owner | transient task / prediction state |
| favorable dwell | Existing owner | temporal support / exposure |
| cadence motif | CandidateUnresolved | 缺 controlled residual reversal |
| imbalance-like vulnerability | CandidateUnresolved | 缺 LMB-lure-specific residual evidence |
| generic stateBonus | Rejected | 无明确因果 scope，易重复计权 |

## 7. 外部证据边界

大口黑鲈捕获研究支持以下结构性事实：

- 捕获依赖 locomotor positioning；
- sensory pre-strike information 会改变 ram / suction 与 approach kinematics；
- 环境流速变化时，大口黑鲈会调整 prey-capture kinematics；
- 因而 Perception、TaskDemand 与 FunctionalCapacity 分层是合理的。

这些研究不直接证明 cadence 或 vulnerability 应得到独立 valuation coefficient。

参考入口：

- Higham 2007, *Feeding, fins and braking maneuvers: locomotion during prey capture in centrarchid fishes*, PMID 17170154.
- Gardiner & Motta 2012, *Largemouth bass switch feeding modalities in response to sensory deprivation*, PMID 22285791.
- Feeding in Flow 2026, *Environmental Flow Conditions Alter Prey Capture Kinematics in Fish*, PMID 42868420.
- Integrative biology of injury in animals, PMCID PMC10087827.

## 8. 下一步

不要继续发明新的 valuation labels。

下一步应当二选一：

1. 寻找或设计足够严格的 cadence controlled holdout；
2. 寻找或设计 cue-only vulnerability controlled holdout。

如果两者都无法获得 residual reversal，Step 4 可以接受“当前没有独立 presentation-state valuation mechanism”，直接让最终 response 由 Target / Perception、TaskAffordance、fish-side Motivation 等已有语义闭合。

# Proposal C｜语义契约

状态：Working Design / Candidate。本文只定义语义接口，不冻结生产参数或代码结构。

口径来源：`docs/lure-response-joint-evaluation` 的 Working Closure，按 `311ae70d` 快照核对；该分支在此之后持续更新，本轮未逐条重新纳入。与旧 10-27 入口不一致处，以本文列出的来源文档为准。

## 1. 通用状态协议

`ResolutionIncomplete` 是归约器对未能形成最终标量的外层输出，不是每个原子输入事实都必须携带的状态。

| 状态 | 含义 | 可否当作数值 |
|---|---|---|
| `Unknown` | 必要事实缺失，结果可能改变 | 否 |
| `NotConfigured` | 规则、owner 或适用配置不存在 | 否 |
| `NoMatch` | 适用规则已检查，但没有命中 | 只有规则明确提供数值结果时 |
| `ResolvedNonResponsive` | 输入完整，结果为零响应 | 是，`0` |
| `ResolvedResponsive` | 输入完整，结果为正响应 | 是，`0 < x <= 1` |
| `Reject` | 类型硬边界 | 作为 typed zero，不进入连续公式 |
| `ResolutionIncomplete` | 归约阶段仍无法形成最终标量 | 否 |

转移规则：

- `Unknown` 或 `NotConfigured` 进入可能改变输出的归约时，输出 `ResolutionIncomplete`；
- `NoMatch` 只在适用规则明确给出数值时转换：数值 `0` → `ResolvedNonResponsive`；正值 → `ResolvedResponsive`；
- 规则只给出非数值的 NoMatch（例如“条件不成立”但没有定义输出值）时，保持 `NoMatch`，由归约器输出 `ResolutionIncomplete`；
- 已解析的数值 `0` 与 `Unknown`、`NotConfigured` 不同；
- `Reject` 直接产生 typed hard zero，不转成普通 `ResolvedNonResponsive`，也不写成超大 cost。

## 2. ActualPresentation

### 输入

- 呈现实例 ID、装配版本和连续段 ID；
- 带时间戳的主体位置、速度或可复算轨迹；
- 环境关系：水面、底部、水流参照；
- 按需提供的局部部件记录；
- 每项事实的单位、参考系、有效时段、来源和解析状态。

### 输出

实际事实，不附带猎物身份、自然程度、捕获难度或奖励。

```text
PresentationFact = {
  value,
  unit,
  reference_frame,
  valid_interval,
  source,
  status
}
```

### 约束

世界速度和相对水体速度分开。近底和水面关系分开。记录缺口不能当作静止、没有动作或零值。

## 3. PreyInterpretation

### 输入

- ActualPresentation 的事实；
- 当前装配的显式证据绑定；
- 每份证据自己的基值、路径、上限和来源。

### 输出

按猎物类型组织的 support，范围 `[0,1]`，允许区间或状态：

```text
PreySupport[type] = value | [lower, upper] | Unknown | NotConfigured | NoMatch
```

### 数值语义

support 不是排序分数，而是 interpretation retention scale（来源：`lure-response-proposal-c-support-scale-contract.md`）：

```text
support = 0    → 该解释不贡献 Feeding response
support = 1    → reference full-support，不衰减
0 < support < 1 → 按同一比例保留该解释的贡献
```

如果某种证据需要非线性压缩、阈值或饱和，在猎物解释层完成，不在 Response 再投影一次。

### 约束

- 同一呈现可以支持多个猎物解释；
- 同一证据重复登记不叠加；
- 同级证据的替代组合取最强值；
- 未覆盖的猎物类型保持 `NotConfigured`，不自动填零；
- 规则完整检查后没有支持，才输出 `NoMatch` 或规则定义的零。

## 4. PreyConditionedState

### 输入

- PreyInterpretation 的结果和证据来源；
- ActualPresentation 的事实和持续记忆；
- 对应猎物类型的状态规则。

### 输出

状态维度、事件和时序关系分开保存：

```text
StateDimension = { name, value, status, evidence, observed_interval }
StateEvent     = { name, start, end, confirmation_time, status, evidence }
```

同时输出攻击触发强度：

```text
TriggerIntensity_p ∈ [0,1]
```

它由 prey-conditioned state interpreter 完成语义判断后给出，不是 raw turn magnitude、burst speed 或 event count（来源：`lure-response-proposal-c-state-trigger-intensity-contract.md`）。

### 约束

- 当前低位移与移动后停留可以同时存在；
- 缺少前史时，当前状态可以已知，前史保持未知；
- 过程事件必须保存顺序、时间和连续性；
- 不用一个窗口平均值替代有序事件；
- 不把状态标签直接转成 bonus、penalty 或猎物身份变化；
- 攻击诱因只表达“已被解释为可接受猎物后，当前状态是否额外促发出手”，不承载领地、护巢、烦躁、调查等非摄食语义（来源：`lure-response-proposal-c-attack-trigger-strategy-contract.md`）。

## 5. FishCondition

### 五个评价项

```text
FoodValue
StateTriggerValue
ClosingCost(theta)
RiskCost
WillingnessThreshold(Motivation)
```

Prediction 不在第一版主体内，作为待证明的局部代价保留。

### 5.1 食物价值

```text
CurrentFoodValue
= clamp(BaseDietAffinity + SizePreferenceAdjustment + DietaryShiftDelta, 0, 1)
```

- `Reject` 是连续轴外的 typed hard boundary；
- `Poor=0` 是合法连续值；
- FoodValue 与 Motivation 分开。

### 5.2 攻击诱因

```text
StateTriggerValue_p
= TriggerBudget × TriggerIntensity_p

TriggerBudget ≈ 0.10 ~ 0.15   # Working effect-size budget
```

Response 不再对原始轨迹特征做第二套 Trigger 解释。

### 5.3 摄食意愿

```text
M <= 0.80:
    threshold = 0.60 - 0.40 * M

M > 0.80:
    threshold = 0.60 - 0.40 * M - 0.50 * (M - 0.80)
```

- `M=0.5` 时 threshold 仍锚定 `Marginal=0.40`；
- 普通区间保持基准斜率 `0.40`；
- 只有极高 Motivation 进入额外 tail relief，让 Poor 出现窄弱响应窗口，而不压垮中低 Motivation 的 Good（来源：`lure-response-proposal-c-poor-reject-separation.md`，提交 `d656e938`）。

旧 `K_mot=0.60` 的全轴调整已被撤回复。`Reject` 任何情况下不复活。

### 5.4 追赶负担

```text
q = horizontal lure speed relative to water / InterceptSpeedLimit
u_close(theta) = max(0, q * cos(theta))

ClosingCost(theta) = K_close * u_close(theta)^2 * ActivityCostMultiplier(Activity)
```

- `InterceptSpeedLimit` 只表达鱼种 / size cohort 的追赶能力，不受 Activity 修改；
- Activity 表达“愿意为追赶付出多少行为代价”，只调制负担倍率（来源：`lure-response-proposal-c-activity-closing-cost-contract.md`、`lure-response-proposal-c-activity-motivation-separation.md`）；
- Activity 与 FeedingMotivation 是两个正交问题，不能都退化成“鱼现在积极不积极”；
- `u_close >= 1 → hard-zero` 已撤回；
- Closing 只解释“当前运动是否把已有机会沿径向带离鱼”，不单独承担完整高速惩罚（来源：`lure-response-proposal-c-soft-closing-fast-burst-regression.md`）；
- 垂直运动不进入 `u_close`；它按候选归属交给 Spatial / Opportunity 的垂直可交互窗口处理。该 seam 的正式 owner 尚未落仓，见[开放决策](lure-response-proposal-c-open-decisions.md)（来源：`lure-response-proposal-c-vertical-motion-ownership.md`）。

### 5.5 风险顾虑

```text
RiskCost = K_wary * Wariness * SuspicionLoad
```

`SuspicionLoad` 只能来自具名、独立拥有的风险线索。禁止 `1 - prey_support`、高速、频繁转向自动生成 SuspicionLoad。

## 6. DecisionMargin

```text
DecisionMargin(theta)
= CurrentFoodValue
+ StateTriggerValue
- ClosingCost(theta)
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

若未来证明 Prediction 能产生独立策略排序，再作为额外负项加入；当前不加入主体。

### 可补偿性

加法表达的是“同一出手余量标尺上的可补偿关系”（来源：`lure-response-proposal-c-decision-margin-compensability.md`）：

- 正向 soft evidence：FoodValue、StateTriggerValue；
- 负向 soft burden：ClosingCost、RiskCost，可被足够高的价值、触发或 Motivation 部分补偿；
- Motivation 不是奖励项，而是移动门槛。

不可补偿语义必须在进入 Margin 前处理：

- `Reject` → typed zero；
- `Unknown / NotConfigured` → `ResolutionIncomplete`，不输出标量；
- 未来若拿到合法的 encounter geometry / reaction-window contract，可引入 `HardInterceptionInfeasible` typed zero，但不能用超大 ClosingCost 冒充。

## 7. ConditionalResponse

```text
C(Margin) = clamp((Margin - M0) / (M1 - M0), 0, 1)

Working: M0 = 0.00, M1 = 0.40
```

来源：`lure-response-proposal-c-margin-response-projection.md`（提交 `5af7515b`）。旧 `M1=0.30` 已被取代。

```text
Margin <= 0    → ResolvedNonResponsive, C = 0
0 < Margin     → 0 < C <= 1
```

约束：

- `ResolutionIncomplete` 不进入投影；
- 先在每个 latent bearing 计算，再聚合；
- 不能先平均 Margin 再投影；
- 不能先平均 Margin 再加 time bonus。

## 8. PreyModeResponse

同一 Feeding route 的 sibling alternatives 使用有界部分解析（来源：`lure-response-proposal-c-sibling-partial-resolution.md`）：

```text
每条 sibling path 携带区间：C_i ∈ [L_i, U_i]

L_feed = max_i(L_i)
U_feed = max_i(U_i)
```

- `L_feed == U_feed` 时才输出最终标量；
- 否则保持 `ResolutionIncomplete`，携带 `response_bounds`，不可进入 roll；
- `Unknown` 不等于 0，也不因为有已解析 sibling 就直接忽略未解析路径；
- 已解析 sibling 可以把区间压缩，不能凭空填满。

## 9. Opportunity join

来源：`lure-response-proposal-c-opportunity-integration-closure.md`。

第一版不在 Response 内新增连续 `ExposureRate(t)`，也不由 Response 按持续时间积分。职责拆分为：

```text
姿态颗粒 / semantic presentation grain
→ Response：计算该颗粒的 conditional response C

姿态颗粒 → Opportunity / Spatial：计算该颗粒的 native opportunity support L

Candidate join
→ q = L × C
→ Opportunity Reduce
→ NativeCandidateSnapshot
```

- `L × C` 只乘一次，Candidate 后段不重复乘 Response；
- 时间、停留、穿越有效区域、覆盖范围不进入出手余量；
- 垂直运动通过“多久处在可交互垂直区域”影响 `L`；该窗口的具体输出形态与正式 owner 由 Opportunity / Spatial 侧决定，当前尚未落仓，属候选边界；
- 若既有 Candidate pipeline 已把 `L` 定义为 opportunity 侧的量，复用该量，不另造第二个 Exposure multiplier。

## 10. CandidateRetention

Candidate owner 接收 Opportunity Reduce 的结果，生成 native contribution。Proposal C 不重新定义生产 reducer，也不把 Candidate 结果反写成上游响应。

## 11. 证据追溯

每个数值、区间或状态至少能追溯到：

```text
source fact
→ rule or path
→ intermediate result
→ output status/value
```

没有可追溯证据的数值只能作为设计假设，不能写成已验证事实。

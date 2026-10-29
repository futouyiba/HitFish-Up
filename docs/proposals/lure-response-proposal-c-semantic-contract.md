# Proposal C｜语义契约

状态：Working Design / Candidate。本文只定义语义接口，不冻结生产参数或代码结构。

## 1. 通用输入状态

所有层都使用以下输入状态。`ResolutionIncomplete` 是归约器对未能形成最终标量的外层输出，不是每个原子输入事实都必须携带的状态。

| 状态 | 含义 | 可否当作数值 |
|---|---|---|
| `Unknown` | 必要事实缺失，结果可能改变 | 否 |
| `NotConfigured` | 规则、owner 或适用配置不存在 | 否 |
| `NoMatch` | 适用规则已检查，但没有命中 | 只有规则明确提供数值结果时 |
| `ResolvedNonResponsive` | 输入完整，结果为零响应 | 是，`0` |
| `ResolvedResponsive` | 输入完整，结果为正响应 | 是，`0 < x <= 1` |
| `Reject` | 类型硬边界 | 作为 typed zero，不进入连续公式 |
| `ResolutionIncomplete` | 归约阶段仍无法形成最终标量 | 否 |

状态转移规则：

- `Unknown` 或 `NotConfigured` 进入可能改变输出的归约时，输出 `ResolutionIncomplete`；
- `NoMatch` 只有在适用规则明确给出数值零或其他数值结果时，才转为对应的 `ResolvedNonResponsive` 或数值结果；否则保持非数值状态并由归约器输出 `ResolutionIncomplete`；
- 已解析的数值 `0` 与 `Unknown`、`NotConfigured` 不同；
- `Reject` 直接产生 typed hard zero，不转成普通 `ResolvedNonResponsive`。

## 2. ActualPresentation

### 输入

- 呈现实例 ID、装配版本和连续段 ID；
- 带时间戳的主体位置、速度或可复算轨迹；
- 环境关系，例如水面、底部和水流参照；
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

按猎物类型组织的支持值或支持区间：

```text
PreySupport[type] = value | [lower, upper] | Unknown | NotConfigured | NoMatch
```

支持值表示当前事实支持该解释的程度。它不是概率，也不要求各类型相加为 1。

### 约束

- 同一呈现可以支持多个猎物解释；
- 同一证据重复登记不叠加；
- 同级证据的替代组合可取最强值，但不规定后续响应也取最大值；
- `NoMatch` 只有在适用规则已完整检查且规则明确返回零时，才能作为 `ResolvedNonResponsive` 进入连续响应；
- 未覆盖的猎物类型保持 `NotConfigured`，不自动填零；
- 已配置且规则完整检查后没有支持，才可输出 `NoMatch` 或规则定义的零。

## 4. PreyConditionedState

### 输入

- PreyInterpretation 的支持结果和证据来源；
- ActualPresentation 的事实和持续记忆；
- 对应猎物类型的状态规则。

### 输出

状态维度、事件和时序关系分开保存：

```text
StateDimension = {
  name,
  value,
  status,
  evidence,
  observed_interval
}

StateEvent = {
  name,
  start,
  end,
  confirmation_time,
  status,
  evidence
}
```

示例状态包括水面、近底、移动、低位移、上升、下落、移动后停留和失衡样下沉。状态名称不自动代表生物原因。

### 约束

- 当前低位移与移动后停留可以同时存在；
- 缺少前史时，当前状态可以已知，前史保持未知；
- 过程事件必须保存顺序、时间和连续性；
- 不用一个窗口平均值替代有序事件；
- 不把状态标签直接转成 bonus、penalty 或猎物身份变化。

## 5. FishCondition

### 输入

- 已解析的 CurrentFoodValue 或 typed `Reject`；
- FeedingMotivation；
- StateTriggerValue；
- ClosingCost、PredictionCost、RiskCost；
- 这些量的来源、适用范围和解析状态。

### 输出

每个量先保留自己的语义和状态，再形成 `DecisionMargin`：

```text
DecisionMargin(theta)
= CurrentFoodValue
+ StateTriggerValue
- ClosingCost(theta)
- PredictionCost
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

只有所有必需输入已解析时，才输出数值 `DecisionMargin`。任一未知输入可能改变结果时，输出 `ResolutionIncomplete`。

### 约束

- FoodValue 与 FeedingMotivation 分开；
- Activity 只影响 soft Closing cost，不降低 `InterceptSpeedLimit`；
- sudden turn 可以同时提供 StateTriggerValue 和 PredictionCost，但不能产生第三个匿名作用；
- high speed、low prey support 和 pause 不自动生成 SuspicionLoad；
- `Reject` 不能被 Motivation、Trigger 或 DietaryShift 复活。

## 6. ConditionalResponse

### 输入

已解析的 `DecisionMargin(theta)`，以及本轮采用的 projection anchors。

### 输出

```text
C(theta) = clamp((Margin(theta) - M0) / (M1 - M0), 0, 1)
```

`M0` 和 `M1` 是 calibration anchors，不是物理常数或生产批准值。

### 约束

- `ResolutionIncomplete` 不进入 projection；
- 已解析不响应输出 `C=0`；
- 已解析响应输出 `0<C<=1`；
- 先在每个 latent bearing 计算，再聚合；
- 不能先平均 Margin 再投影。

## 7. PreyModeResponse

对同一 Feeding route 的 sibling alternatives，可以使用替代聚合：

```text
C_prey = prey_support × E_theta[C(theta)]
C_feed = max(sibling prey responses)
```

但 Unknown sibling 必须使用上下界：

```text
known_lower_bound = max(known resolved sibling responses)
possible_upper_bound = max(
  known_lower_bound,
  unresolved siblings' allowed upper bounds
)
```

只有未解析路径不可能改变 winner，或上下界收敛时，才输出最终 scalar；否则保持 `ResolutionIncomplete`。这一规则仍是 Working seam，不是 production aggregation contract。

只有同一 `presentation_segment_id`、同一局部机会窗口和同一 Feeding route 的 sibling alternatives 才能进入同一次 sibling 聚合。机会记录由 TemporalOpportunity owner 创建和去重；PreyModeResponse 只提供聚合输入，不为每个猎物解释各自创建独立机会。

机会去重发生在 sibling 聚合之后、Candidate retention 之前：PreyModeResponse 先把同一路径的 sibling responses 收敛成一个 `C_feed`，再由 TemporalOpportunity owner 用 opportunity key 创建或复用一条机会记录。
## 8. TemporalOpportunity

### 输入

- 已解析的瞬时 `C(t)`；
- opportunity owner 提供的 exposure；
- 明确的时间窗口、局部范围、单位和连续性。

### 输出

```text
instantaneous response C(t)
× temporal / local opportunity exposure
→ accumulated opportunity
→ Candidate retention
```

### 约束

- 未配置或无法解析的 exposure 不能当作零曝光；
- 已解析的零曝光才表示没有机会；
- 归约器必须明确按事件窗口或采样时段累积；
- 不把停留时长直接放进 `DecisionMargin`；
- Candidate 后段不得再次乘 Response。

## 9. CandidateRetention

Candidate owner 接收 Opportunity Reduce 的结果，并生成 native contribution。Proposal C 不重新定义 Candidate 的生产 reducer，也不把 Candidate 结果反写成上游响应。

## 10. 证据追溯

每个数值、区间或状态至少能追溯到：

```text
source fact
→ rule or path
→ intermediate result
→ output status/value
```

没有可追溯证据的数值只能作为设计假设，不能写成已验证事实。

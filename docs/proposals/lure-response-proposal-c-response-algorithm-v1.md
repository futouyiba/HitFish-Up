# Proposal C｜响应（Response）端到端算法 v1（Candidate）

状态：Working Algorithm / Candidate。把已收口的各层写成一条可执行规格；不引入新机制，不冻结生产参数。本版是会议回写前的 Working 状态（逐 latent bearing 投影、有界 sibling 部分解析）；2026-10-30 会议方向（去掉 θ、sibling 取 max、一竿一 Snapshot）尚未回写，见[会议对齐稿](../alignment/lure-response/2026-10-30-lure-response-alignment-draft.md)。回写并复审前，本规格是实现与 probe 的算法基线。

来源：设计骨架、语义契约、呈现解释与状态契约、五评价项契约、响应与机会契约、第一轮闭合审查、Fish Condition Production Contract。

## 1. 输入与不变量

输入：

```text
PresentationSegment   轨迹、时间、环境关系、局部记录
AssemblySnapshot      证据绑定与适用标记
FishCondition         resolved baseline（可选授权 overlay）
OpportunityFacts      L 及其状态
WorkingParams         K_close、TriggerBudget、M0/M1、tail 参数
```

不变量：

1. 先按 latent bearing 算成本与 Margin，再投影，最后聚合；不能先平均 Margin。
2. 支持度只乘一次；机会量只乘一次，`q = L × C`。
3. `Unknown`、`NotConfigured`、`InvalidInput` 不当作 0；`Reject` 是 typed zero。
4. 过期、越界或缺来源的 Fish Condition 不沿用最后值。
5. 时间、停留、覆盖不进入出手余量。
6. Candidate 后段不再乘 Response。
7. 同一事实可被多层读取，但同一作用只在一个 owner 结算。

## 2. 算法

```text
function response(segment, assembly, fc, opportunity, params):

  # 0. 帧校验
  require segment.valid and assembly.version == segment.assemblyVersion
  require fc.version matches segment, fc.validity covers segment.time
  if not satisfied: return ResolutionIncomplete

  # 1. 猎物解释
  supports = interpret(segment, assembly)      # per family: value | [L,U] | status
  if supports covers no family: return NotApplicable

  # 2. 每个 sibling family
  for family in declaredSiblingSet:
      relation = targetRelation(segment, family)   # 目标关系按 family 求值
      if relation == Reject:
          interval[family] = (Reject, 0.0, 0.0)    # typed hard zero，不再计算
          continue
      support = supports[family]

      if support == Reject:
          interval[family] = (Reject, 0.0, 0.0)
          continue
      if support == NoMatch:
          if ruleReturnsNumber(family):
              v = ruleValue(family)
              interval[family] = (Resolved, v, v)
          else:
              interval[family] = (ResolutionIncomplete, 0.0, 1.0)
          continue
      if support == Unknown:
          lo, hi = knownSupportBounds(family)      # 默认 (0,1)，有部分信息就收窄
          interval[family] = (ResolutionIncomplete, lo, hi)
          continue
      if support == InvalidInput:
          interval[family] = (InvalidInput, 0.0, 1.0)
          continue
      if support == NotConfigured:
          interval[family] = (ResolutionIncomplete, 0.0, 1.0)
          continue

      state = extractState(segment, family)        # dims, events, TriggerIntensity
      if state.status == Reject:
          interval[family] = (Reject, 0.0, 0.0)     # typed zero，短路
          continue
      if state.status == InvalidInput:
          interval[family] = (InvalidInput, 0.0, 1.0)
          continue
      if state.status in (Unknown, NotConfigured):
          interval[family] = (ResolutionIncomplete, 0.0, 1.0)
          continue

      if support is an interval:
          interval[family] = responseInterval(support, state, fc, params)
          continue

      C_cond = evaluate(state, fc, params)         # 已解析输入下的条件响应
      if C_cond == Reject:
          interval[family] = (Reject, 0.0, 0.0)
          continue
      if C_cond == InvalidInput:
          interval[family] = (InvalidInput, 0.0, 1.0)
          continue
      if C_cond is Unknown / NotConfigured:
          interval[family] = (ResolutionIncomplete, 0.0, 1.0)
          continue

      C_f = support.value * C_cond
      interval[family] = (Resolved, C_f, C_f)

  # 3. sibling 组成
  (status, L_feed, U_feed) = compose(interval)
  if status != Resolved:
      return (status, (L_feed, U_feed))   # response_bounds；status 可为 RI 或 InvalidInput

  # 4. 机会接入
  if opportunity.L == InvalidInput: return InvalidInput
  if opportunity.L in (Unknown, NotConfigured): return ResolutionIncomplete
  q = opportunity.L * L_feed
  return (Resolved, q)


function compose(interval):
  # Reject 分支按 (0,0) 参与 max；Unresolved 分支用已知边界参与
  L_feed = max(branch.lower for branch in interval)
  U_feed = max(branch.upper for branch in interval)
  if any(branch.status == InvalidInput for branch in interval):
      return (InvalidInput, L_feed, U_feed)
  if L_feed == U_feed: return (Resolved, L_feed, U_feed)
  return (ResolutionIncomplete, L_feed, U_feed)


function evaluate(state, fc, params):

  # Returns a resolved conditional response, or a non-numeric status.
  food      = clamp(base + size + dietShift, 0, 1)
  trigger   = params.TriggerBudget * state.TriggerIntensity
  risk      = params.K_wary * fc.wariness * suspicionLoad      # 无 cue 时为 0
  threshold = f(fc.feedingMotivation)                          # 分段线性 + tail

  # 逐 latent bearing：先算 Margin，再投影，最后聚合
  for each latent bearing theta:
      closing(theta) = params.K_close * u_close(theta)^2 * activityMultiplier(fc.activity)
      margin(theta)  = food + trigger - closing(theta) - risk - threshold
      C(theta)       = clamp((margin(theta) - params.M0) / (params.M1 - params.M0), 0, 1)

  return E_theta[C(theta)]        # C_conditional；不能先平均 Margin 再投影


function responseInterval([a, b], state, fc, params):
  C_cond = evaluate(state, fc, params)     # 以 support=1 计算条件响应
  if C_cond == Reject: return (Reject, 0.0, 0.0)
  if C_cond is Unknown / NotConfigured / InvalidInput:
      return (C_cond, 0.0, 1.0)
  return (ResolutionIncomplete, a * C_cond, b * C_cond)   # 不提前取中点；收敛由 compose 判定
```

### 2.1 各步状态

| 步骤 | 可返回 |
|---|---|
| 帧校验 | `ResolutionIncomplete` |
| 猎物解释 | 数值 / 区间 / `Unknown` / `NotConfigured` / `NoMatch` |
| 状态提取 | 状态维度、事件、`TriggerIntensity`；非数值状态向上传播 |
| 评价 | 五项各自状态；`Reject` 单独处理 |
| 投影 | 数值 `C(theta)`；不输出非数值 |
| sibling 组成 | 标量或 `ResolutionIncomplete` + bounds |
| 机会接入 | 标量 `q` 或 `ResolutionIncomplete` |

## 3. 状态代数

```text
Reject            → typed zero，不进入连续公式
Unknown           → 需要的下游步骤转 ResolutionIncomplete
NotConfigured     → 同上，且不当作 NoMatch
NoMatch           → 只有规则明确给数值时才转 Resolved
NotApplicable     → 该 family 不在本次评价范围，不制造 Unknown
InvalidInput      → 配置或输入错误，不可 roll
ResolvedNonResponsive → C=0
ResolvedResponsive    → 0<C<=1
```

聚合优先级（同一分支内）：

```text
Reject > InvalidInput > NotConfigured > Unknown > Resolved
```

- 同一分支出现 `Reject`（target relation、support、state 或评价项）时按 typed zero 短路，不再检查该分支其余输入；
- sibling 之间不做优先级合并：各自映射为区间后取 max；
- `NotApplicable` 的 family 不进入 sibling set，也不制造 `Unknown`；
- 任何数值输入为 NaN / Infinity 时按 `InvalidInput` 处理，不进入 `clamp`。

### 失败对照

| 情况 | 结果 |
|---|---|
| Activity 非有限或为负 | 该分支 `InvalidInput`，不可 roll |
| Motivation 缺失 | `ResolutionIncomplete`，不回填 0.5 |
| Wariness 缺失且存在 cue | `ResolutionIncomplete` |
| Wariness 缺失且无 cue | `RiskCost=0` |
| DietShift[family] 缺失 | 该 family 的 FoodValue 不可闭合 |
| TriggerIntensity 缺失 | `ResolutionIncomplete` |
| support 为区间 | 进入 sibling 区间，不提前取中点 |
| `L` 缺失 | `ResolutionIncomplete`，不是零机会 |

## 4. 计算追溯

输入：

```text
support = 1.0
FoodValue = 0.70
TriggerIntensity = 0.80 → StateTriggerValue = 0.08
Activity multiplier = 1.0
q = 0.40
RiskCost = 0
Motivation = 0.50 → threshold = 0.40
M0 = 0, M1 = 0.40
```

逐 bearing 算成本与 Margin，投影后取平均：

```text
C_conditional = 0.874
C_prey        = 1.0 × 0.874 = 0.874
```

若 `L = 0.50`：

```text
q = 0.50 × 0.874 = 0.437
```

只乘一次；Candidate 后段不再乘 Response。

## 5. 可执行入口

- `prototypes/lure-response/proposal_c_end_to_end_probe.py`：跑通 happy path、Unknown Activity、Reject、Unknown support、sibling 收敛 / 未收敛、`L` 缺失与单次乘法。
- 各形状 probe：投影、Closing、Trigger、support retention、机会量。

## 6. 未闭口

- 各 Condition 的生成语义与标定；
- 事件提取的滤波、采样与阈值；
- `L` 的生产函数与窗口口径；
- 真实 encounter geometry 是否引入 hard gate；
- 生产参数：`K_close`、Trigger budget、`K_wary`、`M0/M1`、tail 参数。

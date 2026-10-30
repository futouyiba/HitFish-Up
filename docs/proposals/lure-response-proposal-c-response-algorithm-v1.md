# Proposal C｜响应（Response）端到端算法 v1（Candidate）

状态：Working Algorithm / Candidate。把已收口的各层写成一条可执行规格；不引入新机制，不冻结生产参数。已按 2026-10-30 会议方向回写：不模拟相对方位 θ、同级猎物解释取最大值、Fish Condition 一竿一个快照。会议记录见[会议对齐稿](../alignment/lure-response/2026-10-30-lure-response-alignment-draft.md)，回写后的实现基线即本规格与 probe。

来源：设计骨架、语义契约、呈现解释与状态契约、五评价项契约、响应与机会契约、第一轮闭合审查、Fish Condition Production Contract。

## 1. 输入与不变量

输入：

```text
PresentationSegment   轨迹、时间、环境关系、局部记录
AssemblySnapshot      证据绑定与适用标记
CastFishCondition     抛竿时形成的鱼况快照（可选授权 overlay）
OpportunityFacts      L 及其状态
WorkingParams         K_close、TriggerBudget、M0/M1、tail 参数
```

不变量：

1. 单方向算成本与 Margin，再投影为 `C`；不跨方位平均，也不先平均 Margin。
2. 支持度只乘一次；机会量只乘一次，`q = L × C`。
3. `Unknown`、`NotConfigured`、`InvalidInput` 不当作 0；`Reject` 是 typed zero。
4. Fish Condition 在抛竿时形成快照，整竿内沿用；形成快照时过期、越界或缺来源的值不沿用旧值。
5. 时间、停留、覆盖不进入出手余量。
6. Candidate 后段不再乘 Response。
7. 同一事实可被多层读取，但同一作用只在一个 owner 结算。
8. 同级猎物解释取最大值；未解析分支跳过并记录，不当作 0。

## 2. 算法

```text
function response(segment, assembly, fc, opportunity, params):

  # 0. 帧校验
  require segment.valid and assembly.version == segment.assemblyVersion
  require castFC.snapshotId and castFC.castId == segment.castId   # 一竿一个快照
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
          results[family] = (Reject, 0.0)
          continue
      if support == NoMatch:
          if ruleReturnsNumber(family):
              results[family] = (Resolved, ruleValue(family))
          else:
              results[family] = (ResolutionIncomplete, None)
          continue
      if support == Unknown:
          results[family] = (ResolutionIncomplete, None)
          continue
      if support == InvalidInput:
          results[family] = (InvalidInput, None)
          continue
      if support == NotConfigured:
          results[family] = (ResolutionIncomplete, None)
          continue

      state = extractState(segment, family)        # dims, events, TriggerIntensity
      if state.status == Reject:
          results[family] = (Reject, 0.0)
          continue
      if state.status == InvalidInput:
          results[family] = (InvalidInput, None)
          continue
      if state.status in (Unknown, NotConfigured):
          results[family] = (ResolutionIncomplete, None)
          continue

      C_cond = evaluate(state, castFC, params)     # 已解析输入下的条件响应
      if C_cond == Reject:
          results[family] = (Reject, 0.0)
          continue
      if C_cond == InvalidInput:
          results[family] = (InvalidInput, None)
          continue
      if C_cond is Unknown / NotConfigured:
          results[family] = (ResolutionIncomplete, None)
          continue

      results[family] = (Resolved, support.value * C_cond)

  # 3. sibling 组成：取最大值
  (status, C_feed, skipped) = compose(results)
  if status != Resolved:
      return status                     # RI 或 InvalidInput

  # 4. 机会接入
  if opportunity.L == InvalidInput: return InvalidInput
  if opportunity.L in (Unknown, NotConfigured): return ResolutionIncomplete
  q = opportunity.L * C_feed
  return (Resolved, q)


function compose(results):
  # Reject 贡献 0；未解析分支跳过并记录；InvalidInput 阻断；没有已解析分支 -> RI
  resolved = [value for (status, value) in results if status == Resolved]
  resolved += [0.0 for (status, value) in results if status == Reject]
  skipped  = [family for family, (status, _) in results
              if status in (ResolutionIncomplete, Unknown, NotConfigured)]
  if any(status == InvalidInput for (status, _) in results):
      return (InvalidInput, None, skipped)
  if not resolved:
      return (ResolutionIncomplete, None, skipped)
  return (Resolved, max(resolved), skipped)


function evaluate(state, fc, params):

  # Returns a resolved conditional response, or a non-numeric status.
  food      = clamp(base + size + dietShift, 0, 1)
  trigger   = params.TriggerBudget * state.TriggerIntensity
  closing   = params.K_close * state.q^2 * activityMultiplier(fc.activity)   # 单方向：鱼在追拟饵
  risk      = params.K_wary * fc.wariness * suspicionLoad      # 无 cue 时为 0
  threshold = f(fc.feedingMotivation)                          # 分段线性 + tail

  margin = food + trigger - closing - risk - threshold
  return clamp((margin - params.M0) / (params.M1 - params.M0), 0, 1)   # C
```

### 2.1 各步状态

| 步骤 | 可返回 |
|---|---|
| 帧校验 | `ResolutionIncomplete`（含快照缺失或错竿） |
| 猎物解释 | 数值 / `Unknown` / `NotConfigured` / `NoMatch` |
| 状态提取 | 状态维度、事件、`TriggerIntensity`；非数值状态向上传播 |
| 评价 | 五项各自状态；`Reject` 单独处理 |
| 投影 | 数值 `C`；不输出非数值 |
| sibling 组成 | 标量（max）或 `ResolutionIncomplete` |
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
- sibling 之间不做优先级合并：已解析分支取 max，未解析分支跳过并记录 provenance；
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
| support 未收敛为标量 | 该分支 `ResolutionIncomplete`，跳过并记录 |
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

单方向算成本与 Margin，再投影（Working `K_close = 0.19`，单方向标尺）：

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

- `prototypes/lure-response/proposal_c_end_to_end_probe.py`：跑通 happy path、Unknown Activity、Reject、Unknown support、sibling 取最大与未解析跳过、`L` 缺失与单次乘法。
- 各形状 probe：投影、Closing、Trigger、support retention、机会量。

## 6. 未闭口

- 各 Condition 的生成语义与标定；
- 事件提取的滤波、采样与阈值；
- `L` 的生产函数与窗口口径；
- `K_close` 的 no-θ 重标定（Working 0.19，替代方位平均下的 0.76）；
- 真实 encounter geometry 是否引入 hard gate；
- 生产参数：`K_close`、Trigger budget、`K_wary`、`M0/M1`、tail 参数。

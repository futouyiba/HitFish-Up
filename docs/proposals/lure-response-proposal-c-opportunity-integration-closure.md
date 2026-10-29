# Proposal C｜Opportunity Integration Closure

状态：Working Closure / Candidate。不是 Current，也不是生产参数。

本页只闭合 Proposal C 与姿态颗粒 / Opportunity / Candidate 之间的职责边界，不重新定义 Spatial、Candidate 或参考实现。

## 1. 结论

第一版不在 Response 内新增连续 `ExposureRate(t)`。

当前 Working 拆分为：

```text
姿态颗粒 / semantic presentation grain
→ Response：计算该颗粒当前的 conditional captureRetention C

姿态颗粒进入 Opportunity
→ Opportunity：消费 Spatial facts，计算该颗粒对应的 native opportunity support L

Candidate join
→ q = L × C
→ Opportunity Reduce
→ NativeCandidateSnapshot
```

其中：

- `C` 回答：这一次局部呈现机会中，鱼有多大程度会响应；
- `L` 回答：这一颗粒在当前空间、时间和局部可达条件下提供了多少 native opportunity support；
- `L` 的正式 owner 是 Opportunity；Spatial 只提供事实；
- 时间、停留、穿越有效区域、覆盖范围都不进入 `DecisionMargin`；
- Response 不再自行对 `C` 按持续时间积分；
- Candidate 只执行一次 `L × C`，不重复乘 Response。

## 2. 为什么撤回 Response-owned ExposureRate

此前 Candidate 草案曾写：

```text
C(t)
× ExposureRate(t)
→ OpportunityIntensity(t)
→ integrate over time
```

这个表达作为数学直觉可以解释“更长暴露带来更多机会”，但不适合作为 Response 的新 production owner。

最新参考实现证据显示，Opportunity 层已经有独立的语义事件和时间输入：

```text
EntryOpportunity
kind = FIRST_ACCESS | ARRIVAL | SEMANTIC_REEVALUATION
```

并且 `form_proposals()` 显式消费：

```text
accessible_fraction
temporal_factor
entry_grade
```

参考实现还明确把 canonical opportunity id 建立在稳定语义身份上，并排除 runtime callback / tick id。

因此如果 Proposal C 再在 Response 中创建一套按秒积分的 `ExposureRate`，会有两类风险：

1. 与 Opportunity 已有 temporal / accessibility 语义重复计权；
2. 把调用频率、切片粒度或帧率误当成机会数量。

所以第一版只保留一个 seam：Response 输出 `C`，Opportunity 输出 `L` 或等价 native support，Candidate 做一次 retention join。

## 3. 姿态颗粒如何进入 Opportunity

沿用此前姿态颗粒设计，不重新定义其切分规则。

本页只冻结：

> 姿态颗粒是 Response 与 Opportunity 的共同离散求值载体，但“一个 runtime tick”不是“一个新机会”。

因此：

```text
pose grain j
├→ response state / C_i,j
└→ opportunity support L_i,j

q_i,j = L_i,j × C_i,j
```

姿态颗粒必须有稳定语义身份或稳定的 semantic partition。不能仅因为系统多调用一次 evaluator，就生成新的机会。

如果同一颗粒被重算：

```text
same semantic grain
+ same opportunity identity
→ replay / reevaluation
→ 不增加 native opportunity count
```

如果出现真正新的语义颗粒或合法语义触发：

```text
new semantic grain / stable semantic trigger
→ 新的 opportunity support 单元
```

具体 opportunity identity、dedupe 和 reevaluation 仍由 Opportunity Owner 决定。

## 4. 时间与停留的归属

更长停留不能修改：

```text
FoodValue
StateTriggerValue
ClosingCost
RiskCost
WillingnessThreshold
```

但可以影响 Opportunity support。

例如，同样的 Response 状态：

```text
C = 0.6
```

如果姿态颗粒在有效 interaction region 中停留更久：

```text
L_long > L_short
```

于是：

```text
q_long = L_long × 0.6
q_short = L_short × 0.6
```

这保持：

```text
longer dwell
≠ better instantaneous prey value

longer dwell
= more native opportunity support
```

但本页不冻结 `L(duration)` 的生产函数。

## 5. 高速、慢速与 pause 的整链职责

### Slow / Pause

```text
速度下降
→ Closing burden 下降
→ C 可能提高
```

同时：

```text
在有效区域停留更久
→ L 可能提高
```

不再增加第三个：

```text
PauseBonus
DwellBonus
ExposureBonus
```

### Fast / Burst

```text
背离 bearing
→ Closing burden ↑
→ C 下降
```

但：

```text
迎面 / 横切 bearing
→ Closing 不强造 penalty
```

高速的另一部分代价来自：

```text
更快穿过当前有效 interaction region
→ 单个局部机会的 temporal support 下降
→ L 下降
```

同时它也可能：

```text
单位时间覆盖更多空间
→ 遇到更多新的 Spatial facts
→ Opportunity 建立更多新的 opportunity identity / support
```

这是实际空间遍历产生的 Opportunity 结果，不是 FastSearchInformationBonus。

因此最终单位时间效率应由：

```text
Opportunity support L
× Response retention C
→ Candidate q
```

共同决定，Response 单独不能宣称 Fast 一定更差。

## 6. Vertical motion 的统一解释

沿用 vertical ownership closure：

```text
vertical position / rise / fall
→ Opportunity eligibility
→ 是否进入、离开有效垂直机会区域
→ L 的大小 / 有效时间窗口
```

```text
horizontal water-relative motion
→ Closing radial-separation burden
→ C
```

所以 vertical jigging 不需要额外 `VerticalClosingPenalty`，也不需要把 Isotropic2D 强行升级成 3D latent fish position。

## 7. 与现有 Candidate Bridge 的关系

Candidate Bridge 已冻结 Working topology：

```text
Spatial facts
→ Opportunity eligibility / identity / duration / dedupe / reevaluation / reducer
→ native opportunity support L
```

scalar specialization：

```text
q_i,j = L_i,j × C_i,j
W_i^opp = Σ_j α_j · q_i,j
```

本页不新增第二个 temporal multiplier。

如果现有 `L_i,j` 已经包含：

- spatial native support；
- 当前颗粒的 accessibility；
- temporal opportunity support；
- 当前局部机会窗口；

则直接复用 `L_i,j`。

如果生产系统把这些拆成多个 Opportunity-side 中间量，也必须在进入 Candidate join 前合成为同一 native support，不能让 Response 额外再乘一次 duration / exposure。

## 8. 参考实现证据与权威边界

`programaticHitFish` 当前参考实现中：

```text
EntryOpportunity.kind
= FIRST_ACCESS | ARRIVAL | SEMANTIC_REEVALUATION
```

Opportunity ledger 按稳定 semantic identity 去重，并明确排除 runtime callback / tick id。

Proposal formation 使用：

```text
entry_probability
= clamp(accessible_fraction × temporal_factor × grade_probability)
```

这些是实现证据，不自动成为本仓 Current Contract。

它支持的设计判断是：

1. Opportunity 是 `L` 的正式 owner。Spatial 提供位置、区域、几何、垂直层和有效空间窗口等事实；
2. 时间 / accessibility 已经有明确承接位置；
3. 机会 identity 应是语义稳定的，而不是 evaluator 调用次数；
4. Proposal C 不应再创建一套平行的 Response-owned ExposureRate。

正式生产字段名和数学仍需由 Current Opportunity / Candidate Owner 承接。

## 9. 必须保持的 invariants

### 9.1 Tick-rate invariance

```text
相同 semantic presentation
在 30Hz / 60Hz / 120Hz evaluator 下
→ native opportunity expectation 不变
```

### 9.2 Replay invariance

同一 semantic grain 重算不能制造额外机会。

### 9.3 Partition invariance

如果只是工程切片变化、语义呈现没有变化：

```text
1 个连续区间
vs
等价拆成多个内部 runtime chunk
```

最终 native opportunity 不应因为切得更碎而增加。

### 9.4 Response zero invariance

```text
C = 0
→ L × C = 0
```

再长 duration 也不能救活 resolved non-response / Reject。

### 9.5 No double time counting

如果 duration 已经进入 `L` / Opportunity support，则不能再次：

```text
q = L × C × duration
```

除非 `L` 的 Contract 明确不含时间，而且 Opportunity Owner 显式定义另一项 canonical temporal measure。

### 9.6 No double Response

禁止：

```text
L × C
→ W
→ W × C
```

## 10. 仍未闭合

本页没有冻结：

- `L_i,j` 的生产字段名；
- Spatial facts 到 Opportunity identity 的正式映射；
- `temporal_factor` 与 `L_i,j` 是否是一一对应、子项还是旧实现概念；
- pause / slow / fast 下 `L` 的生产曲线；
- spatial coverage 与 local dwell 如何共同形成 native support；
- `α_j` 的生产语义；
- Opportunity Reduce 的最终公式；
- 连续 presentation 何时形成新的 `SEMANTIC_REEVALUATION`。

这些属于 Opportunity / Candidate production contract，不应由 Response 偷偷补造。

## 11. Working 裁定

第一版冻结：

```text
Spatial facts
→ Opportunity
→ 每颗粒输出 native opportunity support L

Candidate
→ q = L × C
→ Opportunity Reduce
```

并撤回：

```text
Response-owned continuous ExposureRate
Response-owned dwell integration
runtime tick = opportunity
```

这使 slow / pause / fast / vertical movement 的系统效果都能分别落到已有 owner，而不重复计权。
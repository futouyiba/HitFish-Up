# Proposal C｜Temporal Exposure / Opportunity Contract

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

Proposal C 当前的 `C(t)` 只表达：

> 在当前这一刻、当前 presentation 条件下，如果存在一次局部 interaction opportunity，鱼的 Feeding response / retention strength 有多高。

它不是整段 presentation 的最终咬口概率，也不拥有持续时间。

第一版把时间维度独立成：

```text
C(t)
× ExposureRate(t)
→ OpportunityIntensity(t)
→ integrate over time
→ OpportunityMass
→ Opportunity Reduce
→ Candidate native retention
```

其中：

- `C(t)`：Response Owner；
- `ExposureRate(t)`：Temporal Exposure / Opportunity Owner；
- `OpportunityMass`：一段 presentation 中累计的有效 Feeding opportunity 量；
- `Opportunity Reduce`：把累计 opportunity 量压缩到 Candidate 可消费的 bounded retention。

因此 duration 不进入 `DecisionMargin`。

## 2. 为什么不能给 DecisionMargin 加 dwell bonus

禁止：

```text
DecisionMargin += K_dwell * dwell_time
```

也禁止：

```text
pause_duration
→ StateTriggerBonus
```

除非 pause duration 本身被 prey-state interpreter 作为具名状态识别的一部分。

原因：

1. `DecisionMargin` 回答“这一次机会值不值得响应”；
2. duration 回答“有多少次机会 / 多长时间暴露”；
3. 把 duration 放进 Margin，会让一条本来很差的 presentation 仅靠停得足够久变成高价值食物；
4. 还会和 Candidate / Opportunity 的时间累计重复计权。

因此：

```text
Longer exposure
≠ better instantaneous prey value

Longer exposure
= more accumulated opportunity
```

## 3. 最小数学拓扑

第一版只需要：

```text
OpportunityIntensity(t)
= C(t) * ExposureRate(t)

OpportunityMass
= ∫ OpportunityIntensity(t) dt
```

这里 `ExposureRate(t)` 的单位应是：

```text
opportunity / second
```

或其它明确、可积分的等价 rate 单位。

`C(t)` 无量纲，范围 `[0,1]`。

因此：

```text
OpportunityMass
```

可理解为该段 presentation 的“有效 opportunity 数量尺度”，但第一版不宣称它是真实独立 Bernoulli 次数。

## 4. Opportunity Reduce

`OpportunityMass` 不能直接当概率。

第一版推荐保持 reducer 可替换，但要求：

```text
OpportunityMass = 0
→ retention = 0

OpportunityMass ↑
→ retention 单调不降

OpportunityMass → ∞
→ retention 有界
```

一个最小 Working candidate 是 Poisson-style saturation：

```text
OpportunityRetention
= 1 - exp(-OpportunityMass)
```

它的好处：

- 小量时近似线性：`retention ≈ OpportunityMass`；
- exposure 越久收益递减；
- 不需要硬 cap；
- 多段 exposure 在强度层面可自然相加。

但这只是 reducer shape candidate，不是 production formula。

如果 Candidate native retention 已有权威 reducer，应由 Candidate Owner 接管，不在 Response 重定义第二套。

## 5. ExposureRate 不由 C 自己生成

Response 不能：

```text
ExposureRate = f(C)
```

否则会把“鱼愿不愿意响应”和“有多少局部接触机会”混成同一个量。

ExposureRate 应由上游 / Opportunity Owner 基于局部 presentation 与候选空间关系生成，例如未来可能消费：

- lure 在有效 candidate 区域内的时间；
- 局部 sweep / covered path；
- spatial support / local abundance；
- mode-specific encounter semantics；
- presentation 是否已离开该候选区域。

但当前仓没有找到 Current Markdown Contract 明确生产这些量，因此这里只冻结 seam，不补造具体公式。

## 6. Pause / slow retrieve 的语义

Pause 和 slow retrieve 的收益现在可以分成两条独立路径：

```text
速度下降
→ ClosingCost 下降
→ C(t) 可能上升
```

以及：

```text
在有效 interaction region 中停留更久
→ ExposureMass 增加
```

这两条可以同时发生，因为它们回答不同问题。

禁止再加：

```text
PauseBonus
DwellBonus
```

否则会第三次奖励同一策略。

## 7. 高速 retrieve 的语义

高速 presentation 可能：

```text
更高速度
→ Closing burden 上升
→ C(t) 降低
```

但与此同时，高速可能覆盖更多空间：

```text
更高 sweep / search coverage
→ ExposureRate 或 candidate coverage 上升
```

因此“快收线一定更差”不能由 Response 单独裁定。

正确的系统层结果可能是：

```text
per-opportunity response 较低
×
单位时间 encounter 较多
```

最终 efficiency 由二者共同决定。

这正是把 Response 与 Opportunity 分开的主要价值。

## 8. 与 Candidate 的关系

当前 Working seam：

```text
presentation / prey interpretation
→ C_i,j(t)

local opportunity process
→ ExposureRate_i,j(t)

q_i,j(t)
= L_i,j(t) * C_i,j(t)
```

如果既有 Candidate pipeline 已把 `L_i,j` 定义为 opportunity / exposure 侧的量，则应复用该量，不再额外创建第二个 Exposure multiplier。

最终：

```text
Opportunity Reduce
→ W_i^opp
→ NativeCandidateSnapshot
→ optional Pre-Roll Gameplay Policy
→ TrueRoll
```

Response 不再在 Candidate 后二次乘 `C`。

## 9. 关键 feature ownership

| 事实 / 语义 | Owner | 禁止重复进入 |
|---|---|---|
| 当前 response strength | `C(t)` / Response | Exposure reducer 不重新解释 prey value |
| presentation 持续时间 | Temporal Exposure | DecisionMargin / FoodValue |
| pause 导致速度下降 | Closing | 额外 PauseBonus |
| pause 导致停留更久 | Exposure | 额外 DwellBonus |
| 高速导致追赶难 | Closing | generic FastPenalty |
| 高速导致覆盖空间更大 | Opportunity / Spatial | Closing 不负责 search coverage |
| prey-state move→pause | State interpreter → StateTrigger | 不自动等于 dwell exposure |

## 10. Typed semantics

如果该 Candidate path 需要 Exposure：

```text
ExposureRate = Unknown
→ ResolutionIncomplete
```

不能默认 0。

如果某种 mode 明确不使用时间累计，可以显式：

```text
ExposureModel = Disabled / NotApplicable
```

但必须由 mode contract 声明，而不是因为缺数据就静默关闭。

`C(t)=0` 是已解析非响应；即使 exposure 很长：

```text
0 * ExposureRate = 0
```

持续时间不能复活零响应。

Reject 同理保持 hard zero。

## 11. 首版 acceptance stories

### Case A：同样的 C，不同持续时间

```text
C = 0.5
ExposureRate 相同
2 秒 exposure > 1 秒 exposure
```

但 `C` 本身不变。

### Case B：Pause

```text
pause
→ ClosingCost ↓
→ C ↑ 或保持

同时
→ 如果仍处于有效 region
→ accumulated exposure ↑
```

没有第三份 PauseBonus。

### Case C：差 presentation 停很久

```text
C ≈ 0
长时间 exposure
→ 仍几乎没有有效 opportunity mass
```

因此“磨时间”不能救活非响应 presentation。

### Case D：Fast Search

```text
C per opportunity ↓
但 encounter / coverage 可能 ↑
```

最终单位时间中鱼效率不能仅由 Response 层判断。

## 12. 当前缺口

尚未闭合：

- Temporal Exposure / Opportunity 的 Current Owner；
- `ExposureRate` 的生产定义；
- 与 spatial abundance / local candidate density 的精确边界；
- lure path / sweep / valid-region residency 的数据来源；
- Candidate 是否已有可直接复用的 `L_i,j` / opportunity reducer；
- reducer 是否采用 `1-exp(-x)` 还是既有 Candidate native reducer；
- repeated exposure / conditioning 是否影响 Opportunity、Wariness 或独立 memory；
- 如何定义一次连续 presentation 的 segment boundary。

## 13. Working 裁定

第一版冻结：

```text
C(t) 不拥有 duration
DecisionMargin 不加 dwell bonus
Temporal Exposure 独立累计 opportunity
Opportunity Reduce 负责 bounded accumulation
Response 不重复 Candidate reducer
```

本页闭合的是职责边界和最小数学 seam，不宣称 Opportunity production 已完成。

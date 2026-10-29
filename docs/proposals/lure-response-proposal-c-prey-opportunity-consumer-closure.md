# 方案 C｜Prey Opportunity Interpretation Consumer Closure

日期：2026-10-26  
状态：Working Probe Closure，非 Current，非生产契约。

## 1. 问题

上一轮已经确认：`escaping-like / struggling-like / vulnerable-like` 等 fishing-domain semantics 有解释价值，但不应压成 flat `OpportunityState` 或统一 `OpportunityBonus`。

本轮只问一个更工程化的问题：

> `Prey Opportunity Interpretation` 是否有独立下游消费方，因此值得成为一个生产级 authoritative object？

如果 downstream 最终只消费它内部已有的 constituent fields，那么这个 packet 只是 projection / Explain View，不应增加新的持久对象、版本治理和同步成本。

可执行 probe：`../../prototypes/lure-response/proposal_c_step4_opportunity_consumer_probe.py`。

## 2. 两条等价路径

### Path A：直接消费 constituents

Complete Feeding Response 侧直接读取：

```text
prey-side semantics
+ TaskAffordance
+ temporal context
+ fish-side Motivation
→ mode selection / response reasoning
```

### Path B：先包装 Opportunity packet

```text
same constituents
→ Prey Opportunity Interpretation packet
→ unpack
→ same mode selection / response reasoning
```

如果 Path B 没有引入新的事实、状态、约束或决策能力，它就不是新的 authority。

## 3. Probe 结果

本轮在 ChatGPT 本地 Python 环境实际执行通过。

受控案例包括：

1. 同一 `escaping-like` semantic，Feasible capture → `pursuit_or_intercept`；
2. 同一 `escaping-like` semantic，Infeasible capture → `observe_or_track`；
3. `struggling-like + vulnerable-like` 可共存，并与 favorable dwell 一起进入 Explain；
4. `vulnerable-like` 不会暗中改写低 Feeding Motivation。

直接消费 constituents 与经过 Opportunity packet 后再消费，最终决策完全一致。

结论：

```text
consumer_equivalence = true
```

当前 Opportunity packet 没有购买新的 downstream decision power。

## 4. 当前裁决

### 不 admission 为独立 authoritative production object

当前不建议建立：

```text
PreyOpportunityStateRecord
PreyOpportunityAuthority
OpportunityScore
OpportunityCoeff
```

也不建议让它成为新的可配置 Source of Truth。

原因：

- 信息全部可由已有 constituent owners 复算；
- 没有新的 decision boundary；
- 没有独立生命周期；
- 没有新的配置语义；
- 额外持久化只会增加 stale / version drift / double-authoring 风险。

### 保留为 projection / Explain View

`Prey Opportunity Interpretation` 这个名字仍然有用，但当前更适合作为：

```text
Projection / Explain View
```

它可以把：

- prey semantics；
- TaskDemand / TaskAffordance；
- temporal exposure；
- optional admitted valuation semantics；
- fish-side motivation snapshot；

组织成一张“为什么此刻是这种捕食机会”的解释卡。

但这些字段的 authority 仍属于各自 owner。

## 5. 什么时候它才值得升级为生产对象

未来至少满足一条，才重新考虑：

1. **Stable downstream contract**：多个消费方都要求一个稳定、版本化的 Opportunity packet；
2. **Expensive derivation / cache need**：计算昂贵，且必须跨帧/跨系统复用；
3. **Independent lifecycle**：Opportunity 有独立的产生、过期、撤销语义，不能简单从 constituent snapshot 重算；
4. **New decision semantics**：存在 constituent fields 单独无法表达的、明确下游决策边界；
5. **Provenance aggregation requirement**：需要稳定保存多来源证据链供调试、回放或服务器校验。

在此之前，projection 比 authority 更合理。

## 6. 对整体链条的影响

当前推荐链条收紧为：

```text
ActualPresentation
→ prey-type / prey-state interpretation
→ prey-side semantic facets

species × size cohort → InterceptSpeedLimit
+ fish-relative geometry / presentation facts
→ ResolvedTaskDemand / Closing feasibility
→ Activity-aware soft Closing cost when feasible
→ TaskAffordance

Perception / temporal context
+ fish-side Motivation
+ optional admitted valuation semantics
+ prey semantic facets when a specific consumer needs them
→ Complete Feeding Response Mode
```

`Prey Opportunity Interpretation` 不需要插成强制计算层。

它可以在调试 / Editor / Explain / telemetry 中投影出来：

```text
[Projection]
Prey Opportunity Interpretation
= why this target currently looks like this kind of feeding opportunity
```

## 7. 一个重要后果

这意味着我们不必追求每个现实/钓鱼语义都有一层生产模型。

`vulnerable-like`、`escaping-like` 等 semantic 可以存在并被具体 downstream rule 消费，但不需要先汇总成一个 Opportunity authority。

这比：

```text
State → Opportunity → Valuation → Response
```

固定四层流水线更灵活，也更符合目前的 causal evidence。

## 8. 下一步

现在应该直接攻击 `Complete Feeding Response Mode` 的最小闭合条件：

1. 哪些输入是 mode validity / gating；
2. 哪些输入是 TaskAffordance；
3. fish-side Feeding Motivation 在哪里决定“愿不愿意做”；
4. prey semantic facets 是否只在特定 mode / fish archetype 中被显式消费；
5. 是否需要独立 Valuation 层，还是可以由少量 mode-local rules 直接闭合。

在这一步之前，不再增加 Opportunity 层级或新的通用分数。
# 台钓中鱼机制｜Production Contract 候选

> 状态：Candidate / Working Contract
> 日期：2026-10-30
> 边界：本文把已确认的 Owner 边界翻译成可实现的字段、状态和接口候选。它不是 FCF Current Contract，不提供生产参数，也不替 Owner 决定各 Condition 的 cause、曲线或校准。
>
> 上游依据：Fish Condition 七项 Owner 裁定见 [Issue #161](https://github.com/futouyiba/HitFish-Up/issues/161) 的 Owner 评论；Proposal C 五项裁定见 PR [#130](https://github.com/futouyiba/HitFish-Up/pull/130) 的提交 `5caf1f119ab6e5a5c595a4ba913e7962aa338ec3`。两者均按其声明范围承接，不把工作文档升级为 Current。

## 1. 目标

当前缺口不是再发明一个总公式，而是让实现能够区分：

- 烘焙得到的 Fish Condition baseline；
- 被授权的运行时 overlay；
- 已解析、合法为零、未知、失效和拒绝；
- GenericFCF 与 ProposalCOpportunity 两条不可混用的响应接口。

本文只规定载体和状态协议。每个 Condition 的语义、输入原因、曲线、reducer 和标定仍归对应机制 Contract。

## 2. Fish Condition baseline block

DEF 条件组下保存一个结构化 block，而不是散落的裸字段：

```text
ConditionGroup × EngagementMode
→ FishConditionBaselineBlock
```

候选结构：

```text
FishConditionBaselineBlock {
  conditionGroupRef
  engagementMode
  snapshotRef
  generatedAt
  sourceVersion
  validity {
    startsAt
    expiresAt?
  }
  conditions {
    activity
    feedingMotivation
    wariness
    dietShiftByPreyFamily
  }
}
```

每个 Condition 值都不是裸数字，而是带统一解析状态的记录：

```text
ConditionValue<T> {
  value?
  status: Resolved | Zero | Unknown | Invalid | NotApplicable
  sourceRef?
  producerVersion?
  validity?
  provenance?
}
```

约束：

1. baseline 的生产者是 Bake 线；Bake 负责编排、物化和校验，不单方面决定 Condition 语义。
2. `ConditionGroup`、`EngagementMode`、snapshot、来源版本和 validity 必须可追溯。
3. 过期、越界或缺少必要来源统一解析为 `Unknown`，不得沿用最后值，也不得静默当作 0 或默认值。
baseline 数值越界一律保留 `Unknown`，例如来源齐全的 Activity=-0.1。结构、类型、所有权错误与未授权 overlay 才用 `Invalid`。Response 若绕过解析器直接收到非法数值，可独立返回 `InvalidInput`，不改变 baseline 状态。

4. `Unknown` 与合法 `Zero` 不相同。消费者必须传播 `ResolutionIncomplete` 或按自身 Contract 阻断。
5. DEF 保存 baseline；运行时 overlay 不写回 DEF。
6. Activity 非负且必须为有限数值；`1.0` 只是 Working reference，不是生产默认值或语义上界。
7. Activity、Feeding Motivation、Diet Shift 不因公共载体存在而自动获得 runtime overlay。
8. Wariness 只有在 Wariness 机制 Contract 授权后才能出现 runtime overlay；V1 可以只有 baseline。

## 3. Runtime overlay

运行时层只承接被明确授权的 Condition：

```text
FishConditionBaselineBlock
  + AuthorizedRuntimeOverlaySet
  → ResolvedFishCondition
```

候选 overlay：

```text
RuntimeOverlay {
  overlayId
  condition: Wariness | ...authorized condition...
  eventSourceRef
  scopeRef
  valueOrDelta
  effectiveFrom
  expiresAt?
  sourceVersion
  provenance
}
```

解析规则：

1. 未授权的 Condition overlay 是 `Invalid`，不能降级为普通输入。
2. 已过期 overlay 不参与求值；若该 Condition 没有仍有效的来源，则结果为 `Unknown`。
3. overlay 只能修改声明的 Condition，不能顺带修改其它 Condition、DEF 或 `SpatialDistributionWeight`。
4. 事件来源、作用粒度、衰减、有效期和跨 session 记忆没有落 Contract 前，不实现 Wariness 累积。
5. Response 只读 `ResolvedFishCondition`，不写回 baseline 或 overlay。

## 4. Response candidate envelope

每个响应候选在进入圆桌前携带一个不可混淆的接口类型：

```text
ResponseCandidateEnvelope {
  candidateId
  interfaceType: GenericFCF | ProposalCOpportunity
  identityAxes
  provenance
  resolutionStatus
  payload
}
```

载荷规则：

```text
GenericFCF {
  payload: AdaptationCoeff
  assembly: SpatialDistributionWeight × AdaptationCoeff
}

ProposalCOpportunity {
  payload: q = L × C
  assembly: direct candidate weight
}
```

组装器规则：

1. `interfaceType` 缺失时阻断组装，不猜测。
2. `GenericFCF` 不得携带已消费的 `L` 并再次进入通用组装。
3. `ProposalCOpportunity` 不得作为 `AdaptationCoeff` 交给通用组装器。
4. `ProposalCOpportunity` 不再乘 `SpatialDistributionWeight` 或第二个 `L`。
5. 只有显式 `Reject` 才产生 typed hard gate；合法 `Zero` 或已解析的数值零仍按其自身 Contract 作为数值结果处理。

`Reject` 不属于 `ConditionValue<T>.status`；它属于 Response candidate 的语义结果层。Condition 值只使用 `Resolved | Zero | Unknown | Invalid | NotApplicable`。

`interfaceType` 的具体实现载体可以是 tagged union、显式 schema discriminator 或等价的不可混淆结构；本页不指定序列化格式。

## 5. Response 输入消费矩阵

| 输入 | 唯一主要消费者 | 当前状态 | 禁止 |
|---|---|---|---|
| Fish Condition baseline / resolved state | Response 只读消费 | Candidate / Current 载体边界 | Groundbait 直接写入或自行成为第二消费者 |
| FoodValue | Response 的唯一 Food 输入或对象价值 | Candidate | 在 `selection_m` 再消费 |
| Chemical Cue | Encounter / 趋近 / Response Flavor 候选 | Candidate / OPEN | 在 `selection_m` 再消费 |
| EIO | Feeding Event 生产 | Candidate / OPEN | 进入 active `DecisionMargin` |
| `L` | Opportunity；ProposalCOpportunity 组装 | Proposal C working boundary | GenericFCF 再消费 |
| `AdaptationCoeff` | GenericFCF 圆桌组装 | Current interface / formula OPEN | 作为概率使用 |

## 6. 失败语义

| 输入状态 | 解析结果 | 下游行为 |
|---|---|---|
| 已解析合法值 | `Resolved(value)` | 按对应 Contract 求值 |
| 合法真实零 | `Zero` | 作为零贡献继续 |
| 明确不适用 | `NotApplicable` | 从适用聚合中排除 |
| 缺来源、过期、未收敛 | `Unknown` | 传播 `ResolutionIncomplete` |
| 违反字段 / 所有权 / 类型 Contract | `Invalid` | 阻断候选并报错 |
| 明确语义拒绝 | `Reject` | 产生 typed hard gate |

绝不允许：

```text
Unknown → 0
Unknown → last value
Invalid → empty fish
missing interfaceType → GenericFCF
q → AdaptationCoeff
```

## 7. 实现顺序

### V0：载体和解析器

先实现：

- `FishConditionBaselineBlock`；
- `ConditionValue<T>`；
- validity / source / version / provenance；
- `AuthorizedRuntimeOverlaySet` 的授权检查；
- `ResponseCandidateEnvelope` 的 discriminator；
- 缺失、过期、Invalid、Reject 的状态传播。

### V1：只读消费

- Bake 物化 baseline；
- Response 只读 resolved Fish Condition；
- Proposal C 继续 `RiskCost = 0`，不伪造 `TackleConspicuousness`；
- GenericFCF 与 ProposalCOpportunity 分别走唯一组装路径；
- Wariness runtime overlay 保持关闭，直到机制 Contract 补齐。

### V2：逐 Condition 生产 Contract

每个 Condition 单独补：

- 合法输入和 cause；
- 生成曲线 / reducer；
- 时间粒度；
- validity / TTL；
- runtime overlay authority；
- 标定证据与失败边界。

## 8. 验收不变量

1. DEF 中每个 baseline block 都有条件组、模式、来源版本和 validity。
2. 过期或缺来源不产生可用旧值。
3. 未授权 runtime overlay 不能改变 resolved Condition。
4. Groundbait 移除不改变 Fish Condition baseline。
5. Response 不写回 DEF、baseline 或 overlay。
6. `Unknown` 不被静默转成 0、last value 或空鱼。
7. 每个响应候选只有一个 `interfaceType`。
8. GenericFCF 与 ProposalCOpportunity 不会走同一组装路径。
9. EIO 不进入 active `DecisionMargin`。
10. `TackleConspicuousness` 未准入前 `RiskCost = 0`，不使用 SKU 或其它代理。

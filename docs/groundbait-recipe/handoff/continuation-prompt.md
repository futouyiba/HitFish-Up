# Continuation Prompt｜台钓窝料 / 配方机制

> 状态：Transient Handoff Context
> 日期：2026-10-29
> 说明：本文只用于跨会话接续，不是机制 Contract。

当前主脊：

```text
Recipe Facts
  → Physical Release
  → Feeding Place State
  → Feeding Event
      encounter
      feasible action set
      action selection
      action success
      ingestion outcome
  → Response Stage 的候选输入
```

新增对象模型见 `candidate/object-model.md`；一次摄食事件见 `candidate/feeding-event.md`。

当前最重要的概念修正：

- 粒径不是鱼的独立 Bonus，而是一次摄食动作的约束；
- Edible Size Response 应解释“对象出现后能否被有效利用”，不是直接解释吸引或最终中鱼；
- 多 Feeding Mechanism 是同一对象的替代动作路径，不能直接求和；`max` 只能作为简化上界，不能自动升级为机制真理；
- Groundbait 必须区分投放时分布与 Feeding Place 中当前可接触分布；
- Physical Release 的产物是 Feeding Place 状态，不是 `release_score`；
- 粒径既可作为鱼侧对象属性，也可作为物理对象属性，两个影响必须经不同中间状态进入，不能跨链总加权。

下一步按以下顺序推进，不能跳过前置语义：

1. 核对 `object-model.md` 的对象、状态和因果所有权。
2. 核对 `feeding-event.md` 的 encounter、可行性、选择、成功和对象状态更新。
3. 收窄 `edible-size-response.md`，只让尺寸、形态和状态进入动作约束。
4. 把 `particle-distribution.md` 接到当前 Feeding Place 对象集合，而不是静态投放比例。
5. 把 `physical-release.md` 接到 Feeding Place 状态转换。
6. 用 `response-stage-mapping.md` 对照现有 Response Stage、Response Condition、Persistent Response Field 和 Fish Condition。
7. 最后才保留少量反例，检查因果所有权、守恒和重复计权。
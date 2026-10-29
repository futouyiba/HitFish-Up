# Continuation Prompt｜台钓窝料 / 配方机制

> 状态：Transient Handoff Context
> 日期：2026-10-29
> 说明：本文只用于跨会话接续，不是机制 Contract。

当前主脊：

```text
数据
  → 烘焙 / DEF / 空间分布权重 + 鱼侧动态参数
  → 玩家策略与操作 / 呈现刺激
  → 响应 / 鱼适配系数集
  → 圆桌权重表 / 挤占
  → 抽鱼和生成
  → Fish AI（范围外）
```

Groundbait 是主脊上的第一个候选消费者：

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

端到端对象与所有权见 `candidate/system-object-model.md`；冲突与未决项见 `decisions/conflict-register.md`；Groundbait 对象模型见 `candidate/object-model.md`；一次摄食事件见 `candidate/feeding-event.md`。

当前最重要的概念修正：

- 粒径不是鱼的独立 Bonus，而是一次摄食动作的约束；
- Edible Size Response 应解释“对象出现后能否被有效利用”，不是直接解释吸引或最终中鱼；
- 多 Feeding Mechanism 是同一对象的替代动作路径，不能直接求和；`max` 只能作为简化上界，不能自动升级为机制真理；
- Groundbait 必须区分投放时分布与 Feeding Place 中当前可接触分布；
- Physical Release 的产物是 Feeding Place 状态，不是 `release_score`；
- 粒径既可作为鱼侧对象属性，也可作为物理对象属性，两个影响必须经不同中间状态进入，不能跨链总加权。

下一步按以下顺序推进，不能跳过前置语义：

1. 核对 `decisions/conflict-register.md` 的未决项和裁决方。
2. 核对 `candidate/system-object-model.md` 的对象、权重和阶段隔离。
3. 环境烘焙：只消费 `SpatialDistributionWeight`，不重新计算环境系数。
4. Fish Condition：只作为条件输入，不由窝料或味型直接写入。
5. Response Stage：先定输入输出和持久字段语义，再定聚合公式。
6. Groundbait 全栈：对象守恒 → 释放状态 → 分布 → 摄食事件 → Food / Flavor。
7. 圆桌与抽鱼：先定顺序和所有权，再谈具体权重规则。
8. 最后才保留少量反例，检查因果所有权、守恒和重复计权。
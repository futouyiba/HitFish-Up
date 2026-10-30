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

当前状态：

候选链已在接口层闭合。Size、Food、Flavor、Physical Release、Attraction / Retention 的 Candidate 判断和 Response Aggregation 映射都已落文档。

剩余工作是 Owner 决策和数值公式：`AdaptationCoeff`、组件聚合、模式聚合、多 Target 算子、化学强度准入、Local Population / Residence、Overfeeding，以及冲突登记里的 OPEN 项。

如果讨论开始扩张到 Attraction、Retention、Recipe Grammar、Food Taxonomy 或 Flavor Taxonomy，就停下来，说明已经偏离当前工作项。

端到端对象、烘焙、鱼况、响应和圆桌文档仍作为背景和边界，不是本轮任务。冲突与未决项见 `decisions/conflict-register.md`。

不把 `KEEP_OPEN` 项写成已确认规则，也不把 `CANDIDATE_BRANCH` 当成 Owner 裁定。
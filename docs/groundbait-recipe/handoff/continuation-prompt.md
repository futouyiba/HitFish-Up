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

当前阶段文档：

- 端到端对象与所有权：`candidate/system-object-model.md`
- 环境烘焙接入：`candidate/environment-bake-integration.md`
- Fish Condition：`candidate/fish-condition-integration.md`
- Response 算法接口：`candidate/response-algorithm.md`
- Groundbait 全栈：`candidate/groundbait-integration.md`、`candidate/food-flavor.md`
- 圆桌与抽鱼：`candidate/roundtable-and-draw.md`
- 跨阶段不变量：`candidate/cross-stage-invariants.md`
- 冲突与未决项：`decisions/conflict-register.md`

下一步不是继续扩写机制，而是处理 Owner 决策和证据缺口：

1. 按 `conflict-register.md` 的裁决顺序，先处理 C-01、C-02、C-03。
2. 处理 C-04、C-05，决定 Response 接入和持久字段语义。
3. 处理 C-06、C-07、C-08、C-12、C-13、C-14，决定空间、时间与鱼况边界。
4. 处理 C-09、C-10、C-11，决定抽鱼、刺鱼和多目标聚合。
5. 只有在语义闭合后，才考虑最小 Fixture 和实现验证。

不把 `KEEP_OPEN` 项写成已确认规则，也不把 `CANDIDATE_BRANCH` 当成 Owner 裁定。
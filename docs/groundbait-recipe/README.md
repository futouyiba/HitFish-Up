# 台钓窝料 / 配方机制文档入口

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 权威边界：本目录整理当前讨论形成的工作提案、工作决定、已排除方向和跨会话上下文。它不是 FCF Current Contract，不自动覆盖现有中鱼框架、Response Contract 或术语规范。正式术语与权威关系仍以 [`docs/README.md`](../README.md)、[`docs/authority-model.md`](../authority-model.md) 和对应 Current 文档为准。

## 目录职责

```text
docs/groundbait-recipe/
├─ README.md                         # 唯一入口
├─ decisions/                        # 工作决定及其成熟度
│  ├─ working-decisions.md
│  └─ conflict-register.md
├─ candidate/                        # 当前最新工作提案
│  ├─ proposal.md
│  ├─ system-object-model.md
│  ├─ environment-bake-integration.md
│  ├─ fish-condition-integration.md
│  ├─ response-algorithm.md
│  ├─ roundtable-and-draw.md
│  ├─ cross-stage-invariants.md
│  ├─ object-model.md
│  ├─ groundbait-integration.md
│  ├─ food-flavor.md
│  ├─ edible-size-response.md
│  ├─ feeding-event.md
│  ├─ particle-distribution.md
│  ├─ physical-release.md
│  ├─ response-stage-mapping.md
│  └─ plain-language-explainer.md
├─ rejected/                         # 已排除 / 当前不采用的反设计
│  └─ anti-designs.md
└─ handoff/                          # 跨会话临时上下文，不是长期机制事实
   └─ continuation-prompt.md
```

`decisions/` 区分“已收敛边界”和“仍待推演的算法候选”，并登记跨文档冲突；`candidate/` 保存当前完整方案；`rejected/` 不参与正常主线读取，避免旧方案与最新方案并肩竞争注意力；`handoff/` 只服务跨会话接续。

## 阅读顺序

后续 Agent 处理台钓窝料、混饵、味型、粒径或小药机制时，按以下顺序读取：

1. [`decisions/working-decisions.md`](decisions/working-decisions.md)：先确认哪些是已收敛边界，哪些仍只是 Active Candidate。
2. [`decisions/conflict-register.md`](decisions/conflict-register.md)：跨文档、跨候选栈的冲突与未决项。
3. [`candidate/proposal.md`](candidate/proposal.md)：整体提案。
4. [`candidate/system-object-model.md`](candidate/system-object-model.md)：端到端对象、权重与阶段隔离。
5. [`candidate/environment-bake-integration.md`](candidate/environment-bake-integration.md)：环境烘焙与空间分布权重的消费边界。
6. [`candidate/fish-condition-integration.md`](candidate/fish-condition-integration.md)：鱼况在完整链中的位置与消费者。
7. [`candidate/response-algorithm.md`](candidate/response-algorithm.md)：Response Stage 的输入输出与聚合顺序。
8. [`candidate/roundtable-and-draw.md`](candidate/roundtable-and-draw.md)：圆桌、抽鱼、生成与 Fish AI 边界。
9. [`candidate/cross-stage-invariants.md`](candidate/cross-stage-invariants.md)：跨阶段不变量与最小反例。
8. [`candidate/object-model.md`](candidate/object-model.md)：Groundbait 对象、状态与因果所有权。
9. [`candidate/groundbait-integration.md`](candidate/groundbait-integration.md)：四条事实路径的整合与重复计权检查。
10. [`candidate/food-flavor.md`](candidate/food-flavor.md)：Food 与 Flavor 的候选位置和准入问题。
11. [`candidate/edible-size-response.md`](candidate/edible-size-response.md)：可摄食尺寸如何进入动作约束。
12. [`candidate/feeding-event.md`](candidate/feeding-event.md)：一次摄食事件的可行性、选择与成功。
13. [`candidate/particle-distribution.md`](candidate/particle-distribution.md)：Groundbait 粒径分布及对象状态候选。
14. [`candidate/physical-release.md`](candidate/physical-release.md)：雾化、黏度、解体和沉降的释放候选。
15. [`candidate/response-stage-mapping.md`](candidate/response-stage-mapping.md)：与现有 Response Stage 的候选接口映射。
16. [`candidate/plain-language-explainer.md`](candidate/plain-language-explainer.md)：面向人类快速理解当前设计。
17. [`rejected/anti-designs.md`](rejected/anti-designs.md)：只在评审、反例检查或需要理解边界时读取。
18. [`handoff/continuation-prompt.md`](handoff/continuation-prompt.md)：跨会话继续工作用的临时上下文与任务提示。

当前设计主旨不是四个并列 Bonus，而是一条从数据到抽鱼的完整主脊：

```text
数据
  → 烘焙 / DEF / 空间分布权重 + 鱼侧动态参数
  → 玩家策略与操作 / 呈现刺激
  → 响应 / 鱼适配系数集
  → 圆桌权重表 / 挤占
  → 抽鱼和生成
  → Fish AI（范围外）
```

Groundbait 是这条主脊上的第一个候选消费者：

```text
Recipe Facts
  → Physical Release
  → Feeding Place State(place, t)
  → Feeding Event
  → Response Stage 的候选输入
```

Food、Flavor、Particle、Physical Release 各自进入主脊的不同位置，不在末端直接相加。哪些部分是 Current 术语、哪些是 Reference 证据、哪些只是 Candidate，见 `decisions/conflict-register.md` 和 `candidate/system-object-model.md`。

- Food、Flavor、Particle Size、Physical Release 的职责不同，不直接并列成四个 Bonus 相加。
- 小药不作为免费固定 Bonus；状态饵也必须承担固体份额或其它真实成本。
- 雾化、黏度等首先改变释放速度、扩散范围、沉降和持续时间，不直接写成中鱼倍率。
- Particle Size 单独抽成 `Edible Size Response`，目标是让窝料颗粒和后续钩上饵球共享同一套“可摄食尺寸”语言，但 Hookbait 仍有自己的入口性、持钩、姿态等额外因素。
- “天气直接切换味型偏好”目前证据不足，不作为候选规则；天气等环境输入优先进入现有 Fish Condition / Feeding Readiness 语义。
- 最终是否存在单一 `RecipeFit` 尚未决定。Attraction、Retention、Ingestion、Selection 可能需要保留为不同语义，不能因为公式整齐而提前相加。

当前主要算法候选仍需验证：

- Food：同 Target 合并后边际递减。
- Flavor：先按 Chemical Cue Exposure / Potency 混成整体 Flavor Profile，并保留总 Intensity；不是按 Ingredient 质量份额直接当味型百分比。
- Edible Size：用鱼的线性体尺、形态和 Feeding Mechanism 解释实体对象如何进入有效摄食；多 Feeding Mechanism 是受限的替代路径，不是默认求和。

## 研究输入

本轮主要设计输入之一：

- `futouyiba/programaticHitFish/docs/research/2026-10-27-rf4-recipe-aggregation-design-recommendation.md`
- 已读取版本 blob：`88ac78e33f90cd55ea5c01af90406bbca084b91f`

该研究明确是 Research / Working Proposal，不是 RF4 内部公式事实，也不是 FCF Current。当前目录只吸收其中经本轮继续推敲后仍保留的设计结论。

## 当前推进顺序

```text
阶段 0：权威冻结与冲突清单
↓
阶段 1：端到端对象与权重所有权
↓
阶段 2：环境烘焙 / DEF / 空间分布权重
↓
阶段 3：Fish Condition
↓
阶段 4：Response Stage 与 Adaptation Coefficient
↓
阶段 5：Groundbait 全栈（对象 / 释放 / 分布 / 摄食 / Food / Flavor）
↓
阶段 6：圆桌与抽鱼
↓
阶段 7：抽鱼/生成与 Fish AI 边界
↓
阶段 8：跨阶段不变量与最小验证
```

不要从最终总公式开始倒推各模块，也不要在语义未定时先写 Fixture。

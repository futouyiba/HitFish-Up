# 台钓窝料 / 配方机制文档入口

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 权威边界：本目录整理当前讨论形成的工作提案、工作决定、已排除方向和跨会话上下文。它不是 FCF Current Contract，不自动覆盖现有中鱼框架、Response Contract 或术语规范。正式术语与权威关系仍以 [`docs/README.md`](../README.md)、[`docs/authority-model.md`](../authority-model.md) 和对应 Current 文档为准。

## 术语对照

| 中文 | English / Identifier | 说明 |
|---|---|---|
| 基础权重 | Base Weight / Base Opportunity Intensity | 环境影响前的基础机会量级 |
| 空间分布权重 | SpatialDistributionWeight | 基础权重乘环境系数，未归一化 |
| 派生环境场 | DEF / Derived Environment Field | 烘焙结果，按条件组保存 |
| 鱼况 | Fish Condition | 活跃度、摄食动机、食性偏移、警戒度 |
| 响应阶段 | Response Stage | 读取烘焙结果和玩家刺激，输出适配系数 |
| 持久响应场 | Persistent Response Field | 持续玩家行为的增量层 |
| 适配系数 | Adaptation Coefficient | 响应阶段的无量纲倍率 |
| 圆桌权重表 | Roundtable Weight List | 抽鱼前的候选权重列表 |
| 挤占 | Crowding-out | 圆桌抽鱼中的候选竞争 |
| 配方事实 | Recipe / Ingredient Facts | 原料和配比提供的事实 |
| 配方角色 | Recipe Role | 玩家在配方里赋予 Ingredient 的功能角色，不是原料分类 |
| 物理释放 | Physical Release | 配方状态到摄食地点状态的转换 |
| 可食颗粒 | Edible Particle | 进入尺寸响应的实体可食部分 |
| 载体颗粒 | Carrier / Non-edible Particle | 有粒径、参与释放，但不进入可食利用 |
| 摄食地点状态 | Feeding Place State | 本目录工作词，当前可接触对象与线索 |
| 摄食事件 | Feeding Event | 本目录工作词，一次摄食机会 |
| 有效摄食机会 | Effective Ingestion Opportunity | 本目录工作词，候选输出接口 |
| 化学线索场 | Chemical Cue Field | 本目录工作词，可感知化学线索 |
| 颗粒对象 | Particle Object | 本目录工作词，实体食物对象 |

Current 术语以 [`docs/terminology.md`](../terminology.md) 为准；Candidate-local 词不进入正式术语表。

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
│  ├─ edible-size-gold-fixture.md
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
10. [`candidate/object-model.md`](candidate/object-model.md)：Groundbait 对象、状态与因果所有权。
11. [`candidate/groundbait-integration.md`](candidate/groundbait-integration.md)：四条事实路径的整合与重复计权检查。
12. [`candidate/food-flavor.md`](candidate/food-flavor.md)：Food 与 Flavor 的候选位置和准入问题。
13. [`candidate/edible-size-response.md`](candidate/edible-size-response.md)：可摄食尺寸如何进入动作约束。
14. [`candidate/edible-size-gold-fixture.md`](candidate/edible-size-gold-fixture.md)：窄版结构验证，不进入生产参数。
15. [`candidate/feeding-event.md`](candidate/feeding-event.md)：一次摄食事件的可行性、选择与成功。
16. [`candidate/particle-distribution.md`](candidate/particle-distribution.md)：Groundbait 粒径分布及对象状态候选。
17. [`candidate/physical-release.md`](candidate/physical-release.md)：雾化、黏度、解体和沉降的释放候选。
18. [`candidate/response-stage-mapping.md`](candidate/response-stage-mapping.md)：与现有 Response Stage 的候选接口映射。
19. [`candidate/plain-language-explainer.md`](candidate/plain-language-explainer.md)：面向人类快速理解当前设计。
20. [`rejected/anti-designs.md`](rejected/anti-designs.md)：只在评审、反例检查或需要理解边界时读取。
21. [`handoff/continuation-prompt.md`](handoff/continuation-prompt.md)：跨会话继续工作用的临时上下文与任务提示。

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
- “天气直接切换味型偏好”目前证据不足，不作为候选规则；天气等环境输入优先进入现有 Fish Condition 语义。
- 最终是否存在单一 `RecipeFit` 尚未决定。Attraction、Retention、Ingestion、Selection 可能需要保留为不同语义，不能因为公式整齐而提前相加。

当前工作重点是 Size，不是把外围框架继续铺满：

- 先按 WD-23 完成三个前置语义闭合：Ingredient 与 Recipe Role、物理颗粒与可食颗粒、Edible Size 输出语义。
- 然后用 `candidate/edible-size-gold-fixture.md` 检查结构，不做生产参数。
- Fixture 失败就修 Size Candidate；通过就停在这里，不进入 Food、Flavor 或完整 Recipe Grammar。

Food、Flavor、Attraction、Retention 和完整配方语法仍停在候选层，不作为这一轮的下一步。

## 研究输入

早期讨论引用过一份外部研究：

- `futouyiba/programaticHitFish/docs/research/2026-10-27-rf4-recipe-aggregation-design-recommendation.md`
- 记录的 blob：`88ac78e33f90cd55ea5c01af90406bbca084b91f`

2026-10-29 复核时，本地未找到该文件或 blob，因此这份引用只能当作来源声明，不能当作可复核证据。它即使可读，也只是 Research / Working Proposal，不是 RF4 内部公式事实，也不是 FCF Current。当前目录只保留经本轮继续推敲后仍有仓内依据的设计结论。

## 当前推进顺序

```text
Step 0：Size 前置语义闭合
↓
Step 1：Edible Size Gold Fixture
↓
Step 2：Groundbait Particle Distribution
↓
Step 3：Food Aggregation
↓
Step 4：Flavor + 小药 + Avoidance
↓
Step 5：Physical Release
↓
Step 6：判断 Attraction / Retention 是否需要独立模块
↓
Step 7：最终 Response Aggregation
```

这份顺序是当前工作项，不是对整个端到端计划的否定。端到端对象、烘焙、鱼况、响应和圆桌文档仍作为背景和边界；它们不要求在 Size 之前全部完成。

不要从最终总公式开始倒推各模块，也不要在语义未定时先写 Fixture。

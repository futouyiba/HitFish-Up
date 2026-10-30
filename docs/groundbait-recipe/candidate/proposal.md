# 台钓窝料 / 饵料混合机制 Candidate Proposal

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 说明：本文记录当前整体提案。`decisions/working-decisions.md` 区分已收敛边界与仍待验证的算法候选；本文不把 Candidate 写成正式 Contract。

## 1. 设计目标

这套机制要让玩家围绕以下问题做配方选择：

1. 目标鱼吃什么。
2. 哪种化学线索 / 味型更容易形成有效刺激。
3. 颗粒尺寸会筛选哪些鱼和哪些体型。
4. 饵料如何在水中释放，决定开窝速度、扩散范围、沉降位置和持续时间。
5. 小药、状态饵和主攻饵之间存在真实机会成本，而不是免费叠加 Buff。

目标不是算出一个隐藏的最佳配方总分，而是让不同组成承担不同职责，并能被玩家观察、试验和学习。

## 2. 总体因果结构

当前主脊不是四个加分层，而是一次状态转换和一次摄食事件：

```text
Recipe / Ingredient Facts
  ├─ Food Identity
  ├─ Chemical Cue Potential
  ├─ Particle / Object Properties
  └─ Physical Release Properties
        ↓
Physical Release
        ↓
Feeding Place State(place, t)
  ├─ contactable objects
  ├─ Chemical Cue Field
  ├─ location / layer
  └─ object processing state
        ↓
Feeding Event
  ├─ encounter
  ├─ feasible action set
  ├─ action selection
  ├─ action success
  └─ effective ingestion opportunity
        ↓
Response Stage 的候选输入
        ↓
现有 Adaptation Coefficient / 下游权重链
```

`Feeding Place State`、`Feeding Event` 和 `Effective Ingestion Opportunity` 仅是本目录的 Candidate-local 工作词，不是 FCF Current Contract。

## 3. Common Ingredient / Recipe Facts

配方事实只描述来源和资源，不直接提供鱼种总分。每条事实进入自己的因果路径：

| 事实 | 进入的中间状态 | 主要被谁消费 | 不直接负责 |
|---|---|---|---|
| Food Identity | 实体对象的 Food 属性 | Food 目标 / Response 输入 | 尺寸成功、释放速度 |
| Chemical Cue Potential | Chemical Cue Field | 发现、趋近、回避与 Response 输入 | 实体质量、尺寸成功 |
| Particle / Object Properties | Particle Object / Object State | 动作可行性、动作成功 | 鱼种偏好、最终中鱼 |
| 可食 / 载体区分 | Edible Particle Distribution / Carrier | Size Response / Physical Release | 不把载体算成可食 |
| Physical Release Properties | Feeding Place State | 接触机会、位置、水层、持续时间 | 固定中鱼 Bonus |

同一个 Ingredient 可以同时提供多类事实，但相同来源不意味着可以把不同路径相加。Ingredient Facts 是原料的固有事实；`Base / Target / State / Attractant` 是配方级角色和配比约束，不是 Ingredient 的固有分类。完整对象和所有权见 `object-model.md`。

固体还要区分可食颗粒和载体 / 不可食颗粒。两者都可以有粒径，也都可以参与释放，但只有可食颗粒进入尺寸响应。完整分层见 `particle-distribution.md`。

## 4. Food：同 Target 合并后边际递减

### 4.1 当前候选

同一 Food Target 的 Ingredient 先合并 Exposure，再做 Target 级边际递减。

```text
Ingredient shares
        ↓
同 Food Target Exposure 合并
        ↓
Fish × Food Target Preference
        ↓
Target Response with diminishing returns
```

设计意图：

- 避免逐 Ingredient 饱和导致“拆成多个 ID 就变强”。
- 缓解简单线性加权下，单目标鱼把全部预算堆给单位系数最高 Ingredient 的退化。
- 当鱼确实同时喜欢两个 Food Target 时，允许出现有限混配价值。

注意：边际递减不保证混配一定更优。如果某鱼只有甲壳类强响应，虫类为 None，则 40% 甲壳类主攻饵应允许优于 30% 甲壳 + 10% 虫。

### 4.2 仍未闭合

完整聚合见 `food-aggregation.md`。

- Food Target 字典的正式成员和版本化 admission 流程。
- 饱和函数族和参数如何标定。
- 多 Target 聚合算子按基线 R0 保持 OPEN，不在本页选择 `sum`、`weighted average`、`max` 或 `Noisy-OR`。
- Food 只作为 Response 的唯一 Food 输入或对象价值来源；当前不在 `selection_m` 动作选择中再次消费。

## 5. Flavor：由 Cue Exposure 形成整体味型画像

### 5.1 当前候选

完整候选见 `flavor-and-avoidance.md`。在化学强度准入前，当前工作分支只使用化学签名集合；下面的 Cue Exposure 模型属于被阻塞的分支 B，不能当作当前可用公式。

Flavor 不直接按 Ingredient 的质量百分比求“味型占比”。先由每个 Ingredient 的用量 / 剂量与 Chemical Cue Potency 生成各味型的 Exposure：

```text
Ingredient amount / dose
× Cue Potency
→ Cue Exposure by flavor family
```

然后从这些 Exposure 得到两类量：

```text
Flavor Intensity     = 总体化学线索强度
Flavor Composition   = 各味型在总 Exposure 中的相对组成
```

示意：

```text
腥   40%
谷香 30%
果香 20%
奶香 10%
```

这里的百分比代表 Cue Exposure 组成，不代表原料质量占比。

鱼侧再用 Flavor Preference / Avoidance 去解释这张画像及其总强度。

### 5.2 为什么不使用 Flavor Target 独立饱和后求和

如果腥、奶、果、蒜每种都独立获得一条饱和曲线，玩家会自然趋向“每种都放一点”的 Flavor 全家桶。Composition 方案让新味型改变和稀释旧味型，因此既可能改善，也可能破坏原配方。

### 5.3 小药

小药当前定义倾向：

> 低剂量、高 Potency 的 Chemical Cue Modifier。

它不应当是：

```text
基础配方分 + 固定小药 Bonus
```

而应显著改写 Flavor Exposure / Composition / Intensity。

RF4 公开资料可以支持 attractant 很强，但“强且一定短效”目前不足以视为 RF4 事实。若本项目未来采用高峰值、快衰减，需要作为自己的机制设计验证。

### 5.4 Sparse Avoidance

“不喜欢”和“排斥”分开：

- 不喜欢：未获得正向匹配。
- 排斥：某种 Cue 出现会主动降低响应。

不建议把所有 Fish × Flavor 配成完整 `-1..+1` 矩阵。Repulsion / Avoidance 应当稀疏，只为有明显解释价值的关系配置。

浓度过高导致普遍 Overdose 与“天生排斥某味型”是不同机制。首版不必同时购买两套复杂度。

## 6. Particle Size：解释对象如何进入有效摄食

颗粒大小不是 Food 或 Flavor Bonus。它主要解决：

> 当实体对象已经出现在鱼可接触的地点和状态中，这条鱼能否通过某种摄食动作有效利用它？

完整 Candidate 见 `object-model.md`、`edible-size-response.md` 和 `feeding-event.md`。Groundbait 粒径分布与物理释放分别见 `particle-distribution.md` 和 `physical-release.md`；这些页面描述对象、状态和因果接口，不把归一化 Fixture 冒充生产参数。尺寸的结构验证见 `edible-size-gold-fixture.md`。

当前核心结构：

```text
Body / Morphology
→ action capacity

Feeding Place + object state
→ feasible action paths

feasible paths + object size
→ size-conditioned usability

size-conditioned usability
→ effective ingestion opportunity
```

`Body Linear Size` 必须是体长等线性尺度。重量不能直接与无量纲 Ratio 相乘生成长度。

Groundbait 用当前地点可接触的可食颗粒分布求 `EdibleUtilization`；载体和不可食颗粒只进入物理释放。Hookbait 后续可用单颗饵球尺寸复用“尺寸约束”语言，但 Hookbait 还会有入口性、硬度、持钩、姿态等其它因素，不等于整套 Groundbait Response 直接复用。

## 7. Physical Release：雾化、黏度不是直接中鱼系数

### 7.1 当前职责

雾化、黏度、比重、粒径等先决定或参与决定：

- 解体速度；
- Chemical Cue 释放速度；
- Food / Particle 空间扩散；
- 沉降和所在水层；
- 局部留存和持续时间。

这些结果再形成 Feeding Place 的时空状态。当前不预设“某个物理属性越高越好”，也不把“高黏度必然更集中”等尚未验证关系写成硬规则。完整状态转移和守恒账本见 `physical-release.md`。

### 7.2 需要验证的策略故事

- 快速开窝 vs 长时间守窝；
- 快速扩散、容易发现 vs 集中、持久；
- 细颗粒提高广泛利用 / 频率 vs 粗颗粒提高体型筛选；
- 高释放可能带来杂鱼和维护成本，而非单向增益；
- 状态饵占据固体份额，用物理效果换取 Food / Flavor 机会成本。

这些是策略目标，不是已完成公式。

## 8. Fish Condition 与 Diet Shift

### 8.1 当前较稳边界

天气、时段等环境输入优先通过现有 Fish Condition 语义影响“现在愿不愿意响应”。

### 8.2 Diet Shift 仍是后置候选

不采用“每杆随机今天喜欢什么”，也不采用无证据的“下雨固定喜欢腥、晴天固定喜欢果香”。

若后续需要 Diet Shift，可测试：

```text
Baseline Diet / Preference
        ↓
Contextual Shift
        ↓
可选 Slow Bounded Stochastic Drift
```

较慢的生态 Context，例如季节、水温阶段、水域食物结构、生物事件等，只有在有证据或明确玩法价值时才进入 Preference Shift。随机漂移是否需要、如何产生仍是 Open，不应提前当作既定机制。

## 9. Candidate 与现有 Response Stage 的边界

现有仓内术语把窝料列为 `Response Condition` 的玩家侧输入，并为持续生效的玩家行为保留 `Persistent Response Field` 入口。本 Candidate 只提供可被这些入口消费的候选状态：

```text
Feeding Place State
+ Fish Condition
+ Response Components
+ Presentation Signal（若适用）
→ 现有 Response Stage
→ Adaptation Coefficient / 下游候选权重
```

候选模块不定义 `Adaptation Coefficient` 公式，不写回 `SpatialDistributionWeight`，不直接设置 `Fish Condition`，也不把同一份窝料效果同时作为持久和即时增量重复消费。具体映射与 OPEN 项见 `response-stage-mapping.md`。

## 10. 不急于定义单一 RecipeFit

当前不为了公式整齐而直接写：

```text
RecipeFit = FoodFit + FlavorFit + ParticleFit + PhysicalFit
```

原因：这些量处于不同阶段。Food Identity、Chemical Cue、对象约束和物理释放必须先沿各自路径形成 Feeding Place 与 Feeding Event 状态，再由现有 Response Stage 消费。简单相加会重复计算。

`Attraction`、`Retention`、`Ingestion`、`Selection` 仍只是解释候选，不是本目录已经确认的正式中间层；如需使用，必须明确它属于哪个阶段、由谁生产、由谁消费。当前判断是 Attraction 和 Retention 都不独立成模块，理由和翻转条件见 `../decisions/attraction-retention-verdict.md`。最终聚合映射见 `response-aggregation-map.md`。

以下只描述配方输入的资源与职责边界，不是平衡定值：

| 角色 | 候选限制 |
|---|---|
| Base | 1 槽，约 50–70% 固体质量 |
| Target Bait | 1–2 槽，总计约 20–40% |
| State Ingredient | 0–1 槽，0–20%，占固体质量 |
| Attractant / 小药 | 0–1 槽，独立剂量但必须有上限 / 成本 |
| 固体总量 | 100% |
| 玩家配比步长 | 5% 或“份”优先，避免精确数学极值玩法 |

## 11. 推荐推进顺序

1. 先收清实体对象从配方到 Feeding Place 的状态转换。
2. 定义一次摄食事件中的动作可行、动作选择和动作成功边界。
3. 用体尺、形态和摄食动作生成可解释的尺寸约束；不先手填最佳毫米数。
4. 把粒径分布接入当前地点的可接触对象，而不是直接接最终 Response。
5. 把雾化、黏度、沉降和解体写成 Feeding Place 状态转换。
6. 再处理 Food Target、Flavor Exposure、小药和 Sparse Avoidance 如何进入发现、趋近、留存和摄食。
7. Groundbait 机制闭合后，再让 Hookbait 复用鱼侧尺寸约束；不复用完整响应。
8. 最后再收 Diet Shift 与下游 Response Aggregation。

Fixture 只承担反例和边界检查，不承担机制设计本身。

## 12. Regression Guardrails

持续检查以下退化，不把它们重新写回主方案：

- 单位效果最高 Ingredient 永远全塞。
- 同作用 Ingredient 拆多个 ID 后凭空变强。
- 每个 Food / Flavor Target 都塞一点的全家桶。
- 小药永远必加。
- 状态饵成为免费 Buff。
- 高雾化或高黏度成为无条件更好。
- 多 Feeding Mechanism 因为数量多而叠加套利。
- 颗粒尺寸使用假精度，要求每鱼手填毫米值。
- 天气被硬编码成简单 Flavor 密码。

已排除方向及原因集中见 `../rejected/anti-designs.md`。

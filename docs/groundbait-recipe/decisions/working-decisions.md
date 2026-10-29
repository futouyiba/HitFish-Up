# 台钓配方机制｜Working Decision Ledger

> 状态：Working Decision Ledger
> 日期：2026-10-29
> 边界：这里记录本轮讨论形成的工作决定，并明确区分成熟度。它们仍不是正式 FCF Contract；若与更高权威 Current / Owner 裁定冲突，以更高权威为准。

## 状态说明

- **BOUNDARY**：当前已收敛的设计边界。后续 Agent 不应无故从零重开；若要推翻，应给出新的证据或明确反例。
- **ACTIVE CANDIDATE**：当前最值得推演和验证的机制方案，仍需证据或反例攻击，不得当作已确认公式。
- **OPEN**：尚未闭合，只记录问题边界。

## WD-01｜Groundbait 作为第一个完整消费者

**状态：BOUNDARY**

先建立薄的 Common Ingredient / Recipe Facts，然后优先用 Groundbait 验证完整机制；Hookbait / 饵球后续只复用适合共用的 Size Response 等语言。

当前最不确定、最能暴露配方策略深度的问题主要在 Feeding Place、粒径分布、雾化、黏度、释放、留鱼和补窝。

## WD-02｜Food、Flavor、Particle、Physical Release 分责

**状态：BOUNDARY**

- Food：表达有什么可摄食目标。
- Flavor / Chemical Cue：表达鱼感知到什么化学线索。
- Particle Size：表达实体食物尺寸对不同鱼 / 体型的可利用性。
- Physical Release：表达这些信号何时、在哪里、持续多久出现。

不直接把四者做成四个并列 Bonus。

## WD-03｜Food 与 Flavor 不共用同一个 Target 字典

**状态：BOUNDARY**

虫、谷物、甲壳等可摄食目标与腥、奶、果、蒜等化学线索语义不同。Flavor 不直接塞进 Food Target / `FeedingTargetKey`。

## WD-04｜Food 同 Target 合并后边际递减

**状态：ACTIVE CANDIDATE**

同作用 Food Target 的 Exposure 先合并，再进入饱和 / 边际递减。目标是避免逐 Ingredient 拆分套利，并允许鱼同时喜欢两个 Food Target 时出现有限混配价值。

这仍需证据或反例攻击，不等于最终数值公式已定，也不保证混配一定优于单一 Target 专精。

## WD-05｜Flavor 使用 Cue Exposure 形成整体画像

**状态：ACTIVE CANDIDATE**

当前候选由：

```text
Ingredient amount / dose × Cue Potency
→ Cue Exposure
→ Composition + Intensity
```

组成。加入新味型会改变和稀释原有 Cue Exposure 的相对组成，不按味型逐项领取独立 Bonus。

`Composition` 不是 Ingredient 质量百分比。

## WD-06｜小药不是免费 Buff

**状态：BOUNDARY**

小药不能简单设计成“基础配方分 + 固定小药 Bonus”。当前候选是低剂量、高 Potency 的 Chemical Cue Modifier；具体 Exposure / 衰减模型仍待验证。

## WD-07｜排斥与“不喜欢”分开

**状态：BOUNDARY**

- 不喜欢：没有获得明显正收益。
- 排斥：Cue 出现会主动压低响应。

Avoidance 应稀疏配置，不建立全量 Fish × Flavor 负数矩阵。

## WD-08｜雾化、黏度首先属于释放机制

**状态：BOUNDARY**

雾化、黏度、比重、颗粒等首先参与决定 Breakdown、Cue Release、Spread、Sinking、Persistence 等过程，不直接写成中鱼倍率。

具体物理关系，例如“高黏度是否一定更集中、更持久”，仍需后续 Physical Release Fixture 验证。

## WD-09｜Particle Size 抽成独立 `Edible Size Response`

**状态：BOUNDARY**

Groundbait Particle 与 Hookbait / 饵球可以共享“尺寸是否适合摄食”这一鱼侧语言。

共享不等于整套 Response 复用；Hookbait 还会有形状、硬度、钩体阻碍、持钩、姿态等额外因素。

## WD-10｜线性体尺与 Morphology 分开

**状态：ACTIVE CANDIDATE**

- Body Linear Size 负责个体成长尺度。
- Morphology Profile 负责同体尺下的物种形态差异。

普通口部路径可由线性体尺与 Oral Scale 生成 Reference。重量不能直接乘无量纲 Ratio 生成颗粒尺寸。

FILTER 不强制使用同一线性比例关系，可由 Filter Morphology 直接提供或生成独立 Reference / Efficiency Window。

## WD-11｜Feeding Mechanism 是动作路径

**状态：ACTIVE CANDIDATE**

PICK、SUCTION、BENTHIC_SUCTION、GULP、FILTER 等不是同一条尺寸曲线的倍率，而是不同的摄食动作路径。每条路径必须分别说明前提、动作能力、对象约束与成功结果。

## WD-12｜多 Feeding Mechanism 是受限的替代路径

**状态：ACTIVE CANDIDATE**

多个 Feeding Mechanism 代表同一对象的不同处理路径，不是多个可同时领取的奖励。直接求和会把一次摄食事件重复计奖。

当前只收敛到：

```text
EdibleSizeUsability = aggregate over feasible action paths
```

`max(proficiency × curve)` 可以作为“动作可自由切换、没有切换代价”的简化上界，但不再把它写成默认机制公式。路径选择必须只在可行集合中归一化；若未来需要表达选择概率，应与动作成功分开。

## WD-13｜大颗粒筛小鱼；小颗粒不默认强烈排斥大鱼

**状态：ACTIVE CANDIDATE**

当前对大对象的强约束应首先落在相关动作的可行性与成功，而不是额外创建“大鱼 / 小鱼 Bonus”。

左侧是否存在细小对象的处理损失，应由具体动作、对象价值和状态解释，不能统一降到 0，也不能仅因鱼体更大就人为加负分。

## WD-14｜天气不直接作为 Flavor 密码

**状态：BOUNDARY**

“下雨就喜欢腥、晴天就喜欢果香”目前证据不足，不作为候选机制。天气、时段等环境输入优先进入现有 Fish Condition 语义。

Diet Shift 的驱动方式仍是 **OPEN**。若以后保留，可测试 Contextual Shift 和慢、有界、有记忆的随机漂移，但随机漂移本身尚未确认。

## WD-15｜Groundbait 先形成 Feeding Place 中的对象状态

**状态：ACTIVE CANDIDATE**

Groundbait 不能直接从投放配方比例跳到鱼侧可利用率。当前候选链是：

```text
Recipe Particle Distribution
  → Physical Release
  → Available Particle Distribution(place, t)
  → Edible Size Usability(f, place, t)
```

粒径分布与物理释放分别描述对象属性和状态转换，但不是两个并列 Bonus。质量份额只能作为明确声明的计量投影，不能代替 Feeding Place 中当前可接触对象的分布。

对应候选文件：`candidate/particle-distribution.md`、`candidate/physical-release.md`。

## WD-16｜Groundbait 只能通过现有 Response Stage 接入

**状态：BOUNDARY**

本 Candidate 只定义 Groundbait 产生的对象状态、线索状态和有效摄食机会候选。它们如何落入 `Response Condition`、`Persistent Response Field` 或其它既有响应入口，必须按现有 Current / Owner 语义核对；不新造 Current Schema，不直接写 `Adaptation Coefficient` 公式。

窝料不写回 `SpatialDistributionWeight`，不直接设置 `Fish Condition`，也不把同一份效果同时作为持久和即时增量重复消费。映射细节见 `candidate/response-stage-mapping.md`。

## WD-17｜最终总聚合公式后置

**状态：BOUNDARY**

目前不强行定义：

```text
RecipeFit = Food + Flavor + Particle + Physical
```

先闭合每条因果链，再检查是否需要 Attraction、Retention、Ingestion、Selection 等多个中间语义，最后接现有 Response / Adaptation Coefficient。

这些中间名称本身仍是 Candidate，不应提前固化成新的正式术语。

## WD-18｜端到端冲突显式登记

**状态：BOUNDARY**

完整中鱼链跨越环境烘焙、鱼况、响应、圆桌、抽鱼和 Fish AI，跨文档、跨候选栈的冲突不能靠某一份 Candidate 自行裁决。冲突与未决项统一登记在 `conflict-register.md`，每项标明出处、影响、暂定处理和裁决方。

本目录任何文档不得把 `KEEP_OPEN` 项写成已确认规则，也不得把 `CANDIDATE_BRANCH` 当成 Owner 裁定。

## WD-19｜Ingredient 固有事实与配方角色分开

**状态：BOUNDARY**

`Ingredient` 提供的是固有事实：可食物质、化学线索潜力、颗粒属性、物理属性。`Base / Target / State / Attractant` 是玩家在这次配方里赋予它的功能角色和配比约束，不是 Ingredient 的固有分类。

同一个虾粉可以在不同配方里被当主攻饵、状态饵或填充料，但它的固有事实不变。不得写成 `Ingredient.Type = TARGET_BAIT`。

## WD-20｜物理颗粒与可食颗粒分开

**状态：BOUNDARY**

窝料固体可以同时包含可食颗粒和不可食 / 载体颗粒。两者都可以有粒径，也都可以参与雾化、扩散和沉降，但只有可食颗粒进入 Size Response。

```text
Recipe solids
├─ Edible particulate matter
│    → Size Response → Edible Utilization
└─ Non-edible / carrier particulate matter
     → Physical Release
     → 不进入 Edible Utilization
```

同一个 Ingredient 也可以同时贡献可食部分和载体部分。第一版不必把数据拆得很细，但语义必须先分开。

## WD-21｜Edible Size 只回答有效利用

**状态：BOUNDARY**

Edible Size 只回答：这份实体可食物，目标鱼以当前体型和摄食方式有多容易有效利用。

它不回答：

- 鱼会不会被吸引过来；
- 鱼愿不愿意留窝；
- 香味强不强；
- 吃了以后饱不饱；
- 中鱼概率是多少。

输出是摄食 / 利用约束，不是 Bite Bonus，也不是最终 Response。

## WD-22｜Groundbait 与 Hookbait 只共享尺寸约束接口

**状态：BOUNDARY**

Groundbait 与 Hookbait 只共享鱼侧尺寸约束接口：体尺、形态、摄食动作能力、对象尺寸 / 状态对动作的影响。

它们不共享完整的 Feeding Place、释放、分布或响应机制。Hookbait 还有入口性、硬度、钩体阻碍、持钩和姿态等额外因素。

## WD-23｜先闭合 Size 前置语义，再做 Gold Fixture

**状态：BOUNDARY**

当前工作项按以下顺序：

1. 修正 Size 所需的三个前置语义：Ingredient 与 Recipe Role、物理颗粒与可食颗粒、Edible Size 输出语义。
2. 立即做窄版 Edible Size Gold Fixture。
3. 如果 Fixture 失败，修 Size Candidate。
4. 到此停止，不进入 Food、Flavor、Attraction、Retention 或完整 Recipe Grammar。

Part A 必须保持很短。如果讨论开始扩张到 Attraction、Retention、Recipe Grammar、Food Taxonomy 或 Flavor Taxonomy，就说明已经偏离 Size blocker。

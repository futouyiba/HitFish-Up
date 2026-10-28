# 台钓配方机制｜已收敛 Working Decisions

> 状态：Working Decision Ledger
> 
> 日期：2026-10-28
> 
> 边界：这里记录本轮讨论中已经相对收敛、后续 Agent 不应无故重新从零争论的工作结论。它们仍不是正式 FCF Contract；若与更高权威 Current / Owner 裁定冲突，以更高权威为准。

## WD-01｜先把 Groundbait 做成第一个完整消费者

先建立薄的 Common Ingredient / Recipe Facts，然后优先用 Groundbait 验证完整机制；Hookbait / 饵球后续复用 Size Response 等共用语言。

原因：当前最不确定、最能暴露配方策略深度的问题主要在 Feeding Place、粒径分布、雾化、黏度、释放、留鱼和补窝。

## WD-02｜Food、Flavor、Particle、Physical Release 分责

- Food：表达有什么可摄食目标。
- Flavor / Chemical Cue：表达鱼感知到什么化学线索。
- Particle Size：表达实体食物尺寸对不同鱼 / 体型的可利用性。
- Physical Release：表达这些信号何时、在哪里、持续多久出现。

禁止把四者默认做成四个并列 Bonus。

## WD-03｜Food 与 Flavor 不是同一个 Target 字典

虫、谷物、甲壳等可摄食目标与腥、奶、果、蒜等化学线索语义不同。Flavor 不直接塞进 Food Target / FeedingTargetKey。

## WD-04｜Food 当前采用“同 Target 先合并，再边际递减”的候选骨架

同作用 Food Target 的 Exposure 先合并，再进入饱和 / 边际递减。这样避免逐 Ingredient 拆分套利，并允许鱼同时喜欢两个 Food Target 时出现有限混配价值。

这条仍需 Gold Fixture 验证，不等于最终数值公式已定。

## WD-05｜Flavor 使用整体画像，不逐味型独立领 Bonus

Flavor 由：

```text
Composition + Intensity
```

描述。加入新味型会改变和稀释原有味型构成。鱼对整体 Flavor Profile 求响应。

## WD-06｜小药是 Chemical Cue Modifier，不是免费 Buff

小药倾向于低剂量、高 Potency，主要改写 Flavor Profile / Intensity。不能简单设计成“基础配方分 + 小药 Bonus”。

## WD-07｜排斥与“不喜欢”分开

- 不喜欢：没有获得明显正收益。
- 排斥：Cue 出现会主动压低响应。

Avoidance 应稀疏配置，不建立全量 Fish × Flavor 负数矩阵。

## WD-08｜雾化、黏度首先属于释放机制

雾化、黏度、比重、颗粒等先影响：

- Breakdown Rate
- Cue Release Rate
- Spatial Spread
- Sinking / Layer Behavior
- Persistence

它们不直接写成中鱼倍率。

## WD-09｜Particle Size 抽成独立 `Edible Size Response`

Groundbait Particle 与 Hookbait / 饵球尺寸共享同一鱼侧 Size Response 语言。

鱼侧主要由：

```text
Body Size
Morphology Profile
Feeding Mechanism Profile
```

生成，不为每条鱼直接手填最佳毫米值。

## WD-10｜Body Size 与 Morphology Ratio 分开

- Body Size 负责个体成长。
- Morphology Ratio 负责同体长下的物种形态差异。

两者共同生成 Intake Reference。Ratio 默认物种级，只有有依据时才用 Growth Stage Override。

## WD-11｜Feeding Mechanism 决定曲线形状，不只是一个倍率

PICK、SUCTION、BENTHIC_SUCTION、GULP、FILTER 等摄食方式应拥有不同标准 Size Response Curve。

FILTER 可以使用独立 Filter Reference，不强行用 Mouth Reference。

## WD-12｜多 Feeding Mechanism 第一版采用 Best Available Path

同一食物对象由多个替代摄食路径处理。第一版倾向：

```text
EdibleSizeFit = max(proficiency_m × curve_m)
```

避免“会的机制越多越强”的叠加套利。是否改为平滑 best-path 留给 Fixture。

## WD-13｜大颗粒可以筛小鱼，但小颗粒不默认强烈排斥大鱼

当前 Size Fit 的强约束主要在右侧：颗粒过大后小鱼无法有效利用。

若后续需要表达“大鱼更愿意留在粗颗粒窝”，优先研究 Retention / Food Value，而不是先给大鱼对 Fine Particle 人为大幅负分。

## WD-14｜天气默认先影响 Feeding Readiness，不直接改 Flavor 密码

“下雨就喜欢腥、晴天就喜欢果香”目前证据不足，不作为现行候选机制。

Diet Shift 若保留，倾向：

```text
Baseline Preference
→ Contextual Shift
→ Slow Bounded Stochastic Drift
```

且后置到 Food / Flavor 本体闭合以后。

## WD-15｜最终总聚合公式后置

目前不强行定义：

```text
RecipeFit = Food + Flavor + Particle + Physical
```

先闭合每条因果链，再检查是否需要 Attraction、Retention、Ingestion、Selection 等多个中间语义，最后接现有 Response / Adaptation Coefficient。

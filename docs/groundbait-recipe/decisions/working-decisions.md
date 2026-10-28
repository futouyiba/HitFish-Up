# 台钓配方机制｜Working Decision Ledger

> 状态：Working Decision Ledger  
> 日期：2026-10-28  
> 边界：这里记录本轮讨论形成的工作决定，并明确区分成熟度。它们仍不是正式 FCF Contract；若与更高权威 Current / Owner 裁定冲突，以更高权威为准。

## 状态说明

- **BOUNDARY**：当前已收敛的设计边界。后续 Agent 不应无故从零重开；若要推翻，应给出新的证据或明确反例。
- **ACTIVE CANDIDATE**：当前最值得验证的算法方案，但仍需 Gold Fixture / 真实数据攻击，不得当作已确认公式。
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

这仍需 Gold Fixture 验证，不等于最终数值公式已定，也不保证混配一定优于单一 Target 专精。

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

## WD-11｜Feeding Mechanism 决定曲线形状，不只是倍率

**状态：ACTIVE CANDIDATE**

PICK、SUCTION、BENTHIC_SUCTION、GULP、FILTER 等摄食方式应允许拥有不同 Size Response Curve；是否全部进入首版仍待 Fixture 和内容需要确认。

## WD-12｜多 Feeding Mechanism 使用 Best Available Path

**状态：ACTIVE CANDIDATE**

当前首测：

```text
EdibleSizeFit = max(proficiency_m × curve_m)
```

目的是避免“会的机制越多越强”的叠加套利。`max` 是否过于尖锐、是否需要平滑 best-path，必须由 Fixture 决定。

## WD-13｜大颗粒筛小鱼；小颗粒不默认强烈排斥大鱼

**状态：ACTIVE CANDIDATE**

当前 Size Fit 的强约束主要放在右侧：颗粒过大后小鱼难以有效利用。

左侧使用机制特定的 `fine_utilization`，不统一降到 0。若后续需要表达“大鱼更愿意留在粗颗粒窝”，优先研究 Retention / Food Value，而不是先给大鱼对 Fine Particle 人为大幅负分。

## WD-14｜天气不直接作为 Flavor 密码

**状态：BOUNDARY**

“下雨就喜欢腥、晴天就喜欢果香”目前证据不足，不作为候选机制。天气、时段等环境输入优先进入现有 Fish Condition / Feeding Readiness / Activity 语义。

Diet Shift 的驱动方式仍是 **OPEN**。若以后保留，可测试 Contextual Shift 和慢、有界、有记忆的随机漂移，但随机漂移本身尚未确认。

## WD-15｜最终总聚合公式后置

**状态：BOUNDARY**

目前不强行定义：

```text
RecipeFit = Food + Flavor + Particle + Physical
```

先闭合每条因果链，再检查是否需要 Attraction、Retention、Ingestion、Selection 等多个中间语义，最后接现有 Response / Adaptation Coefficient。

这些中间名称本身仍是 Candidate，不应提前固化成新的正式术语。

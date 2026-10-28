# 台钓窝料 / 饵料混合机制 Candidate Proposal

> 状态：Candidate / Working Design  
> 日期：2026-10-28  
> 说明：本文记录当前最新整体提案。`decisions/working-decisions.md` 区分已收敛边界与仍待验证的算法候选；本文不把 Candidate 冒充正式 Contract。

## 1. 设计目标

这套机制要让玩家围绕以下问题做配方选择：

1. 目标鱼吃什么。
2. 哪种化学线索 / 味型更容易形成有效刺激。
3. 颗粒尺寸会筛选哪些鱼和哪些体型。
4. 饵料如何在水中释放，决定开窝速度、扩散范围、沉降位置和持续时间。
5. 小药、状态饵和主攻饵之间存在真实机会成本，而不是免费叠加 Buff。

目标不是制造一个隐藏的“最佳 RecipeFit 公式”，而是让配方的不同组成承担不同职责，并能被玩家观察、试验和学习。

## 2. 总体因果结构

```text
Ingredient / Recipe
        ↓
Source Facts
├─ Food Identity
├─ Flavor / Chemical Cue Potential
├─ Particle Distribution
└─ Physical Properties
        ↓
Physical Release
├─ Breakdown Rate
├─ Cue Release Rate
├─ Spatial Spread
├─ Sinking / Layer Behavior
└─ Persistence
        ↓
Feeding Place
├─ Available Food
├─ Chemical Cue Field
└─ Particle State
        ↓
Fish Interpretation
├─ Food Preference
├─ Flavor Preference
├─ Sparse Avoidance
├─ Edible Size Response
└─ Fish Condition
        ↓
Response
        ↓
现有下游 Adaptation Coefficient / 权重链
```

关键边界：Food、Flavor、Particle、Physical Release 不是四个并列 Bonus。Physical Release 先决定信号何时、在哪里、以什么强度出现；Fish Response 再解释这些状态。

## 3. Common Ingredient / Recipe Facts

第一版 Ingredient 建议至少提供以下事实，不直接提供“鲤鱼 +0.8”一类鱼种总分：

| 类别 | 示例 | 主要用途 |
|---|---|---|
| Food Identity | 谷物、虫、甲壳、植物、藻类等 | 鱼对可摄食目标的偏好 |
| Flavor / Chemical Cue Potential | 腥、谷香、奶、果、蒜等及其强度 | 生成 Chemical Cue Exposure |
| Particle Properties | 粒径分布、颗粒形态 | 尺寸筛选和释放 |
| Physical Properties | 黏性、溶散倾向、比重等 | 生成释放过程 |
| Potency / Quality | Ingredient 自身强度 | 区分同类 Ingredient，不直接等于鱼种响应 |

同一个 Ingredient 可以同时贡献多类事实。例如虾粉既可能贡献甲壳类 Food Identity，也贡献腥味 Chemical Cue Potential，还具有自己的粒径和物理性质。

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

- Target 字典如何定义。
- `k` 等饱和参数如何标定。
- Food Target 是否完全来自可摄食目标，还是还需拆更多语义。
- 最终 Food Response 如何进入更高层响应。

## 5. Flavor：由 Cue Exposure 形成整体味型画像

### 5.1 当前候选

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

## 6. Particle Size：单独建立 Edible Size Response

颗粒大小不是 Food 或 Flavor Bonus。它主要解决：

> 这条鱼以当前线性体尺、摄食形态和摄食方式，能否有效利用这个尺寸的实体食物。

完整 Candidate 见 `edible-size-response.md`。

当前核心结构：

```text
Body Linear Size
+ Morphology Profile
→ Intake Reference

Intake Reference
+ Feeding Mechanism Curve
→ Mode Size Fit

多个可替代 Feeding Mechanism
→ Best-path Candidate
→ Edible Size Fit
```

`Body Linear Size` 必须是体长等线性尺度。重量不能直接与无量纲 Ratio 相乘生成长度。

Groundbait 用粒径分布求可利用份额；Hookbait 后续可用单颗饵球尺寸复用“Size Fit”语言，但 Hookbait 还会有入口性、硬度、持钩、姿态等其它因素，不等于整套 Groundbait Response 直接复用。

## 7. Physical Release：雾化、黏度不是直接中鱼系数

### 7.1 当前职责

雾化、黏度、比重、粒径等先决定或参与决定：

- 解体速度；
- Chemical Cue 释放速度；
- Food / Particle 空间扩散；
- 沉降和所在水层；
- 局部留存和持续时间。

这些结果再形成 Feeding Place 的时空状态。当前不预设“某个物理属性越高越好”，也不把“高黏度必然更集中”等尚未验证关系写成硬规则。

### 7.2 需要验证的策略故事

- 快速开窝 vs 长时间守窝；
- 快速扩散、容易发现 vs 集中、持久；
- 细颗粒提高广泛利用 / 频率 vs 粗颗粒提高体型筛选；
- 高释放可能带来杂鱼和维护成本，而非单向增益；
- 状态饵占据固体份额，用物理效果换取 Food / Flavor 机会成本。

这些是策略目标，不是已完成公式。

## 8. Fish Condition 与 Diet Shift

### 8.1 当前较稳边界

天气、时段等环境输入优先通过现有 Fish Condition / Feeding Readiness / Activity 语义影响“现在愿不愿意响应”。

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

## 9. 不急于定义单一 RecipeFit

当前不为了公式整齐而直接写：

```text
RecipeFit = FoodFit + FlavorFit + ParticleFit + PhysicalFit
```

原因：这些量不一定处于同一阶段，简单相加可能重复计权。

后续需要检验是否应保留不同语义，例如：

- Attraction：鱼是否被信号吸引 / 发现。
- Retention：鱼是否愿意持续留在 Feeding Place。
- Ingestion：实体食物是否容易被有效摄食。
- Selection：鱼种和体型如何被筛选。

这些名称本身也仍是 Candidate；最后再决定如何映射到现有 Response / Adaptation Coefficient。

## 10. 首轮 Recipe Grammar 候选

以下只作为 Fixture 范围，不是平衡定值：

| 角色 | 候选限制 |
|---|---|
| Base | 1 槽，约 50–70% 固体质量 |
| Target Bait | 1–2 槽，总计约 20–40% |
| State Ingredient | 0–1 槽，0–20%，占固体质量 |
| Attractant / 小药 | 0–1 槽，独立剂量但必须有上限 / 成本 |
| 固体总量 | 100% |
| 玩家配比步长 | 5% 或“份”优先，避免精确数学极值玩法 |

## 11. 推荐推进顺序

1. 凿实 `Edible Size Response`。
2. 建立小型 Gold Fixture，攻击尺寸模块。
3. 用真实代表鱼生成 Morphology / Feeding Mechanism 参数，验证 authoring 路径。
4. 接 Groundbait Particle Distribution。
5. 设计 Physical Release，把雾化、黏度等变成时空释放。
6. 回到 Food Target，验证单品统治、多 Target 拼盘、拆分套利。
7. 完成 Flavor / 小药 / Sparse Avoidance。
8. 形成 Groundbait 完整玩法闭环。
9. Hookbait / 饵球复用 Edible Size Response 中的尺寸响应语言。
10. 最后再收 Diet Shift 与 Response Aggregation。

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
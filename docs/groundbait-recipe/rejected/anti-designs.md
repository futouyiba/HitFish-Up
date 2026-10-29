# 台钓配方机制 Anti-designs / 当前排除方向

> 状态：Rejected / Deferred Design Boundaries
> 日期：2026-10-29
> 用途：记录已经讨论过、当前不应被后续 Agent 直接重新采用的退化方案。这里只保留“为什么不能这么做”的承重结论，不保存聊天流水账。`Deferred` 表示首版不采用，不代表永久禁止。

## 1. 全 Ingredient 线性加权作为完整方案

```text
Q_f = Σ share_i × E[i,f]
```

### 为什么不采用

在固定预算、单目标鱼情况下，最优解通常把全部可分配份额给单位系数最高 Ingredient。混配只是在两个端点之间做加权平均，容易退化为查表题。

### 保留什么

线性 Exposure 仍可作为更底层的局部聚合步骤，但不能单独承担完整 Recipe Strategy。

---

## 2. 逐 Ingredient 独立饱和

```text
Q = Σ_i Sat(share_i × effect_i)
```

### 为什么排除

等效成分拆成多个 ID 后会重复重置饱和曲线，导致“拆分套利”。实际信号没增加，但输出变强。

### 当前边界

若使用饱和，必须先在等效作用语义上完成合并，再进入饱和。

---

## 3. 所有 Food / Flavor Target 各自饱和后直接求和

### 为什么不采用统一方案

虽然能缓解单品统治，但会产生新的退化策略：每个有效 Target 都塞一点，形成“多 Target 全家桶”。

Flavor 尤其不适合按“腥 + 奶 + 果 + 蒜各领一份 Bonus”的方式累加。

### 当前替代

- Food：Active Candidate 为同 Target 合并 + 边际递减，并用稀疏偏好和有限 Recipe Grammar 做 Fixture 攻击。
- Flavor：先由 Ingredient 用量 / 剂量与 Cue Potency 生成 Cue Exposure，再得到整体 Composition + Intensity。

---

## 4. `FoodFit + FlavorFit + PhysicalFit + ParticleFit` 直接相加

### 为什么排除

这些量并不处在同一因果阶段。简单相加会把同一 Ingredient 的“是食物”“有某味型”“释放得快”等事实重复计权，也会让 Physical Property 变成隐藏 Bonus。

### 当前替代

Physical Release 先改变 Feeding Place 的时空状态，Fish Response 再解释这些状态。最终是否需要单一 RecipeFit 尚未决定。

---

## 5. 小药 = 固定额外 Bonus

```text
RecipeScore = BaseRecipeScore + AttractantBonus
```

### 为什么排除

若小药不占主体质量预算、只提供正收益且合法剂量内没有真实代价，则“加满一个小药”会严格支配“不加”。Dose Cap 只能限制幅度，不能解决支配关系。

### 当前替代

小药作为高 Potency 的 Chemical Cue Modifier，改变 Cue Exposure / Flavor Profile / Intensity；新味型可能改善，也可能破坏原配方。

---

## 6. 状态饵 = 免费 Buff

### 为什么排除

状态饵若既不占固体预算，又直接提供雾化、持续时间或中鱼加成，则没有机会成本，会成为固定必选项。

### 当前替代

状态饵占固体质量份额，用 Food / Flavor 机会成本换取物理性质和释放行为。

---

## 7. 雾化 / 黏度直接映射中鱼倍率

例如：

```text
高雾化 → Bite +20%
高黏度 → Bite +10%
```

### 为什么排除

这种做法无法解释什么时候高雾化是坏事，也无法形成开窝、守窝、杂鱼、补窝频率等策略。

### 当前替代

雾化、黏度等先影响 Breakdown / Release / Spread / Sinking / Persistence。具体物理关系仍需后续 Fixture，不能把“高黏度一定更集中、更持久”提前写死。

---

## 8. 每条鱼手填“最佳粒径 X mm”

### 为什么排除

- 参数量大。
- 容易出现假精度。
- 同一鱼种成长后需要重复配置。
- 难以说明数据来源。

### 当前替代

Body Linear Size + Morphology Profile + Feeding Mechanism Catalog 生成默认 Size Response；少量关系 Override。

---

## 9. Runtime 直接使用万能 `particle < mouth × constant`

### 为什么排除

嘴部 / gape 是重要上游证据，但不是所有摄食方式的完整解释。滤食、吸食、吞食等对尺寸的响应曲线形状不同；FILTER 甚至可能更直接依赖鳃耙 / 过滤结构，而不是 Mouth Reference。

### 当前替代

普通口部路径可以由线性体尺与 Oral Morphology 生成 Intake Reference，再由 Feeding Mechanism Curve 解释。FILTER 允许从独立 Filter Morphology 生成 Reference / Efficiency Window。

---

## 10. 多 Feeding Mechanism 直接求和

```text
Fit = suction_fit + pick_fit + gulp_fit
```

### 为什么排除

会的摄食方式越多就越强，产生机制数量套利。多个 Feeding Mechanism 对同一食物对象主要是替代处理路径，不是多份独立奖励。

### 当前替代

首轮 Fixture 测试 best available path：

```text
EdibleSizeFit = max(proficiency_m × mode_curve_m)
```

`max` 本身仍是 Active Candidate；若过于尖锐，再测试平滑 best-path，而不是退回直接求和。

---

## 11. 纯高维向量空间统一 Food / Flavor / Physical

例如把 Ingredient 和 Fish 都写成不可解释的高维向量，再做 cosine similarity。

### 为什么当前不采用

- 缺少训练数据。
- 人工 author 高维向量只是把配表藏进数学空间。
- Debug 难以回答“为什么这条鱼喜欢这份配方”。
- 容易发生不同维度之间的无意义补偿。

### 当前保留的局部向量思想

Flavor Profile 可以看作低维、显式、有业务语义的 Composition Vector。当前排除的是“不可解释的统一高维 embedding”，不是所有向量运算。

---

## 12. 天气直接作为味型密码

例如：

```text
下雨 → 腥 +30%
晴天 → 果香 +20%
```

### 为什么当前排除

现有证据不足以支持这种普遍直接因果，而且很容易形成新的明牌查表。

### 当前边界

天气、时段等优先进入现有 Fish Condition / Feeding Readiness / Activity 语义。Diet Shift 的具体驱动仍是 Open；不能把“慢随机漂移”提前写成已确认替代方案。

---

## 13. 每杆随机 Diet Preference

### 为什么排除

玩家无法观察、推理和学习，只能试密码或查外部攻略。

### 当前边界

若未来引入随机漂移，它至少应慢、连续、有边界、有记忆；是否需要随机漂移本身仍待验证。

---

## 14. 任意 Ingredient × Ingredient Pair Synergy 首版铺表

### 为什么后置

Pair Table 很快进入 N² 内容维护，且容易用隐藏 Bonus 掩盖原本没有闭合的 Food / Flavor / Physical 机制。

### 当前边界

先验证 Food Target Saturation、Flavor Composition、Physical Release 是否已经产生足够策略。只有明确发现无法表达的重要组合关系时，才考虑极少数有证据的组合规则。

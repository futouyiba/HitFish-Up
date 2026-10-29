# Groundbait Particle Distribution｜颗粒分布 Candidate

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 权威边界：本页不是 FCF Current Contract，也不替代现有 Response / Condition 语义。

## 1. 颗粒分布描述什么

Particle Distribution 不是一条“配方粒径得分”。它描述窝料固体从配方事实到 Feeding Place 当前状态的变化，并区分两个不同用途：

```text
Recipe solids
├─ Physical Particle Distribution
│    → Physical Release / 沉降 / 扩散 / 留存
└─ Edible Particle Distribution
     → Size Response → Edible Utilization
```

两者可以有共同底层数据，但语义分开。载体、黏结料、泥和不提供营养的颗粒可以有粒径，也可以参与释放，但不能因为尺寸合适就进入可食利用。

## 2. 两层分布

```text
Recipe solids
├─ Physical Particle Distribution(recipe)
│    → 释放 / 沉降 / 解体 / 消耗
│    → Available Physical Particle Distribution(place, t)
│
└─ Edible Particle Distribution(recipe)
     → 释放 / 沉降 / 解体 / 消耗
     → Available Edible Particle Distribution(place, t)
     → Size Response
     → Edible Utilization(f, place, t)
```

第一层是配方事实，第二层是 Feeding Place 当前状态，第三层是鱼侧尺寸响应。不能拿投放时的固体百分比直接冒充当前可食分布。

### 2.1 最小对象描述

```text
ParticleObject
├─ effective_size
├─ edible_mass_or_value
├─ carrier_mass_or_value
├─ shape / hardness / cohesion
└─ location / release_state
```

`effective_size` 是对当前动作有意义的尺寸。对松散团块、纤维或不规则对象，它不一定等于筛网粒径；如何生成仍是 OPEN。对象状态不能偷偷编码进尺寸值。

## 3. 从 Ingredient 到配方分布

每个 Ingredient 至少提供：

```text
IngredientParticleFacts
├─ edible_fraction_of_ingredient
├─ physical_size_distribution
├─ edible_size_distribution (optional)
└─ carrier_note (optional)
```

Recipe 按质量份额混合。对每个尺寸桶 `b`：

```text
physical_share_b
  = Σ_i recipe_share_i × physical_dist_i(b)

edible_mass_i
  = recipe_share_i × edible_fraction_i

edible_fraction_of_solids
  = Σ_i edible_mass_i

edible_share_b
  = Σ_i edible_mass_i × edible_dist_i(b)
    / edible_fraction_of_solids

carrier_fraction
  = 1 - edible_fraction_of_solids
```

约束：

1. `recipe_share_i` 在配方内部求和为 1；
2. `edible_fraction_i ∈ [0, 1]`；
3. `physical_dist_i` 在单个 Ingredient 内部求和为 1；
4. `edible_dist_i` 在单个 Ingredient 的可食部分内部求和为 1；
5. `edible_fraction_i = 0` 时，该 Ingredient 不贡献可食分布；
6. 若省略 `edible_size_distribution`，可以退化为使用 `physical_size_distribution`，但必须标记为假设；
7. `edible_fraction_of_solids = 0` 时，`edible_share` 未定义，不进入 Size Response。

这一步只生成配方分布，不生成当前地点分布。

## 4. 从配方分布到 Feeding Place

用一个状态转换表示：

```text
T: RecipeDistribution × place × t × environment
  → AvailableDistribution(place, t)
```

对每个尺寸桶和每个账本，`T` 把投放量分成四份：

```text
recipe_mass_b
  = available_b
  + left_place_b
  + consumed_b
  + unprocessable_b
```

分别对物理账本和可食账本成立。载体账本可以单独记，也可以从物理账本减去可食账本得到。

`T` 内部的物理关系仍是 OPEN：解体速度、沉降、漂移、暴露时间和被摄食速度都没有生产公式。本页只固定：

- 输入是配方分布；
- 输出是当前地点的可用分布；
- 四份之和守恒；
- 可食账本不混入载体。

## 5. Feeding Place State 与守恒账本

```text
FeedingPlaceState(place, t)
├─ available_physical_bins
├─ available_edible_bins
├─ contactable_share
├─ object_state
└─ provenance
```

`contactable_share` 是当前地点可被鱼接触的比例，不是配方份额。它由位置、水层、沉降和扩散决定，具体规则属于 Physical Release。

守恒账本示例，按 100 g 固体计：

| 账本 | 投放 | 可用 | 离开地点 | 被摄食 | 不可处理 | 合计 |
|---|---:|---:|---:|---:|---:|---:|
| 物理 | 100.0 | 80.0 | 12.0 | 5.0 | 3.0 | 100.0 |
| 可食 | 74.0 | 59.2 | 8.9 | 3.7 | 2.2 | 74.0 |
| 载体 | 26.0 | 20.8 | 3.1 | 0.0 | 2.1 | 26.0 |

这些数字只用于检查账本，不是生产参数。

## 6. 结构 Fixture

三份配方只改变可食组成或载体份额，用来检查语义是否分开。

### 6.1 配方

| 配方 | Base | Target | Carrier |
|---|---|---|---|
| A | 70%，可食 0.80，1 / 2 mm 各半 | 20%，可食 0.90，5 mm | 10%，可食 0，0.5 mm |
| B | 56%，可食 0.80，1 / 2 mm 各半 | 16%，可食 0.90，5 mm | 28%，可食 0，0.5 mm |
| C | 70%，可食 0.80，1 / 2 mm 各半 | 20%，可食 0.90，0.5 mm | 10%，可食 0，0.5 mm |

### 6.2 生成结果

| 配方 | 可食比例 | 物理分布（0.5 / 1 / 2 / 5 mm） | 可食分布（0.5 / 1 / 2 / 5 mm） |
|---|---:|---|---|
| A | 0.74 | 0.10 / 0.35 / 0.35 / 0.20 | 0.00 / 0.378 / 0.378 / 0.243 |
| B | 0.592 | 0.28 / 0.28 / 0.28 / 0.16 | 0.00 / 0.378 / 0.378 / 0.243 |
| C | 0.74 | 0.30 / 0.35 / 0.35 / 0.00 | 0.243 / 0.378 / 0.378 / 0.00 |

读法：

- B 增加了载体，物理分布在 0.5 mm 处明显上升，但可食分布不变。
- C 把 Target 从 5 mm 移到 0.5 mm，物理分布和可食分布都改变。

### 6.3 尺寸利用

用 `edible-size-gold-fixture.md` 的 PICK 和 BENTHIC 曲线：

| 配方 | Small Pick（参考 6 mm） | Large Benthic（参考 36 mm） |
|---|---:|---:|
| A | 0.94 | 0.74 |
| B | 0.94 | 0.74 |
| C | 0.85 | 0.61 |

结构行为：

- A 到 B 只增加载体，载体不进入可食分布，所以两个鱼的结果都不变。
- A 到 C 把可食 Target 移细，两个鱼的结果都下降，因为 0.5 mm 对它们的动作效率都低于 5 mm。
- 物理分布可以变化而鱼侧可食利用不变，说明两个账本没有混在一起。

这些读数只证明结构，不是生产参数。

## 7. 退化测试

1. **配方份额守恒**：三份配方的 `recipe_share` 求和为 1；不等于 1 时报错，不自动归一化。
2. **Ingredient 拆分不变**：把 Base 拆成两个同分布 Ingredient，结果不变。
3. **载体隔离**：只增加载体份额，`EdibleUtilization` 不变；物理分布可以改变。
4. **可食比例边界**：`edible_fraction_of_solids = 0` 时，不产生可食分布，也不进入 Size Response。
5. **桶拆分不变**：把 1 mm / 0.378 拆成两个 1 mm 桶各 0.189，结果不变。
6. **状态守恒**：任一时点，`available + left + consumed + unprocessable = recipe`，物理账本和可食账本分别成立。
7. **摄食后更新**：可食对象被摄食后，必须从 `available_edible_bins` 减少或转为已消耗，不能保留完整价值。

## 8. 粒径改变了什么，没改变什么

粒径可以同时影响多个环节，但影响方式不同：

- 在鱼侧：改变可食颗粒的捕获、吸入、留住和处理难度；
- 在物理侧：改变沉降、解体、扩散、局部留存和暴露时间；
- 在资源侧：改变单位可食颗粒或载体颗粒的质量、数量或能量结构。

这些影响不能合并成一个 Particle Bonus。特别是：

- “小鱼难处理大颗粒”是动作可行性 / 成功约束；
- “大颗粒更久留在底部”是 Physical Release 假设；
- “大颗粒让鱼更愿意留下”是更高层 Retention 假设。

只有第一项直接属于本模块与 Edible Size 的连接。

## 9. 未收口问题

- 对象的有效尺寸如何从不规则形态、团聚和解体状态生成；
- 载体 / 不可食颗粒与可食颗粒的占比如何从 Ingredient 数据生成；
- 是否可以省略 `edible_size_distribution`，直接复用物理分布；
- `T` 的解体、沉降、漂移和摄食速率如何标定；
- Groundbait 的对象价值最终按质量、数量、能量还是接触机会表示；
- 同一粒径是否因硬度、形状和状态而进入不同动作路径；
- 是否需要显式建模颗粒间的团聚，而不是把它当作一个静态粒径桶。
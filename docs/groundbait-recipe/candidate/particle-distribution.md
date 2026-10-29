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

## 3. 当前工作接口

在没有更完整的对象模型时，可用离散桶近似当前 Feeding Place：

```text
Available Physical Distribution(place, t) = {physical bins with contactable share}
Available Edible Distribution(place, t)   = {edible bins with contactable share}
```

鱼侧尺寸响应只读取可食分布：

```text
EdibleUtilization_f
  = Σ_i edible_share_i(place, t) × SizeFit_f(size_i, state_i)
```

其中 `edible_share` 在可食部分内部求和为 1，不包含载体和不可食颗粒。若需要绝对可食质量，再显式乘 `edible_fraction_of_solids × total_solids`。

物理释放读取物理分布，解释对象何时、在哪里、以什么状态出现。一次摄食事件从可食分布中遇见对象，再交给 `feeding-event.md` 定义的事件状态机：

```text
object bin
  → encounter opportunity
  → feasible action set
  → selected action
  → action success
  → object state update
```

对象价值可以是质量、数量、能量或其它明确计量，但一次实现只能先钉定一种口径，不能在不同模块间静默切换。

## 4. 粒径改变了什么，没改变什么

粒径可以同时影响多个环节，但影响方式不同：

- 在鱼侧：改变可食颗粒的捕获、吸入、留住和处理难度；
- 在物理侧：改变沉降、解体、扩散、局部留存和暴露时间；
- 在资源侧：改变单位可食颗粒或载体颗粒的质量、数量或能量结构。

这些影响不能合并成一个 Particle Bonus。特别是：

- “小鱼难处理大颗粒”是动作可行性 / 成功约束；
- “大颗粒更久留在底部”是 Physical Release 假设；
- “大颗粒让鱼更愿意留下”是更高层 Retention 假设。

只有第一项直接属于本模块与 Edible Size 的连接。

## 5. 输入守恒与数据边界

当前候选输入：

```text
ParticleDistribution
├─ physical_bins: [{effective_size, physical_share}]
├─ edible_bins: [{effective_size, edible_share}]
├─ edible_fraction_of_solids
├─ object_state: optional
└─ provenance: required
```

约束：

1. `effective_size > 0`；
2. `physical_share >= 0`，在全部固体内部求和为 1；
3. `edible_share >= 0`，在可食部分内部求和为 1；
4. `edible_fraction_of_solids ∈ [0, 1]`，载体份额为 `1 - edible_fraction_of_solids`；
5. 释放后重新形成的 `Available Physical Distribution` 和 `Available Edible Distribution` 不得伪装成投放时原始分布；
6. 缺少形状、硬度或状态证据时，不能把它们偷偷编码进尺寸值；
7. 摄食事件成功后，对象价值必须从后续 Feeding Place 状态中减少或转为已消耗状态。

首轮可以用质量份额作为工作计量，但应把它标为 `MassShareProjection`，而不是写成最终机制单位。

## 6. 必须保留的退化检查

- 同一对象桶拆分或合并，不应改变事件输入；
- 复制一个动作路径不能增加单次对象收益；
- 只改变释放位置 / 时间时，不能直接改写对象的固有尺寸约束；
- 只改变对象尺寸时，不能顺手改变其释放速度，除非明确声明这是 Physical Release 的联动；
- 投放份额与当前可接触份额必须能被区分；
- 粒径分布变化只有在改变了当前对象集合或动作约束时，才应改变下游结果；
- 对象被摄食后不能继续以完整价值存在。

## 7. 未收口问题

- 对象的有效尺寸如何从不规则形态、团聚和解体状态生成；
- 载体 / 不可食颗粒与可食颗粒的占比如何从 Ingredient 数据生成；
- Groundbait 的对象价值最终按质量、数量、能量还是接触机会表示；
- 同一粒径是否因硬度、形状和状态而进入不同动作路径；
- 被释放、沉降、扩散和摄食消耗后的分布如何在 Feeding Place 中保存；
- 是否需要显式建模颗粒间的团聚，而不是把它当作一个静态粒径桶。

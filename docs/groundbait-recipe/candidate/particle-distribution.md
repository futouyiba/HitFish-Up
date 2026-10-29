# Groundbait Particle Distribution｜颗粒分布 Candidate

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 权威边界：本页不是 FCF Current Contract，也不替代现有 Response / Condition 语义。

## 1. 颗粒分布描述什么

Particle Distribution 不是一条“配方粒径得分”。它描述实体食物对象从配方事实到 Feeding Place 当前状态的变化，并为一次摄食事件提供对象输入。

```text
Recipe Particle Distribution
  → Physical Release / State Transition
  → Available Particle Distribution(place, t)
  → Feeding Event
```

它供两个不同过程消费：

- Physical Release：解释对象何时、在哪里、以什么状态出现；
- Feeding Event / Edible Size：解释鱼遇到对象后，哪些动作可行、哪些动作能成功。

所以同一份投放配方，在不同时间和地点的有效分布可以不同。沉降、解体、漂移、被吃掉和失去可处理状态都会改变当前对象集合。

## 2. 从投放配方到 Feeding Place

应区分三层：

```text
Recipe Particle Distribution
        ↓ 物理释放 / 沉降 / 解体 / 消耗
Available Particle Distribution(place, t)
        ↓ 遇见与动作路径
Effective Ingestion Opportunity(f, place, t)
```

第一层是配方事实；第二层是 Feeding Place 状态；第三层是一次或一段时间内摄食事件的候选输出。不能拿第一层的质量百分比直接冒充第三层。

### 2.1 最小对象描述

```text
ParticleObject
├─ effective_size
├─ declared_value
├─ shape / hardness / cohesion
└─ location / release_state
```

`effective_size` 是对当前动作有意义的尺寸。对松散团块、纤维或不规则对象，它不一定等于筛网粒径；如何生成仍是 OPEN。对象状态不能偷偷编码进尺寸值。

## 3. 当前工作接口

在没有更完整的对象模型时，可用离散桶近似当前 Feeding Place：

```text
P(place, t) = {object bins with contactable share}
```

桶只提供对象分布，不提供鱼种响应。一次摄食事件从桶中抽取或遇见对象，再交给 `feeding-event.md` 定义的事件状态机：

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

- 在鱼侧：改变捕获、吸入、留住和处理的难度；
- 在物理侧：改变沉降、解体、扩散、局部留存和暴露时间；
- 在资源侧：改变单位对象的质量、数量或能量结构。

这些影响不能合并成一个 Particle Bonus。特别是：

- “小鱼难处理大颗粒”是动作可行性 / 成功约束；
- “大颗粒更久留在底部”是 Physical Release 假设；
- “大颗粒让鱼更愿意留下”是更高层 Retention 假设。

只有第一项直接属于本模块与 Edible Size 的连接。

## 5. 输入守恒与数据边界

当前候选输入：

```text
ParticleDistribution
├─ bins: [{effective_size, declared_value_share}]
├─ object_state: optional
└─ provenance: required
```

约束：

1. `effective_size > 0`；
2. `declared_value_share >= 0`；
3. 份额总和代表明确的对象价值空间；若要求总和为 `1.0`，必须说明这是哪一层的分布；
4. 释放后重新形成的 `Available Particle Distribution` 不得伪装成投放时原始分布；
5. 缺少形状、硬度或状态证据时，不能把它们偷偷编码进尺寸值；
6. 摄食事件成功后，对象价值必须从后续 Feeding Place 状态中减少或转为已消耗状态。

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
- Groundbait 的对象价值最终按质量、数量、能量还是接触机会表示；
- 同一粒径是否因硬度、形状和状态而进入不同动作路径；
- 被释放、沉降、扩散和摄食消耗后的分布如何在 Feeding Place 中保存；
- 是否需要显式建模颗粒间的团聚，而不是把它当作一个静态粒径桶。

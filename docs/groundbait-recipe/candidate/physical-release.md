# Physical Release｜物理释放 Candidate

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 权威边界：本页不是 FCF Current Contract；它只描述配方状态如何成为 Feeding Place 状态。

## 1. 物理释放的职责

Physical Release 不是“窝料的强弱分”。它是一个状态转换：

```text
Recipe / Ingredient Facts
        ↓
投放后物理过程
        ↓
Feeding Place State(place, t)
```

它回答的是：

- 哪些实体食物对象在什么时候出现；
- 这些对象位于什么空间 / 水层；
- 对象是完整、解体、悬浮、沉降还是已失去可处理状态；
- 化学线索和实体食物分别以什么时间形状可被感知。

它不直接回答鱼会不会被吸引、会不会留存或会不会吞食。

## 2. 必须区分的状态

最小 Feeding Place 状态不应压成一个 `release_score`，至少包含：

```text
FeedingPlaceState(place, t)
├─ contactable_food_objects
├─ chemical_cue_field
├─ location / layer
├─ object_state
└─ persistence / turnover
```

其中：

- `contactable_food_objects` 供 Particle Distribution 和 Feeding Event 消费；
- `chemical_cue_field` 供 Flavor / Chemical Cue 消费；
- `location / layer` 决定鱼和摄食动作是否有机会接触；
- `object_state` 决定对象是否仍是可处理实体；
- `persistence / turnover` 描述状态如何随时间消失或补充。

化学线索与实体食物可以共享部分物理来源，但不能默认拥有同一条释放曲线。两者的“出现”也不等于同一件事。

## 3. 输入不是一组直接加权的旋钮

候选输入包括：

```text
RecipePhysicalFacts
├─ cohesion / binder tendency
├─ water interaction
├─ density relation
├─ particle object distribution
├─ dose / amount
└─ environmental conditions
```

这些输入先改变解体、沉降、漂移、局部聚集和暴露时间，再形成 Feeding Place 状态。不能写成：

```text
high_binder → +Retention
high_breakdown → +Attraction
```

因为同一物理变化可能同时扩大暴露、缩短留存、改变水层或降低实体食物可处理性，最终方向取决于鱼、地点和时间窗口。

## 4. 因果链

当前最小机制骨架是：

```text
物理性质
  → 对象 / 线索的释放与迁移
  → Feeding Place 中的可接触状态
  → 鱼的发现、动作可行性和摄食利用
```

粒径在这里有两种不同身份：

1. 作为实体对象属性，进入 `Edible Size Response`；
2. 作为物理对象属性，影响沉降、解体和暴露。

如果同一粒径影响两边，必须通过两个不同的中间状态进入，不能给粒径一个跨链总系数。

## 5. 可接受的工作模型

当前只需要保留状态转移的接口，不需要先编造生产参数：

```text
release(recipe_facts, environment, t)
  → FeedingPlaceState(place, t)
```

对任何候选实现，至少应能回答：

- 输入的实体食物总量去了哪里；
- 哪部分仍在 Feeding Place；
- 哪部分变成不可接触、不可处理或离开空间；
- 化学线索的来源与实体食物是否一致；
- 变化是时间变化、空间变化，还是对象状态变化。

这些问题比“快开窝 / 慢开窝哪个分数高”更基础。没有回答它们，就不能把曲线或标签升级为机制。

## 6. 机制边界

### 不属于本模块的直接结论

- 高雾化必然更容易中鱼；
- 高黏度必然更集中或更持久；
- 释放量越大最终 Response 越高；
- 状态饵可以在不占用 Food / Flavor 预算的情况下免费增强配方。

### 当前 Working Hypothesis

- 释放首先改变 Feeding Place 中鱼能遇到什么，而不是改变鱼的固有偏好；
- 快速释放与长期局部留存是不同的时间空间策略，不能用一个总分替代；
- 状态材料占据配方资源，应通过物料与释放状态进入，而不是固定 Bonus；
- 实体食物与化学线索的释放可以错位，这种错位可能是机制的一部分。

### OPEN

- Feeding Place 状态需要多细的空间、时间和水层分辨率；
- 哪些物理量可由现有 Ingredient Facts 取得，哪些需要实验或 Owner 输入；
- 对象的“可接触”和“可处理”是否应分开建模；
- 释放后的 Feeding Place 如何与现有 Response / Condition Contract 对接；
- 颗粒团聚和解体是否需要显式对象生命周期。

## 7. 最小验证要求

1. `FeedingPlaceState(place, t)` 只产生接触机会、对象状态、位置和线索场；不能直接产生最终 Response。
2. 同一总物料只改变释放速度时，改变的是时间分布，不是凭空增加物料。
3. 只改变空间位置时，改变的是接触机会，不直接改写鱼的尺寸曲线。
3. 只改变对象状态时，若影响摄食，必须经对象处理约束进入，不能伪装成化学吸引。
4. 线索释放与食物释放可以不同步，模型不能强迫二者相等。
5. 改变物理释放不能绕过 Feeding Place 直接生成最终 Response。

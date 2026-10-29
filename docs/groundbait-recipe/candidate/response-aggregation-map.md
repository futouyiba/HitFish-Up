# Response Aggregation Map｜最终聚合接口 Candidate

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页只定义窝料候选输出如何进入现有 Response Stage。它不定义 `Adaptation Coefficient` 公式，也不创建新的总分。

## 1. 目的

前面的步骤分别得到：

- Food 响应；
- Flavor 结果；
- Edible Utilization；
- Feeding Place State 与 Physical Release 状态。

本页回答最后一个问题：

> 这些输出如何进入现有 Response Stage，而不是被压成一个 `RecipeFit = Food + Flavor + Particle + Physical`？

结论先给：

- 不建立单一 `RecipeFit`。
- 候选只提供输入。
- 最终聚合仍由现有 Response Stage 完成：

```text
SpatialDistributionWeight × AdaptationCoeff
→ 下游候选权重
```

- `AdaptationCoeff` 的具体公式仍是 OPEN，不由本页定义。

## 2. 现有 Current 边界

`docs/terminology.md` §5.2 定义：

```text
SpatialDistributionWeight
+ Fish Condition
+ Response Components
+ Presentation Signal
→ 响应评价
→ 下游候选权重

可表达为：
SpatialDistributionWeight × AdaptationCoeff
→ 下游候选权重
```

因此本页只能做三件事：

1. 把候选输出映射到现有输入槽位；
2. 定义求值顺序；
3. 定义不能做的合并方式。

不能做：

- 定义 `AdaptationCoeff` 的乘加公式；
- 把候选输出直接写成最终概率；
- 改写 `SpatialDistributionWeight`；
- 把 `Fish Condition` 当作候选的自由输出槽位。

## 3. 输入映射

| 候选输出 | 进入的槽位 | 角色 | 不能做 |
|---|---|---|---|
| Feeding Place State（对象、线索、位置、状态） | Response Condition / 上下文 | 决定当前有什么可被评价 | 不直接变成系数 |
| Food 响应 | Response Component | 选择或对象价值的修正 | 不改尺寸成功、不改释放 |
| Flavor 结果 | Response Component | 发现、趋近、选择或回避的修正 | 不改尺寸成功、不改释放 |
| Edible Utilization | Response Component | 摄食 / 利用的修正 | 不改发现、不改偏好 |
| Physical Release 状态（`A/L/U/Q`） | Response Condition / 上下文 | 可用性、位置、持久性 | 不直接乘进响应 |
| 持久释放部分 | Persistent Response Field | 持续增量 | 不复制 DEF，不与即时重复 |
| Fish Condition | 现有条件输入 | 只读状态 | 不由窝料写入 |
| Presentation Signal | 现有呈现输入 | 当前饵 / 钓组 | 不混入窝料释放 |

`Effective Ingestion Opportunity` 仍只是候选中间量。它进入哪个槽位、是否作为独立组件，仍是 OPEN。本页不替它选位置。

## 4. 求值顺序

设计顺序：

1. 解析候选身份：鱼种、中鱼习性模式、FishStock、ConditionGroup。
2. 读取 `SpatialDistributionWeight` 作为上下文；不重新乘 `Base Weight`。
3. 读取 `Fish Condition`。
4. 读取 `Persistent Response Field`。
5. 解析 Feeding Place State：当前地点有哪些对象、线索、位置和状态。
6. 求门控：是否存在可遇见对象、是否存在可表现线索、是否存在可处理对象。
7. 求修正：Food、Flavor、Edible、Release context。
8. 按模式聚合组件；算子 OPEN。
9. 按鱼种 / 模式聚合为 `Fish Adaptation Coefficient Set`；算子 OPEN。
10. 交给圆桌，由圆桌执行 `SpatialDistributionWeight × AdaptationCoeff`。

运行时顺序与设计顺序一致，但第 8、9 步的具体函数不在本页。

## 5. 门控与修正分开

候选输出分两类：

- **门控**：当前有没有值得评价的对象或线索。例如没有遇见机会、没有可处理对象。
- **修正**：在门控通过后，响应有多强。例如 Food 偏好、Flavor 正响应、Edible 利用。

规则：

1. 门控失败不能被修正补偿。
2. 门控和修正不能使用同一个事实两次。
3. 门控结果可以是 0 / 1，也可以是连续概率；具体形式 OPEN。
4. 修正不能把门控失败变成成功。

这条规则避免“高 Food 分抵消没有可食对象”或“强香味抵消尺寸不可处理”。

## 6. 禁止的合并方式

### 6.1 单一总分

不写：

```text
RecipeFit = FoodFit + FlavorFit + ParticleFit + PhysicalFit
```

原因：四项处于不同阶段，简单相加会重复计权。

### 6.2 同一事实双算

同一 Cue、Food Identity、粒径或释放状态不能同时作为门控和修正各算一次。每一份事实只保留一个主要消费者。

### 6.3 释放直接乘响应

`A/L/U/Q` 不能直接乘进 `AdaptationCoeff`。它们先形成 Feeding Place State，再由响应读取。

### 6.4 Fish Condition 自由写入

窝料候选不能写 `Activity`、`Feeding Motivation`、`Diet Shift` 或 `Wariness`。如果未来需要，必须另立机制 Contract。

### 6.5 提前归一化

候选输出不是概率。只有圆桌抽样阶段才归一化。

## 7. 结构 Fixture

四份配方只检查映射，不计算最终分数。

| 配方 | Food | Flavor | Edible | Release |
|---|---|---|---|---|
| A | 强 | 弱 | 中 | 快 |
| B | 弱 | 强 | 中 | 慢 |
| C | 中 | 中 | 强 | 中 |
| D | 强 | 强 | 弱 | 快 |

映射检查：

- A 的强 Food 进入 Food 组件，不进入 Flavor 或 Edible。
- B 的强 Flavor 进入 Flavor 组件，不进入 Food 或 Edible。
- C 的强 Edible 进入 Edible 组件，不进入 Food 或 Flavor。
- D 的强 Food 和强 Flavor 不能补偿弱 Edible；Edible 仍是独立组件。
- A 和 D 的快释放只改变 Release context，不改变 Food / Flavor / Edible 的值。

这张表不产生数值排序。它只证明四条路径在映射上分开。

## 8. 退化测试

1. **无单一总分**：输出不能是一个 `RecipeFit` 标量。
2. **门控优先**：没有可食对象时，高 Food 或强 Flavor 不能产生有效摄食。
3. **同事实不双算**：同一 Cue 或 Food Identity 不能既做门控又做修正。
4. **释放不直乘**：改变 `A/L/U/Q` 不能直接改变 `AdaptationCoeff`。
5. **Fish Condition 不被写**：窝料候选不能修改鱼况四参数。
6. **适配系数不是概率**：`AdaptationCoeff` 在圆桌前不归一化。
7. **圆桌只乘一次**：`SpatialDistributionWeight × AdaptationCoeff` 只在圆桌执行一次。
8. **输出是集合**：响应输出是鱼种 × 模式的系数集，不是单鱼总分。
9. **移除候选**：移除窝料候选后，现有 Response Stage 不应被本目录改写。

## 9. 结论

- 不建立单一 `RecipeFit`。
- 四条候选输出分别进入 Response Condition、Response Component 或 Persistent Response Field。
- 最终聚合仍由现有 Response Stage 的 `SpatialDistributionWeight × AdaptationCoeff` 完成。
- `AdaptationCoeff` 的具体公式、组件聚合算子和模式聚合算子仍是 OPEN。
- 本页闭合的是候选到现有接口的映射，不是数值公式。

## 10. 未收口问题

- `AdaptationCoeff` 的正式公式。
- 多个 Response Component 的聚合算子。
- 多个中鱼习性模式的聚合算子。
- `Effective Ingestion Opportunity` 的落点和量纲。
- 门控和修正的正式区分方式。
- `Persistent Response Field` 的 Schema、时间、范围、衰减。
- 候选输出是否需要进入刺鱼或搏鱼。

对应冲突登记 C-04、C-05a、C-05b、C-09。
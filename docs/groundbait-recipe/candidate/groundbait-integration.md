# Groundbait 全栈整合

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页把 Groundbait 的四条事实路径接成完整候选链，不定义 Current Contract，也不写最终总公式。

## 1. 四条事实路径

```text
Recipe / Ingredient Facts
  ├─ Food Identity ─────────────→ Food Target → 选择 / 对象价值
  ├─ Chemical Cue Potential ────→ Chemical Cue Field → 发现 / 趋近 / 选择 / 回避
  ├─ Particle / Object Properties → 动作可行性 / 动作成功
  └─ Physical Properties ───────→ Physical Release → Feeding Place State
```

同一 Ingredient 可以同时提供多类事实，但四条路径分别进入，不在末端合并成一个总分。整合的重点是每个事实只进入它该进的阶段，不是让四个都算。

文中的 `Feeding Place State`（摄食地点状态）、`Feeding Event`（摄食事件）、`Effective Ingestion Opportunity`（有效摄食机会）都是本目录的 Candidate-local 工作词。

## 2. 完整候选链

```text
Recipe / Ingredient Facts
        ↓
Physical Release
        ↓
Feeding Place State(place, t)
  ├─ contactable particle objects
  ├─ Chemical Cue Field
  ├─ location / layer
  └─ object processing state
        ↓
Encounter / Approach
        ↓
Feeding Event
  ├─ feasible action set
  ├─ action selection
  ├─ action success
  └─ ingestion / object update
        ↓
Groundbait Candidate Response Inputs
        ↓
Response Stage 的候选接口
```

## 3. 阶段职责表

| 输入 | 进入阶段 | 可以影响 | 不能影响 |
|---|---|---|---|
| Food Identity | 动作选择、对象价值 | 鱼愿意尝试哪个对象、一次摄食值多少 | 动作可行性、释放速度 |
| Chemical Cue | 发现、趋近、选择、回避 | 鱼是否感知、是否接近 | 尺寸成功、物理释放 |
| Edible Particle | 动作可行性、动作成功 | 能否捕获、吸入、处理可食对象 | 发现、Food Preference |
| Carrier / Non-edible Particle | Physical Release | 雾化、扩散、沉降、留存 | Edible Utilization |
| Physical Properties | 状态转换 | 对象何时、在哪、以什么状态出现 | 直接中鱼率、鱼偏好 |
| 状态粉 | 物料与物理性质 | 释放、黏度、持续时间 | 免费 Buff |
| 小药 | 线索场 | Cue Exposure / Composition | 免费固体质量、固定 Bonus |

## 4. 对象守恒与状态更新

实体对象在以下状态之间转移：

```text
投放存在
  → 当前仍存在
  → 当前可接触
  → 当前可处理
  → 被摄食 / 离开地点 / 不可接触 / 不可处理 / 转态
```

可食颗粒和载体颗粒分别记账。载体可以有粒径，也参与释放，但不进入可食利用。生成公式和守恒账本见 `particle-distribution.md` §3–§5。

规则：

- 投放份额不等于当前可接触份额。
- 可食份额在可食部分内部归一化，不混入载体。
- 摄食成功后对象价值必须减少或移除。
- 释放可以补充对象，但不能凭空增加总物料。
- 质量、数量、能量只能声明一种工作计量，转换必须显式。

## 5. 重复计权检查点

### 5.1 同一 Ingredient 的多路径

虾粉同时提供 Food、Cue、Particle 和 Physical 事实时：

- Food 走对象选择与价值；
- Cue 走线索场；
- Particle 走动作约束；
- Physical 走释放状态。

不能因为来源相同就在末端合成一个“虾粉总分”。

### 5.2 粒径的两个身份

- 鱼侧：动作可行性与成功。
- 物理侧：沉降、解体、暴露。

两条链都读尺寸，但必须各自产生中间状态，不能给粒径一个跨链总系数。

### 5.3 环境食物浓度与窝料对象

如果环境侧已经表达食物浓度，窝料对象状态不能再把同一事实作为另一份正向响应。当前保留两种解释，待 Owner 裁决：

1. 环境侧是背景事实，窝料是玩家增量；
2. 二者是同一事实，需要在消费端合并。

对应冲突登记 C-06。

## 6. Overfeeding 与局部鱼群

外部研究记录 RF4 存在 overfeeding：population 下降、咬口频率降低、需要休息和补窝。该研究是外部证据，不是本仓 Current。

当前候选只保留问题边界：

- Overfeeding 是否首版纳入。
- 若纳入，放在 Feeding Place（对象与线索状态）还是 Fish Condition（饱食 / 警戒）。
- 是否需要历史累积、非单调结果、补窝频率和跨 session 语义。
- 局部鱼群 / 招募是否需要显式建模，还是只体现为机会权重变化。

在本仓没有证据和位置前，不写具体惩罚公式。对应冲突登记 C-07a、C-07b。

## 7. 发现与趋近

当前候选把发现和趋近合并在 `Encounter` 里。它读取：

- Feeding Place 的空间位置、水层和对象可接触状态；
- Chemical Cue Field；
- Fish Condition 的 Activity、Feeding Motivation、Wariness；
- 当前 Response Condition / Presentation Signal。

`Encounter` 不读取对象尺寸来宣布“更吸引”，也不把尺寸成功提前算进发现概率。

是否把 `Encounter` 拆成 Detection、Approach 和 Temporal Opportunity，仍是 OPEN。对应冲突登记 C-08。

## 8. 与 Response Stage 的接口

Groundbait 只提供候选输入：

```text
Feeding Place State
+ Feeding Event 输出
+ Effective Ingestion Opportunity
```

它们如何落入 `Response Condition`、`Response Component`、持久响应场或其它既有入口，仍为 OPEN。候选不定义 `AdaptationCoeff` 公式，不写回 `SpatialDistributionWeight`，不直接设置 `Fish Condition`。

## 9. 最小结构反例

- 四条路径末端相加：重复计权。
- 投放份额直接当鱼侧可利用率：跳过释放状态。
- 粒径同时改鱼侧成功和物理沉降，又给一个总系数：跨链重复。
- 摄食成功后对象仍保留完整价值：守恒失败。
- 小药增加实体食物质量：来源越权。
- Overfeeding 直接写成固定惩罚：缺证据。
- Groundbait 影响摄食机会却自动改 Feeding Motivation：状态越权。
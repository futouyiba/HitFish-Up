# Groundbait Object Model｜对象与因果所有权 Candidate

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 权威边界：本页只整理窝料机制的候选对象和因果边界，不创建 FCF Current Schema，也不修改现有 Current Contract。

## 1. 主脊

窝料机制先处理“世界里有什么、它现在处于什么状态”，再交给鱼侧响应：

```text
Recipe Facts
  → Physical Release
  → Feeding Place State(place, t)
  → Feeding Event
  → Effective Ingestion Opportunity
  → Response Stage 的候选输入
```

这里的 `Feeding Place`、`Feeding Place State`、`Feeding Event` 和 `Effective Ingestion Opportunity` 都是本目录的 Candidate-local 工作词，不是仓内正式术语。

## 2. 对象、状态与过程

### 2.1 Recipe / Ingredient Facts

配方事实描述原料和配比能提供什么，不直接提供“某鱼加多少分”。同一 Ingredient 可以分别贡献不同事实：

```text
Ingredient Facts
├─ Food Identity
├─ Chemical Cue Potential
├─ Particle / Object Properties
└─ Physical Release Properties
```

同一个来源进入多条路径，不表示这些路径可以在末端合成一个总分。每条路径都必须有自己的中间状态和消费者。

### 2.2 Particle Object

`Particle Object`（颗粒对象）表示实体食物对象，至少保留：

```text
Particle Object
├─ effective_size       对当前动作有意义的有效尺寸
├─ declared_value       质量、数量或能量中的一种明确计量
├─ shape / hardness     形状与硬度
├─ cohesion             是否团聚、松散或正在解体
├─ location / layer     当前空间与水层
└─ release_state        完整、解体、悬浮、沉降等状态
```

`effective_size` 不必等于筛网粒径。对团块、纤维或不规则对象，如何从形态和状态生成有效尺寸仍是 OPEN。形状、硬度、团聚不能静默编码进尺寸值。

### 2.3 Chemical Cue Field

`Chemical Cue Field`（化学线索场）表示地点和时间中的可感知化学线索：

```text
Chemical Cue Field
├─ cue family / composition
├─ intensity
├─ spatial exposure
└─ time profile
```

线索可以没有实体食物伴随，例如低固体小药；实体食物也可能存在但线索很弱。二者来源可以相关，但状态不能合并。

### 2.4 Feeding Place State

`Feeding Place State`（摄食地点状态，`place, t` 表示地点与时点）是某地点、某时点对鱼可见的状态集合：

```text
Feeding Place State
├─ contactable particle objects
├─ chemical cue field
├─ location / layer
├─ object processing state
└─ persistence / turnover
```

它由 Physical Release 和运行时状态产生，供 Feeding Event 消费。它不是一个吸引分，也不是最终 Response。

### 2.5 Fish and Feeding Event

鱼侧对象至少包括：

```text
Fish State
├─ Body Linear Size / Morphology
├─ Feeding Action Capacity
└─ Fish Condition（引用现有 Current 语义）
```

`Feeding Event`（摄食事件）是一次具体摄食机会的过程，不是鱼种静态属性。它依次处理：对象是否遇到、哪些动作可行、选择哪条动作路径、动作是否成功、对象是否被有效处理。

## 3. 因果所有权矩阵

| 量 / 状态 | 生产者 | 主要消费者 | 所属阶段 | 当前状态 |
|---|---|---|---|---|
| Food Identity | Recipe / Ingredient Facts | 鱼侧目标选择与对象价值 | 配方事实 → Feeding Event | Candidate |
| Cue Exposure / Field | Ingredient + Physical Release | 发现、趋近、回避与选择 | Feeding Place | Candidate |
| effective_size | Particle Object / Object State | 动作可行性与动作成功 | Feeding Event | Candidate |
| shape / hardness / cohesion | Particle Object / Object State | 捕获、保留、处理 | Feeding Event | OPEN / Candidate |
| contactable object set | Physical Release + place state | Encounter / Feeding Event | Feeding Place | Candidate |
| action feasibility | Fish morphology + place + object state | Action selection | Feeding Event | Candidate |
| action selection | Fish policy / condition | One Feeding Event | Feeding Event | OPEN |
| action success | Action capacity + object constraints | Handling / ingestion | Feeding Event | Candidate |
| object consumption / turnover | Feeding Event + Physical Release | Next place state | State transition | Candidate |
| Effective Ingestion Opportunity | Feeding Event aggregation | Response Stage candidate interface | Response input | OPEN |
| Fish Condition | 现有 Fish Condition 语义 | Response / Feeding Event 的条件输入 | Current | CURRENT |
| Adaptation Coefficient | 现有 Response Stage | 下游候选权重 | Current | CURRENT |

`Effective Ingestion Opportunity` 目前只表示候选输出接口，不表示它已经映射为 Adaptation Coefficient。

## 4. 两个身份：同一粒径进入两条链

同一对象尺寸可以同时影响两件不同的事，但不能用一个总系数代替：

```text
对象尺寸
├─ Physical Release：影响沉降、解体、迁移和暴露时间
└─ Feeding Event：影响捕获、吸入、保留和处理成功
```

前者改变鱼在何时何地遇到什么，后者改变遇到以后能否有效利用。若两条链都读尺寸，必须各自产生自己的中间状态，并保留 causal provenance。

## 5. 计量投影

首轮允许使用 `MassShareProjection` 作为离散对象分布的工作投影，因为它能表达守恒并易于核对。但它不是最终机制单位：

- `declared_value` 必须声明是质量、数量还是能量；
- 投放时份额不能冒充当前可接触份额；
- 从质量转换到数量或能量必须显式写出转换；
- 不同阶段不能静默换用另一种单位。

最终采用哪种价值空间仍为 OPEN。

## 6. 不能越过的边界

1. 不从静态配方比例直接跳到鱼侧有效摄食。
2. 不把 Food、Flavor、Particle、Physical 四条路径在末端相加。
3. 不把鱼的偏好写进 Particle Object；对象描述“是什么”，鱼侧规则描述“如何评价”。
4. 不让 Physical Release 改写对象的固有尺寸；它只能改变状态、位置、可接触性和时间分布。
5. 不把 Candidate-local 工作词写成 `docs/terminology.md` 已确认的正式术语。
6. 不把 `Effective Ingestion Opportunity` 写成最终中鱼率或 Adaptation Coefficient。

## 7. 最小结构反例

- 虾粉可以同时提供 Food Identity、Chemical Cue Potential 和 Particle Properties；三条路径必须分开，不能因来源相同而合并。
- 草莓小药可以提供 Chemical Cue Field，但不能增加实体食物质量。
- 同样的投放配方在不同时间点的 contactable object set 可以不同；投放份额不等于 Feeding Place 份额。
- 同样尺寸的对象在完整、团聚和解体状态下，动作成功可能不同；差异应由 object state 进入，不应偷偷改写尺寸值。

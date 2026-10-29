# Response 算法接口

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页只定义 Response Stage 的输入输出、两条通道和聚合顺序，不定义 `Adaptation Coefficient` 的生产公式，不修改 Current Contract。

## 1. 已验证的 Current 语义

候选输出如何进入本 Stage 的完整映射和求值顺序见 `response-aggregation-map.md`。

`docs/terminology.md` §5.2 把响应阶段描述为：

```text
空间分布权重 SpatialDistributionWeight
+ 鱼况 Fish Condition
+ 响应习性组件 Response Components
+ 当前刺激 / 呈现信号 Presentation Signal
→ 响应评价
→ 下游候选权重
```

当前可表达为：

```text
SpatialDistributionWeight × AdaptationCoeff
→ 下游候选权重
```

术语只给出这一层关系，没有给出 `AdaptationCoeff` 的具体公式。

## 2. 两条通道

### 2.1 持久响应

```text
玩家持久操作（打窝、响动等）
  → 条件派生
  → 持久响应因子运算
  → 持久响应场 Persistent Response Field
```

持久响应场是运行时对 DEF 的增量层，不复制 DEF。它记录来源、影响的条件 / 因子、强度、生效范围、持续时间和衰减。

### 2.2 姿态响应

```text
持久响应场
+ 中鱼习性模式空间结果
+ 当前饵 / 姿态
+ 玩家位置与操作
+ DEF
  → 响应条件整理
  → 响应因子运算
  → 响应系数聚合
  → 鱼适配系数集
```

姿态响应是当前呈现下的即时计算，频率高。

出处：`docs/terminology.md` §5.2、`feishu-module-framework.md` 模块表。

## 3. 输入输出契约

### 3.1 输入

| 输入 | 来源 | 读 / 乘 / 门控 | 限制 |
|---|---|---|---|
| `SpatialDistributionWeight` | 烘焙 | 读，或按 Current 公式组合 | 不重新乘 Base Weight |
| `Fish Condition` | 鱼况机制 | 读 | 不由响应改写 |
| `Response Components` | 鱼侧配置 | 读 | 不默认复用环境侧 Profile 结构 |
| `Presentation Signal` | 玩家呈现 | 读 | 与 Response Condition 的边界待定 |
| `Persistent Response Field` | 持久响应 | 读一次 | 不与即时增量重复消费 |

### 3.2 输出

- `鱼适配系数集`：鱼种 × 中鱼习性模式 → 适配系数。
- 适配系数是无量纲倍率，不是单鱼概率。
- 适配系数集交给圆桌，不在响应阶段归一化。

## 4. 响应组件

术语明确：响应习性组件的内部配置不默认复用环境侧的 `Profile → Affinity → Fit` 结构。

当前候选只要求每个组件回答：

```text
Response Component
├─ 读取哪些响应条件 / 呈现信号
├─ 是否设门控
├─ 输出什么适配值或系数
└─ 缺失时如何处理
```

不先规定组件必须使用线性、饱和或分段曲线。

## 5. 聚合顺序

设计顺序：

1. 定义输入语义和单位。
2. 定义单个 Response Component 的输出。
3. 定义多个组件的聚合角色和缺失行为。
4. 定义同一中鱼习性模式内多个组件的聚合。
5. 定义模式之间的聚合，形成鱼适配系数集。
6. 最后定义与 `SpatialDistributionWeight` 的组合接口。

运行时顺序：

```text
解析候选身份
  → 读取空间权重 / 鱼况 / 组件 / 呈现
  → 读取持久响应场
  → 每个组件求值
  → 模式内聚合
  → 模式间聚合
  → 输出鱼适配系数集
```

## 6. 持久响应与即时响应

当前只提出职责分工，不宣称新的 Contract：

- 打窝、补窝、持续释放等持续效果进入持久响应场。
- 当前饵、姿态、操作进入响应条件 / 呈现刺激。
- 同一窝料状态不能既以完整效果写入持久字段，又以同一份效果作为即时条件再次加权。
- 若两条路径同时存在，必须声明来源、增量、时间、范围和衰减。

## 7. 与窝料候选的接口

窝料候选只提供输入候选：

```text
Feeding Place State
+ Feeding Event 输出
+ Effective Ingestion Opportunity
```

它们如何落入 `Response Condition`、`Response Component`、持久响应场或其它既有入口，仍为 OPEN。候选文档不定义 `AdaptationCoeff` 公式，不写回 `SpatialDistributionWeight`，不直接设置 `Fish Condition`。

## 8. 未决项

- `Response Condition` 与 `Presentation Signal` 的正式边界。
- 响应组件是否需要自己的 grammar，还是可以复用环境侧结构。
- 多组件、多模式的聚合角色和缺失行为。
- `Persistent Response Field` 的正式 Schema、时间、范围、衰减。
- `Effective Ingestion Opportunity` 的落点和量纲。
- 同一来源在持久与即时两条通道的消费规则。

以上登记在 `docs/terminology.md` §5.2 的缺口和 `decisions/conflict-register.md`。

## 9. 最小结构反例

- 响应改写了 `SpatialDistributionWeight`：越权。
- 同一 Cue 在持久和即时各算一次：重复计权。
- 响应直接输出概率：阶段混用。
- 移除窝料候选后响应仍变化：隐藏依赖。
- 模式缺少系数但没有显式缺席标记：候选静默丢失。
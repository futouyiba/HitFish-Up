# 台钓中鱼系统对象模型

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页描述完整台钓中鱼链的对象、状态、权重和所有权，不定义 FCF Current Contract，也不替代 `docs/terminology.md`。

## 1. 目的

在深入任何子模块前，先把“谁在场、谁响应、谁被抽中”的对象和状态分清楚，避免：

- 同一事实在两个阶段各算一次；
- 把权重、系数和概率混名；
- 把条件组级的结果当成坐标级结果；
- 把 Candidate-local 工作词写成正式术语。

## 2. 端到端主脊

沿用 `fcf-system-map/README.md` 的七层主线：

```text
一、数据
  环境上下文 / 钓场投鱼配置 / 鱼的习性配置
        ↓
二、烘焙
  烘焙 → 派生环境场 DEF → 空间分布权重 + 鱼侧动态参数
        ↓
三、玩家策略与操作
  钓具 / 钓组 / 姿态 → 呈现刺激
        ↓
四、响应
  响应模块 → 鱼适配系数集
        ↓
五、圆桌抽鱼
  品质抽取调整 / 圆桌权重表构建 / 硬保底 / 动态权重调整
        ↓
六、抽鱼和生成
  鱼种 / 品质 / 大小 / 重量；鱼侧动态参数透传
        ↓
七、范围外
  Fish AI（刺鱼 / 搏鱼）
```

空间侧与鱼侧是两条并行支路，只在圆桌抽鱼汇合一次。这个汇合点是本页所有所有权规则的基准。

## 3. 对象表

表中的 Candidate-local 工作词：`Feeding Place State`（摄食地点状态）、`Feeding Event`（摄食事件）、`Effective Ingestion Opportunity`（有效摄食机会）。

| 对象 | 所属阶段 | 生产者 | 主要消费者 | 生命周期 | 持久化 | 成熟度 |
|---|---|---|---|---|---|---|
| 环境上下文 | 数据 | 世界 / 课程表 / 钓场三维数据 | 烘焙 | 场景级 | 是 | Current 术语 |
| 投鱼配置 | 数据 | 钓场配置 | 烘焙、圆桌 | 场景级 | 是 | Current 术语 |
| 鱼的习性配置 | 数据 | Fish Habit Editor / 配置表 | 烘焙、响应 | 配置级 | 是 | Current 术语 |
| 原始条件 / 派生条件 | 烘焙输入 | 环境与配置 | 因子运算 | 条件组级 | 是 | Current 术语 |
| 条件组 ConditionGroup | 烘焙 | 烘焙 | DEF、响应 | 条件组级 | 是 | Current 术语 |
| 环境习性组件 / 响应习性组件 | 配置 | 鱼侧配置 | 因子运算 | 配置级 | 是 | Current 术语 |
| 门控结果 / 适配值 | 烘焙 / 响应 | 因子运算 | 通道聚合 | 求值级 | 否 | Current 术语 |
| 派生环境场 DEF | 烘焙 | 烘焙 | 响应、圆桌 | 烘焙快照 | 是 | Current 术语 |
| 空间分布权重 | 烘焙 | 烘焙 | 响应、圆桌 | 烘焙快照 | 是 | Current 术语 |
| 鱼侧动态参数（Fish Condition） | 烘焙 / 运行时 | 对应机制 | 响应、刺鱼、搏鱼 | 动态状态 | 视 Contract | Current 术语；更新公式 OPEN |
| 玩家策略与操作数据 | 玩家输入 | 玩家 | 响应 | 每次操作 | 否 | Current 术语 |
| 呈现刺激 Presentation Signal | 玩家输入 | 玩家策略 | 响应 | 每次呈现 | 否 | Current 术语 |
| 持久响应场 Persistent Response Field | 响应 | 持久响应 | 姿态响应 | 持续增量 | 是 | Current 术语；Schema OPEN |
| 响应评价 | 响应 | 响应模块 | 适配系数 | 每次响应 | 否 | Current 术语；公式 OPEN |
| 鱼适配系数集 | 响应 | 响应模块 | 圆桌 | 每次响应 | 是 | Current 术语；公式 OPEN |
| 圆桌权重表 | 圆桌 | 圆桌计算 | 抽鱼 | 每次抽鱼 | 是 | Current 术语；四件规则 OPEN |
| 抽鱼结果 | 抽鱼 | 抽鱼 | 生成 | 每次抽鱼 | 否 | Current 术语 |
| 生成鱼对象 | 生成 | 生成模块 | Fish AI | 单条鱼 | 是 | Current 术语 |
| 配方 / Ingredient Facts | 玩家输入 | 配方配置 | Groundbait 候选 | 配方级 | 是 | Candidate |
| 可食颗粒分布 Edible Particle Distribution | Groundbait Candidate | Recipe Facts + Physical Release | Size Response | 地点时间级 | 视实现 | Candidate-local |
| 载体颗粒分布 Carrier Particle Distribution | Groundbait Candidate | Recipe Facts + Physical Release | Physical Release | 地点时间级 | 视实现 | Candidate-local |
| Feeding Place State | Groundbait Candidate | Physical Release | Feeding Event | 地点时间级 | 视实现 | Candidate-local |
| Feeding Event | Groundbait Candidate | 鱼侧事件 | Groundbait 响应输入 | 单次事件 | 否 | Candidate-local |
| Effective Ingestion Opportunity | Groundbait Candidate | Feeding Event | Response 候选输入 | 单次事件或时段 | 否 | Candidate-local / OPEN |
| Fish AI | 范围外 | 下游模块 | 下游玩法 | 运行时 | 是 | 范围外 |

## 4. 权重、系数与概率

| 名称 | 定义 | 是否归一化 | 是否概率 | 主要生产者 |
|---|---|---|---|---|
| Base Weight / 基础机会强度 | 环境影响介入前的基础量级 | 否 | 否 | 投鱼条目 |
| 空间分布权重 SpatialDistributionWeight | `Base Weight × FinalEnvCoeff` | 否 | 否 | 烘焙 |
| 环境系数 EnvCoeff | 多因子环境评价的聚合倍率 | 否 | 否 | 烘焙 |
| 适配系数 Adaptation Coefficient | 响应阶段产生的无量纲倍率 | 否 | 否 | 响应 |
| 圆桌权重 Roundtable Weight | 响应之后组装的候选权重 | 否 | 否 | 圆桌 |
| 抽样概率 | 圆桌权重归一化后的抽取概率 | 是 | 是 | 抽鱼 |
| 中鱼等待时间 | 系统输出 | 不适用 | 不适用 | 抽鱼 / 生成之后 |

硬规则：

- `Base Weight` 只在 `SpatialDistributionWeight = Base Weight × FinalEnvCoeff` 中乘一次。
- `SpatialDistributionWeight` 不是概率，不提前归一化。
- `Adaptation Coefficient` 不是单鱼概率。
- `Roundtable Weight` 仍不是概率；只有进入抽样并归一化后才成为概率。
- 中鱼等待时间不在响应模块直接产出。

## 5. 身份轴

每个权重或候选必须携带可声明的身份轴元组，至少包括：

```text
FishStock
FishQualityRef
Species
EngagementMode
ConditionGroupRef
Place
Time
```

没有声明轴的聚合不允许发生。不同轴的候选不能因为字段名相同就合并。

## 6. 阶段隔离规则

1. **烘焙**只产生 DEF、空间分布权重和鱼侧动态参数。响应不重新乘环境系数，也不写回 DEF。
2. **鱼况**由对应机制更新。窝料、味型、Food 不直接写入 `Activity`、`Feeding Motivation`、`Diet Shift`、`Wariness`。
3. **持久响应**只产生叠加层，不复制 DEF。同一来源不能在持久字段和即时条件中各消费一次。
4. **响应**读取 DEF、鱼况、玩家刺激和持久增量，输出鱼适配系数集。它不产生最终概率。
5. **圆桌**只组装候选权重，不改写上游事实。挤占、裁剪和抽鱼按各自 Current 执行。
6. **抽鱼和生成**消费圆桌权重表，输出鱼对象。
7. **Fish AI** 属于范围外。它读取生成鱼对象和必要的鱼况输入，不反向改写圆桌或响应。

## 7. 唯一的汇合点

空间侧和鱼侧只在圆桌权重构建处汇合。响应阶段如果读取空间分布权重作为上下文，必须满足：

- 只读，不修改；
- 不第二次乘以基础权重；
- 有明确 trace；
- 不与圆桌处的乘法重复计权。

该规则对应冲突登记 C-04a、C-04b 与 Response Current 的待决问题。

## 8. 与 Groundbait Candidate 的接口

Groundbait Candidate 只提供候选输入：

```text
Recipe / Ingredient Facts
  → Physical Release
  → Feeding Place State
  → Feeding Event
  → Effective Ingestion Opportunity
  → Response Stage 的候选输入
```

它不定义 `Adaptation Coefficient` 公式，不写回 `SpatialDistributionWeight`，不直接设置 `Fish Condition`，也不进入 Fish AI。可食颗粒分布只进入 Size Response；载体颗粒分布只进入 Physical Release，两者不共享一个可食利用结果。具体映射见 `candidate/response-stage-mapping.md`。

## 9. 未决项

- `Effective Ingestion Opportunity` 的落点和量纲。
- `Persistent Response Field` 的正式 Schema、时间、范围、衰减。
- `Fish Condition` 四参数的更新公式和时间粒度。
- 圆桌四件、挤占、裁剪和抽鱼的先后与规则。
- 环境“食物浓度”与窝料对象状态如何合并。
- 刺鱼、搏鱼是否消费本链输出。

以上都登记在 `decisions/conflict-register.md`，本页不自行裁决。

## 10. 最小结构反例

- 同一温度既进 `EnvCoeff` 又进 Fish Condition，若两处都乘最终权重，就是重复计权。
- 同一打窝效果同时写 `Response Condition` 和 `Persistent Response Field`，若没有来源与增量区分，就是双计。
- 响应前后 `SpatialDistributionWeight` 发生变化，说明响应越权。
- 圆桌权重在归一化前被当成概率，说明阶段混用。
- 抽中空鱼候选后仍生成鱼对象，说明抽鱼和生成边界错误。
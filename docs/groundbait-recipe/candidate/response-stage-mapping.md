# Response Stage Mapping｜窝料候选与现有响应阶段的映射

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 权威边界：本页只做候选接口映射，不修改 `docs/terminology.md`，不定义 `Adaptation Coefficient` 或 `Persistent Response Field` 的新 Schema。

最终聚合映射和求值顺序见 `response-aggregation-map.md`。

## 1. 现有 Current 语义

仓内术语将响应阶段描述为：

```text
SpatialDistributionWeight
+ Fish Condition
+ Response Components
+ Presentation Signal
→ Response Evaluation
→ 下游候选权重
```

`Response Condition` 包括玩家侧的饵、姿态、窝料、线组、玩家位置与操作；`Persistent Response Field` 用于承载持续生效的玩家行为影响，例如打窝。以上是 Current 入口；本目录只说明窝料候选产生什么输入，不改写这些入口的定义。

## 2. Candidate 输出映射

| Candidate 输出 | Current 槽位候选 | 方向 | 状态 | 边界 |
|---|---|---|---|---|
| Recipe / Ingredient Facts | Response Condition 的窝料来源 | 输入 | Candidate 接口 | 不直接进入最终权重 |
| Feeding Place State(place, t) | Response Condition 的派生状态 | 输入 | Candidate，待 Owner 确认 | 代表当前地点的对象与线索状态 |
| Feeding Place 的持续部分 | Persistent Response Field | 持续增量输入 | Candidate，待 Owner 确认 | 记录范围、时间、衰减；不复制 DEF |
| Chemical Cue Field | Response Condition 的派生条件候选 | 输入 | 部分已有术语可承接，具体映射 OPEN | 不把线索直接写成吸引分 |
| Food Identity / Food Preference | Response Components 或鱼侧偏好数据 | 规则输入 | OPEN | 不擅自新增组件类型 |
| Feeding Event 输出 | Response Stage 的响应条件候选 | 输入 | OPEN | 不直接等于 Adaptation Coefficient |
| Effective Ingestion Opportunity | Response Evaluation 的候选中间输入 | 输入 | OPEN | 不决定最终公式 |
| Fish Condition | 现有 Fish Condition | 只读条件 | CURRENT 边界 | 窝料不直接设置 Activity / Motivation / Wariness |
| SpatialDistributionWeight | 环境权重阶段输出 | 只读输入 | CURRENT 边界 | 窝料不写回烘焙阶段 |
| Adaptation Coefficient | 现有 Response Stage 输出 | 下游输出 | CURRENT 边界 | 本 Candidate 不改公式 |

## 3. 持久响应与即时响应

当前只提出职责分工，不宣称新的 Contract：

```text
打窝 / 补窝 / 持续释放
  → Persistent Response Field 的候选来源

当前饵 / 姿态 / 操作
  → Response Condition / Presentation Signal 的候选来源
```

同一窝料事件不能既以完整效果写入持久字段，又以同一份效果作为即时条件再次加权。若两条路径同时存在，必须声明：

- 哪个是来源状态；
- 哪个是响应阶段的消费；
- 是否只保留一条有效增量；
- 时间、范围和衰减如何区分。

这些组合关系仍需 Owner / Current 收口。

## 4. 与 Fish Condition 的边界

窝料可以改变 Feeding Place 状态，也可能在未来影响鱼的动态行为，但本 Candidate 不直接写入 `Fish Condition`：

- `Activity`、`Feeding Motivation`、`Wariness` 的更新公式属于对应机制 Contract；
- Food / Flavor / Particle 的结果不能一律伪装成 Feeding Motivation；
- 如果未来要表达持续摄食改变鱼况，必须单独定义时间、记忆和衰减，不在本页隐含发生。

天气、时段等环境输入继续沿现有 Fish Condition 语义处理，不转换成简单的味型密码。

## 5. 与环境侧“食物浓度”的重复计权问题

如果现有环境因子已经表达水体背景食物或食物浓度，Groundbait 产生的对象状态不能再把同一事实作为另一份正向响应重复消费。

当前只保留两种可能解释：

1. 环境侧表示背景事实，Groundbait 表示玩家投放造成的增量；
2. 二者属于同一事实来源，需要在消费端合并，而不是分别加权。

选择哪一种需要查对应 Current / Owner 语义，本 Candidate 不自行决定。

## 6. 不可越过的边界

1. 不把 `Feeding Place State` 写成新的正式术语或 Current Schema。
2. 不定义 `Adaptation Coefficient` 的乘法、加法或替代公式。
3. 不把窝料写回 `SpatialDistributionWeight` 或环境烘焙阶段。
4. 不把 `Fish Condition` 当作窝料的免费输出槽位。
5. 不让 Response Stage 直接消费配方百分比；它应消费已解析的状态或候选中间输入。
6. 不让同一份窝料效果同时作为持久增量和即时增量重复计权。

## 7. 当前必须由 Owner / Current 决定的问题

- `Feeding Place State` 是否能作为 `Response Condition` 的派生状态存在；
- 打窝产生的持续状态是否应完整进入 `Persistent Response Field`，还是由既有窝料字段承载；
- `Chemical Cue Field` 是否已有可复用的 Response Condition / 派生条件入口；
- `Effective Ingestion Opportunity` 是 Response Component 输入、独立因子，还是只供下游某个既有计算消费；
- 玩家投放造成的食物增量与环境背景食物浓度如何合并；
- 该候选是否需要进入刺鱼、搏鱼等后续模块，还是只服务响应和抽鱼。

## 8. 最小映射反例

- 移除 Groundbait 候选后，现有 Response Stage 不应被本目录偷偷改写。
- 同一窝料状态同时写入 `Response Condition` 和 `Persistent Response Field`，若没有来源/增量区分，就构成重复计权。
- Groundbait 影响 `Effective Ingestion Opportunity`，不能因此自动改变 `Fish Condition.Feeding Motivation`。
- Groundbait 形成空间状态，不能因此直接改写 `SpatialDistributionWeight`。

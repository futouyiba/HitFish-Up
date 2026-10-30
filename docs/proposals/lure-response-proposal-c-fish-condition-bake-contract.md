# Proposal C｜Fish Condition 与 Bake 反推契约（Candidate）

状态：Working Design / Candidate。本文只写 Response 需要 Bake 产出什么，不定义 Bake 的生成公式，也不修改术语或 V1 语义。

## 1. 目的与边界

Response 已收口到五项评价。下一步是把上游需求反过来写成对 Fish Condition 的要求：

```text
Response 消费什么
→ Fish Condition 必须产出什么
→ Bake 必须保证什么
```

本文不回答“天气怎样算出 Activity”，也不新增 Fish Condition。

## 2. 现状事实

- 术语表把 Fish Condition 定义为鱼侧动态参数：Activity、Feeding Motivation、Diet Shift、Wariness；并说明更新公式、时间粒度与下游消费由对应机制 Contract 定义。
- 术语表把 `DEF` 定义为烘焙阶段按条件组归并的结果，条件组下保存中鱼习性模式的空间结果，包括空间分布权重与鱼况。
- V1 Common Semantics 明确把 Bake / condition evaluation 列在语义负向清单，不在 V1 承诺范围内。
- Fixed Bake 参考实现明确排除 Fish Condition。
- 窝料候选文档明确 Fish Condition 是只读条件，窝料不直接设置 Activity / Motivation / Wariness。

结论：Fish Condition 目前只有语义与存放位置，没有生成契约，也没有运行时字段。

## 3. Response 的消费需求

| Condition | Response 消费点 | 需要的语义 | 范围与参考（Candidate） | 缺失时 |
|---|---|---|---|---|
| Activity | `ActivityCostMultiplier` | 当前愿意为主动追赶付出多少行为代价，不是物理速度能力 | 非负倍率；参考 1.0 是候选假设 | `ResolutionIncomplete`，不能默认 1.0 |
| Feeding Motivation | `WillingnessThreshold(M)` | 当前为了食物出手需要多强的理由 | `M ∈ [0,1]`；0.5 是设计包的 Working 锚 | `ResolutionIncomplete`，不能默认 0.5 |
| Diet Shift | `DietaryShiftDelta(prey family)` | 相对基础食性的动态偏移，按猎物家族分别给出 | 与 FoodValue 同标尺的有符号偏移 | 该 family 的 FoodValue 不可闭合 |
| Wariness | `RiskCost` 的乘子 | 对已解析风险线索有多敏感 | `[0,1]` 是候选假设，未裁定 | Risk 不可闭合；当前 Risk cue 未实现时整体为 0 |

表中的范围与参考来自设计包的 Working 值或本页的 Candidate 假设，不是已批准 Contract。缺失时的归约遵循语义契约的通用状态协议。

### 3.1 Activity

- 只调制追赶负担，不进入 Closing 的结构速度上限；
- `ActivityCostMultiplier` 非负；1.0 只是 Working reference，不是缺失默认值；
- 当前无证据支持上界，不新增 runtime cap；
- 不能与 Feeding Motivation 共用一个“积极程度”标量。

### 3.2 Feeding Motivation

- 只移动门槛，不乘 FoodValue；
- `M ∈ [0,1]` 是 Candidate/Working 域；0.5 是参考锚，不是缺失 fallback；
- 高 Motivation 不复活 `Reject`。

### 3.3 Diet Shift

- 按 prey family 给出有符号偏移，只影响对应 family 的 FoodValue；
- 不增加全局 Diet Shift 分量；全局摄食意愿由 Feeding Motivation 表示；
- 与 Feeding Motivation 分开：前者改变“哪种食物更值”，后者改变“现在多愿意出手”。

### 3.4 Wariness

- `[0,1]` 仅为 Candidate 表示域；
- 只放大已解析的 `SuspicionLoad`；Risk 只消费 Wariness，不生成它；
- 没有可疑线索时，高 Wariness 不产生风险顾虑；
- 累积更新归 Fish Condition / 动态机制，owner、事件、粒度与衰减待指定；
- fishing pressure 若已作为 Wariness 的上游原因，不得再进入 SuspicionLoad。

## 4. 粒度与载体

`DEF` 按条件组归并，并在中鱼习性模式下保存鱼况，这是术语表的 Working 语义。

2026-10-30 裁决采用路径 B（见[裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md)）：

```text
Bake 产出 ConditionGroup × EngagementMode 基线
+ 运行时仅更新已有机制 Contract 明确授权的维度
当前仓内只有 Wariness 有“随过程累积变化”的语义依据
```

边界：

- Response 不写回 Fish Condition；
- Activity、Feeding Motivation、Diet Shift 目前只随上游重新求值或 Bake 刷新变化，不获得运行时累积权限；
- 窝料、Persistent Response Field、玩家即时操作只提供上游原因或独立输入，不直接改写 Fish Condition；
- 值必须携带来源、适用区间与解析状态；过期、越界或缺少必要来源不得沿用最后值，转为 `Unknown`。具体有效期、刷新频率与运行时 Wariness 的事件窗口待 Owner 定。

路径 B 的正式 Contract 化、Wariness 累积 owner 与过期状态协议仍列在[裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md)第 3 节。

## 5. 上游输入边界

允许作为 Bake 上游输入的候选：

```text
天气 / 时段 / 水温 / 溶氧 / 光照 / 流速
+ 钓压与历史事件（作为 Wariness 的上游）
+ 鱼种 / 体型 / 模式
```

约束：

- 同一上游原因不能同时驱动两个 Condition，除非明确声明各自的语义不同；
- fishing pressure 只进入 Wariness，不进入 SuspicionLoad；
- 时段只能作为上游原因，不能直接等于 Activity；
- 任何 Condition 的生成都不得读取玩家当前操作或饵的呈现。

## 6. 第一版最小输出

路径 B 的 Bake 基线最低可消费集合如下；范围与参考仍是 Candidate：

| 输出 | 最小要求 |
|---|---|
| Activity | 每个条件组 × 模式一个倍率或 `Unknown` |
| Feeding Motivation | 每个条件组 × 模式一个 `[0,1]` 值或 `Unknown` |
| Diet Shift | 每个条件组 × 模式 × prey family 一个偏移或 `Unknown` |
| Wariness | 每个条件组 × 模式一个 `[0,1]` 基线值或 `Unknown`；运行时累积另需授权 |

允许第一版只产出常量或按天气 / 时段分档的 placeholder；必须标注 `Candidate/Working`、适用范围、版本、有效期、来源与未标定状态，不能冒充生产参数。

## 7. 验收

Response 侧应能验证：

1. `Unknown` 的 Activity 不会默认成 1.0；
2. `Unknown` 的 Motivation 不会默认成 0.5；
3. `Wariness` 高但没有 cue 时 `RiskCost=0`；
4. 同一 prey family 的 Diet Shift 只影响该 family 的 FoodValue；
5. 运行时玩家操作不会改写任何 Fish Condition；
6. 过期、越界或缺来源的 Fish Condition 不会被沿用为最后值。

第 6 项的裁决建议是转 `Unknown`；正式状态协议仍待 Owner 确认。

## 8. 未决

裁决已定的部分见[裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md)。仍需 Owner 决定：

- 路径 B 是否正式 Contract 化，以及 Wariness 之外是否有 Condition 获得运行时更新权限；
- Wariness 累积的 owner、事件、粒度、有效期、衰减与会话记忆边界；
- 过期转 `Unknown` 是否作为正式状态协议；
- Activity 是否需要生产上界与标定来源；
- `TackleConspicuousness` 的字段、数据 owner 与 schema；
- DEF 中 Fish Condition 的版本与有效区间载体；
- 四个 Condition 的生成公式、来源与审核职责。

## 9. 来源

术语与边界：

- [`docs/terminology.md`](../terminology.md) §4、§5.2（Working Terminology Ledger）；
- [裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md)（2026-10-30 Fable 子代理裁决）；
- [`common-semantics.md`](../fish-habit-editor-v1/common-semantics.md) §13（V1 负向清单）；
- [`reference/0340-fixed-bake/README.md`](../../reference/0340-fixed-bake/README.md)（参考实现范围）；
- [`response-stage-mapping.md`](../groundbait-recipe/candidate/response-stage-mapping.md)（只读边界）。

消费点与状态（本页表格与验收由这些设计包条目反推）：

- [五评价项契约](lure-response-proposal-c-evaluation-items.md)（Activity / Motivation / Diet Shift / Wariness 的消费点与 Working 锚）；
- [语义契约](lure-response-proposal-c-semantic-contract.md) §1（通用状态与 `ResolutionIncomplete`）；
- [响应与机会契约](lure-response-proposal-c-response-opportunity.md)（`L × C` 与状态表）。

本页的范围、参考值与有效期规则是 Candidate 要求，不是已批准 Contract。

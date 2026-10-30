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

| Condition | Response 消费点 | 必须满足的语义 | 范围与参考 | 缺失时 |
|---|---|---|---|---|
| Activity | `ActivityCostMultiplier` | 当前愿意为主动追赶付出多少行为代价，不是物理速度能力 | 非负倍率；参考值 1.0 | `ResolutionIncomplete`，不能默认 1.0 |
| Feeding Motivation | `WillingnessThreshold(M)` | 当前为了食物出手需要多强的理由 | `M ∈ [0,1]`，参考 0.5 | `ResolutionIncomplete`，不能默认 0.5 |
| Diet Shift | `DietaryShiftDelta(prey family)` | 相对基础食性的动态偏移，按猎物家族分别给出 | 与 FoodValue 同标尺的有符号偏移 | 该 family 的 FoodValue 不可闭合 |
| Wariness | `RiskCost` 的乘子 | 对已解析风险线索有多敏感 | `W ∈ [0,1]` | Risk 不可闭合；当前 Risk cue 未实现时整体为 0 |

### 3.1 Activity

- 只调制追赶负担，不进入 Closing 的结构速度上限；
- 必须能表达“当前不积极但物理上仍追得上”；
- 不能与 Feeding Motivation 共用一个“积极程度”标量。

### 3.2 Feeding Motivation

- 只移动门槛，不乘 FoodValue；
- `M=0.5` 是参考摄食意愿，不是默认填充值；
- 高 Motivation 不复活 `Reject`。

### 3.3 Diet Shift

- 是相对基础食性的偏移，不是全局食欲；
- 必须按 prey family 给出，不能只给一个总数；
- 与 Feeding Motivation 分开：前者改变“哪种食物更值”，后者改变“现在多愿意出手”。

### 3.4 Wariness

- 只放大已解析的 `SuspicionLoad`；
- 没有可疑线索时，高 Wariness 不产生风险顾虑；
- fishing pressure 若已作为 Wariness 的上游原因，不得再进入 SuspicionLoad。

## 4. 粒度与载体

Response 读取的是已烘焙的 Fish Condition，不在运行时重新生成：

```text
条件组 × 中鱼习性模式
→ Fish Condition（Activity / Motivation / Diet Shift / Wariness）
→ Response 只读消费
```

要求：

- 每个值必须带有效区间与来源；过期或越界即 `Unknown`；
- Response 不得对 Fish Condition 做插值、平滑或反推；
- 不得把运行时玩家操作写回 Fish Condition；
- 窝料、持久响应场只提供上游原因或独立输入，不直接改写 Fish Condition。

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

## 6. 第一版 Bake 最小输出

不需要先实现完整生态模型。最低可消费集合：

| 输出 | 最小要求 |
|---|---|
| Activity | 每个条件组 × 模式一个倍率或 `Unknown` |
| Feeding Motivation | 每个条件组 × 模式一个 `[0,1]` 值或 `Unknown` |
| Diet Shift | 每个条件组 × 模式 × prey family 一个偏移或 `Unknown` |
| Wariness | 每个条件组 × 模式一个 `[0,1]` 值或 `Unknown` |

允许第一版只产出常量或按天气 / 时段分档的值；关键是状态与边界正确，不是公式复杂。

## 7. 验收

Response 侧应能验证：

1. `Unknown` 的 Activity 不会默认成 1.0；
2. `Unknown` 的 Motivation 不会默认成 0.5；
3. `Wariness` 高但没有 cue 时 `RiskCost=0`；
4. 同一 prey family 的 Diet Shift 只影响该 family 的 FoodValue；
5. 运行时玩家操作不会改写任何 Fish Condition；
6. 过期的 Fish Condition 被标为 `Unknown`，而不是沿用最后值。

## 8. 未决

- 四个 Condition 的生成公式与时间粒度；
- DEF 中 Fish Condition 的字段形态与版本；
- 各 Condition 的 owner 与审核流程；
- 天气 / 时段 / 钓压等上游数据来源；
- 圆桌与其它消费者是否读取同一份 Fish Condition；
- 第一版是否允许常量占位，以及占位值如何标注。

## 9. 来源

- `docs/terminology.md` §4、§5.2（Working Terminology Ledger）；
- `docs/fish-habit-editor-v1/common-semantics.md` §13（V1 负向清单）；
- `reference/0340-fixed-bake/README.md`（参考实现范围）；
- `docs/groundbait-recipe/candidate/response-stage-mapping.md`（只读边界）。

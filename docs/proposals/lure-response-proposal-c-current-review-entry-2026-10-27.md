# Proposal C｜当前审阅入口（2026-10-27）

状态：Working Review Entry / Candidate。不是 Current，不是生产参数。

用途：Proposal C 的统一审阅入口。本页只做导航和审阅指引，不重复维护公式与数值；当前设计语义以设计包为准，避免同一口径在入口和子文档各写一份。

> 若本文与更高 Authority 冲突，以 `docs/authority-model.md` 与已合并 Current Owner 为准。本页现在是 `main` 上 Proposal C Candidate 设计包的统一审阅入口；研究分支只作为持续研究与历史证据来源，不能覆盖已经回写并合并到 `main` 的设计包。
>
> 2026-10-30 同步：第一版 `DecisionMargin` 使用五项式；Prediction 为 `Deferred Research`；`L` 的正式 owner 是 Opportunity，Spatial 只提供空间事实。依据：Proposal C Working Closure（PR [#130](https://github.com/futouyiba/HitFish-Up/pull/130) 提交 `5caf1f119ab6e5a5c595a4ba913e7962aa338ec3`）§4–§5、Issue [#152](https://github.com/futouyiba/HitFish-Up/issues/152) 与 Issue [#161](https://github.com/futouyiba/HitFish-Up/issues/161)。
>
> 2026-10-30 会议方向已由 PR #171 回写并合并到设计包：不模拟相对方位 θ、同级猎物解释取最大值、Fish Condition 一竿一个快照；`K_close` 按单方向标尺改为 `0.19`。

## 1. 当前设计入口

| 要回答的问题 | 入口 |
|---|---|
| 主链、负向边界、计算顺序 | [设计骨架](lure-response-proposal-c-design-spine.md) |
| 每层的输入、输出、状态与 owner | [语义契约](lure-response-proposal-c-semantic-contract.md) |
| 证据、支持度插值、区间与状态提取 | [呈现解释与状态契约](lure-response-proposal-c-presentation-interpretation.md) |
| 五评价项的合成方式与边界 | [五评价项契约](lure-response-proposal-c-evaluation-items.md) |
| 投影、sibling 取最大与候选接入 | [响应与机会契约](lure-response-proposal-c-response-opportunity.md) |
| 用反例检查设计 | [工作案例](lure-response-proposal-c-worked-cases.md) |
| 未收口、无 owner 或冲突的问题 | [开放决策](lure-response-proposal-c-open-decisions.md) |
| 第一轮玩法闭合：AttackTrigger、Risk 输入、策略 probe | [第一轮闭合审查](lure-response-proposal-c-first-round-closure.md) |
| Escape-like 第一版事实与判定 | [Escape-like Trigger v1](lure-response-proposal-c-escape-trigger-v1.md) |
| 机会量与单位时间收益的玩具模型 | [机会量支持](lure-response-proposal-c-opportunity-support.md) |
| 机会量的生产结构：遭遇率、窗口、身份与归约 | [L 生产函数草案](lure-response-proposal-c-opportunity-l-production.md) |
| 提交给独立裁定人的问题单 | [裁定请求](lure-response-proposal-c-adjudication-request.md) |
| 顾问建议与 2026-10-30 Owner 确认 | [建议记录](lure-response-proposal-c-adjudication-recommendation-2026-10-30.md) |
| Fish Condition 与 Bake 的反推需求 | [鱼况/Bake 契约](lure-response-proposal-c-fish-condition-bake-contract.md) |
| Fish Condition 裁决记录（2026-10-30） | [裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md) |
| Fish Condition 剩余七项：Owner 决定请求 | [Owner 决定请求](lure-response-proposal-c-fish-condition-owner-decisions.md) |
| Fish Condition 的载体、状态与校验 | [Fish Condition Production Contract](lure-response-proposal-c-fish-condition-production-contract.md) |
| 端到端 Response 算法规格 | [Response Algorithm v1](lure-response-proposal-c-response-algorithm-v1.md) |
| 四个 Fish Condition 的机制草案 | [Fish Condition 机制契约](lure-response-proposal-c-fish-condition-mechanisms.md) |
| 规则到 probe 的覆盖关系 | [回归矩阵](lure-response-proposal-c-regression-matrix.md) |
| 当前 Working 参数与缺数据 | [标定台账](lure-response-proposal-c-calibration-register.md) |
| 图形化说明 | [设计图](../mockups/proposal-c-design-map.html) |

口径状态：当前 Candidate 口径以 `main` 上本设计包为准。早期 `docs/lure-response-joint-evaluation` 的 `311ae70d` Working Closure 及后续研究提交保留为证据来源；新的研究结论只有在回写设计包并经 PR 合并后，才改变本入口所指向的当前 Candidate 设计。

### 各层状态（Candidate）

| 层 | 文档 | 状态 | 主要缺口 |
|---|---|---|---|
| 呈现事实 | 呈现解释与状态契约 | 已写接口 | 生产采集、遮挡与可见性 |
| 猎物解释 | 呈现解释与状态契约 | 已写规则 | 生产锚点、family 表 |
| 状态提取 | 呈现解释与状态契约 | 已写规则 | 采样、滤波、姿态输入 |
| 触发 | Escape-like v1 | 已准入一种 | 事件阈值、family 适用 |
| 五评价项 | 五评价项契约 | 已写合成与边界 | 生产标定、Risk 无输入 |
| 投影 | 响应与机会契约 | M0/M1 Working | reference calibration |
| sibling | 响应与机会契约 | 同级取最大 | 生产组合分布 |
| 机会 | 响应与机会契约、机会量支持 | seam + 玩具模型 | `L` 生产函数与 reducer |
| 候选 | 响应与机会契约 | 接口 | Candidate reducer |
| Fish Condition | 契约、Production Contract、机制草案 | 架构已裁、机制骨架 | 生成曲线与数据 |
| 端到端 | Response Algorithm v1 | 可执行规格 + probe | 生产参数 |

## 2. 第一版主体

```text
出手余量
= 食物价值
+ 攻击诱因
- 追赶负担
- 风险顾虑
- 摄食意愿门槛
```

详细定义、数值范围与状态传播见语义契约。三条最容易在评审中读错的边界：

- 预测困难当前不在主体内，只作为待证明的局部代价；
- 机会量 `L` 归 Opportunity；Spatial 只提供位置、区域、几何等空间事实；`q = L × C` 只乘一次；
- `Reject`、`Unknown`、`ResolutionIncomplete` 都是 typed 状态，不用超大 cost 或零值模拟。

## 3. 当前仍成立的结构边界

以下不应被审阅者无反例地重新打开：

1. FoodValue 与 FeedingMotivation 分离；
2. Activity 与 FeedingMotivation 正交，Activity 只调制追赶负担，不降低物理速度能力；
3. Reject 与 Poor typed semantics 分离，Poor 可在极端有利条件下弱响应；
4. CurrentFoodValue 完整连续域 `[0,1]`；
5. sudden turn 在诊断或候选评估中可以同时记录 Trigger 正效应与 Prediction 负效应，但不合并成新字段；第一版生产主体不含 Prediction，只有出现独立策略价值证据时才重开；
6. `q >= 1 → hard-zero` 已撤回，Closing 只解释径向分离负担；
7. 垂直运动经 Opportunity 的垂直可交互窗口进入 `L`，不进入 Closing（Spatial 只提供空间事实）；
8. sibling 取最大值；未解析分支跳过并记录，不当作 0；
9. high speed / low prey support / pause 不产生匿名 Suspicion 或 bonus；
10. combined soft burden 不加 runtime total cap；
11. temporal duration 不进入出手余量；
12. Response 不内建 ExposureRate，也不按持续时间积分。

## 4. 审阅者建议攻击点

1. 五个评价项是否真的购买不同玩家策略，还是有两项在重复买同一维度；
2. 攻击诱因是否可能变成免费收益；
3. 追赶负担在低活性与高速组合下是否给出正确排序；
4. 风险顾虑的第一版实现层是否够用，是否会把自然呈现误判；
5. 同级取最大时，未解析分支跳过是否掩盖了应阻断的情况；
6. 机会量与响应的 `L × C` 是否存在系统性过度衰减；
7. Prediction 是否出现独立策略价值证据；没有证据时维持不进第一版主体；
8. 哪些开放项真正阻塞生产，哪些只是标定。

审阅者必须区分事实、Candidate、Working seed、建议；不能把缺少 owner 的内容补造成生产规则。替代方案必须指出它替换哪个归属方、消除了什么重复计权，以及对回归证据的影响。

## 5. 可复核入口

- [`proposal_c_prediction_challenge_probe.py`](../../prototypes/lure-response/proposal_c_prediction_challenge_probe.py)：Prediction challenge 形状；
- [`proposal_c_response_projection_probe.py`](../../prototypes/lure-response/proposal_c_response_projection_probe.py)：响应投影形状比较；
- [`proposal_c_closing_cost_shape_probe.py`](../../prototypes/lure-response/proposal_c_closing_cost_shape_probe.py)：Closing 成本形状；
- [`proposal_c_support_retention_projection_probe.py`](../../prototypes/lure-response/proposal_c_support_retention_projection_probe.py)：support × response retention；
- [`proposal_c_strategy_probe.py`](../../prototypes/lure-response/proposal_c_strategy_probe.py)：追赶、摄食意愿、警戒度三组策略排序与敏感度；
- [`proposal_c_escape_trigger_probe.py`](../../prototypes/lure-response/proposal_c_escape_trigger_probe.py)：逃逸样事件窗口、family 适用与取 max 判定；
- [`proposal_c_opportunity_support_probe.py`](../../prototypes/lure-response/proposal_c_opportunity_support_probe.py)：机会量、遭遇饱和与单位时间收益；
- [`proposal_c_end_to_end_probe.py`](../../prototypes/lure-response/proposal_c_end_to_end_probe.py)：端到端状态传播与单次乘法；
- [`proposal_c_fish_condition_probe.py`](../../prototypes/lure-response/proposal_c_fish_condition_probe.py)：Fish Condition baseline、过期与授权 overlay。

这些 probe 是形状检查，不是生产标定；其参数与设计包中的 Working 值分开记录。

## 6. 完成度

设计、逻辑、机制与算法已推到 Candidate 完成度：

- 各层契约、端到端算法、状态代数与失败对照已写入文档；
- 规则到 probe 的覆盖写在[回归矩阵](lure-response-proposal-c-regression-matrix.md)；
- 当前 Working 参数与缺数据写在[标定台账](lure-response-proposal-c-calibration-register.md)；
- 9 个 probe 全部可运行。

不声称生产闭合。仍缺：Fish Condition 的生成曲线与数据、机会量 `L` 的生产函数、事件提取阈值、各参数标定，以及 `TackleConspicuousness` 的字段与 owner。

# Proposal C｜Current Review Entry（2026-10-27）

状态：Working Review Entry / Candidate。不是 Current，不是生产参数。

用途：Proposal C 的统一审阅入口。本页只做导航和审阅指引，不重复维护公式与数值；当前设计语义以设计包为准，避免同一口径在入口和子文档各写一份。

> 若本文与更高 Authority 冲突，以 `docs/authority-model.md` 与已合并 Current Owner 为准。本文是 `futou-/exciting-payne-95a562` 分支的审阅入口；Proposal C 的 Working 研究文档保留在 `docs/lure-response-joint-evaluation` 分支。

## 1. 当前设计入口

| 要回答的问题 | 入口 |
|---|---|
| 主链、负向边界、计算顺序 | [设计骨架](lure-response-proposal-c-design-spine.md) |
| 每层的输入、输出、状态与 owner | [语义契约](lure-response-proposal-c-semantic-contract.md) |
| 证据、支持度插值、区间与状态提取 | [呈现解释与状态契约](lure-response-proposal-c-presentation-interpretation.md) |
| 五评价项的合成方式与边界 | [五评价项契约](lure-response-proposal-c-evaluation-items.md) |
| 投影、sibling 区间与候选接入 | [响应与机会契约](lure-response-proposal-c-response-opportunity.md) |
| 用反例检查设计 | [工作案例](lure-response-proposal-c-worked-cases.md) |
| 未收口、无 owner 或冲突的问题 | [开放决策](lure-response-proposal-c-open-decisions.md) |
| 第一轮玩法闭合：AttackTrigger、Risk 输入、策略 probe | [第一轮闭合审查](lure-response-proposal-c-first-round-closure.md) |
| Escape-like 第一版事实与判定 | [Escape-like Trigger v1](lure-response-proposal-c-escape-trigger-v1.md) |
| 机会量与单位时间收益的玩具模型 | [机会量支持](lure-response-proposal-c-opportunity-support.md) |
| 提交给独立裁定人的问题单 | [裁定请求](lure-response-proposal-c-adjudication-request.md) |
| 顾问建议与 2026-10-30 Owner 确认 | [建议记录](lure-response-proposal-c-adjudication-recommendation-2026-10-30.md) |
| Fish Condition 与 Bake 的反推需求 | [鱼况/Bake 契约](lure-response-proposal-c-fish-condition-bake-contract.md) |
| Fish Condition 裁决记录（2026-10-30） | [裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md) |
| Fish Condition 剩余七项：Owner 决定请求 | [Owner 决定请求](lure-response-proposal-c-fish-condition-owner-decisions.md) |
| Fish Condition 的载体、状态与校验 | [Fish Condition Production Contract](lure-response-proposal-c-fish-condition-production-contract.md) |
| 图形化说明 | [设计图](../mockups/proposal-c-design-map.html) |

口径来源：本包按 `docs/lure-response-joint-evaluation` 的 `311ae70d` Working Closure 快照核对。该分支在此之后持续更新，本轮未逐条重新纳入；引用前先核对该分支当前 head。研究分支更新后，先回写设计包，再更新本入口。

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
- 机会量 `L` 由 Spatial / Opportunity 提供，`q = L × C` 只乘一次；
- `Reject`、`Unknown`、`ResolutionIncomplete` 都是 typed 状态，不用超大 cost 或零值模拟。

## 3. 当前仍成立的结构边界

以下不应被 Reviewer 无反例地重新打开：

1. FoodValue 与 FeedingMotivation 分离；
2. Activity 与 FeedingMotivation 正交，Activity 只调制追赶负担，不降低物理速度能力；
3. Reject 与 Poor typed semantics 分离，Poor 可在极端有利条件下弱响应；
4. CurrentFoodValue 完整连续域 `[0,1]`；
5. sudden turn 在诊断或候选评估中可以同时记录 Trigger 正效应与 Prediction 负效应，但不合并成新字段；第一版生产主体不含 Prediction，是否重入待裁定；
6. `u_close >= 1 → hard-zero` 已撤回，Closing 只解释径向分离负担；
7. 垂直运动归 Spatial / Opportunity，不进入 `u_close`；
8. sibling 使用有界部分解析，区间收敛才输出标量；
9. high speed / low prey support / pause 不产生匿名 Suspicion 或 bonus；
10. combined soft burden 不加 runtime total cap；
11. temporal duration 不进入出手余量；
12. Response 不内建 ExposureRate，也不按持续时间积分。

## 4. Reviewer 建议攻击点

1. 五个评价项是否真的购买不同玩家策略，还是有两项在重复买同一维度；
2. 攻击诱因是否可能变成免费收益；
3. 追赶负担在低活性与高速组合下是否给出正确排序；
4. 风险顾虑的第一版实现层是否够用，是否会把自然呈现误判；
5. 有界部分解析是否在真实 sibling 组合下频繁停在不完整状态；
6. 机会量与响应的 `L × C` 是否存在系统性过度衰减；
7. Prediction 是否出现独立策略价值证据；没有证据时维持不进第一版主体；
8. 哪些开放项真正阻塞生产，哪些只是标定。

Reviewer 必须区分事实、Candidate、Working seed、建议；不能把缺少 owner 的内容补造成生产规则。替代方案必须指出它替换哪个归属方、消除了什么重复计权，以及对回归证据的影响。

## 5. 可复核入口

- [`proposal_c_prediction_challenge_probe.py`](../../prototypes/lure-response/proposal_c_prediction_challenge_probe.py)：Prediction challenge 形状；
- [`proposal_c_response_projection_probe.py`](../../prototypes/lure-response/proposal_c_response_projection_probe.py)：响应投影形状比较；
- [`proposal_c_closing_cost_shape_probe.py`](../../prototypes/lure-response/proposal_c_closing_cost_shape_probe.py)：Closing 成本形状；
- [`proposal_c_support_retention_projection_probe.py`](../../prototypes/lure-response/proposal_c_support_retention_projection_probe.py)：support × response retention；
- [`proposal_c_strategy_probe.py`](../../prototypes/lure-response/proposal_c_strategy_probe.py)：追赶、摄食意愿、警戒度三组策略排序与敏感度；
- [`proposal_c_escape_trigger_probe.py`](../../prototypes/lure-response/proposal_c_escape_trigger_probe.py)：逃逸样事件窗口、family 适用与取 max 判定；
- [`proposal_c_opportunity_support_probe.py`](../../prototypes/lure-response/proposal_c_opportunity_support_probe.py)：机会量、遭遇饱和与单位时间收益。

这些 probe 是形状检查，不是生产标定；其参数与设计包中的 Working 值分开记录。

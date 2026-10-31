# Proposal C｜当前审阅入口（2026-10-27）

状态：Working Review Entry / Candidate。不是 Current，不是生产参数。

用途：Proposal C 的统一审阅入口。本页只做导航和审阅指引，不重复维护公式与数值；当前设计语义以设计包为准，避免同一口径在入口和子文档各写一份。

> 若本文与更高 Authority 冲突，以 `docs/authority-model.md` 与已合并 Current Owner 为准。
>
> 2026-10-30～31 已同步：第一版出手余量使用五项式；运动可预测性（Prediction）不进入第一版 active numeric core；机会量 `L` 的正式 owner 是 Opportunity，Spatial 只提供空间事实；第一版不模拟相对方位 θ；同级猎物解释取最大值；Fish Condition 使用一竿一个快照；`K_close` 按单方向标尺使用 Working 值 `0.19`。
>
> 2026-10-31 补充：跨 feature 的重复计权与 owner 边界由 [Feature Ownership Matrix](lure-response-proposal-c-feature-ownership-matrix.md) 承接；跨文档负向边界见[路亚响应设计护栏](../design-guardrails/lure-response.md)。

## 1. 当前设计入口

| 要回答的问题 | 入口 |
|---|---|
| 主链、负向边界、计算顺序 | [设计骨架](lure-response-proposal-c-design-spine.md) |
| 每层的输入、输出、状态与 owner | [语义契约](lure-response-proposal-c-semantic-contract.md) |
| 证据、支持度插值、猎物状态与过程 | [呈现解释与状态契约](lure-response-proposal-c-presentation-interpretation.md) |
| 五评价项的合成方式与边界 | [五评价项契约](lure-response-proposal-c-evaluation-items.md) |
| 投影、sibling 取最大与候选接入 | [响应与机会契约](lure-response-proposal-c-response-opportunity.md) |
| 跨 feature owner 与防重复计权 | [Feature Ownership Matrix](lure-response-proposal-c-feature-ownership-matrix.md) |
| 跨文档负向边界、不得恢复的路线 | [路亚响应设计护栏](../design-guardrails/lure-response.md) |
| 用反例检查设计 | [工作案例](lure-response-proposal-c-worked-cases.md) |
| 未收口、无 owner 或冲突的问题 | [开放决策](lure-response-proposal-c-open-decisions.md) |
| 第一轮玩法闭合：攻击诱因、Risk 输入、策略 probe | [第一轮闭合审查](lure-response-proposal-c-first-round-closure.md) |
| 逃逸样第一版事实与判定 | [Escape-like Trigger v1](lure-response-proposal-c-escape-trigger-v1.md) |
| 机会量与单位时间收益的玩具模型 | [机会量支持](lure-response-proposal-c-opportunity-support.md) |
| 机会量的生产结构：遭遇率、窗口、身份与归约 | [L 生产函数草案](lure-response-proposal-c-opportunity-l-production.md) |
| 提交给独立裁定人的问题单 | [裁定请求](lure-response-proposal-c-adjudication-request.md) |
| 顾问建议与 2026-10-30 Owner 确认 | [建议记录](lure-response-proposal-c-adjudication-recommendation-2026-10-30.md) |
| Fish Condition 与 Bake 的反推需求 | [鱼况/Bake 契约](lure-response-proposal-c-fish-condition-bake-contract.md) |
| Fish Condition 裁决记录（2026-10-30） | [裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md) |
| Fish Condition 的载体、状态与校验 | [Fish Condition Production Contract](lure-response-proposal-c-fish-condition-production-contract.md) |
| 端到端 Response 算法规格 | [Response Algorithm v1](lure-response-proposal-c-response-algorithm-v1.md) |
| 四个 Fish Condition 的机制草案 | [Fish Condition 机制契约](lure-response-proposal-c-fish-condition-mechanisms.md) |
| 规则到 probe 的覆盖关系 | [回归矩阵](lure-response-proposal-c-regression-matrix.md) |
| 当前 Working 参数与缺数据 | [标定台账](lure-response-proposal-c-calibration-register.md) |
| 图形化说明 | [设计图](../mockups/proposal-c-design-map.html) |
| 会议叙事与玩家策略故事 | [会议对齐稿](../alignment/lure-response/2026-10-30-lure-response-alignment-draft.md) |

### 各层状态（Candidate）

| 层 | 文档 | 状态 | 主要缺口 |
|---|---|---|---|
| 呈现事实 | 呈现解释与状态契约 | 已写接口 | 生产采集、遮挡与可见性 |
| 猎物解释 | 呈现解释与状态契约 | 已写规则 | 生产锚点、prey family 表 |
| 状态提取 | 呈现解释与状态契约 | 已写规则 | 采样、滤波、姿态输入 |
| 触发 | Escape-like v1 | 已准入一种 | 事件阈值、family 适用 |
| 五评价项 | 五评价项契约 | 已写合成与边界 | 生产标定、Risk 无生产输入 |
| 投影 | 响应与机会契约 | M0/M1 Working | reference calibration |
| sibling | 响应与机会契约 | 同级取最大 | 真实 sibling 分布复核 |
| 机会 | 响应与机会契约、机会量支持、L 生产函数草案 | seam + Candidate | `L` 生产函数与 reducer |
| 候选 | 响应与机会契约 | 接口 | Candidate reducer |
| Fish Condition | 契约、Production Contract、机制草案 | 架构已裁、机制骨架 | 生成曲线与数据 |
| 跨 feature ownership | Feature Ownership Matrix | 已写边界 | 与生产字段联调 |
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

三条最容易读错的边界：

- 运动可预测性不在第一版主体；只有控制现有路径后仍证明存在独立、稳定、可学习的策略排序，才重开；
- 机会量 `L` 归 Opportunity；Spatial 只提供位置、区域、几何等空间事实；`L × C` 只乘一次；
- `Reject`、`Unknown`、`NotConfigured`、`ResolutionIncomplete` 都是 typed 状态，不用超大 cost 或零值模拟。

## 3. 当前仍成立的结构边界

以下不应被无反例地重新打开：

1. FoodValue 与 Feeding Motivation 分离；
2. Activity 与 Feeding Motivation 正交，Activity 只调制追赶负担，不修改物理速度能力；
3. Reject 与 Poor typed semantics 分离，Poor 可在极端有利条件下弱响应；
4. CurrentFoodValue 的连续域为 `[0,1]`；
5. sudden turn / burst 只有在猎物解释器将其解析为 Escape-like 时才形成攻击诱因；若 burst 同时改变实际速度，Closing 可独立读取速度变化；不再产生 active PredictionCost；
6. `q >= 1 → hard-zero` 已撤回；第一版不模拟相对方位 θ，按“鱼在追拟饵”估算追赶负担；
7. 垂直运动经 Opportunity 的垂直可交互窗口进入 `L`，不进入 Closing；
8. sibling 取最大值；未解析分支按状态协议记录，不当作 0；
9. high speed / low prey support / pause 不产生匿名 Suspicion 或 bonus；
10. combined soft burden 不加 runtime total cap；
11. temporal duration 不进入出手余量，且不预设“停留越久，L 必然越大”；
12. Response 不内建 ExposureRate，也不按持续时间积分；
13. Candidate 不重新解释 Response，也不再次乘 `C`；
14. Fish Condition baseline 在抛竿开始时形成快照，本竿只读；下一竿重新解析。

## 4. 审阅者建议攻击点

1. 五个评价项是否购买不同玩家策略，是否仍有重复计权；
2. 攻击诱因是否会变成免费收益；
3. 追赶负担在低 Activity 与高速组合下是否给出正确排序；
4. 终端钓组显眼度是否有足够数据与玩法价值支撑 Risk 上线；
5. 同级取最大时，跳过未解析 sibling 是否在真实分布上产生偏差；
6. 机会量与适配系数的 `L × C` 是否系统性过度衰减；
7. 体型档是否足以表达尺寸偏好与追赶能力，何时必须拆 cohort；
8. 哪些开放项真正阻塞生产，哪些只是标定。

替代方案必须指出它替换哪个 owner、消除了什么重复计权，以及对回归证据的影响。

## 5. 可复核入口

当前主 probe：

- `proposal_c_response_projection_probe.py`：响应投影；
- `proposal_c_closing_cost_shape_probe.py`：单方向 Closing 成本形状；
- `proposal_c_support_retention_projection_probe.py`：support × response retention；
- `proposal_c_strategy_probe.py`：追赶、摄食意愿、警戒度策略排序；
- `proposal_c_escape_trigger_probe.py`：逃逸样事件与 family 适用；
- `proposal_c_opportunity_support_probe.py`：机会量与单位时间收益；
- `proposal_c_end_to_end_probe.py`：端到端状态传播与单次 `L × C`；
- `proposal_c_fish_condition_probe.py`：Fish Condition baseline / snapshot 与授权 overlay。

旧 Prediction probe 只作为“为何第一版不需要独立 PredictionCost”的研究证据，不属于 active numeric core。

这些 probe 是形状检查，不是生产标定。

## 6. 完成度

设计、逻辑、机制与算法已推到 Candidate 完成度：

- 主链、五项评价、状态协议、Opportunity seam 与 Fish Condition 架构已写入文档；
- 2026-10-30～31 的会议方向已回写设计包；
- 防重复计权与跨 feature ownership 有独立入口；
- 回归矩阵与标定台账分别承接 probe 覆盖和 Working 参数。

不声称生产闭合。仍缺：Fish Condition 的生成曲线与数据、机会量 `L` 的生产函数、事件提取阈值、各参数标定，以及终端钓组显眼度的生产字段与 owner。
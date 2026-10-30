# Proposal C｜开放决策

状态：Working Design / Candidate。这里只列尚未收口、尚未有 owner 或两侧口径冲突的问题。

> 2026-10-30 Owner 已确认五项顾问建议，记录见[建议记录](lure-response-proposal-c-adjudication-recommendation-2026-10-30.md)。下面的「已裁定」条目按该裁定执行；其余条目保持原状态。

## 1. 已裁定（2026-10-30）

| 议题 | 裁定 | 影响 |
|---|---|---|
| 探索 / 信息覆盖 | 不新增独立数值机制；实际空间覆盖由 Opportunity 保留，不奖励“快搜”标签 | Response 不加搜索奖励 |
| Risk MVP | 只立 `TackleConspicuousness`，可后置实现；`EntryDisturbance` 暂不实现 | 实现前 `RiskCost` 仍为 0 |
| CapacityModifier | 从 active design 删除 | 契约不再列可选聚合 |
| Prediction | 第一版不含，状态改为 `Deferred Research` | 不再是当前待设计项 |
| `L` owner | 正式归 Opportunity；Spatial 只提供空间事实 | `q = L × C` 不变 |

### 重开条件

- **探索 / 信息覆盖**：发现 Opportunity 架构无法表达“扫过更多空间意味着更多有效试探”时，按 Opportunity 实现缺口处理，不在 Response 加 bonus。
- **CapacityModifier**：species / size 能力基线加 Activity 仍无法解释某类必要玩法差异，且该差异确实是“当前实际运动能力改变”，不是“愿不愿追”。
- **Prediction**：固定 FoodValue、AttackTrigger、Closing、Risk、Motivation、Opportunity `L`，只改变运动可预测性，仍得到稳定、可复现、玩家能理解且足以改变打法选择的排序；不能只靠统计拟合改善。

## 2. Owner 缺口

- Feeding、Defense、Investigation 的 Interaction composition；
- `TackleConspicuousness` 的字段与数据 owner：2026-10-30 裁定暂不投入，`RiskCost=0`；需要交付真实警戒玩法时再立项；
- Wariness runtime overlay 的事件来源、粒度、衰减、有效期与会话记忆边界：职责已归 Fish Condition 线，具体机制 Contract 未闭合；
- 若未来启用 `ExplicitDirectional` bearing prior，production directional support 的 owner；
- 垂直可交互窗口的正式实现 owner（`L` 归 Opportunity 后由该线承接）。

## 3. 语义缺口

- AttackTrigger：Escape-like 已准入；Injured / Struggling 与 imbalance-like vulnerability 为 `CandidateUnresolved`，等 cue-only holdout；pause 本身不得作为 Trigger；
- Risk：只立 `TackleConspicuousness`，`EntryDisturbance` 暂不实现；实现前 `RiskCost = 0`，Wariness 暂无真实玩家策略消费方；
- 完整自然度模型；
- 非摄食咬击（护巢、领地、防御、烦躁）如何作为独立 family 组合；
- Fish Condition：Owner 2026-10-30 裁定「Bake baseline + 仅机制授权的 runtime overlay → resolved → Response 只读」；V1 可只实现 baseline；见 [Issue #161](https://github.com/futouyiba/HitFish-Up/issues/161)；
- Fish Condition 名单与生成方式：名单沿用现行四个鱼况；各 Condition 的语义、曲线与标定归对应机制 Contract，Bake 只负责执行、物化与校验；
- 装配版本变化时，共用轨迹记忆可以保留到什么边界。

## 4. 标定缺口

- FoodValue relation anchors 的生产来源；
- 动机 tail 的起点 `0.80` 与额外斜率 `0.50`；
- `StateTrigger` 的最终预算；
- `K_close`、`K_wary`、`tau_recover`；
- `M0 / M1` 的 reference calibration，当前 Working `M1=0.40`；
- prey support、response、opportunity 和 Candidate 的整链分布；
- saturation 和 zero-response guardrails。

## 5. 数据缺口

- 实际水流与相对水体速度的稳定来源；
- 鱼与饵的 encounter geometry、reaction window 和 strike reach；
- 各鱼种 `InterceptSpeedLimit` 与体型缩放来源；
- 猎物解释所需的可见性、遮挡和装配局部数据；
- `TackleConspicuousness` 的装备 / 线组事实来源；
- 机械操控暴露指标的实际采集口径（来源：`lure-response-proposal-c-mechanical-control-exposure-metrics.md`）。

## 6. 本轮不做的事

- 不把 Working seed 升格为 production parameter；
- 不把 Proposal C 研究分支的文件当作当前 Contract；
- 不为缺少 owner 的内容补造公式；
- 不通过新增 runtime cap 掩盖重复计权或标定失败；
- 不在 Response 内增加搜索奖励或单位时间效率模型；
- 不恢复已删除的 `CapacityModifier` 或 Prediction 主体项，除非满足重开条件。

## 7. 下一轮收口顺序

1. Escape-like 的事件提取（滤波、采样、最短间隔）、family 适用表、强度缩放、窗口与刷新语义仍 OPEN，下一步是轨迹采集与这些参数的落定；
2. `TackleConspicuousness`：按 2026-10-30 裁定暂不投入，`RiskCost` 保持 0；需要真实警戒玩法时再立项字段与 owner；
3. 机会量 `L` 归 Opportunity 后，由该线补生产函数、单位与窗口口径；
4. 用 `proposal_c_strategy_probe.py` 的排序结果检查参数敏感度，再进入生产标定；
5. Fish Condition / Bake：Owner 已裁定架构与七项；下一步是 DEF baseline block 的字段形态与校验、各 Condition 的机制 Contract，再谈上游输入与公式；
6. Prediction 保持 `Deferred Research`，满足重开条件时再单独开题。

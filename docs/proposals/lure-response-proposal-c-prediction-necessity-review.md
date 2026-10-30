# Proposal C｜Prediction Deferred Research Gate

状态：Deferred Research。不是第一版 active Response 变量，不是生产参数。

## 1. 当前裁定

第一版不把 `PredictionChallenge` 或 `PredictionCost` 放进 active `DecisionMargin`。旧的 `TurnStrength + max_recent`、`τ_recover` 和相关 probe 只保留为历史研究证据，不作为当前实现输入。

这不是断言预测困难不存在，而是当前 probe 没有证明它购买了独立、必要且玩家可理解的策略排序。第一版先由 `FoodValue`、`AttackTrigger`（仅 `Escape-like`）、`ClosingCost`、`RiskCost` 和 `WillingnessThreshold` 完成 Response 主链。

## 2. 重开门槛

只有同时满足以下条件，才重新打开 Prediction：

```text
固定 FoodValue
固定 AttackTrigger
固定 Closing
固定 Risk
固定 Motivation
固定 Opportunity L
只改变运动可预测性
```

并且仍然得到：

- 稳定且可复现的 Response 差异；
- 玩家能够理解并通过操作影响的差异；
- 足以改变打法选择的独立策略排序；
- 不属于 Closing、Risk、AttackTrigger 或 Opportunity 已有后果的重复表达。

统计拟合改善、鱼理论上需要预测猎物、转向次数增加，均不足以通过重开门槛。

## 3. 未来研究的最低要求

如果重开，优先研究：

```text
近期实际运动
→ 形成短时预测
下一段实际运动 vs 预测
→ prediction error
```

不得直接恢复：

```text
ω_traj / fish_turn_capacity
turn magnitude = PredictionCost
```

规则圆周、稳定蛇形和其它可学习轨迹必须能与真正突然偏离区分；不能把所有转向都当成持续不可预测。

## 4. 当前不承担的职责

Prediction 不负责：

- 追赶能力或 Closing burden；
- prey-state `Escape-like` Trigger；
- Risk / Suspicion；
- pause、dwell、空间覆盖或 `L`；
- hard-zero。

本页不再维护 active Prediction 公式、effect-size budget 或生产 probe。若未来门槛成立，再另开研究记录和实现契约。

# Proposal C｜Owner 裁定记录（2026-10-29）

状态：Owner Adjudication / Working。不是 Current，不是生产参数。

本页记录 Issue #152 的五项 Owner 裁定。Issue 固定问题单基线为 `626d0653`；本页只把裁定落回 Proposal C 的 active Working 入口，不提升为已合并 Current Contract。

## 1. 总裁定

| 项目 | 裁定 | 是否阻塞第一版 | 执行归属 |
|---|---|---:|---|
| 探索 / 信息覆盖收益 | 不新增独立数值机制。空间覆盖与实际试探由 Opportunity 链路表达，不给“快搜”标签 bonus | 否 | Opportunity owner；Spatial 提供覆盖事实 |
| Risk MVP | 只准入 `TackleConspicuousness` 作为正式输入方向；第一版可后置实现。当前没有生产输入时 `RiskCost = 0` | 不阻塞 Response 主链 | Interaction / Target-Presentation Interpretation 提供事实与派生；Fish Condition 提供 Wariness |
| CapacityModifier | 从 active Candidate 删除。当前只保留重新打开条件，不进入第一版 | 否 | Future capability owner，若反例成立再开题 |
| Prediction | 第一版 Deferred，不进入 active DecisionMargin。旧 turn-event / max-recent 只作研究证据 | 否 | 后续独立研究；满足重开门槛后再回到 Response |
| `L` owner | 正式归 Opportunity。Spatial 提供位置、区域、几何和有效窗口事实；Opportunity 消费事实并产出 `L`，管理 identity / duration / dedupe / reevaluation / reducer | 是实现前接口约束 | Opportunity owner；Spatial 为事实提供者 |

## 2. 探索 / 信息覆盖收益

不新增：

```text
FastSearchInformationBonus
SearchCoverageBonus
FastLabelBonus
```

高速移动更多空间的收益属于实际空间遍历与新的 opportunity support：

```text
实际空间覆盖
→ 新的语义机会被发现 / 试探
→ Opportunity 产生对应的 native support L
```

这不是 Response 的单次 `C` 奖励，也不是 Candidate 对 `L × C` 之外再乘一个信息系数。

如果以后发现 Opportunity 无法表达“实际扫过更多空间意味着更多有效试探”，应修复 Opportunity 的 coverage / identity / reducer contract，不重开 Response bonus。

## 3. Risk MVP

正式保留的输入方向只有：

```text
TackleConspicuousness
→ SuspicionLoad

Wariness × SuspicionLoad
→ RiskCost
```

`TackleConspicuousness` 表达线、前导、钩、连接件等终端装配对当前目标的可见或侵入程度。它不是 SKU 名称，也不是从产品标签直接推断的等级；必须由配置提供可解释的 tackle / terminal fact，再由 presentation interpretation 派生风险暴露。

`EntryDisturbance` 本轮不进入第一版正式输入方向。它保留为未来候选，不得在当前链路中假定存在。

当前仓内没有生产字段或已合并 Contract，因此：

```text
Risk input = Disabled / NotConfigured
RiskCost = 0
```

这表示本轮实现未启用 Risk cue，不表示已知“没有风险”。一旦 `TackleConspicuousness` 有合法生产输入，才允许进入 `SuspicionLoad` 和 `RiskCost`；不能用 prey support、speed、turn count 或 SKU 名称代替。

## 4. CapacityModifier

从 active Proposal C 设计删除：

```text
PhysiologicalCapacityModifier
EffectiveInterceptSpeedLimit
CapacityModifier Candidate
```

当前保留：

```text
species × size cohort
→ InterceptSpeedLimit
Activity
→ soft Closing cost
```

只有出现稳定、可复现且玩家可理解的反例时，才重新打开 capability modifier：

1. species / size baseline 与 Activity 仍无法解释必要的玩法差异；
2. 差异确实表达实际运动能力改变，而不是追赶负担容忍度、摄食意愿或风险敏感度；
3. 有独立 owner、输入来源、时间尺度和不重复计权证据。

在此之前，低温、缺氧、疲劳等原因不得在 Response 内偷偷生成第二套能力修正。

## 5. Prediction

第一版不把 Prediction 放进 active numeric core：

```text
DecisionMargin
= FoodValue
+ AttackTrigger
- ClosingCost
- RiskCost
- WillingnessThreshold
```

`PredictionChallenge`、`PredictionCost`、`TurnStrength + max_recent` 和 `τ_recover` 保留为 Deferred Research / 历史 probe 语义，不是当前 OPEN 的实现项。

重开必须同时满足：

```text
固定 FoodValue
固定 AttackTrigger
固定 Closing
固定 Risk
固定 Motivation
固定 Opportunity L
只改变运动可预测性
```

并且仍得到稳定、可复现、玩家能理解、足以改变打法选择的独立 Response 排序。统计拟合改善、鱼理论上需要预测猎物，或 turn count 增加本身都不构成重开依据。

若重开，优先验证“实际下一段运动相对短时预测的偏差”，不能直接恢复通用 `ω_traj / fish_turn_capacity` 或把方向变化幅度当成预测困难。

## 6. `L` 的正式 owner

```text
Spatial
→ 位置、区域、几何、垂直层、有效空间窗口等事实

Opportunity
→ 消费 Spatial 事实
→ 生成 native opportunity support L
→ 管理 opportunity identity、duration、dedupe、reevaluation、reducer

Candidate
→ q = L × C
```

`Opportunity / Spatial` 不再作为并列 owner 表述。Spatial 是事实提供者；Opportunity 是 `L` 的唯一语义 owner。Response 不生成 `L`、ExposureRate、搜索 bonus 或单位时间信息奖励。

高速覆盖的正面结果只能通过新的空间事实与 Opportunity identity 进入 `L`；高速穿越局部区域造成的短驻留也由 Opportunity 的 temporal support 表达。

## 7. Active 主线

```text
ActualPresentation
→ Prey Interpretation
→ Prey State

→ FoodValue
→ AttackTrigger [Escape-like v1]
→ ClosingCost
→ RiskCost [当前未启用时 = 0]
→ WillingnessThreshold

→ DecisionMargin
→ Response C

Spatial facts
→ Opportunity
→ L

L × C
→ Candidate
```

第一版不含：

```text
PredictionCost
FastSearchInformationBonus
CapacityModifier
EntryDisturbance
```

`AttackTrigger` 只准入 `Escape-like`。`Injured / Struggling` 与 imbalance-like vulnerability 保持 `CandidateUnresolved`；pause 本身不进入 Trigger。

## 8. 证据边界

本页是 Owner 裁定记录，不是实现完成证明，也不替代已合并 Current Authority。相关 probe、参考实现和旧候选文档保留用于证据追溯；它们不能反向恢复本页明确 Deferred 或删除的机制。

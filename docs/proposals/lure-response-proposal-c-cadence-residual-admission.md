# Proposal C｜Cadence Motif Residual Admission

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 结论

第一版不准入独立的 `CadenceValue` / `CadenceBonus` / `CadencePenalty`。

原因不是“节奏不重要”，而是当前已经有更具体的机制承接了多数可解释效果：

- sudden redirection / burst → prey-conditioned `StateTriggerValue`；
- sudden turn → `PredictionChallenge` → `PredictionCost`；
- retrieve speed / radial separation → `ClosingCost(θ)`；
- pause duration → temporal exposure / cumulative opportunity；
- move→pause / history → prey-conditioned process interpretation / attention history。

在这些量都控制住后，当前没有足够证据证明 temporal sequence 本身还需要一个独立 scalar 才能稳定解释玩家可学习的 response ranking。

## Residual admission gate

只有出现以下 controlled fixture，才重新打开 cadence scalar：

1. prey support 相同；
2. FoodValue 相同；
3. StateTriggerValue 相同；
4. current ClosingCost distribution 相同；
5. current PredictionChallenge / PredictionCost 相同；
6. favorable temporal exposure 相同；
7. attention / target-history state 相同；
8. Feeding Motivation 相同；
9. 唯一稳定变化是 sequence / motif；
10. 该 motif 仍产生可复现、可解释、玩家可学习的 ranking difference。

在满足这些条件前，cadence 只保留为事件历史 / explain feature，不进入 DecisionMargin。

## 为什么不是 universal cadence coeff

`jerk → jerk → pause`、`steady → pause`、`burst → glide` 等模式在实钓中可能表现不同，但这些差异通常同时伴随：

- 不同的转向事件；
- 不同的速度变化；
- 不同的 prediction disruption；
- 不同的 prey-state interpretation；
- 不同的有利状态持续时间。

若直接再乘一个 cadence 系数，会把这些已存在的因果路径重复结算。

## 与外部证据的关系

当前外部证据支持“运动时序、可预测性和 strike timing 会影响捕食行为”，但不足以隔离出一个独立、通用的 cadence valuation term。因此这些资料支持保留 temporal history，不支持直接增加 universal cadence scalar。

## 当前合法结构

```text
Temporal history
├→ prey-state interpretation
├→ PredictionChallenge
├→ attention / target-history state
└→ temporal exposure
```

不增加：

```text
CadenceValue
CadenceBonus
CadencePenalty
```

## 重新打开条件

若后续出现受控测试，能在上述所有 downstream consequence 相同的前提下，只改变 motif 仍稳定改变 response，则可以重新 admission。此时还必须说明作用范围，例如 species / prey family / lure family / context，不允许默认 universal。

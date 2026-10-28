# Proposal C｜StateTrigger × Prediction 联合机制回归

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

同一次 trajectory event 可以同时产生：

```text
prey-conditioned state interpretation
→ StateTriggerValue (+)

recent trajectory disruption
→ PredictionChallenge
→ PredictionCost (-)
```

这不是重复计权，因为两条路径回答不同问题：

- `StateTriggerValue`：按当前 prey interpretation 理解，这个状态是否额外容易触发攻击；
- `PredictionCost`：无论它是否像猎物，当前轨迹是否让短时截获预测更困难。

第一版不把两者合并成 `ErraticValue`、`ManeuverNet` 或钟形曲线，也不要求它们机械抵消。

运行时仍分别进入：

```text
DecisionMargin(theta)
= FoodValue
+ StateTriggerValue
- ClosingCost(theta)
- PredictionCost
- RiskCost
- WillingnessThreshold(Motivation)
```

`StateTriggerValue - PredictionCost` 可以作为回归诊断量，但不是新的运行时字段或 owner。

## 2. 为什么同一事件允许两条路径

例如一次 sudden redirection：

```text
方向突然改变
```

对 baitfish interpretation 可能同时意味着：

```text
像逃逸 / 受伤猎物
→ 更容易诱发攻击
```

以及：

```text
未来轨迹更难预测
→ 截获决策更困难
```

这两个后果可以同时成立。

禁止双路径的标准不是“是否来自同一个 raw event”，而是“是否在重复回答同一个问题”。

如果两条路径都只是表达“动作更像猎物”，就是重复计权；当前 Trigger 与 Prediction 不属于这种情况。

## 3. 两条路径不能共享同一个强度函数

拒绝把同一个 `turn_intensity` 同时机械映射为：

```text
StateTriggerValue = A * turn_intensity
PredictionCost    = B * turn_intensity
```

然后仅靠 `A-B` 决定效果。

这种结构表面上有两个 owner，实际上只得到一个净系数：

```text
Net = (A-B) * turn_intensity
```

会失去两条机制本来要购买的独立策略表达。

第一版要求：

### Trigger 输入

Trigger 来自 **prey-conditioned state interpretation**：

```text
current prey state
→ TriggerIntensity_prey
→ StateTriggerValue
```

它可以读取 sudden redirection / burst 等事实，但必须先回答：

> 对这个 prey family，这些事实当前是否组成有攻击触发意义的 escape / distress / struggle state？

### Prediction 输入

Prediction 读取近期 trajectory disruption：

```text
TurnStrength(delta_psi)
= (1 - cos(delta_psi)) / 2

PredictionChallenge(t)
= max_recent[
    TurnStrength * exp(-age / tau_recover)
  ]

PredictionCost
= K_pred * PredictionChallenge
```

它不读取 prey family 对该动作“像不像逃逸”的价值判断。

因此同一个 event 可以进入两条路径，但映射和时间语义独立。

## 4. 当前 effect-size 关系

已有 Working budget：

```text
StateTriggerValue
≈ 0.10 ordinary
≈ 0.15 upper guardrail

PredictionCost
≈ 0.08 ~ 0.12 strong-challenge upper range
```

这些不是 production 参数。

第一版保留一个体验级护栏：

> **典型 prey-appropriate 中等 dart 应有净正向价值；单次强 dart 可以被 Prediction 明显削薄，但不应因为 Prediction 机制本身稳定变成负收益。**

因此在 calibration 上通常应满足：

```text
moderate prey-appropriate dart:
StateTriggerValue > PredictionCost
```

但不冻结为全局数学不变量：

```text
PredictionCost <= StateTriggerValue
```

不能逐 case 强制成立，因为：

- 某个动作可能只有很弱 prey-state trigger，却有很高 prediction disruption；
- 某些 prey interpretation 根本不承认该动作有 trigger，此时 Prediction 可以单独为负；
- 高频/极端动作的 Trigger 不应随事件次数累加，而 Prediction 可以持续保持高位。

旧的 `K_pred <= TriggerBudget` 只保留为粗 calibration guardrail，不作为逐事件 clamp。

## 5. 关键策略排序

控制 FoodValue、Motivation、Closing、Risk 相同，只看 Trigger / Prediction。

### A. Straight baseline

```text
Trigger = 0
Prediction = 0
→ net state effect = 0
```

### B. Prey-appropriate moderate dart

```text
Trigger = moderate-positive
Prediction = small/moderate-negative
→ net state effect > 0
```

目标：合理 twitch / dart 有实际策略价值。

### C. Very hard single dart

```text
Trigger approaches its bounded high range
Prediction approaches strong challenge
→ net benefit smaller than naïve Trigger-only result
```

不要求它必然低于 moderate dart；这取决于 prey-state interpretation。第一版只要求 Prediction 能削薄收益，而不是制造匿名“越猛越差”规则。

### D. Same turn, prey interpretation does not value it

```text
Trigger = 0 or low
Prediction > 0
→ net state effect < 0
```

同一动作不是对所有 prey family 都是奖励。

### E. Repeated extreme zig-zag

Trigger 不按 turn count 累加：

```text
StateTriggerValue
≤ TriggerBudget
```

PredictionChallenge 由反复事件不断刷新：

```text
repeated turns
→ PredictionChallenge stays elevated
```

因此不会出现：

```text
turn count ↑
→ Trigger unbounded ↑
→ response 越乱越高
```

高频极端动作可以自然趋向小净收益、零净收益，甚至负净收益，而不需要额外 `ErraticPenalty`。

## 6. 时间行为

两条路径的时间行为也不能机械绑定。

Prediction 的恢复由：

```text
tau_recover
```

控制。

Trigger 的持续时间则由 prey-conditioned state 本身决定。例如：

```text
sudden dart event
→ 可能形成短时 escape-like state
```

或：

```text
burst → pause
→ prey interpreter 可能解析成新的 vulnerable / distressed state
```

是否继续有 Trigger，取决于该 prey state contract，而不是因为 Prediction 正在衰减就自动同步衰减。

因此可以自然出现：

```text
dart 刚发生
→ Trigger 高 + Prediction 高

短暂经过后
→ Trigger 仍有意义 / 或转成另一 prey state
→ Prediction 已部分恢复
→ net response 可能更高
```

如果 prey-state 本身不支持持续 Trigger，则不能为了制造“抽停最好”而添加 `PostDartBonus` 或 `PredictionResetBonus`。

## 7. 与 ResponseProjection 的关系

当前 Working projection：

```text
C = clamp(Margin / 0.40, 0, 1)
```

因此 Trigger 与 Prediction 的净 margin 变化可以直接解释成 response effect。

例如只作量级说明：

```text
Trigger +0.10
Prediction -0.05
→ Margin +0.05
→ 在线性中段相当于 C 约 +0.125 的潜在变化
```

实际 `C` 变化仍受原始 Margin 的 0/1 clipping 影响；这不是固定增量。

这也是不再给 Trigger / Prediction 单独做第二层 projection 的原因。

## 8. 不准入的结构

当前拒绝：

```text
ErraticBonus
ErraticPenalty
ManeuverNet runtime field
PredictionOffsetToTrigger
TriggerMinusPrediction clamp
```

也拒绝：

```text
StateTriggerValue = f(turn magnitude only)
```

因为 Trigger 必须先经过 prey-conditioned state interpretation。

同样拒绝：

```text
PredictionCost = f(prey trigger intensity)
```

因为 Prediction 不应依赖鱼是否认为该状态诱人。

## 9. Regression fixtures

至少保留：

1. straight baseline；
2. prey-appropriate moderate dart；
3. prey-appropriate strong dart；
4. identical dart under a prey interpretation that does not value it；
5. repeated moderate turns；
6. repeated extreme turns；
7. dart → short pause；
8. dart → long pause。

每个 case 记录：

```text
TriggerIntensity
StateTriggerValue
PredictionChallenge
PredictionCost
StateTriggerValue - PredictionCost   # diagnostic only
DecisionMargin
C_conditional
```

主要检查：

- moderate prey-appropriate dart 相对 straight 有净收益；
- 非 prey-appropriate dart 不被误奖励；
- repeated turns 不产生 Trigger 累加爆炸；
- Prediction 能持续约束高频 disruption；
- pause 后的改善来自已有 state + Prediction decay，而不是额外 bonus。

## 10. 当前 Working Closure

第一版冻结：

```text
Prey state value
→ StateTriggerValue (+)

Trajectory predictability
→ PredictionCost (-)

两者独立计算
→ 在 DecisionMargin 中自然相抵
```

不新增统一 erratic 轴，不人为要求每次事件固定净正或净负。

Calibration 目标是策略排序，而不是让两个数字形式上“平衡”。

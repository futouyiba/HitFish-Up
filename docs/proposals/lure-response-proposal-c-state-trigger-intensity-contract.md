# Proposal C｜StateTriggerIntensity 数值契约

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

第一版把 `StateTriggerValue` 收成两层：

```text
prey-conditioned state interpreter
→ TriggerIntensity_p ∈ [0,1]

Response
→ StateTriggerValue_p
= TriggerBudget × TriggerIntensity_p
```

其中：

```text
TriggerBudget ≈ 0.10 ~ 0.15   # Working effect-size budget
```

`TriggerIntensity` 不是 raw turn magnitude、burst speed 或 event count。它是 prey-state interpreter 已经完成语义判断后的**攻击触发强度**。

Response 不再对 raw trajectory feature 自己做第二套 Trigger 解释。

## 2. 为什么要先得到 TriggerIntensity

当前第一版已经允许：

```text
sudden redirection
burst / sudden acceleration
```

作为 prey-conditioned state 的正向证据。

但不能直接写成：

```text
Trigger
= a * turn_strength
+ b * burst_strength
```

原因是：

- 一次 escape dart 往往同时包含 turn 与 burst，直接相加会重复奖励同一个行为；
- 不同 prey family 对相同 raw feature 的含义不同；
- event count 增加不应让 Trigger 无界累加；
- 轨迹是否构成 escape / distress / struggle 需要状态语义，而不是单特征阈值。

所以正确边界是：

```text
raw events / trajectory facts
→ prey-conditioned state interpretation
→ TriggerIntensity
→ TriggerBudget * intensity
```

## 3. TriggerIntensity 的标尺

最终交给 Response 的 `TriggerIntensity` 必须使用统一 `[0,1]` gauge：

```text
0
→ 当前已解析 prey state 没有额外攻击触发价值

1
→ 当前 prey family 的 reference strong-trigger state

0 < I < 1
→ 在同一 TriggerBudget 下按比例贡献触发价值
```

因此：

```text
TriggerBudget = 0.12
I = 0.5
→ StateTriggerValue = 0.06
```

这里 `I=0.5` 不表示“50% 概率是逃逸状态”，而表示该 prey-state 在 Trigger gauge 上达到 reference strong-trigger 的一半作用强度。

不同 prey family 可以使用不同的状态识别逻辑，但最终 `I=1` 必须具有相同 effect-size 语义，否则共享 `TriggerBudget` 无法成立。

## 4. raw evidence 不在 Response 内求和

Response 不消费：

```text
turn_strength
burst_strength
left_right_score
irregularity_score
```

然后自行聚合。

这些属于 prey-state interpretation 的输入。

例如 baitfish 可以把：

```text
sudden redirection
+ acceleration burst
+ recent motion context
```

解释成：

```text
EscapeLikeState
TriggerIntensity = 0.8
```

而 crayfish 对同一 raw motion 可能得到：

```text
TriggerIntensity = 0.2
```

或没有合法 trigger state。

Response 只看到最终 intensity。

## 5. 同一 prey 下多个 trigger-state 解释如何处理

若同一 physical prey state 同时可被解释为：

```text
EscapeLike
DistressedLike
StruggleLike
```

默认把它们视为**同一个当前状态的替代 trigger explanations**，不直接求和。

第一版推荐：

```text
TriggerIntensity
= max(
    I_escape,
    I_distress,
    I_struggle,
    ...
  )
```

原因：

- 同一次运动可能同时支持多个标签；
- 求和会让标签数量本身制造额外 response；
- `max` 保留最有攻击触发意义的解释，不重复结算同一 prey state。

只有未来有明确证据证明两个 trigger mechanism 可以在同一时刻独立叠加，并且购买新的稳定策略排序，才允许从 `max` 重开组合方式。

## 6. 为什么 TriggerValue 继续线性映射

第一版：

```text
StateTriggerValue
= TriggerBudget * TriggerIntensity
```

不再增加：

```text
sigmoid(I)
power(I)
soft_gate(I)
```

因为 `TriggerIntensity` 本身已经是状态解释器校准后的 effect-strength gauge。

如果低中强度需要非线性，应优先在 state interpreter 里重新定义 intensity 标尺，而不是 Response 再加第二次 projection。

Response 只负责把统一 intensity 换算到 DecisionMargin units。

## 7. 与 Prediction 的边界

同一 sudden turn 可以同时：

```text
prey-state interpreter
→ TriggerIntensity
→ StateTriggerValue (+)
```

以及：

```text
trajectory disruption
→ PredictionChallenge
→ PredictionCost (-)
```

但两条路径不能共享同一个 intensity。

TriggerIntensity 回答：

> 这对当前 prey interpretation 是不是有攻击触发意义的状态？

PredictionChallenge 回答：

> 当前轨迹在短时内有多难预测？

所以：

```text
TriggerIntensity != PredictionChallenge
```

也不能写成固定互补：

```text
PredictionChallenge = 1 - TriggerIntensity
```

## 8. 与 support 的边界

`prey support` 与 `TriggerIntensity` 也不是同一个量：

```text
support
→ 这份 prey interpretation 有多少贡献资格

TriggerIntensity
→ 假定沿这份 prey interpretation 评价，当前状态额外多能触发攻击
```

因此仍保持：

```text
FoodValue
+ StateTriggerValue
- costs
- threshold
→ C_conditional

support * C_conditional
→ C_prey
```

不让 TriggerIntensity 再修改 support。

同一 raw cue 若同时参与 support 与 Trigger，必须回答不同问题；不能把“更像逃逸小鱼”在两条路径上重复奖励成同一个效果。

## 9. 时间与重复事件

TriggerIntensity 表示**当前 prey state**，不是累计事件数量。

因此：

```text
10 次 turn
```

不会因为次数本身得到十倍 Trigger。

重复事件只会通过 state interpreter 更新当前状态与 intensity。

这与 Prediction 的 `max_recent` 不同：Prediction 可以因为新事件不断刷新 challenge；Trigger 仍受 `[0,1]` state intensity 约束。

因此 extreme repeated zig-zag 不会靠 Trigger 无限增长。

## 10. Typed status

若 prey-state trigger 所需数据缺失：

```text
TriggerIntensity = Unknown
```

且该输入对当前 prey response 是 required，则：

```text
ResolutionIncomplete
```

不能默认：

```text
Unknown → 0
```

如果该 prey family 明确没有 trigger-state valuation：

```text
TriggerModel = NotApplicable
→ StateTriggerValue = 0
```

这是声明过的不适用，不是缺数据。

## 11. Regression fixtures

至少保留：

1. straight / neutral state → `I=0`；
2. moderate prey-appropriate escape → `0<I<1`；
3. strong reference escape → `I≈1`；
4. 同一 raw dart 对不同 prey family 得到不同 intensity；
5. turn + burst 属同一 escape event 时不因两个 feature 直接相加翻倍；
6. multiple trigger labels 默认 max，不因标签数量增益；
7. repeated turns 不使 Trigger 超过 TriggerBudget；
8. Unknown 与 NotApplicable 分离。

## 12. 当前 Working Closure

第一版冻结：

```text
prey-conditioned state
→ calibrated TriggerIntensity [0,1]
→ TriggerBudget * TriggerIntensity
→ StateTriggerValue
→ additive DecisionMargin
```

并冻结：

```text
raw features do not sum directly in Response
multiple trigger-state explanations default to max
TriggerIntensity does not equal PredictionChallenge
Trigger does not accumulate by event count
```

仍未 production-closed：

- 各 prey family 如何从具体 state evidence 生成 `TriggerIntensity`；
- `TriggerBudget` 最终是全局共享还是少量 family profile；
- `0.10~0.15` effect-size budget 的生产标定。

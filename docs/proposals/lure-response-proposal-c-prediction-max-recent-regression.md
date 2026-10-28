# Proposal C｜Prediction `max_recent` 持续转向回归

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

当前：

```text
TurnStrength(delta_psi)
= (1 - cos(delta_psi)) / 2

PredictionChallenge(t)
= max_recent[
    TurnStrength
    * exp(-age / tau_recover)
  ]
```

不需要因为“持续 zig-zag 可能被低估”立即改成累加模型。

原因：重复 direction-change event 会不断刷新 `max_recent`，因此：

```text
single turn
→ challenge 出现后持续衰减

repeated turns
→ challenge 被周期性刷新
→ 形成持续较高的平台
```

所以 cadence 已经通过“事件刷新间隔相对于 `tau_recover` 的关系”进入系统，而不是完全丢失。

首版继续保留 `max_recent`。当前真正需要标定的是 `tau_recover` 与 `K_pred`。

---

## 2. 单次转向

设一次事件强度：

```text
S = TurnStrength(delta_psi)
```

事件发生后：

```text
P_single(t)
= S * exp(-t / tau_recover)
```

因此 pause 或稳定直行会自然恢复：

```text
t ↑
→ PredictionChallenge ↓
```

不需要 `PredictionResetBonus`。

---

## 3. 重复同强度转向

若同强度事件每 `Delta_t` 秒出现一次，则每次事件都会把近期最大值重新刷新到 `S`。

两个事件之间：

```text
P_repeat(t)
= S * exp(-t / tau_recover)

0 <= t < Delta_t
```

所以稳态区间内的最低值为：

```text
P_min
= S * exp(-Delta_t / tau_recover)
```

当：

```text
Delta_t << tau_recover
```

则：

```text
P_min ≈ S
```

也就是高频 zig-zag 会维持接近持续满强度的 PredictionChallenge。

当：

```text
Delta_t >> tau_recover
```

每次转向之间 challenge 已基本恢复，再次转向表现得更接近多个相互独立的单次事件。

因此 cadence 已被 `Delta_t / tau_recover` 自然表达。

---

## 4. 为什么暂不改成累加

若改为：

```text
PredictionChallenge
= sum(decayed turn events)
```

会引入新的问题：

1. 高频操作可能无上限累积，需要额外 saturation；
2. 需要决定多少历史事件进入窗口；
3. 同一个 raw turn frequency 会同时通过 prey-state pattern 与 Prediction 累积被放大；
4. 新增 accumulation shape / cap / window 等自由参数。

当前没有证据证明这些复杂度购买了新的玩家可学习排序。

`max_recent` 的优势是：

```text
大转向决定瞬时 challenge 上限
转向频率决定 challenge 能维持多久
```

两个作用已经分开。

---

## 5. 它确实不表达什么

`max_recent` 不会让：

```text
10 次相同 30° turn
```

在同一瞬间产生比：

```text
1 次 30° turn
```

更高的峰值。

它只让前者的高 challenge **持续更久**。

这是首版有意的语义：

> PredictionChallenge 表达当前预测被破坏到什么程度，不表达鱼因为历史上累计看过多少次转向而额外“欠下”多少预测债务。

如果未来要表达 habituation / repeated exposure memory，应由独立 memory / Wariness 路径拥有，而不是偷偷塞进 Prediction。

---

## 6. Alternating turns

左右交替本身不获得额外 numeric bonus / penalty。

例如：

```text
+45°
-45°
+45°
-45°
```

若每次实际 direction-change magnitude 相同，则 PredictionChallenge 主要取决于：

```text
TurnStrength(45°)
事件间隔
τ_recover
```

而不是因为“左右交替”这个模式名称再增加一层 `CadencePenalty`。

如果 prey interpreter 认为该时序更像受伤 / 逃逸猎物，它可以通过独立的 prey-state evidence 影响 StateTrigger；这与 Prediction 的职责不同。

---

## 7. `tau_recover` 的体验意义

`tau_recover` 是现在最关键的 Prediction 时间尺度。

它决定：

```text
玩家一次 twitch 后
鱼需要多久恢复对轨迹的可预测性
```

同时决定多高的操作 cadence 会被视为“持续不可预测”。

因此它不应只按数值拟合，需要用玩家操作节奏标定，例如：

```text
single twitch
slow repeated twitch
normal jerk cadence
very fast zig-zag
jerk → pause
```

要求：

- single twitch 的 penalty 不应拖太久；
- normal repeated jerk 可以保持一定 PredictionCost；
- pause 后 challenge 应明显恢复；
- very fast zig-zag 不需要无限累加，保持接近峰值即可。

---

## 8. 当前 regression stories

### A. Single turn

```text
one turn
→ P=S
→ monotonic decay
```

### B. Repeated moderate turns

```text
same S
Delta_t < tau_recover
→ challenge repeatedly refreshed
→ average / minimum challenge > single-turn long-run value
```

### C. Sparse repeated turns

```text
Delta_t >> tau_recover
→ each event nearly independent
```

### D. Turn → pause

```text
no new event
→ PredictionChallenge decays
```

### E. Repeated tiny turns vs one major turn

若 tiny-turn `S` 很低，即使高频刷新，也只维持低峰值；一次 major turn 可以产生更高峰值但随后恢复。

这提供两种不同策略语义，不需要 sum accumulation。

---

## 9. 重开 accumulation 的条件

只有 controlled fixtures 证明以下任一问题稳定存在，才重新打开 accumulation：

1. 高频中小转向与单次转向在玩家体验上应有明显不同峰值，但 `max_recent` 只能表达持续时间差；
2. 合理的 `tau_recover` 无法同时拟合 single twitch 与 repeated jerk；
3. 某些关键真实钓法排序必须依赖“多次预测错误累积”，而不是持续刷新；
4. 新增 accumulation 后能解释稳定、可学习的玩家策略，而不是只提高拟合自由度。

在此之前不新增：

```text
CadencePenalty
TurnCountPenalty
PredictionDebt
sum_recent_turns
```

---

## 10. 当前裁定

保留：

```text
PredictionChallenge(t)
= max_recent[
    TurnStrength * exp(-age / tau_recover)
  ]
```

当前 P1-B 从“结构缺口”降级为 calibration / regression：

```text
tau_recover
K_pred
```

需要与真实 presentation cadence 联合标定。

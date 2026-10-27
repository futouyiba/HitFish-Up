# Proposal C｜Poor 与 Reject 行为区分

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`Poor` 保持连续 Feeding target，`Reject` 保持 typed hard semantic boundary。

第一版不修改：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00
Reject    = hard semantic boundary
```

也不扩大 `StateTrigger` 的 Working budget。

为满足“Poor 在极端有利鱼情下可偶发越线，但普通高 Motivation 不能把 Poor 变成常规目标”的语义，Working `K_mot` 从：

```text
0.40
```

调整为：

```text
K_mot = 0.60
```

因此：

```text
WillingnessThreshold(M)
= 0.40 + 0.60 * (0.5 - M)
= 0.70 - 0.60M
```

这只是 calibration seed，不是 production 参数。

## 2. 为什么改 K_mot，而不是改 Poor anchor

`Poor=0` 现在同时承担两个重要语义：

1. 它是 `CurrentFoodValue [0,1]` 连续域的低端合法值；
2. 它与轴外的 `Reject` 保持类型区别。

如果为了让 Poor 偶发响应而把 Poor anchor 抬到正值，会改动整个 FoodValue gauge，也会影响 SizePreference / DietaryShift 的下界解释。

当前问题并不是 Poor 的食物价值定义错误，而是 Working Motivation swing 太小，导致阈值在最高 Motivation 时仍高于 StateTrigger 可提供的最大正向证据。

因此优先修阈值幅度更符合 owner 边界。

## 3. 为什么不扩大 StateTrigger

当前 StateTrigger Working budget：

```text
ordinary ≈ 0.10
upper guardrail ≈ 0.15
```

StateTrigger 表达当前 prey-state 的具名正向攻击证据，不应该为了修复 Poor/Reject 区分而整体放大。

如果把 Trigger 上限直接提高到 `0.20+`，会同时改变 Marginal / Good 的大量普通 case，并可能让 prey-state cue 吞掉 relation class 的职责。

所以本轮不改 Trigger budget。

## 4. 新 Working threshold

```text
M = 0.00 → threshold = 0.70
M = 0.25 → threshold = 0.55
M = 0.50 → threshold = 0.40
M = 0.75 → threshold = 0.25
M = 0.90 → threshold = 0.16
M = 1.00 → threshold = 0.10
```

重要性质：

- `M=0.5` 时 threshold 仍等于 `Marginal=0.40`；
- 所有 reference-Motivation burden calibration 不变；
- Motivation 只在远离 reference 时获得更大作用范围。

## 5. Poor 的可响应窗口

Poor：

```text
CurrentFoodValue = 0
```

无负 burden 时：

```text
DecisionMargin
= StateTriggerValue - WillingnessThreshold(M)
```

### 普通 Trigger

若：

```text
StateTrigger = 0.10
```

由于最低 threshold 也是 `0.10`：

```text
M <= 1
→ Margin <= 0
→ C = 0
```

所以 ordinary Trigger 不会把 Poor 抬成可响应目标。

### 强 Trigger

若：

```text
StateTrigger = 0.15
```

需要：

```text
0.15 > 0.70 - 0.60M
```

即：

```text
M > 0.9167
```

Poor 才进入正 Margin。

在极端端点：

```text
M = 1
Trigger = 0.15
Costs = 0

Margin = 0.05
C ≈ 0.17   # 按 Working M1=0.30
```

因此 Poor 的响应窗口非常窄：

```text
very high Motivation
+ upper-range legal Trigger
+ almost no Closing / Prediction / Risk burden
→ weak but non-zero response
```

这正好保持“偶发越线”，而不是变成普通目标。

## 6. Reject 仍然不同

`Reject` 不进入上述连续计算。

```text
Reject
→ typed hard semantic zero
```

即使：

```text
M = 1
Trigger = 0.15
Costs = 0
```

也不能复活。

因此行为上重新形成明确区别：

```text
Poor
→ 极端有利条件下可出现弱响应

Reject
→ 所有条件下保持不可响应
```

## 7. 对其它 relation 的影响

由于 `M=0.5` 时 threshold 仍为 `0.40`，旧 reference-Motivation calibration 不变：

```text
Preferred margin = +0.60
Good      margin = +0.30
Marginal  margin =  0.00
Poor      margin = -0.40
```

所以：

- combined burden stress basket 在 reference Motivation 下不需要重标；
- `Good - Marginal` gap 不变；
- `Marginal - Poor` gap 不变；
- Response projection `M1=0.30` 的 reference interpretation 不变。

真正变化的是低 / 高 Motivation 两端。

## 8. 需要新增的 regression

至少检查：

### A. Poor ordinary high Motivation

```text
Poor
M = 1
Trigger = 0.10
Costs = 0
→ C = 0
```

### B. Poor extreme favorable

```text
Poor
M = 1
Trigger = 0.15
Costs = 0
→ weak C > 0
```

### C. Poor + tiny burden

确认很小的 Closing / Prediction / Risk burden 是否能快速把该弱响应压回 0，保持窗口稀窄。

### D. Good at low Motivation

确认 `M≈0.2–0.4` 时 Good 不会在普通 presentation 下过早全面失效。如果该 regression 不通过，应重新标定 `K_mot`，而不是修改 Poor / Reject 语义。

### E. Preferred at very low Motivation

确认 Preferred 在极低 Motivation 下仍保留明显高于 Good / Marginal 的结构优势。

## 9. 当前 Working 裁定

第一版 Working seed 更新为：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00

K_mot     = 0.60
Trigger ordinary ≈ 0.10
Trigger upper guardrail ≈ 0.15
```

这闭合的是 Poor 与 Reject 的行为区分，不代表这些数值已 production calibrated。

下一轮若真实 Fish Condition 分布显示 `M>0.92` 过于常见或几乎永远不可达，应从上游 Motivation distribution 与完整 regression 重新标定，而不是把 `Poor` 或 `Reject` 的语义偷偷改掉。

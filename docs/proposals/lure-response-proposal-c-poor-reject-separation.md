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

上一版为救活 Poor，把整个 Motivation 线性斜率从 `0.40` 提到 `0.60`。回归后发现这会把中低 Motivation 下的 Good 压得过狠，因此撤回该全轴调整。

当前 Working 改为：

> 普通 Motivation 区间继续使用原来的线性阈值；只有极高 Motivation 进入额外的 tail relief，使 Poor 在极端条件下出现很窄的弱响应窗口。

---

## 2. 当前 Working threshold

基础阈值保持：

```text
BaseThreshold(M)
= 0.40 + 0.40 * (0.5 - M)
= 0.60 - 0.40M
```

只在极高 Motivation 增加 tail relief：

```text
ExtremeMotivationRelief(M)
= 0.50 * max(0, M - 0.80)
```

最终：

```text
WillingnessThreshold(M)
= BaseThreshold(M)
- ExtremeMotivationRelief(M)
```

即：

```text
M <= 0.80:
    threshold = 0.60 - 0.40M

M > 0.80:
    threshold = 0.60 - 0.40M - 0.50(M - 0.80)
```

这些数值只是 Working calibration seed。

---

## 3. 为什么撤回 `K_mot = 0.60`

上一版全轴线性式：

```text
threshold = 0.70 - 0.60M
```

虽然能让：

```text
Poor + M≈1 + strong Trigger
→ weak response
```

但它同时扩大了低 Motivation 端的惩罚。

以：

```text
Good = 0.70
ordinary combined burden = 0.18
Trigger = 0
ResponseProjection M1 = 0.30
```

为例：

```text
K_mot = 0.60:
M = 0.5 → C ≈ 0.40
M = 0.4 → C ≈ 0.20
M = 0.3 → C = 0
```

这与既有护栏冲突：Good 是稳定正常目标，中等偏低 Motivation 可以明显削弱它，但不应过早让普通 Good 全面失效。

所以问题不是需要更大的全轴 Motivation swing，而是需要一个只服务于“极端高 Motivation 解锁 Poor”的尾部效应。

---

## 4. 新 threshold 的关键点

当前 Working：

```text
M = 0.00 → threshold = 0.60
M = 0.20 → threshold = 0.52
M = 0.30 → threshold = 0.48
M = 0.40 → threshold = 0.44
M = 0.50 → threshold = 0.40
M = 0.70 → threshold = 0.32
M = 0.80 → threshold = 0.28
M = 0.90 → threshold = 0.19
M = 1.00 → threshold = 0.10
```

重要性质：

- `M=0.5` 时仍锚定 `Marginal=0.40`；
- `M<=0.8` 完全保持旧 `K_mot=0.40` 的行为；
- 极高 Motivation 才获得额外 relief；
- `M=1` 时仍能达到 `threshold=0.10`，保留 Poor 的极端弱响应窗口。

---

## 5. Good / Preferred regression

### Good

在：

```text
Good = 0.70
ordinary burden = 0.18
Trigger = 0
```

下：

```text
M = 0.5
margin = 0.12
C ≈ 0.40

M = 0.4
margin = 0.08
C ≈ 0.27

M = 0.3
margin = 0.04
C ≈ 0.13

M = 0.2
margin = 0
C = 0
```

这比上一版 `K_mot=0.60` 更符合目标：

- 中等偏低 Motivation 明显削弱 Good；
- 但不会在 `M≈0.3` 就把普通 Good 完全判死；
- 很低 Motivation 仍可以让 Good 掉到响应线下。

### Preferred

在同样 ordinary burden 下：

```text
M = 0
threshold = 0.60
margin = 1.00 - 0.18 - 0.60 = 0.22
C ≈ 0.73
```

所以即使 Motivation 极低，Preferred 仍保留明显响应能力。

这也满足：

```text
M=0
≠ hard no-feeding state
```

---

## 6. Poor 的响应窗口

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

```text
Trigger = 0.10
```

最低 threshold 仍为 `0.10`，因此：

```text
M <= 1
→ Margin <= 0
→ C = 0
```

普通 Trigger 不会让 Poor 成为可响应目标。

### 强 Trigger

```text
Trigger = 0.15
```

在 tail 区：

```text
0.15 > 0.60 - 0.40M - 0.50(M - 0.80)
```

得到约：

```text
M > 0.9444
```

才进入正 Margin。

端点：

```text
M = 1
Trigger = 0.15
Costs = 0

threshold = 0.10
margin = 0.05
C ≈ 0.17
```

因此 Poor 的合法响应窗口更窄：

```text
extreme high Motivation
+ upper-range legal Trigger
+ almost no negative burden
→ weak but non-zero response
```

---

## 7. Reject 仍然不同

`Reject` 不进入连续阈值计算：

```text
Reject
→ typed hard semantic zero
```

任何 Motivation、Trigger 或 tail relief 都不能复活。

因此：

```text
Poor
→ 极端有利条件下可弱响应

Reject
→ 永远不可响应
```

---

## 8. 为什么 tail relief 属于 Motivation，而不是 Trigger

这个额外项回答：

> 当鱼的全局摄食意愿已经进入极端高位时，它是否愿意降低最低可接受食物价值。

它不回答：

> 当前 prey state 是否更像逃跑、受伤或容易攻击。

因此它仍属于 FeedingMotivation → WillingnessThreshold 路径，不应扩大 `StateTriggerValue`。

同时 tail relief 只移动阈值，不改变 `FoodValue`，也不改变 prey identity。

---

## 9. Working 参数与 OPEN

当前 Working seed：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00

Base K_mot = 0.40
Extreme tail start = 0.80
Extreme tail extra slope = 0.50

Trigger ordinary ≈ 0.10
Trigger upper guardrail ≈ 0.15
```

仍未 production-closed：

- `0.80` 是否应是 tail start；
- `0.50` 是否应是 tail extra slope；
- 上游 FeedingMotivation 的真实分布；
- `M>0.94` 在真实鱼情中出现的频率；
- Good / Preferred 在完整 Closing + Prediction + Risk 分布下的最终 retention。

如果真实 Motivation 分布表明高端 tail 太常见或几乎不可达，应重新标定 tail start / slope；不要修改 Poor / Reject 的 typed semantics。

---

## 10. 当前裁定

撤回：

```text
K_mot = 0.60
```

作为全轴线性 Working seed。

当前采用：

```text
BaseThreshold(M)
= 0.60 - 0.40M

ExtremeMotivationRelief(M)
= 0.50 * max(0, M - 0.80)

WillingnessThreshold(M)
= BaseThreshold(M) - ExtremeMotivationRelief(M)
```

这个形状同时满足：

1. reference Motivation 与旧 calibration 不变；
2. 中低 Motivation 下 Good 不被额外过度处罚；
3. Preferred 在极低 Motivation 下仍保留结构优势；
4. Poor 只在极端高 Motivation + 强合法 Trigger + 极低 burden 下弱响应；
5. Reject 永远不可复活。

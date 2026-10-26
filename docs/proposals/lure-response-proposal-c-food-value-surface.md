# 方案 C｜Food Value × Motivation × TaskStrain 响应面

日期：2026-10-26  
状态：Working Probe，非 Current，非生产参数。

## 1. 目标

本页攻击一个窄问题：鱼口变好时，Target / Food Value 应如何参与 Feeding Response？

需要同时满足两件事：

- 鱼口好应降低挑食程度，让较弱 Target Relation 更容易进入响应区；
- 但 `Reject` 代表明确语义拒绝，不能被高 Motivation 或低 TaskStrain 复活。

可执行 probe：`../../prototypes/lure-response/proposal_c_food_value_surface_probe.py`。

## 2. Working Target Relation 标尺

仅用于观察响应面，不是 Production 数值：

| Target Relation | Working Value |
|---|---:|
| Preferred | 1.00 |
| Good | 0.80 |
| Marginal | 0.55 |
| Poor | 0.35 |
| Reject | 0.00 |

`Reject` 与其它四档不同：它是足够明确的 Direct Negative / hard semantic boundary。`Poor` 只是低价值，不是 hard zero。

## 3. 当前 Working Formula

沿用体验预算 v2 后的最小 family，只作 probe：

```text
TaskCost = 0.33 × TaskStrain^4
Threshold = 0.72 - 0.45 × Motivation
Margin = FoodValue - TaskCost - Threshold
C_mode = clamp(Margin / 0.38, 0, 1)
```

其中 `TaskStrain > 1`、`Motivation = 0`、`Reject` 继续走 typed hard gate。

## 4. 响应面

下表分别给出 easy / medium / demanding task：`TaskStrain = 0.25 / 0.55 / 0.80`。

### 鱼口差｜Motivation = 0.25

| Relation | Easy | Medium | Demanding |
|---|---:|---:|---:|
| Preferred | 1.00 | 0.95 | 0.68 |
| Good | 0.50 | 0.43 | 0.15 |
| Marginal | 0 | 0 | 0 |
| Poor | 0 | 0 | 0 |
| Reject | 0 | 0 | 0 |

含义：鱼口差时，只有 Preferred / Good 值得讨论；Marginal 以下不应因为“鱼在这里”就产生稳定 Feeding response。

### 正常鱼口｜Motivation = 0.60

| Relation | Easy | Medium | Demanding |
|---|---:|---:|---:|
| Preferred | 1.00 | 1.00 | 1.00 |
| Good | 0.92 | 0.84 | 0.57 |
| Marginal | 0.26 | 0.18 | 0 |
| Poor | 0 | 0 | 0 |
| Reject | 0 | 0 | 0 |

含义：Marginal 在正常鱼口、任务足够轻松时可以出现少量响应，但不应和 Good 竞争。

### 鱼口好｜Motivation = 0.90

| Relation | Easy | Medium | Demanding |
|---|---:|---:|---:|
| Preferred | 1.00 | 1.00 | 1.00 |
| Good | 1.00 | 1.00 | 0.92 |
| Marginal | 0.62 | 0.54 | 0.26 |
| Poor | 0.09 | 0.01 | 0 |
| Reject | 0 | 0 | 0 |

含义：好鱼口扩大可接受机会区域，但并不是把所有目标统一乘高。

## 5. 新增验收边界

### FVAL-1 Target Relation 单调

固定 Motivation / TaskStrain：

```text
Preferred >= Good >= Marginal >= Poor >= Reject
```

不能出现更差的 Target Relation 因曲线形状反而响应更高。

### FVAL-2 Reject 永久为 0

```text
Reject
+ Motivation=1
+ TaskStrain≈0
→ C_mode = 0
```

因为 Reject 是语义边界，不是低 Value 数字。

### FVAL-3 Poor 不是默认 hard zero

Poor 允许在极高 Motivation + 极低 TaskStrain 下产生少量 response，但不能因此接近 Good / Preferred。

这防止把连续价值判断偷换成额外 categorical gate。

### FVAL-4 Marginal 应受 Motivation 明显调节

Marginal 是观察“鱼口好会不会降低挑食”的主要测试层：

```text
低 Motivation → 通常不出手
正常 Motivation + easy task → 少量响应
高 Motivation + easy task → 明显进入响应区
```

### FVAL-5 TaskStrain 仍然有因果权力

即使 Target Relation 相同，TaskStrain 上升仍应压低 response；Food Value 不能让 TaskAffordance 失去作用。

## 6. 当前判断

这轮没有逼出新的维度，也没有要求增加 `PoorPenalty` / `MarginalBonus`。

当前 threshold topology 本身已经能表达：

```text
鱼口差
→ 更挑食

鱼口好
→ Marginal 开始可接受
→ Poor 在极有利条件下偶尔可接受
→ Reject 永远不可接受
```

因此当前更值得保留的是：

```text
Target Relation / Food Value
+ Motivation-adjusted threshold
+ TaskCost(TaskStrain)
→ Decision Margin
```

而不是按 Target Relation 分别配五条独立 response curve。

## 7. 尚未闭合

- Preferred / Good / Marginal / Poor 的生产 numeric anchors；
- 是否需要保留这五档 categorical class，还是只保留 class + numeric projection；
- 不同 prey / species 是否共享同一 Value projection；
- `Poor` 在极好鱼口下允许的最大 response budget；
- ResponseCurve 是否仍需非线性映射。

这些应继续由 Reference Fishing Story + experience backsolve 决定，不从本页示例数字直接晋升。

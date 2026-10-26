# Proposal C：State Trigger Value 幅度预算

> Status: Working Calibration Constraint / non-production
>
> Scope: prey-conditioned State Trigger Value inside Feeding Decision

## 结论

`StateTriggerValue` 可以与 `FoodValue` 一起进入 `DecisionMargin`，但它不能拥有与一个完整 Target Relation 档位相当或更大的自由幅度。

当前推荐的 Working 约束是：

```text
DecisionMargin
= FoodValue
+ StateTriggerValue
- TaskCost
- WillingnessThreshold(Motivation)
```

同时：

```text
0 <= StateTriggerValue <= TriggerBudget
```

`TriggerBudget` 第一轮只建议落在约 `0.10 ~ 0.15` 的量级，用于结构验证，不是生产常数。

这个范围来自现有 Working FoodValue 标尺与响应面反推，不来自外部生物学测量。

## 为什么 Trigger 不能太大

当前 FoodValue Working 标尺为：

| Target Relation | Working FoodValue |
|---|---:|
| Preferred | 1.00 |
| Good | 0.80 |
| Marginal | 0.55 |
| Poor | 0.35 |
| Reject | hard zero |

相邻档位差约为 `0.20 ~ 0.25`。

如果允许 `StateTriggerValue` 达到 `+0.25 ~ +0.30`，它就拥有了“跨越一个完整 FoodValue 档位”的能力，会开始抹平 Target Relation 的因果权力。

在现有 Working formula、medium task 下：

| Trigger | Marginal / normal bite | Poor / good bite |
|---:|---:|---:|
| 0.00 | 0.18 | 0.01 |
| 0.10 | 0.45 | 0.28 |
| 0.15 | 0.58 | 0.41 |
| 0.20 | 0.71 | 0.54 |
| 0.25 | 0.84 | 0.67 |
| 0.30 | 0.97 | 0.80 |

当 Trigger 接近 `0.25 ~ 0.30` 时，Poor prey 在好鱼口下已经接近主力 response，这与“动作很漂亮，但目标本身仍然不太值得吃”的语义冲突。

## 推荐的语义边界

### TRG-1 可以救 Marginal

一个非常可信的 prey-appropriate escape / distress state，应允许把 Marginal prey 从“差一点不值得出手”推入明显响应区。

这正是 State Trigger 购买的核心策略表达能力。

### TRG-2 不应普遍把 Poor 变成主力

Poor 不是 hard zero，因此在：

```text
高 Motivation
+ 低 TaskCost
+ 强 State Trigger
```

下可以产生可见 response。

但强 Trigger 不应让 Poor 在普通条件下稳定接近 Good / Preferred。

### TRG-3 Reject 永远不能被救活

`Reject` 是 typed semantic boundary：

```text
Reject + max Trigger + max Motivation + easy task
→ C_mode = 0
```

Trigger 不参与翻转这个 gate。

### TRG-4 Trigger 不应替代 Motivation

低 Motivation 时，即使逃逸状态很强，也不应自动产生高 response。

Trigger 表示“当前呈现更容易触发攻击”，Motivation 表示“鱼现在愿不愿意为这顿饭出手”。两者必须保留独立因果权力。

### TRG-5 Trigger 不应替代 TaskAffordance

强 Trigger 可以让目标更值得追，但不能把 hard Infeasible 变成可捕获。

对于 soft Steering / Prediction cost，也应允许出现：

```text
更诱人，但太难抓
→ 总 response 仍下降
```

## 量纲判断

第一版可以让 `StateTriggerValue` 与 `FoodValue` 共用 Decision Margin 的无量纲效用尺度，因为两者都表达“对出手决策的正向价值”。

但这不意味着二者是同一个概念：

- `FoodValue`：这个目标本身值不值得吃；
- `StateTriggerValue`：它此刻的状态有没有额外触发性。

因此 Trigger 必须有显著更小的预算上限，不能成为第二套 FoodValue。

## 更稳的参数化方式

不建议直接 author 每种状态的 `+0.12`。

更稳的是：

```text
StateTriggerValue
= TriggerBudget * TriggerIntensity
```

其中：

```text
0 <= TriggerIntensity <= 1
```

`TriggerIntensity` 来自 prey-conditioned escape / distress state interpretation；`TriggerBudget` 是全局或 family-level calibration budget。

第一版应优先尝试共享较小的 `TriggerBudget`，只有跨 prey-family fixture 明确失败，才允许 family-specific budget。

## 当前 Working fixture

使用 `TriggerBudget = 0.12` 仅作示例时：

- 正常鱼口、medium task：Marginal 从约 `0.18` 提升到约 `0.50`；
- 鱼口差、medium task：Marginal 仅到约 `0.09`；
- 好鱼口、medium task：Poor 约 `0.33`；
- demanding task 下，Poor 即使好鱼口也仍很低。

这符合当前希望的角色：

> Trigger 能改变“差一点”的决策，但不会压倒 FoodValue、Motivation 和 TaskCost。

## 当前状态

- `StateTriggerValue`：Working Admitted Semantic。
- 与 `FoodValue` 共用无量纲 Decision Margin：Working Hypothesis。
- `TriggerBudget ≈ 0.10 ~ 0.15`：Working calibration range，仅用于 probe。
- `0.12`：示例值，不是 production anchor。
- Reject / hard Infeasible / ResolutionIncomplete：继续保持 typed hard boundary。

对应 probe：`../../prototypes/lure-response/proposal_c_state_trigger_budget_probe.py`。

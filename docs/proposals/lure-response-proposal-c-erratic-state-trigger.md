# Proposal C：Erratic / Escape State Trigger 准入

> Status: Working Admitted Semantic / production function unresolved
>
> Scope: prey-conditioned state valuation inside Feeding Response

## 结论

`Erratic / Escape State Trigger` 有资格作为 Proposal C 中第一个正式准入的 optional Presentation-State Valuation 语义，但必须满足两个限制：

1. 它不是通用 `ErraticBonus`，而是**按 prey interpretation 解释后的状态价值**；
2. 它只负责“这种状态是否更容易触发攻击”，不能重复承担 prey identity、Closing、Steering、pause dwell 或 prediction break 已经负责的作用。

推荐主链：

```text
Actual trajectory / temporal pattern
        ↓
prey-conditioned state interpretation
        ↓
Escape-like / Erratic / Distressed state evidence
        ↓
State Trigger Value (+)

同时：
Actual trajectory
        ↓
Closing / Steering / prediction consequences
        ↓
Task / temporal cost (-)
```

因此新的 Working Decision Margin 可以写成：

```text
DecisionMargin
= FoodValue
+ StateTriggerValue
- TaskCost
- WillingnessThreshold(Motivation)
```

`StateTriggerValue` 当前只准入语义位置，不准入生产曲线和数值。

## 为什么需要这个独立语义

仅用 `FoodValue - TaskCost - Threshold` 无法稳定表达以下真实且重要的路亚策略故事：

```text
同一拟饵、同样平均前进速度：
A. 机械直线匀速
B. 适度 dart / zig-zag
C. 极端高速、剧烈且难预测的乱窜
```

设计上应允许：

```text
B > A
B > C
```

其中 B 对 A 的优势不是因为更好抓，而是因为 escape-like / injured-like / erratic state 本身更容易触发攻击；B 对 C 的优势则可以来自高强度状态下迅速上升的 handling / prediction cost。

这意味着不需要手工造一个“中等 erratic 最好”的钟形 bonus。更简单的结构是：

```text
StateTriggerValue(erratic_state)
→ 随状态强度上升后饱和

Handling / Prediction Cost(erratic_state)
→ 高强度区凸增
```

两者相减，自然形成中间最优。

Working probe 仅用于结构验证：

```text
mechanical straight: trigger 0.000, cost 0.000, net delta 0.000
moderate darting:    trigger 0.333, cost 0.046, net delta 0.288
extreme erratic:     trigger 0.424, cost 0.429, net delta -0.005
```

这些数字不是 production calibration。

## 外部证据支持什么，不支持什么

Bass fishing 实战资料长期把 jerkbait 的 side-to-side slashing、darting、stop-and-go、随机/非机械动作描述为 reaction-strike / triggering qualities；同时 cadence 与 pause 决定实际咬口时机。近期产品说明也继续把 erratic darting 与 injured baitfish 模拟联系起来。

动物行为实验还显示，erratic prey movement 可能同时带来两类相反结果：更难追踪，但更快触发 predator strike。这个方向与本提案的“正向 trigger + 负向 capture/prediction consequence”拆分一致。

这些资料只能支持方向和机制分离，不能直接给出本系统的数值曲线、阈值或跨鱼种普适系数。

## 为什么不是通用 `ErraticBonus`

同样的轨迹变化，对不同 prey interpretation 可能不是同一种状态：

- baitfish：可能解释为 escape dart / wounded slash；
- crayfish：可能是 backward escape burst；
- frog：可能是 surface struggle；
- worm：相同高频折线未必有同样生态含义。

因此输入不能是：

```text
raw zig-zag score → universal bonus
```

而应是：

```text
raw trajectory / event history
→ prey-conditioned state interpretation
→ EscapeLikeIntensity / DistressLikeState / equivalent semantic
→ StateTriggerValue
```

具体状态名称可以按 prey family 不同，但下游只消费经过解释的 state valuation packet。

## 与已有路径的去重边界

### 不重复 prey-type support

prey-type support 回答“像不像这种猎物”；State Trigger 回答“按这种猎物理解时，当前状态是不是容易触发攻击”。

同一 raw feature 可以参与两条解释链，但不能把同一个效果重复算两次。

### 不重复 pause

pause 仍按既有路径处理：

- favorable dwell / temporal support；
- prediction reset / break；
- Closing Demand 降低。

`StateTriggerValue` 不因为出现 pause 就直接加分。只有 prey-state interpreter 明确把某个 temporal pattern 解释成有意义的 distressed / escape state 时，才可形成相应状态价值。

### 不重复 Steering / Prediction Challenge

轨迹急转可以同时产生：

- 正向 prey-state trigger；
- 负向 steering / prediction consequence。

这是同一事实的两个不同因果后果，不是重复计权。但两条链必须分别解释自己的语义，不能都简单读取同一个 raw `omega_traj` 后各自随意加减。

## 第一版推荐的特征边界

正向 trigger 不应只用 `omega_traj = v*kappa`。

原因：规则圆周运动可以有很高 `omega_traj`，但非常机械、可预测；jerkbait / walking bait 的策略价值更接近：

- 离散 direction-change event；
- 左右交替；
- burst / jerk event；
- 事件节律是否机械重复；
- 近期是否出现 sudden escape-like change。

因此第一版状态解释应优先从**事件序列和 prey-conditioned pattern**生成 `EscapeLikeIntensity`，而不是从单个连续运动量直接映射。

## Admission fixtures

至少保留以下验收故事：

### E1 机械直线 vs 适度 dart

固定 FoodValue、Motivation、平均前进速度及其它条件：

```text
moderate prey-appropriate darting
> mechanical straight
```

要求差异达到玩家可感知，而不是 `+0.001` 形式上的排序。

### E2 适度 dart vs 极端乱窜

在相同 prey interpretation 下：

```text
moderate darting
> extreme high-load erratic motion
```

该 reversal 应主要由 capture / prediction consequence 产生，而不是强行让 TriggerValue 自己下降。

### E3 prey-conditioned specificity

同一 raw trajectory 若对 baitfish 是强 escape cue，但对另一 prey family 没有对应状态解释，则不得自动获得相同 TriggerValue。

### E4 no hidden pause bonus

如果两条轨迹的 prey-state evidence 相同，只是其中一条 pause 更长，则 StateTriggerValue 不自动更高；pause 作用留给 temporal / task 路径。

### E5 hard semantic boundaries remain

- Target Relation Reject 仍为 hard zero；
- Task hard Infeasible 仍不能被 StateTriggerValue 救活；
- ResolutionIncomplete 仍不输出 scalar。

## 当前状态

- `State Trigger Value`：Working Admitted Semantic。
- `ErraticBonus`：Rejected naming / rejected universal mechanism。
- `EscapeLikeIntensity`：Working candidate intermediate semantic，具体 prey-family 状态名待后续收敛。
- 生产公式、输入特征、强度范围、跨 prey-family projection：Open。
- 当前 probe：`prototypes/lure-response/proposal_c_erratic_state_trigger_probe.py`。

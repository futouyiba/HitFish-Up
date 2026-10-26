# Proposal C：Escape-like State Trigger 的特征路由

> Status: Working Hypothesis / feature-admission review
>
> Scope: Proposal C Step 3→4，prey-conditioned state interpretation → optional state valuation

## 结论

`EscapeLikeIntensity` 不应由一组通用“乱动分数”直接生成。

第一版最小通用底座只保留两类正向状态证据：

1. **Redirection Event Strength**：突然改变运动方向有多强；
2. **Burst Event Strength**：突然加速 / 逃逸脉冲有多强。

`direction alternation` 与 `timing irregularity` 不直接增加 Trigger Value；它们只用于判断这段运动是否更像某个 prey interpretation 下的逃逸 / 受伤 / 挣扎状态。

`pause` 不进入 Escape Trigger。Pause 已由 temporal support / favorable dwell / prediction-break 等现有路径结算；将 `burst → pause` 整体再作为 Trigger 会重复计权。

## 为什么需要这样拆

当前已有外部策略故事支持：jerkbait / hard bait 的 darting、slashing、erratic action 可以触发 reaction strike；pause/cadence 又独立影响具体击口窗口。因此同一段 retrieve 可以同时产生：

```text
trajectory events
  ├─ prey-state evidence → positive State Trigger Value
  ├─ steering / prediction consequence → task-side negative effect
  └─ pause / dwell / cadence → temporal support
```

这三条不能压成一个 `ErraticBonus`。

## 特征归属

| 特征 | 第一版归属 | 是否直接增加 Trigger | 说明 |
|---|---|---:|---|
| 突然方向改变 | prey-state evidence | 是 | 典型 dart / escape cue |
| 突然加速 / burst | prey-state evidence | 是 | 典型 fleeing cue |
| 左右交替 | interpretation confidence | 否 | 只有在该 prey pattern 下有意义 |
| 时序不规则 | interpretation confidence | 否 | 不规则本身不是价值，只影响“像不像” |
| pause | temporal support | 否 | 不在 Trigger 再算一次 |
| 长时间静止 | temporal / state-specific path | 否 | 可能是悬停、受伤、伪装等，不可统一解释 |
| 连续高曲率 | maneuver / steering | 否 | 可能同时参与 prey-state path，但不得直接按同一量二次加分 |

## Working 计算结构

通用 feature extraction 只输出可复用事实：

```text
RedirectionEventStrength
BurstEventStrength
AlternationPattern
TimingPattern
```

随后由 prey-conditioned interpreter 决定：

```text
Small Baitfish:
  dart + burst + side alternation
  → escape-like support

Crayfish:
  backward burst / hop-like transition
  → escape-like support

Frog:
  surface kick / struggle sequence
  → struggle-like support
```

最终可产生：

```text
PreyStateSemantic {
  semantic: EscapeLike | DistressedLike | StrugglingLike | ...
  support: 0..1 | Unknown
  evidence: ...
}
```

只有已经被该 prey interpretation 支持的 state semantic，才可以进入 optional `State Trigger Value`。

## 不准入的简化

以下做法第一版不准入：

```text
ErraticnessScore → Universal Bonus
Irregularity → Bonus
TurnRate → Bonus
Pause → Bonus
```

原因分别是：

- 缺少 prey semantics；
- 容易奖励机械噪声；
- 与 maneuver cost 重复；
- 与 temporal support 重复。

## Probe 观察

配套 probe：

`prototypes/lure-response/proposal_c_escape_feature_routing_probe.py`

Working toy 输出的相对关系约为：

| Pattern | Escape-like support |
|---|---:|
| straight | 很低 |
| circular | 低 |
| regular zig-zag | 中高 |
| burst-pause | 高，但 pause 本身不入 trigger |
| erratic escape | 最高 |

这只验证特征路由能区分“机械转圈”和“真正 dart / burst pattern”；数值、权重、阈值均不是 production contract。

## 与现有 Proposal C 主链的关系

Working 主链现在可以写成：

```text
ActualPresentation
  ↓
prey-conditioned state interpretation
  ├─ Escape / Distress / Struggle semantic
  │      ↓
  │   State Trigger Value (+)
  │
  ├─ Closing / Intercept consequence
  │      ↓
  │   TaskCost (-)
  │
  └─ pause / dwell / cadence consequence
         ↓
      Temporal Support
```

然后进入：

```text
FoodValue
+ StateTriggerValue
- TaskCost
- WillingnessThreshold(Motivation)
→ DecisionMargin
→ Response Projection
→ C_mode
```

## 仍未闭合

1. `Redirection Event Strength` 的生产事件定义与时间窗；
2. `Burst Event Strength` 是读速度增量、加速度积分，还是 prey-specific proxy；
3. 各 prey family 是否真的共享同一 generic evidence layer；
4. `State Trigger Value` 的最大幅度与 FoodValue 的量纲关系；
5. 同一 raw trajectory feature 同时参与 state interpretation 与 task consequence 时，如何保留 provenance 并避免语义重复。

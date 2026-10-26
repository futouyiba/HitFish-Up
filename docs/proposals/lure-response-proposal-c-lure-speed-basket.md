# Proposal C｜Representative Lure-Speed Basket

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 目的

本页不尝试建立“所有拟饵的统一绝对速度表”。它只定义一组用于 Closing / Intercept 标定的代表性 presentation regime，使：

```text
lure family runtime speed
→ map to representative regime
→ combine with InterceptSpeedLimit
→ q = lure_speed_relative_to_water / InterceptSpeedLimit
→ Closing calibration
```

公开钓法资料对 slow roll、steady retrieve、fast/burning、jerk-and-pause、stop-and-go 等操作类型存在稳定共识，但不同 lure family 的绝对工作速度范围差异显著。因此第一版 basket 以 **presentation regime** 为主，绝对 m/s 由具体 lure family / runtime measurement 提供，不从通用 basket 硬编码。

## 2. 第一版 basket

### A. Pause / Near-Stationary

```text
instantaneous lure speed ≈ 0
```

用途：

- Closing demand 基本消失；
- 用来验证 Activity 不应在零追赶需求时仍制造显著处罚；
- 与 PredictionChallenge 的自然衰减分开。

注意：Pause 本身没有额外 bonus。

### B. Slow Presentation

代表：slow roll、drag、慢速软饵、缓慢 bottom-contact presentation。

语义：当前操作主动压低追赶负担，通常用于低活性 / 冷水 / 精细作钓等策略故事。

要求：在大多数正常 locomotor archetype 上，q 应明显低于能力边界。

### C. Normal Steady Retrieve

代表：常规 crankbait / spinner / swimbait steady retrieve。

这是 K_close 的主要 reference calibration regime。

要求：

```text
GeneralistSwimmer × reference size × reference Activity
→ ordinary average Closing burden
```

应大致落在 combined-burden stress test 为 Closing 预留的 ordinary 区间，而不是接近 hard infeasible。

### D. Fast Search / Burning

代表：快速 crankbait、spinnerbait、lipless / search presentation 等。

语义：以更高 Closing demand 换取搜索效率或 reaction-trigger 策略。

要求：

- HighSpeedPursuer 仍应有较多可响应 bearing；
- GeneralistSwimmer 应明显增加 Closing burden；
- SlowBenthic 可出现较高 hard-infeasible share；
- 不能靠另加 FastPenalty 表达，速度影响只走 Closing，除非未来另有独立 owner。

### E. Burst / Twitch Peak

代表：jerk、snap、dart、短时 rod-induced burst 的局部峰值。

这里必须区分：

```text
instantaneous speed peak
≠ sustained retrieve speed
```

Closing 使用当前真实 speed / short-window state；Prediction 另行消费 abrupt direction-change。不能因为同一次 twitch 同时有 speed peak 和 turn event 就再增加 generic ManeuverPenalty。

该 regime 主要用于检查：

- angle-local hard infeasible 是否正常出现；
- burst 不应导致 whole-mode hard-zero；
- burst → pause 是否能通过 Closing 降低和 Prediction decay 自然产生节奏差。

## 3. 为什么不直接冻结通用 m/s 档位

绝对 lure speed 取决于：

- lure family；
- reel / gear ratio / line pickup；
- rod manipulation；
- lure hydrodynamics；
- current / water-relative reference frame；
- animation / gameplay implementation。

外部资料常给 reel retrieve rate、MPH、slow/medium/fast 等不同口径，不能直接混成一套生产 m/s。

因此生产过程应优先从游戏本身取得：

```text
ActualPresentation telemetry / authored motion profile
→ lure_speed_relative_to_water
```

外部资料用于 sanity check 与 strategy-story coverage，不作为最终 runtime 数值来源。

## 4. 必须使用 water-relative speed

Closing contract 已要求：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
```

不是 world-space ground speed。

原因：水流会同时改变 lure 与 fish 的相对运动语义。若生产当前没有可靠 water-relative speed，需要显式声明缺口，不能用 ground speed 无痕替代。

## 5. Basket 的真正标定对象

每个 regime 不直接绑定固定 q。应在不同 locomotor archetype 上观察 q distribution：

```text
presentation regime
× lure family
× locomotor archetype
× fish size cohort
→ q distribution
```

重点不是平均值一项，而是：

- median / P50 q；
- P10 / P90 q；
- q >= 1 的 bearing-local hard-infeasible exposure；
- after-bearing-integration 的 Closing burden；
- Good / Preferred response retention。

## 6. Working acceptance stories

### Pause

```text
q ≈ 0
→ ClosingCost ≈ 0
```

### Slow Presentation

```text
Generalist / SlowBenthic
→ 通常可追
→ Closing burden 低
```

### Normal Steady

```text
Generalist reference case
→ ordinary Closing burden
```

它应成为 K_close calibration 的核心篮子。

### Fast Search

```text
HighSpeedPursuer
→ 仍较可行

Generalist
→ 明显 cost

SlowBenthic
→ 高 cost / 部分 bearing hard-zero
```

### Burst Peak

```text
部分 bearing hard-zero
+ 其它 bearing 仍可能高 response
```

不得升级成 whole-mode hard-zero。

## 7. 与 StateTrigger / Prediction 的边界

同一个高速或 twitch 事件可能伴随其它合法后果：

```text
speed magnitude
→ Closing

sudden direction-change
→ PredictionChallenge

escape-like prey-state evidence
→ StateTriggerValue
```

这些 owner 分别回答不同问题。

禁止：

```text
high speed
→ generic Suspicion / FastPenalty
```

除非未来控制 Closing / Prediction / Trigger 后仍证明存在独立、稳定的风险语义。

## 8. 外部资料如何使用

外部钓法资料可用于确认 basket 覆盖现实策略：

- steady retrieve 是基础操作；
- slow roll / dragging 代表低速 presentation；
- burning / high-speed retrieve 是真实搜索或 reaction 策略；
- jerk-and-pause / stop-and-go 包含短时 burst 与 pause；
- 不同 lure family 的适用速度范围不同。

但这些资料通常不会提供可直接映射到游戏 water-relative lure speed 的统一数据，因此不把外部速度值晋升为 production input。

## 9. 推荐生产流程

```text
1. 从游戏实际 lure motion / telemetry 取得 water-relative speed
2. 按 lure family + presentation regime 分桶
3. 统计每桶 speed distribution
4. 与各 locomotor archetype / size cohort 组合得到 q distribution
5. 裁定 bearing prior dimensionality
6. 在 Normal Steady reference basket 反推 K_close
7. 用 Slow / Fast / Burst 做跨 regime validation
8. 再接 Activity multiplier 和 combined-burden test
```

## 10. 当前 OPEN

- 项目是否已有可直接取得的 water-relative lure speed；
- lure family catalog 与 regime mapping；
- 各 regime 的 production speed distributions；
- Normal Steady 的 reference lure family；
- Isotropic2D / Isotropic3D 最终裁定；
- locomotor archetype catalog；
- InterceptSpeedLimit production calibration；
- K_close production value。

本页只冻结 calibration basket 的语义与数据流程，不冻结通用 m/s 档位。

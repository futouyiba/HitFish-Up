# Proposal C｜Prediction Challenge：撤回通用 Maneuver Cost

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 结论

当前第一版不再把 `ω_traj = v·κ` 或 `ω_traj / fish_turn_capacity` 直接映射为通用 `ManeuverCost`。

原因是系统没有具体鱼点，也没有鱼相对拟饵的即时朝向与截获路径。仅凭拟饵自身曲率，无法推出鱼为了成功捕获它必须达到的最低转向率。鱼可以切弯、截击、调整追击策略，也可以在重新获得合适攻击窗口后再出手。

第一版把负向后果收缩为两类：

```text
ClosingCost(θ)
→ 拟饵在当前 latent relative angle 下是否正在拉开距离、追赶负担有多大

PredictionChallenge
→ 突然变向之后，鱼的攻击预测是否仍处于重新建立阶段
```

原先的通用 `ManeuverCost` 暂不进入 numeric core。

## 为什么这样改

### 1. 转弯确实会影响捕获，但不是简单轨迹复制

鱼类捕食研究支持：捕获时需要定位、制动、转向和运动控制；这些能力会影响捕获表现。同时，捕食者会根据猎物的逃逸方向、可预测性和感官信息改变追击方式，并不要求逐点复制猎物轨迹。

因此：

```text
拟饵轨迹角速度很高
```

不能直接推出：

```text
鱼必须以同样角速度转向，否则捕获失败
```

### 2. 真正独立且当前可观测的负向语义是“预测被打断”

对没有具体鱼点的 FCF 来说，突然方向改变至少可以稳定说明一件事：此前建立的运动趋势预测可能失效，鱼需要重新获得合适的攻击预测。

这与 `StateTriggerValue` 的正向语义可以同时成立：

```text
sudden redirection
    ├→ prey-conditioned escape/distress cue
    │      → StateTriggerValue (+)
    │
    └→ recent trajectory prediction becomes stale
           → PredictionChallenge (-)
```

两条链回答不同问题，不是重复计权。

## 第一版 transient state

先把一次方向突变定义成有界事件强度：

```text
TurnEventStrength(Δψ) = (1 - cos Δψ) / 2
```

其中使用最小绝对转角：

- 0° → 0
- 60° → 0.25
- 90° → 0.50
- 120° → 0.75
- 180° → 1.00

这个定义只用于得到无量纲、单调、有界的 turn-event strength；不是生物学标定。

随后维护一个近期 PredictionChallenge：

```text
P(t)
= max over recent turn events e:
  TurnEventStrength(e) × decay(age_e / τ_recover)
```

Working probe 暂用指数衰减：

```text
decay = exp(-age / τ_recover)
```

其意义是：

- 单次转向后 challenge 随时间消退；
- 连续折线会不断刷新 challenge，因此长期保持较高；
- 不把多个转向简单累加到无上限；
- 直线高速本身不会产生 PredictionChallenge。

`τ_recover` 是鱼侧重新建立攻击预测所需的 characteristic time，当前没有生产标定。

## 为什么不直接使用 ω_traj

`ω_traj = vκ` 仍可以保留为轨迹事实 / Explain 特征，但当前不取得独立 penalty authority。

反例：规则圆周运动可以持续拥有较高 `ω_traj`，但其路径高度可预测。另一方面，一次突然 90° dart 即使平均曲率窗口不高，也可能瞬间让此前预测失效。

因此对 prediction 来说，离散 redirection event 与其近期历史比连续曲率更接近需要表达的因果。

## 和 Closing 的边界

PredictionChallenge 不负责：

- 拟饵速度是否超过鱼的追赶能力；
- 拟饵是否正在背离某个 latent angle；
- pause 后径向 Closing Demand 是否下降。

这些仍由 Closing 路径结算。

反过来，Closing 也不因为一次急转就自动增加 penalty，除非急转后的实际速度方向在某个 latent angle 上确实改变了 Closing burden。

## 和 State Trigger 的边界

`TurnEventStrength` 不能直接同时当：

```text
+Trigger
-PredictionCost
```

然后用同一条万能曲线正负各算一次。

正向 Trigger 必须先经过 prey-conditioned state interpretation：例如 baitfish dart、crayfish backward burst、frog struggle 等。

PredictionChallenge 是 fish-side、prey-family-independent 的近期运动可预测性负担。它可以读取同一个实际 turn event，但其语义和后续映射独立。

## 对 Decision Margin 的修正

第一版更推荐写成：

```text
DecisionMargin(θ)
= FoodValue
+ StateTriggerValue
- ClosingCost(θ)
- PredictionCost(P)
- WillingnessThreshold(Motivation)
```

而不是：

```text
... - TaskCost(Closing, Maneuver)
```

`PredictionCost(P)` 当前只准入语义位置；生产曲线、最大幅度和 `τ_recover` 均未冻结。

如果未来获得具体 fish-relative geometry，能够证明某些 capture geometry 产生独立、可验证的 physical steering burden，再重新准入 Maneuver / Capture-Geometry Cost。

## Pause 的位置

一次 dart 后 pause 可以同时造成：

- Closing burden 降低；
- PredictionChallenge 随时间恢复；
- favorable dwell 增加；
- prey-state process 发生变化。

但 pause 本身仍没有匿名 `PauseBonus`。

特别注意：

> PredictionChallenge 的自然衰减已经表达“给鱼时间重新建立预测”。不能再额外添加一个同义的 `PredictionResetBonus`。

## 验收案例

### PRED-1 直线高速

```text
fast straight retrieve
→ PredictionChallenge = 0
```

高速可能增加 Closing burden，但不能因为快就自动获得 prediction penalty。

### PRED-2 单次 dart 后恢复

```text
90° sudden turn
→ P rises
→ no further turns
→ P decays with time
```

### PRED-3 连续 zig-zag

相近间隔不断发生显著 redirection：

```text
P remains elevated
```

因此正向 escape trigger 可以饱和，而 prediction burden 持续存在，允许形成中间最优。

### PRED-4 规则圆周不等于持续 prediction break

若未来明确识别到稳定、可预测的周期轨迹，不应仅因连续高 `ω_traj` 就强制高 PredictionChallenge。

当前 event-only probe 已比 `ω_traj` penalty 更接近该边界；完整周期预测模型暂不增加。

### PRED-5 不生成 hard infeasible

PredictionChallenge 只形成 soft negative consequence。当前它不拥有：

```text
P > threshold → whole mode C=0
```

的 hard gate 权力。

## 当前撤回 / 保留

撤回：

- `ω_traj / fish_turn_capacity` 直接作为 universal Maneuver utilization；
- Maneuver utilization > 1 → hard zero；
- 没有 fish-relative geometry 时声明精确 physical steering demand。

保留：

- `ω_traj` 作为轨迹事实 / Explain feature；
- future geometry-aware Maneuver Cost 的重开可能；
- sudden redirection 的 prey-state Trigger 路径；
- sudden redirection 的 transient PredictionChallenge 路径。

## 未闭合

- `τ_recover` 如何由 Functional Capacity / sensory condition 决定；
- `PredictionChallenge → PredictionCost` 的生产函数；
- PredictionCost 的 effect-size budget；
- 是否需要区分“方向预测恢复”和“strike timing/window”两个后果；
- prey periodicity / learnable cadence 是否未来需要独立模型。

参考 probe：`../../prototypes/lure-response/proposal_c_prediction_challenge_probe.py`。

# 方案 C｜Step 4 Pause Dependency / Cadence Admission Closure

日期：2026-10-26  
状态：Working Probe Closure，不是 Current，不规定最终 response aggregation。

## 1. 本轮结论先行

“刚停有效”这一判断保留，但不再把它直接等价成一个 `pauseBonus`。

经过 dependency / double-count audit 后，四条候选路径收敛为：

```text
move → pause
├─ attention continuity
│   → Perception / bounded history
│   → 不新增独立 scalar
│
├─ trajectory / prediction break
│   → transient task / prediction state
│   → 不新增独立 scalar
│
├─ favorable dwell / attack window
│   → temporal support / exposure
│   → 不新增 pause scalar
│
└─ cadence motif
    → 唯一剩余的独立 Valuation candidate
    → 但当前仍未 admission
```

可执行 probe：`../../prototypes/lure-response/proposal_c_step4_pause_dependency_cadence_probe.py`。

本轮已在 ChatGPT 本地 Python 环境实际执行并通过全部 assertions。

## 2. Attention continuity：编译进 Perception/history

“运动先把鱼吸引过来，停下时鱼仍在关注”是合理候选，但其首要语义不是食物价值增加，而是目标已经通过先前运动建立了 perceptual / attention history。

因此优先表示为：

```text
prior perceptual salience
+ bounded temporal memory
→ current attention / target-history state
```

若已有 Perception / Target interpretation 可以消费短时历史，就不再新增 `AttentionBonus`。

这条机制仍可能真实改变 response；只是效果应通过 Perception / Target 是否仍处于有效 evidence state 体现，而不是在下游再乘一次停顿系数。

## 3. Prediction break：编译进 transient task-state

目标持续运动时，鱼可能形成短期 trajectory expectation。突然停下后，expected trajectory 与 actual trajectory 出现断裂。

如果这个变化确实影响 strike timing / interception，它属于：

```text
trajectory history
+ current transition
→ transient prediction / task state
→ TaskDemand / strike timing consequence
```

它不是“停顿让猎物更美味”。

因此不新增 `PredictionBreakBonus`。如果未来验证出 ranking difference，应通过它改变的具体 task consequence 进入。

## 4. Favorable dwell：编译进 temporal support / exposure

“停在攻击窗口里更久”很可能是 pause 有效的重要原因之一，但其因果量本质上是：

```text
有利 geometry / affordance
持续了多久
```

而不是 pause 标签本身。

若 Candidate / Opportunity 已在 canonical temporal support 上对 response 状态按时间积分，则这部分效果应在 support / exposure 上自然体现。

因此首轮明确禁止：

```text
有利状态持续 1.5 s
→ temporal support 已经累计
→ 又乘一个 PauseDurationBonus
```

否则是典型 double counting。

## 5. Cadence motif：唯一剩余的独立 Valuation candidate

把当前速度、位置、TaskDemand、attention history、favorable dwell 都控制住后，仍可能存在：

```text
jerk → jerk → pause
vs
steady → pause
```

这种 sequence 本身改变 fish-side interpretation / attack tendency 的机制。

如果存在，它才是真正意义上的 `cadence effect`。

但本轮不 admission。

原因：现有证据更多来自实钓经验与职业钓手总结，强烈支持“cadence / pause 经常影响咬口”，但没有把 attention、current speed、target location、dwell time、prey vulnerability cue 等混杂变量控制掉；不同经验来源对 pause length 的重要性也并不一致。

因此当前合法状态是：

```text
CadenceMotif = CandidateUnresolved
```

不是 0，也不是已确认 bonus。

## 6. Cadence admission gate

未来只有满足以下条件，才允许它从 Explain / Candidate 进入 Feeding-mode Valuation：

1. 当前 prey support 相同；
2. current Perception / attention history 相同；
3. current TaskDemand / TaskAffordance 相同；
4. favorable temporal support / dwell horizon 相同；
5. fish-side Feeding Motivation 相同；
6. 唯一稳定变化是 temporal motif / cadence；
7. motif 能产生可复现、可解释、玩家可学习的 ranking difference；
8. 作用范围有 provenance，例如 fish species / lure family / temperature regime / presentation context，而不是 universal cadence coeff。

在没有这类证据时，runtime 可以保留 motif ID / Explain，但不得制造数值 ranking。

## 7. 实钓证据怎样使用

职业钓鱼材料大量强调 jerkbait cadence、pause 和停顿时长会影响 largemouth bass 的咬口；也有经验明确认为 pause 长度并非总是关键。这类材料说明：

- temporal presentation 确实值得模型保留；
- 效果高度 context-dependent；
- 不能从“钓手常用 pause”直接推出一个通用 `PauseCoeff`；
- 不能把职业经验当作已经隔离好的 causal experiment。

参考入口：

- Bassmaster, *Techniques for better bass fishing, part 1*：强调 jerkbait cadence 与 sustained pause。
- Bassmaster, *Why I throw jerkbaits, part 1*：明确认为 pause length 并不总关键，同时强调姿态/下沉与 vulnerability impression。
- In-Fisherman, *Sticking Coldwater Largemouth*：冷水下 longer pause 的强经验案例。
- Bassmaster, *Unlocking Bass* / *Get with the cadence*：强调 retrieve cadence 与 pause 需要针对当日鱼情调整。

这些只能作为 Candidate evidence，不是独立 effect-size 标定。

## 8. TaskDemand 当前 Working Contract

上一轮的两类最小 TaskDemand 继续保留：

```text
ResolvedTaskDemand
├─ Intercept / Closing Demand
└─ Maneuver / Capture-Geometry Demand
```

第二维有独立物理意义与 topology value：在 Intercept Demand 不变时，仅改变 Maneuver Demand 可以独立造成 Feasible → Constrained → Infeasible reversal。

它仍是 Working semantic，不是生产参数维度冻结。后续需要用更多 fish / prey / geometry holdout 检查是否还能进一步压缩。

## 9. 当前 admission / rejection

### Provisional admission

- `Intercept / Closing Demand`
- `Maneuver / Capture-Geometry Demand`
- bounded temporal history 作为 Step 3 / Interaction 可消费事实

### 编译进已有 owner，不新增 scalar

- attention continuity → Perception/history
- prediction break → transient task/prediction state
- favorable dwell → temporal support/exposure

### CandidateUnresolved

- cadence motif → Feeding-mode Valuation candidate
- imbalance-like vulnerability → Feeding-mode Valuation candidate

### 明确不 admission

- universal `pauseBonus`
- `PauseDurationCoeff`
- `AttentionBonus`
- `PredictionBreakBonus`
- `stateBonus`
- presentation state 直接改写 fish-side Feeding Motivation

## 10. 下一步

Step 4 已经不需要继续扩 pause taxonomy。下一轮应该进入真正的 Valuation admission attack：

1. `cadence motif` 与 `imbalance-like vulnerability` 两个 Candidate 二选一先攻；
2. 固定 Perception、TaskDemand、TaskAffordance、temporal support、Feeding Motivation；
3. 只有 Candidate cue / motif 改变；
4. 若无法找到独立、稳定、策略可学习的 ranking reversal，则该 Valuation 分支删除。

在 Valuation 至少有一个独立语义被证明前，不设计最终 `C_mode` 聚合公式。
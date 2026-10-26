# 方案 C｜Step 4 TaskDemand / Pause Mechanism Closure

日期：2026-10-26  
状态：Working Probe Closure，不是 Current，不规定最终 response aggregation。

## 1. 本轮问题

沿用“大口黑鲈 × 小型饵鱼”的窄案例，本轮同时攻击两件事：

1. `TaskDemand` 是否真的需要独立的 Maneuver / Capture-Geometry 维度，而不只是 Intercept / Closing；
2. “刚刚停下”如果确实有效，它可能通过哪些不同因果路径进入，而不是统一变成 `pauseBonus`。

可执行 probe：`../../prototypes/lure-response/proposal_c_step4_task_pause_probe_v3.py`。

本轮已在 ChatGPT 本地 Python 环境实际执行并通过全部 assertions。

## 2. TaskDemand：第二维有独立语义价值

### 2.1 最小语义暂收敛为两类任务

```text
Intercept / Closing Demand
← fish-target relative geometry + relative motion
回答：鱼需要完成多大的接近 / 截获任务？

Maneuver / Capture-Geometry Demand
← orientation / lateral or vertical reposition / actual strike geometry consequence
回答：即使能接近目标，鱼还需要完成多大的姿态、方向与攻击几何调整？
```

这里不把 distance、speed、turn、vertical、roll 分别永久保留成五个独立 penalty。原始事实先进入具体 task semantics，再与鱼的 FunctionalCapacity 比较。

### 2.2 反事实 M1

保持 Intercept Demand 完全相同，只改变 Maneuver Demand：

```text
intercept = 0.50（固定）

maneuver 0.10 → Feasible
maneuver 0.30 → Constrained
maneuver 0.50 → Infeasible
```

人工阈值只用于验证 topology，不是生物标定。

结果说明：第二维能够在第一维完全不变时独立制造 Affordance reversal。因此在当前 Working Probe 中，`Maneuver / Capture-Geometry Demand` 获得 provisional admission。

这不是“因为写了两个阈值所以证明存在两个生物参数”。它的 admission 依赖两个条件同时满足：

- 有独立物理语义：接近目标与形成可完成 strike 的 orientation / capture geometry 不是同一个任务；
- 有外部证据支持该边界：centrarchid prey capture 依赖 locomotor positioning、body orientation、strike timing 与 suction volume 对 prey 的时空对准。

因此第二维先作为最小 task semantic 保留，后续再用更多 fish / presentation holdout 攻击是否可以继续压缩。

## 3. roll 的正确路由

`roll` 本身不是 TaskDemand。

应先问它造成了什么：

```text
roll / pose fact
├─ 只改变“看起来像失衡”的 cue
│   → Target / Valuation candidate
│
└─ 实际改变轨迹、迎击面、orientation、strike geometry
    → Maneuver / Capture-Geometry Demand
```

两条作用可以同时存在，但必须分别有独立 physical meaning。不能因为 `roll=75°` 就在 Valuation 与 TaskDemand 两处机械各扣一次。

因此此前“roll 0° 与 75° 的 TaskDemand 必须相同”只在 cue-only controlled counterfactual 中成立，不是一般事实。

## 4. “刚停”不要再问一个笼统的 pause bonus

用户纠正成立：移动后突然停下很可能真实改变捕食过程。问题不应是“pause 有没有作用”，而应是“作用具体通过哪条机制产生”。

本轮先拆四条候选因果路径。

### 4.1 Attention continuity / refresh

运动可能先产生较强 perceptual evidence；停止后，鱼不会瞬间失去刚刚建立的目标注意或目标记忆。

首轮路由：

```text
prior salient motion
+ recent pause age
→ Perception / short-term target-history state
```

不是 Feeding Motivation，也不是固定 Valuation bonus。

Probe P1 只验证接口纪律：开启 attention mechanism 后，recent pause 与 long-static 可以拥有不同的 perception-history state；关闭机制时不允许暗中产生差异。

当前状态：**Candidate，较强优先级。**

### 4.2 Prediction / trajectory break

移动中的目标形成运动趋势；突然停止会破坏刚刚形成的 trajectory prediction。它可能改变 strike timing、interception plan 或短时 task state。

首轮路由：

```text
expected trajectory
vs actual transition to pause
→ transient prediction / task-state
```

它不等于“停下来更好吃”。

Probe P2 只证明该机制可独立存在于 current speed 之外；是否真实影响大口黑鲈 response 仍需专门证据 / gameplay test。

当前状态：**Candidate。**

### 4.3 Attack-window / favorable-geometry horizon

停止可能让目标在一个有利的距离、角度或结构位置停留更久。这与“刚停”高度相关，但它的因果量不是 pause 标签，而是 favorable state 的持续时间 / exposure。

首轮路由：

```text
current favorable geometry
× future / observed dwell horizon
→ support / exposure over time
```

不优先作为 instantaneous Valuation bonus。

这条尤其要避免重复计权：如果 Candidate / Opportunity 已在 canonical temporal support 上积分同一段有利状态，就不能在 C_mode 中再乘一次 `pauseDurationBonus`。

Probe P3 将其表达为 `favorable_geometry_horizon`，而不是 response scalar。

当前状态：**Candidate，且很可能与 support alignment 强相关。**

### 4.4 Sequence / cadence trigger

即使 attention、prediction 和 dwell time 都控制住，某些 movement → pause → twitch 等时序模式仍可能形成独立的 target / feeding interpretation。

只有这一类候选在当前结构中允许继续进入 Valuation：

```text
explicit temporal motif
→ evidence-backed feeding-mode valuation candidate
```

但必须显式配置 pattern / rule；不能只凭 `recent_move_then_pause=True` 自动加分。

Probe P4 只在 `cadence_trigger` 被明确启用且存在 pattern ID 时生成 Candidate。

当前状态：**Candidate，证据要求最高。**

## 5. P0：没有机制就没有隐藏的 pause bonus

这是本轮最重要的执行不变量：

```text
recent pause
vs
long static
```

如果没有开启任何 attention / prediction / attack-window / cadence mechanism，则 evaluator 输出必须相同。

这并不是说现实中 pause 没作用；它表示系统必须说明“为什么有作用”。

这样可以防止未来出现：

```text
pause 已通过速度下降影响 TaskDemand
+ 又通过 favorable dwell 被时间积分
+ 又因为 recent_move_then_pause 字段自动 +20%
```

这种无法追溯的三重计权。

## 6. 当前 Working Contract

### TaskDemand

暂时保留两类最小任务语义：

```text
ResolvedTaskDemand
├─ Intercept / Closing Demand
└─ Maneuver / Capture-Geometry Demand
```

原始 speed / distance / orientation / vertical / roll 等不是天然独立 DOF；只有当它们对具体 task semantic 有独立作用时才进入。

### Pause-related effects

```text
move → pause
├─ attention continuity     → Perception / history Candidate
├─ trajectory break        → transient prediction / task-state Candidate
├─ favorable dwell horizon → temporal support / exposure Candidate
└─ cadence motif           → Valuation Candidate
```

没有 universal `pauseBonus`。

### Feeding Motivation

以上四条都不直接重写 fish-side Feeding Motivation。若未来发现 presentation 会诱发真正的 internal behavioral-state transition，需要单独证明并遵守 Readiness / Interaction ownership，不从这里偷渡。

## 7. 外部证据边界

现有研究支持以下较弱但重要的结构事实：

- 大口黑鲈与其他 centrarchid 捕食时需要主动 locomotor positioning；
- predator 可以通过 body orientation / position 调整 suction capture geometry；
- 大口黑鲈会随 sensory / flow condition 改变 approach、ram、suction、braking 等 capture kinematics；
- 大口黑鲈攻击底栖 goby 的观察中出现 stop-and-go、orientation / positioning、减速甚至停下后再 strike 的序列。

这些证据支持“捕获任务不只是 closing speed”以及“temporal sequence 值得保留为候选”，但不直接证明本 probe 的任何阈值、pause 时长或 cadence bonus。

参考：

- Higham 2007, *Feeding, fins and braking maneuvers: locomotion during prey capture in centrarchid fishes*, PMID 17170154.
- Holzman et al. 2014, *Modelled three-dimensional suction accuracy predicts prey capture success in three species of centrarchid fishes*, PMCID PMC4006267.
- Gardiner & Motta 2012, *Largemouth bass switch feeding modalities in response to sensory deprivation*, PMID 22285791.
- Takeuchi et al. 2012, largemouth bass attack behavior on gobies, J Exp Biol 215:2390-2398.
- *Feeding in Flow* 2026, largemouth bass alter prey-capture kinematics across flow speeds, PMID 42868420.

## 8. 下一步

下一轮不再继续添加新的 pause 名词。优先做两件事：

1. 对四条 pause candidate 做 **dependency / double-count audit**：尤其是 attention continuity、prediction break、favorable dwell 是否其实可以由现有 Perception / TaskDemand / support 机制自然导出，而不需要新增 persistent scalar；
2. 开始攻击 `Feeding-mode Valuation` 的最小语义：先从 vulnerability / temporal cadence 两个 Candidate 中选择一个，要求它在 TaskDemand、Perception 与 temporal support 都控制后仍能产生有意义的 ranking difference，否则删除。

在这两步完成前，不设计最终 `C_mode` 聚合公式。
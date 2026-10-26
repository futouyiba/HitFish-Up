# 方案 C｜Step 4 Counterfactual Closure：大口黑鲈 × 小型饵鱼

日期：2026-10-26  
状态：Working Probe Closure，不是 Current，不规定最终 response aggregation。

## 1. 范围

固定同一条大口黑鲈、同一小型饵鱼解释、相同 prey support（0.90）、相同鱼侧内部状态，只攻击三个反事实：

- Q1：只改变 target 当前速度；
- Q2：当前物理状态完全相同，只改变“刚停 / 久停”的时序前史；
- Q3：下沉速度和位置完全相同，只改变 roll 0° / 75°。

目的不是标定数值，而是判断 Step 3 信息究竟应该进入 TaskDemand、Target / Valuation，还是根本不获得独立作用。

可执行 probe：`../../prototypes/lure-response/proposal_c_step4_counterfactual_probe.py`。

本轮已在 ChatGPT 本地 Python 环境实际执行并通过全部 assertions。

## 2. Q1：当前速度反转

### 输入

同一 fish / prey support / distance，仅 target speed 取三档人工 probe 值：0.10、0.22、0.40。Fish capacity 同样使用人工 probe 阈值：comfortable closing 0.15，hard closing limit 0.30。

这些数字仅用于验证语义拓扑，不是大口黑鲈生物学阈值。

### 结果

```text
0.10 → Feasible
0.22 → Constrained
0.40 → Infeasible
```

prey support 始终为 0.90；feeding motivation 不随 target speed 被重写。

### 结论

当前速度变化已经可以通过：

```text
ActualPresentation motion
→ ResolvedTaskDemand
× ResolvedFunctionalCapacity comparison
→ TaskAffordance
```

自然制造 ranking / feasibility reversal。

因此首轮不 admission 独立的“fast lure penalty / slow lure bonus”。如果后续需要 cost 或 willingness effect，必须证明它不只是 TaskDemand 的重复投影。

生物力学证据支持较弱但足够的方向：大口黑鲈会随 prey-capture 条件调整 locomotor positioning、ram / suction 与捕获运动；更高流速等条件也会改变其捕获运动学。这支持 motion / geometry 进入 TaskDemand，但不提供这里的人工阈值。

## 3. Q2：刚停 vs 久停

### 输入

两种情况当前均为：

- target speed = 0；
- distance 相同；
- prey support = 0.90；
- fish state 相同。

唯一差异：

- Q2a：刚从移动转为停留，pause age = 0.20 s；
- Q2b：已经静止 5 s。

### 结果

两者得到完全相同的：

- TaskDemand；
- TaskAffordance；
- feeding motivation delta = 0；
- temporal valuation delta = 0。

`recent_move_then_pause` 只在 Explain 中不同。

### 结论

当前没有足够理由给 `recent_move_then_pause` 独立数值自由度。

因此默认契约应是：

```text
刚停
→ 当前速度下降
→ TaskDemand 改变

recent_move_then_pause
→ Explain / Candidate Mechanism only
```

如果未来要新增 temporal trigger，必须通过一个保持当前物理状态一致的 holdout，证明“刚停”和“久停”存在稳定、可复现、对玩家有策略意义的 ranking difference。

路亚经验材料确实常强调 cadence / pause 有时会改变咬口，但这类经验材料无法拆掉当前速度、位置、目标附近停留、注意触发等混杂因素，因此目前只能作为 Candidate evidence，不能直接晋升为独立 response bonus。

## 4. Q3：同样下沉，姿态不同

### 输入

两种情况完全相同：

- prey support = 0.90；
- target speed = 0.05；
- sinking speed = -0.05；
- distance 相同。

唯一差异：

- Q3a：roll = 0°；
- Q3b：roll = 75°。

### 结果

两者：

- TaskDemand 完全相同；
- TaskAffordance 完全相同；
- feeding motivation 不变。

仅 Q3b 生成：

```text
vulnerability_interpretation = candidate_vulnerable
```

### 结论

“失衡样侧翻”不能进入 capture feasibility；如果它未来有独立作用，只能通过 Target / Feeding-mode Valuation 路由。

这也意味着不能写：

```text
roll 75° → injured → easier → +response
```

因为其中至少包含三层尚未证明的语义跃迁。

当前仅允许：

```text
roll + sinking
→ imbalance-like cue
→ candidate vulnerability interpretation
→ optional valuation mechanism if later validated
```

若后续验证不出独立 ranking difference，则整个 vulnerability 分支删除，只保留姿态事实 / Explain。

## 5. 三个反事实共同排除的错误结构

这一轮可以较有把握地排除首轮 universal state scalar：

```text
stateBonus = f(speed, pause, sinking, roll, ...)
response = preySupport × stateBonus × motivation
```

原因不是“乘法一定错误”，而是这些输入属于不同因果角色：

- speed / geometry：TaskDemand；
- recent pause：目前只证明是 history / Explain；
- imbalance-like cue：Target / Valuation Candidate；
- Feeding Motivation：fish-side current context。

把它们提前压成一个 stateBonus 会丢失 owner、原因和反事实可解释性，也容易重复计权。

## 6. Step 4 当前最小闭合结构

```text
Target / prey interpretation
+ ActualPresentation current motion / geometry
+ fish-relative geometry
+ ResolvedFunctionalCapacity
        ↓
ResolvedTaskDemand
        ↓
TaskAffordance
= Feasible | Constrained | Infeasible | Unknown

同时：
Target value
+ optional evidence-backed valuation cues
+ current fish-side Feeding Motivation
        ↓
Feeding-mode Valuation

Perception / Target outcome
+ TaskAffordance
+ Feeding-mode Valuation
        ↓
Complete Feeding Response Mode
        ↓
C_mode
```

本轮只证明语义路由与最小反事实，不规定最后三者如何聚合，也不证明一定需要一个独立 scalar Valuation。

## 7. 当前 admission / rejection

### 暂时 admission

- `ResolvedTaskDemand`：需要；Q1 已证明其可购买真实 reversal 表达能力。
- `TaskAffordance`：需要；至少保留 Feasible / Constrained / Infeasible / Unknown。
- imbalance-like → vulnerability interpretation：只保留 Candidate semantic route，不保留 bonus。

### 暂不 admission

- fast lure penalty；
- pause bonus；
- `recent_move_then_pause` 独立系数；
- universal stateBonus；
- “失衡 = 受伤 = 易捕 = 加分”的捷径；
- target state 改写 fish Feeding Motivation。

## 8. 外部证据边界

大口黑鲈与其他 centrarchid 的研究显示，捕获成功依赖 locomotor positioning / strike timing，且大口黑鲈可随感知与环境条件调整 ram、suction、接近速度和捕获运动。这支持 TaskDemand / FunctionalCapacity 的因果位置。

这些研究不直接证明：

- 本 probe 的任何数值阈值；
- pause 有独立奖励；
- 侧翻路亚被鱼稳定解释为受伤猎物；
- 最终 response 应怎样聚合。

参考：

- Higham 2007, *Feeding, fins and braking maneuvers: locomotion during prey capture in centrarchid fishes*, PMID 17170154.
- Gardiner & Motta 2012, *Largemouth bass switch feeding modalities in response to sensory deprivation*, PMID 22285791.
- Holzman et al. 2014, *Modelled three-dimensional suction accuracy predicts prey capture success in three species of centrarchid fishes*, PMCID PMC4006267.
- *Feeding in Flow* 2026, largemouth bass modulate prey-capture kinematics across flow speeds, PMID 42868420.

Bassmaster 等钓鱼经验资料常见“pause / cadence 有时改变咬口”的叙述；这里只把它们视为 temporal-trigger Candidate evidence。此类资料通常同时改变当前速度、位置、结构物附近停留和注意触发，不能隔离证明 `recent_move_then_pause` 本身拥有独立 bonus。

## 9. 下一步

Step 4 下一轮不再增加 presentation state。优先解决两个更核心的问题：

1. `ResolvedTaskDemand` 最少需要哪些独立维度，才能解释距离、closing/interception 和必要 maneuver，而不重复参数化；
2. `Feeding-mode Valuation` 到底需要哪些真实独立语义。尤其要用 vulnerability Candidate 做一次 admission attack：如果它不能在 TaskDemand 相同的条件下产生稳定、策略可学习的 ranking reversal，就删除它。

在这两个问题闭合前，不设计最终 C_mode 聚合公式。
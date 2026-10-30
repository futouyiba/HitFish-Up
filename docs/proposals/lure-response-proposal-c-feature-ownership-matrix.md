# Proposal C｜Feature Ownership Matrix

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 目的

本页只解决一个问题：同一个 raw presentation / context feature 是否可以被多个 Response 路径消费，以及如何避免重复计权。

基本原则：

> 同一个 raw fact 可以有多个独立语义后果，但每个后果必须有不同 owner、不同问题定义和可复核的路径。不能因为同一事实“看起来重要”，就在多个系数里重复结算同一个结果。

第一版禁止匿名 residual bonus / penalty。

## 2. Feature → Owner Matrix

| Raw feature / event | 允许的首版 owner | 首版禁止的额外解释 | 说明 |
|---|---|---|---|
| lure speed relative to water | Closing | Suspicion、generic naturalness penalty | speed 回答追赶负担；除非未来有独立风险证据，不因“太快不自然”重复扣分 |
| radial-away component under latent bearing | Closing | Trigger、Suspicion | 只负责 Closing demand；当前不授予单变量 hard-feasibility authority |
| sudden direction change | prey-state interpretation → StateTrigger（仅 Escape-like v1） | PredictionCost；generic ErraticBonus / ErraticPenalty；Suspicion by default | 第一版只在形成 Escape-like 时进入 Trigger；Prediction Deferred，不能再从同一事件生成 active cost |
| burst / sudden acceleration | prey-state interpretation → StateTrigger；若改变 closing demand，则通过 speed 进入 Closing | generic ExcitementBonus；Suspicion by default | raw event 可改变多个不同中间量，但不能直接贴额外 multiplier |
| pause / low displacement | 通过低 speed 降低 Closing；通过 Opportunity 处理停留与时间支持；可改变 prey-state interpretation | PauseBonus、DwellBonus、PredictionCost | pause 本身不是 Trigger owner |
| favorable dwell duration | Opportunity | Feeding DecisionMargin；Response-owned exposure | 同一瞬时状态下，持续更久不提高瞬时 C；`L` 由 Opportunity 负责 |
| prey support | prey interpretation support；最终 `support × response` | SuspicionLoad=`1-support`；FoodValue | “不像某 prey”不等于“危险”或“这类 prey 不值钱” |
| low prey support | 同上 | automatic risk / unnaturalness penalty | 防止一次匹配不足被 support 与 risk 双扣 |
| tackle / line / hook conspicuousness | TackleConspicuousness → SuspicionLoad（有合法输入后） | prey support by default；Closing / Prediction；SKU 直接映射 | 当前无生产输入；未启用时 `RiskCost=0` |
| entry splash / impact / noise | CandidateUnresolved；未来可单独评估 | 当前 Risk MVP；generic disturbance coefficient | 本轮不进入第一版正式输入方向 |
| repeated exposure / conditioning | 当前未分配；待 Wariness Bake / memory owner 裁定 | 同时进入 Wariness 和 SuspicionLoad | 同一 fishing-pressure/history cause 不能在乘法两边重复放大 |
| fishing pressure | 优先作为 Wariness 上游 cause | SuspicionLoad by default | 防止 `Wariness × SuspicionLoad` 对同一 pressure 近似平方放大 |
| prey family identity | BaseDietAffinity / DietaryShift | support strength | 身份与“像不像”分开 |
| prey size | SizePreference / PreySizeFeasibility | Closing by default；Motivation | 除非尺寸改变物理 presentation speed 等具体事实，否则不跨 owner |
| prey current state | StateTrigger；必要时解释 metadata | BaseDietAffinity | 基础食性与当前状态诱发分开 |
| Fish Activity | Closing soft-cost multiplier | InterceptSpeedLimit；Motivation | Activity 不改物理硬速度，也不代表想不想吃 |
| FeedingMotivation | WillingnessThreshold | FoodValue multiplier；Closing | 只负责整体愿意接受多差的净交易 |
| Wariness | RiskCost sensitivity | global threshold；Closing | 只与已解析 SuspicionLoad 交互 |
| DietaryShift | prey-relative FoodValue delta | common-mode feeding boost | 所有 prey 共同升降优先归 Motivation |

## 3. 允许的多路径：必须回答不同问题

### 3.1 sudden turn

第一版只在 prey-state interpretation 形成 `Escape-like` 时进入 `StateTrigger`。Prediction Deferred，不从 sudden turn 生成 active `PredictionCost`。

禁止：

```text
+ ErraticBonus
- ManeuverPenalty
- SuspicionPenalty
```

在没有新增独立语义和证据时继续第三、第四次结算。

### 3.2 burst / sudden acceleration

同一个 burst 可以：

- 作为 prey-state evidence 提供 Trigger；
- 因为实际 lure speed 改变，通过 Closing 增减追赶负担。

这里也不是重复，因为一个是攻击价值，一个是执行成本。

禁止额外再加 `BurstBonus`。

## 4. 禁止的重复计权模式

### 4.1 speed 双扣

禁止：

```text
high speed
→ ClosingCost
→ SuspicionLoad because "unnatural"
```

除非 future controlled evidence 证明，在固定 Closing / prey support / Prediction 后，高 speed 本身仍构成独立 receiver-side risk cue。

### 4.2 low support 双扣

禁止：

```text
low prey support
→ support retention lower
→ SuspicionLoad = 1 - support
```

这会把“证据不足”偷换成“危险”，并重复处罚同一 presentation mismatch。

### 4.3 pause 重复奖励

禁止：

```text
pause
→ Closing lower
→ Prediction recovers
→ PauseBonus
```

pause 已经通过已有 owner 获益，不需要匿名 bonus。

### 4.4 fishing pressure 平方式放大

禁止：

```text
fishing pressure
→ Wariness high
→ SuspicionLoad high
→ RiskCost = Wariness × SuspicionLoad
```

除非两边分别有独立 cause。第一版 fishing pressure 优先归 Wariness 上游；SuspicionLoad 必须由当前 presentation-local risk cue 产生。

## 5. 新 Feature / Cue 的 admission gate

任何新 raw feature 想进入第二条 Response 路径时，必须回答：

1. 这条新路径回答的具体问题是什么？
2. 与现有 owner 的语义是否不同？
3. 控制现有路径后，是否还有稳定 residual ranking difference？
4. 玩家能否通过不同策略独立改变这个后果？
5. 是否会把同一个 raw cause 在加法或乘法结构里重复放大？

不能回答清楚时，保持 metadata / explain，不进入 numeric core。

## 6. 回归测试要求

至少建立以下 controlled pairs：

```text
A. same Closing / Prediction, different Trigger evidence
B. same Trigger / Closing, different Prediction disruption
C. same support, different Suspicion cue
D. same Suspicion cue, different support
E. same speed, different prey-state trigger
F. same prey-state, different speed
```

每组只改一个 semantic outcome，检查非 owner 路径不随之变化。

还应测试：

```text
Escape-like Trigger enabled
→ StateTrigger changes

Escape-like Trigger disabled
→ only baseline response paths remain
```

## 7. 当前缺口

- SuspicionLoad 的生产 cue 数据仍未闭合；
- Opportunity `L` 的 production contract 仍需实现；
- repeated exposure / conditioning 尚未决定属于 Wariness Bake、memory 还是其它 owner；
- Risk cue 未启用时 `RiskCost=0`；
- 本矩阵尚未写回总 Working Closure。

本页冻结首版 feature ownership 与防重复计权边界，不冻结各路径最终 effect size。
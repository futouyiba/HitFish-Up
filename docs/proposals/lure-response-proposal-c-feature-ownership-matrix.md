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
| radial-away component under latent bearing | Closing | Trigger、Suspicion | 只负责 closing demand / hard feasibility |
| sudden direction change | Prediction；prey-state interpretation → StateTrigger | generic ErraticBonus / ErraticPenalty；Suspicion by default | 可有双路径，因为一条回答攻击预测受损，另一条回答猎物状态触发；禁止第三次匿名结算 |
| burst / sudden acceleration | prey-state interpretation → StateTrigger；若改变 closing demand，则通过 speed 进入 Closing | generic ExcitementBonus；Suspicion by default | raw event 可改变多个不同中间量，但不能直接贴额外 multiplier |
| pause / low displacement | 通过低 speed 降低 Closing；通过时间推进使 PredictionChallenge 衰减；可改变 prey-state interpretation | PauseBonus、DwellBonus | pause 本身不是数值 owner |
| favorable dwell duration | temporal exposure / opportunity（待合法 Owner） | Feeding DecisionMargin | 同一瞬时状态下，持续更久不提高瞬时 C |
| prey support | prey interpretation support；最终 `support × response` | SuspicionLoad=`1-support`；FoodValue | “不像某 prey”不等于“危险”或“这类 prey 不值钱” |
| low prey support | 同上 | automatic risk / unnaturalness penalty | 防止一次匹配不足被 support 与 risk 双扣 |
| tackle / line / hook conspicuousness | SuspicionLoad（若有权威输入） | prey support by default；Closing / Prediction | 表达目标旁的非猎物风险线索 |
| entry splash / impact / noise | SuspicionLoad（若有权威输入）；若同时形成 prey-state event，必须独立取证 | generic disturbance coefficient | 需要明确时间窗和量纲；不能因为“刚抛入”自动处罚 |
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

允许：

```text
sudden turn
├→ prey-state escape / distress evidence
│  → StateTriggerValue (+)
└→ attack prediction disruption
   → PredictionChallenge
   → PredictionCost (-)
```

这不是重复计权，因为：

- Trigger 回答“这个猎物当前状态是否更容易触发攻击”；
- Prediction 回答“已有攻击预测是否更难维持”。

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
sudden turn with Trigger disabled
→ only Prediction changes

sudden turn with Prediction disabled
→ only Trigger path changes
```

用于证明两条路径可分别关闭，不是同一个隐藏 scalar 的两个名字。

## 7. 当前缺口

- SuspicionLoad 的生产 cue 数据仍未闭合；
- temporal exposure / opportunity 的 Current Owner 仍缺失；
- repeated exposure / conditioning 尚未决定属于 Wariness Bake、memory 还是其它 owner；
- 完整链路还需要测试 Closing + Prediction + Risk 多 soft-cost 同时叠加时是否过强；
- 本矩阵尚未写回总 Working Closure。

本页冻结首版 feature ownership 与防重复计权边界，不冻结各路径最终 effect size。
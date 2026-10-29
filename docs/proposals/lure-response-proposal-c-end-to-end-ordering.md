# Proposal C：Feeding Response 端到端计算顺序审查

> Status: Working Closure / topology audit
>
> Scope: ActualPresentation → prey interpretation → Feeding decision → latent-angle expectation → mode composition → captureRetention

## 结论

当前主链可以收成下面这个顺序：

```text
ActualPresentation
→ prey-type support
→ prey-conditioned current state
→ mode validity / resolution
→ FoodValue
→ StateTriggerValue
→ latent-angle task evaluation
→ DecisionMargin(theta)
→ ResponseProjection
→ C_mode = E_theta[C(theta)]
→ Interaction-owned mode composition
→ captureRetention C_i,j
→ Candidate Resolver: dQ = C · dM
```

本轮确认两条承重规则：

1. **latent angle 必须在 ResponseProjection 之后做期望**；
2. **prey-type support 不是概率分布，不能直接当 mixture weight。**

## 1. 哪些量在 angle 积分之外

以下语义通常对同一个 prey-mode 的所有 latent angle 共用：

```text
FoodValue
StateTriggerValue
WillingnessThreshold(Motivation)
Steering / Prediction soft consequence（若其定义不依赖 fish-relative angle）
```

Reject、Mode Invalid、ResolutionIncomplete 也应在进入 angle loop 前处理。

### Reject

```text
Target Relation = Reject
→ resolved zero
→ 不进入 angle integration
```

Trigger、Motivation 都不能救活 Reject。

### ResolutionIncomplete

```text
required input Unknown
→ no scalar
→ 不进入 projection / expectation
```

Unknown 不能被当成某些 angle 的零响应。

## 2. 哪些量必须留在 angle 内

当前 angle-only Closing 模型中，潜在鱼相对拟饵运动方向的角度 `theta` 会改变 Closing Demand。

因此：

```text
ClosingUtilization(theta)
→ local Closing gate / local ClosingCost
→ TaskCost(theta)
→ DecisionMargin(theta)
→ C(theta)
```

然后才：

```text
C_mode = E_theta[C(theta)]
```

### 为什么不能先平均 TaskCost

存在 hard zero、凸 TaskCost、clipped linear projection 时：

```text
E[C(theta)] != C(E[TaskCost(theta)])
```

Working probe 示例：

```text
base margin before task = 0.18
half angles task cost = 0.00
half angles task cost = 0.30
projection = clamp(margin / 0.20, 0, 1)
```

结果：

```text
project then average = 0.45
average task cost then project = 0.15
```

差异达到 3 倍。后者虚构了一条不存在的“平均鱼”。

因此 angle 是 mode 内部的 latent microstate distribution，不是一个应先压成平均 physically-feasible task consequence 的输入。

## 3. Closing hard gate 的正确粒度

当前只允许 Closing 在 angle-local 层面形成 hard infeasible：

```text
某 theta 下 lure radial-away demand > fish Closing Capacity
→ C(theta) = 0
```

但这不意味着整个 mode hard zero，因为其它 angle 仍可能容易截获。

因此错误写法是：

```text
存在任意难追 angle
→ whole mode Infeasible
```

正确语义是：

```text
这些微观几何状态被 thinning 掉
→ 剩余 angle 仍贡献 response
```

这与最终 `captureRetention` 的概率/保留比例语义一致。

## 4. Steering / Maneuver 不再拥有默认 hard gate

前序审查已经修正：

```text
trajectory turn rate / fish turn capability > 1
```

不能直接推出“捕获物理不可能”。鱼可以切弯、预测截获、等待进入 strike window。

因此第一版：

- Closing：可在 angle-local 层面 hard-zero；
- Steering / Prediction Challenge：只允许 soft consequence，除非未来有独立反例证明新的 hard physical boundary。

## 5. prey-type support 不能直接当概率

第 2 步的 prey support 定义是“有多少证据支持按某种 prey 来解释”，不是身份概率，也不要求和为 1。

例如：

```text
baitfish support = 0.90
crayfish support = 0.75
```

这是合法的，并不表示：

```text
90% baitfish + 75% crayfish
```

因此以下默认都错误：

```text
C = 0.90*C_baitfish + 0.75*C_crayfish
FoodValue *= prey_support
normalize supports then mixture-average C
```

这些都会把 evidence strength 偷换成 probability / response coefficient。

### 当前真正的缺口

`prey support` 怎样影响 complete-mode admission / composition，仍未闭合。

当前只能冻结：

- support=0 / NoMatch 与有效 mode 必须区分；
- support Unknown 不能被补成 0；
- support 数值不能直接当概率权重；
- 多 prey interpretations 若属于同一 capture opportunity 的 alternatives，其 composition 仍由 Interaction owner 决定；不能由 Candidate Resolver 做 mixture。

是否使用 max、evidence-qualified admission 或其它 operator，仍是 OPEN，不能在本页静默裁决。

## 6. 当前最小 Feeding numeric loop

对一个已经合法 admission 的 prey-conditioned feeding mode：

```text
baseDecisionValue
= FoodValue
+ StateTriggerValue
- WillingnessThreshold(Motivation)
```

对每个 latent angle：

```text
ClosingState(theta)
→ if local Closing Infeasible: C(theta)=0
→ else ClosingCost(theta)

TaskCost(theta)
= combine(ClosingCost(theta), SteeringSoftCost, ...)

DecisionMargin(theta)
= baseDecisionValue - TaskCost(theta)

C(theta)
= clipped_linear_projection(DecisionMargin(theta))
```

最后：

```text
C_mode = E_theta[C(theta)]
```

这比先构造一个综合平均 physically-feasible task consequence 更符合当前 retention 语义。

## 7. 不应重复计权的 Cause

### prey identity vs FoodValue

prey support 负责“是否有依据这样解释”；FoodValue 负责“鱼是否觉得这类目标值得吃”。不要把 support 再乘一次 FoodValue。

### StateTrigger vs prey support

同一 direction-change / burst raw fact 可以帮助解释 prey state，但不能既提高 prey-type support、又无条件再用同一个数值直接加 Trigger。两条链必须说明各自购买的语义。

### pause

pause 的作用留在 Closing、prediction break、favorable dwell / temporal support。StateTrigger 不因 pause 本身自动加分。

### Response 与 Candidate

Interaction 只输出一次 aggregate `captureRetention C_i,j`；Candidate Resolver 只做一次：

```text
dQ = C · dM
```

不得在 `W_i^opp` 之后再乘一次 Response。

## 8. 当前端到端 topology

```text
ActualPresentation facts
        ↓
Prey Interpretation
├─ prey support evidence
└─ prey-conditioned state semantics
        ↓
Mode admission / resolution
        ↓
Target Relation ─────────────→ FoodValue
Current prey state ──────────→ StateTriggerValue
Fish condition ──────────────→ WillingnessThreshold
species × size cohort → InterceptSpeedLimit
+ current motion / relative geometry
→ ClosingUtilization(theta) / local Closing hard gate
→ Activity-aware soft Closing cost
→ TaskCost(theta)
├─ DecisionMargin(theta)
└─ C(theta)
        ↓ expectation
C_mode
        ↓
Interaction mode composition
        ↓
CaptureResponsePacket(captureRetention + typed status)
        ↓
Candidate Resolver
Spatial dM × captureRetention
        ↓
Native Candidate
```

## 9. 仍未闭合

1. prey support → complete-mode admission / composition 的正式 operator；
2. `p(theta)` 是否长期保持 uniform，或允许 context-conditioned distribution；
3. Steering / Prediction soft cost 的 production function；
4. temporal support 与 instantaneous `C(theta)` 的最终接口；
5. `M0 / M1`、FoodValue、TriggerBudget、TaskCost 的生产校准；
6. Feeding 外其它 response families 的 composition。

其中第 1 项现在是最承重的结构缺口。其它公式继续细化之前，应优先避免把 prey support 偷偷当成概率权重。

## 10. Probe

对应可执行 topology probe：

`../../prototypes/lure-response/proposal_c_end_to_end_ordering_probe.py`

它验证：

- project-then-average 与 average-then-project 不等价；
- prey support 可以合法相加超过 1，因此不是 probability simplex。

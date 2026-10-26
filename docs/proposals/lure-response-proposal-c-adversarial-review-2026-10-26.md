# Proposal C｜整链攻击审查（2026-10-26）

状态：Working Review / Candidate。不是 Current，不是生产参数。

对齐范围：Proposal C 当前 Feeding Response Working 链。Activity 文档修改由另一执行线处理，本页不改 Activity 方案本身。

## 1. 结论

当前 Proposal C 的瞬时 Feeding Response 已形成较完整的数值链，但还不能称为“生产闭合”。

本轮攻击识别出 4 个 P0/P1 级结构缺口，以及若干 P2 数值与生产缺口。

最重要的结论：

```text
当前最大缺口不是再调 g / m / K_mot / M1，
而是 latent-angle prior、FoodValue adjustment boundary、feature ownership、以及 temporal exposure owner。
```

在这些问题解决前，不应把现有 Working seed 当 production calibration。

---

## 2. 当前链条

```text
Presentation
→ prey interpretation / support
→ prey-conditioned state

Fish-side state
├→ BaseDietAffinity + SizePreference + DietaryShift → CurrentFoodValue
├→ FeedingMotivation → WillingnessThreshold
├→ Activity / pursuit geometry → ClosingCost
├→ trajectory history → PredictionCost
└→ Wariness × SuspicionLoad → RiskCost

prey-conditioned state
→ StateTriggerValue

全部
→ DecisionMargin(theta)
→ ResponseProjection
→ C_conditional(theta)
→ E_theta[C_conditional(theta)]
→ prey support
→ Feeding composition
→ Interaction
→ captureRetention
→ Candidate join
```

Working numeric seed currently includes：

```text
Preferred = 1.00
Good      = 0.70
Marginal  = 0.40
Poor      = 0.00

K_mot     = 0.40
M0        = 0.00
M1        = 0.30
Trigger ordinary ≈ 0.10
Trigger upper guardrail ≈ 0.15
```

这些值只用于受控探针。

---

# 3. P0｜latent angle 的 prior 未定义

当前硬 topology：

```text
theta
→ local Closing feasibility / cost
→ local DecisionMargin
→ C(theta)
→ E_theta[C(theta)]
```

问题不在计算顺序，而在：

> `E_theta` 对哪一个 theta 分布取期望？

当前系统明确没有具体鱼点，也不应虚构鱼位置。因此没有天然的相对方位事实。

如果默认：

```text
theta ~ Uniform
```

等价于额外假设“潜在鱼从各方向等权出现”。这不是从现有事实推出的。

如果按：

- 当前流向；
- structure orientation；
- cast direction；
- fish holding orientation；
- shoreline geometry；

做非均匀 prior，则必须找到合法上游 owner 和数据。

### 影响

没有 angle prior 时：

```text
E_theta[C(theta)]
```

不是唯一值，因此 Feeding response scalar 尚未数学闭合。

### 建议

不要偷偷写 uniform。

需要单独做一个 `Latent Relative Geometry Prior` 决策：

A. 明确声明第一版 isotropic prior，并把它标成 production assumption；或
B. 从已有空间 / flow / holding-orientation owner 推导 prior；或
C. 放弃积分形式，改用一个不需要未知方向 prior 的保守摘要量。

在这个决策完成前，所有 angle-integrated 数值只应视为 probe。

---

# 4. P0｜CurrentFoodValue 的 adjustment boundary 未闭合

当前：

```text
CurrentFoodValue
= BaseDietAffinity
+ SizePreferenceAdjustment
+ DietaryShiftDelta
```

基础 relation gauge 已冻结：

```text
Poor      = 0
Preferred = 1
```

但 adjustment 后可能出现：

```text
CurrentFoodValue > 1
CurrentFoodValue < 0
```

目前没有 production 规则说明：

- clamp 到 `[0,1]`；
- 允许 extrapolation；
- 每个 adjustment 自己受限；
- 还是使用其它 constrained composition。

### 为什么不能以后随便 clamp

如果：

```text
Base = Preferred = 1
DietaryShift = +0.15
```

直接 clamp 后，正向 shift 完全不可见。

类似地：

```text
Base = Poor = 0
SizeAdjustment = -0.15
```

clamp 会吞掉负向差异。

这会造成：

- relation 顶部 / 底部大量饱和；
- DietaryShift / SizePreference 的 effect-size 难以识别；
- calibration 被迫在中间 relation 才有意义。

### 建议

下一轮单独裁 `CurrentFoodValue` 的合法域和 adjustment composition。

优先检查三种候选：

1. bounded residual headroom：adjustment 只消费距上下界的剩余空间；
2. latent score → bounded projection：relation anchor 只是 latent score，再投影到 response-value；
3. 允许有限 extrapolation，但 DecisionMargin calibration 明确接受 >1 / <0。

在未裁前，不冻结 DietaryShift / SizePreference 最终幅度。

---

# 5. P1｜同一 presentation feature 可能跨 support / Trigger / Prediction / Suspicion 重复计权

当前架构允许同一物理事件产生不同语义后果，这本身是合理的。例如：

```text
sudden redirection
├→ escape-like evidence → StateTrigger (+)
└→ prediction disruption → PredictionCost (-)
```

但整链仍存在更广泛的 feature ownership 风险。

例如某个“异常动作 / 明显装备 / 入水扰动”可能同时被用来：

- 降低 prey support；
- 增加 SuspicionLoad；
- 增加 PredictionChallenge；
- 影响 prey-state interpretation；
- 甚至未来影响 attention / opportunity support。

如果只说“语义不同所以都可以用”，很容易形成同一 raw feature 的多次负向惩罚。

Wariness 文档已经明确：`1 - prey_support` 不能直接变成 SuspicionLoad；同一 raw fact 若双路消费必须做 controlled fixture。这条原则应提升为整链级规则。

### 建议

建立一个 `Presentation Feature Ownership Matrix`：

| raw feature | support | prey-state / trigger | prediction | suspicion | temporal exposure |
|---|---|---|---|---|---|
| sudden redirection | 可作为 identity/state evidence | 是 | 是 | 默认否 | 否 |
| splash / entry disturbance | 默认否 | 视 prey 解释 | 否 | 候选是 | event/history |
| tackle visibility | 否 | 否 | 否 | 是 | 否 |
| low displacement / pause | state evidence | 可能 | prediction recovery | 默认否 | 是 |

每一个双路消费必须回答：

> 两条路径是否在回答不同的 counterfactual？

如果拿掉其中一条，另一条是否仍有独立存在理由？

---

# 6. P1｜soft costs 的联合预算尚未验证

当前 soft negative terms：

```text
ClosingCost
PredictionCost
RiskCost
```

均加法进入同一 DecisionMargin。

单项预算有若干 guardrail，但缺少“真实 presentation 下三项同时出现”的联合篮子。

风险：

```text
Closing 0.15
+ Prediction 0.10
+ Risk 0.10
= total burden 0.35
```

对当前：

```text
Good(reference margin) = 0.30
```

会直接清零。

这可能是合理体验，也可能导致多数现实操作只有 Preferred 才工作。当前不足以判断。

### 建议

不要先加 total-cost cap。

先做 burden coexistence basket，至少覆盖：

```text
steady natural retrieve
fast-away retrieve
moderate dart
hard erratic retrieve
stealth finesse
visible / intrusive presentation
```

检查真实操作中三项成本的共现结构。

若大量正常操作稳定出现 `total soft burden > 0.30`，应优先检查重复 ownership 或各 cost budget，而不是直接提高 M1。

---

# 7. P1｜瞬时 C 与累计中鱼效率之间仍有明确 owner 缺口

当前 `C` 明确不是：

- 每秒 bite probability；
- 最终 candidate probability；
- 累计中鱼率。

Favorable dwell 已被正确排除出瞬时 DecisionMargin。

因此需要：

```text
instantaneous resolved response
× temporal exposure / opportunity support
→ cumulative opportunity
```

当前已知仓内没有该链的 Current Markdown Contract owner。

### 影响

即使瞬时 Feeding Response 完全闭合，仍无法仅凭 C 回答：

- 停 0.2 秒和停 3 秒最终差多少；
- 某段 retrieve 的总攻击机会；
- 操作 cadence 最终如何改变单位时间中鱼效率。

这也是现在不能用单次 C 直接做体验标定的主要原因之一。

### 建议

明确登记为外部 Owner 缺口，不让 Feeding 接管。

后续需要一个 Opportunity / Temporal Exposure contract 承接。

---

# 8. P2｜Good 在理想条件下与 Preferred 同时饱和

当前：

```text
Good reference margin = 0.30
M1 = 0.30
```

因此零 burden 时：

```text
Good      → C = 1
Preferred → C = 1
```

已有解释是：Preferred 买到更大的 burden tolerance，而不是更高 peak。

这在结构上成立，但需要攻击一个体验风险：

> 如果实际大多数 presentation 的 total burden 很低，Preferred / Good 会长期无法区分。

因此不能只在数学上接受这一点，要在完整 probe 里检查现实操作的 burden 分布。

如果大多数 Good case 都落在 C≈1，应优先调整：

- `Good anchor`；或
- `M1`；

而不是给 Preferred 再加额外 bonus。

---

# 9. P2｜Prey support × projected response 可能形成过强双层筛选

当前：

```text
C_prey
= prey_support × E_theta[C_conditional]
```

语义上 support 与 fish-side response 不同，因此不是天然重复计权。

但完整体验上存在压缩风险。例如：

```text
support = 0.6
fish-side C = 0.5
→ C_prey = 0.3
```

再进入 Interaction / Candidate 后可能继续被其它结构缩小。

这不是结构错误，但必须在 full-chain simulation 看分布，不能单独把 fish-side C 调得很激进来补 support multiplication。

### 护栏

若 full-chain 输出过低，应先定位是：

- support calibration；
- response projection；
- Interaction composition；
- Candidate normalization；
- temporal opportunity；

哪一层造成的，不允许加匿名 compensation coefficient。

---

# 10. P2｜SuspicionLoad 与 RiskCost 仍不可生产

当前 topology：

```text
RiskCost = K_wary × Wariness × SuspicionLoad
```

语义是清晰的，但：

- Suspicion cue vocabulary 未闭合；
- tackle visibility 没有 Current owner；
- entry disturbance 标尺未闭合；
- repeated exposure / conditioning owner 未闭合；
- K_wary 未标定。

所以 Wariness 路径当前是“结构闭合、数据未闭合”。

不要因为公式存在就把它计入 production-ready response。

---

# 11. P2｜生产数据依赖仍未闭合

以下量仍缺 production source / coverage：

- species × size cohort 的 `InterceptSpeedLimit`；
- cohort representative length；
- 全量约 200 鱼种的 DietArchetype / BaseDietAffinity coverage；
- prey-family catalog 的 production coverage；
- SizePreference 的生产曲线；
- SuspicionLoad cues；
- angle prior；
- temporal exposure owner。

当前仓内 Fixed Bake fixture 只有 largemouth bass Q3 reference fixture，不能证明上述全量 production data 已存在。

---

# 12. 暂时未发现的结构问题

本轮没有发现必须撤回的下列设计：

### A. FoodValue 与 Motivation 分离

```text
FoodValue → prey-specific value
Motivation → global willingness threshold
```

当前仍成立，且比 `FoodValue × Motivation` 更容易识别。

### B. Activity 不改物理速度上限

按当前 Owner 决定，Activity 只应影响 soft pursuit cost，不应重新变成 `InterceptSpeedLimit × Activity`。Activity 线由其它执行者同步，本审查不重复修改。

### C. Trigger 与 Prediction 双路

同一 sudden-redirection event 同时：

```text
Trigger (+)
PredictionCost (-)
```

有独立 counterfactual，当前不是重复计权。

### D. Reject 独立于 Poor

仍应保持：

```text
Poor → continuous low value
Reject → hard non-responsive semantic boundary
```

### E. projection 使用 clipped linear

当前没有证据要求改 sigmoid。projection 本身不是首要风险。

---

# 13. 推荐闭合顺序

下一步优先级：

```text
P0-1  Latent angle prior
P0-2  CurrentFoodValue adjustment boundary
P1-1  Presentation Feature Ownership Matrix
P1-2  soft-burden coexistence basket
P1-3  temporal exposure / opportunity Owner gap 登记并路由
P2    再回头调 M1 / relation anchors / cost budgets
```

不要先继续增加新状态参数。

---

# 14. 当前判断

Proposal C 已经从“框架概念讨论”进入“可做系统性攻击”的阶段，这是进展，但还没有 production closure。

当前最大的设计风险已经从公式本身转移到：

```text
隐藏假设
+ feature ownership
+ production data availability
+ 跨阶段累计机会
```

下一轮应首先闭合 latent-angle prior。因为只要 `E_theta` 的 measure 未定义，当前完整瞬时 response 就还不是唯一函数。

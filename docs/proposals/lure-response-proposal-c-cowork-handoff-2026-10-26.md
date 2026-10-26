# Proposal C｜Claude Cowork Handoff｜2026-10-26

状态：Raw Handoff / Working Context。不是 Current，不是生产规范。

用途：让新的 Claude Cowork / coding agent 在**不重读完整聊天历史**的情况下，安全接手「路亚 Feeding Response / Proposal C」当前设计线，并继续清理、验证、收口。

---

## 0. 接手时先做什么

不要直接从本页内容开始改机制。

先执行最小 Documentation Rebase：

1. 读 `docs/README.md`；
2. 读 `docs/authority-model.md`；
3. 按当前任务读取相关 Current / contracts；
4. 再读本页和下面列出的 Working 文档；
5. 如果 Current 与本页冲突，以 Current / Owner 裁定为准，并把冲突写出来，不要静默裁决。

当前仓内 Authority 规则：Git Markdown 是已收口规范的可 diff 权威载体；历史材料和 Working / Candidate 不能因为“已经写在仓里”自动升为 Current。

---

## 1. 仓库、分支、PR 与版本风险

仓库：`futouyiba/HitFish-Up`

当前 Working 分支：

```text
docs/lure-response-joint-evaluation
```

Draft PR：

```text
#130  docs: 路亚摄食响应方案 B 与方案 C
```

本 handoff 写入前：

```text
main = cd74d363d0478d7c7aecfeb7320ff0419b1b6fd0
branch head = 9693589ce506146ae0bc7e936991c309e62cc7e5
merge base = 1dbb6ee5f39a0a233e20eb454045b24c51785e1f
branch vs main = ahead 154 / behind 110
```

因此：

- 分支已明显 diverged；
- PR 仍是 Draft、未合并；
- **不要 merge**；
- **不要因为 Working 设计已经较完整就提升为 Current**；
- 准备真正合并或晋升 Current 前，必须单独做 rebase / conflict / authority audit。

已有远端对齐审计：

`docs/proposals/lure-response-proposal-c-remote-alignment-audit-2026-10-26.md`

它确认：最新 `main` 没有发现直接 supersede Proposal C 的仓内 Feeding Response production formula；Response Authority 仍有外部 linked owner，因此 Proposal C 只能保持 Working / Candidate。

---

## 2. 当前任务范围

现在不要重新设计整个 FCF，也不要重新讨论 Candidate Weight / Spatial Distribution / Fish AI。

当前窄范围是：

> **路亚 Feeding Response：从 ActualPresentation 的 prey interpretation，一直到 Feeding 内部 response coefficient，再交给 Interaction / Candidate。**

当前主链：

```text
ActualPresentation
→ prey support
→ prey-conditioned current state
→ FoodValue / StateTrigger / Activity-aware Closing / Prediction / FeedingMotivation
→ latent-angle conditional response
→ prey-mode response
→ Feeding composition
→ Interaction composition
→ captureRetention C_i,j
→ Candidate Resolver: q_i,j = L_i,j × C_i,j
```

Candidate 只消费 Interaction 聚合后的 `captureRetention C_i,j`，Response 不能在 Candidate 再乘一次。

---

## 3. 当前最新 Owner 决定：FunctionalCapacity 退出

**这是最近一轮最重要的变化。**

用户决定：

> `FunctionalCapacity` 与 `Activity` 语义过于重叠。计划去掉 FunctionalCapacity。Fish Condition Bake 直接烘出：
>
> - `Activity`
> - `FeedingMotivation`
> - `Wariness`
> - `DietaryShift`

不要再恢复 `FunctionalCapacity → InterceptCapacity` 作为当前 Working 路线。

旧文档：

`docs/proposals/lure-response-proposal-c-functional-capacity-to-intercept.md`

已经压成 Superseded stub，只用于历史考古。

---

## 4. 四个 Bake 输出的职责

当前 Working 语义：

| Bake 输出 | 回答什么 | 当前消费位置 |
|---|---|---|
| `Activity` | 当前主动发起和维持运动行为有多容易 | physically-feasible Closing 的 soft cost |
| `FeedingMotivation` | 当前有多愿意为了食物出手 | `WillingnessThreshold` |
| `Wariness` | 当前面对风险 / 可疑呈现有多受抑制 | 独立 Wariness response path，尚未闭合 |
| `DietaryShift` | 当前食性相对基线如何偏转 | TargetRelation / FoodValue 上游 |

同一个原始原因可以同时影响多个 Bake 输出，但必须由上游分别解释。例如低温可以同时降低 Activity 和 FeedingMotivation，但 Response 不能因为 Activity 低就自动降低 Motivation。

禁止把四个结果重新压回一个“总体鱼情系数”。

---

## 5. Activity 当前 Working Contract

主文：

`docs/proposals/lure-response-proposal-c-activity-bake-contract.md`

辅助职责文档：

`docs/proposals/lure-response-proposal-c-activity-closing-ownership.md`

### 5.1 Activity 定义

Activity 只回答：

> 当前这类鱼在当前环境与时间上下文下，主动发起和维持运动行为有多容易。

它不是：

- 物理极速；
- 摄食意愿；
- 风险回避；
- 食物偏好；
- 总体“鱼情好坏”。

首版标尺：

```text
Activity ∈ [0,1]

1.0 = reference-high activity；不增加额外 pursuit soft cost
0.0 = 强低活跃状态；追赶明显不利，但不表示失去物理运动能力
```

特别注意：

```text
Activity = 0
≠ InterceptSpeedLimit = 0
```

低 Activity 的鱼仍可以吃停顿、缓慢、或朝鱼移动的目标。

### 5.2 Activity Bake reducer

首版 Working 候选：把每个已准入 raw cause 解释成“仅看这个原因，当前最多支持多少 Activity”。例如：

```text
A_period
A_temperature
A_oxygen
A_other...
```

然后：

```text
Activity = min(enabled resolved activity-support causes)
```

语义是 bottleneck，而不是乘法复利。

理由：避免无证据的：

```text
0.8 × 0.8 × 0.8 = 0.512
```

如果未来 controlled fixture 证明多个中等原因存在稳定、可学习的累积抑制，再重开 reducer。

Unknown / Disabled / NotApplicable 必须区分：

```text
required cause = Unknown
→ Activity = Unknown
→ 依赖 Activity 的 Closing ResolutionIncomplete

Disabled / NotApplicable
→ 不参与 min
```

---

## 6. 物理速度上限与代表长度

最新方向：**物理追赶上限直接来自鱼种 / 体型配置，不由 Activity 动态修改。**

首版结构：

```text
FishSpeciesConfig
├─ reference_length
├─ reference_intercept_speed
└─ size_scaling_rule

Species × SizeCohort
├─ representative_length
└─ baked_intercept_speed_limit
```

runtime Response 优先直接查 baked `intercept_speed_limit`。

### 6.1 代表长度优先级

```text
1. 已有权威具体个体长度
2. 当前 species × cohort 的真实生成分布中位数
3. cohort authoring reference length
4. 最后才退化到 species reference length
```

不要使用“整个鱼种平均长度”。

如果 cohort 只有 `[min_length, max_length]` 且明确按长度均匀生成，中位数才等于区间中点。

如果同一 cohort 的尺寸跨度已经让：

- `InterceptSpeedLimit` 明显跨档；
- 同一 retrieve 在 cohort 内一部分可追、一部分不可追；
- response ranking 对 size distribution 高度敏感；

则一个代表长度已经不够。优先拆 cohort；必要时才考虑 size distribution integration。首版不要为了精度引入隐藏 size micro-sampling。

---

## 7. Closing 当前公式

当前 Working：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
u_close(theta) = max(0, q * cos(theta))

if u_close(theta) >= 1:
    C_conditional(theta) = 0
else:
    ClosingCost(theta)
    = K_close * u_close(theta)^2
      * ActivityCostMultiplier(Activity)
```

Activity multiplier 首版：

```text
ActivityCostMultiplier(A)
= 1 + K_activity * (1 - A)
```

其中：

- `A=1` → multiplier = 1；
- Activity 越低，主动追赶 soft cost 越高；
- `u_close=0` → ClosingCost=0，因此 Activity 不产生匿名全局 penalty；
- `K_close`、`K_activity` 都未 production calibration。

### 7.1 hard feasibility 与 Activity 必须分开

不要采用：

```text
EffectiveSpeedLimit = InterceptSpeedLimit × Activity
```

否则会把“当前不活跃”偷换成“物理上追不上”。

hard infeasible 只由：

- species / size 对应的 `InterceptSpeedLimit`；
- 当前 lure relative-water motion；
- latent angle；

共同决定。

Activity 只影响**已经物理可行**的 pursuit 有多费劲。

策略故事：

```text
低 Activity + 高速背离
→ 很差

低 Activity + 慢速 / pause
→ 明显 rescue
```

---

## 8. Feeding Response 其它已收口边界

以下不要轻易重开：

### 8.1 Prey support

- support 是 prey interpretation 的证据强度；
- 不要求不同 prey support 和为1；
- 不是 prey probability；
- Unknown / NotConfigured / NoMatch 分开；
- first version：

```text
C_prey = support_prey × E_theta[C_conditional,p(theta)]
```

这是尺度复用，不是概率解释。

### 8.2 多 prey interpretation

同一个 physical lure 同时支持 baitfish / crayfish 等，默认是同一次 feeding opportunity 的 alternative sibling interpretations：

```text
C_feed = max(C_baitfish, C_crayfish, ...)
```

不要默认求和、概率 union、support-normalized average。

### 8.3 FoodValue / StateTrigger / Motivation

当前解释：

```text
AttackValue = FoodValue + StateTriggerValue

DecisionMargin(theta)
= FoodValue
+ StateTriggerValue
- ClosingCost(theta)
- PredictionCost
- WillingnessThreshold(FeedingMotivation)
```

`AttackValue` 只是解释对象，不要求成为 runtime object。

`StateTriggerValue` 属 prey + current-state local value，不修改 fish-global Motivation。

`Reject` 是 hard semantic boundary；高 Motivation / Trigger 不能救活 Reject。

### 8.4 Prediction

通用：

```text
ManeuverCost = omega_traj / fish_turn_capacity
```

已经撤回。

现在只保留：

```text
sudden direction change
→ PredictionChallenge
→ soft PredictionCost
```

Working probe：

```text
TurnStrength(delta_psi) = (1 - cos(delta_psi)) / 2
P(t) = max_recent[TurnStrength * exp(-age / tau_recover)]
PredictionCost = K_pred * PredictionChallenge
```

`K_pred` 当前 Working budget 约 0.08～0.12，但不是 production parameter。

Prediction 不拥有 hard-zero authority。

### 8.5 latent angle integration

硬 topology：

```text
theta
→ Closing hard-zero / cost
→ DecisionMargin(theta)
→ ResponseProjection
→ C(theta)
→ E_theta[C(theta)]
```

**不能先平均 cost 再 projection。**

### 8.6 ResponseProjection

首版倾向 clipped linear：

```text
C = clamp((Margin - M0) / (M1 - M0), 0, 1)
```

`M0/M1` 未 production calibration。

### 8.7 Pause / dwell / cadence

- 不准入匿名 `PauseBonus`；
- pause 可以通过 Closing 下降、Prediction 恢复、prey-state interpretation 改变而生效；
- favorable dwell duration 不进入瞬时 Feeding C；其累计价值属于 temporal exposure / opportunity owner；
- 第一版不准入独立 `CadenceValue / CadenceBonus / CadencePenalty`；只有 residual fixture 成立才重开。

### 8.8 Candidate seam

Feeding 只是 Interaction 内部 complete-mode contribution。

Interaction 聚合后产生：

```text
CaptureResponsePacket
└─ captureRetention C_i,j
```

Candidate Resolver：

```text
q_i,j = L_i,j × C_i,j
```

Response 只结算一次。禁止：

```text
L × C → W → W × C
```

---

## 9. 当前已知文档冲突

### 9.1 Feeding Response Working Closure 仍残留旧 FunctionalCapacity 段落

文件：

`docs/proposals/lure-response-proposal-c-feeding-response-working-closure.md`

里面仍有类似：

```text
LocomotorBaseline
× CapacityStateModifier(FunctionalCapacity)
→ EffectiveInterceptCapacity
```

这段已经被最新 Owner 决定 supersede。

**Claude Cowork 的第一项任务应该先修这个总入口。**

修正方向：

```text
species × size cohort
→ InterceptSpeedLimit
→ hard Closing feasibility

Fish Condition Bake
→ Activity
→ Closing soft-cost multiplier

Fish Condition Bake
→ FeedingMotivation
→ WillingnessThreshold
```

不要顺手重写其它已收口章节；只做必要 consistency delta，再回读检查。

### 9.2 旧窄文档不等于当前规则

以下类文档很多是历史 Working / probe evidence：

- locomotor baseline generation；
- functional capacity projection；
- maneuver input routing；
- 早期 TaskCost / pause / cadence 探针。

不要因为文件仍在就拼回当前 Working Closure。

---

## 10. 下一步建议顺序

### P0：先修文档一致性

1. 更新 `lure-response-proposal-c-feeding-response-working-closure.md`；
2. 全文搜索 `FunctionalCapacity / EffectiveInterceptCapacity / LocomotorBaseline`，判断哪些是历史证据、哪些仍误写成当前方案；
3. 不删除历史证据，必要时标 `Superseded`；
4. 回读 PR #130 body 与 Working Closure，确保一致。

### P1：Activity production closure

不要马上调最终 coefficient。先闭合：

- `A_period` 的 authoring / bake 语义；
- `A_temperature` 的输入是什么：绝对温度、对 species 的适宜度、还是已归一化 suitability；
- `A_oxygen` 同理；
- 这些 cause curve 是否应配置在 Species Base / cohort / template；
- `min` reducer 的 controlled counterexamples。

重点攻击 `min`：

> 两个分别只有中等抑制的原因同时发生时，是否真的不应比任一单独原因更差？

如果答案是“应更差”，不要直接跳到 product；先定义想购买的玩家策略故事，再比较 capped-sum / generalized mean / bottleneck+surcharge 等低自由度模型。

### P2：Activity effect-size

在 reducer 稳定后，才标 `K_activity`。

至少要有以下 controlled fixtures：

```text
same fish / same prey / same motivation
Activity high vs low
× retrieve slow / normal / fast
```

要求：

- slow 的差距小；
- fast 的差距明显；
- pause 不产生 Activity penalty；
- Activity 变化不能改写 prey support / FoodValue / Motivation；
- hard feasibility 不随 Activity 改变。

### P3：InterceptSpeedLimit production

再做：

- reference speed 的数据来源；
- size scaling；
- cohort representative length；
- cohort 是否需要拆分的自动验收。

不要用一个跨物种 `L^0.5` 之类的未标定公式直接生产化。

---

## 11. 当前 OPEN 列表

仍未闭合：

- FoodValue production anchors；
- FeedingMotivation → WillingnessThreshold production mapping；
- `K_close`；
- `K_activity`；
- Activity raw cause curves；
- Activity `min` reducer 是否成立；
- species × size cohort `InterceptSpeedLimit` 的生产数据；
- representative length 的真实数据源；
- cohort 拆分阈值；
- Wariness response path；
- latent-angle prior；
- Prediction event extraction；
- `tau_recover` / `K_pred`；
- `M0/M1`；
- StateTrigger production budget；
- support × conditional response production calibration；
- prey-family-specific state rules；
- temporal exposure / cumulative opportunity Current Owner；
- Feeding / Defense / Investigation route graph；
- runtime hot-path representation；
- production regression thresholds。

---

## 12. 推荐阅读顺序

接手本任务，不要扫完整 `docs/proposals/`。

最小顺序：

```text
1. docs/README.md
2. docs/authority-model.md
3. docs/proposals/lure-response-proposal-c-remote-alignment-audit-2026-10-26.md
4. 本 handoff
5. docs/proposals/lure-response-proposal-c-activity-bake-contract.md
6. docs/proposals/lure-response-proposal-c-activity-closing-ownership.md
7. docs/proposals/lure-response-proposal-c-feeding-response-working-closure.md
8. PR #130 body
```

需要某个具体问题的推导证据时，再按需读窄文档，不要默认全量加载。

---

## 13. 工作纪律

- 不要 merge PR；
- 不要把 Candidate 写成 Current；
- 不要从历史聊天补造缺失规则；
- 修改前先确认 owner / scope；
- 推导和 production 参数分开；
- 事实、Owner 决定、Working hypothesis、建议、OPEN 分开写；
- 保留 Unknown / zero / NotConfigured / NotApplicable 的语义差异；
- 不因为“公式能跑”就宣称标定完成；
- 每次新结构必须检查 double counting；
- 小步提交，写后回读；
- 如果发现和 main / Current 冲突，先报告，不静默裁决。

---

## 14. 给 Claude Cowork 的建议首轮目标

首轮不要继续发散设计。

目标只做：

> **把最新 Owner 决定完整投影进 Working Closure，并建立一个干净、无 FunctionalCapacity 残留的 Activity-aware Feeding Response baseline。**

完成标准：

1. Working Closure 不再把 FunctionalCapacity 当当前输入；
2. hard `InterceptSpeedLimit` 与 soft `Activity` 职责清楚；
3. 四个 Bake 输出职责表存在且无重叠；
4. 旧 FunctionalCapacity 文档明确 Superseded；
5. PR body 与 Working Closure 一致；
6. 不修改尚未讨论的 Wariness / DietaryShift 生产公式；
7. 不 merge。

完成这一轮后，再进入 Activity cause curves / reducer 的设计与攻击。

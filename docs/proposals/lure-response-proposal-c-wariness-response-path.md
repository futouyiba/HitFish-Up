# Proposal C｜Wariness Response Path

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`Wariness` 不作为第二份 `FeedingMotivation`，也不直接抬高全局 `WillingnessThreshold`。

第一版把鱼侧当前警惕状态与当前呈现的可疑 / 风险负担分开：

```text
Wariness
× SuspicionLoad
→ RiskCost
```

然后进入 Feeding Decision Margin：

```text
DecisionMargin(theta)
= FoodValue
+ StateTriggerValue
- ClosingCost(theta)
- PredictionCost
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

`Wariness` 回答：当前这类鱼对风险 / 异常线索有多敏感。

`SuspicionLoad` 回答：当前这次呈现里，有多少已解析的风险 / 可疑证据需要被警惕状态放大。

## 2. 为什么不能把 Wariness 直接当总减益

若直接使用：

```text
C *= (1 - Wariness)
```

或：

```text
WillingnessThreshold += WarinessPenalty
```

会把“警惕”偷换成“所有食物都不想吃”。这样无法表达高钓压下通过更自然、更轻、更安静、更低侵入的呈现恢复咬口。

第一版要求：

```text
SuspicionLoad = 0
→ RiskCost = 0
```

因此高 Wariness 不会凭空处罚一个没有已知可疑线索的呈现。

## 3. 与其它变量的边界

### FeedingMotivation

```text
FeedingMotivation
→ 值不值得为了食物出手

Wariness
→ 面对可疑 / 风险线索时有多受抑制
```

二者都可以受 fishing pressure、时段、历史事件等上游原因影响，但 Bake 必须分别产出。

禁止在 Response 内由低 Motivation 自动推高 Wariness，或由高 Wariness 自动降低 Motivation。

### Activity

`Activity` 只影响主动追赶的 soft cost。Wariness 不修改 `InterceptSpeedLimit`，也不进入 ClosingCost。

### DietaryShift

`DietaryShift` 改变 prey / food 的相对评价。Wariness 不修改 prey identity，也不把某食物变成 Reject。

### Prediction

PredictionChallenge 表达攻击预测刚被破坏的任务难度；Wariness 表达风险 / 可疑抑制。两者不互相替代。

## 4. SuspicionLoad 的 owner

`SuspicionLoad` 不能由 Wariness 自己生成，否则会形成自乘式循环。

建议 owner：Interaction / Target-Presentation Interpretation 侧，根据已解析的 presentation / tackle / disturbance / history cues 形成目标局部的风险负担。

Presentation 只提供事实；下游解释这些事实是否对当前鱼构成可疑 / 风险证据。

第一版不把 `1 - prey_support` 直接当 `SuspicionLoad`。

原因：

- prey support 低只表示当前呈现对某 prey interpretation 的支持不足；
- 不等于鱼一定认为它危险；
- 否则同一“自然度不足”会先降低 prey support，再通过 SuspicionLoad 重复处罚。

若同一 raw fact 同时影响 prey support 和 SuspicionLoad，必须能说明两条独立语义后果，并通过 controlled fixture 检查是否重复计权。

## 5. 第一版数值形状

最小自由度候选：

```text
RiskCost
= K_wary × Wariness × SuspicionLoad
```

Working 约束：

```text
Wariness ∈ [0,1]
SuspicionLoad ∈ [0,1]
K_wary >= 0
```

其中：

- `Wariness = 0` → generic wary response path 不产生额外成本；
- `SuspicionLoad = 0` → 当前 presentation 不受 Wariness 处罚；
- 固定其它量，Wariness 增加不能提升 response；
- 固定其它量，SuspicionLoad 增加不能提升 response。

`K_wary` 尚未 calibration。

当前没有证据准入 `Wariness²`、sigmoid threshold、hard gate 或多个 free coefficients。

## 6. 不拥有 hard-zero authority

Generic Wariness 第一版只允许 soft cost：

```text
Wariness high
→ RiskCost high
```

不能直接：

```text
Wariness > threshold
→ C = 0
```

如果未来存在明确的 predator / alarm / acute-danger semantic，需要作为具名状态另行 admission，不能偷塞进通用 Wariness。

因此强 StateTrigger、很高 FoodValue 或很低 SuspicionLoad 仍可能让高 Wariness 鱼产生 response。

## 7. 对策略体验的要求

该路径主要购买以下策略故事：

```text
高 Wariness + 高 SuspicionLoad
→ 明显压低 response

高 Wariness + 低 SuspicionLoad
→ 仍保留较好 response

低 Wariness + 同一 SuspicionLoad
→ 处罚较轻
```

它应允许：

- 高钓压时自然 / finesse / stealth presentation 相对受益；
- 强 prey-state trigger 有机会压过部分风险成本；
- “警惕”与“没食欲”在玩家策略上可区分。

## 8. Unknown / zero

必须区分：

```text
Wariness = Unknown
→ 若本 response path 被启用，则 ResolutionIncomplete

SuspicionLoad = Unknown
→ 不能默认 0
```

如果当前系统明确未启用 Wariness response family，可以显式 Disabled，不参加本路径。

Known zero 与 Disabled 语义不同。

## 9. 当前缺口

尚未闭合：

- `SuspicionLoad` 的生产 cue vocabulary；
- tackle visibility、entry disturbance、重复暴露、船 / 人为扰动等哪些事实具有 authority；
- 是否存在 species-specific 风险解释；
- `K_wary` effect-size budget；
- Wariness Bake 的上游 cause curves；
- 与 Defense / Investigation family 的 routing relation；
- controlled fixtures，确认 low prey support 与 high SuspicionLoad 不发生重复处罚。

在这些缺口闭合前，本页只冻结 owner 边界、numeric topology 与 hard/soft 权限。

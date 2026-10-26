# Proposal C｜SuspicionLoad Contract

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`SuspicionLoad` 只表达**当前 presentation 自身已解析出的风险 / 可疑证据**。

它不表达：

- 鱼当前有多警惕；那是 `Wariness`；
- 鱼当前有多想吃；那是 `FeedingMotivation`；
- presentation 对 prey interpretation 支持不足；那是 prey support；
- 当前追赶有多难；那是 Closing / Prediction；
- 全局 fishing pressure；优先作为 Wariness 的上游 cause，而不是再进入 SuspicionLoad。

当前 Response seam：

```text
current presentation risk cues
→ SuspicionLoad

Wariness × SuspicionLoad
→ RiskCost
```

## 2. 第一版只准入具名风险 cue

不允许直接造一个 `unnaturalness` 总分。

首版优先考虑两类与 prey support 较正交的 cue：

### TackleConspicuousness

表达终端连接 / 线 / 钩 / 其它已声明 tackle 事实对当前目标的可见或侵入程度。

它的意义是“目标旁边存在可疑的非猎物线索”，不是“目标不像猎物”。

当前仓内没有找到这类视觉 cue 的生产 Contract，因此这里先冻结语义，不假装 runtime 已有输入。

### EntryDisturbance

表达本次 presentation 进入局部区域时产生的、已解析的异常扰动，例如过强 splash / impact / noise。

它只使用有明确事件时间窗和量纲 / 归一化口径的事实；不能把“刚抛过来”本身自动当风险。

当前仓内同样没有完整生产 Contract，因此先保持输入缺口。

## 3. 首版不准入的内容

### 不使用 `1 - prey_support`

```text
low prey support
≠ automatically suspicious
```

目标不像某种 prey，只说明该 prey interpretation 支持不足；不等于鱼把它判断为危险。

### 不默认使用高速度 / 高频转向

这些事实已由 Closing、Prediction、StateTrigger 等路径消费。除非未来证明存在独立的风险语义，否则不能再以“动作太怪”为名重复处罚。

### 不把 fishing pressure 再塞进 SuspicionLoad

Fishing pressure 可以提高 `Wariness`。如果又同时提高 `SuspicionLoad`，同一原因会在 `Wariness × SuspicionLoad` 中被平方式放大。

### 不默认使用 repeated exposure

重复见到同一 lure / rig 属于 conditioning / history 问题。首版不决定它属于 Wariness Bake、独立 memory 还是 presentation-local risk；在 owner 闭合前不进入 SuspicionLoad。

## 4. Reducer

如果多个已准入 Suspicion cue 同时存在，首版倾向：

```text
SuspicionLoad = max(enabled resolved cue loads)
```

理由：这些 cue 首先作为“足以让当前 presentation 变得可疑”的替代证据；当前没有证据支持无条件求和或相乘。

因此：

```text
line visible = 0.6
entry disturbance = 0.4
→ SuspicionLoad = 0.6
```

这不是永久规则。只有 controlled fixture 证明“控制最强 cue 后，多 cue 仍有稳定额外 residual effect”，才准入累积 reducer。

## 5. Typed semantics

每个已启用 cue 必须区分：

```text
KnownZero
KnownPositive
Unknown
Disabled / NotApplicable
```

`Unknown` 不能当 0。

显式 Disabled / NotApplicable 不参加 max。

如果某 cue family 尚未进入产品能力范围，应标 Disabled / NotConfigured，而不是因为 runtime 没数据就伪装成 KnownZero。

## 6. 与 Wariness 的组合

第一版：

```text
RiskCost
= K_wary × Wariness × SuspicionLoad
```

所以：

```text
高 Wariness + 低 SuspicionLoad
→ 处罚仍低

低 Wariness + 高 SuspicionLoad
→ 处罚有限

高 Wariness + 高 SuspicionLoad
→ 处罚最大
```

这保留了“鱼侧状态 × presentation 风险”的交互，而不是给所有 presentation 一个统一钓压 penalty。

## 7. 当前数据缺口

当前仓内没有找到可以直接生产以下量的 Current Markdown Contract：

- tackle / line / hook receiver-side visibility；
- lure entry splash / noise / disturbance 的标准化风险读数；
- repeated-exposure / conditioning 的合法 owner。

因此本页不能声称 `SuspicionLoad` 已可生产。

在这些输入没有 authority 前，Wariness path 只能作为结构闭合，不应偷偷用现有 prey support、speed、prediction challenge 等变量代替。

## 8. 后续 admission gate

新增 Suspicion cue 必须回答：

1. 它对应什么明确的世界 / presentation 事实？
2. 为什么该事实表达风险，而不是 prey support、task difficulty 或 state trigger？
3. 是否已经在其它 path 结算同一后果？
4. 玩家是否能通过可理解的操作改变该 cue？
5. controlled fixture 控制已有变量后，它是否仍产生独立排序？

未通过这些问题的 cue 不进入生产 `SuspicionLoad`。

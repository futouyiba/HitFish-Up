# Proposal C｜Favorable Dwell Ownership Closure

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`favorable dwell` 不进入 Feeding `DecisionMargin`，也不新增 `DwellBonus`、`PauseDurationCoeff` 或同义 scalar。

如果两段呈现在当前评价时刻具有相同的：

- prey support；
- FoodValue；
- StateTriggerValue；
- ClosingCost；
- PredictionCost；
- Feeding Motivation；

但只是有利状态已经持续的时长不同，那么它们的**瞬时 Feeding response** 应相同。

更长 dwell 的优势是：有利状态存在得更久，因此累计提供更多潜在攻击机会。这个效应属于 temporal exposure / opportunity，不属于鱼此刻更想攻击。

## 2. 受控反例

比较：

```text
A：目标已在同一个有利状态停留 0.2 s
B：目标已在同一个有利状态停留 1.2 s
```

控制当前速度、位置关系、Closing、Prediction、FoodValue、Trigger、Motivation 全部相同。

若把 dwell duration 加入 `DecisionMargin`，B 会获得更高 `C`，等价于声称：

> 仅因为同一个有利状态已经持续得更久，这条鱼在当前瞬间就更愿意攻击。

当前没有独立机制支持这个结论。

更自然的解释是：

```text
instantaneous C 相同
×
有利状态持续更久
→
累计机会更多
```

可执行说明：`../../prototypes/lure-response/proposal_c_favorable_dwell_owner_probe.py`。

Probe 使用一个 hazard-style exposure 公式只为展示 topology：相同 `C` 下，更长 duration 可以得到更高 cumulative opportunity。该公式不是 Production Contract。

## 3. 与 pause 的关系

pause 仍可通过已存在的独立因果路径改变 Feeding response：

```text
pause
├→ lure speed 下降
│   → ClosingCost 下降
│
├→ 一段时间内没有新的 abrupt redirection
│   → PredictionChallenge 自然恢复
│   → PredictionCost 下降
│
└→ prey-conditioned state/process interpretation 改变
    → 若有独立证据，可改变 StateTriggerValue
```

这些后果已经足以让 pause 改变瞬时 `C`。

不能再增加：

```text
pause duration
→ favorable dwell bonus
→ DecisionMargin 再加一次
```

否则同一个 pause 会被重复奖励。

## 4. 时间持续仍然重要，但 Owner 不在 Feeding scalar

本轮并不裁定“持续时间没有玩法价值”。相反，更长有利状态很可能提高玩家最终获得攻击机会的累计概率。

但这个问题属于：

```text
resolved response state
×
temporal exposure / opportunity support
→ cumulative opportunity
```

而不是：

```text
longer duration
→ fish-side instantaneous value increases
```

当前仓内 `main` 没有找到已承接 temporal support / exposure integration 的 Current Markdown Contract。因此这里记录的是一个明确缺口：

> Feeding 不接管该缺口；Opportunity / temporal exposure 的 Owner 需要后续单独登记或闭合。

在 Owner 未闭合前，不用 `PauseDurationBonus` 临时填洞。

## 5. 哪些 duration 仍可以合法进入 Feeding

只有 duration 改变了另一项已定义语义时，才通过那项语义进入 Feeding。

例如：

- recent turn age 改变 `PredictionChallenge`；
- 某个 prey-specific process 要求“挣扎持续至少 X 秒”，duration 参与 state interpretation；
- attention / perceptual history 有明确保持或衰减规则，duration 改变 Perception state；
- current movement segment duration 参与某个已准入的 cadence/state rule。

这时 duration 是**上游事实**，不是通用“待得久就更好”的 bonus。

## 6. 对 Cadence 的影响

这次裁定进一步缩小了 Cadence 的准入空间。

未来若要证明 `jerk → jerk → pause` 本身存在独立 cadence effect，必须控制：

- current speed / Closing；
- PredictionChallenge；
- prey-conditioned state trigger；
- attention / perceptual history；
- total favorable exposure；
- Feeding Motivation。

只有在这些都相同后，sequence motif 仍产生稳定、可学习的 ranking difference，才有资格新增 cadence valuation。

否则 cadence 只是已有路径的组合描述。

## 7. 当前 Working 边界

准入 Feeding numeric core：

```text
FoodValue
+ StateTriggerValue
- ClosingCost(theta)
- PredictionCost
- WillingnessThreshold(Motivation)
```

不准入 Feeding numeric core：

- `DwellBonus`；
- `PauseDurationCoeff`；
- generic favorable-window bonus；
- 为补 temporal integration 缺口而临时提高 `C`。

OPEN：

- Opportunity / temporal exposure 的 Current Owner；
- cumulative opportunity 的 Production operator；
- cadence motif 是否存在独立 residual effect。

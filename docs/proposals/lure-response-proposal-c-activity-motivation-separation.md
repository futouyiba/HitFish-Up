# Proposal C｜活性与摄食意愿的职责分离

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

为了避免 `Activity` 与 `FeedingMotivation` 都退化成“鱼现在积极不积极”，第一版把两者拆成两个正交问题：

```text
FeedingMotivation
→ 为了食物出手，需要多强的理由？
→ 移动基础出手门槛

Activity
→ 为了追赶这个具体目标，运动投入有多难接受？
→ 调制追赶负担
```

因此主体保持：

```text
DecisionMargin
= FoodValue
+ TriggerValue
- ClosingCost(Activity, relative speed, geometry)
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

## 2. 最重要的判别测试

如果目标几乎不需要追赶：

```text
ClosingLoad ≈ 0
```

那么：

```text
Activity 高 / 低
→ 应几乎不改变 Response
```

但：

```text
FeedingMotivation 高 / 低
→ 仍会明显改变是否出手
```

这就是两者最清楚的边界。

反过来，在目标高速远离、需要主动追赶时：

```text
ClosingLoad ↑
→ Activity 差异被放大
```

而 FeedingMotivation 仍主要通过门槛作用，不直接改变追赶负担。

## 3. 四格反例

### 高 Activity + 低 FeedingMotivation

```text
鱼不排斥高强度追赶
但普通食物仍不值得出手
```

玩家含义：

- 快速搜索仍可行；
- 但普通稳定呈现可能鱼口差；
- 合法攻击诱因或更高食物价值可能使其跨线。

### 低 Activity + 高 FeedingMotivation

```text
鱼很想吃
但不愿为了高速目标付出大追赶代价
```

玩家含义：

- 慢速、近身、停顿呈现受益；
- 高食物价值不能无限抵消过高追赶负担。

### 高 Activity + 高 FeedingMotivation

```text
既愿意追，也容易因为食物出手
```

通常是积极鱼情，允许更主动、更高覆盖率打法。

### 低 Activity + 低 FeedingMotivation

```text
既不愿追，也需要更强理由才出手
```

整体困难，但不应通过把两个变量合成同一个倍率来表达。

## 4. 数学上的正交性

建议保留结构：

```text
ClosingCost
= BaseClosingCost(q, theta)
  × ActivityCostMultiplier(A)

DecisionMargin
= PositiveValue
- ClosingCost
- RiskCost
- Threshold(M)
```

这样：

```text
当 BaseClosingCost → 0：
Activity 的边际影响 → 0
```

而：

```text
Threshold(M)
```

仍然存在。

这比让 Activity 直接改变全局 Response 或让 FeedingMotivation 去缩放 Closing 更容易解释和标定。

## 5. 不建议用“愿不愿意追”作为 Activity 的最终定义

“愿不愿意”容易与 FeedingMotivation 混淆。

更精确的 Response 侧语义是：

> `Activity` 表示鱼对主动运动投入 / 追赶负担的容忍程度。

因此它不是：

- 对食物的欲望；
- 一般攻击性；
- 物理极速；
- 是否能进食。

它只回答：

> 同样的追赶负荷，对当前这条鱼来说有多贵？

## 6. 与物理能力的边界

鱼种 / 体型决定基础追赶能力：

```text
Species / Size
→ InterceptSpeedLimit
```

若未来要表达低温、缺氧、疲劳等对真实运动能力的降低，应走独立的生理能力修正：

```text
BaseInterceptSpeed
× PhysiologicalCapacityModifier
→ EffectiveInterceptSpeedLimit
```

`Activity` 不直接替代该修正。

重要护栏：

如果同一个上游原因同时降低 Activity 和 PhysiologicalCapacity，必须证明两条效果确实不同；否则会重复惩罚。

## 7. Activity 倍率的标定方式

不要先问：

```text
K_activity 应该是 0.8 还是 1.2？
```

更好的标定问题是玩家策略交叉点：

> 对一条 GeneralClosing 鱼，在低 / 中 / 高 Activity 下，什么 retrieve speed 开始让快速搜索明显失去单次机会优势？

先定义体验锚：

```text
低 Activity
→ Normal 到 Fast 区间应出现明显 Response 损失

中 Activity
→ Normal 可接受，Fast 有可见代价

高 Activity
→ Fast 仍可接受，但 Burst 不应免费
```

再反推 `ActivityCostMultiplier` 的幅度。

因此当前：

```text
ActivityCostMultiplier(A)
= 1 + K_activity * (A_ref - A)
```

只保留为最小曲线族，不把 `K_activity=1` 视为产品决定。

## 8. 当前 Working 裁定

保留：

```text
Activity
→ 追赶负担敏感度

FeedingMotivation
→ 摄食出手门槛

Species / Size / physiological capacity
→ 追赶能力
```

这三条分别购买：

```text
能不能追
追起来有多贵
值不值得为了吃而出手
```

后续回归优先使用这三个问题检查职责，不再用模糊的“活跃程度”解释它们。

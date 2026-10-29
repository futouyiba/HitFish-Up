# Proposal C｜活性如何调制追赶负担

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

第一版把 `Activity` 解释为：

> 当前这条鱼愿意为主动追赶付出多少行为代价。

它**不修改鱼的物理极速**，也不再生成第二套速度阈值。

追赶负担继续由目标相对速度与鱼种 / 体型对应的追赶能力决定，`Activity` 只调制这个负担的大小：

```text
相对追赶速度 q
→ 基础追赶负担

Activity
→ 追赶负担倍率

两者结合
→ 最终追赶负担
```

因此第一版保持：

```text
u_close(theta)
= max(0, q * cos(theta))

ClosingCost(theta)
= K_close
  * u_close(theta)^2
  * ActivityCostMultiplier(Activity)
```

其中 `InterceptSpeedLimit` 继续只表达鱼种 / size cohort 的追赶能力，不受 Activity 修改。

---

## 2. 为什么 Activity 不应修改追赶速度上限

如果直接写成：

```text
EffectiveInterceptSpeed
= InterceptSpeedLimit * f(Activity)
```

会把“当前不积极”与“物理上游不动”混成同一件事。

这样低 Activity 会像鱼突然失去运动能力，并且会破坏现有分工：

```text
Species / Size
→ 能追多快

Activity
→ 愿不愿意为追赶付出代价
```

第一版需要购买的玩家策略不是“低活性鱼绝对追不上”，而是：

```text
同样一个快速移动的目标
高活性鱼 → 更容易觉得值得追
低活性鱼 → 更容易觉得不值得追
```

所以 Activity 进入 soft cost，而不是 physical hard limit。

---

## 3. 为什么 Activity 应该乘在追赶负担上

Activity 的策略作用应随追赶难度自动变化。

慢速目标本身几乎不需要主动追赶：

```text
基础追赶负担低
× Activity multiplier
→ 活性差异仍然小
```

快速目标需要更强主动追赶：

```text
基础追赶负担高
× Activity multiplier
→ 活性差异自然放大
```

这正好购买目标体验：

```text
慢速 finesse
→ 各 Activity 都相对可接受

快速搜索
→ 高 Activity 更能承受
→ 低 Activity 明显受损
```

因此不需要额外再写：

```text
if Activity low and speed fast:
    extra fast penalty
```

已有 `q^2 × ActivityMultiplier` 已经自然产生交互。

---

## 4. 第一版倍率形状

首版优先使用最简单的线性倍率：

```text
ActivityCostMultiplier(A)
= 1 + K_activity * (A_ref - A)
```

Working：

```text
A ∈ [0,1]
A_ref = 0.5
K_activity = 1.0  # calibration seed
```

得到：

```text
A = 0.0 → multiplier = 1.5
A = 0.2 → multiplier = 1.3
A = 0.5 → multiplier = 1.0
A = 0.8 → multiplier = 0.7
A = 1.0 → multiplier = 0.5
```

这些只是结构测试用 seed，不是生产数值。

当前没有证据需要 sigmoid、指数、soft gate 或额外 Activity threshold。

如果生产回归显示极低 / 极高 Activity 需要更明显差异，再调整 `K_activity` 或重开曲线族。

---

## 5. 为什么不让 Activity=0 直接归零响应

`Activity=0` 当前只表示最低端的主动追赶意愿 / 活跃状态，不等于：

```text
不能进食
不能移动
不能伏击
```

因此：

```text
低 Activity + 很慢 / 很近的目标
→ 仍然可能响应
```

这对 finesse 很重要。

如果未来存在真正的休眠、失能、强生理抑制等 hard state，应由独立类型化状态承接，不能把 Activity 数值端点偷换成硬关闭。

---

## 6. 与摄食意愿的边界

两者不能合并。

```text
Activity
→ 追这个目标要付出的行动代价有多难接受

FeedingMotivation
→ 当前需要多强的摄食理由才愿意出手
```

典型反例：

```text
高 Activity + 低 FeedingMotivation
→ 鱼有能力 / 有活跃性快速追
→ 但普通食物仍可能不值得出手
→ 强合法攻击诱因可能翻转
```

反过来：

```text
低 Activity + 高 FeedingMotivation
→ 很想吃
→ 但高速目标追起来仍然不划算
→ 慢速呈现显著受益
```

这两个组合正是保留两个变量的价值。

---

## 7. 与快速搜索收益的边界

Activity 只影响 Response 内的追赶负担。

它不负责给快速搜索增加正收益。

完整策略仍是：

```text
快速 retrieve
→ 单次局部机会的追赶负担可能上升

同时
→ 单位时间覆盖水体更多
→ 获得更多空间 / 鱼位信息与 encounter opportunity
```

因此最终“快速搜索是否划算”必须在：

```text
单次机会 Response
× Opportunity / exposure
× Spatial coverage rate
```

联合层判断。

不能为了让高 Activity 快速搜索显得有优势，就在 Activity 或 Response 里额外增加速度奖励。

---

## 8. 数值结构探针

为只检查结构，使用：

```text
K_close = 0.76
FoodValue = 0.70  # Good
FeedingMotivation = 0.5
WillingnessThreshold = 0.40
Trigger = 0
Risk = 0
ResponseProjection M1 = 0.40
```

使用 Working：

```text
ActivityCostMultiplier(A)
= 1 + (0.5 - A)
```

先看不乘 `K_close` 的相对追赶负担：

| q | A=0.2 | A=0.5 | A=0.8 |
|---:|---:|---:|---:|
| 0.4 | 0.208 | 0.160 | 0.112 |
| 0.7 | 0.637 | 0.490 | 0.343 |
| 1.0 | 1.300 | 1.000 | 0.700 |

这说明同一 Activity 差异在低 q 时影响较小，在高 q 时自然变得重要。

对 GeneralClosing Working q basket 做 Isotropic2D bearing 数值积分，得到 Good 的 conditional response 近似：

| q | 低 Activity 0.2 | 中 Activity 0.5 | 高 Activity 0.8 |
|---:|---:|---:|---:|
| 0.325 | 0.685 | 0.700 | 0.715 |
| 0.650 | 0.523 | 0.552 | 0.610 |
| 0.975 | 0.468 | 0.483 | 0.507 |
| 1.300 | 0.444 | 0.454 | 0.470 |

这些数值不是目标 retention，只说明：

- 慢速时 Activity 差异小；
- 中高速时 Activity 能改变排序；
- 极高速时 Closing 的 latent-bearing 结构地板会压缩差异，不能靠提高 Activity leverage 修复。

完整高速体验仍需 Opportunity / coverage 联合回归。

---

## 9. 当前 Working 护栏

第一版要求：

1. 同一 presentation 下，高 Activity 的追赶负担不得高于低 Activity；
2. Activity 对慢速 presentation 的影响应明显小于对高速 presentation 的影响；
3. 低 Activity 不应让慢速 / 近身 presentation 普遍归零；
4. 高 Activity 不应消除高速本身的追赶负担；
5. Activity 不修改 `InterceptSpeedLimit`；
6. Activity 不降低摄食门槛，不修改 FoodValue，也不直接改变风险顾虑；
7. 不新增匿名 `FastBonus` / `LowActivityPenalty`。

---

## 10. 当前裁定

第一版暂定：

```text
q
= lure radial separation speed
  / InterceptSpeedLimit

u_close(theta)
= max(0, q * cos(theta))

ActivityCostMultiplier(A)
= 1 + K_activity * (0.5 - A)

ClosingCost(theta)
= K_close
  * u_close(theta)^2
  * ActivityCostMultiplier(A)
```

其中：

```text
K_activity = 1.0
```

只作为 Working calibration seed。

真正需要生产验证的是策略排序：

```text
低 Activity
→ 快速呈现相对更差
→ 慢速 / finesse 相对受益

高 Activity
→ 能承受更高 retrieve speed
→ 快速搜索的 Response 代价缩小
```

是否最终值得快速搜索，还要与单位时间机会生成率和覆盖率联合判断。

本页只闭合 Response 内的 Activity → ClosingCost 关系，不修改 Activity 上游定义或生产文档。

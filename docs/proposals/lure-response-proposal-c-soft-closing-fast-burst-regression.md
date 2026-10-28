# Proposal C｜纯 Soft Closing 的 Fast / Burst 回归

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

撤掉 `u_close >= 1 → hard-zero` 后，纯 soft Closing 仍能形成稳定的速度排序，但它**不能也不应该单独承担完整的高速惩罚**。

核心原因不是 `K_close` 太小，而是 Horizontal Isotropic2D 的结构性质：

```text
u_close(theta) = max(0, q * cos(theta))
```

约一半 latent bearing 满足：

```text
cos(theta) <= 0
→ u_close = 0
→ ClosingCost = 0
```

这些方向代表拟饵当前没有沿径向远离潜在鱼。

因此当 `q → ∞` 时，单靠 Closing 的平均 response 仍存在约 `0.5` 的迎面方向地板。继续增大 `K_close` 不能消除这个结构地板，只会进一步处罚背离方向。

这不是公式 bug，而是职责边界：

```text
Closing
→ 当前运动是否把已有机会沿径向带离鱼

Opportunity / temporal exposure
→ 当前 presentation 在局部可交互区域中留下多少有效接触窗口
```

高速 presentation 的完整系统效果必须由两者共同形成。

---

## 2. 回归基线

本轮只隔离 Closing，不加入 Prediction / Risk / Trigger。

Working：

```text
K_close = 0.76
ActivityCostMultiplier = 1
FeedingMotivation = 0.5
threshold = 0.40
ResponseProjection M1 = 0.30
```

FoodValue：

```text
Good      = 0.70
Preferred = 1.00
```

因此 Closing 前 margin：

```text
Good      = 0.30
Preferred = 0.60
```

Working q basket：

| Locomotor profile | Slow | Normal | Fast | Burst |
|---|---:|---:|---:|---:|
| HighClosing | 0.225 | 0.450 | 0.675 | 0.900 |
| GeneralClosing | 0.325 | 0.650 | 0.975 | 1.300 |
| LowClosing | 0.450 | 0.900 | 1.350 | 1.800 |

这些仍是 calibration seed。

---

## 3. 纯 Closing 的平均响应

对 Isotropic2D bearing 数值积分，得到近似：

### Good

| Profile | Slow | Normal | Fast | Burst |
|---|---:|---:|---:|---:|
| HighClosing | 0.968 | 0.872 | 0.724 | 0.657 |
| GeneralClosing | 0.933 | 0.736 | 0.643 | 0.605 |
| LowClosing | 0.872 | 0.657 | 0.601 | 0.575 |

### Preferred

| Profile | Slow | Normal | Fast | Burst |
|---|---:|---:|---:|---:|
| HighClosing | 1.000 | 1.000 | 0.988 | 0.832 |
| GeneralClosing | 1.000 | 0.996 | 0.791 | 0.701 |
| LowClosing | 1.000 | 0.832 | 0.693 | 0.640 |

这些数字只用于结构回归，不是生产 retention 目标。

---

## 4. 回归说明了什么

### 4.1 速度排序仍存在

对同一 profile：

```text
Slow > Normal > Fast > Burst
```

仍然成立。

所以撤掉 hard-zero 没有让 Closing 失去速度敏感性。

### 4.2 locomotor profile 排序仍存在

同一速度 regime 下，整体仍保持：

```text
HighClosing > GeneralClosing > LowClosing
```

因此 `InterceptSpeedLimit` 仍购买了鱼种 / size cohort 的 Closing 差异。

### 4.3 高速差异会逐渐压缩

例如 Good：

```text
Fast:
High    ≈ 0.724
General ≈ 0.643
Low     ≈ 0.601

Burst:
High    ≈ 0.657
General ≈ 0.605
Low     ≈ 0.575
```

随着 q 增大，平均值逐渐靠近约 `0.5` 的结构地板。

这意味着不能期待单靠 Closing 在极高速区继续无限拉开差异。

---

## 5. 为什么存在约 0.5 的地板

当：

```text
cos(theta) <= 0
```

拟饵当前正在朝潜在鱼接近，或至少没有沿径向离开鱼。

第一版 Closing 的问题是：

> lure motion 正在多强地扩大鱼与目标的径向距离？

所以这些方向得到：

```text
ClosingCost = 0
```

是正确的。

当 q 极大时，背离方向可以被 soft cost 压到 `C≈0`，但迎面方向仍可保留高 conditional response。

因此：

```text
E_theta[C]
```

不会仅靠 Closing 收敛到 0。

如果为了消除地板而加入：

```text
abs(speed) generic penalty
TangentialPenalty
VerticalClosingPenalty
```

就会重新破坏 feature ownership，并把没有几何依据的惩罚塞回 Response。

---

## 6. 高速的另一半代价属于 Opportunity

迎面高速并不意味着玩家可以无限免费获得高 response。

高速目标即使在某一瞬间：

```text
ClosingCost ≈ 0
C_conditional high
```

也可能因为快速穿过有效 interaction region，使：

```text
eligible opportunity duration ↓
```

从而：

```text
accumulated opportunity ↓
```

所以完整链应理解为：

```text
receding / escaping geometry
→ ClosingCost ↑
→ instantaneous C ↓
```

同时：

```text
high transit speed through local opportunity
→ effective opportunity window ↓
→ accumulated opportunity ↓
```

现有姿态颗粒机会机制应承接后一条，不在 DecisionMargin 新增 `FastPenalty`。

---

## 7. 对 Fast Search 的含义

高速 retrieve 还可能带来相反收益：

```text
单位时间覆盖更多空间 / encounter 更多候选区域
```

因此系统层不是简单的：

```text
faster = worse
```

而是：

```text
per-local-opportunity retention
× local exposure window
× search / coverage rate
```

共同决定单位时间收益。

这正是把 Response、Opportunity、Spatial coverage 分开的价值。

Closing 不应该为了保证“高速一定差”而侵占另外两层。

---

## 8. Calibration 裁定

不要因为 Fast / Burst 的平均 `C` 没有降到足够低，就直接提高 `K_close`。

`K_close` 应主要标定：

```text
同一个局部 opportunity 内
不同 radial separation load
→ conditional response 差多少
```

而不是标定：

```text
整段 retrieve 最终中鱼效率差多少
```

后者必须等 Opportunity / coverage 一起进入整链回归。

因此旧目标：

```text
Fast / Burst 必须仅靠 Closing 大量归零
```

撤回。

---

## 9. 下一步整链 regression

需要在现有姿态颗粒机会机制上验证至少四组：

1. Slow / Normal / Fast / Burst 的最终 accumulated opportunity ordering；
2. HighClosing / GeneralClosing / LowClosing 在相同 presentation 下是否保持可学习差异；
3. 高速迎面 case 是否表现为高瞬时 C + 短 opportunity window，而不是匿名 speed penalty；
4. Fast Search 是否能在降低单次局部效率的同时，通过更高 coverage 保留策略价值。

这些属于 Response × Opportunity × Spatial 的联合回归，不再由 Closing 单独承担。

---

## 10. 当前裁定

第一版继续保留：

```text
u_close(theta)
= max(0, q * cos(theta))

ClosingCost(theta)
= K_close * u_close(theta)^2
  * ActivityCostMultiplier(Activity)
```

并接受它的结构性质：

```text
Closing alone
≠ complete speed effect
```

不新增 generic FastPenalty，不恢复 `u_close>=1` hard-zero，不为了消除约 0.5 地板引入无 owner 的 tangential / vertical penalty。

Fast / Burst 的完整效果必须在 Opportunity 与 Spatial coverage 接入后联合验证。

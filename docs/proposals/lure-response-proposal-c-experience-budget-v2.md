# 方案 C｜Feeding Response Experience Budget v2

日期：2026-10-26  
状态：Working Calibration Hypothesis，非 Current，非生产参数。

## 1. 本轮目标

上一轮已经建立：

```text
玩家体验目标
→ 反推 C_mode
→ 再反推 TaskCost / Motivation Threshold / Response Curve
```

本轮不先调公式，而先攻击体验预算本身。

三个最重要的问题：

1. 差鱼口时，slow / pause 对 fast retrieve 的“救回”应该有多强；
2. 正常鱼口时，fast retrieve 相比 reference-good 应损失多少；
3. 好鱼口时，fast retrieve 应恢复到 reference-good 的多少。

## 2. 钓鱼策略证据支持什么

现有钓鱼策略资料稳定支持以下方向：

- 冷水、低活性、鱼不愿追时，明显放慢 cadence、延长 pause 是常见且关键的调整；有时 pause 可延长到数秒乃至几十秒；
- 条件正常时，brisk jerk-jerk-pause 本身就是常见起手法，不应该天然受到很重惩罚；
- 鱼积极摄食时，快速、激进的 presentation 仍可工作，甚至很多不同 retrieve 都能获得咬口。

这些证据支持“量级分层”，但不直接给出游戏里的 C_mode 数字。因此以下目标用区间表达，不冒充现实测量值。

## 3. Working Experience Budget v2

仍沿用 Candidate Calibration 的 reference anchor：

```text
reference-good C = 1
reference target active-roll time = 30 normalized seconds
```

在该 reference basket 的 underfilled fixture 中：

```text
T_target ≈ 30 / C
```

因此可以把体验区间先写成 C 区间，再换算成 normalized active-roll target time。

| Story | Working C 区间 | 对应 target active-roll time | 设计含义 |
|---|---:|---:|---|
| 差鱼口 + fast | 0.15–0.25 | 120–200s | 基本失效，但不是物理 Infeasible |
| 差鱼口 + slow / pause 后 | 0.50–0.65 | 46–60s | 明显救回，效率约为 fast 的 2–4 倍 |
| 正常鱼口 + fast | 0.75–0.85 | 35–40s | 有竞争力，只比 reference-good 略差 |
| 正常鱼口 + reference-good | 0.95–1.00 | 30–32s | 基准强响应 |
| 好鱼口 + fast | 0.90–1.00 | 30–33s | 基本恢复到 reference-good |
| species × size cohort / InterceptSpeedLimit 过高的 fast case | 0.25–0.35 | 86–120s | Closing 超过 hard limit 时不可行；Activity 不改变该边界 |
| 低 Activity + physically-feasible slow | 0.85–0.95 | 32–35s | Activity 只增加可行 Closing 的 soft cost，不改变 `InterceptSpeedLimit` |

这些值是 Working Experience Budget，不是 Production calibration。

## 4. 为什么“弱鱼 + slow”必须高于“正常鱼 + fast”

如果两者 Food Value 与 Motivation 相同，而且：

```text
low Activity + slow     → physically-feasible Closing，soft cost higher
species × size cohort   → InterceptSpeedLimit
```

那么前者必须具有不低于后者的 C_mode。

否则等于物理 hard feasibility 与 Activity soft cost 被重复或错误合并；`InterceptSpeedLimit` 只负责 Closing 是否可行，Activity 只影响可行 Closing 的 soft cost。

因此体验预算本身也必须服从：

```text
same Value + same Motivation
lower Closing demand / Activity soft cost
→ C_mode 不得更低
```

这类检查应先于任何公式拟合。

## 5. 对当前简单 threshold family 的重新评价

继续测试：

```text
TaskCost = k × physically-feasible task consequence^p
Threshold = b - c × Motivation
Margin = FoodValue - TaskCost - Threshold
C_mode = clamp(Margin / r, 0, 1)^gamma
```

用本轮预算中点做诊断拟合后，一组可行参数约为：

```text
k     ≈ 0.47
p     ≈ 4.0
b     ≈ 0.75
c     ≈ 0.40
r     ≈ 0.34
gamma ≈ 0.89
```

这组数字不是生产候选。真正值得注意的是：

> 最优诊断会把 `TaskCost` 推向明显凸曲线。

也就是：

```text
低 / 中 physically-feasible task consequence
→ 成本上升较慢

接近 `InterceptSpeedLimit` 的可行边界
→ 成本快速上升
```

这恰好能同时满足：

- 正常鱼口下 fast retrieve 仍有竞争力；
- 差鱼口或弱能力时 demanding presentation 明显掉下去；
- slowdown / pause 只要实质降低 Closing demand 或可行 Closing 的 Activity soft cost，就能产生明显 rescue；
- 真正 Infeasible 仍由 hard gate 归零。

## 6. 本轮修正了上一轮的一个判断

上一轮因为一组体验目标拟合不佳，曾怀疑：

```text
Motivation → Threshold
```

的线性关系可能过于简单。

本轮发现，之前的部分困难来自体验目标自身不一致，例如同 Value / Motivation 下反而要求较低 physically-feasible task consequence 得到更低 C。

修正预算后，简单线性 Threshold 已能与目标相当接近。

因此当前更稳妥的结论是：

- **暂不需要为了拟合而增加 nonlinear Motivation curve；**
- **优先继续验证强凸 TaskCost 是否是稳定需求；**
- 只有在更多 reference stories 证明 linear Threshold 无法同时满足策略目标时，再购买额外自由度。

## 7. 下一步

下一轮应把同一 Experience Budget 扩展到不同 Target Relation / Food Value：

```text
Preferred / high-value prey
Good / normal prey
Marginal prey
```

重点检查：

1. 高 Motivation 是否会让普通 prey 进入可接受区域，但不会让明显低价值 prey 全部变成满响应；
2. 高 Value 是否能补偿一部分 Constrained Task，但不会穿透 Infeasible；
3. `FoodValue` 与 `Motivation` 是否继续表现出不同的策略作用，而不是又被拟合成近似对称；
4. 强凸 TaskCost 是否会导致中等 strain 区过于平坦，使玩家操作差异不够敏感。

可执行 probe：`../../prototypes/lure-response/proposal_c_experience_budget_v2_probe.py`。

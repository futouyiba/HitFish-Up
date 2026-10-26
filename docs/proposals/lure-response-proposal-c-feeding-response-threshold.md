# 方案 C｜Feeding Response 计算结构：阈值模型 Working Probe

日期：2026-10-26  
状态：Working Hypothesis / Probe，非 Current，非生产参数。

## 1. 问题

Complete Feeding Response Mode 已收敛到最小输入：

- Target / Food Value；
- Feeding Motivation；
- TaskAffordance / TaskStrain；
- Resolution / Mode Validity。

本轮不再扩语义层，只攻击：`C_mode` 到底应如何从这些输入计算。

可执行 probe：`../../prototypes/lure-response/proposal_c_feeding_response_threshold_probe.py`。

## 2. 先拒绝一个过早的默认公式

最直接的写法是：

```text
Drive = FoodValue × Motivation
C_mode = f(Drive, TaskCost)
```

它有一个严重副作用：`FoodValue` 与 `Motivation` 被做成完全对称。

例如：

```text
FoodValue=1.0, Motivation=0.4
FoodValue=0.4, Motivation=1.0
```

两者都会得到 `Drive=0.4`。

但它们的领域含义不同：

- 前者是“猎物非常合口，但当前鱼口差”；
- 后者是“鱼口很好，但这个猎物本身只是一般”。

当前没有证据或设计理由要求两者恒等，因此不把 `V×M` 提升为 production formula。

## 3. Working Hypothesis：Motivation 改变出手门槛

更自然的结构是：

```text
Food Value
- Task Cost
- Willingness Threshold(Motivation)
= Decision Margin

Decision Margin
→ Response Curve
→ C_mode
```

大白话：

> 鱼口越好，越愿意接受普通一点、难一点的捕食机会；鱼口越差，只有特别合口、特别省力的目标才值得出手。

Motivation 因而不是一个最终 bonus，也不是给 Food Value 打折，而是改变“值不值得发起捕食行为”的 reservation threshold。

## 4. Task 侧

TaskAffordance 的 categorical label 继续保留：

```text
Feasible | Constrained | Infeasible | Unknown
```

但连续计算建议消费一个 derived `TaskStrain`：

```text
0   = 很轻松
1   = 接近当前能力边界
>1  = Infeasible
```

`TaskStrain > 1` 是 hard gate，不允许再被高 Food Value 或高 Motivation 补回来。

第一版 TaskCost 只需要满足：

- 随 TaskStrain 单调上升；
- 低 strain 成本较小；
- 接近能力边界时成本明显增加。

probe 暂用：

```text
TaskCost = 0.45 × TaskStrain^1.6
```

这里只验证拓扑，不是生产标定。

## 5. Probe 使用的临时公式

```text
Threshold(M) = 0.90 - 0.80 × M

Margin = FoodValue - TaskCost - Threshold(M)

C_mode = clamp(Margin / 0.45, 0, 1)
```

并保留 typed gates：

```text
ResolutionIncomplete → no scalar
ModeInvalid          → 0
TaskStrain > 1       → 0
FoodValue <= 0       → 0
Motivation <= 0      → 0
```

所有数字只用于观察二维/三维响应面的性质。

## 6. 数值表：Motivation 改变可接受机会区域

列是 `FoodValue`，行是 `TaskStrain`。

### Motivation = 0.3｜鱼口差

| TaskStrain \\ FoodValue | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |
|---:|---:|---:|---:|---:|---:|
| 0.2 | 0.00 | 0.00 | 0.00 | 0.23 | 0.68 |
| 0.4 | 0.00 | 0.00 | 0.00 | 0.08 | 0.52 |
| 0.6 | 0.00 | 0.00 | 0.00 | 0.00 | 0.31 |
| 0.8 | 0.00 | 0.00 | 0.00 | 0.00 | 0.06 |
| 1.0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

策略故事：鱼口差时，大量普通机会直接不值得出手；高价值、低任务成本的 presentation 仍有明显优势。

### Motivation = 0.6｜正常鱼口

| TaskStrain \\ FoodValue | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |
|---:|---:|---:|---:|---:|---:|
| 0.2 | 0.00 | 0.00 | 0.32 | 0.77 | 1.00 |
| 0.4 | 0.00 | 0.00 | 0.17 | 0.61 | 1.00 |
| 0.6 | 0.00 | 0.00 | 0.00 | 0.40 | 0.85 |
| 0.8 | 0.00 | 0.00 | 0.00 | 0.14 | 0.59 |
| 1.0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.29 |

### Motivation = 0.9｜鱼口好

| TaskStrain \\ FoodValue | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |
|---:|---:|---:|---:|---:|---:|
| 0.2 | 0.00 | 0.41 | 0.86 | 1.00 | 1.00 |
| 0.4 | 0.00 | 0.26 | 0.70 | 1.00 | 1.00 |
| 0.6 | 0.00 | 0.05 | 0.49 | 0.94 | 1.00 |
| 0.8 | 0.00 | 0.00 | 0.23 | 0.68 | 1.00 |
| 1.0 | 0.00 | 0.00 | 0.00 | 0.38 | 0.82 |

策略故事：鱼口好时，可接受机会区域扩张，普通 prey / 较高 task strain 也开始产生响应；但真正 Infeasible 仍然不能突破。

## 7. 当前最有价值的性质

### 7.1 Motivation 是“扩张捕食窗口”

它不是简单让所有 response 同比例放大。

```text
低 Motivation
→ 只有高 Value + 低 Cost 才过门槛

高 Motivation
→ 更多 Value / Cost 组合进入可响应区域
```

这自然形成“鱼口好时什么都更敢追，鱼口差时要把饵送到嘴边、还得特别合口”的玩法故事。

### 7.2 Value 与 Motivation 不再被强迫对称

临时参数下，同样 `V×M=0.4` 的两个案例：

```text
V=1.0, M=0.4, strain=0.4 → C≈0.70
V=0.4, M=1.0, strain=0.4 → C≈0.44
```

这个差异不是当前结论本身；重要的是模型允许二者不同，而不被公式结构强制相等。

### 7.3 高价值可以补偿“有点难”，不能补偿“不可能”

```text
Constrained
→ 作为 cost，可被高 Food Value / 高 Motivation 部分补偿

Infeasible
→ hard gate，C_mode=0
```

这符合当前 TaskAffordance 的语义边界。

## 8. 与 Current 的关系

Natural Bite Readiness Current v9 明确：

- Motivation 是 Complete Response Mode 的原因与输入，不是最终 bonus；
- 不建立 universal globalAvailability multiplier；
- mode-specific soft motivation effect 在 Interaction 内结算。

Interaction / Capture Current v15 也只要求 Complete Mode 独立闭合 `Perception / Interpretation + Valuation / Motivation / Risk / Cost + TaskAffordance → C_mode`，并未冻结乘法结构。

因此“Motivation 改 threshold”的模型与 Current ownership 相容，但目前仍只是 Proposal C 的 Working Hypothesis。

## 9. 当前 Working Conclusion

第一版优先研究：

```text
FoodValue
- TaskCost(TaskStrain)
- WillingnessThreshold(Motivation)
→ DecisionMargin
→ ResponseCurve
→ C_mode
```

而不是：

```text
FoodValue × Motivation × AffordanceCoeff
```

当前需要标定/验证的核心自由度因此缩小为：

1. `FoodValue` 的实际尺度与 reference anchors；
2. `TaskStrain → TaskCost` 的曲线形状；
3. `Motivation → WillingnessThreshold` 的曲线形状；
4. `DecisionMargin → C_mode` 的 response curve。

## 10. 下一轮应该攻击什么

下一步不再调随机参数，而应拿具体策略故事做约束：

- 大口黑鲈，正常鱼口，标准 baitfish jerkbait；
- 慢速好抓 vs 快速逃逸；
- 高价值 baitfish vs 低匹配 prey；
- 鱼口差时 pause / slower retrieve 是否能通过降低 TaskCost 把 response 拉回；
- 鱼口好时 aggressive retrieve 是否应该从不可接受变成可接受；
- 同一 presentation 对不同 FunctionalCapacity 的鱼是否产生预期翻转。

先把这些 qualitative ordering / reversal 写成验收矩阵，再反推四条曲线，而不是先凭手感定生产参数。

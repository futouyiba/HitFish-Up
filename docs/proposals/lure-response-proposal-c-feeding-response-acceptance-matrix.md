# 方案 C｜Feeding Response 验收矩阵

日期：2026-10-26  
状态：Working Acceptance Matrix，非 Current，非生产参数。

## 1. 为什么先写验收，不继续调公式

当前 Working Hypothesis 已能形成：

```text
FoodValue
- TaskCost(TaskStrain)
- WillingnessThreshold(Motivation)
→ DecisionMargin
→ ResponseCurve
→ C_mode
```

但“公式看起来合理”不等于玩法正确。后续所有曲线与参数都应先服从一组可复核的策略约束。

本页把验收分成三层，避免把随机 fixture 当成领域真理：

1. **Hard Semantic Invariants**：机制结构不能违反；
2. **Strategy Ordering / Reversal**：玩家应能学到的方向性策略；
3. **Calibration / Effect-Size Fixtures**：差异是否大到足以形成体验，数值仍可调整。

可执行 probe：`../../prototypes/lure-response/proposal_c_feeding_response_acceptance_probe.py`。

## 2. Hard Semantic Invariants

这些不是调参目标，而是当前 Proposal C 的结构约束。

| ID | 不变量 | 含义 |
|---|---|---|
| H1 | Food Value 单调 | 其它相同，更值得吃的目标不能反而更低响应 |
| H2 | Motivation 单调 | 其它相同，更强 feeding motivation 不能反而更低响应 |
| H3 | Task Strain 单调 | 其它相同，更难完成的捕获任务不能反而更高响应 |
| H4 | Infeasible = hard zero | 真正做不到不能被 Food Value / Motivation 补偿 |
| H5 | Food Value = 0 → zero feeding response | 已解析为无食物价值时，不应靠其它因子复活 Feeding mode |
| H6 | Motivation = 0 → zero feeding response | 已解析为零 feeding drive 时，不应靠 target value 复活 Feeding mode |
| H7 | `0 ≤ C_mode ≤ 1` | `captureRetention` 语义不能放大 authoritative native supply |
| H8 | Food Value 与 Motivation 不被结构强制对称 | `V=1,M=.4` 不要求恒等于 `V=.4,M=1` |

Unknown / ResolutionIncomplete 仍沿 final-output contract：不产出 scalar，不属于上述 numeric checks。

## 3. Strategy Ordering / Reversal

这些约束描述玩家应能学习到的策略方向，不冻结具体差值。

| ID | 策略约束 | 玩法含义 |
|---|---|---|
| S1 | 鱼口差时，低 Task Strain > 高 Task Strain | 慢一点、送近一点、降低追逐要求应有价值 |
| S2 | 鱼口好时，高 Task Strain presentation 仍可有响应 | aggressive retrieve 不应永远被判死 |
| S3 | 提高 Motivation 会扩大可接受机会区域 | 鱼口好不是统一倍率，而是更多机会值得出手 |
| S4 | 高 Food Value 可补偿部分 Constrained task | 特别合口的猎物值得多费一点劲 |
| S5 | 高 Value / Motivation 不能突破 Infeasible | “太香了所以突然追得上”禁止 |
| S6 | 同 presentation 下，更高 Functional Capacity 应通过更低 derived TaskStrain 获得优势 | 能力差异必须有真实 task consequence |
| S7 | Pause 没有隐藏 bonus | pause 只有通过降低 TaskDemand、增加 exposure 或其它具名机制才有效 |

## 4. Calibration / Effect-Size Fixtures

这一层最容易被误写成“规则”。它们只是用来问：**方向虽然对，但玩家能不能感受到？**

当前 probe 先放五个工作 fixture：

- F1：鱼口差，同一较高价值 prey，快速 presentation → 慢速 presentation 应产生可观察 rescue；
- F2：正常鱼口，中等偏上 target value，在较难与较易 task 之间应存在 threshold crossing；
- F3：鱼口好，中等 target value + demanding task 仍应保留正响应；
- F4：鱼口差，即使 prey 较好，demanding task 也应受到明显压制；
- F5：鱼口好 + 高 value + easy task 应接近强响应区。

这些 fixture 的具体输入值不是 Production anchor，只是用来检查 response surface。

## 5. 当前 Working Formula 的执行结果

使用 `lure-response-proposal-c-feeding-response-threshold.md` 中当前临时公式：

```text
TaskCost(S) = 0.45 × S^1.6
Threshold(M) = 0.90 - 0.80 × M
Margin = FoodValue - TaskCost - Threshold
C_mode = clamp(Margin / 0.45, 0, 1)
```

本轮等价 probe 实际执行结果：

```text
Semantic invariants passed: H1 H2 H3 H4 H5 H6 H7 H8
Strategy orderings passed: S1 S2 S3 S4 S5 S6 S7
```

说明当前结构至少没有立刻违反已列出的语义与方向性策略。

但 effect-size 诊断暴露了一个重要问题。

### F1：数学翻转不等于玩法翻转

当前工作 fixture：

```text
FoodValue = 0.75
Motivation = 0.25

fast  strain = 0.75 → C = 0
slow  strain = 0.25 → C ≈ 0.0023
```

从 Boolean 看：

```text
fast = 0
slow > 0
```

“rescue 成功”。

但 `0.0023` 几乎不可能形成有意义的玩家体验差异。

因此验收不能只写：

```text
slow > fast
```

还必须最终定义某种 **effect-size / perceptibility budget**：哪些策略差异应当只是轻微，哪些应当足以造成明显的 catch-efficiency / target-purity / time-to-catch 差异。

当前不冻结统一 `ΔC_mode` 门槛，因为 `C_mode` 对最终玩家体验的作用还会经过 Spatial supply、Candidate competition、Opportunity cadence 与 Catch Cycle。应该在完整 reference basket / simulator 上反推。

## 6. 验收层级的意义

以后调四条曲线时：

```text
FoodValue scale
TaskStrain → TaskCost
Motivation → Threshold
DecisionMargin → C_mode
```

检查顺序必须是：

```text
先守 Hard Invariants
↓
再守 Strategy Ordering / Reversal
↓
最后调 Effect Size
```

不能为了把某个体验差异做大，破坏硬门或 Cause ownership。

也不能只因为所有 ordering 都正确，就认为参数已经可用。

## 7. 下一步

下一步应把 effect-size 从 `C_mode` 内部尺度提升到玩家可感知尺度。

优先做一个 **reference fishing scenario simulator**：

```text
固定 Spatial / Base Supply
+ 两三个 competing species
+ Opportunity cadence
+ 当前 Candidate Resolver / TrueRoll
```

只改变：

- Food Value；
- Motivation；
- TaskStrain。

然后观察：

- target share / purity；
- target active-roll time；
- any-fish rate；
- 完整 catch-cycle 下的 target wall-clock。

这样才能回答：

> `C_mode` 从 0.2 变到 0.4，玩家到底感觉有多大？

在这个映射建立前，不应凭 `ΔC_mode=0.1/0.2` 直接定义“明显差异”。

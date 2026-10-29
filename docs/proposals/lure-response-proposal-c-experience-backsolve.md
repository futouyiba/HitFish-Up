# 方案 C｜从玩家体验反推 Feeding Response

日期：2026-10-26  
状态：Working Calibration Probe，非 Current，非生产参数。

## 1. 这轮解决什么

前几轮已经确认：

- 只检查 `slow > fast` 不够；
- `ΔC_mode` 本身没有统一的玩家体验意义；
- Response 的最终幅度应该从玩家体验目标反推，而不是先给 `C_mode` 随手定差值。

本轮第一次按下面的方向做反推：

```text
Reference Fishing Story
→ 玩家体验目标
→ target active-roll time / purity / efficiency
→ 反推 C_mode
→ 再检查当前 TaskCost / Motivation Threshold / ResponseCurve 能否拟合
```

可执行 probe：`../../prototypes/lure-response/proposal_c_experience_backsolve_probe.py`。

## 2. 与最新远端资料对齐

2026-10-26 读取 `main` 后，和本问题直接相关的更新包括：

- `fcf-system-map/README.md` 已明确：空间分布权重与鱼侧动态参数是两条并行支路；Response 消费鱼侧动态参数与呈现刺激，Spatial 与 Response 只在圆桌权重聚合时汇合一次。
- `fcf-system-map/contracts.json` 的 `RESPONSE` 已链接到《Behavioral Regime × Largemouth Bass》v8；该 Rationale 中 Baseline Feeding 的 Working 主链为：

```text
Feeding Enabled
+ Target Interpretation
→ Target Relation
+ Feeding Motivation
+ TaskAffordance
→ Feeding Decision Resolver
→ Decision Strength
→ Response Projection
→ C_feed
```

同时明确：Accessible Alternatives、Risk、SpeciesBaseThreshold、Universal ActionCost 暂不强制；没有独立 counterfactual / ranking reversal 时不购买新 DOF。

因此本轮继续研究 `Target Value / Relation + Motivation + TaskAffordance → Decision Margin / Strength → C_mode`，没有引入新的跨域 Owner。

## 3. 先回答：策略约束要不要进文档

要，而且已经应该作为长期 Working Acceptance 保留，但必须分层。

### 3.1 Hard Semantic Invariants

这些是机制不能违反的约束：

- 其它相同，Food Value 提高，response 不应反降；
- 其它相同，Feeding Motivation 提高，response 不应反降；
- 其它相同，Task Strain 提高，response 不应反升；
- `Infeasible` 永远是 hard zero；
- 真正的 zero Food Value / zero Feeding Motivation 不应被其它软因素复活；
- `C_mode / captureRetention` 保持在 `[0,1]`；
- Food Value 与 Motivation 不应被公式结构强制成完全对称变量。

### 3.2 Strategy Ordering / Reversal

这些是应当能被玩家学会的策略方向：

- 鱼口差时，降低 Task Strain 应当有价值；
- 鱼口好时，aggressive retrieve 可以重新变得可用；
- 高 Food Value 可以补偿部分 Constrained task，但不能突破 Infeasible；
- 同 presentation 下，较高 `InterceptSpeedLimit` 应通过真实 Closing consequence 获得优势；Activity 只在 Closing physically feasible 后改变 soft cost；
- pause 本身没有匿名 bonus，只能通过降低 TaskDemand、增加 exposure 等具名机制起效。

这些内容已经由 `lure-response-proposal-c-feeding-response-acceptance-matrix.md` 承接。具体 effect size 不属于这两层，而属于 Calibration。

## 4. 使用当前 Candidate Calibration Reference Basket

Candidate Weight Calibration Current v8 提供了一个方便的标准尺：

- T2 Target reference active-roll time = `30s`；
- any-fish active-roll time = `12s`；
- Target purity = `40%`；
- Reference-good Target Response = `1.0`；
- 这是 `λ=1/s` 的 normalized active-roll anchor，不是 Production wall-clock 常量。

一个等价、便于计算的 working representation 是：

```text
Target native mass at C=1 = 40
Background total mass     = 60
N                         = 1200
λ                         = 1/s
```

于是整个 reference basket 始终处于 `F<N`，并有：

```text
W_target = 40 × C
T_target = 1200 / (40 × C)
         = 30 / C
```

所以第一次反推非常直接：

```text
C = 30 / target_active_roll_time
```

## 5. 第一版 Reference Fishing Story 体验预算

下面数字全部是 **Working Experience Budget**，不是自然事实，也不是 Production 定值。目的只是让故事先有可攻击的体验差异。

固定：同一较高价值 baitfish-like feeding target；只改变 Motivation、Closing demand、`InterceptSpeedLimit` 与 Activity soft cost。

| Story | 玩家体验目标：Target Active-Roll Time | 反推 C | 约束意图 |
|---|---:|---:|---|
| 差鱼口 + fast retrieve | 150s | 0.20 | 几乎失效，但不是硬 Infeasible |
| 差鱼口 + slow / pause 后低 strain | 60s | 0.50 | 明显 rescue，但仍差于正常鱼口 |
| 正常鱼口 + fast retrieve | 45s | 0.67 | 有损失，但仍是可用打法 |
| 正常鱼口 + reference-good | 30s | 1.00 | 当前 Reference Anchor |
| 好鱼口 + fast retrieve | 35s | 0.86 | aggressive retrieve 基本恢复竞争力 |
| 较低 `InterceptSpeedLimit` + fast | 120s | 0.25 | Closing 物理边界或 soft cost 造成明显受限 |
| 较低 `InterceptSpeedLimit` + 降速 | 40s | 0.75 | 降低 Closing demand 后大幅恢复 |

这些预算对应的 Reference purity 约为：

| C | Purity |
|---:|---:|
| 0.20 | 11.8% |
| 0.25 | 14.3% |
| 0.50 | 25.0% |
| 0.67 | 30.8% |
| 0.75 | 33.3% |
| 0.86 | 36.4% |
| 1.00 | 40.0% |

注意：这里 purity 的变化只是当前 Reference Basket 下的结果。换 Candidate pool regime 后，同一个 `C` 不会保留同样的 purity / wall-clock meaning。

## 6. 第一次反推暴露出的约束

### 6.1 先检查体验目标自身是否违反语义

这是一个很重要的新护栏。

如果两条 Story 的

```text
Food Value 相同
Motivation 相同
```

而 Story A 的 physically-feasible task consequence 更低，那么体验预算反推得到的 `C_A` 不能反而低于 `C_B`。

否则还没开始拟合公式，体验目标自己就已经违反 physically-feasible task consequence 的单调不变量。

本轮原始草案曾出现：

```text
normal fast: strain≈0.65, C≈0.67
weak fish slow: strain≈0.50, C≈0.60
```

这组预算不合法：如果 physically-feasible task consequence 已经足以表达 Closing / task 差异，就不能再因为“它叫弱鱼”额外压一次 Response。

因此 Working budget 修正为：

```text
weak fish slow: C≈0.75（40s）
```

这里保留的是 Closing / task consequence，而不是 fish label bonus / penalty。

### 6.2 体验预算开始真正约束公式

把上面的 `C` 目标交给当前简单 threshold family：

```text
TaskCost = k × physically-feasible task consequence^p
Threshold = b - c × M
Margin = V - TaskCost - Threshold
C = clamp(Margin / r, 0, 1)^gamma
```

对一组离散参数做粗搜索后，当前最好的一组只是诊断值：

```text
k     = 0.35
p     = 1.6
b     = 0.85
c     = 0.45
r     = 0.40
gamma = 1.2
RMSE  ≈ 0.062
```

对应：

| Story | Target C | 当前简单 surface 预测 |
|---|---:|---:|
| 差鱼口 + fast | 0.20 | 0.21 |
| 差鱼口 + slow | 0.50 | 0.56 |
| 正常鱼口 + fast | 0.67 | 0.55 |
| 正常 reference-good | 1.00 | 0.95 |
| 好鱼口 + fast | 0.86 | 0.94 |
| 弱能力 + fast | 0.25 | 0.25 |
| 弱能力 + slow | 0.75 | 0.72 |

这说明当前结构能大体表达这些故事，但仍有系统性偏差：

- `normal fast` 被压得过低；
- `good fast` 又略偏高；
- reference-good 也未自然顶到 1。

现在不应为了消灭残差去修改体验目标。应先判断这些 Experience Budget 是否真的合理；如果合理，再问简单 `linear Motivation threshold + single TaskCost curve + single ResponseCurve` 是否表达能力不足。

## 7. 这轮最重要的方法变化

以前容易这样做：

```text
先定公式
→ 调到看起来顺
→ 再解释玩家体验
```

现在改成：

```text
先写 Fishing Story
→ 定玩家应该感受到的差异
→ 映射到 target time / purity / efficiency
→ 反推 C_mode
→ 检查 Story 之间是否自洽
→ 再拟合 TaskCost / Motivation Threshold / ResponseCurve
```

公式成为被验收对象，而不是体验目标的来源。

## 8. 还不能下的结论

当前还不能说：

- `150s / 60s / 45s / 35s` 就是正确 Production 体验；
- TaskCost 必须是幂函数；
- Motivation 必须线性降低 threshold；
- ResponseCurve 必须是 power curve；
- `C=0.5` 在所有鱼池都代表同样体验。

这些都还是 Working Calibration Hypothesis。

## 9. 下一步

下一步优先做两件事：

1. **攻击 Experience Budget 本身。** 例如“差鱼口 slow 60s、fast 150s”到底是不是我们真的想让玩家感受到的差距；正常鱼口 fast 45s 是否过度惩罚。
2. **只在预算稳定后攻击公式 family。** 如果目标合理而当前简单 surface 持续存在结构性残差，再考虑 Motivation threshold 非线性、TaskCost 分段 / 饱和、Response Projection 非线性，而不是先增加新的 semantic DOF。

这一轮的产物不是最终参数，而是一套可反复执行的“体验目标 → C → 内部曲线”反推路径。

# 方案 C｜从 C_mode 到玩家体验：Response Effect-Size Mapping

日期：2026-10-26  
状态：Working Calibration Probe，非 Current，非生产参数。

## 1. 问题

Feeding Response 验收矩阵已经发现：只检查 `slow > fast` 之类排序不够；数学上的微小差异可能对玩家不可感知。

但也不能直接规定：

```text
ΔC_mode >= 0.1
```

就算“明显”。

原因是 `C_mode / captureRetention` 后面还会进入 Candidate Resolver 与 TrueRoll；同样的 `ΔC` 在不同 Candidate pool regime 下，对 target probability、purity、throughput 与完整 catch-cycle 的影响不同。

本页用最小 reference simulator 建立第一层映射。

可执行 probe：`../../prototypes/lure-response/proposal_c_response_effect_size_simulator.py`。

## 2. Current-aligned mapping

沿用当前跨域 seam：

```text
Interaction captureRetention C
× Spatial / Native Supply
→ W_target
```

并使用当前 TrueRoll 形式：

```text
F = Σ W_i
p_i = W_i / max(N, F)
```

本页只固定背景 mass，改变目标鱼的 `C`，观察：

- target native weight；
- target per-opportunity probability；
- target purity；
- any-fish probability；
- normalized active-roll target time；
- 带简单 bycatch handling cost 的 diagnostic wall-clock。

最后一项只是简单 renewal fixture，不是 Production Catch Cycle。

## 3. Fixture A：Underfilled Pool

工作参数：

```text
Target native supply before C = 40
Background total mass = 50
N = 100
λ = 1 opportunity / s
```

在 `C∈[0,1]` 内始终有 `F<N`。

| C | W_target | F | p_target | purity | p_any | target active-roll time |
|---:|---:|---:|---:|---:|---:|---:|
| 0.10 | 4 | 54 | 0.04 | 7.4% | 0.54 | 25.0s |
| 0.20 | 8 | 58 | 0.08 | 13.8% | 0.58 | 12.5s |
| 0.40 | 16 | 66 | 0.16 | 24.2% | 0.66 | 6.25s |
| 0.60 | 24 | 74 | 0.24 | 32.4% | 0.74 | 4.17s |
| 0.80 | 32 | 82 | 0.32 | 39.0% | 0.82 | 3.13s |
| 1.00 | 40 | 90 | 0.40 | 44.4% | 0.90 | 2.50s |

这里：

```text
C 0.4 → 0.8
p_target 0.16 → 0.32
```

目标鱼 active-roll rate 近似翻倍。

因此在 underfilled regime 下，`C` 的差异会比较直接地映射成目标鱼绝对机会率差异。

## 4. Fixture B：跨过 Saturation

工作参数：

```text
Target native supply before C = 40
Background total mass = 80
N = 100
λ = 1 opportunity / s
```

当 `C > 0.5` 左右后，`F≥N`，总 Spawn throughput 封顶。

| C | W_target | F | p_target | purity | p_any | target active-roll time |
|---:|---:|---:|---:|---:|---:|---:|
| 0.10 | 4 | 84 | 0.040 | 4.8% | 0.84 | 25.0s |
| 0.20 | 8 | 88 | 0.080 | 9.1% | 0.88 | 12.5s |
| 0.40 | 16 | 96 | 0.160 | 16.7% | 0.96 | 6.25s |
| 0.60 | 24 | 104 | 0.231 | 23.1% | 1.00 | 4.33s |
| 0.80 | 32 | 112 | 0.286 | 28.6% | 1.00 | 3.50s |
| 1.00 | 40 | 120 | 0.333 | 33.3% | 1.00 | 3.00s |

这里同样：

```text
C 0.4 → 0.8
```

但：

```text
p_target 0.16 → 0.286
```

不再翻倍。

因为进入 `F≥N` 后，提高目标鱼 `W` 会与背景鱼发生真实的零和竞争。

## 5. 当前最重要的结论

### 5.1 `ΔC` 没有 universal gameplay meaning

同样：

```text
ΔC = +0.2
```

可能处于：

- underfilled 区，直接提高目标绝对 rate；
- saturation 附近，同时改变 throughput 与 composition；
- saturated 区，主要改变 composition，且有边际收益递减。

所以不能脱离 Candidate context 说“0.2 就是明显差异”。

### 5.2 Response curve 不应独立标定

Response 的四条曲线：

```text
FoodValue scale
TaskStrain → TaskCost
Motivation → Threshold
DecisionMargin → C_mode
```

不能只看 `C_mode` surface 漂不漂亮。

至少要同时看：

```text
C_mode
→ W_target
→ p_target / purity / p_any
→ target active-roll time
→ full catch-cycle wall-clock
```

### 5.3 “策略可感知度”应该最终用体验指标定义

例如将来可以定义：

```text
明显策略差异
= 在 Reference Scenario 下
  target active-roll time / target purity / wall-clock
  达到某个设计预算
```

而不是：

```text
明显策略差异 = ΔC >= 常数
```

具体预算当前仍 Open，应由体验目标反推。

## 6. 简单 catch-cycle diagnostic

probe 额外用了一个非常简化的 fixture：

```text
每次 Opportunity active cost = 1 / λ
每次 background Spawn Commit 增加 5s handling/reset
```

则期望 target wall-clock：

```text
E[T_target] = (active_step + p_background × handling_cost) / p_target
```

它只用于说明 bycatch interruption 会放大 composition 差异对真实等待时间的影响，不是 Production Catch Cycle 公式。

这与 Candidate Calibration Current 的边界一致：active-roll probability 与真实 wall-clock 不是同一个量，bycatch fight / handling / reset / re-entry 可产生额外成本。

## 7. 下一步

现在已经具备两层 probe：

```text
Feeding Response acceptance matrix
→ 保证语义 / 策略方向正确

Response effect-size simulator
→ 把 C 映射到 candidate / experience metrics
```

下一步不宜继续手调 threshold。

应选 3～5 个具体的 **Reference Fishing Stories**，为每个故事先写玩家体验目标，例如：

1. 鱼口差：fast retrieve 几乎失效，pause / slower retrieve 应产生明显恢复；
2. 鱼口正常：标准 retrieve 是基准，高 value prey 与适度降速各有可见收益；
3. 鱼口好：aggressive retrieve 仍具竞争力，不要求玩家一直慢钓；
4. 弱 Functional Capacity：高 demanding presentation 明显劣于强鱼；
5. Infeasible：任何 Value / Motivation 都不能复活。

然后给每个故事指定 target purity / target-time / relative-efficiency 区间，再反推 Response 曲线参数。

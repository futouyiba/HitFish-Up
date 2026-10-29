# 方案 C｜Step 4 Refinement：Temporal Mechanism 与 Roll 的双路由

日期：2026-10-26  
状态：Working Probe Refinement，不是 Current，不规定最终 response aggregation。

## 1. 为什么需要修正上一轮结论

上一轮 counterfactual closure 有两处表述过强：

1. `recent_move_then_pause` 在“当前物理状态相同”的 probe 中没有自动改变 TaskDemand，这只能证明它不是当前 TaskDemand 的同义反复，不能据此拒绝它的独立作用。真实路亚策略里，刚停可能通过注意、预测、攻击时机、窗口停留等机制起作用；这些机制需要单独识别。
2. `roll 0° vs 75°` 只有在我们人为固定“roll 不改变实际轨迹、水动力或捕获几何”时 TaskDemand 才相同。真实侧翻可能同时带来 capture-geometry consequence，因此 roll 可能同时产生 valuation cue 与 physical task consequence。

因此 Q2 从“reject temporal effect”修正为“temporal mechanism remains candidate”；Q3 从“roll routes only to valuation”修正为“cue-only 与 physically consequential 两类路径必须分开”。

## 2. Q2：刚停为什么可能真的重要

`recent_move_then_pause` 不应该直接映射到固定 bonus，但它完全可能有独立作用。

需要区分至少四种候选机制：

```text
A. 当前速度下降
   → TaskDemand 降低

B. 先运动后停住
   → 感知/注意刷新、目标预测变化

C. 停在可攻击位置
   → Opportunity / geometry window 延长

D. cadence / sequence 本身
   → 可能改变 Feeding-mode interpretation / trigger
```

上一轮只隔离了 A，不能因此删除 B/C/D。

当前处理：

- `recent_move_then_pause` 保留为 typed temporal relation；
- 不默认给数值 bonus；
- 后续通过 holdout 分别隔离 attention / attack-window / sequence effect；
- 若无法证明独立 ranking reversal，再删除对应机制。

## 3. Q3：为什么 TaskDemand 不必相同

关键不是 roll 角本身，而是它有没有改变捕获任务。

### 3.1 Cue-only roll

人为固定：

- translational trajectory 相同；
- relative speed 相同；
- future position evolution 相同；
- target capture geometry 相同；
- only visible pose / roll differs。

此时 TaskDemand 可以保持相同，差异只能走 Target / Valuation Candidate：

```text
roll / imbalance-like cue
→ vulnerability interpretation candidate
```

### 3.2 Physically consequential roll

如果侧翻实际改变：

- 迎击面或 target orientation；
- 稳定性 / 可预测性；
- 水动力导致的轨迹或速度；
- 鱼需要的转向、垂直重定位或 strike geometry；

那么它会合法改变 TaskDemand。

但原则是：

```text
raw roll angle
≠ generic task penalty

roll
→ actual capture-relevant physical consequence
→ TaskDemand
```

同一 roll 还可能同时产生 vulnerability cue；两条路径可以并存，但必须分别有独立 physical / semantic meaning，不能匿名重复计权。

## 4. TaskDemand 最小骨架继续压缩

不要永久保存 raw `speed penalty + distance penalty + vertical penalty + roll penalty`。

当前更好的最小候选是：

### 4.1 Intercept / Closing Demand

由鱼-目标相对位置与相对运动共同形成，回答：

> 从当前状态到可攻击位置，鱼需要完成多大的接近 / 截获任务？

因此 distance 与 speed 首先应尝试在这个 task semantic 中合并，而不是天然成为两个独立 response 系数。

### 4.2 Maneuver / Capture-Geometry Demand

回答：

> 为了形成有效攻击姿态，鱼还需要多少额外的转向、垂直重定位或 target-orientation 适配？

只有当某项因素能在 Intercept Demand 相同的情况下制造独立 feasibility / cost reversal，才 admission 到这一维。

## 5. 修正后的 Step 4 路由

```text
ActualPresentation / Step-3 facts
        │
        ├─ current relative motion + position
        │      → Intercept / Closing Demand
        │
        ├─ actual maneuver / orientation consequence
        │      → Maneuver / Capture-Geometry Demand
        │
        ├─ recent_move_then_pause / cadence history
        │      → Temporal Mechanism Candidate
        │         (attention / attack-window / sequence)
        │
        └─ imbalance-like visible cue
               → Target / Valuation Candidate

species × size cohort → InterceptSpeedLimit
+ fish-relative geometry / presentation facts
→ Closing feasibility
→ ResolvedTaskDemand
→ Activity-aware soft Closing cost
→ TaskAffordance

Target / Feeding-mode valuation candidates
+ fish-side current motivation
→ Feeding-mode Valuation / interpretation
```

不规定最后如何聚合。

## 6. v2 executable probe

新增：

`../../prototypes/lure-response/proposal_c_step4_counterfactual_probe_v2.py`

它检查：

- Q1：相对运动通过 Intercept Demand 形成 Feasible → Constrained → Infeasible；
- Q2：当前 TaskDemand 相同，但 recent-pause 仍保留独立 temporal candidate；
- Q3a：cue-only roll 只改变 valuation candidate；
- Q3b：当 roll 产生明确 capture-orientation consequence 时，也可以改变 TaskDemand。

所有数值只用于测试拓扑，不是大口黑鲈生物学标定。

## 7. 下一步

继续两条线：

1. **TaskDemand dimension attack**：构造相同 Intercept Demand、不同 maneuver/geometry consequence 的案例，验证第2维是否真的需要；若不能制造独立 reversal，就继续压回1维。
2. **Temporal mechanism decomposition**：对 `recent_move_then_pause` 不再只问“有没有 bonus”，而分别测试 attention、attack-window、sequence/cadence 是否购买独立且玩家可学习的策略差异。

这两条闭合之前，不设计最终 C_mode 总公式。
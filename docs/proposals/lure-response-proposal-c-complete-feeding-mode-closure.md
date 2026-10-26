# 方案 C｜Complete Feeding Response Mode 最小闭合

日期：2026-10-26  
状态：Working Closure，非 Current，非生产公式。

## 1. 本轮问题

经过 Step 3、TaskDemand、Opportunity projection 与 Valuation admission attack 后，当前需要回答：

> Complete Feeding Response Mode 最少需要哪些独立语义才能闭合？是否必须存在一个额外的 presentation-state Valuation 层？

可执行 probe：`../../prototypes/lure-response/proposal_c_complete_feeding_mode_probe.py`。

## 2. 先澄清：Target/Food Value 与 State Valuation 不是一回事

当前设计中已经存在且有独立意义的 Target/Food Value，例如：

- 当前食物偏好；
- prey size / intake suitability；
- diet shift 后的相对食物评价。

这些回答的是：

> 这个已解释出的猎物，对当前这条鱼而言值不值得作为食物？

而此前未证明的是另一层：

> presentation state 本身是否还需要一个独立的额外 Valuation modifier，例如 cadence bonus / vulnerability bonus？

本轮只攻击后者是否为 mandatory layer。

## 3. 四个独立职责

### 3.1 Resolution / Mode Validity

负责判断必要事实是否已经闭合，以及该 Feeding Mode 是否成立。

典型结果：

- `Resolved`；
- `ResolutionIncomplete`；
- `ModeInvalid`。

Unknown 不能被转成 0 或 neutral coefficient。

### 3.2 Target / Food Value

负责食物本身的 mode-local value。

同样的 Perception、TaskAffordance 与 Motivation 下，不同 Target Value 应允许产生不同 response ranking。

因此 Target Value 是独立消费语义，不能被 Motivation 或 TaskAffordance 替代。

### 3.3 TaskAffordance

来自 ResolvedTaskDemand 与 ResolvedFunctionalCapacity 的比较。

至少区分：

- Feasible；
- Constrained；
- Infeasible；
- Unknown。

Infeasible 表示当前任务做不到，不等于鱼不想吃，也不应该通过降低 Motivation 来表示。

### 3.4 Feeding Motivation

来自 fish-side behavioral context / readiness。

它回答：

> 当前这条鱼对获取食物的行为激励有多强？

它不负责重新判断 prey identity，也不负责物理能力。

## 4. 反事实结果

probe 固定其它输入，分别改变：

1. Target Value；
2. Feeding Motivation；
3. TaskAffordance；
4. resolution status；
5. 是否存在独立 state valuation modifier。

结果：

- Target Value 独立变化可改变 response ranking；
- Motivation 独立变化可改变 response ranking；
- TaskAffordance 独立变化可改变 response ranking，并可单独进入 Infeasible；
- Unknown 必须保留为 `ResolutionIncomplete`，不能 roll；
- 在没有任何 presentation-state valuation modifier 时，Complete Feeding Response Mode 仍然能够闭合；
- 若未来 cadence / vulnerability 等机制真的通过 admission gate，可以显式插入 optional modifier，而不需要改写 Target Value、Motivation 或 TaskAffordance 的 owner。

## 5. 当前推荐结构

```text
Target / Perception Resolution
        ↓
Mode Validity / Resolution State

Target / Food Value
        ┐
Feeding Motivation
        ├──→ Complete Feeding Response Mode
TaskAffordance
        ┘

[optional admitted presentation-state valuation semantics]
        └──→ 只在未来被证明后加入
```

更完整地：

```text
ActualPresentation
→ prey type / prey state interpretation
→ sparse prey semantics

fish-relative geometry + FunctionalCapacity
→ ResolvedTaskDemand
→ TaskAffordance

fish-side behavioral context
→ Feeding Motivation

prey identity / size / diet context
→ Target / Food Value

以上语义闭合后
→ Complete Feeding Response Mode
→ C_mode / downstream response contract
```

## 6. Valuation 层的当前裁决

### 必须保留

`Target / Food Value`

因为它有独立问题定义与独立反事实作用。

### 当前不必建立

独立通用的 `Presentation-State Valuation Layer`。

尤其不建立：

- `StateBonus`；
- `PauseBonus`；
- `CadenceCoeff`；
- `VulnerabilityCoeff`；
- `OpportunityScore`。

### 保留扩展点

若未来某个 presentation semantic 在控制 Perception、TaskAffordance、temporal exposure、Target Value 与 Motivation 后仍产生稳定 residual ranking difference，可以 admission 为：

```text
optional admitted state valuation semantic
```

它是可选插件，不是 Complete Feeding Response Mode 的 mandatory layer。

## 7. 重要边界

- Mode validity / resolution 不是数值惩罚；
- Infeasible 不是 low motivation；
- low motivation 不代表 target unsupported；
- Target Value 不等于 Feeding Motivation；
- prey semantic 不自动等于 bonus；
- Opportunity projection 不成为新的 authority；
- state valuation 为空是合法状态。

## 8. 关于 probe 中的 response_proxy

probe 使用一个人工的 `response_proxy` 只用于证明各语义可以独立制造排序变化，以及 state valuation 不是 mandatory。

它不是最终聚合公式，也不代表生产应使用乘法、线性 modifier 或固定 Feasible/Constrained 系数。

真正的最终聚合仍需单独决定。

## 9. 当前 Working Conclusion

Complete Feeding Response Mode 的最小语义闭合目前可以是：

```text
Mode Validity / Resolution
+ Target / Food Value
+ TaskAffordance
+ Feeding Motivation
```

并允许：

```text
+ optional admitted presentation-state valuation semantics
```

但最后这一项当前可以为空。

因此 Step 4 不需要为了框架对称性强行创建一个独立 State Valuation 层。

## 10. 下一步

下一步不再扩语义层，而应直接攻击最终输出 contract：

1. `Complete Feeding Response Mode` 应输出 categorical decision、continuous response strength，还是两者都有；
2. Feasible / Constrained / Infeasible 与 Motivation / Target Value 应如何组合，哪些是 gating，哪些参与连续排序；
3. Unknown / ResolutionIncomplete 如何阻止 roll；
4. 多个完整 Feeding hypotheses / modes 同时存在时，何时 max，何时不能 max；
5. 最终 `C_mode` 与 HitFish candidate / roll 的接口究竟应该是什么。

在这些问题闭合前，不把 probe 的 `response_proxy` 晋升为生产公式。

# 方案 C｜Prey Opportunity Interpretation 抽象攻击

日期：2026-10-26  
状态：Working Probe，非 Current，非生产参数。

## 1. 问题

当前想验证一个候选中层抽象：

> 是否应该在 Prey State Interpretation 与 Fish-side Evaluation 之间增加一个统一的 `Prey Opportunity State / 猎物机会状态`？

钓鱼领域确实存在大量稳定叙事：

- escaping / fleeing baitfish；
- injured / dying / vulnerable baitfish；
- stunned baitfish；
- struggling prey；
- pause / regroup / erratic movement。

这些语义对玩家策略故事有价值，但不能因此直接假设它们属于一个扁平状态枚举。

可执行 probe：`../../prototypes/lure-response/proposal_c_step4_prey_opportunity_probe.py`。

## 2. 第一轮结论：不要做 flat OpportunityState

一个扁平枚举例如：

```text
OpportunityState
= escaping
| exposed
| vulnerable
| stunned
| struggling
```

会混合至少三类不同语义：

1. **Prey Behavior**：猎物正在做什么，例如 escaping-like / struggling-like；
2. **Prey Condition Cue**：猎物看起来处于什么条件，例如 vulnerable-like / stunned-like；
3. **Fish-relative Opportunity**：对当前这条鱼而言，是否容易接近、截获、形成 strike geometry。

第三类不是 target 自身状态，而是 fish × target × context 的关系。

## 3. 反事实证明 flat state 会丢信息

### A/B：同样 escaping-like，不同 TaskAffordance

保持 prey semantic 都为 `escaping-like`：

- A：距离近、相对速度低 → Feasible；
- B：距离远、相对速度高 → Infeasible。

说明：

```text
escaping-like != opportunity quality
```

同一个“逃逸中的猎物”故事，可以对一条鱼是好机会，对另一时刻是根本追不上。

### C/D：同样 vulnerable-like，不同 TaskAffordance

保持 `sinking + roll` 所形成的 vulnerable-like cue 相同：

- C：截获几何容易 → Feasible；
- D：截获要求过高 → Infeasible。

说明：

```text
vulnerable-like != easy-to-capture
```

Vulnerability semantic 可以成立，但不能直接替代 TaskDemand / TaskAffordance。

### E：多个 prey semantics 可以共存

同一时刻可以同时存在：

```text
struggling-like
+
vulnerable-like
```

因此这些语义本质上更适合作为 sparse facets，而不是互斥枚举。

## 4. 推荐结构：Opportunity Interpretation 是 packet，不是 factor

建议保留 `Prey Opportunity Interpretation` 这个名字，但定义成一个组合解释包 / view：

```text
Prey Opportunity Interpretation
├─ Prey-side semantics
│  ├─ Behavior Motifs
│  │  ├─ escaping-like
│  │  ├─ struggling-like
│  │  └─ ...
│  └─ Condition Cues
│     ├─ vulnerable-like
│     ├─ stunned-like
│     └─ ...
│
├─ Fish-relative capture evaluation
│  ├─ ResolvedTaskDemand
│  └─ TaskAffordance
│
├─ Temporal support / attack-window context
│
└─ Optional admitted valuation semantics
```

它的作用是把“当前这是什么样的捕食机会”组织起来，而不是输出一个新的统一数值。

禁止默认生成：

```text
OpportunityBonus
OpportunityCoeff
OpportunityScore
```

除非未来有明确 downstream contract 证明一个标量确实必要。

## 5. 哪些语义当前可以 admission

### Fishing-domain semantic 可以 admission

玩家与钓鱼内容中，以下叙事足够常见，可作为 Working Semantic：

- `escaping-like`：模仿被追逐 / 逃逸的 baitfish；
- `struggling-like`：尤其 surface presentation 中模仿 struggling prey；
- `vulnerable-like`：injured / sick / dying / wounded-minnow 风格 presentation。

这里的 admission 是：

> 允许系统解释“这个 presentation 看起来像什么猎物状态”。

不是：

> 自动给最终 response 一个 bonus。

### 仍需谨慎

- `stunned-like`：钓鱼叙事中存在，但应先定义可观测证据，不要与 vulnerable-like 同义化；
- `exposed`：更像 fish-relative geometry / attack-window relation，不宜当作 prey 自身 condition；
- `easy prey`：这是下游结论，不能当输入标签。

## 6. 与现有 Step 3 / Step 4 的边界

### Step 3 继续负责

- 实际运动、暂停、下沉、roll、surface / near-bottom 等事实；
- prey-conditioned process interpretation，例如 burst / pause pattern；
- 不评价当前 fish 是否容易捕获。

### Prey-side semantic interpretation

从 Step 3 facts / process 中得到：

```text
escaping-like
struggling-like
vulnerable-like
...
```

这些是 target-side interpretation，不是 response。

### Fish-side Step 4

结合：

- prey-side semantics；
- fish-relative geometry；
- FunctionalCapacity；
- TaskDemand / TaskAffordance；
- Perception / temporal support；
- Feeding Motivation；

形成当前捕食机会的完整解释。

## 7. 对 vulnerability 的修正

此前把 vulnerability admission 过多绑定在严格生态学“是否证明捕食者偏好伤鱼”上，不适合当前游戏设计目标。

本项目更重要的第一层证据是 fishing-domain cognition：钓手是否稳定地把某些 erratic / sinking / crooked / struggling presentation 解释成 injured / sick / dying / vulnerable prey。

现有 Bassmaster / Rapala 等材料明确存在这种认知，因此：

```text
Vulnerability Interpretation
→ Working Admitted Semantic
```

但仍然：

```text
VulnerabilityBonus / VulnerabilityCoeff
→ Not Admitted
```

语义 admission 与数值 admission 分开。

## 8. 当前推荐的数据形态

不要：

```json
{
  "opportunity_state": "vulnerable"
}
```

更接近：

```json
{
  "prey_semantics": {
    "behavior_motifs": ["struggling_like"],
    "condition_cues": ["vulnerable_like"]
  },
  "task_affordance": "Feasible",
  "temporal_context": {
    "favorable_dwell": "..."
  },
  "valuation_semantics": []
}
```

这允许一个 presentation 同时拥有多种语义，也允许同样 prey semantic 在不同鱼、不同距离、不同能力下产生不同 capture opportunity。

## 9. 外部领域证据

以下材料只用于证明 fishing-domain semantic，而不是生物学参数：

- Bassmaster, *How to hunt bass in the open*：描述 bass 先 stun baitfish，随后吞食下沉的 injured baitfish；
- Bassmaster, *Why I throw jerkbaits, part 1*：明确把下沉、跑偏、停顿后的 jerkbait 描述为 injured / sick / vulnerable minnow；
- Bassmaster, *Lesson 4: Hard baits*：topwater bait 模仿 wounded baitfish struggling on surface；
- Bassmaster, *Striking moves*：escaping baitfish retrieve 被作为可学习的 bass 策略；
- Rapala：长期使用 wounded-minnow action 作为产品语义。

这些材料支持：`escaping-like / struggling-like / vulnerable-like` 是有效的钓鱼领域语言。

## 10. 当前 Working Conclusion

1. **不要建立 flat `Prey Opportunity State` enum。**
2. **可以建立 `Prey Opportunity Interpretation` packet / projection。**
3. `escaping-like / struggling-like / vulnerable-like` 作为 fishing-domain semantic 可以 Working Admission。
4. prey semantic 与 TaskAffordance 正交：同一 semantic 可以对应 Feasible 或 Infeasible。
5. 多个 prey semantic 可以共存，因此应使用 sparse facets。
6. 不从 Opportunity Interpretation 自动生成统一 bonus / coefficient。
7. vulnerability semantic 已有足够 fishing-domain cognition 支持；它是否产生额外 valuation effect 是另一个问题。

## 11. 下一步

下一步不再扩词表，而应该验证这个 packet 是否真的改善最终 Complete Feeding Response Mode 的表达：

- 对同一个 `vulnerable-like` presentation，让不同 fish / fish state 得到不同 response；
- 对同一个 `escaping-like` presentation，让高 FunctionalCapacity 与低 FunctionalCapacity 产生策略 reversal；
- 检查 `prey_semantics` 是否只需要参与 Explain / mode selection，还是至少有一个 semantic 真正需要进入 Valuation。

如果 Opportunity packet 最终只是把已有字段重新包装而没有消费方，就不把它做成独立生产对象，只保留为解释视图。
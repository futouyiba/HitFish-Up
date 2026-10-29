# 方案 C｜Final Output Contract Closure

日期：2026-10-26  
状态：Working Closure，非 Current，非生产公式。

## 1. 目标

在 Step 4 最小语义已闭合后，本轮只回答最终输出边界：

- Complete Feeding Response Mode 输出 categorical state 还是 continuous strength；
- Unknown 与 resolved zero 如何区分；
- Feasible / Constrained / Infeasible 哪些属于 gating，哪些仍可参与连续排序；
- 多个完整 feeding hypotheses / modes 何时允许 max；
- `C_mode` 如何作为 HitFish candidate / roll 的输入而不吞掉未决状态。

可执行 probe：`../../prototypes/lure-response/proposal_c_final_output_contract_probe.py`。

## 2. 必须同时输出 categorical status 与 continuous strength

仅输出一个 scalar 会把这些语义错误合并：

```text
Unknown
Resolved but Infeasible
Resolved but Motivation = 0
Resolved and weakly responsive
```

因此 Complete Feeding Response Mode 最少需要：

```text
status
= ResolutionIncomplete
| ResolvedNonResponsive
| ResolvedResponsive

strength
= null            when ResolutionIncomplete
| 0               when ResolvedNonResponsive
| continuous > 0  when ResolvedResponsive
```

这里 `strength` 的具体数学公式仍未确定；probe 里的有界映射只用于验证 contract 拓扑。

## 3. Unknown != 0

### ResolutionIncomplete

只要 mode 的 required semantic 仍有 Unknown，例如：

- required target support / target value 未解析；
- required Feeding Motivation 未解析；
- TaskAffordance = Unknown；
- 其它 mode-local required input 缺失；

则：

```text
status = ResolutionIncomplete
strength = null
rollability = false
reason = required input unresolved
```

它不是低响应，也不是零响应。

### ResolvedNonResponsive

以下情况可以是“已知地不响应”：

- target 对该 mode 已知 invalid；
- TaskAffordance 已知 Infeasible；
- Target / Food Value 或 Feeding Motivation 在当前 resolved contract 下产生零 drive；
- 其它明确的 mode-local hard failure。

此时：

```text
status = ResolvedNonResponsive
strength = 0
```

因此 `null` 与 `0` 必须保留为不同语义。

## 4. Gating 与 continuous ranking 分工

### 硬 gating / blocking

当前 Working Contract 建议：

- Resolution incomplete → block；
- mode validity / required target semantics invalid → resolved nonresponsive；
- TaskAffordance = Infeasible：只有在 required physical task 已有独立 hard-feasibility contract，且该 contract 已知当前任务不可达时，才输出 resolved nonresponsive；`u_close ≥ 1` 在当前缺少 encounter geometry / reaction-window contract 时不单独满足这一条件；
- TaskAffordance = Unknown → resolution incomplete；
- Activity may change soft cost only after physically feasible Closing is established；it must not be folded into `InterceptSpeedLimit` or create a second hard gate。

### continuous ranking

在 mode 已合法、required semantics 已解析、TaskAffordance 不为 Infeasible 的情况下，以下量可继续影响 continuous strength：

- Target / Food Value；
- Feeding Motivation；
- Feasible vs Constrained 的 affordance 差异；
- 未来经过 admission 的 optional state valuation semantics。

因此 `Constrained` 不应默认等价于 hard fail。它可以仍为 ResolvedResponsive，只是 response strength 较低。

## 5. `C_mode` 是 resolved mode contribution，不是 resolution container

建议把 `C_mode` 限定为：

> 一个已经完整闭合的 mode 对 HitFish candidate / roll 的连续贡献值。

于是：

```text
ResolutionIncomplete
→ no C_mode

ResolvedNonResponsive
→ C_mode = 0

ResolvedResponsive
→ C_mode > 0
```

这比“任何 mode 都先给一个 coefficient”更安全，因为它避免把 Unknown 偷换成 neutral / zero coefficient。

最终交给 HitFish candidate 侧的对象应至少保留：

```text
mode_id
status
C_mode?        # only when resolved
reason / provenance
```

不要只传一个裸 float。

## 6. 多个 hypotheses / modes 何时可以 max

`max` 不是通用聚合。

只有同时满足下列条件时才允许：

1. 属于同一个 response family / sibling group；
2. 它们表示同一 actual opportunity 的替代解释或高度重叠的替代响应；
3. 每个 required sibling 都已经完整解析；
4. 选择更强 sibling 不会丢失另一条独立、可同时成立的 response channel。

例如同一个 actual lure presentation 同时支持 baitfish / crayfish 两份**替代 Feeding hypotheses**，若 contract 明确它们属于同一个 Feeding sibling group，并且两份都已闭合，则可以由最强完整 Feeding response 主导。

不能 max 的情况包括：

- 两个 mode 不是替代，而是可同时成立的独立行为通道；
- 某个 required sibling 仍为 ResolutionIncomplete；
- max 会掩盖另一个必须单独保留的风险、逃逸、攻击或非 feeding response；
- 只是因为数学上方便而把不同 owner / 不同意义的 scalar 放进同一个池子。

## 7. 未决 sibling 如何处理

本轮采用较保守的 closure contract：

> 对一个声明为“required exhaustive alternative set”的 sibling group，只要其中 required alternative 仍有 Unknown，group-level final `C_mode` 就保持 ResolutionIncomplete。

因此禁止：

```text
known baitfish response = 0.6
unknown crayfish response = ?
→ 偷偷 max = 0.6
→ 继续 roll
```

如果未来某个 sibling group 明确允许 partial resolution，则必须由 group contract 显式声明；不能默认这么做。

## 8. 与 HitFish candidate / roll 的接口

当前推荐接口不是：

```text
Interaction -> float C_mode -> roll
```

而是：

```text
Complete Feeding Response Mode
    ↓
ModeResponsePacket
{
  mode_id,
  status,
  C_mode?,
  reasons,
  provenance
}
    ↓
HitFish candidate / roll adapter
```

adapter 规则：

- `ResolutionIncomplete`：不可 roll，不当 0，不当 neutral；
- `ResolvedNonResponsive`：已知 contribution = 0；
- `ResolvedResponsive`：允许将 `C_mode` 作为该 mode 的已解析 contribution 进入候选/roll；
- 多 mode aggregation 必须先按 sibling / composition contract 处理，不能由 candidate 层重新猜语义。

Candidate / roll 层不应重新读取 Step 3 raw state、重新解释 prey semantics，或自行把 Unknown 补零。

## 9. 本轮 probe 已验证

本地 Python 实际运行通过：

```text
Final output contract probe passed:
categorical+continuous,
Unknown!=0,
gating,
sibling max,
incomplete blocks
```

具体反事实包括：

- Feasible 与 Constrained 都可保持 ResolvedResponsive，但 strength 有序；
- Infeasible → ResolvedNonResponsive + 0；
- Motivation Unknown → ResolutionIncomplete + null；
- Motivation resolved 0 → ResolvedNonResponsive + 0；
- `null != 0`；
- 两个完整明确替代 sibling 可 max；
- 一个 required sibling 未解析时 group final `C_mode` 被阻断。

## 10. 当前 Working Conclusion

Proposal C 到这里可以得到一个较完整的主干：

```text
ActualPresentation
→ prey-type / prey-state interpretation
→ sparse prey semantics

species × size cohort → InterceptSpeedLimit
+ fish-relative geometry / presentation facts
→ Closing feasibility
→ ResolvedTaskDemand
→ Activity-aware soft Closing cost
→ TaskAffordance

Mode Validity / Resolution
+ Target / Food Value
+ TaskAffordance
+ Feeding Motivation
+ optional admitted state valuation semantics
→ Complete Feeding Response Mode
→ ModeResponsePacket(status + C_mode?)
→ sibling/composition contract
→ HitFish candidate / roll adapter
```

其中：

- `Unknown` 不产生 scalar；
- resolved zero 与 unresolved 分开；
- categorical status 与 continuous strength 同时保留；
- `max` 只属于明确的 alternative sibling composition；
- HitFish candidate 层消费已解析结果，不重新发明 Interaction 语义。

## 11. 尚未闭合

本轮没有确定：

- `C_mode` 的生产数学公式；
- Feasible / Constrained 的具体数值映射；
- production threshold / calibration；
- 所有 response families 的 composition operator；
- 当前 HitFish Candidate Weight / Base Opportunity 等既有链路中，`C_mode` 最终具体插在哪个数学位置。

最后一项需要回到 HitFish 主链的 Candidate / Weight / Roll authority 上做接口对齐，而不能仅靠 Proposal C 自己决定。

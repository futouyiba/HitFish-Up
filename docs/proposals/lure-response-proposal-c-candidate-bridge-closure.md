# 方案 C｜Interaction → Candidate Resolver Bridge Closure

日期：2026-10-26  
状态：Working Proposal Evidence，非 Current，非生产参数。

## 1. 问题

Proposal C 已闭合到：

```text
Complete Response Modes
→ ModeResponsePacket(status + C_mode?)
```

剩余跨域问题是：`C_mode` 应如何进入现有 HitFish Candidate / Weight / Roll 主链。

本页不重新定义 Candidate Resolver 或 TrueRoll。接口必须服从现有 Current Owner。

可执行 probe：`../../prototypes/lure-response/proposal_c_candidate_bridge_probe.py`。

## 2. Current Authority 对齐

本轮对齐版本：Interaction / Capture Current v15（2026-08-28 17:24）；Candidate Resolver / Assembly Current v8（2026-08-28 20:28）；Candidate Pre-Roll Gameplay Policy Current v1（2026-08-28 14:51）；Candidate Weight Calibration Current v8（2026-08-28 22:49）。时间均为 Asia/Taipei。

### Interaction / Capture Current v15

Current 明确冻结：

```text
Complete Mode Resolver → C_mode
→ AggregateCompleteModes
→ captureRetention
→ CaptureResponsePacket
```

只有完整闭合的 `C_mode` 可以参与 mode aggregation。Interaction 对 Candidate Resolver 输出 Opportunity-owned canonical support 上的 typed、support-aligned `C_i,j` / equivalent result。

因此 `C_mode` 是 Interaction 内部 complete-mode contribution。Candidate Resolver 不应直接逐 mode 消费它，更不应重新解释其 prey / motivation / task semantics。

### Candidate Resolver / Assembly Current v8

Current 已冻结 Native composition：

```text
Spatial Native Supply Measure dM_i(s,t)
× Interaction CaptureRetention C_i(s,p,t)
→ retained Native Candidate measure dQ_i = C_i · dM_i
→ Opportunity Reduce
→ W_i^opp
```

scalar specialization：

```text
q_i,j = L_i,j × C_i,j
W_i^opp = Σ_j α_j · q_i,j
```

这是 retention / thinning 语义要求的 operator，不是额外调参系数。

### Candidate Pre-Roll Gameplay Policy Current v1

Gameplay Policy 在 `NativeCandidateSnapshot` 之后作用：

```text
NativeCandidateSnapshot
→ Explicit Gameplay Policy
→ EffectiveCandidateSurface / ResolutionCondition
→ Canonical TrueRoll
```

因此 Native Interaction response 不得再次包装成 MassTransform、Eligibility tweak 或匿名 Candidate Weight modifier。

### Candidate Weight Calibration Current v8

Calibration Current 将 Native baseline 明确为 raw Spatial + raw Capture + Roster / World Presence；Calibration 不取得 Interaction Cause authority。因此 `captureRetention` 属 Native Candidate Assembly，不是 `W_i^opp` 之后的 calibration correction。

## 3. Canonical Bridge

当前推荐桥接：

```text
Proposal C complete modes
        ↓
ModeResponsePacket[]
        ↓
Interaction-owned mode composition
        ↓
CaptureResponsePacket
├─ status
└─ captureRetention C_i,j
        ↓
Candidate Resolver
Spatial L_i,j × Interaction C_i,j
        ↓
q_i,j
        ↓ Opportunity-owned Reduce
W_i^opp
        ↓
NativeCandidateSnapshot
        ↓
optional explicit Pre-Roll Gameplay Policy
        ↓
EffectiveCandidateSurface
        ↓
Canonical TrueRoll
```

Proposal C 的 `C_mode` 因而不是：

- Base Opportunity Intensity；
- Spatial Distribution Weight；
- Candidate Weight 本身；
- Pre-Roll Gameplay MassTransform；
- `W_i^opp` 之后再乘一次的 ResponseCoeff。

它先由 Interaction 聚合为 canonical `captureRetention`，之后只在 Candidate Resolver 的 native retention join 中使用一次。

## 4. Typed status 对齐

Proposal C final-output contract 与 Candidate Resolver 的 Resolve-Before-Roll 边界相容：

### ResolutionIncomplete

```text
Mode / required Interaction input unresolved
→ no canonical captureRetention
→ Candidate support unresolved
→ CandidateSnapshot ResolutionIncomplete / NotRollable
```

不能补成 0 或 1。

### ResolvedNonResponsive

若 Interaction semantic contract 已合法闭合为 terminal / resolved non-response：

```text
captureRetention = 0
→ q = L × 0 = 0
```

这是 resolved native zero，不是 Unknown short-circuit。

### ResolvedResponsive

```text
0 < captureRetention ≤ 1
→ q = L × C
```

它只 thinning authoritative Native Supply。若某设计需要 `>1` 的玩家增益，不应把 `captureRetention` 改造成 supply amplification；应检查 Cause 属于 Spatial Supply 还是显式 Gameplay Policy。

## 5. Mode composition 必须发生在 Interaction 内

Candidate Resolver Current 要求每 candidate/support 消费一个 resolved Interaction output。故：

```text
C_mode[]
→ Interaction aggregation
→ C_i,j
```

必须先于：

```text
L_i,j × C_i,j
```

Candidate Resolver 不拥有：

- Feeding / Defense mode meaning；
- sibling overlap；
- max / mixture / union 的 mode routing semantics；
- Target / Motivation / TaskAffordance。

因此 Proposal C 中的 sibling max / completeness contract 仍属于 Interaction。只有 aggregate 后的 typed `C_i,j` 穿过跨域 seam。

## 6. Double-count guard

错误结构：

```text
L × C
→ W_native
→ W_native × C
```

会把同一 Interaction cause 结算两次。

示例：

```text
L = 0.75
C = 0.80
正确：q = 0.60
错误再次乘 C：0.48
```

这不是 calibration 差异，而是 Cause ownership violation。

同理，以下结构默认错误：

```text
NativeCandidateSnapshot
→ GameplayPolicy(ResponseCoeff = C)
```

因为 CandidateSnapshot 已经包含 Native Interaction retention。

## 7. 与 Base Opportunity / Spatial 的关系

Base Opportunity / Native Supply 与 Interaction response 是并行 Cause：

```text
Native Supply / Spatial
        ─┐
         ├→ Native Retention Join → Candidate mass
Interaction Response
        ─┘
```

因此不要说：

> `C_mode` 修正 Base Opportunity。

更准确的是：

> Base Opportunity / Spatial 先描述 native supply；Interaction 描述这份 supply 在当前 presentation 下有多少被 response retained；Candidate Resolver 在 canonical support 上执行 join。

这能保持：更多鱼 / 聚鱼归 Spatial；玩家 presentation / fish response 归 Interaction。

## 8. Executable probe result

本轮已在 ChatGPT Python 环境实际执行等价 probe，通过：

```text
Candidate bridge probe passed
```

断言包括：

1. declared alternative sibling modes 先在 Interaction 内 compose；
2. Candidate Resolver 只消费 aggregate 后的 `captureRetention`；
3. `L × C` 只执行一次；
4. resolved zero 合法进入 native zero；
5. Interaction Unknown 保持 ResolutionIncomplete；
6. 再次乘 C 会产生可检测的 squared attenuation。

仓内 reference probe 保存同一 topology test；数值仅为说明，不是生产公式或 calibration。

## 9. 当前 Working Conclusion

Proposal C 到现有 HitFish 主链的 seam 可以暂时收口为：

```text
ModeResponsePacket[]
→ Interaction CaptureResponsePacket(C_i,j + typed status)
→ Candidate Resolver: dQ_i = C_i · dM_i
→ W_i^opp
→ NativeCandidateSnapshot
→ optional explicit Gameplay Policy
→ TrueRoll
```

因此 Proposal C 自身不再需要设计 Candidate Weight 插入公式。

## 10. 仍未闭合

这次没有证明或冻结：

- `C_mode` 的生产数学函数；
- Feasible / Constrained 到 `C_mode` 的生产映射；
- Feeding / Defense 等所有 mode family 的最终 aggregation operator；
- production calibration；
- runtime struct 名称与 hot-path representation。

这些仍由对应 Interaction / Candidate / Calibration Owner 承接。

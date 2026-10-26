# Proposal C：Prey Support → Feeding Mode Bridge

> Status: Working Closure / non-production numeric mapping
>
> Scope: prey interpretation evidence → complete feeding-mode contribution

## 结论

`prey support` 不能直接解释成猎物身份概率，也不能归一化后做 mixture。

第一版推荐把它当作**某个 prey interpretation 对 feeding response 的解释资格 / 识别保留度来源**：

```text
prey support
→ RecognitionProjection
→ Interpretation Retention R
```

然后先在“假定该 prey interpretation 成立”的条件下，完成鱼侧响应：

```text
FoodValue
+ StateTriggerValue
- TaskCost
- WillingnessThreshold
→ DecisionMargin
→ C_conditional
```

最后：

```text
C_prey_mode = R × C_conditional
```

其中 `R` 不是“它有 R 的概率真的是这类猎物”，而是“这套 prey interpretation 有多大资格贡献 feeding response”。

`prey support` 与 `R` 不应默认恒等。support 当前只是解释证据标尺；若未来 production 采用线性或非线性 `RecognitionProjection`，应由体验与回归 fixture 单独校准。

## 为什么不能只做 admission gate

若只设置：

```text
support > threshold
→ mode admitted
```

则 `support=0.41` 与 `support=0.90` 一旦都过门，就会得到相同的 conditional feeding response。

这会丢掉第2步已经明确表达的“按这种猎物解释的证据强弱”。

因此 support 不能只决定“有没有这个 mode”；已知且非零时，它还必须影响 mode 最终贡献。

## 为什么不直接改 FoodValue

`FoodValue` 回答：

> 如果目标按该 prey interpretation 被识别，这条鱼认为这种目标有多值得吃？

`prey support` 回答：

> 当前 presentation 有多少依据可以按该 prey interpretation 理解？

两者不是同一个 Cause。

因此第一版不推荐：

```text
FoodValue *= prey_support
```

这会把“目标身份解释强度”与“鱼对这种食物的价值判断”混成一个字段。

同理，也不推荐让 support 改写 Motivation Threshold。

## 为什么在 ResponseProjection 之后乘 R

推荐：

```text
conditional prey-mode evaluation
→ DecisionMargin
→ C_conditional
→ × R
→ C_prey_mode
```

而不是把 support 先塞进 FoodValue / TaskCost / Threshold。

这样可以保持：

1. Fish-side decision 的语义仍然是“若按这种 prey interpretation 识别，这条鱼会怎么反应”；
2. prey evidence 强弱只控制该 interpretation 能贡献多少；
3. `Reject`、Task hard-zero、ResolutionIncomplete 等 typed semantics 不被 support 偷换；
4. StateTriggerValue 也自然被同一个 `R` 约束，不会出现“几乎不像小鱼，却因为一次 dart 获得完整 baitfish trigger”的问题。

## Typed status

### NoMatch / known zero support

若某 prey 已在评价范围内，结果明确为无适用证据：

```text
prey support = NoMatch / 0
→ interpretation unsupported
→ C_prey_mode = 0
```

这里的原因应保留为 `InterpretationUnsupported` 或等价 provenance。

它不等于：

```text
FoodValue Reject
```

前者是“这个 presentation 不支持把它看成该 prey”；后者是“即使是该 prey，鱼也明确不把它当食物目标”。

### Unknown support

```text
prey support = Unknown
→ Recognition unresolved
→ no scalar C_prey_mode
```

不能补成 0。

若该 prey mode 属于 required sibling 集合，则继续沿用既有 completeness rule：required Unknown 不得被偷偷忽略后继续 roll。

## 多 prey interpretation 如何 composition

同一个物理拟饵可能同时得到：

```text
baitfish support = 0.90
crayfish support = 0.75
```

这不表示：

```text
90% 是 baitfish
75% 是 crayfish
```

也不表示两个独立 feeding opportunity。

在没有独立 synergy 证据前，这些 prey interpretations 应默认声明为**同一个物理 feeding opportunity 的 alternative sibling interpretations**。

因此第一版推荐：

```text
C_feed = max(C_baitfish, C_crayfish, ...)
```

而不是：

```text
sum
normalized weighted average
1 - product(1-C)
```

原因：后面三者都会让“同时像多种猎物”天然制造额外 response mass，等价于把同一个拟饵算成多次独立摄食机会。

`max` 的语义是：鱼可以沿最有利的 prey interpretation 响应该目标，但默认不因多重解释而叠加多份 opportunity。

如果以后有明确策略故事证明“跨 prey cue 的组合本身产生独立 synergy”，应单独经过 admission gate，而不是静默从 `max` 改为 union / sum。

## 与现有 sibling max 规则的关系

本页不是新增一个 Candidate-side operator。

它只是进一步明确 Interaction 内的 sibling declaration：

```text
同一物理 presentation
+ 多个互为替代的 prey interpretations
→ alternative sibling feeding modes
→ Interaction-owned max composition
```

只有完成 composition 后的 `captureRetention` 才交给 Candidate Resolver。

## Working topology

当前 Feeding 主链可写成：

```text
ActualPresentation
→ prey support map
→ prey-conditioned current state

for each prey interpretation p:
    support_p
    → RecognitionProjection
    → R_p

    TargetRelation(fish, prey_p)
    → FoodValue_p

    prey-conditioned state_p
    → StateTriggerValue_p

    presentation task + FunctionalCapacity
    → latent-angle task evaluation
    → DecisionMargin_p(theta)
    → ResponseProjection
    → C_conditional_p(theta)
    → E_theta[C_conditional_p(theta)]

    R_p × conditional response
    → C_prey_mode

alternative prey sibling composition
→ C_feed = max_p(C_prey_mode)

other complete response modes
→ Interaction composition
→ captureRetention
→ Candidate Resolver: dQ = C · dM
```

## Rejected shortcuts

### 1. `support` 直接作为 probability

Rejected。

support map 不归一化；多项可同时很高。当前契约明确它是解释证据强度，不是身份概率。

### 2. `FoodValue *= support`

Rejected as default topology。

会混淆 prey interpretation 与 fish food valuation。

### 3. support 只作 hard admission threshold

Rejected as default。

会把 threshold 以上所有证据强度压成相同效果，并制造人为跳变。

### 4. 多 prey mode 求和 / union

Rejected as default。

会重复计算同一物理 feeding opportunity。

## Open items

当前仍未冻结：

- `RecognitionProjection(support) -> R` 的 production curve；
- 是否所有 prey family 共用同一 projection；
- support 的 production numeric anchors 是否需要重标定；
- 是否存在值得单独 admission 的 cross-prey synergy；
- prey hierarchy（例如 fish / shad 子类）最终如何声明 mutually-exclusive / overlapping siblings。

这些属于后续 calibration / interaction semantics，不从本页 probe 数字直接晋升。

## Probe

对应 executable probe：

`prototypes/lure-response/proposal_c_prey_support_bridge_probe.py`

probe 只验证 topology：

- support 不要求和为 1；
- stronger known support 可产生更高 mode contribution；
- NoMatch 与 Unknown 区分；
- alternative prey readings 默认 max；
- Candidate 之前不产生多份 feeding opportunity。

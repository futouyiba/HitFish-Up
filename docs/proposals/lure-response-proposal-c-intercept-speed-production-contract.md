# Proposal C｜InterceptSpeedLimit 生产 Contract

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`InterceptSpeedLimit` 表达当前 species / size 在参考状态下，短时追赶中允许 Closing feasibility 判断使用的结构能力上限。

第一版建议把它作为 `Species × Size` 的 Bake 结果：

```text
SpeciesConfig
├─ ReferenceLength
├─ ReferenceInterceptSpeed
└─ SizeScalingRule

Species × SizeCohort
├─ RepresentativeLength
└─ BakedInterceptSpeedLimit
```

Response 只消费：

```text
InterceptSpeedLimit
```

不在 Response 内重新读取 species、size、temperature、oxygen、period、Activity 等原因。

当前仓内未找到已有 Current / production `InterceptSpeedLimit` 合同，因此本页只提供 Proposal C Candidate contract，不声明已承接现行 authority。

## 2. 语义边界

`InterceptSpeedLimit` 不是：

- 文献里的绝对最高 burst speed；
- cruising speed；
- critical swimming speed；
- 当前鱼的实时游速；
- 当前 willingness / Motivation；
- 当前 Activity。

它是本项目为短时 Closing feasibility 提供的结构能力尺度。

Response 中：

```text
q = lure_speed_relative_to_water / InterceptSpeedLimit
u_close(theta) = max(0, q * directional_cosine(theta))
```

若：

```text
u_close(theta) >= 1
```

该 latent bearing 局部 hard infeasible。

因此 `InterceptSpeedLimit` 决定 feasibility 边界；`K_close` 决定边界以内的 soft burden。两者不能互相代偿。

## 3. Fish Condition 不修改 InterceptSpeedLimit

当前 Proposal C 已把 Fish Condition 中的 `Activity` 定位为执行状态：

```text
Activity
→ Closing soft-cost multiplier
```

因此第一版禁止：

```text
InterceptSpeedLimit *= Activity
```

或：

```text
Activity low
→ lower speed limit
→ higher ClosingCost again
```

否则同一低 Activity 会：

1. 先把更多 bearing 推入 hard infeasible；
2. 再提高剩余 bearing 的 soft cost。

这会把“当前不愿 / 不积极追”误写成“物理上追不上”，并造成双重处罚。

如果未来确有急性生理失能需要改变硬能力边界，应建立具名 hard-cap state / capability modifier；不能复用通用 Activity。

## 4. Size scaling 的最小模型

第一版推荐使用 reference-normalized power rule 作为**可校准拓扑**：

```text
InterceptSpeedLimit(L)
= ReferenceInterceptSpeed
  × (L / ReferenceLength)^alpha
```

其中：

- `ReferenceLength > 0`；
- `ReferenceInterceptSpeed > 0`；
- `alpha` 是 size scaling 参数；
- `L` 是本次 Bake 使用的代表长度。

这只是 Working topology，不冻结生产 `alpha`。

选择 power rule 的原因：

- reference 点语义清楚；
- 单调性容易检查；
- 不为每个 cohort 直接手填一套独立 speed；
- 允许未来用真实 fish-locomotion evidence 或项目体验标定 size effect；
- 比每个 species × cohort 自由配值减少 authoring 漂移。

第一版不准入高阶多项式、piecewise spline 或多个自由 exponent，除非 coverage / residual evidence 证明单一 rule 不足。

## 5. alpha 的 authoring 边界

当前不建议 200 个 species 每个独立手填一个 `alpha`。

优先顺序：

1. 若有权威数据支持统一 size-scaling family，使用共享 `alpha`；
2. 若真实覆盖显示不同 locomotor group 存在稳定系统差异，可引入少量 named scaling profile；
3. species-specific override 只用于明确异常；
4. 若大量 species 都需要 override，应重构 scaling profile，而不是接受海量自由参数。

这与 DietArchetype 的治理思路一致：先购买少量稳定结构，再用 sparse override 处理真实异常。

## 6. RepresentativeLength 来源

Response 若合法拥有当前个体真实 length，并且该信息在 response resolution 之前已经确定，则优先使用真实 length：

```text
actual individual length
→ InterceptSpeedLimit(actual length)
```

但不能为了 Response 临时生成一个“假个体长度”。

若 response 发生时只有 `Species × SizeCohort`，则 Bake 使用 `RepresentativeLength`。

推荐来源优先级：

```text
1. 当前 cohort 实际生成长度分布的 median
2. 当前 generation contract 的显式 reference / representative length
3. cohort authoring midpoint（仅当与真实生成分布相容）
4. species-wide reference length 作为最后 fallback
```

不推荐默认使用 arithmetic mean，因为长尾 generation distribution 可能让均值偏离典型个体；median 更适合作为代表性 Closing 能力锚点。

如果生成系统只有离散 size cohort，没有连续长度分布，则直接使用该 cohort 的权威 representative length。

## 7. Cohort 内 variation 的处理

不要一开始就把 cohort 内长度分布积分进 Response。

第一版：

```text
cohort
→ RepresentativeLength
→ one baked InterceptSpeedLimit
```

只有当验证显示 cohort 内 size variation 会系统性改变：

- hard-feasible bearing 占比；
- lure-speed ranking；
- player-learnable strategy；
- response 分布；

才升级模型。

优先升级方式是：

```text
split cohort
```

而不是马上在 runtime 对 hidden length distribution 做积分。

原因：split cohort 更可解释、更容易 Bake、测试和 Explain。

## 8. 数据来源与外部证据

外部 fish locomotion 资料可以帮助确定：

- species / locomotor group 的相对能力排序；
- size scaling 的方向与大致形状；
- 是否需要多个 scaling profile。

但不能机械把：

- burst speed；
- sustained speed；
- critical swimming speed；
- laboratory sprint；

直接等同于本项目 `InterceptSpeedLimit`。

项目量是一个 gameplay-facing effective limit，需要和 lure-speed distribution、latent-bearing prior、Closing calibration 联合标定。

因此外部资料提供 evidence / ordering / plausible range，不自动成为最终生产参数。

## 9. 与 lure speed 的参考系

`InterceptSpeedLimit` 必须和 lure speed 使用同一 reference frame。

当前 Proposal C 推荐：

```text
lure_speed_relative_to_water
/
InterceptSpeedLimit_relative_to_water
```

不能把 world-space lure speed 除以 water-relative fish capacity。

若未来流场系统改变 reference-frame contract，必须两边一起迁移。

## 10. Calibration 顺序

生产标定顺序固定为：

```text
Species / size locomotion evidence
→ ReferenceLength / ReferenceInterceptSpeed / SizeScalingRule
→ Species × Cohort RepresentativeLength
→ Baked InterceptSpeedLimit distribution
→ representative lure-speed distribution
→ q distribution
→ RelativeBearingPrior dimensionality
→ K_close
→ ActivityCostMultiplier integration
→ combined burden stress test
```

禁止倒序用 `K_close` 去补偿错误的 InterceptSpeedLimit。

## 11. Coverage / regression 检查

至少监控：

```text
q distribution by species/cohort
P(q > 1)
hard-infeasible bearing share
median / p90 ClosingCost
speed-limit rank by species/cohort
cohort split sensitivity
```

重点异常：

- 普通 lure retrieve 对大量正常 predator species 都 `q >> 1`；
- 几乎所有 lure 对所有 species 都 `q << 1`；
- size 增长造成无依据的巨大能力倍增；
- 同一 cohort 内真实 length variation 会把 feasibility ranking 翻转；
- 为了让玩法正常，只能把 `K_close` 调到极端值。

出现这些情况应回查 speed contract，而不是末端修 projection。

## 12. Unknown / provenance

生产数据应保留 provenance：

```text
InterceptSpeedProfile {
  reference_length
  reference_intercept_speed
  scaling_profile
  source / provenance
  confidence / review status
}
```

必要输入 Unknown 时：

```text
InterceptSpeedLimit = Unknown
→ Closing resolution incomplete
```

不能自动给所有鱼同一个默认 speed。

如果产品明确允许某类 fish 使用共享 fallback profile，必须把它作为已声明的 fallback rule 和 provenance，而不是 runtime silent default。

## 13. 当前 OPEN

- `ReferenceInterceptSpeed` 的生产来源与 authoring pipeline；
- `alpha` 是全局共享、按 locomotor profile，还是少量 species override；
- 生产 species / cohort 的真实 length distribution 来源；
- representative lure-speed distribution；
- RelativeBearingPrior 最终采用 Horizontal2D 还是 Full3D；
- ActivityCostMultiplier 范围由 Cowork 分支闭合；
- `K_close` production calibration。

本页只闭合 `InterceptSpeedLimit` 的 owner、size-scaling topology、representative-length 规则和 calibration 顺序，不冻结生物学参数或最终 gameplay 数值。

# Proposal C｜ReferenceInterceptSpeed 生成方法

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`ReferenceInterceptSpeed` 不应直接抄真实鱼类的某一个游泳速度指标，也不应由 200 个鱼种逐条独立拍值。

第一版推荐三层生成：

```text
external locomotion evidence
→ LocomotorArchetype / evidence profile
→ gameplay calibration
→ ReferenceInterceptSpeed
```

其中：

- 外部数据负责提供合理范围、相对排序与 size-scaling 证据；
- `LocomotorArchetype` 负责把稀疏、异质的真实资料压缩成少量共享 profile；
- gameplay calibration 负责把这些 profile 映射到本项目短时截获语义下的最终 `ReferenceInterceptSpeed`。

`ReferenceInterceptSpeed` 是项目内部模型参数，不等于自然界里的 `Ucrit`、burst speed、cruising speed 或最大游速。

## 2. 为什么不能直接使用 Ucrit / burst speed

真实文献里的游泳速度指标回答的不是同一个问题。

例如：

```text
Ucrit
→ prolonged / critical swimming performance

burst speed
→ 很短时间内的高强度游泳能力

ReferenceInterceptSpeed
→ Proposal C 中 reference fish 在短时截获语境下的结构能力边界
```

三者相关，但不能直接等同。

已有鱼类研究表明，绝对游速通常随体长增加，但不同科、不同种的 scaling slope 与 baseline 差异显著；因此 species identity / taxonomic group 与 body length 都有解释力。真实资料可用于约束模型，但不足以定义本项目的唯一参数。

## 3. 外部证据的角色

外部 locomotion evidence 只购买以下信息：

### 3.1 相对排序

例如：

```text
fast pursuit-oriented fish
> generalist swimmer
> slow / maneuver-oriented benthic fish
```

若多个来源都支持这种相对排序，可用于 archetype placement。

### 3.2 合理区间

真实数据可以帮助拒绝明显不合理的项目值，例如某普通小型淡水鱼被配置成远高于大型高速掠食鱼。

但该区间仍需转换到项目 `ReferenceInterceptSpeed` 语义，而不是直接复制一个文献数值。

### 3.3 size scaling

已有研究支持绝对游速通常随体长增加，并常用 power-law / allometric 形式描述：

```text
U ∝ L^alpha
```

但 `alpha` 不应全鱼类共用，也不应默认等于文献中某个 Ucrit 回归斜率。

外部研究只提供 locomotor group 的 scaling evidence；项目仍需用 gameplay probe 检查 scaling 后对 `q = lure_speed / InterceptSpeedLimit` 的影响。

## 4. LocomotorArchetype

为了约 200 个鱼种的生产可维护性，第一版推荐少量共享 archetype，而不是每种鱼独立 author 全套速度参数。

示意：

```text
LocomotorArchetype
├─ HighSpeedPursuer
├─ GeneralistSwimmer
├─ BurstAmbushPredator
├─ ManeuverOriented
└─ SlowBenthic
```

这些名称只是 Candidate 示例，不是最终 catalog。

每个 archetype 可持有：

```text
reference speed seed
size scaling profile
allowed evidence range
provenance
```

Species 默认继承一个 archetype；只有存在稳定、明确证据时才写 sparse override。

如果大量 species 需要 override，说明 archetype catalog 或分组规则失败，而不是接受 200 条鱼逐条调参。

## 5. BurstAmbushPredator 为什么应和 HighSpeedPursuer 分开

第一版不能只按“最高速度快不快”分组。

例如伏击型捕食鱼可能具备较强短时爆发，却不意味着长期巡航 / pursuit profile 与高速巡游鱼相同。

Proposal C 的 `ReferenceInterceptSpeed` 更接近短时 closing capability，所以 burst evidence 有价值；但又不能把一次极端实验 burst maximum 当 reference。

因此：

```text
burst capability
→ archetype evidence
→ gameplay-calibrated reference intercept speed
```

而不是：

```text
measured maximum burst speed
→ ReferenceInterceptSpeed
```

## 6. Species / Cohort 生产结构

推荐：

```text
LocomotorArchetype
→ reference-speed seed + scaling profile

Species
→ archetype assignment
→ optional sparse species override

SizeCohort
→ RepresentativeLength

Bake
→ ReferenceInterceptSpeed(species)
→ InterceptSpeedLimit(species, cohort)
```

与上一页 contract 对齐：

```text
InterceptSpeedLimit(L)
= ReferenceInterceptSpeed
  × SizeScalingRule(L / ReferenceLength)
```

`ReferenceInterceptSpeed` 的 reference length 必须显式记录；不能把某来源 20cm 个体的速度无说明地当成整个 species baseline。

## 7. 推荐的数据优先级

同一 species 的 locomotion evidence 建议按以下优先级使用：

1. species-specific、尺寸与实验语境清楚的短时 / burst / acceleration evidence；
2. species-specific Ucrit / prolonged performance，用于相对能力和 scaling 辅助；
3. congeneric / family-level locomotion evidence；
4. body form / locomotor ecology 对应 archetype；
5. gameplay-only fallback archetype。

这只是 evidence 优先级，不表示第1项可以直接成为项目数值。

每一层都应记录 provenance。

## 8. Gameplay Calibration 才决定最终数值

最终 `ReferenceInterceptSpeed` 必须经过项目代表性 lure-speed basket 校准。

目标不是让速度“像论文”，而是使：

```text
ordinary lure operation
→ ordinary q distribution
→ ordinary Closing burden

high-speed presentation
→ 明显提高 q / hard-infeasible bearing share

slow / pause presentation
→ 明显降低 Closing burden
```

同时保留 species / size 的相对 locomotor 差异。

因此 calibration 顺序：

```text
external evidence
→ archetype placement
→ initial speed seed
→ representative lure-speed basket
→ q distribution
→ latent-bearing integration
→ Closing response behavior
→ adjust project ReferenceInterceptSpeed
```

最终项目值允许偏离自然实验速度，只要：

- 偏离有 gameplay calibration 解释；
- species / archetype 相对排序仍有证据支持；
- 不越出明显不可接受的生物学合理区间；
- Explain / provenance 能说明这是 project-calibrated value。

## 9. 不推荐直接用 BL/s 作为运行时主值

Body-lengths-per-second 对跨尺寸比较很直观，但运行时 Closing 使用 lure 与 fish 的同一绝对速度参考系。

因此生产输出仍推荐绝对速度：

```text
m/s
```

BL/s 可以作为 authoring / validation 辅助量，用于发现异常 scaling。

例如：

```text
absolute speed 随尺寸上升
relative BL/s 可能下降
```

两者并不矛盾。

## 10. Unknown / evidence gap

缺少 species-specific 游泳资料时：

```text
missing species evidence
≠ speed = 0
≠ arbitrary manual value
```

而是：

```text
species
→ resolved locomotor archetype
→ inherited project-calibrated baseline
```

只有连 archetype placement 都无法判断时，才是 authoring `NotConfigured / Unknown`。

不要把资料缺失当成运行时 Unknown；这是生产数据管线应该在 Bake 前解决的问题。

## 11. 验收指标

真实 200 species 数据接入后至少检查：

```text
archetype coverage rate
species override rate
speed distribution by archetype
BL/s distribution by size cohort
q distribution by species/cohort
hard-infeasible bearing share
ordinary Closing burden distribution
```

高 override rate 表示 archetype 失败。

若某 archetype 的 speed ranges 与另一 archetype 几乎完全重叠且没有不同策略表现，应考虑合并。

若某一 archetype 内存在稳定双峰并造成大量 override，应考虑拆分。

## 12. 当前 OPEN

- 最终 LocomotorArchetype catalog；
- 外部 locomotion evidence 数据源与批量采集流程；
- 每个 archetype 的 initial speed seed；
- size-scaling profile / alpha；
- reference length 规范；
- 代表性 lure-speed basket；
- gameplay calibration 的 q target distribution；
- 2D / 3D RelativeBearingPrior 裁定；
- 最终 `K_close`。

本页冻结数据生成架构与证据边界，不冻结任何鱼种的 production speed。
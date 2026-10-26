# Proposal C｜DietArchetype Contract

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`DietArchetype` 是 BaseDietAffinity 的 authoring / data-production helper，不是 runtime 生物学对象。

第一版建议从 5 个基础 archetype 起步：

```text
Piscivore
MacroInvertivore
MicrofaunaFeeder
Omnivore
HerbivoreDetritivore
```

另保留一个候选扩展：

```text
MixedPredator
```

只有 coverage test 证明大量 species / cohort 长期同时以 finfish 与大型无脊椎为高价值目标、且用 `Piscivore + sparse override` 会产生较高 override-rate 时，才正式加入 `MixedPredator`。

这套 archetype 不是自然分类学。它只为项目稳定的 operational prey-family catalog 提供默认关系。

## 2. 为什么先压到 5 类

公开淡水鱼生态研究常反复使用几类粗 trophic guild：

- piscivore / predator；
- invertivore / insectivore / micro-carnivore；
- planktivore / zooplanktivore；
- omnivore；
- herbivore / detritivore。

不同研究会进一步拆 benthivore、zoobenthivore、aquatic insectivore 等，但这些拆分有时混入 habitat / foraging-zone 信息。

本项目已经把空间、水层和 prey-state 交给其它 owner，因此 `DietArchetype` 不应复制 `benthic / pelagic / surface` 之类空间语义。

## 3. Archetype 只提供默认 relation

Archetype 不输出胃含物比例，也不要求 prey-family 值和为 1。

作者侧使用 relation class：

```text
Preferred
Good
Marginal
Poor
Reject
Unknown / NotConfigured
```

Bake 再投影到统一 continuous BaseDietAffinity anchor。

因此：

```text
DietArchetype
→ default relation per prey family

Species / Cohort
→ most-specific sparse override

Bake
→ BaseDietAffinity
```

Species / Cohort override 是替换，不与 archetype 数值继续相加或相乘。

## 4. 第一版 archetype 语义

### 4.1 Piscivore

回答：

> 参考上下文下，以鱼类猎物作为长期主要动物性目标的鱼。

Working 默认排序应满足：

```text
Finfish
> MacroCrustacean / Amphibian / other macro animal prey
> Insect / WormLikeInvertebrate / Mollusk / Microfauna
```

但本页不冻结具体 relation class。

`Piscivore` 不代表只吃鱼。大型甲壳类、两栖类等可以是合法的 `Good / Marginal`，具体由模板和 species override 决定。

### 4.2 MacroInvertivore

回答：

> 参考上下文下，以可独立识别的大型无脊椎动物作为主要摄食目标的鱼。

通常重点覆盖：

```text
MacroCrustacean
Insect
WormLikeInvertebrate
Mollusk
```

其中哪一类是 Preferred 不由 archetype 名预先决定。

如果 coverage test 显示大量鱼稳定分成“crustacean-dominant”和“insect-dominant”，并导致高 override-rate，再考虑拆 archetype；首版不预拆。

### 4.3 MicrofaunaFeeder

回答：

> 参考上下文下，以 zooplankton、microcrustacean、微型 larval animal prey 等 operational microfauna 为主要摄食目标的鱼。

主要价值：

- 给 planktivore / zooplanktivore 提供稳定模板；
- 避免把 copepod 等因分类学关系同时塞进 `MacroCrustacean`；
- 允许成长阶段从 MicrofaunaFeeder 转向其它 archetype。

### 4.4 Omnivore

回答：

> 长期食谱跨越多个 prey / plant family，且没有单一动物性 family 稳定占据明显主导的 generalist。

`Omnivore` 不是“所有东西都 Good”。

它只表示：

- 多个 family 合法进入食谱；
- 默认 profile 比专食型更宽；
- 仍允许明确的 Preferred / Marginal 差异。

如果把 Omnivore 做成全表高值，会吞掉 DietaryShift、species override 和玩家选饵差异，因此禁止这种默认。

### 4.5 HerbivoreDetritivore

回答：

> 参考上下文下，主要依赖 PlantAlgae / Detritus 等非动物食物来源的鱼。

它主要服务全局 diet / bait / natural-food 系统，不意味着所有 lure-response path 都会消费该 archetype。

动物 prey family 可以是 Poor / Marginal / Reject / Unknown，但必须按具体 evidence 决定，不因 archetype 名自动 hard Reject。

## 5. 为什么暂不设 Benthivore

`Benthivore / Zoobenthivore` 在生态研究中是合法 trophic guild，但它混合了：

```text
吃什么
+
通常在哪里吃
```

本项目已将位置、水层、结构、底质等事实交给 spatial / prey-state owner。

因此首版不直接加入：

```text
BenthicInvertivore
SurfaceFeeder
PelagicPredator
```

如果未来 coverage test 发现两个 species 对同一 prey-family profile 很接近，但必须靠“底栖来源”才能区分 diet affinity，优先检查是不是 prey-family catalog / trait owner 需要增强，而不是先加 habitat-archetype。

## 6. MixedPredator 的 admission gate

`MixedPredator` 不是默认基础类。

只有满足以下条件时才加入：

1. 多个 species / cohort 都长期表现为 `Finfish` 与 `MacroCrustacean`（或其它大型 animal prey）同时接近主食；
2. 用 `Piscivore` 或 `MacroInvertivore` 都需要多项稳定 override；
3. 这种差异不是季节性的 DietaryShift；
4. 这种差异不是纯 prey-size 造成；
5. 新 archetype 能显著降低 override-rate，而不只是换名字。

否则继续：

```text
base archetype + sparse override
```

## 7. Archetype 不负责的事情

`DietArchetype` 不负责：

- prey availability；
- FeedingMotivation；
- Activity；
- Wariness；
- DietaryShift；
- prey size fit；
- 当前 presentation support；
- habitat / water layer；
- 当前季节里“今天更想吃什么”。

这些由其它 owner 处理。

## 8. Species / Cohort 映射规则

第一版 production workflow：

```text
species / cohort diet evidence
        ↓
choose nearest DietArchetype
        ↓
compare evidence vs archetype defaults
        ↓
write only stable sparse overrides
```

如果成长阶段发生系统性食性切换，例如：

```text
juvenile: MicrofaunaFeeder
adult: Piscivore
```

允许 cohort 改 archetype。

如果只是：

```text
adult 更偏 Finfish
但整体仍是 MacroInvertivore / Omnivore
```

优先用 sparse override 或 size preference，不轻易切 archetype。

## 9. Coverage test 的验收指标

真正拿到约 200 鱼种数据后，至少统计：

```text
archetype coverage rate
override rate per species
override rate per prey family
cohort archetype-switch rate
Unknown / NotConfigured rate
new-archetype request frequency
```

Working guardrail：

> 如果大量 species 在大量 prey family 上需要 override，说明 archetype 或 prey-family 粒度有问题。

不要把高 override-rate 当成正常生产成本。

建议同时观察：

- 某个 archetype 是否实际只覆盖极少数鱼；
- 某个 prey family 是否几乎所有 species 都 override；
- 某两种 archetype 是否 profile 几乎相同。

这些都应触发 archetype merge / split review。

## 10. Working default profile 的使用原则

在全量 coverage 前，不冻结具体 relation matrix。

可以做 probe matrix，但必须标 Working，例如：

```text
Piscivore:
  Finfish = Preferred
  MacroCrustacean = Good
  Insect = Marginal

MacroInvertivore:
  Finfish = Marginal
  MacroCrustacean = Preferred
  Insect = Good

MicrofaunaFeeder:
  Microfauna = Preferred
  Insect = Marginal
  Finfish = Poor
```

这些只能用于检查结构、override 语义和 authoring 成本，不能晋升为生产食性参数。

## 11. 与当前 prey-family catalog 的关系

当前 catalog 仍是 Working Candidate。

本页只依赖以下稳定原则：

- prey family 是 operational feeding-target vocabulary，不是自然分类学；
- 同一 resolution 下，一个具体 prey object 只映射到一个 operational leaf；
- parent 仅用于 inheritance / fallback；
- family 不编码 habitat / motion state；
- child override parent，不叠加父子值。

如果 catalog 最终改名或拆分，DietArchetype defaults 做术语映射即可，不改变本页的生产结构。

## 12. 当前 OPEN

- 5 个基础 archetype 是否足以覆盖实际约 200 鱼种；
- `MacroInvertivore` 是否需要拆 Insectivore / Crustacivore；
- `MixedPredator` 是否有足够覆盖价值；
- `HerbivoreDetritivore` 是否应拆 Herbivore / Detritivore；
- final prey-family catalog；
- relation-class numeric anchors；
- species / cohort diet evidence 数据源和批量 authoring workflow；
- override-rate 触发重构的具体阈值。

在全量 production fish list 与 diet evidence 到位前，本页冻结 archetype 职责和 admission / override 规则，不冻结具体鱼种归类和具体 relation 数值。

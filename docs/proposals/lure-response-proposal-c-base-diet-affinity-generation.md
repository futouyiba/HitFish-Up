# Proposal C｜BaseDietAffinity 生产方案

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`BaseDietAffinity` 不建议按 `species × prey family` 全矩阵逐格手填连续数。

第一版推荐：

```text
DietArchetype
→ prey-family default relations

Species / Cohort
→ sparse overrides

Bake
→ BaseDietAffinity(prey family)
```

`DietArchetype` 是 authoring / data-production helper，不是新的 runtime 生物学对象。runtime 只消费 Bake 后的 `BaseDietAffinity`。

## 2. 为什么需要模板层

项目鱼种规模约 200 种。若每种鱼对每个 prey family 独立配置连续值，会带来：

- 配置量快速膨胀；
- 不同作者尺度漂移；
- 同类鱼之间缺少一致默认；
- 后续新增 prey family 时需要重填整张矩阵；
- 连续小数容易产生伪精确。

因此第一版先用少量可解释的食性原型提供默认关系，再让具体鱼种 / cohort 只修改真正有证据的差异。

## 3. DietArchetype 的职责

DietArchetype 只回答：

> 这种食性类型在参考上下文、参考 prey size 下，对各 prey family 的默认相对食物价值是什么？

它不是：

- taxonomy / 系统分类学；
- 栖息地标签；
- FeedingMotivation；
- DietaryShift；
- prey support；
- 精确胃含物比例。

候选 archetype 可以参考常见 trophic guild，例如：

```text
Piscivore
Invertivore / Insectivore
Benthic-Invertebrate Feeder
Omnivore / Opportunist
Planktivore
Herbivore / Detritivore
```

实际项目是否需要全部这些类、是否应拆分，必须由现有鱼种覆盖测试决定，不能为了 taxonomy 完整而预先冻结。

## 4. 外部数据如何使用

FishBase 等来源提供分层 food-item taxonomy、已观察摄食项、diet composition / commonness 等证据，可用于确定：

- 某 prey family 是否真实进入物种食谱；
- 哪些食物更常见 / 更主要；
- 某物种更接近哪个 DietArchetype；
- 是否需要 species override。

但不能直接把：

```text
胃内容出现频率 = BaseDietAffinity
```

因为 observed diet 同时受猎物可获得性、采样地点、季节、尺寸阶段等影响，并不等于纯 preference。

因此外部数据是 authoring evidence，不是自动 production coefficient。

## 5. authoring 推荐用关系档，不手填连续小数

第一版推荐 DietArchetype 与 species override 都使用人类可读 relation：

```text
Preferred
Good
Marginal
Poor
Reject
Unknown / NotConfigured
```

其中：

- `Reject` 是明确硬语义拒绝；
- `Poor` 仍是可食的低价值目标；
- `Unknown` 不是 Poor / Reject；
- `NotConfigured` 不能静默补默认。

Bake 再将非 Reject 档位映射到唯一连续 anchor：

```text
RelationClass
→ BaseDietAffinity numeric anchor
```

具体 anchor 尚未 production calibration。

这样 authoring 侧避免大量 0.63 / 0.71 之类无法取证的小数，同时 runtime 仍获得连续 FoodValue。

## 6. archetype + override 的合成

推荐：

```text
resolved_relation(prey)
=
SpeciesOrCohortOverride(prey)
?? DietArchetypeDefault(prey)
```

即 override 是替换，不是再乘 / 再加一层 bonus。

原因：species override 的语义是“这个具体物种在该 prey family 上偏离模板”，如果同时保留 archetype 值再叠加 offset，会增加双重尺度与隐藏自由度。

Bake 输出 provenance 应能说明该值来自：

- archetype default；或
- species override；或
- cohort / life-stage override。

## 7. cohort / life-stage

食性会随成长阶段变化时，不应复制整份 species profile。

推荐继承：

```text
Species DietArchetype / defaults
        ↓
Cohort sparse overrides
```

例如幼体以无脊椎为主、成体明显转向 piscivory 时，只覆盖受影响 prey families，或在差异足够系统时允许 cohort 选择不同 DietArchetype。

不要仅因鱼变大就自动改变 BaseDietAffinity；纯尺寸效应优先由 `SizePreferenceAdjustment` 承接。

只有“食性组成 / prey family preference 本身改变”才进入 cohort diet override。

## 8. prey family 粒度

`BaseDietAffinity` 应对稳定、可复用的 prey family author，而不是对每个商品饵、每个具体 prey species author。

prey family 粒度必须满足：

- 玩家能通过钓法 / 拟饵选择感知差异；
- 外部资料能较可靠支持；
- 同 family 内基础食性差异不会大到必须大量 override；
- 不与 presentation state / lure geometry 混淆。

FishBase 的 Food II / Food III 层级可作为数据整理参考，但项目不应机械复制其全部 taxonomy。项目只保留能购买玩法表达能力的层级。

## 9. 不要求 BaseDietAffinity 归一化

不同 prey family 的基础 affinity 不要求和为 1。

例如：

```text
baitfish = Preferred
crayfish = Good
insects = Good
```

是合法的。

这些值回答各自“值不值得吃”，不是 diet composition probability。

因此不要：

```text
normalize(BaseDietAffinity) so sum = 1
```

DietaryShift 的中心化约束也只是为了消除 common-mode 与 FeedingMotivation 的不可识别性，不把最终 affinity 变成概率分布。

## 10. Reject 的准入标准

`Reject` 应保守使用。

只有有较强语义依据确认该 prey family 对当前 species / cohort 基本不属于 Feeding target 时才配置 Reject。

如果只是：

- 很少吃；
- 特定季节不常吃；
- prey availability 低；
- 当前并非主食；

更适合配置 `Poor / Marginal`，或交给 DietaryShift / Opportunity / spatial ecology，而不是写死 Reject。

这样避免 DietaryShift 永远无法表达真实的季节性食性变化。

## 11. Missing / Unknown

必须区分：

```text
Archetype default known
+ no species override
→ use archetype default
```

```text
Archetype has no rule for prey family
→ NotConfigured / Unknown
→ Bake 不得补 0
```

```text
Species evidence missing
→ 不是自动 Reject
```

如果项目希望新增 prey family 后旧鱼种继续可运行，应通过显式 migration / template default 策略处理，而不是 runtime fallback。

## 12. 数据生产流程

推荐批量生产：

```text
1. 定 prey-family catalog
2. 定少量 DietArchetype defaults
3. 将现有鱼种映射到 archetype
4. 用外部 diet evidence 做异常扫描
5. 只为明显偏离项写 species / cohort override
6. Bake relation class → numeric BaseDietAffinity
7. 做覆盖率 / override-rate / Unknown 检查
```

一个重要验收指标：

> 如果大量鱼种的大量 prey family 都需要 override，优先说明 archetype 或 prey-family 粒度设计失败，而不是继续堆 override。

## 13. 当前 OPEN

- 项目最终 prey-family catalog；
- DietArchetype 的最终数量 / 名称；
- 约 200 种鱼的 archetype 覆盖测试；
- Preferred / Good / Marginal / Poor 的 numeric anchors；
- 外部证据到 relation class 的 authoring guideline；
- cohort 何时切换 archetype、何时只 sparse override；
- override-rate 多高应触发 archetype 重构。

本页只闭合生产结构，不冻结具体鱼种食性参数。

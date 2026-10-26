# Proposal C｜Locomotor Baseline 生成策略

状态：Working Proposal / Candidate。不是 Current，不是生产参数。

对齐：本页承接 `lure-response-proposal-c-intercept-capacity-semantics.md` 中的 `LocomotorBaseline(species, size/stage)` 缺口。

## 1. 结论

第一版不为约 200 个鱼种逐鱼手填一套“最高游速”。推荐采用：

```text
LocomotorBaseline
= ArchetypeReferenceCapacity
× SizeScale(length)
× SpeciesOverride(optional)
× StageEcologyOverride(optional)
```

这里表达的是 authoring ownership，不冻结为生产线性乘法。

核心目标是：

- 让绝大多数鱼通过少量原型 + 体长自动生成；
- 允许少量明显离群鱼做 species override；
- 成长阶段默认由体长变化自动带出，不复制整套参数；
- 只有成长阶段确实发生运动生态/体型机制变化时，才使用 stage override。

## 2. 为什么不逐鱼手填

逐鱼直接 author 一个速度值的问题：

1. 数据来源不一致：不同论文使用 burst、critical、sustained 等不同口径；
2. 约 200 种鱼 × 成长阶段会迅速膨胀为大量难维护参数；
3. 数字容易产生伪精确，且难解释鱼种之间为什么差 10% 或 20%；
4. 后续平衡调整会变成逐行修表，而不是调整少量可解释的生产规则。

因此科研资料更适合：

- 帮助鱼种归类；
- 校验排序；
- 发现离群种；
- 给 reference archetype 提供量级参考；

而不是强迫每条鱼都有独立实测速度。

## 3. 为什么不能只按体长

已有研究反复显示：

- 绝对游泳能力通常随体长增加；
- 以 BL/s 表示的相对速度会随体长变化，不能假定恒定；
- 体型、形态、栖息水流类型、温度和生理状态都会影响表现；
- 不同鱼类运动学存在明显差异。

因此 `SizeScale(length)` 只能承担“同一运动原型内的尺寸趋势”，不能替代 archetype。

## 4. Locomotor Archetype 的职责

Archetype 只回答：

> 在相似体长下，这一类鱼的短时追赶能力大致处于什么相对档位？

它不是分类学，也不是完整游泳行为模型。

第一轮可从少量、易判断的 production buckets 起步，例如：

- streamlined-fast：流线、高速持续/追赶型；
- active-generalist：常规主动游泳型；
- burst-ambush：伏击、短时爆发型；
- draggy-slow：高阻体型、整体偏慢型；
- benthic-low-mobility：底栖、低机动型。

这些名称和数量都还是 Working。不能先冻结 taxonomy，再强迫全部鱼种套入。

正确做法是拿现有鱼种做一次覆盖测试：

- 是否大多数鱼能自然落入少量 bucket；
- 是否经常出现“同 bucket 内策略故事明显冲突”；
- override 比例是否足够低。

如果 override 大量出现，应优先重构 archetype，而不是继续堆 species override。

## 5. SizeScale

当前只冻结语义，不冻结指数：

```text
SizeScale(length)
```

必须满足：

1. 体长增加时，绝对 LocomotorBaseline 默认不下降；
2. 增长应是次线性的，不默认 `capacity ∝ length`；
3. 不默认 `BL/s` 恒定；
4. 曲线应连续，避免成长阶段边界跳变。

当前不准入一个跨所有鱼种统一的 `length^0.5`、`length^0.7` 等指数作为生产规则。已有研究只足够支持方向，不足以支持一个通用指数。

推荐后续用体验标定反推少量曲线参数，并用现实资料做排序约束，而不是反过来从某篇单一论文直接抄指数。

## 6. 成长阶段

默认：

```text
same species
+ different representative length
→ same archetype
→ SizeScale 自动改变 baseline
```

不默认：

```text
young_speed
mature_speed
large_speed
```

逐阶段各配一套。

只有下列情况才准入 `StageEcologyOverride`：

- 幼体与成体体型/推进方式明显变化；
- 成长阶段伴随栖息环境或运动生态显著切换；
- 现有 size scaling 无法保持明确的玩家可感知排序。

Stage override 应是例外，不是主生产路径。

## 7. Species Override

Species override 只用于可说明的离群情况。

准入条件建议：

- 同 archetype、同体长下，现实证据或策略体验稳定显示明显偏离；
- 偏离足够大，值得玩家感知；
- 不能通过改 archetype 或 size curve 更干净地解释。

禁止为了“让每条鱼都更独特”给所有物种加微小 override。

否则会退化成 200 个手填参数。

## 8. 与 Functional Capacity 的边界

`LocomotorBaseline` 是健康/标准状态下的结构性能力基线。

当前鱼情影响由另一层承接：

```text
LocomotorBaseline
× CapacityStateModifier(FunctionalCapacity)
→ EffectiveInterceptCapacity
```

因此温度、低氧、疲劳、疾病等，如果已经进入 FunctionalCapacity，不能同时改 LocomotorBaseline。

同理，Feeding Motivation 不修改 LocomotorBaseline。

## 9. 推荐 authoring 面

第一版每个 species/stage 不应暴露一个“速度输入框”。更适合暴露：

```text
species:
  locomotor_archetype
  representative_length_source
  species_capacity_override?   # sparse

stage:
  representative_length
  stage_ecology_override?      # sparse
```

Archetype reference capacity 与 SizeScale 曲线属于共享生产配置。

这样 200 种鱼的维护成本主要是分类与代表体长，而不是逐鱼调浮点数。

## 10. 验收条件

上线前至少检查：

1. 同 archetype 内，绝对 baseline 随代表体长单调不降；
2. growth stage 默认连续，不在阶段边界突跳；
3. 高速流线型与低机动底栖型的排序稳定；
4. species override 比例保持稀疏；
5. 同一鱼在更高 FunctionalCapacity 下得到更高 EffectiveInterceptCapacity；
6. 不因 size、archetype、FunctionalCapacity 在多个层重复计权；
7. 最终玩家策略故事可通过 lure speed / pause / fish capacity 的变化解释。

## 11. 当前 OPEN

- archetype 的最终集合与命名；
- 每个 archetype 的 reference capacity；
- `SizeScale(length)` 的生产曲线；
- representative length 从哪张生产数据表读取；
- species override 的允许范围；
- stage ecology override 的准入表结构；
- 与 Fish Condition / Functional Capacity 的生产 owner 对接。

## 12. 当前裁决

Working 推荐：

> **共享 archetype + 连续 size scaling + 稀疏 override。**

不推荐：

- 200 鱼逐鱼手填最高游速；
- 每个成长阶段重复一整套速度；
- 单纯用体长决定所有鱼的能力；
- 把文献中的 burst/Ucrit 数值直接当游戏的 EffectiveInterceptCapacity；
- 为追求“鱼种差异”而普遍使用 species micro-override。

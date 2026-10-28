# Edible Size Response｜可摄食尺寸响应 Candidate

> 状态：Candidate / Working Design
> 
> 日期：2026-10-28
> 
> 目标：建立一套可同时服务 Groundbait 粒径筛选与后续 Hookbait / 饵球尺寸筛选的鱼侧响应模型。

## 1. 问题定义

不要直接给每条鱼配置“最佳颗粒大小 = X mm”。当前提案把尺寸响应拆成：

```text
Fish Body Size
        ×
Morphology Profile
        ↓
Intake Reference Size
        +
Feeding Mechanism Curve(s)
        ↓
Edible Size Fit
```

其中：

- `Body Size`：当前个体 / 成长阶段有多大。
- `Morphology Profile`：同样体长下，这个物种的口部或过滤结构相对有多大。
- `Feeding Mechanism`：鱼如何摄食，决定尺寸响应曲线的形状。
- `Edible Size Fit`：当前尺寸的实体食物对这条鱼是否容易被有效利用。

`Intake Reference Size` 只是尺寸基准，不等于最佳颗粒尺寸。

## 2. 为什么 Body Size 与 Ratio 分开

这两个量承担不同职责：

```text
Body Size
→ 个体成长变化

Morphology Ratio
→ 物种形态差异
```

例如两条同为 30 cm 的鱼，可以因为口部相对尺寸不同而拥有不同 Intake Reference。反过来，同一物种从幼鱼长到成年时，Body Size 改变即可让 Size Response 自然整体右移。

### 2.1 Candidate 字段

```text
Species Morphology Profile
├─ OralRatio
├─ FilterRatio optional
└─ GrowthStageOverride optional
```

默认不引入复杂异速生长公式。只有存在明确证据或 Fixture 需要时，才为特定成长阶段 Override Ratio。

## 3. Feeding Mechanism Catalog

第一版候选类型：

```text
PICK              啄食
SUCTION           吸食
BENTHIC_SUCTION   底层吸食
GULP              吞食
FILTER            滤食
GRAZE             刮食（是否首版需要待核）
```

Feeding Mechanism 不只是一个倍率。不同机制拥有不同的标准 Size Response Curve。

### 3.1 统一曲线接口

每条标准曲线至少表达：

| 参数 | 含义 |
|---|---|
| `tiny_threshold` | 尺寸太小时开始失去作为有效实体食物的价值 |
| `preferred_min` | 高效区间下界 |
| `preferred_max` | 高效区间上界 |
| `max_ingestible` | 超过后快速失去可摄食性 |

第一版优先用简单梯形 / 分段线性曲线，避免过早购买复杂函数。

```text
Fit
1.0          ┌──────────┐
             │          │
            /            \
           /              \
0 ────────┘                └────
       太小   高效区间      太大
```

## 4. 各摄食方式的结构差异

### 4.1 PICK

候选特征：

- 高效区间偏小到中等。
- 过小颗粒可能降低单颗利用价值。
- 对超大颗粒下降较快。
- 曲线相对窄。

### 4.2 SUCTION

候选特征：

- 对较细颗粒的利用范围更宽。
- 小到中颗粒都可高效利用。
- 右侧仍受入口尺度约束。

### 4.3 BENTHIC_SUCTION

Size Curve 可与 SUCTION 接近，但“底层”不要写进尺寸曲线本身。

底层可用性应由 Feeding Place 中颗粒所在位置 / 水层决定，避免同一语义重复计权。

### 4.4 GULP

候选特征：

- 高效区间相对右移。
- 对较大对象容忍更高。
- 很细颗粒不一定不能吃，但可能不是该机制最有效的利用方式。

### 4.5 FILTER

FILTER 使用独立 Reference Source：

```text
Body Size × FilterRatio
→ Filter Reference
```

不要因为鱼嘴很大就推出“滤食鱼偏好大颗粒”。滤食响应需要表达对悬浮 / 可截留粒径的效率窗口。

## 5. 多 Feeding Mechanism 如何聚合

一条鱼可以拥有多个摄食机制，例如：

```text
BENTHIC_SUCTION proficiency = 1.0
PICK            proficiency = 0.5
```

每个机制独立求值：

```text
ModeFit_m = proficiency_m × curve_m(size / reference_m)
```

第一版推荐：

```text
EdibleSizeFit = max(ModeFit_m)
```

原因：多个摄食方式是完成“处理同一个食物对象”的替代路径。鱼应使用当前最有效的一条，而不是因为会的方式多就累加 Bonus。

暂不采用：

```text
sum(ModeFit_m)
```

否则会出现“Feeding Mechanism 越多越强”的叠加套利。

是否需要 softmax / 平滑 best-path，留给 Fixture 后再决定。

## 6. Groundbait 如何消费 Size Response

Groundbait 输入不是单个尺寸，而是 Particle Distribution：

```text
Fine      20%
Small     40%
Medium    30%
Coarse    10%
```

对鱼 `f`：

```text
EdibleFraction_f = Σ_b MassShare_b × SizeFit_f(b)
```

语义：

> 这团窝料的实体食物质量中，有多少比例对当前鱼而言可被有效利用。

这可以自然形成体型筛选：粗颗粒窝不需要写“大鱼概率 +30%”，而是因为小鱼的 Size Fit 在大颗粒区间下降，导致其可利用份额更低。

## 7. Hookbait / 饵球如何复用

Hookbait 输入可以是单个 `BaitBallSize`：

```text
BaitBallSize
    ↓
Edible Size Response
    ↓
SizeFit
```

因此 Groundbait 与 Hookbait 共享鱼侧：

```text
Body Size
Morphology Profile
Feeding Mechanism Profile
```

区别只在输入：

```text
Groundbait → Particle Distribution
Hookbait   → Single Bait Size / Size Distribution
```

## 8. 不把“小颗粒”默认做成大鱼强负分

当前 Candidate 认为：

- 太大颗粒对小鱼可以形成明显的右侧生理 / 行为约束。
- 小颗粒对大鱼通常不应仅因“大鱼嘴大”就产生强烈负分。

“大颗粒筛大鱼”的首要机制可以来自：

```text
小鱼无法高效利用大颗粒
vs
大鱼可以同时利用小颗粒和大颗粒
```

如果玩法验证发现这不足以产生目标体型差异，再研究“大鱼对细碎食物的单位留存价值 / 摄食收益”是否应由其它机制承担，而不是先硬写进 Size Fit。

## 9. 参数生成，而不是全量手填

数据生产链候选：

```text
Evidence
├─ Fish body-size range
├─ Mouth / gape information
├─ Feeding mechanism
├─ Filter structure when needed
└─ Typical natural food / prey size
        ↓
Parameter Generator
        ↓
Morphology Profile
+ Feeding Mechanism Set
        ↓
Generated Size Response
        ↓
Sparse Exact Override
```

建议记录 Evidence Level：

```text
DIRECT
INFERRED
ARCHETYPE_DEFAULT
OVERRIDE
```

嘴部 / gape 信息可以作为重要上游证据，但不把 Runtime 简化成一条固定 `particle < mouth × constant` 的万能公式。

## 10. 第一轮 Gold Fixture

先不追求完整真实鱼库。用六类角色攻击结构：

| Fixture | 目的 |
|---|---|
| 小型啄食鱼 | 验证 Fine / Small |
| 大型底吸鱼 | 验证 Body Size 右移 |
| 小型底吸鱼 | 与大型同机制对照 |
| 大口吞食鱼 | 验证 GULP 曲线 |
| 滤食鱼 | 验证 Filter Reference |
| 双模式鱼 | 验证 `max` 聚合不套利 |

测试尺寸可先用一组 Working Fixture，例如：

```text
0.2 / 0.5 / 1 / 2 / 5 / 10 / 20 mm
```

这些数值只用于看结构行为，不是生产定值。

### 10.1 必须出现的结构行为

1. 同物种变大后 Size Response 整体向更大尺寸移动。
2. 同体长鱼可因 Morphology Ratio 不同而产生差异。
3. PICK / SUCTION / GULP 不是简单倍率缩放，而是曲线形状不同。
4. FILTER 不依赖 Mouth Reference 才能工作。
5. 多 Feeding Mechanism 不因数量多而叠加获利。
6. 粗颗粒能明显降低小鱼的可利用份额。
7. 细颗粒不会无依据地强烈排斥大鱼。

## 11. Open Questions

- 第一版实际需要哪些 Feeding Mechanism，`GRAZE` 是否可以后置。
- Size Curve 的标准参数如何由真实作钓 / 生物证据标定。
- `max` 是否过于尖锐，是否需要 softmax 或 best-path 平滑。
- Particle Size 是否还应独立影响 Attraction / Release，而不仅是 Ingestion。
- 大颗粒带来的“大鱼留存 / 价值”是否需要由 Food Amount / Retention 而不是 Size Fit 表达。
- 实际生产使用毫米连续值还是离散 Size Class。当前偏向 Authoring 可先使用 Size Class，Runtime 后续再决定是否映射到连续物理尺度。

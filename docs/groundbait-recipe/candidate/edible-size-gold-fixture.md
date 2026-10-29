# Edible Size Gold Fixture

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页只验证 Edible Size 的结构性质，不定义生产参数，也不证明真实鱼种偏好。

## 1. 这组 Fixture 要回答什么

只回答四个问题：

1. 体尺和形态变化时，尺寸约束是否按预期移动。
2. 不同摄食动作是否表现出不同曲线，而不是同一曲线的倍率。
3. 多动作路径是否避免数量套利。
4. 可食颗粒和载体颗粒是否真的分开。

不回答 Attraction、Retention、Food Preference、Flavor 或最终 Response。

## 2. 输入

### 2.1 鱼侧

| 鱼 | 体长 | 形态比例 | 参考尺寸 | 动作路径 |
|---|---:|---:|---:|---|
| Small Benthic | 60 mm | 0.20 | 12 mm | BENTHIC_SUCTION 1.0 |
| Large Benthic | 180 mm | 0.20 | 36 mm | BENTHIC_SUCTION 1.0 |
| Small Pick | 30 mm | 0.20 | 6 mm | PICK 1.0 |
| Large Gulp | 120 mm | 0.35 | 42 mm | GULP 1.0 |
| Dual Path | 90 mm | 0.20 | 18 mm | PICK 0.5 + BENTHIC_SUCTION 1.0 |
| Filter | 不适用 | 不适用 | 过滤参考 10 mm | FILTER 1.0 |

普通口部路径的参考尺寸用 `体长 × 形态比例`。这只是候选映射，不是 Runtime 真理。FILTER 不使用口部参考，直接使用过滤参考。

### 2.2 颗粒侧

只使用可食颗粒分布。载体和不可食颗粒不进入本 Fixture 的尺寸拟合。

```text
Fine mix
  0.2 mm  edible_share 0.50
  1.0 mm  edible_share 0.30
  2.0 mm  edible_share 0.20

Very coarse mix
  5.0 mm  edible_share 0.20
  10.0 mm edible_share 0.50
  20.0 mm edible_share 0.30
```

`edible_share` 在可食部分内部求和为 1。可食部分占固体的比例另记，例如 0.70；载体占 0.30。

## 3. 曲线

第一轮使用分段线性曲线：

```text
fit(r; floor, preferred_min, preferred_max, cutoff):
  r <= preferred_min  → floor + (1 - floor) × r / preferred_min
  r <= preferred_max   → 1
  r < cutoff            → (cutoff - r) / (cutoff - preferred_max)
  r >= cutoff           → 0
```

Fixture 参数：

```text
PICK              floor 0.25, preferred_min 0.20, preferred_max 0.80, cutoff 1.50
BENTHIC_SUCTION   floor 0.40, preferred_min 0.10, preferred_max 0.50, cutoff 1.50
GULP              floor 0.20, preferred_min 0.55, preferred_max 1.35, cutoff 3.50
FILTER            floor 0.10, preferred_min 0.20, preferred_max 1.00, cutoff 2.50
```

这些数值只用于看结构行为，不是生产定值。

## 4. 单尺寸期望输出

表中值为 `max(proficiency × curve(size / reference))`，四舍五入到两位。

| 鱼 | 0.2 mm | 1 mm | 2 mm | 5 mm | 10 mm |
|---|---:|---:|---:|---:|---:|
| Small Benthic | 0.50 | 0.90 | 1.00 | 1.00 | 0.67 |
| Large Benthic | 0.43 | 0.57 | 0.73 | 1.00 | 1.00 |
| Small Pick | 0.38 | 0.88 | 1.00 | 0.95 | 0.00 |
| Large Gulp | 0.21 | 0.23 | 0.27 | 0.37 | 0.55 |
| Filter | 0.19 | 0.55 | 1.00 | 1.00 | 1.00 |

读法：

- Small Benthic 和 Large Benthic 使用同一动作，但参考尺寸从 12 mm 移到 36 mm，高效区间整体右移。
- Small Pick 在大尺寸上快速降到 0，曲线比 BENTHIC 窄。
- Large Gulp 在 10 mm 仍有 0.55，右侧更宽。
- Filter 不使用口部参考，10 mm 仍为 1.00。

### 4.1 Dual Path 对照

Dual Path 的参考尺寸为 18 mm：

```text
pick_path    = 0.5 × PICK(size / 18)
benthic_path = 1.0 × BENTHIC_SUCTION(size / 18)
max_path     = max(pick_path, benthic_path)
```

| 尺寸 | pick_path | benthic_path | max | 直接求和（反例） |
|---:|---:|---:|---:|---:|
| 0.2 mm | 0.15 | 0.47 | 0.47 | 0.61 |
| 1 mm | 0.23 | 0.73 | 0.73 | 0.96 |
| 2 mm | 0.33 | 1.00 | 1.00 | 1.33 |
| 5 mm | 0.50 | 1.00 | 1.00 | 1.50 |
| 10 mm | 0.50 | 0.94 | 0.94 | 1.44 |

直接求和列只作退化对照。它会让同一对象的利用率超过 1，并让动作数量变成收益。

## 5. Groundbait 聚合

```text
EdibleUtilization_f = Σ edible_share_i × SizeFit_f(size_i)
```

可食份额只在可食部分内部归一化，载体不参与。

| 配方 | 可食分布 | Small Benthic | Large Benthic |
|---|---|---:|---:|
| Fine mix | 0.2 / 1 / 2 mm | 0.72 | 0.53 |
| Very coarse mix | 5 / 10 / 20 mm | 0.53 | 0.98 |

结构行为：

- 极粗分布下，Small Benthic 的可利用份额明显下降。
- Large Benthic 仍能利用大部分可食颗粒。
- 体型筛选来自动作约束，不需要额外写“大颗粒 → 大鱼概率 +30%”。

### 5.1 载体不变性

保持可食分布不变，只改变可食部分占固体的比例：

```text
方案 A：可食 70%，载体 30%
方案 B：可食 40%，载体 60%
```

`EdibleUtilization` 不变。若需要绝对可食质量，再乘：

```text
absolute_edible_mass = edible_fraction_of_solids × total_solids × EdibleUtilization
```

载体有粒径、参与释放，但不进入尺寸拟合。

## 6. 退化测试

1. **载体隔离**：只改变载体份额，`EdibleUtilization` 不变；载体尺寸变化也不改变它。
2. **桶拆分不变**：把 1 mm / 0.30 拆成两个 1 mm 桶各 0.15，结果不变。
3. **重复路径不变**：把 BENTHIC_SUCTION 复制一份，Dual Path 结果不变。
4. **体尺移动**：参考尺寸从 12 mm 增到 36 mm，10 mm 处的 BENTHIC fit 从 0.67 升到 1.00。
5. **细颗粒边界**：Large Benthic 在 0.2 mm 处得到 0.43，不因体长大而归零。
6. **动作隔离**：只改变尺寸，不改变 Chemical Cue；只改变 Cue，不改变 SizeFit。
7. **过滤独立**：改变普通口部形态比例，FILTER 的尺寸拟合不变。

## 7. 这组 Fixture 不证明什么

- 不证明这些曲线参数适合真实鱼种。
- 不证明 `max` 是最终聚合方式；它只在“动作可自由切换、无切换成本”的假设下作为上界。
- 不证明可食部分与载体部分的实际比例。
- 不证明 Groundbait 聚合应该按质量、数量还是能量。
- 不证明 Edible Size 可以进入 Attraction、Retention 或最终 Response。

## 8. 下一步

Fixture 通过后，只说明 Size 的结构没有混淆。接下来才考虑 Groundbait Particle Distribution 的实际数据接入；不进入 Food、Flavor 或完整 Recipe Grammar。
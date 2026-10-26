# Proposal C｜Functional Capacity → Intercept Capacity

状态：Working Hypothesis / Candidate。不是 Current，不是生产参数。

## 1. 结论

Closing 不直接解释温度、低氧、疲劳、消化负担等原始 Fish Condition 原因。

这些原因应先由上游 Fish Condition / Functional Capacity 逻辑解释，再向 Closing 暴露一个更窄的运动能力保留量：

```text
FunctionalCapacity
        ↓
LocomotorCapacityRetention
        ↓
EffectiveInterceptCapacity
```

第一版不在 Closing 侧再增加一条自由的非线性能力曲线。

如果上游明确把 `FunctionalCapacity` 定义为“相对参考正常状态的可用短时运动能力比例”，则允许：

```text
LocomotorCapacityRetention = FunctionalCapacity
```

否则 identity 不成立，必须保留显式 projection seam。

## 2. 为什么不直接用环境因素

温度、溶氧、疲劳等对鱼类游泳表现确实有影响，但跨物种、适应状态和时间尺度并不一致。存在：

- 温度升高后性能先升后降；
- 低氧导致能力下降；
- 长期适应后出现部分甚至反向补偿；
- 不同生态型的 locomotor performance 与 hypoxia tolerance 存在 trade-off。

因此 Closing 不能写成类似：

```text
low_oxygen → capacity × 0.7
temperature_bad → capacity × 0.8
fatigue → capacity × 0.6
```

否则会在 Response 层复制一套 Fish Condition 模型，并极易与上游重复计权。

## 3. 与 Motivation 的边界

固定：

```text
Functional / locomotor capacity
→ 能不能做到

Feeding Motivation
→ 愿不愿意出手
```

低 Motivation 不降低 `EffectiveInterceptCapacity`。

低 locomotor capacity 也不直接提高 `WillingnessThreshold`。

二者可以同时受同一个环境原因影响，但必须由上游分别投影，不允许在 Feeding Resolver 中把它们合成同一个“鱼情差”系数。

## 4. 推荐标尺

如果后续决定让 FunctionalCapacity 直接服务 locomotor capacity，推荐把它定义成无量纲 retention：

```text
1.0 = 当前物种 / 尺寸基线的参考正常短时运动能力
0.7 = 只保留约 70% 的该能力
0.0 = 对本 response mode 没有可用的短时 Closing 能力
```

这样：

```text
EffectiveInterceptCapacity
= LocomotorBaseline
× LocomotorCapacityRetention
```

这里的线性不是生理定律，而是**标尺定义**：retention 本身就被定义成能力保留比例。

真正的非线性应发生在上游：

```text
raw causes
(temperature / oxygen / fatigue / disease / digestion ...)
        ↓ species/context-specific interpretation
LocomotorCapacityRetention
```

而不是在 Closing 再从 retention 猜一次能力。

## 5. 为什么拒绝带底值线性

不采用：

```text
capacity_modifier = floor + (1-floor) × FunctionalCapacity
```

除非上游明确声明 `FunctionalCapacity=0` 仍代表某个非零 locomotor ability。

否则 floor 会让“没有可用 Closing 能力”的语义失真，并引入难以解释的永久最低速度。

## 6. 为什么不先用凸 / 凹映射

例如：

```text
modifier = FunctionalCapacity^2
modifier = sqrt(FunctionalCapacity)
```

都会制造新的玩法自由度，但当前没有独立受控 fixture 能识别指数。

如果 FunctionalCapacity 已经是 retention 标尺，这些曲线反而属于二次解释。

只有未来出现受控反例，例如“50% FunctionalCapacity 明显不应对应 50% 短时 Closing 能力”，才重新打开 projection shape。

## 7. Unknown 与 zero

必须区分：

```text
FunctionalCapacity = Unknown
→ LocomotorCapacityRetention = Unknown
→ Closing ResolutionIncomplete
```

不能当 0。

```text
LocomotorCapacityRetention = 0
→ EffectiveInterceptCapacity = 0
→ 对需要 Closing 的角度不可行
```

这两个状态语义不同。

## 8. 与 LocomotorBaseline 的组合

当前 Candidate：

```text
ArchetypeReferenceCapacity
× SizeScale(length)
× sparse species/stage override
→ LocomotorBaseline

FunctionalCapacity
→ LocomotorCapacityRetention

LocomotorBaseline
× LocomotorCapacityRetention
→ EffectiveInterceptCapacity
```

之后才进入：

```text
q = lure_speed_relative_to_water / EffectiveInterceptCapacity
u_close(θ) = max(0, q cosθ)
```

## 9. 当前缺口

仍未闭合：

- 上游 `FunctionalCapacity` 的 Current 定义与数值标尺；
- 是否已有独立 locomotor projection owner；
- raw Fish Condition causes → locomotor retention 的 species/context-specific production mapping；
- calibration anchors。

在这些缺口闭合前，本页只冻结 owner 边界和最小 projection topology，不冻结生产值。

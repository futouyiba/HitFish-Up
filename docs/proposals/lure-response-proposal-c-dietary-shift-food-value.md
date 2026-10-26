# Proposal C｜Dietary Shift → FoodValue

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

`DietaryShift` 不表示“今天整体更想吃东西”。

它只表达：

> 在仍然属于食物的目标之间，当前情境让鱼的相对食性偏向发生了什么变化。

因此：

```text
BaseFoodPreference(prey)
+ DietaryShift(prey)
→ CurrentFoodValue(prey)
```

而整体摄食强弱继续由：

```text
FeedingMotivation
→ WillingnessThreshold
```

承担。

## 2. DietaryShift 不是单一总倍率

不采用：

```text
FoodValue *= DietaryShiftScalar
```

因为一个单一 scalar 只能让所有食物一起升降，这与 FeedingMotivation 高度重合。

第一版应把 `DietaryShift` 理解成 prey / food-family keyed 的相对偏转，例如：

```text
baitfish: +0.20
crayfish: -0.10
frog:     0.00
```

这些数值只是结构示例，不是生产参数。

因此 `DietaryShift` 更接近一个稀疏 profile / vector，而不是一个 Fish Condition scalar。

## 3. 与 Reject 的边界

`Reject` 继续是 hard semantic boundary。

它表示该 target relation 不属于当前 Feeding mode 可接受的食物关系，而不是“最近暂时不太爱吃”。

因此默认：

```text
Base TargetRelation = Reject
→ DietaryShift 不能救活
```

如果某种目标会随季节 / 生命阶段从“基本不吃”变成“会吃”，那说明它不应在基础语义上使用永久 `Reject`；应把它建模为可食但低价值的 relation / FoodValue，再由 DietaryShift 改变排序。

这样避免一边把 Reject 定义成 hard boundary，一边又用季节偏转穿透它。

## 4. 只改变相对偏好，不改变 prey support

`DietaryShift` 发生在鱼侧食物评价层。

禁止：

```text
DietaryShift
→ 修改 prey support
```

同一个 lure 是否能被解释成 baitfish / crayfish，由 presentation evidence 决定；鱼当前更想吃 baitfish 不能反过来让 lure “更像 baitfish”。

当前顺序：

```text
presentation
→ prey support
→ prey-conditioned state
→ BaseFoodPreference + DietaryShift
→ FoodValue
```

## 5. 与 FeedingMotivation 的可识别性

如果所有 prey 的 DietaryShift 都同时增加同一个常数：

```text
Δ_baitfish += c
Δ_crayfish += c
Δ_frog += c
```

它在体验上会逐渐退化成“整体更愿意吃”，与 FeedingMotivation 混淆。

因此生产标尺必须去掉 common-mode freedom。

第一版有两种合法做法：

### A. 锚定一个 reference food family

```text
Δ_reference = 0
其它 prey 相对它偏移
```

### B. 对当前可食 prey set 做中心化

```text
weighted_mean(Δ_prey) = 0
```

当前更推荐 B，因为不要求人为指定某个永久参考食物；但权重口径仍未冻结。

中心化只是解决参数可识别性，不把 prey preference 解释成概率，也不要求 FoodValue 之和为 1。

## 6. 推荐内部表示

为了方便正负偏转，第一版更适合在一个可加的 latent preference score 上工作：

```text
z_current(prey)
= z_base(prey) + Δ_diet(prey)
```

之后再映射到项目实际使用的：

```text
Preferred / Good / Marginal / Poor / Reject
```

或连续 FoodValue anchor。

本页不冻结 `z → FoodValue` 的生产映射。

不要直接对离散标签做“Preferred + 1 档”式字符串运算；那会让跨边界、标定和插值难以解释。

## 7. 与 prey size / state 的边界

DietaryShift 只负责“当前更偏向哪类食物”。

如果 FoodValue 还包含：

- prey size appropriateness；
- energy / handling value；
- prey life-stage；
- prey state-specific value；

这些仍应作为 FoodValue 自己的明确输入，不全部塞进 DietaryShift。

特别是 StateTriggerValue 继续独立：

```text
DietaryShift
→ target / food value

StateTriggerValue
→ 当前 prey state 是否额外触发攻击
```

不能因为当前偏爱 baitfish，就把 sudden darting trigger 再放大一遍，除非另有独立证据。

## 8. Bake 输出形态

Fish Condition Bake 不应只输出：

```text
DietaryShift = 0.7
```

更合理的是：

```text
DietaryShiftProfile {
  prey_family_A: delta,
  prey_family_B: delta,
  ...
}
```

可以是稀疏 profile：未发生偏转的 family 使用已定义的 neutral zero；缺失配置仍需与 KnownZero 区分。

具体 profile 的 key 应复用项目已有 prey / food taxonomy，不在本页新造第二套食物分类。

## 9. Unknown / zero

必须区分：

```text
Δ(prey) = 0
→ 已知当前无偏转

Δ(prey) = Unknown
→ 当前 FoodValue 不能假装使用 base 值继续结算
```

如果某 prey family 明确不参与 DietaryShift，则应声明 NotApplicable / Disabled，而不是依赖字段缺失推断。

## 10. 玩家策略故事

该变量应购买类似：

```text
同样的 Activity
同样的 FeedingMotivation
同样的 Wariness

今天 baitfish 倾向增强、crayfish 倾向减弱
→ baitfish-like presentation 相对上升
→ crayfish-like presentation 相对下降
```

而不是：

```text
所有 lure 都一起更容易咬
```

后者属于 FeedingMotivation。

## 11. 当前 OPEN

- base food preference 的 production scale；
- `z_base + Δ_diet → FoodValue` 的生产映射；
- center / reference anchor 的最终选择与权重；
- DietaryShift profile 的 prey taxonomy owner；
- raw causes（季节、猎物丰度、生命周期等）如何 Bake 成 profile；
- shift 幅度的 effect-size budget；
- 是否需要 species × stage 的不同 shift sensitivity。

在这些问题闭合前，本页只冻结职责、相对偏转语义、Reject 边界和 common-mode 禁止规则。

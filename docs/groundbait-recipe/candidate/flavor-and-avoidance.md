# Flavor、小药与 Avoidance Candidate

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页整理 Flavor 的两条分支、小药和 Avoidance 的候选结构。它不定义 FCF Current Contract；连续化学强度分支按基线保持阻塞。

## 1. 作用范围

Flavor 只回答：

> 水中出现了哪些可感知的化学线索，目标鱼如何解释这些线索？

它不回答：

- 实体食物有多少；
- 颗粒尺寸能否处理；
- 雾化、沉降或留存；
- 最终中鱼概率。

Flavor 当前可以影响 `encounter`、趋近、回避候选和 Response 的 Flavor 输入，不在 Feeding Event 的 `selection_m` 动作选择中再次消费 Chemical Cue。

## 2. 两条分支

仓内 PC 基线的准入状态决定了两条分支：

- **分支 A（已准入）**：只使用化学类型 / 身份，也就是 `presentation.chemical_signature`。它不携带连续强度。
- **分支 B（未准入）**：使用 Cue Exposure、Composition 和 Intensity。它需要 `cue.chemical_intensity` / `cue.odor_concentration` 先获得 Owner 准入。

出处：`docs/baselines/FCF-PC-BASELINE-R2-20260916.md` 第 60 行、`docs/baselines/FCF-PC-BASELINE-R3-20260916.md` 第 64 行、`docs/holdout/FCF-PC-R2_BLIND_HOLDOUT_R1_20260916.md` 第 240–248 行。

当前工作候选是分支 A。分支 B 只保留结构说明，不参与计算。

## 3. 分支 A：类型集合

### 3.1 输入

每个 Ingredient 提供化学签名集合：

```text
IngredientCueFacts
├─ signature_set: {GRAIN, FISH, GARLIC, ...}
└─ dose_cost
```

Recipe 的签名集合是各 Ingredient 签名的并集：

```text
SignatureSet(recipe) = ∪ signature_set_i
```

同一签名由多个 Ingredient 提供时，仍然只是一个签名。分支 A 不区分浓度、比例或强度。

### 3.2 鱼侧关系

鱼侧对签名使用稀疏关系：

```text
relation(fish, signature) ∈ {POSITIVE, NEUTRAL, AVOID}
```

规则：

- 未配置的关系默认 `NEUTRAL`，不是 `AVOID`。
- `AVOID` 必须显式配置，不能从低偏好推导。
- 不建立全量 Fish × Signature 矩阵，只为有明显解释价值的对配置关系。

### 3.3 候选聚合

分支 A 只处理集合，不处理比例。当前候选是一个优先级解析，不是数值求和：

```text
if any signature in SignatureSet has relation AVOID:
    FlavorOutcome = AVOID
elif any signature in SignatureSet has relation POSITIVE:
    FlavorOutcome = POSITIVE
else:
    FlavorOutcome = NEUTRAL
```

性质：

- `AVOID` 优先，避免“加一点喜欢的东西抵消排斥”的套利。
- 多个 `POSITIVE` 签名不叠加，不产生全家桶。
- 多个 `NEUTRAL` 签名不改变结果。
- 该解析是 Candidate，不是 Current 规则。

### 3.4 分支 A 的限制

分支 A 不能表达：

- 同一签名的强弱；
- 不同签名之间的相对比例；
- 少量小药对整体画像的稀释或增强；
- 浓度过高导致的 Overdose。

这些都需要分支 B。分支 A 只够回答“有没有这个类型”和“是否有显式排斥”。

## 4. 分支 B：连续强度（阻塞）

以下结构只作说明，当前不可用于计算：

```text
CueExposure_f = Σ_i dose_i × cue_potency_i(f)
FlavorComposition = CueExposure_f / Σ_f CueExposure_f
FlavorIntensity = Σ_f CueExposure_f
FlavorResponse_B = F(fish, FlavorComposition, FlavorIntensity, Avoidance)
```

阻塞原因：

- `cue.chemical_intensity` / `cue.odor_concentration` 未准入；
- 任何连续强度、浓度或气味量级都不得在当前阶段落成生产字段；
- 准入与否是产品决策，不是实现细节。

分支 B 一旦准入，至少需要回答：

- 强度是释放量、到达鱼端浓度，还是感知强度；
- Composition 是否按 Exposure 归一化；
- Intensity 是否有上限、衰减和 Overdose；
- 小药的 Potency、剂量、衰减和成本如何定义。

## 5. Avoidance

### 5.1 与“不喜欢”分开

- 不喜欢：没有获得明显正收益，结果为 `NEUTRAL`。
- 排斥：显式配置的 `AVOID`，出现时主动压低响应。

`NEUTRAL` 不是 `AVOID`；缺少配置也不是 `AVOID`。

### 5.2 与 Wariness 分开

- `Wariness` 是 Fish Condition 的动态状态，随过程累积；
- `Avoidance` 是稀疏配置的签名关系，不随时间自行变化。

两者都可能压低响应，但来源和 trace 必须分开，不能合并成一个负分。

### 5.3 稀疏配置

只为有明显解释价值的 Fish × Signature 对配置 `AVOID`。不建立全量负数矩阵，也不把“浓度过高”自动解释成“天生排斥”。

## 6. 小药

### 6.1 分支 A

小药可以：

- 增加一个化学签名；
- 触发该签名的 `POSITIVE` 或 `AVOID` 关系；
- 占剂量或成本；
- 不增加实体食物质量。

小药不能：

- 提供固定 Bonus；
- 绕过签名集合直接改最终响应；
- 在不占成本的情况下改变结果。

### 6.2 分支 B（阻塞）

小药可以定义为低剂量、高 Potency 的 Chemical Cue Modifier，改变 Exposure、Composition 或 Intensity。它仍必须：

- 有剂量上限；
- 有成本；
- 有衰减或持续时间；
- 不增加实体食物质量。

具体公式在分支 B 准入后再定。

## 7. 在 Feeding Event 中的位置

Flavor 可以影响：

- `encounter`：鱼是否可能发现或接近；
- Response 的 Flavor 候选：正向线索、排斥候选及其 provenance。

当前工作候选不在 `selection_m` 动作选择中再次消费 Chemical Cue。若未来 Owner 选择让 Flavor 直接影响动作选择，必须关闭对应的 Response 消费路径并补充 provenance / 去重规则。

Flavor 不直接影响：

- 动作可行性；
- 动作成功；
- 对象尺寸约束；
- 环境权重或圆桌竞争。

## 8. 分支 A 结构 Fixture

鱼侧关系：

```text
GRAIN  = POSITIVE
FISH   = NEUTRAL
GARLIC = AVOID
```

配方：

| 配方 | 签名集合 | 结果 |
|---|---|---|
| A | {GRAIN} | POSITIVE |
| B | {GRAIN, FISH} | POSITIVE |
| C | {GRAIN, GARLIC} | AVOID |
| D | {FISH} | NEUTRAL |
| E | {GRAIN, GARLIC 小药 1%} | AVOID |

结构行为：

- B 加入一个 `NEUTRAL` 签名，不产生额外正收益。
- C 加入一个 `AVOID` 签名，结果翻转为 `AVOID`。
- E 的小药只增加签名并占成本，不增加实体质量；它可以把结果从 `POSITIVE` 翻成 `AVOID`。
- 分支 A 不能表达 B 中 GRAIN 与 FISH 的比例，也不能表达小药对强度的稀释。

## 9. 退化测试

1. **签名集合去重**：同一签名由两个 Ingredient 提供，集合仍只有一个元素。
2. **拆分不变**：把一个 Ingredient 拆成两个同签名 ID，结果不变。
3. **未配置不是排斥**：没有 `AVOID` 配置时，结果不能变成 `AVOID`。
4. **不喜欢不是排斥**：低偏好或 `NEUTRAL` 不能自动升级为 `AVOID`。
5. **AVOID 优先**：同时存在 `POSITIVE` 和 `AVOID` 签名时，结果为 `AVOID`。
6. **小药有成本**：小药必须占剂量或成本，且不增加实体食物质量。
7. **隔离**：改变 Flavor 不改变尺寸成功、动作可行性或释放速度。
8. **分支 B 阻塞**：未准入前，不能使用连续强度、浓度或气味量级。

## 10. 未收口问题

- 分支 B 是否准入，以及准入后强度、Composition 和 Intensity 的口径。
- 分支 A 的优先级解析是否足够表达玩法；是否需要在不引入连续强度的前提下增加粗粒度等级。
- 多个 `POSITIVE` 签名之间是否需要区分，还是分支 A 只保留“有正响应”。
- 化学签名族和字典如何定义。
- 小药的剂量上限、成本、衰减和持续时间。
- Overdose 与天生 Avoidance 是否首版同时建模。
- `Diet Shift` 是否改变签名关系，时间尺度多大。
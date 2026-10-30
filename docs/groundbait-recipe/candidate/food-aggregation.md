# Food Aggregation｜食物目标聚合 Candidate

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页整理 Food Target 的合并、饱和和多 Target 聚合候选。它不是 FCF Current Contract；多 Target 聚合按基线 R0 保持 OPEN。

## 1. 作用范围

Food Aggregation 只回答：

> 这份配方提供了哪些可摄食目标，目标鱼对这些目标的响应有多强？

它不回答：

- 鱼是否发现或接近；
- 颗粒尺寸能否处理；
- 香味是否合适；
- 鱼是否愿意留下；
- 最终中鱼概率。

Food 响应可以进入 Feeding Event 的动作选择或对象价值，但不进入动作可行性、动作成功、环境权重或圆桌竞争。

## 2. Food Target 字典

`Food Target` 是版本化、低基数、稳定、可跨 Item 复用的可摄食目标概念，不是 Item ID、SKU、商品分类或味型。

候选成员只作示例，不是定案：

```text
GRAIN
AQUATIC_INSECT
CRUSTACEAN
PLANT
ALGAE
PREPARED_FOOD
```

出处与边界：

- R0 把 `FeedingTargetKey` 定义为版本化、低基数、稳定、可跨 Item 复用的 feeding-target domain concept，示例成员不冻结 taxonomy。出处：`docs/baselines/FCF-PC-BASELINE-R0-20260915.md` 第 181–197 行。
- R3 明确 lane 中的 `FEEDING_TARGET_TEST_VOCABULARY = {SMALL_BAITFISH, CRUSTACEAN}` 只是 validation fixture 的局部 test vocabulary，不是 canonical dictionary。出处：`docs/baselines/FCF-PC-BASELINE-R3-20260916.md` 第 52–55 行。
- 字典成员变更需要版本化 admission，不能在运行时临时新增。

## 3. 同 Target 合并

对每个 Food Target `t`，先把同一目标下的 Ingredient 贡献合并，再做 Target 级饱和：

```text
E_t = Σ_i recipe_share_i × food_identity_i(t) × potency_i
```

其中：

- `food_identity_i(t)` 是 Ingredient 对目标 `t` 的身份权重；
- `potency_i` 是 Ingredient 自身的强度或品质；
- 求和发生在同一目标内部，不跨目标。

这一步必须先做。否则同一作用的 Ingredient 拆成多个 ID 后，会各自饱和，产生拆分套利。

## 4. Target 级饱和

```text
R_t = P_t × S_t(E_t)
```

- `P_t` 是鱼侧对该目标的偏好；
- `S_t` 是饱和函数；
- `R_t` 是目标级响应。

候选性质：

1. `S_t(0) = 0`；
2. `S_t` 单调非减；
3. `S_t` 有界，例如不超过 1；
4. `S_t` 连续；
5. `S_t` 凹，边际收益递减。

`P_t = 0` 表示鱼对该目标没有正响应；它不等于“缺少配置”。缺少配置应报错或显式缺席，不能静默当成 0。

饱和函数族和参数仍是 OPEN。当前只固定性质，不固定形式。

## 5. 多 Target 聚合

```text
FoodResponse = Agg_T({R_t})
```

`Agg_T` 仍为 OPEN。基线 R0 明确把 multi-target hypothesis aggregation 列为不冻结项，并禁止 Coding Agent 自行引入 `sum`、`weighted average`、`max` 或 `Noisy-OR`。出处：`docs/baselines/FCF-PC-BASELINE-R0-20260915.md` 第 256–268 行、第 495–513 行。

本页只固定任何候选算子都必须满足的性质：

1. **非负**：`Agg_T ≥ 0`；
2. **单调**：任一 `R_t` 增加，`Agg_T` 不下降；
3. **有界**：`Agg_T` 不超过声明的上界；
4. **可交换**：Target 顺序不影响结果；
5. **连续**：`R_t` 的微小变化不导致跳变；
6. **跨 Target 递减**：向已经很强的总响应再加一个目标，增量应小于向很弱的总响应加同样目标；
7. **无全家桶**：加入少量第三目标不能产生大幅跃升；
8. **零处理**：`R_t = 0` 不贡献；
9. **无隐式互补**：任何 Target 之间的协同必须显式声明，不能由算子偷偷产生。

候选算子族的性质对照，仅用于讨论，不是定案：

| 算子 | 有界 | 单调 | 混配价值 | 主要风险 |
|---|---|---|---|---|
| 直接求和 | 否 | 是 | 有 | 全家桶、无界 |
| 取最大 | 是 | 是 | 无 | 忽略真实混配 |
| 加权平均 | 是 | 是 | 有，但会稀释 | 强 Target 被弱 Target 拉低 |
| Noisy-OR | 是 | 是 | 有 | 假设独立，多弱 Target 可能过奖 |
| 求和后全局饱和 | 是 | 是 | 有，递减 | 需要全局饱和参数 |

选择哪一个需要 Owner 裁决。当前不采用任何一个作为默认公式。

## 6. 结构 Fixture

只验证同 Target 合并和 Target 级饱和。多 Target 部分只比较候选算子的输出范围，不选边。

### 6.1 输入

鱼侧偏好：

```text
P_GRAIN      = 0.8
P_CRUSTACEAN = 0.6
P_INSECT     = 0.0
```

饱和函数用 `S(E) = E / (E + 1)`，仅用于手算。

配方：

| 配方 | 组成 | E_GRAIN | E_CRUSTACEAN |
|---|---|---:|---:|
| A | 40% 谷物 | 0.4 | 0 |
| B | 40% 谷物 + 20% 甲壳 | 0.4 | 0.2 |
| C | 60% 谷物 | 0.6 | 0 |
| D | 40% 谷物拆成两个 20% ID | 0.4 | 0 |

### 6.2 目标级响应

```text
R_GRAIN      = 0.8 × S(E_GRAIN)
R_CRUSTACEAN = 0.6 × S(E_CRUSTACEAN)
```

| 配方 | R_GRAIN | R_CRUSTACEAN |
|---|---:|---:|
| A | 0.23 | 0.00 |
| B | 0.23 | 0.10 |
| C | 0.30 | 0.00 |
| D | 0.23 | 0.00 |

结构行为：

- A 到 C 只增加同一目标，响应按饱和上升。
- D 把同一目标拆成两个 ID，结果与 A 相同，没有拆分套利。
- B 引入第二个目标，目标级响应分别成立；总响应取决于 `Agg_T`，本页不选。

### 6.3 多 Target 算子对照

以 B 的 `R_GRAIN = 0.23`、`R_CRUSTACEAN = 0.10` 为例：

| 算子 | 输出 |
|---|---:|
| 直接求和 | 0.33 |
| 取最大 | 0.23 |
| 按曝光加权平均 | 0.19 |
| Noisy-OR | 0.31 |
| 求和后全局饱和 | 0.25 |

这些数字只说明不同算子会给出不同策略倾向：

- 直接求和奖励混配，但可能无界。
- 取最大不奖励混配。
- 加权平均会被弱 Target 稀释。
- Noisy-OR 奖励互补，但假设独立。
- 求和后全局饱和保留混配价值，同时有界。

它们都不是本页的默认公式。

### 6.4 拆分对照

同一 Target 先合并，再饱和：

```text
S(0.2) + S(0.2) = 0.33
S(0.4)          = 0.29
```

分开饱和会高于合并后饱和，说明必须在饱和之前合并同一 Target。

## 7. 退化测试

1. **同 Target 拆分不变**：把一个 Ingredient 拆成两个同 Target ID，`E_t` 和 `R_t` 不变。
2. **同 Target 合并不变**：两个同 Target Ingredient 合并计算与先算 Exposure 再相加一致。
3. **饱和单调**：`E_t` 增加时，`R_t` 不下降。
4. **饱和有界**：`R_t ≤ P_t`（或声明的上界）。
5. **零曝光**：`E_t = 0` 时，`R_t = 0`。
6. **缺失不等于零**：未配置的 Target 不能静默当成 `P_t = 0`。
7. **算子可交换**：交换 Target 顺序，`Agg_T` 不变。
8. **全家桶**：加入少量第三 Target 不能绕过跨 Target 递减性质。
9. **隔离**：改变 Food Target 不改变尺寸成功、释放速度或环境权重。

## 8. 进入 Feeding Event 的位置

Food 响应可以进入：

- 动作选择：鱼更愿意尝试哪个对象；
- 对象价值：一次有效摄食对鱼值多少。

Food 响应不进入：

- 动作可行性；
- 动作成功；
- 环境权重；
- 圆桌竞争；
- 最终 Response 的直接倍率。

## 9. 未收口问题

- Food Target 字典的正式成员和版本化 admission 流程。
- 饱和函数族和参数如何标定。
- 多 Target 聚合算子由 Owner 裁决。
- Food 响应按对象计算还是按 Feeding Place 计算。
- Food 响应如何分配到动作选择与对象价值。
- `Diet Shift` 如何改变 `P_t`，时间尺度多大。
- `P_t` 是静态配置还是随 Engagement Mode 变化。R1 的 `StaticTargetAffinity = Species × FeedingTargetKey` 不含 Mode 轴，若未来需要 Mode 轴，应按新语义申请处理。
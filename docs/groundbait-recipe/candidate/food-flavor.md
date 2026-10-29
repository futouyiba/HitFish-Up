# Food 与 Flavor 机制候选

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页只整理 Food 与 Flavor 在完整中鱼链中的候选位置和未决项，不定义 Current Contract，也不把化学强度当作已准入量。

## 1. 为什么 Food 与 Flavor 要分开

Food 回答“有什么可吃”，Flavor 回答“水中有哪些可感知的化学线索”。两者可以来自同一个 Ingredient，但语义不同：

- Food 不进入 `FeedingTargetKey` 以外的化学字段。
- Flavor 不直接塞进 Food Target。
- 同一个虾粉可以同时提供甲壳类 Food Identity 和腥味线索，但两条路径分别进入，不合并成一个总分。

出处：`docs/terminology.md` §3.3 的响应条件；`decisions/working-decisions.md` 的 WD-02、WD-03。

## 2. Food

### 2.1 当前候选

```text
Ingredient 质量 / 份额
  → 同 Food Target 的 Exposure 合并
  → Target 级边际递减
  → 鱼侧 Food Target Preference
  → 进入选择或对象价值
```

设计意图：

- 避免逐 Ingredient 饱和导致“拆成多个 ID 就变强”。
- 允许鱼同时喜欢两个 Target 时出现有限混配价值。
- 不保证混配一定优于单一 Target 专精。

出处：`candidate/proposal.md` §4、`decisions/working-decisions.md` 的 WD-04。完整合并、饱和和多 Target 聚合见 `food-aggregation.md`。

### 2.2 在 Feeding Event 中的位置

Food 影响两件事：

- 动作选择：鱼更愿意尝试哪个对象；
- 对象价值：一次有效摄食对鱼值多少。

Food 不直接影响：

- 动作是否可行；
- 尺寸处理是否成功；
- 环境权重或圆桌竞争。

### 2.3 未决项

完整聚合见 `food-aggregation.md`。其中同 Target 合并和 Target 级饱和是当前候选；多 Target 聚合按基线 R0 保持 OPEN，不在本页选择 `sum`、`weighted average`、`max` 或 `Noisy-OR`。

## 3. Flavor

### 3.1 当前候选

```text
Ingredient amount / dose
× Chemical Cue Potency
→ Cue Exposure by flavor family
→ Flavor Composition + Flavor Intensity
```

要点：

- `Composition` 是各味型在总 Cue Exposure 中的相对组成，不是原料质量百分比。
- 加入新味型会改变和稀释原有组成，不按味型逐项领取独立 Bonus。
- 少量高 Potency 小药可以显著改变画像。
- 小药不是免费 Buff，必须占剂量或成本。

出处：`candidate/proposal.md` §5、`decisions/working-decisions.md` 的 WD-05、WD-06。

### 3.2 准入问题

仓内 PC 基线把化学强度判为未准入：

- R2：`cue.chemical_intensity` / `cue.odor_concentration` 保持候选，不进入 core；`presentation.chemical_signature` 只表达 chemical type / identity。
- R3：chemical magnitude / odor concentration 标为 `DEFERRED / NOT_ADMITTED`。
- H17：把它标为 `NEW_PRIMITIVE_REQUIRED`，并说明是否准入是产品决策。

出处：`docs/baselines/FCF-PC-BASELINE-R2-20260916.md` 第 60 行、`docs/baselines/FCF-PC-BASELINE-R3-20260916.md` 第 64 行、`docs/holdout/FCF-PC-R2_BLIND_HOLDOUT_R1_20260916.md` 第 240–248 行。

因此本页保留两个分支：

- **分支 A（强度未准入）**：只使用化学类型和稀疏关系，不宣称连续强度。
- **分支 B（Owner 准入强度后）**：使用 Cue Exposure、Composition 和 Intensity。

当前采用分支 A 作为工作候选，分支 B 标为 OPEN。对应冲突登记 C-02。分支 A 的集合解析、Avoidance 和小药结构见 `flavor-and-avoidance.md`。

### 3.3 在 Feeding Event 中的位置

Flavor / Chemical Cue 可以影响：

- Encounter：鱼是否可能发现或接近；
- Selection：鱼更愿意尝试哪个对象；
- Avoidance：某些 Cue 主动压低响应。

Flavor 不直接影响：

- 对象尺寸约束；
- 动作可行性；
- 动作成功；
- 环境权重或圆桌竞争。

### 3.4 小药

小药当前定义为低剂量、高 Potency 的 Chemical Cue Modifier。

它不能是：

```text
基础配方分 + 固定小药 Bonus
```

它必须：

- 改变 Cue Exposure 或 Composition；
- 占剂量或成本；
- 不增加实体食物质量。

### 3.5 排斥与不喜欢

- 不喜欢：没有获得明显正收益。
- 排斥：Cue 出现会主动压低响应。

Avoidance 应稀疏配置，不建立全量 Fish × Flavor 负数矩阵。浓度过高导致的普遍 Overdose 与天生排斥某味型是不同机制，首版不必同时购买两套复杂度。

出处：`candidate/proposal.md` §5.4、`decisions/working-decisions.md` 的 WD-07。

## 4. 与 Fish Condition 的边界

- Food 和 Flavor 的 Exposure 不直接写 `Diet Shift`。
- `Diet Shift` 是 Fish Condition 的动态偏移。
- `Wariness` 是状态，Sparse Avoidance 是配置；两者都压低响应，但来源和 trace 必须分开。

对应冲突登记 C-12、C-13。

## 5. 最小结构反例

- 同一作用拆成多个 Ingredient ID 后变强：拆分套利。
- 每个 Food / Flavor Target 都放一点：全家桶。
- 小药不占成本却提升响应：免费 Buff。
- 加入新味型必然变好：忽略稀释。
- Flavor 改变尺寸成功：越权。
- Food 改变释放速度：越权。
- 天气直接映射成味型偏好：密码化。
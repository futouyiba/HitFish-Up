# 台钓中鱼机制｜端到端工作算法

> 状态：Candidate / Working Algorithm
> 日期：2026-10-30
> 边界：本文把当前目录与 Proposal C 的已知边界组织成一条可执行的工作算法。它不是 FCF Current Contract，不提供生产标定值，也不把 PR 分支上的 Owner 裁定升级为 `main` 上的 Current。
>
> 上游依赖：Proposal C 的 Issue #152 五项 Owner 裁定记录在 PR [#130](https://github.com/futouyiba/HitFish-Up/pull/130) 的提交 `5caf1f119ab6e5a5c595a4ba913e7962aa338ec3`。截至 2026-10-30，该 PR 仍为 draft。本文承接其工作边界，但每次实现前仍须以最新提交复核。

## 1. 一句话版本

```text
配置与环境事实
  → 环境烘焙 / DEF / SpatialDistributionWeight
  → Fish Condition
  → Opportunity / L
  → 玩家呈现与窝料状态
  → Response Evaluation / C
  → 按接口类型组装：
      GenericFCF: SpatialDistributionWeight × AdaptationCoeff
      ProposalCOpportunity: q = L × C
  → Roundtable Weight List
  → Crowding-out / Clipping / Draw
  → Spawn
  → Fish AI（本仓范围外）
```

Groundbait 只负责中间这条链：

```text
Recipe Facts
  → Recipe Distribution
  → Physical Release
  → Feeding Place State
  → Feeding Event
  → Food / Flavor / Edible Utilization / EIO
  → Response 输入
```

## 2. 量、状态和阶段

### 2.1 四种不同的量

| 量 | 范围 | 是否归一化 | 是否概率 |
|---|---|---:|---:|
| `BaseWeight` | 投鱼条目 / 空间候选 | 否 | 否 |
| `SpatialDistributionWeight` | 空间与鱼种模式 | 否 | 否 |
| `AdaptationCoeff` / `C` | 响应候选 | 通常不归一化，按 Contract 定上界 | 否 |
| `RoundtableWeight` | 抽鱼候选 | 否 | 否 |
| `DrawProbability` | 一次抽样 | 是 | 是 |

禁止用一个字段同时表示这些量。任何转换都必须带阶段和身份轴。

### 2.2 最小身份轴

每个候选至少携带：

```text
FishStock
Species
FishQualityRef
EngagementMode
ConditionGroupRef
Place
Time
PresentationId
```

Groundbait 的对象和状态还要携带：

```text
RecipeId
IngredientId / provenance
ParticleBucket
ObjectId（若对象已 materialize）
```

### 2.3 阶段所有权

| 阶段 | 唯一主要生产者 | 输出 | 不能做什么 |
|---|---|---|---|
| Bake | 环境烘焙 | DEF、空间结果、`SpatialDistributionWeight` | 不读取玩家临时呈现，不输出最终概率 |
| Fish Condition | 鱼况机制 | `Activity`、`FeedingMotivation`、`DietShift`、`Wariness` | 不由 Groundbait 直接写入 |
| Opportunity | Opportunity 机制 | `L` 与机会身份、持续时间、去重、重评估 | 不生成 Response `C` |
| Groundbait Release | 物理释放 | `FeedingPlaceState` | 不直接生成中鱼倍率 |
| Feeding Event | 事件机制 | 可行动作、选择、成功、摄食消耗、EIO | 不改变环境权重 |
| Response | 响应机制 | `C` / `AdaptationCoeff` | 不重新乘 `BaseWeight`，不输出抽样概率 |
| Roundtable | 圆桌 | `RoundtableWeightList` | 不反向改写上游事实 |
| Draw / Spawn | 抽鱼与生成 | 抽取结果、鱼对象 | 不把空鱼生成成鱼对象 |

## 3. 环境烘焙与空间权重

本算法消费既有 Bake 输出，不复制 Fixed Bake 公式。

```text
Raw Condition
  → Derived Condition
  → Factor
  → Environment Component
  → Gate / Fit
  → Channel Aggregation
  → Mode Spatial Result
  → DEF
  → FinalEnvCoeff
```

对每个具有有效身份轴的候选：

```text
SpatialDistributionWeight
  = BaseWeight × FinalEnvCoeff
```

约束：

1. `BaseWeight` 只乘一次。
2. `SpatialDistributionWeight` 在圆桌抽样前不归一化。
3. Response 只读该结果，不重新计算环境系数。
4. Groundbait 改变 `FeedingPlaceState`，不写回 DEF。
5. Bake 失败是 `ResolutionIncomplete` 或显式错误，不伪装成零权重或空鱼。

## 4. Fish Condition 工作更新

四个参数是鱼侧状态，不是四个独立 Bonus。实现可以把状态按 FishStock、ConditionGroup、时间片保存，但必须声明键和生命周期。

对任一 `[0,1]` 状态 `x`，采用有界的一阶更新作为工作算法：

```text
α = 1 - exp(-Δt / τ_x)

x_target = clamp(
    base_x
    + Σ enabled_cause support_x,cause
    + Σ event_delta_x,event,
    0,
    1
)

x_next = clamp((1 - α) × x_prev + α × x_target, 0, 1)
```

规则：

- 缺失的必需 cause 产生 `ResolutionIncomplete`，不当作 0。
- 显式 `Disabled` / `NotApplicable` 不参加聚合。
- 同一环境事实不能同时在 `EnvCoeff` 和状态更新中产生两份未经说明的效果。
- `Activity` 只进入运动 / Closing 负担和 Fish AI 边界，不作为动态 `CapacityModifier`。
- `FeedingMotivation` 进入 `WillingnessThreshold`。
- `DietShift` 改变上游 `TargetRelation` / `FoodValue`，不由 Food 事件直接写入。
- `Wariness` 进入风险解释；它与静态 / 稀疏 `Avoidance` 保持独立 provenance。
- 没有跨 session 历史 Contract 前，状态生命周期限定在声明的 session / 场景范围。

这里的 `τ_x`、cause support 和 event delta 是实现前输入，不是本文提供的生产参数。

## 5. Opportunity 与 `L`

承接 Proposal C 的上游工作裁定：

```text
Spatial facts
  → Opportunity
  → L
```

Spatial 只提供：位置、区域、几何、垂直层、有效空间窗口等事实。Opportunity 唯一负责：

- opportunity identity；
- duration / temporal support；
- dedupe；
- reevaluation；
- reducer；
- native opportunity support `L`。

实际空间覆盖不产生 `FastSearchInformationBonus`。更快移动只有在实际遍历产生新的 opportunity identity 或 support 时才改变 `L`。

`L` 是候选机会支持，不是概率；不在 Response 内再次生成或乘一个搜索系数。

## 6. 配方到 Feeding Place

### 6.1 配方分布

对 Ingredient `i`：

```text
edible_mass_i = recipe_share_i × edible_fraction_i
edible_total = Σ_i edible_mass_i

physical_share_b = Σ_i recipe_share_i × physical_dist_i(b)

edible_share_b =
  Σ_i edible_mass_i × edible_dist_i(b)
  / edible_total
```

约束：

- `recipe_share` 必须和为 1，不能静默归一化。
- `edible_total = 0` 时，不产生 Edible Size 输入。
- 载体可以有粒径和物理释放，但不进入 `edible_share`。
- 每个桶保留来源、配方、Ingredient 和对象状态。

### 6.2 物理状态转移

对每个物料桶，采用竞争转移率作为工作算法：

```text
Λ = λ_breakdown + λ_leave
p_move = 1 - exp(-Λ × Δt)

B = A × p_move × λ_breakdown / Λ
S = A × p_move × λ_leave / Λ
H = A × (1 - p_move)
```

其中 `H` 是本步转移后仍留在当前地点、等待 Feeding Event 消费的可用量。

- `B` 进入 `U`，表示已不可处理；
- `S` 进入 `L`，表示已离开当前地点；
- `H` 保持在当前地点，等待 Feeding Event 消费；
- `λ_* = 0` 时按零率处理，`Λ = 0` 时 `B = S = 0` 且 `H = A`。

Feed Event 在物理转移后消费 `H`：

```text
E = min(H, E_event)
A_next = H - E
L_next = L + S
U_next = U + B
C_next = C + E
```

每个账本满足：

```text
A + L + C + U = initial_mass
```

化学线索另记：

```text
Q_next = clamp(Q + R, 0, 1)
```

`Q` 不与实体质量共享守恒式。`λ_breakdown`、`λ_leave`、`R` 的生产输入来自 Ingredient / 环境 / 水体事实，未提供时不得猜测数值。

## 7. Flavor 与 Food

### 7.1 Flavor

当前准入分支只使用签名集合：

```text
SignatureSet = union(Ingredient.signature_set)
```

关系：

```text
relation(fish, signature) ∈ {POSITIVE, NEUTRAL, AVOID}
```

工作解析：

```text
if any AVOID:
    FlavorState = AVOID
    FlavorSignal = explicit_penalty_candidate
elif any POSITIVE:
    FlavorState = POSITIVE
    FlavorSignal = positive_candidate
else:
    FlavorState = NEUTRAL
    FlavorSignal = neutral_candidate
```

`AVOID` 在当前 Owner ballot 未收口前只产生带 provenance 的排斥候选，不是硬门，也不直接变成 `Reject`。它在 Response 中的唯一消费位置仍待 C-13a / C-13b 与对应 Current 收口；同一签名不能同时作为硬门和软修正消费。连续浓度、比例、Intensity 和 Overdose 未获得准入前不得进入计算。`Avoidance` 与 `Wariness` 必须分别追踪。

### 7.2 Food

目标 `t` 先在同目标内合并：

```text
E_t = Σ_i recipe_share_i × food_identity_i(t) × potency_i
```

鱼侧目标偏好由静态基础偏好和动态食性偏移得到：

```text
P_t = clamp(BaseAffinity_t + DietShift_t, 0, 1)
```

目标级响应采用有界、单调、凹函数：

```text
S_t(E_t) = E_t / (K_t + E_t)
R_t = P_t × S_t(E_t)
```

多目标聚合目前只保留参数化接口：

```text
FoodValue = AggFood({R_t}; aggregation_profile)
```

`AggFood` 必须满足非负、单调、有界、可交换、连续、跨 Target 边际递减、零处理和无隐式互补。`WD-26` 仍将具体算子标为 OPEN；全局饱和只保留为实验分支，不进入默认 V1 生产接入，也不能作为 Owner 已裁定的公式。`K_t`、`BaseAffinity` 和聚合 profile 是校准 / Owner 输入，不是本文给定的生产值。

## 8. Edible Size 与 Feeding Event

### 8.1 动作可行性

对对象 `o` 和动作 `m`：

```text
feasibility_m
  = location_gate_m
  × object_state_gate_m
  × size_condition_m
```

`size_condition_m` 读取体尺、形态、动作能力、对象尺寸、形状、硬度、团聚和释放状态。它不进入 encounter 的吸引，也不直接进入 FoodValue。

```text
F = {m | feasibility_m > 0}
```

若 `F = ∅`，事件不能成功。

### 8.2 动作选择和成功

在可行集合内产生选择分布。当前工作算法只让选择读取动作自身代价和可行状态；Food / Flavor 不在此处再消费，避免与 Response 的候选输入重复计权：

```text
z_m = β_m
    - w_cost × ActionCost_m
    - w_wary × Wariness

P(select m | F) = exp(z_m) / Σ_{j∈F} exp(z_j)
```

对所选动作：

```text
p_success_m
  = feasibility_m
  × success_shape_m
  × success_hardness_m
  × success_cohesion_m
  × success_state_m

p_ingest_m = p_success_m × ingestability_m
```

对象一次事件的有效摄食量：

```text
E_event(o)
  = contactable_mass(o)
  × P(encounter | place, cue, fish_condition)
  × Σ_{m∈F} P(select m | F) × p_ingest_m
```

一次事件只允许一条实际动作路径。复制动作、Ingredient 或机制不能增加收益。摄食成功后从 `available_edible_bins` 减少并转入 `C`。

### 8.3 EIO

```text
EIO = Σ_o E_event(o) × value(o)
```

`value(o)` 必须声明为质量、数量、能量或其它单一价值空间；在未声明前只能使用无量纲相对值。EIO 是 Candidate 中间输入，不等于 `C`，也不等于抽样概率。

EIO 在 Owner / Current 收口前不进入 active `DecisionMargin`，也不默认赋予独立的 `w_eio`。它只通过已声明的 Response Component / Candidate branch 接口消费；该接口必须明确单位、归一化基准、provenance 和唯一消费者。
## 9. Response Evaluation

### 9.1 硬门与软量

先求已收口的硬门：

```text
G = G_resolution × G_opportunity × G_prey
```

其中：

- `G_resolution = 0` 仅用于显式非法 / Reject；`Unknown` 传播为 `ResolutionIncomplete`，不静默转 0；
- `G_opportunity = 0` 表示没有有效 Opportunity / 可消费机会；
- `G_prey = 0` 表示目标解释被明确 Reject。

`AVOID` 当前只产生带 provenance 的 Flavor 排斥候选，不自动进入硬门；它的唯一消费位置须待 C-13a / C-13b 与对应 Current 收口。
然后求软的 `DecisionMargin`：

```text
M = b
  + w_food × FoodValue
  + w_trigger × AttackTrigger
  - w_close × ClosingCost
  - w_risk × RiskCost
  - w_threshold × WillingnessThreshold
```

`EIO` 不在 active `M` 中。若未来 Owner / Current 将 EIO 接入 Response，必须作为独立 Candidate branch 明确其唯一消费位置，并先补齐单位、归一化基准、provenance 和与 Feeding Event 的去重规则。

Proposal C 的 active 边界要求：

- `AttackTrigger` 首版只准入 Escape-like；
- `RiskCost` 未启用合法 `TackleConspicuousness` 输入时为 0；
- `PredictionCost` 第一版不进入 `M`；
- `CapacityModifier` 不进入 `M`；
- `Activity` 只调制 Closing soft cost；
- `L` 不进入 active `M`。Proposal C 中它只作为 `q = L × C` 的 Opportunity 支持；GenericFCF 不消费 `L`。

### 9.2 从 Margin 到响应系数

用单调有界投影得到响应系数：

```text
C_conditional = clamp(σ(M), 0, 1)
C = G × C_conditional
```

`σ` 是声明版本的单调 sigmoid；若项目需要零基线 / 上界标定，可替换为经过批准的 `M0/M1` 投影，但必须保持：硬门先于投影，`Reject` 不可被软量救活，`C` 不归一化成概率。

如果存在 latent presentation / prey interpretation `θ`：

```text
C = G × E_θ[C_conditional(θ)]
```

顺序必须是：先在每个 `θ` 上执行 hard gate 与 margin，再对 `C(θ)` 求期望；不能先平均成本再判断硬门。

### 9.3 Groundbait 的接入

Groundbait 的 `FoodValue` 可作为 Response 的候选输入；`EIO` 在 Owner / Current 收口前不进入 active `M`。Flavor 的 `Avoidance` 只保留为带 provenance 的候选，不自动成为硬门。Food、Flavor、EIO 每份事实只能有一个已声明的主要消费者：不能在 Feeding Event 和 active Response Margin 中重复消费同一份输入。

候选消费矩阵：

| 事实 | Feeding Event | active Response `M` | 当前状态 |
|---|---|---|---|
| `FoodValue` | 不直接消费 | 可作为唯一 Food 响应输入 | Candidate / Working |
| `FlavorSignal` / `Avoidance` | 不直接消费 | 消费位置待 C-13a / C-13b 收口 | Candidate / OPEN |
| `EIO` | 由 Feeding Event 生产 | 不消费 | Candidate / OPEN |

Groundbait 不直接写 Fish Condition，不直接改 `SpatialDistributionWeight`，不再乘一次 `L`。
同一持续窝料效果只能进入持久响应场或即时响应条件中的一个有效增量；若同时保留来源状态和即时摘要，必须带 provenance 并明确只消费一次。

## 10. 圆桌、抽鱼与生成

每个响应候选必须带不可混淆的接口类型：

```text
GenericFCF
  output: AdaptationCoeff
  assembly: SpatialDistributionWeight × AdaptationCoeff

ProposalCOpportunity
  output: final candidate weight q = L × C
  assembly: no additional SpatialDistributionWeight multiplication
```

调用者必须按接口类型选择唯一一条组装路径；禁止把 `q` 当作 `AdaptationCoeff`，也禁止把 `AdaptationCoeff` 当作已经包含 `L` 的 `q`。

```text
RoundtableWeight_k
  = SpatialDistributionWeight_k × AdaptationCoeff_k
```

对 Proposal C 的机会响应分支，采用上游 Owner 裁定的接口：

```text
q_k = L_k × C_k
```

其中 `L` 已由 Opportunity 消费 Spatial facts 后产生，`C` 是 Response 输出。两种表达不能叠加使用：实现必须先声明当前候选属于哪条接口，并证明 `L` 是否已经包含空间权重；不得未经声明计算 `SpatialDistributionWeight × L × C`。

之后按现有圆桌规则执行：

```text
candidate weights
  → FishStock 去重
  → 实鱼权重汇总
  → 0.3.4.1 空鱼扩张（若该版本启用）
  → 现有 Crowding-out
  → 现有 Clipping
  → Roundtable Weight List
  → normalize at draw only
  → Draw
  → Spawn if selected candidate is real fish
```

约束：

- 空鱼是伪候选，不生成鱼对象。
- 前置求值失败不能转成空鱼。
- `C=0` 的显式 Reject 候选不参与正向竞争；`ResolutionIncomplete` 不是 `C=0`。
- 圆桌不反向修改 `SpatialDistributionWeight`、Fish Condition 或 Feeding Place。
- 两条接口必须二选一：通用 FCF 候选只使用 `SpatialDistributionWeight × AdaptationCoeff`，其中空间权重由 `SpatialDistributionWeight` 提供；Proposal C 候选只使用 `q = L × C`，其中机会支持由 Opportunity 产出的 `L` 提供。
- 通用 FCF 接口不得再乘 `L`；Proposal C 接口不得再乘 `SpatialDistributionWeight` 或第二个 `L`。任何上游已消费的权重都不得在圆桌重复相乘。

## 11. 缺失、错误与回退

| 状态 | 语义 | 是否继续 |
|---|---|---|
| `Resolved(value)` | 已解析数值 | 按公式继续 |
| `Zero(value)` | 合法真实零 | 按零贡献继续 |
| `Disabled` | 该机制显式关闭 | 跳过该机制，不改写其它机制 |
| `NotApplicable` | 该对象不适用 | 从对应聚合排除 |
| `Unknown` | 尚未解析 | 传播 `ResolutionIncomplete` |
| `Invalid` | 输入违反 Contract | 阻断该候选并报错 |
| `Reject` | 明确语义拒绝 | 产生 typed zero / hard gate |

禁止：

- `Unknown → 0`；
- `Invalid → 空鱼`；
- 缺少绑定 → `IGNORED`；
- 失败的前置计算 → 正常候选；
- 用候选 Fixture 数字补生产字段。

## 12. 版本化实现顺序

### V0：结构闭合

实现对象、身份轴、状态机、provenance、typed status、守恒账本和 Roundtable 汇合。所有校准量由配置注入。

### V1：候选算法

按本文顺序接入：Bake 读取、Fish Condition 更新、Opportunity `L`、Recipe Distribution、Release、Food、Flavor、Edible Size、Feeding Event、Response、Roundtable。

### V2：生产化前置

补齐并审核：

- Fish Condition cause、时间尺度和生命周期；
- Opportunity 的 identity / duration / reducer；
- `TackleConspicuousness` 生产字段；
- Food Target、偏好、饱和参数；
- Release rates、Cue release、对象价值空间；
- Response 权重、投影和校准；
- 圆桌四件 Current Contract。

在 V2 完成前，本文仍只能作为 Working Algorithm，不能写成已实现或已收口 Current。

## 13. 通过条件

实现或审阅至少通过以下性质：

1. 同一派生事实只有一个主要生产者。
2. `A + L + C + U` 对每个物料账本守恒。
3. 同 Target 先合并再饱和；拆分 Ingredient 不产生收益。
4. 载体改变时，若可食分布不变，Edible Utilization 不变。
5. 不可行动作不能获得选择概率。
6. 一次 Feeding Event 不能通过复制动作获得额外收益。
7. `Unknown`、`Invalid`、`Reject` 和合法零不混淆。
8. 已声明且只使用一条圆桌接口，任何上游权重不重复消费。
9. 圆桌权重在抽样前不是概率。
10. 空鱼不生成鱼对象。
11. Groundbait 移除后，Bake、Fish Condition 和圆桌 Current 规则不变。
12. Prediction、CapacityModifier、FastSearchInformationBonus、EntryDisturbance 未被偷偷恢复。

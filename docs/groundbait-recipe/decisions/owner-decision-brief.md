# 台钓中鱼机制｜Owner 裁决清单

> 状态：Candidate / Working Document
> 日期：2026-10-29
> 用途：把冲突登记整理成可逐项裁决的清单，供 Owner 或外部评审阅读。
> 边界：本文不是 FCF Current Contract，也不替 Owner 做决定。推荐项只是工作建议。

## 0. 给外部评审的说明

这份文件来自 `docs/groundbait-recipe/`。该目录是 Candidate / Working Design，不是已收口的 Current Contract。

请按以下约束评审：

1. 不要建议单一 `RecipeFit = Food + Flavor + Particle + Physical`。
2. 不要把 Candidate 词当成 Current 术语。
3. 不要引入未准入的连续化学强度。
4. 不要给生产数值；只判断结构和方向。
5. 对每项给出：选哪个、为什么、翻转成本、需要补什么证据。

## 1. 已完成的部分

候选链已经按以下顺序推到接口层：

- Size：可食尺寸约束、Gold Fixture、载体隔离。
- Food：同 Target 先合并再饱和；多 Target 算子 OPEN。
- Flavor：签名集合分支可用；连续强度分支阻塞。
- Physical Release：离散时间状态转移、四份守恒账本、线索分离。
- Attraction / Retention：判断为不独立成模块。
- Response Aggregation：四条候选输出映射到现有 Response Stage。

Current 只定义到 `SpatialDistributionWeight × AdaptationCoeff → 下游候选权重`，没有给 `AdaptationCoeff` 公式。

## 2. 术语速查

| 词 | 含义 |
|---|---|
| SpatialDistributionWeight | 基础权重乘环境系数，未归一化，不是概率 |
| AdaptationCoeff | 响应阶段的无量纲倍率，公式未定 |
| Fish Condition | 活跃度、摄食动机、食性偏移、警戒度 |
| Response Stage | 读取烘焙结果、鱼况、响应组件和玩家刺激，输出适配系数集 |
| Persistent Response Field | 持续玩家行为的增量层，不复制 DEF |
| Feeding Place State | 本目录工作词：当前地点的对象、线索、位置、状态 |
| Feeding Event | 本目录工作词：一次摄食机会的遇见、可行、选择、成功 |
| Effective Ingestion Opportunity | 本目录工作词：一次事件的有效摄食机会，落点未定 |

## 3. 决策总表

| ID | 决策 | 层级 | 推荐 | 翻转成本 |
|---|---|---|---|---|
| C-01 | 尺寸归属 | 形状 | 动作约束，不进 Food Value | 低 |
| C-02 | 化学强度准入 | 形状 | v1 只用签名集合 | 中 |
| C-03 | Feeding Event vs Decision | 形状 | 事件分解为主 | 中高 |
| C-04 | Effective Ingestion Opportunity 落点 | 接口 | 暂缓，等 C-03 | 中 |
| C-05 | Persistent Response Field 语义 | 接口 | 叠加层，不复制 DEF | 低中 |
| C-06 | 环境食物浓度与窝料对象 | 接口 | 背景 + 增量，显式合并 | 中 |
| C-07 | Overfeeding / Local Population | 边界 | 首版后置 | 低 |
| C-08 | Encounter 是否拆分 | 接口 | v1 保持合并 | 中 |
| C-09 | 刺鱼 / 抽鱼接口 | 边界 | 本候选不进入刺鱼 | 低 |
| C-10 | 多 Feeding Mechanism 聚合 | 边界 | max 只作上界 | 低 |
| C-11 | 多 Food Target 聚合 | 边界 | 同 Target 合并 + 饱和，算子 OPEN | 中 |
| C-12 | Diet Shift 所有权 | 边界 | 留在 Fish Condition | 中 |
| C-13 | Wariness vs Avoidance | 边界 | 分开 | 低 |
| C-14 | Feeding Readiness 是否正式状态 | 边界 | 不新增 | 低 |

## 4. 第一层：形状决策

### C-01 尺寸归属

**背景**：Groundbait 候选把尺寸当作动作约束；Proposal C 把 `SizePreferenceAdjustment` 放进 `CurrentFoodValue`。

**选项**：

A. 尺寸只进动作可行性和成功，不进 Food Value。
B. 尺寸只进 Food Value，不进动作。
C. 两者分层：动作约束和 Food Value 各读一次，但分别记录 provenance。

**推荐**：A。现有 Size、Feeding Event、Gold Fixture 都按 A 写；C 会要求两套证据，当前没有。

**请回答**：选 A / B / C？如果选 C，两边的输入和去重规则是什么？

### C-02 化学强度准入

**背景**：R2/R3 只准入 `chemical_signature`（类型 / 身份），`cue.chemical_intensity` / `cue.odor_concentration` 是 DEFERRED / NOT_ADMITTED。H17 说明浓度级策略真实存在，但准入是产品决策。

**选项**：

A. v1 只用签名集合，不表达浓度、比例或强度。
B. 准入连续强度，建立 Exposure、Composition、Intensity 和衰减。
C. 先做粗粒度等级（如 TRACE / PRESENT / STRONG），但明确是新的产品决策。

**推荐**：A。可测试、不违反基线；B 会引入新的 primitive 和标定工作；C 仍是 magnitude，需要 Owner 明确批准。

**请回答**：选 A / B / C？如果选 B 或 C，强度是释放量、到达鱼端浓度，还是感知强度？

### C-03 Feeding Event vs Feeding Decision

**背景**：Groundbait 用事件分解：`encounter → feasible action → selection → success → ingestion`。Proposal C 用决策裕量：`DecisionMargin = FoodValue + Trigger - Closing - Prediction - Risk - WillingnessThreshold`。

**选项**：

A. 以事件分解为主，决策裕量作为后续鱼侧解释。
B. 以决策裕量为主，事件分解只作实现细节。
C. 两套并存，按场景选择。

**推荐**：A。事件分解已经有 Feeding Place、动作可行、对象状态和守恒；决策裕量更适合描述“鱼为什么犹豫”，不适合替代对象处理链。

**请回答**：选 A / B / C？如果选 A，决策裕量放在 Response 前还是 Response 内？

## 5. 第二层：接口决策

### C-04 Effective Ingestion Opportunity 落点

选项：

A. Response Condition 的派生状态。
B. Response Component 的输入。
C. 独立因子。
D. 只供某个既有计算消费，不单独暴露。

**推荐**：暂缓，等 C-03。若 C-03 选 A，则倾向 B；若选 C，则可能 D。

**请回答**：选哪个？它的单位和量纲是什么？

### C-05 Persistent Response Field 语义

选项：

A. DEF 之外的运行时叠加层，DEF 只读。
B. 直接修改 DEF 的增量。
C. 独立的状态对象，Response 读取时合并。

**推荐**：A。术语说它“不复制 DEF”，Groundbait 也明确不写回 DEF。

**请回答**：选哪个？时间、范围、衰减和重叠规则由谁定义？

### C-06 环境食物浓度与窝料对象

选项：

A. 环境侧是背景事实，窝料是玩家增量，消费端合并。
B. 二者是同一事实，必须在消费端去重。
C. 环境侧不表达食物浓度，只由窝料表达。

**推荐**：A。需要显式合并规则，避免同一事实双算。

**请回答**：选哪个？合并发生在 Response 前还是 Response 内？

### C-08 Encounter 是否拆分

选项：

A. v1 保持合并的 Encounter。
B. 拆成 Detection、Approach、Temporal Opportunity。
C. 只拆 Detection 和 Approach，时间窗口并入 Approach。

**推荐**：A。当前没有足够证据区分“没发现”和“不想靠近”；拆分需要感官和空间模型。

**请回答**：选哪个？如果拆分，谁拥有 cue 羽流几何和到达鱼端浓度？

### C-09 刺鱼 / 抽鱼接口

选项：

A. 本候选停在 Response / Roundtable，不进入刺鱼。
B. 输出吞饵成功概率，交给刺鱼。
C. 输出 Candidate retention，交给抽鱼。

**推荐**：A。刺鱼属于 Fish AI，范围外；B/C 都需要新的状态和证据。

**请回答**：选哪个？

## 6. 第三层：边界与内容决策

### C-07 Overfeeding / Local Population

选项：

A. 首版后置，只记录缺口。
B. 放进 Feeding Place（对象与线索状态）。
C. 放进 Fish Condition（饱食 / 警戒）。
D. 建立独立的 Local Population / Residence 模块。

**推荐**：A。外部研究只作线索，仓内没有证据和位置。

**请回答**：选哪个？如果后置，failure boundary 是什么？

### C-10 多 Feeding Mechanism 聚合

选项：

A. `max` 只作“总能选最优路径”的上界，不作默认公式。
B. 用选择概率加权。
C. 直接求和（已排除）。

**推荐**：A。C 已经排除；B 需要选择模型和证据。

**请回答**：选哪个？

### C-11 多 Food Target 聚合

选项：

A. 同 Target 合并 + 饱和；多 Target 算子保持 OPEN。
B. 直接求和。
C. 取最大。
D. Noisy-OR。
E. 求和后全局饱和。

**推荐**：A。基线 R0 禁止自行引入 B–E；需要 Owner 裁决。

**请回答**：选哪个？如果选 A，什么时候允许选具体算子？

### C-12 Diet Shift 所有权

选项：

A. 留在 Fish Condition，作为动态偏移。
B. 进入 Food Value 的加项。
C. 进入 Flavor Composition。
D. 不建模。

**推荐**：A。术语已把 Diet Shift 列为 Fish Condition 参数。

**请回答**：选哪个？时间尺度和记忆窗口是什么？

### C-13 Wariness vs Avoidance

选项：

A. 分开：Wariness 是动态状态，Avoidance 是静态稀疏关系。
B. 合并成一个负分。
C. 只保留 Avoidance。

**推荐**：A。两者来源和 trace 不同，合并会重复扣分。

**请回答**：选哪个？

### C-14 Feeding Readiness 是否正式状态

选项：

A. 不新增，只作为描述性说法。
B. 作为第五个 Fish Condition 状态。
C. 作为派生复合量，不落 Schema。

**推荐**：A。术语表只定义四个参数；B/C 需要 Owner 明确。

**请回答**：选哪个？

## 7. 请外部评审回答的最小问题集

1. C-01 选 A / B / C？为什么？
2. C-02 选 A / B / C？如果选 B/C，强度口径是什么？
3. C-03 选 A / B / C？决策裕量放在哪？
4. C-04–C-06、C-08、C-09 各选哪个？
5. C-07、C-10–C-14 各选哪个？
6. 哪些项可以现在定，哪些必须等证据？
7. 有没有我们没列出的冲突？

## 8. 不要做什么

- 不要建议单一 `RecipeFit`。
- 不要给生产数值。
- 不要把 Candidate 词写成 Current 术语。
- 不要引入未准入的连续化学强度。
- 不要用“大多数游戏都这样”代替证据。
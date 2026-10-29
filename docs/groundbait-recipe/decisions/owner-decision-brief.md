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
3. 在 C-02 裁决前，不得默认假定连续化学强度已经准入。若推荐 B 或 C，必须显式说明新增 primitive、口径、标定成本和失败边界。
4. 不要给生产数值；只判断结构和方向。
5. 对每项给出：选哪个、为什么、翻转成本、需要补什么证据。
6. 如果某项不应现在裁决，说明理由和依赖条件。

## 1. 已完成的部分

候选链已经按以下顺序推到接口层：

- Size：可食尺寸约束、Gold Fixture、载体隔离。
- Food：同 Target 先合并再饱和；多 Target 算子 OPEN。
- Flavor：签名集合分支是当前工作分支；连续强度待 C-02 裁决。
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
| Decision Margin | Proposal C 的决策裕量；是否进入 Feeding Event 待 C-03b |
| Effective Ingestion Opportunity | 本目录工作词：一次事件的有效摄食机会，落点未定 |
| Overfeeding | 投喂过多后的非单调反馈；与 Local Population 分开 |
| Local Population / Residence | 局地鱼群数量或驻留状态；与 Overfeeding 分开 |

## 3. 决策总表

| ID | 决策 | 层级 | 推荐 | 翻转成本 |
|---|---|---|---|---|
| C-01 | 尺寸归属 | 形状 | 动作约束，不进 Food Value | 低 |
| C-02 | 化学强度准入 | 形状 | v1 签名集合；B/C 可裁 | 中 |
| C-03a | Feeding Event 是否外层结构 | 形状 | 是 | 中 |
| C-03b | Decision Margin 进入哪一步 | 形状 | selection；首版可暂缓 | 中高 |
| C-04 | Effective Ingestion Opportunity 落点 | 接口 | 暂缓，等 C-03a/b | 中 |
| C-05a | Persistent Field 数据所有权 | 接口 | DEF 只读，响应层持有增量 | 低 |
| C-05b | Persistent Field 表示与消费 | 接口 | 独立对象；即时投影是备选 | 低中 |
| C-06 | 环境食物浓度与窝料对象 | 接口 | 背景 + 增量，显式合并 | 中 |
| C-07a | Overfeeding | 边界 | 首版后置 | 低 |
| C-07b | Local Population / Residence | 边界 | 首版后置 | 低 |
| C-08 | Encounter 是否拆分 | 接口 | v1 合并；magnitude 准入后再决定 | 中 |
| C-09 | 刺鱼 / 抽鱼接口 | 边界 | 本候选不进入刺鱼 | 低 |
| C-10 | 多 Feeding Mechanism 聚合 | 边界 | max 只作上界 | 低 |
| C-11 | 多 Food Target 聚合 | 边界 | 同 Target 合并 + 饱和，算子 OPEN | 中 |
| C-12a | Diet Shift 所有权 | 边界 | 留在 Fish Condition | 低 |
| C-12b | Diet Shift 消费语义 | 边界 | 暂不决定；Food/Flavor 分别取证 | 中 |
| C-13a | Wariness 与 Avoidance 是否不同语义 | 边界 | 不同 | 低 |
| C-13b | Avoidance 表示形式 | 边界 | 暂不决定 | 中 |
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

B 和 C 都是合法选项，不是被预先排除的方案。选择它们时，需要说明：

- 新增哪个 primitive；
- 强度是释放量、到达鱼端浓度，还是感知强度；
- 谁生产、谁消费；
- 标定成本和失败边界。

**推荐**：A。可测试、不违反基线；B 会引入新的 primitive 和标定工作；C 仍是 magnitude，需要 Owner 明确批准。

**请回答**：选 A / B / C？如果选 B 或 C，上述四项分别是什么？

### C-03a Feeding Event 是否作为外层过程结构

**背景**：Groundbait 用事件分解：`encounter → feasible action → selection → success → ingestion`。Proposal C 用决策裕量描述鱼如何比较和判断。两者未必互斥：决策裕量可以嵌在事件分解的某一步里。

**选项**：

A. 采用 Feeding Event 作为外层过程结构。
B. 不采用；用 Decision Margin 作为外层结构。
C. 其它结构，需要说明。

**推荐**：A。事件分解已经有 Feeding Place、动作可行、对象状态和守恒；Decision Margin 更适合作为其中一步的决策函数。

**请回答**：选 A / B / C？如果选 C，外层步骤是什么？

### C-03b 若采用 Feeding Event，Decision Margin 进入哪一步

**前提**：仅当 C-03a 选 A 时回答。

**选项**：

A. 进入 `selection`，作为鱼比较可行动作的决策函数。
B. 进入单独的 approach / risk 步骤。
C. 不进入；Feeding Event 使用其它选择规则。
D. 暂不决定。

**推荐**：A。selection 是鱼在可行动作之间做取舍的位置；如果首版不需要显式比较，可以先 D。

**请回答**：选 A / B / C / D？如果选 A 或 B，Decision Margin 的输入和输出是什么？

## 5. 第二层：接口决策

### C-04 Effective Ingestion Opportunity 落点

**依赖**：C-03a 和 C-03b。

选项：

A. Response Condition 的派生状态。
B. Response Component 的输入。
C. 独立因子。
D. 只供某个既有计算消费，不单独暴露。

**推荐**：暂缓。若 C-03a 选 A 且 C-03b 选 A，则倾向 B；若 C-03b 选 C，则可能 D。

**请回答**：选哪个？它的单位和量纲是什么？

### C-05a Persistent Field 数据所有权

选项：

A. DEF 只读，响应层持有增量。
B. 修改或写回 DEF。
C. 其它，需要说明。

**推荐**：A。术语说 Persistent Response Field 是“增量层，不复制 DEF”；Groundbait 也明确不写回 DEF。

**请回答**：选哪个？如果选 A，增量的时间、范围、衰减和重叠由谁定义？

### C-05b Persistent Field 表示与消费

**前提**：与 C-05a 正交。即使选 A，仍需决定表示方式。

选项：

A. 独立的 Persistent Field 对象，Response 读取时合并。
B. 在 Response 求值时即时投影，不持久化独立对象。
C. 其它，需要说明。

**推荐**：A。术语已经把它命名为一个 Field；B 可以作为实现优化，但不改变语义。

**请回答**：选哪个？如果选 A，Schema 由谁维护？如果选 B，投影的输入和缓存策略是什么？

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

**请回答**：选哪个？

**依赖条件**：只有 C-02 准入 magnitude 后，才继续决定“谁拥有 cue 羽流几何和到达鱼端强度”。如果 C-02 选 A，本题只决定是否拆分 Encounter，不涉及浓度所有权。

### C-09 刺鱼 / 抽鱼接口

选项：

A. 本候选停在 Response / Roundtable，不进入刺鱼。
B. 输出吞饵成功概率，交给刺鱼。
C. 输出 Candidate retention，交给抽鱼。

**推荐**：A。刺鱼属于 Fish AI，范围外；B/C 都需要新的状态和证据。

**请回答**：选哪个？

## 6. 第三层：边界与内容决策

### C-07a Overfeeding

选项：

A. 首版后置，只记录缺口。
B. 放进 Feeding Place（对象与线索状态）。
C. 放进 Fish Condition（饱食 / 警戒）。
D. 建立独立的 Overfeeding 模块。

**推荐**：A。外部研究只作线索，仓内没有证据和位置。

**请回答**：选哪个？如果后置，failure boundary 是什么？

### C-07b Local Population / Residence

选项：

A. 首版后置，只记录缺口。
B. 只体现为机会权重变化，不建显式鱼群状态。
C. 建立显式 Local Population / Residence 状态。
D. 其它，需要说明。

**推荐**：A。外部研究提到 Feed 会增加局部 population，但没有仓内证据支持具体状态和更新规则。

**请回答**：选哪个？如果选 C，状态的键、更新和衰减是什么？

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

### C-12a Diet Shift 所有权

选项：

A. 留在 Fish Condition，作为动态偏移。
B. 不建模。
C. 修改现有语义，需要 Owner 明确覆盖。

**推荐**：A。术语已把 Diet Shift 列为 Fish Condition 参数。

**请回答**：选哪个？如果选 C，覆盖范围和迁移方案是什么？

### C-12b Diet Shift 消费语义

**前提**：仅当 C-12a 选 A 时回答。

选项：

A. 修改 Food Preference。
B. 修改 Flavor Preference。
C. 两者都改，但必须分别有因果依据。
D. 暂不决定。

**推荐**：D。当前没有证据说明 Diet Shift 应该只改 Food、只改 Flavor，还是两者都改。

**请回答**：选哪个？如果选 A/B/C，因果依据和时间尺度是什么？

### C-13a Wariness 与 Avoidance 是否不同语义

选项：

A. 不同：Wariness 是状态，Avoidance 是 Cue 反应。
B. 相同：合并成一个负分。
C. 只保留 Avoidance。

**推荐**：A。两者来源和 trace 不同，合并容易重复扣分。

**请回答**：选哪个？

### C-13b Avoidance 的表示形式

**前提**：仅当 C-13a 选 A 时回答。

选项：

A. 静态稀疏 Profile。
B. Context-sensitive relation。
C. 其它，需要说明。
D. 暂不决定。

**推荐**：D。当前 Working Decision 只收敛了“排斥 ≠ 不喜欢”和“稀疏配置”，没有收敛它必须是静态关系。

**请回答**：选哪个？如果选 A/B/C，触发条件和去重规则是什么？

### C-14 Feeding Readiness 是否正式状态

选项：

A. 不新增，只作为描述性说法。
B. 作为第五个 Fish Condition 状态。
C. 作为派生复合量，不落 Schema。

**推荐**：A。术语表只定义四个参数；B/C 需要 Owner 明确。

**请回答**：选哪个？

## 7. 请外部评审回答的最小问题集

1. C-01 选 A / B / C？为什么？
2. C-02 选 A / B / C？如果选 B/C，新增 primitive、口径、标定成本和失败边界是什么？
3. C-03a 选 A / B / C？C-03b 选 A / B / C / D？
4. C-04、C-05a、C-05b、C-06、C-08、C-09 各选哪个？
5. C-07a、C-07b、C-10、C-11、C-12a、C-12b、C-13a、C-13b、C-14 各选哪个？
6. 哪些项可以现在定，哪些必须等证据？
7. 有没有我们没列出的冲突？

## 8. 不要做什么

- 不要建议单一 `RecipeFit`。
- 不要给生产数值。
- 不要把 Candidate 词写成 Current 术语。
- 不要默认连续强度已经准入；推荐 B/C 时，必须说明新增 primitive、口径和成本。
- 不要用“大多数游戏都这样”代替证据。
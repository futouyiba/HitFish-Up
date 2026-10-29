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
- Attraction / Retention：Candidate 判断已完成，当前不独立成模块。
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
| C-03b | Decision Margin 进入哪一步 | 形状 | D（首版可暂缓），否则 A | 中高 |
| C-04a | EIO 是否为一等中间语义 | 接口 | 是，显式派生状态 | 中 |
| C-04b | 若显式，谁消费 | 接口 | Response Component | 中 |
| C-05a | Persistent Field 数据所有权 | 接口 | DEF 只读，响应层持有增量 | 低 |
| C-05b | Persistent Field 是否存在独立语义 | 接口 | 存在独立持续语义 | 低中 |
| C-06a | 是否存在环境背景食物浓度 | 接口 | 有 | 中 |
| C-06b | 背景与增量是否保留独立 provenance | 接口 | 保留，消费前合并 | 中 |
| C-06c | 合并在哪里发生 | 接口 | Response 前；待 C-06a/b | 中 |
| C-07a1 | Overfeeding 是否首版纳入 | 边界 | 后置 | 低 |
| C-07a2 | Overfeeding 承载层 | 边界 | 若纳入再定 | 中 |
| C-07b | Local Population / Residence | 边界 | 首版后置 | 低 |
| C-08 | Encounter 是否拆分 | 接口 | v1 合并；magnitude 准入后再决定 | 中 |
| C-09 | 刺鱼 / 抽鱼接口 | 边界 | 本候选不进入刺鱼 | 低 |
| C-10 | 多 Feeding Mechanism 聚合 | 边界 | 生产聚合 OPEN；max 仅 Fixture 上界 | 低 |
| C-11b | 多 Food Target 聚合 | 边界 | 保持 OPEN；具体算子待裁 | 中 |
| C-12a1 | Diet Shift 所有权 | 边界 | Fish Condition | 低 |
| C-12a2 | 保留或覆盖现有语义 | 边界 | 保留 | 中 |
| C-12a3 | 不设所有权时旧语义如何处置 | 边界 | 保留为描述性候选 | 中 |
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

### C-03a 是否采用 Feeding Event 作为外层过程结构

**背景**：Groundbait 用事件分解：`encounter → feasible action → selection → success → ingestion`。Proposal C 用决策裕量描述鱼如何比较和判断。两者不在同一层：事件分解是过程结构，决策裕量是某一步的比较函数。

**选项**：

A. 是，采用 Feeding Event 作为外层过程结构。
B. 否，暂不引入统一 Feeding Event 外层结构，继续沿用既有 Response / Proposal C 各自的求值结构。
C. 其它结构，需要说明。

**推荐**：A。事件分解已经有 Feeding Place、动作可行、对象状态和守恒；Decision Margin 的位置由 C-03b 单独决定。

**请回答**：选 A / B / C？如果选 C，外层步骤是什么？

### C-03b 若采用 Feeding Event，Decision Margin 进入哪一步

**前提**：仅当 C-03a 选 A 时回答。

**选项**：

A. 进入 `selection`，作为鱼比较可行动作的决策函数。
B. 进入单独的 approach / risk 步骤。
C. 不进入；Feeding Event 使用其它选择规则。
D. 暂不决定。

**推荐**：D（首版不需要显式比较时），否则 A。selection 是鱼在可行动作之间做取舍的位置。

**请回答**：选 A / B / C / D？如果选 A 或 B，Decision Margin 的输入和输出是什么？

## 5. 第二层：接口决策

### C-04a 是否建立 Effective Ingestion Opportunity 这个一等中间语义

选项：

A. 是，作为显式派生状态。
B. 否，只作为某个现有计算内部量。
C. 暂缓。

**推荐**：A。它是 Feeding Event 的输出，也是 Response 接入的候选接口；显式化后才有唯一生产者。

**请回答**：选哪个？如果选 A，它的单位和量纲是什么？

### C-04b 若显式存在，谁消费

**前提**：仅当 C-04a 选 A 时回答。

选项：

A. Response Component。
B. 某个既有 Factor。
C. Response Aggregation 内部。
D. 其它，需要说明。

**推荐**：A。Response Component 是现有响应评价的消费单元；选 B/C 需要说明为什么不走组件。

**请回答**：选哪个？消费时的输入和去重规则是什么？

### C-05a Persistent Field 数据所有权

选项：

A. DEF 只读，响应层持有增量。
B. 修改或写回 DEF。
C. 其它，需要说明。

**推荐**：A。术语说 Persistent Response Field 是“增量层，不复制 DEF”；Groundbait 也明确不写回 DEF。

**请回答**：选哪个？如果选 A，增量的时间、范围、衰减和重叠由谁定义？

### C-05b Persistent Field 是否存在独立语义

**前提**：与 C-05a 正交。即使选“DEF 只读”，仍需决定是否存在独立的持续语义。

本题只裁语义：是否存在一个具有持续生命周期、来源、范围、衰减语义的 Persistent Field。物理上是否 materialize 为独立对象、是否按需计算、如何缓存，交给 Implementation Brief，不由 Owner 裁。

选项：

A. 存在独立的 Persistent Field 语义。
B. 不存在独立语义；持续效果只是 DEF 或其它状态的投影。
C. 暂不决定。

**推荐**：A。术语已经把它命名为一个 Field，并给出持续增量语义。

**请回答**：选哪个？如果选 A，来源、范围、衰减的语义边界由谁定义？

### C-06a 环境是否存在 Groundbait 之外的背景食物浓度

选项：

A. 有，环境侧存在背景 Food Availability / Concentration。
B. 没有，食物浓度只由窝料表达。
C. 暂不决定。

**推荐**：A。术语把“食物浓度”列为环境因子示例，但具体口径仍需确认。

**请回答**：选哪个？如果选 A，背景事实的载体和口径是什么？

### C-06b 背景与玩家增量是否保留独立 provenance

**前提**：仅当 C-06a 选 A 时回答。

选项：

A. 保留独立 provenance，消费前合并。
B. 直接物化成一个统一状态，不再区分来源。
C. 其它，需要说明。

**推荐**：A。保留 provenance 才能查重和调试；合并可以发生在消费前。

**请回答**：选哪个？如果选 A，合并后的状态是否仍保留来源引用？

### C-06c 合并在哪里发生

**前提**：仅当 C-06a 选 A，且 C-06b 选 A 时回答。

选项：

A. 在 Response 之前合并，Response 只读合并后的状态。
B. 在 Response 内部合并，Response 同时读取两个来源。
C. 暂不决定。

**推荐**：A。先合并再进入响应，避免同一事实在响应里被两条路径各读一次。

**请回答**：选哪个？如果选 B，去重规则和 trace 放在哪里？

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

### C-07a1 Overfeeding 是否首版纳入

选项：

A. 首版后置，只记录缺口。
B. 首版纳入。
C. 暂不决定。

**推荐**：A。外部研究只作线索，仓内没有证据和位置。

**请回答**：选哪个？如果后置，failure boundary 是什么？

### C-07a2 Overfeeding 的承载层

**前提**：仅当 C-07a1 选 B 时回答。

选项：

A. 放进 Feeding Place（对象与线索状态）。
B. 放进 Fish Condition（饱食 / 警戒）。
C. 建立独立的 Overfeeding 模块。
D. 暂不决定。

**推荐**：D。首版没有证据支持具体承载层；若必须选，A 更接近投喂状态。

**请回答**：选哪个？状态的键、更新和衰减是什么？

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

A. 多 Feeding Mechanism 的生产聚合保持 OPEN；`max` 仅作为“可自由选择最佳路径”的 Fixture 上界。
B. 用选择概率加权。
C. 直接求和（已排除）。

**推荐**：A。生产聚合保持 OPEN；B 需要选择模型和证据。

**请回答**：选哪个？

### C-11a 前提：同 Target 先合并再饱和

同 Target 的 Ingredient 先合并 Exposure，再做 Target 级饱和，已作为 WD-25 工作候选。这一条不在本轮裁决；如果 Owner 要改，另行提出。

### C-11b 多个 Food Target 如何聚合

本项只问多个 Food Target 之间的聚合，不涉及同 Target 合并与饱和。

选项：

A. 保持 OPEN，暂不选择生产算子。
B. 直接求和。
C. 取最大。
D. Noisy-OR。
E. 求和后全局饱和。
F. 其它，需要说明。

**推荐**：A。基线 R0 禁止自行引入 B–E；需要 Owner 裁决。

**请回答**：选哪个？如果选 A，什么时候允许选具体算子？

### C-12a1 Diet Shift 的所有权

选项：

A. Fish Condition。
B. 其它承载位置，需要说明。
C. 明确不设所有权，不建模。

**推荐**：A。术语已把 Diet Shift 列为 Fish Condition 参数。

**请回答**：选哪个？如果选 B，承载对象是什么？如果选 C，继续回答 C-12a3。

### C-12a2 保留或覆盖现有 Fish Condition 语义

**前提**：仅当 C-12a1 选 A 时回答。

选项：

A. 保留现有语义：Diet Shift 是 Fish Condition 的动态偏移。
B. 覆盖现有语义，需要 Owner 明确。
C. 暂不决定。

**推荐**：A。术语已经给出该语义，覆盖需要新的裁定。

**请回答**：选哪个？如果选 B，覆盖范围、迁移和旧语义处置是什么？

### C-12a3 若不设所有权，现有 Diet Shift 语义如何处置

**前提**：仅当 C-12a1 选 C 时回答。

选项：

A. 保留为描述性候选，不落 Schema。
B. 废弃并迁移，需要迁移方案。
C. 其它，需要说明。
D. 暂不决定。

**推荐**：A。先保留为描述性候选，避免在未迁移前直接删除。

**请回答**：选哪个？如果选 B，迁移范围和旧引用清单是什么？

### C-12b Diet Shift 消费语义

**前提**：仅当 C-12a1 选 A，且 C-12a2 选 A 或 B 时回答。

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
C. 只保留 Avoidance；删除或废弃 Wariness，需要迁移方案。

B 和 C 会覆盖现有 Fish Condition 中 Wariness 的语义，需要 Owner 明确 override 和迁移范围。C 还是删除或废弃决定，不是纯粹的语义区分选项。

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

## 7. 建议裁决顺序

不要一次回答全部。建议分三轮：

**第一轮：模型形状**

C-01、C-02、C-03a、C-03b。

这四项决定整个模型的形状。裁完后，后面不少接口项会自动收窄。

**第二轮：接入现有 FCF**

C-04a、C-04b、C-05a、C-05b、C-06a、C-06b、C-06c、C-08、C-09。

**第三轮：首版边界与暂缓项**

C-07a1、C-07a2、C-07b、C-10、C-11b、C-12a1、C-12a2、C-12a3、C-12b、C-13a、C-13b、C-14。

每轮结束后再进入下一轮，避免把形状项和接口项混在一次回答里。

## 8. 请外部评审回答的最小问题集

1. C-01 选 A / B / C？为什么？
2. C-02 选 A / B / C？如果选 B/C，新增 primitive、口径、标定成本和失败边界是什么？
3. C-03a 选 A / B / C？C-03b 选 A / B / C / D？
4. C-04a、C-04b、C-05a、C-05b、C-06a、C-06b、C-06c、C-08、C-09 各选哪个？若 C-04a 不选 A，C-04b 是否不适用？若 C-06a 不选 A，C-06b/C-06c 是否不适用？若 C-06b 不选 A，C-06c 是否不适用？
5. C-07a1、C-07a2、C-07b、C-10、C-11b、C-12a1、C-12a2、C-12a3、C-12b、C-13a、C-13b、C-14 各选哪个？若 C-07a1 选 A，C-07a2 是否不适用？C-11a 是 WD-25 前提，不在本轮回答。
6. 若 C-12a1 选 A，C-12a2 选什么？若 C-12a2 选 B，覆盖和迁移方案是什么？若 C-12a1 选 C，C-12a3 选什么？
7. 哪些项可以现在定，哪些必须等证据？
8. 有没有我们没列出的冲突？

## 9. 不要做什么

- 不要建议单一 `RecipeFit`。
- 不要给生产数值。
- 不要把 Candidate 词写成 Current 术语。
- 不要默认连续强度已经准入；推荐 B/C 时，必须说明新增 primitive、口径和成本。
- 不要用“大多数游戏都这样”代替证据。
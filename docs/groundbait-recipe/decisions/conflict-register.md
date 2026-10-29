# 台钓中鱼机制｜冲突与未决项登记

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页登记跨文档、跨候选栈的语义冲突和未决项。它不裁决 Owner 权限内的问题，只记录出处、双方主张、影响和暂定处理。

## 1. 使用方式

文中的 `Feeding Place State`（摄食地点状态）、`Feeding Event`（摄食事件）、`Effective Ingestion Opportunity`（有效摄食机会）都是本目录的 Candidate-local 工作词。

每项记录五件事：冲突是什么、双方出处、影响哪些阶段、当前暂定处理、需要谁裁决。

暂定处理只有三类：

- `KEEP_OPEN`：没有足够依据，保持开放，不选边。
- `CANDIDATE_BRANCH`：本目录暂时采用某一分支，只作为工作选择，不自动成为 Current。
- `CURRENT_ALREADY_DECIDES`：仓内 Current 或 Owner 裁定已有明确结论，按该结论执行。

## 2. 冲突清单

### C-01｜尺寸归属

- **主张 A**：Groundbait Candidate 认为尺寸是动作约束，只进入动作可行性和成功，不进入 Food Preference 或最终 Response。出处：`candidate/edible-size-response.md`、`candidate/feeding-event.md`、`decisions/working-decisions.md` 的 WD-09、WD-13。
- **主张 B**：Proposal C 把尺寸放进食物价值：`CurrentFoodValue = clamp(BaseDietAffinity + SizePreferenceAdjustment + DietaryShiftDelta, 0, 1)`。出处：`docs/proposals/lure-response-proposal-c-current-review-entry-2026-10-27.md` 第 30–45 行。
- **冲突点**：同一尺寸既可能被当成食物偏好修正，也可能被当成动作约束。两处都算会重复计权。
- **影响**：Feeding Event、Food 选择、Response 聚合、Hookbait 复用。
- **暂定处理**：`KEEP_OPEN`。本目录只使用主张 A 的候选分支；Proposal C 的尺寸项只作为冲突来源引用，不合并。
- **裁决方**：Owner / 对应 Response Current。

### C-02｜化学强度是否准入

- **主张 A**：Groundbait Candidate 的 Flavor 主量依赖 `Flavor Intensity` 与 `Cue Exposure`。出处：`candidate/proposal.md` §5、`candidate/object-model.md` §2.3。
- **主张 B**：PC 基线把化学强度判为未准入。R2 写明 `cue.chemical_intensity` / `cue.odor_concentration` 保持候选，不进入 core；R3 把 chemical magnitude / odor concentration 标为 `DEFERRED / NOT_ADMITTED`；H17 把它标为 `NEW_PRIMITIVE_REQUIRED`，并说明是否准入是产品决策。出处：`docs/baselines/FCF-PC-BASELINE-R2-20260916.md` 第 60 行、`docs/baselines/FCF-PC-BASELINE-R3-20260916.md` 第 64 行、`docs/holdout/FCF-PC-R2_BLIND_HOLDOUT_R1_20260916.md` 第 240–248 行。
- **冲突点**：Flavor 候选的核心量没有已准入的 Current 载体；是否准入是产品决策。
- **影响**：Flavor、Chemical Cue Field、小药、发现与选择。
- **暂定处理**：`KEEP_OPEN`。当前工作分支是 A（只使用化学类型和稀疏关系）；B/C 需要 Owner 准入，不在裁决前预先排除。若选 B/C，必须说明新增 primitive、口径、标定成本和失败边界。
- **裁决方**：Owner。

### C-03a｜Feeding Event 是否作为外层结构

- **主张 A**：Groundbait Candidate 使用事件分解：`encounter → feasible action set → selection → success → ingestion`。出处：`candidate/feeding-event.md`。
- **主张 B**：不采用统一 Feeding Event 外层结构，继续沿用既有 Response / Proposal C 各自的求值结构。
- **冲突点**：事件分解是过程结构，Decision Margin 是某一步的比较函数，两者不在同一层。C-03a 只问是否采用事件分解作为外层结构。
- **影响**：Feeding Event、Response 输入、Groundbait 与拟饵机制的共用语义。
- **暂定处理**：`CANDIDATE_BRANCH`。本目录以事件分解为外层结构；Decision Margin 的位置由 C-03b 单独决定。
- **裁决方**：Owner / Response Current。

### C-03b｜Decision Margin 进入哪一步

- **前提**：仅当 C-03a 选“事件分解为外层结构”时成立。
- **主张 A**：Decision Margin 进入 `selection`，作为鱼比较可行动作的决策函数。
- **主张 B**：Decision Margin 进入单独的 approach / risk 步骤。
- **主张 C**：不进入；Feeding Event 使用其它选择规则。
- **冲突点**：现有 Groundbait 候选没有显式 Decision Margin；Proposal C 有，但没有声明它替代哪一步。
- **影响**：Feeding Event 的 selection、Response 输入、拟饵机制复用。
- **暂定处理**：`KEEP_OPEN`。本目录暂不引入 Decision Margin；若需要，优先放在 selection。
- **裁决方**：Owner / Response Current。

### C-04a｜EIO 是否为一等中间语义

- **主张 A**：Groundbait Candidate 输出 `Effective Ingestion Opportunity`，但明确它不等于 `Adaptation Coefficient`。出处：`candidate/object-model.md` §3、`candidate/response-stage-mapping.md` §2。
- **主张 B**：现有术语只定义 `SpatialDistributionWeight × AdaptationCoeff → 下游候选权重`，没有“有效摄食机会”槽位。出处：`docs/terminology.md` §5.2。
- **冲突点**：它是否作为显式派生状态存在，还是只作为某个现有计算的内部量。
- **影响**：Response 接入、圆桌权重构建、Groundbait 候选闭环。
- **暂定处理**：`KEEP_OPEN`。候选文档保留接口和单位说明。
- **裁决方**：Owner / Response Current。

### C-04b｜若显式存在，谁消费

- **前提**：仅当 C-04a 选“是，作为显式派生状态”时成立。
- **主张 A**：Response Component。
- **主张 B**：某个既有 Factor。
- **主张 C**：Response Aggregation 内部。
- **冲突点**：消费位置决定它进入哪条响应路径，以及如何与 AdaptationCoeff 组合。
- **影响**：Response 接入、组件聚合、圆桌权重。
- **暂定处理**：`KEEP_OPEN`。当前倾向 Response Component。
- **裁决方**：Owner / Response Current。

### C-05a｜Persistent Field 数据所有权

- **主张 A**：术语把 `Persistent Response Field` 定义为“运行时对 DEF 的持续性增量影响层，不复制一份 DEF”。出处：`docs/terminology.md` §4。
- **主张 B**：Groundbait Candidate 明确不把窝料写回 DEF 或 `SpatialDistributionWeight`。出处：`candidate/response-stage-mapping.md` §6。
- **冲突点**：“增量”可能被实现成直接修改 DEF，导致持续效果和即时效果重复消费。
- **影响**：持久响应、姿态响应、窝料、响动。
- **暂定处理**：`CANDIDATE_BRANCH`。本目录把持久字段理解为 DEF 之外的运行时叠加层：DEF 只读，响应层持有增量。
- **裁决方**：Owner / Response Current。

### C-05b｜Persistent Field 是否存在独立语义

- **前提**：与 C-05a 正交。即使数据所有权选“DEF 只读”，仍需决定是否存在独立的持续语义。
- **主张 A**：存在独立的 `Persistent Response Field` 语义，具有持续生命周期、来源、范围、衰减。
- **主张 B**：不存在独立语义；持续效果只是 DEF 或其它状态的投影。
- **冲突点**：如果存在独立语义，它需要自己的生命周期和衰减；如果不存在，它只是其它状态的投影。
- **影响**：Response 读取、持久字段语义、Schema 边界。
- **暂定处理**：`KEEP_OPEN`。当前倾向 A；物理 materialization、按需计算和缓存属于 Implementation Brief，不由 Owner 裁。
- **裁决方**：Owner / Response Current。

### C-06a｜环境是否存在背景食物浓度

- **主张 A**：术语把“食物浓度”列为环境因子示例。出处：`docs/terminology.md` §3.1。
- **主张 B**：Groundbait 产生独立的 `Feeding Place State` 与对象集合。出处：`candidate/object-model.md` §2.4。
- **冲突点**：环境侧是否在窝料之外表达背景食物浓度。
- **影响**：环境烘焙、Response、Groundbait 全栈。
- **暂定处理**：`KEEP_OPEN`。可能解释：有背景事实；或没有，只由窝料表达。
- **裁决方**：Owner / 环境与响应 Current。

### C-06b｜背景与玩家增量是否保留独立 provenance

- **前提**：仅当 C-06a 选“有背景事实”时成立。
- **主张 A**：保留独立 provenance，消费前合并。
- **主张 B**：直接物化成一个统一状态，不再区分来源。
- **冲突点**：保留 provenance 才能查重和调试；统一状态更简单，但难以追溯。
- **影响**：环境烘焙、Response、Groundbait 状态。
- **暂定处理**：`KEEP_OPEN`。当前倾向保留 provenance。
- **裁决方**：Owner / 环境与响应 Current。

### C-06c｜合并在哪里发生

- **前提**：仅当 C-06a 选“有背景事实”，且 C-06b 选“保留独立 provenance”时成立。
- **主张 A**：在 Response 之前合并，Response 只读合并后的状态。
- **主张 B**：在 Response 内部合并，Response 同时读取两个来源。
- **冲突点**：合并位置决定谁持有去重责任，以及 trace 放在哪里。
- **影响**：Response 输入、持久字段、Groundbait 状态。
- **暂定处理**：`KEEP_OPEN`。当前倾向 Response 前合并。
- **裁决方**：Owner / Response Current。

### C-07a1｜Overfeeding 是否首版纳入

- **主张 A**：外部研究记录 RF4 存在 overfeeding：population 下降、咬口频率降低、需要休息和补窝。出处：`programaticHitFish/docs/research/2026-10-21-rf4-bait-groundbait-mechanism-deep-research.md` 第 22–23、243–249、636、641 行。这只是外部研究，不是本仓 Current。
- **主张 B**：Groundbait Candidate 只有 `persistence / turnover`，没有 overfeed、历史累积、补窝频率和跨 session 语义。出处：`candidate/physical-release.md` §2、§8。
- **冲突点**：如果只做“越多越好”的释放，会丢失 overfeed 这个非单调策略轴；如果直接并入，又没有仓内证据和位置。
- **影响**：Physical Release、Feeding Place State、Fish Condition、补窝玩法。
- **暂定处理**：`KEEP_OPEN`。外部研究只作证据线索；是否首版纳入待 Owner 决定。
- **裁决方**：Owner。

### C-07a2｜Overfeeding 的承载层

- **前提**：仅当 C-07a1 选“首版纳入”时成立。
- **主张 A**：放进 Feeding Place（对象与线索状态）。
- **主张 B**：放进 Fish Condition（饱食 / 警戒）。
- **主张 C**：建立独立的 Overfeeding 模块。
- **冲突点**：承载层决定状态键、更新和衰减归谁。
- **影响**：Physical Release、Feeding Place State、Fish Condition。
- **暂定处理**：`KEEP_OPEN`。当前没有证据支持具体承载层。
- **裁决方**：Owner。

### C-07b｜Local Population / Residence

- **主张 A**：外部研究记录 Feed 会提高局部 fish population，overfeeding 后 population 会下降。出处：`programaticHitFish/docs/research/2026-10-21-rf4-bait-groundbait-mechanism-deep-research.md` 第 186–189、247–249 行。这只是外部研究，不是本仓 Current。
- **主张 B**：Groundbait Candidate 没有局地鱼群数量或驻留状态，只有 Feeding Place 的对象与线索。出处：`candidate/object-model.md` §2.4。
- **冲突点**：如果“留鱼”需要显式的局地鱼群状态，现有链无法表达；如果只体现为机会权重变化，又需要明确它和 Response 的关系。
- **影响**：Feeding Place、Response、抽鱼、留鱼玩法。
- **暂定处理**：`KEEP_OPEN`。首版可只记录缺口，或只体现为机会权重变化；不建显式 population state。
- **裁决方**：Owner。

### C-08｜发现与趋近的阶段划分

- **主张 A**：Groundbait Candidate 把发现和趋近合并在 `Encounter` 里。出处：`candidate/feeding-event.md` §2.1。
- **主张 B**：Proposal C 区分 `ClosingCost`、`PredictionCost` 和 `RiskCost`，把接近与风险分开；外部研究也建议把“进入范围、试探、攻击、吞饵”拆成多阶段。出处：`docs/proposals/lure-response-proposal-c-current-review-entry-2026-10-27.md` 第 162、227、242、251 行；外部研究 `programaticHitFish/docs/rf4_fishing_planet_bite_mechanism_research_report.md`。
- **冲突点**：`Encounter` 同时承担感知、接近和时间窗口，难以区分“没看见”“不想靠近”“没时间”。
- **影响**：Feeding Event、Cue、Fish Condition、刺鱼接口。
- **暂定处理**：`KEEP_OPEN`。本目录保留 `Encounter` 作为合并候选，但在对象模型里记录它可能拆成 Detection / Approach / Temporal Opportunity。
- **依赖条件**：只有 C-02 准入 magnitude 后，才继续决定“谁拥有 cue 羽流几何和到达鱼端强度”。若 C-02 选 A，本题只决定是否拆分 Encounter，不涉及浓度所有权。
- **裁决方**：Owner。

### C-09｜刺鱼与抽鱼接口

- **主张 A**：Groundbait Candidate 停在 `Effective Ingestion Opportunity`。出处：`candidate/object-model.md` §3。
- **主张 B**：Proposal C 停在 `Candidate retention`，并说归约结果进入 Candidate retention，不能在 Candidate 后段再次乘 Response。出处：`docs/proposals/lure-response-proposal-c-current-review-entry-2026-10-27.md` 第 347、359 行。
- **冲突点**：术语里没有 `Candidate retention` 这个阶段；`Effective Ingestion Opportunity` 也不等于“鱼已吞饵”。圆桌前是否还有“吞饵成功”层、刺鱼是否消费这些输出，都没有定义。
- **影响**：Response、圆桌、抽鱼、刺鱼边界。
- **暂定处理**：`KEEP_OPEN`。候选文档只声明“不进入刺鱼”，不补造接口。
- **裁决方**：Owner / 圆桌 Current。

### C-10｜多 Feeding Mechanism 的聚合

- **主张 A**：Groundbait Candidate 反对直接求和，`max` 只作为“总能自由切换、无切换成本”的简化上界。出处：`candidate/edible-size-response.md` §4、`candidate/feeding-event.md` §5、WD-12。
- **主张 B**：Proposal C 对 sibling prey 使用 `max(C_baitfish, C_crayfish, ...)`。出处：`docs/proposals/lure-response-proposal-c-current-review-entry-2026-10-27.md`。
- **冲突点**：两处都在用 `max` 做替代聚合，但对象不同：一个是动作路径，一个是猎物解释。是否允许同一算子出现在两层，没有统一说明。
- **影响**：Feeding Event、Food 选择、Response。
- **暂定处理**：`KEEP_OPEN`。生产聚合保持 OPEN；`max` 仅作为“可自由选择最佳路径”的 Fixture 上界，不作为生产聚合候选，也不推广到其它层。
- **裁决方**：Owner。

### C-11a｜同 Target 先合并再饱和（WD-25 前提）

- **状态**：`ACTIVE CANDIDATE`（WD-25）。同 Target 的 Ingredient 先合并 Exposure，再做 Target 级饱和。
- **说明**：这是当前工作候选，不在本轮 Owner ballot 中单独裁决。若 Owner 要改，另行提出。

### C-11b｜多个 Food Target 如何聚合

- **主张 A**：保持 OPEN，暂不选择生产算子。
- **主张 B**：直接求和。
- **主张 C**：取最大。
- **主张 D**：Noisy-OR。
- **主张 E**：求和后全局饱和。
- **冲突点**：基线 R0 禁止自行引入 B–E；多 Target 聚合仍未获准。
- **影响**：Food、Response、圆桌。
- **暂定处理**：`KEEP_OPEN`。多 Target 算子为 OPEN（WD-26）。
- **裁决方**：Owner。

### C-12a1｜Diet Shift 的所有权

- **主张 A**：术语把 `Diet Shift` 列为 `Fish Condition` 参数。出处：`docs/terminology.md` §5.2。
- **主张 B**：Groundbait Candidate 把 Diet Shift 后置为慢变生态候选。出处：`candidate/proposal.md` §8.2、WD-14。
- **主张 C**：Proposal C 把它作为 `CurrentFoodValue` 的加项。出处：`docs/proposals/lure-response-proposal-c-current-review-entry-2026-10-27.md` 第 45 行。
- **冲突点**：Diet Shift 属于谁，和它影响 Food 还是 Flavor，是两个不同问题。本项只问所有权。
- **影响**：Fish Condition、Food Preference、Response。
- **暂定处理**：`CANDIDATE_BRANCH`。本目录把所有权放在 Fish Condition：Baseline Diet 是静态配置，Diet Shift 是动态偏移。
- **裁决方**：Owner。

### C-12a2｜保留或覆盖现有 Fish Condition 语义

- **前提**：仅当 C-12a1 选“所有权在 Fish Condition”时成立。
- **主张 A**：保留现有语义：Diet Shift 是 Fish Condition 的动态偏移。
- **主张 B**：覆盖现有语义，需要 Owner 明确。
- **冲突点**：保留还是覆盖，是独立于所有权位置的第二个决定。
- **影响**：Fish Condition、下游消费者、迁移。
- **暂定处理**：`CANDIDATE_BRANCH`。当前保留现有语义。
- **裁决方**：Owner。

### C-12a3｜不设所有权时旧语义如何处置

- **前提**：仅当 C-12a1 选“明确不设所有权，不建模”时成立。
- **主张 A**：保留为描述性候选，不落 Schema。
- **主张 B**：废弃并迁移，需要迁移方案。
- **冲突点**：不设所有权不等于自动删除现有语义；需要明确旧引用如何处置。
- **影响**：Fish Condition、旧文档引用、迁移。
- **暂定处理**：`KEEP_OPEN`。当前倾向保留为描述性候选。
- **裁决方**：Owner。

### C-12b｜Diet Shift 消费语义

- **前提**：仅当 C-12a1 选“所有权在 Fish Condition”，且 C-12a2 选“保留”或“覆盖”时成立。
- **主张 A**：Diet Shift 修改 Food Preference。
- **主张 B**：Diet Shift 修改 Flavor Preference。
- **主张 C**：两者都改，但必须分别有因果依据。
- **冲突点**：当前没有证据说明 Diet Shift 应该只改 Food、只改 Flavor，还是两者都改。
- **影响**：Food、Flavor、Response。
- **暂定处理**：`KEEP_OPEN`。暂不决定；若选 C，两条路径必须分别保留 provenance。
- **裁决方**：Owner。

### C-13a｜Wariness 与 Avoidance 是否不同语义

- **主张 A**：`Wariness` 是随过程累积的 Fish Condition 状态。出处：`docs/terminology.md` §5.2。
- **主张 B**：`Avoidance` 是稀疏配置的 Cue 排斥。出处：`candidate/proposal.md` §5.4、WD-07。
- **冲突点**：两者都可能压低响应，容易重复扣分；但“是否不同语义”和“Avoidance 用什么表示”是两个问题。
- **选项说明**：“只保留 Avoidance”是删除或废弃 Wariness 的决定，需要迁移方案，不是纯粹的语义区分选项。
- **影响**：Response、Flavor、Feeding Event。
- **暂定处理**：`CANDIDATE_BRANCH`。本目录要求两者各自保留来源和 trace，不合并成一个“负分”。
- **裁决方**：Owner / Response Current。

### C-13b｜Avoidance 的表示形式

- **前提**：仅当 C-13a 选“不同语义”时成立。
- **主张 A**：静态稀疏 Profile。
- **主张 B**：Context-sensitive relation。
- **冲突点**：当前 Working Decision 只收敛了“排斥 ≠ 不喜欢”和“稀疏配置”，没有收敛它必须是静态关系。
- **影响**：Flavor、Response、Authoring。
- **暂定处理**：`KEEP_OPEN`。不把“静态”当成已确认前提。
- **裁决方**：Owner / Response Current。

### C-14｜Feeding Readiness 是否为正式状态

- **主张 A**：Groundbait Candidate 多处使用 `Feeding Readiness`。出处：`decisions/working-decisions.md` 的 WD-14、`candidate/proposal.md` §8.1。
- **主张 B**：术语表只定义 `Activity`、`Feeding Motivation`、`Diet Shift`、`Wariness`。出处：`docs/terminology.md` §5.2。
- **冲突点**：`Feeding Readiness` 可能是派生复合量，也可能被悄悄当成第五个状态。
- **影响**：Fish Condition、Response。
- **暂定处理**：`KEEP_OPEN`。未裁定前，不作为独立状态落 Schema，只作为描述性说法。
- **裁决方**：Owner。

## 3. 裁决顺序建议

分三轮，与 `owner-decision-brief.md` §7 保持一致。

**第一轮：模型形状**

C-01、C-02、C-03a、C-03b。

**第二轮：接入现有 FCF**

C-04a、C-04b、C-05a、C-05b、C-06a、C-06b、C-06c、C-08、C-09。

**第三轮：首版边界与暂缓项**

C-07a1、C-07a2、C-07b、C-10、C-11b、C-12a1、C-12a2、C-12a3、C-12b、C-13a、C-13b、C-14。

## 4. 不冒充裁决

本页只登记冲突，不替 Owner 做产品决定。任何标为 `CANDIDATE_BRANCH` 的处理都只是本目录的工作选择；`KEEP_OPEN` 的项在任何下游文档中都不得被写成已确认规则。
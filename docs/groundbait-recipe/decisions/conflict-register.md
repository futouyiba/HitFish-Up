# 台钓中鱼机制｜冲突与未决项登记

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页登记跨文档、跨候选栈的语义冲突和未决项。它不裁决 Owner 权限内的问题，只记录出处、双方主张、影响和暂定处理。

## 1. 使用方式

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
- **冲突点**：Flavor 候选的核心量没有已准入的 Current 载体。
- **影响**：Flavor、Chemical Cue Field、小药、发现与选择。
- **暂定处理**：`KEEP_OPEN`。在 Owner 准入前，Flavor 只保留“化学类型 + 稀疏关系”的降级候选，连续强度标为未准入。
- **裁决方**：Owner。

### C-03｜Feeding Event 与 Feeding Decision

- **主张 A**：Groundbait Candidate 使用事件概率分解：`encounter → feasible action set → selection → success → ingestion`。出处：`candidate/feeding-event.md`。
- **主张 B**：Proposal C 使用决策裕量：`DecisionMargin = CurrentFoodValue + StateTriggerValue - ClosingCost - PredictionCost - RiskCost - WillingnessThreshold`，再投影为 `C(Margin)`。出处：`docs/proposals/lure-response-proposal-c-current-review-entry-2026-10-27.md` 第 30–36 行、第 272 行。
- **冲突点**：两套都在解释“鱼吃不吃”，但一个是事件概率，一个是决策裕量；没有映射，也没有声明谁覆盖谁。
- **影响**：Feeding Event、Response 输入、Groundbait 与拟饵机制的共用语义。
- **暂定处理**：`KEEP_OPEN`。本目录以事件分解为主候选；Proposal C 的决策裕量保留为并行候选，不混用变量名。
- **裁决方**：Owner / Response Current。

### C-04｜有效摄食机会的落点

- **主张 A**：Groundbait Candidate 输出 `Effective Ingestion Opportunity`，但明确它不等于 `Adaptation Coefficient`。出处：`candidate/object-model.md` §3、`candidate/response-stage-mapping.md` §2。
- **主张 B**：现有术语只定义 `SpatialDistributionWeight × AdaptationCoeff → 下游候选权重`，没有“有效摄食机会”槽位。出处：`docs/terminology.md` §5.2。
- **冲突点**：`Effective Ingestion Opportunity` 是 Response Condition、Response Component、独立因子，还是只供某个既有计算消费，尚未确定；它如何与 AdaptationCoeff 组合也未定。
- **影响**：Response 接入、圆桌权重构建、Groundbait 候选闭环。
- **暂定处理**：`KEEP_OPEN`。候选文档只保留接口和单位说明，不定义组合公式。
- **裁决方**：Owner / Response Current。

### C-05｜Persistent Response Field 是增量还是覆盖层

- **主张 A**：术语把 `Persistent Response Field` 定义为“运行时对 DEF 的持续性增量影响层，不复制一份 DEF”。出处：`docs/terminology.md` §4。
- **主张 B**：Groundbait Candidate 明确不把窝料写回 DEF 或 `SpatialDistributionWeight`。出处：`candidate/response-stage-mapping.md` §6。
- **冲突点**：“增量”可能被实现成直接修改 DEF，导致持续效果和即时效果重复消费。
- **影响**：持久响应、姿态响应、窝料、响动。
- **暂定处理**：`CANDIDATE_BRANCH`。本目录把持久字段理解为 DEF 之外的运行时叠加层：DEF 只读，持久字段记录来源、范围、强度、持续时间和衰减，Response 只读一次。
- **裁决方**：Owner / Response Current。

### C-06｜环境食物浓度与窝料对象状态

- **主张 A**：术语把“食物浓度”列为环境因子示例。出处：`docs/terminology.md` §3.1。
- **主张 B**：Groundbait 产生独立的 `Feeding Place State` 与对象集合。出处：`candidate/object-model.md` §2.4。
- **冲突点**：如果环境侧已经表达食物浓度，窝料对象状态再把同一事实作为正向响应，就是重复计权。
- **影响**：环境烘焙、Response、Groundbait 全栈。
- **暂定处理**：`KEEP_OPEN`。只保留两种解释：环境侧是背景事实、窝料是玩家增量；或二者是同一事实，需要在消费端合并。
- **裁决方**：Owner / 环境与响应 Current。

### C-07｜Overfeeding 与补窝历史

- **主张 A**：外部研究记录 RF4 存在 overfeeding：population 下降、咬口频率降低、需要休息和补窝。出处：`programaticHitFish/docs/research/2026-10-21-rf4-bait-groundbait-mechanism-deep-research.md` 第 22–23、186–189、243–249、636、641 行。这只是外部研究，不是本仓 Current。
- **主张 B**：Groundbait Candidate 只有 `persistence / turnover`，没有 overfeed、历史累积、补窝频率和跨 session 语义。出处：`candidate/physical-release.md` §2、§6。
- **冲突点**：如果只做“越多越好”的释放，会丢失 overfeed 这个非单调策略轴；如果直接并入，又没有仓内证据和位置。
- **影响**：Physical Release、Feeding Place State、Fish Condition、补窝玩法。
- **暂定处理**：`KEEP_OPEN`。外部研究只作证据线索；是否首版纳入、放在 Feeding Place 还是 Fish Condition，待 Owner 决定。
- **裁决方**：Owner。

### C-08｜发现与趋近的阶段划分

- **主张 A**：Groundbait Candidate 把发现和趋近合并在 `Encounter` 里。出处：`candidate/feeding-event.md` §2.1。
- **主张 B**：Proposal C 区分 `ClosingCost`、`PredictionCost` 和 `RiskCost`，把接近与风险分开；外部研究也建议把“进入范围、试探、攻击、吞饵”拆成多阶段。出处：`docs/proposals/lure-response-proposal-c-current-review-entry-2026-10-27.md` 第 162、227、242、251 行；外部研究 `programaticHitFish/docs/rf4_fishing_planet_bite_mechanism_research_report.md`。
- **冲突点**：`Encounter` 同时承担感知、接近和时间窗口，难以区分“没看见”“不想靠近”“没时间”。
- **影响**：Feeding Event、Cue、Fish Condition、刺鱼接口。
- **暂定处理**：`KEEP_OPEN`。本目录保留 `Encounter` 作为合并候选，但在对象模型里记录它可能拆成 Detection / Approach / Temporal Opportunity。
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
- **暂定处理**：`KEEP_OPEN`。本目录只在动作路径层使用受限聚合，不把 `max` 推广到其它层。
- **裁决方**：Owner。

### C-11｜Food Target 与多 Target 聚合

- **主张 A**：Groundbait Candidate 使用“同 Target 合并后边际递减”。出处：`candidate/proposal.md` §4、WD-04。
- **主张 B**：PC 基线明确 multi-target hypothesis aggregation 为本轮不冻结项，并禁止 Coding Agent 自行引入 `sum / weighted average / max / Noisy-OR`。出处：`docs/baselines/FCF-PC-BASELINE-R0-20260915.md` §4、§13。
- **冲突点**：候选算法尚未获准成为正式聚合。
- **影响**：Food、Response、圆桌。
- **暂定处理**：`ACTIVE CANDIDATE`。只在本目录作为工作候选，不写成 Current。
- **裁决方**：Owner。

### C-12｜Diet Shift 的所有权

- **主张 A**：术语把 `Diet Shift` 列为 `Fish Condition` 参数。出处：`docs/terminology.md` §5.2。
- **主张 B**：Groundbait Candidate 把 Diet Shift 后置为慢变生态候选。出处：`candidate/proposal.md` §8.2、WD-14。
- **主张 C**：Proposal C 把它作为 `CurrentFoodValue` 的加项。出处：`docs/proposals/lure-response-proposal-c-current-review-entry-2026-10-27.md` 第 45 行。
- **冲突点**：三处都在改“鱼想吃什么”，更新时间尺度和消费者不同。
- **影响**：Fish Condition、Food Preference、Response。
- **暂定处理**：`KEEP_OPEN`。本目录规定：Baseline Diet 是静态配置，Diet Shift 是 Fish Condition 的动态偏移，Food/Flavor Exposure 不直接写 Diet Shift。
- **裁决方**：Owner。

### C-13｜Wariness 与 Avoidance 的边界

- **主张 A**：`Wariness` 是随过程累积的 Fish Condition 状态。出处：`docs/terminology.md` §5.2。
- **主张 B**：`Avoidance` 是稀疏配置的 Cue 排斥。出处：`candidate/proposal.md` §5.4、WD-07。
- **冲突点**：两者都可能压低响应，容易重复扣分。
- **影响**：Response、Flavor、Feeding Event。
- **暂定处理**：`CANDIDATE_BRANCH`。本目录要求两者各自保留来源和 trace，不合并成一个“负分”。
- **裁决方**：Owner / Response Current。

### C-14｜Feeding Readiness 是否为正式状态

- **主张 A**：Groundbait Candidate 多处使用 `Feeding Readiness`。出处：`decisions/working-decisions.md` 的 WD-14、`candidate/proposal.md` §8.1。
- **主张 B**：术语表只定义 `Activity`、`Feeding Motivation`、`Diet Shift`、`Wariness`。出处：`docs/terminology.md` §5.2。
- **冲突点**：`Feeding Readiness` 可能是派生复合量，也可能被悄悄当成第五个状态。
- **影响**：Fish Condition、Response。
- **暂定处理**：`KEEP_OPEN`。未裁定前，不作为独立状态落 Schema，只作为描述性说法。
- **裁决方**：Owner。

## 3. 裁决顺序建议

1. C-01、C-02、C-03 先决，它们决定 Groundbait 候选能否继续使用现有量。
2. C-04、C-05 决定 Response 接入和持久字段语义。
3. C-06、C-07、C-08、C-12、C-13、C-14 决定空间、时间与鱼况边界。
4. C-09、C-10、C-11 决定抽鱼、刺鱼和多目标聚合。

## 4. 不冒充裁决

本页只登记冲突，不替 Owner 做产品决定。任何标为 `CANDIDATE_BRANCH` 的处理都只是本目录的工作选择；`KEEP_OPEN` 的项在任何下游文档中都不得被写成已确认规则。
# EXP-PROTOCOL-FCF-PC-R0 — Authorability / Vocabulary Generalization 实验协议

- 状态:**ACTIVE(PROPOSAL 部分更新至 R1)**
- 执行对象:契约链 R0 → [R1 Addendum](../baselines/FCF-PC-BASELINE-R1-ADDENDUM-2026-09-16.md)(A1–A4/B1–B2)→ [R2](../baselines/FCF-PC-BASELINE-R2-20260916.md)(D1–D6,冻结)→ [R3 Candidate](../baselines/FCF-PC-BASELINE-R3-CANDIDATE-2026-09-16.md)(窄 Delta 1–3,NOT YET FROZEN);Round 1 盲测证据见 [归档报告](../holdout/FCF-PC-R2_BLIND_HOLDOUT_R1_20260916.md)
- 配套自审:[FCF-PC-BASELINE-R0-SELFREVIEW-2026-09-15](../reviews/FCF-PC-BASELINE-R0-SELFREVIEW-2026-09-15.md)
- 标注 **[PROPOSAL-R0]** 的条目中,对应 A/B 裁决的部分已按 R1 Addendum 更新并标注 **[R1-ADJUDICATED]**;其余仍未得到 Design Owner 裁决的 proposal 保持 proposal 状态,不自行 promotion。

## 1. 实验主张(引自 §1)

攻击以下主张:新 Item / Presentation / strategy story 进入系统时,大部分内容应能复用有限的 canonical facts、derived descriptors 与 relation resolvers,而不是线性制造新的 semantic token、Fish × Descriptor rule 或 item-specific exception。

Kill signals(§9):new Item count ↑ ≈ semantic token count 线性 ↑;或一个新 descriptor → 大量 Species 需新增专门 Response rule。出现即为 factorization degeneration。

## 2. 角色与权限矩阵

| 角色 | 职责 | 禁止 |
|---|---|---|
| Coding Agent | 冻结词汇内实现、case 分类初判、度量产出、ledger 维护 | 改冻结词汇;引入 §4 禁止的聚合算子(sum/weighted average/max/Noisy-OR);挑选或探知 holdout 身份;把失败 case 就地转基线修订 |
| Independent Reviewer(`gpt-5.6-sol`,中等推理;结构级事项高推理——按 AGENTS.md「独立审核」) | 分类抽查、conflict 报告复核、holdout 采样监督 | 代替实现 |
| Sample Agent | 冻结后从抽样框独立选取 blind holdout 并封存(见 [HOLDOUT-HANDOFF-R0](HOLDOUT-HANDOFF-R0.md)) | 与 Coding Agent 讨论候选 |
| Owner(用户) | 晋升/修订(R1)/open 项闭合/抽样框提供 | — |

## 3. 资产位置

- 本仓 `docs/experiments/`:协议、注册表、交接契约、run 记录。
- Harness 实现:`futouyiba/programaticHitFish`(本地 `/Volumes/Mac DS - Data/SharedProjects/programaticHitFish`;**2026-09-16 Design Owner 裁决修正**——原协议误写 `fishingGameTuningShowcase`)。在既有 authoring compiler / deterministic pre-generation harness / fixture-test infra 上增加 Presentation/Cue Contract Validation Lane,不平行建立第二套 execution framework。
- 语义对照与期望值来源:中鱼库(Notion `中鱼升级`)、推导表(飞书);Notion「Simplified V0 Working Main」与「Response Language Contract Delta R0」为 Engagement Mode / ResponseBand / SET-CAP 语义出处。

## 4. Run 生命周期

前置检查(全部满足才可开 run):

- [ ] freeze 文档存在,其内容 hash 记录进 run 记录
- [ ] cue/presentation schema 版本号已定义并记录 **[PROPOSAL-R0]**(补 P3-13;首轮可为 `schema-v0`)
- [ ] [DEVSET-REGISTRY-R0](DEVSET-REGISTRY-R0.md) 期望值已从中鱼库/推导表回填并标注来源
- [ ] holdout 抽样框已由 Owner 钉住、Sample Agent 已交付封存清单(补 P2-8)

步骤:

1. **Intake**:Development Set 先行;holdout 身份在实现冻结后揭示 **[PROPOSAL-R0]**——run 1 实现期间 Coding Agent 只可见 count/strata 汇总。
2. **Classification**:按 §10 + 本协议 §5 判定树,先分类后实现。
3. **实现**:仅 COVERED / ANNOTATION_ONLY / DERIVED_DESCRIPTOR_ONLY 在冻结词汇内实现;UNRESOLVED 不实现任何绕过方案。
4. **度量**:按本协议 §6 规范产出。
5. **Ledger 更新**:unresolved / semantic delta requests / conflicts。
6. **独立抽查**:Reviewer 复核分类,抽样量 ≥20% 且 ≥10 个 case(取大)**[PROPOSAL-R0]**。
7. **Run 报告**:§11 全量指标 + 分组 + kill-signal 布尔判定及证据。

## 5. 分类判定程序 **[R1-ADJUDICATED]**(Design Owner 裁决,见 R1 Addendum §A4;替代本节原 [PROPOSAL-R0] 判定树)

每个 Case 必须有:

```text
primary_classification: exactly one
requested_deltas: zero or more
flags: zero or more
```

Primary 判定程序(顺序固定):

```text
CAUSE_OWNERSHIP_CONFLICT
→ 若当前表达首先违反 owner / double-count

UNRESOLVED
→ 若必须先做尚未冻结的 semantic decision

否则寻找「使 Case 可合法表达的最小充分改动」：
COVERED
ANNOTATION_ONLY
DERIVED_DESCRIPTOR_ONLY
NEW_GENERIC_RULE_REQUIRED
NEW_PRIMITIVE_REQUIRED
NEW_RELATION_REQUIRED
ITEM_SPECIFIC_EXCEPTION
```

若 Case 同时需要多种 Delta:primary = 最先不可缺少的最小充分 semantic change;其它需求进入 `requested_deltas[]`;aggregate metrics 分别计数,不丢失多 Delta 信息。

`DERIVED_DESCRIPTOR_ONLY` 的「确定性派生」要求(A4 原文):只读取当前已 admitted fish-independent facts,并且相同输入必须唯一地产生相同 descriptor;不得读取 Species / Mode / response / hidden SKU identity。

补充执行规则:

- 「最小充分改动」的搜索顺序即 A4 列出的七档;UNRESOLVED 命中 §13/§4 显式 open 机制(如 multi-target aggregation、SET/CAP 终局)时,该 case 不实现绕过方案,记录 semantic delta request。
- `cue.displacement` 依赖(A2):fixture 无明确 semantic definition 时,不得据此判 `COVERED`,应标 `UNRESOLVED` 或避开该字段。
- 每条分类记录判定路径与证据(用到的字段、规则草稿)。
- 分类由 Coding Agent 初判,Reviewer 抽查(抽样量 ≥20% 且 ≥10 个,取大——**此项仍为 [PROPOSAL-R0]**,裁决未覆盖);分歧 case 双记并标注,以 Reviewer 结论归档。

## 6. 度量规范 **[PROPOSAL-R0]**(补自审 P2-6)

总口径:(i) dev / holdout 分组分别报告;(ii) run 1 报绝对值,之后 run 报 Δ;(iii) 不设综合分(§11)。

| 指标 | 操作化定义 |
|---|---|
| case count by classification | 主标签计数与两个 flag 的计数分开列 |
| Δ primitive / descriptor / relation / rule requests | 本 run 新增 admission 请求数,分 admitted / rejected 两列 |
| Δ manual annotation | 新增 sparse annotation 条目数 |
| Δ item-specific exception | 新增 item 例外规则数 |
| Δ unresolved / Δ conflict | 新增 flag case 数 |
| descriptor token count | 当前生效 `presentation.*` / `cue.*` token 总数,批准与 candidate 分列 |
| single-use descriptor count | 仅被 1 个 item 的任何事实引用的 descriptor 数 |
| Fish × Descriptor direct-touch | Response 规则中同时绑定具体 Species 与具体 descriptor 的规则数(依 A3:Static Affinity 无 Mode 轴;Mode 绑定按 ResponseProfile 维度单独统计) |
| per-descriptor Species/Mode fan-out | 每 descriptor 被引用的 Species(×Mode)数分布 |
| generic rule fan-out | 每条通用规则实际覆盖的 item×presentation 数分布 |
| descriptor→target 非恒等映射率(WATCH-15) | Target Interpretation 输出与输入 descriptor 一一对应的假设占比;持续≈100% 则两层 vocabulary 有一层冗余 |

## 7. Ledger 模板

- **ClassificationRecord**:`case_id, run_id, primary_label, flags[], ladder_step, evidence(引用字段/规则草稿), reviewer_verdict(抽查后填)`
- **UnresolvedRecord**:`case_id, open_item(引用 §13/§4 具体条目), requested_decision`
- **ConflictRecord**:`rule_id, derived_cue, co_consumed_primitive, provenance_ref, justified(BOOL + 理由文本)`
- **SemanticDeltaRequest**:`case_id, proposal_type(primitive/descriptor/relation/rule), rationale(逐项回答 §9 六问)`

## 8. 基线修订纪律(执行 §10 / §12)

任何因 case 而起的基线调整:该 case 即刻移入 Development Set;修订形成 R1 候选文档(新 freeze ID);R0 不回写;R0→R1 diff 附于修订说明。冻结文本不得因单个失败 case 被就地修改后把该 case 重记 PASS。

## 9. 单 run 验收标准

- §11 全量指标按 §6 口径产出(dev/holdout 分组)。
- 对 §9 两个 kill signal 分别输出布尔判定 + 支撑数据。
- Reviewer 抽查记录在案(抽查量、分歧数、结论)。
- holdout 评估在实现冻结后执行,过程可回放(评估脚本 + 数据入库时以 holdout 序号脱敏引用 item 身份,直至 run 报告发布)。

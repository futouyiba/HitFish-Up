# OPEN-ITEMS — 审之前先读这个

> **Historical V0.2 — 非 Current Authority。** 本文件正文冻结为 R2 / V0.2 当时的设计、Review 或 evidence 状态；下文出现的“现行 / Current”只表示 **V0.2 当时**。Fish Habit Editor 当前产品与公共语义以 [`docs/fish-habit-editor-v1/`](../../fish-habit-editor-v1/README.md) 为准。不得用本历史包覆盖 V1 Current。

**用途**：本审阅包唯一的可变问题台账：记录处置、剩余工作与关闭依据。README／开发 brief 只导航；[图像登记](figma-current.md#image-evidence)负责画面事实、版本与指纹。**七页编辑器规范的收口文本来自 Git Markdown；Notion Current 是面向人和对话式阅读的发布投影；Owner 裁定决定产品语义。** 图像只能证明所拍状态；审查关闭必须引用对应 exact head 的独立 REVIEW。本台账不新增产品权威，也不以“已裁／已投影”替代复审结论。

<a id="active-review-items"></a>
## 1. 当前审查项与证据

本节是问题处置与证据台账，不是产品 Contract。A2 的 Current 读取结果是本次核对的历史来源快照；其页面版本与 Notion 载体只说明取证时点，不改变 Git 规范源或当前 Owner。

<a id="species-role-ui"></a>
### Species Role UI：操作入口与记录态分别验收

| 项 | 处置及可核证据 | 剩余工作／关闭依据 |
|---|---|---|
| `CXR-ROLE-UI-01` 操作入口 | 作者的 `[04]` 记录描述物种侧两枚独立操作 chip；随包整帧也能看到。它回答“能否选择 operation”，不单独证明记录态。 | [#7 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/7#issuecomment-5757267260) @ `7438477536aa695955b966de1040b11aa8a11ab1` 已确认 `[04]` 解决操作入口问题；保留该确认，不重开入口修复，也不能借它关闭下一行的记录态问题。 |
| **`ADJ-03`：CLOSED（设计形态／语义映射／随包证据）** | SET 与 INHERIT 局部图水温 Role 同为 CORE，但前者有“Role 已钉住”、后者无；新版 SET 局部与整帧一致。版本／指纹见[图像登记](figma-current.md#image-evidence)。 | 关闭依据：[#7 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/7#issuecomment-5758470596) @ `ca17a2306b3c567e6fe7bc2eedcc6ed43ed3a2e5`。物种层持久化读写往返仍未实测，属实现侧验证，不作为重新挂开设计包的额外门禁。 |

**ADJ-03 的依据与射程**：

- **产品裁定与证明范围**：完整记录态／显示规则见[汇编 §9](component-contract-consolidated.md#role-record-intent)，交互与验收见[RoleControl](contract-cards.md#role-control)。来源仍沿 §2 ADJ-03 的裁定记录与固定历史；卡片是执行投影，不把裁定原句冒称卡2 的逐字引文，也不把下面的图片证据当 durable 往返结果。
- **实现证据边界**：前轮[独立 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/7#issuecomment-5757933398)亲读实现仓 `84e2221`，记录物种 `policyRecipe` 与行级 `rules` 分属两条 lane、`isRoleExpressed` 检查物种角色键存在性，clear／absent 同值测试针对行级 patch。另据 **CC 经 Owner 转达的实测勘误**，`durableRolesOf` 只读顶层 `rules`（`AffinityRolePatch`，键 `(row_key, component)`），物种 Role 落 `species[].policyRecipe`（CC 引 `stateSchema.ts:44`；该转述未另登记实现 head）。因此 `durableRolesOf`／`applyDurableRoles` 的行级路径不能证明物种层 `INHERIT` 与同原值 `SET` 的记录态。`species[].policyRecipe.roles` 读写往返尚未实测；本批没有重跑实现或扩大上述旁证，设计关闭不等于实现通过。
- **图片与审核**：#7 的两态设计证据关闭见上表；INHERIT 1×替换由 [#17 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/17#issuecomment-5758641670) @ `8d4523c0372c12cbf1aad14ec652159c2782e5ad` 批准。后续 #16 兼容提交先按用户授权免复审合并，再获[合并后独立补审](https://github.com/futouyiba/HitFish-Up/pull/16#issuecomment-5758896391) @ `fdb203c461bfe4ff2410a5244042d762d7adba32`；不能倒写成合并前已审。资产版本与证明范围只在[图像登记](figma-current.md#image-evidence)维护，本批未重读 live Figma。

<a id="source-sync"></a>
### `CXR7-SOURCE-SYNC-01`：CLOSED（来源状态投影）

**关闭依据**：[#7 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/7#issuecomment-5758470596) @ `ca17a2306b3c567e6fe7bc2eedcc6ed43ed3a2e5` 已确认来源状态投影关闭。实际整帧版本／来源显示见[图像登记](figma-current.md#image-evidence)，产品规则见[汇编 §7](component-contract-consolidated.md#7-组件卡--焦点编辑栏)，annotation证据见[画布摘要](figma-current.md#source-entry-evidence)。旧图问题与重导经过由 Git 保留；本批未重测实时交互。

<a id="packet-consistency"></a>
### 包内自洽／物证卫生

状态去重与图片兼容的完成依据为 [#16 合并后 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/16#issuecomment-5758896391) @ `fdb203c461bfe4ff2410a5244042d762d7adba32`；其先免审合并、后补审的顺序见上节。README旧重复状态不再作为待办。

[PR #14 的 APPROVE](https://github.com/futouyiba/HitFish-Up/pull/14#issuecomment-5758212127) 仅适用 `842f13029b1adb03eab6cfe52f5cfda2b8250702` 的 CLEAR 引用净改动，不关闭 #7 全包或 #10 原 head 的 findings。#9／#11及#10的其它既有问题不因文档收敛清零。

本台账不维护修订过程、旧问题簇总览或重复数量统计；理解规则必需的短理由随对应仓内投影保留。

## 2. Owner 裁决索引（产品依据，不代表审查关闭）

ADJ-01…13 的关闭裁定、原出处与投影定位见[固定裁决索引](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#2-owner-裁决索引产品依据不代表审查关闭)；不在日常台账重复维护已关闭的规则清单。“已裁／已投影”不证明实现、图片或本轮审核通过；本批未重读实时 Owner 记录。

- **ADJ-01 实现归属边界**：durable schema 由 TS 编辑器仓实现，另一侧原型不承担本契约；原出处为记录页 §374／§377，不代表已经实现。
- **ADJ-08 的迁移语境**：桶仍是数据迁移期的行单位表达；身份边界见[汇编 §16](component-contract-consolidated.md#identity-boundaries)，原页侧落点为 CT §1.1／§3.3、RS §11.1。
- **ADJ-03 设计关闭与实现取证**：[当前证据边界](#species-role-ui)分别登记；不因裁定已闭而关闭持久化验证。
- Temperature Concrete Import 缺值策略与目标物种护栏从[卡8](contract-cards.md#template-list)读取；其已裁依据见固定索引，不再维护“未冻结／三选一待裁”的旧问题。

<a id="role-profile-history"></a>
**Role／Profile／Setup 历史入口**：原裁定及撤回规则见[固定台账](https://github.com/futouyiba/HitFish-Up/blob/78fe441fb0b857f75bee097b87afa4a60e3dec04/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#role-profile-history)与其指向的旧 RoleControl；现行定义见[汇编 §11](component-contract-consolidated.md#profile-lifecycle)与[RoleControl](contract-cards.md#role-control)。旧关闭／读数不得扩大为保存重载通过。

<a id="remaining-evidence"></a>
## 3. 剩余取证项

本轮来源取证由 A2 [#45](https://github.com/futouyiba/HitFish-Up/issues/45) 于 **2026-09-22（Asia/Shanghai）**读取；本批依据其保存的 Current 正文与报告核对，不冒称再次实时 fetch。范围为《编辑器与 Resolve》v12（RS）、《编辑器界面》v20（UI）、《编辑器心智模型与 IA》v2（IA）、《Editor → Persistence 数据契约》v3（EP）、《编辑器持久层契约》v16（CT）、《编辑器条件开关》v7（SW）、《配置表与校验》v5（SC）、《中鱼因子聚合逻辑化-开发需求》v16（MR）的八份正文。下文代号均对应这些版本，日期相同。

“未检出”只指上述扫描范围，不等于全库没有依据。来源疑点、UI选择、实现取证分别处理；下列来源回读可消除指定疑点，本批审查关闭仍以对应 exact-head 独立 REVIEW 为准，不证明实时 Figma 或运行实现。

| 项 | 当前处理边界 | 下一步所需证据 |
|---|---|---|
| UI细则出处 | 本轮逐项来源与未检出范围见[下方](#ui-evidence)；已有冻结执行语义保留。 | 未确认的形态交独立设计任务 [#51](https://github.com/futouyiba/HitFish-Up/issues/51)，本批不采纳新 UI 约束。 |
| 影响面“三数／四项”跨页读数 | **来源疑点已消除**：RS §11.3、UI §1.1、IA §5、CT §3.10 本轮读数均为四项。完整仓内规则仍归[§14](component-contract-consolidated.md#template-reference-sets)。 | 只关闭所列页面的统计数量不同步疑点；实现与 Figma 同步须各自取证。 |
| CLEAR 的替代标签 | “已被本层替代”的显示场景仍归[卡2](contract-cards.md#operation-control)；能否另取“不再继承”只是旧比较的可翻转点，未新增命名裁定。 | 若重开命名，需 Current／Owner 依据，不能以整理改词。 |
| Species Policy Recipe 实现取证 | CT §3.6 本轮确认第五类 TemplateKind；仓内机制仍归[§9](component-contract-consolidated.md#policy-profile)。旧实现缺口未复核。 | 绑定新实现 head 取证；来源已核不证明当前实现已具备，也不重报旧“实现里不存在”。 |

<a id="brief-source-verification"></a>
**原 brief 的来源取证**：MR §3.3／§3.4 的 AggregationRole 与次要聚合规则已回读确认；SC 定义角色词表，但八页内未检出整数编码映射，不能补造编码值。`fail_env_coeff` 的设计值域、默认与 resolved 字段由 SC §3／§5、MR §4.4／§4.5.1 确认，仓内现行约束仍归[汇编 §9](component-contract-consolidated.md#policy-profile)。**GAP-013/014 的实现状态及“列＋264行值都就位”的生产数据实证仍未核**；前两 ID 未在八页正文检出，不代表实现任务已关闭。下一步需绑定实现 head 与实际数据版本检查；[原待核记录](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/implementation-brief-0.3.4.0-B.md#L119-L125)仅作历史来源，不作为今日验收读数。

<a id="ui-evidence"></a>
**UI细则：本轮来源核对与剩余工作（原汇编 §18.5）**。下表是问题处置，不另维护规则；未检出的精确形态不能自行升级为 Current 要求，也不据此删除已有冻结投影。原缺出处记录见[固定汇编 §18](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/component-contract-consolidated.md#18-未核--待裁)。

| 待核范围 | 本轮已核来源／关闭范围 | 未确认部分与下一步 |
|---|---|---|
| 本层操作数／诊断数／profile presence／source health | UI §1.1、§1.4 与 CT §6.5／§7.1 有摘要、继承/覆盖、可见诊断及派生量依据。 | 八页未检出四项必须并列或完整计数算法；CLEAR计数保留[卡2](contract-cards.md#operation-control)的冻结执行投影，不能标成上游已核。额外形态交 #51。 |
| Structure“全部／本层修改／问题”筛选 | UI §1.1 已核动态字段、Source顺序与两列焦点栏；现行入口[卡3](contract-cards.md#field-value-editor)。 | 三标签及必设筛选未检出；保留已有投影，不把固定字段数或新筛选要求加入本批。 |
| 卡片不做 mini heatmap／完整字段 provenance／操作历史时间线 | UI §1 与 IA §3 支持卡片摘要、焦点编辑职责；IA §3 明确焦点栏 History。 | 三条逐字负向未检出；不得据卡片范围禁掉焦点 History。需要新增负向约束时交 #51，职责仍按[§7](component-contract-consolidated.md#7-组件卡--焦点编辑栏)。 |
| TimePeriod Setup六步／预设preview四项形态 | UI §1.2、CT §3.3、SW §2 已核 Setup 可达；UI §1.1 已核预设覆盖条件。机制继续归[§11](component-contract-consolidated.md#profile-lifecycle)及[§15](component-contract-consolidated.md#timeperiod-batch-guard)。 | 六步固定序列、旧四项固定形态未检出；不据此重开机制裁定，也不删现行 Guard。具体承载交 #51。 |
| template candidate“N项待审查修改／撤销／审查修改” | CT §3.10 的候选/确认机制及 UI §9.1 的未durable丢弃范围已核；入口[§8](component-contract-consolidated.md#source-transaction)、[卡7](contract-cards.md#autosave-status)。 | 精确字串和三按钮形态未检出；本轮可逆文案／承载投影见[共享N2](contract-cards.md#rebase-impact-preview)，不是上游逐字串。 |
| Species“不弹Modal、只在行旁影响摘要” | CT §6.3／§3.10 可核普通编辑与 Source staged 的区别，传播分档仍归[§8](component-contract-consolidated.md#source-transaction)。 | 未检出绝对不弹 Modal；本轮候选承载见[共享N2](contract-cards.md#rebase-impact-preview)，未设全局Modal禁令，不以旧UI概括替代确认契约。 |
| 非CORE时temp_threshold显示／保存／不消费文案 | MR §3.2、SC §5／§6 已核 threshold消费/required范围；UI §1.1 有六参和同图展示，SW §2、CT §3.5／§3.10约束Role切换不隐式改数据。 | 本轮当前呈现、合法编辑可达及上下文用途说明见[卡3局部投影](contract-cards.md#temperature-threshold-ui)；不扩成永久跨界面限制，不把用途标签当免校验。 |
| same-source pin“当前值不变，但继承关系变化” | **机制来源疑点已消除**：CT §3.3／§3.10确认同值意图及预览边界；完整机制归[§8](component-contract-consolidated.md#source-transaction)。 | 精确中文串仍为可逆执行投影，由[卡1](contract-cards.md#source-selector)消费机制，不冒称 Current 逐字引文；实现/Figma另验。 |
| P0通道variants清单 | UI §0／§1.4及SC §5／§6已核主要界面与诊断/required类别；具体卡片验收不变。 | 八页未检出统一全局变体清单；所需视觉代表态交 #51，不凭缺图新增产品门禁。 |

<a id="ui-projection-decision"></a>
**#51 本轮UI选择与关闭边界**：[decision log](https://github.com/futouyiba/HitFish-Up/issues/51#issuecomment-5764424219)经独立反方收窄后，承接为[共享N2](contract-cards.md#rebase-impact-preview)与[卡3阈值局部投影](contract-cards.md#temperature-threshold-ui)，具体方案及回退见[Semantic提案](../../proposals/0.3.4.0-B-n2-ui-projection.md)。本条只登记该设计选择的承接，不替代最终exact-head DESIGN／REVIEW；Figma写入与验收仍待实时证据。其余UI取证仍按上表范围，已有摘要、筛选、Setup与卡片验收不变，本批不新增计数算法、固定向导或全局variants门槛。

## 4. 易误报项的阅读入口

此处只导航，不另存规则或几何事实：
- 容器高度、卡侧层级与SourceLabel恢复风险：[图像登记 §五](figma-current.md#五2026-09-21-节点与-annotation-回读记录)。
- Authoring Subject Navigation 的顶层可达性、单一 scroll owner、Fish disclosure 行为，以及 `中鱼习性模式 [兼容]`：看[汇编 §1](component-contract-consolidated.md#subject-navigation)与[差异清单 D0-D2 / D8](../0.3.4.0-B-ui-vs-figma-current-delta-backlog.md#左栏-drawer)。**图像登记 §五的 122px Policy 控制条高度不是 Rail 设计依据。**
- 物种／行级 CLEAR、操作概念名与行内显示：[汇编 §4](component-contract-consolidated.md#field-value-control)及[§10](component-contract-consolidated.md#policy-clear)。
- Role角标为何保留角色色：[图像登记 §八](figma-current.md#八原快照的卡上-role-角标--为什么它是三态下拉以及为什么它不做成白场)。
- 图上“示意／空态”及“未标不等于已实现”的取证边界：[图像登记 §三／四](figma-current.md#三2026-09-20-的历史回读)。“类型名（示意）”不声称真实对象存在。

## 5. 契约读数与能力裁定（沿用固定来源）

原契约读数／能力问题的关闭范围与出处见[固定能力表](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#5-契约读数与能力裁定沿用固定来源)。`CLOSED` 不代表实现、图证据或整个 Persistence 通过；现行形状与算法归汇编／执行卡，不在此保留第二张规则表。Species Role 的后续验证见[当前审查项](#species-role-ui)，第五类 TemplateKind 的旧缺口见[剩余取证](#remaining-evidence)。

<a id="other-material-items"></a>
## 6. 其它材料与实现取证边界

- **上游链接归属**：本轮 MR §3.0 → RS §11／EP，以及 RS §11.4 → CT 的现行链路已核；未见旧“作者分层链到副本”的问题，所核链路的来源疑点消除。不将此扩大为全库链接体检；其它旧副本路径未经逐一重建，不能推断全部已修。
- **卡10／卡11视觉投影**：CT §3.10、UI §1.1／§7 已核核心事务；八页未检出“等实现后才可设计”门禁。旧登记的等待顺序由本轮用户授权（[#43](https://github.com/futouyiba/HitFish-Up/issues/43)）更新为 **可开展标明 UNIMPL 的目标设计**，不要求先证明运行实现完成。本轮候选承载与局部形态的决策承接见[UI选择记录](#ui-projection-decision)，其余未确认项仍按来源范围处理。写入仍须实时 intake、写前快照、已审契约和独立 Figma 审核；本批无 live 读数，物证仍见[图像登记](figma-current.md#image-evidence)。
- **契约名／实现名映射**：`ProductionRowLedger` 对应实现名的旧定位、类型与行号见[固定取证](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#other-material-items)；只用于定位，不是新身份，原裁定不为外观一致改名。本批未重核实现，使用前须在目标实现 head 确认。

<a id="source-drift-implementation-evidence"></a>
### 静态来源漂移：历史观察与当前实现取证

- **历史证据**：[固定基线卡4](https://github.com/futouyiba/HitFish-Up/blob/042f3a9df2ee7521e8ef32d77b6d78407e10946c/docs/review/ui-component-contract-r2/contract-cards.md#L182)转录编辑器仓 `GAP-ED-26`，称当时耐久记录不带来源快照，不能检测来源漂移；原观察未登记被核实现 head。固定 SHA 只锚文档，不补造实现版本，也不判断今日缺口仍复现或已关闭。
- **现行展示边界**：按[卡4](contract-cards.md#effective-value-display)读取静态当前态与候选 before/after 的区别；卡2只是该显示规则的消费者。旧文“增加来源快照”仅为当时的候选方案，不是本轮指定的唯一实现路径或新的 durable schema 要求。
- **下一步**：若核验实现或提出来源变化显示能力，先绑定新的实现 head，分别取证当前记录态与跨时点/候选变化；若需改变展示契约或记录形状，另走设计提案。当前未重跑实现，不以本次状态迁移判通过。

<a id="template-import-implementation-evidence"></a>
### 卡8 Concrete Import：实现逐项对表

卡8两步导入语义、缺值推导和显式目标物种护栏仍归[卡8](contract-cards.md#template-list)。**实现线逐项对表仍待新实现 head 取证**；本次未验证导入或重导行为，不宣布与契约对齐。

原 Part3 的唯一挂项描述属于当时冻结批次的交付记录，范围见[固定收口提示](https://github.com/futouyiba/HitFish-Up/blob/042f3a9df2ee7521e8ef32d77b6d78407e10946c/docs/review/ui-component-contract-r2/contract-cards.md#L394)，不能作为今天全包的挂项数量。下一步按目标实现逐条检查卡8，再记录结果与验证范围；卡片正文不再维护动态任务状态。

需要核对先前原文时使用 Git 历史；它不取代现行规则与新的实证。

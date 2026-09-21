# OPEN-ITEMS — 审之前先读这个

**用途**：本审阅包唯一的可变问题台账：记录处置、剩余工作与关闭依据。README／开发 brief 只导航；[图像登记](figma-current.md#image-evidence)负责画面事实、版本与指纹。**产品真相来自 Notion Current／Owner 裁定；图像只能证明所拍状态；审查关闭必须引用对应 exact head 的独立 REVIEW。** 本台账不新增产品权威，也不以“已裁／已投影”替代复审结论。

<a id="active-review-items"></a>
## 1. 当前审查项与证据

本节分别登记设计／图证据关闭与实现未核；每条审核只适用于其 exact head。后续文档修改按[风险分级与审核收口](REVIEW-PROMPT.md#review-closure)验收，不沿用旧批准。产品规则只从所引汇编／执行卡读取。

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

本表只维护处置、出处和仓内规则入口；`PROJECTED IN` 是投影定位，不证明实现或图片通过。原裁决转录可在[固定基线 §2](https://github.com/futouyiba/HitFish-Up/blob/78fe441fb0b857f75bee097b87afa4a60e3dec04/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#2-owner-裁决索引产品依据不代表审查关闭)查阅；本批未重读实时 Owner 记录。

**Temperature Concrete Import 缺值策略：已裁。** 规则及目标物种护栏在[卡8](contract-cards.md#template-list)，不再挂“未冻结／三选一待裁”。选择该方案的理由随卡8；原过程由 Git 保留。

| ID | 处置与原出处 | PROJECTED IN |
|---|---|---|
| ADJ-01 | 已裁；记录页 §374／§377。实现仓归属读数，不是实现完成证明。 | 实现归属摘要：durable schema 由 TS 编辑器仓实现，另一侧原型不承担本契约；依据见固定基线 ADJ-01，不代表已实现。 |
| ADJ-02 | 已裁并投影；记录页 §374／§377。 | [统一缺席矩阵 §11](component-contract-consolidated.md#profile-lifecycle) |
| ADJ-03 | 已裁并投影；记录页 §374／§377。设计关闭／实现未核分别处理。 | [记录态 §9](component-contract-consolidated.md#role-record-intent)、[RoleControl](contract-cards.md#role-control)、[证据边界](#species-role-ui) |
| ADJ-04 | Component Recipes 形状已裁；记录页 §374／§377，持久层 §3.1。 | [RoleControl Durable mutation](contract-cards.md#role-control) |
| ADJ-05 | Source override 独立绑定已裁；记录页 §374／§377。 | [组件记录 §3](component-contract-consolidated.md#component-clear)、[Source Selector](contract-cards.md#source-selector) |
| ADJ-06 | Authoring 粒度已裁；记录页 §383。不得与 ADJ-08 的物理键混读。 | [Policy／粒度 §9](component-contract-consolidated.md#policy-profile)、[身份边界 §16](component-contract-consolidated.md#identity-boundaries) |
| ADJ-07 | raw Role 默认已裁；记录页 §383。 | [Role记录态 §9](component-contract-consolidated.md#role-record-intent) |
| ADJ-08 | C_SPLIT_REGISTERS 已裁并投影；记录页 §385。 | [身份边界 §16](component-contract-consolidated.md#identity-boundaries)，完整保留业务概念／物理键／Runtime边界；桶仍是数据迁移期的行单位表达；原页侧落点为 CT §1.1／§3.3、RS §11.1。 |
| ADJ-09 | C_NARROW 已裁并投影；记录页 §392。 | [Source事务 §8](component-contract-consolidated.md#source-transaction)、[事务分类 §15](component-contract-consolidated.md#transaction-model) |
| ADJ-10 | 作者词命名已裁；记录页 §393。原“页内相抵”定性不再使用。 | [卡7](contract-cards.md#autosave-status)已承接作者词与丢弃射程；不能再登记“本包不投影”。 |
| ADJ-11 | A_NARROW 已闭并投影；持久层 v16 §3.7。 | [空底板投影 §11](component-contract-consolidated.md#empty-profile-projection) |
| ADJ-12 | Setup能力已 CLOSED；原裁定转录在本包 RoleControl。 | [Setup §11](component-contract-consolidated.md#profile-lifecycle)、[RoleControl](contract-cards.md#role-control)；不替代UI形态／实现验证。 |
| ADJ-13 | target／同层atomic batch已裁；原转录在本包汇编 §12。 | [TimePeriod §12](component-contract-consolidated.md#component-specifics)、[覆盖确认 §15](component-contract-consolidated.md#timeperiod-batch-guard) |

“已裁”与“已有执行投影”分别核对；链接只证明存在入口，完整性仍须沿所引内容审核，不能以表格非空替代验收。

<a id="role-profile-history"></a>
**Role／Profile／Setup 历史入口**：原裁定及撤回规则见[固定台账](https://github.com/futouyiba/HitFish-Up/blob/78fe441fb0b857f75bee097b87afa4a60e3dec04/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#role-profile-history)与其指向的旧 RoleControl；现行定义从上表读取。旧关闭／读数不得扩大为保存重载通过。

## 3. 剩余取证项

| 项 | 当前处理边界 | 下一步所需证据 |
|---|---|---|
| UI细则出处 | 未在本批复核，不自动升级为Current要求；完整清单只在[汇编 §18.5](component-contract-consolidated.md#18-未核--待裁)维护。 | 逐项 Current／Owner 依据；不能以文字整理作通过。 |
| 影响面“三数／四项”跨页读数 | 旧记录指 Resolve §11.3 未同步，本批未重读该页；仓内规则按[§14](component-contract-consolidated.md#template-reference-sets)。 | 新鲜回读对应页面，才能判断今天仍冲突或已消失。 |
| Structure 固定字段数误读 | **已收口**；原“25 个 slot”的写法不能再作为当前冲突。 | 现行投影与原收口见[汇编 §18.8](component-contract-consolidated.md#18-未核--待裁)及[卡3](contract-cards.md#field-value-editor)。 |
| ADJ-11 展开分支缺口 | 已闭；不重复列为剩余规则缺口。 | 完整规则见上表；实现是否通过另验。 |

## 4. 易误报项的阅读入口

此处只导航，不另存规则或几何事实：
- 容器高度、卡侧层级与SourceLabel恢复风险：[图像登记 §五](figma-current.md#五2026-09-21-节点与-annotation-回读记录)。
- 物种／行级 CLEAR、操作概念名与行内显示：[汇编 §4](component-contract-consolidated.md#field-value-control)及[§10](component-contract-consolidated.md#policy-clear)。
- Role角标为何保留角色色：[图像登记 §八](figma-current.md#八原快照的卡上-role-角标--为什么它是三态下拉以及为什么它不做成白场)。
- 图上“示意／空态”及“未标不等于已实现”的取证边界：[图像登记 §三／四](figma-current.md#三2026-09-20-的历史回读)。“类型名（示意）”不声称真实对象存在。

## 5. 契约读数与能力裁定（沿用固定来源）

`CLOSED` 只表示原契约读数／能力问题已回答，不代表实现、图证据或整个Persistence通过。形状与算法只在所引文件维护；原完整读数见[固定基线 §5](https://github.com/futouyiba/HitFish-Up/blob/78fe441fb0b857f75bee097b87afa4a60e3dec04/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#5-契约读数与能力裁定沿用固定来源)。

| 子项 | 状态 | 规则入口／验证边界 |
|---|---|---|
| Component Recipe Shape | CLOSED（读数） | 持久层 §3.1；[RoleControl](contract-cards.md#role-control) |
| Affinity Role Patch | CLOSED（读数） | 持久层 §3.4；[RoleControl Durable mutation](contract-cards.md#role-control) |
| Affinity Fail Env Coeff Patch | CLOSED（读数） | 持久层 §3.4；[RoleControl Durable mutation](contract-cards.md#role-control) |
| Species Policy Recipe | CLOSED（读数） | 持久层 §3.1；旧实现取证曾报第五类TemplateKind缺口，**当前实现未复核**，不得将旧“实现里不存在”当新实测。 |
| Affinity Source Override | CLOSED（读数） | [组件记录 §3](component-contract-consolidated.md#component-clear)、[authoring／物理键分层 §16](component-contract-consolidated.md#identity-boundaries) |
| Profile Presence | CLOSED | [Profile生命周期 §11](component-contract-consolidated.md#profile-lifecycle) |
| Species Role UI | [当前审查项](#species-role-ui) | 操作入口、记录态和实现分别验收。 |
| Follow／Pin | CLOSED（语义） | [Source×Operation §3](component-contract-consolidated.md#component-clear)、[卡1](contract-cards.md#source-selector) |
| Source Transaction | CLOSED（能力） | [§8](component-contract-consolidated.md#source-transaction)、[§15](component-contract-consolidated.md#transaction-model) |
| TimePeriod Transaction | CLOSED（能力） | [target §12](component-contract-consolidated.md#component-specifics)、[Batch Overwrite Guard](component-contract-consolidated.md#timeperiod-batch-guard)；“预设”的不同指称仍须区分，不据术语清理重开已裁能力。 |

<a id="other-material-items"></a>
## 6. 其它材料与实现取证边界

- **上游链接归属**：旧记录指主开发需求 §3.0 将作者分层链到副本，而定义归持久层 §3.3；本批未重读这些页面，不以旧记录宣布当前链接仍错或已修。
- **卡10／卡11视觉投影**：旧登记为等实现后再投；本批未核实现或live Figma，实际物证仍从[图像登记](figma-current.md#image-evidence)取得，不因文档清理视为完成。
- **契约名／实现名映射**：旧取证将契约 `ProductionRowLedger`（持久层 §3.2／§3.4）对应为实现 `ProductionRows`／`ProductionRowRecord`（`src/data/derived.ts:36/51`），`refs: Partial<Record<ProfileField, number | string | null>>` 对应四组件键。该记录用于按名定位，不是新身份；原裁定不为外观一致改名。原读数见[固定取证](https://github.com/futouyiba/HitFish-Up/blob/78fe441fb0b857f75bee097b87afa4a60e3dec04/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#other-material-items)，**本批未重核实现，行号与类型是否仍相同需到实现仓确认**。

需要核对先前原文时使用 Git 历史；它不取代现行规则与新的实证。

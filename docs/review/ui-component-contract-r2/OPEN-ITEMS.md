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

ADJ-01…13 的关闭裁定、原出处与投影定位见[固定裁决索引](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#2-owner-裁决索引产品依据不代表审查关闭)；不在日常台账重复维护已关闭的规则清单。“已裁／已投影”不证明实现、图片或本轮审核通过；本批未重读实时 Owner 记录。

- **ADJ-01 实现归属边界**：durable schema 由 TS 编辑器仓实现，另一侧原型不承担本契约；原出处为记录页 §374／§377，不代表已经实现。
- **ADJ-08 的迁移语境**：桶仍是数据迁移期的行单位表达；身份边界见[汇编 §16](component-contract-consolidated.md#identity-boundaries)，原页侧落点为 CT §1.1／§3.3、RS §11.1。
- **ADJ-03 设计关闭与实现取证**：[当前证据边界](#species-role-ui)分别登记；不因裁定已闭而关闭持久化验证。
- Temperature Concrete Import 缺值策略与目标物种护栏从[卡8](contract-cards.md#template-list)读取；其已裁依据见固定索引，不再维护“未冻结／三选一待裁”的旧问题。

<a id="role-profile-history"></a>
**Role／Profile／Setup 历史入口**：原裁定及撤回规则见[固定台账](https://github.com/futouyiba/HitFish-Up/blob/78fe441fb0b857f75bee097b87afa4a60e3dec04/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#role-profile-history)与其指向的旧 RoleControl；现行定义见[汇编 §11](component-contract-consolidated.md#profile-lifecycle)与[RoleControl](contract-cards.md#role-control)。旧关闭／读数不得扩大为保存重载通过。

<a id="remaining-evidence"></a>
## 3. 剩余取证项

以下项目沿既有未核范围登记，不以本轮文字整理宣称新缺陷或已完成。

| 项 | 当前处理边界 | 下一步所需证据 |
|---|---|---|
| UI细则出处 | 完整待核清单见[下方](#ui-evidence)，不自动升级为 Current 要求。 | 逐项 Current／Owner 依据；不能以文字整理作通过。 |
| 影响面“三数／四项”跨页读数 | 旧记录指 Resolve §11.3 未同步，本批未重读该页；仓内规则按[§14](component-contract-consolidated.md#template-reference-sets)。 | 新鲜回读对应页面，才能判断今天仍冲突或已消失。 |
| CLEAR 的替代标签 | “已被本层替代”的显示场景仍归[卡2](contract-cards.md#operation-control)；能否另取“不再继承”只是旧比较的可翻转点，未新增命名裁定。 | 若重开命名，需 Current／Owner 依据，不能以整理改词。 |
| Species Policy Recipe 实现取证 | 契约读数已闭；旧取证曾报第五类 TemplateKind 缺口，当前实现未复核。 | 绑定新实现 head 取证，不能把旧“实现里不存在”当今日状态。 |

<a id="brief-source-verification"></a>
**原 brief 的来源取证**：AggregationRole 的现行数值／次要聚合规则，以及 fail_env_coeff 的 GAP-013/014 现状，仍需回 Current 复核。原稿“列＋值都就位／空列会判 264 行非法”只是[原待核记录](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/implementation-brief-0.3.4.0-B.md#L119-L125)，不得作为现行数值或验收判据。 本次仅迁移登记，未重读对应 Current 或重跑实现验证。

<a id="ui-evidence"></a>
**UI 细则完整待核清单（原汇编 §18.5）**：本层操作数／诊断数／profile presence／source health 四展示项；结构筛选“全部／本层修改／问题”；组件卡不做 mini heatmap／完整字段 provenance／操作历史时间线三条负向（不能把焦点栏的独立 History 一并禁掉）；TimePeriod Setup 六步的具体 UI 序列与旧预设 preview 四项形态；模板 candidate 的“N 项待审查修改／撤销／审查修改”形态；Species 编辑“不弹 Modal、只在行旁给影响摘要”的强度映射；非 CORE 时 `temp_threshold` 的显示／保存及“不消费”文案；same-source pin 的“当前值不变，但继承关系变化”文案；P0 通道 variants 清单。原逐项缺出处说明见[固定汇编 §18](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/component-contract-consolidated.md#18-未核--待裁)。Setup／Preset **机制**已分别在[汇编 §11](component-contract-consolidated.md#profile-lifecycle)／[汇编 §15](component-contract-consolidated.md#timeperiod-batch-guard)投影，本项不据旧 UI 取证重开机制裁定，也不把上述 UI 形态当成 Current 已核要求。

## 4. 易误报项的阅读入口

此处只导航，不另存规则或几何事实：
- 容器高度、卡侧层级与SourceLabel恢复风险：[图像登记 §五](figma-current.md#五2026-09-21-节点与-annotation-回读记录)。
- 物种／行级 CLEAR、操作概念名与行内显示：[汇编 §4](component-contract-consolidated.md#field-value-control)及[§10](component-contract-consolidated.md#policy-clear)。
- Role角标为何保留角色色：[图像登记 §八](figma-current.md#八原快照的卡上-role-角标--为什么它是三态下拉以及为什么它不做成白场)。
- 图上“示意／空态”及“未标不等于已实现”的取证边界：[图像登记 §三／四](figma-current.md#三2026-09-20-的历史回读)。“类型名（示意）”不声称真实对象存在。

## 5. 契约读数与能力裁定（沿用固定来源）

原契约读数／能力问题的关闭范围与出处见[固定能力表](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#5-契约读数与能力裁定沿用固定来源)。`CLOSED` 不代表实现、图证据或整个 Persistence 通过；现行形状与算法归汇编／执行卡，不在此保留第二张规则表。Species Role 的后续验证见[当前审查项](#species-role-ui)，第五类 TemplateKind 的旧缺口见[剩余取证](#remaining-evidence)。

<a id="other-material-items"></a>
## 6. 其它材料与实现取证边界

- **上游链接归属**：旧记录指主开发需求 §3.0 将作者分层链到副本，而定义归持久层 §3.3；本批未重读这些页面，不以旧记录宣布当前链接仍错或已修。
- **卡10／卡11视觉投影**：旧登记为等实现后再投；本批未核实现或live Figma，实际物证仍从[图像登记](figma-current.md#image-evidence)取得，不因文档清理视为完成。
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

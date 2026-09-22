# Issue #55｜既有投影最小同步与逐卡候选稿

**状态：只读 intake 与候选写稿，零 Figma 写入。** 依据：main 契约文件与当前目标文件的 Plugin API fresh read（对象 `Document`／`figma`／当前页 `Current｜0.3.4.0-B 编辑器假图（W4B B Current）`，`skipInvisibleInstanceChildren=false`，页面节点数2476）。本文件不读取 Notion、不把静态图升级为运行时证据；帧号＋层名定位，不公开节点 ID。

## 1. 逐卡需改／不需改清单

### Card 1｜A①-卡1 Source Selector

- **契约依据**：[卡1 Source Selector](../review/ui-component-contract-r2/contract-cards.md#source-selector)、[Source 事务](../review/ui-component-contract-r2/component-contract-consolidated.md#source-transaction)、[组件清除](../review/ui-component-contract-r2/component-contract-consolidated.md#component-clear)。
- **画布读数**：`proj_ss_1` 态1「正常跟随（缺省）」主体 `templateRow` 的 `sel_结构` 层为「类型名（示意） ▾」；`proj_ss_3` 态3「same-source pin」主体 `chipPin` 层为「已显式固定」；两帧 annotation 都说明静态图不证明提交/持久化。
- **判断：不需改（保留）**。当前态已覆盖同值显式 pin 与 Source/Role 意图区分的图面事实；N2 候选正文另在已落组，不把 Card1 重画成候选确认面板。

### Card 2｜A①-卡2 Operation Control

- **契约依据**：[Operation Control](../review/ui-component-contract-r2/contract-cards.md#operation-control)、[Operation 语义](../review/ui-component-contract-r2/component-contract-consolidated.md#source-operation-正交)。
- **画布读数**：`proj_oc_1`–`proj_oc_8` 的 `chip_follow`／`chip_add`／`chip_set`／`chip_clear` 层分别可读「仅使用来源」「调整为…」「设置为…」「仅使用当前来源」；`proj_oc_9` 态9的 annotation 仅说明层×字段类型选项集。
- **判断：不需改（保留）**。ADD／SET／CLEAR 的入口形态和否定边界已有覆盖；不为与新卡10/11视觉整齐而重做。

### Card 3｜A①-卡3 Field Value Editor

- **契约依据**：[Field Value Editor](../review/ui-component-contract-r2/contract-cards.md#field-value-editor)、[Temperature threshold UI](../review/ui-component-contract-r2/contract-cards.md#temperature-threshold-ui)、[Temperature behavior](../review/ui-component-contract-r2/component-contract-consolidated.md#temperature-behavior)、[Profile lifecycle](../review/ui-component-contract-r2/component-contract-consolidated.md#profile-lifecycle)。
- **画布读数**：`proj_fv_6` 态6「水温豁免（连续曲线）」层 `parameterEditEntry` 为「编辑六参数 ↗（10 Authoring · 水温）」；`effectiveRoleThresholdContext` 为「示例：物种 A / bucket A · Effective Role SECONDARY；阈值仅供 CORE 门控，当前不使用」；`thresholdValidationBoundary` 为「非 CORE 缺 threshold 不报 required；已有越界值仍报 ERROR，不清值、不补值」。
- **判断：不需改（保留）**。当前投影已经覆盖阈值用途、非CORE护栏、越界保留与六参数编辑入口；不把局部投影扩大为永久跨界面禁令。

### Card 4｜A①-卡4 Effective Value Display

- **契约依据**：[Effective Value Display](../review/ui-component-contract-r2/contract-cards.md#effective-value-display)。
- **画布读数**：`proj_ev_1`–`proj_ev_6`；`proj_ev_1`、`proj_ev_2`、`proj_ev_5` 主体有 `ro`「只读 · 派生」，`proj_ev_6` 有 `noEdit`「本栏无输入框 / 无档位 / 无“恢复为底板”」；annotation 已保留实现未重核边界。
- **判断：不需改（保留）**。只读派生值与无编辑入口已表达；不把卡4改造成卡10/卡11编辑载体。

### Card 5｜A①-卡5 Provenance Display

- **契约依据**：[Provenance Display](../review/ui-component-contract-r2/contract-cards.md#provenance-display)、[Template list](../review/ui-component-contract-r2/contract-cards.md#template-list)。
- **画布读数**：`proj_pv_1` 的 `note` 为「每段可展开到该项的 op 记录（含 tier）；本链＝『这个值为什么是这样』」；`proj_pv_2` 的 `unimpl` 为来源类别未在耐久层表达；`proj_pv_4` 的 `h1/h2` 明确「生态数据（前四项）」与「游戏参数」；`proj_pv_5` 的 `c1/c2/c3` 明确不进 Resolver／Runtime payload、不塞 production name、不作关联／复用判据。
- **判断：不需改（保留）**。现状已覆盖来源→操作→当前值、字段来源性质、以及 Runtime／命名／复用边界；`⚑UNIMPL`／`⚐UNVERIFIED` 仍保留，不用静态图宣称实现。

### Card 6｜A①-卡6 Validation·Diagnostic

- **契约依据**：[Validation／Diagnostic](../review/ui-component-contract-r2/contract-cards.md#validation-diagnostic)、[Validation autosave](../review/ui-component-contract-r2/component-contract-consolidated.md#validation-autosave)。
- **画布读数**：`proj_vd_3` `cnt`「1 警」＋`note`「不阻断保存」；`proj_vd_4` `cnt`「2 错」＋`note`「仍可保存 · Publish 阻断到修复」；`proj_vd_5` `statusA/statusB`「已保存 ·／有错误」与 `note` 定位首个 ERROR；`proj_vd_6` `ref` 层显示失效来源 owner/component/ref 与不 fallback。
- **判断：不需改（保留）**。保存状态、诊断与Publish阻断已分层表达；新增字段级定位/Setup运行态仍标记为未实现/未核，不从静态图补功能。

### Card 7｜A①-卡7 Autosave Status

- **契约依据**：[Autosave Status](../review/ui-component-contract-r2/contract-cards.md#autosave-status)、[Cross-layer guards](../review/ui-component-contract-r2/component-contract-consolidated.md#cross-layer-guards)。
- **画布读数**：`proj_as_4` `st`「保存失败」与 `rs`「I/O · 写盘失败」；`proj_as_5` `st`「保存失败」与 `rs`「revision 冲突 · 外部修改」；`proj_as_6` `st`「丢弃未保存的改动」；`proj_as_7` `st`「Publish」及显式／批量／独立摘要。`proj_as_6` annotation 只有记录页桥接，画面文本不重复实现规则。
- **判断：不需改（保留）**。现有画面覆盖保存失败、冲突、丢弃与Publish分工；本轮不以“其它卡要短形”为由改卡7。

### Card 8｜A②-卡8 Template Library List

- **契约依据**：[Template Library List](../review/ui-component-contract-r2/contract-cards.md#template-list)、[Template reference sets](../review/ui-component-contract-r2/component-contract-consolidated.md#template-reference-sets)。
- **画布读数**：`proj_tl_1`–`proj_tl_4`；`proj_tl_1` `hdr` 为「模板清单 · 平铺（不分组 / 不折族）」；`proj_tl_2` `n1` 明确 source name 只读、不作键；`proj_tl_4` `n1/n2` 区分提取模板与 Concrete Source 导入两步。
- **判断：不需改（保留）**。平铺、别名、source name 身份边界与导入→提取链已有图面覆盖。

### Card 9｜A②-卡9 Template Lifecycle

- **契约依据**：[Template Lifecycle](../review/ui-component-contract-r2/contract-cards.md#template-lifecycle-control)、[Template lifecycle guards](../review/ui-component-contract-r2/component-contract-consolidated.md#template-lifecycle-guards)。
- **画布读数**：`proj_tlc_1`–`proj_tlc_3`；`proj_tlc_2` `st`「ARCHIVED」、`n1`「要改先 Restore；归档模板从普通 Source Picker 隐藏／降级」、`n2` 明确不自动改引用／fallback／找相似／复制payload；`proj_tlc_3` `rs` 钉 DirectReferenceSet 非空时不可Hard Delete。
- **判断：不需改（保留）**。ACTIVE／ARCHIVED、Restore／Hard Delete前置及不自动fallback边界已有覆盖。

### Card 12｜A②-卡12 Reference List

- **契约依据**：[Reference List](../review/ui-component-contract-r2/contract-cards.md#reference-list)、[Template reference sets](../review/ui-component-contract-r2/component-contract-consolidated.md#template-reference-sets)。
- **画布读数**：`proj_rl_1` `hdr` 缺省显示 EffectiveConsumerSet（含经物种层继承者），并分「经继承／直接引用」；`proj_rl_2` 有 Direct／Effective 两区、`c3a–c3d` 四项数；`proj_rl_3` `hdr`「不截断、只滚动（现行实现形态：可滚动约4.5行）」。
- **判断：需改：`proj_rl_2`。** Card12是无候选变更的只读清单；契约验收要求没有候选时不显示「最终结果变化数／新增 Error·Warning」，而现状 `c3c/c3d` 仍显示这两项。只改这两个画面层 TEXT：删除 `最终结果变化数 24` 与 `新增 Error·Warning 2E · 3W`，保留直接引用数／Effective consumer数及两集分区；不改 `proj_rl_1`／`proj_rl_3`，不改N2。

### RoleControl｜现有目标投影未在当前页以 `SECTION name` 命中

- **契约依据**：[RoleControl](../review/ui-component-contract-r2/contract-cards.md#role-control)、[Role intent](../review/ui-component-contract-r2/component-contract-consolidated.md#role-record-intent)、[Source transaction](../review/ui-component-contract-r2/component-contract-consolidated.md#source-transaction)。
- **画布读数**：当前页 `PROJECTION｜` 顶层 SECTION 名没有 `RoleControl`；本轮只读目标页枚举没有发现可按既有 section 名定位的 RoleControl 组。仓内 `figma-current.md` 以 Source/Role 双入口为现状入口描述，但本次不以“未命中”冒称全文件不存在。
- **判断：SOURCE_GAP／需另定 intake**。无法在当前页已读范围找到 RoleControl 对应现有目标投影；不能凭旧 annotation、仓文档或相似卡面编造投影帧。需主代理提供明确帧号/层名或另行限定文件/页后再判需改／保留。

## 2. 需改项逐字稿：A②-卡12 Reference List 修订候选

> 本轮唯一确认需改项是卡12 `proj_rl_2` 的只读清单。此稿只给候选，不写 Figma；节点的物理名不公开。

### §0 组登记

- 组：`PROJECTION｜A②-卡12 Reference List（三态）`
- 帧：`proj_rl_2`
- 修改性质：既有帧最小同步；保留两集分区、直接引用数与Effective consumer数，删除候选变更专属的后两项统计文本。
- 不改：`proj_rl_1`、`proj_rl_3`、N2、卡10、卡11、其余Cards。

### §1 帧内逐字文案

保留现有帧文案逐字不动，删除两条与无候选清单契约冲突的文本：

```text
删除：最终结果变化数 24
删除：新增 Error·Warning 2E · 3W
```

保留：`直接引用数 12`、`Effective consumer 数 31` 及 Direct／Effective 两区现有行。

### §2 annotation 计划

本帧现有 annotation 保留，不新增 annotation，不改变现有长形证据与版本登记。

### §3 契约映射

- [卡12 Reference List](../review/ui-component-contract-r2/contract-cards.md#reference-list)：无候选变更的列表不显示最终结果变化数／新增 Error·Warning，也不制造候选机制。
- [Template reference sets](../review/ui-component-contract-r2/component-contract-consolidated.md#template-reference-sets)：DirectReferenceSet 与 EffectiveConsumerSet 分列；后两项属于候选变更场景，不是无候选只读清单的当前读数。

### §4 验收判据

1. `proj_rl_2` 保留 Direct／Effective 两区和「直接引用数 12」「Effective consumer 数 31」。
2. 帧主体不再含「最终结果变化数 24」或「新增 Error·Warning 2E · 3W」；其 annotation 仍可保留对旧候选示例的解释，不能把 annotation 中的说明当作帧主体当前读数。
3. `proj_rl_1` 与 `proj_rl_3` 的文本、几何、annotation 不变。
4. 回读报告帧号＋层名定位、TEXT数量变化、annotation数组、绝对几何、flag与截图；写前必须保留目标组＋上下邻组 before 快照，并对拍未改区域。

### §5 冲突清单

- C12-1：画布 `proj_rl_2` 仍有旧候选示例四项数，但其 annotation 已说明只有 Direct／Effective 两数可作当前读数。建议只删除帧主体后两项，保留 annotation 的历史示例解释。
- C12-2：卡12组登记当前整体静态投影形态，不把删除两个文本行解释为运行时统计实现。

## 3. 仅annotation承载而Markdown缺失的“该回填契约”项表

本轮以现有帧文本、annotation 与契约逐条对拍；发现以下内容不应由 annotation 独自承担，需回填契约／执行卡后再视为可消费规则：

| 项 | 当前只在 annotation 的信息 | 建议回填载体 | 依据与处置 |
|---|---|---|---|
| 卡1选择器“类型名（示意）”是占位，旧鱼名示例不构成永久命名规则 | `proj_ss_1/2/3/4/5` 内嵌层 annotation | Card1 Source Selector 的示例数据／非规范字段约定 | 画布 annotation 自己声明这是示意；契约已规定 source name 只读、不作键，但没有这句示例免责声明。若该免责声明要成为消费者规则，先回填；本批不在画布补。 |
| 卡5旧GAP-ED-26/27是历史实现证据，不代表最新schema／当前实现 | `proj_pv_1/2/3/4` annotation | OPEN-ITEMS／实现证据登记 | 需求契约应区分历史证据与当前规则；本轮不从annotation反推当前实现状态。 |
| Card6/Validation 的“当前实现未重核”与字段级Setup入口UNIMPL | `proj_vd_4/5/8` annotation | OPEN-ITEMS／实现证据登记 | 这是实现状态而非产品契约；不得由静态图独立证明，需实现head绑定。 |
| Card7 `proj_as_6` 的“丢弃覆盖 raw buffer、未确认 staged candidate 等全部未durable本地态” | `proj_as_6` annotation | Card7 Actions／执行卡 | 画面文本只有记录页桥接，若该射程要成为可执行规则，应回填卡7；且该帧annotation不含 `⚑UNIMPL/⚐UNVERIFIED`，不因标记口径放松而改变。 |
| Card8 导入Concrete Source→可提取模板两步及Role激活不自动创建 | `proj_tl_4` annotation | Card8 Actions／契约卡 | 画面主体仅显示摘要，完整两步约束主要在annotation；需回填后才可当规范事实。 |
| Card9 归档不自动改引用/fallback/复制payload | `proj_tlc_2` 主体已有一部分，annotation补充细节 | Card9 Must not | 主体已有部分，但完整否定集合在annotation；回填唯一Owner，避免画面注释成为第二套规则。 |
| Card12 旧四项候选统计只是历史示例，非当前读数 | `proj_rl_2` annotation | Card12 Must show／契约卡 | 契约已有“无候选不显示后两项”，但旧示例的解释只在annotation；本批删除主体后两项，不依赖annotation替代规则。 |

**本表不新增规则；只列“现有 annotation 独有、若要作为可执行规范应回填”的候选项。** `⚑UNIMPL`／`⚐UNVERIFIED` 标记继续保留，不因短摘要／直链口径放松而删除。

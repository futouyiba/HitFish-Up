# UI Component Inventory ＋ 第一批 Contract Cards（「编辑器具体设计」席 · A 线）

<a id="batch-freeze-status"></a>
**状态（两批各自唯一；改自记录页 §265 裁 `F-07`）**：**批次① ＝ 七张全部「已冻结 v1.1」**（`A①-卡1`／`卡2`／`卡3`／`卡4`／`卡5`／`卡6`／`卡7`）；**批次②（`A②-卡8`…`卡12`）＝ 已冻结**（记录页 §244，以该节为冻结留痕）。**本文件不再有任何「起草稿」状态。** 据记录页 §164（冻结接口，已回页核实）。铁律遵守：卡片＝执行投影，机制唯一载体仍是 Current 文档，「依据」行不空——引 Current § 或记录页 §。

**阅读边界**：各卡保留消费者操作、显示、记录和验收场景；所引汇编维护共用机制，卡片摘要不另增规则。卡2恢复执行依据的原核对与修订过程见[固定基线](https://github.com/futouyiba/HitFish-Up/blob/ceceb630ec338f23a11170f9e047fbabd101eaf0/docs/review/ui-component-contract-r2/contract-cards.md#L3-L10)，不作为新一轮来源扫描。操作选择与值输入分卡的职责按[汇编 §4](component-contract-consolidated.md#field-value-control)。

**命名口径（记录页 §271 裁 `A-F-09`）**：本文件各卡的 `Component:` 行**是卡片层标识，不是产品／契约命名** —— 允许与页面语汇不同形，但**不得被下游当作稳定标识符**（不得拿它去建代码枚举／schema 字段／选择器／i18n key）。**凡页面上已有名字的物，一律以页面名为准**（如草稿的 `FieldValueRow` ⇒ 页面名 **`FieldValueControl`**）。正文（需求文档）里指向同一个物时，**只用页面已有的串、或纯语义描述**（§19 前置句已定）。

---

## Part 1｜UI Component Inventory v1（控件总清单）

| # | 控件 | 层·面 | 批次 | 状态／入口 |
|---|---|---|---|---|
| A1 | 顶栏（Editor Global Shell：工具身份/全局状态/Publish） | 框架 | ①（保存状态）＋④（系统面） | 不承载 Resolve/Bake 视图入口；Fish Subject 的编辑/解析预览位于 Context Header。保存区按[卡7](#autosave-status)，Publish 按汇编 §15 |
| A2 | 当前 Subject 标题 / 路径 | 上下文总览 | ④ | 放在中栏 Context Header：至少显示 Fish + 基础习性/Mode（含必要 `[兼容]`）；不是 Topbar 第二套导航，也不要求做可点击 breadcrumb |
| A3 | dirtyDot（按层待写盘） | 框架 | ④ | 语义已拍＝记录页 §167 六（随卡7 落地） |
| A4 | Subject Navigation Rail（FISH / 共享资产） | 主体导航 | ④ | 当前规则见[汇编 §1](component-contract-consolidated.md#subject-navigation)：顶层可达、单 Section 展开、鱼→基础习性/中鱼习性模式 |
| C1 | Source Selector·物种层 | 上下文总览 | **①卡1** | [卡1](#source-selector) |
| C2b | Source Selector·覆盖层变体 | 上下文总览 | **①卡1** | [卡1](#source-selector) |
| N1 | 卡上 templateName 显示 | 上下文总览 | ①（随卡1） | 通则=同源同名 |
| C3 | 组件卡 ×4（摘要/角标/覆盖计数） | 上下文总览 | ②/③ 分批 | 已规格（v2） |
| C4 | roleBadge＋Role 三态 | 上下文总览 | ③（Policy） | 已规格（v2） |
| C5 | 档案级字段块（fail_env_coeff） | 上下文总览 | ③（Policy ADD/SET 化） | 已规格（v2） |
| C7 | Authoring boundary 块 | 上下文总览 | ④ | 已规格（v2） |
| C8 | Operation Control（四动作） | 上下文总览/焦点编辑 | **①卡2** | [卡2](#operation-control) |
| C9 | 档位控件（四档＋Custom） | 焦点编辑 | **①卡3 内含** | [卡3](#field-value-editor) |
| C10 | 列底状态行 | 上下文总览 | 下一期（reconcile 实现） | 维持 §125 四 现状；机制契约落《契约》§6.5/§9.4 且按记录页 §167 一.3 **移 Deferred**：界面 §9.2 不把「重新导入/采纳配置表值」当当前控件，只读诊断（drift/orphan）可留；实现出期＝§163 |
| C11 | 统一抽屉（本期四节） | 上下文总览 | ①（校验节=卡6）＋④（整抽屉） | v1.1 已收；本次候选变更的承载分工见[共享N2](#rebase-impact-preview) |
| D1 | 编辑栏空态 | 焦点编辑 | ④ | 已规格（v2） |
| D2 | 编辑栏分档（可编/置灰只读） | 焦点编辑 | 通则 | 已规格（v2） |
| D3 | 水温编辑面（6 参＋曲线＋导入） | 焦点编辑 | ③（Temperature） | 已规格（v2）；**6 参中衰减形状为枚举项（项名 `falloff`／显示标签 `falloff_shape`）⇒ 无「调整」入口**（记录页 §175、六.2） |
| D4 | 结构/水层/时段编辑面 | 焦点编辑 | ①载体（slice C 首线=Structure） | 载体形态=卡1/2/3 |
| D5 | 时段空态路径＋三预设 | 焦点编辑 | ③ | 已规格（v2） |
| E1 | 鱼列表 | 独立面 | ④ | 已规格（v2） |
| E2 | 共享资产 → 习性模板（清单/别名/生命周期/Replace） | 独立面 | ② | 已规格（v2）；Species Presets 为共享资产 sibling view |
| E3 | 引用者列表（两集两数） | 独立面 | ② | 已规格（v2） |
| E4 | Resolve Preview | Fish Subject 只读工作视角 | ④ | V1 产品 Current 见 [Secondary Surfaces §1](../../fish-habit-editor-v1/secondary-surfaces.md#1-resolve-preview解析预览) |
| E5 | Bake Preview | Post-V1 | — | 不属于 V1；待条件输入 / 基础权重等口径闭合后再设计 |
| N2 | Rebase／Impact Preview 面板 | 编辑/工作区 | ②/④ | [共用交互与验收](#rebase-impact-preview)；事务机制按汇编 |

---

## Part 2｜第一批 Contract Cards（A①-卡1…卡7）

批次状态见[文件头](#batch-freeze-status)。原冻结依据为记录页 §165；`A①-卡2` 2026-09-21 恢复的依据见文件头固定基线。

**编号口径（防撞车）**：本席编号＝**A 线批次编号**，标题带前缀（`A①-卡1`…`A①-卡7`、`A②-卡8`…`A②-卡12`）。**GPT 清单另有一套「卡4 ComponentCard／卡5 Impact Preview」，与本席 `A①-卡4`（Effective Value Display）／`A①-卡5`（Provenance Display）不是同一批** —— 引用务必带前缀。

<a id="source-selector"></a>
### A①-卡1｜Source Selector（来源选择器；物种层＋兼容 Mode）

**机制入口**：[汇编 §8](component-contract-consolidated.md#source-transaction) 定义 Source staged 协议、fan-out 与同值意图边界；V1 的产品承载见 [Fish Authoring Surface §12](../../fish-habit-editor-v1/authoring-surface.md#12-source-change-candidate)。

```
Component: Source Selector｜组件卡唯一 Source mutation 入口
Reads:
  - 当前 source binding（Species recipe source；兼容 Mode 的 sourceOverride / follow-parent）
  - 按汇编 §8 的层级 Source allowlist 生成合法候选
  - Shared Template 清单；Temperature 在合法 Species Concrete 已存在时可显示“当前物种生态数据”
Actions:
  - SELECT_SOURCE：建立 ephemeral candidate，不立即写盘；确认后物种层写 recipe source，Mode 写 sourceOverride。
  - FOLLOW_PARENT：Mode 选择“跟随基础习性”；按同一 staged 协议确认后删除 sourceOverride。
  - 换源后既有 operations / patches 原样保留，在 candidate 上重 Resolve。
Durable mutation:
  - candidate 不写持久；Preview + 显式确认 + revision 核验后原子提交。
  - 换源不清 operation，不生成保值 SET。
Acceptance:
  - Local / Propagated 由 fan-out 决定，但两者都使用同一个 V1 Review Panel，不出现先写盘后预览。
  - explicit pin ↔ follow-parent 即使当前 Effective Source / values 相同也是真实 durable change，必须显示 binding intent 与未来传播差异。
  - 选择与当前 durable binding intent 完全相同的候选是 exact no-op，不建立 candidate。
Must show:
  - Component Card 上当前 Source 的作者可读名称。
  - Mode 跟随时显示“跟随基础习性 → <Effective Source>”；显式 pin 显示“<Source> · 本模式设置”。
  - same-effective explicit pin 与 follow-parent 必须可区分。
Must not:
  - 不保留顶部 templateRow / 前层 Source Selector 作为第二 mutation entry。
  - Focus Editor 不提供 Source Selector。
  - 不自动清 operations；不静默生成 SET；same-effective 不自动去 pin。
  - Mode picker 不列 SpeciesConcrete；需要消费物种 Concrete 时走“跟随基础习性”。
  - ARCHIVED Template 不作为新候选。
依据: Source allowlist / durable shape / transaction 见汇编 §8；V1 UI entry ownership 见 V1 Product Current。
```

<a id="operation-control"></a>
### A①-卡2｜Operation Control（缺省支·调整·设置为·仅使用当前来源）

**语义入口**：[汇编 §3](component-contract-consolidated.md#component-clear) 定义组件 CLEAR / absent、Source 独立性与同值意图；[§13](component-contract-consolidated.md#component-operation-allowlist) 定义组件 allowlist；[§4](component-contract-consolidated.md#field-value-control) 定义落盘时机与无值动作例外。本卡保留「层 × 类型」四格 UI 和展示职责，不另存一份完整解析定义；Policy 用[§10](component-contract-consolidated.md#policy-clear)。 Tier 的定义与形状见[§5](component-contract-consolidated.md#tier-contract)。Profile／Setup 机制另见[§11](component-contract-consolidated.md#profile-lifecycle)；原实现类型缺口只按[固定取证](https://github.com/futouyiba/HitFish-Up/blob/add09fdaa9c197740df6735160af45c1ebb32370/docs/review/ui-component-contract-r2/contract-cards.md#L115)读取。

```
Component: Operation Control｜字段操作控件（INHERIT/ADD/SET/CLEAR 四动作）
Reads:
  - 该字段当前层 op（absent/ADD/SET/CLEAR）与上层 op（继承源）
  - 来源值（= **当前来源值** —— ADD 的基准；**当前来源**可以是共享模板，也可以是合法的 `SPECIES_CONCRETE`）（记录页 §316 裁 `CXR-04`）
  - **字段类型**（数值项 / 枚举绝对值项）与**层**（物种层 / 桶·习性档案层）—— 决定出哪些选项（见 Actions 首条）
  - tier（作者档位，独立字段）
Actions:
  - UI 采用稳定作者词表，不根据上层当前 op 类型动态改动作名称：
      · **Species Base × 数值**：沿用来源 / 调整 / 设置为；
      · **Species Base × 枚举**：沿用来源 / 设置为；
      · **Compat Mode × 数值**：沿用物种设置 / 仅用当前来源 / 调整 / 设置为；
      · **Compat Mode × 枚举**：沿用物种设置 / 仅用当前来源 / 设置为。
  - “沿用来源”＝物种层无本层 operation；“沿用物种设置”＝Mode absent；“仅用当前来源”＝Mode CLEAR；“调整”＝ADD；“设置为”＝SET。
  - ADD / SET 需要参数；切到需要参数的 operation 时先进入 transient raw-input，不自动制造 ADD 0、不沿用旧 operation 参数、不自动保持 Effective Value。
  - absent / CLEAR 属无值动作，可直接形成 ordinary durable edit。
  - 调整（ADD）始终相对当前 Source value；设置为（SET）是绝对值。
Durable mutation:
  - 按所引汇编 §3 写入／删除字段记录，不经值差合成；typed 值的提交要求和 INHERIT / CLEAR 例外按汇编 §4。
  - UI 计数沿用本卡冻结投影：CLEAR 计入本层操作数。来源核对由卡前所引汇编 §4 导航至 UI取证台账；不能借 durable 语义把它升级为上游已核规则。
  - Tier 独立字段的适用形状按汇编 §5 写入；不按当前有效数值补元数据。
  - 写记录时机按所引汇编 §4「切操作时的落盘」。
Must show:
  - 选项集随「层 × 字段类型」变化（枚举项不出现「调整」；物种层不出现「仅使用当前来源」）——出选项不得靠形状统一
  - 四动作用户语言分开，且**缺省支按层给串**：**物种层缺省＝「仅使用来源」**（它上面没有可沿用的操作 ⇒ 不写没有宾语的「跟随」）；**桶层缺省＝「沿用物种操作」**（**行内显示按实际继承到的那个操作给具体串**：「沿用物种调整」／「沿用物种设置为」；**物种层无操作时该行显示「仅使用来源」**）；「沿用物种操作」≠「仅使用当前来源」，不得合并成一个「恢复」
  - **`CLEAR` 那一态必须在行内可见「移除了哪条继承操作」**（视觉降级行，如「物种调整 −0.20 · 已被本层替代」）—— **不许只靠文字区分**它与「本层什么都没表达」（两者结果值可能相同、**意图不同**）；被替代的 op **只用于解释 provenance、不参与链式计算**
  - 三行展示「来源值 / 相对调整 / 当前值」；ADD 与 SET 显著不同视觉语言
  - 已覆盖但同值仍读作已覆盖（显示读记录，不按值差）
  - **SET 掩盖**可视（**被 SET 盖住**）；静态当前态的显示边界按 `A①-卡4`，本卡不另维护实现缺口状态。
Must not:
  - 不合并两个「恢复」；不叠第三层 delta / 多 op 链
  - 不从 payload 相等推断继承（同值/同源显式表达必须保留）；SET 同值不得自动删
  - 不静默 clamp/取绝对值/平移/归一（负值交卡6 报 ERROR）
依据: 语义与层／类型 allowlist 见卡前链接（汇编 §3／§13；Policy §10；提交 §4）。UI 四格：记录页 §312 XR-F-03；用户语言：《编辑器界面》v18 §1.2；被替代 op 只解释 provenance：本卡 Must show。Tier 的完整规则与原裁定边界见汇编 §5。旧 Q3 引文及 CXR-04 更正注保留于卡前固定版本链接，当前来源基准按汇编 §3。
```

<a id="field-value-editor"></a>
### A①-卡3｜Field Value Editor（数值/档位/曲线输入）

**机制入口**：[Tier §5](component-contract-consolidated.md#tier-contract)、[校验 §6](component-contract-consolidated.md#validation-autosave)、[水温 §12](component-contract-consolidated.md#temperature-behavior)、[Profile／Setup §11](component-contract-consolidated.md#profile-lifecycle)、[TimePeriod Batch Overwrite Guard §15](component-contract-consolidated.md#timeperiod-batch-guard)。本卡保留输入、显示及具体操作。

<a id="temperature-threshold-ui"></a>
**本批水温阈值用途投影**：保留卡3现有阈值呈现、已有值与合法编辑入口；这是当前投影，不是跨界面永久禁止折叠或只读的规则。用途说明按明确的 species／bucket Effective Role：非 CORE 时可显示“仅 CORE 用于门控；当前上下文不使用此阈值”。共享模板没有唯一当前 Role，只说明“供 CORE 消费者门控使用”，不套用单一角色文案。Role 切换不据该说明清空或补值；校验仍消费《配置表与校验》v5 §5／§5.2／§6及[汇编 §6](component-contract-consolidated.md#validation-autosave)，用途标签不表示免校验。

验收：非 CORE 缺阈值不因这一缺值报 required；已有越界值仍显示既有诊断，不能因“不使用”清空、clamp或报全部合法。结构可表达错误的保存／Publish区别沿既有规则；共享模板面能辨识其对CORE消费者的用途，合法参数编辑仍可达。本段不复制值域或新增必填规则。设计来源与回退见[本批提案](../../proposals/0.3.4.0-B-n2-ui-projection.md)。

```
Component: Field Value Editor｜值输入控件（数值输入、档位选择、水温曲线）
Reads:
  - typed 当前值
  - 汇编 §5 的档位表与可表达范围，读取当前作者选择的 tier。
  - 档位适用面：**结构＝按当前 Source 动态生成的 StructureType 字段控件（不固化字段数量**；现行实例 25 —— 其 `member_key` `0`…`24` 是**数据/记录层的查表键数**，不得反读成 UI 的固定字段数）／水层 3 行／时段 5 行；水温豁免（连续曲线）
  - 水温曲线参数（六参；`temp_threshold ∈ [0,1]`；**衰减形状＝枚举绝对值项**）
  - **两层名（记录页 §175 六.2，现行）**：**项名位写 `falloff`**（与同列短形族一致：`acceptMin / favMin / favMax / acceptMax / threshold`）；**字段位 / UI 显示标签写 `falloff_shape`**（对应字段族长形 `temp_accept_min / …`）。**两处各按其位、不判谁对谁错、不做统一**
Actions:
  - 数值输入：Enter/blur 形成有效 typed 值＝一笔 semantic edit
  - 档位选择（tier）；Custom 精确值
  - **`falloff_shape` 那格（项名 `falloff`）是枚举 `<select>`（`LINEAR` / `SMOOTHSTEP`）——不给 `ADD` 入口**（口径与卡2 一致：枚举项三支）
  - 水温曲线按汇编 §12 展示；参数继续通过各项输入控件编辑，数值项的相对调整交卡2。曲线只读不能扩大成整段温度档案不可编辑。 阈值的上下文用途显示与验收按卡前投影。
  - 时段三预设一次性填表（覆盖确认按卡前所引汇编 §15 Batch Overwrite Guard；模板名不进 Runtime）
Durable mutation:
  - 有效 typed 值经卡2 落 op；raw buffer（"-" "0." "abc"）不写 durable typed、不覆盖上一 durable 值（保留 UI local）
  - Tier 元数据按汇编 §5 的记录形状交给卡2持久化。
Must show:
  - 仅在汇编 §5 适用的字段／op 上提供档位选择；越档保留作者选中的标签，并显示诊断供作者显式修改。
  - 每项 继承/已覆盖 状态（读记录）
  - 按汇编 §6 显示 Effective 值诊断；ERROR／WARNING 都用红标，靠文案与阻断性区分，不靠颜色。
  - 不可解析＝即时输入错误
  - 时段未配时显示空态，并按汇编 §11 引导显式 Setup、呈现缺 required Profile 诊断（卡6）；本卡不另定义 Role promotion 后果。
Must not:
  - 不静默 clamp/取绝对值/平移/归一
  - 不把 raw 字符串写 typed state；不把「未配置」编码成 null 必填字段的现存记录
  - 不因 UI 统一强行给枚举绝对值项上 ADD（**射程只落在枚举绝对值项 `falloff_shape`**；`acceptMin / favMin / favMax / acceptMax` **属那 5 个数值项、`ADD` 合法**，不得一并禁掉）
依据: Tier规则见汇编 §5；校验／持久化边界见 §6 与 §4；参数／曲线机制见 §12；operation allowlist见 §13。输入与显示依据：《编辑器界面》§1.1／§1.2、《编辑器持久层契约》§7.1；项名／字段名分层采用记录页 §175 六.2（不采用其已撤销的 §175 四统一命名）；temp_threshold∈[0,1]＝《配置表与校验》§5／《开发需求》§4.3。
```

<a id="effective-value-display"></a>
### A①-卡4｜Effective Value Display（当前值展示）

本卡保留静态当前态的显示边界；旧实现观察、候选方案与当前取证任务见[问题台账](OPEN-ITEMS.md#source-drift-implementation-evidence)，不以历史实测口吻判断今日实现。

```
Component: Effective Value Display｜有效值展示（只读）
Reads:
  - Effective Source ＋ per-field Effective Operation 的 Resolve 结果
Actions:
  - 只读；查看来源链→切换当前 Fish Subject 到“解析预览”并聚焦对应字段
Durable mutation:
  - 无——Effective 是派生结果，可缓存/预览，不作 authoring truth 持久化
Must show:
  - 当前值与 provenance（值来自哪层表达、哪份来源）
  - **SET 掩盖**：**只报当前态可证的那一半** —— **「本层的最终操作是 `SET`」**（当前可判）。⚠️ **「最终值未变」本卡不出现** —— 它**需要 before/after 比较**，**只有 Impact Preview 语境可算**（卡10／卡11）；本卡没有候选变更输入。**不要求为此新增耐久快照机制。**（记录页 §312 裁 `XR-F-06／CXR-05`）
  - **「来源已变」不呈现**：静态当前态不能证明来源在两个时点间发生变化；本卡不要求新增耐久来源快照。候选变更的 before/after 判读仍在卡10／卡11，不与本卡当前 SET 记录态混用。
Must not:
  - 不把 Effective Value 写为 authoring source；不据此反推 ops/继承
依据: 《编辑器界面》§9.1（焦点编辑栏显式展示「来源 → 当前层操作 → 当前值」）；《编辑器与 Resolve》§11.1（Effective Source＋Effective Operation → Effective Value＝派生结果）；《编辑器持久层契约》§3.7（equal-value SET 与纯 source pin **在 projection 复用判定上**必须区分——**不是**立牌可判的根）；⚠️ **「SET 掩盖」这个量只在 Impact Preview 语境可算**（`A②-卡10`／`A②-卡11` 的 before/after 都在手，其分类里保留该支）；**立牌上收纳**（本卡）
```

<a id="provenance-display"></a>
### A①-卡5｜Provenance Display（解析说明）

V1 产品层承载见 [Secondary Surfaces §2](../../fish-habit-editor-v1/secondary-surfaces.md#2-右栏解析说明)。本卡只保留当前 Effective Configuration 的最短充分来源解释；外部生态数据 Import / Reimport 不属于 V1。

```
Component: Resolve Explanation｜解析说明（只读）
Reads:
  - Effective Source relation
  - per-field Effective Operation relation
  - Effective Value
  - Policy Template / Species / Mode 的 Role 与 fail_env_coeff 解析链
Actions:
  - 只读查看
  - “在编辑中打开”切回同 Subject 的 Edit 并定位对应 Component / Field / Policy
Durable mutation:
  - 无；全部为 derived projection
Must show:
  - Source 与 Operation 两条独立继承轴，不压成模糊“继承”
  - 来源值 → 有效操作 → 最终值的最短充分解释
  - Role / fail_env_coeff 的 Template → Species → Mode → Effective 链
  - SET 当前态可说明 Source value 被本层设置覆盖；无 before/after 输入时不得声称“来源已变 / 结果未变”
Must not:
  - 不显示 row_key / production row name / materializer trace
  - 不把 Resolve 做成第二套只读 Editor
  - 不引入 Bake / condition snapshot / evaluator trace
  - 不把 derived provenance 持久化为第二份 truth
依据: Effective Source + Effective Operation → Effective Value 的低层语义见汇编 §3；Policy 语义见 §9–§10；V1 产品承载见 V1 Product Current。
```

<a id="validation-diagnostic"></a>
### A①-卡6｜Validation·Diagnostic（校验诊断；＝C11 抽屉校验节）

**机制入口**：[通用校验 §6](component-contract-consolidated.md#validation-autosave)、[断链来源 §8](component-contract-consolidated.md#source-transaction)、[Profile 缺席 §11](component-contract-consolidated.md#profile-lifecycle)；本卡规定诊断如何展示与定位，下面是消费者场景。

```
Component: Validation·Diagnostic｜校验诊断（ERROR/WARNING）
Reads:
  - editor-state ＋ current schema ＋ current validator——diagnostics 全量派生重算（重开即重算）
Actions:
  - 打开校验清单；每条展示可读 breadcrumb 与错误原因。已有局部 locate / focus 若可用可继续保留，但 V1 不要求跨 Context 精准跳转。
  - Publish 前全量校验（消费 durable revision）
Durable mutation:
  - 无——diagnostics 不作第二 durable truth；semantic ERROR 随 state 一同 durable 保存（「编辑器已保存 · 有错误」态）
Must show:
  - ERROR（＝Publish 阻断项）/ WARNING（如 Soft Fit>1）分级
  - 顶栏「编辑器已保存 · 有错误」的「有错误」点击＝展开 ERROR 清单；不要求自动跨 Context 定位首个 ERROR
  - BROKEN_SOURCE_REF：对象/component/ref；可加载修复、Publish 阻断、不 fallback
  - **Role 激活（CORE／SECONDARY）后立刻显示「缺 required Profile」校验态**（记录页 §199 ⑥③ 的附条件：不提示地让作者停在非法态，是那一条唯一风险面）
  - Preset→归档源不可 Apply 且指名哪个源已归档
  - Publish blocker 至少显示「对象 → 层/行 → 区域/组件 → 具体项」breadcrumb + message；跨字段不变量可定位到共同 Profile / 区域并在消息中列相关字段
Must not:
  - 不把 ERROR 显示成「保存失败」；不伪造 0/默认值/静默补齐（不能解析＝Error/N-A，能解析区继续展示）
  - 不把 required 缺失当 autosave 阻断（durable-valid 与 publish-valid 分开）
  - 不为 V1 新增统一 `Diagnostic.owner` / Context Router / EditorAddress 身份层；不因导航未统一而删除已有局部 locate
依据: 记录页 §199 ⑥③（激活 Role 后须立刻把「缺 required Profile」做成可见校验态；**判级仍按上游**——界面 §1.4 已载「CORE / SECONDARY 缺必需 Profile 才阻断」，本条补的是**时点与可见性**，不是新的判级）；《编辑器界面》§1.4（三处校验分工：开发需求 §7 总则／条件开关 §10 编辑器静态／配置表 §5 Schema 不变量）＋§1.2（越界两侧；Validator ERROR 不是「保存失败」）；《开发需求》§7（发布阻断总则；发布前阻断≠authoring 持久化阻断）；《配置表与校验》§5；《编辑器持久层契约》§7.1（durable-valid 与 publish-valid 分开、durable 允许携带 ERROR）＋§6.5（诊断＝派生量、每次重算）＋§3.10（BROKEN_SOURCE_REF load-tolerant/publish-strict；Preset 引归档源 invalid-for-apply 且 UI 指名）
```

<a id="autosave-status"></a>
### A①-卡7｜Autosave Status（保存状态；＝A1 顶栏保存状态区）

**本批来源核对**：《编辑器界面》v20（`Last Updated 2026-09-21 17:19 +08:00`）§9.1 明确丢弃未 durable 的本地态；《编辑器持久层契约》v16 §6.3 规定保存／Publish／revision 边界。旧窗口限定及 `CXR7-DISCARD-01` 修正过程保留于[固定基线卡7](https://github.com/futouyiba/HitFish-Up/blob/add09fdaa9c197740df6735160af45c1ebb32370/docs/review/ui-component-contract-r2/contract-cards.md#L231)，不再作为当前动作限制。实时记录页 §178／§393 本批未重读，历史作者词裁定不替代本次 Current 射程。

```
Component: Autosave Status｜自动保存状态区（顶栏）
Reads:
  - durable write 结果；base revision 对比（打开时记录、每次 commit 前校验）
Actions:
  - 保存失败时：重试／显式 reload-reconcile（外部修改＝BLOCK＋报告，不 auto-merge）
  - 「丢弃未保存的改动」：仅清除真正尚未 durable 的本地态，包括输入临时字符串、未确认的 staged Source candidate 及其它明确 ephemeral UI 状态；防抖未提交与保存失败后仍未持久的编辑同在此范围。显示回到上次成功持久化 revision，不回退任何已成功 autosave 的语义编辑；不是 Undo。Source candidate 的确认协议见卡1。
  - 顶栏 `发布到生产配置…`：只进入 / 聚焦 canonical Publish 区，不直接执行 writeback。唯一 Publish executor 在该区内；消费 durable revision，持久化失败先修（Publish 不隐式执行不可见 Save）。完整 preflight / generation 边界见[汇编 §15 Publish](component-contract-consolidated.md#publish-boundary)。
Durable mutation:
  - 状态本身不入 durable（UI state）；semantic edit→debounce/coalesce→原子持久
  - **「丢弃未保存的改动」不改 durable** —— 它只丢弃未落盘的那一笔；盘上仍是上次成功的 revision（故它不产生新记录、也不删任何已持久记录）
Must show:
  - 四态：`编辑器已保存` / `编辑器已保存 · 有错误` / `编辑器保存中…` / `编辑器保存失败`（I/O·revision 冲突）；不得缩成会与 Production Publish 混淆的裸 `已保存`。
  - 「有错误」链接到卡6 校验节
Must not:
  - 不常驻 Save 按钮；不把 Validator ERROR 当保存失败
  - 作者可见动作名为「丢弃未保存的改动」，不用工程词 Reset（命名裁定沿卡前固定历史）。
  - **「丢弃未保存的改动」不得读作「回到出厂 / 空态」**；它也不是 Publish 的一部分（不因它触发任何物化 / 发布）
  - 不 silent last-write-wins；autosave ≠ Publish ≠ Git commit；Production generation mismatch / unverifiable 属 Publish preflight，不显示成 Autosave 保存失败。
依据: 《编辑器界面》v20 §1.1／§1.2（保存状态、ERROR≠保存失败、外部改动阻断并显式重载／reconcile）、§9.1（丢弃真正未 durable 的本地态，明确含未确认 staged candidate；不是 Undo）；《编辑器持久层契约》v16 §6.3（语义编辑、乐观 revision 检测、禁止 silent last-write-wins；Autosave／Git commit／Publish 相互独立，Publish 不隐式 Save）。历史命名及修正依据见卡前固定版本链接，不以旧窗口概括当前射程。
```

---

## 收口提示（给主代理）

Structure 竖切的实现依赖见[汇编 §2](component-contract-consolidated.md#structure-slice)，卡片冻结状态见文件头。卡片正文用「兼容壳／习性档案」，技术标识符原样保留（记录页 §102）；已满足的冻结前门禁与逐卡派单经过由 Git 保存。

---

## Part 3｜第二批 Contract Cards（A②-卡8…卡12 · 模板生命周期）

批次状态与冻结依据见[文件头](#batch-freeze-status)。

覆盖 Inventory E2/E3/N2。底稿＝v2 规格，依据引②后 Current §（落页措辞已逐字核）。

<a id="template-list"></a>
### A②-卡8｜Template Library List（模板清单与别名）

```
Component: Template Library List｜模板清单与别名（共享资产 → 习性模板；Subject Navigation 入口同源）
Reads:
  - 模板清单（按组件过滤；平铺、默认按引用量排序）
  - 每模板：templateId / stableKey（只读）、displayName、中文别名 name_zh / 英文别名 name_en（别名不是生产行 name）、extracted_from（只作追溯、不作关联依据）
  - 生命周期状态（ACTIVE / ARCHIVED）
Actions:
  - 浏览 / 按组件筛选；编辑 name_zh / name_en
  - 「从当前鱼提取模板」（创建）＝**`A①-卡1` 的 EXTRACT_TEMPLATE 在本工作区的入口**——**同一动作、两个入口**，不另实现一套
  - **V1 不提供“从钓鱼元素周期表导入 / Reimport”动作，也不暴露 Lux CLI。** 该能力已移出 V1；其既有 Concrete Source / provenance / reimport 低层语义仅作为 Post-V1 参考保留，不构成当前 Template Library UI action。
Durable mutation:
  - 别名写编辑器持久层模板记录（template_key 空＝未物化，editor_key 必填）；抽取创建模板资产
  - displayName 改名 ≠ identity rename
Must show:
  - source name 只读；引用量排序；ARCHIVED 降级/标记；别名可空（空＝未起）
Must not:
  - source name 不作键；不提供 stableKey identity rename（错名处置＝新建＋Replace＋归档旧）
  - 不引入分组 / 族折叠（平铺）；不因结构对称给 Quality 预造 Template
  - **V1 不显示周期表导入入口**；**不因 Role 激活自动创建模板／Profile**（记录页 §199 ⑥③：创建永远显式）
依据: 《编辑器持久层契约》§3.6（模板清单与别名记录表）＋§3.10（identity immutable；displayName 可改）；《编辑器界面》§7（平铺可滚动、按引用量排序、别名可编辑、source name 只读）
```

<a id="template-lifecycle-control"></a>
### A②-卡9｜Template Lifecycle（ACTIVE / ARCHIVED）

**机制入口**：[汇编 §14 生命周期与删除](component-contract-consolidated.md#template-lifecycle-guards)；本卡只承接操作、记录与显示。

```
Component: Template Lifecycle｜模板生命周期
Reads:
  - lifecycle；按汇编 §14 枚举的完整 DirectReferenceSet（包括 Preset／Policy durable 直接绑定）
Actions:
  - Archive（ACTIVE→ARCHIVED）／Restore（ARCHIVED→ACTIVE）；Hard Delete 执行前按所引 guard 清点引用
Durable mutation:
  - Archive／Restore 只改 lifecycle；Hard Delete 通过 guard 后删除模板资产
Must show:
  - ARCHIVED 标记与不可新引用／不可直改值的限制；Restore 入口；删除前的直接引用清单
Acceptance:
  - 只有 Preset 仍直接引用、或模板已归档但仍有直接引用时，Hard Delete 不可执行；清空全部直接引用后才允许删除。
  - 归档后既有 Recipe 仍可 Resolve／Publish；引用归档源的 Preset 不能 apply，指出具体源。编辑完整值须先 Restore。
Must not:
  - 不绕过汇编 §14 的两态、删除及归档传播边界；普通 Source Picker 按该节隐藏／降级归档项
依据: 《编辑器持久层契约》v16 §3.6／§3.10；完整机制与来源版本见卡前入口。
```

<a id="rebase-impact-preview"></a>
### 共用N2｜Source / Propagation Candidate Review

本段只保留 staged mutation 的共用语义护栏；Fish Habit Editor V1 的具体承载以 [Fish Authoring Surface §12](../../fish-habit-editor-v1/authoring-surface.md#12-source-change-candidate) 为产品层 Current。

**V1 承载**：
- Candidate 是短事务，不是可跨页面挂起的 Draft，也不新增第三个长期工作视角。
- Fish Source Change 的 Review 复用当前右侧 Focus Editor 临时承载；不新建独立 N2 Workspace / Modal。
- Candidate active 时暂停其它导航、ordinary mutation 与 Publish，直到确认或取消。
- Local / Propagated 使用同一 Review Panel；是否传播只决定 Review 内容重量，不决定是否 staged confirm。

**共用必须表达**：
- 当前 binding intent 与候选 binding intent；
- before / after Effective 结果；
- value 不变但被 SET / operation 遮罩的情况；
- same-effective explicit pin ↔ follow-parent 的未来传播差异；
- Candidate 新增 / 解除的诊断；
- Propagated 情况下区分“直接修改”与“跟随受到影响”。

**提交边界**：
- Candidate 不先写盘；确认前做 revision check，确认后 atomic durable commit。
- 取消只丢弃 Candidate，不回滚已 durable 的 ordinary edit。
- Candidate after-state 有 publish-blocking ERROR 时，只要 mutation 本身 schema-valid，仍允许确认保存；确认不是 Publish。
- exact binding intent no-op 不建立 Candidate。
- 不为保持旧 Effective Value 自动制造 SET，不清已有 operation。

模板完整值编辑、Replace References 等其它 propagated mutation 可复用同一 staged transaction semantics；其各自对象、写集与影响集合仍由对应卡片和汇编 §14 定义。V1 不要求它们使用与 Fish Source Change 完全相同的屏幕几何，但不得重新引入先写盘后预览、长期 Draft 或第二套 durable truth。

<a id="template-value-editor"></a>
### A②-卡10｜Edit Template Value（模板完整值编辑；高影响）

**机制入口**：[模板完整值与影响统计 §14](component-contract-consolidated.md#template-reference-sets)、[确认及改值边界](component-contract-consolidated.md#template-replace-boundary)、[水温曲线 §12](component-contract-consolidated.md#temperature-behavior)、[Publish边界 §15](component-contract-consolidated.md#cross-layer-guards)与[卡7](#autosave-status)；共用候选交互见[N2](#rebase-impact-preview)，水温用途说明见[卡3局部投影](#temperature-threshold-ui)。本卡保留模板编辑流程及显示。

```
Component: Edit Template Complete Value｜模板改值（共享模板完整值编辑）
Reads:
  - 模板完整值 completeValue；EffectiveConsumerSet（改值的真正影响对象）
Actions:
  - 编辑模板完整值候选 → 按共享N2完成预览／确认；按既有机制原子 durable 提交后，re-resolve 并刷新受影响投影的预览。
  - 生产物化／写回由独立的显式 Publish 按卡前所引汇编 §15 与卡7触发，不由本次模板保存确认自动执行。
  - ⚠️ **本卡不出现 `ADD`／`SET`／`CLEAR` 这类 operation 语义** —— 模板是**完整值资产**，**operation 只存在于物种 Recipe 与桶 patch 上**（《编辑器持久层契约》§3.3／§3.7）。
  ⇒ 具体记录规则按汇编 §14；本卡不把模板值编辑呈现为字段 operation 编辑。
  - 水温曲线按汇编 §12 只读展示；作者仍通过参数项编辑模板完整值，不提供曲线拖拽／Handle。
Durable mutation:
  - 改 completeValue＝一次全局作者确认；Preview buffer＝短命 UI state，不是 durable Draft Entity
Must show:
  - 候选影响的共用显示按N2，统计定义按汇编 §14；本卡只提供模板完整值编辑对象。
  - after-state 出现 publish-blocking ERROR 时醒目标出（仍可确认保存；Publish 阻断到修复——错误进卡6）
Must not:
  - **不实现水温曲线 drag-author**（P0）；也**不得把「曲线只读」扩大成「温度档案不可编辑」**
  - 不给全部引用者制造逐项 review debt（正常传播不产生 N 个下游待办；只有真实异常 / Validator 问题单独暴露）
  - 不静默改任何 consumer 绑定
依据: 《编辑器持久层契约》§3.10／§3.7、《编辑器界面》§1.1／§7，机制统一见汇编 §14；水温曲线 P0 能力见汇编 §12（记录页 §199 ⑥②）。
```

<a id="replace-references"></a>
### A②-卡11｜Replace References（批量换绑 A→B）

**机制入口**：[汇编 §14 两引用集](component-contract-consolidated.md#template-reference-sets)与[Replace 边界](component-contract-consolidated.md#template-replace-boundary)；staged 协议按[§8](component-contract-consolidated.md#source-transaction)，共用候选交互见[N2](#rebase-impact-preview)。

```
Component: Replace References｜批量换绑（模板 A → 模板 B）
Reads:
  - DirectReferenceSet(A)（改绑目标）；候选 B；全图 before／after Resolve 结果
Actions:
  - 选 A → 选 B → 将本次换绑候选交共享N2预览／确认，提交只执行下述直接绑定 mutation。
Durable mutation:
  - 只写直接 source bindings；operations／patches 按所引边界保留
Must show:
  - 改绑对象与有效影响对象的区分按N2展示；引用集与四项统计定义按汇编 §14。
Acceptance:
  - Species 直接引用 A、child 继承它时，换绑只写 Species binding；child 经 Resolve 消费 B，仍无新增 sourceOverride。
  - 已有 ADD／SET／CLEAR 保留；不为维持旧值制造 SET；after 统计来自全图 Resolve，不能只 diff 模板 payload。
依据: 《编辑器持久层契约》v16 §3.10；Source 与操作正交仍见汇编 §3。
```

<a id="reference-list"></a>
### A②-卡12｜Reference List（引用者列表；两集两数）

**机制入口**：[汇编 §14 两引用集与统计上下文](component-contract-consolidated.md#template-reference-sets)；原 CXR-03 修正出处在该节保留，本卡不另维护一份定义。

原“四组件分组／约4.5行”为[固定历史实现观察](https://github.com/futouyiba/HitFish-Up/blob/042f3a9df2ee7521e8ef32d77b6d78407e10946c/docs/review/ui-component-contract-r2/contract-cards.md#L391)，不限定本卡目标范围；本批未重跑实现。

```
Component: Reference List｜「这一行还被谁用」引用者列表
Reads:
  - DirectReferenceSet 与 EffectiveConsumerSet；覆盖当前五类 TemplateKind，按模板类别与引用关系组织，集合及 Policy 引用边界按卡前汇编 §14；不扩展 ComponentType 或 Runtime 四条件槽。
Actions:
  - 只读浏览（可滚动、不截断）；Replace 面板（卡11）另列 Direct 集
Durable mutation:
  - 无（纯展示）
Must show:
  - 缺省显示 EffectiveConsumerSet（含经物种层继承者），标注「直接引用／经继承」
  - 直接引用数／Effective consumer 数并列；共 N 条鱼／M 个鱼种
Acceptance:
  - 一个直接绑定有多个继承消费者时，两集两数分别展示；没有候选变更的列表不显示最终结果变化数／新增 Error·Warning，也不制造候选机制。
  - Policy 模板被 Species／SpeciesPreset 直接绑定时，可完整列出其直接引用与 Effective consumers；按汇编 §14 区分两集，不虚构 Affinity policySourceOverride。
Must not:
  - 不截断（只做滚动）；不把物理行共享展示成 Authoring 继承意图（碰巧同值 ≠ 有意共享）
依据: 《编辑器持久层契约》v16 §3.10（两集）、§3.7（lineage复用）；《编辑器界面》v20 §7（列表滚动不截断）。其余沿既有取证：界面 §5 不做三档分级；原实现形态的版本边界见卡前固定链接。
```

## Part 3 收口提示
1. 卡8「周期表导入」的两步读法、目标物种与缺值护栏按[卡8](#template-list)；实现线逐项对表任务及原冻结批次状态的证据范围见[问题台账](OPEN-ITEMS.md#template-import-implementation-evidence)。
2. 五卡与批次①卡1 的交界：EXTRACT_TEMPLATE 动作在卡1（发起处）与卡8（工作区入口）各出现一次，是同一动作两个入口，不是两个动作；
3. 本次候选正文／确认、C11与N2的承载分工及共用验收统一见[共享N2](#rebase-impact-preview)；卡10／11保留各自独有编辑对象与写集。

---

### `RoleControl`｜Policy Role / fail_env_coeff

<a id="role-control"></a>
**机制入口**：[汇编 §9](component-contract-consolidated.md#role-record-intent) 定义 raw Role 与记录态，[§10](component-contract-consolidated.md#policy-clear) 定义 Policy CLEAR / 词表，[§11](component-contract-consolidated.md#profile-lifecycle) 定义 Role × Profile 校验。V1 产品投影按“一兼容 Mode = 一条既有 FishEnvAffinity 行”收敛。

```
Component: Policy Focus Editor｜四个 Role + fail_env_coeff
Reads:
  - Policy Authoring Truth：四个 Effective Role、各自当前 Authoring Intent、必要 provenance、fail_env_coeff。
  - Component Card 只读取对应 Effective Role 形成只读 badge；不拥有 Role mutation。
  - Species Context 读取 Policy Template raw values + Species Policy Recipe。
  - Compat Mode 读取 Species Effective Policy + 当前单条 FishEnvAffinity row patch。
Actions:
  - **Species Role**：沿用策略模板 / 设置为 CORE / SECONDARY / IGNORED。
  - **Mode Role**：沿用基础习性角色 / 使用策略模板原始角色 / 设置为 CORE / SECONDARY / IGNORED。
  - **Species fail_env_coeff**：沿用策略模板值 / 调整 / 设置为。
  - **Mode fail_env_coeff**：沿用基础习性配置 / 使用策略模板原始值 / 调整 / 设置为。
  - 所有 Role / fail_env_coeff ordinary edits 走 autosave；不因 Role 变化自动创建、删除或改写 Profile。
Durable mutation:
  - Role / fail_env_coeff durable truth 仍在 Policy 域，Component Card 不另建 state。
  - Species：Species Policy Recipe 持有四个 Role op 与 fail_env_coeff op。
  - Mode：AffinityRolePatch key=(row_key, component)，op=CLEAR|SET；AffinityFailEnvCoeffPatch key=row_key，op=CLEAR|ADD|SET。
  - 行级 patch 仍显式携 op，不从 Effective Value 反推记录。
Acceptance:
  - INHERIT/absent 与 same-value SET 必须可区分；CLEAR 与 absent 必须可区分。
  - IGNORED + Profile absent → 改 CORE/SECONDARY：先保存 Role，随后产生 required-Profile ERROR 并阻断 Publish；不自动建 Profile、不自动选 Source、不回滚 Role。
  - CORE/SECONDARY → IGNORED：已有 Profile 保留，可继续编辑。
  - V1 Compat Mode 只对应一条既有 FishEnvAffinity 行；更新当前 Mode Policy 不广播到其它 Mode。
Must show:
  - Policy Focus Editor 统一显示 Effective Role + Authoring Intent + 必要 provenance。
  - Species / Mode Context 由当前 Subject breadcrumb 决定；普通 UI 不要求作者看到 row_key、Quality 或 production row 名。
  - Component Card 可显示 Effective Role 的只读 badge，用于 Overview 扫描。
Must not:
  - Component Card 不提供 Role dropdown / toggle。
  - 不保留 multi-row Compat 的 Role 聚合、production-row 展开或跨行批量编辑。
  - 不给 Component Card 建 durable Role state。
  - Role 永不允许 ADD。
依据: durable tokens / keys 见持久层契约与汇编 §9–§11；V1 mutation surface ownership 见 V1 Product Current。
```

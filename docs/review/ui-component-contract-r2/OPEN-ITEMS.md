# OPEN-ITEMS — 审之前先读这个

**用途**：本审阅包唯一的可变问题台账：记录处置、剩余工作与关闭依据。README／开发 brief 只导航；[图像登记](figma-current.md#image-evidence)负责画面事实、版本与指纹。**产品真相来自 Notion Current／Owner 裁定；图像只能证明所拍状态；审查关闭必须引用对应 exact head 的独立 REVIEW。** 本台账不新增产品权威，也不以“已裁／已投影”替代复审结论。

<a id="active-review-items"></a>
## 1. 当前审查项与证据

本表按 [#7 最新有效 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/7#issuecomment-5758470596)（**`ca17a2306b3c567e6fe7bc2eedcc6ed43ed3a2e5`，`APPROVE`**）登记：该 head 的设计／契约投影审查通过，ADJ-03 与 CXR7-SOURCE-SYNC-01 两项关闭。此前 `1409a13…` 的 `REQUEST_CHANGES` 由该轮完整增量复审更新。**此批准不等于下游实现通过，也不自动批准本分支的状态去重新改动。**

<a id="species-role-ui"></a>
### Species Role UI：操作入口与记录态分别验收

| 项 | 处置及可核证据 | 剩余工作／关闭依据 |
|---|---|---|
| `CXR-ROLE-UI-01` 操作入口 | 作者的 `[04]` 记录描述物种侧两枚独立操作 chip；随包整帧也能看到。它回答“能否选择 operation”，不单独证明记录态。 | [#7 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/7#issuecomment-5757267260) @ `7438477536aa695955b966de1040b11aa8a11ab1` 已确认 `[04]` 解决操作入口问题；保留该确认，不重开入口修复，也不能借它关闭下一行的记录态问题。 |
| **`ADJ-03`：CLOSED（设计形态／语义映射／随包证据）** | SET 与 INHERIT 局部图水温 Role 同为 CORE，但前者有“Role 已钉住”、后者无；新版 SET 局部与整帧一致。版本／指纹见[图像登记](figma-current.md#image-evidence)。 | 关闭依据：[#7 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/7#issuecomment-5758470596) @ `ca17a2306b3c567e6fe7bc2eedcc6ed43ed3a2e5`。物种层持久化读写往返仍未实测，属实现侧验证，不作为重新挂开设计包的额外门禁。 |

**ADJ-03 的依据与射程**：

- **产品裁定**沿用 §2 ADJ-03 的出处：由 Species Role durable op record 是否存在派生状态位；无记录不显示、有记录（包括同 raw 值 SET）显示“Role 已钉住”，不增加第二份 durable UI state。卡2 是记录意图的执行投影，**不把裁定原句冒称卡2 的逐字引文**。
- **实现旁证**仅转述[前轮独立 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/7#issuecomment-5757933398)对实现仓 `84e2221` 的亲读：物种 `policyRecipe` 与行级 `rules` 是两条 lane，`isRoleExpressed` 检查物种角色键存在性；`durableRolesOf` 输出角色值，测试里的 clear／absent 同值对照针对**行级 patch**。这些不能独自替代 Species INHERIT 与同 raw 值 SET 的记录态／显示证据。作者登记 `species[].policyRecipe.roles` 的读写往返尚未实测；本批及该轮 reviewer 均未运行下游实现。实现验证另归实现侧，不把实现仓整体完成设为本设计投影的前置。
- **图片证据**只按实际文件判读；上述 #7 REVIEW 已亲核两态图片与语义映射，但未将其当成实现运行结果。后续 INHERIT 1×替换由 [#17 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/17#issuecomment-5758641670) @ `8d4523c0372c12cbf1aad14ec652159c2782e5ad` 独立批准，现已进入 main；实际版本与指纹只在图像登记维护。本次与新 main 的兼容提交按 Owner 于 2026-09-21 的明确决定跳过增量复审并直接合并；这不构成独立审核通过，也不继承 #17 或本分支旧 head 的批准。后续新增或替换 Role 图只更新[图像登记](figma-current.md#image-evidence)及本条处置／剩余工作；README 与 brief 不复制状态。

<a id="source-sync"></a>
### `CXR7-SOURCE-SYNC-01`：CLOSED（来源状态投影）

旧审查在 `1409a13…` 指出顶部时段来源“未选”、卡内 `period_Largemouth_Bass` 与“未配（空态）”并存。作者提交 `ef2a0c0c…` 将卡内来源改为“未选”并重导；新整帧两入口均为“未选”，摘要“未配（空态）”。**关闭依据**：[#7 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/7#issuecomment-5758470596) @ `ca17a2306b3c567e6fe7bc2eedcc6ed43ed3a2e5` 亲核 live Figma、随包图与 RGB 像素差，确认该项关闭。本批只亲看图片、登记该裁决，未重测实时交互。产品规则仍见[汇编 §7](component-contract-consolidated.md#7-组件卡--焦点编辑栏)及[画布摘要 §七](figma-current.md#source-entry-evidence)。

<a id="packet-consistency"></a>
### 包内自洽／物证卫生

上述 #7 REVIEW 已按设计／契约投影范围批准 `ca17a230…`；README 的旧“未落地／四张”摘要被明确列为**非阻塞的状态去重余项**，由本批处理。**本批处置**：删除重复摘要，保留真实图证据及实现未核边界；本分支新 head 仍须独立复审，不继承 #7 的 APPROVE。后续记录关闭依据时须写受审完整 SHA 与 REVIEW 链接。

[PR #14 的 APPROVE](https://github.com/futouyiba/HitFish-Up/pull/14#issuecomment-5758212127) 仅适用 `842f13029b1adb03eab6cfe52f5cfda2b8250702` 的 CLEAR 引用净改动，不关闭 #7 全包或 #10 原 head 的 findings。

### 历史语义处置（固定来源）

以下八簇是 [#7 固定版本的原登记](https://github.com/futouyiba/HitFish-Up/blob/1409a13fde46dcb8d10bae039c26f6a0090bf497/docs/review/ui-component-contract-r2/OPEN-ITEMS.md)，保留其语义与处置背景；未补造当时的独立 REVIEW 链接，不能把这份历史登记扩写成本分支的批准。

#### 原登记的八个语义簇

| 簇 | 内容 |
|---|---|
| 操作存储 / 解析 / 显示 | 一条 op 存在哪一层、`INHERIT`/`absent`/`CLEAR`/`ADD` 怎么解 |
| 影响面数字需要候选与前后文 | 「被 SET 盖住、最终值未变」不能只读当前态 |
| 高影响动作边界 | `candidate → Preview → 显式确认 → 原子提交` |
| **压层**（per-layer 规则被写成层无关的一句） | 最典型：把桶层语言暴露给物种层 |
| 温度参数的类型与 ADD 可达性 | 5 个数值项 ＋ 1 个枚举项（`falloff_shape`）；枚举不得 ADD |
| 来源入口拓扑 | 「卡 ＋ 焦点编辑栏」双入口 vs 「顶行 ＋ 卡」—— **已按「顶行 ＋ 卡」修订**（前层 Source Selector 在顶部 `templateRow` 每组件一个 ＋ 组件卡的来源 / Source 下拉）；**焦点编辑栏不提供 Source 下拉** —— 那是被否掉的那一侧（再放一个就成了「顶行 ＋ 卡 ＋ 焦点编辑栏」三个 mutation surface，**复杂度没有买到新能力**）。⚠️ **本行先前误写「已按前者」，方向写反了 —— 2026-09-21 更正** |
| 组件命名 / 稳定标识纪律 | 16 个组件名的命名与页面出处 |
| 评审包范围与忠实性 | 两份输入的 reviewable snapshot |

---

## 2. Owner 裁决索引（产品依据，不代表审查关闭）

本节保留固定来源中的十三项裁决及投影定位。`PROJECTED IN` 是出处检查，不能证明图片齐全、实现完成或独立复审通过；Species Role UI 的处置统一见[当前审查项](#species-role-ui)。

★ **留痕（一度 X ＋ 收口 Y）**：**一度**「卡8 的 Temperature Concrete Import 缺值策略**三选一未裁** ⇒ 该子情形按**未冻结**读」（登记来源：独立复审在 `fa96900` 上报出「卡8 自称未冻结，而 README／OPEN-ITEMS 说『零项待裁』」这处不一致）→ **收口（Owner 2026-09-21 裁）**：**取「按既定口径推导」，三选一已关闭** ⇒ **该子情形不再是未冻结**；规则逐字见 `contract-cards.md` 卡8（含「**不得保留旧 `accept`**」与其理由）。

**已裁（记终局，不记两侧各半）**：

| ID | 裁定 | `PROJECTED IN`（**执行投影落在哪**） |
|---|---|---|
| **ADJ-01** | durable schema 的 canonical 实现 ＝ **TS 编辑器仓**（另一侧的原型不承担本契约） | —（**实现侧事实，本包不投影**） |
| **ADJ-02** | Profile 缺席矩阵 ＝ **统一**：缺席合法性**只由 `Role` 决定**；**时段不特权** | `contract-cards.md` **`A①-卡2` Reads**；`component-contract-consolidated.md` **§11 ＋ §12** |
| **ADJ-03** | 物种层 Role：`INHERIT` **需要一个与三值可区分的形**；**选中等于 raw Role 的值一律写 `SET`（钉住）** | `contract-cards.md` **`A①-卡2` Durable mutation**（同值 `SET` 仍留记录）；[记录态证据与剩余工作](#species-role-ui) |
| **ADJ-04** | §3.1 的四个组件字段 **就是** Component Recipes（Source ＋ 逐字段 op） | `contract-cards.md` **`RoleControl` Durable mutation**（`component recipes`） |
| **ADJ-05** | `sourceOverride` ＝ **组件级独立 durable 绑定**（不是 §3.3 那张逐项记录上的字段） | `contract-cards.md` **`A①-卡1`／`RoleControl`**；`component-contract-consolidated.md` **§3** |
| **ADJ-06** | owner 粒度 ＝ **（物种, 桶）** | `contract-cards.md` **`RoleControl`**；`component-contract-consolidated.md` **§9** |
| **ADJ-07** | Policy Template 的 raw Role 默认值 ＝ **`CORE`** | `contract-cards.md` **`RoleControl` Reads**；`component-contract-consolidated.md` **§11** |
| **ADJ-08** | ★ **`C_SPLIT_REGISTERS`：Semantic Concept ≠ Durable Identity**（Owner 2026-09-21 refine；**取代**先前那个「owner ＝ `Engagement Mode`」的读法）—— `Engagement Mode`／中鱼习性模式 是 **Simplified Production V0 的正式业务概念**；**B P0 不物化独立的 `EngagementMode` durable／runtime identity**，也不实现 Mode Share／Routing；**物理 durable key ＝ `FishEnvAffinityRef`**，`FishEngagementModeCompat` 是**对它的 mode-like authoring projection／兼容壳**；**桶是数据迁移期的行单位表达**。★ **要消灭的是「owner」这个模糊中间词**：`sourceOverride` 写作 **`(fishEnvAffinityRef, component)`**（若 schema 字段名为 `owner_ref`，则 **`owner_ref := FishEnvAffinityRef`**）。 | `component-contract-consolidated.md` **§16（含射程说明）**；**页侧：CT §1.1 ／ CT §3.3 ／ RS §11.1（本轮落）** |

**已裁（续）**：

| ID | 裁定 | `PROJECTED IN` |
|---|---|---|
| **ADJ-09** | **C_NARROW，已裁并投影**；记录页 §392。原登记将 staged confirm 与 full high-impact 混成一轴的判断已撤回，不重新派单。 | [汇编 §8 完整机制](component-contract-consolidated.md#source-transaction)、[§15 事务分类](component-contract-consolidated.md#transaction-model)、[卡1交互／验收](contract-cards.md#source-selector)；原裁定转录见下方固定历史边界。 |
| **ADJ-10** | 顶栏该动作的作者可见词 ＝ **「丢弃未保存的改动」**；**`Reset` 不得作作者可见词**（**这是命名裁定，不是页内相抵** —— 见 §6） | —（**作者可见词，落在页与画布；本包不投影**） |
| **ADJ-11** | **A_NARROW** —— **空底板那一支：**当某组件的 Authoring Profile / Species Base **为空**、**且**该组件的 **Effective Role ＝ `IGNORED`** 时：**不产生该组件的 production projection、不创建显式空 Profile、不因这一点阻断 Publish**；但 **`FishEnvAffinity` 主行与该组件的 `Role = IGNORED` 仍正常写回**，**只是不生成/写回该组件的完整 Profile 子表值**；尚未产生生产 Profile 的对象 **`ProductionRowLedger.refs[component]` 保持空**。★ **「空」＝尚无该组件的 production projection，不是一种新的 Runtime Profile 值** —— **不是**把 `null`/`empty` 发下去，而是**该组件因 `IGNORED` 根本不进入 evaluator**。 | `component-contract-consolidated.md` **§11** |
| **ADJ-12** | **四组件都必须有 reachable Setup path——P0 可用性缺口，能力已 CLOSED**：`Profile absent → 显式 Setup／配置档案 → 选择合法 Source／建立可 Resolve 的 Profile`。★ **不得自动生成 `1.00` Profile** —— ★ **`Role promotion ≠ Profile creation`**：「提角色」这个动作**本身不造数**；`IGNORED → CORE / SECONDARY` **不自动建 Profile、也不补一份全 `1.00`**。★ **旧「提角色时自动补一份行为中立档案」的规则按 `superseded` 处理**（Owner 2026-09-21）；本行此前写「提角色那条补档案规则**仍在**」与本包 `contract-cards.md` 的 `RoleControl`（`B1a`/`B1b`）**相抵**，已按后者更正（独立复审在 `fa96900` 上报出）。**TimePeriod 保持 Setup 能力；三种预设只是 Setup 后/中的一次性填表便利，不得被定义成 TimePeriod 独有的「Profile 创建语义」**。**UI exact shape 归 Species Role/UI 工作流**（见 §5）。 | `contract-cards.md` **`RoleControl` Reads** |
| **ADJ-13** | **TimePeriod Preset 的 target layer ＝ 作者当前所在的 authoring layer**：`Apply TimePeriod Preset → write five SET operations → target = current authoring layer / owner`。**不切换 authoring layer／不默认提升到 Species／不创建第三个 preset layer／不改 Source／不持久化 `presetId`／五个 `SET` 作为一个 atomic batch**。★ 若某 UI surface 本版只开放 Species authoring ⇒ 在那里自然只写 Species，**那是 surface capability 的后果，不是 Preset 自身拥有 Species 语义**。 | `component-contract-consolidated.md` **§12** |

★ **`PROJECTED IN` 是一栏检查，不是一个记录** —— **加一条 ADJ 的动作里包含「把这一栏填满」，空栏 ＝ 那条还没落投影。**
理由（本族实测）：**「登记册」与「执行投影」之间原本没有一致性检查**，所以每加一条裁定就会漏 N 处投影、而由下游逐条抓出来 —— 实测三条：**ADJ-02 落在卡上而汇编里没有**、**ADJ-09 的两档在卡与汇编里都没投**、**ADJ-07 的 `CORE` 默认只在登记册**。⇒ **判据：一条 ADJ 的「已裁」与「已投」是两件事；只有 `PROJECTED IN` 全非空才算落完。**

**十三项的裁决留痕**：ADJ-01～05 ＝ §374／§377；**ADJ-06／ADJ-07 ＝ §383**（ADJ-07 的后果一/二/三也在此节）；**ADJ-08 ＝ §385**；**ADJ-09 ＝ §392**；**ADJ-10 ＝ §393**（★ 该节把它写成「页内相抵」，**定性已作废**，收口见 `deltas`）；**ADJ-11 ＝ 已落 Current** —— 《编辑器持久层契约》**§3.7「展开的第三条臂（组件级）」** 逐字存在（页 Version **16** / `Last Updated 2026-09-21 14:34`），**该节是它的 canonical owner**（2026-09-21 回读）；**ADJ-12 ＝ 本包 `contract-cards.md` 的 `RoleControl`**；**ADJ-13 ＝ 本包 `component-contract-consolidated.md` §12**。★ **前十一项**的这些节是它们在**记录页**的**唯一可引用落点**；**ADJ-12／ADJ-13 的落点在本包（如上），记录页节号未在此登记** —— 本表的 ID 只是索引。

## 3. 其他登记项（保留原取证边界）

- **无页面出处的 UI 细则**：卡上「本层操作数 / 诊断数 / profile presence / source health」四个展示项；结构编辑面的筛选；「组件卡不做 mini heatmap / 不展开完整字段 provenance / 不做操作历史时间线」三条负向。—— 页面上只列了摘要、模板选择器、Role 角标、继承/覆盖状态。
- **两处口径不一致**：影响面数字「三项 vs 四项」（**四项那一侧有页面依据**）；「25 个 Structure slot」只在一处出现（**UI 不固化字段数**）。
- **~~一条覆盖缺口~~ ⇒ ★ 已闭（`ADJ-11 ＝ A_NARROW`，见 §6）**：`§3.7` 的展开算法原**只分「有数值覆盖 → 取覆盖值」／「否则 → 取底板值」两支**，**没有「底板该组件为空」那一支** —— 而契约别处明确承认那个状态。**★ 现状：第三条展开臂已落**（《编辑器持久层契约》§3.7），**本条保留作留痕**。⚠️ **先前本行写「一条覆盖缺口」而 §6 写「已闭」—— 同一份文件两处相抵**，2026-09-21 按 §6 更正。

---

## 4. 看着像缺陷、其实**是有意的** —— 请不要报

1. **容器高度未改**：控制条内容到 y=121、容器高 122，**紧贴下缘**。已登记——加高会吃掉与下方块的 12px。
2. **物种层没有 `CLEAR`**：层面结构限制，不是漏做。
3. **「沿用物种操作」是缺省名，`沿用物种调整`/`沿用物种设置为` 属「行内显示」层**：**名字 ≠ 显示**，两者不矛盾；**不得合并成「恢复」**。
4. **卡侧只显示物种层**：桶层的三个操作只在 Policy 控制条里作选项。
5. **Role 角标保留角色色**（不做成白场）：已裁——**角色色是「非常重要信息」**。
6. **图上标「示意 / 空态」不是缺陷**：那是**不声称它存在**的记号；`类型名（示意）` 是占位。

---

## 5. 契约读数与能力裁定（沿用固定来源）

下表的 `CLOSED` 仅表示原登记的契约读数／能力裁定已回答，不代表实现、图证据或本分支审查已关。不得据此宣告整个 Persistence 完成。

| 子项 | 状态 | 依据 / 剩什么 |
|---|---|---|
| **Component Recipe Shape** | **CLOSED** | 读数已裁（§3.1 的四个组件字段**就是** Component Recipes：Source ＋ 逐字段 op）；逐字已交写入者 |
| **Affinity Role Patch** | **CLOSED** | §3.4 逐字齐：`(row_key, component)`、op `CLEAR|SET`、`SET` 携 `role`、`INHERIT` ＝ 无记录 |
| **Affinity Fail Env Coeff Patch** | **CLOSED** | §3.4 逐字齐：`row_key`、op `CLEAR|ADD|SET`、越界报错不 clamp |
| **Species Policy Recipe** | **CLOSED（读数）** | §3.1 记录里逐字有 `policy_source_binding`；**但它的指称物（第五类 `TemplateKind`）在实现里不存在** ⇒ 那是**实现缺口**，不是形状未定 |
| **Affinity Source Override** | **CLOSED** | 读数已裁（**组件级独立绑定**）；★ **两层必须分开**：**authoring 粒度 ＝（物种, 桶）**（ADJ-06）；**物理 durable key ＝ `FishEnvAffinityRef`**（ADJ-08 ＝ `C_SPLIT_REGISTERS`）；**`Engagement Mode` 只是业务概念、不是 durable identity**。 |
| **Profile Presence** | **CLOSED** | 矩阵已裁（**统一**：缺席合法性只由 `Role` 决定，时段不特权）；**默认值已裁 ＝ `CORE`** |
| **Species Role UI** | [当前审查项](#species-role-ui) | 操作入口、记录态分别验收；此处不复制动态状态。 |
| **Follow / Pin 语义** | **CLOSED** | ⚠️ **先前这里写「相抵」，已撤回**：回原页核完，**它是已定的、只是没落到 picker 那一处** —— §3.3 逐字「无 `sourceOverride` ＝ 跟随」＋ §3.5 表「覆盖→不跟随／恢复为底板→跟随」⇒ **跟随 ＝ 没有那条记录**，故「跟随物种」**＝ 删除** `sourceOverride`（**不写同源记录**）。落页已派 |
| **Source Transaction** | **CLOSED** | ADJ-09 射程已裁；机制与交互沿 §2 该行的投影入口。旧“两条耐久规则相抵”判断已撤回，完整原文仅按下方固定历史读取；不以本能力状态代替实现验收。 |
| **TimePeriod Transaction** | **CLOSED** | 原三项裁定已收：target／同层 atomic batch 见[汇编 §12](component-contract-consolidated.md#component-specifics)，覆盖确认的完整规则见[§15 Batch Overwrite Guard](component-contract-consolidated.md#timeperiod-batch-guard)，不从 ADJ-09 推导。`预设` 的四个指称物须分别写、不合并，属 terminology hygiene，不因此重开本能力项；原裁定转录沿下方固定历史读取。 |

**Source／TimePeriod 事务历史边界**：本表 ADJ-09 与两项能力结论沿用[本批基线的裁定转录](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#5-契约读数与能力裁定沿用固定来源)及其 §2 ADJ-09／记录页 §392 出处。它们保留原处置和取证时点；本次整理不重审实时 Owner 记录、不宣告实现完成。完整规则由上述仓内投影承接，不在台账重复维护。

<a id="other-material-items"></a>
## 6. 材料侧登记与固定处置背景

- **`§3.7` 的展开算法少一支** ⇒ **★ 已闭（ADJ-11 ＝ A_NARROW）**：它原来只分「有数值覆盖 → 取覆盖值」／「否则 → 取底板值」，**没有「底板该组件为空」那一支**。⇒ **现在补上**：`底板为空` **且** `Effective Role ＝ IGNORED` ⇒ **不产生该组件的 production projection、不创建显式空 Profile、不因这一点阻断 Publish**（主行与该组件的 `Role = IGNORED` 仍正常写回；`ProductionRowLedger.refs[component]` 保持空）。**投影落在汇编 §11。**
  - ★ **保留这条作留痕**（它一度是一个缺口）；**不移除**。
- **链接图指向副本而非 owner**：《主开发需求》§3.0 把作者分层诸事实链到《编辑器与 Resolve》§11 与《Editor → Persistence》，而它们的 canonical owner 是《编辑器持久层契约》§3.3。
- ★ **跨页重复定义 —— 「超过 60 处／已盘出」这句已撤回（2026-09-21）**：**我无法证实那个数**（**没有清单、没有出处**；全族只在我写的那一句里出现过），而写入者用**两个独立探测器**复现：**句级恒等**命中 10 条（其中 7 条是噪声：`<table header-row="true">`、`**Last Updated:**` 行、单 `<td>`、mermaid 边）／**字符 30-gram 重合**（扩到 8 页、剥掉 URL 与块标记）**真内容只有 3 条** ⇒ ★ **机械口径下全族只有 3 处**。
  ⇒ ★ **判据**：**一个不可证实的数不该驱动一项机械工作**；而且**这一句「已盘出」正是本族禁的那类断言 —— 它让下游放弃追查**。（本族同族条：[[corrections-need-evidence]]、[[intent-claims-need-authority]]。）
  - **收口（机械口径的 3 处）**：**D1**「激活后未生成期间须呈现可见校验态」—— **定义处唯一在《编辑器界面》§1.4**，另两处是**指回** ⇒ **合判据，保留**｜**D2**「三种时段预设只是一次性填表便利」—— **两处各由一条已裁动作明令在位** ⇒ **保留两处 ＋ 各加一句互指**｜**D3**「Role 三态切换显示 change notice；无额外 Gate 状态需同步」—— **真重复**，**归属裁为《编辑器条件开关》**（RS §2.3 **自述**「Gate 的业务判据和失败分支不在本页重复定义」⇒ 它不是该类的 owner）⇒ **RS §2.3 改指回**。
  - ★ **判据仍是 `competing normative owner = 0`**（每个事实**恰好一个定义处**），**不是「某字符串 occurrence = 0」**。
  - ★ **那三组「明确不许合并」仍然有效**（物种层 `INHERIT` vs 桶层 `absent`／物种层 Role 默认 vs `AffinityRolePatch`／「同值」vs「同意图」）—— 它们**不在上面 3 处里**，是**另一层（不许合并）的护栏**，**独立于本条生效**。
- ★ **ADJ-08 已由 Owner 收口为 `C_SPLIT_REGISTERS`（本轮落页）** —— 曾经的问题是**「owner」这个词同时被用来指「业务语义归属」和「物理 durable identity」**，于是同一页上既出现「patch owner ＝ `Engagement Mode`」又出现「durable owner ＝ `FishEnvAffinityRef`」。
  - ★ **现在消灭的是那个模糊的中间词**：**物理 durable key ＝ `FishEnvAffinityRef`**；`Engagement Mode` 只是**正式业务概念**；`FishEngagementModeCompat` 是**对 Affinity 的兼容壳／投影**；Runtime 仍**无独立 `EngagementMode` identity**。
  - ⚠️ **UI §5 ／ RS §7 ／ IA §8 不动** —— 它们写的是 **Runtime 域**那句，**与本次收口相容**。
  - ⚠️ **本包 §16 只作射程说明与标注**；页侧本轮 delta 的逐字见**仓外/本地工作件**（**不在本包**）。
- ★ **顶栏动作名 `Reset` ＝ 一条命名裁定，不是「页内相抵」**（**已落页**，UI §9.1 ⇒「丢弃未保存的改动」，Version 12→13）：★ **《编辑器界面》§1.2 并没有禁 `Reset` 的句子** —— 回读实测（**2026-09-21 12:40 之后**）**该页全页 `Reset` = 0、`Override` = 0、「不向作者暴露」= 0、「工程词」= 0**；§1.2 给的是**操作 → 用户语言的映射**（`CLEAR` ⇒「仅使用当前来源」）。⇒ **「不能叫 `Reset`」的依据在裁定侧、不在页上**；**替换词＝「丢弃未保存的改动」**（判据见 `component-contract-consolidated.md` §4 的出处校正）。**不必再报。**
  - ⚠️ ★ **那个「全页 = 0」必须带时点锚**：它是 **12:40 那笔落页之后**的读数，**不是「页上从来没有过」** —— 该页 §9.1 在此之前**逐字就是** `` `Reset` / `Publish` / `导出` / `Bass 预设` ``，**画布上那个 `Reset` 不是凭空来的**。⇒ **状态断言不带时点/版本锚，会被读成「从来没存在过」。**（这条是画布侧提出、我采的。）
- **作者词汇的旧派单记录**：[原版本](https://github.com/futouyiba/HitFish-Up/blob/1409a13fde46dcb8d10bae039c26f6a0090bf497/docs/review/ui-component-contract-r2/OPEN-ITEMS.md) 曾要求顶行、LocalOp、Policy chip 和 Reset 的作者可见串修正。随包整帧可见“来源 / Source”“仅使用来源”“丢弃未保存的改动”等修正，旧“已派、一次重导”不再作为当前工作清单。最新 #7 REVIEW 保持原 IMPORT／OP／DISCARD 修复关闭；Source **值**修复与复核进展见[当前项](#source-sync)。作者面／投影面的词汇分工见 `figma-current.md` §四，态10 的契约令牌括注不因本次整理变为缺陷。
- **卡10／卡11 投影**：原登记为等实现后再投，本批未核实现或实时画布；后续补充时登记真实版本与物证，不因文字清理视为完成。
- ★ **契约名 ↔ 实现名 的对照（已核两侧逐字，**不是**竞争权威）**：
  | 契约侧（《编辑器持久层契约》） | 实现侧（编辑器仓） | 判定 |
  |---|---|---|
  | **`ProductionRowLedger`** —— §3.4 逐字用它，并自述「**`ProductionRowLedger` ＝ §3.2 的生产行记录**」；出现在 `ProductionRowLedger[row_key].species_key` 那句不变量里 | **`ProductionRows`**（映射）／**`ProductionRowRecord`**（一条记录），`src/data/derived.ts:36/51` | **同一对象、两侧名字不同**。⇒ **裁定：不改名**（契约名是契约层的概念名、实现名是实现的类型名，**没有任何一处自定义**；改名的收益只是「看起来一致」，代价是 4 个文件的无行为变更 —— **无谓改动会污染基线**） |
  | **`refs`** | `ProductionRowRecord.refs: Partial<Record<ProfileField, number \| string \| null>>`，**键空间就是四个组件** | **同名、同形** ✓ |

  ⇒ ★ **登记它的理由**：不登记，下一个人会以为是**两个东西**。**读本包的人按契约名找实现时，请用右边那一列。**

---

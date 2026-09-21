# OPEN-ITEMS — 审之前先读这个

**用途**：免得把**已经裁过的**当缺口重报（旧容器里这占了大量返工）。**六节：已关 ／ 待 Owner 裁 ／ 登记在册 ／ 有意如此 ／ 细粒度结项表 ／ 材料侧已报出但不要你判的。**

---

## 1. 已裁 / 已关 —— **请不要重报**

上游那轮复审共提出 **11 个语义簇**。**现在没有一个仍以「缺陷」形态开着**，但**两类状态要分清**：

### (a) 复审已明确关闭（**8 簇**，每一轮都确认过）

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

（**另有三簇** —— **Role**、**包内自洽**、**包的物证卫生** —— 见 (b)。⇒ 8 ＋ 3 ＝ **11**，与本节开头的「11 个语义簇」对得上。）

### (b) 处置已在树上，但**本 head 上还没有复审裁决**（**作者方执行，不等于复审已关**）

| 簇 | 处置 | 状态 |
|---|---|---|
| **Role：物种默认 vs 行覆盖、op 词表、durable 形状、其投影** | 图上把两个作用域分成两组＋两条分隔线；物种组补上它自己的两个可用操作 | **执行完毕，待复审** |
| **包内自洽**（执行状态 / 未决台账 / 修订残留） | 卡 2 依既有裁定「落到页后即恢复」**恢复为已冻结**；批次①读作七张 | **执行完毕，待复审** |
| **包的物证卫生**（图 / 字节 / 现状摘要漂移） | 现状摘要四处陈旧已 sweep；新增一节把控制条现状作为唯一现行表述 | **执行完毕，待复审** |

⇒ **请把这三行当「待你确认」而不是「已解决」**：它们**在树上**，但**没有人在本 head 上判过**。

---

## 2. Owner 裁决状态 —— **十三项已裁，零项待裁**

**已裁（记终局，不记两侧各半）**：

| ID | 裁定 | `PROJECTED IN`（**执行投影落在哪**） |
|---|---|---|
| **ADJ-01** | durable schema 的 canonical 实现 ＝ **TS 编辑器仓**（另一侧的原型不承担本契约） | —（**实现侧事实，本包不投影**） |
| **ADJ-02** | Profile 缺席矩阵 ＝ **统一**：缺席合法性**只由 `Role` 决定**；**时段不特权** | `contract-cards.md` **`A①-卡2` Reads**；`component-contract-consolidated.md` **§11 ＋ §12** |
| **ADJ-03** | 物种层 Role：`INHERIT` **需要一个与三值可区分的形**；**选中等于 raw Role 的值一律写 `SET`（钉住）** | `contract-cards.md` **`A①-卡2` Durable mutation**（同值 `SET` 仍留记录）；**「形」仍未设计 ⇒ 见 §5** |
| **ADJ-04** | §3.1 的四个组件字段 **就是** Component Recipes（Source ＋ 逐字段 op） | `contract-cards.md` **`RoleControl` Durable mutation**（`component recipes`） |
| **ADJ-05** | `sourceOverride` ＝ **组件级独立 durable 绑定**（不是 §3.3 那张逐项记录上的字段） | `contract-cards.md` **`A①-卡1`／`RoleControl`**；`component-contract-consolidated.md` **§3** |
| **ADJ-06** | owner 粒度 ＝ **（物种, 桶）** | `contract-cards.md` **`RoleControl`**；`component-contract-consolidated.md` **§9** |
| **ADJ-07** | Policy Template 的 raw Role 默认值 ＝ **`CORE`** | `contract-cards.md` **`RoleControl` Reads**；`component-contract-consolidated.md` **§11** |
| **ADJ-08** | owner 身份 ＝ **「中鱼习性模式」（`Engagement Mode`）**；**桶是数据迁移期的行单位表达** | `component-contract-consolidated.md` **§16（含射程说明）**；**页侧 CT §3.3 已落／RS §11.1 待**（见 §6） |

**已裁（续）**：

| ID | 裁定 | `PROJECTED IN` |
|---|---|---|
| **ADJ-09** | **C_NARROW** —— **Source mutation 一律 staged、不分类别**；**Local Rebase Preview** 与 **Propagated Impact Preview** 两档按 **fan-out** 分级（不是按「点了几个控件」）。★ **核心不变量：「是否需要 staged confirm」≠「是否属于 full high-impact mutation」** —— 影响面只决定 Preview 有多重，不决定能不能先写盘。事务模型**只有两层**，不新增第三种 | `contract-cards.md` **`A①-卡1` Actions**；`component-contract-consolidated.md` **§8 ＋ §15** |
| **ADJ-10** | 顶栏该动作的作者可见词 ＝ **「丢弃未保存的改动」**；**`Reset` 不得作作者可见词**（**这是命名裁定，不是页内相抵** —— 见 §6） | —（**作者可见词，落在页与画布；本包不投影**） |
| **ADJ-11** | **A_NARROW** —— **空底板那一支：**当某组件的 Authoring Profile / Species Base **为空**、**且**该组件的 **Effective Role ＝ `IGNORED`** 时：**不产生该组件的 production projection、不创建显式空 Profile、不因这一点阻断 Publish**；但 **`FishEnvAffinity` 主行与该组件的 `Role = IGNORED` 仍正常写回**，**只是不生成/写回该组件的完整 Profile 子表值**；尚未产生生产 Profile 的对象 **`ProductionRowLedger.refs[component]` 保持空**。★ **「空」＝尚无该组件的 production projection，不是一种新的 Runtime Profile 值** —— **不是**把 `null`/`empty` 发下去，而是**该组件因 `IGNORED` 根本不进入 evaluator**。 | `component-contract-consolidated.md` **§11** |
| **ADJ-12** | **四组件都必须有 reachable Setup path——P0 可用性缺口，能力已 CLOSED**：`Profile absent → 显式 Setup／配置档案 → 选择合法 Source／建立可 Resolve 的 Profile`。★ **不得自动生成 `1.00` Profile** —— 提角色那条补档案规则**仍在**，但**不得反过来变成「所有新对象出生时自动生成默认 Profile」**。**TimePeriod 保持 Setup 能力；三种预设只是 Setup 后/中的一次性填表便利，不得被定义成 TimePeriod 独有的「Profile 创建语义」**。**UI exact shape 归 Species Role/UI 工作流**（见 §5）。 | `contract-cards.md` **`RoleControl` Reads** |
| **ADJ-13** | **TimePeriod Preset 的 target layer ＝ 作者当前所在的 authoring layer**：`Apply TimePeriod Preset → write five SET operations → target = current authoring layer / owner`。**不切换 authoring layer／不默认提升到 Species／不创建第三个 preset layer／不改 Source／不持久化 `presetId`／五个 `SET` 作为一个 atomic batch**。★ 若某 UI surface 本版只开放 Species authoring ⇒ 在那里自然只写 Species，**那是 surface capability 的后果，不是 Preset 自身拥有 Species 语义**。 | `component-contract-consolidated.md` **§12** |

★ **`PROJECTED IN` 是一栏检查，不是一个记录** —— **加一条 ADJ 的动作里包含「把这一栏填满」，空栏 ＝ 那条还没落投影。**
理由（本族实测）：**「登记册」与「执行投影」之间原本没有一致性检查**，所以每加一条裁定就会漏 N 处投影、而由下游逐条抓出来 —— 实测三条：**ADJ-02 落在卡上而汇编里没有**、**ADJ-09 的两档在卡与汇编里都没投**、**ADJ-07 的 `CORE` 默认只在登记册**。⇒ **判据：一条 ADJ 的「已裁」与「已投」是两件事；只有 `PROJECTED IN` 全非空才算落完。**

**十一项的裁决留痕**：ADJ-01～05 ＝ §374／§377；**ADJ-06／ADJ-07 ＝ §383**（ADJ-07 的后果一/二/三也在此节）；**ADJ-08 ＝ §385**；**ADJ-09 ＝ §392**；**ADJ-10 ＝ §393**（★ 该节把它写成「页内相抵」，**定性已作废**，收口见 `deltas`）；**ADJ-11 ＝ 尚未落页**（Owner 逐字已成文，**按 2026-09-21 工作令先落 delta、等放行**）。★ 这些节是它们的**唯一可引用落点** —— 本表的 ID 只是索引。

## 3. 仍开 —— **登记在册的「未核 / 无页面出处」**（你可以给意见，但**不必**当缺口报）

- **无页面出处的 UI 细则**：卡上「本层操作数 / 诊断数 / profile presence / source health」四个展示项；结构编辑面的筛选；「组件卡不做 mini heatmap / 不展开完整字段 provenance / 不做操作历史时间线」三条负向。—— 页面上只列了摘要、模板选择器、Role 角标、继承/覆盖状态。
- **两处口径不一致**：影响面数字「三项 vs 四项」（**四项那一侧有页面依据**）；「25 个 Structure slot」只在一处出现（**UI 不固化字段数**）。
- **一条覆盖缺口**：`§3.7` 的展开算法**只分「有数值覆盖 → 取覆盖值」／「否则 → 取底板值」两支**，**没有「底板该组件为空」那一支** —— 而契约别处明确承认那个状态。

---

## 4. 看着像缺陷、其实**是有意的** —— 请不要报

1. **容器高度未改**：控制条内容到 y=121、容器高 122，**紧贴下缘**。已登记——加高会吃掉与下方块的 12px。
2. **物种层没有 `CLEAR`**：层面结构限制，不是漏做。
3. **「沿用物种操作」是缺省名，`沿用物种调整`/`沿用物种设置为` 属「行内显示」层**：**名字 ≠ 显示**，两者不矛盾；**不得合并成「恢复」**。
4. **卡侧只显示物种层**：桶层的三个操作只在 Policy 控制条里作选项。
5. **Role 角标保留角色色**（不做成白场）：已裁——**角色色是「非常重要信息」**。
6. **图上标「示意 / 空态」不是缺陷**：那是**不声称它存在**的记号；`类型名（示意）` 是占位。

---

## 5. **细粒度结项表**（状态**逐项**给，**不给整块的 `Persistence CLOSED`**）

理由：本族出现过「一整块写着 CLOSED、而其中两个子项其实还开着」。⇒ **只有所有子项都 CLOSED，才允许说那一块 CLOSED。**

| 子项 | 状态 | 依据 / 剩什么 |
|---|---|---|
| **Component Recipe Shape** | **CLOSED** | 读数已裁（§3.1 的四个组件字段**就是** Component Recipes：Source ＋ 逐字段 op）；逐字已交写入者 |
| **Affinity Role Patch** | **CLOSED** | §3.4 逐字齐：`(row_key, component)`、op `CLEAR|SET`、`SET` 携 `role`、`INHERIT` ＝ 无记录 |
| **Affinity Fail Env Coeff Patch** | **CLOSED** | §3.4 逐字齐：`row_key`、op `CLEAR|ADD|SET`、越界报错不 clamp |
| **Species Policy Recipe** | **CLOSED（读数）** | §3.1 记录里逐字有 `policy_source_binding`；**但它的指称物（第五类 `TemplateKind`）在实现里不存在** ⇒ 那是**实现缺口**，不是形状未定 |
| **Affinity Source Override** | **CLOSED** | 读数已裁（**组件级独立绑定**）；**owner 已裁** —— 身份是「中鱼习性模式」（`Engagement Mode`），**（物种, 桶）是它在数据迁移期的表达** |
| **Profile Presence** | **CLOSED** | 矩阵已裁（**统一**：缺席合法性只由 `Role` 决定，时段不特权）；**默认值已裁 ＝ `CORE`** |
| **Species Role UI** | **OPEN —— 控件形态待设计** | 裁定已给（`INHERIT` **需要一个与三值可区分的形**；**同值写 `SET`**）；**这个形本身还没被设计出来** —— 所以它开着的不是「待裁」而是「待做」。★ **2026-09-21 消歧**（bot 在 `OPEN-ITEMS.md:97` 上报的「状态相抵」）：**本行说的是这个控件的形**；**§1(b) 说的是「图上两个作用域分组的投影已执行完、待复审」** —— **两件事，不是同一状态**。⇒ **能力侧另有裁定（ADJ-12）：四组件必须有 reachable Setup path，该能力要求已 CLOSED；控件的精确形仍归 Species Role/UI 工作流。** |
| **Follow / Pin 语义** | **CLOSED** | ⚠️ **先前这里写「相抵」，已撤回**：回原页核完，**它是已定的、只是没落到 picker 那一处** —— §3.3 逐字「无 `sourceOverride` ＝ 跟随」＋ §3.5 表「覆盖→不跟随／恢复为底板→跟随」⇒ **跟随 ＝ 没有那条记录**，故「跟随物种」**＝ 删除** `sourceOverride`（**不写同源记录**）。落页已派 |
| **Source Transaction** | **CLOSED** | 射程已裁（**ADJ-09 ＝ C_NARROW**）：**Source mutation 一律 staged**，Preview 按 **fan-out** 分 **Local / Propagated** 两档。⚠️ **先前这里写「两条耐久规则相抵」，已撤回** —— 实测是**两个正交判据**（「要不要 staged confirm」 vs 「属于哪一档」），不是一条轴的两端 |
| **TimePeriod Transaction** | **CLOSED** | ★ **2026-09-21 三处都收了**（Owner 裁定；**其中预览那一条推翻了我先前的归类**）：**① 预设的五个 `SET` 落到哪一层** ⇒ **`target = 当前 active Recipe / Patch authoring owner`**（两个合法 durable target：Species context ⇒ Species TimePeriod Recipe；Affinity／bucket context ⇒ 当前 Affinity TimePeriod operationPatches）；**五个 `SET` 一个 atomic batch**；不切换 layer／不默认提升到 Species／**不创建第三个 preset layer**／不改 Source／不持久化 `presetId`／**不得跨两层拆写**。**② 预览边界** ⇒ ★ **`ADJ-09` 是 Source mutation 的事务规则，不得自动推导到 TimePeriod Preset**；**窄规则**：**若 target layer 没有将被覆盖的 local ops ⇒ 不要求 staged confirmation**（正常 semantic edit／autosave，**可展示结果但不强制确认页**）；**若会覆盖已有 local ops ⇒ batch preview**（五字段 before/after ＋ 明确哪些 local ops 被替换 ＋ 新增 Error·Warning）**＋ explicit confirm ＋ atomic commit**。**不做 full-library impact scan。** **③ `预设` 一词有四个指称物** ⇒ **terminology hygiene**（四者分别写、不合并），**不因此把本节整体挂开**。 |

**⇒ 上表现在只剩 一项 开着**：`Species Role UI` 的**形** —— 它是唯一「**待做**」而非「待裁」的那项；**能力侧已由 ADJ-12 收口**（四组件 must have reachable Setup path，CLOSED），**形归 Species Role/UI 工作流**（设计任务已在跑）。
★ **但按本族规矩：`Persistence` 这一块仍只在全部子项 CLOSED 之后才说 CLOSED** —— 那一项是「**待做**」，所以**现在仍不能说整块 CLOSED**。

## 6. 七处我（材料侧）报出去的、**不要求你判**的

- **`§3.7` 的展开算法少一支** ⇒ **★ 已闭（ADJ-11 ＝ A_NARROW）**：它原来只分「有数值覆盖 → 取覆盖值」／「否则 → 取底板值」，**没有「底板该组件为空」那一支**。⇒ **现在补上**：`底板为空` **且** `Effective Role ＝ IGNORED` ⇒ **不产生该组件的 production projection、不创建显式空 Profile、不因这一点阻断 Publish**（主行与该组件的 `Role = IGNORED` 仍正常写回；`ProductionRowLedger.refs[component]` 保持空）。**投影落在汇编 §11。**
  - ★ **保留这条作留痕**（它一度是一个缺口）；**不移除**。
- **链接图指向副本而非 owner**：《主开发需求》§3.0 把作者分层诸事实链到《编辑器与 Resolve》§11 与《Editor → Persistence》，而它们的 canonical owner 是《编辑器持久层契约》§3.3。
- **超过 60 处跨页重复定义**：已盘出（按页计数最高的是《编辑器与 Resolve》与《编辑器界面》），**其中至少三组明确不许合并**（物种 `INHERIT` vs 桶层 `absent`；物种层 Role 默认 vs `AffinityRolePatch`；「同值」vs「同意图」）。清理按「已裁动作」执行，**不做语义等价判断**。
- ★ **ADJ-08 对齐 —— 真正要对齐的只有两处：CT §3.3 与 RS §11.1**（**已 CLOSED、未写**）。两处都带着「**不新增 EngagementMode durable identity**」这个**读起来像整体否定**的引子，而 **CT §3.3 的正面句已在同节前两段**（逐字「**这条 patch 的 owner 是「中鱼习性模式」（`Engagement Mode`）**…**数据迁移期以桶为行单位表达**」）。⇒ **实现者会据那个引子认为「不存在 durable 的 Mode 身份」、从而把 owner 键在行单位（桶）上。**
  - ⚠️ **UI §5 / RS §7 / IA §8 不需要改** —— 它们写的是 **Runtime 域**那句（「Runtime 无 EngagementMode identity」），**与 ADJ-08 相容**；补正面句反而会把两个寄存器混起来。
  - ⚠️ **本包 `component-contract-consolidated.md` §16 只作射程说明与标注，不改写原句。** 页侧精确 delta 见**仓外/本地工作件**（**不在本包**）—— 按 Owner 2026-09-21 工作令，**Notion 写入暂停**，先落 delta、再由单一写入者落页。
- ★ **顶栏动作名 `Reset` ＝ 一条命名裁定，不是「页内相抵」**（**已落页**，UI §9.1 ⇒「丢弃未保存的改动」，Version 12→13）：★ **《编辑器界面》§1.2 并没有禁 `Reset` 的句子** —— 回读实测（**2026-09-21 12:40 之后**）**该页全页 `Reset` = 0、`Override` = 0、「不向作者暴露」= 0、「工程词」= 0**；§1.2 给的是**操作 → 用户语言的映射**（`CLEAR` ⇒「仅使用当前来源」）。⇒ **「不能叫 `Reset`」的依据在裁定侧、不在页上**；**替换词＝「丢弃未保存的改动」**（判据见 `component-contract-consolidated.md` §4 的出处校正）。**不必再报。**
  - ⚠️ ★ **那个「全页 = 0」必须带时点锚**：它是 **12:40 那笔落页之后**的读数，**不是「页上从来没有过」** —— 该页 §9.1 在此之前**逐字就是** `` `Reset` / `Publish` / `导出` / `Bass 预设` ``，**画布上那个 `Reset` 不是凭空来的**。⇒ **状态断言不带时点/版本锚，会被读成「从来没存在过」。**（这条是画布侧提出、我采的。）
- ★ **画布侧：bot 报的四处里，只有三处要改**（分拣依据＝`figma-current.md` §四 的「作者面 vs 投影面」分工，**读图前先读那条**）：
  - **要改（作者面）**：**`108:315` 顶行** `模板` ⇒ `来源 / Source` ｜ **`108:687` 的 25 个 `LocalOp`** `INHERIT` ⇒ `仅使用来源` ｜ **Policy 控制条 `242:676`／`678`／`680`** 三枚**选项 chip** ⇒ `沿用物种操作`／`仅使用当前来源`／`设置为`（★ 取**概念层名**；`沿用物种调整`／`沿用物种设置为` 那两个具体串属**状态显示位**，本帧未给继承来源，**不该出现在选项标签里**）｜ **顶栏 `Reset`** ⇒ `丢弃未保存的改动`（需加宽按钮 ＋ 改母件 `93:54`，已授权并带前置）。**已派，一次改完、我一次重导。**
  - ★ **不改（投影帧记号）**：**态10（`230:673`）里的 `仅使用当前来源 (CLEAR)` 与 provenance 那行 `（本层 CLEAR 移除继承的 op）`** —— 那是**投影帧把作者词钉到操作令牌上的绑定括注**，**正是投影面该有的东西**；且后者是上一轮 `FIG-03` 定下的措辞、其 annotation 亦按此记。
    ⇒ **bot 在 `figma-current.md:56` 那条（「态10 暴露被禁术语」）判为「不是缺陷」** —— **不必再报**。★ 判错的机理：**把「作者面」的规则套到了「投影面」上**；`108:*`（1220 高）是作者面，`230:*`／`232:*`（1080 高）是投影区。
- ★ **契约名 ↔ 实现名 的对照（已核两侧逐字，**不是**竞争权威）**：
  | 契约侧（《编辑器持久层契约》） | 实现侧（编辑器仓） | 判定 |
  |---|---|---|
  | **`ProductionRowLedger`** —— §3.4 逐字用它，并自述「**`ProductionRowLedger` ＝ §3.2 的生产行记录**」；出现在 `ProductionRowLedger[row_key].species_key` 那句不变量里 | **`ProductionRows`**（映射）／**`ProductionRowRecord`**（一条记录），`src/data/derived.ts:36/51` | **同一对象、两侧名字不同**。⇒ **裁定：不改名**（契约名是契约层的概念名、实现名是实现的类型名，**没有任何一处自定义**；改名的收益只是「看起来一致」，代价是 4 个文件的无行为变更 —— **无谓改动会污染基线**） |
  | **`refs`** | `ProductionRowRecord.refs: Partial<Record<ProfileField, number \| string \| null>>`，**键空间就是四个组件** | **同名、同形** ✓ |

  ⇒ ★ **登记它的理由**：不登记，下一个人会以为是**两个东西**。**读本包的人按契约名找实现时，请用右边那一列。**

---

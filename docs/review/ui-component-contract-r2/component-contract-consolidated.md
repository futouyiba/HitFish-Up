# 组件契约｜编辑器 UI Component Contract（现行）

本文只写现行规定。出处写作《页名》§N、记录页 §N 或 冻结卡 `A①-卡N` / `A②-卡N`；查不到出处的条目列在末节「未核 · 待裁」，不进正文。标（本轮裁定）的条目＝本轮已定口径，其依据随条给出。

## 1. 产品拓扑与三栏
- 三栏＝对象导航 ｜ 上下文总览 ｜ 焦点编辑。几何：250 ＋ 890 ＋ 460 ＋ 边距 ＝ 1680。（《编辑器界面》§9.1；《编辑器心智模型与 IA》§3）
- 左栏三类入口：FISH（Species → 习性 / 品质）／TEMPLATES（五类）／SPECIES PRESETS。物种预置＝一次性写五个来源绑定（四组件 ＋ Policy），**不是父节点**。（《编辑器心智模型与 IA》§3、§4）
- 中栏 Context 与右栏 Focus **不是同一个导航状态**：允许短暂 detached，但必须显式提示（右栏标题明确对象身份 ＋ 低成本「切回当前上下文」），不得让作者误以为右栏仍在编辑中栏对象。detached 只是 UI 导航状态，不产生新的 durable authoring entity。（《编辑器心智模型与 IA》§3 逐字「切换上下文不销毁编辑现场」）
- 中栏与右栏不得形成两套重复编辑器。（《编辑器界面》§1 导语：逐字段值编辑在焦点编辑栏完成）
- 控件名用现行页已经落下的 `FieldValueControl`（承载 Field ＋ Effective Value ＋ optional Tier ＋ Local Operation ＋ Diagnostic）。（裁定 f；《编辑器界面》§1。草稿另有叫法，见 §19）

<a id="structure-slice"></a>
## 2. Structure 竖切
- 第一条竖切路径：Species → Structure → 共享模板 → Species ADD → Affinity sourceOverride → SET / CLEAR → autosave → Resolve Preview → materialize。选型依据：结构在 allowlist 里只允许共享模板、查表取值无跨字段约束。（记录页 §164）
- 切片刻画的样例族：Species ＋ 共享模板 ＋ ADD ／ Affinity 沿用物种操作 ／ Affinity 固定另一来源 ＋ 继承物种操作 ／ 同源显式 pin ／ CLEAR ／ 本层 ADD ／ SET ＋ Tier ／ 换源 Rebase Preview ／ Effective < 0 → ERROR ＋ autosave ＋ Publish 阻断 ／ Effective > 1 → WARNING 放行 ／ 断链来源 ／ 已归档来源的既有引用 ／ Publish 阻断清单与定位。各状态的规定见本文对应节。（记录页 §164；各条出处见 §3–§8）

<a id="component-clear"></a>
## 3. Source × Operation 正交

**本节是组件字段 CLEAR / 继承语义在本包的完整投影，权威仍是《编辑器持久层契约》v16 §3.3、§3.5。** 本次直接核对其 `Last Updated 2026-09-21 14:34 +08:00` 版本，以及《编辑器与 Resolve》v12 §11.1–11.2；Policy 域另见 [§10](#policy-clear)，不能套用组件来源定义。组件的层 × 字段类型 allowlist 统一见 [§13](#component-operation-allowlist)。

- **按记录解析，不按结果值反推**：物种层 `INHERIT` ＝ 无本层记录；桶层 `absent` ＝ 无该字段 patch，沿用物种层 operation。桶层 `CLEAR` 则保留一条 **op-only** patch，显式移除继承的 operation，回到当前 Effective Source 原值；它是继承控制，不是第三种数值调整。同值 `SET` 仍保留显式 pin，不能因结果相等改成 `absent` 或 `CLEAR`。（《编辑器持久层契约》§3.3、§3.5；记录页 §265 裁 `F-03`）
- **「恢复为底板」的数据动作是删除该字段覆盖记录**，从而回到 `absent`；不是写 `CLEAR`，也不是写一个恰好相等的 `SET`。这三个意图不得共用模糊的「恢复」操作名。物种层没有 `CLEAR`；其 `INHERIT` 同样用无记录表达。（《编辑器持久层契约》§3.3、§3.5；《编辑器与 Resolve》§11.2）
- Source ≠ Operation：换 Source 保留既有操作，改操作保留 Source。（记录页 §172「KEEP」；《编辑器与 Resolve》§11.3）
- `ADD / SET` 按字段 allowlist 各存一个本层最终 operation；桶层的 `ADD / SET` **替换**物种层操作，不形成第三层叠加。（《编辑器与 Resolve》§11.1 逐字「不是叠第三层 delta」；《编辑器持久层契约》§3.3）
- **来源值与计算**：物种层无操作时直接用来源值；桶层按上面的分支选择 Effective Operation，再作用于该桶的当前 Effective Source。`ADD` ＝ 当前来源值 ＋ delta；`SET` ＝ 绝对值。当前来源可以是共享模板，也可以是该组件合法使用的 `SPECIES_CONCRETE`；不能要求每层都持久化一个显式 Source ref。（《编辑器与 Resolve》§11.1；记录页 §288、§312、§316 对 `CXR-04` 的更正；P0 Source allowlist 见 §8）
- 桶层 `sourceOverride` ＝ 固定 Source Choice，不冻结配置：pin 之后 patch 仍缺省时仍继承物种层操作；`sourceOverride` 不自动 SET 全部字段、不清既有操作；解除 pin ＝ 删除 `sourceOverride`，重新跟随物种层 Source。（《编辑器持久层契约》§3.3）
- same-source pin 是真实 authoring intent：桶层 `sourceOverride` 与物种层 Source 相同时也不自动移除。（《编辑器持久层契约》§3.3；记录页 §172「KEEP」）
- **`CLEAR` 保留 `sourceOverride`**：若来源被钉住，清除继承操作后仍读那条来源；物种以后换 Source 不会解除该 pin。来源自身更新时，该字段读取更新后的 raw 值。操作跟随与来源跟随是两条独立轴；删除字段 patch 与删除组件级 `sourceOverride` 也是不同动作。（《编辑器持久层契约》§3.3「操作与来源是两条可以分开的跟随轴」）

<a id="field-value-control"></a>
## 4. 字段控件（`FieldValueControl`）
**拆成两个交互面**（选哪个动作 / 敲什么数）；卡2（Operation Control）与卡3（Field Value Editor）的拆分不改 —— 它们拆的是控件职责，与「UI 上是否并成一行」是两件事。（本轮裁定 f；冻结卡 `A①-卡2`、`A①-卡3`）

**操作选项**：组件 allowlist 见 [§13](#component-operation-allowlist)，Policy 见 [§10](#policy-clear)；四格用户选项投影见 [卡2](contract-cards.md#operation-control)。

**用户语言**（裁定 c；初版被 commit 侧证据修正，见 §17.1）：
- 物种层：**仅使用来源** / **调整** / **设置为**。
- Affinity 层：**沿用物种调整** / **沿用物种设置为**（按实际继承到的那一个操作给串）/ **仅使用当前来源**（`CLEAR`）/ **调整** / **设置为**。
- Affinity 缺省支显示的是**实际继承到了什么**，不显示泛称「沿用物种操作」；物种层没有操作时，Affinity 缺省支显示「仅使用来源」。
- 「沿用物种调整 / 沿用物种设置为」沿用的是物种层的**操作**，不是物种层的最终数值；这两支不得与「仅使用当前来源」合并成一个模糊的「恢复」。（《编辑器与 Resolve》§11.1 逐字「`absent` ＝ 跟随物种层 operation」、§11.2）
- **⚠️ 上面三条要按「两个寄存器」读，别读成「泛称被禁」**：**「沿用物种操作」是这一支的「名字」（概念层，保留）**；**行内「显示」必须给具体串**（见上一条）。⇒ **名字 ≠ 显示**：**名字保留、显示给具体串**，两者不矛盾。而「沿用物种操作」与「仅使用当前来源」**不得合并成一个模糊的「恢复」**。（记录页 §331 四、§359 ①）
- **作者可见的串一律取作者词汇**：`INHERIT` / `ADD` / `SET` / `CLEAR` 是**操作令牌**，`Override` / `Reset` 是**工程词**，两者都不是作者词；作者词＝本节上一段那五支。（《编辑器界面》§1.2「操作的用户语言」；《编辑器心智模型与 IA》§2 作者词汇表）
  - ⚠️ **出处校正（2026-09-21，回读复核后）**：本条此前写作「**不向作者暴露** `CLEAR` / `Override` / `Reset` 等工程词（《编辑器界面》§1.2 只给四词用户语言）」。★ **那不是《编辑器界面》§1.2 的逐字** —— 回读实测该页**全页 `Reset` = 0、`Override` = 0、「不向作者暴露」= 0**，§1.2 给的是**操作 → 用户语言的映射**（`CLEAR` ⇒「仅使用当前来源」），**页上没有禁令句**。⇒ **本条的实际强度是「作者词表由该映射给出」，不是「页上有一条禁令」。**
  - ⇒ **给下游的用法限制**：**不得把本条当成「页上明禁 `Reset` / `CLEAR`」引用**。「`Reset` 不能作作者可见词」是一条**命名裁定**（记录页），**不是页内相抵**。（★ 这一处是**我把转述当成了页上逐字** —— 记在案的同类错：**引《页》§N 前先回那页读一次**。）

**显示**：
- 折叠态只显示：字段名、当前操作摘要、Effective Value、Diagnostic。展开态显示：当前来源、被继承的操作、本层操作、Effective Value、provenance / 算式。（本轮裁定 g；草稿 §4）
- 显式展示「来源 → 当前层操作 → 当前值」；`ADD` 与 `SET` 视觉可辨；典型三行：来源值 `0.80` · 相对调整 `-0.20` · 当前值 `0.60`。（《编辑器心智模型与 IA》§3；《编辑器界面》§1.2）
- 被替代的上级操作**只用于解释 provenance，不再参与链式计算**，且视觉降级。（本轮裁定 g；草稿 §4、§6）
- **不许把「替换」画成「叠加」**（按层分写）：**每层每字段最多一个最终 operation**（**不允许 `ADD+ADD`／`SET+ADD` 之类的链**）；**覆盖是整层替换、不是叠加**：某桶对该项一旦自己表达，**底板那一层对该项整个不生效**。（《编辑器持久层契约》**§3.3** 逐字，L456／L457；另见《编辑器心智模型与 IA》§1 同规则的自行表述）
- 已覆盖但数值与**底板**相同，**仍须读作已覆盖**（界面读记录，不按值差）。（《编辑器持久层契约》§3.5 逐字）

**durable 语义**：
- CLEAR 留记录与同值 pin 按 [§3](#component-clear)；每层每字段最多一个最终操作，编辑＝替换当前格。（《编辑器持久层契约》§3.3、§3.5）
- **「计入本层操作数」属于 UI 展示项，Current 页面无出处**（§18 未核项 5）；保留 [卡2](contract-cards.md#operation-control) 的既有执行投影，不将其升级为 Current 规则。
- 输入控件里的临时字符串（`-`、`0.`、空）不是持久值，不覆盖上一笔 durable 值。（《编辑器界面》§1.2；《编辑器持久层契约》§7.1）

**切操作时的落盘**（本轮裁定 d）：
- 选定操作即落盘成立（《编辑器界面》§1.2 逐字把「操作 / 角色 / Source 选定」列为一次有效语义编辑、经短 debounce 原子落盘），**但「选定」须伴随一个合法 typed 值**；未成值不落盘。
  - ★ **这条 guard 的射程只到 `ADD` / `SET`** —— **只有它们带 typed 值**；**`INHERIT` / `CLEAR` 按定义没有 typed 值**，**不受本条约束**（`INHERIT` ＝ 删记录；`CLEAR` ＝ 落一条 op-only 子 patch —— 下一行那两条才是它们的边界）。
- 因此不得因为选了「调整」就写 `ADD(0)`、也不得因为选了「设置为」就写同值 `SET(当前值)`；同值 `SET` 是真实 pin，须在用户确认 typed value 后才 durable。
- local pending 编辑器可以作实现形态，但不得整体改成「必须再确认才落」。
- `INHERIT` / `CLEAR` 是明确语义动作，不做「自动保持结果」。

## 5. Tier
- Tier 不是第三条计算轴：属 Authoring 表达，不是生产配置表字段、不是 Runtime 输入；编辑器必须在保存 / Resolve 前确定性解析为最终数值。（《编辑器与 Resolve》§2.1；《主开发需求》§6 第 3 条）
- **`ADD` 不带 `tier` 字段；`CUSTOM` 只作 `SET` 下拉里的一个选项。**（本轮裁定 a；记录页 §199 ⑥①；冻结卡 `A①-卡2`、`A①-卡3`「不得用伪造 `CUSTOM` tier 满足 schema」）
- 适用面：Structure / Feeding Layer / Time Period；**Temperature 不带 `affinity_tier`**。（记录页 §174 二（Owner 直收）、§172 二 APPLY DELTA ③）
- 四档锚点与可表达范围：PREFERRED 1.00（1.00）／SUBOPTIMAL 0.60（0.50–0.75）／ACCEPTABLE 0.25（0.20–0.30）／REJECT 0.05（0.00–0.10）；Custom 可精确值。（《编辑器界面》§1.1）
- **不得从裸数值自动反推 Tier**：数字落进某档范围不等于声明该档。（《编辑器持久层契约》§3.3「不得从生产最终值反推」）
- **`SET` 值越出该档可表达范围时不自动转 `CUSTOM`**（那是静默改写作者意图）：保留档位标签 ＋ 出一个可见诊断，由作者显式改。（本轮裁定 e；《编辑器持久层契约》§3.4）

## 6. 校验 × Autosave
- 三条通道分开：raw input 非法（不落 typed、不产生 durable）／typed 语义非法（可 durable 自动保存）／I/O 或 revision 冲突（写入未成功）。（《编辑器界面》§1.2、§1.4；《编辑器持久层契约》§7.1）
- 校验对象＝ resolved / Effective 值，不是 `ADD` 操作数的符号；负 `ADD` 使终值非负即合法。（《编辑器界面》§1.2；《主开发需求》§9）
- `< 0` ＝ ERROR：可自动保存（带错误继续修）、阻断 Publish、Runtime 不得接收。（《编辑器界面》§1.2；《主开发需求》§7、§9）
- `> 1` ＝ WARNING：不阻断（保存 / 校验 / Resolve / Publish 均放行），Runtime 原值消费、不 clamp；**分级靠文案与阻断性区分，不靠颜色** —— 这一侧是「红标」。（本轮裁定 b；《编辑器界面》§1.2、§1.4 与《主开发需求》§7 三处逐字）
- 不允许 runtime clamp / abs / shift / 归一 / fallback / 带符号权重修复负 Fit。（《主开发需求》§9 逐字）
- `0` 不自动等于 Gate Fail：离散 Fit ＝ `0` 时，CORE 触发 Gate、SECONDARY 不触发、IGNORED 不消费 —— 同一个 `0` 的后果由 Role 决定。（《编辑器界面》§1.1 四档表 REJECT 行逐字；记录页 §199 ④ GAP-007）

- 顶栏四态：已保存 / 已保存·有错误 / 保存中 / 保存失败；Validator ERROR 不是「保存失败」；无常驻 Save。（《编辑器界面》§1.1、§1.2；冻结卡 `A①-卡7`）
- 阻断 Publish 时提供可发现的出口：进入校验清单、逐条定位到组件 / 字段，执行仍被阻断。（《编辑器界面》§1.1 逐字「发布前全量校验，错误精确定位，不静默修复」；冻结卡 `A①-卡6`）
- 诊断是派生量，每次重算，不持久化为第二真相。（《编辑器持久层契约》§6.5）

## 7. 组件卡 ＋ 焦点编辑栏
- 组件卡是**摘要 ＋ 快速编辑入口**，不是只读卡：可就地改 **Source / Template** 与 **Role 三态**；逐字段值仍在右侧 460px 焦点编辑栏完成。（《编辑器界面》§1 导语、§1.1）
- 卡上展示：组件身份、当前 Source / Template、当前 Role 角标、继承 / 覆盖状态、诊断。（《编辑器界面》§1.1「卡片展示摘要、模板选择器、Role 角标与继承 / 覆盖状态」；冻结卡 `A①-卡1` 的「卡上 `templateName` 与闭值同源同名」「same-source pin 的『已显式固定』记号」）
- **入口与 Truth 的对应**：**前层 Source Selector（顶部 `templateRow`，每组件一个）与组件卡的来源 / Source 下拉**（**卡上这一个入口同时覆盖 Template 与 Source** —— 换模板就是换 Source 绑定）指向**同一个**组件 Recipe Source binding；**卡的 Role 下拉与 Policy 区 Role 行**指向**同一个** Policy Authoring Truth。⇒ **各自「双入口、单 Truth」，不得改成单入口，也不得增设第三个 mutation 面。** ⚠️ **入口叫「来源 / Source」，不叫 Template** —— 合法来源里含 `SPECIES_CONCRETE`（**它不是模板**）；**当所选来源是共享模板时，卡上以该模板名显示它**（展示层才出现 Template 字样）。⚠️ **卡上这两样都是「就地可改」**（Template / Source 与 Role 三态）—— **卡不是只读卡**；卡上改 Source 写的是 **Component Recipe Source binding**、改 Role 写的是 **Policy Authoring Truth**，**两者都不是卡自己存一份副本**。⚠️ **两入口「同源」说的是 durable truth 同源**；**未确认的 Source 变更是 candidate（UI 态）** —— 两处可同时显示它，**但它还不是 truth**（见 §8 的 candidate → Rebase Preview → 显式确认 → 原子提交）。⚠️ **焦点编辑栏不提供 Source 下拉** —— 它只显示当前 Source 的上下文／来源说明（在那里再放一个 Source 选择器，就成了「Top Row ＋ Card ＋ Focus Editor」三个 mutation surface，**复杂度没有买到新能力**）。（《编辑器持久层契约》§8 首行「每组件一个**前层** Source 选择器」；《编辑器界面》§1 导语、§1.1、§7；《编辑器心智模型与 IA》§6、§7、§8；记录页 §172 二 KEEP、§331 裁 `R3-FIG-01`、§358 裁「入口不叫 Template」）
- 卡的 Source / Role 不得另建一套 durable state。（《编辑器界面》§7；《编辑器心智模型与 IA》§8）
- 字段行**原地展开**，不设二级 drawer。（本轮裁定 g；页面只规定 2 列紧凑控件与折叠栏位）

<a id="source-transaction"></a>
## 8. Source 选择器 ＋ Rebase Preview

**本节是 Source mutation、两档 Preview 及确认边界在本包的完整机制投影**；权威为《编辑器持久层契约》§3.10、§6.3 及记录页 §392 的 ADJ-09 裁定。本批回读持久层 v16（`Last Updated 2026-09-21 14:34 +08:00`），未重读记录页；其余历史出处沿用基线。具体动作／字段／验收见[卡1](contract-cards.md#source-selector)，事务分类与 TimePeriod 的独立护栏见[§15](#transaction-model)。

- 每组件一个前层 Source 选择器；桶（覆盖层）另有「跟随物种」；温度多一项「当前物种生态数据」（存在时）。（《编辑器界面》§1.1；《编辑器与 Resolve》§11.3）
- 可选来源矩阵（**按层分写**）：**前层（物种层）** —— Temperature ＝ `SHARED_TEMPLATE | SPECIES_CONCRETE`，Structure / Feeding Layer / Time Period ＝ 仅 `SHARED_TEMPLATE`；**桶（覆盖层）** —— **所有组件都只有 `SHARED_TEMPLATE` ＋「跟随物种」**，**不列 `SPECIES_CONCRETE`**（**连当前物种的也不列** —— 要引用当前物种的 Concrete，走「跟随物种」）。**任何层都不得 pin 非当前物种的 Concrete。**（《编辑器持久层契约》§3.3；《编辑器与 Resolve》§11.3 逐字「桶层另有「跟随物种」选项，**不把任何物种的 Concrete 当通用可选项**」；冻结卡 `A①-卡1`）
- `SPECIES_CONCRETE` 属当前物种：identity ＝ `(speciesId, componentType)`，不进模板清单、不可被其它物种引用；不得 pin 另一物种的 Concrete。（《编辑器持久层契约》§3.3；记录页 §172 二）
- **每一笔 Source mutation 都要 staged confirm**：候选保持 ephemeral → before / after Resolve → 对应档位的 **Rebase / Impact Preview** → 显式确认 → 乐观 revision 核验 → 原子 durable 提交。禁止为保持旧 Effective Value 自动生成 `SET`。（《编辑器与 Resolve》§11.3；《编辑器界面》§1.1；《编辑器持久层契约》§3.10；记录页 §392 裁 ADJ-09）
- **Preview 取哪一档由 `fan-out` 决定，不由「点了几个控件」决定**（记录页 §392 裁 ADJ-09）：**Local Rebase Preview** ＝ 只覆盖本次作用域（binding / Effective Source / follow-pin / 字段值 / 诊断 的 before-after；**不要求算整库**，不算两引用集 / 全局 changed count / 新增 Error·Warning 的全局计数）—— **桶组件的 `sourceOverride` 通常属这一档**；**Propagated Impact Preview** ＝ **当一次 mutation 会主动扩散到当前 owner 之外的多个 consumer** 时升档（**物种层 Source 变更若只被自己消费仍是 Local，传播到多个 follower 才升档**）。改 Shared Template 完整值、Replace References、Concrete reimport、批量换绑继续走完整 Impact Preview；直接引用集与有效消费者的用途见[§14](#template-lifecycle)。
- ⚠️ **「要不要 staged confirm」与「是不是 full high-impact」是两个正交判据，不是一条轴的两端** —— 影响面大小**只决定 Preview 有多重，不决定能不能先写盘**。（记录页 §392 逐字；本判据＝该节核心不变量）
- **`FOLLOW_PARENT`（删 `sourceOverride`）不留例外**：它同样改变 Effective Source ⇒ 也是 Source mutation；**即使当前 Effective Source 恰好不变也不是 no-op**（pin 住 `Template_A` 与跟随到 `Template_A` 当前值可相同、**未来行为不同**）⇒ **Preview 不得只展示 value diff**，至少还要 Binding intent／Effective Source／Future propagation。（记录页 §392）
- Preview 至少区分：最终结果变化、结果未变但被本层 `SET` / 操作遮罩、新增 Error、新增 Warning。**被遮罩 ≠ 无影响。**（《编辑器持久层契约》§3.7「SET-masked 可不变」；冻结卡 `A②-卡10`、`A②-卡11`；记录页 §172 二 APPLY DELTA ⑦）
- 已归档来源：既有 durable 引用继续合法、继续 Resolve / Publish，选择器显示「已归档」，不允许新建引用，普通 picker 隐藏 / 降级，不视为 ERROR。（《编辑器持久层契约》§3.10；《编辑器界面》§1.1）
- 断链来源：可加载（load tolerant）、显示明确的 Source Missing、ERROR ＋ 阻断 Publish、**禁止任何自动 fallback / 自动切回物种来源 / 自动挑最近似模板**，必须由作者显式选新的合法来源。（《编辑器持久层契约》§3.10；冻结卡 `A①-卡6`）

<a id="policy-profile"></a>
## 9. Profile × Spatial Opportunity Policy

**本节保留 Policy 归属与 Role 记录态的完整机制投影**；Profile 缺席、promotion 与 Setup 的完整投影在[§11](#profile-lifecycle)，Policy 操作词表／CLEAR 来源仍在[§10](#policy-clear)，落盘形状与键见[RoleControl](contract-cards.md#role-control)。权威仍是 Current／Owner；本批回读《编辑器持久层契约》v16（`Last Updated 2026-09-21 14:34 +08:00`）§3.1／§3.4／§3.7，以及《编辑器界面》v20（`Last Updated 2026-09-21 17:19 +08:00`）§1.2／§1.4，未重读实时裁定记录。

- Profile 回答「这条鱼对这个环境轴是什么习性」；Role 回答「这份习性在聚合里如何被消费」。（《编辑器与 Resolve》§2.2；《编辑器心智模型与 IA》§7）
- Role 与 Profile 的变更边界按[§11](#profile-lifecycle)，不能由改变消费角色推导创建／删除或改写 Profile。
- 空间机会聚合策略有独立共享 Policy Template，payload ＝ 四个角色 ＋ `fail_env_coeff`；它是第五类 `TemplateKind`，**不是第五个 Component** —— 不扩 `ComponentType`、Runtime 仍四条件槽、不新建生产 Policy 子表。（《编辑器持久层契约》§3.6；记录页 §172 二 A）
- Policy Source 只绑物种层；**桶层没有 `policySourceOverride`**，不得虚构这类直接引用。（《编辑器持久层契约》§3.10；记录页 §172 二 B）
- 粒度必须分离：数值 override 按 **bucket**（`young / mature`，TimePeriod 不按规格 / row）；Role override 按 **生产行**。同一 id 组合的不同行可有不同 Role，Validator 不得因 Role 不同报错。（《编辑器持久层契约》§3.4、§3.7）
- `fail_env_coeff` 属档案级、不挂在某个组件卡内部；`[0, 0.10]`，默认 `0.01`，越界 ERROR ＋ 阻断 Publish、不 silent clamp。（《编辑器界面》§1.1；《编辑器持久层契约》§3.4）
- `fail_env_coeff` 的 `ADD` 是绝对数值增量，不是百分比 / 乘数。（《编辑器持久层契约》§3.4 逐字「ADD 为绝对数值增量」）
- Editor 没有钓场上下文：不提供 Pond selector，不编辑 `baseOpportunityIntensity / isBackgroundFish / envCoeffMin`；`fail_env_coeff` 是本编辑器可编辑的习性档案字段，不是 `FishRelease` 的 `envCoeffMin`。（《编辑器界面》§6）
- 诊断归属：字段 → 字段控件；Profile → 组件卡；Policy → 聚合策略区；全局 / Publish → 顶栏 ＋ 校验清单。（冻结卡 `A①-卡6`；《编辑器界面》§1.4）

<a id="role-record-intent"></a>
**Role 记录态与 UI 派生**：
- Policy Template 的 raw Role 默认值为 `CORE`，不是 `IGNORED`，不能由实现自选缺省或留未定义；「初生默认」与作者从 IGNORED 提角色是不同事件。（《编辑器持久层契约》§3.1；记录页 §383 ADJ-07）
- 物种 Role 的 `INHERIT` 用无本层 op record 表示；选中任何具体 Role（包括与当前 Policy Template raw Role 相同的值）仍写 `SET`。回到 INHERIT 要显式删除本层 Role op，不能用选同值代替；行级 patch 与物种默认仍按不同记录／键落盘。（《编辑器持久层契约》§3.1、§3.4；完整字段见 RoleControl）
- 物种 UI 必须可区分无记录 INHERIT 与三值 SET。状态位从 Species Role durable op record 是否存在派生：无记录不显示“Role 已钉住”，有记录（含同 raw 值 SET）显示；不增加第二份 durable UI state。此显示裁定沿用[固定基线 ADJ-03 依据](https://github.com/futouyiba/HitFish-Up/blob/add09fdaa9c197740df6735160af45c1ebb32370/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#L20)，本批未重读该实时 Owner 记录；卡片只承接显示／验收。设计证据与保存重载未核的区别见[问题台账](OPEN-ITEMS.md#species-role-ui)。

<a id="policy-clear"></a>
## 10. Role 与 Policy 的操作词表
**本节是 Policy 域 CLEAR 的完整投影**，权威为《编辑器持久层契约》v16 §3.4（同 §3 的核对版本）；裁决依据为记录页 §265 `F-04`。仅负责此域的来源与词表，记录存在性、同值意图区分沿用 [§3](#component-clear)，无值动作的落盘例外见 [§4](#field-value-control)。
- Role：物种层 `INHERIT / SET`；桶层 `absent / CLEAR / SET`；**永不允许 `ADD`**。（《编辑器持久层契约》§3.4）
- `fail_env_coeff`：物种层 `INHERIT / ADD / SET`；桶层 `absent / CLEAR / ADD / SET`。（《编辑器持久层契约》§3.4）
- Policy 侧的 `CLEAR` 语义：移除继承自物种层的操作，**回到物种当前 Policy Template 的 raw 值**。（《编辑器持久层契约》§3.4）
- 该定义同时覆盖四个 Role 与 `fail_env_coeff`；`CLEAR` 不携值。**Affinity 没有 `policySourceOverride`**，不能把组件级来源 pin 的能力搬入 Policy。（《编辑器持久层契约》§3.4、§3.10）
- 桶层缺省（继承物种层操作）与 `CLEAR`（回到 Policy Source 原值）是两个不同动作，UI 必须区分。（《编辑器持久层契约》§3.4；《编辑器与 Resolve》§11.2）
- 不因最终值 / 枚举相等自动推断 inherit、CLEAR 或 SET。（《编辑器持久层契约》§3.5、§3.3）

<a id="profile-lifecycle"></a>
## 11. Profile 生命周期

**本节是 Role／Profile／Setup 关系在本包的完整机制投影**；来源版本见[§9](#policy-profile)。ADJ-02／07／11／12 的裁定出处、关闭范围和历史转录归[台账](OPEN-ITEMS.md#role-profile-history)，不以本节声明实现已经通过。

**缺席与校验**（《编辑器界面》§1.4；《编辑器持久层契约》§3.1、§3.7）：四组件按同一 Effective Role 矩阵判断，TimePeriod 不特权。`IGNORED` 时缺 Profile 合法、自动不消费；`CORE / SECONDARY` 缺必需 Profile 则 Resolve／Publish 阻断。按[§9 的 raw 默认](#role-record-intent)，新物种尚未配置时会处于阻断态；合法空态须显式设成 IGNORED，不能把“尚未配置”当作默认忽略。激活 CORE／SECONDARY 但缺 required Profile 时必须立即显示可见诊断，不能停在无提示非法态；这是 UI 呈现要求，不改变上游判级。

**Promotion 与 Setup**（《编辑器持久层契约》§3.1；《编辑器界面》§1.2／§1.4；原 B1a／B1b 裁定沿固定历史）：
- 改 Role 只改变角色，不创建／删除 Profile，不改 Profile 数值、不自动选择默认 Source、不写全 `1.00`。将 Role 设为 IGNORED 不删除已有 Profile；本版不提供通用“删除组件 Profile”动作（持久层 §3.3）。
- 四组件都必须有显式可达的 Setup 路径：`Profile absent → choose / establish a legal Source → 可 Resolve 的完整 Profile`。初值来自所选合法 Source；不能另建通用 `1.00` 默认值契约，不新增空 Profile 对象或 required Source／identity 为 null 的半成品。
- Setup 优先复用 Source 模型，不新增 durable `CreateProfile`，也不要求必须有字面“新建档案”按钮；判据是路径可达（界面 §1.2）。四组件数据形态不同：Structure／Feeding／Time 是 affinity 数值，Temperature 是曲线参数，不能用通用 `1.00` Profile 统一。具体入口见[RoleControl](contract-cards.md#role-control)，Source allowlist 仍按[§8](#source-transaction)。
- TimePeriod 同样有 Setup 能力；三种预设只是 Setup 后／中的一次性填表便利，不是它独有的 Profile 创建机制（持久层 §3.3；界面 §1.2）。预设的 target 与覆盖确认仍按[§12](#component-specifics)、[Batch Overwrite Guard](#timeperiod-batch-guard)，不因 Setup 收敛改变。
- `IGNORED + absent → 作者提 Role → Role durable autosave → CORE + absent` 是可达的 durable-but-publish-invalid 中间态：显示 required-Profile ERROR／Publish Block，聚焦 Setup，再由作者显式选择／建立 Source；不得丢 Role 回默认掩盖错误。该执行顺序沿用[已审 brief 的 ED-20 护栏](https://github.com/futouyiba/HitFish-Up/blob/add09fdaa9c197740df6735160af45c1ebb32370/docs/implementation-brief-0.3.4.0-B.md#L54)，持久有效与可发布有效仍分开。

<a id="empty-profile-projection"></a>
**空底板的生产投影分支（ADJ-11＝A_NARROW）**，权威为《编辑器持久层契约》§3.7：
- 仅当该组件 `Authoring Profile / Species Base 为空` **且** `Effective Role = IGNORED`，才不产生该组件的 Component Profile production projection、不创建显式空 Profile，也不因该组件缺席阻断 Publish。
- `FishEnvAffinity` 主行及该组件的 `Role = IGNORED` 仍正常写回；仅不生成／写回该组件完整 Profile 子表值。尚无 production Profile 时，`ProductionRowLedger.refs[component]` 保持空（载体与字段见持久层 §3.2）。
- “空”表示尚无该组件 production projection，不是新 Runtime Profile 值，不把 null／empty 当 Profile 下发；该组件根本不进入 evaluator。CORE／SECONDARY 缺必需 Profile 仍阻断，不能把合取条件放宽成任意缺席都放行。
- 保留本包既有执行约束：caller 按上述合取条件先排除该组件，其余才进入已有展开判定，不扩该判定的取值域；不得让 `namedItemsOfProfiles` 将无档案压成全 0 再触发门控失败。[原解释与修正留痕](https://github.com/futouyiba/HitFish-Up/blob/add09fdaa9c197740df6735160af45c1ebb32370/docs/review/ui-component-contract-r2/component-contract-consolidated.md#L132)仅作历史审计，不再另维护一份机制。

<a id="component-specifics"></a>
## 12. Feeding Layer / Time Period / Temperature
**Feeding Layer**：SURFACE / MIDDLE / BOTTOM 三项最终系数，复用数值型项的同一套能力，不新增组件类型。（《编辑器界面》§1.1；《编辑器持久层契约》§3.3）

**Time Period**（覆盖确认的完整规则见 [§15 Batch Overwrite Guard](#timeperiod-batch-guard)，不得套用 Source 事务）：
- 五段 DAWN / MORNING / AFTERNOON / DUSK / NIGHT；未配置时显示合法空态，不置灰（**它的合法性来自 §11 的统一矩阵，不是时段特权**；且按 §11，空态须由作者**显式**把 `Role` 设成 `IGNORED` 得到）。（《编辑器界面》§1.1；记录页 §377／§383）
- 三预设（晨暮型 / 昼行型 / 夜行型）是一次性批写五个字段的 `SET`：不是 Source、不是模板 identity、不进长期继承链；应用后不持久化 `presetId`，当前 Source binding 不变；覆盖已有本层操作时须 batch preview ＋ 显式确认；五个 `SET` 各自可带该预设明确的 Tier 语义；**后续单字段修改后不得再宣称仍属某预设**；模板名不进 Runtime。（《编辑器界面》§1.1；记录页 §172 二 APPLY DELTA ④）
- 预设不负责创建 Source；应用后原 Source binding 仍在（即使五项都被 `SET` 遮罩也不删除 / 弱化）。（《编辑器界面》§1.1）
- ★ **三预设那五个 `SET` 落到哪一层（ADJ-13，refine 后）**：**`target = active Recipe / Patch authoring owner`** —— **Species context ⇒ 写 Species TimePeriod Recipe 的 5 个 `SET`；Affinity / bucket context ⇒ 写当前 Affinity TimePeriod operationPatches 的 5 个 `SET`**；**五个 `SET` 同 owner、同 layer、一个 atomic batch**。
  - **不切换 authoring layer／不默认提升到 Species／不创建第三个 preset layer／不改 Source／不持久化 `presetId`／五个 `SET` 作为一个 atomic batch。**（记录页裁 **ADJ-13**）
  - ★ **若某 UI surface 本版只开放 Species authoring ⇒ 在那里自然只写 Species** —— **那是 surface capability 的后果，不是 Preset 自身拥有 Species 语义**。（★ 与 ADJ-12 同源：**三种预设是 Setup 后/中的一次性填表便利，不是 TimePeriod 独有的「Profile 创建语义」**）

**Temperature**：
- 6 参数 ＋ 连续曲线；同图显示 `temp_threshold`；另有「从钓鱼元素周期表导入」入口。（《编辑器界面》§1.1）
- 字段能力：`acceptMin / favMin / favMax / acceptMax / threshold` ＝ 数值型项（无档位）；`falloff_shape`（项名位 `falloff`）＝ 枚举绝对值项。（《编辑器持久层契约》§3.3；记录页 §175 六.2）
- **P0 曲线只读、不 drag-author**；**6 项参数（5 数值 ＋ `falloff_shape` 枚举）**仍按项编辑。（记录页 §199 ⑥②；冻结卡 `A①-卡3`）
- 跨字段不变量：`accept ≤ fav`（四边界链）；相等合法；非法组合可 durable 保存但阻断 Publish。（《主开发需求》§7；记录页 §199 ④ GAP-008）
- `temp_threshold` 不改变曲线形状，只作 CORE 的 Gate 阈值。（记录页 §199 ④ GAP-010 引《配置表与校验》§5；《编辑器界面》§1.1）
- 跨字段非法时禁止 silent repair：不自动排序四个边界、不交换字段身份、不 clamp 到相邻边界、不把作者输入静默改成「合法值」；曲线区不得伪造一条自动修正后的曲线。（《主开发需求》§9；《编辑器持久层契约》§7.1）
- 生态数据重导只更新 Concrete Source 本身，不落成 tuning 操作、不自动切换当前 Recipe Source；研究事实修正走更新来源，游戏调参保持来源、写物种层操作。（《编辑器持久层契约》§3.3）

<a id="component-operation-allowlist"></a>
## 13. 字段能力表
（页面上只有「数值型项 / 枚举绝对值项」两种说法；草稿另起了三个名，见 §19）
- 数值型 · 带档位（Structure / Feeding Layer / Time Period）：物种层 `ADD` / `SET`（无操作 ＝ `INHERIT`）；桶层 `absent` / `CLEAR` / `ADD` / `SET`；`SET` 可携带 `affinity_tier`。（《编辑器持久层契约》§3.3）
- 数值型 · 无档位（Temperature 四边界 ＋ `threshold`）：同上；Temperature 不带 `affinity_tier`。（同上；记录页 §174 二）
- 枚举绝对值（`falloff_shape`，项名位 `falloff`）：物种层 `SET`（无操作 ＝ `INHERIT`）；桶层 `absent` / `CLEAR` / `SET`；**不得 `ADD`**。（《编辑器持久层契约》§3.3 逐字「枚举绝对值不得 ADD」）
- 层决定有无 `CLEAR`，字段类型决定有无 `ADD`；不可把桶层选项暴露给物种层。对应四格用户语言见 [卡2](contract-cards.md#operation-control)。（记录页 §312 裁 `XR-F-03`）

<a id="template-lifecycle"></a>
## 14. 模板工作区与模板生命周期

**本节是模板生命周期、两引用集及 Replace 边界在本包的完整机制投影**；卡9／11／12保留交互、记录与验收。权威为《编辑器持久层契约》v16（`Last Updated 2026-09-21 14:34 +08:00`）§3.6／§3.10；本批同时回读《编辑器界面》v20（`Last Updated 2026-09-21 17:19 +08:00`）§7。其余历史出处沿用基线，未重读实时 Owner 记录，也不声明实现已通过。Source staged 协议仍按[§8](#source-transaction)，不在本节重定义。

- 五类 Live Template：Temperature / Structure / Feeding Layer / Time Period / Spatial Opportunity Policy。（《编辑器心智模型与 IA》§4；《编辑器持久层契约》§3.6）
- 模板是**完整值资产**：operation 只存在于物种 Recipe 与桶 patch 上。（《编辑器持久层契约》§3.3、§3.7）
- 两个入口、一个焦点编辑器：从组件卡钻入（中栏保持鱼上下文）与从模板库进入（中栏切到模板上下文）复用同一个模板值编辑器。（《编辑器心智模型与 IA》§4；《编辑器界面》§7）
- 平铺、可滚动、默认按引用量排序；中文 / 英文别名可编辑；source name 只读且不作键。（《编辑器界面》§7）
- 关联一律按 id；别名属 editor-state；不把 inheritance lineage 编进生产行 name。（《编辑器持久层契约》§3.6、§4.4；《编辑器界面》§1.2）
- 「从当前鱼提取模板」**只创建 Template Asset**：不改当前鱼 Source、不清既有操作、不把 Recipe 折成新模板引用（即使 payload 完全相同）；要改 Source 须另走 Source Change ＋ Rebase Preview。（《编辑器界面》§7 逐字；记录页 §172 二 APPLY DELTA ⑤）
<a id="template-lifecycle-guards"></a>
**生命周期与删除**（持久层 §3.6／§3.10；交互见[卡9](contract-cards.md#template-lifecycle-control)）：
- 五类模板统一只有 `ACTIVE / ARCHIVED` 两态。归档后既有引用继续 Resolve／Publish，但不可新建引用、不可直接改完整值；可查看引用／Replace References／Restore，要改值先 Restore，再走 Impact Preview。普通 Source Picker 隐藏／降级归档模板。
- Archive 不自动改引用、不 fallback、不自动找相似模板、不自动复制 payload；`ARCHIVED` 不等于可删。Hard Delete 仅在下述 `DirectReferenceSet` 为空时允许；已有直接引用须先显式解除／替换，检查范围包括 SpeciesPreset 与其它 durable 直接引用，不能只数当前 Effective consumers。
- Preset 引用归档 source 时 `invalid-for-apply`，UI 指名是哪一个；禁止静默跳过／fallback／选最近似模板。这与既有 Recipe 引用仍可 Resolve／Publish 分开。（持久层 §3.10）

<a id="template-reference-sets"></a>
**两引用集与影响统计**（持久层 §3.10；只读展示见[卡12](contract-cards.md#reference-list)）：
- `DirectReferenceSet(A)`＝durable state 中直接写了 A 的 source ref 的对象，包括 Species Recipe source、Affinity `sourceOverride`、SpeciesPreset binding、Policy source；用于 Replace 改动目标、Hard Delete guard 和直引清单。Policy Template 的 direct refs 是 Species policy source binding 与 SpeciesPreset policy binding；Affinity 没有 `policySourceOverride`，不得虚构。
- `EffectiveConsumerSet(A)`＝Resolve 后当前 Effective Source 为 A 的全部最终 Recipe，含经物种层继承者；用于改值的 Impact Preview／before-after 分析。两集不能互代。
- 模板改值／Replace 的候选变更场景中，影响面分列直接引用数／Effective consumer 数／最终结果变化数／新增 Error·Warning，四者可不同。卡12只读列表没有候选与 before/after 输入，故只展示前两项，不展示后两项、不自行制造候选机制；后两项归卡10／11等候选变更场景。此上下文边界沿用[固定基线卡12的 CXR-03 修正](https://github.com/futouyiba/HitFish-Up/blob/38f3dac85083542a63c310c5d65383579d1353b0/docs/review/ui-component-contract-r2/contract-cards.md#reference-list)，不冒称本批重读实时记录页 §288。

<a id="template-replace-boundary"></a>
**改值与批量换绑**（持久层 §3.10；卡10／[卡11](contract-cards.md#replace-references)）：
- 模板完整值修改与 Replace 都属高影响动作，按[§8](#source-transaction)走候选、before/after Impact Preview、显式确认与原子提交；重新 Resolve 后的生产投影沿[§15](#cross-layer-guards)及卡10的既有边界，不以只比较两个模板 payload 代替影响分析。
- Replace A→B 只重写 `DirectReferenceSet(A)` 的 durable 绑定，保留既有 operations／patches（含 `ADD / SET / CLEAR`），重 Resolve 全图。禁止给经继承消费的 child 自动写 `sourceOverride`，禁止为保持旧 Effective Value 生成 `SET`；同值不改变上述拓扑边界。

- 正常传播不给每个消费者制造待复核债；只有真实诊断 / 复核条件才进待复核。（《编辑器心智模型与 IA》§5；《编辑器界面》§1.1）
- 模板 → 模板的实时继承不支持；clone / save-as 后是独立模板；分类 / 族只用于分类与推荐，不构成继承父节点。（《编辑器持久层契约》§3.6；《编辑器心智模型与 IA》§4）

<a id="cross-layer-guards"></a>
## 15. 跨层护栏
- Editor durable state 存作者意图（Source binding / `sourceOverride` / 物种操作 / 桶 patch / Role 与 Policy / 模板完整值 / identity 与生命周期），**不把 Effective / resolved 值当第二份可编辑真相**；Effective、provenance、诊断、影响结果都是派生。（《编辑器持久层契约》§3.3、§6.5；《编辑器界面》§1.3）
- 自动保存：一次有效语义编辑 → 内存 typed 状态 → 短 debounce 合并 → 原子持久化；无常驻 Save；预览缓冲是短命 UI 状态，不落成草稿实体。（《编辑器界面》§1.2、§7；《编辑器持久层契约》§3.10）

<a id="transaction-model"></a>
**事务分类**（《编辑器持久层契约》§6.3；记录页 §392）：只有两层，不新增第三种 durable transaction type。① 普通 semantic edit（值 / op / Role）走上述 debounce autosave，通常无 staged preview；② 所有 Source binding mutation 与 Shared / bulk 传播类，执行 [§8 的 staged 协议与 Preview 分档](#source-transaction)。

<a id="timeperiod-batch-guard"></a>
**TimePeriod Batch Overwrite Guard**（Owner 2026-09-21 裁，沿用[固定基线 §15](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/review/ui-component-contract-r2/component-contract-consolidated.md#15-跨层护栏)与[原能力裁定](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#L122-L123)）：Preset 不是 Source mutation，不因 ADJ-09 自动要求 staged confirm；它属于普通 semantic edit。
- target layer 没有将被覆盖的 local ops：正常 semantic edit／autosave，可展示结果，不强制确认页。
- 会覆盖已有 local ops：batch preview 列五字段 before/after、哪些 local ops 被替换、新增 Error·Warning，随后 explicit confirm ＋ atomic commit；不做 full-library impact scan。
- 五个 `SET` 是同 owner／同 layer 的一个 atomic batch；target、Source 不变及不持久化 presetId 等边界见[§12](#component-specifics)。该护栏不是第三种 durable transaction type，也不是 Source Rebase Preview。

- Publish 只读取已成功持久化的 revision；尚未成值的输入不参与 Publish；未确认的高影响候选不得被当成 durable truth。（《编辑器界面》§1.1；《编辑器持久层契约》§6.3）
- revision 冲突＝乐观检测：commit 只在预期 revision 仍匹配时写入，禁止 last-write-wins、禁止静默 auto-merge，进入重载 / 对比 / 对账路径。（《编辑器界面》§1.2；《编辑器持久层契约》§6.3）
- 「生产配置外部变化」与「Editor State revision 冲突」是两类不同问题，不得都显示成「保存失败」。（《编辑器持久层契约》§6.4、§6.5；《编辑器界面》§9.2）
- 本版只有一次性 Bootstrap：`Production →（一次性 Bootstrap）→ 初始化 editor durable state → 此后 editor durable state 是 authoring truth`；持续的批量反向对账 / 采纳生产值**不在本版**，只给只读诊断。（《编辑器持久层契约》§6.5；《编辑器界面》§9.2）
- 往返冒烟测试＝本版验收：Production → Bootstrap → Editor → 不做任何编辑 → Publish → Production，应逐位一致。（记录页 §164）
- 生产侧只保存物化后的完整值 / 枚举，不保存 Source / op / patch provenance；Runtime 不做 base ＋ delta 合并。（《编辑器与 Resolve》§11.1）
- 生产投影按结构化 authoring lineage 复用，不按 payload 相等：物种层用共享模板且无有效操作 → 可复用该模板的生产 Profile；桶层完全继承物种 Recipe → 可复用物种投影；有显式 `sourceOverride` 但最终为「纯共享模板 ＋ 零操作」→ 仍可复用该模板的 Profile（显式 pin 只分叉继承关系，不强制复制行）；最终仍含任何有效操作 → 该桶自有投影。**同值 `SET` 与纯 source pin 必须区分**：同值 `SET` 阻断未来模板改值 ⇒ 自有投影；`sourceOverride` ＋ 零操作 ＝ 未来继续跟随 ⇒ 可安全复用。（《编辑器持久层契约》§3.7）
- ★ **`name` 的射程要分两层写**（原文只写「只是人类可读标签，不作 identity / join / 复用键」—— **过宽**，独立复审于 `fa96900` 报出，2026-09-21 Owner 同向裁定）：**Editor / Materializer 内部定位 → 稳定 id / key**（`name` **不作** Editor identity）；**Production XLSX 跨子表引用 → 仍按现有物理 schema 写 `targetRow.name`**。⇒ **本期不得把 XLSX 引用单元格顺手迁成 id**（那是单独的**配置表 Schema Migration**；`TimePeriod` 连数字 group id 都没有）。因此 **新增／新建的 production row `name` 必须在对应 production lookup domain 内无歧义**，collision ⇒ **BLOCK**（不 silent suffix / fallback）。行名的三级形态＝模板级（作者填，不预填）/ 物种派生级 / 桶派生级（自动生成）。（《编辑器持久层契约》§4.4）
- 不隐藏耦合：换来源不自动改 Role；改 Role 不自动换来源；Role 置 IGNORED 不自动删 Profile；重导 / 生态数据更新不自动切 Recipe Source；预设应用不产生长期预设 identity；值相等不自动转继承；同源不自动删 `sourceOverride`；payload 相等不自动合并 authoring owner；归档 / 断链来源不自动 fallback。（《编辑器持久层契约》§3.3、§3.5、§3.7、§3.10）

<a id="identity-boundaries"></a>
## 16. 负向清单
不做（画进假图等于把作者引向不存在的能力）：
- 程序开关；`if / else / return` 之类控制流编写；自定义聚合算子；自由编排 / 任意输入连线；Gate 控件 / `GatePolicy` 字段；模板共享面板的三档分级；不新增顶层空的 `Calculation Surfaces` 导航；不显示 Activity / Feeding Readiness 之类空壳；不新增第二套 Bake Editor、不新增脚本入口。（《编辑器界面》§5）
- 占比 / 比例 与 分群逻辑两处只以禁用占位行呈现（字段位在、控件不在），不提供编辑控件；不得据此宣称本版已实现 Mode Share / Routing。（《编辑器界面》§5、§1.2）
- 桶不是真正的 Engagement Mode；Runtime 无 EngagementMode identity，不得据 UI 名称另建 durable 的 Engagement Mode 身份 / 注册表 / 模式级 Concrete 来源。（《编辑器界面》§5；《编辑器与 Resolve》§11.1；记录页 §172 二 KEEP）
  - ⚠️ ★ **2026-09-21 Owner 收口为 `C_SPLIT_REGISTERS`（取代本节先前那条「owner 的 canonical 名是「中鱼习性模式」」的读法）**：**要消灭的是「owner」这个同时指「业务语义归属」与「物理 durable identity」的模糊中间词。**
    ⇒ **业务语义概念** ＝ `Engagement Mode`／中鱼习性模式（**Simplified Production V0 的正式业务概念**，**B P0 不实现 Mode Share / Routing**）；**物理 durable key ＝ `FishEnvAffinityRef`**；`FishEngagementModeCompat` 是**对 Affinity 的 mode-like authoring projection ／ 兼容壳**；**Runtime / production 无独立 `EngagementMode` identity。**
    ⇒ ★ **上面那条禁令（不得据 UI 名称另建身份 / 第二套注册表 / 模式级 Concrete 来源）依然成立** —— 它禁的是**据 UI 名称造身份**，与本次收口**同向**。
    ⇒ ★ **`sourceOverride` 一律写作 `(fishEnvAffinityRef, component)`**（**若 schema 字段名为 `owner_ref`，则 `owner_ref := FishEnvAffinityRef`**）—— **不要留一个抽象的 `owner` 让实现者猜是哪套 identity。**（记录页裁 **ADJ-08 ＝ `C_SPLIT_REGISTERS`**）
  - ⚠️ ★ **页侧本轮已收口（2026-09-21）**：**CT §1.1 ／ CT §3.3 ／ RS §11.1 三处已按 `C_SPLIT_REGISTERS` 改写**；**《编辑器界面》§5 不动** —— 它写的是 **Runtime 域**那句（「Runtime 无 `EngagementMode` identity」／「durable owner ＝ `FishEnvAffinityRef`」），**与本次收口相容**；RS §7 ／ IA §8 同理。⇒ **不再有「按滞后页照录」这件事。**
- 品质页本版不开放（入口置灰、不展示品质字段）；不新建品质模板库、不把品质当作第五个习性组件。（《编辑器界面》§0、§2）
- 组件卡不承担逐字段 `ADD / SET / CLEAR` 编辑（逐字段值在焦点编辑栏完成）；不给组件卡 Source / Role 另建 durable state；不把 Effective Value 当编辑真相存储；不为视觉一致强迫所有字段支持 `ADD`；不为结构对称给品质造模板；不按「当前数值相同」跨无关谱系合并生产行。（《编辑器界面》§1 导语、§7；《编辑器心智模型与 IA》§8）

---

## 17. 两份不一致
逐条给两侧逐字与判断依据；不调和、不静默丢弃。

**CLEAR 相关审计留痕**：本节第 1、4、5、6 项及 §18 第 1–2 项保留 [PR #7 固定版本](https://github.com/futouyiba/HitFish-Up/blob/1409a13fde46dcb8d10bae039c26f6a0090bf497/docs/review/ui-component-contract-r2/component-contract-consolidated.md#17-两份不一致) 的比较与更正原文，不作为另一份持续维护的定义。现行投影请沿 [§3](#component-clear)、[§4](#field-value-control)、[§10](#policy-clear) 阅读；历史探针的命中数只代表原核对时点。

1. **桶层缺省支的显示文案** —— 裁在「两侧各有可取、合成了新形态」
   - paste（`paste-inbox.md` §2）逐字：「Affinity 层有四种：… 沿用物种操作｜patch absent｜当前 Source + Species operation」。
   - commit（`chatgpt-ui-component-contract-phase1.md` §19.5）逐字：「Species 有 ADD：显示"沿用物种调整"；Species 有 SET：显示"沿用物种设置"；Species 无 operation：显示"仅使用来源"，不要显示空洞的"沿用物种操作"」。
   - 判断：**裁定 c 的初版（取 paste 的单一泛称「沿用物种操作」）被 commit 侧证据修正** —— commit 侧说的是**实际继承到了什么**，可判据更强：泛称在物种层无操作时**没有宾语**，且与物种层的「仅使用来源」并列会撞。⇒ 采用 commit 侧形态（按继承到的那一个操作给串），并把「物种层无操作」那一支接到「仅使用来源」；两者合成为 §4 的五支清单。这同时解掉初版的易混点：Affinity 缺省支不再一律用泛称，而是按实际继承到的操作给串。
2. **`SET` 值越出档位可表达范围时是否自动改档**
   - paste §3 逐字：「如果作者输入明显脱离该档位，例如从 SUBOPTIMAL 改到 0.91，我倾向于自动转：tier = CUSTOM op = SET(0.91)」。
   - commit §21.1 逐字：「Custom 可表达精确值，但不能因为数字落进某 Tier range 就自动声称该 Tier」。
   - 判断 —— **裁在 commit 侧**。两侧方向相反，裁定 e 取 commit 侧（不自动转 `CUSTOM`）并补可见诊断；两侧的「自动」写法都不进正文（§5）。一句判据：自动改档＝静默改写作者意图，与「Tier 不得从生产最终值反推」同族。
3. **`ADD` 的 tier metadata**（两侧同向、但都与现行相抵）
   - paste §3 逐字：「Durable authoring metadata 可以记：tier = CUSTOM op = ADD(-0.20)」；commit §5 逐字：「ADD = relative tuning intent，tier metadata 视为 CUSTOM」。
   - 判断 —— **裁在现行条款侧（两侧同向、都不得采）**。两侧同属 commit §15 自己写的「`SET` 可携带 `affinityTier`」的反面，也与「冻结卡 `A①-卡2`：`ADD` 记录不带 tier」相抵；裁定 a 覆盖两侧：`ADD` 不带 `tier` 字段。一句判据：哨兵值＝把缺失码伪装成值（本族已在 `min_env_coeff` 的 `0` vs 空上栽过一次）。
4. **被替代的上级操作用什么措辞**
   - paste §5 逐字：「物种操作 / 调整 -0.20 已取消」；同一稿 §6 逐字：「调整 -0.20 已由本层替代」，§9 逐字：「物种调整 -0.20 · 已被本层替代」。
   - commit §4 逐字：「被替代的 parent operation 只用于解释 provenance，不继续参与链式计算」——未给标签。
   - 判断 —— **裁在「已被本层替代」一侧**。paste 稿内自己就有两个串，正文统一取「已被本层替代」。一句判据：《编辑器持久层契约》§3.3 的用词是「整层替换…底板那一层对该项整个不生效」。可翻转点：若认 `CLEAR` 那一格不是「被替代」而是「不再继承」，该格另取一词（两种读法都无页面逐字）。
5. **Policy 侧两个动作的措辞**
   - commit §20.9 逐字：「因此"恢复为物种角色"（patch absent）与"恢复为 Policy Source raw Role"（CLEAR）是两个不同动作，UI 必须区分」。
   - paste 无对应句（其 §2 只给数值项的四词）。
   - 判断 —— **裁在 paste 的立场（不给这两支命名为「恢复」）**。commit 用「恢复」给两个动作命名，与现行相抵；正文按 §10 的两分法写（缺省支 vs `CLEAR` 支），不采用「恢复为…」这一对措辞。一句判据：《编辑器与 Resolve》§11.2 逐字把「恢复」判为模糊词、禁止合并使用。
6. **INHERIT / CLEAR 是否走 pending**
   - commit §4 逐字：「INHERIT / CLEAR 是明确语义动作，不做自动保持结果」。
   - paste §8 只规定「选择"调整" / "设置为"」两种情形要进 local pending editor，未涉 INHERIT / CLEAR。
   - 判断 —— **裁在 commit 侧（射程更明确的一侧）**。两个动作**不参与 pending 机制**。★ **本行先前写「并按裁定 d 补上『须伴随一个合法 typed 值』这一条」—— 该补写是错的，已删**：§4 逐字把那条 guard 的**射程限定在 `ADD` / `SET`**（「只有它们带 typed 值；`INHERIT` / `CLEAR` 按定义没有 typed 值，**不受本条约束**」），而本行把条件**重新附加到 `INHERIT` / `CLEAR`** 上 ⇒ 作者从 `SET` 切到 `INHERIT` 删记录、或选 `CLEAR` 写 op-only patch 时，会**去等一个定义上不存在的 typed 值** ⇒ **两处相抵，且是行为级**（独立复审在 `72a49c25` 上报出 `CXR7-OP-01`）。**现行判断 ＝ 两个动作直接执行，不附加 typed 值。** 一句判据：paste 未涉 = 留白，不是相反主张，取写明射程的一侧不会丢东西。
7. **commit 自己记录的途中收敛（Card 只读 → 可快速编辑）**
   - commit §18.1 逐字：「第三次复核后确认：此前把 Card 收窄为只读摘要，是本轮中途产生的错误收敛，**不应进入集成**」；§22.4/§7 同向（「ComponentCard 是摘要 + 快速编辑入口，不是只读卡」）。
   - paste 不涉及组件卡。
   - 判断 —— **裁在 commit 侧（可快速编辑）**。这一条是 commit 自己推翻过的东西；正文取「可快速编辑」侧（§7），「只读卡」形态不进正文。一句判据：《编辑器界面》§1 导语（逐字段值编辑在焦点编辑栏完成，卡仍可就地改模板与角色）与 §7「双入口、单 Truth」。

## 18. 未核 · 待裁
1. **物种层缺省支的用户语言「仅使用来源」与现行页面相抵**：现行《编辑器界面》§1.2 与《编辑器心智模型与 IA》§2 逐字都是「跟随（INHERIT）」／「跟随」；本轮裁定 c 取「仅使用来源」。正文按裁定写；落页时须连动改这两页（含冻结卡 `A①-卡2` 的同一句）。 **〔2026-09-21 已落、本项收口〕** 两页回读：旧串「跟随（INHERIT）」「跟随」**均 0 命中**；**「仅使用来源」已在两页在位** ⇒ **本项所述「与现行页面相抵」已不成立**，无需再连动改页。
2. **Affinity 缺省支与 `CLEAR` 的用户语言未落页**：新形态的四串（「沿用物种调整」「沿用物种设置为」「仅使用当前来源」，以及物种层的「仅使用来源」）在本轮六个页面与记录页 0 命中（探针作用域见末行）；页面现文仍是「跟随物种配置」与「恢复为来源值」（《编辑器界面》§1.2、《编辑器心智模型与 IA》§2、冻结卡 `A①-卡2`）。判据成立（《编辑器与 Resolve》§11.1 逐字「`absent` ＝ 跟随物种层 operation」；§11.2 逐字把「恢复」判为模糊词）。落页归需求页写入者。**〔2026-09-21 已落、本项收口〕两页回读：旧串「跟随物种配置」「恢复为来源值」「跟随（INHERIT）」**均 0 命中**；「仅使用来源」与「仅使用当前来源」**在位**，且**两页各自写明**这一区分 —— 《编辑器界面》§1.2 **逐字**：「桶（覆盖层）须**显式区分**「沿用物种操作」与「仅使用当前来源」两个动作，不合并成一个模糊的「恢复」」；《编辑器心智模型与 IA》§2 **以另一措辞**写明同一区分：「「沿用物种操作」（无记录）与「仅使用当前来源」（CLEAR）是两个动作」。⚠️ **本条 2026-09-21 精确化**：先前这里写「两页均写明」并只给一句引文 —— **只有《编辑器界面》§1.2 是逐字，另一页是同义的另一句**；且**该页那句里的「显式区分」带内联粗体标记**，用不带标记的串去 grep 会**假 0 命中**（探针必须与物同形）。「沿用物种调整」／「沿用物种设置为」**不在页上是合裁定的** —— 按后来的裁定，**泛称「沿用物种操作」才是缺省名，那两个具体串属「行内显示」层**。**冻结卡 `A①-卡2` 的降级前提随之消失（该卡已按记录页 §312 裁 `XR-F-07` 的「落到页后即恢复」恢复）。**〕**
3. **正文里出现的页面不存在串，已一律清出**：清出的清单与仍需命名的项集中在 §19。
4. **commit 的 16 个组件名清单**页面上没有对应名，已移入 §19。
5. **无页面出处的 UI 细则**（正文未收）：卡上「本层操作数 / 诊断数 / profile presence / source health」四个展示项（页面只逐字列了摘要、模板选择器、Role 角标、继承 / 覆盖状态）；结构编辑面的筛选用「全部 / 本层修改 / 问题」；「组件卡不做 mini heatmap / 不展开完整字段 provenance / 不做操作历史时间线」三条负向（页面 §5 负向清单里没有这三条；《编辑器心智模型与 IA》§3 反而要求焦点编辑栏有独立 History）；Time Period Setup 的六步序列（页面只有「未配置是合法空态 ＋ 激活后须当场可见校验态 ＋ 空态指向显式创建 / 选择来源」）；Time Period 预设 batch preview 的四项内容（页面只有「须 batch preview ＋ 显式确认」）；模板 candidate 编辑的「N 项待审查修改 / [撤销] / [审查修改]」形态（页面只有「预览缓冲是短命 UI 状态，不落成草稿实体」）；Species 字段编辑「不弹 Modal、只在行旁给影响摘要」的强度映射（页面无此分级）；`temp_threshold` 在非 CORE 时「仍显示 / 保存但标注当前不消费」的文案（页面只规定「只对 CORE 必需」与「同图显示」）；`same-source pin` 的文案「当前值不变，但继承关系变化」（页面只要求「已显式固定」记号）；P0 每条通道的验收 variants 清单（commit 列 39 条、paste 列 13 条，属测试计划，正文只收成状态族，见 §2）。
6. **顺带复查到的另一处页面间冲突**（非本两份草稿的内容）：冻结卡 `A①-卡3` 逐字「Effective <0＝ERROR（红）、>1＝WARNING（黄）」，而《编辑器界面》§1.2、§1.4 与《主开发需求》§7 三处逐字都是「`> 1` 的 WARNING ＝ 红标」。本轮裁定 b 取三票侧；卡3 那句待改。 **〔2026-09-21 已收口〕** 冻结卡 `A①-卡3` 现逐字为「Effective<0＝ERROR（**红标**）、>1＝WARNING（**红标，不阻断**）」⇒ 与《编辑器界面》§1.2／§1.4 的**同向**表述一致，「WARNING（黄）」已不存在。
7. **《编辑器与 Resolve》§11.3 与其余三处对影响面数字的口径不一致**：Resolve §11.3 逐字「「引用数 / Effective consumer 数 / 最终数值变化数」是三个可以不同的数字」，而《编辑器持久层契约》§3.10、《编辑器界面》§1.1 与《编辑器心智模型与 IA》§5 逐字都是**四项**（含「新增 Error·Warning」）。记录页 §208 记的收口是「三数→四项」，Resolve §11.3 那处未随之改。
8. **「25 个 Structure slot」**（只有 paste 有这一处；commit 全文不出现「25」作字段数）
   - paste §1 逐字：「25 个 Structure slot 如果每行把 Source / Species / Affinity / Effective 全铺开，右侧 460px 会直接变成 debugger」，收尾逐字：「这样一个 25 格 Structure 编辑器不会变成…」。
   - commit 只给 Structure 的 Detail Filter 与「Structure → 数值型项」的映射，不给字段数。
   - 判断 —— **裁在现行页面侧（UI 不固化字段数）**。一句判据：《编辑器界面》§1.1、§1.3 逐字「字段顺序跟随 Source，不在 UI Contract 固化名称清单或固定字段数量」⇒ paste 这处写法不成立。但**不得读成「25 不是 schema 数」**：《编辑器持久层契约》§3.3 `member_key` 逐字「结构 = `0`…`24`」、《主开发需求》§3.1 与 §4.0 逐字「逻辑查表键共有 25 项」「按当前 StructureType 展开，约 25 项」⇒ 25 是 StructureType 查表键数、属数据 / 记录层枚举。错的只是把它当成 UI 的固定字段数。冻结卡 `A①-卡3`「档位适用面：结构 25 槽」是同一处错。 **〔2026-09-21 已收口〕** 冻结卡 `A①-卡3` 现逐字写明「**按当前 Source 动态生成 StructureType 字段控件（不固化字段数量；现行实例 25 是数据/记录层的查表键数，不得反读成 UI 的固定字段数）**」⇒ **「25」不再作为固定 contract**。
## 19. 待命名 · 需裁定
正文规定里一律只用页面已有的串、或用纯语义描述。下列串**页面上不存在**：需要新名（或直接弃用草稿名）时在此一次裁定，**不得由下游另发明一套名字** —— 本族标识符按字节精确，正文里用一个文档里不存在的串＝让下游造第二套名字。
1. **控件名**：草稿叫 `FieldValueRow`；页面上已落的名字是 `FieldValueControl`（承载 Field ＋ Effective Value ＋ optional Tier ＋ Local Operation ＋ Diagnostic）。建议直接弃用草稿名。
2. **来源选择的三个草稿串**：`BOUND_SOURCE` / `FOLLOW_SPECIES_SOURCE` / `PIN_SOURCE(sourceRef)`。页面已有的对应物是「跟随物种」这一选项与 durable 字段 `sourceOverride`。
3. **三个字段能力名**：`tieredNumeric` / `numericRelative` / `enumAbsolute`。页面只有「数值型项 / 枚举绝对值项」；正文 §13 已按页面说法写，草稿名未采用。
4. **组件 / 区域名（commit 的 16 个）**：`ObjectContextHeader` / `ComponentCard` / `SourceSelector` / `FieldOperationControl` / `FieldValueRow` / `ValidationIndicator` / `AutosaveStatus` / `ComponentDetailEditor` / `RoleControl` / `SpatialOpportunityPolicy` / `TemplatePicker` / `TemplateWorkspace` / `ImpactPreview` / `TemperatureProfileEditor` / `TemperatureCurvePreview` / `SpeciesConcreteSourcePanel`。页面用的是「组件卡 / 焦点编辑栏 / 前层 Source 选择器 / 聚合策略区 / 顶栏 / 模板工作区」这类称呼；除 `FieldValueControl` 外都没有页面名。
5. **其他只在草稿里出现的串**：`profileCanStartAbsent` / `ModeConcreteSource` / `BootstrapSurface` / `DirectReferenceCount` / `localOperationCount`。`completeValue` 在《编辑器持久层契约》§3.7 有用法，正文按页面的「模板完整值」写。
6. **冻结卡自己的两个控件名**（`A①-卡2` Operation Control / `A①-卡3` Field Value Editor）是卡片层编号名；正文只在 §4 提到「两个交互面的拆分」，未把它们当控件名用。

本文的 0 命中声明，探针作用域＝本轮新取的六个页面（变更与裁决记录 / 编辑器界面 / 编辑器心智模型与 IA / 编辑器与 Resolve / 编辑器持久层契约 / 主开发需求）＋ `/tmp/edseat/inventory-batch1-cards.md`＋`/private/tmp/hitfish-inbox/paste-inbox.md`＋`/tmp/edseat/chatgpt-ui-component-contract-phase1.md`。

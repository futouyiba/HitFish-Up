# 组件契约｜编辑器 UI Component Contract（现行）

本文只写现行规定。出处写作《页名》§N、记录页 §N 或 冻结卡 `A①-卡N` / `A②-卡N`；查不到出处的条目列在 §18 的未核边界与 §19 的命名边界，不进正文。标（本轮裁定）的条目＝本轮已定口径，其依据随条给出。

## 1. 产品拓扑与三栏
- 三栏＝对象导航 ｜ 上下文总览 ｜ 焦点编辑。几何：250 ＋ 890 ＋ 460 ＋ 边距 ＝ 1680。（《编辑器界面》§9.1；《编辑器心智模型与 IA》§3）
- 左栏三类入口：FISH（Species → 习性 / 品质）／TEMPLATES（五类）／SPECIES PRESETS。物种预置＝一次性写五个来源绑定（四组件 ＋ Policy），**不是父节点**。（《编辑器心智模型与 IA》§3、§4）
- **Quality Stable Data 与 Production 习性引用分开**：`FISH QUALITY STABLE` 页面本期仍置灰，不开放品质自身字段。StockRelease / Production 中既有的 Quality＋`FishEnvAffinityRef` 引用由 Production / 数据迁移维护；习性档案 Authoring Surface 只读展示**当前 Editor 会话载入快照中，哪些既有 Production 引用指向该 Affinity**。UI 可按 Quality 聚合成人类可读摘要，但不得把聚合反推成新的全局 `Quality → Affinity` durable identity；同一 Quality 若在不同 Production 行引用不同 Affinity，可以同时出现在多个 Affinity 摘要中，这本身不是冲突。该摘要也不是实时 Routing 数据源。Production 后续外部变化由 drift / generation 诊断处理。Editor 本期不新增、删除或重分配这些引用，也不引入 Quality / Engagement Mode / tier / routing identity。
- **本版习性层级＝物种底板 ＋ 兼容覆盖**：Species Base 是主要 Authoring Truth；`young / mature` 是当前版本的兼容 authoring scope，不是真正的 Engagement Mode。numeric patch 按 bucket；Component Source 仍沿既有 Affinity/sourceOverride 身份规则；Role 与 `fail_env_coeff` 按 production-row 粒度处理。UI 同处一个兼容覆盖 Context 不改变这些物理 owner。产品 UI 显示「物种底板」与「兼容覆盖 · 幼年 / 成年及以上」。只有当该 Compat 下**没有任何本地 authoring record**（包括 numeric patch、`sourceOverride`、所含 production rows 的 Role / `fail_env_coeff` patch）时才显示「沿用底板」；存在任一记录则显示「有本层调整」，不按 Effective 值是否相同反推。不得用「未存」暗示档案缺失，也不得把生产行名（如 `NORMAL`）冒充产品 Mode identity。
- 中栏 Context 与右栏 Focus **不是同一个导航状态**：允许短暂 detached，但必须显式提示（右栏标题明确对象身份 ＋ 低成本「切回当前上下文」），不得让作者误以为右栏仍在编辑中栏对象。detached 只是 UI 导航状态，不产生新的 durable authoring entity。（《编辑器心智模型与 IA》§3 逐字「切换上下文不销毁编辑现场」）
- 中栏与右栏不得形成两套重复编辑器。（《编辑器界面》§1 导语：逐字段值编辑在焦点编辑栏完成）
- 控件名用现行页已经落下的 `FieldValueControl`（承载 Field ＋ Effective Value ＋ optional Tier ＋ Local Operation ＋ Diagnostic）。（裁定 f；《编辑器界面》§1。草稿另有叫法，见 §19）

<a id="structure-slice"></a>
## 2. Structure 竖切
- 第一条竖切路径：Species → Structure → 共享模板 → Species ADD → Affinity sourceOverride → SET / CLEAR → autosave → Resolve Preview → materialize。选型依据：结构在 allowlist 里只允许共享模板、查表取值无跨字段约束。（记录页 §164）
- 切片刻画的样例族：Species ＋ 共享模板 ＋ ADD ／ Affinity 沿用物种操作 ／ Affinity 固定另一来源 ＋ 继承物种操作 ／ 同源显式 pin ／ CLEAR ／ 本层 ADD ／ SET ＋ Tier ／ 换源 Rebase Preview ／ Effective < 0 → ERROR ＋ autosave ＋ Publish 阻断 ／ Effective > 1 → WARNING 放行 ／ 断链来源 ／ 已归档来源的既有引用 ／ Publish 阻断清单与定位。各状态的规定见本文对应节。（记录页 §164；各条出处见 §3–§8）

<a id="component-clear"></a>
## 3. Source × Operation 正交

**本节是组件字段 CLEAR / 继承语义在本包的完整投影，Git Markdown 的承接位置见[文档权威与发布投影](../../authority-model.md)。** 本次直接核对《编辑器持久层契约》v16 §3.3、§3.5，以及《编辑器与 Resolve》v12 §11.1–11.2；Policy 域另见 [§10](#policy-clear)，不能套用组件来源定义。组件的层 × 字段类型 allowlist 统一见 [§13](#component-operation-allowlist)。

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

**用户语言**（裁定 c；概念名与行内显示分层）：
- 物种层：**仅使用来源** / **调整** / **设置为**。
- Affinity 层：**沿用物种调整** / **沿用物种设置为**（按实际继承到的那一个操作给串）/ **仅使用当前来源**（`CLEAR`）/ **调整** / **设置为**。
- Affinity 缺省支显示的是**实际继承到了什么**，不显示泛称「沿用物种操作」；物种层没有操作时，Affinity 缺省支显示「仅使用来源」。
- 「沿用物种调整 / 沿用物种设置为」沿用的是物种层的**操作**，不是物种层的最终数值；这两支不得与「仅使用当前来源」合并成一个模糊的「恢复」。（《编辑器与 Resolve》§11.1 逐字「`absent` ＝ 跟随物种层 operation」、§11.2）
- **⚠️ 上面三条要按「两个寄存器」读，别读成「泛称被禁」**：**「沿用物种操作」是这一支的「名字」（概念层，保留）**；**行内「显示」必须给具体串**（见上一条）。⇒ **名字 ≠ 显示**：**名字保留、显示给具体串**，两者不矛盾。而「沿用物种操作」与「仅使用当前来源」**不得合并成一个模糊的「恢复」**。（记录页 §331 四、§359 ①）
- **作者可见的串一律取作者词汇**：`INHERIT` / `ADD` / `SET` / `CLEAR` 是**操作令牌**，`Override` / `Reset` 是**工程词**，两者都不是作者词；作者词＝本节上一段那五支。（《编辑器界面》§1.2「操作的用户语言」；《编辑器心智模型与 IA》§2 作者词汇表）
  - **出处边界**：《编辑器界面》§1.2 给的是操作到用户语言的映射，不得引成页上逐字禁止 `Reset`／`Override`。`Reset` 不能作作者可见词的依据是记录页命名裁定，具体动作见[卡7](contract-cards.md#autosave-status)；原校正过程由 Git 保留。

**显示**：
- 折叠态只显示：字段名、当前操作摘要、Effective Value、Diagnostic。展开态显示：当前来源、被继承的操作、本层操作、Effective Value、provenance / 算式。（本轮裁定 g；草稿 §4）
- 显式展示「来源 → 当前层操作 → 当前值」；`ADD` 与 `SET` 视觉可辨；典型三行：来源值 `0.80` · 相对调整 `-0.20` · 当前值 `0.60`。（《编辑器心智模型与 IA》§3；《编辑器界面》§1.2）
- 被替代的上级操作**只用于解释 provenance，不再参与链式计算**，且视觉降级。（本轮裁定 g；草稿 §4、§6）
- **显示约束**：不得把[§3 的整层操作替换](#component-clear)画成叠加；被替代的上层操作只解释 provenance，不参加计算。
- 已覆盖但数值与**底板**相同，**仍须读作已覆盖**（界面读记录，不按值差）。（《编辑器持久层契约》§3.5 逐字）

**durable 语义**：
- CLEAR 留记录、同值 pin 及每格唯一操作按[§3](#component-clear)。
- **「计入本层操作数」的来源核对与扫描范围见[UI取证台账](OPEN-ITEMS.md#ui-evidence)**；保留[卡2](contract-cards.md#operation-control)的既有执行投影，不将未确认的上游依据升级为 Current 规则。
- 输入控件里的临时字符串（`-`、`0.`、空）不是持久值，不覆盖上一笔 durable 值。（《编辑器界面》§1.2；《编辑器持久层契约》§7.1）

**切操作时的落盘**（本轮裁定 d）：
- 选定操作即落盘成立（《编辑器界面》§1.2 逐字把「操作 / 角色 / Source 选定」列为一次有效语义编辑、经短 debounce 原子落盘），**但「选定」须伴随一个合法 typed 值**；未成值不落盘。
  - ★ **这条 guard 的射程只到 `ADD` / `SET`** —— **只有它们带 typed 值**；**`INHERIT` / `CLEAR` 按定义没有 typed 值**，**不受本条约束**（`INHERIT` ＝ 删记录；`CLEAR` ＝ 落一条 op-only 子 patch —— 下一行那两条才是它们的边界）。
- 因此不得因为选了「调整」就写 `ADD(0)`、也不得因为选了「设置为」就写同值 `SET(当前值)`；同值 `SET` 是真实 pin，须在用户确认 typed value 后才 durable。
- local pending 编辑器可以作实现形态，但不得整体改成「必须再确认才落」。
- `INHERIT` / `CLEAR` 是明确语义动作，不做「自动保持结果」。

<a id="tier-contract"></a>
## 5. Tier

**本节保留 Tier 的完整规则与记录限定**；卡2／卡3按此读取和执行，不再重复定义。适用范围／不可反推直接核《编辑器持久层契约》v16 §3.3，档位表直接核《编辑器界面》v20 §1.1（分别为 `2026-09-21 14:34`／`17:19 +08:00`）。ADD／SET 的 Tier 形状及越档不自动转 Custom 沿既有 Owner 裁定；[固定基线卡2](https://github.com/futouyiba/HitFish-Up/blob/db97e9bb4784a8eaf2421cf88894c6d4e4beef2c/docs/review/ui-component-contract-r2/contract-cards.md#operation-control)保留 §199 ⑥① 取代旧未决形状与 §148 推断不作裁定的来源边界，本批未重读实时记录页。

- Tier 不是第三条计算轴：属 Authoring 表达，不是生产配置表字段、不是 Runtime 输入；编辑器必须在保存 / Resolve 前确定性解析为最终数值。（《编辑器与 Resolve》§2.1；《主开发需求》§6 第 3 条）
- **`ADD` 不带 `tier` 字段；`SET` 才可携 Tier，`CUSTOM` 只作 `SET` 下拉里的选项，不是缺失值哨兵。** Tier 是独立的作者元数据，适用的记录按 `{op, value, tier}` 形状携带，不因最终值相同而反推／补写。不得用伪造 `CUSTOM` tier 满足 schema。（既有裁定 a、记录页 §199 ⑥①／§154；持久层 §3.3 的组件适用边界）
- 适用面：Structure / Feeding Layer / Time Period；**Temperature 不带 `affinity_tier`**。（记录页 §174 二（Owner 直收）、§172 二 APPLY DELTA ③）
- 四档锚点与可表达范围：PREFERRED 1.00（1.00）／SUBOPTIMAL 0.60（0.50–0.75）／ACCEPTABLE 0.25（0.20–0.30）／REJECT 0.05（0.00–0.10）；Custom 可精确值。（《编辑器界面》§1.1）
- **不得从裸数值自动反推 Tier**：数字落进某档范围不等于声明该档。（《编辑器持久层契约》§3.3「不得从生产最终值反推」）
- **`SET` 值越出该档可表达范围时不自动转 `CUSTOM`**（那是静默改写作者意图）：保留档位标签 ＋ 出一个可见诊断，由作者显式改。（本轮裁定 e；《编辑器持久层契约》§3.4）

<a id="validation-autosave"></a>
## 6. 校验 × Autosave

本节是通用校验判级的完整仓内投影；卡3／卡6保留控件反馈、定位与验收，保存状态及动作见[卡7](contract-cards.md#autosave-status)。
- 三条通道分开：raw input 非法（不落 typed、不产生 durable）／typed 语义非法（可 durable 自动保存）／I/O 或 revision 冲突（写入未成功）。（《编辑器界面》§1.2、§1.4；《编辑器持久层契约》§7.1）
- 校验对象＝ resolved / Effective 值，不是 `ADD` 操作数的符号；负 `ADD` 使终值非负即合法。（《编辑器界面》§1.2；《主开发需求》§9）
- `< 0` ＝ ERROR：可自动保存（带错误继续修）、阻断 Publish、Runtime 不得接收。（《编辑器界面》§1.2；《主开发需求》§7、§9）
- `> 1` ＝ WARNING：不阻断（保存 / 校验 / Resolve / Publish 均放行），Runtime 原值消费、不 clamp；**分级靠文案与阻断性区分，不靠颜色** —— 这一侧是「红标」。（本轮裁定 b；《编辑器界面》§1.2、§1.4 与《主开发需求》§7 三处逐字）
- 不允许 runtime clamp / abs / shift / 归一 / fallback / 带符号权重修复负 Fit。（《主开发需求》§9 逐字）
- `0` 不自动等于 Gate Fail：离散 Fit ＝ `0` 时，CORE 触发 Gate、SECONDARY 不触发、IGNORED 不消费 —— 同一个 `0` 的后果由 Role 决定。（《编辑器界面》§1.1 四档表 REJECT 行逐字；记录页 §199 ④ GAP-007）

- 顶栏保存状态及其与 Validator ERROR 的区别按[卡7](contract-cards.md#autosave-status)展示；校验诊断不替代持久化结果。
- 阻断 Publish 时必须提供**可读位置**：进入校验清单，每条至少说明「对象 → 当前层 / 行 → 区域 / 组件 → 具体项」以及错误原因，使作者可沿现有稳定导航自行找到并修复。V1 **不要求**建立跨 Context 的精准跳转、Back stack、`EditorAddress / TargetRouter / RevealPlan` 或“最佳修复位置”系统。
- Diagnostic producer 不得在生成过程中丢掉渲染位置所需的已有语义信息（如 species / row 或 scope、component、item / field）；这些信息只用于派生 breadcrumb / UI 展示，不新增第二份 durable truth，也不要求新增统一 `Diagnostic.owner` 身份层。
- 已有的局部 locate / focus 能力可以保留为超集，但不是 V1 Freeze 的必要 Contract；不得为了统一导航而反向删除已有可用能力。
- 跨字段不变量的诊断指向共同语义区域并在消息中列出相关字段，不强行把错误归罪给任意单字段（例如水温边界顺序错误定位到 Temperature Profile）。
- 诊断是派生量，每次重算，不持久化为第二真相。（《编辑器持久层契约》§6.5）

## 7. 组件卡 ＋ 焦点编辑栏
- 组件卡是**摘要 ＋ 快速编辑入口**，不是只读卡：可就地改 **Source / Template**；Role 在当前 Context 对应单一 Role owner 时可就地改，multi-row Compat 只显示 Role 摘要，实际行级 mutation 由 Policy 区生产行表承接。逐字段值仍在右侧 460px 焦点编辑栏完成。（《编辑器界面》§1 导语、§1.1）
- 卡上展示：组件身份、当前 Source / Template、当前 Role 角标、继承 / 覆盖状态、诊断。（《编辑器界面》§1.1「卡片展示摘要、模板选择器、Role 角标与继承 / 覆盖状态」；冻结卡 `A①-卡1` 的「卡上 `templateName` 与闭值同源同名」「same-source pin 的『已显式固定』记号」）
- **入口与 Truth 的对应**：**前层 Source Selector（顶部 `templateRow`，每组件一个）与组件卡的来源 / Source 下拉**（**卡上这一个入口同时覆盖 Template 与 Source** —— 换模板就是换 Source 绑定）指向**同一个**组件 Recipe Source binding；**卡的 Role 控件与 Policy 区 Role 行**指向**同一个** Policy Authoring Truth。⇒ **各自「双入口、单 Truth」，不得增设第三个 mutation 面。** ⚠️ **入口叫「来源 / Source」，不叫 Template** —— 合法来源里含 `SPECIES_CONCRETE`（**它不是模板**）；**当所选来源是共享模板时，卡上以该模板名显示它**（展示层才出现 Template 字样）。⚠️ Source 在合法当前 owner 上可就地改；Role 只有在当前 Context 对应**单一 Role owner**时才提供卡上可编辑下拉。multi-row Compat 的卡上只显示 Role 摘要，Policy 区直接使用生产行表逐行编辑，不得把 row-level Role 伪装成 bucket-level 控件。两入口都不另存 durable 副本。⚠️ **两入口「同源」说的是 durable truth 同源**；**未确认的 Source 变更是 candidate（UI 态）** —— 两处可同时显示它，**但它还不是 truth**（见 §8 的 candidate → Rebase Preview → 显式确认 → 原子提交）。⚠️ **焦点编辑栏不提供 Source 下拉** —— 它只显示当前 Source 的上下文／来源说明（在那里再放一个 Source 选择器，就成了「Top Row ＋ Card ＋ Focus Editor」三个 mutation surface，**复杂度没有买到新能力**）。（《编辑器持久层契约》§8 首行「每组件一个**前层** Source 选择器」；《编辑器界面》§1 导语、§1.1、§7；《编辑器心智模型与 IA》§6、§7、§8；记录页 §172 二 KEEP、§331 裁 `R3-FIG-01`、§358 裁「入口不叫 Template」）
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
- 已归档来源的既有引用与新建限制按[§14 生命周期](#template-lifecycle-guards)；选择器显示「已归档」，不将合法既有引用标为 ERROR。（《编辑器持久层契约》§3.10；《编辑器界面》§1.1）
- 断链来源（诊断码 `BROKEN_SOURCE_REF`）：可加载（load tolerant）、显示明确的 Source Missing、ERROR ＋ 阻断 Publish、**禁止任何自动 fallback / 自动切回物种来源 / 自动挑最近似模板**，必须由作者显式选新的合法来源。（《编辑器持久层契约》§3.10；冻结卡 `A①-卡6`）

<a id="policy-profile"></a>
## 9. Profile × Spatial Opportunity Policy

**本节保留 Policy 归属与 Role 记录态的完整机制投影**；Profile 缺席、promotion 与 Setup 的完整投影在[§11](#profile-lifecycle)，Policy 操作词表／CLEAR 来源仍在[§10](#policy-clear)，落盘形状与键见[RoleControl](contract-cards.md#role-control)。Owner 裁定决定产品语义；本节是 Git Markdown 的仓内规范承接位置。本批回读《编辑器持久层契约》v16（`Last Updated 2026-09-21 14:34 +08:00`）§3.1／§3.4／§3.7，以及《编辑器界面》v20（`Last Updated 2026-09-21 17:19 +08:00`）§1.2／§1.4，未重读实时裁定记录。

- Profile 回答「这条鱼对这个环境轴是什么习性」；Role 回答「这份习性在聚合里如何被消费」。（《编辑器与 Resolve》§2.2；《编辑器心智模型与 IA》§7）
- Role 与 Profile 的变更边界按[§11](#profile-lifecycle)，不能由改变消费角色推导创建／删除或改写 Profile。
- 空间机会聚合策略有独立共享 Policy Template，payload ＝ 四个角色 ＋ `fail_env_coeff`；它是第五类 `TemplateKind`，**不是第五个 Component** —— 不扩 `ComponentType`、Runtime 仍四条件槽、不新建生产 Policy 子表。（《编辑器持久层契约》§3.6；记录页 §172 二 A）
- Policy Source 只绑物种层；**桶层没有 `policySourceOverride`**，不得虚构这类直接引用。（《编辑器持久层契约》§3.10；记录页 §172 二 B）
- 粒度必须分离：数值 override 按 **bucket**（`young / mature`，TimePeriod 不按规格 / row）；Role override 与 `fail_env_coeff` patch 按 **生产行**。同一 bucket 内不同生产行可有不同 Role / `fail_env_coeff`，Validator 不得因这些行级值不同报错。（《编辑器持久层契约》§3.4、§3.7）
- `fail_env_coeff` 不挂在某个组件卡内部；Species Context 编辑物种默认值，兼容覆盖 Context 若只有一条 production row 可直接编辑该行，若聚合多条 production rows 则在 **Policy 区的行级表**中逐行显示 / 编辑。`[0, 0.10]`，默认 `0.01`，越界 ERROR ＋ 阻断 Publish、不 silent clamp。（《编辑器界面》§1.1；《编辑器持久层契约》§3.4）
- `fail_env_coeff` 的 `ADD` 是绝对数值增量，不是百分比 / 乘数。（《编辑器持久层契约》§3.4 逐字「ADD 为绝对数值增量」）
- Editor 没有钓场上下文：不提供 Pond selector，不编辑 `baseOpportunityIntensity / isBackgroundFish / envCoeffMin`；`fail_env_coeff` 是本编辑器可编辑的习性档案字段，不是 `FishRelease` 的 `envCoeffMin`。（《编辑器界面》§6）
- 诊断归属：字段 → 字段控件；Profile → 组件卡；Policy → 聚合策略区；全局 / Publish → 顶栏 ＋ 校验清单。（冻结卡 `A①-卡6`；《编辑器界面》§1.4）

<a id="role-record-intent"></a>
**Role 记录态与 UI 派生**：
- Policy Template 的 raw Role 默认值为 `CORE`，不是 `IGNORED`，不能由实现自选缺省或留未定义；「初生默认」与作者从 IGNORED 提角色是不同事件。（《编辑器持久层契约》§3.1；记录页 §383 ADJ-07）
- 物种 Role 的 `INHERIT` 用无本层 op record 表示；选中任何具体 Role（包括与当前 Policy Template raw Role 相同的值）仍写 `SET`。回到 INHERIT 要显式删除本层 Role op，不能用选同值代替；行级 patch 与物种默认仍按不同记录／键落盘。（《编辑器持久层契约》§3.1、§3.4；完整字段见 RoleControl）
- 物种 UI 必须可区分无记录 INHERIT 与三值 SET。显示从 Species Role durable op record 是否存在派生：无记录显示为「策略模板」，有记录（含同 raw 值 SET）显示为「本层设置」；不增加第二份 durable UI state。设计证据与保存重载未核的区别见[问题台账](OPEN-ITEMS.md#species-role-ui)。

<a id="policy-clear"></a>
## 10. Role 与 Policy 的操作词表
**本节是 Policy 域 CLEAR 的完整投影**，权威为《编辑器持久层契约》v16 §3.4（同 §3 的核对版本）；裁决依据为记录页 §265 `F-04`。仅负责此域的来源与词表，记录存在性、同值意图区分沿用 [§3](#component-clear)，无值动作的落盘例外见 [§4](#field-value-control)。
- Role：物种层 `INHERIT / SET`；**生产行级** `absent / CLEAR / SET`；**永不允许 `ADD`**。（《编辑器持久层契约》§3.4）
- `fail_env_coeff`：物种层 `INHERIT / ADD / SET`；**生产行级** `absent / CLEAR / ADD / SET`。（《编辑器持久层契约》§3.4）
- `fail_env_coeff` 的作者语言按 Policy 数值字段表达：物种层＝`沿用策略模板值 / 调整 / 设置为`；生产行级＝`沿用物种配置 / 使用策略模板原始值 / 调整 / 设置为`，分别对应 absent / CLEAR / ADD / SET。它不使用 Role 的三态词表，也不虚构 row-level Policy Source。
- Policy 侧的 `CLEAR` 语义：移除继承自物种层的操作，**回到物种当前 Policy Template 的 raw 值**。（《编辑器持久层契约》§3.4）
- 该定义同时覆盖四个 Role 与 `fail_env_coeff`；`CLEAR` 不携值。**Affinity 没有 `policySourceOverride`**，不能把组件级来源 pin 的能力搬入 Policy。（《编辑器持久层契约》§3.4、§3.10）
- 行级缺省（继承物种层 Role 操作）与 `CLEAR`（回到 Policy Template raw Role）是两个不同动作，UI 必须区分：物种层作者词为「沿用策略模板 / 设置为 CORE|SECONDARY|IGNORED」；行级作者词为「沿用物种角色 / 使用策略模板原始角色 / 设置为 CORE|SECONDARY|IGNORED」。`INHERIT / absent / CLEAR / SET` 只作为 durable 令牌，不直接充当作者文案。
- Role 控件显示 **Effective Role ＋ 当前 Authoring Intent ＋ 必要 provenance**。Species Context 只编辑 Species Role。兼容覆盖若只对应一条 production row，可直接编辑该行 Role；若对应多条 production rows，组件卡只显示摘要，**Policy 区直接展开行级表**（每行明确 row identity，逐行编辑四个 Role 与 `fail_env_coeff`），不得另造隐式广播的 bucket-level Role / coeff 控件。P0 不做跨行批量 Role / `fail_env_coeff`。
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
- 三预设（晨暮型 / 昼行型 / 夜行型）是一次性批写五个字段的 `SET`：不是 Source、不是模板 identity、不进长期继承链；应用后不持久化 `presetId`，当前 Source binding 不变；覆盖确认按本节所引 §15；五个 `SET` 各自可带该预设明确的 Tier 语义；**后续单字段修改后不得再宣称仍属某预设**；模板名不进 Runtime。（《编辑器界面》§1.1；记录页 §172 二 APPLY DELTA ④）
- 预设不负责创建 Source；应用后原 Source binding 仍在（即使五项都被 `SET` 遮罩也不删除 / 弱化）。（《编辑器界面》§1.1）
- ★ **三预设那五个 `SET` 落到哪一层（ADJ-13，refine 后）**：**`target = active Recipe / Patch authoring owner`** —— **Species context ⇒ 写 Species TimePeriod Recipe 的 5 个 `SET`；Affinity / bucket context ⇒ 写当前 Affinity TimePeriod operationPatches 的 5 个 `SET`**；**五个 `SET` 同 owner、同 layer、一个 atomic batch**。
  - **不切换 authoring layer／不默认提升到 Species／不创建第三个 preset layer／不改 Source／不持久化 `presetId`／五个 `SET` 作为一个 atomic batch。**（记录页裁 **ADJ-13**）
  - ★ **若某 UI surface 本版只开放 Species authoring ⇒ 在那里自然只写 Species** —— **那是 surface capability 的后果，不是 Preset 自身拥有 Species 语义**。（★ 与 ADJ-12 同源：**三种预设是 Setup 后/中的一次性填表便利，不是 TimePeriod 独有的「Profile 创建语义」**）

<a id="temperature-behavior"></a>
**Temperature**（本包完整参数／曲线机制；具体控件见[卡3](contract-cards.md#field-value-editor)，导入前提与目标物种护栏见[卡8](contract-cards.md#template-list)）：
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
- 数值型 · 带档位（Structure / Feeding Layer / Time Period）：物种层 `ADD` / `SET`（无操作 ＝ `INHERIT`）；桶层 `absent` / `CLEAR` / `ADD` / `SET`；Tier 元数据按[§5](#tier-contract)。（《编辑器持久层契约》§3.3）
- 数值型 · 无档位（Temperature 四边界 ＋ `threshold`）：操作选项同上，Tier 适用边界按[§5](#tier-contract)。（同上；记录页 §174 二）
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
**事务分类**（《编辑器持久层契约》§6.3；记录页 §392）：只有两层，不新增第三种 durable transaction type。① 普通 semantic edit（值 / op / Role）走上述 debounce autosave，通常无 staged preview；② **staged binding / propagated mutation**：Component Source binding 与 Shared / bulk 传播类，都必须先形成 ephemeral candidate，再 Preview、显式确认、revision 核验、原子提交。

<a id="timeperiod-batch-guard"></a>
**TimePeriod Batch Overwrite Guard**（Owner 2026-09-21 裁，沿用[固定基线 §15](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/review/ui-component-contract-r2/component-contract-consolidated.md#15-跨层护栏)与[原能力裁定](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/review/ui-component-contract-r2/OPEN-ITEMS.md#L122-L123)）：Preset 不是 Source mutation，不因 ADJ-09 自动要求 staged confirm；它属于普通 semantic edit。
- target layer 没有将被覆盖的 local ops：正常 semantic edit／autosave，可展示结果，不强制确认页。
- 会覆盖已有 local ops：batch preview 列五字段 before/after、哪些 local ops 被替换、新增 Error·Warning，随后 explicit confirm ＋ atomic commit；不做 full-library impact scan。
- 五个 `SET` 是同 owner／同 layer 的一个 atomic batch；target、Source 不变及不持久化 presetId 等边界见[§12](#component-specifics)。该护栏不是第三种 durable transaction type，也不是 Source Rebase Preview。

<a id="publish-boundary"></a>
**Publish 边界**：
- 顶栏 `发布到生产配置…` **只作为入口**，进入 / 聚焦唯一 Publish 区；唯一 writeback executor 留在该区。Autosave 只表达 Editor durable state（`编辑器已保存 / 编辑器已保存 · 有错误 / 编辑器保存中… / 编辑器保存失败`），Publish 不隐式 Save，也不等同 Git commit。
- Publish 只消费**最新成功持久化 revision**；尚未成值的输入、保存失败编辑、未确认 staged candidate 均不得进入 Publish。
- Preflight 只看三项：① Editor state 已 durable；② full validation 无 blocking ERROR；③整组 Production generation 可验证且仍匹配 expected baseline。任一失败均 BLOCK。
- Generation 只作并发安全 token：mismatch / unverifiable 都 BLOCK，不 silent overwrite / auto-merge / 自动采纳 Production。成功 writeback 后重新读取**整组 Production generation**作为下一次 baseline（当前实现为 7 本工作簿同刻度身份）；partial failure 不得显示成功，也不得按 target 拼 baseline，必须先重读整组 generation。
- V1 只展示本次 Publish 的 success / failure / partial failure；不维护 `已发布 / 有未发布修改 / 与上次发布一致` 或 durable Publish History。Editor revision 冲突与 Production generation mismatch 是两类问题，不得都显示成「保存失败」。
- 本版只有一次性 Bootstrap：`Production → Bootstrap → Editor durable state`；持续反向对账 / 自动采纳 Production 不在本版。验收包含无编辑往返：Production → Bootstrap → Editor → Publish → Production 逐位一致。
- 生产侧只保存物化后的完整值 / 枚举，不保存 Source / op / patch provenance；Runtime 不做 base ＋ delta 合并。（《编辑器与 Resolve》§11.1）
- 生产投影按结构化 authoring lineage 复用，不按 payload 相等：物种层用共享模板且无有效操作 → 可复用该模板的生产 Profile；桶层完全继承物种 Recipe → 可复用物种投影；有显式 `sourceOverride` 但最终为「纯共享模板 ＋ 零操作」→ 仍可复用该模板的 Profile（显式 pin 只分叉继承关系，不强制复制行）；最终仍含任何有效操作 → 该桶自有投影。**同值 `SET` 与纯 source pin 必须区分**：同值 `SET` 阻断未来模板改值 ⇒ 自有投影；`sourceOverride` ＋ 零操作 ＝ 未来继续跟随 ⇒ 可安全复用。（《编辑器持久层契约》§3.7）
- ★ **`name` 的射程要分两层写**（原文只写「只是人类可读标签，不作 identity / join / 复用键」—— **过宽**，独立复审于 `fa96900` 报出，2026-09-21 Owner 同向裁定）：**Editor / Materializer 内部定位 → 稳定 id / key**（`name` **不作** Editor identity）；**Production XLSX 跨子表引用 → 仍按现有物理 schema 写 `targetRow.name`**。⇒ **本期不得把 XLSX 引用单元格顺手迁成 id**（那是单独的**配置表 Schema Migration**；`TimePeriod` 连数字 group id 都没有）。因此 **新增／新建的 production row `name` 必须在对应 production lookup domain 内无歧义**，collision ⇒ **BLOCK**（不 silent suffix / fallback）。行名的三级形态＝模板级（作者填，不预填）/ 物种派生级 / 桶派生级（自动生成）。（《编辑器持久层契约》§4.4）
- 不隐藏耦合：换来源不自动改 Role；改 Role 不自动换来源；Role 置 IGNORED 不自动删 Profile；重导 / 生态数据更新不自动切 Recipe Source；预设应用不产生长期预设 identity；值相等不自动转继承；同源不自动删 `sourceOverride`；payload 相等不自动合并 authoring owner；归档 / 断链来源不自动 fallback。（《编辑器持久层契约》§3.3、§3.5、§3.7、§3.10）

<a id="identity-boundaries"></a>
## 16. 负向清单
不做（画进假图等于把作者引向不存在的能力）：
- 程序开关；`if / else / return` 之类控制流编写；自定义聚合算子；自由编排 / 任意输入连线；Gate 控件 / `GatePolicy` 字段；模板共享面板的三档分级；不新增顶层空的 `Calculation Surfaces` 导航；不显示 Activity / Feeding Readiness 之类空壳；不新增第二套 Bake Editor、不新增脚本入口。（《编辑器界面》§5）
- 本版**不显示占比 / 分群的伪控件或预留字段**，也不提供对应编辑入口；若需要说明边界，只用普通说明文字表达「本版不实现 Mode Share / Routing」。未来 Routing 另行设计，不从当前 Compat UI 反推其参数形态。
- 桶不是真正的 Engagement Mode；Runtime 无 EngagementMode identity，不得据 UI 名称另建 durable 的 Engagement Mode 身份 / 注册表 / 模式级 Concrete 来源。（《编辑器界面》§5；《编辑器与 Resolve》§11.1；记录页 §172 二 KEEP）
  - **业务概念与 durable identity 分离**（记录页 §385，ADJ-08＝`C_SPLIT_REGISTERS`）：`Engagement Mode`／中鱼习性模式是 Simplified Production V0 的正式业务概念；B P0 不实现 Mode Share／Routing。物理 durable key 为 `FishEnvAffinityRef`；`FishEngagementModeCompat` 是对 Affinity 的 mode-like authoring projection／兼容壳；Runtime／production 无独立 `EngagementMode` identity。业务概念不能充当另一套物理身份。
  - `sourceOverride` 的物理键写作 `(fishEnvAffinityRef, component)`；若 schema 字段名为 `owner_ref`，则 `owner_ref := FishEnvAffinityRef`。不留抽象的 `owner` 让实现猜身份；原页侧依据为 CT §1.1／§3.3、RS §11.1，Runtime 禁令与 UI §5／RS §7／IA §8 相容。逐页改写经过由 Git 保留。
- **Quality Stable Data 页面本版不开放**（入口置灰、不展示/编辑品质自身字段）；**不新建品质模板库、不把品质当作第五个习性组件**。StockRelease / Production 中既有的 Quality＋`FishEnvAffinityRef` 引用仅作为当前 Editor 会话载入快照只读投影到习性档案上下文；可按 Quality 聚合显示，但不新增全局 Quality→Affinity identity。本版不提供关联、删除、重分配、占比或 Routing 编辑。
- 组件卡不承担逐字段 `ADD / SET / CLEAR` 编辑（逐字段值在焦点编辑栏完成）；不给组件卡 Source / Role 另建 durable state；不把 Effective Value 当编辑真相存储；不为视觉一致强迫所有字段支持 `ADD`；不为结构对称给品质造模板；不按「当前数值相同」跨无关谱系合并生产行。（《编辑器界面》§1 导语、§7；《编辑器心智模型与 IA》§8）

---

## 17. 两份不一致

旧稿比较、撤回过程与历史探针见[固定基线 §17](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/component-contract-consolidated.md#17-两份不一致)，不作为当前规则或本轮测量。现行入口：字段交互 [§4](#field-value-control)、Tier [§5](#tier-contract)、组件卡 [§7](#7-组件卡--焦点编辑栏)、Policy CLEAR [§10](#policy-clear)；具体替代标签场景见[卡2](contract-cards.md#operation-control)。未决命名的处置只在台账维护。

<a id="18-未核--待裁"></a>
## 18. 取证与现行入口

未核事项、下一步及完整 UI 细则清单只在[问题台账](OPEN-ITEMS.md#remaining-evidence)维护；原 **§18.5** 的完整清单已移至[UI 取证入口](OPEN-ITEMS.md#ui-evidence)，此处不再维护第二份动态状态。旧读数与已收口经过见[固定 §18](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/component-contract-consolidated.md#18-未核--待裁)。

物种／Affinity 字段语言见[§4](#field-value-control)，校验颜色见[§6](#validation-autosave)，Structure 动态字段与数据查表键的区别见[卡3](contract-cards.md#field-value-editor)；命名边界仍在 §19。

<a id="19-待命名--需裁定"></a>
## 19. 命名边界

沿用[固定基线 §19](https://github.com/futouyiba/HitFish-Up/blob/db97e9bb4784a8eaf2421cf88894c6d4e4beef2c/docs/review/ui-component-contract-r2/component-contract-consolidated.md#19-待命名--需裁定)的命名边界；旧“页面不存在／零命中”是当时取证，不作为本批的新全页扫描结论。需要新名时仍须裁定，不能由下游另造产品名、记录或身份。

1. 正文控件使用 `FieldValueControl`；草稿 `FieldValueRow` 不替代它。
2. `BOUND_SOURCE / FOLLOW_SPECIES_SOURCE / PIN_SOURCE(sourceRef)` 仅是旧草稿串；按现行 Source 交互及 durable `sourceOverride` 字段读取。
3. `tieredNumeric / numericRelative / enumAbsolute` 是草稿能力名；字段类别按 §13。
4. 旧16组件／区域名的完整列表保留在固定历史，不将这些草稿名统一晋升为页面规定。
5. `profileCanStartAbsent / ModeConcreteSource / BootstrapSurface / DirectReferenceCount / localOperationCount` 沿原未核边界；`completeValue` 的现有用法见持久层 §3.7，不因清理改名。
6. 卡2 `Operation Control`／卡3 `Field Value Editor` 是卡片编号名；§4 的两个交互职责不因此成为两个新产品控件名。

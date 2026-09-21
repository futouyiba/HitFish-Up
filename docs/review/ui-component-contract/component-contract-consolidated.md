# 组件契约｜编辑器 UI Component Contract（现行）

本文只写现行规定。出处写作《页名》§N、记录页 §N 或 冻结卡 `A①-卡N` / `A②-卡N`；查不到出处的条目列在末节「未核 · 待裁」，不进正文。标（本轮裁定）的条目＝本轮已定口径，其依据随条给出。

## 1. 产品拓扑与三栏
- 三栏＝对象导航 ｜ 上下文总览 ｜ 焦点编辑。几何：250 ＋ 890 ＋ 460 ＋ 边距 ＝ 1680。（《编辑器界面》§9.1；《编辑器心智模型与 IA》§3）
- 左栏三类入口：FISH（Species → 习性 / 品质）／TEMPLATES（五类）／SPECIES PRESETS。物种预置＝一次性写五个来源绑定（四组件 ＋ Policy），**不是父节点**。（《编辑器心智模型与 IA》§3、§4）
- 中栏 Context 与右栏 Focus **不是同一个导航状态**：允许短暂 detached，但必须显式提示（右栏标题明确对象身份 ＋ 低成本「切回当前上下文」），不得让作者误以为右栏仍在编辑中栏对象。detached 只是 UI 导航状态，不产生新的 durable authoring entity。（《编辑器心智模型与 IA》§3 逐字「切换上下文不销毁编辑现场」）
- 中栏与右栏不得形成两套重复编辑器。（《编辑器界面》§1 导语：逐字段值编辑在焦点编辑栏完成）
- 控件名用现行页已经落下的 `FieldValueControl`（承载 Field ＋ Effective Value ＋ optional Tier ＋ Local Operation ＋ Diagnostic）。（裁定 f；《编辑器界面》§1。草稿另有叫法，见 §19）

## 2. Structure 竖切
- 第一条竖切路径：Species → Structure → 共享模板 → Species ADD → Affinity sourceOverride → SET / CLEAR → autosave → Resolve Preview → materialize。选型依据：结构在 allowlist 里只允许共享模板、查表取值无跨字段约束。（记录页 §164）
- 切片刻画的样例族：Species ＋ 共享模板 ＋ ADD ／ Affinity 沿用物种操作 ／ Affinity 固定另一来源 ＋ 继承物种操作 ／ 同源显式 pin ／ CLEAR ／ 本层 ADD ／ SET ＋ Tier ／ 换源 Rebase Preview ／ Effective < 0 → ERROR ＋ autosave ＋ Publish 阻断 ／ Effective > 1 → WARNING 放行 ／ 断链来源 ／ 已归档来源的既有引用 ／ Publish 阻断清单与定位。各状态的规定见本文对应节。（记录页 §164；各条出处见 §3–§8）

## 3. Source × Operation 正交
- 物种层操作：`ADD` / `SET`，无操作 ＝ `INHERIT`（无记录）。桶 / 习性档案层操作：patch 缺省（继承物种层）/ `CLEAR` / `ADD` / `SET`。（《编辑器持久层契约》§3.3；《编辑器与 Resolve》§11.1）
- Source ≠ Operation：换 Source 保留既有操作，改操作保留 Source。（记录页 §172「KEEP」；《编辑器与 Resolve》§11.3）
- 桶层 `ADD / SET` **替换**物种层操作，不形成第三层叠加。（《编辑器与 Resolve》§11.1 逐字「不是叠第三层 delta」；《编辑器持久层契约》§3.3）
- Resolve（**按层分两支**；本节自记录页 §270 更正 —— 原写法把两种「缺省」混成了一个）：**物种层**无操作（`INHERIT` ＝ 无记录）⇒ **直接用来源值**；**桶 / 习性档案层** patch `absent` ⇒ **跟随物种层 operation**（物种层也无操作时，才落到来源值）—— **`absent` 不是「用来源值」**；`CLEAR` ⇒ **移除继承的 operation、回到当前 Effective Source 原值**（**与 `absent` 是两个不同动作**）；`ADD` ＝ **该层的有效来源值**（**`SHARED_TEMPLATE` 的模板值** 或 **`SPECIES_CONCRETE` 的值**）＋ delta；`SET` ＝ 绝对值 —— **基准是「这一层挂的那个来源的值」，不要求该来源是共享模板**（记录页 §288 据 `CXR-04` 更正：原写「该层所挂模板值」**会把 `SPECIES_CONCRETE` 这个合法来源排除在外**；而 §8 明定物种层 Temperature 的来源可以是 `SHARED_TEMPLATE | SPECIES_CONCRETE`、且 Concrete「不进模板清单」）。（《编辑器与 Resolve》§11.1、§11.2 逐字：「`absent` ＝ 跟随物种层 operation」／「`CLEAR` ＝ 移除继承的 operation、回到当前 Effective Source 原值」／两者「不得合并成一个模糊的『恢复』」）
- 桶层 `sourceOverride` ＝ 固定 Source Choice，不冻结配置：pin 之后 patch 仍缺省时仍继承物种层操作；`sourceOverride` 不自动 SET 全部字段、不清既有操作；解除 pin ＝ 删除 `sourceOverride`，重新跟随物种层 Source。（《编辑器持久层契约》§3.3）
- same-source pin 是真实 authoring intent：桶层 `sourceOverride` 与物种层 Source 相同时也不自动移除。（《编辑器持久层契约》§3.3；记录页 §172「KEEP」）

## 4. 字段控件（`FieldValueControl`）
**拆成两个交互面**（选哪个动作 / 敲什么数）；卡2（Operation Control）与卡3（Field Value Editor）的拆分不改 —— 它们拆的是控件职责，与「UI 上是否并成一行」是两件事。（本轮裁定 f；冻结卡 `A①-卡2`、`A①-卡3`）

**操作选项 ＝ 层 × 字段类型 两把筛子**（《编辑器持久层契约》§3.3；冻结卡 `A①-卡2`）：
- 层决定有没有 `CLEAR`：桶 / 习性档案层才有，物种层没有。
- 字段类型决定有没有 `ADD`：数值项才有；枚举绝对值项没有。

**用户语言**（裁定 c；初版被 commit 侧证据修正，见 §17.1）：
- 物种层：**仅使用来源** / **调整** / **设置为**。
- Affinity 层：**沿用物种调整** / **沿用物种设置为**（按实际继承到的那一个操作给串）/ **仅使用当前来源**（`CLEAR`）/ **调整** / **设置为**。
- Affinity 缺省支显示的是**实际继承到了什么**，不显示泛称「沿用物种操作」；物种层没有操作时，Affinity 缺省支显示「仅使用来源」。
- 「沿用物种调整 / 沿用物种设置为」沿用的是物种层的**操作**，不是物种层的最终数值；这两支不得与「仅使用当前来源」合并成一个模糊的「恢复」。（《编辑器与 Resolve》§11.1 逐字「`absent` ＝ 跟随物种层 operation」、§11.2）
- 不向作者暴露 `CLEAR` / `Override` / `Reset` 等工程词。（《编辑器界面》§1.2 只给四词用户语言）

**显示**：
- 折叠态只显示：字段名、当前操作摘要、Effective Value、Diagnostic。展开态显示：当前来源、被继承的操作、本层操作、Effective Value、provenance / 算式。（本轮裁定 g；草稿 §4）
- 显式展示「来源 → 当前层操作 → 当前值」；`ADD` 与 `SET` 视觉可辨；典型三行：来源值 `0.80` · 相对调整 `-0.20` · 当前值 `0.60`。（《编辑器心智模型与 IA》§3；《编辑器界面》§1.2）
- 被替代的上级操作**只用于解释 provenance，不再参与链式计算**，且视觉降级。（本轮裁定 g；草稿 §4、§6）
- **不许把「替换」画成「叠加」**（按层分写；本行自记录页 §292 更正 —— 原句是草稿话、其出处撑不住它）：**每层每字段最多一个最终 operation**（**不允许 `ADD+ADD`／`SET+ADD` 之类的链**）；**覆盖是整层替换、不是叠加**：某桶对该项一旦自己表达，**底板那一层对该项整个不生效**。（《编辑器持久层契约》**§3.3** 逐字，L456／L457；另见《编辑器心智模型与 IA》§1 同规则的自行表述）
- 已覆盖但数值与**底板**相同，**仍须读作已覆盖**（界面读记录，不按值差）。（《编辑器持久层契约》§3.5 逐字；本行自记录页 §292 更正：原写「与来源相同／仍读作」—— **换了物名（底板→来源）＋掉了「须」**）

**durable 语义**：
- `CLEAR` 尽管 Effective Value 可能等于来源原值，**仍是明确的 durable 本层操作** —— 《编辑器持久层契约》§3.3 `op` 行逐字：`INHERIT` ＝ **无记录**、`CLEAR` **不是第三种数值调整** ⇒ **`CLEAR` 有记录**。⚠️ **「计入本层操作数」这一点属 UI 展示项、页面无出处**（§18 未核项 5 已登记；卡片层依据＝冻结卡 `A①-卡2`）。（本行自记录页 §292 更正出处：原引「§3.3 `op` 行」**撑不住后半句**）
- 每层每字段最多一个最终操作；编辑＝替换当前格；同值 `SET` 仍是 pin、仍留记录。（《编辑器持久层契约》§3.3、§3.5）
- 输入控件里的临时字符串（`-`、`0.`、空）不是持久值，不覆盖上一笔 durable 值。（《编辑器界面》§1.2；《编辑器持久层契约》§7.1）

**切操作时的落盘**（本轮裁定 d）：
- 选定操作即落盘成立（《编辑器界面》§1.2 逐字把「操作 / 角色 / Source 选定」列为一次有效语义编辑、经短 debounce 原子落盘），**但「选定」须伴随一个合法 typed 值**；未成值不落盘。
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
- 三处入口写同一份 Authoring Truth：卡的 Source 下拉与焦点编辑栏的 Source 选择器指向同一个组件 Recipe Source binding；卡的 Role 下拉与 Policy 区 Role 行指向同一个 Policy Authoring Truth。**双入口、单 Truth，不得改成单入口**。（《编辑器界面》§7；《编辑器心智模型与 IA》§6；记录页 §172 二 KEEP）
- 卡的 Source / Role 不得另建一套 durable state。（《编辑器界面》§7；《编辑器心智模型与 IA》§8）
- 字段行**原地展开**，不设二级 drawer。（本轮裁定 g；页面只规定 2 列紧凑控件与折叠栏位）

## 8. Source 选择器 ＋ Rebase Preview
- 每组件一个前层 Source 选择器；桶（覆盖层）另有「跟随物种」；温度多一项「当前物种生态数据」（存在时）。（《编辑器界面》§1.1；《编辑器与 Resolve》§11.3）
- 可选来源矩阵（**按层分写**；本节自记录页 §271 更正 —— 原写法**层次无关**，会被读成桶层也列 Concrete）：**前层（物种层）** —— Temperature ＝ `SHARED_TEMPLATE | SPECIES_CONCRETE`，Structure / Feeding Layer / Time Period ＝ 仅 `SHARED_TEMPLATE`；**桶（覆盖层）** —— **所有组件都只有 `SHARED_TEMPLATE` ＋「跟随物种」**，**不列 `SPECIES_CONCRETE`**（**连当前物种的也不列** —— 要引用当前物种的 Concrete，走「跟随物种」）。**任何层都不得 pin 非当前物种的 Concrete。**（《编辑器持久层契约》§3.3；《编辑器与 Resolve》§11.3 逐字「桶层另有「跟随物种」选项，**不把任何物种的 Concrete 当通用可选项**」；冻结卡 `A①-卡1`）
- `SPECIES_CONCRETE` 属当前物种：identity ＝ `(speciesId, componentType)`，不进模板清单、不可被其它物种引用；不得 pin 另一物种的 Concrete。（《编辑器持久层契约》§3.3；记录页 §172 二）
- 换 Source 是高影响动作：候选来源 → before / after Resolve → **Rebase Preview** → 显式确认 → 原子提交。禁止为保持旧 Effective Value 自动生成 `SET`。（《编辑器与 Resolve》§11.3；《编辑器界面》§1.1；《编辑器持久层契约》§3.10）
- Preview 至少区分：最终结果变化、结果未变但被本层 `SET` / 操作遮罩、新增 Error、新增 Warning。**被遮罩 ≠ 无影响。**（《编辑器持久层契约》§3.7「SET-masked 可不变」；冻结卡 `A②-卡10`、`A②-卡11`；记录页 §172 二 APPLY DELTA ⑦）
- 已归档来源：既有 durable 引用继续合法、继续 Resolve / Publish，选择器显示「已归档」，不允许新建引用，普通 picker 隐藏 / 降级，不视为 ERROR。（《编辑器持久层契约》§3.10；《编辑器界面》§1.1）
- 断链来源：可加载（load tolerant）、显示明确的 Source Missing、ERROR ＋ 阻断 Publish、**禁止任何自动 fallback / 自动切回物种来源 / 自动挑最近似模板**，必须由作者显式选新的合法来源。（《编辑器持久层契约》§3.10；冻结卡 `A①-卡6`）

## 9. Profile × Spatial Opportunity Policy
- Profile 回答「这条鱼对这个环境轴是什么习性」；Role 回答「这份习性在聚合里如何被消费」。（《编辑器与 Resolve》§2.2；《编辑器心智模型与 IA》§7）
- 改 Role **不创建 / 不删除 Profile、不改 Profile 数值**。（《编辑器持久层契约》§3.4；界面 §1.2「Role 三态互斥」）
- 空间机会聚合策略有独立共享 Policy Template，payload ＝ 四个角色 ＋ `fail_env_coeff`；它是第五类 `TemplateKind`，**不是第五个 Component** —— 不扩 `ComponentType`、Runtime 仍四条件槽、不新建生产 Policy 子表。（《编辑器持久层契约》§3.6；记录页 §172 二 A）
- Policy Source 只绑物种层；**桶层没有 `policySourceOverride`**，不得虚构这类直接引用。（《编辑器持久层契约》§3.10；记录页 §172 二 B）
- 粒度必须分离：数值 override 按 **bucket**（`young / mature`，TimePeriod 不按规格 / row）；Role override 按 **生产行**。同一 id 组合的不同行可有不同 Role，Validator 不得因 Role 不同报错。（《编辑器持久层契约》§3.4、§3.7）
- `fail_env_coeff` 属档案级、不挂在某个组件卡内部；`[0, 0.10]`，默认 `0.01`，越界 ERROR ＋ 阻断 Publish、不 silent clamp。（《编辑器界面》§1.1；《编辑器持久层契约》§3.4）
- `fail_env_coeff` 的 `ADD` 是绝对数值增量，不是百分比 / 乘数。（《编辑器持久层契约》§3.4 逐字「ADD 为绝对数值增量」）
- Editor 没有钓场上下文：不提供 Pond selector，不编辑 `baseOpportunityIntensity / isBackgroundFish / envCoeffMin`；`fail_env_coeff` 是本编辑器可编辑的习性档案字段，不是 `FishRelease` 的 `envCoeffMin`。（《编辑器界面》§6）
- 诊断归属：字段 → 字段控件；Profile → 组件卡；Policy → 聚合策略区；全局 / Publish → 顶栏 ＋ 校验清单。（冻结卡 `A①-卡6`；《编辑器界面》§1.4）

## 10. Role 与 Policy 的操作词表
- Role：物种层 `INHERIT / SET`；桶层 `absent / CLEAR / SET`；**永不允许 `ADD`**。（《编辑器持久层契约》§3.4）
- `fail_env_coeff`：物种层 `INHERIT / ADD / SET`；桶层 `absent / CLEAR / ADD / SET`。（《编辑器持久层契约》§3.4）
- Policy 侧的 `CLEAR` 语义：移除继承自物种层的操作，**回到物种当前 Policy Template 的 raw 值**。（《编辑器持久层契约》§3.4）
- 桶层缺省（继承物种层操作）与 `CLEAR`（回到 Policy Source 原值）是两个不同动作，UI 必须区分。（《编辑器持久层契约》§3.4；《编辑器与 Resolve》§11.2）
- 不因最终值 / 枚举相等自动推断 inherit、CLEAR 或 SET。（《编辑器持久层契约》§3.5、§3.3）

## 11. Profile 生命周期
- Role ＝ IGNORED 不删除 Profile；本版不提供通用的「删除组件 Profile」动作。（《编辑器持久层契约》§3.3；界面 §1.4）
- Time Period 支持合法空态（Role ＝ IGNORED ＋ Profile 缺省）；**激活 CORE / SECONDARY 不自动生成 Profile**，生成是显式动作。（《编辑器界面》§1.2；记录页 §199 ⑥③）
- 激活 CORE / SECONDARY 而未生成所需 Profile 时，**必须当场呈现为可见校验态**，不得让作者停在无提示的非法态；判级仍按上游（CORE / SECONDARY 缺必需 Profile ＝ 阻断）。（《编辑器界面》§1.4；记录页 §199 ⑥③）
- 不得创建 required Source / identity 为 null 的半成品记录。（《编辑器持久层契约》§3.7 四件之 1）

## 12. Feeding Layer / Time Period / Temperature
**Feeding Layer**：SURFACE / MIDDLE / BOTTOM 三项最终系数，复用数值型项的同一套能力，不新增组件类型。（《编辑器界面》§1.1；《编辑器持久层契约》§3.3）

**Time Period**：
- 五段 DAWN / MORNING / AFTERNOON / DUSK / NIGHT；未配置时显示合法空态，不置灰。（《编辑器界面》§1.1）
- 三预设（晨暮型 / 昼行型 / 夜行型）是一次性批写五个字段的 `SET`：不是 Source、不是模板 identity、不进长期继承链；应用后不持久化 `presetId`，当前 Source binding 不变；覆盖已有本层操作时须 batch preview ＋ 显式确认；五个 `SET` 各自可带该预设明确的 Tier 语义；**后续单字段修改后不得再宣称仍属某预设**；模板名不进 Runtime。（《编辑器界面》§1.1；记录页 §172 二 APPLY DELTA ④）
- 预设不负责创建 Source；应用后原 Source binding 仍在（即使五项都被 `SET` 遮罩也不删除 / 弱化）。（《编辑器界面》§1.1）

**Temperature**：
- 6 参数 ＋ 连续曲线；同图显示 `temp_threshold`；另有「从钓鱼元素周期表导入」入口。（《编辑器界面》§1.1）
- 字段能力：`acceptMin / favMin / favMax / acceptMax / threshold` ＝ 数值型项（无档位）；`falloff_shape`（项名位 `falloff`）＝ 枚举绝对值项。（《编辑器持久层契约》§3.3；记录页 §175 六.2）
- **P0 曲线只读、不 drag-author**；6 个数值参数仍按项编辑。（记录页 §199 ⑥②；冻结卡 `A①-卡3`）
- 跨字段不变量：`accept ≤ fav`（四边界链）；相等合法；非法组合可 durable 保存但阻断 Publish。（《主开发需求》§7；记录页 §199 ④ GAP-008）
- `temp_threshold` 不改变曲线形状，只作 CORE 的 Gate 阈值。（记录页 §199 ④ GAP-010 引《配置表与校验》§5；《编辑器界面》§1.1）
- 跨字段非法时禁止 silent repair：不自动排序四个边界、不交换字段身份、不 clamp 到相邻边界、不把作者输入静默改成「合法值」；曲线区不得伪造一条自动修正后的曲线。（《主开发需求》§9；《编辑器持久层契约》§7.1）
- 生态数据重导只更新 Concrete Source 本身，不落成 tuning 操作、不自动切换当前 Recipe Source；研究事实修正走更新来源，游戏调参保持来源、写物种层操作。（《编辑器持久层契约》§3.3）

## 13. 字段能力表
（页面上只有「数值型项 / 枚举绝对值项」两种说法；草稿另起了三个名，见 §19）
- 数值型 · 带档位（Structure / Feeding Layer / Time Period）：物种层 `ADD` / `SET`（无操作 ＝ `INHERIT`）；桶层 `absent` / `CLEAR` / `ADD` / `SET`；`SET` 可携带 `affinity_tier`。（《编辑器持久层契约》§3.3）
- 数值型 · 无档位（Temperature 四边界 ＋ `threshold`）：同上；Temperature 不带 `affinity_tier`。（同上；记录页 §174 二）
- 枚举绝对值（`falloff_shape`，项名位 `falloff`）：物种层 `SET`（无操作 ＝ `INHERIT`）；桶层 `absent` / `CLEAR` / `SET`；**不得 `ADD`**。（《编辑器持久层契约》§3.3 逐字「枚举绝对值不得 ADD」）
- 层 × 类型的交集读法见 §4。（冻结卡 `A①-卡2`）

## 14. 模板工作区与模板生命周期
- 五类 Live Template：Temperature / Structure / Feeding Layer / Time Period / Spatial Opportunity Policy。（《编辑器心智模型与 IA》§4；《编辑器持久层契约》§3.6）
- 模板是**完整值资产**：operation 只存在于物种 Recipe 与桶 patch 上。（《编辑器持久层契约》§3.3、§3.7）
- 两个入口、一个焦点编辑器：从组件卡钻入（中栏保持鱼上下文）与从模板库进入（中栏切到模板上下文）复用同一个模板值编辑器。（《编辑器心智模型与 IA》§4；《编辑器界面》§7）
- 平铺、可滚动、默认按引用量排序；中文 / 英文别名可编辑；source name 只读且不作键。（《编辑器界面》§7）
- 关联一律按 id；别名属 editor-state；不把 inheritance lineage 编进生产行 name。（《编辑器持久层契约》§3.6、§4.4；《编辑器界面》§1.2）
- 「从当前鱼提取模板」**只创建 Template Asset**：不改当前鱼 Source、不清既有操作、不把 Recipe 折成新模板引用（即使 payload 完全相同）；要改 Source 须另走 Source Change ＋ Rebase Preview。（《编辑器界面》§7 逐字；记录页 §172 二 APPLY DELTA ⑤）
- 生命周期 `ACTIVE / ARCHIVED` 两态：归档后既有引用继续 Resolve / Publish，不允许新建引用、不允许直接改完整值，可查看引用 / Replace References / Restore；要改先 Restore。归档模板从普通选择器隐藏 / 降级。（《编辑器持久层契约》§3.10）
- 硬删除仅当直接引用集为空；`Archive` 不自动改引用 / 不 fallback / 不自动找相似 / 不自动复制 payload；归档 ≠ 可删。（《编辑器持久层契约》§3.10）
- 改模板完整值是高影响动作：candidate → Impact Preview → 显式确认 → 原子提交 → 重新 Resolve → 物化受影响的生产投影。（《编辑器持久层契约》§3.10）
- 影响面四项数：直接引用数 / Effective consumer 数 / 最终结果变化数 / 新增 Error·Warning —— **四个可以互不相同的数字**。（《编辑器持久层契约》§3.10；《编辑器界面》§1.1；记录页 §208）
- Replace References 只改**直接引用集**；禁止给经继承消费的下游自动写 `sourceOverride`；不为保旧值生成 `SET`；现有 `ADD / SET / CLEAR` 全部保留；影响展示用重新 Resolve 后的结果，不是只 diff 两个模板 payload。（《编辑器持久层契约》§3.10；《编辑器与 Resolve》§11.3；冻结卡 `A②-卡11`）
- 正常传播不给每个消费者制造待复核债；只有真实诊断 / 复核条件才进待复核。（《编辑器心智模型与 IA》§5；《编辑器界面》§1.1）
- 模板 → 模板的实时继承不支持；clone / save-as 后是独立模板；分类 / 族只用于分类与推荐，不构成继承父节点。（《编辑器持久层契约》§3.6；《编辑器心智模型与 IA》§4）

## 15. 跨层护栏
- Editor durable state 存作者意图（Source binding / `sourceOverride` / 物种操作 / 桶 patch / Role 与 Policy / 模板完整值 / identity 与生命周期），**不把 Effective / resolved 值当第二份可编辑真相**；Effective、provenance、诊断、影响结果都是派生。（《编辑器持久层契约》§3.3、§6.5；《编辑器界面》§1.3）
- 自动保存：一次有效语义编辑 → 内存 typed 状态 → 短 debounce 合并 → 原子持久化；无常驻 Save；高影响动作（换来源 / 改模板完整值 / 重导 / 时段批量预设 / Replace References）走 prepare → Preview → 显式确认 → 一次原子提交；预览缓冲是短命 UI 状态，不落成草稿实体。（《编辑器界面》§1.2、§7；《编辑器持久层契约》§3.10）
- Publish 只读取已成功持久化的 revision；尚未成值的输入不参与 Publish；未确认的高影响候选不得被当成 durable truth。（《编辑器界面》§1.1；《编辑器持久层契约》§6.3）
- revision 冲突＝乐观检测：commit 只在预期 revision 仍匹配时写入，禁止 last-write-wins、禁止静默 auto-merge，进入重载 / 对比 / 对账路径。（《编辑器界面》§1.2；《编辑器持久层契约》§6.3）
- 「生产配置外部变化」与「Editor State revision 冲突」是两类不同问题，不得都显示成「保存失败」。（《编辑器持久层契约》§6.4、§6.5；《编辑器界面》§9.2）
- 本版只有一次性 Bootstrap：`Production →（一次性 Bootstrap）→ 初始化 editor durable state → 此后 editor durable state 是 authoring truth`；持续的批量反向对账 / 采纳生产值**不在本版**，只给只读诊断。（《编辑器持久层契约》§6.5；《编辑器界面》§9.2）
- 往返冒烟测试＝本版验收：Production → Bootstrap → Editor → 不做任何编辑 → Publish → Production，应逐位一致。（记录页 §164）
- 生产侧只保存物化后的完整值 / 枚举，不保存 Source / op / patch provenance；Runtime 不做 base ＋ delta 合并。（《编辑器与 Resolve》§11.1）
- 生产投影按结构化 authoring lineage 复用，不按 payload 相等：物种层用共享模板且无有效操作 → 可复用该模板的生产 Profile；桶层完全继承物种 Recipe → 可复用物种投影；有显式 `sourceOverride` 但最终为「纯共享模板 ＋ 零操作」→ 仍可复用该模板的 Profile（显式 pin 只分叉继承关系，不强制复制行）；最终仍含任何有效操作 → 该桶自有投影。**同值 `SET` 与纯 source pin 必须区分**：同值 `SET` 阻断未来模板改值 ⇒ 自有投影；`sourceOverride` ＋ 零操作 ＝ 未来继续跟随 ⇒ 可安全复用。（《编辑器持久层契约》§3.7）
- 生产行 name 只是人类可读标签，不作 identity / join / 复用键；行名的三级形态＝模板级（作者填，不预填）/ 物种派生级 / 桶派生级（自动生成）。（《编辑器持久层契约》§4.4）
- 不隐藏耦合：换来源不自动改 Role；改 Role 不自动换来源；Role 置 IGNORED 不自动删 Profile；重导 / 生态数据更新不自动切 Recipe Source；预设应用不产生长期预设 identity；值相等不自动转继承；同源不自动删 `sourceOverride`；payload 相等不自动合并 authoring owner；归档 / 断链来源不自动 fallback。（《编辑器持久层契约》§3.3、§3.5、§3.7、§3.10）

## 16. 负向清单
不做（画进假图等于把作者引向不存在的能力）：
- 程序开关；`if / else / return` 之类控制流编写；自定义聚合算子；自由编排 / 任意输入连线；Gate 控件 / `GatePolicy` 字段；模板共享面板的三档分级；不新增顶层空的 `Calculation Surfaces` 导航；不显示 Activity / Feeding Readiness 之类空壳；不新增第二套 Bake Editor、不新增脚本入口。（《编辑器界面》§5）
- 占比 / 比例 与 分群逻辑两处只以禁用占位行呈现（字段位在、控件不在），不提供编辑控件；不得据此宣称本版已实现 Mode Share / Routing。（《编辑器界面》§5、§1.2）
- 桶不是真正的 Engagement Mode；Runtime 无 EngagementMode identity，不得据 UI 名称另建 durable 的 Engagement Mode 身份 / 注册表 / 模式级 Concrete 来源。（《编辑器界面》§5；《编辑器与 Resolve》§11.1；记录页 §172 二 KEEP）
- 品质页本版不开放（入口置灰、不展示品质字段）；不新建品质模板库、不把品质当作第五个习性组件。（《编辑器界面》§0、§2）
- 组件卡不承担逐字段 `ADD / SET / CLEAR` 编辑（逐字段值在焦点编辑栏完成）；不给组件卡 Source / Role 另建 durable state；不把 Effective Value 当编辑真相存储；不为视觉一致强迫所有字段支持 `ADD`；不为结构对称给品质造模板；不按「当前数值相同」跨无关谱系合并生产行。（《编辑器界面》§1 导语、§7；《编辑器心智模型与 IA》§8）

---

## 17. 两份不一致
逐条给两侧逐字与判断依据；不调和、不静默丢弃。

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
   - 判断 —— **裁在 commit 侧（射程更明确的一侧）**。两个动作不参与 pending 机制；并按裁定 d 补上「须伴随一个合法 typed 值」这一条。一句判据：paste 未涉 = 留白，不是相反主张，取写明射程的一侧不会丢东西。
7. **commit 自己记录的途中收敛（Card 只读 → 可快速编辑）**
   - commit §18.1 逐字：「第三次复核后确认：此前把 Card 收窄为只读摘要，是本轮中途产生的错误收敛，**不应进入集成**」；§22.4/§7 同向（「ComponentCard 是摘要 + 快速编辑入口，不是只读卡」）。
   - paste 不涉及组件卡。
   - 判断 —— **裁在 commit 侧（可快速编辑）**。这一条是 commit 自己推翻过的东西；正文取「可快速编辑」侧（§7），「只读卡」形态不进正文。一句判据：《编辑器界面》§1 导语（逐字段值编辑在焦点编辑栏完成，卡仍可就地改模板与角色）与 §7「双入口、单 Truth」。

## 18. 未核 · 待裁
1. **物种层缺省支的用户语言「仅使用来源」与现行页面相抵**：现行《编辑器界面》§1.2 与《编辑器心智模型与 IA》§2 逐字都是「跟随（INHERIT）」／「跟随」；本轮裁定 c 取「仅使用来源」。正文按裁定写；落页时须连动改这两页（含冻结卡 `A①-卡2` 的同一句）。
2. **Affinity 缺省支与 `CLEAR` 的用户语言未落页**：新形态的四串（「沿用物种调整」「沿用物种设置为」「仅使用当前来源」，以及物种层的「仅使用来源」）在本轮六个页面与记录页 0 命中（探针作用域见末行）；页面现文仍是「跟随物种配置」与「恢复为来源值」（《编辑器界面》§1.2、《编辑器心智模型与 IA》§2、冻结卡 `A①-卡2`）。判据成立（《编辑器与 Resolve》§11.1 逐字「`absent` ＝ 跟随物种层 operation」；§11.2 逐字把「恢复」判为模糊词）。落页归需求页写入者。
3. **正文里出现的页面不存在串，已一律清出**：清出的清单与仍需命名的项集中在 §19。
4. **commit 的 16 个组件名清单**页面上没有对应名，已移入 §19。
5. **无页面出处的 UI 细则**（正文未收）：卡上「本层操作数 / 诊断数 / profile presence / source health」四个展示项（页面只逐字列了摘要、模板选择器、Role 角标、继承 / 覆盖状态）；结构编辑面的筛选用「全部 / 本层修改 / 问题」；「组件卡不做 mini heatmap / 不展开完整字段 provenance / 不做操作历史时间线」三条负向（页面 §5 负向清单里没有这三条；《编辑器心智模型与 IA》§3 反而要求焦点编辑栏有独立 History）；Time Period Setup 的六步序列（页面只有「未配置是合法空态 ＋ 激活后须当场可见校验态 ＋ 空态指向显式创建 / 选择来源」）；Time Period 预设 batch preview 的四项内容（页面只有「须 batch preview ＋ 显式确认」）；模板 candidate 编辑的「N 项待审查修改 / [撤销] / [审查修改]」形态（页面只有「预览缓冲是短命 UI 状态，不落成草稿实体」）；Species 字段编辑「不弹 Modal、只在行旁给影响摘要」的强度映射（页面无此分级）；`temp_threshold` 在非 CORE 时「仍显示 / 保存但标注当前不消费」的文案（页面只规定「只对 CORE 必需」与「同图显示」）；`same-source pin` 的文案「当前值不变，但继承关系变化」（页面只要求「已显式固定」记号）；P0 每条通道的验收 variants 清单（commit 列 39 条、paste 列 13 条，属测试计划，正文只收成状态族，见 §2）。
6. **顺带复查到的另一处页面间冲突**（非本两份草稿的内容）：冻结卡 `A①-卡3` 逐字「Effective <0＝ERROR（红）、>1＝WARNING（黄）」，而《编辑器界面》§1.2、§1.4 与《主开发需求》§7 三处逐字都是「`> 1` 的 WARNING ＝ 红标」。本轮裁定 b 取三票侧；卡3 那句待改。
7. **《编辑器与 Resolve》§11.3 与其余三处对影响面数字的口径不一致**：Resolve §11.3 逐字「「引用数 / Effective consumer 数 / 最终数值变化数」是三个可以不同的数字」，而《编辑器持久层契约》§3.10、《编辑器界面》§1.1 与《编辑器心智模型与 IA》§5 逐字都是**四项**（含「新增 Error·Warning」）。记录页 §208 记的收口是「三数→四项」，Resolve §11.3 那处未随之改。
8. **「25 个 Structure slot」**（只有 paste 有这一处；commit 全文不出现「25」作字段数）
   - paste §1 逐字：「25 个 Structure slot 如果每行把 Source / Species / Affinity / Effective 全铺开，右侧 460px 会直接变成 debugger」，收尾逐字：「这样一个 25 格 Structure 编辑器不会变成…」。
   - commit 只给 Structure 的 Detail Filter 与「Structure → 数值型项」的映射，不给字段数。
   - 判断 —— **裁在现行页面侧（UI 不固化字段数）**。一句判据：《编辑器界面》§1.1、§1.3 逐字「字段顺序跟随 Source，不在 UI Contract 固化名称清单或固定字段数量」⇒ paste 这处写法不成立。但**不得读成「25 不是 schema 数」**：《编辑器持久层契约》§3.3 `member_key` 逐字「结构 = `0`…`24`」、《主开发需求》§3.1 与 §4.0 逐字「逻辑查表键共有 25 项」「按当前 StructureType 展开，约 25 项」⇒ 25 是 StructureType 查表键数、属数据 / 记录层枚举。错的只是把它当成 UI 的固定字段数。冻结卡 `A①-卡3`「档位适用面：结构 25 槽」是同一处错。

## 19. 待命名 · 需裁定
正文规定里一律只用页面已有的串、或用纯语义描述。下列串**页面上不存在**：需要新名（或直接弃用草稿名）时在此一次裁定，**不得由下游另发明一套名字** —— 本族标识符按字节精确，正文里用一个文档里不存在的串＝让下游造第二套名字。
1. **控件名**：草稿叫 `FieldValueRow`；页面上已落的名字是 `FieldValueControl`（承载 Field ＋ Effective Value ＋ optional Tier ＋ Local Operation ＋ Diagnostic）。建议直接弃用草稿名。
2. **来源选择的三个草稿串**：`BOUND_SOURCE` / `FOLLOW_SPECIES_SOURCE` / `PIN_SOURCE(sourceRef)`。页面已有的对应物是「跟随物种」这一选项与 durable 字段 `sourceOverride`。
3. **三个字段能力名**：`tieredNumeric` / `numericRelative` / `enumAbsolute`。页面只有「数值型项 / 枚举绝对值项」；正文 §13 已按页面说法写，草稿名未采用。
4. **组件 / 区域名（commit 的 16 个）**：`ObjectContextHeader` / `ComponentCard` / `SourceSelector` / `FieldOperationControl` / `FieldValueRow` / `ValidationIndicator` / `AutosaveStatus` / `ComponentDetailEditor` / `RoleControl` / `SpatialOpportunityPolicy` / `TemplatePicker` / `TemplateWorkspace` / `ImpactPreview` / `TemperatureProfileEditor` / `TemperatureCurvePreview` / `SpeciesConcreteSourcePanel`。页面用的是「组件卡 / 焦点编辑栏 / 前层 Source 选择器 / 聚合策略区 / 顶栏 / 模板工作区」这类称呼；除 `FieldValueControl` 外都没有页面名。
5. **其他只在草稿里出现的串**：`profileCanStartAbsent` / `ModeConcreteSource` / `BootstrapSurface` / `DirectReferenceCount` / `localOperationCount`。`completeValue` 在《编辑器持久层契约》§3.7 有用法，正文按页面的「模板完整值」写。
6. **冻结卡自己的两个控件名**（`A①-卡2` Operation Control / `A①-卡3` Field Value Editor）是卡片层编号名；正文只在 §4 提到「两个交互面的拆分」，未把它们当控件名用。

本文的 0 命中声明，探针作用域＝本轮新取的六个页面（变更与裁决记录 / 编辑器界面 / 编辑器心智模型与 IA / 编辑器与 Resolve / 编辑器持久层契约 / 主开发需求）＋ **本目录内的** `contract-cards.md`（冻结卡）。

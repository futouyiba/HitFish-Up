# UI Component Inventory ＋ 第一批 Contract Cards（「编辑器具体设计」席 · A 线）

<a id="batch-freeze-status"></a>
**状态（两批各自唯一；改自记录页 §265 裁 `F-07`）**：**批次① ＝ 七张全部「已冻结 v1.1」**（`A①-卡1`／`卡2`／`卡3`／`卡4`／`卡5`／`卡6`／`卡7`）；**批次②（`A②-卡8`…`卡12`）＝ 已冻结**（记录页 §244，以该节为冻结留痕）。**本文件不再有任何「起草稿」状态。** 据记录页 §164（冻结接口，已回页核实）。铁律遵守：卡片＝执行投影，机制唯一载体仍是 Current 文档，「依据」行不空——引 Current § 或记录页 §。

**阅读边界**：各卡保留消费者操作、显示、记录和验收场景；所引汇编维护共用机制，卡片摘要不另增规则。卡2恢复执行依据的原核对与修订过程见[固定基线](https://github.com/futouyiba/HitFish-Up/blob/ceceb630ec338f23a11170f9e047fbabd101eaf0/docs/review/ui-component-contract-r2/contract-cards.md#L3-L10)，不作为新一轮来源扫描。操作选择与值输入分卡的职责按[汇编 §4](component-contract-consolidated.md#field-value-control)。

**命名口径（记录页 §271 裁 `A-F-09`）**：本文件各卡的 `Component:` 行**是卡片层标识，不是产品／契约命名** —— 允许与页面语汇不同形，但**不得被下游当作稳定标识符**（不得拿它去建代码枚举／schema 字段／选择器／i18n key）。**凡页面上已有名字的物，一律以页面名为准**（如草稿的 `FieldValueRow` ⇒ 页面名 **`FieldValueControl`**）。正文（需求文档）里指向同一个物时，**只用页面已有的串、或纯语义描述**（§19 前置句已定）。

---

## Part 1｜UI Component Inventory v1（控件总清单）

| # | 控件 | 层·面 | 批次 | 状态／入口 |
|---|---|---|---|---|
| A1 | 顶栏（对象标题/动作/保存状态/Publish） | 框架 | ①（保存状态）＋④（系统面） | 保存区及「丢弃未保存的改动」动作按[卡7](#autosave-status)；本行仅作入口索引 |
| A2 | 面包屑 | 框架 | ④ | 已规格（v2） |
| A3 | dirtyDot（按层待写盘） | 框架 | ④ | 语义已拍＝记录页 §167 六（随卡7 落地） |
| A4 | drawer 导航 ×4 变体 | 对象导航 | ④ | 已规格（v2） |
| C1 | Source Selector·物种层 | 上下文总览 | **①卡1** | [卡1](#source-selector) |
| C2b | Source Selector·覆盖层变体 | 上下文总览 | **①卡1** | [卡1](#source-selector) |
| N1 | 卡上 templateName 显示 | 上下文总览 | ①（随卡1） | 通则=同源同名 |
| C3 | 组件卡 ×4（摘要/角标/覆盖计数） | 上下文总览 | ②/③ 分批 | 已规格（v2） |
| C4 | roleBadge＋Role 三态 | 上下文总览 | ③（Policy） | 已规格（v2） |
| C5 | 档案级字段块（fail_env_coeff） | 上下文总览 | ③（Policy ADD/SET 化） | 已规格（v2） |
| C6 | 分群/占比块 | 上下文总览 | ③/④ | 已规格（v2＋缺口已转 Figma） |
| C7 | Authoring boundary 块 | 上下文总览 | ④ | 已规格（v2） |
| C8 | Operation Control（四动作） | 上下文总览/焦点编辑 | **①卡2** | [卡2](#operation-control) |
| C9 | 档位控件（四档＋Custom） | 焦点编辑 | **①卡3 内含** | [卡3](#field-value-editor) |
| C10 | 列底状态行 | 上下文总览 | 下一期（reconcile 实现） | 维持 §125 四 现状；机制契约落《契约》§6.5/§9.4 且按记录页 §167 一.3 **移 Deferred**：界面 §9.2 不把「重新导入/采纳配置表值」当当前控件，只读诊断（drift/orphan）可留；实现出期＝§163 |
| C11 | 统一抽屉（本期四节） | 上下文总览 | ①（校验节=卡6）＋④（整抽屉） | v1.1 已收 |
| D1 | 编辑栏空态 | 焦点编辑 | ④ | 已规格（v2） |
| D2 | 编辑栏分档（可编/置灰只读） | 焦点编辑 | 通则 | 已规格（v2） |
| D3 | 水温编辑面（6 参＋曲线＋导入） | 焦点编辑 | ③（Temperature） | 已规格（v2）；**6 参中衰减形状为枚举项（项名 `falloff`／显示标签 `falloff_shape`）⇒ 无「调整」入口**（记录页 §175、六.2） |
| D4 | 结构/水层/时段编辑面 | 焦点编辑 | ①载体（slice C 首线=Structure） | 载体形态=卡1/2/3 |
| D5 | 时段空态路径＋三预设 | 焦点编辑 | ③ | 已规格（v2） |
| E1 | 鱼列表 | 独立面 | ④ | 已规格（v2） |
| E2 | 模板工作区（清单/别名/生命周期/Replace） | 独立面 | ② | 已规格（v2） |
| E3 | 引用者列表（两集两数） | 独立面 | ② | 已规格（v2） |
| E4 | Resolve Preview | 独立面 | ④（slice C 含一角） | 已规格（v2） |
| E5 | Bake Preview | 独立面 | ④ | 已规格（v2） |
| N2 | Rebase／Impact Preview 面板 | 编辑/工作区 | ②/④ | 约束已规格（v2 C2b/C11） |

---

## Part 2｜第一批 Contract Cards（A①-卡1…卡7）

批次状态见[文件头](#batch-freeze-status)。原冻结依据为记录页 §165；`A①-卡2` 2026-09-21 恢复的依据见文件头固定基线。

**编号口径（防撞车）**：本席编号＝**A 线批次编号**，标题带前缀（`A①-卡1`…`A①-卡7`、`A②-卡8`…`A②-卡12`）。**GPT 清单另有一套「卡4 ComponentCard／卡5 Impact Preview」，与本席 `A①-卡4`（Effective Value Display）／`A①-卡5`（Provenance Display）不是同一批** —— 引用务必带前缀。

<a id="source-selector"></a>
### A①-卡1｜Source Selector（来源选择器；物种层＋覆盖层两变体）

**机制入口**：[汇编 §8](component-contract-consolidated.md#source-transaction) 完整定义 Source staged 协议、fan-out 分档和同值意图边界；[§15](component-contract-consolidated.md#transaction-model) 区分事务类别。本卡保留动作、落盘字段、展示与验收，不另定义分档机制。原长引文和裁定链见[固定基线卡1](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/review/ui-component-contract-r2/contract-cards.md#L54-L90)。

```
Component: Source Selector｜来源选择器（模板行每格；物种层与兼容壳·覆盖层两变体）
Reads:
  - 该组件当前 source binding（物种层 recipe source；覆盖层 patch sourceOverride）
  - 按所引汇编 §8 的层级 Source allowlist 生成可选项；本卡不另维护矩阵。
  - 模板清单（平铺、作者命名、默认按引用量排序；ARCHIVED 降级不列）
  - 水温额外读「当前物种生态数据存在与否」
Actions:
  - SELECT_SOURCE：先选 candidate；确认提交时物种层改 recipe source，覆盖层写 sourceOverride（桶可换模板）。按所引汇编 §8 执行，不一选即写盘。
  - FOLLOW_PARENT：覆盖层选择「跟随物种」；按同一协议确认提交时删除 sourceOverride，不另开解除即落盘通路。（记录页 §312 XR-F-01；§328 R3-F-01）
  - EXTRACT_TEMPLATE：从当前组件提取为模板；与 A②-卡8 工作区入口是同一创建动作，不是第二套动作。
  - 换源后既有 ops 原样保留，在 candidate 上重 Resolve；高影响批量换绑交 A②-卡11，只改直接引用集。
Durable mutation:
  - candidate 不写持久；确认并通过 revision 核验后原子写 source binding / patch。FOLLOW_PARENT 在此步删除 sourceOverride。
  - 换源不生成保值 SET；EXTRACT_TEMPLATE 只创建模板资产。
Acceptance:
  - Local 或 Propagated 的选择由所引汇编 §8 判定；两档都先预览确认，不出现先写盘后预览。
  - pin Template_A → FOLLOW_PARENT（父层当前也是 A）：即使 value diff 为零，也展示 Binding intent（PINNED → FOLLOW_PARENT）、Effective Source（可相同）、Future propagation（固定 → 跟随）；确认前不删记录，确认后父层改 B 应跟到 B。
  - 反向创建与父层同 Source 的 explicit pin 仍是 durable change；不以当前值相同折成 no-op。（记录页 §392 ADJ-09）
Must show:
  - 闭值按层级显示：水温=物种具体级 token（该组件独有形态，保留作主示意）；模板绑定=类型名；水温双来源带类别记号可区分
  - same-source pin 的「已显式固定」记号（名字与物种相同也显示）
  - 「来源已更换·待复核」轻量标记（挂受影响 ADD）
  - 截断规则 (a)：值区右固定 ~16px ▾ 保留区＋超宽 ellipsis＋全名进 tooltip/下拉首项
  - 卡上 templateName 与闭值同源同名（通则）
Must not:
  - 不自动清 operations；不静默生成 SET 保旧值；same-source 不自动去 pin
  - 覆盖层 picker 不列 SpeciesConcrete（Mode 经「跟随物种」间接继承）
  - 归档模板不出现在普通 picker；不做分组/族折叠（平铺）
依据: Source矩阵与事务见汇编 §8（《编辑器界面》§1.1；《编辑器持久层契约》§3.3／§3.10）；生命周期／引用集见汇编 §14。显示层级（四格裁定）＝记录页 §160 四；截断 (a)＝记录页 §167 六。
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
  - 操作选项按所引汇编 §13 allowlist；用户语言必须按「层 × 字段类型」四格展示：
      · **物种层 × 数值**：仅使用来源 / 调整 / 设置为（**没有 `CLEAR`，也没有「沿用…」**）；
      · **物种层 × 枚举**：仅使用来源 / 设置为；
      · **桶层 × 数值**：沿用物种调整 / 沿用物种设置为（**按实际继承到的那个操作给串**；**物种层无操作时该缺省支显示「仅使用来源」**）/ 仅使用当前来源 / 调整 / 设置为；
      · **桶层 × 枚举**：沿用物种设置为 / 仅使用当前来源 / 设置为（**物种层无操作时该缺省支同样显示「仅使用来源」**）。
      ⇒ UI 四格出处：记录页 §312 裁 `XR-F-03`。
  - 缺省支与「仅使用当前来源」是独立入口；执行所引汇编 §3 的 absent / CLEAR 分支。
  - 调整（ADD）：输入相对当前来源值的带符号增量，按汇编 §3 解析；合法 SPECIES_CONCRETE 没有模板绑定，因此输入提示不得只写「模板值」。（记录页 §312／§316 CXR-04）
  - 设置为（SET）：绝对值
  - 每次编辑=替换当前格唯一 op（每层每字段至多一个最终 op）；**`SET` 之后下层仍可 `ADD`** —— **下层表达替换上层 operation，`ADD` 仍以下层当前来源值为基准**（记录页 §316 裁 `CXR-04`）
  - 档位控件的可用性按汇编 §5 随当前 op 切换。
  - Profile 缺席、Role promotion 与可见校验按汇编 §11 的统一机制；错误显示仍交 A①-卡6，不由本卡另定义空态矩阵。
    - 原取证曾记录解析类型只有时段可空、其余三组件不可空，属于实现缺口而非时段特权；本批未重跑实现，不能用该历史读数判当前实现；固定记录见卡前链接。
Durable mutation:
  - 按所引汇编 §3 写入／删除字段记录，不经值差合成；typed 值的提交要求和 INHERIT / CLEAR 例外按汇编 §4。
  - UI 计数沿用本卡冻结投影：CLEAR 计入本层操作数。该计数仍属 Current 页面未核的 UI 展示项（汇编 §4、§18.5），不能借 durable 语义把它升级为 Current 规则。
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
  - 水温曲线按汇编 §12 展示；参数继续通过各项输入控件编辑，数值项的相对调整交卡2。曲线只读不能扩大成整段温度档案不可编辑。
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
  - 只读；查看来源链→跳 Resolve Preview
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

### A①-卡5｜Provenance Display（来源与过程展示）

```
Component: Provenance Display｜provenance 展示（编辑器侧）
Reads:
  - source binding、op 记录（含 tier）、导入 provenance（周期表导入挂 Concrete Source 更新与 diff）
Actions:
  - 只读查看；跳 Resolve Preview 的 provenance 区
Durable mutation:
  - 无（纯展示；provenance 数据随 op 记录/Concrete Source 携带）
Must show:
  - 「这个值为什么是这样」：来源→操作→当前值 的链
  - 周期表导入的字段级 provenance 差异（前四项=生态数据；temp_threshold/falloff_shape=游戏参数）
Must not:
  - provenance 不进 Resolver/Runtime payload；不塞进 production name；不作为关联/复用判据
依据: 《编辑器持久层契约》§3.3（周期表重新导入更新 Concrete Source 本身、不落 tuning operation；研究事实修正走更新 Source、游戏调参保持 Source 写 Species operation；SPECIES_CONCRETE identity＝(speciesId, componentType)）；《编辑器与 Resolve》§3（Resolve Preview provenance 区）＋§11.3（Template/档位/delta 不进 Runtime）；《编辑器界面》§1.3（别名与微调 provenance 留 editor-state）；fav/accept 取值口径＝记录页 §103
```

### A①-卡6｜Validation·Diagnostic（校验诊断；＝C11 抽屉校验节）

**机制入口**：[通用校验 §6](component-contract-consolidated.md#validation-autosave)、[断链来源 §8](component-contract-consolidated.md#source-transaction)、[Profile 缺席 §11](component-contract-consolidated.md#profile-lifecycle)；本卡规定诊断如何展示与定位，下面是消费者场景。

```
Component: Validation·Diagnostic｜校验诊断（ERROR/WARNING）
Reads:
  - editor-state ＋ current schema ＋ current validator——diagnostics 全量派生重算（重开即重算）
Actions:
  - 行定位：跳 owner 的 Context＋编辑栏聚焦该字段（跨 Context 跳转走「回到该 Context」、不销毁旧现场）
  - Publish 前全量校验（消费 durable revision）
Durable mutation:
  - 无——diagnostics 不作第二 durable truth；semantic ERROR 随 state 一同 durable 保存（「已保存·有错误」态）
Must show:
  - ERROR（＝Publish 阻断项）/ WARNING（如 Soft Fit>1）分级
  - 顶栏「已保存·有错误」的「有错误」点击＝展开并定位首个 ERROR
  - BROKEN_SOURCE_REF：owner/component/ref；可加载修复、Publish 阻断、不 fallback
  - **Role 激活（CORE／SECONDARY）后立刻显示「缺 required Profile」校验态**（记录页 §199 ⑥③ 的附条件：不提示地让作者停在非法态，是那一条唯一风险面）
  - Preset→归档源不可 Apply 且指名哪个源已归档
  - Publish blocker 定位到 owner/component/field/provenance（必要时含 before/after）
Must not:
  - 不把 ERROR 显示成「保存失败」；不伪造 0/默认值/静默补齐（不能解析＝Error/N-A，能解析区继续展示）
  - 不把 required 缺失当 autosave 阻断（durable-valid 与 publish-valid 分开）
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
  - Publish 按钮：显式、批量、独立——消费 durable revision；持久化失败先修（Publish 不隐式执行不可见 Save）
Durable mutation:
  - 状态本身不入 durable（UI state）；semantic edit→debounce/coalesce→原子持久
  - **「丢弃未保存的改动」不改 durable** —— 它只丢弃未落盘的那一笔；盘上仍是上次成功的 revision（故它不产生新记录、也不删任何已持久记录）
Must show:
  - 四态：已保存 / 已保存·有错误 / 保存中… / 保存失败（I/O·revision 冲突）
  - 「有错误」链接到卡6 校验节
Must not:
  - 不常驻 Save 按钮；不把 Validator ERROR 当保存失败
  - 作者可见动作名为「丢弃未保存的改动」，不用工程词 Reset（命名裁定沿卡前固定历史）。
  - **「丢弃未保存的改动」不得读作「回到出厂 / 空态」**；它也不是 Publish 的一部分（不因它触发任何物化 / 发布）
  - 不 silent last-write-wins；autosave ≠ Publish ≠ Git commit
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
Component: Template Library List｜模板清单与别名（模板工作区 22:2；对象导航 TEMPLATES 入口同源）
Reads:
  - 模板清单（按组件过滤；平铺、默认按引用量排序）
  - 每模板：templateId / stableKey（只读）、displayName、中文别名 name_zh / 英文别名 name_en（别名不是生产行 name）、extracted_from（只作追溯、不作关联依据）
  - 生命周期状态（ACTIVE / ARCHIVED）
Actions:
  - 浏览 / 按组件筛选；编辑 name_zh / name_en
  - 「从当前鱼提取模板」（创建）＝**`A①-卡1` 的 EXTRACT_TEMPLATE 在本工作区的入口**——**同一动作、两个入口**，不另实现一套
  - 水温「从钓鱼元素周期表导入」：按现行契约走 **Concrete Source 更新**（**不是直接造模板**）—— ⚠️ **它是高影响重导**：**prepare → Preview → 显式确认 → 一次原子提交**（汇编 §15 已把「重导」列为高影响动作）；**Concrete Source 已被 Recipe／继承行消费时，重导会改变多个 Effective Value** ⇒ **不得写成「直接更新 Source」**。（记录页 §312 裁 `XR-F-05`）；本工作区入口按「导入 → 可提取为模板」两步读（**收口已确认**）。**不承诺导入后四值齐备**。★ **此处先前有内部不闭合，收口如下**（同一份文件另处已写「周期表导入的字段级 provenance 差异：**前四项＝生态数据**；`temp_threshold`/`falloff_shape`＝游戏参数」）：**「四值齐备与否」是「源里有没有」的事实，不是口径未定** ——
  · **来源边界**：下条推导是设计值、非实测，原交付物为水温调研包 `final/`；原登记未落 Current，本次未核上游是否已落页，不把这一历史状态当今天的实测。
  · ★ **该子情形已裁（Owner 2026-09-21）：取「按既定口径推导」。** 规则收窄为 —— `favMin` / `favMax` **有效时**：`acceptMin = max(0, favMin − 2℃)`、`acceptMax = favMax + 2℃`；`acceptMin` / `acceptMax` **属设计推导值，不要求周期表提供实测值**；**若连推导前提 `favMin` / `favMax` 都缺失或非法 ⇒ Reject Import**。
  · ★ **不得「保留旧 `accept`」** —— 理由（Owner 逐字）：保留旧值会形成「**新 `fav` ＋ 旧 `accept`**」的**历史依赖与混合 provenance**，使 **Reimport 非幂等**；既定推导则**确定、可解释、可重复**。  处置与来源索引见 `OPEN-ITEMS` §2。
  · ★ **目标物种护栏（独立条件，不因上述缺值裁定而删除）**：**⚠️ 导入必须带显式目标物种**：该动作更新的是 `SPECIES_CONCRETE` 的 identity ＝ `(speciesId, componentType)`，**而本工作区（`22:2`）的 Reads 里没有 current species、也没有 species selector** ⇒ **入口必须显式选目标物种**（有当前物种时可默认为它），**不得用隐式/未知物种执行**；**未选物种 ＝ 该动作不可执行**，不是「就用当前物种」。替代方案（等价）：把该入口限定到**已有明确 species context** 处。（记录页 §328 裁 `R3-F-06`）
Durable mutation:
  - 别名写编辑器持久层模板记录（template_key 空＝未物化，editor_key 必填）；抽取创建模板资产
  - displayName 改名 ≠ identity rename
Must show:
  - source name 只读；引用量排序；ARCHIVED 降级/标记；别名可空（空＝未起）
Must not:
  - source name 不作键；不提供 stableKey identity rename（错名处置＝新建＋Replace＋归档旧）
  - 不引入分组 / 族折叠（平铺）；不因结构对称给 Quality 预造 Template
  - **不承诺「导入即得四值」**（按本卡 Actions 的已裁缺值规则执行）；**不因 Role 激活自动创建模板／Profile**（记录页 §199 ⑥③：创建永远显式）
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

### A②-卡10｜Edit Template Value（模板完整值编辑；高影响）

**机制入口**：[模板完整值与影响统计 §14](component-contract-consolidated.md#template-reference-sets)、[确认及改值边界](component-contract-consolidated.md#template-replace-boundary)、[水温曲线 §12](component-contract-consolidated.md#temperature-behavior)；本卡保留模板编辑流程及显示。

```
Component: Edit Template Complete Value｜模板改值（共享模板完整值编辑）
Reads:
  - 模板完整值 completeValue；EffectiveConsumerSet（改值的真正影响对象）
Actions:
  - 编辑草稿 → Impact Preview（before / after Resolve）→ 显式确认 → 原子提交 → re-resolve → 物化受影响 production projections
  - ⚠️ **本卡不出现 `ADD`／`SET`／`CLEAR` 这类 operation 语义** —— 模板是**完整值资产**，**operation 只存在于物种 Recipe 与桶 patch 上**（《编辑器持久层契约》§3.3／§3.7）。
  ⇒ 具体记录规则按汇编 §14；本卡不把模板值编辑呈现为字段 operation 编辑。
  - 水温曲线按汇编 §12 只读展示；作者仍通过参数项编辑模板完整值，不提供曲线拖拽／Handle。
Durable mutation:
  - 改 completeValue＝一次全局作者确认；Preview buffer＝短命 UI state，不是 durable Draft Entity
Must show:
  - 候选变更的四项影响统计按汇编 §14 分列，不把直接引用与最终结果变化混作一个数。
  - after-state 出现 publish-blocking ERROR 时醒目标出（仍可确认保存；Publish 阻断到修复——错误进卡6）
Must not:
  - **不实现水温曲线 drag-author**（P0）；也**不得把「曲线只读」扩大成「温度档案不可编辑」**
  - 不给全部引用者制造逐项 review debt（正常传播不产生 N 个下游待办；只有真实异常 / Validator 问题单独暴露）
  - 不静默改任何 consumer 绑定
依据: 《编辑器持久层契约》§3.10／§3.7、《编辑器界面》§1.1／§7，机制统一见汇编 §14；水温曲线 P0 能力见汇编 §12（记录页 §199 ⑥②）。
```

<a id="replace-references"></a>
### A②-卡11｜Replace References（批量换绑 A→B）

**机制入口**：[汇编 §14 两引用集](component-contract-consolidated.md#template-reference-sets)与[Replace 边界](component-contract-consolidated.md#template-replace-boundary)；staged 协议按[§8](component-contract-consolidated.md#source-transaction)。

```
Component: Replace References｜批量换绑（模板 A → 模板 B）
Reads:
  - DirectReferenceSet(A)（改绑目标）；候选 B；全图 before／after Resolve 结果
Actions:
  - 选 A → 选 B → 展示直接改绑对象与 Impact Preview → 显式确认 → 原子 rebind
Durable mutation:
  - 只写直接 source bindings；operations／patches 按所引边界保留
Must show:
  - 哪些对象将被改绑；四项影响统计按汇编 §14 分列；Preview 中 ERROR 醒目
Acceptance:
  - Species 直接引用 A、child 继承它时，换绑只写 Species binding；child 经 Resolve 消费 B，仍无新增 sourceOverride。
  - 已有 ADD／SET／CLEAR 保留；不为维持旧值制造 SET；after 统计来自全图 Resolve，不能只 diff 模板 payload。
依据: 《编辑器持久层契约》v16 §3.10；Source 与操作正交仍见汇编 §3。
```

<a id="reference-list"></a>
### A②-卡12｜Reference List（引用者列表；两集两数）

**机制入口**：[汇编 §14 两引用集与统计上下文](component-contract-consolidated.md#template-reference-sets)；原 CXR-03 修正出处在该节保留，本卡不另维护一份定义。

```
Component: Reference List｜「这一行还被谁用」引用者列表
Reads:
  - DirectReferenceSet 与 EffectiveConsumerSet；按四组件分组
Actions:
  - 只读浏览（可滚动、不截断）；Replace 面板（卡11）另列 Direct 集
Durable mutation:
  - 无（纯展示）
Must show:
  - 缺省显示 EffectiveConsumerSet（含经物种层继承者），标注「直接引用／经继承」
  - 直接引用数／Effective consumer 数并列；共 N 条鱼／M 个鱼种
Acceptance:
  - 一个直接绑定有多个继承消费者时，两集两数分别展示；没有候选变更的列表不显示最终结果变化数／新增 Error·Warning，也不制造候选机制。
Must not:
  - 不截断（只做滚动）；不把物理行共享展示成 Authoring 继承意图（碰巧同值 ≠ 有意共享）
依据: 《编辑器持久层契约》v16 §3.10（两集）、§3.7（lineage复用）；《编辑器界面》v20 §7（列表滚动不截断）。其余沿既有取证：界面 §5 不做三档分级；原实现形态为可滚动约4.5行、按四组件分组，本批未重跑实现。
```

## Part 3 收口提示
1. 卡8「周期表导入」的两步读法、目标物种与缺值护栏按[卡8](#template-list)；实现线逐项对表任务及原冻结批次状态的证据范围见[问题台账](OPEN-ITEMS.md#template-import-implementation-evidence)。
2. 五卡与批次①卡1 的交界：EXTRACT_TEMPLATE 动作在卡1（发起处）与卡8（工作区入口）各出现一次，是同一动作两个入口，不是两个动作；
3. 影响面 Preview 的承载（C11 影响面节 vs 独立面板 N2）在卡10/11 都留了「Preview 正文不进抽屉」口径——与 C11 v1.1 一致。

---

### 补记｜`RoleControl`（Role 三态 × 两层）—— 主代理 2026-09-20 裁（记录页 §249／§250／§252）

<a id="role-control"></a>
**机制入口**：[汇编 §9](component-contract-consolidated.md#role-record-intent)定义 raw Role 与记录态／UI 派生，[§11](component-contract-consolidated.md#profile-lifecycle)定义 Profile 缺席、promotion、Setup及空底板投影；Policy CLEAR／词表仍见[§10](component-contract-consolidated.md#policy-clear)。本卡保留读取、交互、落盘字段和验收。旧 Setup 重复说明及 B1a／B1b 收口原文见[固定基线 RoleControl](https://github.com/futouyiba/HitFish-Up/blob/add09fdaa9c197740df6735160af45c1ebb32370/docs/review/ui-component-contract-r2/contract-cards.md#L386)，不复述已废的自动补档案规则。

```
Component: RoleControl｜Role 三态（CORE / SECONDARY / IGNORED）
Reads:
  - Policy Authoring Truth（四个角色＋fail_env_coeff）：组件卡 Role 下拉与 Policy 区 Role 行读取同一份。
  - 当前物种默认 Role op／Policy Template raw Role、或当前生产行的 Role patch；显示从记录派生，按所引汇编 §9 判读。
  - 当前层／行、Profile presence、合法 Source 可用性及当前诊断；默认值／缺席矩阵按所引 §9／§11，不从最终值反推记录。
Actions:
  - 物种层选具体角色：写本层 SET（各行继承该默认）；回到 INHERIT：显式删除本层 Role op，不以选中同 raw 值代替。
  - 行级设置：只改当前行的覆盖；CLEAR 与缺省支按所引 §10 分别执行，UI 区分两个动作。
  - 显式 Setup：Structure／Feeding Layer／Temperature 空态提供进入合法 Shared Template Source 选择的可达路径；Temperature 若合法 Species Concrete 存在，另可走生态数据导入／建立来源，导入目标物种与缺值护栏仍按卡8。
    · TimePeriod 同样保留 Source／Setup 路径；三种预设只是 Setup 后／中的一次性填表便利，不能充当独有 Profile 创建语义。具体可用来源按汇编 §8 的层级 allowlist。
    · 不新增空 Profile 对象；UI exact shape 仍归 Species Role/UI 工作流。Setup 的完整机制与初值来源按汇编 §11。
Durable mutation:
  - **Role 的 durable 落点在 Policy**，**不另建卡级 state**
  - **形状（裁决 `AR-FCF-CT-01/02/03/04`，2026-09-21；记录页 §342）**：
    · **物种侧**：§3.1 那条整体记录**仍叫 `Species Base Record`／底板记录、不改名** —— **它不只装 Policy**（还装 `temperature`／`structure`／`feeding_layer`／`time_period`／`roles`／`name_cache`）⇒ `Species Policy Recipe` **不能当整条记录的名字**。记录**内部**分两层：`component recipes`（＝ `Species Recipe`：四个 Component 的 Source ＋ field operations）与 **`Species Policy Recipe`**（＝ **Policy 专属子结构**：`policy source binding` ＋ 四个 Role op ＋ `fail_env_coeff` op）。
    · **row 侧两条独立 durable 记录**（**不用 `field`／`track` 判别列**）：**`AffinityRolePatch`** —— key ＝ **`(row_key, component)`**、`op ＝ CLEAR | SET`、`role`（**SET 时必携**）；**`AffinityFailEnvCoeffPatch`** —— key ＝ **`row_key`**、`op ＝ CLEAR | ADD | SET`、`value`（**ADD／SET 时必携**）。
    · **与 `AffinityAuthoringPatch`（§3.3：`sourceOverride` ＋ numeric patches）并列 —— 不改名、不合并**（两者**粒度不同**：numeric ＝ bucket-level，Role ＝ row-level）。可以说「share the same Affinity owner」，**不能说「是同一条持久化记录」**。
    ⇒ **没有 `layer`、没有 `"*"` 哨兵、没有 nullable scope、没有 `track` 判别列**；**Role 值不得参与唯一键**。
  - ⚠️ **行级 patch 必须携 `op`**：不携 op 则 **`CLEAR` 与「`SET` 恰好等于模板 raw 值」不可区分** ⇒ **op 不得从值反推**。
  - ⚠️ **`scope_key` 正式改名 `row_key`（不是简称）**：该记录**永远只有 row scope** —— 留一个泛化的 `scope_key` 没买到能力、**反而暗示还有别的 scope**。`species_key` **降为属性**（组织／查询／reconcile／诊断），**不参与 identity**；**唯一键 ＝ `(row_key, component)`**。
  - 粒度：**两条 patch 轨道（`AffinityRolePatch` / `AffinityFailEnvCoeffPatch`）恒为 row-level**；**物种层的 Role op（`INHERIT` / `SET`）不是 override，而是决定该物种的 `Effective Default Role`**，住在 §3.1 的 `Species Base Record`／`Species Policy Recipe` —— **与本节两条 patch 轨道并存；不得为「统一粒度」把它删掉**。**物种层默认与行级覆盖分属不同记录，不得塞回同一张** —— 物种层默认的**唯一键 ＝ `(species_key, component)`**，**每个「物种 × 组件」恰好一个 Effective Default Role**（同 id 组合的不同行可以有不同 Role）。
Acceptance:
  - 物种 raw Role=CORE：INHERIT（无记录）与 SET CORE 的 Effective Role 可相同，但记录态及“Role 已钉住”显示必须可区分；修改一处，另一入口直接读同一 Truth，不经同步代码。
  - IGNORED＋缺 Profile 后选 CORE：只保存 Role，不自动建 Profile／选默认 Source；立即可见 required-Profile ERROR，Publish 阻断，作者可进入 Setup。四组件分别走通，Temperature 不套全1.00数值档案，TimePeriod 不靠预设替代 Source 建立。
  - 同一组合的两条生产行可有不同 Role，更新目标行不得影响另一行；粒度与键按上面的独立记录形状验收。
  - 空底板且 IGNORED 的组件按汇编 §11 不投影，主行／Role照写、refs空；改为 CORE／SECONDARY 且仍缺必需 Profile 必须阻断，不能一概按空态放行。
Must show:
  - 物种记录态标记按所引汇编 §9，从 Role op record 派生，不另存状态位。
  - **必须显式说出「你在改哪一层 / 哪一行」**：物种层 ⇒「默认（各行继承）」；行级 ⇒ 当前那一行（如 `LAKE_A × LARGEMOUTH_BASS/Q3`）
  - **不许**默认改整个 scope 却在 UI 上说成改一行
  - **批量改多行 ⇒ 必须是显式的多选/批量动作，不是缺省**
Must not:
  - **不许两份 state** —— 不许「持久化一份 + UI 一份」／不许两处各存一份再同步／不许 UI 侧缓存。**判据：改一处之后，另一处不经过任何「同步代码」就变了。**
  - 不给组件卡另建 durable Role state
  - **永不允许 `ADD`**（契约 §3.4）
依据: 契约 §3.4（Role 词表：物种层 `INHERIT / SET`、桶层 `absent / CLEAR / SET`、**永不 `ADD`**；粒度不变量）＋§3.10（Role 单独按生产行覆盖）＋§7／§9（双入口单 Truth；Policy payload ＝ 四角色 ＋ `fail_env_coeff`）＋**记录页 §342（裁决 `AR-FCF-CT-01`＝两条 sibling track／`-02`＝四个名字按层级拆开、整条记录不改名／`-03`＝两条并列 durable record／`-04`＝`species_key` 降属性 ＋ `scope_key` 改名 `row_key`、唯一键 `(row_key, component)`）** ＋记录页 §249／§250（Owner 澄清：**数据只有一份**，持久层与内存态都在 Policy；Policy 视觉须与习性组件明显不同）＋§252（裁 B）
```

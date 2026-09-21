# UI Component Inventory ＋ 第一批 Contract Cards（「编辑器具体设计」席 · A 线）

**状态（两批各自唯一；改自记录页 §265 裁 `F-07`）**：**批次①：`A①-卡1`／`卡3`／`卡4`／`卡5`／`卡6`／`卡7` ＝ 已冻结 v1.1**（记录页 §165）；⚠️ **`A①-卡2` ＝ 已裁、但暂不作为无条件执行依据** —— 它所需的用户语言**尚未落入 Current 页面**、且 Current 仍保留相抵旧串（汇编 §18.1–2）⇒ **落到页后即恢复**。（记录页 §312 裁 `XR-F-07`）；**批次②（`A②-卡8`…`卡12`）＝ 已冻结**（记录页 §244，以该节为冻结留痕）。**⚠️ 凡「批次」级状态一律排除 `A①-卡2`**（**即：批次①可作无条件执行依据的是六张**）；**本文件不再有任何「起草稿」状态。** 据记录页 §164（冻结接口，已回页核实）。铁律遵守：卡片＝执行投影，机制唯一载体仍是 Current 文档，「依据」行不空——引 Current § 或记录页 §。

**批次①清单口径**：§164 原列六项；主代理工作令列七项（多出 Field Value Editor）。本稿按七张出——**建议保留分卡**：op 选择（选哪个动作）与值输入（敲什么数）是两个交互面、两条校验链；收口时若判并入 Operation Control 可并，机械合并即可。

**命名口径（记录页 §271 裁 `A-F-09`）**：本文件各卡的 `Component:` 行**是卡片层标识，不是产品／契约命名** —— 允许与页面语汇不同形，但**不得被下游当作稳定标识符**（不得拿它去建代码枚举／schema 字段／选择器／i18n key）。**凡页面上已有名字的物，一律以页面名为准**（如草稿的 `FieldValueRow` ⇒ 页面名 **`FieldValueControl`**）。正文（需求文档）里指向同一个物时，**只用页面已有的串、或纯语义描述**（§19 前置句已定）。

---

## Part 1｜UI Component Inventory v1（控件总清单）

| # | 控件 | 层·面 | 批次 | 状态 |
|---|---|---|---|---|
| A1 | 顶栏（对象标题/动作/保存状态/Publish） | 框架 | ①（保存状态）＋④（系统面） | 保存区=卡7；**`Reset`＝丢弃尚未落盘的编辑、回到上次成功持久化的 revision（记录页 §178）——不是「回到出厂/空态」** |
| A2 | 面包屑 | 框架 | ④ | 已规格（v2） |
| A3 | dirtyDot（按层待写盘） | 框架 | ④ | 语义已拍＝记录页 §167 六（随卡7 落地） |
| A4 | drawer 导航 ×4 变体 | 对象导航 | ④ | 已规格（v2） |
| C1 | Source Selector·物种层 | 上下文总览 | **①卡1** | 本批 |
| C2b | Source Selector·覆盖层变体 | 上下文总览 | **①卡1** | 本批 |
| N1 | 卡上 templateName 显示 | 上下文总览 | ①（随卡1） | 通则=同源同名 |
| C3 | 组件卡 ×4（摘要/角标/覆盖计数） | 上下文总览 | ②/③ 分批 | 已规格（v2） |
| C4 | roleBadge＋Role 三态 | 上下文总览 | ③（Policy） | 已规格（v2） |
| C5 | 档案级字段块（fail_env_coeff） | 上下文总览 | ③（Policy ADD/SET 化） | 已规格（v2） |
| C6 | 分群/占比块 | 上下文总览 | ③/④ | 已规格（v2＋缺口已转 Figma） |
| C7 | Authoring boundary 块 | 上下文总览 | ④ | 已规格（v2） |
| C8 | Operation Control（四动作） | 上下文总览/焦点编辑 | **①卡2** | 本批 |
| C9 | 档位控件（四档＋Custom） | 焦点编辑 | **①卡3 内含** | 本批 |
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

## Part 2｜第一批 Contract Cards（**六张已冻结 v1.1 ＝ 记录页 §165；`A①-卡2` 见文件头，暂不作为无条件执行依据**）

**编号口径（防撞车）**：本席编号＝**A 线批次编号**，标题带前缀（`A①-卡1`…`A①-卡7`、`A②-卡8`…`A②-卡12`）。**GPT 清单另有一套「卡4 ComponentCard／卡5 Impact Preview」，与本席 `A①-卡4`（Effective Value Display）／`A①-卡5`（Provenance Display）不是同一批** —— 引用务必带前缀。

### A①-卡1｜Source Selector（来源选择器；物种层＋覆盖层两变体）

```
Component: Source Selector｜来源选择器（模板行每格；物种层与兼容壳·覆盖层两变体）
Reads:
  - 该组件当前 source binding（物种层 recipe source；覆盖层 patch sourceOverride）
  - allowlist（**按层分写**）：**前层（物种层）** —— 水温 = `SHARED_TEMPLATE` ∣ `SPECIES_CONCRETE`；结构 / 觅食水层 / 时段 = 仅 `SHARED_TEMPLATE`；**桶（覆盖层）** —— **所有组件都只有 `SHARED_TEMPLATE` ＋「跟随物种」**，**不列 `SPECIES_CONCRETE`**（与同卡 Must not 那句一致）（记录页 §312 裁 `XR-F-02`）
  - 模板清单（平铺、作者命名、默认按引用量排序；ARCHIVED 降级不列）
  - 水温额外读「当前物种生态数据存在与否」
Actions:
  - SELECT_SOURCE：物种层改 recipe source；覆盖层写 sourceOverride（桶可换模板）
  - FOLLOW_PARENT：覆盖层删 sourceOverride = 跟随物种（缺省态）—— ⚠️ **它走与 `SELECT_SOURCE` 同一条边界**：**candidate → Rebase Preview → 显式确认 → 原子提交**。**解除 pin 同样改变 Effective Source** ⇒ **不得成为直接写盘的旁路**。（记录页 §312 裁 `XR-F-01`）
  - EXTRACT_TEMPLATE：从当前组件提取为模板（创建动作，挂组件上下文——提案已交）——**同一动作、两个入口**（此处由组件卡／编辑面发起 ＋ `A②-卡8` 的工作区入口；不是两个动作）
  - 换源后既有 ops 原样保留、在新源上重 Resolve；必附 Rebase Preview（before/after）
  - 高影响批量换绑（Replace References）走 prepare→preview→confirm→atomic，且只改直接引用集
Durable mutation:
  - **换 Source 不是「一选即写盘」**：`SELECT_SOURCE` 先形成 **candidate（不写持久）** → **Rebase Preview（before / after Resolve）** → **显式确认** → **原子提交**（《编辑器与 Resolve》§11.3；汇编 §8）。**`FOLLOW_PARENT`（跟随物种）的持久变更＝删除 `sourceOverride`，同样发生在该动作的「原子提交」那一步 —— 它与 `SELECT_SOURCE` 是同一条边界，不得读成「解除即写盘」。** 落盘对象：`source binding` / `patch`。（记录页 §272 裁 `A-F-05`；§328 裁 `R3-F-01` —— 消掉「解除那一步才写持久」留下的第二口径）
  - 换源不生成任何保值的 SET；EXTRACT_TEMPLATE 创建模板资产
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
依据: 《编辑器界面》§1.1（前层 Source 选择器；温度多一项「当前物种生态数据」；桶另有「跟随物种」；换源不复制不清除＋Rebase Preview；提取为模板；归档隐藏/降级）；《编辑器持久层契约》§3.3（P0 allowlist：温度＝SHARED_TEMPLATE∣SPECIES_CONCRETE、余三组件仅 SHARED_TEMPLATE；AffinityAuthoringPatch.sourceOverride＝桶可换模板；同源显式 pin 保留）＋§3.10（生命周期两态、两引用集、**四项数**、Replace 只改 Direct、BROKEN_SOURCE_REF、高影响四步）；显示层级（四格裁定）＝记录页 §160 四（照准）；截断 (a)＝记录页 §167 六
```

### A①-卡2｜Operation Control（缺省支·调整·设置为·仅使用当前来源）

```
Component: Operation Control｜字段操作控件（INHERIT/ADD/SET/CLEAR 四动作）
Reads:
  - 该字段当前层 op（absent/ADD/SET/CLEAR）与上层 op（继承源）
  - 来源值（= **当前来源值** —— ADD 的基准；**当前来源**可以是共享模板，也可以是合法的 `SPECIES_CONCRETE`）（记录页 §316 裁 `CXR-04`）
  - **字段类型**（数值项 / 枚举绝对值项）与**层**（物种层 / 桶·习性档案层）—— 决定出哪些选项（见 Actions 首条）
  - tier（作者档位，独立字段）
Actions:
  - **操作选项 ＝ 两把筛子取交集**：**层**决定有无 `CLEAR`（**桶／习性档案层才有**，物种层没有）；**字段类型**决定有无 `ADD`（**数值项才有**；**枚举绝对值项没有** —— 其 allowlist ＝ 物种层 `INHERIT / SET`、桶层 `absent / CLEAR / SET`）
    ⇒ **结果必须按「层 × 字段类型」四个格子分别写，不得压成「数值项四支／枚举项三支」**（**压起来会把桶层语言与 `CLEAR` 暴露给物种层**）：
      · **物种层 × 数值**：仅使用来源 / 调整 / 设置为（**没有 `CLEAR`，也没有「沿用…」**）；
      · **物种层 × 枚举**：仅使用来源 / 设置为；
      · **桶层 × 数值**：沿用物种调整 / 沿用物种设置为（**按实际继承到的那个操作给串**；**物种层无操作时该缺省支显示「仅使用来源」**）/ 仅使用当前来源 / 调整 / 设置为；
      · **桶层 × 枚举**：沿用物种设置为 / 仅使用当前来源 / 设置为（**物种层无操作时该缺省支同样显示「仅使用来源」**）。
      ⇒ 依据：**层决定有无 `CLEAR`**（物种层没有）、**字段类型决定有无 `ADD`**（枚举绝对值项没有）。（记录页 §312 裁 `XR-F-03`）
  - 跟随（absent）：覆盖层=删该字段 patch；物种层=无记录
  - 仅使用当前来源（CLEAR）：清除继承的上层 operation，回到当前 Effective Source 原值
  - 调整（ADD）：带符号增量，**相对当前来源值**（**当前来源**可以是共享模板，也可以是合法的 `SPECIES_CONCRETE`）—— ⚠️ **不写成「模板值」**：合法来源里 `SPECIES_CONCRETE` **没有模板绑定**。⚠️ **合法来源里 `SPECIES_CONCRETE` 没有模板绑定**（汇编 §8 明定物种层温度可 Concrete、且 Concrete 不进模板清单）⇒ 写「相对该层所挂模板值」会**把这一类合法来源排除在外**。（记录页 §312 裁 `CXR-04`）
  - 设置为（SET）：绝对值
  - 每次编辑=替换当前格唯一 op（每层每字段至多一个最终 op）；**`SET` 之后下层仍可 `ADD`** —— **下层表达替换上层 operation，`ADD` 仍以下层当前来源值为基准**（记录页 §316 裁 `CXR-04`）
  - **档位随 op 走**：`ADD` 不带 Tier、`SET` 才用 Tier（记录页 §199 ⑥①）
  - **时段 Empty ＋ Role 激活不自动生成 Profile**（记录页 §199 ⑥③）：无 profile ＝ 合法 Empty、op 控件不出；**激活 CORE／SECONDARY 也不自动造 profile**（其可见校验态落 `A①-卡6`）
Durable mutation:
  - **`ADD`／`SET`／`CLEAR` 各落一条；只有「跟随」那一支删条**（`INHERIT`／桶层缺省 `absent` ⇒ 不造记录）——记录由编辑动作直接写，不经值差合成。⚠️ **此处不再把「恢复」当操作名**：本族已把「恢复」判为**模糊词**（《编辑器与 Resolve》§11.2），它只能以「**不得合并成一个「恢复」**」的形式出现（见本卡 Must not）。（记录页 §265 裁 `F-03`）
  - 同值 `SET` 仍留记录（钉住）；`INHERIT` 不造记录；**`CLEAR` 作为 child-patch 状态持久存在** —— 它**尽管 Effective Value 可能等于来源原值，仍是明确的 durable 本层操作、计入本层操作数**（《编辑器持久层契约》§3.3 `op` 行）。（记录页 §265 裁 `F-03`）
  - tier 形状：**§199 ⑥①（`ADD` 无 Tier、`SET` 才用 Tier）已收口该形状问题**（它取代 §174 三「本条不回答形状问题、仍开」那句）；记录仍按 `{op, value, tier}` 携 tier、`ADD` 记录不带 tier。**§148 四.3 的「与 op 正交」为推断**，不作为已裁表述
  - 写记录时机=提交/保存那一刻
Must show:
  - 选项集随「层 × 字段类型」变化（枚举项不出现「调整」；物种层不出现「仅使用当前来源」）——出选项不得靠形状统一
  - 四动作用户语言分开，且**缺省支按层给串**：**物种层缺省＝「仅使用来源」**（它上面没有可沿用的操作 ⇒ 不写没有宾语的「跟随」）；**桶层缺省＝「沿用物种操作」**（**行内显示按实际继承到的那个操作给具体串**：「沿用物种调整」／「沿用物种设置为」；**物种层无操作时该行显示「仅使用来源」**）；「沿用物种操作」≠「仅使用当前来源」，不得合并成一个「恢复」
  - **`CLEAR` 那一态必须在行内可见「移除了哪条继承操作」**（视觉降级行，如「物种调整 −0.20 · 已被本层替代」）—— **不许只靠文字区分**它与「本层什么都没表达」（两者结果值可能相同、**意图不同**）；被替代的 op **只用于解释 provenance、不参与链式计算**
  - 三行展示「来源值 / 相对调整 / 当前值」；ADD 与 SET 显著不同视觉语言
  - 已覆盖但同值仍读作已覆盖（显示读记录，不按值差）
  - **SET 掩盖**可视（**被 SET 盖住**）——同 `A①-卡4`：**「来源已变」不呈现**（未实现支 ＝ 编辑器仓 `docs/gaps.md` `GAP-ED-26`；立牌判不出，见卡4）
Must not:
  - 不合并两个「恢复」；不叠第三层 delta / 多 op 链
  - 不从 payload 相等推断继承（同值/同源显式表达必须保留）；SET 同值不得自动删
  - 不静默 clamp/取绝对值/平移/归一（负值交卡6 报 ERROR）
依据: 《编辑器持久层契约》§3.3「**各字段的 operation allowlist**」（数值型项按业务允许 `ADD`；**枚举绝对值不得 `ADD`**——水温 `falloff`（**项名位**；其字段 / UI 显示标签为 `falloff_shape`——记录页 §175 六.2）属此类：物种层 `INHERIT / SET`、桶层 `absent / CLEAR / SET`）＋同节 op 行（`CLEAR` 只在桶／习性档案层）＋§3.4（Role 不允许 ADD）；**「两把筛子取交集」这一通则＝设计层对该二处的合成读法（主代理口径，本席照录）；记录页 §175＝其 `falloff` 实例（enum absolute ⇒ 不得 ADD）＋Owner 直裁出处**（§175 六.1 并更正定性：不是改判，是把实现的 5 项拉回契约已写的 6 项）；《编辑器界面》§1.2（用户语言按层给串：物种层缺省「仅使用来源」／桶层缺省「沿用物种操作」（行内显示按实际继承到的操作给具体串）；`CLEAR` 的用户语言＝「仅使用当前来源」；「沿用物种操作」与「仅使用当前来源」不合并；三行典型展示 来源值0.80·相对调整−0.20·当前值0.60）；《编辑器与 Resolve》§11.1（每层每字段最多一个最终 op、编辑＝替换；absent/CLEAR/ADD·SET 语义；算例 0.8−0.1=0.7；Q3：上层 SET 后下层仍可 ADD、基准＝该层所挂模板值（⚠️ **该引文的「模板值」须读作「**当前来源值**」**：`SPECIES_CONCRETE` 无模板绑定；本卡 Actions 已按此写明 —— 记录页 §312 裁 `CXR-04`）；换源不清 op；同源 pin）；《编辑器持久层契约》§3.3（op 词表含 CLEAR＝继承控制非第三种数值调整；INHERIT＝无记录；affinity_tier 行）＋§3.5（同值仍是 override、界面读记录判据）；Tier 与 op＝记录页 §199 ⑥①（`ADD` 无 Tier／`SET` 才用 Tier）、§174（Temperature 免）、§154（独立字段形状）
```

### A①-卡3｜Field Value Editor（数值/档位/曲线输入）

```
Component: Field Value Editor｜值输入控件（数值输入、档位选择、水温曲线）
Reads:
  - typed 当前值
  - 档位表：PREFERRED 1.00 / SUBOPTIMAL 0.60 / ACCEPTABLE 0.25 / REJECT 0.05 ＋ Custom 精确值（含各档可表达范围）
  - 档位适用面：**结构＝按当前 Source 动态生成的 StructureType 字段控件（不固化字段数量**；现行实例 25 —— 其 `member_key` `0`…`24` 是**数据/记录层的查表键数**，不得反读成 UI 的固定字段数）／水层 3 行／时段 5 行；水温豁免（连续曲线）
  - 水温曲线参数（六参；`temp_threshold ∈ [0,1]`；**衰减形状＝枚举绝对值项**）
  - **两层名（记录页 §175 六.2，现行）**：**项名位写 `falloff`**（与同列短形族一致：`acceptMin / favMin / favMax / acceptMax / threshold`）；**字段位 / UI 显示标签写 `falloff_shape`**（对应字段族长形 `temp_accept_min / …`）。**两处各按其位、不判谁对谁错、不做统一**
Actions:
  - 数值输入：Enter/blur 形成有效 typed 值＝一笔 semantic edit
  - 档位选择（tier）；Custom 精确值
  - **`falloff_shape` 那格（项名 `falloff`）是枚举 `<select>`（`LINEAR` / `SMOOTHSTEP`）——不给 `ADD` 入口**（口径与卡2 一致：枚举项三支）
  - **水温曲线 P0 只读、不 drag-author**（记录页 §199 ⑥②）；**6 项参数仍按项编辑**（**5 个数值项 ＋ 1 个枚举项 `falloff_shape`**；相对关系走显式相对调整入口＝卡2 ADD）—— ⚠️ 原文写「6 个**数值**参数」**把枚举项也算进「数值」**；**数 6 本身不改**（它是记录页 §175 六.1 的裁定：「把实现的 5 项拉回契约已写的 6 项」）。（记录页 §312 裁 `XR-F-04`）。⚠️ 该条**取代** Checkpoint「直接拖动绝对曲线／Handle 仍应表达为 SET」那句——不要再给曲线加拖拽授权
  - 时段三预设一次性填表（应用时覆盖确认；模板名不进 Runtime）
Durable mutation:
  - 有效 typed 值经卡2 落 op；raw buffer（"-" "0." "abc"）不写 durable typed、不覆盖上一 durable 值（保留 UI local）
  - tier 独立持久化、不得从生产最终值反推；**随 op 走：`ADD` 无 Tier、`SET` 才用 Tier**（记录页 §199 ⑥①）
Must show:
  - **档位（Tier）随 op 走：`ADD` 不带 Tier、`SET` 才用 Tier**（记录页 §199 ⑥①；该条同时关掉 `affinity_tier ↔ op` 的形状问题）
  - **Temperature 不带 `affinity_tier`**（记录页 §174）；**不得用伪造 `CUSTOM` tier 满足 schema**
  - 每项 继承/已覆盖 状态（读记录）
  - 越界分级反馈：Effective<0＝ERROR（**红标**）、>1＝WARNING（**红标，不阻断**）、两者皆可保存 —— **分级靠文案与阻断性区分，不靠颜色**（三处逐字：《编辑器界面》§1.2／§1.4 ＋《主开发需求》§7）
  - 不可解析＝即时输入错误
  - 时段未配空态文案；**激活 CORE／SECONDARY 不自动生成 Profile**（记录页 §199 ⑥③）——空态应指向**显式创建／选择来源**的路径，并**立刻显示「缺 required Profile」校验态**（`A①-卡6`）。⚠️ **不得再写「提为 CORE/SECONDARY 即生成 profile」**——依据写法＝「**记录页 §116 二（该支）已被 §199 ⑥③ 取代**」（**只废那一支，§116 二 整条未废**，勿写成「§116 已作废」）
Must not:
  - 不静默 clamp/取绝对值/平移/归一
  - 不把 raw 字符串写 typed state；不把「未配置」编码成 null 必填字段的现存记录
  - 不因 UI 统一强行给枚举绝对值项上 ADD（**射程只落在枚举绝对值项 `falloff_shape`**；`acceptMin / favMin / favMax / acceptMax` **属那 5 个数值项、`ADD` 合法**，不得一并禁掉）
依据: 《编辑器界面》§1.1（Affinity 四档表；时段未配置合法空态；三预设表）＋§1.2（越界分两侧：>1＝WARNING 放行、<0＝ERROR 阻断 Publish；校验对象＝resolved/Effective 值、负 ADD 使终值非负即合法；临时字符串（-、0.、空）不是持久值；语义编辑经短 debounce 原子落盘）；《开发需求》§3.2/§7/§9；《配置表与校验》§5（Effective Fit 两侧＋不 clamp）；《编辑器持久层契约》§7.1（未解析控件字符串不入 durable）＋§3.3（affinity_tier **按组件适用**——记录页 §174：Temperature 免、只适 Structure／Feeding Layer／Time Period；不能从生产最终值反推；**各字段 operation allowlist：枚举绝对值不得 ADD，`falloff` 属此类**）；衰减形状可项级覆盖＝记录页 §175（**§175 六.1** 定性更正：不是改判、是把实现的 5 项拉回契约已写的 6 项；**§175 六.2** 命名更正＝项名/字段名两层、不统一——本条按六.2 写。⚠️ §175 四「统一用 `falloff`」**已被六.2 撤销**，勿引）；temp_threshold∈[0,1]＝《配置表与校验》§5／《开发需求》§4.3
```

### A①-卡4｜Effective Value Display（当前值展示）

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
  - （保留的逐字一格）**「来源已变」不呈现** —— 逐字已收一格：**「来源已变」不呈现**（未实现支 ＝ **编辑器仓 `docs/gaps.md` `GAP-ED-26`**，逐字「『SET 盖住来源』只报得出**一半**：来源**漂移**检测不出（耐久记录不带来源快照）」；本席**读过该文件核过**。机理：耐久记录 `{op, value, tier}` 不含来源快照 ⇒ 立牌上判不出「来源已变」）。**可翻转点**：若要保留「来源已变」，须实现侧加**来源快照**（动 durable 记录形状）＝一条独立的路（回改＝本卡 ＋ 记录形状两处）
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

### A①-卡7｜Autosave Status（保存状态；＝A1 顶栏保存状态区）

```
Component: Autosave Status｜自动保存状态区（顶栏）
Reads:
  - durable write 结果；base revision 对比（打开时记录、每次 commit 前校验）
Actions:
  - 保存失败时：重试／显式 reload-reconcile（外部修改＝BLOCK＋报告，不 auto-merge）
  - **`Reset` ＝ 丢弃尚未落盘的编辑，回到「上一次成功持久化的 revision」**——autosave 下只在两个窗口有实际效果：**防抖未到点**、**保存失败之后**（此时盘上仍是上次成功版本）
  - Publish 按钮：显式、批量、独立——消费 durable revision；持久化失败先修（Publish 不隐式执行不可见 Save）
Durable mutation:
  - 状态本身不入 durable（UI state）；semantic edit→debounce/coalesce→原子持久
  - **`Reset` 不改 durable** —— 它只丢弃未落盘的那一笔；盘上仍是上次成功的 revision（故它不产生新记录、也不删任何已持久记录）
Must show:
  - 四态：已保存 / 已保存·有错误 / 保存中… / 保存失败（I/O·revision 冲突）
  - 「有错误」链接到卡6 校验节
Must not:
  - 不常驻 Save 按钮；不把 Validator ERROR 当保存失败
  - **`Reset` 不得读作「回到出厂 / 空态」**；它也不是 Publish 的一部分（不因 Reset 触发任何物化 / 发布）
  - 不 silent last-write-wins；autosave ≠ Publish ≠ Git commit
依据: 《编辑器界面》§1.1（验证入口：无常驻 Save、四态 已保存/已保存·有错误/保存中/保存失败、Publish 显式批量独立、错误精确定位）＋§1.2（四态口径；ERROR≠保存失败；外部改动⇒阻断覆盖、显式重载/reconcile）＋§9.1（动作按钮 Reset/Publish/导出/Bass 预设；Publish 消费已持久化 revision）；《编辑器持久层契约》§6.3（语义编辑边界；乐观检测、禁 silent last-write-wins；Autosave≠Publish≠Git commit；Publish 不隐式执行不可见 Save）；**`Reset` 语义＝记录页 §178**（Reset＝丢弃尚未落盘的编辑、回到上次成功持久化的 revision；只在防抖未到点／保存失败后有效；不做出厂/空态、不属 Publish）
```

---

## 收口提示（给主代理）
1. **卡3 去留**：建议保留分卡（理由见封面）；若并，卡3 的 raw-buffer/越界/档位条款并入卡2/卡6。
2. **slice C 依赖**：七卡中 1/2/3/4/6/7 全部落在 Structure vertical slice 路径上（Species→Structure→Shared Template→Species ADD→Affinity sourceOverride→SET/CLEAR→autosave→Resolve Preview→materialize）⇒ 这六张冻结前，实现线勿动该路径、Figma 线勿投影该块（§164 护栏已含）。
3. **②后的机械替换点**：各卡「依据」行 packet 指针→Current §（预计落点：契约 §3.3/§3.7（§162 已落 op 行/lineage 句）、界面 §1.x、开发需求 §7）；替换时逐卡回报。
4. 术语按 §102：卡片正文用「兼容壳/习性档案」，标识符原样。


---

## Part 3｜第二批 Contract Cards（五张 · 批次②模板生命周期 · **已冻结**；编号 `A②-卡8`…`A②-卡12`）（记录页 §244 为此批冻结留痕；§265 裁 `F-07` 去掉原「起草稿」）

覆盖 Inventory E2/E3/N2。底稿＝v2 规格，依据引②后 Current §（落页措辞已逐字核）。

### A②-卡8｜Template Library List（模板清单与别名）

```
Component: Template Library List｜模板清单与别名（模板工作区 22:2；对象导航 TEMPLATES 入口同源）
Reads:
  - 模板清单（按组件过滤；平铺、默认按引用量排序）
  - 每模板：templateId / stableKey（只读）、displayName、中文别名 name_zh / 英文别名 name_en、extracted_from（只作追溯）
  - 生命周期状态（ACTIVE / ARCHIVED）
Actions:
  - 浏览 / 按组件筛选；编辑 name_zh / name_en
  - 「从当前鱼提取模板」（创建）＝**`A①-卡1` 的 EXTRACT_TEMPLATE 在本工作区的入口**——**同一动作、两个入口**，不另实现一套
  - 水温「从钓鱼元素周期表导入」：按现行契约走 **Concrete Source 更新**（**不是直接造模板**）—— ⚠️ **它是高影响重导**：**prepare → Preview → 显式确认 → 一次原子提交**（汇编 §15 已把「重导」列为高影响动作）；**Concrete Source 已被 Recipe／继承行消费时，重导会改变多个 Effective Value** ⇒ **不得写成「直接更新 Source」**。（记录页 §312 裁 `XR-F-05`）；本工作区入口按「导入 → 可提取为模板」两步读（**收口已确认**）。**不承诺导入后四值齐备**（`accept` 上下限来源仍在裁）。**⚠️ 导入必须带显式目标物种**：该动作更新的是 `SPECIES_CONCRETE` 的 identity ＝ `(speciesId, componentType)`，**而本工作区（`22:2`）的 Reads 里没有 current species、也没有 species selector** ⇒ **入口必须显式选目标物种**（有当前物种时可默认为它），**不得用隐式/未知物种执行**；**未选物种 ＝ 该动作不可执行**，不是「就用当前物种」。替代方案（等价）：把该入口限定到**已有明确 species context** 处。（记录页 §328 裁 `R3-F-06`）
Durable mutation:
  - 别名写编辑器持久层模板记录（template_key 空＝未物化，editor_key 必填）；抽取创建模板资产
  - displayName 改名 ≠ identity rename
Must show:
  - source name 只读；引用量排序；ARCHIVED 降级/标记；别名可空（空＝未起）
Must not:
  - source name 不作键；不提供 stableKey identity rename（错名处置＝新建＋Replace＋归档旧）
  - 不引入分组 / 族折叠（平铺）；不因结构对称给 Quality 预造 Template
  - **不承诺「导入即得四值」**（值来源待裁）；**不因 Role 激活自动创建模板／Profile**（记录页 §199 ⑥③：创建永远显式）
依据: 《编辑器持久层契约》§3.6（模板清单与别名记录表）＋§3.10（identity immutable；displayName 可改）；《编辑器界面》§7（平铺可滚动、按引用量排序、别名可编辑、source name 只读）
```

### A②-卡9｜Template Lifecycle（ACTIVE / ARCHIVED）

```
Component: Template Lifecycle｜模板生命周期
Reads:
  - 生命周期状态；DirectReferenceSet（Hard Delete guard 用）
Actions:
  - Archive（ACTIVE→ARCHIVED）；Restore（ARCHIVED→ACTIVE）
  - Hard Delete（仅 DirectReferenceSet＝∅；Preset 引用也算 live）
Durable mutation:
  - Archive / Restore 改生命周期状态；Hard Delete 删资产（前置＝显式解除 / 替换全部直接引用）
Must show:
  - ARCHIVED 的限制可视（不可新建引用 / 不可直改完整值；要改先 Restore）
  - Hard Delete 前的引用清点
Must not:
  - Archive 不自动改引用 / 不 fallback / 不自动找相似 / 不自动复制 payload
  - ARCHIVED ≠ 可删；不新增第三态；归档模板从普通 Source Picker 隐藏 / 降级
依据: 《编辑器持久层契约》§3.10（生命周期两态、Hard Delete＝DirectReferenceSet 空、Preset 引归档源 invalid-for-apply 且 UI 指名、归档从 Picker 隐藏）
```

### A②-卡10｜Edit Template Value（模板完整值编辑；高影响）

```
Component: Edit Template Complete Value｜模板改值（共享模板完整值编辑）
Reads:
  - 模板完整值 completeValue；EffectiveConsumerSet（改值的真正影响对象）
Actions:
  - 编辑草稿 → Impact Preview（before / after Resolve）→ 显式确认 → 原子提交 → re-resolve → 物化受影响 production projections
  - ⚠️ **本卡不出现 `ADD`／`SET`／`CLEAR` 这类 operation 语义** —— 模板是**完整值资产**，**operation 只存在于物种 Recipe 与桶 patch 上**（《编辑器持久层契约》§3.3／§3.7）。
  ⇒ 原第 2 条「档位（Tier）随 `op` 走：`ADD` 不带 Tier、`SET` 才用 Tier」**已删**：那条依据的记录页 §199 ⑥① 讲的是**值记录**的 `{op, value, tier}` 形状，**属另一个寄存器**；搬进「模板完整值编辑」是**跨界搬用**（记录页 §265 裁 `F-06`）。
  - **水温曲线：P0 只读、不 drag-author**（记录页 §199 ⑥②）—— 本席读作**仅禁拖拽／Handle 授权，6 项参数（5 数值 ＋ 1 枚举）仍可编辑**（主语是「曲线」而非「温度档案」）。**本读法主代理 2026-09-20 已核、待复核点关闭**：与界面 §1.1「6 参数 ＋ 连续曲线」同口径 ⇒ 曲线作为**编辑面**只读，**参数作为项仍可编辑**。**可翻点**：若翻成「整段不可编辑」，改动面＝本卡 Actions ＋ 界面 §1.1 那句，两处
Durable mutation:
  - 改 completeValue＝一次全局作者确认；Preview buffer＝短命 UI state，不是 durable Draft Entity
Must show:
  - **四项分列（逐字；《契约》§3.10 与《编辑器界面》§7 同句）**：**直接引用数 / Effective consumer 数 / 最终结果变化数 / 新增 Error·Warning** —— 是**四个可以互不相同的数字**
  - after-state 出现 publish-blocking ERROR 时醒目标出（仍可确认保存；Publish 阻断到修复——错误进卡6）
Must not:
  - **不实现水温曲线 drag-author**（P0）；也**不得把「曲线只读」扩大成「温度档案不可编辑」**
  - 不给全部引用者制造逐项 review debt（正常传播不产生 N 个下游待办；只有真实异常 / Validator 问题单独暴露）
  - 不静默改任何 consumer 绑定
依据: 《编辑器持久层契约》§3.10（高影响四步；两引用集；**四项数**）＋§3.7（Template edit 下 projection 生命周期：SET-masked 可不变）；《编辑器界面》§1.1 共享影响面行（**四项数**同句）；水温曲线 P0 只读＝记录页 §199 ⑥②（⚠️ 该条**取代** Checkpoint「直接拖动绝对曲线／Handle 仍应表达为 SET」那句）
```

### A②-卡11｜Replace References（批量换绑 A→B）

```
Component: Replace References｜批量换绑（模板 A → 模板 B）
Reads:
  - DirectReferenceSet(A)（枚举改动目标）；替换候选 B
Actions:
  - 选旧源 → 选新源 → 枚举直接引用 → 保留既有 ops / patches → re-resolve 全图 → before / after Impact Preview → 确认 → 原子 rebind
Durable mutation:
  - 只重写 durable 直接绑定
Must show:
  - 改动前清点（哪些对象将被改绑）；**四项分列**（直接引用数 / Effective consumer 数 / 最终结果变化数 / 新增 Error·Warning）；Preview 含 ERROR 醒目
Must not:
  - 禁止给 EffectiveConsumer 自动写 sourceOverride（会把经继承消费的 child 变成显式 pin、静默改变 authoring 拓扑）
  - 不为保持旧 Effective Value 生成 SET
依据: 《编辑器持久层契约》§3.10（Replace 只改 DirectReferenceSet 逐字）＋§3.3（换源不自动清除既有调整）
```

### A②-卡12｜Reference List（引用者列表；两集两数）

```
Component: Reference List｜「这一行还被谁用」引用者列表
Reads:
  - DirectReferenceSet 与 EffectiveConsumerSet（两组，可分列）；按四组件分组
Actions:
  - 只读浏览（可滚动、不截断）；Replace 面板（卡11）另列 Direct 集
Durable mutation:
  - 无（纯展示）
Must show:
  - 缺省显示 EffectiveConsumerSet（含经物种层继承者），分组标注「直接引用 / 经继承」
  - **两集 ＋ 各自的两个数**（**直接引用数 / Effective consumer 数**）并列（Replace 的 target＝Direct 集）；共 N 条鱼 / M 个鱼种
  - ⚠️ **本卡不出现「四项数」的后两项**（最终结果变化数 / 新增 Error·Warning）—— **它们需要「候选变更 ＋ before/after」上下文，而只读列表没有这个输入**（记录页 §288 裁 `CXR-03`）。**四项数只在有候选变更的上下文里出现（卡10／卡11）**；**不得由实现者自行补造候选机制**。
Must not:
  - 不截断（只做滚动）；不把物理行共享展示成 Authoring 继承意图（碰巧同值 ≠ 有意共享）
依据: 《编辑器持久层契约》§3.10（两引用集定义与用途；**四项数的定义与适用上下文** —— 本卡是只读列表，只取前两项，后两项归有候选变更的分析，记录页 §288 裁 `CXR-03`）＋§3.7（复用按 lineage、禁 payload-equality dedup）；《编辑器界面》§7（引用者列表不截断只滚动）＋§5（负向清单：不做三档分级）；现行实现形态（可滚动约 4.5 行、按四组件分组）
```

## Part 3 收口提示
1. 卡8「周期表导入」两步读法（导入＝Concrete 更新，模板经提取产生）：**措辞按记录页 §255 ③ 保持不动**，**待实现线逐条对表**，如与实现相抵再报 —— **这是本批唯一的一条挂项，不代表整批「待确认」**（记录页 §265 裁 `F-07`）；
2. 五卡与批次①卡1 的交界：EXTRACT_TEMPLATE 动作在卡1（发起处）与卡8（工作区入口）各出现一次，是同一动作两个入口，不是两个动作；
3. 影响面 Preview 的承载（C11 影响面节 vs 独立面板 N2）在卡10/11 都留了「Preview 正文不进抽屉」口径——与 C11 v1.1 一致。

---

### 补记｜`RoleControl`（Role 三态 × 两层）—— 主代理 2026-09-20 裁（记录页 §249／§250／§252）

```
Component: RoleControl｜Role 三态（CORE / SECONDARY / IGNORED）
Reads:
  - **Policy 那条 Authoring Truth**（四个角色 + fail_env_coeff）—— 组件卡上的 Role 下拉与 Policy 区 Role 行**读同一份**
  - 当前上下文：物种层（默认）／行级（当前那一生产行）
Actions:
  - 物种层设置 ⇒ **改"默认"**（各行 INHERIT 它）
  - 行级（桶／生产行）设置 ⇒ **改"该行的覆盖"**（`CLEAR` ⇒ **移除继承自物种层的操作、回到物种当前 Policy Template 的 raw 值** —— **不是**「回到继承」；**桶层缺省（`absent`）才是「回到继承」**；两者是**两个不同动作、UI 必须区分**）（《编辑器持久层契约》§3.4；记录页 §265 裁 `F-04`）
Durable mutation:
  - **Role 的 durable 落点在 Policy**，**不另建卡级 state**
  - **形状：两条记录、按层分开**（记录页 §331 裁 `R3-F-05`）：
    · **`Species Policy Recipe`** —— key ＝ `species_key`：`policy source binding` ＋ 四个 Role 的 op（`INHERIT` 用 **absence** 表达；物种层**最多一个 local Role op**）＋ `fail_env_coeff` op；
    · **`Affinity Policy Patch`** —— key ＝ `row_key`（视情形加 `component`）：Role patch ＝ **`CLEAR | SET`**；`fail_env_coeff` patch ＝ **`CLEAR | ADD | SET`**。
    ⇒ **不设 `layer` 判别字段、不用 `scope_key="*"` 这类哨兵**；**Role 值不得参与唯一键**。
  - ⚠️ **行级 patch 必须携 `op`**：不携 op 则 **`CLEAR` 与「`SET` 恰好等于模板 raw 值」不可区分** ⇒ **op 不得从值反推**。
  - 粒度：**Role 恒为 row-level**；**物种层默认与行级覆盖是两条记录，不得塞回同一张 record** —— 物种层默认的**唯一键 ＝ `(species_key, component)`**，**每个「物种 × 组件」恰好一个 Effective Default Role**（同 id 组合的不同行可以有不同 Role）。
Must show:
  - **必须显式说出「你在改哪一层 / 哪一行」**：物种层 ⇒「默认（各行继承）」；行级 ⇒ 当前那一行（如 `LAKE_A × LARGEMOUTH_BASS/Q3`）
  - **不许**默认改整个 scope 却在 UI 上说成改一行
  - **批量改多行 ⇒ 必须是显式的多选/批量动作，不是缺省**
Must not:
  - **不许两份 state** —— 不许「持久化一份 + UI 一份」／不许两处各存一份再同步／不许 UI 侧缓存。**判据：改一处之后，另一处不经过任何「同步代码」就变了。**
  - 不给组件卡另建 durable Role state
  - **永不允许 `ADD`**（契约 §3.4）
依据: 契约 §3.4（Role 词表：物种层 `INHERIT / SET`、桶层 `absent / CLEAR / SET`、**永不 `ADD`**；粒度不变量）＋§3.10（Role 单独按生产行覆盖）＋§7／§9（双入口单 Truth；Policy payload ＝ 四角色 ＋ `fail_env_coeff`）＋**记录页 §331 裁 `R3-F-05`（形状拆两条记录：`Species Policy Recipe`（key＝`species_key`）＋ `Affinity Policy Patch`（key＝`row_key`）；不设 `layer`、不用哨兵、Role 值不进键；行级 patch 必携 `op`）** ＋记录页 §249／§250（Owner 澄清：**数据只有一份**，持久层与内存态都在 Policy；Policy 视觉须与习性组件明显不同）＋§252（裁 B）
```

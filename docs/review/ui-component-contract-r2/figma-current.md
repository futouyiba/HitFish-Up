# Figma 画面与图像证据登记

**范围与版本**：节点、annotation 和几何记录的历史部分继承自 [#7 固定版本](https://github.com/futouyiba/HitFish-Up/blob/1409a13fde46dcb8d10bae039c26f6a0090bf497/docs/review/ui-component-contract-r2/figma-current.md)，包含多轮历史回读；#7 的图片与导出更正见[固定证据版本](https://github.com/futouyiba/HitFish-Up/blob/ca17a2306b3c567e6fe7bc2eedcc6ed43ed3a2e5/docs/review/ui-component-contract-r2/figma-current.md)；后续 INHERIT 1×图与对应记录继承自 [#17 固定版本](https://github.com/futouyiba/HitFish-Up/blob/8d4523c0372c12cbf1aad14ec652159c2782e5ad/docs/review/ui-component-contract-r2/figma-current.md)。本次整理只核仓内 PNG 指纹、尺寸与元数据，未重读实时 Figma；既有画面判读沿原取证。较早回读不代表较晚图片仍如此。**本文件登记实物与证明范围；处置、剩余工作及关闭证据统一见[问题台账](OPEN-ITEMS.md#active-review-items)。**

**这是一份按取证版本记录画面的清单**，供你比对契约。**不含文件链接**（按本项目的对外规则，内部链接一律不进仓）。

**CLEAR 相关文字的版本边界**：本文件的 op 标签、画布结构与回读叙述保留自 [PR #7 固定快照](https://github.com/futouyiba/HitFish-Up/blob/1409a13fde46dcb8d10bae039c26f6a0090bf497/docs/review/ui-component-contract-r2/figma-current.md)，本次未重读 live Figma；它们是图面证据，不另定义 CLEAR。组件语义见[汇编 §3](component-contract-consolidated.md#component-clear)，Policy 语义见[§10](component-contract-consolidated.md#policy-clear)。图中 Role 控制条的「CLEAR 回到模板 raw 值」仅在 Policy 域解读。

帧尺寸约定：**宽统一 1680**；**高两档** —— 作者面一族 `1680×1220`，其余 `1680×1080`。

---

**日常入口与历史**：本文件保留登记对象、随包资产及证明范围；导出实验、节点演进和旧画面对照统一查[整理前固定全文](https://github.com/futouyiba/HitFish-Up/blob/db97e9bb4784a8eaf2421cf88894c6d4e4beef2c/docs/review/ui-component-contract-r2/figma-current.md)。下列帧／节点与 annotation 摘要沿该版本登记，不是本轮 live Figma 盘点。

## 一、Current 页的帧（7）

| 帧名 | node | 尺寸 | 是什么 |
|---|---|---|---|
| `01 Affinity Compat Mode Authoring` | `8:2` | 1680×1220 | 主编辑面（空态：未选中任何组件卡） |
| `10 Authoring · 编辑（水温）` | `104:269` | 1680×1220 | 同一作者面的**选中态**（水温） |
| `11 Authoring · 编辑（结构）` | `108:311` | 1680×1220 | 同一作者面的**选中态**（结构） |
| `04 Resolve Preview · Subject + Seed` | `9:2` | 1680×1080 | 只读 |
| `05 Bake Preview · ConditionGroup Trace` | `9:39` | 1680×1080 | 只读 |
| `07 Component Template Workspace` | `22:2` | 1680×1080 | 第二工作区 |
| `08 Fish List · CN / EN / ID` | `22:36` | 1680×1080 | 鱼列表 |

**Structure 的表示**：选中 Structure 后在**右侧 460px 焦点编辑栏**、以**2 列紧凑字段控件**编辑（`108:311`；`structureList2Col` 实测两列 x≈1227/1446，**12 行双列 ＋ 1 行单列 ＝ 25 个 `FieldValueControl`** —— **末行只有一列，不要按「13 行 × 2」算成 26**）。
**旧帧 `47:2`（`Component Value Controls · tier & empty state`，形态是 5×5 卡阵）已移出 Current、进归档页**，带 `[FCF-ARCHIVE:v1]` annotation。

**三栏几何**：对象导航 `250` ＋ 上下文总览 `890` ＋ 焦点编辑 `460` ＋ 边距 ＝ `1680`。

---

## 二、投影区（`PROJECTION｜…`，共 11 组）

**A 线（契约卡的逐卡投影；每组＝一卡的关键状态帧）**

| 组 | 卡 | node | 态数 |
|---|---|---|---|
| `A①-卡1 Source Selector` | Source 选择器 | `153:282` | 七态 |
| `A①-卡2 Operation Control` | 字段操作控件 | `163:275` | **十态**（2026-09-20 由八态增至十态） |
| `A①-卡3 Field Value Editor` | 值输入控件 | `166:275` | 八态 |
| `A①-卡6 Validation·Diagnostic` | 校验诊断 | `170:275` | 八态 |
| `A①-卡4 Effective Value Display` | 有效值展示 | `206:704` | 六态 |
| `A①-卡5 Provenance Display` | provenance 展示 | `206:770` | 五态 |
| `A①-卡7 Autosave Status` | 保存状态 | `206:835` | 七态 |
| `A②-卡8 Template Library List` | 模板清单与别名 | `232:670` | 四态 |
| `A②-卡9 Template Lifecycle` | 生命周期两态 | `232:724` | 三态 |
| `A②-卡12 Reference List` | 引用者列表 | `232:746` | 三态 |

**GPT 线（另一套并行投影，与本清单不是同一批）**：`178:291` 卡4 ComponentCard ／ `178:399` 卡5 Impact Preview ／ `183:484` 卡7 FieldValueControl。

**原快照未登记投影**：`A②-卡10`（模板改值·高影响）／`A②-卡11`（批量换绑）；工作状态见[问题台账 §6](OPEN-ITEMS.md#other-material-items)。

---

## 三、2026-09-20 的历史回读

旧用户语言、态9／10与颜色修正见[固定 §三](https://github.com/futouyiba/HitFish-Up/blob/e26af091bf90a049ed2f83ebe6642af240aa5c82/docs/review/ui-component-contract-r2/figma-current.md#三2026-09-20-的历史回读)；早于 `[04]` 的几何／分隔线与未补操作见[原 §九](https://github.com/futouyiba/HitFish-Up/blob/e26af091bf90a049ed2f83ebe6642af240aa5c82/docs/review/ui-component-contract-r2/figma-current.md#九r4-fig-02-的历史回读早于-04)；早于 Role badge 与作者词修正的 `[04]` 中间形态、annotation 校验与导出过程见[原 §十](https://github.com/futouyiba/HitFish-Up/blob/e26af091bf90a049ed2f83ebe6642af240aa5c82/docs/review/ui-component-contract-r2/figma-current.md#十04-的操作入口回读早于-role-badge-与作者词汇修正)。这些旧快照不承担当前缺口判断，也不把历史示意值当产品规定；现行交互见[卡2／卡3](contract-cards.md#operation-control)，实际资产按[§六](#image-evidence)读取。

导出试验、RGBA 比较失效、MCP／REST 管线差异、母件与作者面混拍、未随包 `141:283` 和高倍导出过程见[固定导出记录](https://github.com/futouyiba/HitFish-Up/blob/db97e9bb4784a8eaf2421cf88894c6d4e4beef2c/docs/review/ui-component-contract-r2/figma-current.md#L140)。**旧 REST 缓存归因已撤回**；原实验本轮未复现，不扩为通用机制结论。

---

## 四、本文件侧的记号与纪律（读图时注意）

- **未实现/未核必须标**：`⚑UNIMPL（GAP-ED-NN）` ／ `⚐UNVERIFIED` ／ `⏸BLOCKED`。**「未标」不等于「已实现」**。
- ★ **作者面 vs 投影面的文字分工（2026-09-21 补，读图前先读这条）**：
  - **作者面（Current 页那 3 帧 `1680×1220` 一族）** —— 画面里出现的串是**作者会读到的串** ⇒ **必须用作者词汇**（《编辑器界面》§1.2「操作的用户语言」＋《编辑器心智模型与 IA》§2 的作者词表）；`INHERIT`／`absent`／`CLEAR`／`SET` **不作作者可见串、也不加括注**。
  - **投影区（`PROJECTION｜…` 各组，`1680×1080` 一族）** —— 画面里出现的串是**给读契约的人的记号** ⇒ **`CLEAR`／`INHERIT`／`SET`／`absent` 在这里是合法的**，且**「作者词（操作令牌）」这种绑定括注正是投影帧该有的东西**（把作者词钉到 op 上）。
  - ⇒ ★ **同一条 finding 落在哪一面，结论会相反**：「作者面出现 `INHERIT`」⇒ **要改**；「投影帧出现 `INHERIT`」⇒ **不是缺陷**。
  - ⇒ **判帧靠 node 前缀 ＋ 尺寸两档**：`108:*`／`104:*`／`8:2` ＝ 作者面（1220 高）；`230:*`（`A①-卡2` 组）／`232:*`／`163:*`… ＝ 投影区（1080 高）。★ **不要只按 node 前缀猜** —— 以本文 §一／§二的登记为准。
- 图上的说明**一律走 annotation，不写 comment**；**不把说明文字画进画面主体**。
- 已知残留：`A①-卡2` 与 `A①-卡3` 之间的**间隙现为 70px**（因卡2 增高所致，**非设计意图**；同列其余间隙 200–240px）。

---

## 五、2026-09-21 节点与 annotation 回读记录

来源入口 overlay、Role chip／badge 与 annotation 的逐节点回读见[固定历史 §五](https://github.com/futouyiba/HitFish-Up/blob/db97e9bb4784a8eaf2421cf88894c6d4e4beef2c/docs/review/ui-component-contract-r2/figma-current.md#L83)，不再内嵌过程数据。仍须保留原快照的三条保护约束：

1. Policy 控制条 `108:364` 高122、内容到 y=121；原登记未裁切，容器高度有意保持，加高会占用与 `108:373` 的12px间隔。
2. 卡侧只显示物种层；行级操作在 Policy 控制条，不能把物种层缺少 CLEAR 当漏项。
3. 卡内四个 `SourceLabel` 已从实例移除；对该实例 `resetOverrides` 会使母件标签返回并重影。

节点计数须同时报告 `figma.skipInvisibleInstanceChildren` 的实读值；旧2318／2330的差别及annotation指纹在固定历史查阅，不能当成本轮测量。Role状态位的产品规则按[汇编 §9](component-contract-consolidated.md#role-record-intent)，图证据范围见 §六。

---

<a id="image-evidence"></a>
## 六、随包图像：逐资产版本与证明范围

资产基线为 main @ `fde61e3d3da68f1f2181c4fd37d1e76c348a098f`（已纳入 #17），本次不改图片，五图字节与固定基线一致。各图的内容版本与比例分别登记；导出参数相同不能推出同批，整帧与局部的取证时点也不能相互替代。

| 文件 | node | 像素／字节／作者登记比例 | SHA256 | 版本与可证明范围 |
|---|---|---|---|---|
| [0.3.4.0-B-editor-structure-108-311.png](img/0.3.4.0-B-editor-structure-108-311.png) | `108:311` | 1680×1220／182906／1× | `3221057b4b0a12f04e13b15e372d66ded643bbdfa57cee3d387ca755953b472f` | 整帧：`ef2a0c0c…` 重导，时段两处来源均为“未选”，摘要“未配（空态）”；Role badge 可见。原核对亲看，仅证明所拍画面。 |
| [0.3.4.0-B-card2-state10-230-673.png](img/0.3.4.0-B-card2-state10-230-673.png) | `230:673` | 890×150／24410／1× | `96aac32ea7ccbad882697b14a7be54e0b222bdd9a250535d6770b266e9c3ae58` | 态10 投影图，后续补图未改；不承担 Species Role 记录态对照。 |
| [0.3.4.0-B-policy-176-283.png](img/0.3.4.0-B-policy-176-283.png) | `176:283` | 820×92／13485／1× | `39bff36334e63e93cb70244e6be42b6d18e65e339789db314229bcca8050312c` | Policy 母件图，后续补图未改；不是作者面控制条。 |
| [0.3.4.0-B-policy-block-108-364.png](img/0.3.4.0-B-policy-block-108-364.png) | `108:364` | 854×122／22574／1× | `e174d1e798ab724746d7d4888ba72459bc75a1095e1b4538aa6c8c2e76985cac` | 局部 SET 图，`386ad383…` 重导为 1×，可见 Role badge；替代 21871 字节旧画面及 51787 字节的 2×中间版本。 |
| [0.3.4.0-B-policy-block-108-364-INHERIT.png](img/0.3.4.0-B-policy-block-108-364-INHERIT.png) | `108:364` | 854×122／21871／1× | `b1c0d2a55f89bd0aa27fd3143724bfb0da1349193d01f04b1b7130abd6be9dc1` | 局部 INHERIT 图，#17 @ `8d4523c…` 换为 1×；无 Role badge、整排收拢，无预留槽位。作者登记与 SET 同为 REST／scale=1；同管线同参数不等于同轮导出，不能单凭图证明 durable 读写。 |

**旧版与引用边界**：旧 2.5× INHERIT 的指纹、尺寸和重导经过见[固定登记](https://github.com/futouyiba/HitFish-Up/blob/e26af091bf90a049ed2f83ebe6642af240aa5c82/docs/review/ui-component-contract-r2/figma-current.md#image-evidence)，不属于上表当前资产。整帧／SET 的落地提交与固定被审 PR head 是两种锚：历史 blob URL 指定的是被审快照，不能为了与 main 对齐而换成 merge SHA。

**1× 图的对照范围**：当前 INHERIT 与 `1409a13fde46dcb8d10bae039c26f6a0090bf497` 的旧局部 `0.3.4.0-B-policy-block-108-364.png` 逐字节相同，本次已核字节相同。新资产的 INHERIT 身份按 #17 的交付记录登记，不能反过来把原先未经记录态标定的旧图称为当时已经交付的 INHERIT 证据。[#17 独立 REVIEW](https://github.com/futouyiba/HitFish-Up/pull/17#issuecomment-5758641670) 亲核当前两张局部图 RGB 差异为 6217 像素、bbox `(201,107,832,121)`；这一证据只覆盖两张局部图的像素范围，不证明整份 Figma 的节点、annotation、隐藏内容或持久化行为。

两态图按作者登记分别对应 SET 与 INHERIT；实际画面的亲看结论沿既有审核。记录态对应关系与审查处置见[Species Role UI](OPEN-ITEMS.md#species-role-ui)。图片增加或替换时更新本登记的实际文件、版本、指纹与证明范围。

**原作者的形态说明**：`INHERIT` 按“无预留槽位”渲染；补图提交援引 Owner“以后再考虑固定槽位、现在不为这件小事延长设计”的裁定，登记整排左收 66px。保留这份来源记录，不把两态说成位置一致；本批未重测几何或重验该裁定。

**核图方式与历史边界**：指纹可核版本，不单独证明内容、同批导出或实时画布一致；对拍要核差异像素，并用确知不同的样本验证比较方法。旧导出试验及已撤回解释见[历史入口](#三2026-09-20-的历史回读)，不作为本轮测量。

**本次元数据核验**：五张 PNG 的 `pHYs=2835/2835 unit=1`、`tEXt Software=Figma`、color type 6、bit depth 8；尺寸与登记一致。作者登记比例均1×；这些元数据本身不能证明导出通路、图片同批、实时画布一致或记录态。

---

<a id="source-entry-evidence"></a>
## 七、原快照的 annotation 摘要（不在 PNG 内）

annotation 不在 PNG 内。原组总则与 chip 逐字见[固定历史 §七](https://github.com/futouyiba/HitFish-Up/blob/db97e9bb4784a8eaf2421cf88894c6d4e4beef2c/docs/review/ui-component-contract-r2/figma-current.md#L179)；其中旧操作词和9-chip形态不当作较晚图片的当前文案。

保留的来源入口摘要：`108:311`／`108:335` 顶部 `templateRow` 的四个前层来源选择器与卡内快速编辑入口读取同一 Component Recipe Source truth；不是两个编辑器。该帧是物种上下文，卡上 Role 角标／层签／继承状态分别表达结果值、所在层与记录态。Policy区Role行与卡上Role入口读同一Policy truth。具体产品规则见[汇编 §7](component-contract-consolidated.md#7-组件卡--焦点编辑栏)；时段来源实际画面及关闭证据分别见 §六与[问题台账](OPEN-ITEMS.md#source-sync)。

---

## 八、原快照的卡上 Role 角标 —— 为什么它是"三态下拉"，以及为什么它**不做成白场**

原快照的 Role 角标是带矢量 `roleCaret` 的三态下拉，不是纯状态徽标；保留角色色而非统一改成白场。原命名／颜色裁定为记录页 §104 四：CORE蓝／SECONDARY琥珀／IGNORED灰。尺寸、色值、与Source选择器的对照及“advance vs 墨宽”的推导见[固定历史 §八](https://github.com/futouyiba/HitFish-Up/blob/db97e9bb4784a8eaf2421cf88894c6d4e4beef2c/docs/review/ui-component-contract-r2/figma-current.md#L192)；本轮未重新测量，不把排版推导当实测。

---

## 十一、已知漂移：共享母件 `93:54` 的作者可见串修正 → 顶栏右移 53px

**裁定：`ADJ-FIG-ARCHIVE-01` ＝ C_NARROW（Owner 2026-09-21）。**

【漂移已知】**顶栏 strip 的 10 个 chrome 节点**因共享母件 `93:54` 的作者可见串修正而右移 **53px**（按钮宽 `47 → 100`、徽标 x `+53`）—— 涉及 **Current 页 4 个实例 ＋ 归档 2 个实例**（`93:215` ⊂ `47:2`；`180:493` ⊂ `180:392`）。

**保护性证据未受影响**（裁定明列）：**5×5 legacy 控制拓扑** ／ **标签·状态·交互语义** ／ **结构关系** ／ **可行性证据** ／ **既有 node id 与按 id 的引用**。

像素级历史外观见 **FrozenSnapshot**（冻结版本 `2401504721345405021`）—— **活体归档帧不再需要在「非证据性 chrome」上逐像素一致，那份责任由 FrozenSnapshot 承担**。

⚠️ **未来任何触及上述保护性证据的共享母件漂移，不在该裁定覆盖内，必须重新评估。**

★ 本节是**一句注记**，**不是**漂移追踪系统（裁定明禁另造）；**归档侧同一句由画布侧落**。

# REVISION 7 — `R3-FIG-01` 与 `R3-F-05` 的裁定处置（2026-09-21）

对齐 head：`41c641f48c2edeb050f2e4d0ff35b8bf024fb644`（REVISION 6）。**本版只处置两条**；另外两条（`ann[0]`、IA §1）**不在本 PR 上**，见第四节。

---

## 一、`R3-FIG-01` —— **你们说对了：是契约文本陈旧**（裁定：乙）

**裁定**：`CONTRACT_TEXT_STALE` —— **图面方向保留、不重画**；**先改契约投影**。

你们引 `§7`「卡的 Source 下拉与**焦点编辑栏**的 Source 选择器指向同一个组件 Recipe Source binding」—— **我们核过，`§7` 确实这么写**；而图上实际是**顶部 `templateRow` ＋ 卡内入口**。⇒ **两条载体相抵，成立。而错的那条是契约文本。**

**为什么是拓扑（乙）而不是给焦点编辑栏补一个 Source（甲）**：

- **最新 UI Current 已把焦点编辑栏的职责收成逐字段 Value／Operation／Provenance 编辑** —— 它**没有明确要求 Source selector**；而 Current 又明确要求**卡可就地改模板／Source**，并且有「**每组件一个前层 Source 选择器**」。
- **产品方向**：Source 是**组件级前层选择**，**不应要求先钻进某个字段编辑上下文才能改**。
- **复杂度**：再加一个 Source 选择器 ⇒ 「**Top Row ＋ Card ＋ Focus Editor 三个 mutation surface**」，**复杂度没有买到新能力**。

⇒ 钉死的形态（**已改进 `component-contract-consolidated.md` §7**）：

```
前层 Source Selector（顶部 templateRow）
        ↕   同一份 Component Recipe Source binding
Component Card Source dropdown
```

**并明写**：**焦点编辑栏不提供 Source 下拉** —— 它只显示当前 Source 的上下文／来源说明。

**Role 部分不动**：`Component Card Role ↔ Policy Role Row`，**仍是双入口单 Truth**。

**本版没有改图。** `figma-current.md` 与随包实图（`108:311`，REVISION 6 已换成同批新图）**画的正是 Top Row ＋ Card** ⇒ **图与改后的契约文本一致**；`108:311` 上那张图就是本条的证据。

---

## 二、`R3-F-05` —— **缺口成立，但你们给的修法被否**；真裂缝在别处

### 2.1 你们那条诊断的**位置**不准

> 你们说：Role override key 只有 `species_key + component + row_key`，**所以无法表达物种层 default**。

**这个表述不完全成立。** 《编辑器持久层契约》**§3.1 已有 Species Base Record（key ＝ `species_key`，roles: Temperature／Structure／FeedingLayer／TimePeriod）** ⇒ **物种层「最终默认 Role」已经有存储位置**。而 **§3.4 的 `species_key + component + row_key` 本来就是专门给 row-level Role Override 的** —— **不应该同时拿来装 species default**。

⇒ **明确否决「给 Role Override 加 `layer={species,row}`」**：那会把**两个本来粒度不同的概念重新塞回一张 record**，**正好违反 Current 已明确的「Species default ≠ row-level Role override」**。

### 2.2 但**真裂缝确实存在，且比你们指的那条更深**

新 Policy Template 语义已规定 **Policy Template → Species Policy Recipe → Affinity Policy Patch**，而**旧 record shape 跟不上**：

| 处 | 问题 |
|---|---|
| `§3.1` 的 `roles` | **只存最终默认 Role 值** —— 既**没有表达「物种当前绑定哪个 Policy Template」**，也**没有表达「这个 Role 是 `INHERIT` 还是 `SET`」** |
| `§3.4` 的 row override record | **只有 `role` 字段**，却声称支持 `CLEAR / SET` ⇒ **没有 `op`，实际无法区分 `CLEAR` 与「`SET` 恰好等于 template raw role」** |

⇒ **这不是 Figma polish，是 Persistence Current 自己出现了「新 Policy Recipe 语义 ＞ 旧 record shape」的裂缝。**

### 2.3 裁定：**物种层与 row 层分开表达**（不设 `layer`、不用哨兵）

```
Species Policy Recipe        key = species_key
  · policy source binding
  · Temperature / Structure / Feeding / Time 的 Role op
  · fail_env_coeff op

Affinity Policy Patch        key = row_key (+ 适用时 component)
  · Role patch:            CLEAR | SET
  · fail_env_coeff patch:  CLEAR | ADD | SET
```

- **不需要 `layer` 判别字段**，**也不需要 `scope_key="*"` 这种哨兵**。
- **物种层默认每组件恰好一条**：**每个「物种 × 组件」恰好一个 Effective Default Role**；物种层若用 operation 表达，**最多一个 local Role op**，`INHERIT` 用 **absence** 表达。⇒ **唯一键 ＝ `(species_key, component)`**；**Role 值绝不能参与唯一键**。

**你们说得对的那一半**：**Figma 侧「物种层默认」与「桶层操作」确实需要视觉分开**，否则用户分不清当前改的是哪一层 —— 这一条我们记下，**但它要等契约文本落定之后再动图**（顺序：先契约、后图）。

### 2.4 ⚠️ 本版**落了一半**，如实说明

| 载体 | 状态 |
|---|---|
| 冻结卡 `RoleControl` 的 durable 形状 | **已改**（两条记录 ＋ **行级 patch 必携 `op`** ＋ 唯一键 `(species_key, component)`、Role 值不进键；依据改挂记录页 §331） |
| 《编辑器持久层契约》**§3.1／§3.4 的正文** | **尚未落** —— **这一席不是那两页的写入者**，已按单一写入者规则路由 |

⇒ 请把本节读成「**形状已裁、契约正文待落**」，**不要读成「契约已改完」**。

---

## 三、随本版的改动

| 文件 | 改了什么 |
|---|---|
| `component-contract-consolidated.md` §7 | 入口拓扑句改成「**前层 Source Selector ↔ 卡 Source 下拉**」；明写**焦点编辑栏不提供 Source**；Role 表述不动 |
| `contract-cards.md`（`RoleControl`） | durable 形状**拆成两条记录**；补「**行级 patch 必须携 `op`**，否则 `CLEAR` 与「`SET` 恰好等于模板 raw 值」不可区分」；唯一键与粒度句改写成 `(species_key, component)` |

**两处都只动文本，未动图**；图侧的几何与节点数与 REVISION 6 相同（`108:311` 的随包图为 REVISION 6 同批导出，未再重导）。

---

## 四、另外两条**不在本 PR 上**（说明，不作回应）

- **`ann[0]`（审阅留痕迁出）**：裁定 = **同意，非门项、纯卫生项**。保留当前读图规则与判断口径，把「谁提了什么／为什么这么回／某轮怎么争」迁去治理页。**有 Figma 并发 writer 时不插手**，排在当前 contract gate 之后。
- **IA §1 基准句**：裁定 = **`REQUIRED CURRENT FIX`**，纳入 Notion 侧集成，由**唯一写入者**落；逐字替换为「ADD 的基准是当前来源值；当前来源可以是共享模板，或该组件合法使用的物种生态数据（`SPECIES_CONCRETE`）。」，**只做语义基准句扫描，不全局替换「模板值」**。

这两条**不需要你们在 PR 上闭合**，列在这里只为让「已裁但不在本 PR」这件事有记录。

---

**通过判据**见 `REVIEW-PROMPT.md` §六（两层门）。

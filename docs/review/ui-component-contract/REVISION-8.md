# REVISION 8 — `R4-F-01` 的落笔形状已裁：更正我们在 REVISION 7 里写的形状（2026-09-21）

对齐 head：`1de2338177a5e1d47e0f116ab99bf9ce004ef649`（REVISION 7）。

---

## 一、先说一句必须说的：**REVISION 7 里我们写的形状，有一半是被否掉的**

`R4-F-01`（Role 两层持久化形状）已经裁决落定。而**我们在 REVISION 7 写进 `contract-cards.md` 的那一版，正是被否掉的那一版** —— 具体两处：

| REVISION 7 我们写的 | 裁决结果 |
|---|---|
| **`Species Policy Recipe`（key ＝ `species_key`）当那条记录的名字** | **否**。`Species Policy Recipe` 只能是 **Policy 专属子结构**的名字 —— §3.1 那条记录**不只装 Policy**（还装四个组件值与 `name_cache`）⇒ 它是 `Species Base Record`／底板记录，**不改名** |
| **`species_key` 只降为属性、`scope_key` 字段名不动** | **否**。`scope_key` **正式改名 `row_key`**（不是简称）；理由：§3.4 的 `scope_key` 本来就「固定取 §3.2 的 `row_key`」，留一个泛化名**没买到能力、反而暗示还有别的 scope** |

⇒ 本版**只改这一处**：`contract-cards.md` 的 `RoleControl` durable 形状（执行投影）。**这是我们交付物的错，不是复审的解读问题。**

---

## 二、裁决后的形状（本次落进冻结卡的）

```text
Species Base Record                key = species_key
├─ Component Recipes              （Species Recipe：四个 Component 的 Source ＋ field operations）
└─ Species Policy Recipe          （Policy 专属子结构）
   ├─ policy source binding
   ├─ Role op × 4
   └─ fail_env_coeff op

Affinity side
├─ AffinityAuthoringPatch         → sourceOverride ＋ numeric operationPatches（bucket-level）
├─ AffinityRolePatch              key = (row_key, component)   → op = CLEAR | SET；role（SET 时必携）
└─ AffinityFailEnvCoeffPatch      key = row_key                → op = CLEAR | ADD | SET；value（ADD／SET 时必携）
```

**四条要点**：

1. **row 层是两条独立的 durable record（sibling track），不用 `field`／`track` 判别列** —— 因为两轨**维度不同**（Role ＝ `row × component`；`fail_env_coeff` ＝ **整 row 一份**）且 op 词表不同。**这不与「不需要 `layer` 判别字段」相抵**：这里根本不建跨 layer 的万能 record。
2. **`Species Base Record` 不改名**；四个叫法**按层级拆开**（`底板` ＝ 概念名／`Species Base Record` ＝ §3.1 整体／`Species Recipe` ＝ 组件 recipe／`Species Policy Recipe` ＝ Policy 子结构）。**「一物四名」不是靠删词解决，是把层级概念重新分开。**
3. **`AffinityAuthoringPatch` 与 `AffinityPolicyPatch` 并列**，不改名、不合并 —— 除职责不同，**粒度也不同**（numeric ＝ bucket-level／Role ＝ row-level）；合并会**重新制造已明确禁止的 bucket/row 粒度混合**。
4. **`species_key` 降为属性**（组织／查询／reconcile／诊断），**不参与 identity**；Role patch **唯一键 ＝ `(row_key, component)`**。

**四个「没有」**：没有 `layer`、没有 `"*"` 哨兵、没有 nullable scope、没有 `track` 判别列。

---

## 三、⚠️ 一处跨结果的字面不一致，我们**标明这是取舍、不写成已裁**

裁决文本里：`CT-01` 的 `AffinityRolePatch` 字段表**没有 `species_key`**；而 `CT-04` 的 canonical shape **含 `species_key` 作属性**。

⇒ **我们取 `CT-04`**（它是对「该记录字段表」更具体的那一条；且它正文自己写「`species_key` 继续留作 组织／查询／reconcile／诊断」——**要留就得在字段表里**）。
⇒ **但这是我们按「更具体者优先」做的取舍，不是它明说的。** 若裁决方或 Owner 随后澄清，按澄清改。**在卡里我们把 `species_key` 写成属性、并把这一处取舍标出来。**

---

## 四、边界

- **本版只改执行投影（冻结卡 `RoleControl`）**，未动契约正文 —— 《编辑器持久层契约》§3.1／§3.4 的正文由**该页的唯一写入者**落，**正在落**。
- **`R4-FIG-02`（图侧把「物种层默认／桶层操作」视觉分开）仍在**，按 Owner 的序：**先契约、后图** —— 等 §3.1／§3.4 正文落定后再动图。
- **`ann[0]`** 仍旧排在当前 contract gate 之后。

**通过判据**见 `REVIEW-PROMPT.md` §六（两层门）。

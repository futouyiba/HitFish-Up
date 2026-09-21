# 0.3.4.0-B 开发 brief —— 可开工面 / 阻塞面

**对齐时点**：2026-09-21。**依据 = 权威载体当天直读**，不是包内派生件。

**每条的出处状态**（下游必须能分辨裁定与口误）：

| 标签 | 含义 |
|---|---|
| **【契约】** | 《编辑器持久层契约》**当天逐字直读** |
| **【画布】** | Figma 画布节点 / annotation **当天直读** |
| **【待核】** | 我没逐字核 —— **别当裁定用** |

---

## 一、可以开工 —— 持久化 schema 已闭

### 1. 三个 durable 记录：`Species Base Record` / 生产行台账 / 两条 patch 轨道 【契约】

- **`Species Base Record`（每物种一条，§3.1）** ＝ 物种层的 durable aggregate，内含两条子结构：**`Component Recipes`（四组件的 Source ＋ field operations，＝ `Species Recipe`）** 与 **`Species Policy Recipe`（Policy Source ＋ 四个 Role op ＋ `fail_env_coeff` op）**。**它是整条记录的名字，不等于其中任一条子结构。**
  - 字段：`schema_version` / `species_key`（**键 = 物种 id，不是 name**）/ `name_cache`（**仅作比对基线**，不作键、不导出）/ `temperature`·`structure`·`feeding_layer`·`time_period`（组件值或空）/ `policy_source_binding`（模板标识，必填）/ `roles`（四组件 Role op，必填）/ `fail_env_coeff`（op）。
  - **组件值 = 该组件的字段集；空 = 该组件在这个物种上尚未配置，是合法状态。**
  - **底板没有生产侧标识**：它不进生产表 ⇒ **本记录不含任何子表行引用**。初值**导入时从配置表推出**（取该物种最频繁那份画像的代表行），此后**以编辑器为准**（是种子，不是持续的 Production → Editor 覆盖）。**不能初始为空** —— 否则「还没配」与「配成空」无从区分。
- **生产行台账（§3.2）** ＝ **每个既有 `FishEnvAffinity` 行一条，不折叠**。`row_key`（**键**：生产侧既有行用其行 id；编辑器新造、未写回的行用**编辑器侧稳定键**）/ `row_id`（**空 = 编辑器侧新造、尚未写回**）/ `species_key`（属性，不是键）/ `bucket` / `refs`（四组件的子表行标识）。**它是编辑器自有的关联台账，常驻耐久层**（生产侧没有「哪一行属于哪个物种的哪个桶」这个信息）。
- **两条 row-level patch 轨道（§3.4）**，与 §3.3 的 `AffinityAuthoringPatch` **并列、不改名、不合并**：
  - **`AffinityRolePatch`**：`row_key` ＋ `species_key`（**属性，不参与唯一键**）＋ `component` ＋ `op` ＝ **`CLEAR | SET`** ＋ `role`（`SET` 时携 `CORE|SECONDARY|IGNORED`）。**唯一约束 `(row_key, component)`。**
  - **`AffinityFailEnvCoeffPatch`**：`row_key` ＋ `op` ＝ **`CLEAR | ADD | SET`** ＋ `value`（`ADD`/`SET` 时携）。**唯一约束 `row_key`（整 row 一份）。**
  - **不携 `op` 则 `CLEAR` 与「`SET` 恰好等于模板 raw 值」不可区分；`op` 不得从值反推。**

### 2. op 词表与 allowlist 【契约 ＋ 画布】

| 轴 | 物种层 | 桶 / 习性档案层 | ADD |
|---|---|---|---|
| **Role** | `INHERIT / SET` | `absent / CLEAR / SET` | **不允许** |
| **`fail_env_coeff`** | `INHERIT / ADD / SET` | `absent / CLEAR / ADD / SET` | 允许 |
| **numeric**（§3.3） | `ADD(delta) / SET(value)` | 另有 `CLEAR` | 数值型允许 |
| **枚举绝对值**（如水温 `falloff`） | `INHERIT / SET` | `absent / CLEAR / SET` | **不得 ADD** |

- **`INHERIT` ＝ 无记录**（**不造第三种记录**）；「记录存在 = 已覆盖，记录缺失 = 继承底板」。
- `CLEAR` ＝ 移除继承自物种层的 operation，**回到物种当前 Policy Template 的 raw 值**。
- **`fail_env_coeff` 越界**：最终值仍须满足 `[0, 0.10]`，越界 **Validator 报错，不 silent clamp**。
- **【画布】** 上述 op 集在 Figma 卡2 已画出可目视对照的形态：态1／态6／态7 把 `absent`／`CLEAR`／「缺省支」并排画开；态9 画「层 × 字段类型 ⇒ 选项集」；态10 画「原地展开（不设二级 drawer）」。

### 3. `sourceOverride` 的落点 【契约】

- **桶层的 patch ＝ `AffinityAuthoringPatch`（owner ＝ `FishEnvAffinityRef`）**：**每组件可选 `sourceOverride`（换 Source —— 承载「桶可以换模板」）** ＋ 逐字段 `operationPatches`（`CLEAR | ADD | SET`）。
- **同源显式 pin 保留**：`sourceOverride` 与物种层 Source 相同时**也不自动移除** —— 无 `sourceOverride` ＝ 未来物种层换 Source 时跟随；显式 `sourceOverride` ＝ **钉住**。（与「SET 同值仍是显式 pin」同一条判据：**当前 payload 相等 ≠ authoring intent 相等**。）
- **两条 intent 不可混淆**：`SET 0.8`（模板值也是 0.8）**会阻断未来模板改值** ⇒ 自有 projection；`sourceOverride ＝ A ＋ 零 op` 表示未来继续跟随 A ⇒ **可安全复用 A 的行**。
- **硬删除护栏（§3.10）**：Hard Delete **仅允许 DirectReferenceSet 为空**，须检查 Species Recipe source、Affinity `sourceOverride`、SpeciesPreset 及其它 durable 引用。**ARCHIVED ≠ 可删。**

### 4. 两个引用集必须分开（§3.10）【契约】

- **DirectReferenceSet(A)** ＝ durable state 里**直接写了 A 的 source ref** 的对象（Species Recipe source、Affinity `sourceOverride`、SpeciesPreset binding、Policy source）⇒ 用于 **Replace References 的改动目标 / hard-delete guard / 直引清单**。
- **EffectiveConsumerSet(A)** ＝ Resolve 后**当前 Effective Source ＝ A** 的全部最终 Recipe（**含经物种层继承者**）⇒ 用于 **Impact Preview / before-after 分析**。
- ⇒ **「直接引用数 / Effective consumer 数 / 最终结果变化数 / 新增 Error·Warning」是四个可以互不相同的数字。**
- **Replace References（A → B）只改 DirectReferenceSet**：保留既有 operations / patches、重 Resolve 全图、before/after Impact Preview、**原子提交**。**禁止**给所有 EffectiveConsumer 自动写 `sourceOverride = B` —— 那会把经继承消费的 child 变成**显式 pin**，静默改变 authoring 拓扑。
- **`Affinity` 没有 `policySourceOverride`** ⇒ **不得虚构这类 direct ref**。Policy Template 的 direct refs ＝ Species policy source binding ＋ SpeciesPreset policy binding。

### 5. `absent` / `CLEAR` / 「恢复为底板」是**三件不同的事**（§3.5）【契约】

- `absent` ＝ **没有记录**（走缺省支）。
- `CLEAR` ＝ **有一条记录**，效果是回到 Effective Source 原值。
- 「恢复为底板」＝ **删除该覆盖记录**（**第三个独立动作**）。
- **判据**：**「覆盖这一项」即使值恰好等于底板当前值，也不跟随** ⇒ **最终值相同 ≠ authoring intent 相同**，实现必须**读记录、不读值差**。

### 6. Source 与分类的硬约束 【契约】

- **`templateId / stableKey` 创建后 immutable**；`displayName` 可改（**display rename ≠ identity rename**）。stableKey 有误 ⇒ 新建模板 → Replace References → 归档旧模板，**不提供 identity rename**。
- **Component Source 分两类**：`SHARED_TEMPLATE`（可共享模板资产）与 `SPECIES_CONCRETE`（物种自有生态数据，**不是**可共享资产）。
- **Broken source ref**：Editor 允许加载（便于修复）并报精确 `BROKEN_SOURCE_REF`；Resolve / Publish **不得**当 inherit / default / fallback；**Publish hard block**。判据：**load tolerant, publish strict**。
- **高影响 Source 变更**（改完整值 / Replace References / Concrete reimport / 批量换绑）一律 `prepare → before/after Impact Preview → 显式确认 → 原子 durable 提交`。**Preview buffer 是短命 UI state，不是 durable Draft Entity**（**不建** SpeciesDraft / ModeDraft / TemplateDraft / per-panel draft）。
- **numeric override 的 `scope_kind` 恒为 literal `bucket`**（**不允许 row-level**）；带 `scope_kind=row` ⇒ Validator 按与 Current Schema 不一致处理，**不得静默接受**。

---

## 二、**别按我说的做** —— 我还没逐字核 / 页上未展开的

1. **组件值的「内部形态」**：§3.1 只给到「`temperature` / `structure` / `feeding_layer` / `time_period` = 组件值或空」，**没有展开一个组件值内部怎么装 Source ＋ 逐字段 operation**。记录级字段已定，**序列化细节【待核】** —— 落码前与契约负责人确认，别自行发明。
2. **`AggregationRole` 的三个值与次要聚合的现行数值**：**【待核】**，按现行页复核。
3. **`fail_env_coeff` 的 GAP-013/014 现状**：**【待核】**（打开条件我记的是「列＋值都就位」；空列会把 264 行判非法）。
4. 上面第一节各条的**逐字**我核过，但**页会动**：落码前回到该页**再读一次对应小节**。

---

## 三、给实现方：怎么读这些依据

1. **权威顺序：记录页 > 设计页**。需求文档/契约是「现在是什么」；**画布是「目标态投影，不代表已实现」**。
2. **Figma annotation 读得到，但有坑**：REST `GET /v1/files/{key}/nodes?ids=…` **读得到**（本会话已验）；**`get_metadata` 读不到**（**别据它判「没有说明」**）；`get_design_context` 能，表现为 `data-annotations`。
3. **判「动没动」用等值（字节 / sha256）**；**`version` 连"动没动"都判不了**（受控实测）。
4. **`lastModified` 是分钟粒度、单向可信**：前进 ⇒ 一定写过；**没前进 ⇒ 不能反推没写**。证"没写过"只能**内容对拍**。
5. **图与图之间比字节，先同源**：不同导出管线（插件 `exportAsync` vs REST `scale=1`）出的是**不同产物**，差约 1%。**先用一个未动节点标定管线**（未动节点的重导应与基线逐字节相同）。
6. **两个寄存器别混**：`INHERIT` 这类**名字**与行内**显示给作者的具体串**是两回事，两者不矛盾、也不得合并。

---

## 附：本 brief 依据的取数（可复核）

| 取数 | 值 | 怎么取的 |
|---|---|---|
| 《编辑器持久层契约》§3.1／§3.2／§3.3／§3.4／§3.5／§3.10 | 逐字 | 当天直读该页 |
| 《编辑器持久层契约》§3.4 节标题 | 「Affinity Role Patch 与 AffinityFailEnvCoeffPatch｜两条 row-level 轨道」 | 当天直读 |
| Figma `108:335` annotation | 526 字 · sha12 `970742371cfd` | REST 直读 |
| Figma `108:364` annotation | 546 字 · sha12 `013d7004b126` · `&`＝0 | REST 直读 |

# 0.3.4.0-B 开发 brief —— 可开工面 / 阻塞面

**对齐时点**：2026-09-21（**第二轮**：补齐 §3.6／§3.7／§3.8，并折入当日新裁）。**依据 = 权威载体当天直读**，不是包内派生件。

**★ 基准指针**（本 brief 是**辅助件**，不是权威）：

| 载体 | 地位 | 说明 |
|---|---|---|
| `docs/review/ui-component-contract-r2/`（PR #7 分支） | **主基准** | 投影目录；**读它的 SHA 记在此处会立刻过期** ⇒ 用 `gh pr view 7 --json headRefOid` 取当前 head |
| 本项目内的 Current 文档（记录页 > 设计页） | **权威** | 两者冲突时以 Current 为准 |
| **本文件** | **辅助** | 可开工面／阻塞面的**摘要**；**不替 Current 措辞**。**落码前回到 Current 再读对应小节。** |

**每条的出处状态**（下游必须能分辨裁定与口误）：

| 标签 | 含义 |
|---|---|
| **【契约】** | 《编辑器持久层契约》**当天逐字直读** |
| **【画布】** | Figma 画布节点 / annotation **当天直读** |
| **【裁定·未落页】** | 当日裁定**逐字来自裁定方**，但**尚未落进 Current 页**；**按裁定执行，落页后以页为准** |
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

### 7. 模板清单与别名（§3.6）【契约】

- **`kind` ＝ `TemplateKind` ＝ `TEMPERATURE | STRUCTURE | FEEDING_LAYER | TIME_PERIOD | SPATIAL_OPPORTUNITY_POLICY`** —— **第五类用 Policy payload，不是第五个 Component**。
- 字段：`template_key`（生产子表行标识；**时段 ＝ 组名**；**空 ＝ 提取出来但尚未物化**）/ `editor_key`（`template_key` 为空时必填）/ `name_zh` / `name_en`（**不是生产行 name**）/ `lifecycle`（`ACTIVE | ARCHIVED`）/ `extracted_from`（**只作追溯，不是关联依据**）。
- **唯一约束**：`template_key` 非空时按 `kind + template_key`；为空时按 `kind + editor_key`。
- **第五类的边界**：只进**模板分类** —— **不扩 `ComponentType`、不改 Runtime 四条件槽位、不新增 Production Policy 子表**；payload ＝ 四个聚合角色 ＋ `fail_env_coeff`；**生产侧仍只物化到 `FishEnvAffinity` 的角色列 ＋ `fail_env_coeff`**。模板 identity（`templateId / stableKey` immutable）、`ACTIVE / ARCHIVED`、Replace References、Hard Delete 生命周期**对五类一并适用**。

### 8. 编辑器层 → 生产层的对应（§3.7）【契约】

**展开规则（写回时逐行执行）**：对每条生产行 R（物种 S、桶 B），对每个组件 C 的每个项 k —— **有 numeric override 取 override 值，否则取底板值** ⇒ 得到 R 在 C 上的完整值 ⇒ **沿 Authoring lineage 复用上游已存在的 Profile；跨无关 lineage 不得仅凭完整值相等自动合并；两者皆无才新增一行** ⇒ 把该子表行引用写回 R。Role 同理：**有 row 级 override 取 override，否则取物种默认** ⇒ 写回该 `FishEnvAffinity` 行。

- **★ 展开的第三条臂（组件级）**：**底板为空** ∧ **该组件 `Effective Role = IGNORED`** ⇒ 该组件**不产生 Component Profile 的 production projection**、**不创建显式空 Profile**、**不因这一点阻断 Publish**；而 **`FishEnvAffinity` 主行与该组件的 `Role = IGNORED` 仍正常写回**，只是**不生成／不写回该组件的完整 Profile 子表值**；`ProductionRowLedger.refs[component]` **保持空**。**「空」＝「尚无该组件的 production projection」，不是一种新的 Runtime Profile 值**（该组件**因 `IGNORED` 根本不进入 evaluator**）。
  - **本臂的两条是合取，作用域不得放宽**：**`Effective Role = CORE / SECONDARY` 且缺必需 Profile ⇒ 仍按既有规则阻断 Publish** —— 本臂**不覆盖、也不弱化**它。
- **粒度不变量**：**四个 numeric 组件全部按 bucket**（`(species, bucket, component, member)`，**TimePeriod 不按规格／row**）；**Role 单独按生产行覆盖**（**同 id 组合的不同行可以有不同 Role**，Validator **不得**因「同组合、Role 不同」报错）。⇒ **numeric 与 role 故意使用不同粒度，不要把二者塞进同一条 record shape。**
- **四件必须写明的事**：① **底板不进生产表**；② **零覆盖的生产行也落完整值**；③ **恢复为底板 ＝ 删除 override record**（「override 值刚好等于底板」**仍是 override**）；④ **生产子表按 Authoring lineage 复用**，**跨无关 lineage 不得仅凭完整值相等自动合并**（「碰巧同值 ≠ 有意共享」）—— 本条范围 ＝ **编辑器的使用／导出保存路径**；**数据迁移另走「按完整最终值复用同值行」**，**两套规则明写分开**。**Runtime 只读最终全量，不做 base + delta 合并。**
- **复用判定按结构 lineage，不按 payload 相等**：物种层 Source ＝ 共享模板且无任何 Effective Operation ⇒ **直接复用该模板的 production profile**；`SPECIES_CONCRETE` **即使无 op 也属物种自有 projection**。桶层先 Resolve 出 Effective Source 与逐字段 Effective Operation —— **完全继承物种 Recipe（无 `sourceOverride`、无字段 patch）⇒ 复用物种 projection**；**有显式 `sourceOverride` 但最终 Recipe 恰为「纯共享模板 ＋ 零 op」⇒ 复用该模板的 production profile**（**显式 pin 只分叉继承关系，不强制复制行**）；**最终仍含任何 Effective Operation ⇒ 该桶自有 projection**。★ **`equal-value SET` 与纯 source pin 必须区分**：`SET 0.8`（模板值也是 0.8）**会阻断未来模板改值** ⇒ 自有 projection；`sourceOverride = A ＋ 零 op` ＝ 未来继续跟随 A ⇒ **可安全复用 A 的行**。

### 9. 版本与升级规则（§3.8）【契约】

- 版本字段**逐记录携带** —— 任何一条记录被单独摘出来比对时都能自证版本。
- 版本不符：**报错，不猜、不静默升级**。
- 升级**不自动发生**：一次性迁移脚本 → 迁移后旧文件**由 Git 保留**（Git 就是备份）→ **迁移是显式动作**。
- 空文件与结构**由 schema 生成**；生成器**拒绝覆盖已有作者数据的文件**，**不提供单旗标绕过**；真要清空须走**显式双旗标**。
- **schema 与生成件之间有 parity 测试**：schema 改了而生成件没重生成即报错。

### 10. 当日新裁（`ED-15` / `ED-13` / `ED-20`，含 `§117` supersede）【裁定·未落页】

> **落页状态**：这三条**已裁、可直接实现**；**尚未落进 Current 页**。**落页后以页为准。**

- **`ED-15` 物种级粒度**：**`Species Base` 是主要 Authoring Truth；`young` / `mature` 只是稀疏 exception scope** —— **绝大多数相同的鱼根本不产生 bucket patch**。正确结构是 `Species Base` ＋ 逐桶的**稀疏** patch（**大部分为空**），**不是每桶一份完整 Profile**。
  - **不加钓场维**（legacy 数据按钓场重复多，**推不出「鱼习性该有钓场维度」**）。
  - **`mature` 内部的 quality 差异本期接受压平**（如 Bass 的 `Unique / Apex → period_crepuscular` 若与成年冲突会损失）—— **不得为此新增 quality override 或第三／第四 bucket**；★ 但 **Bootstrap／Migration 必须报告这种 lossy collapse**（migration diagnostic，**不是新的 authoring dimension**）。
- **`ED-13` 三级命名 ＋ 寻址分层**：命名按「**最小业务归属**」分三级 —— **共享 Template 级 `<Kind>_<Template>`**（**已有对应 production row ⇒ 直接复用、不新增行**）／**Species 派生级 `<Kind>_<Species>`**／**Bucket·Affinity 派生级 `<Kind>_<Species>_<Bucket>`**。前缀**沿用现有表主前缀**（`Cover_` / `FeedLayer_` / `Temp_` / `period_`）。**`name` 不作 Editor identity；不要把完整 inheritance/provenance 链塞进 `name`。**
  - ★ **寻址是分层的，不是二选一**：**内部定位 → stable id / stable key / ledger identity**；**Production XLSX 跨子表引用列 → 仍按现有物理 schema 写 `name`**。⇒ 该改的是「**用 name 猜要改哪条 row**」那段实现（`stable identity → target row → targetRow.name → 写 XLSX reference cell`）；**不得本期把 XLSX reference cell 从 `name` 改成 `id`** —— 那是单独的**配置表 Schema Migration**；**`TimePeriod` 连数字 group id 都没有**。
  - **`name` 在对应 lookup domain 内必须无歧义**：**重名约束不是 semantic identity 约束，而是 materialization hard invariant** ⇒ **collision ⇒ BLOCK**，**不 silent suffix / fallback**（不要 `_x2` / `_new` / `_01`）。
- **`ED-20` Role 的 durable 落点 ＋ `setRole` 不补 Profile**：
  - **物种默认 Role → `Species Policy Recipe`**（§3.1 记录内的 Policy 子结构）；**行级 Role override → `AffinityRolePatch`（`(row_key, component)`）**。★ **Role 是「习性档案 / `FishEnvAffinity` 行」的属性，不是 `groups[k]` 的 bucket 属性** —— **不得写成 `groups["young"].role`**（否则一条 bucket 对应多个 row 时没地方表达）。
  - **`composeEntry` 各 lane 独立 compose/resolve，最后统一 validation**：**不得**因为 numeric base 当前缺失，就把 Role patch／`fail_env_coeff`／其它独立 durable patch 一起丢掉。
  - ★ **`§117`（提 Role 时自动补一份行为中立、全 `1.00` 的档案）按 `superseded` 处理** ⇒ **`setRole` 只改 Role：不创建 Profile、不选择默认 Source、不写 `1.00`。**
  - ⇒ `Profile missing + Role=CORE` 是**正常 UI 可达**的 **durable-but-publish-invalid 中间态**。合法流程：`IGNORED + absent` → 用户改 Role → **Role durable autosave** → `CORE + absent` → **visible required-Profile ERROR / Publish Block** → **UI 聚焦 Setup** → 作者显式选择／establish Source → Profile 成立。
  - **不得靠「丢 Role 回默认」来修复非法状态。**

---

## 二、**别按我说的做** —— 我还没逐字核 / 页上未展开的

1. **组件值的「内部形态」—— ★ 本条已由 Current 回答，不再是【待核】（2026-09-21 更正）**：§3.1 逐字「**组件值即该组件的 Component Recipe** —— 一个组件的「组件值」由两部分组成：**该组件的 Source 绑定**（两类 Source，§3.3）与**该组件的逐字段 operation**」，并明说 §1.1 的「Component Recipes（四个组件的 Source ＋ field operations）」「**指的就是上面这四个字段本身，不是另有一条更小的记录**」。
   ⇒ **仍未定的只有「序列化格式」**，而那**归实现线**（§5）：格式不影响字段／类型／必填／键，只看三条判据（逐条可 diff / 可人工比对与 merge / 结构由 schema 生成 ＋ parity 测试）与一条禁令 —— **不得把嵌套结构塞进单个单元格或单个标量字段**。
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
| 《编辑器持久层契约》**§3.6／§3.7／§3.8** | 逐字 | **第二轮**当天直读该页（页 `Version 16` / `Last Updated 2026-09-21 14:34`） |
| **§3.7 的第三条展开臂** | 逐字 | 同上（`ADJ-11 ＝ A_NARROW` 的落点） |
| **当日新裁 `ED-15` / `ED-13` / `ED-20`（含 `§117` supersede）** | 裁定方逐字 | **【裁定·未落页】** —— 落页后以页为准 |
| 《编辑器持久层契约》§3.4 节标题 | 「Affinity Role Patch 与 AffinityFailEnvCoeffPatch｜两条 row-level 轨道」 | 当天直读 |
| Figma `108:335` annotation | 526 字 · sha12 `970742371cfd` | REST 直读 |
| Figma `108:364` annotation | 546 字 · sha12 `013d7004b126` · `&`＝0 | REST 直读 |

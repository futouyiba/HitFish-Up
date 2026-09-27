# Fish Habit Editor V1｜Common Semantics

> Status: Current Semantic Baseline for V1  
> Scope: 只承接 Fish Habit Editor V1 实际消费的公共语义。本文暂时与 V1 共址；当这些语义稳定跨越 V1 / V1.0.1 / V1.1+ 后，再提取到独立 common 目录。  
> Historical evidence: `docs/review/ui-component-contract-r2/` 作为 V0.2 历史版本包与证据来源，不再承担 Current semantic authority。

## 1. Authoring Truth 与物理 Owner

V1 唯一长期 Authoring Truth 是 Editor durable state。

业务对象与物理持久化 owner 分离：

- **Species Base / 基础习性**：业务上属于 Fish / Species。
- **兼容中鱼习性模式**：V1 每个可编辑 Mode 对应一条既有 `FishEnvAffinity`；物理 durable identity 仍使用既有 Affinity / row key。
- **Shared Template**：持续共享 Source，具有稳定 template identity。
- **Policy Template**：Species Base 的 Policy Source。
- **Production materialization**：Authoring Truth 的输出，不是第二个可编辑真相。

V1 不创建新的 durable EngagementMode identity，也不把 Quality / FishPond / StockRelease / FishRelease 拉回 Habit Editor ownership。

## 1.1 V1.0 Existing Species Base boundary

V1.0 不提供 Species Base creation。

普通 Authoring 只处理**已经存在于 authoring working tree** 的 Species Base / 基础习性。如何把更老的 Production 数据整理进 authoring working tree 属数据准备 / migration 工作，不是 V1.0 Editor 产品能力，也不是 Coding Agent 需要实现的普通流程。

Species identity 仍来自 Fish Basic / authoritative Species Catalog：

```text
Fish Basic species_key
→ existing Editor Species Base
→ ordinary Authoring
```

V1.0 不提供“开始配置其他鱼种”、fresh-create Species Base 或 half-created Habit draft。

### 1.2 Default Affinity Projection

每个进入 V1.0 的 Species Base 已经对应一条 system-default `FishEnvAffinity` identity。V1.0 只维护 / Publish 它，不负责创建它。

它不是第二份 Authoring Truth，也不是用户可编辑的 Mode。

```text
Species Base Authoring
        ↓
existing system-default Affinity
        ↓
Production / StockRelease 可引用
```

V1.0 UI 不把 default Affinity 显示为 Mode，不允许把它伪装成 `young` / `mature`。

Quality / StockRelease / FishRelease 与 FishEnvAffinity 的关联继续由各自 domain 维护，Habit Editor 不创建或同步该关系。

V1.0 不提供 Species Base / system-default Affinity Archive / Delete。

### 1.3 V1.0 Subject coverage

普通 UI 只列出已经存在于 authoring working tree、并能正常解析 Species identity 的 Subject。

- 没有 Species Base 的 Fish 不进入 V1.0；
- unmapped / 不支持的 legacy row 不要求 Editor adjudicate，也不作为 blocker 迫使 V1 实现 migration UI；
- 数据准备脚本可以在 Editor 外部处理这些问题。

### 1.4 Broken Species Reference

`species_key` 的 Authority 是 Fish Basic / Species Catalog。

若 Editor 已存在 Species Base，但当前 Catalog 已找不到该 `species_key`：

- Editor 可以 tolerant load 该 durable state，用稳定 key / 已有 cache 帮助定位；
- 产生 `BROKEN_SPECIES_REF` ERROR；
- Publish BLOCK；
- 不自动按名称匹配到另一条 Species；
- 不允许在 Habit Editor 中改写 Species identity；
- 修复必须由 authoritative Catalog / migration 侧恢复原 identity 或完成受控迁移。

### 1.5 Existing Compat ingress boundary

V1 所说的“编辑已有 Compat Mode”不是“任意已有 `FishEnvAffinity` row 都自动成为一个 Mode Subject”。

V1 当前沿用两个既有 physical Compat slot：

- `young`；
- `mature`。

进入 V1 Editor 前，existing Production ingress 必须已经把兼容 row **无歧义映射到其中一个 physical slot**。每个 Species × Compat slot 最多一条可编辑 row。

产品层不把这两个 slot 表达成一套必须穷举 Species 生命周期的完整分类。V1 UI 将它们放在 **“中鱼习性模式”** 下，并投影为：

- `young` → **小个体**；
- `mature` → **大个体**。

这里的“小个体 / 大个体”是作者侧模式标签；底层 `young / mature` token、既有 row identity 与 Production English naming 可以保持不变。

因此：

- 已完成 slot mapping 的 existing row → 可作为 V1 中鱼习性模式 Subject 编辑；
- 一个 Species 可以没有中鱼习性模式，也可以只有其中一个；不要求 young / mature 成对存在；
- 同一 physical slot 存在无法唯一选择的多 row → V1.0 不暴露该 Compat Subject；
- 无法映射到 system-default / young / mature 的 Affinity → V1.0 不作为可编辑 Subject；
- 不允许 UI 根据 row name、Quality 或 payload 相似度自行猜 slot identity；
- 哪些 Quality / stocking rows 实际引用 system-default、young 或 mature Affinity，仍由 StockRelease / FishRelease 域决定。

V1.0.1 只是在同一 fixed physical slot 体系下补“缺失中鱼习性模式 row 的 create”；不会把 `young / mature` 升级为新的业务 Mode taxonomy。

## 2. Source Binding

### 2.1 Source 与 Operation 正交

每个 Component 的解析模型：

```text
Effective Source
+
Effective Operation
→ Effective Value
```

Source 变化不自动清理 Operation；Operation 变化不自动换 Source。

不得为了保持旧 Effective Value 自动制造 SET。

### 2.2 Explicit Component Source

V1.0 每个 Component 的显式 Source 只有两类：

1. **Shared Template**；
2. **Existing Production Source**。

Existing Production Source 是过渡期兼容来源，来自当前本地 Production working tree 中**合法的同 Component Kind row**。

规则：

- Shared Template 是长期主路径；
- Existing Production Source 是只读兼容依赖，不因此成为 Shared Asset；
- Picker 展示所有合法同 Kind Existing Production rows，不按当前 Species / Quality 推导“归属关系”；
- UI 直接显示 Production row 的真实英文 `name`，不生成新的中文解释名或“某鱼现有数据”别名；
- durable binding 使用真实稳定 physical identity / key；display name 不成为第二个 Editor identity；
- Existing Production Source 作为只读 compatibility source 使用；
- Source catalog 在 workspace load / refresh 时建立；Publish 过程中不动态把刚写出的 row 注入当前 Picker，避免同一事务内形成 output → source 循环；
- V1.0 不提供外部生态数据库 Import / Reimport 来生成新的 Concrete Source。

### 2.3 Species Base / Compat Source relation

Species Base 每个 Component 可以显式选择：

- 合法 Shared Template；
- 合法 Existing Production Source。

Compat Mode 每个 Component 可以：

- 跟随基础习性；
- 显式选择合法 Shared Template；
- 显式选择合法 Existing Production Source。

因此 Compat 的 FOLLOW 与“本层显式 pin 某个 Source”仍是两种不同 durable intent；显式 pin 不要求 Source 必须来自 Template。

### 2.4 Follow 与 Explicit Pin

以下即使当前 Effective Source / Effective Values 相同，也不是同一作者意图：

```text
跟随基础习性 → Heavy Cover
Heavy Cover · 本模式设置
```

FOLLOW ↔ explicit pin 改变未来传播行为，因此是真实 durable mutation。

只有候选 binding intent 与当前 durable binding intent 完全相同，才是 exact no-op。

### 2.5 Profile absent

`Profile absent` 是 Resolver / Validator 能容忍的已有数据状态，但不是普通作者主动制造的状态。

- V1 不提供“删除 Profile / 清空 Source”；
- `Profile absent` 表示没有可消费 Profile；
- `BROKEN_SOURCE_REF` 表示已有 binding 指向不存在 / 无法解析的 Source；
- 两者都通过重新选择合法 Source 修复。

## 3. Component Field Operations

### 3.1 Species Base

数值字段：

```text
沿用来源   = absent
调整       = ADD
设置为     = SET
```

枚举绝对值字段：

```text
沿用来源   = absent
设置为     = SET
```

### 3.2 Compat Mode

数值字段：

```text
沿用物种设置   = absent
仅用当前来源   = CLEAR
调整           = ADD
设置为         = SET
```

枚举绝对值字段：

```text
沿用物种设置   = absent
仅用当前来源   = CLEAR
设置为         = SET
```

### 3.3 CLEAR

Component CLEAR 的语义：

> 取消继承自 Species 的 Operation，只使用当前 Effective Source raw value。

CLEAR 不携值。

absence 与 CLEAR 必须可区分；即使两者当前 Effective Value 相同，也不能自动互相折叠。

### 3.4 ADD / SET

- ADD 总是相对**当前 Effective Source value**的增量；
- SET 是绝对值；
- SET 与 Source value 相等仍然是显式 SET；
- 值相等不能反推 inherit / absent；
- 从 ADD 切 SET 或 SET 切 ADD，不自动复用旧参数，不自动保持 Effective Value。

### 3.5 参数提交

需要参数的 ADD / SET：

- 切换 operation type 后先进入 UI transient raw-input；
- 只有完整可解析 typed value 才形成 durable operation；
- incomplete raw input 不写盘、不进 Resolve / Publish；
- 切离 field / Component / Subject / Workspace 前仍未完成，则丢弃 transient，恢复最近一次 durable 表达。

无参数的 absent / CLEAR 可以立即形成 ordinary durable edit。

## 4. Resolve Semantics

Resolve 只从最近一次成功 durable revision 计算。

### 4.1 Effective Value

基本因果：

```text
Source raw value
→ 应用最终有效 Operation
→ Effective Value
```

对于 Mode，Source relation 与 Operation relation 是两条独立轴：

```text
Mode Source 可以显式 pin
同时 Operation 仍可沿用 Species

或

Mode Source 跟随 Species
同时 Operation 可以 CLEAR / ADD / SET
```

不得把两者压成模糊的“继承”。

### 4.2 当前态解释边界

当前 Resolve 可以说明：

- 当前 Effective Source；
- 当前最终 operation；
- Source value 如何得到 Effective Value；
- SET 当前覆盖了 Source value；
- CLEAR 当前取消了哪条 Species operation。

当前 Resolve 不能在没有 before/after 输入时声称：

- 来源“发生了变化”；
- 结果“没有变化”；
- 某次历史编辑造成了什么差异。

## 5. Spatial Opportunity Policy

Policy 与 Profile 正交。Policy 不是第五个 Component。

### 5.1 Policy Template

Policy Template 只属于 Species Base。

Compat Mode 没有 `policySourceOverride`。

### 5.2 Species Role

四个 Component Role：

```text
沿用策略模板   = absent
设置为 CORE    = SET CORE
设置为 SECONDARY = SET SECONDARY
设置为 IGNORED = SET IGNORED
```

Role 不允许 ADD。

### 5.3 Compat Mode Role

```text
沿用基础习性角色       = absent
使用策略模板原始角色   = CLEAR
设置为 CORE/SECONDARY/IGNORED = SET
```

Policy CLEAR 的语义：

> 取消 Species Role override，直接回到当前 Policy Template raw Role。

absence 与 CLEAR 必须可区分。

### 5.4 fail_env_coeff

Species Base：

```text
沿用策略模板值 = absent
调整           = ADD
设置为         = SET
```

Compat Mode：

```text
沿用基础习性配置       = absent
使用策略模板原始值     = CLEAR
调整                   = ADD
设置为                 = SET
```

Mode CLEAR 直接回到 Policy Template raw `fail_env_coeff`。

`fail_env_coeff` 允许 durable 保存后由 Validator 判定；V1 当前合法区间为 `[0, 0.10]`，越界 ERROR、阻断 Publish，不 silent clamp。

## 6. Role × Profile Lifecycle

Role 不自动创建、删除或改写 Profile。

规则：

- CORE / SECONDARY：对应 Component Profile 必须存在，否则 Validator ERROR、阻断 Publish；
- IGNORED + Profile absent：合法；
- IGNORED + Profile present：Profile 保留且仍可编辑，只是当前计算不消费；
- IGNORED → CORE / SECONDARY：Role ordinary edit 先 durable 保存，再显示 required-Profile ERROR；不回滚 Role、不自动选 Source；
- CORE / SECONDARY → IGNORED：不删除 Profile。

## 7. Validation 与 Autosave

### 7.1 durable-valid ≠ publish-valid

能够形成合法 typed authoring intent 的编辑可以 durable 保存，即使结果产生 Validator ERROR。

因此：

```text
Autosave 成功
+
Validator ERROR
=
编辑器已保存 · 有错误
```

不是 Save Failure。

### 7.2 Autosave

普通 semantic edit：

```text
typed state
→ short debounce/coalesce
→ local atomic durable write
```

无常驻 Save 按钮。

V1.0 定位为**单机单写者 workspace**。Editor 不实现多人 / 多会话协同编辑协议；人与人之间的同步、diff、merge、冲突解决全部交给 Git。

### 7.3 Save Failure

本地 Authoring 文件写入失败时：

- 最近一次成功保存的 durable state 仍是 Truth；
- 未成功保存的输入不能进入 Resolve / Publish；
- UI 明确提示保存失败并允许重试。

V1.0 不实现 revision rebase、字段级 merge 或 conflict replay。

### 7.4 Diagnostics

Diagnostics 是 derived state，不持久化为第二份 Truth。

同一诊断可以投影到：

- Field；
- Component Card；
- Policy；
- Global Validation List；
- Resolve；
- Publish Preflight。

ERROR 阻断 Publish；WARNING 默认不阻断。

## 8. Staged Mutation

V1 只有两类 mutation 重量：

1. ordinary semantic edit → Autosave；
2. staged binding / propagated mutation → Candidate Review → Confirm → atomic commit。

### 8.1 Source Change

每一笔 Source binding mutation都 staged confirm。

Candidate：

- ephemeral；
- 只能从最近一次成功保存的 durable state 启动；
- Candidate active 时暂停其它导航、ordinary mutation 与 Publish；
- Confirm 前检查候选 Source 仍存在且 schema 合法；
- 取消不回滚已 durable 的普通编辑。

Preview 必须说明：

- binding intent before / after；
- Effective result before / after；
- operation masking；
- diagnostic delta；
- 如有 propagation，哪些 follower 跟随受到影响。

### 8.2 Policy Template Change

Species Base 更换 Policy Template 复用同一 staged transaction 语义。

不得为了保持旧 Effective Policy 自动制造 Role SET / coeff ADD/SET。

### 8.3 Candidate Error

若 mutation binding 本身 schema-valid，但 after-state 有 publish-blocking Validator ERROR：

- 仍允许 Confirm durable 保存；
- Confirm 后 Editor 进入“已保存 · 有错误”；
- Publish BLOCK。

只有 mutation 本身已无法形成合法 durable commit时，才禁 Confirm。

## 9. Shared Template Semantics

### 9.1 Shared Template

Shared Template 是持续共享 Source。

- complete value 修改会传播到 Effective consumers；
- complete value 修改属于 staged propagated mutation；
- metadata / alias 普通编辑走 Autosave；
- clone / save-as 后是独立模板，不支持 Template → Template 实时继承。

### 9.2 Lifecycle

生命周期：

```text
ACTIVE ↔ ARCHIVED
```

ARCHIVED：

- 既有引用继续合法；
- 不作为新的 Source candidate；
- 可 Restore。

Hard Delete 只有在：

- 已 ARCHIVED；
- DirectReferenceSet 为空；

时才允许。

### 9.3 Replace References

Replace A → B：

- 只重写 DirectReferenceSet(A) 的 durable binding；
- 保留既有 ADD / SET / CLEAR / Role / coeff patches；
- 不给 inherited consumer 自动制造 explicit pin；
- staged preview + explicit confirm + atomic commit。

### 9.4 Direct vs Effective Reference

- `DirectReferenceSet(A)`：durable state 中显式引用 A 的 owner；
- `EffectiveConsumerSet(A)`：Resolve 后最终消费 A 的**作者语义 owner**。系统默认 Affinity 这类隐藏 projection 不作为额外的人类 consumer 重复计数；它的 Production 更新属于所属 Species Base 的 materialization consequence。

两者不能互代。

## 10. Shared Template Creation

V1.0 不创建 Species Base；Shared Template 是独立的可复用 Source asset，Template 创建本身不创建或修改 Fish / Mode identity。

### 10.1 Blank Create

按 Template Kind 创建完整值资产：

- 先确定 Kind；创建后 Kind 不可改；
- 创建表单为 ephemeral，不建立 durable DRAFT_TEMPLATE；
- 只有形成该 Kind 的完整 typed value 与必要 metadata 后，才 atomic create；
- 创建成功后 lifecycle = ACTIVE；
- 创建本身没有 consumer，不需要 Impact Preview。

### 10.2 Extract from Fish Component

从当前 Fish Component 提取模板时，提取的是该 Component 的**当前完整 Effective Profile**，并 flatten 成新的 Template complete value。

它不复制：

- Source binding；
- ADD / SET / CLEAR；
- Species / Mode lineage；
- provenance；
- production row identity。

规则：

- Component 必须能产出完整 typed Effective Profile；Profile absent 或无法 Resolve 时不能 Extract；
- 如果完整 Effective Profile 存在但带 Validator diagnostic，可允许创建，但新 Template 继承同样的 current-value diagnostic；不会因创建动作影响任何既有 consumer；
- Extract 只创建 Template Asset，**不修改当前 Fish Source、不清 local operation、不自动 rebind**；
- 创建后若作者希望当前 Fish 改用新模板，必须另走 Source Change Candidate。

### 10.3 Extract from Effective Policy

Spatial Opportunity Policy Template 也支持对称提取：

- 从当前 Fish Subject 的完整 Effective Policy 提取一个新的 Policy Template；
- flatten 当前四个 Effective Role + Effective `fail_env_coeff`；
- 不复制 Species / Mode Role patch provenance；
- 不自动把当前 Fish 改绑到新 Policy Template；
- 如需改绑，另走 Policy Template Source Change Candidate。

### 10.4 Clone / Save As

Clone / Save As 从现有 Template complete value 创建新的独立 Template：

- 新 identity；
- 无 Template → Template inheritance；
- 后续修改互不传播；
- 创建动作本身不改任何 existing binding。

### 10.5 Template Kind

V1 Template Kind 固定为：

- Temperature
- Structure
- Feeding Layer
- Time Period
- Spatial Opportunity Policy

Kind 决定字段 schema；创建后不可跨 Kind 修改。

## 10.6 Naming layers

V1 明确区分三类命名 / identity：

1. **Editor stable identity**：例如 `template_id`、Affinity `row_key`；用于 durable reference，不因显示名变化。
2. **作者资产名**：Shared Template 有中文名与英文名。中文名是 Editor primary display；英文名是作者可读的 semantic stem，Blank Create / Extract 时可由工具建议、作者可改。
3. **Production projection name**：由 Materializer 根据 owner / lineage 派生；它可能在 Production 内承担 name-based lookup / reference key 的物理职责，但不反向成为 Editor durable identity。

对于 Shared Template 的模板级 Profile projection，V1 只固定一条语义要求：

```text
Production Profile Name
← deterministic derivation from Template English Name
```

是否加入 Component Kind qualifier 不属于 Authoring Semantics。优先可读 convention 可以是 `Struct Heavy Cover`、`Temp Warm Water`；但若真实 Production 已按独立子表 / lookup domain 天然隔离 Kind，则无需为了形式统一增加前缀。exact qualifier、delimiter、case、合法字符 normalization 与各表 collision domain 由 implementation G3 根据真实 schema 固定。

同样，不预设 Spatial Opportunity Policy 一定拥有同构的具名 Production 子表。

对于含 Species / Mode 有效 local operation 的 Profile，使用 owner-specific system-generated projection name，不继续冒用 Template Profile name。

`FishEnvAffinity` row name 与 Component/Profile row name 是不同层级。Affinity row name 不允许作者在 V1 / V1.0.1 手工命名；系统命名必须表达对应的 Affinity semantic class：

- system default → Base 语义；
- physical `young` slot → Production naming 可继续使用既有 Juvenile / Young 语义 token；
- physical `mature` slot → Production naming 可继续使用既有 Mature token。

这些 Production token 不要求与 V1 UI 中文标签一一同义：V1 UI 当前将 `young / mature` 显示为“小个体 / 大个体”。Species canonical English name 作为鱼种可读 stem；exact suffix token / delimiter / case / normalization 仍由 G3 固定。未来 arbitrary Engagement Mode 若需要作者命名，不从 V1 fixed Compat 反推。

## 11. Broken / Archived Source

### ARCHIVED

合法既有引用继续 Resolve；UI 显示归档状态。

### BROKEN_SOURCE_REF

- load tolerant；
- Validator ERROR；
- Publish BLOCK；
- 不 fallback 到 Species / 默认模板 / 最近似模板；
- 必须作者显式重新选择合法 Source。

Resolve UI 只展示 Resolver 实际能给出的结果，不自行补算第二套 Resolver。

## 12. Publish / Materialization Semantics

### 12.1 Publish Scope

Publish 消费当前本机**最近一次成功保存的 Authoring Truth**。

点击 Execute 后，当前 App 暂停 Authoring mutation，直到本次 Publish 成功或失败。V1.0 不处理另一 Editor 会话同时写 Authoring state 的情况。

### 12.2 Production

Production 是本地 Production Git working tree 中的 materialized output，不是第二个 Authoring Truth。

Production payload 无法无损反推出 Template / Source / ADD / SET / CLEAR 等作者意图，因此 V1 不做持续 Production → Editor reverse sync。

### 12.3 Non-destructive Publish

V1.0 Publish 采用**非破坏性 patch**：

```text
read current Production working tree
→ materialize current saved Authoring state
→ create / update 明确目标 rows
→ 保留其它 Production rows
→ reread touched output
→ verify
→ success
```

规则：

- 只修改本次可以明确定位的目标 rows；
- 不因为 Editor 不认识某条 row 就删除它；
- V1.0 不做 orphan GC、obsolete-row cleanup、全表 ownership reconcile；
- Source change / Template rename 产生的旧 row 若不能安全原地复用，可以暂时保留；
- write 后必须 reread + verify 本次 touched output。

### 12.4 Materialization lineage

必须区分：

1. **Affinity identity row**：system-default / existing Compat 各自稳定的 `FishEnvAffinity` identity；
2. **Component/Profile row**：Temperature / Structure / Feeding Layer / Time Period 等 materialized profile。

因此：

- Compat 即使完全跟随 Species、最终值完全相同，也保留自己的 Affinity identity row；
- Component/Profile 可以按明确 Source / lineage 复用；
- same-value SET 仍是 SET；
- V1.0 不因为 payload / name 相似自动 dedupe Production rows。

### 12.5 Local write failure

Production create / update 任一步写入、reread 或 verify 失败，本次 Publish 即失败。

若新建 row 需要 Production `row_id`：

```text
create
→ reread
→ 唯一识别 row_id
→ 更新本地 mapping
→ verify
```

未完成整条链路不得宣告成功，也不得 blind recreate。

## 13. V1 Semantic Negative List

V1 common semantics 不定义或承诺：

- Quality authoring；
- FishPond / StockRelease / FishRelease authoring；
- Mode Share / Routing；
- 新 durable EngagementMode identity；
- Species Preset / 鱼家族预设；
- Family / 聚类辅助初始化；
- Bake / condition evaluation；
- 外部生态数据库 Import / Lux CLI；
- Production reverse import / auto-merge；
- CSV canonical persistence。

这些能力进入后续版本时，应显式扩展或拆出新的 common contract，不得从 V0.2 历史包中直接复活为 Current。

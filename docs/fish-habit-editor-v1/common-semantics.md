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

## 1.1 Species Habit Creation

V1 可以创建 Habit Editor 自己拥有的 **Species Base Record**，但不能创建 Species identity。

Species 创建来源：

```text
Fish Basic / authoritative Species Catalog
→ existing species_key
→ Species Habit Base
```

新建 Species Base 的产品完成条件：

- Temperature Source 已选择；
- Structure Source 已选择；
- Feeding Layer Source 已选择；
- Time Period Source 已选择；
- Policy Template 已选择；
- 四个 Component Profile 与 Policy 均可 Resolve。

创建为一个 atomic durable transaction；不建立 durable half-created wizard / draft。

初始化 transaction 只写 Species Base 的五个 binding：

- 四个 Component Source；
- 一个 Policy Template Source。

不在 initialization transaction 中写 ADD / SET / CLEAR、Role override 或 fail_env_coeff override；这些全部在创建成功后的普通 Authoring 中完成。初始化 Source 只从当前合法、已存在的 ACTIVE Source 选择；Template creation 使用独立 Shared Assets flow。

Species Base **不是** FishEnvAffinity row，也不是默认 Engagement Mode。

### 1.2 Default Affinity Projection

每个 Species Base 在 V1 durable state 中必须**恰好对应一个系统默认 FishEnvAffinity 投影壳**。新建 Species Base 时，两者由同一个 atomic creation transaction 建立；Bootstrap / migration 进入 V1 时也必须补齐这一 invariant。

它不是第二份 Authoring Truth，也不是用户可编辑的 Mode。

初始语义固定：

```text
Default Affinity
├─ Temperature Source  = FOLLOW_SPECIES
├─ Structure Source    = FOLLOW_SPECIES
├─ Feeding Source      = FOLLOW_SPECIES
├─ Time Source         = FOLLOW_SPECIES
├─ numeric operations  = absent
├─ Role patches        = absent
└─ fail_env_coeff      = absent
```

因此它完整继承 Species Base 的四 Component 与 Policy。

Durable / Production identity：

- Editor 创建稳定 `row_key`；
- Production `row_id` 可在 Publish 后获得；
- human-readable production name 系统生成并校验 collision；
- 普通作者 UI 不要求编辑该 name，也不把默认 Affinity 显示为独立 Mode；
- 系统默认 Affinity **不得为了复用旧 schema 被伪装成 `young` 或 `mature` bucket**。其物理表示必须能与固定 Compat bucket 无歧义区分；若当前 ledger schema 无法表达，使用最小显式 schema delta，而不是污染 bucket 语义。

Species Base 仍是作者编辑“默认习性”的唯一入口；默认 Affinity 只是让这套习性拥有一个可被 Runtime / StockRelease 域引用的具体 EnvAffinity projection。

Quality / StockRelease / FishRelease 与 FishEnvAffinity 的关联继续由其各自 domain 维护，Habit Editor 不创建或同步该关系。

V1 不提供 Species Base / system default Affinity 的 Archive / Delete。原因不是技术上不能删，而是 Habit Editor 不拥有完整的跨域 StockRelease / FishRelease 引用生命周期；在没有安全 cross-domain reference guard 前，删除不进入最小闭环。

### 1.3 Species create eligibility

“Editor 中没有 Species Base”不自动等于“可以 fresh create”。

Fish Basic Species 分三类：

```text
CONFIGURED
  Editor Species Base exists
  → 正常编辑

AVAILABLE_NEW
  no Editor Species Base
  + no existing Production FishEnvAffinity footprint for this species
  → 可以“开始配置习性”

LEGACY_UNIMPORTED
  no Editor Species Base
  + existing Production FishEnvAffinity footprint
  → 禁止 fresh create
```

`LEGACY_UNIMPORTED` 必须提示存在旧生产习性数据，需要经过 bounded bootstrap / migration 后才能进入 V1 Editor。V1 不用一套新 Source/Policy 覆盖旧 Production，也不把 generation guard 当 migration 工具。

若并发会话在提交前已经为同一 `species_key` 创建 Species Base，当前 create transaction 必须冲突失败并刷新为现有 Subject，不能生成第二份 Species Base。

### 1.4 Broken Species Reference

`species_key` 的 Authority 是 Fish Basic / Species Catalog。

若 Editor 已存在 Species Base，但当前 Catalog 已找不到该 `species_key`：

- Editor 可以 tolerant load 该 durable state，用稳定 key / 已有 cache 帮助定位；
- 产生 `BROKEN_SPECIES_REF` ERROR；
- Publish BLOCK；
- 不自动按名称匹配到另一条 Species；
- 不允许在 Habit Editor 中改写 Species identity；
- 修复必须由 authoritative Catalog / migration 侧恢复原 identity 或完成受控迁移。

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

### 2.2 Species Base Source

V1 Species Base：

- Structure / Feeding Layer / Time Period：选择 Shared Template；
- Temperature：可选择 Shared Template；若当前 Species 已存在合法 Species Concrete，可继续引用该 Concrete；
- V1 不提供外部生态数据库 Import / Reimport 来新建或更新 Concrete。

### 2.3 Compat Mode Source

Compat Mode 每个 Component 只有：

- 跟随基础习性；
- 显式选择合法 Shared Template。

Mode 不直接选择 Species Concrete；需要消费 Species Concrete 时走“跟随基础习性”。

### 2.4 Follow 与 Explicit Pin

以下即使当前 Effective Source / Effective Values 相同，也不是同一作者意图：

```text
跟随基础习性 → Heavy Cover
Heavy Cover · 本模式设置
```

FOLLOW ↔ explicit pin 改变未来传播行为，因此是真实 durable mutation。

只有候选 binding intent 与当前 durable binding intent 完全相同，才是 exact no-op。

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
→ optimistic revision check
→ atomic durable write
```

无常驻 Save 按钮。

### 7.3 Save Failure

I/O / revision write failure：

- 最近一次成功 durable revision 仍是 Truth；
- 未成功写入的输入不能进入 Resolve / Publish；
- 不 silent last-write-wins。

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
- 只能从最近一次成功 durable revision 启动；
- Candidate active 时暂停其它导航、ordinary mutation 与 Publish；
- 确认前做 revision check；
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

V1 可以从 Fish Basic 创建新的 Species Base + system default Affinity；Shared Template 是另一类独立 Source asset，Template 创建本身不创建或修改 Fish / Mode identity。

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

V1 Publish 永远消费**整个 Editor durable state**，不是当前 Fish / Mode / Component。

### 12.2 Production

Production 保存 materialized full values / enums，不保存 Source / operation provenance。

因此：

- Production payload 无法无损反推出 Authoring intent；
- V1 不支持持续 Production → Editor reverse sync；
- external Production drift 只做检测 / BLOCK，不自动采纳或 merge。

### 12.3 Generation Guard

Publish 必须验证 whole Production generation / baseline：

- mismatch BLOCK；
- unverifiable BLOCK；
- 不 silent overwrite；
- 不按 target 拼接 baseline；
- 成功后 whole reread + verify，才能建立新的 expected baseline。

### 12.4 Materialization lineage

Production projection 按 authoring lineage 决定，不按 payload 相等猜 owner。

至少保持：

- Shared Template + 无有效 local operation：可复用模板级 projection；
- Mode 完全跟随 Species Recipe：可复用 Species projection；
- explicit Source pin + 零 operation：只改变未来 binding relation，不因 pin 本身强制复制一个同值 production row；
- 任何有效 ADD / SET / CLEAR 等 local operation：按对应 owner 的 materialization 规则投影；
- same-value SET 仍是 SET，不能因 payload 相同折回继承。

### 12.5 Partial / Unverifiable Write

V1 不接受“成功一半”。

若 writeback partial 或 final verification 不可证明：

- Publish 失败；
- 不自动采纳当前 Production 为新 baseline；
- 后续 Publish 保持 BLOCK，直到 whole Production 回到可信 baseline；
- recovery / reconcile 不在 V1 内自动完成。

具体产品交互见 [secondary-surfaces.md §7](secondary-surfaces.md#7-publish发布到生产配置)。

### 12.6 Create-from-absent row identity

对于 system default Affinity 或后续固定 Compat Mode 这类 `row_id = null` 的新 row：

- `row_key` 是 Editor durable identity；
- Production create 成功后，必须 reread 得到唯一 `row_id`；
- `row_id` mapping 必须回填到 Editor durable metadata；
- 只有 Production verify 与 mapping durable save 都成功，本次 create-from-absent 才可视为 Publish success。

如果 Production row 已创建，但 `row_id` 回填或 final verification 失败，本次按 partial / unverifiable failure 处理；在恢复可信 `row_key ↔ row_id` 映射前，不允许下一次 blind create 同一语义 row。

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

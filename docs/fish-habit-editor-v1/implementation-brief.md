# Fish Habit Editor V1｜Implementation Brief

> Status: Current Implementation Entry for V1 — G1–G5 physical gates pending  
> Product Authority: [product-contract.md](product-contract.md)  
> Semantic Authority: [common-semantics.md](common-semantics.md)  
> Surface Contracts: [authoring-surface.md](authoring-surface.md), [shared-assets.md](shared-assets.md), [secondary-surfaces.md](secondary-surfaces.md)  
> Scope: [版本范围与阶段路线](../review/fish-habit-editor-version-scope.md)

本文只列 V1 最小生产闭环的实现切面与尚需工程落点，不重新定义产品语义。

G1–G5 不表示 Product Contract 尚未闭合；它们只确认冻结语义如何映射到 Fish Basic、ProductionRowLedger、Production naming 与 legacy bootstrap。任何 Gate 若要求改变 Product / Semantic Current，必须停止实现并回到 Owner / Review，而不是在实现层自行改义。

## 1. V1 最小闭环

```text
Fish Basic
→ 选择已有 Species
→ 若无 Habit：创建 Species Base + 系统默认 Affinity projection
→ Species Base / 已有 Compat Mode Authoring
→ Shared Template
→ Validation / Resolve
→ Publish
```

V1 不实现：

- 新 Species identity；
- 用户创建任意 Mode；
- Family / Species Preset；
- Quality / StockRelease / FishRelease authoring；
- Bake；
- Production reverse reconcile。

## 2. Species Catalog integration

Fish Habit Editor 读取 authoritative Fish Basic：

- `species_key` 使用 Fish Basic 稳定 ID；
- display name 只用于 UI；
- Habit Editor 不写 Fish Basic；
- 已有 Species Base 的 `species_key` 若在当前 Fish Basic 中失效，产生 `BROKEN_SPECIES_REF`，允许 tolerant load 但 Publish BLOCK，不按名称自动 remap；
- 已有 Editor Species Base → 进入正常左栏；
- 无 Editor Species Base + 无 Production FishEnvAffinity footprint → 可通过“开始配置其他鱼种”创建；
- 无 Editor Species Base + 已有 Production FishEnvAffinity footprint → 标记 `LEGACY_UNIMPORTED`，禁止 fresh create，先走 bounded bootstrap / migration。

必须保证同一 `species_key` 不能重复创建 Species Base；create commit 前再次做 uniqueness / revision check，并发冲突时刷新为已经存在的 Subject。

### 2.1 Existing Production ingress

V1 产品不提供 migration UI，但已有 Production 进入 Editor 时必须经过 bounded bootstrap / migration，并满足以下 ingress 约束：

- 一个 Species Base 最终必须恰好一个 system default Affinity projection；
- 不因 Production row 名含 `NORMAL` / `Default` 就自动认定它是 system default；只有存在明确 migration mapping / evidence 时才复用既有 row，否则创建新的 default projection shell；
- V1 Compat UI 只接受固定 `young / mature` 语义，并且每个 Species × Compat type 最多一条可编辑 `FishEnvAffinity`；
- legacy 中同一 Compat type 有多条 rows 时，产生 `MULTIROW_COMPAT_UNSUPPORTED` migration blocker；不得自动聚合、任选一条或按 Quality 猜主行；
- 无法映射到 system default / young / mature 的 legacy Affinity 产生 `UNMAPPED_AFFINITY` migration blocker；不得 silent drop；
- migration 负责形成满足 V1 durable invariants 的 Editor state，之后 Authoring 才以 Editor state 为 Truth。

这不是要求全量自动迁移；可以是目标 Species 集合上的一次性脚本 + 人工 adjudication。

未进入 Editor ownership 的 legacy rows 继续作为 **pass-through Production** 保留在 verified baseline 中。Bootstrap / migration 必须能区分：

- 已被 Editor / ledger 明确接管、后续允许 materialize / cleanup 的 managed rows；
- 尚未 adjudicate、Publish 必须原样保留的 pass-through rows。

不得因为一次 V1 Publish 只覆盖部分 Species，就把其它未迁移 legacy rows 从 Production 中删除。

## 3. Species Base creation transaction

创建输入只有五个 binding：

```text
Temperature Source
Structure Source
Feeding Layer Source
Time Period Source
Policy Template
```

提交前校验：

- 五个 binding 都存在且当前可选；
- 四个 Component 可以 Resolve 完整 Profile；
- Policy 可以 Resolve 完整 Effective Policy；
- resulting Species Base 没有 blocking validation error；
- `species_key` 尚无 Species Base；
- Production 不存在该 Species 的未导入 FishEnvAffinity footprint。

一次 atomic transaction 同时创建：

1. Species Base Record；
2. **恰好一个**系统默认 Affinity projection record / ledger entry。

Bootstrap / migration 载入既有 Species Base 时也必须建立同一 invariant：每个 Species Base 恰好一个 system default Affinity projection。

初始化 transaction 不写：

- ADD / SET / CLEAR；
- Role override；
- fail_env_coeff override；
- Quality / StockRelease binding。

创建成功后直接进入普通 Species Base Authoring。

## 4. System Default Affinity projection

系统默认 Affinity 不是第二个 Authoring Subject，也不是业务 Mode。

固定语义：

```text
4 Component Source = FOLLOW_SPECIES
numeric operation  = absent
Role patch         = absent
fail_env_coeff     = absent
```

因此它完全跟随 Species Base。

实现必须满足：

- 有稳定 Editor identity / row key；
- system default Affinity 的物理表示不能复用 `young` / `mature` bucket 语义；
- Publish 前可以处于未物化状态；
- Publish 后得到 Production row identity；
- ordinary UI 不把它列为“中鱼习性模式” child；
- StockRelease / FishRelease 可以在自己的配置中引用其 Production EnvAffinity；
- Habit Editor 不写这条外部关联。

### 4.1 实现 Gate：default Affinity physical carrier

产品语义已经闭合；落码前只剩物理承载确认：

- ProductionRowLedger 是否已经允许一个**非 young / mature** 的 system-default row；
- 默认 Affinity 的 deterministic Production name：必须由 Species canonical English name + Base 语义派生；exact suffix token、delimiter / case / normalization 与 collision lookup domain 由 G3 固定；
- 新 row 的 `row_key → row_id` 回填路径。

硬规则：

- 不允许为了绕过 schema 修改，把 system default Affinity 填成 `young` 或 `mature`；
- 若现有 ledger 可用 nullable / existing system slot 无歧义表达，直接复用；
- 若不能表达，提交最小 schema delta，使 system-default 与 compat bucket 在 durable identity 上可判别；不顺便设计 arbitrary Engagement Mode。

`row_key` 始终是 Editor durable identity；`row_id` 是 Production binding metadata。若 Production row 已写入但 `row_id` 回填 / final verify 失败，本次 Publish 按 partial / unverifiable failure 处理，禁止下一次 blind create 第二条默认 Affinity，直到 recovery 恢复可信映射。

## 4.2 Species Base lifecycle boundary

V1 不实现 Species Base / system default Affinity 的 Archive / Delete。

原因：default Affinity 可能已经被 StockRelease / FishRelease 域引用，而 Habit Editor 不拥有完整跨域引用生命周期。V1 create 是显式 atomic action；创建后只能继续编辑和发布，删除留到具备 cross-domain reference guard 的后续能力。

## 5. Existing Compat Mode

V1 只编辑已存在、且 ingress 已无歧义映射到 `young / mature` physical slot 的 Compat FishEnvAffinity。产品 UI 把这些 rows 作为“特殊习性”展示：`young → 幼年`，`mature → 大个体`。

- 一个 UI Mode 对应一条既有 Affinity row；
- 该 Affinity row identity 必须保留；即使 Mode 最终完全跟随 Species、所有 Component/Profile payload 与 Species 相同，也只能复用下层 Profile projection，不能把 Compat Affinity row 本身折叠掉；
- Source / numeric operation / Role / coeff 继续按 V1 Common Semantics；
- V1 不创建额外 Mode。

V1.0.1 才补缺失 fixed slot 的按需创建：

```text
幼年      → young
大个体    → mature
```

两个 slot 不要求成对存在；Species Base / 常规习性始终是默认入口。

## 6. Shared Template

实现 [shared-assets.md](shared-assets.md) 的最小能力：

- blank create；
- extract from Effective Component / Policy；
- clone；
- metadata autosave；
- complete-value multi-field candidate；
- impact recompute；
- Archive / Restore；
- Hard Delete guard；
- Replace References。

Template create 与 Fish binding 必须是两笔独立 mutation：

> Create Source ≠ Bind Source.

## 7. Resolve

Resolve 只消费最近成功 durable revision。

输出：

- Resolved Overview；
- 最短充分因果说明；
- partial resolve；
- shared diagnostics。

不得在 UI 内实现第二套 resolver。

## 8. Publish

Publish 是 Editor-global transaction。

Preflight：

1. Editor durable state；
2. full validation / materialization readiness；
3. Production generation baseline。

Executor 必须：

```text
revision check
→ generation check
→ build expected full Production
   = verified pass-through baseline
   + materialized Editor-managed projection
→ write
→ whole Production reread
→ verify
→ success
```

只有 reread + verify 成功才算 Publish success。

Materializer 必须区分 Affinity identity row 与可复用的 Component/Profile row：system-default / Compat Affinity identity 不因 payload 相同而合并；Profile projection 才可以按 lineage 复用。

实现无论采用 full-file replace 还是 row patch，都必须满足同一 ownership 语义：

- managed obsolete rows 可在 desired graph 不再引用时清理；
- pass-through rows 原样保留；
- ownership 不明时不猜、不删，必要时 BLOCK。

Partial / unverifiable write 不自动建立新 baseline。

## 9. 推荐实现顺序

```text
1. Fish Basic read + Species Base lookup
2. Species Base create + default Affinity ledger shell
3. existing Species Base Authoring
4. existing Compat Mode Authoring
5. Shared Template create / edit / propagation
6. Resolve
7. Publish
8. V1.0.1 fixed Compat Mode create
```

其中 1–7 构成 V1；8 不阻塞 V1 Freeze。

## 10. V1 验收最小样例

至少覆盖：

1. 选择 Fish Basic 中 `AVAILABLE_NEW` 的 Species；并验证 `LEGACY_UNIMPORTED` Species 不能 fresh create；
2. 用五个既有 Source / Policy 创建 Species Base，并同时得到且仅得到一个 system default Affinity ledger entry；
3. 默认 Affinity 不出现在 Mode 列表；
4. 修改 Species Base 字段并 Autosave；
5. 从当前 Component 提取 Shared Template；
6. 将 Fish Source 改绑到模板并经过 Candidate；
7. Resolve 解释最终值；
8. Publish 创建 / 更新需要的 Production projection；
9. reread / verify 成功；
10. StockRelease 域可以使用默认 EnvAffinity identity，但 Habit Editor 本身没有创建任何 StockRelease 关联；
11. system default Affinity 不被编码成 young / mature bucket；
12. Species Base / default Affinity 在 V1 没有 Archive / Delete action；
13. Fish Basic 删除 / 断开的 `species_key` 触发 `BROKEN_SPECIES_REF` 并阻断 Publish；
14. create-from-absent row 只有在 Production reread + verify + `row_id` durable backfill 全部成功后才算 Publish success。

V1 不以 arbitrary Mode creation、Family、Quality、Bake 或 reconcile 作为验收前提。

### 10.1 还应覆盖的 Contract 验收

除 Golden Path 外，至少再覆盖：

- `LEGACY_UNIMPORTED` Species 不能 fresh create；
- multi-row same-Compat legacy ingress 被 migration blocker 拒绝，而不是自动聚合；
- unmapped Affinity 不会仅因“已存在”就进入 Compat Subject；
- Existing Compat Mode 的 inherit / ADD / SET / CLEAR 能正确 Resolve；
- Compat Mode 完全跟随 Species 时，Component/Profile projection 可以复用，但 Compat `FishEnvAffinity` identity row 仍保留；
- legacy pass-through rows 与 Editor-managed rows 并存时，Publish 只替换 managed projection，pass-through rows reread 后保持不变；
- obsolete Editor-owned Profile projection 可以 cleanup，但 ownership 不明 row 不会被误删；
- ordinary Autosave 遇到 revision conflict 不 last-write-wins、不自动 merge，Resolve / Publish 使用最近成功 durable truth；
- Shared Template 多字段 Candidate 只提交一次并正确传播；
- Template Value Candidate 遇到 revision stale 不自动把旧字段值 rebase 到新 Template；
- Extract 在 incomplete raw input / save failure 时不会拿旧 durable value 冒充“当前值”创建 Template；
- referenced ARCHIVED Template 仍可 Resolve，Hard Delete commit 会重新检查 DirectReferenceSet；
- Production generation drift 阻断 Publish；
- create-from-absent default Affinity 的 `row_id` 回填失败不能被判为 Publish success；
- `row_id` backfill 不得用旧 Editor revision 覆盖并发产生的新 Authoring state。


## 11. Closure Status

### 11.1 Product / semantic closure

以下内容对 V1 已有唯一 Contract，不应在落码时重新设计：

- Species identity 来自 Fish Basic；
- Species Base creation = 五 binding atomic create；
- 每个 Species Base 恰好一个 hidden system default Affinity projection；
- default Affinity 不是业务 Mode、不是第二个 Authoring Subject；
- V1 只编辑既有 Compat Mode；V1.0.1 才补固定 young / mature create；
- Shared Template create / extract / propagation / lifecycle；
- Source / ADD / SET / CLEAR / Policy semantics；
- Resolve Preview；
- Global Publish / generation guard / reread verify；
- StockRelease / FishRelease 关联不归 Habit Editor；
- Species Base / default Affinity 在 V1 不提供 Archive / Delete。

### 11.2 Remaining engineering gates

以下是落码前需要确认的**物理实现 Gate**，不是新的产品设计分支：

**G1｜Fish Basic adapter**

- 确认 authoritative Fish Basic 的稳定 Species ID 字段；
- 确认 UI display name / production naming 所需的 canonical English name 来源；
- 只读接入，不向 Fish Basic 回写。

**G2｜System default Affinity physical carrier**

- 核当前 ProductionRowLedger/schema 是否能表达非 `young / mature` 的 system-default row；
- 若不能，做最小 schema delta；不得把 default 伪装成 compat bucket。

**G3｜Production naming / collision domain**

产品层已经固定“谁命名、谁不命名”和命名应携带的语义；G3 只完成真实 Production schema 下的物理 convention 与安全边界：

- Shared Template 有作者可编辑中文名 / 英文名；stable template identity 不随改名变化；
- 模板级 Component/Profile projection 的 Production name 必须从 Template English Name 确定性派生；是否需要 Kind qualifier 取决于真实 lookup / collision domain；
- 先核对每个 Component/Profile 是否实际落到独立具名 Production row、主表是否按 name 字符串引用该 row、collision domain 是否跨 Kind 共享；
- 若需要 Kind qualifier，当前优先 vocabulary 为 `Temp / Struct / FeedLayer / Period / Policy`：`Period` 对齐 canonical `Time Period`，避免过宽的 `Time`；`FeedLayer` 对齐 canonical `Feeding Layer`，避免 `Feed` 被误读成 food/feed type；`Policy` 仅在真实 Production 存在独立具名 Policy row 时适用；
- 这些 qualifier 属 G3 Production convention，不是 Authoring Semantic Contract；
- 含 Species / Mode 有效 local operation 的 Profile 使用 owner-specific system-generated name；
- system-default `FishEnvAffinity` 名称必须表达 Species canonical English name + Base 语义；
- V1.0.1 fixed Compat Production naming 可以继续表达 Species canonical English name + Juvenile / Mature physical slot；这不要求 UI 中文标签继续写“成年及以上”；
- `FishEnvAffinity` row name 在 V1 / V1.0.1 不作为作者输入；
- 固定 exact prefix / suffix token、delimiter / case / 合法字符 normalization、各表 lookup/collision domain；
- 核实 Production name 是否承担表内 string-reference key，以及这些引用是否全部处于 Habit Editor 全局 Publish 的重写范围；
- 固定 Template English rename 的 materialization 行为：若可以完整重写并 reread/verify，则允许 Publish；若存在无法证明覆盖的外部 name-based reference、orphan / duplicate 风险，则 Publish BLOCK；
- Fish Basic canonical English name 若参与 Affinity Production naming，必须明确它是**受 Publish snapshot/revision guard 的 live input**，还是在 create/bootstrap 时形成的稳定 naming stem；不得让一个未绑定 revision 的外部可变 display field 在 Preflight 与 Execute 之间悄悄改变 materialized key；
- Production name 可以是物理 reference key，但永远不成为 Editor durable identity。

**G4｜row_key → row_id create-from-absent handoff**

- 固定 Production create 后 reread、唯一 row_id 识别、Editor durable backfill 的具体调用顺序；
- `row_id` backfill 是 Publish transaction 内的 system-owned metadata write，不得覆盖更新后的作者语义；
- 若 Production 写入后另一 Editor session 已推进 durable semantic revision，backfill 必须按 stable `row_key` 做受控 metadata patch，或将本次 Publish 判为 unverifiable / recovery-required；不得用旧 revision 整体回写覆盖新 Authoring state；
- backfill 本身可以推进 Editor revision；Publish success 应以完成 backfill 后的 durable state + 已验证 Production baseline 收尾，但不声称并发产生的更新后 Authoring state 已经被本次 Publish 发布；
- backfill / verify 未完成时不得宣告 Publish success，也不得 blind recreate。

**G5｜Initial legacy bootstrap**

- 对首批已有 Production 的目标 Species执行 bounded bootstrap / migration；
- 做一个窄的 compat-token coupling check：确认现有 Runtime / StockRelease / materializer 没有根据 `mature` token 本身推导“成年”业务行为，而只是把它当作既有 Affinity slot / identity。若存在这种硬编码业务分支，UI 不能只靠改中文标签完成语义迁移，必须先显式处理该 coupling；
- multi-row same-Compat 与 unmapped Affinity 必须进入人工 adjudication，不自动聚合或 silent drop；
- bootstrap 必须区分并可承载“明确 Profile absent”与“已有 binding 但 Source broken”两种 ingress state，不能把缺 Profile 伪造成 `BROKEN_SOURCE_REF`，也不能给缺失 Profile 自动补假数据；
- bootstrap 同时建立 managed-vs-pass-through ownership 边界：被接管 row 进入 Editor / ledger ownership，未 adjudicate legacy row 留在 pass-through baseline，后续 Publish 不得误删。

完成 G1–G5 后，V1 vertical slice 不需要再等待新的产品裁决即可进入实现。

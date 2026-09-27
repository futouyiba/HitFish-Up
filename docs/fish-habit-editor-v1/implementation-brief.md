# Fish Habit Editor V1｜Implementation Brief

> Status: Current Implementation Entry for V1  
> Product Authority: [product-contract.md](product-contract.md)  
> Semantic Authority: [common-semantics.md](common-semantics.md)  
> Surface Contracts: [authoring-surface.md](authoring-surface.md), [shared-assets.md](shared-assets.md), [secondary-surfaces.md](secondary-surfaces.md)  
> Scope: [版本范围与阶段路线](../review/fish-habit-editor-version-scope.md)

本文只列 V1 最小生产闭环的实现切面与尚需工程落点，不重新定义产品语义。

本文按“单机单写者、已有 Fish Habit、非破坏性 Publish”组织。Coding Agent 不需要实现多人协作、Species Base fresh-create、legacy adjudication UI、Production GC 或 Git 客户端。

## 1. V1 最小闭环

```text
已有 Species Base / existing Compat
→ Component Source / Operation / Policy Authoring
→ Shared Template
→ Validation / Resolve
→ Publish 到本地 Production working tree
```

V1.0 不实现：

- Species Base fresh-create；
- 新 Species identity；
- 用户创建任意 Mode；
- Family / Species Preset；
- Quality / StockRelease / FishRelease authoring；
- Bake；
- 多人 / 多会话协同编辑；
- Production reverse reconcile；
- Production orphan GC / cleanup。

## 2. Local workspace / host model

开发阶段：

```text
Browser
→ local dev server
→ same Editor Core / Workspace API
```

正式发布：

```text
Electron renderer
→ preload / IPC
→ same Editor Core / Workspace API
→ local filesystem
```

Web dev 与 Electron release 共享同一套 Domain / Resolver / Validator / Materializer；Electron 只是正式 Host Shell，不另写一套产品逻辑。

发布 ZIP 的目标结构：

```text
FishHabitEditor-v1/
├─ app/                  # Electron executable / runtime
├─ authoring/            # Editor durable truth，V1 当前为 JSON；后续可扩 CSV
├─ production/           # Production tables working tree
│  ├─ .git/
│  └─ ...
└─ workspace.json        # 可选；记录相对路径 / schema version
```

硬规则：

- mutable Authoring / Production 数据与 Electron binary 分离，不塞进 `app.asar`；
- `production/` 作为独立 Git working tree 随 ZIP 一起交付；
- Editor 只读写文件，不实现 Git pull / commit / merge / push；
- 多人协作、版本同步、diff / merge 冲突完全交给 Git 工作流。

V1 可固定目录结构，不要求做 Workspace 管理 UI。

## 3. Existing Fish / Affinity integration

V1.0 只加载已经存在、可以明确映射的 Fish Habit：

- Species identity / display name 来自 Fish Basic，只读；
- Species Base 已存在；
- system-default Affinity 已存在并可映射到该 Species Base；
- existing Compat row 若属于 `young / mature` physical slot，则作为“小个体 / 大个体 [兼容]”Subject；
- 没有 Species Base 的 Fish 不在 V1.0 创建；
- unmapped legacy row 不要求在 Editor 中 adjudicate；V1.0 可以不暴露它。

Affinity identity 与 Component/Profile projection 分开：

- system-default / Compat Affinity identity row 不因 payload 相同而合并；
- Component/Profile row 可以按明确 Source / lineage 复用。

StockRelease / FishRelease 如何把 Quality / FishPoint 映射到哪条 Affinity，仍由下游显式配置；Habit Editor 不维护该关系。

## 4. Source catalog / picker

每个 Component 的 Source Picker 统一支持：

1. **Shared Template**；
2. **Existing Production Profile**。

Existing Production Profile catalog：

- 按 Component Kind 读取合法 Production rows；
- 不建立“属于哪个 Fish”的 ownership 筛选；
- 不根据当前 Species / Quality / Affinity 猜归属；
- UI 直接显示 Production row 已有英文 `name`；
- Shared Template 分组置前，Existing Production 分组置后并标为兼容来源。

Compat Subject 额外允许“跟随基础习性”。

Source change 继续使用 Candidate Preview，因为它会改变整个 Component 的计算基准；这与多人协同无关，不应删除。

## 5. Single-writer persistence

Authoring Truth 只存在本机 workspace。

普通编辑：

```text
typed input
→ debounce/coalesce
→ local atomic save
```

要求：

- save failure 不冒充成功；
- Resolve / Publish 只消费最近一次成功保存的 state；
- V1.0 不做 optimistic multi-session revision protocol；
- 不做字段级 merge / rebase / conflict replay；
- Git 负责人与人之间的协作与冲突解决。

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

Publish 是单机全局动作，但实现保持简单：

```text
flush / verify saved Authoring state
→ full validation
→ read current Production working tree
→ materialize
→ create / update 明确目标 rows
→ keep all other rows unchanged
→ reread touched rows/files
→ verify
→ success
```

V1.0 使用**非破坏性 patch**：

- 不删除 Editor 不认识的 row；
- 不做 orphan GC / obsolete-row cleanup；
- 不做 managed-vs-pass-through ownership graph；
- 不做 whole-generation concurrent baseline protocol；
- 不做多人 revision R / R+1；
- touched output reread + verify 仍是 success 必要条件。

如果 materialization 需要新建 Production row 并取得 `row_id`：

```text
create → reread → unique row_id → local mapping → verify
```

未完成这条链路不宣告成功，不 blind recreate。

## 9. 推荐实现顺序

```text
1. Local workspace / Electron host adapter
2. Existing Species Base + Compat loading
3. Source catalog：Template + Existing Production Profile
4. Species Base / Compat Authoring
5. Shared Template create / edit / propagation
6. Resolve
7. Non-destructive Publish + reread verify
8. V1.0.1 fixed Compat slot create
```

其中 1–7 构成 V1.0；8 不阻塞 V1.0。

## 10. V1 验收最小样例

至少覆盖：

1. 打开 ZIP workspace / dev workspace 后能读取已有 Species Base 与 existing Compat；
2. system-default Affinity 不作为第二个业务 Subject 显示；
3. `young / mature` UI 投影为“小个体 / 大个体”，且缺任一 slot 都合法；
4. Species Base Component 可从 Shared Template 或同 Kind Existing Production Profile 选 Source；
5. Existing Production Source 直接显示原英文 `name`，不生成“当前鱼种现有数据”解释名；
6. Source Change Candidate 正确展示 before / after，原有 Operation 不被偷偷清理；
7. 普通字段 Autosave 到本地 Authoring JSON；
8. Extract / Template edit / propagation 可用；
9. Resolve 解释当前 saved Authoring Truth；
10. Publish 只 create / update 明确目标 row，其它 Production row 保持不变；
11. Publish 后 reread touched output 并 verify；
12. Production working tree 可由外部 Git 直接 diff / commit；Editor 不实现 Git merge；
13. save / Production write failure 不冒充成功；
14. 不存在 Species Base fresh-create / `AVAILABLE_NEW` / `LEGACY_UNIMPORTED` 产品流程。

V1.0 不以 arbitrary Mode creation、Family、Quality、Bake、多人协作、reconcile 或 Production GC 作为验收前提。





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
- V1.0.1 fixed Compat Production naming 可以继续表达 Species canonical English name + Juvenile / Mature physical slot；这不要求 UI 中文标签与旧年龄术语保持直译，当前 UI 使用“小个体 / 大个体”；
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
- multi-row same-Compat 与 unmapped Affinity 必须进入人工 adjudication，不自动聚合或 silent drop；
- bootstrap 必须区分并可承载“明确 Profile absent”与“已有 binding 但 Source broken”两种 ingress state，不能把缺 Profile 伪造成 `BROKEN_SOURCE_REF`，也不能给缺失 Profile 自动补假数据；
- bootstrap 同时建立 managed-vs-pass-through ownership 边界：被接管 row 进入 Editor / ledger ownership，未 adjudicate legacy row 留在 pass-through baseline，后续 Publish 不得误删。
- `young / mature` 在 Habit Editor 中只作为既有 Compat physical slot / identity；哪个 Quality / FishPoint / StockRelease row 使用哪条 Affinity 由下游显式引用关系决定，不从 slot token 自动推导。因此 UI 将其投影为“小个体 / 大个体”不要求重迁既有 Affinity row，也不改变下游映射自由度。

完成 G1–G5 后，V1 vertical slice 不需要再等待新的产品裁决即可进入实现。

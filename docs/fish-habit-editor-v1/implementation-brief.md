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
1. Existing Species Base + Compat loading
2. Species Base / Compat Authoring
3. Source catalog：Template + Existing Production Profile
4. Shared Template create / edit / propagation
5. Resolve
6. Web dev server 下完成 Non-destructive Publish + reread verify
7. Electron Host Shell + portable ZIP packaging
8. V1.0.1 fixed Compat slot create
```

先在 Web dev server 下完成核心闭环，最后再包 Electron；不要让桌面壳阻塞 Domain / Authoring / Publish 开发。

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
14. V1.0 没有 Species Base fresh-create / Species initialization 产品流程。

V1.0 不以 arbitrary Mode creation、Family、Quality、Bake、多人协作、reconcile 或 Production GC 作为验收前提。





## 11. Closure Status

### 11.1 Product / semantic closure

V1.0 已冻结的最小语义：

- 只编辑已有 Species Base / existing Compat；
- Species identity 来自 Fish Basic，只读；
- system-default Affinity 是已有 Species Base 的 Production projection，不是第二个 Authoring Subject；
- `young / mature` 只是既有 Compat physical slots，UI 映射为“小个体 / 大个体”；
- Component Source = Shared Template 或同 Kind Existing Production Profile；Compat 还可 Follow Species；
- Existing Production Source 直接显示原英文 `name`，不推导 Fish ownership；
- Source / ADD / SET / CLEAR / Policy / Resolve 语义保持现行 Contract；
- Shared Template create / extract / propagation / lifecycle 保留；
- Publish = 单机非破坏性 create/update + touched-output reread/verify；
- 多人协作、Git merge、Production GC、reverse reconcile 不属于 V1.0。

### 11.2 Remaining engineering gates

只保留真正会阻塞落码的物理问题。

**G1｜Existing Fish / Species adapter**

- 确认 Fish Basic 稳定 Species ID 与 display / canonical English name 来源；
- 确认已有 Species Base 与 system-default Affinity 的映射入口；
- 只读 Fish Basic，不提供 Species Base fresh-create。

**G2｜Source catalog adapter**

- 为每个 Component Kind 枚举合法 Existing Production Profile rows；
- 暴露稳定 row identity + 原始英文 `name` + typed payload；
- 不实现 current-Species ownership 推断；
- 与 Shared Template 一起提供统一 Source Picker 数据。

**G3｜Production materialization / naming**

- 固定各 Profile / Affinity 子表的真实 lookup key、name collision domain 与 exact normalization；
- Shared Template English name 如何派生 Production Profile name；
- Existing row 能否原地 update、何时必须 create 新 row；
- 新 row 若有 `row_id`，完成 create → reread → mapping → verify；
- Publish 采用非破坏性 patch，不承担旧 row cleanup。

完成 G1–G3 后，V1.0 不需要新的产品裁决即可实现。

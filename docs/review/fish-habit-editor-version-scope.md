# Fish Habit Editor｜版本范围与阶段路线

> Status: Current Scope Baseline  
> Purpose: 只定义 Fish Habit Editor 各阶段承诺的能力边界、明确不做项与后续进入条件。本文不记录决策历史，不替代具体 UI / Persistence / Runtime Contract。
>
> **Version commitment:** V1 是当前需要闭合与验收的交付范围；V1.0.1 是紧随 V1 的窄增量，仅补固定 Compat Mode 创建；V1.1 / V1.2 / V1.3+ / V2 是后续能力分组与进入条件，不构成固定发布日期。不得把后续能力反向塞回 V1。

## 1. 总体产品边界

Fish Habit Editor 的职责是维护“鱼的中鱼习性 Authoring Truth”，并将其通过 Resolve / Publish 投影到生产配置。

长期边界：

- **Habit Editor 管习性 Authoring，不管理 FishPond / StockRelease / FishRelease 的投鱼拓扑。**
- **Quality 不属于 Habit Editor 的普通 Authoring IA。** Quality 数量、大小范围和投放构成由 FishPond / StockRelease / FishRelease 一侧配置；Habit Editor 不维护静态的 `Mode → Quality` durable relation。
- **Production 是 Habit Editor-owned domain 的 materialized output，不是并行 Authoring Truth。**
- Materialized Production 数值不能无损反推出 Template / Source / ADD / SET / CLEAR 等作者意图，因此不把“自动双向同步”作为目标。
- V1.0 是单机单写者工具；多人协作、diff / merge / 冲突处理完全交给 Production / Authoring 工作区外部的 Git 流程。
- V1.0 不创建 Species Base；只编辑已有 Species Base / existing Compat，不接管 StockRelease / FishRelease 等跨域生产拓扑。

## 2. V1｜Species Habit Authoring Minimum Loop

### 2.1 阶段目标

V1.0 证明一条最小、可制作的**已有习性编辑闭环**：

```text
已有 Species Base / existing Compat
→ Authoring
→ Validation
→ Resolve Preview
→ 非破坏性 Publish 到本地 Production working tree
```

V1.0 的核心成果：

1. 已有 Species Base 可以稳定编辑；
2. existing `young / mature` Compat 可以作为“小个体 / 大个体”编辑，且 0 / 1 / 2 个都合法；
3. Component Source 可以在 Shared Template 与同 Kind Existing Production Profile 之间选择；
4. Resolve 能解释 saved Authoring Truth；
5. Publish 只 create / update 明确目标 row，保留其它 Production rows，并 reread / verify 本次写入；
6. 正式发布形态是 Electron 本地工具；多人协作交给 Git。

### 2.2 V1 Included

#### Fish / Subject

- Fish / Species identity 来自 Fish Basic，只读；
- V1.0 只展示已经存在 Species Base 的 Fish；
- Species Base / 基础习性是默认习性 Authoring Truth；
- existing `young / mature` physical slots 作为“小个体 / 大个体 [兼容]”Subject；
- 模式是相对 Species Base 的可选差异，不要求成对存在；
- V1.0 不创建 Species Base，也不创建新的业务 Mode；
- StockRelease / FishRelease 继续负责 Quality / stocking row 到 FishEnvAffinity 的显式引用。

#### Component Authoring

四个 Component：

- Temperature
- Structure
- Feeding Layer
- Time Period

支持：

- Source binding；
- Shared Template；
- Existing Production Profile；
- Species / Compat scope operation；
- ADD / SET / CLEAR / inherit/absent；
- Effective Value / provenance；
- Role / Profile 正交；
- Validation / diagnostics。

Source Picker：

- Shared Template 为主路径；
- Existing Production Profile 为过渡兼容路径；
- Existing Production 只按 Component Kind 筛选；
- 不推导“属于当前鱼种”；
- 直接显示 Production row 原英文 `name`。

#### Spatial Opportunity Policy

- Species-level Policy Template binding；
- Species-level Role / `fail_env_coeff`；
- existing Compat row-level Role / coeff patch；
- 不引入 Quality-owned Policy 或 multi-row Compat 聚合。

#### Shared Assets

- Shared Template browse / create / extract / clone；
- Template value edit + Impact Preview；
- ACTIVE / ARCHIVED；
- Replace References；
- Hard Delete guard。

#### Preview / Publish

- Validation；
- Resolve Preview；
- Source / Template staged Candidate；
- 单一 Publish Surface；
- 非破坏性 create / update；
- touched output reread / verify；
- 不做多人 revision protocol、Production GC、reverse reconcile 或 Git client。

### 2.3 V1 Data / Species Baseline

V1.0 的数据前提很简单：

- Fish Basic 提供稳定 Species identity 与显示信息；
- Species Base 已经存在；
- system-default Affinity 已存在并可映射；
- existing `young / mature` Compat row 可按 physical slot 映射；
- 无法明确映射的 legacy row 可以不暴露给 V1.0 Editor，不要求做 migration adjudication UI；
- 没有 Species Base 的 Fish 不进入 V1.0。

V1.0 不定义 `AVAILABLE_NEW`、`LEGACY_UNIMPORTED`、Species Base initialization 或 fresh-create 流程。

### 2.4 V1 Persistence / Packaging

Canonical Authoring persistence 继续使用当前 JSON Editor State；后续可以扩展为多 CSV，但不作为 V1.0 前提。

正式交付采用 portable Electron workspace：

```text
FishHabitEditor-v1/
├─ app/
├─ authoring/
├─ production/
│  ├─ .git/
│  └─ production tables...
└─ workspace.json
```

- Electron binary 与 mutable data 分离；
- Production 是独立 Git working tree；
- Editor 不实现 Git pull / commit / merge / push；
- 开发阶段可继续通过 local dev server 运行同一套 Editor Core。

### 2.5 V1 Explicitly Out of Scope

V1 不承诺：

- 创建新的 Species identity；
- 创建 Species Base / “开始配置其他鱼种”；
- Family / 鱼家族初始化；
- Species Preset / 鱼家族预设；
- 新建 Engagement Mode；
- Mode lifecycle；
- Mode Routing / Share；
- Quality 页面、Quality authoring、Quality ↔ Mode / Affinity 静态关系；
- FishPond / StockRelease / FishRelease authoring；
- 从钓鱼元素周期表 / 外部生态数据库自动 Import / Reimport；
- Lux CLI 等外部数据接入链路；
- 全量历史 Production 自动迁移 / migration adjudication UI；
- 自动聚类并生成 Shared Template；
- Production 外部修改的自动 reverse import；
- Production ↔ Editor 自动双向同步；
- CSV canonical persistence migration；
- 全量 reconcile / semantic recovery；
- Production orphan GC / obsolete-row cleanup；
- 多人 / 多会话协同编辑协议；
- 内置 Git 客户端；
- Species Base / system default Affinity Archive / Delete。

## 3. V1.0.1｜Fixed Compat Mode Creation

V1.0.1 是紧随 V1 的窄增量，只补 fixed Compat slot 的按需创建：

```text
UI          physical slot
小个体      young
大个体      mature
```

两个 slot **不要求成对创建**。若当前设计只需要“基础习性 + 小个体中鱼习性模式”，可以长期没有 `mature` row。

不支持任意 Mode 名称，不引入正式 Engagement Mode registry / Routing / Share。

创建规则：

- 目标 Species 必须已经有 Species Base；
- 只允许创建当前缺失的固定 Compat Mode；
- 新建对应 `FishEnvAffinity` / ProductionRowLedger 记录；
- Editor 先生成稳定 `row_key`，Production `row_id` 可在 Publish 后获得；
- 四个 Component 初始 Source = 跟随 Species Base；
- numeric operations 初始 absent；
- Role / `fail_env_coeff` 初始 inherit Species；
- UI 业务显示名固定为“小个体 / 大个体”，不要求用户填写 Mode name；physical type 仍为 `young / mature`，Production `FishEnvAffinity` row name 可继续沿用既有 Juvenile / Mature naming convention，不要求同步改英文名；具体命名格式属于 Common Semantics / Implementation Contract。
- StockRelease / FishRelease 是否让某个 Quality 使用该 Affinity，继续由其自己的配置表维护，不属于 Habit Editor。

V1.0.1 的固定 Compat Mode creation 是 create-only 窄增量；不在该版本补 Mode Archive / Delete / rename。删除生命周期仍等待跨域引用边界闭合。

V1.0.1 不处理任意 Engagement Mode 与 bucket-scoped operation owner 的关系。

## 4. V1.1｜Authoring Efficiency

> Bake Preview / 条件组求值预览不属于 V1 承诺。是否在 V1.1 或更后阶段进入，以预览输入、基础权重、条件组来源与验收口径闭合为前提。



V1.1 的目标是提升生产效率，不改变 V1 已验证的 Authoring Truth 边界。

优先候选：

### 4.1 Multi-CSV Bulk Authoring

研究并实现**规范化多 CSV 套表**工作流，目标是让策划和脚本可以直接：

- 横向扫描大量 Fish / Component；
- 用 Excel / 公式 / Python 做批量变更；
- 更直观地 Review before / after；
- 通过 Git diff 审阅二维表格变化；
- 再进入 Validator / Editor 形成安全 durable state。

第一阶段可以采用：

```text
JSON canonical persistence
↔ CSV bulk-edit projection / import
```

先验证真实生产工作流。

如果验证成立，再决定后续是否将规范化 CSV 提升为 canonical persistence。

多 CSV 设计必须保留：

- stable identity；
- absence 与 CLEAR / SET 的语义差异；
- cross-table reference validation；
- schema version；
- stable ordering；
- 多文件事务一致性。

允许保留轻量 manifest / metadata 文件；“业务数据主要采用 CSV”不要求目录内只能存在 CSV。

### 4.2 Authoring Efficiency Enhancements

可根据 V1 使用反馈进入：

- 更好的批量筛选 / Review；
- Template consolidation 辅助；
- 聚类 / Family 初始化研究（只作后续 Topology Creation 输入，不进入 V1 Shared Assets）；
- Golden Seed / migration tooling 的工程化增强。

V1.1 不扩展任意 Engagement Mode / Routing；Species Base initialization 已属于 V1，固定 Compat Mode creation 已属于 V1.0.1。

## 5. V1.2｜Advanced Mode & Data Integration

这一阶段不再解决 Species Base 是否能从 Editor 创建——该闭环已经在 V1 完成。这里开始处理更高级的初始化效率、任意 Engagement Mode 与外部数据接入。

### 5.1 Advanced Fish Initialization

V1 已支持从 authoritative Species Catalog 创建完整 Species Base。

这一阶段只研究更高级的初始化效率，例如：

- Family / 聚类辅助；
- Species Preset；
- 批量初始化；
- 外部生态数据辅助。

Family / Preset 若进入，只作为初始化便利，不形成长期 parent relation。

### 5.2 Engagement Mode Creation

在 V1.0.1 fixed `young / mature` slot（UI：小个体 / 大个体）创建之外，支持：

- 新建真正需要的任意 Engagement Mode；
- Mode identity / lifecycle；
- Mode 初始 Authoring state；
- Mode-level Habit / Policy authoring；
- Materializer 从 absent 创建所需 Habit production projection。

V1.0.1 已覆盖固定 young / mature Compat Mode 的按需创建；本阶段只处理超出固定 Compat 的任意 Mode。

这一阶段开始前必须闭合：

- Mode identity；
- create / archive / delete lifecycle；
- FishEnvAffinity projection / naming / id 规则；
- row-level Policy 初始语义；
- Publish create-from-absent；
- Bootstrap / roundtrip symmetry。

### 5.3 External Ecological Data Integration

外部生态数据接入可在该阶段或之后进入，例如：

- 钓鱼元素周期表；
- Lux CLI；
- Temperature Species Concrete Import / Reimport；
- 外部数据 provenance；
- external-source failure / diff / candidate review。

这类能力不作为 V1 承诺。

### 5.4 Quality Boundary Remains

即使进入 Mode Creation：

- Habit Editor 仍不维护静态 `Mode → Quality` durable relation；
- Quality / stocking composition 继续属于 FishPond / StockRelease / FishRelease domain；
- 不因创建 Mode 把 Release topology 拉回 Habit Editor。

## 6. V1.3+｜Reconcile & Advanced Production Workflow

该阶段处理 Editor 之外发生的修改和更复杂的生产维护。

可能包括：

- Production external drift inspection；
- 显式 reconcile / import session；
- 对无法唯一恢复的作者意图进行人工 adjudication；
- legacy / externally edited production data 的 semantic recovery；
- 更成熟的 migration tooling；
- 若多 CSV 工作流已被验证，评估将其提升为 canonical persistence。

明确不以“自动双向同步”作为默认目标。

## 7. V2｜Full Engagement Mode / Routing

V2 处理真正动态的 Engagement Mode 体系。

可能包括：

- 正式 Engagement Mode identity；
- 基于 Species habit、scene、weather / environment 等因素的模式判断与分群；
- Routing / Share / context-dependent selection；
- Mode 与未来 evaluator / bake / runtime contract 的正式连接。

V1 的兼容 scope UI 不能被用来反推 V2 Routing 参数形态。

## 8. 版本切分原则

每次升级只有在新增能力能形成完整因果闭环时才进入上一版本承诺。

优先顺序：

1. **先闭合 Species Base Creation + Existing Compat Authoring；**
2. **V1.0.1 只补 fixed `young / mature` Compat slot Creation（UI：小个体 / 大个体），且不要求成对创建；**
3. **再提升批量 Authoring / Persistence 效率；**
4. **再进入任意 Engagement Mode / 高级初始化；**
5. **再接外部数据与 reconcile；**
6. **最后进入完整 Engagement Mode / Routing。**

不为了展示“功能多”而提前暴露没有 durable semantics 的按钮、占位字段或伪控件。

V1 Review 的核心问题应始终是：

> **在不依赖后续能力的情况下，一个作者能否从 Fish Basic 选择已有 Species，创建或编辑完整 Species Base，并安全地验证、解析和发布；同时继续编辑已有 Compat Mode？**

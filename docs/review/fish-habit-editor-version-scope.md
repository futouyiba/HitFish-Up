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
- Bootstrap 之后，Habit Editor 不承诺持续 `Production → Editor` 自动反向同步；检测到外部 Production 变化时应阻断 Publish，并交给后续显式 reconcile / migration 流程处理。
- Materialized Production 数值不能无损反推出 Template / Source / ADD / SET / CLEAR 等作者意图，因此不把“自动双向同步”作为目标。
- 已有 Habit owner 内部可以按既有 Materializer 规则创建必要 projection row；“不创建 topology”特指本阶段不创建新的 Fish / Engagement Mode 等业务身份和跨域生产拓扑。

## 2. V1｜Species Habit Authoring Minimum Loop

### 2.1 阶段目标

V1 证明一条最小、可制作的 Authoring 闭环：

```text
Fish Basic / authoritative Species Catalog
→ 已有 Habit：直接编辑
→ 无 Habit：开始配置习性
→ 原子创建完整 Species Base
→ Authoring
→ Validation
→ Resolve Preview
→ Publish
```

V1 的核心成果不是覆盖所有 Runtime / StockRelease 拓扑，而是证明：

1. Species identity 继续由 Fish Basic 提供，Habit Editor 只创建自己拥有的 Species Base；
2. 新建 Species Base 与既有 Species Base 使用同一套 Authoring / Resolve / Publish；
3. 已有兼容 Mode 可以继续编辑；
4. 新建 Species Base 同时得到一个系统默认 FishEnvAffinity 投影，使其具备最小运行时引用入口；
5. V1.0.1 只负责在默认 Affinity 之外再补固定 Compat Mode（幼年 / 成年及以上）。

### 2.2 V1 Included

#### Fish / Subject

- Fish List 读取 Fish Basic / authoritative Species Catalog；Habit Editor 不创建新的 Species identity，也不维护鱼类基础数据、模型、图鉴或 Quality。
- 已有 Habit 的 Species 直接编辑 Species Base / 基础习性。
- 尚无 Habit 的 Species 可以通过“开始配置习性”创建完整 Species Base；Species 只能从 Fish Basic 已有条目中选择。
- 编辑 Bootstrap 已经存在的兼容习性 Scope；产品 UI 可用“中鱼习性模式”表达业务心智，并以中性 `[兼容]` badge 标识当前承载方式。
- **V1 当前兼容拓扑中，一个可编辑中鱼习性模式对应一条既有 `FishEnvAffinity` 行。** 不在一个 Mode Context 下聚合多条 Affinity 行，也不建立额外的 Mode→Quality 解释层。
- V1 不允许用户创建新的业务中鱼习性 Mode；新 Species 只自动建立一个系统默认 FishEnvAffinity 投影。已有兼容 Mode 继续编辑。
- StockRelease / FishRelease 继续负责 Quality / stocking row 与 FishEnvAffinity 的关联，Habit Editor 不创建或维护该关系。

#### Component Authoring

四个习性 Component：

- Temperature
- Structure
- Feeding Layer
- Time Period

支持现行 V1 Authoring Contract 中的：

- Source binding；
- Shared Template；
- Species / Compat scope operation；
- ADD / SET / CLEAR / inherit/absent 等各字段允许的语义；
- Effective Value / provenance 只读派生；
- Role / Profile 正交；
- 合法 Empty / Setup 状态；
- Validation 与 blocking diagnostics。

Temperature V1 以**手工 Authoring**为主，不承诺外部生态数据库自动导入。

#### Spatial Opportunity Policy

- Species-level Policy Template binding。
- Species-level Role / `fail_env_coeff` Authoring。
- 对已有兼容 topology，每个兼容中鱼习性模式直接编辑其对应的单条 `FishEnvAffinity` row-level Role / `fail_env_coeff` patch。
- 不把 row-level Policy 解释成 Quality-owned 数据，也不在 V1 引入 multi-row Compat 聚合 UI。

#### Shared Assets

- Shared Template 浏览与编辑。
- Template 创建 / Extract。
- ACTIVE / ARCHIVED。
- Replace References。
- Hard Delete guard。
- Direct Reference / Effective Consumer 可见性。

V1 Shared Assets **只包含 Shared Template**；Species Preset / 鱼家族预设不进入 V1。

#### Preview / Publish

- Validation。
- Resolve Preview。
- staged Candidate / Rebase / Impact Preview（只用于现行需要 staged confirm 的变更）。
- Publish Preflight。
- 单一 canonical Publish executor。
- Production generation mismatch / unverifiable 时 BLOCK。
- Publish success / failure / partial failure 的明确事务状态。

### 2.3 V1 Data / Species Catalog Baseline

V1 直接读取 Fish Basic / authoritative Species Catalog，不要求所有 Species 预先拥有 Habit Entry。

规则：

- Species identity / `species_key` 只能来自 Fish Basic 既有条目；
- Habit Editor 不创建 Fish Basic Species，也不维护基础数据、模型、图鉴或 Quality；
- 默认 Fish List 可以只展示已配置 Habit 的短列表；
- “开始配置其他鱼种”通过搜索 Fish Basic 选择尚未配置 Habit 的 Species；
- V1 为该 Species 创建 Habit Editor 自己拥有的 Species Base，并同时建立一个**系统默认 FishEnvAffinity 投影壳**；该默认 Affinity 不是新的业务 Mode，也不是第二套 Authoring Subject。

新 Species Habit 的正常创建态要求一次性选择：

```text
Temperature Source
Structure Source
Feeding Layer Source
Time Period Source
Policy Template
```

全部完成后 atomic create：

1. 完整 Species Base；
2. 一个系统默认 `FishEnvAffinity` / ProductionRowLedger 投影壳。

默认 Affinity 的初始语义固定为：

- 四个 Component 全部跟随 Species Base；
- numeric operation 全部 absent；
- Role / `fail_env_coeff` 全部 inherit Species；
- 不作为左栏额外 Mode Subject 展示，避免与“基础习性”形成重复编辑入口；
- Editor 使用稳定 `row_key`，Production `row_id` 在 Publish 后获得；
- human-readable production name 由系统生成并做 collision validation。

因此新 Species 创建完成后已经有一份可被 StockRelease / FishRelease 在其自身配置表中引用的默认 EnvAffinity；Habit Editor **不创建或维护那条 StockRelease 引用关系本身**。

Golden Seed / Snapshot 继续用于 demo / regression / migration / roundtrip evidence，但不决定其它 Fish Basic Species 是否可以开始配置。

已有 Production migration 与新 Species initialization 分开：

- Migration 负责承接已有习性数据；
- 新 Species initialization 由作者显式选择 Source / Policy；
- Shared Template 整理、聚类和业务命名不要求 Bootstrap 自动推断。

### 2.4 V1 Persistence

- Canonical persistence 继续使用当前 JSON Editor State。
- V1 不以 JSON → CSV persistence migration 为交付前提。
- JSON 的限制不阻塞 V1 产品闭环；批量 Authoring / 多 CSV 方案作为后续基础设施候选处理。

### 2.5 V1 Explicitly Out of Scope

V1 不承诺：

- 创建新的 Species identity；
- Family / 鱼家族初始化；
- Species Preset / 鱼家族预设；
- 新建 Engagement Mode；
- Mode lifecycle；
- Mode Routing / Share；
- Quality 页面、Quality authoring、Quality ↔ Mode / Affinity 静态关系；
- FishPond / StockRelease / FishRelease authoring；
- 从钓鱼元素周期表 / 外部生态数据库自动 Import / Reimport；
- Lux CLI 等外部数据接入链路；
- 全量历史 Production 自动迁移；
- 自动聚类并生成 Shared Template；
- Production 外部修改的自动 reverse import；
- Production ↔ Editor 自动双向同步；
- CSV canonical persistence migration；
- 全量 reconcile / semantic recovery。

## 3. V1.0.1｜Fixed Compat Mode Creation

V1.0.1 是紧随 V1 的窄增量，只补固定 Compat Mode 创建：

```text
幼年
成年及以上
```

不支持任意 Mode 名称，不引入正式 Engagement Mode registry / Routing / Share。

创建规则：

- 目标 Species 必须已经有 Species Base；
- 只允许创建当前缺失的固定 Compat Mode；
- 新建对应 `FishEnvAffinity` / ProductionRowLedger 记录；
- Editor 先生成稳定 `row_key`，Production `row_id` 可在 Publish 后获得；
- 四个 Component 初始 Source = 跟随 Species Base；
- numeric operations 初始 absent；
- Role / `fail_env_coeff` 初始 inherit Species；
- 业务显示名固定为“幼年 / 成年及以上”，不要求用户填写 Mode name；Production human-readable row name 由实现按 Species + 固定 Compat type 自动生成并做 collision validation，具体字符串格式属于 implementation contract，不作为新的产品输入。
- StockRelease / FishRelease 是否让某个 Quality 使用该 Affinity，继续由其自己的配置表维护，不属于 Habit Editor。

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

V1.1 不默认等同于“正式创建新 Fish / 新 Mode”；是否进入 Topology Creation 以相关机制 Contract 是否闭合为准。

## 5. V1.2｜Topology Creation & Data Integration

这一阶段开始解决“新的鱼可以从 Editor 出生”。

### 5.1 Advanced Fish Initialization

V1 已支持从 authoritative Species Catalog 创建完整 Species Base。

这一阶段只研究更高级的初始化效率，例如：

- Family / 聚类辅助；
- Species Preset；
- 批量初始化；
- 外部生态数据辅助。

Family / Preset 若进入，只作为初始化便利，不形成长期 parent relation。

### 5.2 Engagement Mode Creation

在 V1.0.1 固定幼年 / 成年及以上创建之外，支持：

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
2. **V1.0.1 只补固定幼年 / 成年及以上 Compat Mode Creation；**
3. **再提升批量 Authoring / Persistence 效率；**
4. **再进入任意 Engagement Mode / 高级初始化；**
5. **再接外部数据与 reconcile；**
6. **最后进入完整 Engagement Mode / Routing。**

不为了展示“功能多”而提前暴露没有 durable semantics 的按钮、占位字段或伪控件。

V1 Review 的核心问题应始终是：

> **在不依赖后续能力的情况下，一个作者能否从 Fish Basic 选择已有 Species，创建或编辑完整 Species Base，并安全地验证、解析和发布；同时继续编辑已有 Compat Mode？**

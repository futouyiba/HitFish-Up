# Fish Habit Editor｜版本范围与阶段路线

> Status: Current Scope Baseline  
> Purpose: 只定义 Fish Habit Editor 各阶段承诺的能力边界、明确不做项与后续进入条件。本文不记录决策历史，不替代具体 UI / Persistence / Runtime Contract。
>
> **Version commitment:** V1 是当前需要闭合与验收的交付范围；V1.1 / V1.2 / V1.3+ / V2 是后续阶段的能力分组与进入条件，不构成已经承诺的发布日期或固定顺序。V1 收口后的真实成本与依赖可以调整后续阶段编号，但不得把后续能力反向塞回 V1。

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

V1 证明一条完整生产闭环：

```text
已有 Production / Bootstrap Seed
→ Editor durable state
→ 手工 Authoring
→ Validation
→ Resolve Preview
→ Publish
→ 更新既有 Habit Production projection
```

V1 的核心成果不是“覆盖所有生产操作”，而是证明：

1. 已有习性数据能够进入新的 Authoring Model；
2. Editor State 可以成为 Habit Authoring Truth；
3. 作者可以在一个因果清楚的工具里完成编辑、验证、预览和发布；
4. Publish 可以安全物化到已有 Habit topology。

### 2.2 V1 Included

#### Fish / Subject

- Fish List 读取 Fish Basic / authoritative Species Catalog；Habit Editor 不创建新的 Species identity，也不维护鱼类基础数据、模型、图鉴或 Quality。
- 已有 Habit 的 Species 直接编辑 Species Base / 基础习性。
- 尚无 Habit 的 Species 可以通过“开始配置习性”创建完整 Species Base；Species 只能从 Fish Basic 已有条目中选择。
- 编辑 Bootstrap 已经存在的兼容习性 Scope；产品 UI 可用“中鱼习性模式”表达业务心智，并以中性 `[兼容]` badge 标识当前承载方式。
- **V1 当前兼容拓扑中，一个可编辑中鱼习性模式对应一条既有 `FishEnvAffinity` 行。** 不在一个 Mode Context 下聚合多条 Affinity 行，也不建立额外的 Mode→Quality 解释层。
- V1 不创建新的中鱼习性 Mode / FishEnvAffinity row；只编辑已经存在的兼容 Mode。
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

### 2.3 V1 Data / Coverage Baseline

V1 明确采用 **Bounded Coverage**：它是“编辑已预置 Habit topology 的鱼”的生产工具，不是 Fish onboarding 工具。

#### V1 Coverage Set

每次部署必须显式定义一个 `V1 Coverage Set`：

> 本次 V1 承诺可在 Editor 中编辑的 Species 集合。

Coverage Set 中的每条 Species 必须在部署前已经拥有可加载的 Habit Entry / 既有兼容 topology。其来源可以是 bounded bootstrap、一次性 migration script 或人工复核后的 seed preparation；这些都是**部署准备 / migration 工作**，不是 Editor 内的“新建鱼”产品能力。

规则：

- Coverage Set 内缺少 Habit Entry ⇒ **V1 deployment blocker**，不能运行时隐式 auto-create；
- Species Catalog 中不在 Coverage Set 的 Species 可以被 Coverage Browser 看见，但不成为可编辑 Subject；
- V1 不为缺失 Entry 自动制造 Species Base、默认 Source、默认 Role 或兼容 Mode；
- Coverage Set 可以是当前里程碑需要的子集，不要求为了 V1 一次性承诺所有未来 Species；
- 若产品目标要求“整个当前 Species Catalog 都可编辑”，则部署前 Coverage Set 就必须覆盖整个目标 Catalog，这属于数据准备成本，不应伪装成 UI 免费能力。

#### Golden Seed / Snapshot

除部署 Coverage 外，V1 仍应提供一份**小而真实、人工复核过的 Golden Seed / Snapshot**，用于：

- 展示真实 Fish Habit Authoring；
- 验证已有 Production 数据能够被 bounded bootstrap 到 Editor；
- 覆盖 Template fan-out、Species override、兼容 scope、Policy、Resolve、Publish 等关键路径；
- 作为 demo / regression / roundtrip evidence。

Golden Seed 不等于完整 Coverage Set；它可以只是其中有代表性的少量对象。

Migration 与 Semantic Consolidation 分开：

- Migration 负责尽量保真地承接 legacy data；
- Shared Template 语义整理、聚类和业务命名属于后续 Authoring / Consolidation，不要求 Bootstrap 自动推断。

### 2.4 V1 Persistence

- Canonical persistence 继续使用当前 JSON Editor State。
- V1 不以 JSON → CSV persistence migration 为交付前提。
- JSON 的限制不阻塞 V1 产品闭环；批量 Authoring / 多 CSV 方案作为后续基础设施候选处理。

### 2.5 V1 Explicitly Out of Scope

V1 不承诺：

- 创建新的 Species identity；
- 初始化全新的 Fish Habit aggregate；
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

## 3. V1.1｜Authoring Efficiency

> Bake Preview / 条件组求值预览不属于 V1 承诺。是否在 V1.1 或更后阶段进入，以预览输入、基础权重、条件组来源与验收口径闭合为前提。



V1.1 的目标是提升生产效率，不改变 V1 已验证的 Authoring Truth 边界。

优先候选：

### 3.1 Multi-CSV Bulk Authoring

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

### 3.2 Authoring Efficiency Enhancements

可根据 V1 使用反馈进入：

- 更好的批量筛选 / Review；
- Template consolidation 辅助；
- 聚类 / Family 初始化研究（只作后续 Topology Creation 输入，不进入 V1 Shared Assets）；
- Golden Seed / migration tooling 的工程化增强。

V1.1 不默认等同于“正式创建新 Fish / 新 Mode”；是否进入 Topology Creation 以相关机制 Contract 是否闭合为准。

## 4. V1.2｜Topology Creation & Data Integration

这一阶段开始解决“新的鱼可以从 Editor 出生”。

### 4.1 Fish Habit Initialization

目标能力：

```text
已有 Species Catalog identity
→ 开始配置习性
→ Family / Preset 初始化
→ Species Base Authoring
```

不在 Habit Editor 中创建任意新的 Species identity；Species identity 仍来自 authoritative Species Catalog。

Family 的主要产品角色是：

> 为新 Fish 提供一组可编辑的初始 Habit Authoring 组合，而不是长期 parent relation。

### 4.2 Engagement Mode Creation

支持：

- 新建真正需要的 Engagement Mode；
- Mode identity / lifecycle；
- Mode 初始 Authoring state；
- Mode-level Habit / Policy authoring；
- Materializer 从 absent 创建所需 Habit production projection。

新 Fish 初始化时**不要求自动创建固定的 young / mature 两个 Mode**；用户按需要建立 Mode。

这一阶段开始前必须闭合：

- Mode identity；
- create / archive / delete lifecycle；
- FishEnvAffinity projection / naming / id 规则；
- row-level Policy 初始语义；
- Publish create-from-absent；
- Bootstrap / roundtrip symmetry。

### 4.3 External Ecological Data Integration

外部生态数据接入可在该阶段或之后进入，例如：

- 钓鱼元素周期表；
- Lux CLI；
- Temperature Species Concrete Import / Reimport；
- 外部数据 provenance；
- external-source failure / diff / candidate review。

这类能力不作为 V1 承诺。

### 4.4 Quality Boundary Remains

即使进入 Mode Creation：

- Habit Editor 仍不维护静态 `Mode → Quality` durable relation；
- Quality / stocking composition 继续属于 FishPond / StockRelease / FishRelease domain；
- 不因创建 Mode 把 Release topology 拉回 Habit Editor。

## 5. V1.3+｜Reconcile & Advanced Production Workflow

该阶段处理 Editor 之外发生的修改和更复杂的生产维护。

可能包括：

- Production external drift inspection；
- 显式 reconcile / import session；
- 对无法唯一恢复的作者意图进行人工 adjudication；
- legacy / externally edited production data 的 semantic recovery；
- 更成熟的 migration tooling；
- 若多 CSV 工作流已被验证，评估将其提升为 canonical persistence。

明确不以“自动双向同步”作为默认目标。

## 6. V2｜Full Engagement Mode / Routing

V2 处理真正动态的 Engagement Mode 体系。

可能包括：

- 正式 Engagement Mode identity；
- 基于 Species habit、scene、weather / environment 等因素的模式判断与分群；
- Routing / Share / context-dependent selection；
- Mode 与未来 evaluator / bake / runtime contract 的正式连接。

V1 的兼容 scope UI 不能被用来反推 V2 Routing 参数形态。

## 7. 版本切分原则

每次升级只有在新增能力能形成完整因果闭环时才进入上一版本承诺。

优先顺序：

1. **先闭合 Existing Topology Authoring；**
2. **再提升批量 Authoring / Persistence 效率；**
3. **再创建新的 Habit topology；**
4. **再接外部数据与 reconcile；**
5. **最后进入完整 Engagement Mode / Routing。**

不为了展示“功能多”而提前暴露没有 durable semantics 的按钮、占位字段或伪控件。

V1 Review 的核心问题应始终是：

> **在不依赖后续能力的情况下，一个作者能否安全地理解、修改、验证并发布已有 Fish Habit topology？**

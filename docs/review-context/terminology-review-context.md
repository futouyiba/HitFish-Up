# Terminology Review Context

> 用途：给 Codex / GPT Work / 独立 Review Agent 提供术语表检查所需的最小上下文。
> Review Target：`docs/terminology.md`
> 边界：本文不是机制 Authority，不替代各 Design Branch / Product Current / Runtime Contract；只汇总进行术语 Review 时必须知道的当前裁决与 Open 问题。

## 1. Review 目标

检查 `docs/terminology.md` 是否存在：

- 已使用但未定义的术语；
- 一词多义或多个词表达同一概念；
- 概念层级混淆；
- 定义之间的因果链断裂；
- 与本仓 supporting docs / system map 已承接语义冲突；
- 临时叙述词被误升格为正式 Domain identity。

不要自行重设计机制。发现机制未闭合时，标记 OPEN / 建议 Issue，不要在术语表里擅自写死 Contract。

## 2. Authority / Supersession 规则

术语 Review 时必须区分“当前裁决”和“历史讨论”。

- 本文件中明确列为“当前已确认”的 Owner 裁决，优先于 Issue / supporting docs 中更早、且未明确声明重新覆盖它的历史讨论。
- 如果旧 Issue 评论、旧 commit 或 supporting artifact 与当前已确认裁决冲突，应报告为 `STALE_TERM` / `STALE_PROJECTION`，不要把已经裁决的事项重新升级为 Owner Open。
- Issue 保持 OPEN 不代表 Issue 中所有问题都仍然 Open；应读取 Issue body 中的“已闭合 / 仍待 Contract 闭合”区分。
- 只有当当前裁决本身没有覆盖冲突点，或最新 Current / Working Authority 与本文件冲突时，才升级为 `CONTRACT_OPEN` / Owner 裁决。
- 对 Current-sensitive 机制问题，本文件仍不能替代 FCF Authority rebase。

## 3. 当前已确认的术语裁决

### 3.1 Mode / Species

- `Species` 是 `Engagement Mode` 的所属主体。
- `Mode Distribution` 的主体是 `Species`；不要引入额外的 `Subject / 鱼侧主体` Domain 概念。
- `Mode Weight` 是正式上位概念，贯穿基础、环境、圆桌等计算阶段；阶段表示“算到哪一步”，Mode 表示“权重属于哪个 Engagement Mode”。
- `Mode Distribution` 可以用于表达不同计算阶段下，同一 Species 的各 Engagement Mode 及其当前 Mode Weight 的整体分布。
- `Mode Distribution Entry` 是求值结果，不是长期业务身份。
- `Mode Base Intensity` 与基础阶段 `Mode Weight` 是否严格等价仍由 Contract 决定。
- Issue #131 中早期“移除 Mode Weight 独立术语”的记录已被后续 Owner 裁决覆盖，不再代表当前口径。

### 3.2 Fish Condition

- `鱼况（Fish Condition）` 即鱼侧动态参数。
- 当前使用：`Activity`、`Feeding Motivation`、`Diet Shift`、`Wariness`。
- `Wariness` 的中文为“警戒度”。
- `Fish Condition` 是否由 DEF 持久承载、如何更新和存储，仍是 Contract Open；不要从术语表反推存储所有权。

### 3.3 单因子评价

推荐最小语义：

```text
Condition
+ Environment Component
→ GateResult（若有 Gate）
→ Fit

多个 Fit
→ Aggregation
→ EnvCoeff
```

- `Affinity`：鱼侧静态偏好配置，不是运行时结果。
- `GateResult`：Gate 的离散结果。
- `Fit`：单组件连续评价结果。
- `EnvCoeff`：多个 Environment Component 聚合并经过 Gate / Background 规则后的整体环境倍率。
- “亲和系数”“因子结果”当前不作为正式术语，除非后续出现独立机制证据。

### 3.4 Background Fish

- `保底鱼（Background Fish）` 是钓场投鱼配置中的兜底供给职责。
- `envCoeffMin` 属于 Background 兜底路径。

### 3.5 分模式逻辑

- 分模式逻辑不是把鱼拆成多个长期鱼群实体。
- 同一 Species 的多个 Engagement Mode 可以分别计算并保留模式身份。
- `Cross-mode Aggregation` 处理同一 Species 下多个 Mode 结果之间的关系。
- `Factor Aggregation` 与 `Cross-mode Aggregation` 是不同层级：前者处理单个 Mode 内多因子结果，后者处理多个 Mode 结果。
- Cross-mode Aggregation 的发生阶段和算子仍由 Contract 决定。

### 3.6 Response

- Response 包含持续生效路径与即时路径；当前术语表使用 `Persistent Response` 与 `Pose Response`。
- `Response Condition` 是被 Response 直接消费的条件集合，分类轴首先按消费模块定义，来源只是属性。
- `Presentation Signal` 是描述当前玩家呈现状态的一类 Response 输入；它与 Response Condition 不是两个互斥的顶层分类。是否形成独立 Runtime interface 仍由 Contract 决定。
- `Fish Condition` 可被 Response 消费，因此不要把 `Response Condition` 定义锁死成“玩家侧来源”。
- `Response Component` 不默认复用 Environment 侧的 `Profile → Affinity → Fit` 内部结构。

### 3.7 Roundtable

- `Roundtable Weight List` / 圆桌权重表是响应之后、抽鱼前的候选权重集合。
- `Quality Share Adjustment`、`Hard Guarantee`、`Dynamic Weight Adjustment`、`Crowding-out` 当前只作为圆桌职责方向 / Working framework terms 使用。
- 除 `Crowding-out` 的相对竞争语义外，其余三者的作用位置、算子、输入和先后顺序不应由术语表写死。

## 4. 当前 Open Issues

- #131：`Mode Weight` 作为正式术语已闭合；仍需闭合 `Mode Base Intensity`、`SpatialDistributionWeight`、圆桌阶段 Mode identity、`Mode Distribution Entry` runtime 字段以及跨模式聚合阶段关系。
- #132：GateResult / Fit / Affinity / EnvCoeff 的术语边界；正文已基本投影。
- #133：Calculation Channel 与 Calculation Surface 的必要性和边界；Channel 是否具有稳定独立 I/O Contract 仍未闭合。在闭合前不要把 Channel 当作独立 Domain identity。

此外仍有以下 Contract Open：

- DEF 是否承载 `Fish Condition`，以及鱼况的所有权 / 更新生命周期；
- `Presentation Signal` 是否形成独立 Runtime interface；
- 圆桌四类职责的具体实现和顺序；
- `Base Weight`、`Base Opportunity Intensity`、`probWeightIdeal`、`baseOpportunityIntensity` 之间是否逐值等价。

## 5. Supporting Evidence

优先读取：

1. `docs/terminology.md`
2. FCF system map / source JSON 中与分模式、跨模式聚合、鱼侧动态参数相关的内容
3. 与当前任务直接相关的中层框架 / Contract 文档
4. GitHub Issues #131 / #132 / #133

如任务是 Current-sensitive 机制裁决，不应仅凭本文件或历史 commit；应按 FCF Authority 路径读取对应 Current / Working Authority。

## 6. Review 输出建议

将发现按以下类别输出：

- `MISSING_TERM`：正文或 supporting docs 使用，但术语表未定义；
- `DUPLICATE_TERM`：两个以上术语表达同一概念；
- `AMBIGUOUS_BOUNDARY`：定义存在，但边界与邻近概念不清；
- `CONTRACT_OPEN`：无法只靠术语层解决，需要机制 Contract 裁决；
- `STALE_TERM`：已被当前裁决替代但仍残留；
- `STALE_PROJECTION`：旧图示 / supporting artifact 仍投影已过时语义；
- `NO_ACTION`：只是具体字段 / Schema / 示例，不值得提升为核心术语。

每个 finding 都应指出证据位置，并区分“术语表可直接修”和“需要 Owner / Contract 决策”。
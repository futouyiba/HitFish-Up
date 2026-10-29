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

## 2. 当前已确认的术语裁决

### 2.1 Mode / Species

- `Species` 是 `Engagement Mode` 的所属主体。
- `Mode Distribution` 的主体是 `Species`；不要引入额外的 `Subject / 鱼侧主体` Domain 概念。
- `Mode Weight` 是上位概念，贯穿基础、环境、圆桌等计算阶段；阶段表示“算到哪一步”，Mode 表示“权重属于哪个 Engagement Mode”。
- `Mode Distribution` 可以跨阶段存在；它表示一个 Species 在当前上下文与计算阶段下，各 Engagement Mode 及其 Mode Weight 的整体分布。
- `Mode Distribution Entry` 是求值结果，不是长期业务身份。
- `Mode Base Intensity` 与基础阶段 `Mode Weight` 是否严格等价仍由 Contract 决定。

### 2.2 Fish Condition

- `鱼况（Fish Condition）` 即鱼侧动态参数。
- 当前使用：`Activity`、`Feeding Motivation`、`Diet Shift`、`Wariness`。
- `Wariness` 的中文为“警戒度”。

### 2.3 单因子评价

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

### 2.4 Background Fish

- `保底鱼（Background Fish）` 是钓场投鱼配置中的兜底供给职责。
- `envCoeffMin` 属于 Background 兜底路径。

### 2.5 分模式逻辑

- 分模式逻辑不是把鱼拆成多个长期鱼群实体。
- 同一 Species 的多个 Engagement Mode 可以分别计算并保留模式身份。
- `Cross-mode Aggregation` 处理同一 Species 下多个 Mode 结果之间的关系。
- `Factor Aggregation` 与 `Cross-mode Aggregation` 是不同层级：前者处理单个 Mode 内多因子结果，后者处理多个 Mode 结果。

### 2.6 Response

- Response 包含持续生效路径与即时路径；当前术语表使用 `Persistent Response` 与 `Pose Response`。
- `Fish Condition` 可被 Response 消费，因此不要把 `Response Condition` 定义锁死成“玩家侧来源”。分类轴应首先按消费模块定义，来源只是属性。
- `Response Component` 不默认复用 Environment 侧的 `Profile → Affinity → Fit` 内部结构。

## 3. 当前 Open Issues

- #131：Mode Weight 贯穿基础 / 环境 / 圆桌；仍需闭合 Mode Base Intensity、SpatialDistributionWeight、圆桌阶段 Mode identity 与跨模式聚合阶段关系。
- #132：GateResult / Fit / Affinity / EnvCoeff 的术语边界；正文已基本投影。
- #133：Calculation Channel 与 Calculation Surface 的必要性和边界；正文已有临时硬边界，但仍需验证 Channel 是否有稳定 Contract。

## 4. Supporting Evidence

优先读取：

1. `docs/terminology.md`
2. FCF system map / source JSON 中与分模式、跨模式聚合、鱼侧动态参数相关的内容
3. 与当前任务直接相关的中层框架 / Contract 文档
4. GitHub Issues #131 / #132 / #133

如任务是 Current-sensitive 机制裁决，不应仅凭本文件或历史 commit；应按 FCF Authority 路径读取对应 Current / Working Authority。

## 5. Review 输出建议

将发现按以下类别输出：

- `MISSING_TERM`：正文或 supporting docs 使用，但术语表未定义；
- `DUPLICATE_TERM`：两个以上术语表达同一概念；
- `AMBIGUOUS_BOUNDARY`：定义存在，但边界与邻近概念不清；
- `CONTRACT_OPEN`：无法只靠术语层解决，需要机制 Contract 裁决；
- `STALE_TERM`：已被当前裁决替代但仍残留；
- `NO_ACTION`：只是具体字段 / Schema / 示例，不值得提升为核心术语。

每个 finding 都应指出证据位置，并区分“术语表可直接修”和“需要 Owner / Contract 决策”。

# 中鱼升级｜术语表

> **状态：Working Terminology Ledger**  
> **范围：** 中鱼升级 / FCF 相关的跨模块命名收敛。  
> **权威边界：** 本文维护术语的推荐名称、定义、层级与禁止混淆项，**不自动替代各 Design Branch / Product Current / Runtime Contract 的现行 Authority**。当本文与 Current Contract 冲突时，以对应 Current Contract 为准，直到发生显式 Adoption / Migration。  
> **Notion 术语 Owner：** `中鱼升级｜Glossary / 术语表｜Working`。

本文只保留当前有用的术语状态，不记录完整推演历史。历史变化从 Git commit / diff 查询。

---

## 1. 命名原则

| 层 | 用途 |
|---|---|
| 业务 / 策划语言 | 人如何理解这个对象或机制 |
| 配置模型 | 编辑器实际编辑、继承、覆盖的对象（Authoring Model） |
| 解析模型 | 配置解析后的稳定投影（Resolved Model） |
| 运行 / 算法 | 游戏运行与算法求值时使用的语义（Runtime / Algorithm） |
| 物理数据结构 | XLSX / JSON / ID / 字段的历史或物理命名（Physical Schema） |
| 工作流 | Resolve / Validate / Publish 等数据流动作 |

原则：

- **中文必须是术语表中的主名称**；英文放在括号或独立英文列中。
- 业务概念名与历史物理表名允许不同，不为了命名纯洁性强制迁移稳定 Schema。
- 只有能独立变化、独立被引用、拥有独立生命周期的东西，才值得拥有独立 identity 名词。
- 不因为 UI grouping 方便就创建新的 Domain object。

---

## 2. 鱼与中鱼习性模式

| 中文正式名 | 英文 / Identifier | 定义 | 状态 / 边界 |
|---|---|---|---|
| 鱼种 | `Species` | 生物 / 内容层的鱼种身份，是习性、鱼品质和其它鱼侧配置的上层归属。 | 正式业务概念。 |
| 鱼品质 | `Fish Quality` / `FishQualityRef` | 长期既有的鱼品质身份。 | 保留既有名称；不因为小个体 / 大个体组织方式改名为 Fish Spec。 |
| 中鱼习性模式 | `Engagement Mode` | 同一鱼侧 Subject 下，为了表达不同中鱼行为而划分出的稳定模式。一个模式同时承接**数量份额**和该模式自己的**环境 / 响应习性配置**。 | 当前正式业务身份。 |
| 基础习性 | `Species Base` | 一个 Species 的默认中鱼习性模式。 | 物理上也是一条特殊 `FishEnvAffinity`；特殊性来自业务角色，而不是另一套生产对象类型。 |
| 习性档案 / 生产承载 | `FishEnvAffinity` / `FishEnvAffinityRef` | 当前 Production 中承载一套 Engagement Mode 的持久记录 / 引用。 | 历史 Schema 名保留。 |
| Bucket | `bucket` | 历史 / Editor 分组表达。 | 降级，不作为正式 Domain identity。 |

### 2.1 Fish Group 正式退役

**Fish Group / 鱼群组 / 分群对象：正式退役，不再作为当前业务身份。**

不要再建立：

```text
Fish Group
→ Engagement Mode
```

或：

```text
Fish Group
→ 一组参数 / 程序
```

当前统一表达为：

```text
FishQuality / Species Subject
        ↓ 模式路由 / 份额分配
Engagement Mode A ── 数量份额 + 环境习性 + 响应习性
Engagement Mode B ── 数量份额 + 环境习性 + 响应习性
...
```

因此原来“分群”的业务意图，后续统一理解为**分模式 / 模式分配**。

---

## 3. 模式划分与数量

### 3.1 模式路由

**模式路由（Engagement Mode Routing）**

定义：根据 FishQuality / Species、当前条件或其它明确输入，决定当前 Subject 应进入哪些 Engagement Mode，以及后续应如何进行模式份额分配。

它是**模式之间的分配逻辑**，不是 Engagement Mode 自身的内部习性。

### 3.2 模式份额

**模式份额（Engagement Mode Share）**

定义：某个 Subject 的基础权重中，分配给某个 Engagement Mode 的数量份额。

典型关系：

```text
基础权重
× 模式份额
→ 该模式的基础权重份额
```

如果同一 Subject 同时存在多个模式，模式份额负责回答：

> “这条鱼当前有多少属于这个行为模式？”

而 Environment / Response 负责回答：

> “这部分鱼在当前环境和玩家操作下，权重如何变化？”

模式份额是否必须严格归一到 `Σ share = 1`，由对应实现 Contract 决定；术语层不替算法提前规定。

### 3.3 模式贡献

**模式贡献（Mode Contribution）**

状态：Working。

定义：某个 Engagement Mode 经过数量份额、环境评价、响应评价等阶段后，对最终候选权重贡献的结果。

它是一个结果语义，不要求必须存在同名持久字段。

---

## 4. 中鱼习性组件

### 4.1 总类

**中鱼习性组件（Engagement Component）**

定义：一条 Engagement Mode 中，围绕一个相对独立的评价或响应语义组织的一组鱼侧配置。

`Component` 单独作为正式英文名过泛；正式总类使用 **Engagement Component**。在已经明确处于中鱼习性上下文时，可以简称 `Component`。

```text
中鱼习性组件 Engagement Component
├─ 环境习性组件 Environment Component
└─ 响应习性组件 Response Component
```

### 4.2 环境习性组件

**环境习性组件（Environment Component）**

定义：一条 Engagement Mode 针对某个环境 Factor 的完整鱼侧评价配置。

当前已存在 / 已讨论的环境 Factor / Component 包括：

- 水温（Temperature）
- 结构类型（Structure Type）
- 觅食生态水层（Feeding Layer）
- 时段（Period）
- 遮蔽物类型（Cover Type）
- 底质类型（Substrate Type）
- 光照 / 水流 / 溶氧（Light / Flow / Oxygen，候选扩展）

### 4.3 响应习性组件

**响应习性组件（Response Component）**

定义：一条 Engagement Mode 针对玩家输入、饵料、窝料、呈现方式或其它刺激的独立响应配置单元。

当前只确认它与 Environment Component 同属 Engagement Component；**不要提前强迫 Response 复用 Environment 的 `Profile → Affinity → Fit` 内部数学结构**。

候选响应语义可以包括：

- 饵料 / 窝料刺激；
- 味型 / 气味 / 食物信号；
- 呈现方式（Presentation）；
- 操作速度、姿态、距离等玩家输入；
- 其它后续明确进入 Response 的刺激维度。

---

## 5. 世界对象、条件与因子

### 5.1 环境实体

**环境实体（Environment Entity）**

场景中实际存在、具有位置 / 形态并可参与环境计算的对象。

例：水草、树桩、沉木、孤立巨石、桥墩、码头构件，以及用于表达地形结构的场景对象。

环境实体首先是**条件数据来源**：它提供类型、位置、形态、尺寸、材质等原始条件。

### 5.2 条件

| 中文正式名 | 英文 | 定义 | 示例 |
|---|---|---|---|
| 原始条件 | `Raw Condition` | 直接编辑、采样或由世界状态提供的事实。 | 实体类型、位置、形态、地形高度、材质、天气 |
| 派生条件 | `Derived Condition` | 从原始条件或其它派生条件确定性计算得到的事实。 | 水深、距 Structure、Cover 密度、光照、局部流速、溶氧 |

### 5.3 因子

**因子（Factor）**

定义：对鱼而言具有独立评价语义、可独立产生评价结果的评价维度。

当前明确：

- 结构类型（Structure Type）是 Factor；
- 遮蔽物类型（Cover Type）是 Factor；
- 底质类型（Substrate Type）是 Factor。

世界侧的 Structure / Cover 实体、地形或材质数据不是 Factor 本身，它们主要提供条件数据。

```text
Environment Entity / Terrain / Material
        ↓
Raw Condition
        ↓
Derived Condition（需要时）
        ↓
Factor Input / Value
        ↕
Environment Component
        ↓
Fit
```

判别法：

> **Entity 是世界里有什么；Condition 是当前事实是什么；Factor 是鱼评价什么；Environment Component 是这条 Engagement Mode 怎么评价它。**

### 5.4 Structure / Cover / Substrate 的世界侧对应

| 中文对象 / 特征 | 世界侧表示 | 对应鱼侧 Factor |
|---|---|---|
| 岬角（Point） | Structure 相关地形 / 几何 | Structure Type |
| 水下隆起（Hump） | Structure 相关地形 / 几何 | Structure Type |
| 陡坎（Drop-off） | Structure 相关地形 / 几何 | Structure Type |
| 台坎（Ledge） | Structure 相关地形 / 几何 | Structure Type |
| 沟槽（Channel） | Structure 相关地形 / 几何 | Structure Type |
| 平坦区（Flat） | Structure 相关地形 / 几何 | Structure Type |
| 水草（Weed） | Environment Entity | Cover Type |
| 灌木（Brush） | Environment Entity | Cover Type |
| 树桩（Stump） | Environment Entity | Cover Type |
| 倒木（Laydown） | Environment Entity | Cover Type |
| 码头（Dock） | Environment Entity / 场景构筑物 | Cover Type |
| 孤立巨石（Boulder） | Environment Entity | 通常 Cover Type |
| 岩脊（Rock reef） | Structure 相关地形 / 几何 | Structure Type |
| 沙 / 砾石 / 泥（Sand / Gravel / Mud） | Surface / Material Property | Substrate Type |

---

## 6. 环境评价与权重

### 6.1 亲和度、适配值与环境系数

| 中文正式名 | 英文 / Identifier | 定义 |
|---|---|---|
| 亲和度 | `Affinity` | 鱼自身静态配置中，对某个离散环境项的偏好值。 |
| 适配值 | `Fit` | 把当前条件代入某个环境习性组件后得到的单组件评价结果。 |
| 环境系数 | `EnvCoeff` | 多个环境习性组件评价结果聚合后的整体环境倍率。 |

`Affinity` 是配置，`Fit` 是单组件评价结果，`EnvCoeff` 是多个环境结果聚合后的倍率。

### 6.2 基础权重 / 基础机会强度

**基础权重（Base Weight）**  
同义业务名：**基础机会强度（Base Opportunity Intensity）**  
既有字段：`baseOpportunityIntensity`

定义：在环境影响介入之前，某鱼侧 Subject 的基础数量 / 机会量级。

当前术语层将“基础权重”和“基础机会强度”视为同一概念的两个名称；中文讨论优先使用**基础权重**。

### 6.3 环境权重 / 空间分布强度 / 空间分布权重

**环境权重（Environment Weight）**  
同义业务名：**空间分布强度（Spatial Distribution Intensity）**  
既有输出名：**空间分布权重（Spatial Distribution Weight / `SpatialDistributionWeight`）**

定义：基础权重经过环境评价及其明确拥有的环境策略修正后得到的**未归一化权重**。

当前把这三个名称视为同一个层级的业务 / 输出语义：

```text
基础权重
× 环境系数
× 该阶段明确拥有的环境策略项
→ 环境权重
  = 空间分布强度
  = 空间分布权重
```

它不是 Probability。

### 6.4 退役：空间机会 / 空间机会强度

以下术语不再作为当前推荐术语：

- `Spatial Opportunity / 空间机会`
- `Spatial Opportunity Intensity / 空间机会强度`

历史文档中若出现，按其原版本语义阅读；新文档、新 Schema、新讨论不要继续引入。

---

## 7. 响应阶段

### 7.1 响应阶段

**响应阶段（Response Stage）**

定义：在已经得到当前模式的环境权重之后，根据玩家操作、饵料 / 窝料、呈现方式以及其它当前响应输入，评价这部分鱼对当前刺激的响应程度。

基本边界：

```text
环境权重
+ Engagement Mode 的响应习性
+ 当前玩家 / 刺激输入
→ Response
→ 后续候选权重
```

Response **消费已经形成的环境结果，不重新计算环境权重**。

### 7.2 响应系数

**响应系数（Response Coefficient）**

状态：Working，优先作为当前响应输出的业务名。

定义：响应阶段产生的倍率，用来表达当前 Engagement Mode 对玩家本次刺激 / 呈现的响应强弱。

典型链路：

```text
环境权重
× 响应系数
→ 响应后的候选权重
```

历史设计中出现过 `ResponseWeight`、`ResponseGrade` 等表达；在当前 Response 设计正式闭合前，不把这些旧名恢复成正式 Contract。

### 7.3 呈现信号

**呈现信号（Presentation Signal / Presentation）**

状态：Working。

定义：玩家如何把饵 / 钓组呈现给鱼的当前输入，例如速度、姿态、深度、距离、运动方式等。

它属于 Response 输入，不属于鱼自身的长期身份。

### 7.4 鱼侧动态状态

**鱼侧动态状态（Fish Condition / Fish Condition Snapshot）**

状态：历史设计中已出现，当前是否保留统一 Snapshot 身份待重新闭合。

曾讨论过的内容包括：

- 活跃度（Activity）；
- 摄食动机（Feeding Motivation）；
- 当前摄食偏好（Feeding Preference）；
- 其它会被 Response 消费的动态鱼情。

术语表暂时只登记这一类信息，不把 `FishConditionSnapshot` 强制恢复成正式 Runtime object。

---

## 8. 计算域

**计算域（Calculation Surface）**

定义：一套配置、角色或规则所作用的**计算问题范围**。它回答“这个配置在哪一类计算里生效”，不是“数据从哪条通道流过”。

因此不推荐翻译为“计算通道”。`Channel / Pipeline` 更适合描述数据流路径。

当前可用的计算域包括：

- **环境权重计算域（Environment Weight Surface）**：回答当前模式在当前环境中的权重如何形成；
- **响应计算域（Response Surface）**：回答当前模式面对玩家刺激时如何调整权重。

`AggregationRole` 必须放在具体计算域中理解，不是全局属性。

---

## 9. 配置、策略与 Gate

### 9.1 习性配置

**习性配置（Profile）**

定义：一个 Engagement Component 中真正描述“这个 Factor / Response 语义如何偏好、如何响应”的结构化配置内容。

边界：

- Engagement Component 是配置单元；
- Profile 是组件内部主要配置内容；
- Source 可以提供 Profile；
- `Profile absent` 表示当前没有可消费 Profile，不等于整个 Component 不存在。

### 9.2 门槛判定

**门槛判定（Gate）**

定义：在连续评分 / 权重聚合之前或之外，对某项条件是否满足最低要求进行的离散判定。

Gate 回答“能不能正常通过”；Fit / EnvCoeff 回答“通过后有多适合”。

### 9.3 Gate 失败环境系数

**Gate 失败环境系数（`fail_env_coeff`）**

定义：普通 Gate fail 路径下使用的环境系数。

### 9.4 保底鱼与最小环境系数

**保底鱼（Background Fish）**

状态：Working。

它不是 Species / FishQuality 的固有身份，而是某个钓场配置下赋予某 FishQuality 的背景供给角色。

相关字段：

```text
FishPond × FishQualityRef
├─ baseOpportunityIntensity
├─ isBackgroundFish
└─ envCoeffMin
```

**最小环境系数（`envCoeffMin`）**：Background 兜底路径下的最低环境系数值。

是否需要独立的 `GatePolicy / BackgroundPolicy` Domain object，等实际出现独立配置、复用和生命周期后再决定。

---

## 10. 已确认的既有机制术语

| 中文正式名 | 英文 / Identifier | 定义 / 边界 |
|---|---|---|
| 觅食生态水层 | `Feeding Layer` | 描述鱼在表层 / 中层 / 底层觅食空间上的习性。 |
| 结构类型 | `Structure Type` | 鱼侧环境评价 Factor；世界侧 Structure 实体 / 地形几何只提供条件数据。 |
| 遮蔽物类型 | `Cover Type` | 鱼侧环境评价 Factor；世界侧 Cover 实体提供条件数据。 |
| 底质类型 | `Substrate Type` | 鱼侧环境评价 Factor；世界侧材质 / 区域数据提供条件数据。 |
| 时段 | `Period` | 一天中的时间区段。 |
| 聚合角色 | `AggregationRole` | 某个 Engagement Component 在某个计算域中采用的聚合角色。枚举可为 `CORE / SECONDARY / IGNORED`。 |
| 忽略 | `IGNORED` | 当前计算域不消费该组件；不表示鱼没有该习性，也不删除其 Profile。 |
| 环境条件组 | `ConditionGroup` | 一组可共同求值的环境条件组合 / 等价类。 |
| 固定烘焙程序 / 固定烘焙逻辑 | `Fixed Bake Program` | 系统拥有的固定多组件聚合流程；Author 不编辑其控制流、顺序或聚合算子。当前为工作命名。 |

---

## 11. 配置与工作流术语

| 中文 | 英文 | 定义 |
|---|---|---|
| 配方 | `Recipe` | 描述一个 Authoring 对象如何由 Source + Operations 形成的表达。 |
| 来源 | `Source` | 为 Component / Profile 提供原始配置值的上游来源。 |
| 操作 | `Operation` | 在 Source value 上表达继承、调整或设置等作者意图的操作。 |
| 解析 | `Resolve` | Source + Operations + overrides → effective resolved truth。 |
| 物化 | `Materialize` | effective truth → 完整 Production rows。 |
| 校验 | `Validate` | 对 Authoring / Resolved / Production 约束进行检查。 |
| 发布 | `Publish` | 将通过发布条件的结果写入 Production。 |
| 烘焙 | `Bake` | resolved fish config + environment facts → 环境评价输出。 |

`flatten` 只作实现描述，不作为独立业务阶段；`compile` 只有在未来出现真正独立阶段时再引入。

---

## 12. 当前需要继续推敲

1. Response Component 的最终输入、内部配置和输出是否使用统一的 Response Coefficient，以及是否还需要 Grade / Band 等离散层。
2. 模式份额的具体 Contract：是否必须归一、由什么上下文决定、何时 Resolve。
3. `Factor` 是否只用于 Environment，还是未来 Response 也有自己的 Factor；当前不强行统一。
4. `Structure Type / Cover Type / Substrate Type` 的 Runtime 输入形式：单一枚举、集合、权重分布，还是由距离 / 密度等 Derived Condition 共同决定。
5. `FishConditionSnapshot` 是否需要恢复成正式统一对象，还是继续保持若干独立动态状态。
6. `Fixed Bake Program` 是否足够直观，仍可继续替换。
7. 更底层的 Resolved / Runtime 名称只有在当前 Contract 重新取证后才进入正式术语区。

---

## 13. 维护规则

- 新文档不得重新引入已经退役的 `Fish Group` 作为业务身份。
- 新文档不得使用 `Spatial Opportunity / Spatial Opportunity Intensity` 作为当前推荐术语。
- “分群”如仅表示把鱼权重拆成不同行为部分，应改写为**分模式 / 模式分配 / 模式路由**。
- “基础权重”与“基础机会强度”是同一概念；中文讨论优先使用“基础权重”。
- “环境权重 / 空间分布强度 / 空间分布权重”指同一层级的未归一化环境结果；不要再额外插入“空间机会强度”。
- 不因为某个模块先实现，就强迫后续模块复制其内部数学结构。
- 每次新增 / 改名时，至少检查：定义、Owner、Scope、输入、输出、与相邻概念的禁止混淆项。
- 本文是术语收敛面，不替代 Current Contract；要进入机制 Authority，必须在对应分支中显式 Adoption。

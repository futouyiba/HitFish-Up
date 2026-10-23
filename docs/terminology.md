# 中鱼升级｜术语表

> **状态：Working Terminology Ledger**  
> **范围：** 中鱼升级 / FCF 相关的当前术语。  
> **权威边界：** 本文维护当前推荐术语、定义与边界，不自动替代各 Design Branch / Product Current / Runtime Contract 的现行 Authority。

本文只描述当前可用语义。术语演进、旧名称和调整原因由 Git commit / diff 承载。

---

## 1. 核心对象

| 中文正式名 | 英文 / Identifier | 定义 |
|---|---|---|
| 鱼种 | `Species` | 鱼种本身的稳定定义。包含名称、体长—体重关系、可用中鱼习性模式等鱼种级数据。 |
| 鱼品质 | `Fish Quality` / `FishQualityRef` | 既有的鱼品质身份，用于表达同一鱼种下的品质 / 个体规格差异。 |
| 中鱼习性模式 | `Engagement Mode` | 某鱼种可复用的一套中鱼习性定义，描述这类鱼在环境和玩家刺激下如何表现。可包含模式自身的基础强度，以及环境习性、响应习性等配置。 |
| 基础习性 | `Species Base` | 一个 Species 的默认中鱼习性模式。当前 Production 中由一条特殊 `FishEnvAffinity` 承载。 |
| 习性档案 | `FishEnvAffinity` / `FishEnvAffinityRef` | 当前 Production 中承载 Engagement Mode 的持久记录 / 引用。 |
| 投鱼条目 | `Stocking Entry` | 某钓场中对一种鱼 / Fish Quality 的投放配置。负责表达这条鱼在该钓场中的基础权重及相关钓场级配置。 |

推荐关系：

```text
Species
├─ Species Base
└─ Engagement Mode(s)
   ├─ Mode Base Intensity
   ├─ Environment Components
   └─ Response Components

Pond
└─ Stocking Entry
   ├─ Fish / FishQuality reference
   └─ BaseWeight
```

判别：

> **Species 说明鱼是什么；Engagement Mode 说明鱼怎么表现；Stocking Entry 说明这个钓场投了什么、投多少。**

---

## 2. 中鱼习性组件

### 2.1 中鱼习性组件

**中鱼习性组件（Engagement Component）**

定义：一条 Engagement Mode 中，围绕一个相对独立的评价或响应语义组织的一组鱼侧配置。

```text
中鱼习性组件 Engagement Component
├─ 环境习性组件 Environment Component
└─ 响应习性组件 Response Component
```

### 2.2 环境习性组件

**环境习性组件（Environment Component）**

定义：一条 Engagement Mode 针对某个环境 Factor 的完整鱼侧评价配置。

典型环境 Factor：

- 水温（Temperature）
- 结构类型（Structure Type）
- 遮蔽物类型（Cover Type）
- 底质类型（Substrate Type）
- 觅食生态水层（Feeding Layer）
- 时段（Period）
- 光照（Light）
- 水流（Flow）
- 溶氧（Oxygen）

### 2.3 响应习性组件

**响应习性组件（Response Component）**

定义：一条 Engagement Mode 针对玩家输入、饵料、窝料、呈现方式或其它刺激的独立响应配置单元。

Response 的内部配置与求值结构不默认复用 Environment 的 `Profile → Affinity → Fit` 结构。

---

## 3. 世界对象、条件与因子

### 3.1 环境实体

**环境实体（Environment Entity）**

世界中实际存在、具有位置 / 形态并可参与环境计算的对象。

例：水草、石块、沉木、树桩、桥墩、码头构件。

环境实体主要提供类型、位置、形态、尺寸、材质等原始条件数据。

### 3.2 条件

| 中文正式名 | 英文 | 定义 | 示例 |
|---|---|---|---|
| 原始条件 | `Raw Condition` | 直接编辑、采样或由世界状态提供的事实。 | 实体类型、位置、形态、地形高度、材质、天气 |
| 派生条件 | `Derived Condition` | 从原始条件或其它派生条件确定性计算得到的事实。 | 水深、距 Structure、Cover 密度、光照、局部流速、溶氧 |

### 3.3 因子

**因子（Factor）**

定义：对鱼而言具有独立评价语义、可独立产生评价结果的评价维度。

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

判别：

> **Entity 是世界里有什么；Condition 是当前事实是什么；Factor 是鱼评价什么；Environment Component 是这条 Engagement Mode 怎么评价它。**

### 3.4 Structure / Cover / Substrate

| 中文对象 / 特征 | 世界侧表示 | 对应鱼侧 Factor |
|---|---|---|
| 岬角（Point） | 地形 / 几何 | Structure Type |
| 水下隆起（Hump） | 地形 / 几何 | Structure Type |
| 陡坎（Drop-off） | 地形 / 几何 | Structure Type |
| 台坎（Ledge） | 地形 / 几何 | Structure Type |
| 沟槽（Channel） | 地形 / 几何 | Structure Type |
| 平坦区（Flat） | 地形 / 几何 | Structure Type |
| 水草（Weed） | Environment Entity | Cover Type |
| 灌木（Brush） | Environment Entity | Cover Type |
| 树桩（Stump） | Environment Entity | Cover Type |
| 倒木（Laydown） | Environment Entity | Cover Type |
| 码头（Dock） | Environment Entity / 场景构筑物 | Cover Type |
| 孤立巨石（Boulder） | Environment Entity | Cover Type |
| 岩脊（Rock reef） | 地形 / 几何 | Structure Type |
| 沙 / 砾石 / 泥（Sand / Gravel / Mud） | Surface / Material Property | Substrate Type |

---

## 4. 环境评价

| 中文正式名 | 英文 / Identifier | 定义 |
|---|---|---|
| 习性配置 | `Profile` | 一个 Engagement Component 内用于描述偏好 / 响应规则的结构化配置。 |
| 亲和度 | `Affinity` | 鱼侧静态配置中，对某个离散环境项的偏好值。 |
| 适配值 | `Fit` | 当前条件代入某个环境习性组件后得到的单组件评价结果。 |
| 环境系数 | `EnvCoeff` | 多个环境习性组件评价结果聚合后的整体环境倍率。 |
| 门槛判定 | `Gate` | 对某项条件是否满足最低要求进行的离散判定。 |
| 聚合角色 | `AggregationRole` | 某环境习性组件在环境权重计算中的角色。当前使用 `CORE / SECONDARY / IGNORED`。 |
| 忽略 | `IGNORED` | 当前环境权重计算不消费该组件；不表示组件数据不存在。 |
| Gate 失败环境系数 | `fail_env_coeff` | 普通 Gate fail 路径下使用的环境系数。 |
| 最小环境系数 | `envCoeffMin` | Background 兜底路径下使用的最低环境系数。 |
| 环境条件组 | `ConditionGroup` | 一组可以共同求值的环境条件组合 / 等价类。 |

---

## 5. 权重与模式分布

### 5.1 基础权重

**基础权重（Base Weight）**

定义：在环境影响介入之前，某投鱼条目的基础数量 / 中鱼机会量级。

当前对应：

| 名称 | Identifier |
|---|---|
| 基础权重 | `Base Weight` |
| 基础机会强度 | `Base Opportunity Intensity` |
| 配表字段 | `probWeightIdeal` |
| 既有机制字段 | `baseOpportunityIntensity` |

### 5.2 空间分布权重

**空间分布权重（Spatial Distribution Weight）**  
Identifier：`SpatialDistributionWeight`

业务上也可称**环境权重**。

定义：基础权重经过环境评价后得到的未归一化权重。

当前核心关系：

```text
BaseWeight × EnvCoeff
→ SpatialDistributionWeight
```

即：

```text
基础权重 × 环境系数
→ 空间分布权重
```

`SpatialDistributionWeight` 不是 Probability；只有与其它候选项共同归一化 / 抽样后，才进入概率意义上的结果。

### 5.3 模式基础强度

**模式基础强度（Mode Base Intensity）**

定义：配置在 Engagement Mode 上的基础强度，用作该模式在当前上下文中参与权重计算的起始量。

环境条件、鱼况以及后续响应逻辑可以在各自阶段影响该模式最终参与计算的权重；具体求值公式由对应 Contract 定义。

### 5.4 模式权重

**模式权重（Mode Weight）**

定义：某个 Engagement Mode 在当前求值上下文下计算得到的权重。

它是一个计算结果，不代表一个新的鱼群实体。

### 5.5 模式分布

**模式分布（Mode Distribution）**

定义：在某个具体求值上下文中，同一鱼侧 Subject 的各个 Engagement Mode 及其模式权重组成的整体分布。

示例：

```text
模式分布 Mode Distribution
├─ 小个体模式 → 300
├─ 大个体模式 → 100
└─ 其它模式   → 50
```

模式分布可以在后续阶段被归一化或继续参与其它权重计算；是否以及何时归一化由对应 Contract 决定。

### 5.6 模式分布条目

**模式分布条目（Mode Distribution Entry）**

定义：模式分布中的单个条目，表达某个 Engagement Mode 在当前上下文中的模式权重。

最小语义：

```text
Mode Distribution Entry
├─ EngagementModeRef
└─ ModeWeight
```

模式分布条目是运行 / 求值结果，不是独立长期业务身份。

---

## 6. 鱼况

**鱼况（Fish Condition）**

定义：随天气、时段及其它动态输入变化的一组鱼侧动态参数，用于描述鱼在当前时刻的活跃、摄食与疲劳等情况，并作为后续 Response 等计算的基础输入。

鱼况及鱼侧动态参数当前包括：

| 中文 | 英文 / Identifier | 说明 |
|---|---|---|
| 活跃度 | `Activity` | 当前整体活跃程度；除参与 Response 外，也可向刺鱼、搏鱼等后续模块提供输入。 |
| 摄食动机 | `Feeding Motivation` | 当前摄食意愿 / 驱动力。 |
| 食性偏移 | `Diet Shift` | 当前相对于基础食性的动态偏移。 |
| 疲劳 / 警觉累积 | `Weariness` | 随过程变化、会影响后续响应的疲劳或警觉性量。 |

基本关系：

```text
天气 / 时段 / 其它动态输入
        ↓
      鱼况 Fish Condition
        ↓
     Response 计算
        ↓
后续中鱼、刺鱼、搏鱼等模块
```

`Fish Condition` 是一个鱼侧动态信息集合；具体参数的更新公式、时间粒度与下游消费关系由对应机制 Contract 定义。

---

## 7. 响应阶段

### 7.1 响应阶段

**响应阶段（Response Stage）**

定义：在环境权重形成之后，根据 Engagement Mode 的响应习性、当前鱼况以及玩家 / 刺激输入，对候选权重进行后续调整。

```text
SpatialDistributionWeight
+ Fish Condition
+ Response Components
+ current stimulus / presentation
→ response evaluation
→ downstream candidate weight
```

### 7.2 响应系数

**响应系数（Response Coefficient）**

定义：响应阶段产生的倍率，用于表达当前 Engagement Mode 对本次玩家刺激 / 呈现的响应强弱。

当前可表达为：

```text
SpatialDistributionWeight × ResponseCoeff
→ downstream candidate weight
```

### 7.3 呈现信号

**呈现信号（Presentation Signal）**

定义：玩家如何把饵 / 钓组呈现给鱼的当前输入，例如速度、姿态、深度、距离、运动方式等。

---

## 8. 计算域

**计算域（Calculation Surface）**

定义：一套配置、角色或规则所作用的计算问题范围。

它回答：

> **“这个配置在哪一类计算中生效？”**

当前主要包括：

- **环境权重计算域（Environment Weight Surface）**
- **响应计算域（Response Surface）**

计算域不是数据传输通道，也不是 Pipeline。

---

## 9. 配置与工作流

| 中文 | 英文 | 定义 |
|---|---|---|
| 配方 | `Recipe` | 描述一个配置对象如何由 Source + Operations 形成。 |
| 来源 | `Source` | 为 Component / Profile 提供原始配置值的上游来源。 |
| 操作 | `Operation` | 在 Source value 上表达继承、调整或设置等作者意图的操作。 |
| 解析 | `Resolve` | Source + Operations + overrides → effective resolved truth。 |
| 物化 | `Materialize` | effective truth → 完整 Production rows。 |
| 校验 | `Validate` | 对 Authoring / Resolved / Production 约束进行检查。 |
| 发布 | `Publish` | 将通过发布条件的结果写入 Production。 |
| 烘焙 | `Bake` | resolved fish config + environment facts → 环境评价输出。 |

---

## 10. 维护规则

- 中文是主名称，英文放在括号或独立英文列中。
- 本文只描述当前状态，不记录术语演进史。
- 旧名称、删除项、rename 原因和决策过程由 Git history 承载。
- 业务名、Authoring 名、Runtime 名、Physical Schema 名允许不同，不强求逐字一致。
- 只有能独立变化、独立被引用、拥有独立生命周期的东西，才建立独立 Domain identity。
- 不因为 UI grouping 方便就创建新的 Domain object。
- 不因为某个模块先实现，就强迫后续模块复用它的内部数学结构。

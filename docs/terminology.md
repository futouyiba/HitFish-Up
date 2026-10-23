# 中鱼升级｜Terminology / 术语表

> **Status: Working Terminology Ledger**  
> **Scope:** 中鱼升级 / FCF 相关的跨模块命名收敛。  
> **Authority boundary:** 本文维护术语的推荐名称、定义、层级与禁止混淆项，**不自动替代各 Design Branch / Product Current / Runtime Contract 的现行 Authority**。当本文与 Current Contract 冲突时，以对应 Current Contract 为准，直到发生显式 Adoption / Migration。  
> **Notion terminology owner:** `中鱼升级｜Glossary / 术语表｜Working`。

本文只保留当前有用的术语状态，不记录完整推演历史。历史变化从 Git commit / diff 查询。

---

## 1. 命名分层

| 层 | 用途 |
|---|---|
| 业务 / 策划语言 | 人如何理解这个对象或机制 |
| Authoring Model | 编辑器实际编辑、继承、覆盖的对象 |
| Resolved Model | Authoring 解析后的稳定投影 |
| Runtime / Algorithm | 游戏运行与算法求值时使用的语义 |
| Physical Schema | XLSX / JSON / ID / 字段的历史或物理命名 |
| Workflow | Resolve / Validate / Publish 等数据流动作 |

原则：**业务概念名与历史物理表名允许不同。不要为了命名纯洁性强制迁移稳定 Schema。**

---

## 2. 鱼与中鱼习性身份

| 中文正式名 | English / Identifier | 定义 | 状态 / 边界 |
|---|---|---|---|
| 鱼种 | `Species` | 生物 / 内容层的鱼种身份，是习性、鱼品质和其它鱼侧配置的上层归属。 | 正式业务概念。 |
| 鱼品质 | `Fish Quality` / `FishQualityRef` | 长期既有的鱼品质身份。 | **保留既有名称**；不因为当前小个体 / 大个体组织方式改名为 Fish Spec。 |
| 中鱼习性模式 | `Engagement Mode` | 同一 Species 下的一套完整、稳定的中鱼习性配置。 | 业务 / UI 正式名。当前 Production 直接由一条 `FishEnvAffinity` 记录承载。 |
| 基础习性 | `Species Base` | 一个 Species 的默认中鱼习性模式。 | **物理上也是一条特殊 `FishEnvAffinity`**；特殊性来自业务角色，而不是另一套生产对象类型。 |
| 习性档案 / 生产承载 | `FishEnvAffinity` / `FishEnvAffinityRef` | 当前 Production 中承载一套 Engagement Mode 的持久记录 / 引用。 | 历史 Schema 名保留；不要把这里的 `Affinity` 误解成下文单值 `Affinity`。 |
| Bucket | `bucket` | 历史 / Editor 分组表达。 | **降级，不作为正式 Domain identity**。若只是多个 Fish Quality 共用同一模式，用 `FishQualityRef → FishEnvAffinityRef` 直接表达。 |

当前推荐关系：

```text
Species
├─ Species Base
│  └─ one special FishEnvAffinity
└─ Engagement Mode(s)
   └─ one FishEnvAffinity per mode

FishQualityRef
        ↓ assignment
FishEnvAffinityRef
```

当前没有必要为了表达“小个体 / 大个体”再增加一层 Bucket identity；它们可以是当前 Engagement Mode 的作者侧名称。

---

## 3. 中鱼习性组件

### 3.1 总类

**中鱼习性组件｜Engagement Component**

定义：一条 Engagement Mode 中，围绕一个相对独立的评价或响应语义组织的一组鱼侧配置。

`Component` 单独作为正式英文名过泛；完整英文使用 **Engagement Component**。在上下文足够明确时，代码 / 文档内部可以简称 `Component`。

```text
Engagement Mode
├─ Environment Components
└─ Response Components
```

### 3.2 环境习性组件

**环境习性组件｜Environment Component**

定义：一条 Engagement Mode 针对某个环境 Factor 的完整鱼侧评价配置。

当前已存在 / 已讨论的环境 Factor / Component 包括：

- Temperature
- Structure Type
- Feeding Layer
- Period
- Cover Type（候选扩展）
- Substrate Type（候选扩展）
- Light / Flow / Oxygen（候选扩展）

其中 `Structure Type / Cover Type / Substrate Type` 明确属于鱼侧评价的 **Factor**；对应的世界实体、地形与材质数据主要负责提供 Raw Condition，必要时再解析为 Derived Condition。

不要把“环境习性组件”当成所有 Engagement Component 的总称。

### 3.3 响应习性组件

**响应习性组件｜Response Component**

定义：一条 Engagement Mode 针对外部刺激、饵料、呈现方式等响应语义的鱼侧配置单元。

> Response 还未闭合。当前只确认它与 Environment Component 同属 Engagement Component；**不要提前强迫 Response 复用 Environment 的 `Profile → Affinity → Fit` 内部数学结构**。

---

## 4. 世界对象与环境条件来源

### 4.1 环境实体

**环境实体｜Environment Entity**

场景中实际存在、具有位置 / 形态并可参与环境计算的对象。

例：水草、树桩、沉木、孤立巨石、桥墩、码头构件，以及用于表达地形结构的场景对象。

环境实体首先是**条件数据来源**：它提供类型、位置、形态、尺寸、材质等 Raw Condition；是否以及如何被归纳成某个 Factor 的当前值，是后续条件处理 / 求值层的责任。

`Spatial Environment Entity` 信息增益不足，且容易与 Spatial Opportunity 混淆，因此不推荐作为正式名。

### 4.2 Structure / Cover / Substrate 的世界侧表达

世界侧可以存在承担不同环境语义的实体或几何 / 材质数据，例如：

- **Structure 相关实体 / 地形几何**：岬角、陡坎、台坎、沟槽、水下隆起等；
- **Cover 相关实体**：水草、倒木、树桩、孤立巨石、码头等；
- **Substrate 数据**：Sand / Gravel / Mud 等水底材质或区域属性。

这些世界侧对象 / 数据**不是 Factor 本身**。它们主要提供 Raw Condition；条件处理层再根据当前评价位置、范围或采样规则形成可用于鱼侧评价的数据。

因此：

```text
Structure Entity / Terrain Geometry
Cover Entity
Substrate Material / Region
        ↓ provide
Raw Condition
        ↓ optional derivation
Derived Condition
        ↓ evaluated as
Structure Type / Cover Type / Substrate Type Factor
```

### 4.3 典型分类

| 候选 | 世界侧表示 | 对应鱼侧 Factor |
|---|---|---|
| Point / 岬角 | Structure 相关地形 / 几何 | Structure Type |
| Hump / 水下隆起 | Structure 相关地形 / 几何 | Structure Type |
| Drop-off / 陡坎 | Structure 相关地形 / 几何 | Structure Type |
| Ledge / 台坎 | Structure 相关地形 / 几何 | Structure Type |
| Channel / 沟槽 | Structure 相关地形 / 几何 | Structure Type |
| Flat / 平坦区 | Structure 相关地形 / 几何 | Structure Type |
| Weed / 水草 | Environment Entity | Cover Type |
| Brush / 灌木 | Environment Entity | Cover Type |
| Stump / 树桩 | Environment Entity | Cover Type |
| Laydown / 倒木 | Environment Entity | Cover Type |
| Dock / 码头 | Environment Entity / 场景构筑物 | Cover Type |
| Boulder / 孤立巨石 | Environment Entity | 通常 Cover Type |
| Rock reef / 岩脊 | Structure 相关地形 / 几何 | Structure Type |
| Sand / Gravel / Mud | Surface / Material Property | Substrate Type |

这里的关键边界是：**世界侧分类描述数据从哪里来；Factor 描述鱼在评价什么。**

---

## 5. Condition、Factor 与求值

| 中文正式名 | English / Identifier | 定义 | 禁止混淆 |
|---|---|---|---|
| 原始条件 | `Raw Condition` | 直接编辑、采样或由世界状态提供的事实。 | 例：实体类型、位置、形态、地形高度、材质、天气。主要由世界对象 / 环境系统提供。 |
| 派生条件 | `Derived Condition` | 从 Raw Condition 或其它 Derived Condition 确定性计算得到的环境事实。 | 例：水深、距 Structure、Cover 密度、局部光照、流速、溶氧。 |
| 因子 | `Factor` | 对鱼而言具有独立评价语义、可独立产生评价结果的环境评价维度。 | `Structure Type / Cover Type / Substrate Type` 都属于 Factor；不要把世界实体或每个 Raw 字段直接等同于 Factor。 |
| 亲和度 | `Affinity` | 鱼自身静态配置中，对某个离散环境项的偏好值。 | 与当前条件求值得到的 `Fit` 不同。 |
| 适配值 | `Fit` | 把当前条件代入某个环境习性配置后得到的单组件求值结果。 | `Affinity` 是配置；`Fit` 是求值结果。 |
| 环境系数 | `EnvCoeff` | 多个环境组件求值结果经过聚合后，对结果施加的整体环境倍率。 | 位于单组件 Fit 与最终 Weight 之间。 |
| 环境条件组 | `ConditionGroup` | 一组可共同求值的环境条件组合 / 等价类。 | 不是 Environment Entity，也不是 EnvironmentSnapshot，也不要求对应连续空间区域。 |

推荐因果链：

```text
Environment Entity / Terrain / Material
        ↓
Raw Condition
        ↓
Derived Condition (when needed)
        ↓
Factor Value / Factor Input
        ↕ evaluated by
Environment Component
        ↓
Fit
        ↓ aggregate
EnvCoeff
```

判别法：

> **Entity 是世界里有什么；Condition 是当前事实是什么；Factor 是鱼评价什么；Environment Component 是这条 Engagement Mode 怎么评价它。**

例如：

```text
水草实体
  ↓ 提供
类型 / 位置 / 范围等 Raw Conditions
  ↓ 条件处理
当前点的 Cover Type / Cover 密度等评价输入
  ↓
Cover Type Factor
  ↕
该 Engagement Mode 的 Cover Environment Component
  ↓
Cover Fit
```

---

## 6. 已确认的既有机制术语

| 中文正式名 | English / Identifier | 定义 / 边界 |
|---|---|---|
| 觅食生态水层 | `Feeding Layer` | 描述鱼在表层 / 中层 / 底层觅食空间上的习性。暂不改为 `Foraging Layer`。 |
| 结构类型 | `Structure Type` | 鱼侧环境评价 Factor：评价当前位置 / 条件对应的地形结构类型。世界侧 Structure 实体 / 地形几何只负责提供其条件数据。 |
| 遮蔽物类型 | `Cover Type` | 鱼侧环境评价 Factor：评价当前位置 / 条件对应的遮蔽物类型。世界侧 Cover 实体负责提供原始条件数据。 |
| 底质类型 | `Substrate Type` | 鱼侧环境评价 Factor：评价当前位置 / 条件对应的水底基质类型。世界侧材质 / 区域数据负责提供原始条件数据。 |
| 时段 | `Period` | 一天中的时间区段，本身不预设 Activity 或 Opportunity ownership。 |
| 聚合角色 | `AggregationRole` | 某个 Engagement Component 在某个 Calculation Surface 中采用的聚合角色。枚举可为 `CORE / SECONDARY / IGNORED`。 |
| 忽略 | `IGNORED` | 当前 Calculation Surface 不消费该 Component；不表示鱼没有该习性，也不删除其 Profile。 |
| 最小环境系数 | `envCoeffMin` / Min Env Coeff | 保底政策下的最低环境系数值。字段名保留，不另造 `BackgroundMinEnvCoeff`。 |
| 空间分布权重 | `SpatialDistributionWeight` | 环境与基础权重合成后的未归一化空间分布权重；不是 Probability。 |
| 固定烘焙程序 / 固定烘焙逻辑 | `Fixed Bake Program` | 系统拥有的固定多组件聚合流程；Author 不编辑其控制流、顺序或聚合算子。当前为工作命名。 |

---

## 7. Opportunity / Background（Working）

**保底鱼｜Background Fish** 目前仍是工作术语。

推荐边界：它不是 Species / FishQuality 的固有身份，而是某个钓场 / Opportunity 配置下赋予某 FishQuality 的稳定背景供给角色。

```text
FishPond × FishQualityRef
├─ baseOpportunityIntensity
├─ isBackgroundFish
└─ envCoeffMin?    # when background
```

因此同一个鱼种 / Fish Quality 可以在一个钓场是 Background Fish，在另一个钓场不是。

---

## 8. Authoring / Workflow 术语

| 中文 | English | 定义 |
|---|---|---|
| 配方 | `Recipe` | 描述一个 Authoring 对象如何由 Source + Operations 形成的表达。Base 是对象，Recipe 是形成方式。 |
| 解析 | `Resolve` | Source + Operations + overrides → effective resolved truth。 |
| 物化 | `Materialize` | effective truth → 完整 Production rows。 |
| 校验 | `Validate` | 对 Authoring / Resolved / Production 约束进行检查。 |
| 发布 | `Publish` | 将通过发布条件的结果写入 Production。 |
| 烘焙 | `Bake` | resolved fish config + environment facts → 目标计算输出。 |

`flatten` 只作实现描述，不作为独立业务阶段；`compile` 只有在未来出现真正独立阶段时再引入。

---

## 9. 当前需要继续推敲

1. `Factor` 是否作为 Environment / Response 共用总概念，还是明确拆成 `Environmental Factor` 等子类。
2. Response Component 的输入、内部配置和输出是否复用 `Profile / Affinity / Fit`，目前不预设。
3. `Structure Type / Cover Type / Substrate Type` 的具体 Runtime 输入形式：是单一枚举、集合、权重分布，还是由距离 / 密度等 Derived Condition 共同决定；术语层暂不预设。
4. `Background Fish` 的英文是否最终保留，还是未来改成更偏 Policy 的名称。
5. `Fixed Bake Program` 是否足够直观，仍可继续替换。

---

## 10. 维护规则

- 只在出现真实语义冲突时改名；稳定既有术语优先保留。
- 业务名、Authoring 名、Runtime 名、Physical Schema 名允许不同，不强求逐字一致。
- 只有能独立变化、独立被引用、拥有独立生命周期的东西，才值得拥有独立 identity 名词。
- 不因为 UI grouping 方便就创建新的 Domain object。
- 不因为某个模块先实现，就强迫后续模块复制其内部数学结构。
- 每次新增 / 改名时，至少检查：定义、Owner、Scope、输入、输出、与相邻概念的禁止混淆项。
- 本文是术语收敛面，不替代 Current Contract；要进入机制 Authority，必须在对应分支中显式 Adoption。

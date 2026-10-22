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

当前已存在 / 已讨论的环境组件包括：

- Temperature
- Structure
- Feeding Layer
- Period
- Cover（候选扩展）
- Substrate（候选扩展）
- Light / Flow / Oxygen（候选扩展）

不要把“环境习性组件”当成所有 Engagement Component 的总称。

### 3.3 响应习性组件

**响应习性组件｜Response Component**

定义：一条 Engagement Mode 针对外部刺激、饵料、呈现方式等响应语义的鱼侧配置单元。

> Response 还未闭合。当前只确认它与 Environment Component 同属 Engagement Component；**不要提前强迫 Response 复用 Environment 的 `Profile → Affinity → Fit` 内部数学结构**。

---

## 4. 世界、环境事实与钓鱼环境语义

### 4.1 环境实体

**环境实体｜Environment Entity**

场景中实际存在、具有位置 / 形态并可影响环境计算的对象。

例：水草、树桩、沉木、孤立巨石、桥墩、码头构件。

`Spatial Environment Entity` 信息增益不足，且容易与 Spatial Opportunity 混淆，因此不推荐作为正式名。

### 4.2 地形结构

**地形结构｜Structure**

水体底部地形、轮廓、深度变化相对周围形成的结构性特征。

典型：

- Point / 岬角
- Hump / 水下隆起
- Drop-off / 陡坎
- Ledge / 台坎
- Channel / 沟槽
- Flat / 平坦区
- Rock reef / 岩脊（当其形成明显底部轮廓时）

Structure 主要描述**底部 contour / terrain semantic**，不是所有可以藏鱼的物体。

### 4.3 遮蔽物

**遮蔽物｜Cover**

为鱼提供贴靠、隐藏、伏击、遮光或避流条件的对象或区域语义。

典型：

- Weed / 水草
- Brush / 灌木
- Stump / 树桩
- Laydown / 倒木
- Dock / 码头
- Boulder / 孤立巨石（通常）

同一个 Environment Entity 可以同时影响多个环境语义。例如一片水草既可以形成 Cover，也可以影响 Light / Flow / Oxygen。

### 4.4 底质

**底质｜Substrate**

水底表层材料 / 基质语义。

典型：

- Sand
- Gravel
- Mud

Substrate 不属于 Structure 或 Cover。世界里存在 Substrate，也**不代表它必须立即成为中鱼 Factor**。

### 4.5 世界表示与钓鱼语义是两条轴

不要用单一分类列把 `Environment Entity` 与 `Structure / Cover / Substrate` 混在一起。

| 候选 | 世界表示 | 钓鱼环境语义 |
|---|---|---|
| Point / 岬角 | 地形 / 几何特征 | Structure |
| Hump / 水下隆起 | 地形 / 几何特征 | Structure |
| Drop-off / 陡坎 | 地形 / 几何特征 | Structure |
| Ledge / 台坎 | 地形 / 几何特征 | Structure |
| Channel / 沟槽 | 地形 / 几何特征 | Structure |
| Flat / 平坦区 | 地形 / 几何特征 | Structure |
| Weed / 水草 | Environment Entity | Cover；也可影响 Light / Flow / Oxygen |
| Brush / 灌木 | Environment Entity | Cover |
| Stump / 树桩 | Environment Entity | Cover |
| Laydown / 倒木 | Environment Entity | Cover |
| Dock / 码头 | Environment Entity / 场景构筑物 | Cover |
| Boulder / 孤立巨石 | Environment Entity | 通常 Cover |
| Rock reef / 岩脊 | 地形 / 几何特征 | Structure |
| Sand / Gravel / Mud | Surface / Material Property | Substrate |

---

## 5. Condition、Factor 与求值

| 中文正式名 | English / Identifier | 定义 | 禁止混淆 |
|---|---|---|---|
| 原始条件 | `Raw Condition` | 直接编辑、采样或由世界状态给出的事实。 | 例：实体类型 / 位置、地形高度、天气。 |
| 派生条件 | `Derived Condition` | 从 Raw Condition 或其它 Derived Condition 计算得到的环境事实。 | 例：水深、遮蔽度、局部光照、流速、溶氧。 |
| 因子 | `Factor` | 在一次鱼侧评价中具有独立语义、可独立产生评价结果的评价维度。 | 不要把每个原始字段都升格为 Factor。 |
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
Derived Condition
        ↓
Factor
        ↕ evaluated by
Environment Component
        ↓
Fit
        ↓ aggregate
EnvCoeff
```

`Structure / Cover / Substrate` 属于环境领域语义层，帮助组织 Condition / Factor；不要机械要求它们都直接对应一个 Runtime Condition。

---

## 6. 已确认的既有机制术语

| 中文正式名 | English / Identifier | 定义 / 边界 |
|---|---|---|
| 觅食生态水层 | `Feeding Layer` | 描述鱼在表层 / 中层 / 底层觅食空间上的习性。暂不改为 `Foraging Layer`。 |
| 结构类型 | `Structure Type` | 既有中鱼配置中的结构类别术语。后续如果正式拆分 Structure 与 Cover，需要单独做 Schema / migration 判断，不能仅凭术语表静默改义。 |
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
3. 既有 `Structure Type` 是否历史上混合了 Structure 与 Cover；如要拆分，需要独立设计 / migration，而不是术语替换。
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

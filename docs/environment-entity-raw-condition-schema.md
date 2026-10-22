# 中鱼升级｜Environment Entity Raw Condition Schema

> **Status:** Working Design / Review Candidate  
> **Authority:** NONE. 本文用于整理 Environment Entity 的 Raw Condition 设计，不替代 Notion `Population / Spatial Current Contract`、Project Current 或其它 Semantic Owner。  
> **Version:** 0.1  
> **Last Updated:** 2026-10-22（Asia/Taipei）  
> **Related:** `docs/terminology.md`、`docs/fish-habit-editor-v1/common-semantics.md`

## 1. 结论

Environment Entity 不应该再拥有一套重复描述场景几何的业务字段。

推荐的数据边界是：

```text
Unity GameObject + Components
├─ Transform / Hierarchy
├─ Mesh / Renderer / Collider
└─ 其它场景原生信息
        ↓ 自动读取
Unity Scene-native Raw Facts

EnvironmentEntity semantic component
└─ 只补 Unity 场景本身无法可靠表达、但 Environment Resolver 确实需要的稀疏语义 Trait
        ↓
Entity Semantic Raw Conditions

Scene-native Raw Facts
+ Entity Semantic Raw Conditions
+ Terrain / Water / Weather 等其它 World Raw Conditions
        ↓
Environment Resolver
        ↓
Derived Conditions
├─ Cover
├─ Light / Shade
├─ Local Flow / Flow Shelter / Turbulence
├─ Oxygen
├─ Depth / Submergence
└─ ...
        ↓
Fish-side Factor / Environment Component
```

因此：

- **位置、旋转、缩放**不应在 Environment Entity 数据里再配一份；Unity `Transform` 已经拥有。
- **形状、尺寸、包围范围、占据空间**优先从 `Mesh / Renderer / Collider` 读取或计算，不重复 author。
- **Volume 不是 GameObject 的一个通用原生字段**，但可由附着的几何 / Collider 计算或用 Bounds 近似；它仍属于 Unity 场景可提取事实，而不是策划重复配置字段。
- 只有 **类型、亚分辨率密度 / 孔隙率、复杂度、柔性、透光性、生命周期状态**等无法从场景几何可靠推出的属性，才考虑进入额外 Raw Condition。
- `CoverStrength`、`LightCoeff`、`FlowCoeff`、`OxygenCoeff`、鱼类亲和度等都不是 Entity Raw Condition。

Unity 官方语义：`Transform` 保存 GameObject 的 Position / Rotation / Scale / parent state；`Bounds` 被 `Collider.bounds`、`Mesh.bounds`、`Renderer.bounds` 使用。参考：

- <https://docs.unity3d.com/6000.0/Documentation/Manual/class-Transform.html>
- <https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Bounds.html>
- <https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Renderer-bounds.html>

---

## 2. Raw Condition 的四个来源层

| 来源层 | 是否属于 Raw Condition | 是否人工配置 | 示例 |
|---|---:|---:|---|
| **Unity Scene-native Facts** | 是 | 否，自动提取 | Position、Rotation、Scale、Hierarchy、Mesh、Collider、Bounds、Footprint、Height、Volume proxy |
| **Entity Semantic Raw Conditions** | 是 | 是，但应稀疏 | EntityType、Vegetation GrowthForm、Patch Density、Porosity、DecayState、LightTransmittance |
| **Other World Raw Conditions** | 是 | 由其它 World System 提供 | Terrain、Water Level、基础流场、天气、时段、温度、浊度 |
| **Derived Conditions** | 否 | 不直接配置 | Cover、Shade、局部流速、避流程度、湍流、溶氧、水深、浸没比例 |

关键规则：**Raw / Derived 描述数据来源，不描述重要性，也不要求只有两层计算。Derived Condition 可以继续参与其它 Derived Condition 的计算。**

---

## 3. Unity 已经拥有的数据：明确标注，不重复配置

| 数据 | Unity 来源 | 在 Environment Entity 中如何处理 | 备注 |
|---|---|---|---|
| Position | `Transform` | **自动读取** | 不新增 `position` 配置字段 |
| Rotation / Orientation | `Transform` | **自动读取** | 流场计算可直接使用世界朝向 |
| Scale | `Transform` | **自动读取** | 与 Mesh / Collider 共同决定实际尺寸 |
| Parent / Child hierarchy | `Transform` hierarchy | **自动读取** | 适合表达 Dock / Bridge 等 Composite Entity |
| Mesh geometry | `MeshFilter / Mesh` | **自动读取** | 用于真实形状、表面积、局部尺度等 |
| Render bounds | `Renderer.bounds` | **自动读取 / 粗略 proxy** | 世界空间 AABB；适合快速空间筛选，不等价真实体积 |
| Collision geometry | `Collider` | **自动读取** | 对 Solid obstacle 通常比渲染 Mesh 更适合作为空间 proxy |
| Collider bounds | `Collider.bounds` | **自动读取 / 粗略 proxy** | 世界空间包围体积 |
| Width / Height / Length | Geometry / Bounds | **自动派生** | 不重复 author |
| Footprint | Geometry 投影 | **自动派生** | 可用于水草 patch、平台等 |
| Volume | Mesh / Collider / Bounds | **自动计算或近似** | 不是 GameObject 通用字段；不要策划再填一个 volume |
| Height above bed | Geometry + Terrain | **Derived** | 不属于 Entity 自身固定 Raw Field |
| Submerged fraction | Geometry + Water Level | **Derived** | 水位变化时会变化 |
| Surface clearance | Geometry + Water Surface | **Derived** | 码头 / 浮台下方净空不应手工复制位置关系 |
| Distance to other entity / Structure | Spatial query | **Derived** | 不属于 Entity Raw |

### 3.1 Material 要谨慎

Unity `Renderer Material` 是渲染资源，不自动等价于环境领域的物理 / 生态材质。

例如一个视觉上使用同一材质的石头 Prefab，不代表 Environment Resolver 可以从 Shader Material 推出：

- 水动力粗糙度；
- 孔隙率；
- 透光率；
- 腐朽程度；
- 生物活性。

只有当项目明确建立了 `Unity Material → Environment Semantic Property` 的稳定映射，才能自动消费；否则需要独立语义 Trait。

---

## 4. 不建议做「每类实体一套完整 Schema」

更稳的模型是：

```text
EnvironmentEntity
├─ EntityType
└─ sparse Traits[]
```

即：所有实体共享 Unity-native geometry，只有需要补充的信息才挂 Trait。

这样可以避免：

```text
Vegetation.position
Boulder.position
Pier.position
Woody.position
...
```

以及避免每个实体都拥有一套互相漂移的：

```text
coverCoeff
lightCoeff
flowCoeff
oxygenCoeff
```

后者应该由统一 Environment Resolver 根据 Raw Cause 推导。

---

## 5. 各类 Environment Entity：具体需要哪些初始数据

### 5.1 Aquatic Vegetation｜水生植被 / 水草 Patch

水生植被是最需要额外语义数据的一类，因为一个 GameObject 往往不是逐片叶子建模，而是一个 **patch / aggregate proxy**。

| 数据 | 来源 | 推荐级别 | 说明 |
|---|---|---|---|
| Position / Rotation / Scale | Unity Transform | 自动 | 不配置 |
| Geometry / Bounds / Footprint / Height | Mesh / Collider | 自动 | 不配置 |
| `EntityType = Vegetation` | Semantic | **必需** | 表明该对象参与植被 Resolver |
| `GrowthForm` | Semantic | **推荐** | `Submerged / Emergent / Floating / FloatingLeaf` 等；决定占据水柱方式 |
| `PatchDensity` | Semantic | **条件必需** | 当 GameObject 只是 patch 外包络而没有逐株几何时，需要描述内部密度 |
| `Porosity` | Semantic | 推荐 / 可与 Density tying | 描述水 / 光穿透空间；若能由 Density + archetype 稳定派生，不应成为第二个自由 DOF |
| `StructuralComplexity` | Semantic | Working | 枝叶复杂度；只在 Cover 表达确实无法由 Geometry + Density 买到时引入 |
| `Flexibility` | Semantic | Future / conditional | 只有需要表达强流倒伏、动态阻流差异时才购买 |
| `GrowthState / Phenology` | Semantic / state | Future / conditional | 只有生长 / 枯萎会在玩法时间尺度变化时需要 |
| `BiomassProxy` | Semantic | Future | 只有 Oxygen / biological process 真正建模时需要 |

**不直接配置：**

```text
CoverStrength
LightOcclusionCoeff
FlowReductionCoeff
OxygenBonus
```

建议因果链：

```text
Geometry + GrowthForm + Density (+ Porosity / Complexity when admitted)
→ Cover
→ Light / Shade
→ Local Flow

Biomass / GrowthState + Light + Temperature + Water Exchange ...
→ Oxygen consequence
```

### 5.2 Boulder / Isolated Rock｜孤立巨石 / 石块

这是最应该依赖 Unity Geometry 的类型之一。

| 数据 | 来源 | 推荐级别 | 说明 |
|---|---|---|---|
| Position / Orientation / Size / Shape | Transform + Collider / Mesh | 自动 | 不配置 |
| `EntityType = Boulder` | Semantic | **必需** | 领域身份 |
| `Embeddedness` | Geometry + Terrain 或 Semantic | Conditional | 若能可靠从 Terrain intersection 求出就自动派生；否则才 author |
| `SurfaceRoughness` | Semantic | Future | 只有水动力模型证明需要时才加入 |
| `HydroProxyShape` | Approximation metadata | Future | 只有 Resolver 不直接消费 Collider / Mesh，而使用简化 shape class 时需要；它是近似代理，不是新的世界 Truth |

**默认不需要**人为配置 Boulder 的 Cover 或 Flow 数值。应由：

```text
Collider / Mesh geometry
+ Terrain relationship
+ current flow
→ Cover geometry / wake / shelter / turbulence
```

### 5.3 Stump｜树桩

树桩与巨石类似，若 Mesh / Collider 足够表达真实形态，额外字段应很少。

| 数据 | 来源 | 推荐级别 | 说明 |
|---|---|---|---|
| Geometry / Position / Height / Diameter | Unity | 自动 | 不配置 |
| `EntityType = Woody` | Semantic | 必需 | 木质环境实体 |
| `WoodySubtype = Stump` | Semantic | 推荐 | 区分 stump / log / laydown / brush |
| `RootwadPresent` | Geometry 或 Semantic | Conditional | 若根盘有独立 child geometry 可自动；否则可做语义标记 |
| `DecayState` | Semantic | Future | 只有腐朽状态会改变结构/生态效果时需要 |

### 5.4 Laydown / Fallen Tree / Log｜倒树 / 沉木 / 原木

这里真正难以从外包围盒推出的是内部枝杈复杂度。

| 数据 | 来源 | 推荐级别 | 说明 |
|---|---|---|---|
| Position / Length / Diameter / Orientation | Unity geometry | 自动 | 不重复配置 |
| `EntityType = Woody` | Semantic | 必需 | 领域身份 |
| `WoodySubtype` | Semantic | 推荐 | `Log / Laydown / Rootwad` |
| `BranchComplexity` | Semantic | **条件推荐** | 当 Mesh 是低细节 proxy、无法体现枝杈可藏身结构时需要 |
| `Porosity` | Semantic | Conditional | 当 envelope geometry 无法表达内部开孔时需要；优先与 Complexity / archetype tying |
| `DecayState` | Semantic | Future | 只有对结构效果有实际 Consumer 时引入 |
| `AnchoringState` | Semantic / state | Future | 只有实体可能移动 / 漂浮时需要 |

### 5.5 Brush / Brush Pile｜灌木 / 枝条堆

Brush 本质上是一个 **高复杂度、多孔 aggregate object**。

| 数据 | 来源 | 推荐级别 | 说明 |
|---|---|---|---|
| Position / outer geometry / footprint | Unity | 自动 | 不配置 |
| `EntityType = Woody / Brush` | Semantic | 必需 | 身份 |
| `PatchDensity` 或 `Porosity` | Semantic | **推荐** | 二选一作为主 Raw Cause；不要默认两个都成为自由 DOF |
| `StructuralComplexity` | Semantic | Conditional | 只有密度不足以区分“直枝束”和“复杂枝杈堆”时才增加 |
| `DecayState` | Semantic | Future | 同上 |

### 5.6 Pier / Pile｜桥墩 / 桩柱

桥墩是典型的 **Geometry-first** 实体。

| 数据 | 来源 | 推荐级别 | 说明 |
|---|---|---|---|
| Position / Rotation / Width / Length / Cross-section | Unity Collider / Mesh | 自动 | 核心水动力输入应直接使用这些事实 |
| Vertical extent | Unity Geometry | 自动 | 不配置 |
| Group layout / spacing | GameObject hierarchy + transforms | 自动 | 多桩阵列从 child layout 获取 |
| `EntityType = Pier / Pile` | Semantic | 必需 | 身份 |
| `HydroProxyShape` | Approximation metadata | Conditional | 仅当实际 Resolver 使用 cylinder / rectangle 等简化模型时需要 |
| `SurfaceRoughness` | Semantic | Future | 只有模型确实敏感时加入 |

**不直接配置：**

```text
FlowObstruction
WakeStrength
TurbulenceStrength
FishCover
```

应该是：

```text
Pier geometry + current flow field + water depth
→ local flow / wake / shelter / turbulence
```

### 5.7 Dock / Platform / Bridge Deck｜码头平台 / 桥面 / 浮台

这类对象建议作为 **Composite Entity**，而不是一个大字段对象。

```text
Dock GameObject
├─ Deck / Platform
├─ Pile 01
├─ Pile 02
└─ Pile 03
```

Deck / Platform 自身：

| 数据 | 来源 | 推荐级别 | 说明 |
|---|---|---|---|
| Footprint / elevation / thickness | Unity Geometry | 自动 | 不配置 |
| Clearance above water | Geometry + Water Level | Derived | 不手填 |
| `EntityType = Platform` | Semantic | 必需 | 身份 |
| `LightTransmittance` | Semantic | **推荐 / conditional** | 实心板、栅格板、半透明表面仅靠外形无法区分透光性 |

Pile 子对象按上一节处理。

由此：

```text
Deck geometry + LightTransmittance + sun / sky condition
→ Shade / Light

Piles + flow field
→ Flow disturbance / local shelter

组合后的空间关系
→ Cover geometry
```

### 5.8 Artificial Reef / Wreck / Complex Structure｜人工鱼礁 / 沉船 / 复杂人工遮蔽物

这类对象如果使用完整 Collider / interior geometry，可以高度依赖 Unity；若只用粗代理，则需要少量亚分辨率 Trait。

| 数据 | 来源 | 推荐级别 | 说明 |
|---|---|---|---|
| Outer / internal geometry | Unity | 自动优先 | 最佳来源 |
| `EntityType` | Semantic | 必需 | Reef / Wreck / ArtificialCover |
| `Porosity` | Semantic | Conditional | 粗 proxy 时描述内部空隙 |
| `InternalAccessibility` | Semantic | Future | 只有鱼是否可进入内部空间产生独立玩法时需要 |
| `StructuralComplexity` | Semantic | Conditional | 只有 Geometry 无法表达时需要 |

---

## 6. 推荐的稀疏 Trait 集合

与其给每类 Entity 建独立表，不如维护一个小型、可 admission 的 Trait vocabulary。

| Trait | 解决什么几何表达不了的问题 | 典型实体 | 默认状态 |
|---|---|---|---|
| `EntityType` | 领域身份 / Resolver dispatch | 所有 Environment Entity | **Required** |
| `Subtype` | 同类实体的重要语义分型 | Woody / Vegetation / Artificial | Recommended where useful |
| `GrowthForm` | 水生植物如何占据水柱 | Vegetation | Recommended |
| `PatchDensity` | aggregate patch 内部并未真实建模的密度 | Vegetation / Brush | Conditional Required |
| `Porosity` | aggregate envelope 内部开放水空间 | Vegetation / Brush / Reef | Conditional；优先与 Density tying |
| `StructuralComplexity` | 同密度下的枝杈 / 孔洞结构差异 | Woody / Brush / Reef | Working / admit only if needed |
| `Flexibility` | 几何会随水流形变 | Vegetation | Future |
| `Embeddedness` | 物体实际暴露程度无法稳定从 Terrain 求出 | Boulder / Woody | Conditional |
| `LightTransmittance` | 外形相同但透光能力不同 | Platform / Vegetation proxy | Conditional |
| `DecayState` | 木质结构随腐朽变化 | Woody | Future |
| `GrowthState` | 植物随生长 / 枯萎变化 | Vegetation | Future |
| `BiomassProxy` | 生物过程不能由 Geometry 推出 | Vegetation | Future; only if Oxygen modeled |
| `HydroProxyShape` | 运行时不消费真实 Mesh 时的简化水动力形状 | Pier / Boulder | Approximation metadata only |

### Trait Admission Rule

新增 Trait 前至少回答：

1. Unity Transform / Mesh / Collider / hierarchy 能不能直接得到？
2. 能不能由已有 Raw Condition 确定性派生？
3. 它是否真的改变某个 Derived Condition，而不是只增加描述完整度？
4. 它是否与已有 Trait 高度相关，可以 archetype / tying，而不新增独立 DOF？
5. 它是否有明确 Consumer、Resolver 和验证方式？

无法通过则默认不加。

---

## 7. 一个重要区分：真实 Geometry vs Aggregate Proxy

同一个实体类型，是否需要额外 Raw Condition，取决于场景表示精度。

### Case A：Geometry 已真实表达

```text
一棵倒树：主干 + 大枝条都有 Collider / Mesh
```

这时：

- Length、diameter、orientation、branch distribution 都可以从 Scene 取得；
- `BranchComplexity` 可能完全不需要配置。

### Case B：GameObject 是一个抽象 Patch / Envelope

```text
一片水草：只有一个 10m × 8m × 2m 的 Box / proxy volume
```

这个 Box 只告诉系统“范围有多大”，没有告诉系统里面是：

- 10% 稀疏水草；
- 80% 密草；
- 直立茎；
- 高度复杂的枝叶。

因此 `PatchDensity / GrowthForm / Porosity` 才成为合理的 Raw Condition。

**结论：很多额外 Entity 参数，本质上不是现实世界又多了一个属性，而是在补偿 Scene Representation 的信息压缩。**

这类参数应该明确标记为 `representation semantic / proxy metadata`，防止未来把它误读成必须与 Unity Geometry 并存的第二份 Truth。

---

## 8. 哪些东西明确不属于 Environment Entity Raw Data

| 数据 | 正确归属 |
|---|---|
| Point / Hump / Drop-off / Channel / Flat | Terrain / Bathymetry → `Structure` semantic |
| Sand / Gravel / Mud | Substrate / surface field |
| Water Level | Water / World State |
| Ambient Flow | Hydrodynamic / Water Field |
| Weather / Period | World / Schedule |
| Temperature | Environment Field |
| Turbidity | Water Condition |
| 当前水深 | Terrain + Water Level → Derived Condition |
| Cover | Entity / Terrain facts → Derived environment semantic / condition |
| Light / Shade | Scene + weather + entities → Derived Condition |
| Local Flow / Shelter / Turbulence | base flow + entity geometry → Derived Condition |
| Oxygen | biological + physical context → Derived Condition |
| Structure affinity | Fish-side Environment Component |
| Cover affinity | Fish-side Environment Component |
| Environment Fit / EnvCoeff | Fish-side evaluation result |

因此不要出现：

```text
EnvironmentEntity
├ coverCoeff
├ lightCoeff
├ flowCoeff
├ oxygenCoeff
└ fishAffinity
```

这会把 World Truth、Derived Condition 和 Fish Response 三层重新揉回一个对象。

---

## 9. 推荐的 Unity 侧概念结构

概念上建议类似：

```text
GameObject
├─ Transform                     # Unity-owned
├─ Mesh / Renderer / Collider    # Unity-owned
├─ child GameObjects             # Unity-owned hierarchy
└─ EnvironmentEntity             # 中鱼环境语义标记
   ├─ entityType
   └─ sparse traits
      ├─ growthForm?
      ├─ density?
      ├─ porosity?
      ├─ complexity?
      ├─ embeddedness?
      ├─ lightTransmittance?
      └─ ...
```

这里的 `EnvironmentEntity` **不是另一份 geometry database**。

它的职责只是：

> 给 Unity 已经存在的世界对象补上 Environment Resolver 无法从普通 GameObject Components 可靠知道的领域语义。

---

## 10. V0 / First Implementation 建议

如果现在就要实现，我不建议一次加入上面所有 Trait。

第一版可以只购买：

| Entity | V0 额外 Raw Condition |
|---|---|
| Vegetation Patch | `EntityType`、`GrowthForm`、`PatchDensity`（仅 aggregate proxy） |
| Boulder | `EntityType`；`Embeddedness` 仅在无法自动求出时 |
| Stump | `EntityType`、`WoodySubtype` |
| Laydown / Log | `EntityType`、`WoodySubtype`、`BranchComplexity`（仅 coarse proxy） |
| Brush | `EntityType`、`PatchDensity` 或 `Porosity` 二选一 |
| Pier / Pile | `EntityType` |
| Platform / Dock Deck | `EntityType`、`LightTransmittance`（非完全 opaque 时） |
| Artificial Reef / Wreck | `EntityType`、`Porosity`（仅 coarse proxy） |

其余全部先从 Unity Scene / World Context 自动取得或留到后续 admission。

这使第一版真正需要人工 author 的参数非常少，同时保留了以后扩张 Light / Flow / Oxygen / Cover resolver 的语义接口。

---

## 11. 当前需要继续验证的问题

1. 当前关卡里的水草 / 沉木 / 石块实际是高精度 Mesh、Collider，还是大量使用 Box / Volume proxy？这直接决定 `Density / Porosity / Complexity` 的必要程度。
2. Terrain / Water Level / Flow Field 当前各自由什么生产数据提供，能否稳定查询 GameObject 与底床 / 水面的关系？
3. Cover Resolver 是否计划直接使用 Collider geometry，还是只使用离散 Entity Type / proximity？若后者，必须明确哪些几何信息会在 projection 中损失。
4. Light / Flow / Oxygen 哪些是真正近期要进入 Authoring / Bake 的 Derived Condition；未进入消费链的 Trait 不应提前生产。
5. 现有“Structure Type”数据里哪些其实是 Environment Entity / Cover，后续需要单独做 schema migration；本文不静默重定义已有 Production 字段。

---

## 12. 设计原则摘要

> **Unity already knows geometry; Environment authoring should add semantics, not copy geometry.**

进一步说：

> **额外 Raw Condition 的价值，在于补足 Scene Representation 中缺失、且 Environment Resolver 真正需要的信息；不是为了把现实世界所有属性都参数化。**

最终目标不是让 Environment Entity “信息最完整”，而是让：

```text
World Truth
→ Raw Conditions
→ Derived Conditions
→ Fish-side Factors
```

每一层只有一个清晰职责，并且不制造重复 Truth。
<title>中鱼中层框架-逻辑模块与相互关系</title>

# 模块与数据：

## 总体

- **输入**

  - 鱼配置
  
    - 投鱼配置；
    - 鱼习性配置；
  - 环境条件
  
    - 课程表；
    - 钓场三维数据；一般在Unity中编辑；
  - 玩家策略
  
    - 钓具
    
      - 饵
      - 线、引线
    - 操作
    
      - 姿态
      - 饵点
      - 人物位置
- **输出**

  - 中鱼等待时间
  - 鱼种Species
- 此外，**中间**有几个非常重要的纽带数据：

  - 派生环境场（即派生环境权重场，Derived Environment Field，DEF）；
  - 持久响应场；（窝料、响动等带来的影响场，持续一段时间）
  - 圆桌权重表；

## 一图流

<whiteboard comment-refs="c1 c2 c3" token="VoEUw6v9Eh5ajgbkRwmcxGc7nQf"></whiteboard>





## 模块主线与数据流

中鱼系统的主要模块和数据流可以概括为：

```text
因子列表
  ↓
构造条件组
  ↓
条件组鱼筛选
  ↓
逐个计算当前条件组中的中鱼习性模式（Engagement Mode）
  ↓
各中鱼习性模式内逐项评估因子
  ↓
中鱼习性模式空间结果集
  ↓
写入派生环境场（DEF）

DEF ───────────────┐
                  ├─→ 响应
玩家策略与操作数据 ──┘
                  ↓
               鱼适配系数集
                  ↓
               圆桌计算
                  ↓
               权重组装
                  ↓
            圆桌权重列表
                  ↓
               抽鱼和生成
                  ↓
            Fish AI / 下游玩法
```

烘焙阶段先根据因子列表构造条件组，再对每个条件组进行条件组鱼筛选，并计算需要保存的中鱼习性模式空间结果集，最后写入派生环境场（DEF）。响应阶段读取 DEF，并结合玩家策略与操作数据计算鱼适配系数集。圆桌计算使用鱼适配系数集、烘焙相关权重、投鱼配置和圆桌控制规则组装圆桌权重列表；抽鱼和生成再根据该列表完成抽鱼、属性确定和鱼对象生成。Fish AI / 下游玩法属于中鱼系统范围外的下游模块。

<table><colgroup><col/><col/><col/><col/><col/><col/><col/><col/></colgroup><tbody><tr><td vertical-align="top"><b>模块</b></td><td vertical-align="top"><b>所属模块</b></td><td vertical-align="top"><b>作用</b></td><td vertical-align="top"><b>触发条件/时机</b></td><td vertical-align="top"><b>运行频率</b></td><td vertical-align="top"><b>主要输入</b></td><td vertical-align="top"><b>主要输出</b></td><td vertical-align="top"><b>关系与说明</b></td></tr><tr><td vertical-align="top">数据输入</td><td vertical-align="top"></td><td vertical-align="top">提供中鱼系统所需的环境、投鱼和鱼习性相关数据。</td><td vertical-align="top">数据配置、编辑或运行时采样时。</td><td vertical-align="top"></td><td vertical-align="top"><ul><li>环境上下文</li><li>钓场投鱼配置</li><li>鱼的习性配置</li><li>玩家策略与操作数据</li></ul></td><td vertical-align="top">供烘焙、响应和后续抽鱼使用的输入数据。</td><td vertical-align="top">是其它模块的基础输入，不负责具体的因子计算。</td></tr><tr><td vertical-align="top">烘焙</td><td vertical-align="top"></td><td vertical-align="top">将相对低频变化的环境和鱼配置转化为可复用的中鱼相关结果。</td><td vertical-align="top"><ul><li>课程表滚动</li><li>修改配置</li><li>修改空间信息</li></ul></td><td vertical-align="top">低</td><td vertical-align="top"><ul><li>鱼配置</li><li>环境条件</li><li>适配条件 / 响应条件</li></ul></td><td vertical-align="top"><ul><li>派生环境场（DEF）</li><li>中鱼习性模式空间结果集</li></ul></td><td vertical-align="top">为响应和圆桌计算提供可复用的烘焙结果；内部计算细节不在本表展开。</td></tr><tr><td vertical-align="top">　├─ 烘焙因子运算</td><td vertical-align="top">烘焙</td><td vertical-align="top">针对单个因子，结合条件和中鱼习性模式进行评价。</td><td vertical-align="top">烘焙过程中。</td><td vertical-align="top"></td><td vertical-align="top"><ul><li>条件</li><li>因子</li><li>对应习性组件</li></ul></td><td vertical-align="top"><ul><li>门控结果</li><li>亲和系数</li><li>因子结果</li></ul></td><td vertical-align="top">属于烘焙内部步骤，不单独构成对外模块。</td></tr><tr><td vertical-align="top">　├─ 烘焙通道聚合</td><td vertical-align="top">烘焙</td><td vertical-align="top">汇总同一条件组下多个因子的结果。</td><td vertical-align="top">相关因子计算完成后。</td><td vertical-align="top"></td><td vertical-align="top">多个因子结果。</td><td vertical-align="top">通道结果。</td><td vertical-align="top">属于烘焙内部步骤；具体聚合规则见烘焙专题。</td></tr><tr><td vertical-align="top">　├─ 中鱼习性模式结果集</td><td vertical-align="top">烘焙</td><td vertical-align="top">汇总同一条件组下多个中鱼习性模式的空间结果，并协调不同模式之间的相对权重。</td><td vertical-align="top">条件组结果生成时。</td><td vertical-align="top"></td><td vertical-align="top">各中鱼习性模式的通道结果。</td><td vertical-align="top">中鱼习性模式空间结果集。</td><td vertical-align="top">同一条件组保留多个模式结果，不按每个 x、y、z 位置重复保存相同条件组合。</td></tr><tr><td vertical-align="top">　└─ 烘焙结果输出</td><td vertical-align="top">烘焙</td><td vertical-align="top">整理并输出烘焙阶段生成的结果。</td><td vertical-align="top">一次烘焙完成后。</td><td vertical-align="top"></td><td vertical-align="top">通道结果及其聚合结果。</td><td vertical-align="top"><ul><li>派生环境场（DEF）</li><li>中鱼习性模式空间结果集</li></ul></td><td vertical-align="top">供响应和圆桌计算读取。</td></tr><tr><td vertical-align="top">响应</td><td vertical-align="top"></td><td vertical-align="top">结合烘焙结果和玩家当前策略，计算本次中鱼响应。</td><td vertical-align="top">持久响应和姿态响应分别在各自条件满足时触发。</td><td vertical-align="top">中/高</td><td vertical-align="top"><ul><li>派生环境场（DEF）</li><li>中鱼习性模式空间结果集</li><li>玩家策略与操作数据</li><li>持久响应场</li></ul></td><td vertical-align="top"><ul><li>响应结果</li><li>鱼适配系数集</li></ul></td><td vertical-align="top">读取烘焙结果，不重新生成派生环境场；鱼适配系数集交给圆桌计算。</td></tr><tr><td vertical-align="top">├─ 持久响应</td><td vertical-align="top">响应</td><td vertical-align="top">计算持续生效的玩家行为对中鱼习性模式和响应结果的影响。</td><td vertical-align="top">玩家进行持久型操作时，例如打窝。</td><td vertical-align="top">中</td><td vertical-align="top"><ul><li>玩家持久操作</li><li>派生环境场（DEF）</li></ul></td><td vertical-align="top">持久响应场。</td><td vertical-align="top">为姿态响应提供持续生效的增量影响，不复制一份派生环境场。</td></tr><tr><td vertical-align="top">　│　├─ 条件派生</td><td vertical-align="top">持久响应</td><td vertical-align="top">把持久操作数据整理为可供后续计算使用的条件。</td><td vertical-align="top">持久操作数据发生变化时。</td><td vertical-align="top"></td><td vertical-align="top"><ul><li>持久操作数据</li><li>已有派生结果</li></ul></td><td vertical-align="top"><ul><li>派生条件</li><li>必要的原始条件</li></ul></td><td vertical-align="top">使用“条件派生”作为人类可读名称，具体规则见响应专题。</td></tr><tr><td vertical-align="top">　│　├─ 因子运算</td><td vertical-align="top">持久响应</td><td vertical-align="top">根据持久响应条件评估相关因子。</td><td vertical-align="top">条件派生完成后。</td><td vertical-align="top"></td><td vertical-align="top">派生条件、因子和习性组件。</td><td vertical-align="top">持久响应因子结果。</td><td vertical-align="top">沿用统一的因子和习性组件语义。</td></tr><tr><td vertical-align="top">　│　└─ 系数聚合</td><td vertical-align="top">持久响应</td><td vertical-align="top">汇总持久响应中的相关因子结果。</td><td vertical-align="top">相关因子运算完成后。</td><td vertical-align="top"></td><td vertical-align="top">持久响应因子结果。</td><td vertical-align="top">持久响应场。</td><td vertical-align="top">具体系数和聚合规则见响应专题。</td></tr><tr><td vertical-align="top">　└─ 姿态响应</td><td vertical-align="top">响应</td><td vertical-align="top">根据当前姿态、饵和玩家操作计算即时响应结果。</td><td vertical-align="top">玩家姿态、饵或操作发生变化时。</td><td vertical-align="top">高</td><td vertical-align="top"><ul><li>持久响应场</li><li>中鱼习性模式空间结果集</li><li>饵与姿态</li><li>玩家位置与操作</li><li>派生环境场（DEF）</li></ul></td><td vertical-align="top"><ul><li>响应条件</li><li>鱼适配系数集</li></ul></td><td vertical-align="top">读取烘焙结果和持久响应场，完成当前姿态下的即时计算。</td></tr><tr><td vertical-align="top">　　├─ 响应条件整理</td><td vertical-align="top">姿态响应</td><td vertical-align="top">将当前姿态、饵和操作整理为因子可使用的条件。</td><td vertical-align="top">姿态响应开始时。</td><td vertical-align="top"></td><td vertical-align="top"><ul><li>鱼侧动态参数</li><li>饵</li><li>窝料</li><li>姿态</li><li>玩家位置与操作</li></ul></td><td vertical-align="top">原始条件与派生条件。</td><td vertical-align="top">使用“响应条件整理”作为人类可读名称；具体派生规则见响应专题。</td></tr><tr><td vertical-align="top">　　├─ 响应因子运算</td><td vertical-align="top">姿态响应</td><td vertical-align="top">根据响应条件评估当前相关因子。</td><td vertical-align="top">响应条件整理完成后。</td><td vertical-align="top">高</td><td vertical-align="top">响应条件、因子、习性组件及派生环境场。</td><td vertical-align="top">各因子适配系数。</td><td vertical-align="top">沿用统一的因子和习性组件语义，不另造一套响应因子体系。</td></tr><tr><td vertical-align="top">　　└─ 响应系数聚合</td><td vertical-align="top">姿态响应</td><td vertical-align="top">汇总响应因子结果，形成当前响应结果。</td><td vertical-align="top">响应因子运算完成后。</td><td vertical-align="top">高</td><td vertical-align="top">响应因子结果及相关权重结果。</td><td vertical-align="top">鱼适配系数集。</td><td vertical-align="top">环境系数与环境权重的具体公式不在本表展开。</td></tr><tr><td vertical-align="top">圆桌计算</td><td vertical-align="top"></td><td vertical-align="top">汇总响应、烘焙、投鱼配置和圆桌控制规则，形成抽鱼依据。</td><td vertical-align="top">一次姿态响应完成后。</td><td vertical-align="top">按次</td><td vertical-align="top"><ul><li>鱼适配系数集</li><li>烘焙相关权重</li><li>投鱼配置</li><li>圆桌控制规则</li></ul></td><td vertical-align="top">圆桌权重列表。</td><td vertical-align="top">圆桌计算在响应之后组装最终抽鱼权重，不属于烘焙输出。</td></tr><tr><td vertical-align="top">　├─ 权重组装</td><td vertical-align="top">圆桌计算</td><td vertical-align="top">汇总各路权重，形成抽鱼所需的权重结果。</td><td vertical-align="top">圆桌计算开始时。</td><td vertical-align="top">按次</td><td vertical-align="top">烘焙相关权重、鱼适配系数集和投鱼配置。</td><td vertical-align="top">圆桌权重结果。</td><td vertical-align="top">具体权重算法见圆桌专题。</td></tr><tr><td vertical-align="top">　└─ 圆桌权重列表</td><td vertical-align="top">圆桌计算</td><td vertical-align="top">汇总并应用圆桌控制规则，形成最终候选权重列表。</td><td vertical-align="top">权重组装完成后。</td><td vertical-align="top">按次</td><td vertical-align="top">圆桌权重结果及圆桌控制规则。</td><td vertical-align="top">最终候选权重列表。</td><td vertical-align="top">圆桌四件的具体规则仍以圆桌专题为准；当前文档只描述模块边界。</td></tr><tr><td vertical-align="top">抽鱼和生成</td><td vertical-align="top"></td><td vertical-align="top">根据圆桌权重列表完成鱼的抽取、属性确定和对象生成。</td><td vertical-align="top">圆桌计算完成后。</td><td vertical-align="top">按次</td><td vertical-align="top">最终候选权重列表、投鱼配置及生成规则。</td><td vertical-align="top"><ul><li>抽鱼结果</li><li>鱼的属性</li><li>生成的鱼对象</li></ul></td><td vertical-align="top">将生成结果交给 Fish AI 和后续玩法；中鱼等待时间属于系统最终输出，但不在响应模块直接产出。</td></tr><tr><td vertical-align="top">Fish AI / 下游玩法</td><td vertical-align="top"></td><td vertical-align="top">处理刺鱼、博鱼以及鱼生成后的运行时行为。</td><td vertical-align="top">鱼对象生成后。</td><td vertical-align="top">高</td><td vertical-align="top">生成的鱼对象及运行时状态。</td><td vertical-align="top">鱼的运行时行为。</td><td vertical-align="top">属于中鱼系统范围外的下游模块。</td></tr></tbody></table>

## 核心中间数据：派生环境场（DEF）

### DEF 的作用

派生环境场（即派生环境权重场，英文名Derived Environment Field，简称 DEF）是烘焙阶段生成的按条件组组织的结果 Map。它不为每个空间位置单独保存一份结果，而是将相同条件组合归并到同一个条件组，并在条件组下保存需要参与计算的中鱼习性模式空间结果。

### DEF 的结构

```text
派生环境场（DEF）
└── 条件组
    └── 中鱼习性模式条目
        └── 中鱼习性模式空间结果
```

一个条件组对应当前条件下需要保存的多条中鱼习性模式条目，而不是只保存一个鱼种的几个模式。条件组鱼筛选会先从全部候选条目中筛出当前条件组需要计算和存储的条目，以额外判断时间换取 DEF 的存储空间。

示例：

```text
条件组 A
├── 鲤鱼 / 伏击模式
│   └── 中鱼习性模式空间结果
├── 鲤鱼 / 开放游弋模式
│   └── 中鱼习性模式空间结果
├── 草鱼 / 开放游弋模式
│   └── 中鱼习性模式空间结果
└── 鲈鱼 / 伏击模式
    └── 中鱼习性模式空间结果
```

### 中鱼习性模式与因子计算

中鱼习性模式（Engagement Mode）是烘焙计算的主要对象。当前过渡阶段，一个中鱼习性模式条目仍可能通过“鱼种 + 中鱼习性模式”确定，但这属于输入组织方式，不改变中鱼习性模式作为主要计算对象的定义。

对每个条件组，系统逐个计算经过条件组鱼筛选的中鱼习性模式。对某个中鱼习性模式，系统逐项处理因子：读取该因子对应的条件，索引该中鱼习性模式对应的习性组件，再得到门控结果、亲和系数和因子结果。

```text
因子列表
  ↓
条件组合 → 条件组
  ↓
条件组鱼筛选
  ↓
中鱼习性模式（Engagement Mode）
  ↓
对应习性组件 × 因子条件
  ↓
因子结果
  ↓
中鱼习性模式空间结果
```

因子在 DEF 烘焙中承担两种角色：一方面，因子列表参与条件组合和条件组构造；另一方面，因子在每个中鱼习性模式内被逐项评估。

### 结果层次

- **中鱼习性模式空间结果**：一个条件组下，一个中鱼习性模式完成各因子计算和聚合后的空间相关结果。
- **中鱼习性模式空间结果集**：同一条件组下多个中鱼习性模式的空间结果，以及模式之间的相对权重协调结果。多个模式结果保留，不压缩成单一结果。

模式之间可以进行整体平衡调整。例如某个模式的权重显著提高时，其他模式的权重可以适当降低，但各模式的空间结果仍保留在结果集中。

### 结果字段

单个中鱼习性模式空间结果包含：

- 环境权重（即空间分布强度）
- 鱼状态量

鱼状态量包括：

- 进食动机（feeding motivation）
- 活跃度（activity）
- 警戒度（wariness）
- 食性偏移（diet shift）

食性偏移不是鱼的基础食性范围，而是当前条件下，鱼在多个可接受饵种之间产生的相对偏向变化。

### 环境系数与环境权重

环境系数、基础机会强度和环境权重是三个不同概念，不能互相替换。

- 环境系数：当前环境对特定计算对象的适配修正量，不是权重。
- 基础机会强度：来自钓场投鱼配置的机会种子（prob_weight_ideal），是尚未乘以环境系数的机会强度。
- 环境权重：由基础机会强度乘以环境系数得到的最终权重结果。

**环境权重 = 基础机会强度 × 环境系数**

环境权重，即空间分布强度。最终合成中，基础机会强度只乘一次环境系数。

## 持久响应场

持久响应场是运行时对 DEF 的持续性增量影响层，不复制一份 DEF。

它可以记录：

- 响应来源，例如打窝等玩家持久操作；
- 影响的条件或因子；
- 影响强度及方向；
- 生效范围；
- 持续时间、衰减状态或失效条件；
- 对中鱼习性模式及其空间结果的影响。

持久响应场由持久响应生成，供姿态响应读取，并与 DEF 中的烘焙结果叠加使用。它不是另一份 DEF，也不改变 DEF 的烘焙结果。

## 圆桌权重表

圆桌权重表是响应阶段之后、抽鱼和生成之前形成的候选权重列表，不属于烘焙产物。

圆桌计算的输入包括：

- 鱼适配系数集；
- 烘焙相关权重；
- 投鱼配置；
- 圆桌控制规则。

圆桌计算先进行权重组装，再形成圆桌权重列表，供抽鱼和生成使用。品质抽取调整、硬保底、动态权重调整等圆桌控制规则的具体语义和字段，仍以圆桌专题的当前权威文档为准；本节只固定其在模块主线中的位置和输入输出关系。

## 数据描述

### 环境实体

空间环境实体（Spatial Environment Entity，简称环境实体）是 3D 钓场中承载环境语义的 Unity 对象。几何事实遵循“Unity 已知的几何不重复配置”：位置、朝向、缩放、层级由 Transform 自动读取；形状、尺寸、包围范围、体积由 Mesh / Collider 自动读取或计算。实体自身配置的语义参数与影响系数，作为原始条件参与计算。

数据分为三类：

- **Unity 原生事实（自动读取，不配置）**：位置 / 朝向 / 缩放（Transform）、父子层级、网格几何、包围盒、footprint、体积近似等。
- **实体参数（原始条件）**：由实体直接配置，包括实体类型等语义参数（EntityType、GrowthForm、PatchDensity 等）与影响系数——隐蔽系数、光照遮挡系数、水流遮挡、溶氧供给强度 / 距离等。
- **派生条件（计算得到）**：由实体影响系数（原始条件）、世界上下文（课程表天光强度、时段、天气、水温等）与空间位置（深度、距离）共同计算出的点级实际值。例如当前饵点的实际光照强度＝遮光程度 × 天光强度 × 深度衰减；实际溶氧、局部流速、掩蔽程度同理。

实体参数（原始条件）示例：

| **实体类型** | **参数** | **示例值** |
|-|-|-|
| 水草实体 | 水草密度 | 0.8 |
| 水草实体 | 隐蔽系数 | 1.0 |
| 水草实体 | 光照遮挡系数 | 0.5 |
| 水草实体 | 溶氧供给强度 | 0.5 |
| 水草实体 | 溶氧供给距离 | 2.0 |
| 石头实体 | 水流遮挡 | 0.3 |
| 石头实体 | 溶氧影响强度 | 0.5 |
| 石头实体 | 光照遮挡系数 | 0.4 |

派生条件示例（点级实际值，示意）：

| **派生条件** | **示意值（饵点处）** |
|-|-|
| 实际光照强度 | 3200lx（遮光程度 × 天光强度 × 深度衰减） |
| 实际溶氧 | 8.2mg/L |
| 局部流速 | 0.1m/s |
| 掩蔽程度 | 0.9 |

几何数据边界的完整论证与各类实体的参数设计参考，见仓库《Environment Entity Raw Condition Schema》：https://github.com/futouyiba/HitFish-Up/blob/main/docs/environment-entity-raw-condition-schema.md

这些实体参数（原始条件）与世界上下文、空间位置一起，派生点级的实际光照、溶氧、流速、掩蔽等条件，并参与栖息波动组的形成。

数据边界分为三层：

### 空间条件输入

3D 空间数据先提供空间事实，再经过条件提取和条件组合，形成参与 DEF 烘焙的条件组。空间输入可分为三层：

- **空间原始数据**：实体类型、位置、范围、深度、底质、结构距离和实体当前状态等直接编辑或采样的数据。
- **空间派生条件**：由空间原始数据推导出的水温、光照、溶氧、水流、掩蔽程度、可视性和生态水层等可计算特征。
- **栖息波动组**：多个环境条件之间的联动关系，例如水温、溶氧、水流和光照变化对同一栖息区域及相关因子的联动影响。

空间原始数据不直接等同于中鱼结果；它们经过条件提取、组合和条件组鱼筛选后，才进入中鱼习性模式的因子计算。

# 术语速查

术语的详细定义、条件分级清单、中鱼习性模式说明与命名讨论，已独立为《中鱼术语与名词定义》：https://pisn3u3ony2.feishu.cn/docx/OyeSdkaheoIAfKxiW13cKZsknLd（本文档的子页面）。以下只保留模块表所需的最小速查。

- **因子**：中鱼运算中的影响因素，独立评估、计算和聚合的对象。
- **条件**：鱼之外输入的数据，因子运算的输入。按推算顺序分原始条件/派生条件；按数据来源分环境条件/适配条件（响应条件）。
- **习性组件**：某中鱼习性模式下，对一个因子及其条件的评价规则（门控、亲和度、响应曲线、聚合参数）。
- **中鱼习性模式（Engagement Mode）**：烘焙计算的主要对象；过渡阶段条目可通过“鱼种 + 模式”定位。
- **系数**：因子经习性组件评价后的输出量（门控结果、亲和系数、因子结果，及聚合后的环境系数、鱼适配系数等）。
- **鱼状态量**：进食动机、活跃度、警戒度、食性偏移（见核心中间数据·结果字段）。
- **派生环境场（DEF，展开名：派生环境权重场）**：按条件组归并的烘焙结果 Map（见核心中间数据章节）。
- **环境权重（即空间分布强度）＝ 基础机会强度 × 环境系数**（见核心中间数据·环境系数与环境权重）。
- **持久响应场 / 圆桌权重表**：见核心中间数据章节。

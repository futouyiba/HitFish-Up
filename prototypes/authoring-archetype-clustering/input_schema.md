# Input Schema｜本 Probe 使用的输入与 Effect Signature 转换规则

状态：PROBE-ONLY / NOT PROMOTED。本文档只描述 `prototypes/authoring-archetype-clustering` 这个数据验证 Prototype 使用的数据与转换规则，不构成 0.3.4 的配置承诺；所有推导值均不冒充正式 Current 配置。

## 1. Contract 依据（读取于 2026-09-15）

| Contract 事实 | 来源 |
|---|---|
| 温度 6 项配置：`temp_accept_min / temp_fav_min / temp_fav_max / temp_accept_max / temp_threshold / falloff_shape`（前四项 Int×0.1°C） | 0.3.4.0 开发需求 §3.2；Bake DSL Core Spec R0 §3.1 |
| `range_fit(x)`：舒适区 Fit=1，可接受区外 Fit=0，中间 LINEAR 或 SMOOTHSTEP 过渡 | Bake DSL Core Spec R0 §7.2（公式逐字实现于 `scripts/lib_signature.py`） |
| 结构亲和：约 25 个 StructureType × float，编辑源为 `tier + fine_tune` | 开发需求 §3.2 / §3.2.1；0.3.4 §5.4.8-A |
| 亲和档位共享尺度：最优 1.00[1.00,1.00] / 次优 0.60[0.50,0.75] / 较差 0.25[0.20,0.30] / 不适 0.05[0.00,0.10]，fine_tune∈[-1,+1] 分段线性 | 开发需求 §3.2.1 |
| 觅食水层：`SURFACE / MIDDLE / BOTTOM` 3 项 float | 开发需求 §3.2；Core Spec §3.1 |
| 时段：固定 5 时段 `DAWN / MORNING / AFTERNOON / DUSK / NIGHT`；旧 8 时段不做自动迁移 | 开发需求 §3.4 / §3.5；Core Spec §3.1 |
| Resolve 链：Species Shared + FishQuality + Engagement Mode → `ResolvedBakeSubjectConfig` → `BakeInputBuilder` → `BakeInputSnapshot` | 开发需求 §3.1 / §2.2 |
| 本 Probe 分析对象 = Species Shared 层（Species 基线），不区分 Engagement Mode Override | 见 §5 说明 |

## 2. 数据源与 provenance 分级

| 级别 | 含义 |
|---|---|
| `SOURCE` | 参考库源快照字段原值（2026-09-08 快照，V3鱼总表·表格2 → Notion V3鱼种数据库，267 条） |
| `SOURCE-LINKED` | 飞书 V3鱼总表源表中存在、Notion 参考库未迁移的字段（本次从飞书直读） |
| `DERIVED` | 本 Probe 用文档化规则从 SOURCE / SOURCE-LINKED 推导，非正式配置 |
| `ASSUMED-CONST` | Contract 新增字段无任何数据，Probe 内设为常量（不参与区分鱼种） |
| `CALIBRATION` | 大口黑鲈 Calibration R0 的校准候选值（唯一一条接近 0.3.4 全格式的鱼） |

### 2.1 Notion V3 鱼种数据库（267 条，快照 2026-09-08）

本 Probe 拉取的字段与覆盖率（`data/raw/fish_reference_267.csv`）：

| 字段 | 覆盖 | 级别 | 用途 |
|---|---|---|---|
| `资料水温下限/上限(°C)`（FishBase Stocks 温度范围） | 267/267 | SOURCE | 温度 acceptable 边界 |
| `最喜欢的温度(°C)`（文本数值） | 267/267 | SOURCE | 温度 comfort 中心 |
| `候选水温带`（冷水/温水/暖水/广温） | 234/267 | SOURCE（策划派生标签） | 交叉验证 |
| `时段偏好`（全天/晨昏/早晨/傍晚/夜间/午后；实测仅出现 4 种） | 267/267 | SOURCE（策划派生标签） | 时段组件唯一输入 |
| `栖息带类型`（DemersPelag：benthopelagic 101 / demersal 95 / reef-associated 13 / pelagic 系 30 / 其它 2 / 空 27） | 240/267 | SOURCE | 水层组件唯一输入 |
| `深度下限/上限(m)` | 152/267、120/267 | SOURCE | 辅助 |
| `食性（源表候选）`、`摄食类型`、复核层字段 | 211–34/267 | SOURCE / Review Overlay | 辅助解释 |

Notion 参考库**明确未迁移**（源表有但本库没有）：逐时段系数、推荐结构体、饵清单及权重、分品质重量、中鱼/搏鱼属性。这直接决定本 Probe 对结构/时段组件的数据策略（见 §3）。

### 2.2 飞书 V3鱼总表源表（表格2，141 源字段）

（本节由飞书直读结果填写；见 `data/raw/feishu_v3_selected_fields.csv` 与 report。）

## 3. 四个组件的 Effect Signature 构造

### 3.1 TemperatureEffectSignature（真实度最高）

- `temp_accept_min/max` ← `资料水温下限/上限(°C)`（SOURCE）。
- comfort 区间：**DERIVED 规则 T1**：以 `最喜欢的温度` 为中心，半宽 = 15% × 可接受宽度，夹紧在 [accept_min, accept_max] 内。源表大多数鱼的"最喜欢温度"就是其范围中点（如 [10,20]→15），此时 T1 等价于"可接受区中间 30% 为舒适区"。
- `falloff_shape`：**ASSUMED-CONST = LINEAR**（全部鱼种统一；该字段为本期新增、无既有数据 → 记入 Spec Gap List）。SMOOTHSTEP 不影响鱼间相对差异的结论，见 report 附录稳健性检查。
- `temp_threshold`：不进入 Signature（无逐鱼数据；属于 Early Return 阈值而非曲线形状）→ Spec Gap List。
- Signature = `range_fit` 在 **0–40°C、步长 0.5°C 的 81 点网格**上的取值向量（覆盖全部 267 条鱼的实际边界范围 -1.3–41°C，越界点为 0）。

### 3.2 StructureEffectSignature

（数据策略取决于飞书源表是否有逐鱼「推荐结构体」；无则按 habitat-class 级模板 + 标记 INSUFFICIENT。填写于 report。）

### 3.3 TimeEffectSignature

- 若飞书源表有逐鱼旧 8 时段系数：按文档化 8→5 聚合规则映射（DERIVED）。
- 否则：**DERIVED 规则 T2**，由 `时段偏好` 标签展开为 5 时段档位锚点（最优1.00/次优0.60/较差0.25/不适0.05）：

| 标签 | DAWN | MORNING | AFTERNOON | DUSK | NIGHT |
|---|---|---|---|---|---|
| 全天活跃 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 晨昏活跃 | 1.00 | 0.60 | 0.25 | 1.00 | 0.60 |
| 早晨活跃 | 1.00 | 1.00 | 0.60 | 0.60 | 0.25 |
| 夜间活跃 | 0.60 | 0.25 | 0.25 | 0.60 | 1.00 |
| 傍晚活跃 / 午后活跃 | （267 条中未出现） | | | | |

该映射为本 Probe 杜撰的等价展开（**DERIVED，非正式**），目的只是让"标签粒度下的时段模板"可量化；标签→系数的正式映射规则在 Contract 中不存在 → Spec Gap List。

### 3.4 FeedingLayerEffectSignature

**DERIVED 规则 T3**：由 `栖息带类型`（FishBase DemersPelag）映射到 3 水层档位锚点：

| DemersPelag | SURFACE | MIDDLE | BOTTOM | 依据 |
|---|---|---|---|---|
| demersal | 0.25 | 0.60 | 1.00 | 底栖为主 |
| benthopelagic | 0.60 | 1.00 | 0.60 | 近底但水柱中摄食（宽层型；与 Bass Calibration 的 0.6/1.0/0.6 同构） |
| reef-associated | 0.60 | 1.00 | 0.60 | 礁区结构导向，水层近似宽层 |
| pelagic / pelagic-neritic / pelagic-oceanic | 1.00 | 0.60 | 0.25 | 上中层开放水 |
| bathydemersal | 0.05 | 0.25 | 1.00 | 深海底层 |
| bathypelagic | 0.25 | 0.60 | 1.00 | 深水柱近底 |
| 空（27 条） | — | — | — | **排除出水层组件分析**（数据缺失） |

DemersPelag → 3 层亲和的正式映射在 Contract 中不存在 → Spec Gap List。25–34 条有 `复核栖息与空间行为` 文本的鱼可作未来精化，但文本解释非确定性，本 Probe 不使用。

## 4. 距离定义（组件级与整体）

- `D_temperature / D_structure / D_time / D_feeding_layer`：各组件 Effect 向量的**平均绝对差**（mean |Δfit| / mean |Δaffinity| / mean |Δcoeff|）。可解释：两条鱼在该组件上平均每维效果差多少。
- `D_joint`：四组件距离先各自除以其理论最大值（温度 1.0；结构/时段/水层档位锚点最大差 0.95≈1.0，统一用 1.0 归一）后**等权平均**。等权 = 四组件在 Bake 乘法链中地位对称（Core Spec 示例 Program 四 rule 顺序相乘），且无任何游戏内权重数据。

## 5. 分析层级声明

本 Probe 的分析单位是 **Species Shared 层基线**（等价于"一条鱼刚建好、NORMAL 0 Override 时的 Species 底版"）。不构造 Engagement Mode 差异（无数据）、不涉及 FishQuality Override（0.3.4 已收窄其职责）。因此结论只回答"**新建 Species 时的一次性 Starter Archetype**"是否成立，与 5.4.11-E 的 Fish Archetype（一次性 Recipe、非持续继承）定义对齐。

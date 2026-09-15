# 0.3.4 鱼侧 Authoring Archetype 数据验证报告
**Verdict：`D. INSUFFICIENT_DATA`（用于正式 Whole-Species Archetype 结论）**
> 数据规模足够（267 条），但 0.3.4 完整生产输入不足：没有可核验的 Species Shared + FishQuality + Engagement Mode → ResolvedBakeSubjectConfig → BakeInputSnapshot 全链路快照。因此数字只能作为候选压缩信号，不能作为正式模板准入证据。
## 1. Rebase 与范围
已按 Router → Project State Current → Design Branch Index → Simplified Production V0 Working Main → 0.3.4 → Bake DSL → 开发需求 → Authoring Tool 路径读取当前文档。当前业务身份是 `Engagement Mode｜中鱼习性模式`；`Program Family / LogicTemplate` 仅为逻辑复用概念，不是鱼分类。

关键链路：`Species Shared Config + FishQuality Stable Config + Engagement Mode Params / Override + BakeProgramRef → ResolvedBakeSubjectConfig → BakeInputSnapshot`。本 Probe 只分析 Species Shared 基线，因为没有 Mode/FishQuality 的逐鱼生产数据。
## 2. 数据盘点
- 飞书 V3 鱼总表表格 2：**267/267 条完整记录**，实测 137 个源字段（任务描述的 141 与当前实测不一致）。
- 有逐鱼源字段：温度上下限、最喜欢温度、容忍系数、温度接受阈值、FG 推荐结构体、8 个 period 系数、候选水层、表/中/底亲和系数、时段标签、食性/饵字段。
- 没有现成逐鱼 0.3.4 `falloff_shape`、正式 5 时段新配置、ResolvedBakeSubjectConfig、Program RequiredParamSchema binding snapshot、BakeInputSnapshot 或 Mode/FishQuality Override。

详见 [输入口径](input_schema.md)、[飞书导出](data/raw/feishu_v3_selected_fields.csv)、[Notion辅助导出](data/raw/fish_reference_267.csv)。
## 3. Effect Signature 与距离
- Temperature：按 Core Spec `range_fit`，0–40°C 每 0.5°C 共 81 维；acceptable 边界取源表，comfort 区间以最喜欢温度按文档化 T1 推导；`falloff_shape=LINEAR` 是统一假设。
- Structure：FG 推荐结构体标签集合的 presence 向量（当前观测到 53 个标签），**不是**正式约 25 类 `StructureType × float`。
- Time：源表 8 个 3 小时系数归一化，**不是** 0.3.4 要求的 5 时段配置。
- Feeding Layer：源表表/中/底 1–10 归一化。
- 组件距离 = 每维平均绝对差；joint = 四组件等权平均。
## 4. 压缩曲线（允许误差 = joint Effect Signature 平均差）

| 允许误差 | Archetypes | 可共享覆盖率* | Median effect error | P90 effect error | 平均复用字段/鱼 | 平均修改字段/鱼 |
|---:|---:|---:|---:|---:|---:|---:|
| 5% | 136 | 67.4% | 0.000 | 0.041 | 2.94 | 1.06 |
| 10% | 60 | 90.6% | 0.052 | 0.091 | 2.15 | 1.85 |
| 15% | 22 | 98.9% | 0.084 | 0.134 | 1.85 | 2.15 |
| 20% | 9 | 99.6% | 0.128 | 0.180 | 1.57 | 2.43 |
| 25% | 5 | 99.6% | 0.146 | 0.203 | 1.68 | 2.32 |
| 30% | 3 | 100.0% | 0.176 | 0.230 | 1.71 | 2.29 |

*可共享覆盖率排除了只服务自身的 singleton archetype；exact radius coverage 因允许 singleton 始终为 100%，不应误读为压缩成功。
## 5. 组件结果与整体 Family 检验
在 joint/各组件 ε=15% 的 average-linkage cut 下：Temperature 14 簇、Structure 21 簇、Time 4 簇、Feeding Layer 4 簇、Joint 31 簇。

组件聚类一致性（ARI/NMI）：

| 组件对 | ARI | NMI |
|---|---:|---:|
| temperature × structure | 0.073 | 0.269 |
| temperature × time | 0.055 | 0.139 |
| temperature × feeding_layer | -0.007 | 0.050 |
| structure × time | 0.150 | 0.311 |
| structure × feeding_layer | 0.017 | 0.151 |
| time × feeding_layer | 0.008 | 0.043 |

低一致性意味着不能把 component clusters 自动解释为 Whole-Species Family；同时 Structure 输入本身仍是标签集合，故该结论仅为风险信号。
## 6. 案例回读

见 [cases.md](outputs/cases.md)。该文件包含 3 个稳定样本、2 个边界样本、5 个最远样本，以及每条鱼的温度/结构/时段/水层原值和模板修改解释。

本轮 outlier（按 joint 距离）包括：丁鱥、鞍带石斑鱼、蓝笛鲷、美洲锐唇鲷、金鲫。它们是当前 probe representation 的 outlier，不是生物学异常判定。
## 7. Authoring 成本 proxy

Baseline 每条新鱼需填写四个组件的完整输入；Archetype 流程可从 medoid 初始化，再修改差异。以 15% 允许误差看，约 98.9% 鱼可加入非 singleton 共享起点，但需要约 2.15/4 个组件字段平均修改（P90 effect error 13.4%），且模板仍有 22 个；这不是“少量模板 + 低 override”的稳健信号。

字段数只是 proxy：结构约 25 条真实 entry、时段 5 条 Contract entry、温度 6 项、层 3 项，远不等于四个字段。正式 override ratio 必须在字段/profile-entry 粒度、使用真实 resolved snapshot 重算。
## 8. Spec Gap List

1. 源表 8 时段系数到 0.3.4 固定 5 时段无正式映射；开发需求明确禁止旧 8→5 自动迁移。
2. 源表 FG 推荐结构体标签到正式 `StructureType` 约 25 类 affinity profile 无确定映射。
3. 源表 `候选水层` / 1–10 亲和系数与 0.3.4 三层 affinity scale 的语义与单位未确认。
4. `falloff_shape` 为新增字段，逐鱼无数据；`temp_threshold` 的 0.3.4 正式值未形成完整生产数据。
5. 没有逐鱼 Mode Params/Override、FishQuality Stable Config、Program `RequiredParamSchema`、Program revision/hash 与 Binding Snapshot。
6. 没有同一版本的环境 Context / SpatialTarget 与 `BakeInputSnapshot`，无法回放 Effect Signature。
7. 参考库候选标签（时段、水温带、食性）含策划推导，不能直接当生态事实或 Runtime 输入。
## 9. 最终裁决

### D. INSUFFICIENT_DATA

**Evidence**：267 条 SOURCE-LINKED 行可支持探索性 component similarity，但缺少正式 0.3.4 resolved provenance；四类输入至少两类需要未经批准的语义推导。

**Compression Gain**：探索性曲线在 ε=15% 使用 22 个起点、98.9% 非 singleton coverage；ε=20% 使用 9 个起点、99.6%，但平均约 2.43/4 组件需修改，且误差上升。

**Override Cost**：以当前粗粒度 proxy 已不低；真实 profile-entry 粒度只会更高或需要更多核验。

**Outlier Cost**：仍有跨水温/结构/水层表达的边界与 outlier，不能通过自然分类或强制 K 消除。

**Human Interpretability**：时段和水层可读；结构推荐标签与正式 affinity entry 不同构，无法保证策划套用后直觉一致。

**Risk**：把源表推导直接提升为 Archetype 会把“参考资料 → 0.3.4 Contract”的缺口藏进模板，并可能制造错误的继承/覆盖期待。

因此本轮**不支持 Whole-Species Archetype，也不批准 Component Archetype 进入正式 Editor**。待补齐真实 0.3.4 配置后，应重跑同一脚本；如果组件一致性仍低而单组件压缩曲线稳定，再考虑 `COMPONENT_ARCHETYPES_ONLY`；如果 override 仍高，则 `ARCHETYPE_NOT_JUSTIFIED`。
## 10. 产物

- [README](README.md)
- [input_schema.md](input_schema.md)
- [clustering.py](scripts/clustering.py)
- [metrics.json](outputs/metrics.json) / [metrics.csv](outputs/metrics.csv)
- [cluster_assignments.csv](outputs/cluster_assignments.csv)
- [cases.md](outputs/cases.md)

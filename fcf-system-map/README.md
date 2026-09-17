# FCF Canonical System Map

`generated/fcf-system-map.drawio` 是**构建产物**——永远不要手工编辑。改 source JSON 后重新生成。

```bash
python3 build/build_diagram.py     # 4 个 source JSON -> generated/fcf-system-map.drawio
python3 build/validate.py          # 全部静态检查 + 确定性 + rename 稳定性
```

---

## 0. 本轮（2026-09-17）的脊椎重构

**上一版（Production Pilot v0.1，commit `2d52879`）把 `FCF Simplified V0 / 0.3.4` 的模块链 4.0–4.7 当成了脊椎。这是错的。**

读「中鱼升级｜」设计分支后确认：**Simplified V0 是第一性结构的一次投影，不是本体**。本轮把脊椎换成第一性结构：

```
中鱼升级（第一性，总体范围）        ← 本体，即本图的主干
 └ FCF v1（压缩 1，范围更小）       ← 本轮未读，留空位
    └ Simplified V0（压缩 2）
       └ 0.3.4（更小）
          └ 0.3.4.0-B（当前版本投影）
```

v0.1 的旧骨架保留在 git 历史 `2d52879` 作为 provenance。

**读取的权威**：

| 用途 | 页面 |
|---|---|
| 主干结构 | 中鱼升级｜Overall System Model：从 World State 到 Fish Spawn Commit (v20) |
| 中层拓扑 | 中鱼升级｜Mechanism Topology V2：Spatial × Response 深入下钻 (v2) |
| 中层 Kernel | 中鱼升级｜Behavioral Regime × Largemouth Bass：Spatial–Response 中层逻辑样板 (v8) |
| 当前版本投影 | 中鱼0.3.4.0-B｜开发需求 R0 / 固定模板分层烘焙 / Authoring & Resolve Contract R0 |

**未读（据 Design Owner 指示或本轮范围）**：FCF v1 / Full Mechanism；0.3.4 主规格只精读 §2 综述与 §4 机制（21.3 万字符全文未读）；Spatial / Interaction / Opportunity 的 Current 页未读。

---

## 1. Source files

| 文件 | 职责 |
|---|---|
| `graph.json` | 31 个节点（stable ID + label + caption + 语义层级 parent + layout lane）+ 35 条类型化语义边 |
| `scopes.json` | Scope 维度 = 压缩阶梯；`OVERALL`（不做裁剪）+ `0.3.4.0-B`（lens，逐节点归类）；其余层级声明为 DECLARED-UNASSIGNED |
| `views.json` | View 维度 = 展开粒度 + 可选 scope lens（文档自述其 §2 五张图是"同一系统的五个观察面"，本维度即为承载这一概念而存在） |
| `contracts.json` | 薄关联层：`semanticId → authorityRef / status / note`；只引用外部权威，不复制内容 |

## 2. 三维度正交

- **Hierarchy** = `graph.json` 的 `parent`（progressive disclosure）；`collapsible` 节点的整棵子树可折叠
- **Scope** = 压缩阶梯的每层投影；实现为对**同一批 cell** 的原生 `style` action 着色——**单实例，零复制**
- **View** = 展开粒度预设；改可见性的视图绝不改样式，反之亦然

## 3. 主干结构（第一性）

```
IO.WORLD / IO.FISH / IO.PLAYER / IO.RESOURCE       因果输入与稳定定义
        ↓
WAIST  W.READINESS / W.FUNCTIONAL / W.PRESENTATION  三个 semantic waist
        ↓
WHO    WHO.OPPORTUNITY (WHEN)                       这张票上可能是什么鱼
       WHO.SPATIAL → L    SP.GATE / SP.HABITAT / SP.VIABILITY / SP.AMBIENT / SP.LOCAL
       WHO.INTERACTION → C  IN.PERCEPTION / IN.INTERPRET / IN.FEEDING / IN.DEFENSE / IN.AGGREGATE
        ↓
JOIN   Candidate Resolver：q_species,j = Σ_r L_r,j × C_r,j   （同 support 先 Join 再 Reduce）
        ↓
RESOLVE RS.POLICY → RS.TRUEROLL → {RS.FALLBACK | RS.INSTANCE} → COMMIT
```

**关键语义（写进图里、不是注释）**：

- `IO.WORLD → WHO.INTERACTION` 是一条 **ANCHOR 边（红点线）**，标签明确写「必要关系事实 / Anchor — 不是最终 EnvironmentWeight」。这是第一性分支反复强调的防重算约束：环境侧与鱼侧是两条并行支路，**只在 JOIN 汇合一次**。
- `q = Σ_r L_r × C_r` 是**合法 retention join**；`TemperatureCoeff × DOCoeff × StructureCoeff` 则**没有默认语义资格**——先定语义关系，再定算子。
- 算子由 route relation 决定：重叠备选→`max`；主路失败才旁路→**残差 `C = C_P + (1−C_P)·C_F`**（`max(C_feed, C_defense)` 已被权威明确拒绝）；互斥混合→`Σ π_m C_m`；集合 union→`μ(∪A_m)/μ(Ω)`。

## 4. 当前版本投影：0.3.4.0-B

`scopes.json` 里 `0.3.4.0-B` 是唯一登记的 lens scope：**6 ACTIVE / 4 BOUNDARY / 21 OUT**。

- **ACTIVE**：`SYS`、`WHO`、`WHO.SPATIAL`、`SP.HABITAT`（Structure + Feeding Ecology Layer 组件）、`SP.VIABILITY`（Temperature 组件，DO 不在 P0）、`SP.AMBIENT`（Base × FinalEnvCoeff）
- **BOUNDARY**：`IO`、`IO.WORLD`（ConditionGroup 来源）、`IO.FISH`（FishQualityRef / FishEnvAffinityRef）、`WHO.OPPORTUNITY`（消费 ResolvedOpportunitySeed）
- **OUT**：Interaction 全域、WAIST 全域、`SP.GATE`、`SP.LOCAL`、JOIN、RESOLVE 全域（含 COMMIT）——**置灰但永不隐藏**

⚠️ **两处需要读者注意的映射判断**（已在 `scopes.json` 的 `basisNote` 记录）：

1. B 的 per-`CORE`-condition `GatePolicy` 与第一性主干里的 **Structural Gate 是不同对象**，故 `SP.GATE` 记为 OUT。
2. B 的 **Time Period 直接进 Opportunity Fit**，在第一性主干上落在哪一槽位**尚未由权威闭合** → 见 SEMANTIC_OPEN-007。

`containerRule`（容器节点 scope = 子节点最高活跃度）是**我们的呈现约定、不是权威声明**——已在 `scopes.json` 里显式写出并逐条列举，便于审计。

## 5. Views

| 视图 | 动 Hierarchy? | 动 Scope 配色? |
|---|---|---|
| **Overall**（默认） | 收起全部细节域 | 清除 lens，恢复中性 |
| **0.3.4.0-B** | **绝不触碰** | 应用 0.3.4.0-B lens |
| **WHO Detail** | 展开 WHO 两个子域 | **绝不触碰** |
| **RESOLVE Detail** | 展开 RESOLVE 域 | **绝不触碰** |

另有手动操作：点击任一 `collapsible` 域标题收起/展开其整棵子树，与按钮状态自由组合。

## 6. Validation

`python3 build/validate.py` → **PASS**：

```
stable IDs:            31 (unique, syntax-safe)
edges:                 35 semantic + 30 structural, endpoints ok
views:                 overall, 0340b, who-detail, resolve-detail (default overall)
scope lens:            0.3.4.0-B — 6 ACTIVE / 4 BOUNDARY / 21 OUT, all nodes classified once
ladder declared, unassigned: 0.3.4, SIMPLIFIED-V0, FCF-V1
contracts:             19 entries (refs valid)
determinism:           consecutive builds byte-identical; committed artifact fresh
rename stability:      cell ID set and geometry invariant under label rename
```

viewer 运行时（官方 pinned `viewer-static.min.js`）：视图切换、展开/折叠、lens 与展开状态正交、OUT 只灰不删、零人工修补 —— 全部 PASS（`build/viewer-harness.html`）。

> harness 说明：预览沙箱读不了 `/Volumes` 卷，测试时镜像到 `/tmp` 再起服务；普通环境直接 `python3 ../spike/verify/serve.py` 后打开 `http://127.0.0.1:8799/fcf-system-map/build/viewer-harness.html`。

## 7. SEMANTIC_OPEN（只记录，不填补）

| ID | 缺口 |
|---|---|
| SEMANTIC_OPEN-001 | 压缩阶梯其余层级（0.3.4 / Simplified V0 / FCF v1）的 per-node scope 归属未登记。0.3.4 主规格 21.3 万字符本轮只精读 §2 与 §4，不足以做逐节点归类而不编造。 |
| SEMANTIC_OPEN-002 | `SP.VIABILITY` 在 0.3.4.0-B 标 ACTIVE 是**部分**的：B P0 只交付 Temperature 组件，DO / Flow 不在 P0。 |
| SEMANTIC_OPEN-003 | 0.3.4.0-B 的 **Time Period** 在「直接进 Opportunity Fit」的语义下，于第一性主干上应落在哪一槽位（WHO.OPPORTUNITY？SP.HABITAT？独立槽位？）尚未由权威闭合。 |
| SEMANTIC_OPEN-004 | Behavioral Regime 轴尚未在图上显形——它只在 `Σ_r L_r C_r` 需要保存 `L_r ↔ C_r` 相关性时 materialize，本轮未确定用何种图元表达。 |
| SEMANTIC_OPEN-005 | 文档自述其 §2 有五张"观察面"（语义边界 / 生产执行 / 模块 Contract / Authoring→Runtime / Bass 实例）。本图目前只承载了语义边界这一面，其余四面的图元表达未设计。 |

## 8. 本轮不做的事

未重新裁算法公式；未修改任何 Notion / 飞书权威页；未读 FCF v1；未把 P哥原图并入；未开发独立 Web App（`build/viewer-harness.html` 仅加载 pinned 官方 viewer，可整体删除）；未扩展通用 Diagram Platform。

---

## 附：对齐草图（throwaway，`align/`）

`align/` 下是 2026-09-17 的对齐过程产物，**不是 canonical**，可整体删除：

| 文件 | 内容 |
|---|---|
| `align-topology-v0/v1.drawio` | 六行模块拓扑（v1 起支持行标折叠、数据/过程样式区分） |
| `align-midlevel-v2.drawio` | 按 Simplified V0 的 4.0–4.7 模块 Contract 对齐（后发现脊椎选错） |
| `align-firstprinciples-v3.drawio` | 换第一性主干：WHO/WHEN/RESOLVE + `q = Σ_r L_r × C_r` |
| `align-interaction-v4.drawio` | 压缩阶梯 + Interaction 下钻 + operator admission 表 |
| `notion-gov-findings.md` | 13 项 Notion 文档治理发现（只读观察，供治理对话） |

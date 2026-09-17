# FCF Canonical System Map（中鱼机制总图）

`generated/fcf-system-map.drawio` 是**构建产物**——永远不要手工编辑。改 source JSON 后重新生成。

```bash
python3 build/build_diagram.py     # 4 个 source JSON -> generated/fcf-system-map.drawio
python3 build/validate.py          # 全部静态检查 + 确定性 + rename 稳定性 + 中文标签
```

---

## 0. 本图的两个硬约束

**① 画在「整体框架」级别。** 七大层自上而下，只表达**流向、模块划分边界、输入输出边界**，不表达"哪个参数算出了下一层哪个参数"。最多表达到"哪几个参数算作一层，进入后面哪一层的前置条件"。

**② 每个格子必须有中文。** 英文只能作副标题。这条已由 `validate.py` **机器强制**（正则查 CJK 区），不靠人记。

## 1. 七大层

| 行 | 内容 | 可折叠 |
|---|---|---|
| 一、数据 | 环境上下文 · 钓场投鱼配置 · 鱼的习性配置 | ✓ |
| 二、烘焙 | 烘焙 → 派生环境场 → 空间分布权重 + 鱼侧动态参数 | ✓ |
| 三、玩家策略与操作数据 | 钓具 / 钓组 · 姿态 → 呈现刺激（左右偏右） | ✓ |
| 四、响应 | 响应模块（适配系数） | ✓ |
| 五、圆桌抽鱼 | 品质抽取调整 · 圆桌权重表构建 · 硬保底 · 动态权重调整 | ✓ |
| 六、抽鱼和生成 | 鱼种 · 品质 · 大小 · 重量 ｜ 鱼侧动态参数透传 | ✓ |
| 七、范围外 | 运行 Fish AI（刺鱼 / 博鱼） | ✗ 不折叠 |

折叠时**行内全部方块与所连箭头一起隐藏**；行标题即折叠手柄。

## 2. 术语与流向的两条修正（2026-09-17 Design Owner）

**① 术语。** 原「环境权重 / EnvironmentWeight」**已废弃**。现行术语是 **「空间分布权重 / spatial distribution weight」**——当前版本与远期规划**同名同概念**。旧文档可能尚未更新。

**② 流向。** 温度类环境事实**只流向烘焙**，在烘焙中转变为「空间分布权重」与「鱼侧动态参数」（活性 / 进食动机 / 食性偏好）；**温度不直接流向响应阶段**。图上的边按此绘制：

```
环境上下文 ─┐
鱼的习性配置 ─┴→ 烘焙 → 派生环境场 ─┬→ 空间分布权重 ──────────┐
                                    └→ 鱼侧动态参数 ─┐        │
钓场投鱼配置（基础机会强度）───────────────────────────┤        │
玩家策略与操作数据 → 呈现刺激 ─────────────────────────┼→ 响应 ─┤
                                                              ↓
                                                        五、圆桌抽鱼 → 六、抽鱼和生成 → 七、范围外
```

空间侧与鱼侧是**两条并行支路**，只在圆桌抽鱼（权重聚合）汇合一次——这是第一性分支「防重算」约束在图上的体现。

## 3. Source files

| 文件 | 职责 |
|---|---|
| `graph.json` | 24 个节点（stable ID + **中文 label** + 英文 caption + 行归属 + lane）+ 13 条语义边（只标"流过去的是什么"） |
| `scopes.json` | Scope = 压缩阶梯 + 透明度；`OVERALL`（不裁剪）+ `0.3.4.0-B`（lens，逐节点归类） |
| `views.json` | View = 展开粒度 + 可选 lens |
| `contracts.json` | 薄关联层：`semanticId → authorityRef / status / note` |

## 4. Scope 与透明度

**压缩阶梯**：`中鱼升级（本体）→ FCF v1 → Simplified V0 → 0.3.4 → 0.3.4.0-B（当前版本投影）`。每一层是范围更小的投影，不是不同系统。

**0.3.4.0-B** 是唯一登记完毕的 lens：**5 ACTIVE / 4 BOUNDARY / 15 OUT**。

- ACTIVE：`SYS`、`R2 烘焙`、`烘焙`、`派生环境场`、`空间分布权重`
- BOUNDARY：`R1 数据`、`环境上下文`、`钓场投鱼配置`、`鱼的习性配置`
- OUT：玩家策略行、响应行、圆桌行、生成行、范围外，以及 `鱼侧动态参数`（B 的「不交付」清单明确含 Fish Condition）

**透明度**是本轮新增：`OUT` 与 `BOUNDARY` 除着色外还被调暗（`opacity` 原生 action），**不隐藏、不移位**——空间记忆得以保留。

| 类别 | 配色 | 透明度 | 语义 |
|---|---|---|---|
| ACTIVE | 本色 | 1.00 | 本版实现 / 修改 |
| BOUNDARY | 本色 + 虚线 | 0.70 | 本版消费，不负责其内部 |
| OUT | 置灰 | **0.28** | 本版不处理（仍可读） |

> `0.28` 是**可调参数、不是机制主张**——原始规范要求「OUT 节点不要隐藏…仍保持上下文可读」，过暗会违反这条。下限建议不要再低。

## 5. Views

| 视图 | 动 Hierarchy? | 动 Scope 配色/透明度? |
|---|---|---|
| **总图**（默认） | 七大层全展开 | 清除 lens，恢复中性 + 全不透明 |
| **0.3.4.0-B** | **绝不触碰** | 应用 lens（范围外调暗但不隐藏） |
| **0.3.4.0-B 聚焦** | 收起本版不触及的行 | 应用 lens |

前两个是正交性示例；第三个是**组合预设**——即"只看这个版本"。想比较范围差异时用第二个（结构不动），想专注本版时用第三个。

## 6. Validation

```
stable IDs:            24 (unique, syntax-safe)
edges:                 13 semantic + 23 structural, endpoints ok
views:                 overall, 0340b, 0340b-focus (default overall)
scope lens:            0.3.4.0-B — 5 ACTIVE / 4 BOUNDARY / 15 OUT, all nodes classified once
ladder declared, unassigned: 0.3.4, SIMPLIFIED-V0, FCF-V1
contracts:             11 entries (refs valid)
determinism:           consecutive builds byte-identical; committed artifact fresh
rename stability:      cell ID set and geometry invariant under label rename
```

外加**中文标签检查**（每个 label 必须含 CJK，负向测试通过）。

官方 pinned viewer 运行时：七大层渲染、默认视图全展开、行折叠（连同所连箭头）、lens 着色 + 透明度（实测 ACTIVE `1.0` / BOUNDARY `0.70` / OUT `0.28`，全部仍 rendered）、零人工修补 —— 全部 PASS。

> harness：预览沙箱读不了 `/Volumes` 卷，测试时镜像到 `/tmp` 再起服务；普通环境 `python3 ../spike/verify/serve.py` 后打开 `http://127.0.0.1:8799/fcf-system-map/build/viewer-harness.html`。

## 7. SEMANTIC_OPEN（只记录，不填补）

| ID | 缺口 |
|---|---|
| 001 | 压缩阶梯其余三层（0.3.4 / Simplified V0 / FCF v1）的 per-node scope 归属未登记——不足的阅读量下归类等于编造 |
| 002 | 「空间分布权重」的 Current 归属页待登记（术语已确认，页面未确认） |
| 003 | 时段在第一性主干上的归向**已由 Design Owner 回答**（当前版本汇入空间分布权重；后续版本汇入 Activity + FeedingMotivation）——但 Design Owner 口述中还有第三个归向未能与文档对上，待确认 |
| 004 | 圆桌抽鱼四件（品质抽取调整 / 权重表构建 / 硬保底 / 动态权重调整）的 Current 归属页未读 |
| 005 | 环境上下文、钓场投鱼配置的 Current 归属页未读 |

## 8. 本轮不做的事

未重新裁算法公式；未修改任何 Notion / 飞书权威页；未读 FCF v1；未开发独立 Web App（`build/viewer-harness.html` 仅加载 pinned 官方 viewer）；未扩展通用 Diagram Platform。

---

## 附：对齐与历史（`align/`，throwaway，可删）

| 文件 | 内容 |
|---|---|
| `align-topology-v0/v1.drawio` | 六行模块拓扑（v1 起支持行标折叠、数据/过程样式区分） |
| `align-midlevel-v2.drawio` | 按 Simplified V0 的 4.0–4.7 模块 Contract 对齐（**后确认脊椎选错**） |
| `align-firstprinciples-v3.drawio` | 换第一性主干：WHO/WHEN/RESOLVE + `q = Σ_r L_r × C_r` |
| `align-interaction-v4.drawio` | 压缩阶梯 + Interaction 下钻 + operator admission 表 |
| `notion-gov-findings.md` | 13 项 Notion 文档治理发现（只读观察，供治理对话） |

历史脊椎（把 Simplified V0 模块链当主干）留 git 历史 `2d52879` / `4712903` 作 provenance。

# FCF Canonical System Map（中鱼机制总图）

`generated/fcf-system-map.drawio` 是**构建产物**——永远不要手工编辑。改 source JSON 后重新生成。

```bash
python3 build/build_diagram.py     # 4 个 source JSON -> generated/fcf-system-map.drawio
python3 build/validate.py          # 全部静态检查 + 确定性 + rename 稳定性 + 中文标签
```

## 常驻预览（改完立刻能看到）

在你**自己的终端**里跑一次即可（App 的 preview 启动器跑在沙箱里，读不了 `/Volumes` 卷；你自己的 shell 没有这个限制，所以不需要镜像到 /tmp）：

```bash
python3 fcf-system-map/tools/preview.py        # 默认 8799，可 --port
```

打开它打印的地址。之后：

- 任何 source 改动 → 服务在**下一次请求时自动重建**（`/api/version` 与取图都会触发）；
- 页面**每 2 秒轮询**产物哈希，一变就自动重绘 —— 不需要手动刷新，更不需要在我和你之间传文件；
- 进程活在**你的终端**里，不随任何一次会话结束而死。

实测：改 source 后仅靠轮询即可从 `776bfd0b…` 变为新哈希；服务产物与本地独立构建**逐字节一致**（确定性未被破坏）。

---

## 内容语义的权威在 Notion

**版面在这里迭代，含义在 Notion 固化。** 每个节点「要表达的意思」以
**《FCF 总图｜内容语义清单 R0｜Canonical Map Content Ledger》**为准
（挂 `Fish-Centric Conditional Funnel｜Design Branch Index` 下，
page `3dea4137-d236-81a3-92c2-d8574720eefa`）。

分工：

| | 归谁 |
|---|---|
| **含义** —— 每一层/每一块表达什么、流与边界、命名约定、待定项 | **Notion 清单**（权威） |
| **版面** —— 行带高度、横向展开 vs 纵向堆叠、是否接容器动态布局 | **本 repo**（自由迭代） |

两者冲突时：**改本 repo 去对齐 Notion**，不要反过来悄悄改含义。

---

## 0. 本图的三个硬约束

**① 骨架冻结在最初对齐草图 v1。** 总拓扑（行结构 / 每行并列方块 / 方块间连接 / 形状语义 / 行与方块的名字）来自 `align/align-topology-v1.drawio`，**已冻结**。后续只允许两类改动：

- **往骨架里加中下层内容**：caption、说明、scope 归类、view 预设、edge 类型与标签、contracts 关联、provenance；
- **更细致的 JSON source 与格式处理**：命名规范、`kind` 字段、校验规则、确定性、渲染与重叠检查。

骨架基线存在 `skeleton.baseline.json`，`validate.py` 每次构建都会比对——**骨架一变即 FAIL**，并提示这是一次需要与 Design Owner 重新对齐的事件。确需改动时走 `python3 build/freeze_skeleton.py` 显式重冻。

> 为什么会需要这条：漂移是渐进的——往 ① 行加一块「条件组」、把图例从形状说明换成 scope 三态，每一步单看都合理，合起来就把已对齐的结构改掉了。护栏已负向测试：加方块被拦、只改 caption 放行。

**② 画在「整体框架」级别。** 七大层自上而下，只表达**流向、模块划分边界、输入输出边界**，不表达"哪个参数算出了下一层哪个参数"。最多表达到"哪几个参数算作一层，进入后面哪一层的前置条件"。

**③ 每个格子必须有中文。** 英文只能作副标题。这条由 `validate.py` **机器强制**（正则查 CJK 区），不靠人记。

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
| `graph.json` | 71 个节点（stable ID + **中文 label** + 英文 caption + 行归属 + lane + `kind` 形状 + `band` 行带高）+ 24 条语义边（只标"流过去的是什么"） |
| `scopes.json` | Scope = 压缩阶梯 + 透明度；`OVERALL`（不裁剪）+ `0.3.4.0-B`（lens，逐节点归类） |
| `views.json` | View = 展开粒度 + 可选 lens |
| `contracts.json` | 薄关联层：`semanticId → authorityRef / status / note` |
| `skeleton.baseline.json` | **骨架基线**（冻结的 v1 拓扑指纹），由 `build/freeze_skeleton.py` 生成 |

## 4. Scope 与透明度

**压缩阶梯**：`中鱼升级（本体）→ FCF v1 → Simplified V0 → 0.3.4 → 0.3.4.0-B（当前版本投影）`。每一层是范围更小的投影，不是不同系统。

**0.3.4.0-B** 是唯一登记完毕的 lens：**17 ACTIVE / 8 BOUNDARY / 46 OUT**。

- ACTIVE：SYS / 行2 / 封面 / 烘焙 / 派生环境场 / **通道 1 及其全部分解**（核心·次要·排除·该通道的值 / 栖息地动态偏好 / 门控 / 通过·不通过）
- BOUNDARY：行1 及其三块与 L1 细节（B 消费的输入）
- OUT：通道 2–5（活性·进食动机·警戒度·动态进食偏好，全在 B 的「不交付」清单里）、行3–7 全域

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
前一个是纯 lens 示例（结构不动）；第二个是**组合预设**——上 lens 并收起本版不涉及的行，即"只看这个版本"。

## 6. Validation

```
stable IDs:            71 (unique, syntax-safe)
edges:                 24 semantic + 62 structural (root->row edges not drawn)
views:                 overall, 0340b (default overall)
scope lens:            0.3.4.0-B — 17 ACTIVE / 8 BOUNDARY / 46 OUT, all nodes classified once
ladder declared, unassigned: 0.3.4, SIMPLIFIED-V0, FCF-V1
contracts:             10 entries (refs valid)
determinism:           consecutive builds byte-identical; committed artifact fresh
rename stability:      cell ID set and geometry invariant under label rename
```

外加三项护栏，均已负向测试：**中文标签检查**（每个 label 必须含 CJK）、**顶点重叠检查**（任何两个方块碰撞即 FAIL）、**骨架漂移检查**（与 `skeleton.baseline.json` 比对，骨架一变即 FAIL）。

官方 pinned viewer 运行时：七大层渲染、默认视图全展开、行折叠（连同所连箭头）、lens 着色 + 透明度（实测 ACTIVE `1.0` / BOUNDARY `0.70` / OUT `0.28`，全部仍 rendered）、零人工修补 —— 全部 PASS。

> harness：预览沙箱读不了 `/Volumes` 卷，测试时镜像到 `/tmp` 再起服务；普通环境 `python3 ../spike/verify/serve.py` 后打开 `http://127.0.0.1:8799/fcf-system-map/build/viewer-harness.html`。

## 7. SEMANTIC_OPEN（只记录，不填补）

| ID | 缺口 |
|---|---|
| 001 | 压缩阶梯其余三层（0.3.4 / Simplified V0 / FCF v1）的 per-node scope 归属未登记——不足的阅读量下归类等于编造 |
| 002 | 「空间分布权重」的 Current 归属页待登记（术语已确认，页面未确认） |
| 003 | 时段归向**已闭合**：当前版本汇入空间分布权重；后续版本汇入 Activity + FeedingMotivation + **警戒度**（Design Owner 确认）。条目保留作 provenance |
| 004 | 圆桌四件的**语义已确认**（见 Notion 清单），但各自的 Current 归属页未逐一登记；其中「动态权重调整」的具体规则仍未细化 |
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

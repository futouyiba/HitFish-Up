# FCF Canonical System Map（中鱼机制总图）

`generated/fcf-system-map.drawio` 是**构建产物**——永远不要手工编辑。改 source JSON 后重新生成。

**版面是怎么定的、为什么这么定，见 [LAYOUT.md](LAYOUT.md)。** 那里记着实测出来的
引擎行为（水平容器是"高度汇"、宽度只能有一个来源且只撑**直接**子块）、折叠语义、
"横向=类别并列 / 竖向=执行顺序"这条语汇、以及**边的走位规则**（层级关系不画线；
出入口约束对平行四边形无效，跨行长边走左右空白走廊）。内容语义边界见下方“内容语义与版面职责”；本仓七页编辑器规范的权威分层见 [authority model](../docs/authority-model.md)。

```bash
python3 build/build_diagram.py     # 5 个 source JSON -> generated/fcf-system-map.drawio
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

## 人机共创：你手拖，我读懂

"我说你改"这条路是**有损**的 —— 你说"这个框往右一点"，我得猜是哪个框、往右多少。
你在 draw.io 里拖一下，落到磁盘上就是**精确的坐标变化**。这条回路把它翻译成我能
直接执行的清单。

三个文件，别混：

| 文件 | 谁动 |
|---|---|
| `generated/fcf-system-map.drawio` | 构建产物，**永远不要手改**（一重建就没了） |
| `working/baseline.drawio` | 快照：建工作副本时那份基线（对差的**参照系**） |
| `working/edited.drawio` | **你在这里改** |

```bash
python3 build/roundtrip.py init     # 建/刷新工作副本（已存在改动时会拒绝覆盖）
python3 build/roundtrip.py open     # 怎么打开它
#   → draw.io Desktop：open -a draw.io <path>   （或 app.diagrams.net → Open from → Device）
#   → 改完**存回同一路径**（Save / Cmd-S），别用 Save as 存到别处
python3 build/roundtrip.py status   # 一句话：改了几处
python3 build/roundtrip.py diff     # 结构化改动清单（--json 给机器读）
python3 build/roundtrip.py reset --force   # 丢掉改动、回到新基线
```

`diff` 的产出按"该改哪个源文件"分三类：

- **语义**（`added`/`removed`/`relabeled`/`reparented`/`reconnected`/`rerouted`）→ 改 `graph.json` / `layout.json` 的结构；
- **几何**（`moved`/`resized`）→ 声明式地块改 `layout.json`，一次性手摆改 overrides 层；
- **样式**（`restyled`/`visibility`）→ 先确认是不是有意的（多半是 lens 或临时试色）。

对差是**按 cell 语义**比的，不是文本 diff：draw.io 保存时会把整份文件重写
（属性顺序、视口的 `dx/dy` 都会变），文本 diff 全是噪声。忽略项由回归测试锁住：

```bash
python3 build/test_roundtrip.py     # 该抓的 8 类 / 该忽略的 2 类，逐一断言
```

**AI 侧的 MCP**：仓库根的 `.mcp.json` 登记了官方 `@drawio/mcp`（v1.6.0，7 个工具），
其中 `get_page` / `set_page` 读写本地 `.drawio` 文件的某一页、**自动解压** draw.io
默认的压缩页 —— 上面那条回路就是靠它们打通的。装上后需要**重启会话**才生效。

> 为什么不用实时协作平台（Excalidraw 房间之类）：那要放弃本图的**声明式布局 +
> 折叠语义**（`childLayout`、mxStackLayout 的自动让位）—— 而 Excalidraw 根本没有
> 布局引擎。实时共编换来的是把整张图退回自由画布重来。所以这里是**文件往返**，
> 不是实时共编；代价只是"你保存 → 我读到"这一拍，而这一拍很短。

---

## 内容语义与版面职责

**版面与已落成规范都在这里以 Git 版本管理；Notion 保留为 Owner 裁定、人工阅读和发布投影的载体。** 本仓七页编辑器规范的权威分层见[文档权威与发布投影](../docs/authority-model.md)。本总图自身的内容语义清单仍是独立的设计语义边界，不因七页编辑器规范的权威迁移而被悄悄改写。

分工：

| | 归谁 |
|---|---|
| **总图内容语义** —— 每一层/每一块表达什么、流与边界、命名约定、待定项 | 本图的语义清单与 Owner 裁定；仓内图源按 Git 管理 |
| **版面** —— 行带高度、横向展开 vs 纵向堆叠、是否接容器动态布局 | **本 repo**（自由迭代） |
| **Notion Current** | 人工阅读与发布投影，不成为本图仓内语义的第二个手工规范源 |

本图的语义清单与仓内图源发生冲突时，先报告冲突并请求确认；不得静默覆盖任一来源。

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
| 一、数据 | 环境上下文 · 钓场投鱼配置 · 鱼的习性配置 | ✗ 常显 section |
| 二、烘焙 | 烘焙 → 派生环境场 → 空间分布权重 + 鱼侧动态参数 | ✓ |
| 三、玩家策略与操作数据 | 钓具 / 钓组 · 姿态 → 呈现刺激（整体向右错开） | ✓ |
| 四、响应 | 响应模块（适配系数） | ✓ |
| 五、圆桌抽鱼 | 品质抽取调整 · 圆桌权重表构建 · 硬保底 · 动态权重调整 | ✓ |
| 六、抽鱼和生成 | 鱼种 · 品质 · 大小 · 重量 ｜ 鱼侧动态参数透传 | ✓ |
| 七、范围外 | 运行 Fish AI（刺鱼 / 博鱼） | ✗ 不折叠 |

**折叠 = 只留标题条。** 七大层各是一个真容器（`childLayout=stackLayout`），
标题条是常驻可见的第一个子块；收起该层时它下面的层**自动上移**，展开时下移。
层内再展开同样会让位 —— 因为重排沿「垂直容器的连续链」传播（见 §7）。
行三整体右缩 `marginLeft`，把左边 gutter 让给「派生环境场」，后者用 `movable=0`
钉在 gutter 里：不进栈、不计入行高，但随行三一起移动、随行三一起收起。

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
| `graph.json` | 73 个节点（stable ID + **中文 label** + 英文 caption + 行归属 + lane + `kind` 形状）+ 31 条语义边（只标"流过去的是什么"；跨模块的边锚在**模块标题**上，见 LAYOUT.md §6.4） |
| `layout.json` | **版面**：容器包纳树（`C:` 前缀的容器 + `graph.json` 节点作叶子；轴线 / 间距 / 缩进 / 侧钉 / 折叠态） |
| `scopes.json` | Scope = 压缩阶梯 + 透明度；`OVERALL`（不裁剪）+ `0.3.4.0-B`（lens，逐节点归类） |
| `views.json` | View = 展开粒度 + 可选 lens |
| `contracts.json` | 薄关联层：`semanticId → authorityRef / status / note` |
| `skeleton.baseline.json` | **骨架基线**（冻结的 v1 拓扑指纹），由 `build/freeze_skeleton.py` 生成 |

## 4. Scope 与透明度

**压缩阶梯**：`中鱼升级（本体）→ FCF v1 → Simplified V0 → 0.3.4 → 0.3.4.0-B（当前版本投影）`。每一层是范围更小的投影，不是不同系统。

**0.3.4.0-B** 是唯一登记完毕的 lens：**21 ACTIVE / 8 BOUNDARY / 44 OUT**。

- ACTIVE：行2 / 烘焙 / **通道 1 及其全部分解**（三种因子各自的形状 / 栖息地动态偏好 /
  门控与条件判断失败 / 汇聚漏斗：系数聚合 · 是否背景鱼 · 系数下限 · 权重聚合 · 通道返回值）
- BOUNDARY：行1 及其三块与 L1 细节（B 消费的输入）
- OUT：通道 2–5（活性·进食动机·警戒度·动态进食偏好，全在 B 的「不交付」清单里）、行3–7 全域

> 原先归在 ACTIVE 的 `SYS` 节点已删除（本图有页面标题，不需要一个代表"系统"的方块），
> `R2.C1.X`（忽略因子往下的一格）也随之删除——忽略因子往下什么都不做。

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
stable IDs:            73 (unique, syntax-safe)
edges:                 31 semantic (层级关系由容器嵌套表达，不再另画结构线)
views:                 overall, 0340b (default overall)
scope lens:            0.3.4.0-B — 21 ACTIVE / 8 BOUNDARY / 44 OUT, all nodes classified once
ladder declared, unassigned: 0.3.4, SIMPLIFIED-V0, FCF-V1
contracts:             9 entries (refs valid)
determinism:           consecutive builds byte-identical; committed artifact fresh
rename stability:      cell ID set and geometry invariant under label rename
```

外加三项护栏，均已负向测试：**中文标签检查**（每个 label 必须含 CJK）、**顶点重叠检查**（任何两个方块碰撞即 FAIL）、**骨架漂移检查**（与 `skeleton.baseline.json` 比对，骨架一变即 FAIL）。

官方 pinned viewer 运行时：七大层渲染、默认视图全展开、**折叠任一层时下方各层精确上移、展开时精确复原**（实测零漂移；折叠后该层高度恰为 `标题 24 + 2×border 10 = 44`，下方各行位移量恰好等于该差值）、lens 着色 + 透明度（实测 ACTIVE `1.0` / BOUNDARY `0.70` / OUT `0.28`，全部仍 rendered）、**零边穿方块**（逐段 polyline 与全部渲染方块求交，实测 0 处）、零人工修补 —— 全部 PASS。

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

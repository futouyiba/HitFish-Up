# 中鱼库文档治理发现｜来自 FCF 总图对齐轮（2026-09-17）

**来源**：为画 FCF Canonical System Map，本轮只读访问了以下页面。
**性质**：只读观察，未修改任何权威页；以下均为**治理建议**，不是机制变更请求。
**读取范围**（供核对）：中鱼机制 0.3.4 主规格、0.3.4.0-B 三页（开发需求 R0 / 固定模板分层烘焙 / Authoring & Resolve R0）、FCF Simplified V0 Working Main、Overall System Model v20、Mechanism Topology V2、Behavioral Regime × Bass 中层逻辑样板 v8。

---

## 一、重复（同一内容多处内联，存在漂移风险）

### G-01｜0.3.4.0-B 的「不交付」清单出现 4 次，条目数不一致
| 位置 | 措辞 | 条目数 |
|---|---|---|
| 开发需求 R0 §6 | 本版明确不交付 | 11 |
| 固定模板分层烘焙 §2.2 | 明确不包含 | 9 |
| 固定模板分层烘焙 §3 表 + §1 | 本版边界（分散） | — |
| Authoring & Resolve R0 §5 | 不出现的 Bake UI | 7 |

**影响**：读者无法判断哪份才是权威全集；四处各自演化后会出现"某页说不交付、另一页没说"的分歧。
**建议**：B 分支设一份 `0.3.4.0-B｜Non-Delivery Registry` 单页作唯一 Owner，其余三页只写一行指针。

### G-02｜聚合公式被内联复制两份
`CoreLoss / SecondaryLossRaw / SecondaryLossApplied / RawEnvCoeff` 这块公式在**开发需求 R0 §5** 与**固定模板分层烘焙 §6** 各出现一次，逐字重复。
两页都注明了 Working Owner 是 `3dca4137-…-5c88a0e56e15ceaf85`，但同时又各自内联了公式副本——**Owner 页更新后两处副本会静默漂移**。
**建议**：二选一 —— 只留 Owner 页内联、其余页引用；或明确这两页为公式的合法副本并在 Owner 页登记副本位置。

### G-03｜AggregationRole 硬规则重复 4 次
```
if aggregationRole != CORE:
    GatePolicy must be absent / NONE
```
出现在：开发需求 §4、固定模板 §5、Authoring & Resolve §2.2、Authoring & Resolve §2.3。
**建议**：合并为一条 Validator Rule 定义，各页引用编号。

### G-04｜「CORE / SECONDARY / EXCLUDED」语义说明重复 3 次
同一段角色语义（CORE 产 FactorFit+独占 Gate、SECONDARY 进 bounded aggregate 无 Gate、EXCLUDED 完全不消费）在开发需求 §4、固定模板 §5、Authoring & Resolve §2.2 三处逐条重述。

---

## 二、混乱 / 易误读

### G-05｜`Compat Mode` / `FishEngagementModeCompat` 命名极易被误读为"已实现 Engagement Mode"
B 分支明确"不做 Mode Share / Routing / condition-based mode selection""Runtime 不暴露 EngagementMode identity"，但反复使用 `Compat Mode`、`FishEngagementModeCompat`、`Engagement Mode compat shell`。
新读者（或 Agent）极可能据此认为 B 实现了 Engagement Mode——本轮我就差点这样归类。
**建议**：改名为带显式后缀的形态（如 `FishEngagementModeCompatShell`、`AffinityCompatView`），或在每个 B 页面页首加一句强提示「本页出现的 Mode 字样均为 legacy table 的兼容视图，不代表本版实现 Mode 语义」。

### G-06｜页面内嵌了被本页自己声明为"历史错误"的可视化
Authoring & Resolve R0 页首 callout 明确写：
> 紧随其后的 `Fixed Bake Editor R1` HTML embed 是 **pre-W4B historical reference**，不得作为当前 Owner / identity / Runtime contract。

即**页面正文内嵌了一个已被声明作废的 embed**，只靠文字警示。
**影响**：读者滚动到 embed 时警示已在屏幕外；Agent 抽取 embed 内容时会当作现行契约。
**建议**：契约变更时须同步"替换或卸载 embed"，并把这写入治理纪律（见 G-11）；对已作废的 embed 建议直接移除或搬到 Historical 子页。

### G-07｜Status 词汇无统一枚举
各页 Status 写法不一：
- `WORKING ALTERNATIVE / NOT PROMOTED｜W4B closure baseline｜2026-09-17`
- `Working Kernel Closed after Dual Adversarial Review / Ready for Use`
- `Working Mechanism Topology Candidate`
- `ACTIVE DESIGN BRANCH / WORKING`
- `LATEST NEXT-DESIGN BASELINE / WORKING / NOT PROMOTED`

**影响**：跨页比较状态需要逐页阅读自然语言，无法检索、无法统计、无法自动校验。
**建议**：定义 Status 枚举（如 `CURRENT / WORKING / CANDIDATE / HISTORICAL / REJECTED` × `PROMOTED / NOT PROMOTED`），并要求 frontmatter 化。

### G-08｜0.3.4.0-B 有两个同日 Checkpoint，均被导为"下一恢复入口"
- `Checkpoint｜0.3.4.0-B Fixed Template Contract × Bass Vertical Slice Prototype｜2026-09-16`（固定模板页页尾标为 "Latest Checkpoint"）
- `Checkpoint｜0.3.4.0-B Main Agent Control｜Contract Closure × Snapshot/Evaluator × Editor IA｜2026-09-16`（同页链接列表中列首位）

两者同日、语义重叠，无明确 current 指针。
**建议**：指定一个为 Current、另一个降级为 prior；或合并。

---

## 三、治理不足（机制层面）

### G-09｜跨分支无术语映射表（本轮最大摩擦源）
三个并列分支各有一套词汇，部分概念重叠但无对照：
| 第一性分支（中鱼升级｜） | Simplified V0 | 0.3.4.0-B |
|---|---|---|
| `L`（Native Supply） | 环境侧 Artifact / `EnvironmentWeight` | `FinalEnvCoeff` × Base |
| `C`（captureRetention） | Response / 响应度 | —（本版不做） |
| `Behavioral Regime` | `Engagement Mode` | `Compat Mode`（仅壳） |
| `ActualPresentation` | Presentation Signals | —（本版不做） |
| `q = Σ_r L_r × C_r` | `EnvironmentWeight × Response` | `Base × FinalEnvCoeff` |

V0 有一页 `英文术语—中文 Glossary R1`，但属 V0 分支。
**建议**：新增一份**跨分支术语映射表**（只做映射，不合并 authority），列为各分支阅读入口的第一步。

### G-10｜分支边界靠自然语言声明，无法机器校验
各页用 `sibling reference`／`不 supersede 任一分支`／`不自动成为 authority` 这类散文声明边界。没有结构化的 `branch_id` / `relation` 字段，因此**无法自动检测"A 分支文档被 B 分支当作 authority 引用"这类越界**。
**建议**：给页面加 frontmatter `branch:` 与 `relation:`（`supersedes` / `sibling` / `adopted-from`），配一条 lint：跨分支引用必须先有显式 `adopted-from` 记录。

### G-11｜缺少"契约变更必须同步可视化"的纪律
G-06 是这条纪律缺失的一个实例。当前治理页（`文档卫生与修订纪律`）覆盖了冻结/修订/回灌，但未覆盖 **embed / Figma / HTML 预览随契约变更的同步或卸载义务**。
**建议**：在 Write Hygiene 纪律中补一条：契约页变更时，页内 embed 必须同 PR/同批次同步；不能同步的须移至 Historical 并在正文移除。

### G-12｜页面尾部超长 `<page url=…>` 列表与正文 Drill-down Map 重复
`Overall System Model` 页尾约 55 条裸链接；`FCF Simplified V0 Working Main` 页尾亦有长表。这些与正文的 Drill-down Map / Progressive Reading 内容重叠，且无分组、无优先级、无状态标注。
**影响**：检索价值低（与正文重复）、维护成本高（新增页要往多处追加）、且容易与正文的推荐顺序矛盾。
**建议**：统一改为结构化索引（数据库视图或统一命名约定），正文只保留少量 high-signal 入口。

### G-13｜同一页内存在 4 处编号重复的章节号（疑似历史合并残留）
`Behavioral Regime × Bass 中层逻辑样板 v8` 页面中出现两次 `## 20.` 系列标题（`# 20. Mode Applicability × Finite Topology × Regime Projection` 与 `# 20. Closure Pass｜Bass V0 Middle-Layer Kernel`），各自还带 `## 20.1`–`## 20.10` 子编号。
**影响**：`§20.x` 这类引用在页内不唯一，交叉引用会指向歧义。
**建议**：重排编号或改为具名锚点（`§Kernel-Closure`、`§Mode-Applicability`）。

---

## 四、优先级建议（若要排期）

| 优先级 | 编号 | 理由 |
|---|---|---|
| P0 | G-05、G-06 | 直接导致读者/Agent 得出错误结论 |
| P0 | G-09 | 跨分支阅读的最大摩擦，且随分支增多会恶化 |
| P1 | G-01、G-02、G-03、G-04 | 漂移风险；已有 4 处副本，越晚收敛成本越高 |
| P1 | G-13 | 引用歧义，低成本可修 |
| P2 | G-07、G-08、G-10、G-11、G-12 | 结构性治理，建议与下一轮治理批次一起做 |

---

## 五、本轮未做的事（边界声明）

- 未修改任何 Notion / 飞书权威页；
- 未对机制本身提出变更请求——以上全部是**文档组织层面**的观察；
- 未读取 FCF v1 / Full Mechanism 分支（按 Design Owner 本轮指示跳过）；
- 观察基于 2026-09-17 当时的页面版本，若页面已更新需重新核对。

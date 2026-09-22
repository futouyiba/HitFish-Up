# #61 RoleControl 两入口同一真值｜目标态设计候选

**状态：离线候选，零 Figma 写入；不是最终源稿，不宣称画布已承接。** 本候选仅投影已定契约的八条验收能力，不反造数据模型、不扩展未裁 UI 细节。两入口、记录态、行级操作及错误态均标 `⚑UNIMPL（GAP 号待补）`／`⚐UNVERIFIED`，静态图不证明运行实现。

## §0 组登记

- 组名候选：`PROJECTION｜RoleControl 两入口／记录态／行级操作（四态）`
- 帧名前缀候选：`proj_role_1` … `proj_role_4`
- 建议载体：新建投影组，不修改 A①-卡1 Source Selector 既有组。
- 建议布局：2×2，沿既有 PROJECTION 裸帧范式；具体 y、宽高和邻组间距留给正式 fresh intake，不在候选中冻结绝对坐标。

## §1 帧清单与逐字文案

### 态1｜两入口同一 Policy Authoring Truth

验证：契约①双入口单 Truth；同一 Role 记录同时在组件卡入口与 Policy 区入口可见，不经同步代码。

```text
[st] RoleControl · 两入口同一真值
[rs] 组件卡 Role 下拉 ↔ Policy 区 Role 行：读取同一份 Policy Authoring Truth
[e1] 入口 A｜组件卡 Role 下拉
[e2] 入口 B｜Policy 区 Role 行
[n1] 修改一处，另一入口直接读同一 Truth；不维护两份 state
[label] 态1｜两入口同一 Truth
```

### 态2｜INHERIT 与同值 SET 记录态分离

验证：契约②④；Effective Role 可以相同，但记录态不能从值反推。

```text
[st] Role 记录态 · Effective Role 可相同
[rs] 同一 Effective Role ≠ 同一 authoring 记录
[r1] INHERIT｜无本层 op record｜跟随上层
[r2] SET CORE｜有本层 SET record｜Role 已钉住
[r3] Effective Role｜CORE（示意）
[n1] 不以最终值相同折成 no-op；不以值反推 INHERIT／SET
[label] 态2｜INHERIT 与同值 SET 可区分
```

### 态3｜行级粒度与显式批量

验证：契约③⑦⑧；明确正在改哪一层／哪一行，批量操作必须显式多选；Role 轴永不允许 ADD。

```text
[st] RoleControl · 行级编辑
[rs] 当前层｜物种层；当前行｜row_key=Fish_A / Mature（示意）
[r1] Role｜INHERIT → SET SECONDARY
[r2] 操作范围｜仅当前行
[multi] 批量修改｜先显式多选行，再执行批量动作
[n1] Role 操作不提供 ADD；INHERIT／SET 是记录态，不从最终值推导
[label] 态3｜当前层／当前行／显式批量
```

### 态4｜CORE／SECONDARY Profile 护栏与 IGNORED 空底板

验证：契约⑤⑥；选 CORE/SECONDARY 不自动建 Profile／选 Source；缺 Profile 立即 required-Profile ERROR 并阻断 Publish；IGNORED 空底板不投影。

```text
[st] Role 变更后的 Profile 护栏
[rs] Role｜IGNORED → CORE（示意）
[e1] required-Profile ERROR｜缺 Profile
[e2] Publish｜阻断到补齐 Profile
[n1] 不自动建 Profile；不自动选 Source；可进入 Setup
[n2] IGNORED 空底板不投影；CORE／SECONDARY 缺 Profile 必须阻断
[label] 态4｜Role 变更触发护栏，不自动补齐
```

> 文案中的 `row_key`、`CORE`、`SECONDARY`、`IGNORED` 均为契约已有术语；示意行值不构成生产读数。`INHERIT` 与 `SET` 的记录态不能以画面静态值证明已持久化。

## §2 annotation 计划

每帧局部短桥接：默认不超过两行、一个稳定规则直链；版本与必要取证按明确覆盖范围落批次说明，不逐条重复。状态标记保留；不把实现状态写成已通过。

### proj_role_1

```text
⚑UNIMPL（GAP 号待补）：组件卡与Policy区读取同一Policy Authoring Truth，不维护两份state。
→ 规则：https://github.com/futouyiba/HitFish-Up/blob/main/docs/review/ui-component-contract-r2/contract-cards.md#role-control
```

### proj_role_2

```text
⚑UNIMPL（GAP 号待补）：Effective Role 可相同，但INHERIT无记录与SET有记录必须可区分，不从值反推。
→ 规则：https://github.com/futouyiba/HitFish-Up/blob/main/docs/review/ui-component-contract-r2/component-contract-consolidated.md#role-record-intent
```

### proj_role_3

```text
⚑UNIMPL（GAP 号待补）：明确层／行；批量须显式多选；Role 轴不提供ADD。
→ 规则：https://github.com/futouyiba/HitFish-Up/blob/main/docs/review/ui-component-contract-r2/contract-cards.md#role-control
```

### proj_role_4

```text
⚑UNIMPL（GAP 号待补）：CORE/SECONDARY缺Profile立即报错并阻断Publish；不自动建Profile或选Source，IGNORED空底板不投影。
→ 规则：https://github.com/futouyiba/HitFish-Up/blob/main/docs/review/ui-component-contract-r2/contract-cards.md#role-control
```

## §3 契约映射

| 验收轴 | 帧 | 契约依据 | 投影表达 |
|---|---|---|---|
| 两入口同一 Truth | 态1 | `contract-cards.md#role-control`；`component-contract-consolidated.md#role-record-intent` | 组件卡入口与Policy区入口并列，写同一Truth，不画第二份state |
| INHERIT／同值SET记录态 | 态2 | `component-contract-consolidated.md#role-record-intent` | 无记录与有SET并列，即使Effective Role相同 |
| 当前层／当前行 | 态3 | `contract-cards.md#role-control` | 层、行、作用范围显式显示 |
| 显式批量／无ADD | 态3 | `contract-cards.md#role-control` | 多选后批量；Role轴不出现ADD |
| 不自动建Profile／不自动选Source | 态4 | `contract-cards.md#role-control` | 明示否定，不把Setup当自动接线 |
| CORE／SECONDARY required-Profile | 态4 | `contract-cards.md#role-control` | ERROR与Publish阻断同态可见 |
| IGNORED空底板 | 态4 | `contract-cards.md#role-control` | 空底板不投影的状态说明 |

## §4 验收判据

1. 四态齐备，组名含「RoleControl」与「四态」；各帧 label 与态标题对应。
2. 态1同时出现组件卡 Role 下拉与 Policy 区 Role 行，并以同一 Truth 说明连接；不得出现两份独立 state。
3. 态2同时出现 INHERIT（无本层 op record）与 SET（有本层 SET record）；Effective Role 可相同但记录态不同。
4. 态3显式显示当前层与当前行；批量动作有显式多选语义；文本与控件中 Role 轴 `ADD` 命中为0。
5. 态4明确 CORE／SECONDARY 缺 Profile 的 required-Profile ERROR、Publish 阻断、Setup 出口；不出现自动建 Profile／自动选 Source 的正向接线；IGNORED 空底板不投影。
6. 四帧 annotation 均短形、单稳定链接、`⚑UNIMPL`／`⚐UNVERIFIED` 标记按源稿保留；版本与取证由批次说明登记，不把静态图当运行证据。
7. 写入前需保存目标组、上下邻组、可能共用母件的 durable before 快照；写后整组回读并报告文本、annotation、几何、节点增量和 flag。
8. 当前候选不改变 A①-卡1、N2、卡10、卡11或共享母件；正式 writer 必须声明文件级写集与实例射程。

## §5 冲突清单

- **R1｜新建范围**：RoleControl 当前目标页没有可命中的既有成组投影；本候选是新建投影，不把卡1 badge 当成已承载八条能力。
- **R2｜运行实现证据**：Role 持久读写、双入口同Truth的运行态、Profile required 阻断均不能由静态图证明；标 `⚑UNIMPL`／`⚐UNVERIFIED`。
- **R3｜行级与批量的未裁UI细节**：多选控件、入口具体位置、错误面板尺寸与视觉组件未由契约裁定；本稿只表达验收语义，不冻结控件外形。
- **R4｜示意值**：row_key、Role值与错误数量均为示意，不构成生产读数。

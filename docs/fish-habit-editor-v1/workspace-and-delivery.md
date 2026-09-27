# Fish Habit Editor V1｜Workspace & Delivery Contract

> Status: Current Workspace / Delivery Contract for V1.0  
> Scope: 定义开发宿主、发布宿主、Authoring / Production 两个 Git working tree、文件边界与 Publish 的本地物化语义。本文不重新定义 Fish Habit Authoring / Resolve / Materialization 业务语义。

## 1. 一句话模型

V1.0 是一个 **本地工作区型编辑器**：

```text
开发阶段：Web Dev Server
发布阶段：Electron Desktop App

                    Fish Habit Editor
                           │
                      WorkspaceRoot
                    ┌──────┴──────┐
                    ↓             ↓
              authoring/      production/
                .git/            .git/
          Editor Authoring    Production Tables
               Truth          Working Tree
                    ↑             ↑
             daily Edit/Resolve   Publish / Verify
                    │             │
                    └─ explicit Import/Bootstrap ─┘
```

Authoring 与 Production 是两个**独立的 sibling Git working tree / repository directory**。它们都保留自己的 Git metadata，用于 pull / diff / commit / merge / history；Habit Editor 不把两者合并成同一个 repo。

关键方向性：

- 普通 Edit / Resolve / Source resolution 只消费 `authoring/`；
- Publish / Production baseline verify 读写 `production/`；
- 显式 Import / Bootstrap 可以读取 `production/`，但必须先把需要承接的数据冻结进 `authoring/`，之后普通 Authoring 不再实时依赖原 Production row。

## 2. 发布包目录

V1.0 portable release 采用一个 ZIP 分发包，解压后保持三个 sibling：

```text
FishHabitEditor-v1/
├─ app/
│  └─ FishHabitEditor.exe / FishHabitEditor.app / Electron runtime
│
├─ authoring/
│  ├─ .git/
│  └─ <current canonical Editor JSON / future CSV set>
│
└─ production/
   ├─ .git/
   ├─ FishEnvAffinity.*
   ├─ TemperatureProfile.*
   ├─ StructureProfile.*
   ├─ FeedingLayerProfile.*
   └─ TimePeriodProfile.*
```

具体 Production 文件名 / 扩展名服从当前真实 Production schema；上图只表达物理边界。

硬规则：

- Electron app / `app.asar` 视为可替换的程序产物；
- 可变 Authoring Truth 不塞进 app binary / `app.asar`；
- Production tables 不塞进 app binary / `app.asar`；
- release ZIP 必须保留 authoring / production 两个目录的 Git metadata；
- V1.0 使用固定 sibling workspace layout，不新增 Workspace Project Manager / 多工作区注册表。

## 3. Authoring working tree

`authoring/` 是 Editor durable Authoring Truth 的物理工作区。

V1.0：

- canonical persistence 继续使用当前 JSON Editor State；
- Autosave / staged mutation confirm 修改的是 authoring working tree；
- 后续若 Authoring persistence 演进为多 CSV，仍留在同一个 authoring working tree 边界内；
- JSON → CSV 不是 V1.0 交付前提；
- Git history / diff 用于协作与恢复，但 Git commit 不是 Editor durable revision 本身。

Editor 不自动替作者执行：

- `git pull`；
- `git commit`；
- `git push`；
- branch / merge / conflict resolution。

这些继续交给 Git CLI、IDE、Coding Agent 或其它成熟 Git 工具。

## 4. Production working tree

`production/` 是当前生产表的本地 working tree，也是 Publish 的 materialization target。

Publish 的产品语义是：

> **把绑定的 exact Authoring durable revision 物化到 Production working tree，并 reread / verify。**

不是：

> Deploy 到服务器。

因此典型协作链：

```text
同步 authoring / production Git working tree
→ 打开 Editor
→ 修改 Authoring
→ Resolve / Validation
→ Publish
→ production working tree 产生文件 diff
→ 使用 Git 检查 / commit / merge / push
```

V1.0 Editor 不内置 Git client，也不把 commit / push 作为 Publish 成功条件。

Production generation / baseline guard 仍以**实际文件内容 / canonical generation**为正确性依据；不能只用 Git HEAD 是否变化替代 whole-output verification，因为 working tree 可能存在未提交修改。

## 5. Dev Host 与 Electron Host

UI / domain core 不为 Web 与 Electron 写两套。

两种 Host 必须解析到同一种 Workspace 语义：

```text
WorkspaceRoot
├─ authoring/
└─ production/
```

- Dev Server：通过启动配置 / 环境参数显式获得 `WorkspaceRoot`；
- Electron：从 release workspace 解析同一个 `WorkspaceRoot`；
- Editor Domain 不直接依赖 `process.cwd()`、源码目录或 Electron app path 来猜数据位置；
- Host 只负责把 `authoringRoot` / `productionRoot` 暴露给统一 Workspace API。

推荐宿主边界：

```text
Renderer / Web UI
      ↓
Editor Domain Core
      ↓
Workspace API
   ┌───────────────┐
   ↓               ↓
Dev adapter     Electron adapter
local dev       preload / IPC
server              ↓
   └──────── local filesystem ────────┘
```

开发阶段可由本地 Web Dev Server 提供 Workspace File API；release 阶段由 Electron main/preload 提供等价的本地文件能力。

正常 Editor 启动首先打开 `authoringRoot`。只有进入 Publish / Production verify / 显式 Import-Bootstrap 边界时才访问 `productionRoot`。

Resolver / Validator / Source semantics / Materializer / Publish transaction 必须共享同一 domain implementation；Host adapter 不重新解释业务语义。

## 6. 两个 Git working tree 的职责边界

```text
authoring/
  保存作者意图
  Source binding / operation / Template / Policy / Editor metadata

production/
  保存物化结果
  FishEnvAffinity / Component Profile / Production physical rows
```

禁止：

- 从 Production output 自动反推并覆盖 Authoring Truth；
- Publish 自动 commit 任一 repo；
- 把两个 repo 合并为一个事务性 Git commit 并作为 V1.0 正确性前提；
- 因 Electron 打包而复制出第三份 mutable Authoring / Production truth。

Git 是协作与版本管理基础设施；Editor revision / Publish verify 才是产品事务语义。

## 7. 显式 Import / Bootstrap 与 Imported Source Snapshot

Production working tree **不是普通 Authoring Source Store**。

过渡期若需要继续使用既有 Production Profile，流程必须是：

```text
production/ 中既有 row
        ↓
explicit Import / Bootstrap
        ↓
authoring/ 中 Imported Source Snapshot
        ↓
普通 Source Picker / Resolve
```

Imported Source Snapshot：

- 是 Authoring durable state 的一部分；
- 保存冻结的完整 Source value；
- 保留原 Production 英文 `name`、原 row identity / generation 等 provenance；
- 日常 binding 指向 Authoring 内稳定 snapshot identity；
- Production working tree 后续变化不会自动改变 snapshot；
- 如需更新，必须再次经过显式 Import / Bootstrap / Reconcile。

因此 V1.0 的三条数据通道是：

```text
A. 日常 Authoring
authoring/ ↔ Editor

B. Publish / Verify
authoring/ → Materializer → production/
                           ↘ reread / verify

C. 显式 Import / Bootstrap
production/ → importer → authoring/
```

C 不得隐式混入 A。Source Picker 不扫描 `production/`，Publish 生成的新 managed row 也不会自动回流为新的 Source Snapshot。

## 8. Workspace 启动检查

Host 解析出 `WorkspaceRoot` 后做最小 preflight：

1. `authoring/` 存在且可读取；
2. canonical Authoring persistence 可识别；
3. `production/` 若当前要执行 Publish / Verify / Import，则必须存在且可读取；
4. 对需要写入的事务检查对应目录可写。

`.git/` 用于正常团队协作与发布包交付，但 **Git metadata 本身不是 Authoring / Publish 语义真相**。实现不得用 Git HEAD 替代 Editor revision 或 whole Production verification。
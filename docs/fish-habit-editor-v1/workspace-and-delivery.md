# Fish Habit Editor V1｜Workspace & Delivery Contract

> Status: Current Workspace / Delivery Contract for V1.0  
> Scope: 定义开发宿主、发布宿主、Authoring / Production 两个 Git working tree、文件边界与 Publish 的本地物化语义。本文不重新定义 Fish Habit Authoring / Resolve / Materialization 业务语义。

## 1. 一句话模型

V1.0 是一个 **本地、单机单写者工作区型编辑器**：

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
```

Authoring 与 Production 是两个**独立的 sibling Git working tree / repository directory**。它们都保留自己的 Git metadata，用于 pull / diff / commit / merge / history；Habit Editor 不把两者合并成同一个 repo。

方向性固定为：

- 普通 Edit / Resolve / Source Picker 只消费 `authoring/`；
- Publish / writeback / touched-output verify 访问 `production/`；
- 如需从旧 Production 承接数据，由 Editor 外的数据准备流程先写入 / 更新 `authoring/`；
- `production/` 不是普通 Authoring Source Store。

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
- Git history / diff 用于人与人之间的协作与恢复；Editor 自身不实现协同 revision protocol。

Editor 不自动替作者执行：

- `git pull`；
- `git commit`；
- `git push`；
- branch / merge / conflict resolution。

这些继续交给 Git CLI、IDE、Coding Agent 或其它成熟 Git 工具。

## 4. Production working tree

`production/` 是当前生产表的本地 working tree，也是 Publish 的 materialization target。

Publish 的产品语义是：

> **把当前本机最近一次成功保存的 Authoring state 非破坏性物化到 Production working tree，并 reread / verify 本次 touched output。**

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

Execute 时重新读取当前本地 Production working tree，作为本次 patch 的输入。V1.0 不维护 Editor 内的 whole-generation baseline / 外部修改合并协议。若作者通过 Git 或其它工具修改了文件，应在继续编辑 / Publish 前显式 reload workspace。

## 5. Dev Host 与 Electron Host

UI / domain core 不为 Web 与 Electron 写两套。

两种 Host 必须解析到同一个 Workspace 语义：

```text
WorkspaceRoot
├─ authoring/
└─ production/
```

- Dev Server 通过启动参数 / 环境配置显式获得 `WorkspaceRoot`；
- Electron 从 release workspace 解析同一个 `WorkspaceRoot`；
- Editor Domain 不依赖 `process.cwd()`、源码目录或 Electron app path 猜数据位置；
- Host 只向统一 Workspace API 提供 `authoringRoot` / `productionRoot`。

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

正常 Editor 启动只需要打开 `authoringRoot`。执行 Publish / verify 时再访问 `productionRoot`。Production → Authoring 的承接属于 Editor 外的数据准备边界，不混入普通 Source resolution。

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

Git 是协作与版本管理基础设施；Editor 只负责当前本机 session 的保存、Resolve 与 Publish verify。

## 7. Authoring 兼容数据与 Production 的边界

Production working tree **不是普通 Authoring Source Store**。

V1.0 只要求：若作者需要继续使用历史 Production 中的某些 Profile，这些可用数据在进入普通 Editor 前已经存在于 Authoring persistence 中。

```text
Editor 外的数据准备
        ↓
authoring/ 中已有兼容数据
        ↓
普通 Source Picker / Resolve
```

这里不定义新的兼容源 Asset 或 Import transaction。具体 Authoring 文件结构沿用当前实现；如果当前已有冻结 input JSON / snapshot 文件，也继续作为 Authoring persistence 的一部分使用即可。

因此 V1.0 的运行时数据方向是：

```text
日常 Authoring
authoring/ ↔ Editor

Publish / Verify
authoring/ → Materializer → production/
                           ↘ reread touched output
```

Production → Authoring 不是普通运行通道。Source Picker 不扫描 `production/`，Publish 生成的新 row 也不会自动成为 Source。

## 8. Workspace 启动检查

Host 解析出 `WorkspaceRoot` 后：

1. `authoring/` 必须存在且 canonical Authoring persistence 可读取；
2. 普通 Edit / Resolve 不要求读取 Production Source catalog；
3. 执行 Publish 时 `production/` 必须存在，并按当前事务要求可读 / 可写；
4. `.git/` 服务团队协作，但 Git metadata 不是 Editor Truth，也不是 Publish verify 的替代品。
# Fish Habit Editor V1｜Secondary Surfaces

> Status: Current Surface Contract for V1  
> 本文收敛 Fish Subject 主 Authoring 之外的 V1 产品面：Resolve Preview 与 Publish。Shared Template 独立由 [shared-assets.md](shared-assets.md) 承担。

## 1. Resolve Preview｜解析预览

### 1.1 产品职责

解析预览回答一个问题：

> **当前已经成功保存的 Authoring Truth，最终解析成什么；如果结果不直观，为什么会得到这个结果？**

它不是：

- 第二套只读 Editor；
- Candidate before/after；
- Bake / 条件组求值；
- Runtime / evaluator trace；
- Production materialization debug；
- 必须逐项 Review 完成的审批流程。

解析预览只读、无 durable mutation，也不形成 reviewed / approved 状态。

### 1.2 与 Authoring 的关系

同一个 Fish Subject 只有两个长期工作视角：

```text
[ 编辑 ] [ 解析预览 ]
```

左栏 Subject Navigation 在两种视角中保持一致。

- 作者在 Resolve 中切换 Fish / 基础习性 / Mode 时，保持“解析预览”视角；
- Subject 变化后，右栏 Resolve Focus 清空，避免把旧 Subject 的 detail 静默映射到新 Subject；
- 从 Edit → Resolve 时，如果当前 Focus 属于同一 Subject 且可映射到 Component / Field / Policy，可保留 focus identity；
- 如果 Edit Focus 处于 Detached 状态，进入 Resolve 时不保留 detached focus；
- 从 Resolve 右栏执行“在编辑中打开”时，切回 Edit，并定位同一 Component / Field / Policy。

Resolve Preview 是可选检查面；Publish 不要求作者先打开或逐项看完 Resolve。

### 1.3 进入 Resolve 的 durable 边界

Resolve 只消费**最近一次成功持久化的 durable revision**。

进入规则：

1. **staged candidate active**：不能进入 Resolve；先确认或取消 Candidate。
2. **Autosave pending**：先 flush / 等待当前 typed edit 写盘，再进入 Resolve。
3. **Autosave failure**：保持在 Edit，不把旧 durable state 冒充作者刚刚修改后的 Resolve。
4. **incomplete raw input**：按 Authoring Surface 的 transient 规则丢弃，不写 durable；可用轻量提示说明“未完成输入未包含在解析预览”。
5. **Validator ERROR / WARNING**：不阻断进入 Resolve。Resolve 正是定位结果与诊断的重要只读面。

### 1.4 三栏承载

```text
Subject Navigation | Resolved Overview | 解析说明
我在看谁？           最终生效成什么？      为什么是这个结果？
```

Global Topbar 继续只显示全局 Editor 状态和 Publish，不增加第二套 Resolve 全局导航。

Context Header 仍使用当前 Subject breadcrumb：

```text
鱼习性 › 大口黑鲈 › 中鱼习性模式 › 大个体 [兼容]     [编辑] [解析预览]
```

### 1.5 中栏：Resolved Overview

中栏保持与 Edit 相同的稳定空间映射：

```text
[ Temperature ] [ Structure ]
[ Feeding     ] [ Time      ]

[ Spatial Opportunity Policy ]
```

但内容变成**最终解析结果**，不复制 Authoring controls。

Component Card 示例：

```text
结构习性                           角色·CORE  ⛔

最终来源
Heavy Cover

Rock        0.80
Weed        1.20
Wood        0.60
Grass       0.40
```

Resolve Card 不显示 Source dropdown、本层 Operation dropdown、ADD / SET 参数输入，也不把“有本层调整 / 沿用底板”当主要信息。

Policy 示例：

```text
空间机会策略

有效策略来源   Predator Policy

温度          CORE
结构          CORE
觅食水层      SECONDARY
时段          IGNORED

fail_env_coeff   0.015
```

### 1.6 Component-specific resolved representation

Resolve 不强迫四个 Component 都长成同一张数值表。

- **Structure / Feeding Layer / Time Period**：按稳定业务字段顺序展示最终值。
- **Temperature**：展示最终六参数；当参数满足曲线定义所需不变量时，可同时显示只读曲线作为结果理解辅助。若参数非法到无法形成合法曲线，则保留真实参数与诊断，不绘制自动修正后的假曲线。曲线不能 author，也不能演变成 Bake。
- **Policy**：展示四个 Effective Role + Effective fail_env_coeff。

Resolved representation 只解释当前最终配置，不引入天气、时段 snapshot、Base Opportunity 或任何 Bake input。

## 2. 右栏：解析说明

右栏不是“完整 provenance debugger”，而是对当前 Focus 的**最短充分因果解释**。

用户语言优先：

```text
解析说明
最终结果
来源
操作
为什么
```

不要求普通作者理解 durable token 名、row key 或 materializer 结构。

### 2.1 Resolve Focus states

V1 Resolve 右栏只有：

1. **Empty**：提示“选择一个组件、字段或策略项查看解析说明”。
2. **Component Detail**：解释该 Component 的 Effective Source relation，并列出字段结果及其主要 operation origin。
3. **Field Detail**：解释一个字段从 Source value 到 Effective Value 的完整最短链。
4. **Policy Detail**：解释 Role / fail_env_coeff 的 Template → Species → Mode → Effective 链。

Resolve 中不需要 Authoring 的 Detached 状态；Subject 变化直接清空 Resolve Focus。

### 2.2 数值字段的最短充分解释

Species Base 示例：

```text
解析说明 · Structure / Rock

最终值
0.80

来源
Heavy Cover
来源值 1.00

本层操作
调整 -0.20

结果
1.00 + (-0.20) = 0.80
```

Compat Mode：Source pin + 继承 Species operation：

```text
解析说明 · Structure / Rock

最终值
0.40

来源
本模式设置 → Rock Cover
来源值 0.60

操作
沿用基础习性 → 调整 -0.20

结果
0.60 + (-0.20) = 0.40
```

Compat Mode CLEAR：

```text
最终值
0.60

来源
本模式设置 → Rock Cover
来源值 0.60

基础习性操作
调整 -0.20

本模式意图
仅用当前来源
→ 已取消基础习性操作

结果
0.60
```

SET：

```text
最终值
0.90

来源值
0.60   （被本层“设置为”覆盖）

本模式操作
设置为 0.90

结果
0.90
```

当前态可以说明“最终操作是 SET / Source value 被 SET 覆盖”；不能在没有 before/after 输入时声称“换源后结果未变”。

### 2.3 Source 与 Operation 是两条独立解释轴

Resolve Detail 必须保持：

```text
Effective Source relation
+
Effective Operation relation
→ Effective Value
```

不能把“跟随基础习性 Source”和“沿用基础习性 Operation”压成一个模糊的“继承”。

### 2.4 Policy Role 解析说明

Species Base：

```text
解析说明 · Structure Role

策略模板
Predator Policy → SECONDARY

基础习性意图
设置为 CORE

最终角色
CORE
```

Compat Mode inherit：

```text
策略模板
Predator Policy → SECONDARY

基础习性
设置为 CORE

本模式
沿用基础习性角色

最终角色
CORE
```

Compat Mode CLEAR：

```text
策略模板
Predator Policy → SECONDARY

基础习性
设置为 CORE

本模式
使用策略模板原始角色
→ 已取消基础习性 Role override

最终角色
SECONDARY
```

不直接向作者展示 absent / CLEAR / SET durable token；显示作者语言。

### 2.5 fail_env_coeff 解析说明

复用同一因果表达：

```text
策略模板原始值
0.010

基础习性
调整 +0.005
→ 0.015

本模式
使用策略模板原始值

最终值
0.010
```

不把它做成单独的计算调试器。

### 2.6 Tier / metadata

如果某个最终 operation 具有作者需要理解的 Tier / metadata，可在对应 operation 下弱显示。

Tier 不作为独立 Resolve 层，不重新组织导航。

## 3. Partial Resolve｜部分解析

Resolve Preview 不采用“一个 ERROR → 整页失败”。每个 Component / Policy 独立表达当前可解析程度。

### 3.1 Resolved

正常显示 final source / value / role。

### 3.2 Resolved with diagnostics

例如 Effective Value 数值已可计算，但违反 Validator：

```text
Rock   -0.10   ⛔
```

仍显示真实 resolved value，同时显示 Error。Publish 是否阻断由 Diagnostic 决定。

### 3.3 IGNORED + Profile present

显示 Profile 的 resolved values，并标明：

```text
角色·IGNORED
当前不参与空间机会计算
```

Profile 不删除，也不禁用查看。

### 3.4 IGNORED + Profile absent

这是合法空态：

```text
结构习性               角色·IGNORED

未配置习性档案
当前角色为 IGNORED，因此无需 Profile
```

不得伪造 0 值 Profile。

### 3.5 CORE / SECONDARY + Profile absent

该 Component 无法完整 Resolve：

```text
结构习性               角色·CORE  ⛔

无法解析
缺少必需的习性档案
```

其它 Component 继续正常解析。

### 3.6 Broken Source

显示明确的“来源缺失”与 blocking diagnostic；**展示 Resolver 实际仍能产出的部分结果，但 UI 不自行推导或补算。**

若 Resolver 无法给出该字段 / Component 的 Effective 结果，则显示“无法解析”；不得因为某个字段看起来存在 SET 就由 UI 自己假设它可以绕过 broken source。

不 fallback 到基础习性 / 默认 Template / 最近似 Source。

### 3.7 Cross-field invalid but numerically resolvable

例如 Temperature 边界顺序非法，但各字段已有完整数值：

- 显示实际 resolved 参数；
- 显示跨字段 Error；
- 不自动排序、修复或画一条假装合法的修正曲线。

## 4. 从 Resolve 回到 Authoring

Resolve 中不直接修数据。

右栏 Detail 提供唯一低成本导航动作：

```text
[在编辑中打开]
```

行为：

- 保持当前 Fish Subject；
- 切换到“编辑”；
- Focus 对应 Component / Field / Policy；
- 不产生 mutation。

对于缺 Profile / broken source 等 Component-level 问题，同一动作落到对应 Component 的 Edit Focus / Source 路径。

中栏每个 resolved row 不重复放“编辑”按钮，避免 Resolve 变成第二套 Editor。

## 5. Resolve 与 Diagnostics

Resolve 使用与 Authoring 相同的一份 derived Diagnostic，不新建 Resolve-specific error truth。

Diagnostic 可投影到 resolved field、resolved Component Card、Policy、Global Validation List。

Resolve Detail 可以解释“为什么当前无法解析 / 为什么 Publish 会阻断”，但不改变诊断判级。

## 6. 不进入 V1 Resolve 的信息

明确不显示：

- Pond / FishRelease / StockRelease Context；
- Quality；
- Mode Share / Routing；
- Weather / Time / Structure condition snapshot；
- Base Opportunity / Background Fish；
- Bake result；
- Gate trace / evaluator execution trace；
- materialized production row name / row key；
- runtime formula editor；
- before/after change history；
- “来源已变”这类需要历史快照才能证明的陈述。

V1 Resolve 的停止线：

> **解释 Authoring Truth 如何解析成当前 Effective Configuration；不解释这个配置放进某场景后会算出什么。**


## 7. Publish｜发布到生产配置

### 7.1 产品职责

V1.0 Publish 的职责只有一件事：

> 把当前本机最近一次成功保存的 Authoring Truth，非破坏性物化到本地 Production Git working tree，并重新读取本次 touched output 验证一致。

它不是部署到服务器，也不是 Git 客户端。

多人之间的 pull / diff / merge / commit / push 由工作区外部 Git 工具负责，Fish Habit Editor 不实现协同编辑或 Git merge。

### 7.2 进入 Publish Surface

Topbar 提供：

```text
[发布到生产配置…]
```

进入独立 Publish Surface。若当前存在：

- incomplete raw input；
- Autosave pending；
- Autosave failure；
- staged Candidate active；

则先完成 / 取消当前本地编辑，再进入 Publish。

Validator ERROR 可以进入 Publish Surface查看 blocker，但 executor 禁用；WARNING 不阻断。

### 7.3 Preflight

V1.0 只保留两个 Gate。

#### Gate A｜编辑器状态

```text
编辑器状态
✓ 已完成保存
```

要求：

- 当前 Authoring 已成功写入本地 durable state；
- 没有 incomplete raw input；
- 没有 save failure；
- 没有 staged candidate。

#### Gate B｜发布校验

对当前 saved state 执行完整 validation / materialization-readiness check。

```text
发布校验
✓ 0 个阻断错误
  3 个警告
```

Blocking ERROR 包括 schema / semantic validation、required Profile 缺失、broken source、Production naming collision 等当前 Validator / Materializer 已知 blocker。

点击 Execute 时重新读取当前本地 Production working tree，作为本次非破坏性 patch 的输入。

### 7.4 Preflight layout

中栏：

```text
发布到生产配置

发布范围
当前 Fish Habit Editor 全量习性配置

✓ 编辑器状态
✓ 发布校验
  0 Error · 3 Warning

警告
...

阻断项
...
```

右栏：

```text
发布操作

当前状态
可以发布

[发布到生产配置]
[返回编辑器]
```

不再额外弹第二层确认 Modal。

### 7.5 Execute

所有 Gate PASS 后：

1. 锁定当前 App 的 Authoring mutation；
2. 读取当前 Production working tree；
3. Materializer 生成本次明确需要 create / update 的 rows；
4. 非破坏性写入；
5. 重新读取本次 touched output；
6. verify；
7. 解锁 Editor。

V1.0 不处理另一 Editor 会话同时修改 Authoring state，也不实现 revision R / R+1 协同协议。

### 7.6 Non-destructive patch

Publish 只 create / update 明确目标 rows。

- 其它 Production rows 原样保留；
- 不做 orphan GC；
- 不做 obsolete-row cleanup；
- 不做全表 ownership reconcile；
- 不按 payload / name 相似度自动 dedupe。

旧 row 暂时留在 Production 的成本，低于 V1 自动清理造成误删的风险。清理 / reconcile 属后续维护能力。

### 7.7 No-op Publish

若本次 materialized touched output 已与当前 Production 对应 rows 一致：

```text
当前生产结果已与 Editor 一致
无需写入
```

不执行无意义 write。

### 7.8 Success

只有：

- write 完成；
- touched output reread 成功；
- reread 值与本次 expected materialization 一致；

才显示：

```text
发布成功
生产配置已重新读取并验证一致
```

Publish success 不代表 Git commit / push 已完成。作者随后通过外部 Git 工具检查 diff、commit、pull / merge / push。

### 7.9 Failure

Publish Failure 与 Autosave Failure 分开。

若 Production write、reread 或 verify 任一步失败：

```text
发布失败
请检查本地 Production 文件状态后重试
```

不宣告 partial success，也不 blind retry create。

对于需要新建 row 并取得 Production `row_id` 的情况：

```text
create
→ reread
→ 唯一识别 row_id
→ 更新本地 mapping
→ verify
```

未完成整条链路不能判定成功。

### 7.10 Warnings

Warnings：

- 不阻断 Publish；
- 不要求逐条确认；
- 不形成 reviewed / waived durable state。

### 7.11 V1 停止线

V1.0 Publish 不做：

- per-Fish / per-Mode partial publish；
- Publish History；
- 协同编辑 / revision merge；
- Git pull / commit / merge / push；
- Production reverse import；
- automatic reconcile；
- Production row GC / cleanup；
- Production row manual editor。

Publish 的停止线：

> **把当前单机 Authoring Truth 安全地非破坏性物化到本地 Production working tree，并验证本次写入。**

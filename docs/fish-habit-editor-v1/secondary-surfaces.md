# Fish Habit Editor V1｜Secondary Surfaces

> Status: Working Candidate  
> 本文收敛 Fish Subject 主 Authoring 之外的 V1 产品面。当前已闭合 Resolve Preview 与 Publish；Shared Assets 等在真正进入收敛时追加，不预先制造空章节。

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
鱼习性 › 大口黑鲈 › 中鱼习性模式 › 成年及以上 [兼容]     [编辑] [解析预览]
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

### 7.1 产品职责与发布范围

Publish 是 **Editor-global transaction**，不是当前 Fish / 当前 Subject 的第三个工作视角。

V1 只有一种发布范围：

> **将当前 Fish Habit Editor 的完整 durable Authoring State 解析并物化到 Production。**

不提供：

- 发布当前 Fish；
- 发布当前 Mode；
- 发布当前 Component；
- 勾选部分对象发布；
- “只发布这次修改”；
- durable Publish History / reviewed state。

顶栏 `发布到生产配置…` 只是进入 Publish Surface 的入口；真正 writeback executor 只存在于 Publish Surface。

### 7.2 进入 Publish Surface

进入 Publish 后，产品语境从 Subject task 临时切换为 global task：

```text
LEFT NAV             CENTER                     RIGHT
只读/锁定             Publish Preflight          Publish Executor
原上下文仍可见         全局检查                   发布动作 / 结果
```

- 左栏保留进入前的 Subject / Shared Asset 上下文作为空间锚点，但在 Publish Surface 内不允许导航或 ordinary mutation；
- 中栏 Context Header 不再显示 Fish breadcrumb，改为 **“发布到生产配置”**；
- 右栏承担唯一执行按钮与本次 transaction 状态；
- 进入前的 Subject / Edit-or-Resolve view 作为 ephemeral return target；退出 Publish 后恢复，不形成导航历史栈。

Publish Surface 不是常驻第三个 Tab，也不与 `[编辑] [解析预览]` 并列。

### 7.3 进入时的 ephemeral state

Publish 永远只消费最近一次成功持久化的 durable revision，因此必须防止作者误以为尚未落盘的输入会被发布。

- **staged candidate active**：Publish 已被 Candidate 短事务锁住，不能进入。
- **Autosave pending**：进入 Publish 时先 flush / 等待该 typed edit 的 durable write 结果，再形成 Preflight snapshot。
- **Autosave failure**：可以进入 Publish 查看 blocker，但 executor 禁用。
- **incomplete raw input**：不 silent discard、不纳入 Publish；Preflight 的“编辑器状态”显示 blocker，并提供“返回编辑处理”。返回后恢复该 transient input。
- **Validator ERROR**：允许进入 Publish Surface；由全量发布校验 Gate 明确阻断。
- **WARNING**：允许发布，不要求逐条勾选确认。

### 7.4 Preflight 只保留三个 Gate

#### Gate A｜编辑器状态

作者语言：

```text
编辑器状态
✓ 已完成保存
```

Pass 要求：

- 当前用于 Publish 的 Editor revision 已成功 durable；
- 没有 incomplete raw input；
- 没有 save failure；
- 没有 staged candidate。

若失败，明确区分：

```text
保存中…
有未完成输入
编辑器保存失败
```

不要把它们统称为“配置错误”。

#### Gate B｜发布校验

从 Gate A 的 exact durable revision 执行全量 validation / materialization-readiness check。

Pass：

```text
发布校验
✓ 0 个阻断错误
  3 个警告（不阻断）
```

Blocking ERROR 可以来自：

- Schema / semantic validation；
- required Profile 缺失；
- broken source；
- Temperature 等跨字段不变量；
- materialization readiness（例如 Production lookup domain 内 name collision）；
- 其它已经由当前 canonical validator / materializer preflight 定义的 Publish blocker。

Warnings 不形成 acknowledgement debt，不要求“我已阅读”复选框。

Blocker 列表使用人类 breadcrumb：

```text
大口黑鲈 › 成年及以上 › 结构习性 › Rock
有效值低于允许范围
```

若当前诊断已有稳定定位能力，可提供“去修复”：**退出 Publish Surface**，回到 Edit 并定位对应 Subject / Component / Field。V1 不为了 Publish 单独创造新的 Diagnostic identity/router。

#### Gate C｜生产配置基线

作者语言：

```text
生产配置基线
✓ 未检测到 Editor 外部修改
```

内部使用 expected Production generation / whole-generation verification，但普通 UI 不要求常驻显示 generation id。

以下都 BLOCK：

- generation mismatch；
- generation 无法读取 / 无法验证；
- current Production 与 expected baseline 不一致。

Blocker 文案：

```text
生产配置已在 Editor 之外发生变化。
V1 不会自动覆盖、合并或采纳这些变化。
```

允许 `重新检查`，但它**只重新读取并比较**；不得把当前 Production generation 自动采纳成新的 expected baseline。

### 7.5 Preflight layout

推荐中栏：

```text
发布到生产配置

发布范围
当前 Fish Habit Editor 全量习性配置

✓ 编辑器状态
✓ 发布校验
  0 Error · 3 Warning
✓ 生产配置基线

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

Topbar 入口使用省略号 `发布到生产配置…`，表达“进入发布任务”；Publish Surface 内的 `发布到生产配置` 才是唯一 executor。

不再额外弹第二层“确定要发布吗？” Modal。进入独立 Preflight Surface + 明确 executor 已经提供足够 intentionality。

### 7.6 Preflight snapshot 与 stale

Preflight 必须绑定一个 exact Editor durable revision 和 expected Production generation。

即使当前 UI 已锁 ordinary mutation，也必须防其它 Editor session / 外部工具修改。

点击 executor 时再次核验：

1. Editor durable revision 仍等于 Preflight revision；
2. expected Production generation 仍匹配。

任一 stale：

```text
发布前检查已过期
没有执行写入

[重新检查]
[返回编辑器]
```

不 silent rebase、不自动覆盖。

### 7.7 No-op Publish

V1 不维护“已发布 / 有未发布修改”的 durable 状志，但可以在 Preflight 中比较：

```text
materialize(current durable revision)
vs.
current verified Production
```

如果完整 Production projection 已完全一致：

```text
当前生产结果已与 Editor 一致
无需写入
```

executor 不执行无意义 write。

这是当前态的 output equality check，不是 Publish History；也不能因为 Production payload 相同就反推 Source / operation / inheritance authoring intent 相同。

### 7.8 Execute

所有 Gate PASS 且存在实际 output delta 时，唯一 executor 可用。

执行开始后：

- 锁定 Publish Surface；
- 不允许导航 / authoring mutation；
- 不提供“写到一半取消”；
- UI 可以依次显示高层阶段：
  - `正在写入生产配置…`
  - `正在重新读取并验证…`

实现内部可以涉及多表 / 多文件 materialization，但产品只存在**一个全局 Publish transaction**。

### 7.9 Success 的必要条件

只有同时满足：

1. writeback 完成；
2. 重新读取**整组 Production generation**成功；
3. reread 后的 Production 与本次预期 materialized output 验证一致；

才显示：

```text
发布成功
生产配置已重新读取并验证一致
```

成功后：

- reread 的 whole Production generation 成为新的 expected baseline；
- 本次 success 可以在当前 Surface / toast 短暂显示；
- V1 不把它持久化成 Publish History，也不在每个 Fish 上制造 Published badge；
- `返回编辑器` 恢复进入 Publish 前的 context。

### 7.10 Failure taxonomy

Publish Failure 不等于 Autosave Failure。

#### A. 写入前 stale / generation mismatch

```text
发布未执行
发布前检查已过期 / 生产配置已发生外部变化
```

没有开始 writeback。

#### B. Writeback 明确失败

显示：

```text
发布失败
生产配置未能完成写入
```

不得显示成功。

#### C. Partial write / completion unknown

如果内部多目标 write 发生部分失败或无法证明整体完成：

```text
发布失败
生产配置可能处于部分更新或未验证状态
```

必须重新读取**整组** Production generation / output 后再允许下一次 Publish；不得按 target 拼接 baseline，不允许“成功一半”。

#### D. 写入完成但 reread / verification 失败

```text
写入已执行，但无法验证最终生产配置
本次不能判定为发布成功
```

同样要求重新检查 whole Production；不可因为 write API 返回 success 就提前宣告成功。

### 7.11 失败后的 Retry

V1 不提供 blind Retry。

失败后只有在重新获得：

- exact durable Editor revision；
- 可验证且匹配 expected baseline / failure recovery rules 的 whole Production state；
- full Publish validation；

以后，executor 才重新可用。

`重新检查` 不是“再次写入”，也不是“接受 Production 当前值”。

### 7.12 Warnings

Warnings 在 Preflight 中集中展示，但：

- 不阻断 executor；
- 不要求逐项 checkbox acknowledgement；
- 不产生 reviewed / waived durable state；
- 不因为 Publish 成功而消失或被标记为已处理。

Warning 仍然只是 current state derived diagnostic。

### 7.13 不进入 V1 Publish 的能力

明确不做：

- per-Fish / per-Mode / per-Component partial publish；
- Publish selection tree；
- semantic change history；
- durable Publish History / author / timestamp ledger；
- “上次发布以来修改了什么”的 Authoring diff；
- 自动采纳外部 Production；
- reverse import / auto merge；
- Production row-level manual override；
- materialized production name / row id 的普通作者编辑；
- second confirmation modal；
- warning acknowledgement workflow。

Publish 的停止线：

> **验证当前 Editor durable state 可以安全物化，并以一个全局 transaction 写入且重新验证 Production；不把 Publish 扩成版本管理、Reconcile 或 Production 编辑器。**

# Fish Habit Editor V1｜Shared Templates

> Status: Current Surface Contract for V1  
> V1 Shared Assets 只包含 Shared Template。Fish Family / Species Preset 不属于 V1；V1.0 不提供 Species Base initialization。

## 1. 产品职责

Shared Template 是持续共享的 Source Asset。V1 必须支持：

- 空白创建 Template；
- 从当前 Fish Component 提取 Template；
- 从当前 Effective Policy 提取 Policy Template；
- Clone / Save As；
- 编辑 complete value；
- Archive / Restore / Hard Delete guard；
- Replace References；
- 查看显式引用与额外跟随使用。

Shared Template 是长期可管理资产；Existing Production Source 不是 Shared Asset，不出现在本 Workspace，也不获得 Template metadata / lifecycle。它只在 Fish Component 的 Source Picker 中作为“已有生产数据 · 兼容”出现。

V1.0 不创建 Species Base；Shared Template 是独立的可复用 Source Asset。Template 创建本身不创建或修改 Fish / Mode identity。

## 2. 左栏导航

```text
共享资产

▼ 习性模板
  ▼ 水温
     高温鱼
     冷水鱼
  ▼ 结构
     Heavy Cover
     Open Water
  ▸ 觅食水层
  ▸ 时段
  ▸ 空间机会策略
```

- `习性模板` 与 Template Kind 只是 group；具体 Template 才是 Subject。
- 当前 Template path 保持可见。
- 搜索按名称 / alias / stable id 查找。
- V1 不显示鱼家族预设占位。

Breadcrumb：

```text
共享资产 › 习性模板 › 结构 › Heavy Cover
```

## 3. 三栏承载

```text
Template Navigation | Template Overview | Template Editor
我在看哪个模板？      它是什么/谁在用？    我具体改什么？
```

中栏 Overview 至少包含：

- Template Kind；
- lifecycle（ACTIVE / ARCHIVED）；
- 当前 complete value 摘要；
- 显式引用；
- 额外跟随使用。

右栏承担：

- metadata；
- complete value；
- lifecycle actions；
- Clone / Replace References 等资产动作。

## 4. 引用情况

产品语言不直接暴露 `DirectReferenceSet / EffectiveConsumerSet`。

显示：

```text
引用情况

显式引用        4
额外跟随使用    7
```

“显式引用”＝ durable state 中直接绑定当前 Template 的 owner。

“额外跟随使用”＝没有直接绑定，但 Resolve 后最终消费该 Template 的**作者语义 follower**。系统默认 Affinity 这类隐藏 projection 不作为额外一条 consumer 重复显示或计数；它随所属 Species Base 的 materialization 自动更新。

Hard Delete 看显式引用；Template complete-value Impact 看所有最终消费者。

引用列表中的 Fish / Mode 可以进入对应 Authoring Subject，并建立单个 ephemeral ReturnTarget：

```text
← 返回 Heavy Cover
```

作者在目标 Workspace 主动选择其它普通 Subject 后，ReturnTarget 可以清除；V1 不维护通用历史栈。

## 5. Metadata

每个 Shared Template 至少有三层身份，不能互相代替：

- **stable template identity**：Editor durable reference；不因改名变化。
- **中文名**：作者在 Editor 中的主要显示名，用于左栏、Breadcrumb、搜索与日常沟通；ordinary autosave；不作为 Production identity。
- **英文名**：作者可读的英文语义名。Blank Create / Extract 时工具应先给出一个可读建议值，作者可以直接接受或修改。它在 Editor 层仍按 ordinary edit 持久化，但属于 **projection-affecting metadata**：改名不会改变 Template identity 或 Effective Value，却可能改变下一次 Publish 生成的 Production Profile name。

Template Context 必须允许直接编辑中文名与英文名。中文名是 UI primary display；英文名视觉上可次一级，但不应隐藏成内部字段。

中文名与英文名都是 Template 的 required metadata：trim 后为空的值不能形成 durable commit。名称重复是否允许由各自 Editor / Production collision domain 决定；即使名称相同，stable template identity 仍不得按名字合并。

Template Kind 创建后不可修改；不同 Kind schema 不同，跨 Kind 改动不做 migration。

### 5.1 Template English Name 与 Production Profile Name

Template 英文名本身不是 Editor stable identity，也不是 `FishEnvAffinity` row name。

当 Template 以**无有效 local operation**的形式直接 materialize 为对应 Component/Profile 子表 row 时，Production Profile name 必须从 Template English Name **确定性派生**；是否额外加入 Kind qualifier 属 Production naming convention，不是 Template 的业务 identity。

例如：

```text
Structure Template
中文名：重障碍区
英文名：Heavy Cover
→ Production Profile：Struct Heavy Cover

Temperature Template
中文名：暖水型
英文名：Warm Water
→ Production Profile：Temp Warm Water
```

优先 convention 是在需要时加入 Kind qualifier，例如 `Struct Heavy Cover`、`Temp Warm Water`：它能提高裸看 Production 时的表意性，并在共享 / 合并 namespace 中降低跨 Kind 撞名风险。但如果真实 schema 已按独立子表或独立 lookup domain 天然隔离 Kind，则不应为了形式统一强制增加无收益前缀。

若 G3 最终确认需要 Kind qualifier，当前优先 vocabulary 为：

- Temperature → `Temp`
- Structure → `Struct`
- Feeding Layer → `FeedLayer`
- Time Period → `Period`
- Spatial Opportunity Policy → `Policy`（仅在真实 Production 中存在独立具名 Policy row 时）

其中 `Period` 保持与 canonical `Time Period` 概念一致，避免 `Time` 与 timestamp / runtime time 等更宽语义混淆；`FeedLayer` 明确保留“觅食水层”语义，避免 `Feed` 被理解成食物 / 饵料类型。这个 vocabulary 属 G3 naming convention，不升级为 Authoring Semantic Contract。

G3 仍需根据真实 schema 固定 delimiter、空格/下划线、大小写与合法字符 normalization。作者不需要手工输入 Kind qualifier。

Spatial Opportunity Policy 只有在现有 Production schema 中确实 materialize 为独立具名 row 时才应用同类命名；不得仅为了 UI 对称预设一个并不存在的 `Policy` 子表。

如果最终 Profile 含有 Species / Mode 的有效 ADD / SET / CLEAR 等 local operation，则它已经不是 Template complete value 本身，应按 owner-specific materialization 规则生成 Production name，而不是继续冒用 Template 的 Production Profile name。

若英文名或派生 Production Profile name 最终造成对应 lookup / collision domain 冲突，由 Publish Validator / materializer preflight 报错；不得把 display name 当作 durable identity。

英文名 rename 不需要升级为 Template Value Candidate：它不改变 Template complete value，也不会改变任何 consumer 的 Effective 配置。但 Publish 必须把它当作 projection rename 处理：如果 Production 侧存在按 name 的引用，Materializer 必须能在本次全局 Publish 中安全重写并验证；如果引用边界无法证明完整、存在 Editor 外部 name-based reference，或 rename 会留下 orphan / duplicate row，则 Publish BLOCK，而不是 silent rename。

## 6. Complete Value 编辑

Template Editor 直接平铺 complete value fields，不要求先进入二级“编辑模式”。

第一处完整、可解析且不同于 durable value 的字段修改建立一个 **Template Value Candidate**。

Candidate active 后：

- 作者可以继续修改**同一个 Template 的多个字段**；
- 所有修改属于同一 ephemeral candidate；
- 左栏导航、metadata / lifecycle ordinary edit 与 Publish 暂停；
- 中栏从普通 Overview 临时切为 Impact Preview；
- 右栏继续编辑 candidate template values；
- Impact 随 candidate 更新 debounce 重算；
- 一次 Confirm 原子提交整份 candidate complete value。

这样避免每改一个字段都单独做一次 fan-out Preview。

未形成完整 typed value 的 raw input 只存在于 candidate UI；不能 Confirm，Cancel 时丢弃。

## 7. Template Value Impact Preview

中栏示例：

```text
Heavy Cover · 更新影响

显式引用             4
额外跟随使用         7
最终结果发生变化     8

新增 Error           1
新增 Warning         2

受到影响

大口黑鲈 › 基础习性 › Structure
  Rock   1.00 → 0.80

大口黑鲈 › 中鱼习性模式 › 大个体 [兼容] › Structure
  Rock   0.80 → 0.60
  原有 ADD -0.20 保留

狗鱼 › 基础习性 › Structure
  Wood   1.20 → 1.20
  本层 SET 遮罩模板变化
```

Impact 必须区分：

- direct binding；
- follower；
- Effective result 真正变化；
- 被 operation 遮罩；
- diagnostic delta。

不要把引用数当作结果变化数，也不要把隐藏 default Affinity projection 当成额外的人类影响对象重复计数。

## 8. Confirm / Cancel

Confirm：

```text
revision check
→ atomic replace template complete value
→ clear candidate
→ re-resolve consumers
→ 回 Template Overview / Editor
```

已有 Fish / Mode operations 全部原样保留。

不得：

- 为保持旧 Effective Value 自动生成 SET；
- 自动清 ADD / SET / CLEAR；
- 自动改 Consumer Source；
- 自动要求每个 Consumer 建“待复核”状态。

若 candidate template schema-valid，但 after-state 产生 publish-blocking diagnostic，仍允许确认保存；Confirm 不是 Publish。

Cancel 只丢弃 candidate，不修改 durable Template。

### 8.1 Candidate revision stale

Template Value Candidate 与 Source Change Candidate 的 stale 处理不同。

Template complete value 是一组作者内容修改；如果 Candidate 基于 revision 104，而 durable Template 已被另一会话改到 105，V1 **不自动把旧 Candidate fields rebase 到新 Template**，避免把并发修改悄悄覆盖。

此时：

- Confirm 禁用；
- 明确提示“模板内容已被其它会话更新，本次候选尚未保存”；
- 当前 candidate 可以暂时保留为只读 / 可复制的本地值，方便作者人工对照；
- 作者必须取消 / 结束当前 candidate，重新读取最新 durable Template，再显式重新应用需要保留的字段修改；
- V1 不做 Template 字段级三方 merge。

Source Change / Policy Source Change / Replace References 这类“稳定 intent + 重算 impact”的 staged mutation 可以按各自 Contract 在最新 durable revision 上重新计算 Preview；不能把这一规则误套到 Template complete-value content edit。

## 9. Blank Create

从 Template Kind group 提供：

```text
+ 新建结构模板
```

创建流程：

- Kind 在启动时确定；
- 表单 ephemeral；
- 不建立 durable DRAFT_TEMPLATE；
- 填写必要 metadata + 该 Kind 完整 typed value；
- 中文名由作者输入；
- 英文名由工具先给出可读建议值，作者可修改；创建时必须已经存在非空英文语义名，但作者不必从空白手输；
- atomic create；
- 创建成功即 ACTIVE。

成功后的去向按入口区分：

- 从 Shared Assets 独立发起 Blank Create → 进入新 Template Context；
- 从 Species initialization 的 Source picker 作为 contextual detour 发起 → 返回原 initialization form，保留此前 ephemeral 选择并刷新 Source candidates；新 Template **不自动绑定 / 不自动选中**，作者仍在原 Source picker 显式选择。

这仍遵守 `Create Source ≠ Bind Source`，也避免为了 contextual detour 建立 durable draft / history stack。

新 Template 尚无 consumer，因此不需要 Impact Preview。

## 10. Extract from Fish

Fish Component Focus：

```text
[提取为共享模板…]
```

Policy Focus：

```text
[提取为策略模板…]
```

提取语义：

- Component → flatten 当前完整 Effective Profile；
- Policy → flatten 当前四个 Effective Role + Effective fail_env_coeff；
- 创建新的独立 Template；
- 不复制 Source / ADD / SET / CLEAR / provenance / lineage；
- 当前 Fish 完全不改；
- 如果希望当前 Fish 改用新模板，必须另走 Source / Policy Template Change Candidate。

### 10.1 Extract creation surface

Extract 采用轻量创建浮层，而不是在左栏先制造未保存 Template Subject。

浮层只承担创建所需的最小信息：

```text
提取为共享模板

来源
大口黑鲈 › 基础习性 › 结构习性

模板类型
Structure                  只读

中文名
[ 重障碍区 ]

英文名
[ Heavy Cover ]

将提取当前完整 Effective Profile。
不会改变当前 Fish 的 Source。

[取消]                  [创建模板]
```

规则：

- Extract 只从**最近一次成功 durable revision**的 Effective Profile / Effective Policy 取值；
- staged candidate active 时 Extract 不可用；
- Autosave pending 时先等待 / flush durable write；save failure 时 BLOCK；
- 当前 Focus 有 incomplete raw input 时 BLOCK，要求作者先完成或取消输入，不 silent discard，也不拿旧 durable value 冒充“当前提取值”；
- 中文名由作者确认 / 输入；
- 英文名由工具根据中文名、当前上下文或已有命名规则先生成可读建议值，作者可修改；创建提交时必须有非空英文语义名；
- 浮层内不编辑 Template complete value；complete value 来自上述 exact durable revision 的 Effective Profile / Effective Policy flatten；
- 创建前不在左栏出现 durable Draft Template；
- 点击创建后 atomic create ACTIVE Template；
- 创建成功后**直接切换到新 Template Context**，左栏选择对应 Template，中栏显示 Template Overview，右栏允许继续编辑中文名、英文名与 Template complete value；
- 保留单个 ephemeral ReturnTarget，例如 `← 返回 大口黑鲈 › 基础习性 › 结构习性`。

这样“创建资产”和“继续编辑资产”分成两个清楚阶段：浮层负责把 Template 生出来，Template Context 负责后续维护。

原则：

> Create Source ≠ Bind Source。

Profile absent / 无法完整 Resolve，或 Policy 无法形成完整 Effective Policy 时不能 Extract。

## 11. Clone / Save As

Clone / Save As 复用 bounded Template creation flow：

- Kind 锁定为当前 Template Kind；
- complete value 复制当前**最近一次成功 durable**的 Template value；active Value Candidate 时 Clone / Save As 不可用；
- 创建表单要求确认新的中文名 / 英文名，可基于当前名称给出“副本 / Copy”等建议，但不能直接复用到会造成 schema / naming collision 的非法名称；
- atomic create 新 Template identity，成功后进入新 Template Context；
- 两者以后完全独立；
- 不形成 Template → Template inheritance；
- 不修改任何 existing binding。

## 12. Archive / Restore / Hard Delete

Lifecycle：

```text
ACTIVE ↔ ARCHIVED
```

Archive：

- 轻量确认；
- 既有引用继续 Resolve / Publish；
- 不再作为新的 Source candidate；
- complete value 不再可编辑；
- 不自动 Replace、fallback 或找相似 Template。

Restore：

- direct atomic action；
- 恢复为可选 Source；
- 不修改已有引用。

Hard Delete 只在：

```text
ARCHIVED
+
显式引用 = 0
```

时出现，并使用 destructive confirm。

执行 delete commit 时必须再次做 optimistic revision / guard check，确认：

- Template 仍为 ARCHIVED；
- DirectReferenceSet 仍为空；
- 当前 durable revision 未使 delete 前提失效。

如果另一会话在确认期间新建了 direct reference，Hard Delete 必须冲突失败并刷新引用状态，不能先删 Template 再制造 broken source。

Hard Delete 删除的是 Editor Template asset。若该 Template 曾经 materialize 出 Editor-owned Production Profile row，实际 Production cleanup 发生在下一次 Global Publish，并受 managed-projection ownership guard 约束：

- ownership 可证明且 current desired graph 已不再引用 → 可删除 obsolete projection；
- ownership 不明 / 与 pass-through row 混淆 → Publish BLOCK，不因 Hard Delete 在 Editor 成功就盲删 Production row。

因此 Hard Delete 成功只表示 Authoring asset 已删除，不等于 Production 已经同步清理。

## 13. Replace References

Replace A → B 是 staged propagated mutation。

限制：

- B 必须是同 Kind、可作为新 Source 的 ACTIVE Template；
- 只重写 A 的 direct bindings；
- inherited / follower 不自动获得 explicit pin；
- 所有 existing ADD / SET / CLEAR / Role / coeff patches 保留；
- old Template 不自动 Archive / Delete。

Preview 至少显示：

```text
将重写显式引用      4
跟随受到影响        7
最终结果变化        6
新增 Error          1
```

Confirm 后 atomic rewrite direct bindings，并重 Resolve 全部受影响对象。

## 14. Contextual Drill-in

Fish Component / Policy 中的“查看模板”可以进入 Shared Template Workspace，并保存一个 ephemeral ReturnTarget：

```text
← 返回 大口黑鲈 › 中鱼习性模式 › 大个体 [兼容] › 结构习性
```

Template 引用列表进入 Fish 时同理可显示“返回当前模板”。

Species initialization 从 Source picker 进入 Shared Assets 创建 Template 时，也使用同一种单层 contextual ReturnTarget；它返回 initialization form，而不是形成通用历史栈。

只保留一个 ReturnTarget，不建立通用 back stack。

## 15. V1 停止线

V1 Shared Template 不扩展为：

- Template inheritance；
- Template version graph；
- per-consumer review debt；
- 自动聚类；
- Family；
- 鱼家族预设；
- Species Base initialization workflow（V1.0 不提供；未来若引入仍不塞进 Template Workspace）；
- 外部生态 Import；
- 批量跨多个 Template 的编辑事务。

停止线：

> **让作者可以安全创建、提取、编辑、传播和维护可复用 Source Asset；不把 Template Workspace 扩成 Existing Production 浏览器、数据迁移或物种初始化系统。**

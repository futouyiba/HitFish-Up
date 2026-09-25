# Fish Habit Editor V1｜Shared Templates

> Status: Working Candidate  
> V1 Shared Assets 只包含 Shared Template。Fish Family / Species Preset 不属于 V1；Species Base initialization 属于 Fish Authoring Surface，不属于 Shared Template Workspace。

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

V1 可以从 Fish Basic 创建 Species Base + 系统默认 Affinity projection；Shared Template 则是独立的可复用 Source Asset。Template 创建本身不创建或修改 Fish / Mode identity。

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

“额外跟随使用”＝没有直接绑定，但 Resolve 后最终消费该 Template 的 follower。

Hard Delete 看显式引用；Template complete-value Impact 看所有最终消费者。

引用列表中的 Fish / Mode 可以进入对应 Authoring Subject，并建立单个 ephemeral ReturnTarget：

```text
← 返回 Heavy Cover
```

作者在目标 Workspace 主动选择其它普通 Subject 后，ReturnTarget 可以清除；V1 不维护通用历史栈。

## 5. Metadata

Template display name / alias 等 metadata ordinary autosave。

Template Kind 创建后不可修改；不同 Kind schema 不同，跨 Kind 改动不做 migration。

内部 stable identity 不由 display name 决定。

若 metadata 最终会造成 Production lookup-domain collision，由 Publish Validator / materializer preflight 报错；普通 UI 不要求作者理解物理 row name。

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

大口黑鲈 › 成年及以上 › Structure
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

不要把引用数当作结果变化数。

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
- atomic create；
- 创建成功即 ACTIVE。

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
- 创建成功后可“查看新模板”；
- 如果希望当前 Fish 改用新模板，必须另走 Source / Policy Template Change Candidate。

原则：

> Create Source ≠ Bind Source。

Profile absent / 无法完整 Resolve，或 Policy 无法形成完整 Effective Policy 时不能 Extract。

## 11. Clone / Save As

Clone / Save As：

- 从当前 complete value 创建新 Template identity；
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
← 返回 大口黑鲈 › 成年及以上 › 结构习性
```

Template 引用列表进入 Fish 时同理可显示“返回当前模板”。

只保留一个 ReturnTarget，不建立通用 back stack。

## 15. V1 停止线

V1 Shared Template 不扩展为：

- Template inheritance；
- Template version graph；
- per-consumer review debt；
- 自动聚类；
- Family；
- 鱼家族预设；
- Species Base initialization workflow（属于 Fish Surface，不塞进 Template Workspace）；
- 外部生态 Import；
- 批量跨多个 Template 的编辑事务。

停止线：

> **让作者可以安全创建、提取、编辑、传播和维护可复用 Source Asset；不把 Template Workspace 扩成数据迁移或物种初始化系统。**

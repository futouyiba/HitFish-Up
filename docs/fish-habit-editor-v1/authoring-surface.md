# Fish Habit Editor V1｜Fish Authoring Surface Contract

> Status: Working Candidate  
> 本文只定义 Fish Subject 的核心编辑屏。Shared Assets、Publish 等其它 Surface 后续单独收敛；低层 operation / persistence token 语义继续引用现有 canonical contract。

## 1. 核心一屏

```text
GLOBAL TOPBAR
Fish Habit Editor              已保存   ⛔2   ● 未确认变更   [发布…]

────────────────────────────────────────────────────────────────

LEFT NAV              CENTER                                       FOCUS

FISH                  鱼习性 › 大口黑鲈 › 中鱼习性模式            结构习性
                      › 成年及以上 [兼容]                          大口黑鲈 · 成年及以上

▼ 大口黑鲈            [ 编辑 ] [ 解析预览 ]                       当前来源
  基础习性                                                          Heavy Cover
  中鱼习性模式        ┌ 温度习性 ────────────────┐
    幼年 [兼容]       │ 来源 Warmwater ▾         │                字段行式编辑
    成年及以上 ●      │ 沿用底板                 │
         [兼容]       └──────────────────────────┘
                      ┌ 结构习性 ──────────── ⛔ ┐
▸ 虹鳟                │ 来源 Heavy Cover ▾      │
                      │ 有本层调整               │
▸ 狗鱼                │ Rock 调整 -0.20 → 0.80 │
                      └──────────────────────────┘
                      ┌ 觅食水层习性 ───────────┐
                      └──────────────────────────┘
                      ┌ 时段习性 ───────────────┐
                      └──────────────────────────┘
                      ┌ 空间机会策略 ───────────┐
                      └──────────────────────────┘
```

中栏优先采用 2×2 Component Overview + 全宽 Policy；具体像素是 projection，不是 semantic contract。

## 2. Subject Navigation

- Subject 只在左栏选择。
- 点击 Fish 名称 → 该 Fish / 基础习性。
- 点击 Mode child → 该 Fish / 对应 Mode。
- Chevron 只控制 disclosure，不改变 Subject。
- 当前 Subject path 始终可见。
- 搜索不改变 selection；若搜索结果会隐藏当前 Fish，应保留轻量“当前”区显示当前路径。

中栏不重复 Fish / Mode selector。

## 3. Context Header

Header 仅一行 identity breadcrumb：

```text
鱼习性 › 大口黑鲈 › 基础习性
鱼习性 › 大口黑鲈 › 中鱼习性模式 › 成年及以上 [兼容]
```

Context Header 不常驻显示 `有本层调整`、Error 数量、Autosave 等 aggregate status；这些分别由 Component/Policy 与 Global Topbar 承担。

Header 同行可放：

```text
[ 编辑 ] [ 解析预览 ]
```

## 4. Component Overview Card

Card 职责是“摘要 + Focus 入口 + Source mutation”，不是完整字段编辑器。

示例：

```text
结构习性                                角色·CORE  ⛔

来源
[ Heavy Cover ▾ ]

本层状态
有本层调整

Rock        调整 -0.20                  0.80
Weed        沿用物种设置                1.20
Wood        设置为 0.60                 0.60
```

交互：

- 点击 Card body → `selectedComponent = Structure`，只改变 UI focus，不保存。
- 点击某 field summary row → 选中 Component，并让 Focus Editor 定位该 field。
- Source Selector → staged Source candidate。
- Diagnostic badge → 选中该 Component 的相关诊断。
- Card 不直接编辑 field numeric value。

## 5. Focus Editor states

四种视觉状态：

1. **Empty**：未选 Component，提示“选择一个习性组件查看和编辑具体参数”。
2. **Editable**：平铺当前 Component 全部可编辑字段。
3. **Read-only**：显示完整值与不可编辑原因，不只用 disabled form。
4. **Detached**：右栏 Focus object 与当前中栏 Subject 不同；明确标出旧对象身份，并提供低成本“切回当前上下文”。Subject change 不静默 rebind 到新 Subject 的同名 Component。

## 6. Inline Field Authoring

Field Authoring 优先表现为宽屏行式编辑，不使用二次 Drawer / Modal / “编辑”按钮。

```text
结构习性

当前来源：Heavy Cover                                  [查看模板]

字段       来源值       本层操作                 参数       有效值
──────────────────────────────────────────────────────────────
Rock       1.00        [调整       ▾]          -0.20       0.80
Weed       0.80        [设置为     ▾]           1.20       1.20
Wood       0.60        [沿用物种设置 ▾]                     0.60
Grass      0.30        [仅用当前来源 ▾]                     0.30
```

- Source value / inherited operation / Effective Value 是解释性 projection。
- 本层 Operation 与参数是 authoring input。
- Focus Editor 不出现 Source mutation control。
- 一屏尽量同时看到该 Component 的全部字段，支持连续扫描与人工批量编辑。

## 7. Operation vocabulary projection

低层 token 语义仍由 canonical semantic contract 维护；V1 UI 采用作者语言。

### Species Base 数值字段

```text
沿用来源
调整
设置为
```

### Compat Mode 数值字段

```text
沿用物种设置
仅用当前来源
调整
设置为
```

其中：

- `沿用物种设置`：本层无 Operation record，继续消费 Species operation。
- `仅用当前来源`：显式 CLEAR 上层 operation，只使用当前 Effective Source raw value。
- `调整`：ADD。
- `设置为`：SET。

`CLEAR` 与 absence 必须可见区分。CLEAR 状态应弱显示被取消的上层 operation，例如：

```text
物种调整 -0.20 · 本层已取消
```

## 8. 从未选中到字段编辑

### 8.1 未选 Component

- 中栏展示 Overview。
- Focus Editor = Empty。
- 不产生持久化变化。

### 8.2 选择 Component

点击 Structure Card：

```text
selectedComponent = Structure
```

只改变 UI focus；右栏立即平铺 Structure fields。

### 8.3 切 Operation

#### 选择无值 Operation

例如沿用来源 / 沿用物种设置，或仅用当前来源 / CLEAR。

操作本身语义完整，可直接形成 ordinary durable edit 并 Autosave。

#### 选择需要数值的 Operation

例如调整 / ADD，设置为 / SET。

切换 Operation Type 时**不自动制造 `ADD 0`、不把旧参数解释成新 Operation，也不自动保持 Effective Value**。

UI 进入 local raw-input state：

```text
[调整 ▾] [      ]
```

输入框获得焦点；只有在得到完整、可解析的参数后才形成新的 durable operation。

### 8.4 ADD ↔ SET

从 ADD 切 SET，或 SET 切 ADD：

- 不复用旧参数作为新语义；
- 不自动把旧 Effective 转换成新的 SET；
- 进入空 transient input，等待作者明确输入。

原则：

> 改变 Operation Type 不自动替作者重解释 Authoring Intent。

## 9. Autosave / raw input / validation

### 9.1 Incomplete raw input

例如 `-`、切换到 ADD / SET 后尚未填写参数，或其它尚不能形成完整 typed value 的输入：

- 只存在 UI local raw state；
- 不进入 durable state；
- 不触发 Resolve input；
- Effective 区继续以最近一次 durable state 为准，并弱提示“未应用”；
- Publish 消费最近一次成功 durable revision；
- 若作者在输入完成前切离该 field / Component / Subject / Workspace，丢弃 transient input，并恢复该行最近一次 durable 表达；不为半完成操作弹保存确认。

### 9.2 Durable-valid but publish-invalid

例如完整输入可解析，但 Effective Value 违反 Validator：

```text
Rock   来源 0.10   [调整] -0.20   → -0.10
                       ⛔ 有效值必须 ≥ 0
```

处理：

```text
typed authoring intent
→ Autosave 成功
→ durable state
→ Validation ERROR
→ Editor 已保存 · 有错误
→ Publish blocked
```

Validator ERROR 不等于 Save Failure。

### 9.3 Save failure

Durable write 本身失败：

- Topbar 显示编辑器保存失败；
- 最近一次成功 durable revision 仍是 Truth；
- 不把未成功保存的数据冒充 Resolve / Publish 输入。

## 10. Diagnostic projection

同一个 Diagnostic 可以投影到 field row、Component Card badge、Global Topbar / Validation List，但它仍是一份 derived diagnostic，不是三份状态。

最小定位 breadcrumb：

```text
对象 → Subject → Component / Policy → Field
```

Rail 最多显示 blocking-presence indicator，不把导航变成 Validation Dashboard。

## 11. 恢复继承

不增加独立的“恢复继承”按钮。

Species Base 的 `沿用来源` 就是删除 Species local operation。

Compat Mode 的 `沿用物种设置` 就是删除本层 operation record。

保持一个 mutation path，避免“下拉操作 + 恢复按钮”两套 mutation entry。

## 12. Source Change Candidate

Source Selector 只在 Component Card 提供。

例如：

```text
Heavy Cover
→ Rock Cover
```

Source change 不走 ordinary autosave，因为它改变整个 Component 的计算基准。

### 12.1 启动前提

Source Candidate 只能从**最近一次成功持久化的 durable state**启动。

若当前存在：

- incomplete raw input；
- Autosave 尚未完成；
- durable save failure；

则不直接建立 Source Candidate。UI 先要求完成/恢复当前普通编辑，使 Preview 的 before-state 有唯一依据。

### 12.2 Exact binding no-op 与 same-effective real mutation

若作者选择的候选与当前 durable **binding intent 完全相同**，不建立 Candidate。

但下列情况即使当前 Effective Source / Effective Value 相同，仍属于真实 Source mutation：

```text
跟随基础习性 → 显式固定 Heavy Cover
显式固定 Heavy Cover → 跟随基础习性
```

因为未来传播行为不同，不能按 value diff = 0 折成 no-op。

Compat Mode 的 Source 展示必须区分：

```text
跟随基础习性 → Heavy Cover
Heavy Cover · 本模式设置
```

普通 UI 不显示底层 sourceOverride token。

### 12.3 Candidate 是短事务，不是第三种长期工作视角

正常 Fish Subject 只有：

```text
[ 编辑 ] [ 解析预览 ]
```

建立 Source Candidate 后，不新增“候选预览”Tab，也不允许作者带着候选离开当前事务继续浏览。

Candidate active 期间：

- 左栏与中栏继续保持当前 Subject / Component 的空间上下文，但其它导航与 ordinary mutation 暂停；
- Publish 暂不可进入；
- Topbar 只需提示“来源变更待确认”，不需要额外的 `[查看候选]` 回返入口；
- Candidate 不写 durable state，不形成 Draft entity；
- Reload / 离开 Editor 会丢弃 Candidate，并应使用普通未确认变更离开警告。

原则：

> Source Candidate 是“选来源 → 当场看清 → 确认或取消”的短事务，不是可跨页面长期挂起的 Draft。

### 12.4 Review 承载：右侧 Focus Editor 临时切换

V1 不为 Local Rebase / Propagated Impact 新建独立 Workspace。

建立 Candidate 后：

- 左栏保持当前 Subject；
- 中栏仍显示当前 **durable** Overview，不把 candidate after-state 混入普通 Card；
- 右侧 Focus Editor 临时切换为 **来源变更预览**；
- 该 Component Card 可显示轻量“正在预览来源变更”状态，但 Source 仍显示 durable current，避免未确认值冒充 Truth。

示例：

```text
来源变更预览
大口黑鲈 · 成年及以上 · 结构习性

来源关系
当前      跟随基础习性 → Heavy Cover
候选      Heavy Cover · 本模式设置

字段结果
Rock      0.80 → 0.80
Weed      1.20 → 1.20
Wood      0.60 → 0.60

当前数值无变化
但来源关系将从“跟随”变为“显式固定”。
以后基础习性更换来源时，本模式将不再跟随。

[取消更换]                    [确认更换来源]
```

### 12.5 Preview 必须回答四件事

#### A. Binding intent 怎么变

必须先显示当前 binding、候选 binding，并在必要时显示当前/候选 Effective Source。不能只显示数值 diff。

#### B. 字段结果怎么变

按该 Component 的稳定字段顺序展示 before / after。字段没有变化也可保留，但视觉降级。

#### C. 为什么某些字段没变

如果结果未变是因为本层 SET / 其它既有 operation 遮罩 Source 变化，应明确说明，例如：

```text
Wood   0.60 → 0.60
本层 SET 0.60，来源变化被遮罩
```

“被遮罩”不是“无影响”。

#### D. Diagnostic 怎么变

只强调 Candidate 带来的诊断变化：新增 Error、新增 Warning，以及必要时被解除的现有诊断。已有且完全不受本 Candidate 影响的诊断不需要在 Review Panel 重复堆叠。

### 12.6 Local 与 Propagated 使用同一 Review Panel

两者不是两套页面。

**Local Rebase** 只影响当前 owner 时，右栏只显示：binding before / after、当前 Component field before / after、operation masking、diagnostic delta。不要显示伪造的全局引用量 / changed consumers 等统计。

**Propagated Impact** 当 Species Base Source 变化会传播到当前 owner 之外的 follower 时，在同一右栏 Review Panel 追加：

```text
同时影响

幼年 [兼容]          3 项变化   0 Error
成年及以上 [兼容]    2 项变化   1 Warning
```

受影响对象可在 Review Panel 内展开看只读明细；不通过左栏导航离开 Candidate 事务。

产品语言优先说“直接修改 / 跟随受到影响”，不要求作者理解 DirectReferenceSet / EffectiveConsumerSet。

### 12.7 Operation 保留

换 Source 时既有 field operations / patches 原样保留。

Preview 展示的是：

```text
新 Source
+
原有 Operation
=
Candidate Effective
```

不得自动清空 ADD / SET / CLEAR；不得为保持旧 Effective Value 自动生成新的 SET；不得因 before/after 数值相同自动改写 operation intent。

### 12.8 Candidate 有 Validation Error 时仍可确认

如果候选 Source 本身是合法 durable binding，但 Candidate Resolve 后出现 publish-blocking validation error：

```text
可保存到 Editor
但会产生 1 个发布阻断错误
```

`确认更换来源` 仍可执行。

确认后：

```text
atomic durable commit
→ Editor 已保存 · 有错误
→ Publish blocked
```

Candidate Confirm 不是 Publish。

### 12.9 真正禁止 Confirm 的情况

只有 Source mutation 本身已经不能形成合法 durable commit 时，才禁用确认，例如：

- candidate source 已删除 / 已不再是合法 selectable source；
- candidate binding 不满足 schema；
- revision stale 且尚未重新计算 Preview。

这与“结果有 Validator ERROR”必须区分。

### 12.10 Revision stale

Confirm 前必须做 optimistic revision check。

若 Preview 基于 revision 104，而 durable state 已变成 105：

```text
候选预览已过期

这笔来源变更尚未保存。
[重新计算预览]
[取消更换]
```

- 不 silent auto-rebase；
- “重新计算预览”保留本次候选 Source intent，以最新 durable revision 重算 before/after；
- 重算后仍需再次显式 Confirm；
- 若候选 Source 本身已失效，则不能继续确认，作者取消后回 Card 重新选择。

### 12.11 Confirm / Cancel

**确认更换来源**

```text
revision check
→ atomic durable commit
→ candidate cleared
→ 回到原 Authoring Surface
→ 原 Component 保持 selected
→ Focus Editor 继续停在该 Component
→ Card / Field 读取新的 durable truth
```

无需成功 Modal；轻量状态反馈即可。

**取消更换**

只丢弃 ephemeral candidate，不回滚任何已 durable 的普通编辑。

用户文案用“取消更换”，不要求作者理解内部 candidate 术语。

### 12.12 Source Change 状态机

```text
Durable Source
      │
      │ Card 选择新的 binding intent
      ▼
Candidate Review
      │
      ├── 取消更换 ───────→ Durable 不变
      │
      ├── stale ──────────→ 重新计算 Preview
      │
      └── 确认更换来源
                 ↓
           atomic commit
                 ↓
          New Durable Source
```

没有 Draft Source、没有先 Apply 再 Save、没有第二个 Source Selector、没有跨页面长期挂起 Candidate。
## 13. Policy Authoring

空间机会策略是独立 Authoring 区，不是第五个 Component。

中栏使用一张全宽 Policy Card，同时展示四个 Effective Role 与 fail_env_coeff；Role mutation 不分散到四张 Component Card。

Species Base 示例：

```text
空间机会策略

策略来源
Predator Policy

温度          CORE        沿用策略模板
结构          CORE        本层设置
觅食水层      SECONDARY   沿用策略模板
时段          IGNORED     本层设置

fail_env_coeff   0.01     沿用策略模板值
```

Compat Mode 示例：

```text
空间机会策略

策略来源
沿用基础习性 → Predator Policy

温度          CORE        沿用基础习性角色
结构          SECONDARY   本模式设置
觅食水层      CORE        使用策略模板原始角色
时段          IGNORED     沿用基础习性角色

fail_env_coeff   0.015    本模式调整
```

### 13.1 Component Card Role badge

每张 Component Card 显示一个**只读 Effective Role badge**，用于 Overview 扫描：

```text
结构习性                         角色·CORE
温度习性                         角色·SECONDARY
时段习性                         角色·IGNORED
```

Role badge 不提供 dropdown / toggle，不是 mutation entry。

保留它的理由是：Role 决定该 Component 当前是否、以及以何种角色参与空间机会计算；如果完全隐藏到 Policy 区，作者在浏览 Component Overview 时会缺失一条关键“是否被消费”的信息。

不把 badge 做成编辑入口的理由是：Profile 与 Policy 是两个正交概念；把 Role dropdown 放进 Component Card 会重新形成第二个 Policy mutation surface。

V1 推荐：

- badge 只读；
- 视觉权重弱于 Component title / diagnostic；
- IGNORED 仍应可见，不通过把整个 Component disabled 来表达；
- 如需解释，可用 tooltip / helper text 指向“在空间机会策略中编辑”，不要求点击 badge 本身承担导航。

### 13.2 Policy Focus Editor

点击 Policy Card 或其中任一 Role row，右栏进入统一 Policy Focus Editor；四个 Role 同时可见并直接编辑，因此不需要靠四个 Component Card 的 Role dropdown 来提高操作效率。

Species Base：

```text
空间机会策略
大口黑鲈 · 基础习性

组件            有效角色       本层意图
────────────────────────────────────────
温度            CORE          [沿用策略模板 ▾]
结构            CORE          [设置为 CORE ▾]
觅食水层        SECONDARY     [设置为 SECONDARY ▾]
时段            IGNORED       [设置为 IGNORED ▾]

fail_env_coeff
来源值 0.01     [调整 ▾] [+0.005]     → 0.015
```

Compat Mode：

```text
组件            有效角色       本模式意图
──────────────────────────────────────────────
温度            CORE          [沿用基础习性角色 ▾]
结构            CORE          [设置为 CORE ▾]
觅食水层        SECONDARY     [使用策略模板原始角色 ▾]
时段            IGNORED       [沿用基础习性角色 ▾]
```

V1 一个兼容 Mode 对应一条既有 FishEnvAffinity 行，因此普通 UI 不显示 row_key / Quality / production row identity，也不保留 multi-row Compat 展开。

### 13.3 Role 与 Profile 正交

Role ordinary edit 走 Autosave。

- IGNORED + Profile absent → 改 CORE / SECONDARY：保存 Role，随后显示 required-Profile ERROR；不自动建 Profile、不自动选 Source、不回滚 Role。
- CORE / SECONDARY → IGNORED：已有 Profile 保留，仍可编辑；仅表示当前计算不消费该 Profile。
- Role 的 Validator ERROR 与 save I/O failure 分开；可 durable 保存但可阻断 Publish。

### 13.4 Policy Template Source

Policy Template Source 只属于 Species Base。

Species Base Policy Card 可提供唯一策略来源选择器：

```text
策略来源
[ Predator Policy ▾ ]
```

更换 Policy Template 会同时影响四个 raw Role baseline 与 fail_env_coeff baseline，因此按 staged mutation 处理，并复用 V1 的短事务 Candidate Review 语义。

Compat Mode 不提供 Policy Source Selector；只读显示：

```text
沿用基础习性 → Predator Policy
```

Mode 只编辑 Role / fail_env_coeff patch，不虚构 policySourceOverride。

## 14. Persistence details hidden from author

Component Card / Focus Editor 不提示 `将存为 cover_largemouth_bass` 或其它 production/materialization row name。

作者只面对 Source / Operation / Role 等语义；物理 name / id 生成属于 Materializer。

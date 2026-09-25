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
结构习性                                           ⛔

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

例如 `-`、`1.` 等尚不能形成完整 typed value 的输入：

- 只存在 UI local raw state；
- 不进入 durable state；
- 不触发 Resolve input；
- Publish 消费最近一次成功 durable revision。

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

## 12. Source Change

Source Selector 只在 Component Card 提供。

例如：

```text
Heavy Cover
→ Rock Cover
```

Source change 不走 ordinary autosave，因为它改变整个 Component 的计算基准。

统一流程：

```text
选择候选 Source
→ 形成唯一 staged candidate
→ Local Rebase / Impact Preview
→ 显式 Confirm
→ revision check
→ atomic durable commit
```

Field ordinary edit 与 Source staged mutation 的重量故意不同：

> 改字段是轻操作；换整套来源是重操作。

具体 Candidate Preview 的布局、锁定规则与失败状态将在下一阶段继续收敛。

## 13. Persistence details hidden from author

Component Card / Focus Editor 不提示 `将存为 cover_largemouth_bass` 或其它 production/materialization row name。

作者只面对 Source / Operation / Role 等语义；物理 name / id 生成属于 Materializer。

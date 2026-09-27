# Fish Habit Editor V1｜Product Contract

> Status: Current Product Contract for V1  
> Scope: Species Habit Authoring Minimum Loop。V1 不创建新的 Species identity / Engagement Mode，不 Author Quality / FishPond / StockRelease / FishRelease，不承诺外部生态数据自动导入，也不包含 Bake Preview。

## 1. 一句话产品模型

V1.0 只编辑已经进入 Editor durable state 的 Species Base / 既有 Compat FishEnvAffinity。作者通过 **Source + 当前层 Authoring Operation** 编辑四类习性与空间机会策略；Resolve 展示派生结果，Publish 将 exact durable Authoring State 物化到本地 Production working tree。V1.0 不提供 Species Base creation。

## 2. Mental Model

### 2.1 我在编辑谁

Fish 是最高层业务对象。

```text
Fish
├─ 常规习性
└─ 特殊习性
   ├─ 幼年          [兼容]
   └─ 大个体        [兼容]
```

- Subject 只在左侧 Subject Navigation 中选择。
- Species Base 是默认 / 常规习性的唯一 Authoring Truth；V1 UI primary label 使用 **“常规习性”**。Contract 中的 `Species Base` 仍是稳定对象名，旧文档里的“基础习性”指同一对象，不新增一层。
- `[兼容]` 是当前承载形态的中性状态，不是 Warning。
- V1 UI 将现有 Compat rows 表达为 **“特殊习性”**，强调它们是相对常规习性的可选偏差，不是把一个 Species 完整切成互斥分桶。
- 现有 physical Compat slot 继续沿用 `young / mature` 承载；V1 UI 分别投影为 **“幼年” / “大个体”**。该 UI label projection 不要求修改底层 bucket token 或 Production English name。
- 特殊习性可以为 0、1 或 2 个；缺少“大个体”不表示数据不完整。一个 Species 完全可以只使用“常规习性 + 幼年特殊习性”。
- V1 一个可编辑特殊习性 Subject 对应一条已经由 ingress / migration 无歧义映射到固定 Compat physical slot 的既有 `FishEnvAffinity` 行；任意未映射 Affinity 不会仅因“已经存在”就自动成为 Subject。
- 普通作者 UI 不要求理解 `FishEnvAffinityRef`、Production row naming 或 materialized row id。

### 2.2 一份习性由什么组成

四个 Component：

- 温度习性
- 结构习性
- 觅食水层习性
- 时段习性

以及独立的空间机会策略。

Component 回答“这条鱼对这个环境轴是什么习性”；Policy 回答“这些习性在聚合中怎样被消费”。Policy 不是第五个 Component。

### 2.3 Component 的核心作者模型

```text
Source
+
当前层 Authoring Operation
=
Effective Profile
```

Editor 保存 Source binding 和作者操作，不把 Effective Value 作为第二份可编辑 Truth。V1.0 的显式 Component Source 包括 Shared Template 与 Existing Production compatibility source；特殊习性还可以选择跟随常规习性。

### 2.4 Truth 与 Derived

唯一长期 Authoring Truth 是 Editor durable state。

```text
Authoring Truth
    ↓
解析预览 Resolve
    ↓
Publish
    ↓
Production materialization
```

V1 不包含 Bake Preview。

Durable authoring intent 包括 Source binding / override、field operation / patch、Role / fail_env_coeff intent、Shared Template content/lifecycle。

Effective Value、Resolve result/provenance、current selection、raw incomplete input、未确认 candidate、validation projection、Publish preflight result 都是 derived / ephemeral，不成为第二份 Truth。

### 2.5 V1.0 Subject baseline

V1.0 不提供“开始配置其他鱼种”或 Species Base creation。

进入普通 Authoring 前，目标 Species 必须已经通过现有 Editor state 或 bounded bootstrap / migration 具备：

- 一个 Species Base / 常规习性 Subject；
- 需要被编辑的既有 Compat FishEnvAffinity（若有）；
- 可解析的 Component Source binding / Policy binding；
- 必要的 stable identity / ledger mapping。

Bootstrap / migration 是数据准备边界，不是普通作者 UI，也不建立第二套长期 Authoring Truth。

若某个 Fish Basic Species 尚未进入 Editor durable state，V1.0 Fish List 不把它显示为“可开始配置”的新对象；新增 Species Base 留给后续明确版本能力。

## 3. Workspace / IA

V1 是 desktop-first wide authoring tool，不以窄屏响应式布局为产品目标。

三栏固定语义：

```text
Subject Navigation | Context / Task Surface | Focus Editor
我在编辑谁？         当前对象整体是什么状态？    我具体看 / 改什么？
```

宽度不写死具体像素；Focus Editor 必须有足够横向空间支持 Inline Field Authoring。1920 级宽桌面是优先优化场景。

### 3.1 Global Topbar

Global Topbar 只承载：

- 工具身份
- Autosave / save failure
- global blocking diagnostics
- staged candidate status
- Publish entry

不承载 Fish / Mode breadcrumb，不重复 Subject Navigation。

### 3.2 左栏两类 Section

```text
FISH
共享资产
```

同一时刻只需一个 Section body 展开并承担滚动；两个 Section header 始终可达。

FISH：

```text
▼ 大口黑鲈
   常规习性
   特殊习性
     幼年          [兼容]
     大个体    [兼容]
▸ 虹鳟
▸ 狗鱼
```

当前 Subject path 保持可见；其它 Fish 使用普通 disclosure，自由展开/折叠。Chevron 只控制展开，不改变 selection。

共享资产：

```text
习性模板
├─ 水温
├─ 结构
├─ 觅食水层
├─ 时段
└─ 空间机会策略
```

V1 Shared Assets 只包含 Shared Template。鱼家族预设 / Species Preset 不进入 V1；V1.0 也不提供 Species Base initialization。

### 3.3 V1.0 Fish coverage

V1.0 Fish Navigation 只展示已经进入 Editor durable state 的 Species / Subjects。

- Species identity 仍来自 Fish Basic / authoritative Species Catalog；
- Habit Editor 不创建新的 Species identity；
- V1.0 不创建新的 Species Base；
- 尚未进入 Editor durable state 的 Species 由 bootstrap / migration 或后续版本能力处理，不在当前 Authoring IA 中制造“开始配置”入口；
- Golden Seed / Snapshot 只用于 demo / regression / migration evidence，不定义产品可编辑范围。

Shared Template 与 Existing Production Source 都可以作为已有 Subject 的合法 Component Source；Source 规则见 [common-semantics.md §2](common-semantics.md#2-source-binding)。

## 4. Context Header

Context Header 属于中栏 Surface，不属于 Global Topbar。

只表达当前对象的**语义层级**，不表达用户从哪个页面点进来，也不常驻显示聚合 authoring status。

Fish 示例：

```text
鱼习性 › 大口黑鲈 › 常规习性
鱼习性 › 大口黑鲈 › 特殊习性 › 大个体 [兼容]
```

Template 示例：

```text
共享资产 › 习性模板 › 水温 › 高温鱼
```

`有本层调整` 不常驻 Context Header；局部 authoring state 由 Component / Policy 自己显示。

## 5. Fish Subject 的两种工作视角

同一 Subject 下：

```text
[ 编辑 ] [ 解析预览 ]
```

它们不是 Subject，也不是独立业务对象。

**编辑**：唯一可改变 Authoring Truth 的主 Surface。

**解析预览**：只读回答“按当前成功持久化的 Authoring Truth，最终配置是什么；为什么会得到这个结果？”

解析预览不提供 authoring controls，不形成第二份 Truth。它复用左栏 Subject Navigation，并把中栏切为 Resolved Overview、右栏切为最短充分的“解析说明”；不进入 Bake / Runtime 条件求值。详细 Contract 见 [secondary-surfaces.md §1](secondary-surfaces.md#1-resolve-preview解析预览)。

## 6. Interaction taxonomy

V1 只保留四类**durable state / transaction 模型**：

| 类型 | 示例 | 持久化模型 |
|---|---|---|
| Ordinary Edit | Field ADD/SET/CLEAR、Role、`fail_env_coeff`、metadata | debounce autosave |
| Staged Mutation | Source change、Shared Template completeValue、Replace References | Candidate → Preview → Confirm → atomic commit |
| Read-only Derived | Effective Value、Resolve、provenance、diagnostics | 不保存为 authoring truth |
| Global Transaction | Publish | Preflight → Execute → Verify |

不新增 Setup transaction、Import transaction、Preview draft 等平行事务类型。

这里的“四类”描述的是**状态模型**，不是说 UI 只能有四种按钮手势。V1 仍有少量 bounded object command，例如：

- Shared Template Blank Create / Extract / Clone：ephemeral form 或当前上下文 → atomic create；
- Archive / Restore：轻量确认或 direct atomic action；
- Hard Delete：满足 guard 后 destructive confirm → atomic delete。

这些动作都**不建立第五种 durable Draft / Candidate / Setup 状态**。只有当动作会对既有 consumer 产生 propagated mutation（例如 Replace References、Template completeValue change）时，才进入 Staged Mutation。

### 6.1 Staged Candidate 的 V1 交互边界

V1 的 staged candidate 是**短事务**，不是可跨页面长期挂起的 Draft。

以 Source Change 为代表：

- Candidate 只能从最近一次成功持久化的 durable state 启动；
- Candidate active 时保留当前 Subject 的空间上下文，但暂停其它导航、ordinary mutation 与 Publish；
- Preview / Confirm / Cancel 在当前事务内闭合；
- Candidate 不写 durable state，也不成为第三个长期工作视角；
- 取消只丢弃 candidate，不回滚已经成功持久化的普通编辑。

具体 Source Change Review 见 [authoring-surface.md §12](authoring-surface.md#12-source-change-candidate)。

## 7. Source Mutation Surface

普通 Fish Authoring 中，**每个 Component 的 Source binding 只在该 Component Card 的 Source Selector 修改**。Policy Template Source 属独立 Policy binding，只在 Species Base Policy Card 修改。

- Component Focus Editor 只展示当前 Source / provenance，可提供“查看模板”等导航，不再放第二个 Component Source Selector。
- Policy Focus 同样不复制 Policy Template Source Selector。
- 旧实现若仍存在顶部 Source Selector，不作为 V1 产品 Contract 要求，应在 projection / migration 中收敛，避免第二 mutation entry。

换 Source 是 staged mutation；改字段是 ordinary edit。两者在交互重量上故意不同。

## 8. Author-facing names vs persistence details

普通 Fish Authoring 界面不显示：

- `FishEnvAffinity` raw row name；
- production subtable row id；
- persistence key 生成规则；
- Materializer 的 delimiter / normalization / collision-domain 等物理细节。

但 Shared Template 是作者资产，因此 Template Context 必须允许直接编辑：

- 中文名：Editor primary display；
- 英文名：作者可读英文语义名，Blank Create / Extract 时由工具先建议、作者可改。

Template 的 stable identity 与名称分离。对于直接复用 Shared Template 的模板级 Production Profile，Materializer 应从 **Template English Name** 确定性派生 Production name；是否加入 Component Kind qualifier 属 G3 的 Production convention。`Struct Heavy Cover`、`Temp Warm Water` 是优先可读示例，但只有在真实 lookup / collision domain 中有价值时才应固化。含 local operation 的 owner-specific Profile 仍由系统生成自己的 projection name。

Template 英文名虽然在 Editor 中是可编辑 metadata，但它会影响下一次 Production projection；rename 的 collision、name-based reference rewrite 与 verify 属 Publish / Materializer 责任，无法证明安全时必须阻断 Publish。

`FishEnvAffinity` 自己的 row name 与 Component/Profile name 是两层不同命名：Affinity row name 由 Species canonical English name + Affinity semantic class 系统派生，V1 不要求作者编辑。Base / Juvenile / Mature 表达的是语义类别，不在 Product Contract 中冻结最终字符串格式。

作者负责业务命名、Source、Operation、Role 等语义意图；稳定 identity、row id 与具体 naming normalization / collision domain 仍属于 Persistence / Materializer Contract。

## 9. Explicit V1 absences

普通 V1 产品 IA 不显示：

- Quality
- Mode Share / Routing
- FishPond / StockRelease / FishRelease
- 新建 Species identity
- 用户创建额外 Engagement Mode / Compat FishEnvAffinity row（系统默认 Affinity projection 除外）
- Family / Preset-assisted Species initialization
- Species Base / system default Affinity Archive / Delete
- 鱼家族预设 / Species Preset
- 钓鱼元素周期表 Import / Lux CLI
- Bake Preview
- CSV persistence controls
- DSL / Gate authoring / script entry

不是 disabled placeholder；没有当前作者价值的入口默认不出现。

## 10. Golden Path

```text
打开 Editor
→ 已有 Habit：直接选择 Fish
→ 无 Habit：从 Fish Basic 选择 Species
   → 选择四个 Component Source + Policy Template
   → atomic create Species Base + system default Affinity projection
→ 左栏选择常规习性 / 已有特殊习性
→ 中栏查看四个 Component + Policy
→ 选择 Component
→ 右栏 Inline Field Authoring
→ 必要时在 Card 换 Source
   → Candidate / Preview / Confirm
→ 普通字段 / Policy Autosave
→ 处理 Validation
→ 解析预览
→ Publish
```

V1 Review 的核心问题：

> 在不依赖后续能力的情况下，一个作者能否从 Fish Basic 选择已有 Species，创建或编辑完整 Species Base，并安全地验证、解析和发布；同时继续编辑已有 Compat Mode？

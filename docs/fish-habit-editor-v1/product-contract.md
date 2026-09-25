# Fish Habit Editor V1｜Product Contract

> Status: Working Candidate  
> Scope: Existing Habit Topology Authoring。V1 不创建新 Fish / 新 Engagement Mode，不 Author Quality / FishPond / StockRelease / FishRelease，不承诺外部生态数据自动导入，也不包含 Bake Preview。

## 1. 一句话产品模型

作者选择一条已有的鱼，在其基础习性或已有中鱼习性模式中，通过 **Source + 当前层 Authoring Operation** 编辑四类习性与空间机会策略；Editor 保存作者意图，解析预览展示派生结果，Publish 将已验证的 durable state 物化到已有 Habit Production topology。

## 2. Mental Model

### 2.1 我在编辑谁

Fish 是最高层业务对象。

```text
Fish
├─ 基础习性
└─ 中鱼习性模式
   ├─ 幼年          [兼容]
   └─ 成年及以上    [兼容]
```

- Subject 只在左侧 Subject Navigation 中选择。
- `[兼容]` 是当前承载形态的中性状态，不是 Warning。
- V1 一个可编辑兼容中鱼习性模式对应一条既有 `FishEnvAffinity` 行。
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

Editor 保存 Source binding 和作者操作，不把 Effective Value 作为第二份可编辑 Truth。

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

Durable authoring intent 包括 Source binding / override、field operation / patch、Role / fail_env_coeff intent、Shared Template content/lifecycle、Species Preset binding。

Effective Value、Resolve result/provenance、current selection、raw incomplete input、未确认 candidate、validation projection、Publish preflight result 都是 derived / ephemeral，不成为第二份 Truth。

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
- staged candidate entry
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
   基础习性
   中鱼习性模式
     幼年          [兼容]
     成年及以上    [兼容]
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

鱼家族预设
├─ 温水掠食鱼
└─ ...
```

“鱼家族预设”是 Species Preset 的产品表达：一次性 Authoring convenience，不是 Fish 的长期父级，也不形成 Resolve inheritance。

## 4. Context Header

Context Header 属于中栏 Surface，不属于 Global Topbar。

只表达当前对象的**语义层级**，不表达用户从哪个页面点进来，也不常驻显示聚合 authoring status。

Fish 示例：

```text
鱼习性 › 大口黑鲈 › 基础习性
鱼习性 › 大口黑鲈 › 中鱼习性模式 › 成年及以上 [兼容]
```

Template 示例：

```text
共享资产 › 习性模板 › 水温 › 高温鱼
```

Preset 示例：

```text
共享资产 › 鱼家族预设 › 温水掠食鱼
```

`有本层调整` 不常驻 Context Header；局部 authoring state 由 Component / Policy 自己显示。

## 5. Fish Subject 的两种工作视角

同一 Subject 下：

```text
[ 编辑 ] [ 解析预览 ]
```

它们不是 Subject，也不是独立业务对象。

**编辑**：唯一可改变 Authoring Truth 的主 Surface。

**解析预览**：只读回答“按当前成功持久化的 Authoring Truth，把 Source、继承、Operation、Role 等解析完以后，最终配置是什么？”

解析预览不提供 authoring controls，不形成第二份 Truth。

## 6. Interaction taxonomy

V1 只保留四类交互模型：

| 类型 | 示例 | 持久化模型 |
|---|---|---|
| Ordinary Edit | Field ADD/SET/CLEAR、Role、`fail_env_coeff`、metadata | debounce autosave |
| Staged Mutation | Source change、Shared Template completeValue、Replace References | Candidate → Preview → Confirm → atomic commit |
| Read-only Derived | Effective Value、Resolve、provenance、diagnostics | 不保存为 authoring truth |
| Global Transaction | Publish | Preflight → Execute → Verify |

不新增 Setup transaction、Import transaction、Preview draft 等平行事务类型。

## 7. Source Mutation Surface

普通 Fish Authoring 中，**Component Card 上的 Source Selector 是主要且唯一的 Source mutation surface**。

- Focus Editor 只展示当前 Source / provenance，可提供“查看模板”等导航。
- 不在 Focus Editor 再放 Source Selector。
- 旧实现若仍存在顶部 Source Selector，不作为 V1 产品 Contract 要求，应在 projection / migration 中收敛，避免第二 mutation entry。

换 Source 是 staged mutation；改字段是 ordinary edit。两者在交互重量上故意不同。

## 8. Persistence details stay hidden

普通作者界面不显示：

- materialized name（例如 `cover_largemouth_bass`）
- production subtable row id
- persistence key 生成规则
- Materializer 的命名细节

作者负责 Source、Operation、Role 等语义意图；物理 projection naming 属 Persistence / Materializer Contract。

## 9. Explicit V1 absences

普通 V1 产品 IA 不显示：

- Quality
- Mode Share / Routing
- FishPond / StockRelease / FishRelease
- 新建 Fish
- 新建 Engagement Mode
- Family 初始化新 Fish
- 钓鱼元素周期表 Import / Lux CLI
- Bake Preview
- CSV persistence controls
- DSL / Gate authoring / script entry

不是 disabled placeholder；没有当前作者价值的入口默认不出现。

## 10. Golden Path

```text
打开 Editor
→ 在 FISH 找到已有 Fish
→ 左栏选择基础习性 / 已有中鱼习性模式
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

> 在不依赖后续能力的情况下，一个作者能否安全地理解、修改、验证并发布已有 Fish Habit topology？

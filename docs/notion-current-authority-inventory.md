# Notion Current 章节级收敛清单

本清单服务于 0.3.4.0-B 编辑器七页 Current 的后续收敛。它不是产品 Contract，不替代七页正文，也不记录 Notion 页面 id、内部链接或凭据。主开发需求不在本批范围。

## 分类与处置规则

| 分类 | 含义 | 处置 |
|---|---|---|
| `OWNER_CONTENT` | 该页在 Git authority model 中唯一拥有的定义、条件、例外或验收边界 | 保留并作为规范源；其它页面只留短摘要与链接 |
| `CONSUMER_SUMMARY` | 为本页读者独立阅读所需的短解释、入口、操作步骤或结果摘要 | 保留短版；不得新增阈值、例外或判定顺序 |
| `HISTORICAL` | 旧实现、旧路线、旧图证据、旧测量或已被替代的推演 | 迁到 `Historical｜…` 载体；Current 正文不留历史隔断 |
| `CONFLICT_NEEDS_OWNER` | 归属、语义或删留边界无法仅凭现行矩阵判定 | 暂不删；先取得 Owner 收口，再形成 exact delta |

## 七页目标分工

| Current 页面 | Git 承接位置 | `OWNER_CONTENT` | `CONSUMER_SUMMARY` | 初步迁移风险 |
|---|---|---|---|---|
| 编辑器与 Resolve | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §1、§8、§9、§11、§15 | 对象模型、编辑 → Resolve → Preview、Resolved Subject、Bake 输出、身份边界 | 面向实现者的最短工作流与结果字段 | 中：与持久层、条件开关有交叉 |
| 编辑器界面 | `docs/review/ui-component-contract-r2/contract-cards.md` Part 1–3 及 A①/A②/共用N2 卡片 | 元素、布局、交互、可见状态、控件行为、Figma 对应 | 卡片操作、显示文案、局部验收 | 高：含图证据与多处局部交互 |
| 编辑器心智模型与 IA | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §1、§4、§7 | 作者词汇、三栏 IA、对象组织、作者阅读模型 | 与操作相邻的认知解释 | 中：与 UI 和持久层术语交叉 |
| 编辑器条件开关 | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §9、§10 | Role 三态、CORE 门控关系、Role 标注方法、编辑器侧校验表现 | Role 操作入口与结果提示 | 低至中：机制判据属于上游产品 Contract |
| Editor → Persistence 数据契约 | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §15；`docs/implementation-brief-0.3.4.0-B.md` §二·2 仅作实现导航 | 物理写回链路、Excel / JSON / 卧龙边界、字段映射入口 | 实现顺序、依赖、任务限定 | 高：Notion 原页明确把字段映射分散到其它页 |
| 编辑器持久层契约 | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §3、§8、§14 | Base/Override、schema、key、operation、bucket、Source、Role patch、reconcile、生命周期 | 持久化摘要与读者入口 | 最高：这是最主要的规范 Owner |
| 配置表与校验 | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §6、§13、§15；`docs/implementation-brief-0.3.4.0-B.md` §二·1–3 仅作实现导航 | 生产字段、Schema / Validator 不变量、错误级别、兼容映射 | UI 呈现、Resolve/Persistence 工作流摘要 | 高：与主需求文档、Persistence 有边界交叉 |

## 重复簇处置表

### A. Source / Operation / CLEAR / SET

- **唯一 Owner**：编辑器持久层契约（Git 承接：汇编 §3、§8、§14）；与配置表与校验的 §6、§13、§15 分工明确：持久层拥有 authoring record / operation 形状，配置表与校验拥有生产字段、Schema / Validator 约束。
- **编辑器与 Resolve**：只保留“来源 + 分层操作 → Resolve → 物化”的心智模型；删除完整 operation allowlist 与字段级例外的重复解释。
- **编辑器界面**：保留作者可见文案、入口和验收；删除 durable 语义、source transaction 完整协议。
- **编辑器心智模型与 IA**：保留用户词汇和作者理解；删除 schema、key 和写回规则。
- **条件开关**：只保留 Role/Policy 的作者操作；不定义 numeric operation。
- **当前状态**：可进入 `OWNER_CONTENT` / `CONSUMER_SUMMARY` 批次；不需要新产品裁定，前提是逐段核对独有例外。

### B. Role / Gate / IGNORED

- **Role authoring Owner**：条件开关（Git 承接：汇编 §9–§10）。
- **Schema / Validator Owner**：配置表与校验（Git 承接：汇编 §6、§13、§15）。
- **持久化形状 Owner**：编辑器持久层契约（Git 承接：汇编 §3.4）。
- **其它页面**：只保留本页读者所需的入口、结果或 Resolve 摘要。
- **当前状态**：可拆成三类摘要，但必须逐段保留 Role/Profile/Policy 粒度差异，不能按字数清理。

### C. Base / Override / Materialize

- **分层与物化 Owner**：编辑器持久层契约（Git 承接：§1、§3.7）。
- **物理写回 Owner**：Editor → Persistence（Git 承接：§15 与 brief 实现导航）。
- **Resolve Owner**：编辑器与 Resolve 只说明解析后的输出与身份。
- **IA Owner**：只说明作者如何理解底板、覆盖、恢复。
- **当前状态**：可收敛；写回规则与产品模型不得混成一节。

### D. 三栏 IA / UI Geometry / 操作面

- **IA Owner**：心智模型与 IA（Git 承接：汇编 §1、§4、§7）。
- **控件与几何 Owner**：编辑器界面（Git 承接：contract-cards Part 1–3）。
- **Resolve/Bake 结果 Owner**：编辑器与 Resolve。
- **当前状态**：可收敛；Figma 版本证据和当前 UI Contract 不能互相替代。

### E. 历史实现与取证

- **Current 内不再承担**：旧实现差异、旧测量、旧版本图、已撤路线和迁移推演。
- **处置**：按原载体和证据范围迁到对应 `Historical｜…` 页面或保留现有固定证据入口。
- **当前状态**：`CONFLICT_NEEDS_OWNER`；本轮尚未对每页托管图片、嵌入块、child page 与历史链接逐块核验，不能据此直接迁移或删除。

## 第一批可执行迁移批次

### 批次 A：条件开关页

范围：只处理 Role / Gate / authoring 标注与条件开关页中的重复摘要。

- 保留：三态、CORE 自动带 Gate、Role transition、作者如何判断 CORE/SECONDARY/IGNORED、编辑器侧校验呈现。
- 收缩：Resolve 公式、持久化记录形状、生产表字段映射、完整 Source/operation 协议。
- 迁出：已废 Role 令牌、旧实现快照和旧路线推演；但先核每段是否为 Current 读法还是 Historical 证据。
- 写入前置：逐段生成 `BEFORE / AFTER / OWNER / reason`，取得指定 canonical writer 放行。

### 批次 B：心智模型与 IA 页

范围：只处理作者词汇、三栏 IA、对象导航与作者阅读模型。

- 保留：`INHERIT / ADD / SET / CLEAR` 的作者语言及三栏职责。
- 收缩：Source transaction、durable key、production writeback、Validator 完整规则。
- **迁出**：旧 IA 方案、被撤下的页内结构和旧测量；具体载体与历史边界本轮未逐块核验，迁移前标 `未核`。
- 先核：哪些段落是当前作者模型，哪些只是实现/历史说明。

### 批次 C：Editor → Persistence 页

范围：只处理物理写回链路和跨页边界。

- 保留：Excel → 卧龙 → JSON 的链路、物理表关系、写回/导出边界；**本轮对其具体实现通路只作仓内来源未核，后续 exact delta 前须绑定实现仓与当前导出命令**。
- 收缩：editor-state schema、Role、Source、Operation 细节，均回链持久层 Owner。
- 迁出：旧实现差异快照和已关闭迁移推演。
- **先核**：当前页中“本页不定义字段映射”与物理落表段的具体承接关系；本轮尚未以实现仓/导出命令证明，标 `未核`。

## 明确不做

- 不修改主开发需求页面。
- 不在本清单里直接写 Notion。
- 不把本清单当作新的产品 Contract。
- 不按标题或字数批量删除段落。
- 不迁移包含托管图片/嵌入块的内容，除非先确认载体和恢复路径。
- 不把 Notion 当前页面版本、预签名图片 URL 或旧快照编号当作规范事实。

## 后续执行闸门

1. 每批先 fresh-read 目标页与 Git 承接章节。
2. 逐段分类；分类无法确定时保留 `CONFLICT_NEEDS_OWNER`。
3. 生成 exact delta，不在本清单内代写正文。
4. 指定 canonical writer 获得授权后才写 Notion。
5. 写入后逐 hunk 回读、块级结构回读，再做 Notion↔飞书对账。

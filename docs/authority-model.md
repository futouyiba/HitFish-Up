# 文档权威与发布投影

本页定义本仓规范文档与外部阅读载体的职责，不定义产品机制。

## 权威分层

- **Owner 裁定**决定产品语义、约束与尚未收口的边界。
- **Git Markdown** 是已收口规范的唯一可 diff 权威载体：规范文本、页面职责、实现 brief 与历史归档先在仓内形成，经 PR 审核后才成为现行仓内规范。
- **Git history 与 PR** 保存作者归属、审核结论、变更范围和版本锚；普通修订不另写流水账。
- **Notion Current** 是面向人和对话式阅读的发布投影，不是高频多 Agent 协作写入面。Notion 中的规范性改动只有在回流 Markdown、经审核合并并重新发布后才生效。
- **Notion 评论**是反馈与讨论，不直接改变规范文本。

Notion 仍适合承载人工浏览、评论和不依赖仓库的阅读入口；没有对应 Git 仓库的设计资料可以继续以 Notion 为主要工作载体。对本仓已有 Markdown 投影的内容，规范变更以 Git 中最近一次已审核合并的版本为准。

## 当前批次的范围

本策略首先覆盖 0.3.4.0-B 编辑器七个 Current 页面及其仓内投影。主开发需求页面不纳入本轮职责重划或瘦身；涉及它的产品语义仍按其现行 Owner 处理。

仓内消费者可以保留足以独立阅读的短摘要、操作说明、验收场景和证据边界，但不得在摘要中新增阈值、例外、判定顺序或其它可独立演化的规范性 Contract。每项规范事实在仓内只保留一个人工维护的 Owner；其它位置链接或引用该 Owner。

## 七页职责矩阵

| Current 页面 | Git Markdown 承接章节（章节级唯一 Owner） | 该 Owner 维护什么 | 消费者可保留 | 不在该 Owner 内维护 |
|---|---|---|---|---|
| 编辑器与 Resolve | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §1 `产品拓扑与三栏`、§8 `Source 选择器 ＋ Rebase Preview`、§9 `Profile × Spatial Opportunity Policy`、§11 `Profile 生命周期`、§15 `跨层护栏` | 编辑器整体心智模型、编辑 → Resolve → Preview 工作流、resolved / bake 产品输出 | 面向操作的短流程、验收场景与结果字段摘要 | editor-state schema、逐字段持久化形状、生产表不变量、纯 UI 几何 |
| 编辑器界面 | `docs/review/ui-component-contract-r2/contract-cards.md` Part 1 `控件总清单`、Part 2 `第一批 Contract Cards`、Part 3 `第二批 Contract Cards` 及其中的 A① / A② / 共用N2 卡片章节 | UI 元素、布局、交互、可见状态与控件行为 | 卡片操作步骤、显示文案、局部验收和画面证据边界 | durable operation 语义、完整 Source 事务、生产表 schema |
| 编辑器心智模型与 IA | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §1 `产品拓扑与三栏`、§4 `字段控件（FieldValueControl）`、§7 `组件卡 ＋ 焦点编辑栏` | 作者词汇、对象组织方式、三栏 IA 与作者阅读模型 | 与具体操作相邻的短解释 | durable record shape、校验实现、生产写回规则 |
| 编辑器条件开关 | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §9 `Profile × Spatial Opportunity Policy`、§10 `Role 与 Policy 的操作词表` | Role / Gate 的 authoring 语义、条件开关表现与相关校验边界 | 组件卡中的 Role 操作和结果提示 | editor-state 记录形状、完整 evaluator、生产列结构 |
| Editor → Persistence 数据契约 | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §15 `跨层护栏`；实现组织见 `docs/implementation-brief-0.3.4.0-B.md` §二·2 `操作、引用与物化入口` | 编辑器到配置表的物理导出、写回链路与字段映射边界 | 实现顺序、依赖和任务限定 | editor-state schema 的完整定义、UI 交互、产品规则副本 |
| 编辑器持久层契约 | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §3 `Source × Operation 正交`、§8 `Source 选择器 ＋ Rebase Preview`、§14 `模板工作区与模板生命周期` | editor-state schema、key、operation、bucket、Source、reconcile 与生命周期 | 面向消费者的持久化摘要和链接 | UI 布局、生产表字段不变量、历史实现快照 |
| 配置表与校验 | `docs/review/ui-component-contract-r2/component-contract-consolidated.md` §6 `校验 × Autosave`、§13 `字段能力表`、§15 `跨层护栏`；实现组织与记录/Schema 入口见 `docs/implementation-brief-0.3.4.0-B.md` §二·1 `记录入口与保留字段`、§二·2 `操作、引用与物化入口`、§二·3 `Schema、版本与载体` | 生产表结构、字段不变量、Schema / Validator 规则在仓内的规范投影 | 受影响字段和阻断结果摘要 | editor-state 记录形状、UI 交互、历史验证状态 |

本矩阵把现有审阅包中的章节作为七页的 Git 承接位置；同一文件内的其它章节不因共用文件而获得该页的 Owner 权限。后续若需要让每页独立发布，可在单独批次把这些章节拆成七个文件，但本批不复制正文。若一个主题横跨多个 Owner，应把交叉点拆成各自的输入、输出和引用关系；不能在两个页面各维护一份完整行为。

## 发布到 Notion 的规则

1. 先冻结要发布的 Git commit、文件范围和本矩阵；先解决 Owner 归属冲突，再生成发布内容。
2. 逐段把 Current 内容分类为：Owner 正文、消费者摘要、历史材料或未收口冲突。没有明确新 Owner 的内容不因“重复”直接删除。
3. 取得本批指定 canonical writer 的明确授权后，按现有 Notion 写入纪律执行：fresh read → exact delta 或受控整篇重建 → 结构与块级回读 → fresh readback；含镜像的页面再做对应对账。
4. 发布后，Notion 只作为这份 Git 规范的阅读投影；人工在 Notion 发现的修正先回流 Markdown，不能在页面上形成第二份长期规范。

本批只建立仓内 authority policy 和职责矩阵，不重建 Notion 页面、不创建发布工具、不修改主开发需求或产品 Contract。公开仓不保存外部页面 id、内网链接、凭据或同步状态。

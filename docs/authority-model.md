# 文档权威与发布投影

本页定义本仓规范文档、产品版本与外部阅读载体的职责，不定义产品机制。Current Authority 与历史版本必须分离；历史 Review 包可以保留完整证据，但不得因仍可阅读就自动获得 Current 解释权。

## 权威分层

- **Owner 裁定**决定产品语义、约束与尚未收口的边界。尚未落仓的 Owner 裁定仍按 Owner 直令执行并如实标明未落仓范围；它不自动成为已审核合并的仓内 Contract。
- **Git Markdown** 是已收口规范的唯一可 diff 权威载体：规范文本、页面职责、实现 brief 与历史归档先在仓内形成，经 PR 审核后才成为现行仓内规范。矩阵所列章节是承接入口，不代表对应 Current 的全部内容已经完整承接。
- **Git history 与 PR** 保存作者归属、审核结论、变更范围和版本锚；普通修订不另写流水账。
- **Notion Current** 是面向人和对话式阅读的发布投影，不是高频多 Agent 协作写入面。对已由 Markdown 承接的内容，Notion 页面编辑本身不改变仓内 Contract；规范修订须回流 Markdown 并经审核合并，随后更新发布投影。Owner 直令按上项处理，不因发布尚未完成而失效。读取 Notion 不是日常设计、实现或审核的前置条件；需要仓内尚未承接的外部设计上下文或 Owner 裁定时，才按名检索并核对当前载体。
- **Notion 评论**是反馈与讨论，不直接改变规范文本。

Notion 仍适合承载人工浏览、评论和不依赖仓库的阅读入口；没有对应 Git 仓库的设计资料可以继续以 Notion 为主要工作载体。对本仓已有 Markdown 投影的内容，规范变更以 Git 中最近一次已审核合并的版本为准。

## 当前版本关系

Fish Habit Editor 文档按**产品版本**理解，不再把 Review Round 编号当成跨版本的永久语义层。

```text
V0.1  ≈ R1 historical lineage
V0.2  = R2 historical package
V1    = docs/fish-habit-editor-v1/ Current
```

- 当前仓树中存在 R2 目录，不存在独立 R1 目录；因此 V0.1 只作为历史 lineage 说明，不为补齐编号而伪造一套 R1 文件。
- R2 保留原目录名 `docs/review/ui-component-contract-r2/`，避免破坏历史链接、证据锚点与 PR 对照；其语义角色改为 **V0.2 historical design / review evidence**。
- V1 是当前产品与语义 Authority。
- 后续若 V1 中的公共语义稳定跨越 V1 / V1.0.1 / V1.1+，再把 `common-semantics.md` 提取到独立 common 目录；在此之前不提前制造跨版本抽象层。

## Fish Habit Editor V1 Current

Current 入口：`docs/fish-habit-editor-v1/`。

- `product-contract.md`：V1 Mental Model、产品 IA、Workspace、Truth / Derived 边界、interaction taxonomy 与产品负向边界。
- `common-semantics.md`：V1 当前消费的 Source / Operation / Resolve / Policy / Validation / staged mutation / Template lifecycle / Publish materialization 公共语义。
- `authoring-surface.md`：Fish Subject 核心编辑屏、Species Habit initialization、导航、Context Header、Component / Policy Overview、Focus Editor 与交互。
- `shared-assets.md`：Shared Template 创建、提取、传播影响、引用与生命周期维护。
- `secondary-surfaces.md`：Resolve Preview、Publish 以及后续真正闭合的 V1 次级 Surface。
- `implementation-brief.md`：V1 当前工程落点、实现顺序与尚需确认的窄实现细节；不重新定义产品语义。
- `docs/review/fish-habit-editor-version-scope.md`：V1 范围与后续阶段边界。

Current Authority 关系：

```text
Version Scope
    ↓
V1 Product Contract ───────┐
                          ├→ V1 Surface Contracts
V1 Common Semantics ──────┘
                          ↓
              Implementation / Figma projection
```

每项规范事实仍只维护一个 Current Owner。V1 Surface 可以为可读性保留短摘要，但 Source / Operation / Policy / Validation 等公共规则以 `common-semantics.md` 为 V1 当前解释入口。

## V0.2 / R2 历史版本包

`docs/review/ui-component-contract-r2/` 现在只承担：

- V0.2 当时的设计状态；
- Review Target / OPEN-ITEMS / Figma snapshot；
- 历史裁定、固定 SHA 与证据链；
- V1 规则的历史来源参考。

它**不再承担**：

- V1 的最终产品 IA；
- V1 的 Source / Operation / Policy / Validation 最终语义解释；
- V1 的 Publish / Resolve 产品交互；
- “因为 R2 曾经写过，所以可以把已被 V1 裁掉的能力重新带回 Current”。

当 V1 与 R2 冲突时：

> **对 V1 范围内的产品与语义，读 V1；R2 只解释历史，不参与 Current arbitration。**

若需要追查某条 V1 规则如何形成，可以从 V1 的 Git blame / PR / 历史引用回看 R2；不能反过来让历史包成为隐藏上游。

## V0.2 历史承接矩阵（非 Current）

下表保留 R2 当时对七页投影的组织方式，只用于版本考古 / evidence lookup，**不是当前 Owner Matrix**。

| V0.2 页面主题 | R2 历史承接位置 | 当前 V1 入口 |
|---|---|---|
| 编辑器与 Resolve | `component-contract-consolidated.md` | `product-contract.md` + `secondary-surfaces.md` |
| 编辑器界面 | `contract-cards.md` | `authoring-surface.md` + `secondary-surfaces.md` |
| 编辑器心智模型与 IA | R2 汇编 §1/§4/§7 | `product-contract.md` |
| 编辑器条件开关 / Policy | R2 汇编 §9/§10 | `common-semantics.md` + `authoring-surface.md` |
| Editor → Persistence | R2 汇编 §15 | `common-semantics.md`；实现细节再读 implementation brief |
| 编辑器持久层语义 | R2 汇编 §3/§8/§14 | `common-semantics.md` |
| 配置表与校验 | R2 汇编 §6/§13/§15 | `common-semantics.md`；具体实现 / schema 再读 implementation brief |

这张历史矩阵不得被新文档引用为 Current semantic owner。

## 发布到 Notion 的规则

1. 先冻结要发布的 Git commit、文件范围和本矩阵；先解决 Owner 归属冲突，再生成发布内容。
2. 逐段把 Current 内容分类为：Owner 正文、消费者摘要、历史材料或未收口冲突。没有明确新 Owner 的内容不因“重复”直接删除。
3. 取得本批指定 canonical writer 的明确授权后，按现有 Notion 写入纪律执行：fresh read → exact delta 或受控整篇重建 → 结构与块级回读 → fresh readback；含镜像的页面再做对应对账。
4. 发布后，Notion 只作为这份 Git 规范的阅读投影；人工在 Notion 发现的修正先回流 Markdown，不能在页面上形成第二份长期规范。

本页只维护仓内 Authority / versioning policy 与发布投影边界，不替代具体 Product Contract。公开仓不保存外部页面 id、内网链接、凭据或同步状态。

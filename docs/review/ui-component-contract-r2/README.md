# 0.3.4.0-B｜UI Component Contract — Review Target（R2，2026-09-21）

**这是当前唯一的对外审阅面。** 它取代此前那个多轮修订容器；**本目标不含修订链**。

## 阅读目标

只拿到本目录即可判断投影及其证据边界，不需要先读旧审阅史。普通修订过程由 Git commit／diff／PR history 保存。

## 本目录包含什么

| 文件 | 是什么 |
|---|---|
| `README.md` | 本文件。范围、权威、基线、怎么读 |
| `REVIEW-PROMPT.md` | **先读这个** —— 审核范围、风险分级与收口 |
| [OPEN-ITEMS.md](OPEN-ITEMS.md#active-review-items) | **唯一问题状态台账**：处置、剩余工作、关闭证据；先读当前审查项，再查裁决出处 |
| `component-contract-consolidated.md` | 共用规则的仓内完整投影与索引，逐条带产品出处 |
| `contract-cards.md` | 操作、显示、记录与验收场景；共用机制直链汇编，卡片独有约束在此维护 |
| [figma-current.md](figma-current.md#image-evidence) | 按版本登记画面事实、图像指纹、证明范围及历史回读 |
| [开发 brief](../../implementation-brief-0.3.4.0-B.md) | 实现组织、依赖与尚无其它完整仓内投影的实现限定 |
| `img/` | 随包图像；逐张版本、角色与证据边界见[图像登记](figma-current.md#image-evidence) |
| `archive-snapshot/` | 不改写的版本化物证与 `MANIFEST.sha256`；保护范围和当前对照见[图像登记 §十一](figma-current.md#十一已知漂移共享母件-9354-的作者可见串修正--顶栏右移-53px) |

## ★ 图证据的**射程**（读之前先知道你能核到什么）

本目录可核的图像及各自版本统一见[图像登记](figma-current.md#image-evidence)。同一节点的整帧与局部图可能来自不同阶段，不能因导出参数相同就当成同批证据；引用前应核对具体资产的证明范围。

未随包的投影只能检查文字是否自洽、是否与执行卡相抵，不能据此验证画布。没有图不等于投影不存在；离开画布不可判的内容标 `NOTE: 不足以判`。缺证据对应的处置与剩余工作见[问题台账](OPEN-ITEMS.md#active-review-items)。

## 权威（本目录是派生物，不是权威）

**Product Authority 是项目内的 Notion Current／Owner 裁定，决定产品事实。Repository Projection Owner／仓内投影 Owner 只决定该事实在仓内由哪个位置完整维护，不升级为产品 Authority。** 图像是特定版本的物证；OPEN-ITEMS 汇总问题状态，不能改变产品规则。独立审查关闭以对应 exact head 的 REVIEW 为依据；文档修改的审核要求见[风险分级](REVIEW-PROMPT.md#review-closure)。

本目录**不含任何内部链接** —— 按项目对外规则，内部 URL 与页面 id 一律不进仓。因此文中的 **《页名》§N** 是**项目内载体的引用**，在本目录里读不到 ⇒ **遇到这类引用，审「这句话本身是否自洽」，不要去核出处**；若某条离开出处就不可判，用 `NOTE` 标出即可（那本身就是有用的信号）。

直接相关的 Current（按名引用，不提供链接）：

- 《中鱼因子聚合逻辑化-开发需求》（主开发需求）
- 《编辑器与 Resolve》
- 《编辑器界面》
- 《编辑器心智模型与 IA》
- 《Editor → Persistence 数据契约》
- 《编辑器持久层契约》（durable schema 的 canonical owner）
- 《编辑器条件开关》
- 《配置表与校验》

<a id="projection-maintenance"></a>
## 投影维护边界

- 消除的是**独立维护的规范性重复**。消费者可保留足以独立阅读的非规范性摘要，直链完整定义；摘要不得新增阈值、例外、判定顺序或其它可独立演化的 Contract。不要用多层跳转拼接一个完整行为。
- 生成投影可以完整重复，但必须可复现、可检查、不允许人工独立编辑，且生成身份和来源可识别。未标识生成身份的文字不能据此豁免去重。
- 以 **Normative Manual Edit Fan-out** 衡量重复维护成本：同一产品事实变化需人工同步多少个独立维护的规范性位置，仓内目标通常为 **1**。消费者独有的行为、验收和实现说明不计为规范性重复，但须明确依赖关系；上游到仓内的人工传递另行说明，不宣称已自动消除。
- 上表只登记文档职责，不扩成逐字段的 Owner Matrix。每批迁移的仓内投影 Owner、消费者、独有内容及验证结果记在 PR，不新增长期迁移台账。
- 理解 Contract 必需的短理由随定义保留；跨 Contract 或很可能重开的重要设计才考虑独立 Decision／Negative Knowledge。普通修订过程交给 Git，不将流水账换名保存。
- 冻结基线、独立审核报告和实验原始记录不按今天的术语追溯改写。当前引用注明已知 target／version 和证明范围；未知不补造。

## 基线（exact baseline）

| 载体 | 基线 |
|---|---|
| 本目录 | 见本 PR 的 head SHA |
| 上游评审容器 | [PR #6](https://github.com/futouyiba/HitFish-Up/pull/6)（历史材料入口） |
| 下游实现投影 | [programaticHitFish PR #16](https://github.com/futouyiba/programaticHitFish/pull/16)（实现线入口，状态以该 PR 为准） |

**CLEAR 查阅入口**：组件解析与记录语义在[汇编 §3](component-contract-consolidated.md#component-clear)，Policy 域在[§10](component-contract-consolidated.md#policy-clear)，组件 allowlist 在[§13](component-contract-consolidated.md#component-operation-allowlist)，落盘例外在[§4](component-contract-consolidated.md#field-value-control)，四格 UI 在[卡2](contract-cards.md#operation-control)。这些都是 Notion Current 的投影；历史比较与 Figma 文字按各处固定 SHA 保留。

## 怎么读

1. 先读 `REVIEW-PROMPT.md`（审什么、怎么报）。
2. 再读[问题台账](OPEN-ITEMS.md#active-review-items)（本次审查的未结事项、依据与关闭边界）。
3. 然后按 `REVIEW-PROMPT.md` 指向的文件读。

**不要**去翻旧容器的评论来建立上下文 —— 本目标的自足性就是它存在的理由。**若你发现某条离开旧史就不可判，直接报 `NOTE: needs history`**，那是有效信号，不是你的失误。

# 0.3.4.0-B｜UI Component Contract — Review Target（R2，2026-09-21）

**这是当前唯一的对外审阅面。** 它取代此前那个多轮修订容器；**本目标不含修订链**。

## 为什么另起一个目标

判据只有一句：**一个只拿到本目录的审阅者，不读任何旧审阅史，能不能直接审。**

旧容器的答案是**不能** —— 它累计了 **98 条**审阅证据（5 个端点）、54 个 finding 编号、16 份 `REVISION` 文件，且**编号会在不同轮次里被复用改义**（同一编号先关后开再关）。**修订链不迁移到本目标**：**git 历史本身就是修订链**，旧的 `REVISION-1…16` 仍在仓库历史里可查。

## 本目录包含什么

| 文件 | 是什么 |
|---|---|
| `README.md` | 本文件。范围、权威、基线、怎么读 |
| `REVIEW-PROMPT.md` | **先读这个** —— 审什么、怎么输出、四条纪律 |
| [OPEN-ITEMS.md](OPEN-ITEMS.md#active-review-items) | **唯一问题状态台账**：处置、剩余工作、关闭证据；先读当前审查项，再查裁决出处 |
| `component-contract-consolidated.md` | 《组件契约（现行）》—— 两套并列材料对拍合并后的**汇编**（逐条带出处） |
| `contract-cards.md` | **冻结卡**（执行投影）—— 实现按这个做 |
| [figma-current.md](figma-current.md#image-evidence) | 按版本登记画面事实、图像指纹、证明范围及历史回读 |
| `img/` | 随包图像；逐张版本、角色与证据边界见[图像登记](figma-current.md#image-evidence) |
| `archive-snapshot/` | ★ **归档消费者的像素级历史外观**（`FROZENSNAPSHOT-pre-*.png`，冻结版本 `2401504721345405021`）＋ **当前对照**（`CURRENT-*.png`）＋ **未变对照组**（`CONTROL-94-334-*.png`）＋ `MANIFEST.sha256`。**活体归档帧不再负责「非证据性 chrome」的逐像素一致 —— 那份责任由它承担**（**`OWNER-DECIDED`**：裁定 `ADJ-FIG-ARCHIVE-01`，见 `figma-current.md` §十一）。 |

## ★ 图证据的**射程**（读之前先知道你能核到什么）

本目录可核的图像及各自版本统一见[图像登记](figma-current.md#image-evidence)。同一节点的整帧与局部图可能来自不同阶段，不能因导出参数相同就当成同批证据；引用前应核对具体资产的证明范围。

未随包的投影只能检查文字是否自洽、是否与执行卡相抵，不能据此验证画布。没有图不等于投影不存在；离开画布不可判的内容标 `NOTE: 不足以判`。缺证据对应的处置与剩余工作见[问题台账](OPEN-ITEMS.md#active-review-items)。

## 权威（本目录是派生物，不是权威）

**产品权威是项目内的 Notion Current／Owner 裁定**，本目录只做投影。图像是特定版本的物证；OPEN-ITEMS 汇总问题状态，不能改变产品规则。审查是否关闭，以对应 exact head 的独立 REVIEW 为准。

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

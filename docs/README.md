# 文档阅读入口

先按任务选择当前规范、发布投影或版本化证据。仓内规范的权威分层与七页职责见[文档权威与发布投影](authority-model.md)；审阅包是当前消费者与证据投影，职责见[审阅包入口](review/ui-component-contract-r2/README.md#projection-maintenance)，Markdown 改动的风险分级与审核收口见[审阅说明](review/ui-component-contract-r2/REVIEW-PROMPT.md#review-closure)；本页只导航，不另维护规则或问题状态。

## 当前工作入口

| 需要回答的问题 | 入口 |
|---|---|
| Fish Habit Editor V1 的产品范围、Mental Model、IA 与核心交互 | [V1 Product Current](fish-habit-editor-v1/README.md) |
| Source / Operation / Policy / Validation / Template lifecycle / Publish materialization 等当前共用语义 | [V1 Common Semantics](fish-habit-editor-v1/common-semantics.md) |
| V0.2 历史设计、旧审阅结论与证据 | [UI Component Contract R2](review/ui-component-contract-r2/README.md)；只作历史版本 / evidence，不作 Current semantic authority |
| 实现顺序、依赖及独有实现限定 | [开发 brief](implementation-brief-0.3.4.0-B.md) |
| 审阅包问题处置、关闭依据及剩余取证 | [问题台账](review/ui-component-contract-r2/OPEN-ITEMS.md#active-review-items) |
| 随包画面版本、指纹及证明范围 | [图像登记](review/ui-component-contract-r2/figma-current.md#image-evidence) |

## 历史验证与取证入口

下列材料保留当时的陈述和证据，不作为今日产品规则或实现进度。引用结论时使用其声明的 target／version 与 scope；未登记的实现 head 不补造。这里的“固定文件版本”标识文档快照，**不等于被测实现版本**。

| 材料 | 已知 target／scope 与使用边界 |
|---|---|
| [Implementation Readiness](implementation-readiness.md)／[Gap Log](implementation-gap.md) | 2026-09-18 对 Fixed Bake executable reference 的来源核对、测试与缺口登记；不是生产编辑器完成证明。固定文件版本：[readiness](https://github.com/futouyiba/HitFish-Up/blob/f70f02afd04244571b9f5973f737451b3214cf30/docs/implementation-readiness.md)、[gap](https://github.com/futouyiba/HitFish-Up/blob/f70f02afd04244571b9f5973f737451b3214cf30/docs/implementation-gap.md)。原“已解决／仍未决／待写回”按该时点读取；今天是否仍成立须另取证，不在旧报告上更新状态。可运行参考的入口见[reference README](../reference/0340-fixed-bake/README.md)。 |
| [偏移检查报告](offset-check-0.3.4.0-B-20260921.md)／[落仓说明](offset-check-0.3.4.0-B-20260921.LANDING-NOTE.md) | 报告声明实现基线 `bae6e6f`；落仓说明登记部分行号跨 `bae6e6f`／`3cb3074`／`ecbd1df`，并说明 `b003dfe` 上的读数。按每个锚的修订理解，不统一改成最新行号。固定快照：[报告](https://github.com/futouyiba/HitFish-Up/blob/fde61e3d3da68f1f2181c4fd37d1e76c348a098f/docs/offset-check-0.3.4.0-B-20260921.md)、[说明](https://github.com/futouyiba/HitFish-Up/blob/42c6968adb02c78e853dfd40d7055b2676cddeab/docs/offset-check-0.3.4.0-B-20260921.LANDING-NOTE.md)。说明中的后续修复、待同步及 PR 合并顺序属于原交付时点，不是今天的待办；本次未重新运行实现验证。 |

PR #9 基线差异的后续取证见 [CXR9-BASELINE-01 窄重核](reviews/CXR9-BASELINE-01-REVALIDATION-20260921.md)：固定历史实现 `bae6e6f`，仅替代 Source Override 与 TimePeriod 覆盖护栏的受影响判定，不代表今日实现状态。

冻结基线、独立审核报告、实验原始记录及图像快照保持原貌，按原目标和版本使用；不因整理术语而追溯改写。普通修订过程从 Git commit／diff／PR history 查阅，不另维护历史汇编。Blind holdout 的访问限制仍按项目约定，本入口不展开其内容。

# Proposal C｜裁定与裁决记录归档（2026-10-30）

状态：历史证据归档。以下四份文件是 2026-10-30 的裁定请求、顾问建议、Fish Condition 裁决与 Owner 决定记录，按原样迁入；唯一改动是把指向设计包与 `prototypes/` 的相对链接前缀改写为从归档目录可达的路径，正文其余内容保持迁入前状态，不再随现行 Candidate 设计包更新。

迁移日期：2026-11-04；迁移基准：`main` 提交 `d8182977`。

| 文件 | 迁入前路径 | 迁入前 Git blob | 角色 |
|---|---|---|---|
| adjudication-request | `docs/proposals/` | `60aab51fc6e99c31aa27092997a2382d820f5f27` | 第一轮玩法闭合问题单（Issue #152） |
| adjudication-recommendation-2026-10-30 | `docs/proposals/` | `044f446737f2c8c550fc4bc567510191564a343c` | 顾问建议与 Owner 确认（Issue #152） |
| fish-condition-rulings-2026-10-30 | `docs/proposals/` | `e65542be43028215fb68cf6fa3f82066fac72022` | Fish Condition A–H 裁决记录（Issue #161） |
| fish-condition-owner-decisions | `docs/proposals/` | `09660828b4d550437f9a1d92d4b8d3267fb5850b` | Fish Condition 七项 Owner 裁定记录（Issue #161） |

使用边界：

- 迁移差异已逐文件对照迁入前 blob：`adjudication-request` 仅 13 处链接前缀改变，`adjudication-recommendation` 字节一致，`fish-condition-rulings` 与 `fish-condition-owner-decisions` 各 1 处链接前缀改变；
- 这些文件里的分支名、提交号和“待裁定 / 待合并”状态都属于当时时点，不代表现状；
- 现行执行口径以 `main` 上的 Candidate 设计包为准：[设计骨架](../../proposals/lure-response-proposal-c-design-spine.md)、[当前审阅入口](../../proposals/lure-response-proposal-c-current-review-entry-2026-10-27.md)、[Fish Condition Production Contract](../../proposals/lure-response-proposal-c-fish-condition-production-contract.md)、[开放决策](../../proposals/lure-response-proposal-c-open-decisions.md)；
- 归档内容不因迁入而升级为 Current Contract 或生产规则。

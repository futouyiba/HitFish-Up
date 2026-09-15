# HOLDOUT-HANDOFF-R0 — Blind Holdout 交接契约

- 状态:**PROPOSAL**(补自审 P2-8;baseline §12 只规定了选择权归属,未规定抽样框)
- 执行时点:baseline 晋升(或 Owner 宣布按 R0 冻结)之后、run 1 实现开始之前。

## 1. 输入(Owner 提供,全部需钉住版本)

| 输入 | 内容 | 钉住方式 |
|---|---|---|
| 抽样框(sampling frame) | item / presentation 候选总体快照(商品目录或设计内 item 清单,含未上线候选) | 快照文件 + 版本号/commit |
| Species × Engagement Mode 清单 | 可评估组合 | 同上 |
| Technique 词汇表 | 玩家可用 technique 枚举 | 同上 |
| 排除清单 | [DEVSET-REGISTRY-R0](DEVSET-REGISTRY-R0.md) 全部 case(同 item × technique 粒度排除) | 引用注册表版本 |

无钉住的抽样框不得开始抽样——这是事后检查 frame-gaming 的基准。

## 2. Sample Agent 职责

- 从抽样框内独立选取 N 个 Item × Presentation(× Species × Mode)case。
- 自行决定并记录:N 的取值与理由、抽样方法、分层(建议至少覆盖 dev set 未覆盖的 Species 与 item 类别——非强制约束,由其专业判断,但必须记录)。
- 产出**封存清单**,仅交付 Owner / Reviewer;不与 Coding Agent 交流任何候选身份。

## 3. 隔离规则

- Coding Agent 工作区不得出现 holdout 身份;run 1 实现冻结前只可见 count / strata 汇总。
- holdout 评估在实现冻结后、独立会话中执行(见 [EXP-PROTOCOL-FCF-PC-R0](EXP-PROTOCOL-FCF-PC-R0.md) §4 步骤 1)。
- 评估脚本与数据入库时以 holdout 序号代替 item 身份,直至 run 报告发布。

## 4. 验收(Reviewer 执行)

- 抽样框未被缩小(所选 case 全部出自钉住快照)。
- 排除清单生效(与 dev set 无同 item × technique 重叠)。
- 封存与交付链路完整(清单未经 Coding Agent 中转)。

任一不满足 → 作废重抽,并记录作废原因。

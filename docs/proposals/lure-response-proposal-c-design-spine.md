# Proposal C｜设计骨架

状态：Working Design / Candidate。本文用于收敛设计，不是 Current Contract，也不是生产参数批准。

口径来源：本包按 `docs/lure-response-joint-evaluation` 的 `311ae70d` Working Closure 快照核对，整理成一份可审阅的设计包；该分支在此之后持续更新，本轮未逐条重新纳入。引用前先核对该分支当前 head。

## 1. 设计问题

在一条鱼、一次实际呈现和一个局部交互机会下，系统需要回答：

> 这次呈现能否形成一次摄食响应，响应强度如何，以及它怎样进入候选留存。

本设计不直接预测咬口概率，不从商品名称推断猎物身份，也不把所有状态压成一个总分。

## 2. 主链

```text
ActualPresentation
→ PreyInterpretation
→ PreyConditionedState
→ FishCondition
→ DecisionMargin
→ ConditionalResponse
→ PreyModeResponse
→ Opportunity join
→ CandidateRetention
```

每一层只负责自己的问题。上游事实可以被多个层读取，但同一种作用只能由一个 owner 结算。

## 3. 五个评价项

第一版主体是一个加性出手余量。各子机制先把自己的结果换算到同一标尺，顶层只做竞争：

```text
出手余量
= 食物价值
+ 攻击诱因
- 追赶负担
- 风险顾虑
- 摄食意愿门槛
```

| 评价项 | 回答的问题 | 购买的玩家策略 |
|---|---|---|
| 食物价值 | 这个目标本身值不值得吃 | 选什么：广谱还是高匹配 |
| 攻击诱因 | 当前猎物状态是否额外促使出手 | 普通口还是反应口 |
| 追赶负担 | 当前呈现对这条鱼有多难追 | 搜多快：快速搜索还是慢速精细 |
| 风险顾虑 | 当前呈现有多容易露馅 | 直接强势还是隐蔽自然 |
| 摄食意愿 | 现在需要多强的理由才愿意出手 | 门槛高低 |

每项的输入、合成方式与边界见[五评价项契约](lure-response-proposal-c-evaluation-items.md)。

预测困难（Prediction）当前不在第一版主体内，只保留为待证明的局部代价。原因见[开放决策](lure-response-proposal-c-open-decisions.md)。

## 4. 负向边界

- 玩家输入指令不能直接冒充实际呈现。
- 猎物支持不等于 FoodValue、Suspicion、可得程度或咬口概率。
- 未知不等于零。
- 缺少规则不等于 NoMatch。
- `Reject` 不进入连续计算；`Poor=0` 仍是合法连续值。
- 状态标签不自动附带 bonus 或 penalty。
- 时间长度不进入出手余量；机会由 `L × C` 表达。
- Candidate 后段不能再次乘同一份 Response。
- 没有独立 owner 的作用不能补进某个系数。
- 不能用一个巨大的 cost 冒充 hard semantic boundary。

## 5. 计算顺序

1. 校验呈现实例、装配版本和时间范围。
2. 读取实际事实及其解析状态。
3. 按装配绑定运行适用的猎物解释规则，输出已校准的 support。
4. 按猎物解释提取当前状态、事件和 TriggerIntensity。
5. 读取鱼侧评价输入，先处理 typed status，再计算数值。
6. 在局部 latent bearing 内计算出手余量并投影成条件响应。
7. 聚合同级猎物解释，得到 feeding 区间或标量。
8. 与 Spatial / Opportunity 的 `L` 做一次 `L × C`，交给 Candidate owner。

任何一步的必要输入未解析，都不能把缺口静默转换为零。

## 6. 设计交付

- [语义契约](lure-response-proposal-c-semantic-contract.md)：逐层写输入、输出、状态、owner 和禁止事项；
- [呈现解释与状态契约](lure-response-proposal-c-presentation-interpretation.md)：证据、支持度插值、区间与状态提取规则；
- [五评价项契约](lure-response-proposal-c-evaluation-items.md)：食物价值、攻击诱因、追赶负担、风险顾虑与门槛的合成方式和边界；
- [响应与机会契约](lure-response-proposal-c-response-opportunity.md)：投影、sibling 区间、`L × C` 与候选接入；
- [工作案例](lure-response-proposal-c-worked-cases.md)：用反例检查每层是否真的区分了不同情况；
- [开放决策](lure-response-proposal-c-open-decisions.md)：只保留尚未有 owner、尚未闭合或存在冲突的问题；
- [第一轮玩法闭合审查](lure-response-proposal-c-first-round-closure.md)：AttackTrigger 准入、Risk 输入实证、策略排序 probe 与判断；
- [Escape-like Trigger v1](lure-response-proposal-c-escape-trigger-v1.md)：事件、窗口、family 适用与 TriggerIntensity 判定；
- [机会量支持](lure-response-proposal-c-opportunity-support.md)：`L`、遭遇饱和与单位时间收益的玩具模型；
- [鱼况/Bake 契约](lure-response-proposal-c-fish-condition-bake-contract.md)：从 Response 消费需求反推 Fish Condition 的产出要求；
- [Fish Condition 裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md)：2026-10-30 的 A–H 裁决与仍待 Owner 的事项；
- [Fish Condition Owner 决定请求](lure-response-proposal-c-fish-condition-owner-decisions.md)：剩余七项与选项；
- [设计图](../mockups/proposal-c-design-map.html)：面向阅读的图形版本。

这些材料共同构成 Proposal C 的设计工作包，不替代已审核的 Current Contract。

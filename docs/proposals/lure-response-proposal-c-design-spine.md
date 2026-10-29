# Proposal C｜设计骨架

状态：Working Design / Candidate。本文用于收敛设计，不是 Current Contract，也不是生产参数批准。

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
→ TemporalOpportunity
→ CandidateRetention
```

每一层只负责自己的问题。上游事实可以被多个层读取，但同一种作用只能由一个 owner 结算。

## 3. 五个问题

| 层 | 回答的问题 | 输出 |
|---|---|---|
| ActualPresentation | 实际发生了什么？ | 带时间、单位、参考系和来源的事实 |
| PreyInterpretation | 这些事实支持哪些猎物解释？ | 按猎物组织的支持值或区间 |
| PreyConditionedState | 按该解释看，当前呈现处于什么状态？ | 状态维度、事件和时序关系 |
| FishCondition | 对这条鱼，这次机会的价值和负担是什么？ | FoodValue、成本、门槛及其状态 |
| Response / Opportunity | 已解析评价怎样形成响应并随机会进入候选？ | 条件响应、聚合结果和 Candidate contribution |

## 4. 负向边界

- 玩家输入指令不能直接冒充实际呈现。
- 猎物支持不等于 FoodValue、Suspicion、可得程度或咬口概率。
- 未知不等于零。
- 缺少规则不等于 NoMatch。
- `Reject` 不进入连续计算；`Poor=0` 仍是合法连续值。
- 状态标签不自动附带 bonus 或 penalty。
- 时间长度不直接进入 `DecisionMargin`。
- Candidate 后段不能再次乘同一份 Response。
- 没有独立 owner 的作用不能补进某个系数。

## 5. 计算顺序

1. 校验呈现实例、装配版本和时间范围。
2. 读取实际事实及其解析状态。
3. 按装配绑定运行适用的猎物解释规则。
4. 按猎物解释提取当前状态和时序关系。
5. 读取鱼侧评价输入，先处理 typed status，再计算数值。
6. 在局部 latent bearing 内计算 `DecisionMargin` 和条件响应。
7. 聚合同级猎物解释。
8. 交给 Temporal Opportunity 和 Candidate owner。

任何一步的必要输入未解析，都不能把缺口静默转换为零。

## 6. 设计交付

后续设计按四份材料推进：

- [语义契约](lure-response-proposal-c-semantic-contract.md)：逐层写输入、输出、状态、owner 和禁止事项；
- [工作案例](lure-response-proposal-c-worked-cases.md)：用反例检查每层是否真的区分了不同情况；
- [开放决策](lure-response-proposal-c-open-decisions.md)：只保留尚未有 owner 或尚未完成标定的问题。

这四份材料共同构成 Proposal C 的设计工作包，不替代已审核的 Current Contract。

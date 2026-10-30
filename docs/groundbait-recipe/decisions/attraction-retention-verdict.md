# Attraction / Retention 判断

> 状态：Candidate / Working Decision
> 日期：2026-10-29
> 边界：本页判断 Attraction / Retention 是否需要独立模块，不定义 FCF Current Contract。

## 1. 要判断什么

两个候选中间语义：

- **Attraction**：鱼是否被信号吸引、发现或趋近 Feeding Place。
- **Retention**：鱼是否愿意继续留在 Feeding Place 或持续摄食。

判断标准是：现有链是否已经有生产者、消费者和状态能表达它们；如果新增独立模块，是否会产生重复计权或循环依赖？

## 2. 判断标准

一个中间语义值得成为独立模块，至少满足：

1. 有独立的输入、输出和单位；
2. 有唯一生产者和明确消费者；
3. 不能被现有状态确定性派生；
4. 能解释现有模块无法表达的策略差异；
5. 不会与现有阶段重复计权。

否则，它应保持为派生摘要或解释词，而不是独立模块。

## 3. Attraction

### 3.1 现有覆盖

- Feeding Event 的 `encounter` 处理“鱼是否可能发现或接近对象”。
- Feeding Event 的 `selection` 处理“鱼更愿意尝试哪个对象”。
- Chemical Cue Field 和 Food 响应分别进入 encounter 和 selection。
- Response Stage 处理候选权重的整体调整。

### 3.2 判断

Attraction 目前不需要独立模块。它是 `encounter` 和 `selection` 的上位解释词，不是独立状态或系数。

理由：

- 新增 `AttractionCoeff` 再乘进响应，会与 encounter / selection 重复计权。
- 如果 Attraction 只是 `P(encounter) × P(approach)` 的摘要，它可以由 Feeding Event 派生，不需要新 owner。
- 现有证据不足以证明存在独立于 encounter / selection 的“吸引力”机制。

### 3.3 允许的用法

- 作为解释词：描述 encounter / selection 的结果。
- 作为派生摘要：例如 `AttractionOpportunity ≈ P(encounter) × P(approach)`，只用于展示或调试，不再乘入响应。
- 若未来要成为独立模块，必须证明它不能被 encounter / selection 派生，且有独立输入输出。

## 4. Retention

### 4.1 现有覆盖

- Feeding Place State 的 `persistence / turnover` 描述对象和线索随时间的变化。
- Physical Release 的 `A(t)`、`L(t)`、`U(t)` 描述可用食物如何减少或离开。
- Feeding Event 可以重复发生，形成持续摄食的时间序列。
- Fish Condition 的 `Wariness` 和 `Feeding Motivation` 可以随时间变化。
- Response Stage 可以按次调整候选权重。

### 4.2 判断

Retention 目前不需要独立模块。它是重复 Feeding Event、Feeding Place 持久性和 Fish Condition 的组合结果，不是单独系数。

理由：

- 新增 `RetentionCoeff` 再乘进响应，会与持久性、鱼况和重复事件重复计权。
- 现有链可以表达“食物持续存在，鱼反复遇到并摄食”，这已经覆盖“留在窝点”的一部分。
- 但“鱼是否移动到窝点、是否长期停留、局部鱼群是否增加”没有显式建模。这是 Local Population / Residence 的缺口，不是 Retention 系数能解决的。

### 4.3 缺口

- 局部鱼群 / 招募：Feed 是否提高该区域的鱼量或机会权重。
- 鱼的空间停留：鱼是否移动到窝点并停留。
- Overfeeding：投喂过多是否降低局部鱼群或咬口。
- 跨 session 记忆：补窝历史是否影响下一次。

这些应作为独立候选问题处理，而不是塞进一个 `RetentionCoeff`。

### 4.4 允许的用法

- 作为解释词：描述重复事件和持久性的结果。
- 作为派生摘要：例如“时间窗口内重复 Feeding Event 的累计有效摄食”，只用于展示或调试，不再乘入响应。
- 若未来要成为独立模块，必须先定义 Local Population / Residence 的状态和证据。

## 5. 结论

| 候选 | 是否独立模块 | 当前处理 |
|---|---|---|
| Attraction | 否 | encounter / selection 的上位解释词；可由事件派生摘要 |
| Retention | 否 | 重复事件 + 持久性 + 鱼况的组合结果；缺口是 Local Population / Residence |
| Selection | 否 | Feeding Event 内部步骤 |
| Ingestion | 否 | Edible Size + Feeding Event 已覆盖 |

不新增 `AttractionCoeff` 或 `RetentionCoeff`。任何需要这两个词的场合，先说明它对应哪个现有阶段，或标为 OPEN。

## 6. 翻转条件

出现以下证据时，可以重新判断：

- Attraction：存在独立于 encounter / selection 的机制，且不能被事件概率派生。
- Retention：存在独立的停留 / 招募机制，且不能由重复事件、持久性和鱼况表达。
- 玩法需要区分“鱼发现了但不吃”和“鱼根本没发现”，而现有 encounter / selection 无法表达。

翻转时必须给出：

- 新模块的输入输出；
- 唯一生产者；
- 与现有阶段的去重方案；
- 反例和 Fixture。

## 7. 最小反例

- 同一 Cue 同时提高 encounter 和 `AttractionCoeff`：重复计权。
- 同一持久性同时提高 `RetentionCoeff` 和响应权重：重复计权。
- 鱼没有被吸引但已经遇到对象：Attraction 不应覆盖 encounter。
- 鱼遇到对象但不选择：Attraction 不应覆盖 selection。
- 窝料持久性高但鱼不摄食：Retention 不应自动提高响应。

## 8. 未收口

- Local Population / Residence 是否需要独立模块。
- Overfeeding 是否首版纳入。
- 重复事件的累计方式。
- 鱼的空间移动是否需要建模。
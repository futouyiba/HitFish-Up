# Fish Condition 接入

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页只整理 Fish Condition 在完整中鱼链中的位置和消费者，不定义更新公式，不修改 `docs/terminology.md`。

## 1. 已验证的 Current 语义

`docs/terminology.md` §5.2 定义 `Fish Condition` 为鱼侧动态参数，随天气、时段等输入变化，供响应等计算使用。四个参数：

| 参数 | 含义 | 已知下游 |
|---|---|---|
| `Activity` | 当前整体活跃程度 | 响应；也可向刺鱼、搏鱼提供输入 |
| `Feeding Motivation` | 当前摄食意愿 / 驱动力 | 响应 |
| `Diet Shift` | 当前相对于基础食性的动态偏移 | 响应 |
| `Wariness` | 当前警觉程度，随过程累积 | 响应 |

术语同时写明：更新公式、时间粒度与下游消费关系由对应机制 Contract 定义。仓内目前没有这些公式。

Fish Condition 的工作更新算法见 [`end-to-end-algorithm.md`](end-to-end-algorithm.md) §4。该算法只是 Candidate / Working Algorithm；时间尺度、cause 输入、生命周期和生产字段仍需对应 Owner / Current Contract 收口。

## 2. 状态位置

```text
天气 / 时段 / 水温 / 光照 / 溶氧 / 水流 / 事件
        ↓
     Fish Condition
        ↓
     Response
        ↓
  后续中鱼、刺鱼、搏鱼
```

Fish Condition 是状态，不是分数。它描述鱼现在处于什么状态，不直接描述某条鱼会不会被抽中。

## 3. 消费者矩阵

| 消费者 | 可读取 | 不能读取 / 不能做的事 |
|---|---|---|
| 环境烘焙 | 不读取 | 不能把 Fish Condition 当作环境条件重新烘焙 |
| Response | Activity、Feeding Motivation、Diet Shift、Wariness | 不能把 Fish Condition 直接当作最终权重 |
| Feeding Event（候选） | 不直接消费 Fish Condition 数值；仅保留候选边界和事件结构 | 未获对应 Condition Contract 授权前，不读取 Wariness 等数值；不能把 Fish Condition 当作动作能力或对象约束 |
| 圆桌 | 不直接读取 | 不能把鱼况乘进候选权重 |
| Fish AI | Activity（边界） | 不在本仓定义具体消费公式 |

## 4. 与窝料、Food、Flavor 的边界

- 窝料产生 Feeding Place State，不直接写 `Activity`、`Feeding Motivation`、`Diet Shift`、`Wariness`。
- Food 和 Flavor 的 Exposure 影响发现、趋近或 Response 候选，不直接写 Diet Shift。
- 如果未来要表达持续摄食改变鱼况，必须单独定义时间、记忆和衰减，不在本页隐含发生。
- 天气、时段等环境输入优先进入现有 Fish Condition 语义，不转换成简单的味型密码。

## 5. 单参数问题

### 5.1 Activity

- 影响响应，也可能影响刺鱼、搏鱼。
- 与 `EnvCoeff` 的边界：环境系数已经表达环境对鱼机会的影响，Activity 表达鱼当前的整体状态；同一环境事实不能在两处各算一次。

### 5.2 Feeding Motivation

- 影响鱼是否愿意响应和摄食。
- 与 Food / Flavor 的边界：Food 和 Flavor 描述刺激，Feeding Motivation 描述鱼当前的意愿；刺激不直接改写意愿。
- 当前只按已声明的 Response 接口消费；若未来 Feeding Event 获得独立机制授权，才可讨论动作选择消费，不影响对象尺寸约束。

### 5.3 Diet Shift

- 是 Fish Condition 的动态偏移，不是静态食性配置。
- 更新时间尺度、是否有记忆、是否跨 session，全部 OPEN。
- Food / Flavor 的 Exposure 不直接写 Diet Shift。

### 5.4 Wariness

- 随过程累积，影响后续响应。
- 与 Sparse Avoidance 分开：Wariness 是状态，Avoidance 是稀疏配置的 Cue 排斥。
- 两者的来源和 trace 必须分别保留，不能合并成一个负分。

## 6. 与现有术语的缺口

- `Feeding Readiness` 在候选文档中出现，但术语表没有定义。未裁定前，它只作为描述性说法，不作为独立状态落 Schema。
- Fish Condition 的 baseline 载体已由 [Issue #161](https://github.com/futouyiba/HitFish-Up/issues/161) 定为 DEF 条件组下的 snapshot / block；更新公式、时间粒度、记忆和衰减仍未落仓。当前只有 Wariness 具备 runtime overlay 的语义依据；具体运行时更新仍须由 Wariness 机制 Contract 授权，并闭合事件来源、粒度、衰减、有效期和会话记忆。Activity、Feeding Motivation、Diet Shift 不自动获得 runtime 更新。
- Fish Condition 是否随地点、条件组或鱼个体变化，没有落仓。

以上登记在 `decisions/conflict-register.md` 的 C-12a1、C-12a2、C-12a3、C-12b、C-13a、C-13b、C-14。

## 7. 最小结构反例

- 下雨直接切换食性：天气被当成味型密码。
- Wariness 只累积不衰减：状态无界。
- 每杆随机 Diet：食性变成不可学习噪声。
- 同一温度既进环境系数又进 Fish Condition：重复计权。
- 窝料持续释放直接写 Feeding Motivation：窝料越权。

# Proposal C｜标定台账（Working 参数）

状态：Working Register / Candidate。记录当前所有 Working 参数、含义、使用位置与缺失的数据来源；不是生产标定表。

## 1. 参数速读

下表用白话解释每个参数管什么，以及现在用的试探值。数值全部是 Working / Probe，不是生产参数。

| 参数 | 白话解释 | 当前 Working |
|---|---|---:|
| `M0` | 开始有响应的 Margin 门槛。Margin ≤ M0 时 C=0 | 0.00 |
| `M1` | 达到满响应的 Margin 锚点。Margin ≥ M1 时 C=1 | 0.40 |
| `TriggerBudget` | 反应口最多允许给 DecisionMargin 加多大一块，防止 Trigger 变成主导一切的超级奖励 | 0.10，护栏约 0.15 |
| `K_close` | 追赶困难在 Margin 里有多“贵” | 0.76 |
| `K_wary` | `Wariness × SuspicionLoad` 换算成 RiskCost 时的总尺度 | 1.0（probe） |
| Motivation tail start | Motivation 高到哪里以后，进入“门槛快速下降区” | 0.80 |
| Motivation tail extra slope | 进入 tail 后，门槛额外下降多快 | 0.50 |
| support anchors | 作者配置 prey evidence 时的参考档位：0.40 约为“有相关线索但区分力有限”，0.90 约为“形态已经很明确” | 0.40 / 0.90 |
| Opportunity `D` | 玩具模型里“停留/机会量随速度衰减”的尺度 | 0.80 |
| Opportunity `Q_cap` | 玩具模型里单位时间遭遇率开始饱和的速度尺度 | 1.00 |
| `coverage` | 玩具模型里某方案实际覆盖多少空间，用来测试隐蔽方案的覆盖成本 | 0.55（probe） |

另外两个门槛参数没有单独成行，属于摄食意愿门槛公式的一部分：

| 参数 | 白话解释 | 当前 Working |
|---|---|---:|
| threshold base | Motivation 为 0 时的门槛高度 | 0.60 |
| threshold slope | Motivation 每升一点，门槛下降多少 | 0.40 |

## 2. 参数台账

| 参数 | 白话解释 | 当前 Working | 使用位置 | 需要什么才能标定 |
|---|---|---:|---|---|
| `M0` | 开始有响应的 Margin 门槛 | 0.00 | 响应投影 | reference stories 的零响应边界 |
| `M1` | 达到满响应的 Margin 锚点 | 0.40 | 响应投影 | 满响应边界 |
| threshold base | Motivation 为 0 时的门槛高度 | 0.60 | 摄食意愿门槛 | 鱼情分布与咬口数据 |
| threshold slope | Motivation 每升一点，门槛下降多少 | 0.40 | 摄食意愿门槛 | 同上 |
| tail start | 进入门槛快速下降区的 Motivation | 0.80 | 摄食意愿门槛 | 高 Motivation 分布 |
| tail extra slope | 进入 tail 后门槛额外下降的速度 | 0.50 | 摄食意愿门槛 | 同上 |
| `TriggerBudget` | 反应口给 DecisionMargin 加分的上限 | 0.10（护栏 0.15） | 攻击诱因 | 反应口钓获对照 |
| `K_close` | 追赶负担换算成 Margin 成本的尺度 | 0.76 | 追赶负担 | 速度与咬口的排序数据 |
| `K_wary` | Wariness × SuspicionLoad 换算成 RiskCost 的尺度 | 1.0（probe） | 风险顾虑 | 钓压与警戒数据 |
| support anchors | prey evidence 的参考档位 | 0.40 / 0.90 | 猎物解释 | 证据配置一致性 |
| 机会 `D` | 停留/机会量随速度衰减的尺度（玩具模型） | 0.80 | 机会量玩具模型 | 有效区域尺寸与停留数据 |
| 机会 `Q_cap` | 单位时间遭遇率的饱和尺度（玩具模型） | 1.00 | 机会量玩具模型 | 单位时间遭遇数据 |
| `coverage` | 方案实际覆盖的空间比例（玩具模型） | 0.55（probe） | 隐蔽方案 | 隐蔽装备的实际覆盖损失 |
| `tau_recover` | Trigger 强度恢复的时间常数 | 未定 | Prediction（Deferred） | 若重开才需要 |

## 3. 使用规则

- 表中数值全部是 Working / Probe，不得写成生产参数；
- 白话解释只帮助阅读，不改变参数归属与公式；
- 任何参数改动都要同时更新使用它的文档与 probe；
- 标定必须给出数据来源、样本范围与排序验收，而不只是拟合误差；
- `Prediction`、`CapacityModifier` 已不在 active 主体，参数只在重开时才登记。

## 4. 缺数据清单

- Fish Condition 的 cause / 曲线数据（Activity、Motivation、Diet Shift、Wariness）；
- 鱼种级 `InterceptSpeedLimit` 与体型缩放；
- 实际水流与相对水速；
- 机会量的空间与时间分布；
- 装备显眼度的事实来源；
- 生产采样、滤波与最大间隔。

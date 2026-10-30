# Proposal C｜标定台账（Working 参数）

状态：Working Register / Candidate。记录当前所有 Working 参数、使用位置与缺失的数据来源；不是生产标定表。

## 1. 参数

| 参数 | 当前值 | 使用位置 | 数据类型 | 需要什么才能标定 |
|---|---:|---|---|---|
| `M0` | 0.00 | 响应投影 | 体验预算锚 | reference stories 的零响应边界 |
| `M1` | 0.40 | 响应投影 | 体验预算锚 | 满响应边界 |
| threshold base | 0.60 | 摄食意愿门槛 | 线性基线 | 鱼情分布与咬口数据 |
| threshold slope | 0.40 | 摄食意愿门槛 | 斜率 | 同上 |
| tail start | 0.80 | 摄食意愿门槛 | 拐点 | 高 Motivation 分布 |
| tail extra slope | 0.50 | 摄食意愿门槛 | 斜率 | 同上 |
| `TriggerBudget` | 0.10（护栏 0.15） | 攻击诱因 | effect-size 预算 | 反应口钓获对照 |
| `K_close` | 0.76 | 追赶负担 | 成本系数 | 速度与咬口的排序数据 |
| `K_wary` | 1.0（probe） | 风险顾虑 | 乘子 | 钓压与警戒数据 |
| support anchors | 0.40 / 0.90 | 猎物解释 | 证据档位 | 证据配置一致性 |
| 机会 `D` | 0.80 | 机会量玩具模型 | 停留尺度 | 有效区域尺寸与停留数据 |
| 机会 `Q_cap` | 1.00 | 机会量玩具模型 | 遭遇饱和 | 单位时间遭遇数据 |
| `coverage` | 0.55（probe） | 隐蔽方案 | 覆盖比例 | 隐蔽装备的实际覆盖损失 |
| `tau_recover` | 未定 | Prediction（Deferred） | 时间常数 | 若重开才需要 |

## 2. 使用规则

- 表中数值全部是 Working / Probe，不得写成生产参数；
- 任何参数改动都要同时更新使用它的文档与 probe；
- 标定必须给出数据来源、样本范围与排序验收，而不只是拟合误差；
- `Prediction`、`CapacityModifier` 已不在 active 主体，参数只在重开时才登记。

## 3. 缺数据清单

- Fish Condition 的 cause / 曲线数据（Activity、Motivation、Diet Shift、Wariness）；
- 鱼种级 `InterceptSpeedLimit` 与体型缩放；
- 实际水流与相对水速；
- 机会量的空间与时间分布；
- 装备显眼度的事实来源；
- 生产采样、滤波与最大间隔。

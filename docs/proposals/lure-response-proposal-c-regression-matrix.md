# Proposal C｜回归矩阵

状态：Working Test Map / Candidate。把设计包里的规则映射到可执行 probe，并写明每个 probe 能证明什么、不能证明什么。

## 1. 覆盖表

| 规则 | 可执行入口 | 能证明 | 不能证明 |
|---|---|---|---|
| 支持度插值 `s = b + (u-b)·f` 与取 max | `proposal_c_interpretation_probe.py`（研究分支） | 插值、单证据取 max、类型汇总 | 生产锚点、真实识别 |
| 支持区间与缺失传播 | 同上 | 区间上下界、未知不填零 | 采样频率下的稳定性 |
| 状态分段与移动后停留 | `presentation_state_probe.py`（研究分支） | 阈值、确认时刻、已观测下界 | 真实鱼行为 |
| 逃逸触发窗口与取 max | `proposal_c_escape_trigger_probe.py` | 窗口过滤、family 适用、不累加、pause 不参与、状态传播 | 事件提取公式与生产阈值 |
| 响应投影形状 | `proposal_c_response_projection_probe.py` | 截断线性的端点与单调性 | 生产 `M0/M1` |
| Closing 成本形状 | `proposal_c_closing_cost_shape_probe.py` | `u_close` 与成本的单调关系 | 完整高速策略排序 |
| support × response | `proposal_c_support_retention_projection_probe.py` | 比例保留形状 | 生产 support 尺度 |
| Trigger 形状 | `proposal_c_prediction_challenge_probe.py` | 单次事件衰减 | 生产 `tau_recover` |
| 三组策略排序 | `proposal_c_strategy_probe.py` | 反应口成立、快搜只部分成立、隐蔽需要外部成本 | 生产参数、覆盖收益 |
| 机会量与单位时间收益 | `proposal_c_opportunity_support_probe.py` | 内部最优、低活性更慢、隐蔽翻转 | 生产 `L` 函数、探索收益 |
| 端到端状态传播 | `proposal_c_end_to_end_probe.py` | Unknown/Reject/区间/L 缺失、单次乘法 | 生产标定 |
| Fish Condition 解析 | `proposal_c_fish_condition_probe.py` | baseline、过期、缺来源、授权 overlay 与回落 | 真实生成与曲线 |

## 2. 缺口

- 研究分支的 `proposal_c_interpretation_probe.py` 与 `presentation_state_probe.py` 不在本分支，矩阵只引用其结论，不声称本地可跑；
- 没有覆盖 Fish Condition 生成的真实数据；
- 没有覆盖生产采样、滤波与设备输入；
- 没有性能或稳定性回归。

## 3. 使用规则

- 任何机制改动都必须指出受影响的矩阵行与 probe；
- 新增 probe 必须写清“能证明 / 不能证明”，不能只报通过；
- 生产标定不属于本矩阵。

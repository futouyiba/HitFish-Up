# Proposal C｜机会量 L 的生产函数草案（Candidate）

状态：Working Design / Candidate。按 2026-10-30 Owner 裁定（Issue #152），`L` 的正式 owner 是 Opportunity，Spatial 只提供空间事实。本文给 `L` 的生产结构、单位、身份、窗口与状态规则，不给生产标定，也不是 Current Contract。

## 1. L 回答什么问题

- `L` 回答：这条鱼在这个语义颗粒上有多少次有效遭遇机会。
- `C` 回答：遇到时鱼多愿意出手。
- `q = L × C` 只乘一次。
- `L` 不进入出手余量；时间、停留与覆盖不改变五项评价。

## 2. 输入

- Spatial facts：位置、区域、几何、有效空间窗口，含垂直可交互窗口；
- 颗粒运动事实：速度、轨迹、停顿；只作为几何输入，不在这里解释猎物；
- 时间事实：决策窗口、窗口开闭；
- 鱼侧可交互范围：reaction window 与 strike reach，尚未生产化。

## 3. 结构

```text
L(颗粒 g) = r_g × τ_g

r_g  单位时间有效遭遇率
τ_g  有效可交互窗口时长
```

- `r_g` 来自空间几何与相对运动：鱼与颗粒进入可交互关系的频率。
- `τ_g` 来自停留、轨迹与窗口：颗粒保持在可交互范围内的时长。垂直运动只通过垂直可交互窗口影响 `τ_g`。
- 初始可用玩具模型近似（见[机会量支持](lure-response-proposal-c-opportunity-support.md)）：`r ≈ q / (1 + q / Q_cap)`，`τ ≈ D / (D + q)`。玩具参数不是生产值。

## 4. 身份、去重与重算

- 颗粒必须有稳定语义身份或稳定语义划分；
- 同一 opportunity identity 的重算是 replay，不增加 `L`；
- 一个 runtime tick 或一次重复调用不是新机会；
- 同一事实可被 Response 与 Opportunity 同时读取，但同一作用只在一个 owner 结算：Response 不乘 `L`，Opportunity 不重算 `C`。

## 5. 覆盖

- 实际空间覆盖不产生快搜 bonus；它只决定哪些颗粒存在，不进入单个颗粒的 `L`；
- 玩具模型把 coverage 当集合因子；生产化时由 Opportunity 按实际扫过区域生成颗粒集合。

## 6. 归约

- Opportunity Reduce 对 `q_i,j` 求和，不重复乘 Response；
- 归约形状（sum / max / 截断）属于 Opportunity owner；第一版默认 sum，需 probe 与分布检查后定；
- 不加 runtime total cap 掩盖重复计权。

## 7. 状态

| 情况 | 结果 |
|---|---|
| `L` 未配置或无法解析 | `ResolutionIncomplete`，不是零机会 |
| 已解析 `L = 0` | 该窗口确实没有机会 |
| 区间未收敛 | 区间 + `ResolutionIncomplete`，不进入 roll |
| 配置或输入错误 | `InvalidInput`，不 roll |

## 8. 不变量

1. `L` 不进 Margin；
2. `q = L × C` 单次乘法；
3. 停留只改 `τ`，不改 `C`；
4. 垂直运动只经 `τ` 与窗口，不进入 Closing；
5. 快搜没有独立数值 bonus；
6. `Unknown` 不等于 0。

## 9. 验收与 probe

- `prototypes/lure-response/proposal_c_opportunity_support_probe.py`：玩具模型形状；
- `prototypes/lure-response/proposal_c_end_to_end_probe.py`：`L` 缺失与单次乘法；
- 待补：replay 去重、窗口开闭、覆盖率与颗粒集合的 probe。

## 10. 未闭口

- `r` 的生产来源：encounter geometry、reaction window、strike reach；
- `τ` 的测量、滤波与最大间隔；
- 归约形状与窗口口径；
- 垂直可交互窗口的定义与数据来源；
- 真实 encounter geometry 闭合后是否引入 hard interception gate。

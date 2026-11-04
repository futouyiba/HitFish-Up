# Proposal C｜机会量 L 的生产函数草案（Candidate）

状态：Working Design / Candidate。按 2026-10-30 Owner 裁定（Issue #152），`L` 的正式 owner 是 Opportunity，Spatial 只提供空间事实。本文给 `L` 的生产结构、单位、身份、窗口与状态规则，不给生产标定，也不是 Current Contract。

上游输入：控饵系统的“原子手法 + 分子手法”定义与时间参数（[飞书：控饵技能与分子手法](https://pisn3u3ony2.feishu.cn/wiki/JGmPwPeq9iFLBpkM1dtcEr0PnBO)，2026-11-04 读取）。原子手法为抽、抖、挑、停、收；分子手法是原子的有序组合，带最大时窗、最小/最大衔接间隔、冷却、重复衰减 `K(n)` 与事件消耗规则。技能持续时间为 6000–12000 ms。

## 1. L 回答什么问题

- `L` 回答：这条鱼在这个语义颗粒上有多少次有效遭遇机会。
- `C` 回答：遇到时鱼多愿意出手。
- `q = L × C` 在本文只作为 Opportunity 内部量；2026-11-04 Owner 方向下，圆桌接口以 `SpatialDistributionWeight × AdaptationCoeff` 为准，`L` 的并入方式待定。
- `L` 不进入出手余量；时间、停留与覆盖不改变五项评价。

## 2. 输入

- Spatial facts：位置、区域、几何、有效空间窗口，含垂直可交互窗口；
- 颗粒运动事实：速度、轨迹、停顿；只作为几何输入，不在这里解释猎物；
- 手法事件：原子手法（抽、抖、挑、停、收）与分子手法组合，含最大时窗、最小 / 最大衔接间隔、冷却与重复衰减 `K(n)`；
- 时间事实：技能持续时间、决策窗口、窗口开闭；
- 鱼侧可交互范围：reaction window 与 strike reach，尚未生产化。

## 3. 结构

```text
L(颗粒 g) = r_g × τ_g

r_g  单位时间有效遭遇率
τ_g  有效可交互窗口时长
```

- 颗粒 `g` 按手法语义定义：一次原子手法事件，或一次命中的分子手法组合；
- `τ_g` 取三者最小：手法最大时窗（或技能持续时间内可用段）、空间可交互窗口、本次机会的有效窗口；分子手法的衔接间隔只用于判定组合是否成立，不直接加进 `τ_g`；
- `r_g` 来自空间几何与相对运动：鱼与颗粒进入可交互关系的频率；
- 初始可用玩具模型近似（见[机会量支持](lure-response-proposal-c-opportunity-support.md)）：`r ≈ q / (1 + q / Q_cap)`，`τ ≈ D / (D + q)`。玩具参数不是生产值。

## 4. 身份、去重与重算

- 颗粒必须有稳定语义身份：原子手法事件带事件 id；分子手法命中沿用组成事件的 id 集合；
- 分子手法按控饵系统的匹配规则消耗原子事件；被消耗的事件不再生成第二个颗粒；
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
2. `q = L × C` 只作为 Opportunity 内部量；圆桌接口按 `SpatialDistributionWeight × AdaptationCoeff`（2026-11-04）；
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
- 分子手法的重复衰减 `K(n)` 是否应进入 `L`（并入 `r` 还是 `τ`），还是完全留给 Response；
- 颗粒粒度是否就等于“原子 / 分子手法事件”，还是需要更细的连续呈现颗粒；
- 按 2026-11-04 Owner 方向，圆桌接口以 `SpatialDistributionWeight × AdaptationCoeff` 为准；`L` 如何并入该接口（进入 SDW 的哪一项，或暂不作为单独因子）仍未定；
- 真实 encounter geometry 闭合后是否引入 hard interception gate。

# Proposal C｜Fish Condition 机制契约 v0（Candidate）

状态：Working Mechanism Contracts / Candidate。按 Issue #161 的架构编写：各 Condition 的语义、合法 cause、输出域、Candidate 生成形状与验收在这里；生产曲线、系数与标定数据仍未闭合。不是 Current Contract，不是生产参数。

上游：[机制骨架](lure-response-proposal-c-fish-condition-mechanisms.md)、[Production Contract](lure-response-proposal-c-fish-condition-production-contract.md)。本文不改变载体、快照与状态协议。

## 0. 通用约定

- 四个 Condition 都是鱼侧状态，不是奖励或惩罚；
- 同一上游事实可以进入多个 Condition，但每个 Condition 必须写清自己的 cause → 输出语义；同一效果不在两处重复结算；
- 生成不读取玩家当前操作；历史遭遇只作为声明了来源与时间范围的摘要输入；
- 所有公式都是 **Candidate 形状**：给出变量、方向与边界，系数是占位符，必须由标定替代；
- 越界、过期、缺来源一律按 Production Contract §4–§6 处理，不截断后继续用。

通用验收：

1. 输出落在声明域内，越界值不静默放行；
2. 每个 cause 的单调方向与边界写清，可被 probe 反例证伪；
3. `Unknown` 不默认成任何常量；
4. 生成结果只经 Bake baseline 或授权 overlay 进入 resolved 值。

## 1. Activity（活跃度）

| 项 | 内容 |
|---|---|
| 语义 | 当前愿意为主动追赶付出多少行为代价；不是物理速度能力 |
| 输出域 | `[0, 2]`；常规状态不突破 `1`，`>1` 只用于极少数极活跃情形；`1.0` 是 Working reference，不是默认值 |
| 更新路径 | Bake baseline；V1 不做 runtime 累积 |
| 消费者 | `ActivityCostMultiplier`（只调制追赶负担） |

Candidate 生成形状：

```text
A_norm = clamp(1 + Σ_i w_i · g_i(x_i), 0, 1)     # 常规带，Σ w_i ≤ 1，g_i ∈ [-1, 1]
A      = clamp(A_norm + rare_bonus, 0, 2)         # rare_bonus ∈ [0, 1]，仅由显式稀有 cause 产生

ActivityCostMultiplier(A) = clamp(1 / A, 0.5, 2)  # A=0 按 2 处理；单调递减
```

- 常规 cause 只能让 `A_norm` 落在 `[0,1]`；`A > 1` 必须由稀有 cause 的 `rare_bonus` 产生；
- `ActivityCostMultiplier` 与 Activity 方向相反：Activity 越高，追赶的行为代价倍率越低；probe 里的 0.8 / 1.6 是直接传入的倍率 fixture，不是 Activity 原值；
- `A = 0` 的倍率按上界 2 处理，不除零；
- `g_i` 的分段线性或单调曲线由各 cause 的机制数据给出；
- 没有 cause 数据时保持 `Unknown`，不回填 `1.0`。

候选 cause：时段、水温、溶氧、天气变化、近期摄食（全部未证实，见机制骨架 §2）。

验收：

1. 低 Activity 不降低 `InterceptSpeedLimit`；
2. `ClosingLoad ≈ 0` 时低 Activity 不凭空压低响应；
3. 输出 `2.0` 以上判越界，不截断；
4. 常规 cause 组合下 `A ≤ 1`；`A > 1` 的样本必须能追溯到稀有 cause；
5. `ActivityCostMultiplier` 随 `A` 单调递减；`A = 0` 时取 2，不除零。

标定需求：各鱼种的时段活动曲线、水温响应、溶氧阈值、极端活跃事件记录；验收按分布分位数与排序，不按拟合误差。

## 2. Feeding Motivation（摄食动机）

| 项 | 内容 |
|---|---|
| 语义 | 当前为了食物出手需要多强的理由；全局摄食驱动力 |
| 输出域 | `[0, 1]`；`0.5` 是参考锚，不是缺失 fallback |
| 更新路径 | Bake baseline；V1 不做 runtime 累积 |
| 消费者 | `WillingnessThreshold(M)` |

Candidate 生成形状：

```text
M = clamp(0.5 + Σ_j w_j · h_j(y_j), 0, 1)

h_j(y_j) ∈ [-1, 1]        各 cause 的归一化响应
Σ w_j ≤ 1
```

候选 cause：时段、近期摄食成功 / 失败、水温与季节、天气变化（全部未证实）。

验收：

1. `M = 0.5` 时门槛锚定 `Marginal = 0.40`；
2. `Unknown` 不回填 `0.5`；
3. `M` 不改变 FoodValue，也不复活 `Reject`；
4. 输出越界判越界，不截断。

标定需求：摄食节律数据、投喂/钓获事件序列、温度与季节响应；验收看不同动机档位下的门槛排序。

## 3. Diet Shift（食性偏移）

| 项 | 内容 |
|---|---|
| 语义 | 相对基础食性的动态偏移，按猎物家族分别给出 |
| 输出域 | 与 FoodValue 同标尺的有符号偏移；Candidate 工作范围 `[-0.2, 0.2]`，由 FoodValue 在 `[0,1]` 内 clamp |
| 更新路径 | Bake baseline；不由 Feeding Event 直接写入 |
| 消费者 | `DietaryShiftDelta(prey family)`，进入 FoodValue 求和 |

Candidate 生成形状：

```text
Δ_f = Σ_k w_{k,f} · d_{k,f}(z_k)      对每个 prey family f；不在偏移阶段截断
|Δ_f| > 0.2 → Unknown                  超出 Candidate 工作范围的 baseline 值不可消费
```

- 只能按 family 给出，不设全局分量；
- 缺失某个 family 的偏移时，只阻断该 family 的 FoodValue；
- 正负号必须能追溯 cause；
- FoodValue 阶段的 `clamp(..., 0, 1)` 是唯一截断点。

候选 cause：季节、近期摄食组成、猎物家族可得性（全部未证实）。

验收：

1. 同一 family 的偏移只影响该 family；
2. 不出现全局 DietShift；
3. clamp 在 FoodValue 阶段完成，偏移阶段不截断；
4. 越界偏移判越界。

标定需求：猎物可得性时间序列、食谱变化数据、按 family 的摄食记录。

## 4. Wariness（警戒度）

| 项 | 内容 |
|---|---|
| 语义 | 当前这类鱼对风险 / 异常线索有多敏感；不是“有多想吃” |
| 输出域 | `[0, 1]`（Candidate 域） |
| 更新路径 | Bake baseline + 可选 `Wariness Runtime Overlay`；V1 可只消费 baseline |
| 消费者 | `RiskCost = K_wary × Wariness × SuspicionLoad` |

Candidate 生成形状：

```text
baseline：W0 = Σ_m w_m · s_m(u_m)          # 原始和，不 clamp；越界 → Unknown
overlay ：W  = W0 + Σ_n δ_n · decay_n(t)    # 原始和，不 clamp；越界 → InvalidInput
```

- 权重与 cause：钓压 / fishing pressure、近期受惊、重复见到同类饵或线组（历史遭遇摘要）、环境突变；
- overlay 只做累加与衰减，不重新定义 baseline；
- 合并结果越过 `[0,1]` 时按 Production Contract 判 `InvalidInput`，不截断成 1；
- V1 允许完全不实现 overlay。

Overlay 必须先闭合的接口（仍 OPEN）：

```text
事件来源与识别
更新粒度与时间窗
增量形状与衰减
有效期
跨 encounter / session 的记忆边界
```

验收：

1. 无 `SuspicionLoad` 时，高 Wariness 不产生 `RiskCost`；
2. `SuspicionLoad` 只来自具名 cue；
3. `Wariness` 不改变 FoodValue 或 Motivation；
4. 过期 overlay 回落到 baseline；越权 overlay 标 `InvalidInput`；baseline 过期或越界转 `Unknown`。

标定需求：钓压代理、受惊事件记录、恢复时间、颜色 / 线组 conditioning 数据。

## 5. 与 Bake 的边界

- 四条生成契约属于各自机制线；Bake 只执行、物化、校验，不拥有语义；
- 生成结果必须带来源、有效期与状态，按 `ConditionGroup × EngagementMode`（DietShift 另加 family）落在 baseline block；
- 曲线与系数改动必须同时更新对应 probe 与回归矩阵。

## 6. 未闭口

- 四条曲线的实际形状与全部系数；
- cause 的数据来源、归一化与采样频率；
- TTL、刷新频率与跨 session 记忆；
- Wariness overlay 的事件与衰减；
- 各 Condition 的审核 owner（Issue #161 已定归属线，具体 Contract 未立项）；
- **验证范围**：四条生成曲线与 cause 权重目前没有执行验证。`fish-condition probe` 只覆盖 Activity/Motivation/Wariness 的解析、范围与 DietShift 逐 family 状态，不覆盖曲线形状、TTL 或 overlay 衰减。

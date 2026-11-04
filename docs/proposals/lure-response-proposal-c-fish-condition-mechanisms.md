# Proposal C｜鱼况（Fish Condition）机制契约草案

状态：Working Mechanism Draft / Candidate。按 2026-10-30 Owner 裁定（Issue #161）编写：本文只定义各 Condition 的语义、允许 cause、输出域、更新路径与验收，不定义生产曲线。

生成语义与曲线仍归各 Condition 的正式机制 Contract；本文是它们的骨架与缺口清单。

## 1. 共同约束

- 四个 Condition 都是鱼侧状态，不是四个奖励或惩罚；
- 同一上游事实可以进入多个 Condition，但每个 Condition 必须有独立的 cause → Condition 语义；同一效果不得在两处重复结算；
- 任何 Condition 的生成都不读取玩家当前操作或饵的当前呈现；历史遭遇记录只能作为独立摘要输入，且必须声明来源与时间范围；
- `Unknown` 不默认成 1.0、0.5 或 0；
- Bake 负责执行、物化与校验，不因此拥有语义裁定权。

## 2. Activity

| 项 | 内容 |
|---|---|
| 语义 | 当前愿意为主动追赶付出多少行为代价；不是物理速度能力 |
| 消费者 | `ActivityCostMultiplier`（只调制追赶负担） |
| 输出域 | 有限、非负；`1.0` 是 Working reference；不设语义上界 |
| 更新路径 | Bake baseline；V1 不做 runtime 累积 |
| 禁止 | 改 `InterceptSpeedLimit`；与 FeedingMotivation 共用“积极程度”；按玩家操作即时变化 |

候选 cause（全部未证实，需要数据）：

| cause | 为什么可能是原因 | 现有证据 |
|---|---|---|
| 时段 | 昼夜活动节律 | 仅术语“随时段变化” |
| 水温 | 代谢与活动范围 | 无仓内映射 |
| 溶氧 | 低氧抑制活动 | 无仓内映射 |
| 天气变化 | 气压 / 锋面影响 | 无仓内映射 |
| 近期摄食 | 饱食降低活动 | 无仓内映射 |

验收：

1. 低 Activity 不降低 `InterceptSpeedLimit`；
2. `ClosingLoad ≈ 0` 时，低 Activity 不凭空压低响应；
3. `Unknown` 不回填 1.0；
4. 非有限或负值被拒绝，不静默截断。

## 3. Feeding Motivation

| 项 | 内容 |
|---|---|
| 语义 | 当前为了食物出手需要多强的理由；全局摄食驱动力 |
| 消费者 | `WillingnessThreshold(M)` |
| 输出域 | `M ∈ [0,1]` 为 Candidate/Working 域；0.5 是参考锚，不是 fallback |
| 更新路径 | Bake baseline；V1 不做 runtime 累积 |
| 禁止 | 乘 FoodValue；替代 DietShift 表达“更想吃某种食物”；复活 `Reject` |

候选 cause（未证实）：

| cause | 可能的作用 | 现有证据 |
|---|---|---|
| 时段 | 摄食高峰 / 低谷 | 仅术语“随时段变化” |
| 近期摄食成功或失败 | 短期摄食驱动力 | 无仓内映射 |
| 水温 / 季节 | 代谢与摄食节律 | 无仓内映射 |
| 天气变化 | 摄食窗口 | 无仓内映射 |

验收：

1. `M=0.5` 时 threshold 锚定 `Marginal=0.40`；
2. `Unknown` 不回填 0.5；
3. `M` 不改变 FoodValue；
4. `M` 不改变 `Reject`。

## 4. Diet Shift

| 项 | 内容 |
|---|---|
| 语义 | 相对基础食性的动态偏移，按猎物家族分别给出 |
| 消费者 | `DietaryShiftDelta(prey family)`，进入 FoodValue 求和 |
| 输出域 | 与 FoodValue 同标尺的有符号偏移；允许正负 |
| 更新路径 | Bake baseline；不由 Feeding Event 直接写入 |
| 禁止 | 全局食欲分量；只给一个总数；替代 FeedingMotivation |

候选 cause（未证实）：

| cause | 可能的作用 | 现有证据 |
|---|---|---|
| 季节 | 猎物可得性变化 | 无仓内映射 |
| 近期摄食组成 | 偏好短期偏移 | 无仓内映射 |
| 猎物家族可得性 | 机会性摄食 | 无仓内映射 |

验收：

1. 同一 family 的偏移只影响该 family 的 FoodValue；
2. 不出现全局 DietShift；
3. `Unknown` 的 family 不闭合该 family 的 FoodValue，不影响其它 family；
4. clamp 在 FoodValue 的 `[0,1]` 内完成，不在偏移阶段截断。

## 5. Wariness

| 项 | 内容 |
|---|---|
| 语义 | 当前这类鱼对风险 / 异常线索有多敏感；不是“有多想吃” |
| 消费者 | `RiskCost = K_wary × Wariness × SuspicionLoad` |
| 输出域 | `[0,1]` 为 Candidate 域，未正式裁定 |
| 更新路径 | Bake baseline + 可选 `Wariness Runtime Overlay`；V1 可只消费 baseline |
| 禁止 | 与 `SuspicionLoad` 混为一个更新源；由 fishing pressure 二次进入 `SuspicionLoad`；由高速 / 转向 / `1 - support` 生成 |

候选 cause（未证实）：

| cause | 可能的作用 | 现有证据 |
|---|---|---|
| 钓压 / fishing pressure | 长期警戒基线 | 术语与设计包提到“作为上游原因” |
| 近期受惊事件 | 短期抬升 | 无仓内映射 |
| 重复见到同类饵 / 线组（历史遭遇记录，不读当前呈现） | conditioning | 无仓内映射 |
| 环境突变（光、声、船影） | 瞬时抬升 | 无仓内映射 |

若实现 runtime overlay，必须先闭合：

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
4. 过期 overlay 回落到 baseline；越权 overlay 标 `InvalidInput`；baseline 本身过期或越界转 `Unknown`。

## 6. Cause 准入表（全部未证实）

| cause | 允许驱动 | 当前状态 | 需要什么证据 |
|---|---|---|---|
| 时段 | Activity / Motivation | 仅术语提及 | 鱼种级活动与摄食节律数据 |
| 水温 | Activity / Motivation | 候选 | 温度响应曲线与钓获数据 |
| 溶氧 | Activity | 候选 | 低氧行为数据 |
| 季节 | DietShift | 候选 | 猎物可得性与食谱变化 |
| 近期摄食 | Motivation / DietShift | 候选 | 摄食事件与后续咬口数据 |
| 钓压 | Wariness | 语义支持 | 钓压代理与警戒行为数据 |
| 近期受惊 | Wariness | 候选 | 事件记录与恢复时间 |

未列出的 cause 不进入生成公式。同一事实进入两个 Condition 时，必须分别写清两边的语义，例如时段影响“活动水平”与“摄食驱动力”是两条不同判断，不能共用同一个映射曲线；同一效果不得在两处结算。

## 7. 未闭口

- 四个 Condition 的生产曲线与标定；
- cause 的实际数据来源与归一化；
- Wariness overlay 的事件与衰减；
- 各 Condition 的 TTL 与刷新；
- 各 Condition 的审核 owner；
- 温度 / 溶氧等环境条件是否由 DEF 直接提供。

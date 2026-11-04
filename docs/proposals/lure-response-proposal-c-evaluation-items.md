# Proposal C｜五评价项契约

状态：Working Design / Candidate。本文把出手余量的五项拆开写，定义每项的输入、合成方式与边界。不是 Current Contract，也不是生产参数。

来源：`docs/lure-response-joint-evaluation` 的 `food-value-production-topology`、`support-scale-contract`、`state-trigger-intensity-contract`、`attack-trigger-strategy-contract`、`activity-closing-cost-contract`、`activity-motivation-separation`、`wariness-response-path`、`suspicion-load-contract`、`poor-reject-separation`，按 `311ae70d` 快照核对；对齐稿部分按其当前内容核对。

## 1. 总式

```text
出手余量
= 食物价值
+ 攻击诱因
- 追赶负担
- 风险顾虑
- 摄食意愿门槛
```

五项都先换算到同一“出手余量标尺”，顶层只做竞争。非线性、状态交互和装备/操作交叉在下层完成，不堆到顶层。

## 2. 食物价值

### 合成

```text
CurrentFoodValue
= clamp(
    BaseDietAffinity(prey family)
    + SizePreferenceAdjustment(prey size)
    + DietaryShiftDelta(prey family),
    0, 1
  )
```

### 各项职责

| 项 | 回答 | 不表达 |
|---|---|---|
| BaseDietAffinity | 参考鱼况、参考尺寸下，这类猎物本来值多少 | 当前多想吃、警惕、像不像、好不好追 |
| SizePreferenceAdjustment | 可食范围内，尺寸相对偏好的软变化 | 尺寸不可食的硬边界 |
| DietaryShiftDelta | 上下文造成的食物之间相对偏转 | 全局食欲升降 |

`Preferred / Good / Marginal / Poor` 默认是连续 FoodValue 的解释标签，不是第二套独立 authoring 数值。

### 边界

- 不使用多个匿名 multiplier 连乘；
- `Reject` 是连续轴外的 typed hard boundary，不等于 `FoodValue=0`；
- 若未来有权威规则确认某尺寸在物理或摄食方式上不可接受，用独立 hard boundary，不塞进 SizePreferenceAdjustment；
- 全局食欲不进入 FoodValue，它属于摄食意愿。

## 3. 攻击诱因

### 合成

```text
StateTriggerValue_p
= TriggerBudget × TriggerIntensity_p
```

- `TriggerIntensity_p ∈ [0,1]` 由 prey-conditioned state interpreter 给出；
- `TriggerBudget ≈ 0.10 ~ 0.15`，是 Working effect-size budget；
- Response 不再对 raw trajectory 做第二套 Trigger 解释。

### TriggerIntensity 不是什么

不是 raw turn magnitude、burst speed 或 event count。理由：一次 escape dart 往往同时包含转向和加速，按特征相加会重复奖励同一个行为；不同猎物对同一 raw feature 的含义不同；事件数不应无界累加。

### 准入边界

只表达“目标已被解释为可接受猎物后，当前猎物状态是否额外促发出手”。

第一版准入结果（见[第一轮玩法闭合审查](lure-response-proposal-c-first-round-closure.md)）：

| 状态 | 结果 |
|---|---|
| Escape-like / 逃逸样 | 准入；用转向强度与 burst 强度，经 prey-conditioned 判定 |
| Injured / Struggling / 受伤挣扎样 | `CandidateUnresolved`；缺生产闭合的识别映射，等 cue-only holdout，不用航迹不规则冒充 |
| Vulnerable Pause / 虚弱停顿样 | pause 本身不得作为 Trigger；imbalance-like vulnerability 保持 `CandidateUnresolved` |

不承载领地、防御、烦躁、护巢、调查。

### 不允许免费诱因

诱因上升时，不额外发明统一的“刺激惩罚”。代价应优先由已有机制产生：可能更高的追赶负担、更明显的机械暴露带来的风险顾虑；若该呈现同时造成更短的局部机会窗口，那部分代价由 Opportunity 侧承接，不是诱因本身的普遍因果。

## 4. 追赶负担

### 合成

```text
q = 拟饵相对水体水平速度 / InterceptSpeedLimit（单方向：在“鱼在追拟饵”假设下按径向需求计）

追赶负担
= K_close *
  q^2 *
  ActivityCostMultiplier(Activity)
```

第一版不模拟鱼与拟饵的相对方位，统一按“鱼在追拟饵”估算；`q` 就是径向速度需求比。`K_close` 的 Working 值按这个单方向标尺取 `0.19`（原 `0.76` 是带方位平均时的值）。

### 职责分离

| 来源 | 回答 |
|---|---|
| 鱼种 / 体型 → InterceptSpeedLimit | 这条鱼能追多快 |
| Activity → ActivityCostMultiplier | 这条鱼当前愿意为追赶付出多少代价 |

Activity 不修改 `InterceptSpeedLimit`。低 Activity 不能表现为“鱼突然失去运动能力”。

`CapacityModifier` 已由 2026-10-30 Owner 裁定从 active design 删除，重开条件见[开放决策](lure-response-proposal-c-open-decisions.md)。

### 边界

- Closing 只解释径向分离负担，不是完整拦截模拟；
- `q >= 1 → hard-zero` 已撤回；
- 垂直主导呈现不进入 Closing，归 Opportunity 的垂直可交互窗口（Spatial 只提供空间事实）；
- 高速的完整系统效果由追赶负担与机会量共同形成，Closing 不单独承担全部高速惩罚。

## 5. 风险顾虑

### 合成

```text
RiskCost = K_wary × Wariness × SuspicionLoad
```

- `Wariness`：当前这类鱼对风险线索有多敏感；
- `SuspicionLoad`：本次呈现里有多少已解析的可疑证据。

### 首版 cue

| cue | 表达 | 状态 |
|---|---|---|
| TackleConspicuousness | 终端连接、线、钩等已声明事实对当前目标的可见或侵入程度 | 正式保留的后续语义方向；当前未立生产字段或 owner，V1 `RiskCost=0` |
| EntryDisturbance | 本次呈现进入局部区域时的已解析异常扰动 | 暂不实现 |

`TackleConspicuousness` 当前仍缺生产字段；实现前：

```text
无已解析 cue → SuspicionLoad = 0 → RiskCost = 0
```

不补造代理；`SKU → conspicuousness` 不允许。冻结验证基线里的 `cue.contact_disturbance`、`sound_amplitude` 瞬态与「线透明度 / 线颜色」派生条件只能作为语义参考，不是生产输入。实现前必须明确：Wariness 暂时没有真实玩家策略消费方。

### 不准入

- `1 - prey_support`：支持不足不等于可疑；
- 高速度、高频转向：已由追赶负担与预测路径消费；
- fishing pressure：它提高 `Wariness`；再塞进 `SuspicionLoad` 会形成平方放大；
- repeated exposure：属于 conditioning / memory，owner 未闭合前不进入。

## 6. 摄食意愿门槛

### 合成

```text
M <= 0.80:
    threshold = 0.60 - 0.40 * M

M > 0.80:
    threshold = 0.60 - 0.40 * M - 0.50 * (M - 0.80)
```

### 性质

- Motivation 不乘 FoodValue，也不放大其它负担；
- `M=0.5` 时 threshold 锚定 `Marginal=0.40`；
- 普通区间保持基准斜率，只有极高 Motivation 进入 tail relief；
- 高 Motivation 不复活 `Reject`；
- `M=0` 不表示绝不摄食，`M=1` 不表示必定攻击。

### 边界

低 Motivation 可以让鱼更挑剔，但不应通过过大的斜率抹掉 Preferred 与其它档位的结构差异。tail 起点与额外斜率仍是 Working，可由真实 Motivation 分布重新标定。

## 7. 合成与可补偿性

- 五项在同一标尺上可补偿：足够高的食物价值可以抵消一部分追赶负担；更强诱因可以帮助边缘目标跨线；更低 Motivation 抬高门槛；
- 可补偿不等于无限补偿；成本可以很大，但不能用超大 cost 冒充 hard boundary；
- `Reject`、`Unknown`、`NotConfigured`、`ResolutionIncomplete` 在进入合成前按状态协议处理；
- 顶层不再加交叉项。

## 8. 与 Fish Condition 的关系

当前鱼况使用 Activity、Feeding Motivation、Diet Shift、Wariness。五项评价与它们不是一一对应：

```text
Fish Condition（鱼侧动态参数）
→ 评价项（本次呈现下的判断）
→ 出手余量
```

- 本轮不重定 Fish Condition 名单；现行 Activity、Feeding Motivation、Diet Shift、Wariness 继续作为上游语义；
- 它们各自如何生成、是否存在可派生量、是否有重复职责，留待专门的 Bake / Owner 讨论；
- `BaseDietAffinity`、`InterceptSpeedLimit`、prey support、TriggerIntensity 都是派生中间量或解释结果，不自动成为 Fish Condition；
- 一个来源只在一个 owner 结算，跨层读取允许，重复加成不允许。

## 9. 未决项

- Prediction：第一版不含，`Deferred Research`；重开条件见[开放决策](lure-response-proposal-c-open-decisions.md)；
- 风险顾虑的最低实现层与完整 Naturalness 边界；`TackleConspicuousness` 尚无生产字段；
- `CapacityModifier` 已从 active design 删除，重开条件见开放决策；
- 垂直主导呈现的机会窗口形态（`L` 归 Opportunity）；
- 各系数的生产标定。

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

五项都先换算到同一“出手余量标尺”，顶层只做竞争。非线性、状态交互和装备/操作交叉在下层完成，不堆到顶层。反应呈现另有一项条件扣减（`ReactionCost`），见 §3；它不是第六个评价项。

## 2. 食物价值

### 合成

```text
CurrentFoodValue_f
= clamp(
    ShiftedDietAffinity_f
    + SizePreferenceAdjustment(prey size),
    0, 1
  )

u_f   = T(BaseDietAffinity_f)          # 公共档位坐标
u'_f  = clamp(u_f + DietTierShift_f, 0, 3)
ShiftedDietAffinity_f = U(u'_f)         # 回到 FoodValue 标尺
```

公共档位标尺与锚（Candidate，版本化）：

```text
档位坐标 0 / 1 / 2 / 3  ↔  Poor / Marginal / Good / Preferred
锚 a = (a0, a1, a2, a3) = (0, 0.25, 0.60, 1.0)   # Owner 2026-11-05；tierScaleVersion = tier-v2
同一标尺版本内所有 family 共用这一组锚，不按 family 另配档距。

T(x)：x 先 clamp 到 [0,1]；对 a_i ≤ x ≤ a_(i+1)，
      T(x) = i + (x − a_i) / (a_(i+1) − a_i)

U(u)：u 先 clamp 到 [0,3]；对 i ≤ u ≤ i+1，
      U(u) = a_i + (a_(i+1) − a_i) × (u − i)

U = T⁻¹；锚间为分片线性插值，单调连续。
```

`DietTierShift_f`（简称 `s_f`）是 DietShift 的输出，单位是“档”，有符号连续值：

- `0` 是已解析的无偏移，不是缺失 fallback；
- `+1` 从当前锚升到下一个锚，顶端除外；`-1` 同理向下；
- 第一版工作域 `[-1, +1]`（一档以内，允许小数档），Owner 2026-11-05 确认；
- **基础 0 可被抬起**：`BaseDietAffinity = 0` 表示“目前基本不把它当食物”，不是 `Reject`（`Reject` 是独立的硬边界）。`s = +1` 可以把它抬到 `Marginal = 0.25`；否则饮食偏移永远无法引入一种新猎物。
- **顶档不抵消尺寸劣势**：基础 `1.0` 加 `+1` 仍是 `1.0`，多出来的档不存着；随后 `SizePreferenceAdjustment = −0.2` 得到 `0.80`。顺序本身不够，靠的是 `U` 输出后的中间值已经饱和，被丢弃的余额不能回头抵消尺寸扣分。

### 各项职责

| 项 | 回答 | 不表达 |
|---|---|---|
| BaseDietAffinity | 参考鱼况、参考尺寸下，这类猎物本来值多少 | 当前多想吃、警惕、像不像、好不好追 |
| SizePreferenceAdjustment | 可食范围内，尺寸相对偏好的软变化 | 尺寸不可食的硬边界 |
| DietTierShift | 上下文造成的、按档计的食物相对偏转 | 全局食欲升降；跨超过一档的重排 |

`Preferred / Good / Marginal / Poor` 由同一公共标尺解释，档位标签从数值派生，不按 family 独立存储第二份档位值，也不另行抽样。旧的 `DietaryShiftDelta` 不再作为 authoring 输入；如需接口兼容，只能派生为 `ShiftedDietAffinity − BaseDietAffinity`，其范围依赖基础值与档距，不做旧的 ±0.2 校验。

### 边界

- 不使用多个匿名 multiplier 连乘；
- 档位坐标的两端饱和是合法饱和，与“非法输入被截断”不同；消费端收到声称已解析但非法的 `s` 必须按 `InvalidInput` 处理，不能先截到合法域再消费；
- `Reject` 是连续轴外的 typed hard boundary，不等于 `FoodValue=0`；
- 若未来有权威规则确认某尺寸在物理或摄食方式上不可接受，用独立 hard boundary，不塞进 SizePreferenceAdjustment；
- 全局食欲不进入 FoodValue，它属于摄食意愿。

## 3. 攻击诱因

### 两个 owner

攻击诱因跨两层，两个量各有唯一 owner：

```text
猎物侧（Prey Interpreter，跨捕食鱼种共享）
    StateMatchStrength_p ∈ [0,1]
    # 描述性：当前运动在多大程度上构成这种猎物状态
    # 输入只有实际事实、事件、该猎物的状态规则；不读捕食鱼的食性、追赶能力或意愿

鱼侧（Response，按捕食鱼 f × EngagementMode）
    TriggerEvaluation_f(p, PreyState_p) ∈ [0,1]
    StateTriggerValue_fp = TriggerBudget × TriggerEvaluation_f(p, PreyState_p)
```

- `StateMatchStrength_p` 由状态解释器给出，只回答“像不像”，不回答“这条鱼多想攻击”；
- `TriggerEvaluation_f` 由 Response 在评价阶段计算，回答“这条鱼面对这个已解释状态，额外产生多少攻击诱因”；
- `TriggerBudget ≈ 0.10 ~ 0.15`，仍是 Working effect-size budget，不因分层而改变；
- 同一呈现、同一猎物类型，换捕食鱼时 `StateMatchStrength_p` 不变；只有鱼侧评价可以不同。

### 第一版默认评价

```text
TriggerEvaluation_f(p, PreyState_p) = StateMatchStrength_p
```

- 第一版使用共享默认规则，不预设按鱼种或习性的动作偏好表，不捏造物种参数；
- 默认规则下数值与分层前一致，排序不发生漂移；
- 未来某鱼种或模式有实证差异时，可以替换 `TriggerEvaluation_f`；未配置的鱼种回落到默认规则，不判 `NotConfigured`，也不让默认逃逸规则失效；
- 配置了鱼种专属评价但输出非有限或越界时，按 `InvalidInput` 处理，不静默截断。

### StateMatchStrength 不是什么

不是 raw turn magnitude、burst speed 或 event count。理由：一次 escape dart 往往同时包含转向和加速，按特征相加会重复奖励同一个行为；不同猎物对同一 raw feature 的含义不同；事件数不应无界累加。

鱼侧评价也不得把这些 raw 特征重新相加。事件已经在猎物侧被解释成事件，鱼侧只读已解释状态。

### 反应呈现的表达成本（Candidate，Owner 2026-11-06）

反应呈现可以跨过自然呈现跨不过的线，但不能免费弥补较差的猎物表达。仅对 reaction presentation：

```text
ReactionCost = λ × (1 − PreySupport)
自然 presentation：ReactionCost = 0

DecisionMargin = 食物价值 + StateTriggerValue − ReactionCost
                 − 追赶负担 − 风险顾虑 − 摄食意愿门槛
C_feed = PreySupport × C        # support 仍只在末端乘一次
```

- 这是 Response 在五项 margin 内的条件扣减，不是第六个顶层评价项，也不归 Trigger；Trigger 只负责正向 `StateTriggerValue`；
- λ 的 Working probe 值为 `0.20`；这是实验夹具，不是生产标定值；
- 不允许用 `TriggerEvaluation × support` 代替；那会与末端 support 乘法重复计权；
- 非反应呈现或未配置时成本为 0，不改变现有排序；
- λ 为负或非有限 → `InvalidInput`；
- 未来按 species / EngagementMode 分化的 λ 需要独立证据，不由实现自行分叉。

证伪条件：在预注册的 support × Motivation × q × trigger 网格上，若低 Motivation 且 reaction support 明显低于 natural 时 reaction 仍系统性胜出，或 `λ=0.20` 连“natural margin 略低于 0”的边缘案例也无法救活，则该规则失败。

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
- `M=0.5` 时 threshold = `0.40`。门槛是独立的 Working 参数，不由档位标签推出；档位锚从 `0.40` 改为 `0.25` 不移动它；
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

### 7.1 标尺、边界与可加性（Candidate）

| 项 | 工作域 | 备注 |
|---|---|---|
| 食物价值 | `[0, 1]` | 已 clamp |
| 攻击诱因 | `[0, 0.15]` | `TriggerBudget × TriggerEvaluation`，预算为 Working 上限 |
| 反应表达成本 | `[0, 0.20]` | 仅 reaction 分支；`λ=0.20`、`PreySupport∈[0,1]` 时的 Working 上界，不是生产值 |
| 追赶负担 | `[0, 1.52]` | `K_close=0.19`、`q∈[0,2]`、`Activity∈[0,2]` 时的上界；不设硬 cap |
| 风险顾虑 | `[0, 1]` | `K_wary=1` 的 Working 尺度；字段未落地时恒为 0 |
| 摄食意愿门槛 | `[0.1, 0.6]` | `Motivation∈[0,1]` 与 tail 参数下的 Working 范围 |
| 出手余量（理论域） | `[-3.12, 1.05]`；reaction 分支 `[-3.32, 1.05]` | 五项端点的组合；reaction 分支叠加 `ReactionCost` 后下界再降 `0.20`。当前 `RiskCost=0` 时分别为 `[-2.12, 1.05]` / `[-2.32, 1.05]`；具体 fixture 的观测范围更窄 |

可加性是 **Working 假设**，不是已验证事实：

- 每项先由自己的机制换算到同一标尺，再由标定把不同机制放到可比的量级；
- 目前没有真实数据证明五项等距可加；投影的截断会掩盖加法误差，标定时要看排序与分档，不只看拟合；
- 任何新增项、交叉项或非线性都必须先证明它不与现有五项重复计权；
- Activity 的 `[0,2]` 域只影响追赶负担；`Activity>1` 的稀有极活跃情形不改变其它项。

## 8. 与 Fish Condition 的关系

当前鱼况使用 Activity、Feeding Motivation、Diet Shift、Wariness。五项评价与它们不是一一对应：

```text
Fish Condition（鱼侧动态参数）
→ 评价项（本次呈现下的判断）
→ 出手余量
```

- 本轮不重定 Fish Condition 名单；现行 Activity、Feeding Motivation、Diet Shift、Wariness 继续作为上游语义；
- 它们各自如何生成、是否存在可派生量、是否有重复职责，留待专门的 Bake / Owner 讨论；
- `BaseDietAffinity`、`InterceptSpeedLimit`、prey support、`StateMatchStrength`、`TriggerEvaluation` 都是派生中间量或解释结果，不自动成为 Fish Condition；
- 一个来源只在一个 owner 结算，跨层读取允许，重复加成不允许。

## 9. 未决项

- Prediction：第一版不含，`Deferred Research`；重开条件见[开放决策](lure-response-proposal-c-open-decisions.md)；
- 风险顾虑的最低实现层与完整 Naturalness 边界；`TackleConspicuousness` 尚无生产字段；
- `CapacityModifier` 已从 active design 删除，重开条件见开放决策；
- 垂直主导呈现的机会窗口形态（`L` 归 Opportunity）；
- 各系数的生产标定。

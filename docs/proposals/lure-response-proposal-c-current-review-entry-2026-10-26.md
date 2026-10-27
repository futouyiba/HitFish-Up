# 方案 C｜当前审阅入口（2026-10-26）

状态：方案 C 的统一审阅入口。本文不是当前契约，也不是生产参数批准。

本文只登记三类内容：

- **结构边界**：本轮已收口、审阅时不应无依据推翻的职责与负向护栏；
- **工作标定种子**：用于探针、案例和回归审阅的暂定值，不是生产参数；
- **生产缺口**：仍缺正式归属方、数据来源或标定结果的内容。

若本文与更高层级的权威定义冲突，以 [`docs/authority-model.md`](../authority-model.md) 和已合并的当前归属方裁定为准。本文所在分支及提交版本由 Git 历史提供，不在正文维护分支状态。

## 1. 主链与输出边界

方案 C 的审阅主链是：

```text
实际呈现（ActualPresentation）
→ 猎物解释 / 支持度（prey interpretation / support）
→ 猎物条件下的当前状态（prey-conditioned current state）
→ 鱼侧评价（fish-side evaluation）
→ 潜在方位下的条件响应（latent-bearing conditional response）
→ 猎物模式响应（prey-mode response）
→ 摄食组合（Feeding composition）
→ 交互组合（Interaction composition）
→ 时间机会（temporal opportunity）
→ 候选原生留存值（Candidate native retention）
→ 最终抽取（TrueRoll）
```

`ActualPresentation` 提供真实呈现事实，包括形态、轨迹、速度、停顿、转向、近底或水面状态。玩家输入指令不能直接冒充实际呈现。

同一呈现可以支持多个猎物解释，例如饵鱼、小龙虾和蛙类。这里的支持度：

- 不要求和为 1；
- 不等于 `FoodValue`、`Suspicion` 或咬口概率；
- 同级猎物解释属于替代解释，不重复当作独立机会叠加。

猎物条件状态可以描述移动、低位移、上升或下落、水面或近底、移动后停顿、突然改向、爆发移动和逃逸或受惊表现。`Unknown`、`NotConfigured`、`NoMatch` 与数值 0 必须分开；缺失数据不能静默按 0 处理。

瞬时 `C` 不是每秒咬口概率、最终候选概率或累计中鱼率。时间维度由时间机会层处理，不进入 `DecisionMargin`。

## 2. 结构边界

### 食物价值与摄食动机

食物价值的结构是：

```text
BaseDietAffinity(prey family)
+ SizePreferenceAdjustment(prey size)
+ DietaryShiftDelta(prey family)
→ RawFoodValue
→ clamp(0, 1)
→ CurrentFoodValue
```

已收口的边界：

- 完整 `CurrentFoodValue` 的合法连续域是 `[0,1]`；
- `Poor=0` 仍是合法的连续摄食目标；
- `Reject` 是连续轴外的带类型硬语义边界，不能被摄食动机、状态触发或食性偏移复活；
- `SizePreferenceAdjustment <= 0`；
- 合法贡献先求和，再统一截断一次；
- `DietaryShift`（食性偏移）是相对于猎物家族的偏移，不是全局食欲加成。

摄食动机不再乘食物价值，而是改变行动门槛。它表示鱼的全局进食意愿，不是特定猎物价值或咬口概率。

### 状态触发、预测负担与警戒

猎物解释下的当前状态可以提供额外的正向攻击证据：

```text
sudden redirection
burst / escape-like state
→ StateTriggerValue
```

同一个突然改向可以沿两条职责不同的路径被使用：

```text
sudden turn
├→ prey-state evidence → StateTriggerValue (+)
└→ prediction disruption → PredictionCost (-)
```

这不允许再添加通用的异常移动加成或惩罚。状态触发（StateTrigger）不改猎物身份，不改摄食动机，也不能复活 `Reject`。

警戒度不作为第二套摄食动机或全局门槛：

```text
Wariness × SuspicionLoad
→ RiskCost
```

`SuspicionLoad`（怀疑负荷）只能消费有独立权威来源的命名线索。不得把它写成 `1 - prey_support`，也不得仅因高速、频繁转向或低支持度自动判定“不自然”。垂钓压力优先作为警戒度的上游原因，不能默认同时抬高怀疑负荷。

### 闭合负担与活跃度

第一版只处理水平潜在方位，并把闭合负担收窄为：

> 拟饵相对潜在鱼的径向远离速度，占鱼短时截获能力的比例。

它不是完整的二维拦截模拟。`cosθ > 0` 才产生径向闭合负担；纯横切和目标向潜在鱼接近的方向当前不增加追赶负担。没有合法归属方的鱼饵距离、交会点和反应延迟，不能补匿名的切向惩罚。

```text
鱼种 / 体型队列
→ 截获速度上限
→ 闭合负担的硬可行性

活跃度
→ 主动追击负担乘数
→ 闭合负担的软成本
```

活跃度不降低 `InterceptSpeedLimit`（截获速度上限）。同一低活跃度不能同时降低硬能力边界并抬高软闭合成本。硬零值只表示当前潜在方位下的径向远离速度达到或超过短时截获能力，不宣称严格二维物理意义上的绝对不可能。

### 决策裕量、响应投影与候选接入

不同原始特征必须只在其所属归属方中结算，不能因为某个特征看起来重要就放进多个系数。

```text
DecisionMargin(θ)
= CurrentFoodValue
+ StateTriggerValue
- ClosingCost(θ)
- PredictionCost
- RiskCost
- WillingnessThreshold(FeedingMotivation)
```

响应投影必须在潜在方位内完成：

```text
θ
→ local feasibility / costs
→ Margin(θ)
→ C(θ)
→ integrate over θ
```

不能先平均决策裕量再做投影。当前结构选择是截断线性投影，但 `M0 / M1` 仍是标定锚点，不能在入口页冻结为生产分母。完整边界与验收状态见 [`lure-response-proposal-c-response-projection.md`](lure-response-proposal-c-response-projection.md)。

同一摄食路径中的同级猎物候选可以使用替代聚合，例如：

```text
C_prey = prey_support * Eθ[C_conditional(θ)]
C_feed = max(C_baitfish, C_crayfish, ...)
```

这不授权所有交互模式都使用统一取最大值。

响应只产生原生贡献：

```text
q_i,j = L_i,j * C_i,j
→ Opportunity Reduce
→ W_i^opp
→ NativeCandidateSnapshot
→ optional Pre-Roll Gameplay Policy
→ TrueRoll
```

候选生成的后段不得再乘一次响应值。输出状态（status）必须区分：

```text
ResolutionIncomplete
ResolvedNonResponsive  C=0
ResolvedResponsive     0<C<=1
Reject                  hard semantic zero
```

`Unknown` 不等于 0。

### 时间机会

时间接口保持在摄食响应之外：

```text
instantaneous response C(t)
× temporal / local opportunity exposure
→ accumulated opportunity
→ Candidate retention
```

不得加入 `DwellBonus` 或 `PauseBonus`，也不得把停留时长放进 `DecisionMargin`。从时间机会或暴露程度到候选归约器的正式当前归属方仍未在仓内收口，方案 C 只定义接口边界。

## 3. 工作标定种子

以下数值只用于探针、案例和回归审阅，不是现实鱼类参数，也不是生产批准：

- `FoodValue`（食物价值）的关系锚点：`Preferred=1.00`、`Good=0.70`、`Marginal=0.40`、`Poor=0.00`；`Reject` 不在连续轴内；
- `FeedingMotivation`（摄食动机）的 `M_ref=0.5`、`T_ref=0.40`、`K_mot=0.40`；
- 普通 `StateTrigger`（状态触发）约 `0.10`，上限护栏约 `0.15`；
- 运动能力的配置档案：`HighClosing`、`GeneralClosing`、`LowClosing`；
- 参考 `q` 种子值：`0.45`、`0.65`、`0.90`；
- 软负担的轻度、普通和重度压力篮子仅用于联合标定检查；
- `K_close`、`K_pred`、`τ_recover`、`K_wary`、`M0 / M1` 和最终状态触发预算均未成为生产值。

当前运行时只有单一的 `InterceptSpeedLimit`，没有持续爆发时长、追击时间窗或转向能力等独立维度。因此第一版不把 `BurstAmbushPredator`、`ManeuverOriented` 和 `SustainedCruiser` 注册为正式运动能力档案。

- 工作标定种子的详细来源与计算分别见：

- [`lure-response-proposal-c-joint-margin-calibration-seed.md`](lure-response-proposal-c-joint-margin-calibration-seed.md)：联合决策裕量标定种子；
- [`lure-response-proposal-c-reference-intercept-speed-working-anchors.md`](lure-response-proposal-c-reference-intercept-speed-working-anchors.md)：参考截获速度的工作锚点；
- [`lure-response-proposal-c-combined-burden-stress-test.md`](lure-response-proposal-c-combined-burden-stress-test.md)：联合软负担压力测试；
- [`lure-response-proposal-c-response-projection.md`](lure-response-proposal-c-response-projection.md)：响应投影。

## 4. 生产缺口

### 归属方与结构缺口

- 从时间机会或暴露程度到候选归约器的正式当前归属方；
- 摄食、防御、调查三类交互的组合规则；
- 未来若启用 `ExplicitDirectional`（显式方向）方位先验，生产方向支持的归属方；
- `SuspicionLoad`（怀疑负荷）的生产线索归属方。

### 生产来源

- 约 200 个鱼种的基础食性亲和度和食性档案覆盖；
- 体型偏好曲线；
- 食性偏移的生产预算与中心化方式；
- `InterceptSpeedLimit`（截获速度上限）的真实绝对米每秒来源；
- 体型缩放档案与指数；
- 路亚家族 × 运动状态的水平相对水速遥测数据；
- 警戒线索的标准化输入。

### 标定

- `K_close`、`K_pred`、`τ_recover`、`K_wary`；
- 最终的良好 / 临界关系锚点；
- 响应投影的 `M0 / M1`；
- 状态触发的最终预算；
- 猎物支持度 × 响应值的整链分布；
- 饱和率与零响应率护栏。

这些缺口不能在入口页中被默认为生产规则，也不能用新增运行时总上限隐藏标定问题。

## 5. 审阅边界

审阅应优先检查：

1. 各变量是否职责重叠或漏项；
2. 同一原始特征是否被重复结算；
3. 径向闭合近似在哪些操作下会造成错误排序；
4. `Isotropic2D`（各向同性二维）在没有具体鱼点时是否仍是可接受的第一版建模约定；
5. 工作标定锚点是否使正常的良好目标长期饱和或长期归零；
6. 猎物支持度、响应值、时间机会与候选值是否产生系统性过度衰减；
7. 哪些缺口阻塞生产，哪些只是后续标定。

替代方案必须指出：它替换哪个归属方，消除了什么重复计权，以及对现有回归样例的影响。审阅不得把历史已关闭问题重新写成当前开放项，不得修改活跃度文档，也不得把缺少归属方的内容补成生产规则。

## 6. 深挖入口

- [`lure-feeding-response-proposal-c.md`](lure-feeding-response-proposal-c.md)：真实呈现 → 猎物解释 / 猎物条件状态；
- [`lure-response-proposal-c-feature-ownership-matrix.md`](lure-response-proposal-c-feature-ownership-matrix.md)：原始特征归属；
- [`lure-response-proposal-c-current-food-value-bounds.md`](lure-response-proposal-c-current-food-value-bounds.md)：食物价值合法域；
- [`lure-response-proposal-c-feeding-motivation-threshold.md`](lure-response-proposal-c-feeding-motivation-threshold.md)：摄食动机 → 行动门槛；
- [`lure-response-proposal-c-latent-bearing-prior.md`](lure-response-proposal-c-latent-bearing-prior.md)：潜在方位约定；
- [`lure-response-proposal-c-latent-bearing-dimensionality-decision.md`](lure-response-proposal-c-latent-bearing-dimensionality-decision.md)：二维决策；
- [`lure-response-proposal-c-closing-geometry-interpretation.md`](lure-response-proposal-c-closing-geometry-interpretation.md)：闭合几何语义；
- [`lure-response-proposal-c-intercept-speed-production-contract.md`](lure-response-proposal-c-intercept-speed-production-contract.md)：截获速度上限的生产拓扑；
- [`lure-response-proposal-c-locomotor-archetype-catalog.md`](lure-response-proposal-c-locomotor-archetype-catalog.md)：运动能力档案；
- [`lure-response-proposal-c-temporal-exposure-opportunity.md`](lure-response-proposal-c-temporal-exposure-opportunity.md)：时间机会接口；
- [`lure-response-proposal-c-adversarial-review-2026-10-26.md`](lure-response-proposal-c-adversarial-review-2026-10-26.md)：历史整链攻击报告，仅作证据。

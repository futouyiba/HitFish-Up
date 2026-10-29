# Proposal C｜响应与机会契约

状态：Working Design / Candidate。本文写清第 5 到第 7 层：已解析的出手余量如何变成条件响应、同级猎物如何组成 feeding 结果、机会量如何接入候选。不是 Current Contract，也不是生产参数。

来源：`docs/lure-response-joint-evaluation` 的 `margin-response-projection`、`sibling-partial-resolution`、`opportunity-integration-closure`、`response-aggregation-topology-review`（按 `311ae70d` 快照核对；该分支持续更新）。

## 1. 范围

```text
已解析 DecisionMargin
→ 条件响应 C(theta)
→ sibling 组成 C_feed
→ 机会接入 q = L × C
→ Opportunity Reduce
→ NativeCandidateSnapshot
→ TrueRoll
```

本文不重新定义 Spatial、Opportunity 或 Candidate 的内部实现，只定义它们与 Response 之间的 seam。

## 2. 条件响应

### 投影

```text
C(theta) = clamp((Margin(theta) - M0) / (M1 - M0), 0, 1)

Working: M0 = 0.00, M1 = 0.40
```

`M0` 是非响应阈值，`M1` 是满响应锚。两者是 Working calibration anchor，不是物理常数。

### 计算顺序

```text
theta
→ local costs
→ Margin(theta)
→ C(theta)
→ E_theta[C]
```

- 必须在每个 latent bearing 内先算成本与 Margin，再投影，最后聚合；
- 不能先平均 Margin 再投影；
- 不能先平均 Margin 再加时间项。

### 状态

```text
ResolutionIncomplete / Unknown → 不调用投影，不输出 C
ResolvedNonResponsive          → C = 0
ResolvedResponsive             → 0 < C <= 1
Reject                         → typed zero，不进入连续计算
```

`C=0` 只表示输入完整且未越过响应阈值，不等于缺失，也不等于 `Reject`。

## 3. Sibling 组成

### 先声明集合

`max` 只作用于上游已声明属于同一 physical target、同一 Feeding route 的 sibling set，例如 `{baitfish, crayfish, frog}`。

```text
未进入该集合的猎物 → NotParticipating，不参与 max，也不构成 Unknown
进入集合但缺配置或输入 → NotConfigured / ResolutionIncomplete，不能从集合里偷偷删除
```

### 每条 sibling 映射到区间

| 状态 | 区间 |
|---|---|
| `ResolvedResponsive`，`C=c` | `[c, c]` |
| `ResolvedNonResponsive` | `[0, 0]` |
| `Reject` | `[0, 0]`，它是硬零，不是 Unknown |
| `NoMatch`，规则明确给出数值零 | `[0, 0]` |
| `NoMatch`，规则只给“条件不成立”等非数值结论 | 保持 `ResolutionIncomplete`，携带当前可证明边界（默认 `[0, 1]`） |
| `Unknown`，无更窄信息 | `[0, 1]` |
| `Unknown`，已有部分信息 | 更窄的 `[L_i, U_i]` |
| `NotConfigured`（已进入 sibling set） | `ResolutionIncomplete`，携带当前可证明边界（默认 `[0, 1]`），不丢上界 |

已有部分信息时必须用更窄区间，不退回 `[0, 1]`。进入集合后缺配置，状态保持 `ResolutionIncomplete`，但仍保留上界，用来判断已知 sibling 是否已经赢。

### 聚合

```text
L_feed = max_i(L_i)
U_feed = max_i(U_i)

L_feed == U_feed → C_feed = L_feed，可进入机会接入；仍需已解析的 L 才能形成 q
否则 → ResolutionIncomplete，携带 response_bounds，不可进入 roll
```

例子：

```text
baitfish = [0.80, 0.80]
crayfish = [0.20, 0.60]
L_feed = 0.80, U_feed = 0.80 → C_feed = 0.80

baitfish = [0.45, 0.45]
crayfish = [0.10, 0.90]
L_feed = 0.45, U_feed = 0.90 → ResolutionIncomplete

baitfish = [0.40, 0.40]
crayfish = NotConfigured → [0, 1]
L_feed = 0.40, U_feed = 1.00 → ResolutionIncomplete
```

### 边界

- sibling 取 `max` 不授权所有 Interaction mode 使用 universal max；
- 区间是缺失输入导致的可能范围，不是置信区间或概率；
- `C_feed` 未收敛时，不得用已知下界冒充最终值。

## 4. 机会接入

### 颗粒与身份

```text
姿态颗粒 / semantic presentation grain j
├→ Response：C_i,j
└→ Opportunity / Spatial：L_i,j

q_i,j = L_i,j × C_i,j
```

- 姿态颗粒必须有稳定语义身份或稳定 semantic partition；
- 一个 runtime tick 或一次重复调用不是新机会；
- 同一语义颗粒、同一 opportunity identity 的重算属于 replay，不增加机会计数；
- 具体 identity、dedupe 与 reevaluation 由 Opportunity owner 决定。

### 时间与停留

更长的停留不修改 FoodValue、Trigger、Closing、Risk 或门槛，只提高机会量：

```text
C = 0.6
L_long > L_short
q_long = L_long × 0.6 > q_short
```

`L(duration)` 的生产函数不在本文冻结。

### 状态

- `L` 未配置或无法解析 → `ResolutionIncomplete`，不是零机会；
- 已解析的 `L=0` 才表示该窗口没有机会；
- `q` 只在 `C` 与 `L` 都已解析且 `C_feed` 收敛时产生。

### 禁止

- Response 内不新增连续 `ExposureRate(t)`；
- Response 不按持续时间积分 `C(t)`；
- 时间、停留、穿越有效区域、覆盖范围不进入出手余量；
- 垂直运动通过“多久处在可交互垂直区域”影响 `L`，不进入 `u_close`。

## 5. Candidate join

```text
q_i,j = L_i,j × C_i,j
→ Opportunity Reduce
→ NativeCandidateSnapshot
→ optional Pre-Roll Gameplay Policy
→ TrueRoll
```

- Response 只产生原生贡献，`L × C` 只乘一次；
- Candidate 后段不再乘 Response；
- `ResolutionIncomplete` 的候选不进入 roll；
- Candidate 的 reducer 与 roll 规则属于 Candidate owner，本文不重定义。

## 6. 端到端状态表

| 层 | 输出 | 下游处理 |
|---|---|---|
| Margin | 数值 / `ResolutionIncomplete` / `Reject` | 只有数值进入投影 |
| C(theta) | `0` / `(0,1]` / 不输出 | 逐方位聚合后再乘 support |
| C_prey | 数值 / 区间 | 区间进入 sibling 聚合 |
| C_feed | 标量 / `ResolutionIncomplete` + bounds | 只有标量进入 `L × C` |
| L | 数值 / `ResolutionIncomplete` | 未解析不当作零 |
| q | 数值 | 只有数值进入 Opportunity Reduce |
| Candidate | native snapshot / 不可 roll | roll 由 Candidate owner 决定 |

## 7. 回归映射

| 规则 | 可复核入口 | 能证明 | 不能证明 |
|---|---|---|---|
| 投影形状与端点 | `proposal_c_response_projection_probe.py` | 截断线性、端点为 0/1 | 生产锚点 |
| 追赶成本形状 | `proposal_c_closing_cost_shape_probe.py` | q 与成本的单调关系 | 完整高速策略排序 |
| support × response | `proposal_c_support_retention_projection_probe.py` | 比例保留的形状 | 生产 support 尺度 |
| Trigger 形状 | `proposal_c_prediction_challenge_probe.py` | 单次事件的衰减形状 | 生产 `tau_recover` |

这些 probe 当前是形状检查；与本文 Working 值不一致的 fixture 需标注来源，不能互相冒充。

## 8. 未决

- Prediction 是否作为独立局部代价重入主体；
- `L` 的生产函数、单位与窗口口径，以及 Opportunity reducer；
- sibling set 的正式上游声明位置；
- `M1=0.40` 与 tail 参数的 reference calibration；
- 真实 encounter geometry 与 reaction window 是否引入 hard interception gate。

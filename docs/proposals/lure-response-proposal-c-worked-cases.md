# Proposal C｜工作案例

状态：Working Design / Candidate。以下案例用于检查语义契约，不是生产标定结果。

每个案例记录：事实 → 适用规则 → 中间结果 → 最终状态 → 禁止的错误实现。

## 1. 同一呈现支持两种解释

**事实：** 裙丝 Jig 加鱼形 T 尾，鱼形轮廓可见，实际运动接近底部，并记录到裙丝展开变化。

**结果：**

- 小鱼解释保留鱼形证据，support 高；
- 小龙虾解释保留近底和局部动态证据；
- 两套解释读取同一份实际记录；
- 两个 sibling response 进入同一次区间聚合；
- 食物偏好不改变猎物解释。

**禁止：** 因为鱼更爱吃小鱼，就把同一呈现改写成小鱼身份；或为两个解释各建一条机会记录。

## 2. 缺失历史不等于停留

**事实：** 记录从低位移开始，前面没有有效轨迹。

**结果：**

```text
current_state = low_displacement
prior_movement = Unknown
move_to_pause = Unknown
```

**禁止：** 把记录起点当作移动结束；给停留增加额外 bonus。

## 3. NoMatch 与 Unknown

**事实 A：** 小龙虾近底规则已配置，所需数据完整，近底条件不成立，规则明确返回零。

**结果 A：** `ResolvedNonResponsive`，`support = 0` 或规则定义的零。

**事实 B：** 同一规则已配置，但局部展开记录缺失，缺失可能改变匹配程度。

**结果 B：** support 区间或 `Unknown`，由归约器输出 `ResolutionIncomplete`。

**禁止：** 把 B 写成 0；把 A 写成 `Unknown`；只写“NoMatch 或零”而不说明规则是否返回数值。

## 4. Poor 与 Reject

**事实 A：** `CurrentFoodValue=0`，`M=1`，合法 Trigger 达到上限 `0.15`，负担接近零。

按 Working 门槛：

```text
threshold = 0.60 - 0.40 - 0.50 * (1 - 0.80) = 0.10
Margin = 0 + 0.15 - 0.10 = 0.05
C = clamp(0.05 / 0.40) = 0.125
```

**结果 A：** Poor 进入窄的弱响应窗口。

**事实 B：** `Reject`，其他条件相同。

**结果 B：** typed hard zero，不能复活。

**禁止：** 为救活 Poor 把全轴 `K_mot` 提到 `0.60`，导致中低 Motivation 的 Good 被压垮；或把 `Reject` 写成超大 cost。

## 5. 同一次突然改向

**事实：** 呈现发生一次 sudden redirection，state interpreter 判定 `TriggerIntensity=0.8`。

**结果（第一版生产主体）：**

```text
StateTriggerValue = 0.10 * 0.8 = 0.08
```

Prediction 不参与生产计算。

**诊断或候选评估时：** 可以同时记录

```text
PredictionCost = K_pred * PredictionChallenge
```

两条路径回答不同问题，因此允许在一次评估里并行记录；`StateTriggerValue - PredictionCost` 只作为回归诊断量，不是新字段，也不是已批准的生产路径。

**禁止：** 再加一个 generic erratic bonus；把 Trigger 直接写成 `a * turn + b * burst + c * event_count`；把诊断并行读成第一版主体已包含 Prediction。

## 6. Sibling 有界部分解析

**事实：**

```text
baitfish  = [0.80, 0.80]   # resolved
crayfish  = [0.20, 0.60]   # unresolved, upper bound 0.60
```

**结果：**

```text
L_feed = max(0.80, 0.20) = 0.80
U_feed = max(0.80, 0.60) = 0.80
L_feed == U_feed → C_feed = 0.80
```

未解析路径的上界低于已解析 winner，不改变结果，可以输出标量。

**反例：**

```text
baitfish  = [0.45, 0.45]
crayfish  = [0.10, 0.90]
```

`L_feed=0.45`，`U_feed=0.90`，保持 `ResolutionIncomplete` 并携带区间。

**禁止：** 把 Unknown 当 0 后直接输出 0.45；或因为有 Unknown 就把整个 feeding 判成 Unknown。

## 7. 机会是 L × C，一次

**事实：** 同一次呈现，Response 得到 `C=0.6`；Spatial / Opportunity 给出该颗粒的 `L=0.5`。

**结果：**

```text
q = 0.5 × 0.6 = 0.30
```

只有一次乘法。Candidate 后段不再乘 Response。

**事实 B：** Spatial / Opportunity 侧的 `L` 未配置或无法解析。

**结果 B：** `ResolutionIncomplete`，不是零机会。

**禁止：** 在 Response 内按持续时间积分 `C(t)`；把停留时长加成 `DecisionMargin` 的 bonus。

## 8. 垂直运动归 Opportunity

**事实：** 垂直 jigging，快速上升后下落，水平相对速度接近零。

**结果：**

- `u_close ≈ 0`，Closing 几乎不增加负担；
- 垂直运动通过“多久处在可交互垂直区域”影响 `L`；
- 不虚构一个 3D 鱼方位把它塞进 Closing。

**禁止：** 把 vertical-dominant presentation 当作已由 Horizontal2D 完整覆盖；或改用 Isotropic3D 来“解决”它。

## 9. Activity 与摄食意愿正交

**事实 A：** `ClosingLoad ≈ 0`，`Activity` 低。

**结果 A：** Activity 对追赶负担的倍率几乎不起作用；不能凭低 Activity 降低响应。

**事实 B：** 同样低 Activity，但目标需要追赶。

**结果 B：** ClosingCost 上升；Motivation 门槛不因此移动。

**禁止：** 让 Activity 同时降低 `InterceptSpeedLimit` 并抬高 soft cost；或把 Activity 和 Motivation 都写成“积极程度”。

## 10. 快速搜索的收益不在 Response 内

**事实：** 玩家选择快速搜索，单位时间覆盖更多水体。

**结果：**

- Response 只回答单次遭遇时鱼是否出手；
- 覆盖收益属于单位时间作钓效率，不在 Response 内加分；
- 快速呈现的代价由追赶负担、风险顾虑和 `L` 共同表达。

**禁止：** 在 Response 里加 search reward；用单次响应高低直接判断整套钓法优劣。

## 11. 攻击诱因不能免费

**事实：** 低摄食意愿，玩家换用强逃逸样呈现。

**结果：**

- 攻击诱因上升，帮助边缘目标跨线；
- 代价由已有机制产生：可能更高的追赶负担、更明显的机械暴露带来的风险顾虑；
- 不额外发明统一的“刺激惩罚”。

**禁止：** 只加诱因不加代价，形成固定最优解。

## 12. 警惕度调制风险顾虑

**事实：** 同样的装备暴露与运动异常，分别在低警惕鱼与高警惕鱼上呈现。

**结果：**

- 低警惕：风险顾虑弱；
- 高警惕：同样暴露产生更强抑制；
- 顶层只看到最终 `RiskCost`。

**禁止：** 把高速、频繁转向直接写成 `SuspicionLoad`；或在顶层再加一个 `自然度 × 警惕度` 交叉项。

## 13. 预测刷新而不是累加

**事实：** 单次转向，对比周期性重复转向。

**结果：**

- 单次：challenge 出现后按 `tau_recover` 衰减；
- 重复：每次事件刷新 `max_recent`，形成较高平台；
- 节奏已经通过刷新间隔进入系统，首版不需要累加模型。

**禁止：** 因为“持续 zig-zag 可能被低估”就立即改成事件累加。

## 14. 装配变化与记忆

**事实：** 呈现过程中更换拖尾。

**结果：**

- 新装配重新绑定证据；
- 仅与旧装配绑定的局部计时和事件失效；
- 同一主体的共用轨迹是否保留，按规则决定；
- 不把旧装配的猎物解释和状态事件直接带入新装配。

## 15. 案例的验收方式

```text
facts
→ applicable rule
→ intermediate state/value
→ final status/value
→ forbidden alternative
```

案例只验证语义区分和状态传播，不证明生产参数、现实鱼类行为或最终玩法效果。

# Proposal C｜Escape-like Trigger 第一版

状态：Working Design / Candidate。本文把已准入的逃逸样攻击诱因落到可执行的事实与判定，不扩展其它状态，也不冻结生产参数。

来源：`docs/lure-response-joint-evaluation` 的 `state-trigger-intensity-contract`、`escape-feature-routing`、`attack-trigger-strategy-contract`（按 `311ae70d` 快照核对）。

## 1. 范围

第一版只做一件事：

```text
轨迹事件
→ prey-conditioned 逃逸样解释
→ TriggerIntensity ∈ [0,1]
→ StateTriggerValue = TriggerBudget × TriggerIntensity
```

不做：受伤 / 挣扎、失衡样虚弱、停顿触发、领地或护巢。

## 2. 输入事实

| 事实 | 来源 | 约束 |
|---|---|---|
| 时间戳 | 轨迹记录 | 递增；窗口与连续性由上游声明 |
| 方向变化 `Δψ` | 相邻速度方向 | 只用实际发生的变化，不读玩家指令 |
| 速度变化 `Δv` | 相邻速度 | 必须声明世界速度或相对水体速度 |
| 猎物解释与 family | 第 2 层结果 | 没有解释就不产生逃逸样判定 |
| family 的触发配置 | 装配 / 规则配置 | 声明哪类事件对该 family 有效 |

事件的最小字段：

```text
TrajectoryEvent = { time, kind, strength, prey_families, source }
kind ∈ { turn, burst, pause, alternation }
strength ∈ [0,1]
```

`strength` 由事件提取器按可配置函数产生；本文不冻结提取公式。

事件在提取时就带上 prey family：某个 family 没有条目，表示该事件不是为这个 family 产生的，不等于 Unknown。该 family 的规则本身缺失，才是 `NotConfigured`。

## 3. 事件语义

### 转向事件

- 一次明显方向改变产生一个 `turn` 事件；
- 强度示例：`TurnStrength = (1 - cosΔψ) / 2`（joint 的 Working 形状）；
- 连续小幅摆动不产生事件；交替模式只影响“像不像”，不单独加分。

### 加速事件

- 一次明显加速产生一个 `burst` 事件；
- 强度是相对该呈现基准速度的归一化增量，缩放参数由配置给出；
- 不以加速度绝对值直接当强度，避免不同速度基准不可比。

### 不参与的事件

| 事件 | 处理 |
|---|---|
| `pause` | 不进入 Trigger；由时间机会与 attention 承接 |
| `alternation` | 只影响猎物解释置信度，不加 Trigger |
| `event count` | 不累加；重复事件不产生额外奖励 |

## 4. 判定规则

```text
1. 只读取当前窗口内的 turn / burst 事件
2. 只保留该 prey family 声明适用的事件
3. 每个 trigger-state explanation 取 max(适用事件强度)
4. 多个 explanation 之间取 max，不求和
5. 没有适用事件 → TriggerIntensity = 0
6. 没有该 family 的配置 → NotConfigured，不当作 0
```

窗口、事件阈值和 family 适用表都是可配置的 Working 参数。示例窗口 0.50 秒只用于验收向量。

### 为什么取 max 而不是求和

- 一次逃逸动作常同时包含转向和加速，求和会重复奖励同一个行为；
- 事件数量不能制造额外响应；
- 同一猎物状态的多个标签是替代解释，不是叠加机会。

## 5. 与代价的关系

Trigger 只提供正向贡献，代价由已有机制产生：

```text
更强的逃逸呈现
→ 更高的水平径向速度 → ClosingCost 上升
→ 更剧烈的机械操作 → RiskCue（若已解析）→ RiskCost 上升
→ 更短的有效窗口 → L 下降
```

Exception：`ClosingLoad ≈ 0` 时，低活性不能凭空压低响应；Trigger 也不补偿这一点。

## 6. 玩家操作映射

| 操作 | 期望事实 | 可能结果 |
|---|---|---|
| 连续急抽 / jerk | 多次 turn，可能有 burst | 触发强度升高，但刷新不累加 |
| 抽停 | burst 后 pause | 只有 burst 进入 Trigger；pause 归时间机会 |
| 快速平收 | 少量 turn，稳定速度 | 触发强度低 |
| 慢速翻滚 | 低强度 turn，无 burst | 第一版不产生逃逸样；受伤样未准入 |

## 7. 验收向量

窗口 0.50 秒；强度为配置输入；`now = 1.00`。

| 案例 | 事件 | 期望 |
|---|---|---|
| A | turn 0.80 @0.9 | I=0.80 |
| B | turn 0.80 @0.9 + burst 0.60 @0.95 | I=0.80（取 max，不是 1.40） |
| C | turn 0.60 @0.3 + turn 0.60 @0.9 | I=0.60（不累加） |
| D | turn 0.90 @0.2（窗口外） | I=0 |
| E | pause 0.90 @0.95 | I=0 |
| F | alternation 0.90 @0.95 | I=0 |
| G | 无事件 | I=0（已解析不响应） |
| H | 事件只标 baitfish，当前解释为 crayfish | I=0（该 family 不适用） |
| I | 当前 family 无配置 | NotConfigured |

可执行入口：`prototypes/lure-response/proposal_c_escape_trigger_probe.py`。它检查窗口过滤、family 适用、取 max 不求和、pause / alternation 不参与、NotConfigured 传播。

## 8. 数据与生产边界

- 事件提取需要连续轨迹与时间戳；仓内当前没有生产采集；
- 原型可用录制的轨迹或人工事件序列检查判定；
- family 适用表、窗口、强度函数均未标定；
- 本文不引入姿态输入；受伤样与虚弱样保持 `CandidateUnresolved`。

## 9. 未决

- 事件提取的滤波、采样与最短间隔；
- 各 family 的事件适用表；
- 强度函数的缩放参数；
- Trigger 窗口与刷新语义；
- 真实玩家能否稳定制造逃逸样，需 playtest 或录制数据。

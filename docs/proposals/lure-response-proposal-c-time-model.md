# Proposal C｜时间模型（Candidate）

状态：Working Design / Candidate。把散在各层的“时间”收在一处：哪些时间量存在、进入哪一层、不进入哪一层。不是 Current Contract，也不是生产参数。

## 1. 时间层

```text
采样 tick
→ 轨迹分段（segment）
→ 手法事件（原子 / 分子）
→ Trigger 窗口
→ 一竿快照（cast snapshot）
→ 机会窗口（L）
→ 会话 / 记忆边界
```

| 时间量 | 作用域 | 说明 |
|---|---|---|
| 采样 tick | 全局 | 第一版 Candidate 20 Hz；低于该频率按时间戳插值，缺口 > 300 ms 判 `Unknown` |
| 轨迹分段 | 一次呈现 | 装配或轨迹不连续时切段；段内时间单调 |
| 手法事件窗口 | 控饵技能 | 分子手法最大时窗、最小 / 最大衔接间隔、冷却、重复衰减 `K(n)`；来自控饵配置 |
| Trigger 窗口 | AttackTrigger | Working 500 ms；同一窗口内取 max，不累加 |
| 一竿快照 | Fish Condition | 抛竿开始形成，整竿只读；时段切换不重新解析 |
| 机会窗口 | `L` | `τ_g` 是手法窗口、空间可交互窗口、有效窗口三者交集的长度；空交集 = 0 |
| 会话 / 记忆 | Wariness overlay、装配记忆 | 跨 encounter / session 的边界仍未闭合 |

## 2. 时间进入哪里

| 层 | 消费的时间 | 规则 |
|---|---|---|
| 猎物解释 | 事件时间戳、窗口 | 只用窗口内事件；未来时间戳不预读 |
| 状态提取 | 分段、事件顺序、持续时长 | 停顿与移动按分段判定 |
| AttackTrigger | Trigger 窗口内的 turn / burst | 取 max；冷却内重复事件不刷新 |
| DecisionMargin | **不消费时间** | 时间、停留、覆盖不进入五项 |
| Fish Condition | 抛竿时刻 | 快照形成时校验；之后不刷新 |
| Opportunity / `L` | 手法窗口、有效窗口、replay | 同一 identity 重算不增加 `L` |
| Candidate | 决策窗口 | 按窗口归约，不反向修改 Response |

## 3. 边界规则

1. 时间只通过 `L` 和事件窗口进入系统，不进入 `DecisionMargin`；
2. 停留改变 `τ`，不改变五项评价；
3. 一竿快照形成后整竿只读；过期检查发生在形成时；
4. replay、重复 tick、重复调用不增加机会；
5. 装配变化切段；旧装配的局部事件与计时失效，共用轨迹是否保留按显式规则；
6. 跨 session 的记忆边界必须显式声明，不能默认继承。

## 4. 未闭口

- 实际采样率与低帧率设备的退化行为；
- reaction window 与 strike reach 的时间定义；
- 控饵技能的最大时窗、最小 / 最大衔接间隔、冷却与重复衰减如何映射到 `τ`；
- 垂直可交互窗口的时间边界；
- 会话边界与 Wariness overlay 的记忆范围；
- 装配变化时共用轨迹记忆的保留边界。

# Proposal C｜Feature Ownership Matrix

状态：Working Closure / Candidate。本文是跨 feature 的 ownership Contract；具体公式与生产参数仍由各机制文档负责。

## 1. 目的

同一个 raw fact 可以有多个不同语义后果，但每个后果必须有明确 owner。本文只解决：

> 一个事实可以被哪些路径消费，以及哪些重复计权不允许发生。

基本原则：

- 允许同一事实进入多个路径，只要回答的是不同问题；
- 禁止用不同字段名重复结算同一个效果；
- 第一版不允许匿名 residual bonus / penalty；
- 新增第二条数值路径前，必须通过 residual admission gate。

## 2. Feature → Owner

| 原始事实 / 事件 | 第一版 owner | 允许的语义 | 第一版禁止 |
|---|---|---|---|
| 拟饵相对水体水平速度 | 追赶负担（Closing） | 当前追赶需求有多高 | 自动变可疑、通用“不自然”惩罚、PredictionCost |
| 鱼种 × 体型档 | 追赶能力 / 尺寸偏好 | `InterceptSpeedLimit`；与猎物尺寸共同影响 SizePreference | 当作鱼况；先抽具体个体再决定是否响应 |
| 猎物 / 拟饵尺寸 | 食物价值（FoodValue） | 与捕食鱼体型档共同形成软尺寸偏好 | 默认进入 Motivation；默认进入 Closing |
| 整体轮廓 / 比例 / 颜色 / 反光 | 猎物解释器：外观证据 | 支持某个 prey interpretation | 直接变成 FoodValue 或咬口概率 |
| 整体运动模式 | 猎物解释器：整体运动证据 | 让某个猎物表达更充分 | 通用 AttackTrigger；通用 naturalness bonus |
| 局部部件动作 | 猎物解释器：局部动作证据 | 尾摆、腿踢、裙丝等 prey-specific 表达 | 直接按动作幅度累加攻击奖励 |
| 水面 / 近底 / 中层 / 触底等空间关系 | 猎物解释器：空间关系证据；Opportunity 读取空间事实 | 支持特定 prey interpretation；决定有效交互窗口 | 单独制造强猎物身份；重复结算同一空间收益 |
| sudden direction change | 猎物状态解释 → AttackTrigger（仅形成 Escape-like 时） | 表达逃逸样状态 | PredictionCost；通用 ErraticBonus；默认 Suspicion |
| burst / sudden acceleration | 猎物状态解释 → AttackTrigger；若实际速度改变，同时进入 Closing | 攻击诱因 + 追赶需求变化 | 额外 BurstBonus；默认 Suspicion |
| Pause / 低位移 | 原子姿态；猎物分子姿态；Closing / Opportunity 读取相关事实 | 组成“抽停”等状态；速度下降；机会窗口重新评价 | PauseBonus；DwellBonus；“停越久 L 必然越大” |
| favorable dwell / duration | Opportunity | 当前机会窗口持续与覆盖关系 | 进入 DecisionMargin；Response 内按时间积分 |
| prey support | 猎物解释层；最终只按既定 Response 契约使用 | 表达解释支持强度 | `1-support → Suspicion`；直接等于 FoodValue；当 prey probability |
| prey current state | 猎物状态解释 → AttackTrigger / explain | 当前猎物状态是否额外促发攻击 | 改写 BaseDietAffinity；状态标签直接加 bonus |
| 终端前导 / 钩 / 别针 / 转环等显眼度 | Tackle Conspicuousness → SuspicionLoad（字段落地后） | 当前终端钓组暴露程度 | SKU 直映；修改 prey support；进入 Closing |
| fishing pressure | Wariness 上游 cause | 提高警戒度 | 同时进入 SuspicionLoad，形成近似平方放大 |
| repeated exposure / conditioning | Wariness runtime update 候选 owner | 未来的累积警戒状态 | 未授权前直接修改 Response 或其它 Fish Condition |
| Activity | Closing soft-cost multiplier | 当前愿意承担多少追赶行为代价 | 修改 `InterceptSpeedLimit`；代替 Feeding Motivation；通用 hard gate |
| Feeding Motivation | WillingnessThreshold | 当前为了食物出手需要多强理由 | 乘 FoodValue；修改运动能力；改 prey identity |
| Wariness | RiskCost sensitivity | 对已解析风险 cue 有多敏感 | 当通用 threshold；进入 Closing |
| Diet Shift | FoodValue 的 prey-family 动态偏移 | 当前食性向哪些 prey family 偏转 | 全局摄食 boost；代替 Motivation |
| 垂直运动 / 水层穿越 | Opportunity | 垂直可交互窗口 | 进入 Closing 伪装追赶负担 |
| 空间覆盖 / 扫过范围 | Opportunity | 快搜真正覆盖多少有效机会 | Response 额外 FastSearchBonus |
| 模式基础强度 / 基础权重 | 上游权重链 | 候选原始量级 | 被适配系数 `C>1` 放大；在 Response 内重新 author |

## 3. 允许同一事实进入多条路径的情况

### 3.1 Burst

同一个 burst 可以同时：

```text
burst
→ prey-conditioned Escape-like
→ AttackTrigger
```

以及：

```text
burst 改变实际速度
→ ClosingCost 改变
```

这不是重复计权，因为一个回答“是否更促发捕食”，另一个回答“是否更难追”。禁止再加第三份通用 BurstBonus。

### 3.2 空间关系

近底可以同时：

- 作为小龙虾等猎物解释的空间证据；
- 作为 Opportunity 的空间事实，判断当前是否真的处在有效交互窗口。

前者回答“像什么”，后者回答“机会有没有形成”。不得把同一近底事实再变成匿名 Response bonus。

## 4. 明确禁止的重复计权

### 4.1 speed 双扣

禁止：

```text
高速
→ ClosingCost
→ 又因为“不自然”进入 SuspicionLoad
```

除非未来控制 Closing、support、Trigger、Opportunity 后仍证明速度本身是独立的风险 cue。

### 4.2 low support 双扣

禁止：

```text
prey support 低
→ 解释贡献低
→ SuspicionLoad = 1 - support
```

“不像某猎物”不等于“危险”。

### 4.3 pause 重复奖励

禁止：

```text
pause
→ 速度下降带来 Closing 变化
→ Opportunity 重算窗口
→ 再加 PauseBonus
```

Pause 只有 prey-specific 状态语义时才通过对应解释路径产生额外效果。

### 4.4 fishing pressure 平方式放大

禁止：

```text
fishing pressure
→ Wariness 高
→ SuspicionLoad 也高
→ RiskCost = Wariness × SuspicionLoad
```

第一版 fishing pressure 只作为 Wariness 的上游；SuspicionLoad 必须来自当前 presentation-local cue。

### 4.5 多猎物解释数量奖励

禁止因为同一拟饵能解释成更多 prey type 就直接加分或做概率并集。

同一 physical target 的 sibling prey interpretations 最终按 Response Contract 取最大已解析适配系数，不按“解释数量”奖励。

## 5. Tackle Conspicuousness 第一版结构

生产字段尚未建立前：

```text
SuspicionLoad = 0
RiskCost = 0
```

字段落地后，第一版 Candidate 聚合：

```text
TackleConspicuousness = 1 - Π(1 - c_i)
```

- `c_i ∈ [0,1]`；
- 只计算目标饵以外的终端钓组逻辑部件；
- 拟饵主体仍归猎物表达；
- 水体透明度、光照等 visibility context 只有证明有必要后再加，不提前构建复杂视觉模型。

## 6. Prey Interpreter ownership

一个拟饵可以声明多个可表达的猎物类型。每个 prey type 自己拥有：

```text
实际呈现事实
→ Support Interpretation
→ Prey Support

同一事实 + 该 prey type 规则
→ State Interpretation
→ Atomic Pose + optional Composite Pose + 其它状态维度
```

共同事实只提取一次；各解释器读取同一事实，不各自重新计算一套速度 / 水层 / 轨迹基础数据。

旧 Dynamic Route 不再是独立 owner，只是解释器内部的动态表达规则。

## 7. Fish Condition 与一竿快照

Fish Condition baseline 在抛竿开始时解析：

```text
ConditionGroup × EngagementMode
→ Cast Fish Condition Snapshot
→ 本竿 Response 只读
```

- Activity、Feeding Motivation、Diet Shift、Wariness 不因存在 runtime framework 就自动获得 runtime state；
- 当前只有 Wariness 有累积语义依据；真正 runtime update 仍需独立机制 Contract 授权；
- 一竿中时段 / 天气映射变化不改写本竿 baseline；下一竿重新解析。

## 8. residual admission gate

任意新 feature / cue 想进入第二条数值路径时，必须回答：

1. 新路径回答的具体问题是什么？
2. 与现有 owner 的语义是否独立？
3. 固定现有路径后，是否仍有稳定 residual ranking difference？
4. 玩家能否通过独立策略改变这个后果？
5. 是否会把同一个 cause 在加法或乘法结构中重复放大？

不能回答清楚时，只保留为 metadata / explain，不进入 numeric core。

## 9. 回归测试建议

至少保留下列 controlled pairs：

```text
A. 同 Closing，不同 Escape-like Trigger
B. 同 Trigger，不同实际速度
C. 同 prey support，不同终端钓组 cue
D. 同终端钓组 cue，不同 prey support
E. 同拟饵速度，不同 Activity
F. 同 FoodValue，不同 Feeding Motivation
G. 同 prey presentation，不同 size cohort
H. 同 Response C，不同 Opportunity L
```

每组只改变一个 semantic outcome；非 owner 路径不应随之漂移。
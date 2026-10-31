# 路亚响应设计护栏

状态：Candidate Guardrail。本文不冻结生产参数，只维护跨模块负向边界。

## 1. 适用范围

当前只约束路亚的姿态响应（Pose Response）主线。台钓 / 浮钓的持久响应与其它 Interaction family 不能机械套用本文算子。

当前主链：

```text
实际呈现
→ 猎物解释器
   ├ 表达支持度
   └ 当前状态
→ 五项响应评价
→ 适配系数 C

同一姿态颗粒
→ Opportunity 计算机会量 L

Candidate join
→ L × C
```

## 2. 猎物解释层护栏

### 2.1 拟饵不是猎物类型

一个拟饵 / 饵装配可以同时表达多个猎物类型。不得用商品类别、SKU 或作者命名直接锁死唯一猎物身份。

每个猎物解释器负责两个问题：

1. 当前呈现有多像该猎物 → 表达支持度；
2. 如果按该猎物理解，当前处于什么状态 → prey-conditioned state。

实现可以是 class、Strategy 或数据规则；Contract 不要求 OO 继承树。

### 2.2 第一版 Evidence 只分四类

- 外观证据（Appearance）
- 整体运动证据（Whole-body Motion）
- 局部动作证据（Articulation）
- 空间关系证据（Spatial Relation）

声音、振动、压力信号只有在证明其具有独立的 prey-specific 身份语义后才进入猎物解释；不能因为“刺激强”就当成猎物支持。

### 2.3 Dynamic Route 不是独立业务层

旧 Dynamic Route 只保留为猎物解释器内部的“动态表达规则”：某种运动可以让已有猎物表达更充分。

它回答“这样动以后更像不像”，不回答“鱼是不是因此更想立刻攻击”。后一个问题归攻击诱因。

### 2.4 同级证据默认不相加

同一 Evidence 内部的替代动态表达默认取最强；同一猎物类型的替代 Evidence 也默认取最强。

```text
EvidenceScore = max(base, dynamic_expression_1, ...)
PreySupport   = max(applicable evidence scores)
```

只有 A+B 同时出现才形成新语义时，才显式配置 Joint Evidence / Joint Expression。不得因为作者把一个事实拆得更细，就得到更高 support。

## 3. 姿态与状态护栏

当前运动姿态按两层表达：

```text
1 个当前原子姿态
+ 0 或 1 个主导分子姿态
```

原子姿态描述当前这一刻，例如移动、停顿、上升、下落；分子姿态描述当前姿态与必要前史形成的过程，例如“抽动→停顿”“爆发→转向→停顿”。

多个分子姿态同时满足时，不叠多个匿名 bonus；猎物解释器选择更具体、解释力更强的主导过程。

水面、近底、侧翻角、离底距离等是正交事实 / 状态维度，不额外占用“姿态槽位”。

停顿（Pause）是原子姿态，但没有通用 `PauseBonus`。

## 4. 攻击诱因护栏

攻击诱因只回答：

> 已经被解释为可接受猎物以后，当前状态是否额外促发捕食出手？

第一版正式准入只有逃逸样（Escape-like）。

“游得更像”“尾摆更自然”“整体拟真度更高”主要提高猎物表达支持度，不自动成为攻击诱因。

不得把一次逃逸动作拆成：

```text
turn bonus
+ burst bonus
+ acceleration bonus
+ event-count bonus
```

同一语义事件只结算一次。

`StateTriggerValue = TriggerBudget × TriggerIntensity` 只能增加出手余量；最终适配系数始终 `0 ≤ C ≤ 1`，不会因 Trigger 把基础强度放大到 1 以上。

## 5. 追赶负担护栏

第一版不模拟相对方位 θ。产品假设是：形成摄食机会时，鱼正在追拟饵。

```text
q = 拟饵相对水体水平速度 / InterceptSpeedLimit
ClosingCost = K_close × q² × ActivityCostMultiplier(Activity)
```

- `InterceptSpeedLimit` 由鱼种 × 体型档提供能力基线；
- Activity 只调制当前追赶负担，不修改物理速度能力；
- `q >= 1` 不自动 hard-zero；
- 没有真实鱼位置时，不用“刚好迎面而来”等相对方位特例抵消高速负担；
- 垂直运动与有效交互窗口归 Opportunity，不塞进 Closing。

## 6. Prediction 护栏

运动可预测性第一版不进入 active numeric core。

原因：大部分玩家可感知后果已经分别由猎物表达、攻击诱因、追赶负担、Opportunity 与风险承接。

只有在控制这些量以后，“纯可预测性”仍稳定改变可学习的玩家策略排序，才允许重开。不得为了拟合结果恢复匿名 `PredictionCost`。

## 7. Risk 护栏

```text
RiskCost = K_wary × Wariness × SuspicionLoad
```

Wariness 是鱼有多警戒；SuspicionLoad 是本次呈现里有多少已解析的可疑线索。两者不能由同一 cause 在乘法两边重复生成。

禁止：

- `SuspicionLoad = 1 - prey_support`；
- 高速度自动变可疑；
- 高频转向自动变可疑；
- fishing pressure 同时进入 Wariness 与 SuspicionLoad；
- SKU 直接映射可疑度。

当前终端钓组显眼度（Tackle Conspicuousness）保留为首个风险方向。生产字段尚未建立前，`RiskCost=0`。

当字段落地时，第一版 Candidate 聚合采用：

```text
TackleConspicuousness = 1 - Π(1 - c_i)
```

`c_i` 是目标饵以外的终端钓组逻辑部件显眼度，例如前导、钩、别针、转环。拟饵主体仍归 prey expression，不重复计入终端钓组显眼度。

## 8. Fish Condition 护栏

正式鱼况只有：

- Activity / 活跃度
- Feeding Motivation / 摄食动机
- Diet Shift / 食性偏移
- Wariness / 警戒度

不得恢复 FunctionalCapacity / CapacityModifier，除非未来证明 species × size cohort 的能力基线 + Activity 仍解释不了一个重要、稳定的动态运动能力差异。

Activity 只要求有限、非负；不设语义生产上界。1.0 只是 Working reference，不是缺失 fallback。

第一版 baseline 使用“一竿一个 Fish Condition Snapshot”：

```text
Cast Start
→ 解析当时的 DEF / ConditionGroup
→ 形成本竿 Fish Condition Snapshot
→ 本竿 Response 只读
→ 下一竿重新解析
```

一竿中时段切换不改写本竿 baseline。Wariness 的 runtime overlay 如果未来实现，必须单独授权，不因此把其它 Condition 都做成持续刷新状态机。

## 9. 机会量与适配系数护栏

正式术语：

```text
C = 适配系数
L = 机会量
```

适配系数回答“机会已经摆到鱼面前时，当前模式对呈现有多适配”。机会量回答“这个机会是否形成、形成多少、在哪个时间 / 空间窗口有效”。

```text
候选贡献 = L × C
```

只乘一次。

停留时间是 Opportunity 的输入之一，但不规定“停越久，L 必然越大”。错误水层、无效窗口或覆盖效率下降时，多停可能没有收益。

## 10. 同级猎物解释聚合护栏

同一物理目标、同一 Feeding route 下的替代猎物解释，最终适配系数取最大：

```text
C_final = max(C_baitfish, C_crayfish, C_frog, ...)
```

只对已解析 sibling 使用该规则；未解析分支按当前状态协议记录，不当作 0。这个 `max` 不自动推广到 Feeding / Defense / Investigation 等不同 Interaction family。

## 11. 通用状态护栏

必须区分：

- `Reject`：明确硬边界；typed zero；
- `Unknown`：必要事实缺失；
- `NotConfigured`：规则 / owner / 配置不存在；
- `NoMatch`：规则已检查但未命中；
- `ResolutionIncomplete`：归约后仍无法形成最终标量；
- `InvalidInput`：输入违反契约或不可计算；
- `ResolvedNonResponsive`：输入完整且结果为 0；
- `ResolvedResponsive`：输入完整且结果大于 0。

不得把 Unknown / NotConfigured / 非数值 NoMatch 偷换成 0。

## 12. 新机制准入门槛

任何新 feature 想进入第二条数值路径，至少回答：

1. 新路径具体回答什么问题？
2. 与现有 owner 的语义是否独立？
3. 控制现有路径以后，是否仍有稳定 residual ranking difference？
4. 玩家是否能通过独立策略改变它？
5. 是否会把同一个 cause 在加法或乘法结构里重复放大？

回答不清楚时，保留为 metadata / explain，不进入 numeric core。

## 13. 当前明确不恢复

- 独立 PredictionCost；
- 相对方位 θ 积分；
- `u_close >= 1` / `q >= 1` 通用 hard gate；
- 通用 PauseBonus / DwellBonus / ErraticBonus / CadenceBonus；
- `1 - prey_support → SuspicionLoad`；
- Activity 乘进 InterceptSpeedLimit；
- Candidate 再乘一次 Response；
- Response 内按时间长度积分；
- 仅为了“更真实”而增加没有独立玩法价值的新轴。
# Fish Condition｜输入登记与状态测试候选

> 状态：Candidate / Working Registry
> 日期：2026-10-30
> 边界：本文只登记四个 Fish Condition 的输入类别、状态判据和最小结构测试，不定义 cause 曲线、生产数值或 runtime overlay Contract。

## 1. 公共输入登记格式

每个 Condition 的机制 Contract 在注册输入时，至少声明：

```text
ConditionInputRegistration {
  condition
  inputRef
  sourceRef
  sourceVersion
  scope: ConditionGroup × EngagementMode
  temporalRole: snapshot | event | overlay
  required: true | false
  status
  provenance
}
```

输入登记和数值求值分开。没有登记的输入不能被实现偷偷读取；登记不等于该输入已经获准进入生产。

## 2. 四个 Condition 的输入面

| Condition | baseline 输入面 | runtime 输入面 | 当前可消费位置 | 未收口内容 |
|---|---|---|---|---|
| `Activity` | 环境 / 鱼习性配置形成的条件组事实 | 未授权前无 | Response 的 Closing soft cost；Fish AI 边界 | cause、映射、reducer、标定 |
| `FeedingMotivation` | 环境 / 时段 / 鱼习性条件组事实 | 未授权前无 | Response 的 WillingnessThreshold | cause、时间语义、threshold 映射 |
| `DietShift` | DEF baseline 的 prey-family identity / snapshot | 未授权前无 | 下游消费仍由 C-12b 决定 | prey-family 字典、映射、消费语义、记忆 |
| `Wariness` | DEF baseline 的条件组事实 | 仅 Wariness Contract 授权后 | Response 只读；Risk 当前不消费真实 cue | 事件来源、粒度、衰减、有效期、session memory |

说明：表中“输入面”只描述允许登记的来源类别，不声明任何天气、温度、溶氧或事件已经对应到某个 Condition。

## 3. 状态判据

### 3.1 Resolved

满足以下条件才可得到 `Resolved(value)`：

- 所有 required 输入已登记且版本可解析；
- source、scope、validity 和 provenance 完整；
- 对应 Condition Contract 已授权该输入和求值形式；
- 值满足该 Contract 的合法性约束。

### 3.2 Zero

`Zero` 只表示已解析且有意义的真实零。它不能用来代替缺少输入、未配置、过期或被阻断。

### 3.3 Unknown

以下任一情况都产生 `Unknown`：

- required 输入缺失；
- snapshot 或 overlay 已过期且无有效替代来源；
- 来源版本不可解析；
- 必要 provenance 不完整；
- 输出是否会改变当前结果尚未收敛；
- baseline 数值越界，包括已知违反非负约束的 Activity=-0.1。

### 3.4 Invalid / NotApplicable

- baseline 解析遵循 Owner 裁定：数值越界、过期或缺源均为 `Unknown`，不因能诊断其原因就改成 `Invalid`。
- `Invalid` 用于结构、类型、所有权错误或未授权 overlay；不覆盖上述 baseline 数值越界规则。
- Response 消费端若被直接注入非法数值，可按其独立输入校验返回 `InvalidInput`；这不是 ConditionValue 状态，也不能回写 baseline 解析状态。
- `NotApplicable`：该 Condition 对当前 scope 明确不适用，并由 Contract 显式声明。
- 未配置不能默认为 `NotApplicable`。

`Reject` 不属于 ConditionValue 状态；它只属于 Response candidate 的语义结果层。

## 4. 最小状态测试

| 测试 | 输入 | 预期 | 禁止退化 |
|---|---|---|---|
| 完整 baseline | required source、version、validity 齐全 | `Resolved` | 仍返回 `Unknown` |
| 合法零 | 已解析、Contract 允许零 | `Zero` | 当成缺失或 Reject |
| 缺 required | 缺少一个必需输入 | `Unknown`；下游信号为 `ResolutionIncomplete` | 回填默认值 |
| 过期 snapshot | validity 已结束且无替代 | `Unknown` | 沿用 last value |
| baseline 数值越界 | 来源完整的 Activity=-0.1 | `Unknown`；下游 `ResolutionIncomplete` | 改判 baseline 为 `Invalid` 或截断到0 |
| 消费端绕过解析器 | Response 被直接注入 Activity=-0.1 | 消费端 `InvalidInput`，不改 baseline 状态 | 与 baseline `Unknown` 混作同一层 |
| 未授权 overlay | overlay 目标 Condition 未授权 | `Invalid` | 当作普通事件 |
| 明确不适用 | Contract 标记 scope 不适用 | `NotApplicable` | 静默缺席 |
| 不完整 provenance | source 或 version 缺失 | `Unknown` | 当作已解析 |
| Response 只读 | Response 进行求值 | baseline / overlay 不变 | 反写 DEF 或 runtime state |

## 5. Condition 专属红线

### Activity

- 不把 `Activity` 变成 `InterceptSpeedLimit` 或 `CapacityModifier`。
- 不用 `[0,1]` 作为未裁定的生产上界。
- `Unknown` 不能回填 `1.0`。

### FeedingMotivation

- 不由 Groundbait、Food 或 Flavor 直接写入。
- 不把缺失 Motivation 当作“没有摄食意愿”的合法零，除非对应 Contract 明确规定。

### DietShift

- `prey family` 是载体 / identity 轴，不自动决定 Food 或 Flavor 消费。
- 不做未获授权的逐杆随机漂移。
- C-12b 未收口前，不把它写成 Food Preference 或 Flavor Preference 的已定规则。

### Wariness

- 不用 Wariness 代替 `TackleConspicuousness`。
- 不因 Wariness 存在就自动产生 `RiskCost`。
- runtime overlay 未授权前只读 baseline。

## 6. 开工顺序

1. 先实现公共 baseline block、状态解析和 provenance 校验。
2. 为 Activity、FeedingMotivation、DietShift、Wariness 分别登记 required 输入，但不填未裁定的 cause 曲线。
3. 用本页状态测试覆盖缺失、过期、合法零、Invalid 和 NotApplicable。
4. 只读 Response 消费 baseline。
5. 最后单独处理 Wariness runtime overlay；没有事件来源和记忆 Contract 就不实现累积。

本页完成后，下一份设计输入应是各 Condition 的独立机制 Contract，而不是一个四者共用的总公式。

# 台钓中鱼机制｜Fish Condition Contract 注册表候选

> 状态：Candidate / Working Registry
> 日期：2026-10-30
> 边界：本文不定义 Activity、Feeding Motivation、Diet Shift 或 Wariness 的生产曲线。它只把四个 Condition 的 Contract 责任、状态载体、消费权限和开工门列成一张注册表。

## 1. 责任分层

```text
各 Condition 机制 Contract
  → 定义语义、合法输入、cause 映射、曲线 / reducer、标定证据

Bake
  → 统一执行、物化 baseline、校验来源 / 状态 / 版本 / validity

DEF
  → 保存 Fish Condition baseline block

被授权的 Runtime Overlay
  → 只修改被授权的 Condition

Response
  → 只读 ResolvedFishCondition
```

公共载体不授予任何 Condition 新的 runtime authority。每个 Condition 必须有自己的 Contract ref 或保持 `NotAdmitted`。

## 2. 注册表

| Condition | baseline 载体 | 当前 runtime overlay | 主要消费者 | 当前开工状态 |
|---|---|---|---|---|
| `Activity` | DEF 条件组 snapshot / block | 不自动授权 | Response 的 Closing soft cost；Fish AI 边界 | baseline 载体可开工；cause / 曲线 / 标定未收口 |
| `FeedingMotivation` | DEF 条件组 snapshot / block | 不自动授权 | Response 的 WillingnessThreshold | baseline 载体可开工；cause / 曲线 / 标定未收口 |
| `DietShift` | DEF 条件组 snapshot / block，按 prey family 轴 | 不自动授权 | 下游消费位置仍由 C-12b Owner / Current 决定；本注册表不预设 Food / Flavor 路径 | baseline 载体可开工；prey family identity / 映射和消费语义未收口 |
| `Wariness` | DEF 条件组 snapshot / block | 仅 Fish Condition / Wariness Contract 授权后可开工 | Response 只读；Risk 方向仍受 `TackleConspicuousness` 阻断 | baseline 可开工；runtime 事件、粒度、衰减、有效期、session memory 未收口 |

## 3. 统一状态协议

每个 baseline 值和 overlay 解析结果都使用：

```text
ConditionValue<T> {
  value?
  status: Resolved | Zero | Unknown | Invalid | NotApplicable
  sourceRef?
  producerVersion?
  validity?
  provenance?
}
```

统一规则：

1. 过期、越界或缺少必要来源 → `Unknown`。
baseline 解析与消费端输入校验分层：Activity=-0.1 在 baseline 解析中为 `Unknown`；直接注入 Response 时可由其返回 `InvalidInput`，不得回写 baseline。`Invalid` 不覆盖 baseline 数值越界规则，只用于结构、类型、所有权错误或未授权 overlay。

2. `Unknown` 不沿用 last value，不静默变成 0 或默认值。
3. 合法零使用 `Zero`，与未知分开。
4. 未授权 overlay → `Invalid`。
5. Response 只读 `ResolvedFishCondition`，不写回 DEF 或 overlay。
6. `Activity` 必须非负且有限，但不设语义生产上界；`1.0` 只是 Working reference。

## 4. 各 Condition 开工门

### 4.1 Activity

已确认边界：

- Activity 不降低 `InterceptSpeedLimit`，不恢复 `CapacityModifier`。
- Activity 只可进入已声明的 Closing soft-cost 消费和 Fish AI 边界。
- 不能把实现方便用的 `[0,1]` clamp 当成生产上界。

开工前仍需：

- 合法输入 cause；
- cause → Activity 的映射；
- reducer / 曲线；
- 有限值和异常处理；
- 标定证据。

### 4.2 Feeding Motivation

已确认边界：

- Feeding Motivation 进入 `WillingnessThreshold`。
- Groundbait、Food、Flavor 不直接写入它。
- 没有单独 runtime Contract 前，只消费 Bake baseline。

开工前仍需：

- baseline 输入与版本；
- cause 映射和时间语义；
- threshold 的消费 Contract；
- 缺失 / Unknown 的响应行为。

### 4.3 Diet Shift

已确认边界：

- Diet Shift 的载体轴是 `prey family`，不自动等同于 Food Target。
- C-12b 的下游消费语义仍为 OPEN；本注册表不预设它修改 Food Preference、Flavor Preference 或两者。
- Diet Shift 不由 Food Event 直接写入。
- 没有单独 runtime Contract 前，不做随机或逐杆漂移。

开工前仍需：

- prey family 字典与版本；
- baseline / identity 的映射 Contract；
- C-12b 的消费裁定或对应机制 Contract；
- 时间尺度、记忆和 validity；
- 与未来消费路径的 provenance。
### 4.4 Wariness

已确认边界：

- Wariness 的最终状态 owner 归 Fish Condition 线。
- V1 可以只有 Bake baseline。
- Runtime overlay 开工前必须闭合事件来源、作用粒度、衰减 / 有效期和跨 session 记忆。
- Risk 当前不使用 Wariness 伪造 `TackleConspicuousness`；未准入时 `RiskCost = 0`。
- Wariness 与 Avoidance 分开保存 provenance。

开工前仍需：

- Wariness Runtime Overlay Contract；
- 事件来源分类；
- encounter / session 边界；
- 过期协议和测试；
- Response 只读消费点。

## 5. 不允许的快捷实现

```text
公共 Fish Condition block → 四个 Condition 都自动 runtime
Activity → InterceptSpeedLimit
Activity → CapacityModifier
Food / Flavor → 直接写 FeedingMotivation
Food Event → 直接写 DietShift
Wariness → 自动 RiskCost
SKU / speed / turn count → TackleConspicuousness
过期 baseline → last value
Unknown → 0
```

## 6. 验收矩阵

| 检查 | 红对照 | 绿条件 |
|---|---|---|
| baseline 承载 | 裸字段散落且无来源 | DEF 条件组 block，带 source / version / validity |
| runtime authority | 四个 Condition 自动可写 | 只有对应 Contract 授权的 Condition 可 overlay |
| stale 处理 | 过期继续沿用 | 无有效来源时为 `Unknown` |
| Activity 上界 | clamp 到任意便利上限 | 非负有限，无语义生产上界 |
| Wariness / Risk | 用 Wariness 代替 Risk cue | `TackleConspicuousness` 未准入时 `RiskCost=0` |
| Diet Shift 轴 | Food Target 与 prey family 静默混同 | 明确 prey family 轴和映射 provenance |
| 响应写入 | Response 改 DEF / overlay | Response 只读 resolved state |

## 7. 下一步

先为四个 Condition 各自建立最小机制 Contract 的输入登记和状态测试，再讨论具体 cause 曲线。第一批优先级：

1. `Activity` baseline 合法输入与 Closing 消费边界；
2. `FeedingMotivation` baseline 到 Threshold 的接口；
3. `DietShift` prey family 轴与 Food 映射；
4. `Wariness` baseline 只读路径；
5. 最后再单独开 Wariness runtime overlay，不与第一版基础链捆绑。

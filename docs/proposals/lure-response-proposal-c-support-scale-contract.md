# Proposal C｜Prey Support 数值标尺契约

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

Proposal C 第一版继续使用：

```text
C_prey
= support_prey
  × E_theta[C_conditional(theta)]
```

但该乘法成立的前提是：`support_prey` 不能只是排序意义上的“更像 / 不太像”分数，而必须在猎物解释器输出处已经被校准为一个可做比例运算的 **interpretation retention scale**。

Response 不再额外增加 `RecognitionProjection`。如果某种 raw evidence 需要非线性压缩、阈值或饱和，应在猎物解释层把它编译进最终 support，而不是在 Response 再投影一次。

## 2. support 的数值语义

最终交给 Response 的 support 范围为 `[0,1]`：

```text
support = 0
→ 当前已评价范围内，这个 prey interpretation 不贡献 Feeding response

support = 1
→ reference full-support；不再衰减该 interpretation 的 conditional response

0 < support < 1
→ 按同一比例保留该 interpretation 的 conditional response contribution
```

因此在其它条件完全相同的情况下：

```text
support = 0.8
C_conditional = 0.75
→ C_prey = 0.60

support = 0.4
C_conditional = 0.75
→ C_prey = 0.30
```

这里的 `0.8 / 0.4` 不是 prey identity probability，而是 Response 可直接消费的 contribution-retention 标尺。

## 3. 为什么这个契约必须显式存在

Proposal C 上游当前允许人工配置证据基值、动态上限，并按解释路径更新支持。例如某份证据可以从 `0.40` 随动态匹配升到 `0.75`。

如果这些数值只表达序位：

```text
0.75 比 0.40 更像
```

则不能自动推出：

```text
0.75 可以保留 75% response
0.40 可以保留 40% response
```

所以第一版要么增加 `RecognitionProjection`，要么让最终 support 本身具有比例语义。

为避免新增一层自由参数，当前选择后者。

## 4. raw evidence 与 final support 分层

推荐解释：

```text
raw / authored evidence
→ prey-specific interpretation path
→ evidence aggregation / dynamic matching
→ final calibrated support [0,1]
→ Response
```

Response 只消费最后一项。

因此：

- 证据基值 `0.40` 是否最终仍是 `support=0.40`，属于解释器 calibration；
- 动态路径上限 `0.75` 是否最终仍是 `support=0.75`，也属于解释器 calibration；
- Response 不知道某个 support 是来自形态、运动、接触还是组合路径；
- Response 不再对 support 做第二次 soft gate / S 曲线。

## 5. 跨 prey family 可比性

由于 Feeding composition 使用：

```text
C_feed
= max_p(
    support_p
    × C_conditional_p
  )
```

不同 prey family 的 support 必须共用同一输出标尺。

否则：

```text
baitfish support = 0.8
crayfish support = 0.6
```

如果两类内部各自采用不同标尺，二者乘完后不能直接 `max`。

第一版因此要求：

> `support=1`、`support=0.5`、`support=0` 在 baitfish / crayfish / frog 等 sibling interpretation 上具有同一 contribution-retention 语义。

各 prey family 可以用完全不同的证据与解释路径，但最终输出必须落到统一 support gauge。

## 6. 与 FoodValue / StateTrigger 的边界

support 回答：

> 当前 presentation 有多强的依据按这类 prey 解释，并以多大比例允许该 interpretation 贡献 Feeding response？

FoodValue 回答：

> 假定已经按该 prey 解释，这条鱼认为它有多值得吃？

StateTrigger 回答：

> 假定按该 prey 解释，当前 prey-state 是否额外容易触发攻击？

因此继续保持：

```text
support
× [FoodValue / Trigger / Costs / Motivation 计算出的 conditional response]
```

而不是：

```text
FoodValue *= support
Trigger *= support
Threshold *= support
```

这样 support 只结算一次，同时约束整个 prey interpretation 的贡献。

## 7. 与动态线索重复计权的护栏

同一 raw motion fact 可以同时参与 prey interpretation 和后续 prey-state evaluation，但必须回答不同问题。

合法例子：

```text
near-bottom crawling pattern
→ 提高 crayfish interpretation support

sudden escape burst
→ 在 crayfish interpretation 已成立的条件下产生 StateTriggerValue
```

不合法例子：

```text
同一次 burst
→ support +0.20
→ 又因为“更像 prey”给 Trigger +0.20
```

如果两条路径实际上都在回答“更像不像这类猎物”，就是重复计权。

Feature admission 仍应检查 distinct question / distinct consequence，而不是只因为字段名不同就允许双路径。

## 8. Typed semantics

```text
NoMatch
→ support = 0
→ C_prey = 0
```

```text
Unknown / NotConfigured required support
→ no scalar support
→ prey mode ResolutionIncomplete
```

Unknown 不能以 `0` 进入乘法。

若 support 为区间，则沿 sibling partial-resolution contract 传播区间，不先取中点。

## 9. 需要的 calibration fixtures

至少保留以下类型：

1. **same conditional, different support**：响应贡献随 support 单调且线性变化；
2. **same support, different prey families**：跨 family 的 support anchor 有可比解释；
3. **full support invariance**：`support=1` 不改变 conditional response；
4. **NoMatch zero**：`support=0` 不产生贡献；
5. **Unknown propagation**：未知不进入 numeric multiplication；
6. **winner swap**：两个 sibling 的 `support × C` 交叉时只发生 winner 切换，不产生额外叠加 mass；
7. **double-count audit**：同一动态 cue 不因“support 提升 + 同义 Trigger”重复增加 response。

## 10. Reopen gate

只有出现以下证据时，才重新引入 `RecognitionProjection(support)`：

- 统一线性 support 标尺无法同时服务多个 prey family；
- 中低 support 系统性高估贡献；
- 高 support 系统性低估贡献；
- authoring 无法直接把 evidence 编译到统一 retention gauge；
- 明确策略故事需要 recognition threshold / saturation，且无法在解释器内部表达。

在此之前：

```text
final support is already calibrated
R = support
C_prey = support × C_conditional
```

是第一版 Working Closure。

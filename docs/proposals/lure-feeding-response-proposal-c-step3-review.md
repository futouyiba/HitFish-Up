# 方案 C 第3步：状态解释原型复核

日期：2026-10-26  
状态：Development Review；不是 Current，不是生产规范。

## 1. 复核结论

第3步独立原型位于：

`prototypes/lure-response/proposal_c_state_interpretation_probe.py`

它实现并编码了方案C正文 §5.9 的 A～P 16个验收向量。当前已完成代码级静态复核；本轮 ChatGPT GitHub 连接环境不能直接执行仓库分支代码，因此这些案例只能表述为 **executable assertions 已编码、待本地/CI实际运行**，不能表述为已运行通过。

当前没有发现需要推翻第3步主体结构的反例。

## 2. Owner 边界

根据当前项目 Contract：

- Step 1 的 fish-agnostic 实际呈现与连续运动事实属于 Presentation Realization / ActualPresentation；
- Step 2～3 的猎物类型解释、类型条件状态属于 Interaction / Target Interpretation 消费侧；
- 因此第3步可以读取 ActualPresentation/history，但其猎物条件结果不能倒灌为 ActualPresentation authority。

原型对应采用两层输出：

1. `facts`：prey-independent 共用事实；
2. `prey`：读取同一事实后的 prey-conditioned interpretation。

类型支持暂时为0时，`facts` 仍持续维护，避免类型重新进入时丢失真实运动前史。

## 3. A～P 覆盖映射

| Case | 核心检查 | 静态复核 |
|---|---|---|
| A | 持续移动 | 已编码 |
| B | 移动后停留，起点与确认时刻分离 | 已编码 |
| C | 近期关系超时但当前停留继续 | 已编码 |
| D | 只有停留前史，移动前史未知 | 已编码 |
| E | 迟滞区间不制造反复切换 | 已编码 |
| F | 下沉 + 姿态缺失 | 已编码 |
| G | 正常姿态下沉 | 已编码 |
| H | 持续侧翻下沉 | 已编码 |
| I | 世界运动与相对水体低运动可并存 | 已编码 |
| J | gap 不制造停留，也不桥接转换 | 已编码 |
| K | prey support=0 时共享运动记忆仍维护 | 已编码 |
| L | 新抛投重置连续段 | 已编码 |
| M | 多猎物解释共用同一事实 | 已编码 |
| N | 复合过程检查顺序与时限 | 已编码 |
| O | 整段/分批输入最终状态一致，重复批次幂等 | 已编码 |
| P | 水面与近底可并存，局部来源换版清理局部事件 | 已编码 |

## 4. 静态复核得到的两个重要语义

### Gap 必须切断需要连续性的状态推断

如果 gap 前已确认 moving，gap 后出现 low-motion 数据，不能直接把两端拼成一次 `moving → pause`。gap 后可以凭足够新数据重新确认当前 low-motion，但跨 gap 的转换关系保持 Unknown。

### “无前史”不是“不匹配”

记录若从停留中途开始，可以确认当前 low-motion，但在没有更早运动记录时，`recent_move_then_pause` 应为 `Unknown`，不是 `NoMatch`。

## 5. 尚未闭合的小型数据契约缺口

方案C §5.7 要求：时长必须说明“精确起点”还是“仅已观测下界”。当前原型的 `Segment` 已预留 `observed_lower_bound` 字段，但尚未真正赋值和输出。

因此 A、D，以及 B 中“此前至少观测到0.60秒移动”的表达目前还不完整。下一次代码修订应补：

- 记录开始时已处于某状态 → 当前段 `duration_is_observed_lower_bound=true`；
- 在完整连续记录中观察到状态转换 → 新段起点可认为已知；
- 已关闭的前一段也保留这一边界信息；
- gap / continuity reset 后重新开始同样遵守该规则。

这属于数据语义完整性，不改变状态判据本身。

## 6. 下一步

在本地或CI实际运行第3步原型，确认 A～P assertions 全部通过；然后补 `observed_lower_bound` 契约并重新运行。

第3步通过后，再进入 Step 4 的窄范围对照：固定同一鱼种与同一 prey support，只改变呈现状态，分别推导食物价值、TaskDemand / 捕获要求、feeding motivation 如何影响鱼侧评价。此时不要提前固定最终聚合公式。

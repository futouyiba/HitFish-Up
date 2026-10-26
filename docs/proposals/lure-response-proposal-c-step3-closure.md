# 方案 C｜Step 3 状态解释 Closure Note

日期：2026-10-26  
状态：Proposal Evidence，不是 Project / Domain Current。

## 结论

Step 3 的首轮状态解释契约已经达到可以进入 Step 4 窄范围推导的程度。

本轮新增 `proposal_c_state_interpretation_probe_v2.py`，补齐 §5.7 要求的时长语义：

- `known_segment_start`：当前分段起点由连续记录中的状态转换确定；
- `observed_lower_bound`：记录开始、gap 后重新观察或新 continuity 开始时，动作可能早于首个可见样本，只能声明“已观测至少持续 X 秒”。

这一区分不改变运动状态本身，只避免把记录边界误写成真实行为起点。

## 实际执行结果

在本轮 ChatGPT 本地 Python 环境中实际执行 closure probe：

```text
Step-3 acceptance passed: A B C D E F G H I J K L M N O P
```

A–P 对应方案 C §5.9 的 16 个验收向量。此次执行不是生产环境验证，也不证明阈值具有生物学标定意义；它只验证当前 proposal 规则在该 reference implementation 中可以一致执行。

## 关键契约确认

1. prey support 与共用运动记忆分离；某类型支持临时为 0，不停止维护实际运动历史。
2. gap 打断需要连续性的计时与跨 gap 事件关系；gap 后必须由新连续记录重新确认当前状态。
3. 新抛投 / 新 continuity 不继承旧段事件。
4. world motion 与 relative-to-water motion 独立保存。
5. 水面与近底不是互斥枚举，可以同时成立。
6. 同一实际呈现可以同时被多个 prey type 条件性解释，但不因此复制 ActualPresentation，也不在本步制造多个响应机会。
7. `recent_move_then_pause`、`burst_then_pause`、`imbalance_like_sinking` 仍是状态 / 过程解释，不是 response bonus。
8. Step 1 的 ActualPresentation truth 属 Presentation Realization；Step 2–3 属 Interaction / Target Interpretation 消费侧。Step 3 结果不得倒灌成 ActualPresentation authority。

## 仍未证明的内容

- 示例阈值（速度、持续时间、3 秒近期窗、roll 角等）仍是 Working Hypothesis；
- 生产采样频率、滤波、允许插值间隔未定；
- Unity / 环境 / 姿态等数据源未接入；
- 完整爬行、逃窜、真实受伤 / 濒死并未建立；
- Step 4 的 food value、capture requirement / task demand、feeding willingness 以及最终 response aggregation 尚未定义。

## 下一步

进入 Step 4 时不要先设计全局公式。先固定一条具体鱼种与一个 prey type，保持 Step 2 类型支持相同，只改变 Step 3 呈现状态，检查鱼侧评价究竟需要哪些变量。

优先对照：

```text
同一鱼种
+ 同一 prey type support
+ 同一基本环境

A. 持续移动
B. 移动后停留
C. 水下下落 / 失衡样下沉

→ 哪些差异改变 TaskDemand / 捕获要求？
→ 哪些差异改变 Feeding Valuation / willingness？
→ 哪些只是解释信息，不需要新增数值自由度？
```

只有能够产生稳定、可解释的 ranking reversal 或玩家策略差异的状态，才值得在 Step 4 获得独立作用。
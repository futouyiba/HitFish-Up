# 活跃度与摄食动机：响应消费设计

> 状态：Candidate / Design Analysis
> 日期：2026-10-31
> 范围：推演 Activity 与 FeedingMotivation 如何分别影响响应。不决定环境如何生成鱼况，不提供生产参数，不覆盖 Proposal C Working Closure 或 Owner 裁定。

## 1. 已有依据与真正缺口

[Issue 161 的 Owner 裁定](https://github.com/futouyiba/HitFish-Up/issues/161#issuecomment-6515133172)明确 Activity 非负、有限、不设语义上界；1.0 不是默认值。该裁定晚于 PR 130 中把 Activity 写成 `[0,1]` 的旧 Working 标尺，因此不能继续拿旧标尺限制生产输入。

本轮读取了以下 Git 对象，而非仅按文件标题推断：

- 提交 `5caf1f119ab6e5a5c595a4ba913e7962aa338ec3` 的 `docs/proposals/lure-response-proposal-c-activity-bake-contract.md`：Activity 只调制 Closing soft cost；旧候选乘数为 `1 + K_activity × (1-A)`。
- 同提交的 `lure-response-proposal-c-feeding-response-working-closure.md` §4–§5：历史五项无权 Margin 和逐 bearing 方案；仅用于版本比较，不作为当前执行顺序。
- 提交 `01807b10ef727c300614de54adcf9da0ef195b0c` 的 `lure-response-proposal-c-fish-condition-mechanisms.md` 与 `lure-response-proposal-c-response-algorithm-v1.md`：已有独立机制草案和响应算法，位于另一个设计版本，不在本工作树复制为 Current。
- 活动对照为 `origin/main` 提交 `ad2ccb5fbd57d46591858c4f7e54783a5c698cc9` 的 `lure-response-proposal-c-response-algorithm-v1.md` 与 `lure-response-proposal-c-evaluation-items.md`：单方向追赶、不模拟 θ 或跨方位平均；Motivation 使用分段门槛。本文不恢复历史 latent-bearing 算法。

真正需要解决的是消费函数的定义域和去重，不是再定义一个总体鱼况分。

## 2. 两个参数各买什么玩法

固定 Food、Trigger、Risk 和 Opportunity：

| 改变 | 应改变什么 | 不应改变什么 |
|---|---|---|
| 降低 Activity | 同一主动追赶任务的 soft cost 更高 | 物理速度尺度、食物价值、全局动机 |
| 提高 Motivation | 更愿意接受既定价值和成本的机会 | 物理能力、猎物身份、空间覆盖 |
| 降低拟饵径向背离速度 | 降低 Closing burden | 自动提高 Motivation 或添加 PauseBonus |

低 Activity、高 Motivation 的鱼可以“想吃但不愿费力追”；高 Activity、低 Motivation 的鱼可以“行动容易但出手要求高”。这两种状态不能压成同一个倍率。

## 3. Activity 旧线性乘数不能直接外推

令 `A ≥ 0`，且 `K_activity > 0`：

```text
h_old(A) = 1 + K_activity × (1-A)
```

当 `A > 1 + 1/K_activity` 时，`h_old < 0`。若仍使用：

```text
ClosingCost = K_close × u_close(θ)^2 × h_old(A)
```

追赶负担就变成负成本，背离速度越高反而越奖励响应。给最终 C 做 clamp 不能修复这个方向错误。

因此，Owner 取消 Activity 上界后，旧乘数必须限定为历史 Working 区间函数，不能无声明地扩展到整个生产输入域。这里不通过截断 Activity 来恢复被否决的上界。

## 4. Activity 消费函数的最低条件

将消费函数记为 `h(A)`，而不是先指定生产函数族。要求：

1. 对所有有限 `A ≥ 0` 有定义，输出有限且非负。
2. 固定其它输入时，A 增加不能使 ClosingCost 增加。
3. `h(1)=1` 只表达参考锚，不表示 A 的上界。
4. `u_close=0` 时 ClosingCost 恒为 0。
5. `InterceptSpeedLimit` 不随 A 改变。
6. 未解析的 A 不回填 1.0；需要该值的求值保持不完整。

一种可检验、尚未获准的扩展候选为：

```text
k ≥ 0
h_trial(A) =
  1 + k × (1-A),        0 ≤ A ≤ 1
  1 / (1+k × (A-1)),    A > 1
```

它保留旧低活跃区间，在 A=1 连续且左右导数均为 `-k`；A>1 后仍为正，不会使追赶变成奖励。`k=0` 时恒为1。

这只是函数族建议，不是上游已批公式。它引入一个必须明确的设计选择：超参考活跃度是否继续降低成本。若没有独立玩法证据，另一候选是在 A≥1 时令 h=1。两者都不限制 Activity 的生产域；它们区别在消费者是否区分超参考状态。

当前不选定生产扩展；已能确定的是旧线性式不得直接外推。进入实现前须由 Activity 消费机制选定函数与版本。

## 5. Motivation 消费门槛，不乘 Food

沿用 Proposal C 的结构：

```text
Margin = FoodValue + StateTriggerValue
            - ClosingCost - RiskCost - T(M)
```

`T(M)` 表示鱼当前需要多强的出手理由，不是物理不可行门。固定旧提交 `5caf1f11` 的历史 Working 对照为：

```text
T_working(M) = 0.70 - 0.60M
```

仅用于历史比较，不是当前默认公式或生产参数。活动对照 `ad2ccb5f` 使用 `M≤0.80` 时 `T=0.60-0.40M`，`M>0.80` 时再减 `0.50(M-0.80)`；这些仍是 Working 参数，不得外推到未声明定义域。本文不覆盖该分段与 tail 方案。

对合法且已解析的 M，仅固定以下消费性质：

- M 越高，T 不增加。
- M 不再乘 FoodValue 或最终 C。
- M 不更改 Activity、InterceptSpeedLimit 或 L。
- Reject 在连续求值前短路；高 M 不能救活 Reject。
- 缺失 M 不等于合法 M=0。

Food 和 Motivation 的区别由结构保留：Food 随目标解释变化，M 是当前鱼况输入。不能因为二者都改变 Margin 就在生产者层合并。

## 6. 联合响应的可证伪判据

所有比较固定目标身份、Food、Trigger、Risk、L、速度参考系和投影版本；只改变指定变量。活动对照采用单方向 Closing 和上游声明的单调投影，不模拟 θ、不跨方位平均，也不混入本目录自己的 sigmoid。历史 `u_close` 只用于旧版反例，不作为当前输入。

| 攻击条件 | 应成立的关系 | 能发现的问题 |
|---|---|---|
| 固定正的径向负担，提高 A | ClosingCost 不增，C 不降 | 活跃度方向反转 |
| 径向负担为0，只改变 A | ClosingCost 均为0，C 不变 | 匿名 Activity 奖励 |
| A 超过旧线性零点 | 成本仍有限且非负 | 负成本奖励 |
| 固定 A，只提高 M | T 不增，C 不降 | 动机被当负向系数 |
| TargetRelation=Reject，提高 A/M | 仍为 typed zero | 软值救活拒绝 |
| 缺少必需 A/M | 不产生可抽样标量 | 默认值掩盖缺失 |
| `u_close ≥ 1` 但无反应窗口依据 | 不额外 hard-zero | 恢复已撤回的追赶门 |
| 复制同一环境 cause 的消费 | 必须在来源检查中阻断或显式解释不同作用 | 同作用重复处罚 |

C 的单调性允许投影饱和后的相等，不要求每次参数变化都产生严格排序。

## 7. Bake 生成仍须独立取证

时段、水温、溶氧可以作为研究候选原因，但不能由本页推出对应的生产曲线、阈值或必需字段。同一水温可以分别影响空间分布与鱼况，前提是解释的是两个不同后果；禁止的是同一后果重复计权，不是禁止同一个原始事实被读取两次。

生产前每条 cause 至少需要明确：输入量和单位、鱼种适用范围、影响哪一个 Condition、证据来源、求值窗口、缺失状态，以及它与其它 cause 是否独立。没有这些证据时，输出状态保持未收口，不用“一切默认正常”伪装成可运行生产链。

本轮确定了消费函数的安全定义域、两类鱼况的不同职责与联合验收条件；没有决定任何新的环境因果映射。

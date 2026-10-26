# Proposal C｜远端对齐与清理审计｜2026-10-26

状态：Working Audit。不是 Current，不改变仓内 Authority。

## 1. 审计基线

本次对齐：

- 最新 `main`：`cd74d363d0478d7c7aecfeb7320ff0419b1b6fd0`
- Proposal C 分支：`docs/lure-response-joint-evaluation`
- 审计开始时分支 head：`511755f016133d6264492103adfc79e087c8c519`
- merge base：`1dbb6ee5f39a0a233e20eb454045b24c51785e1f`

两支已明显分叉：Proposal C 分支相对最新 main `ahead 127 / behind 110`。因此本次不做整分支 rebase，不把分支内容自动晋升为 Current。

## 2. 最新 main 对 Response Authority 的影响

`docs/README.md` 与 `docs/authority-model.md` 在最新 main 上继续要求：

- Git Markdown 是已收口规范的唯一可 diff 权威载体；
- Current 与历史材料分离；
- 未承接到 Git 的外部 Owner/Contract 不能凭引用被当成已迁移 Current。

`fcf-system-map/contracts.json` 最新 main 仍将 `RESPONSE` 指向外部《Behavioral Regime × Largemouth Bass》v8 中层样板，并明确：

- `linked` 只表示登记时读过并匹配；
- 不证明外部源当前 freshness；
- 不表示完整算法已经迁入 Markdown。

因此 Proposal C 当前仍只能是 Working / Candidate。它可以细化 Feeding Decision Resolver，但不能宣称替代现有 Response Current。

## 3. main 过去 110 个提交中与本线相关的变化

从 merge base 到最新 main，变化主要集中在：

- 文档可读性与清理 skill；
- `docs/terminology.md`；
- 环境实体原始条件 schema；
- `fcf-system-map` 的布局、图结构、contracts 与说明。

没有发现新的仓内 Feeding Response 生产公式或新的 Git Markdown Response Current，能够直接 supersede Proposal C 当前 Working 结论。

`fcf-system-map` 仍保持关键边界：Spatial 与 Interaction 是并行 Cause；Response 归 Interaction；系统图只表达模块流向与边界，不表达本轮具体公式。

## 4. 文件级误删检查

从 merge base 到 Proposal C 分支当前状态，Git compare 显示本分支改动为新增文件与 README 增补；没有文件删除。

因此没有发现“误删整个已有文件”的情况。

这不等价于证明正文清理没有语义损失，所以继续检查了 Proposal C 清理前归档与当前正文。

## 5. Proposal C 清理前后检查

清理前完整版本保存在：

`docs/archive/lure-feeding-response-proposal-c-pre-cleanup-2026-10-26.md`

当前主提案：

`docs/proposals/lure-feeding-response-proposal-c.md`

抽查并对照的承重内容包括：

- prey support 不要求归一化，也不是概率；
- Unknown / 未覆盖 / 已知零分开；
- 类型支持、状态解释、鱼侧价值、捕获要求与响应分层；
- 共用运动记忆不随某 prey support=0 被清空；
- gap 不桥接事件；
- 重复输入不重复累计；
- 乱序与同刻冲突作为输入错误；
- 装配变化、新抛投、瞬移与实例变化的 continuity 处理；
- world-relative / water-relative 速度分开；
- surface / near-bottom 可以并存；
- 历史不完整时 duration 只给已观测下界；
- 已用于类型支持的事实不能自动在状态/响应层重复获得同一奖励。

这些承重规则在当前正文中仍可找到。清理前大量探索过程、被替换的旧例、旧参数、早期路径尝试与长解释被移到 archive，属于合理瘦身。

当前没有发现需要把 archive 的探索流水重新恢复到主提案的内容。

## 6. 本轮发现的真正风险

### 6.1 分支陈旧风险

Proposal C 分支落后 main 110 个提交。任何准备合并或晋升 Current 的动作，都必须先做独立 rebase / conflict audit，不能直接按当前分支 merge。

### 6.2 Authority 漏读风险

最新 main 的 `contracts.json` 明确标注 RESPONSE 仍为外部 linked authority。Proposal C 当前的 Working Closure 只能作为 Candidate Delta，不能把“工作上已经闭合”写成“Current 已冻结”。

### 6.3 总文档压缩风险

后续整合 Feeding Response 时，最容易误删的不是公式，而是：

- typed status：`ResolutionIncomplete` 与 resolved zero；
- hard semantic boundary：Reject；
- latent-angle averaging 必须在 per-angle projection 之后；
- support 不是 probability；
- same physical lure 的多 prey interpretation 默认属于 alternative sibling，不是多份独立 opportunity；
- Response 只结算一次，Candidate 只做 `L × C` native retention join；
- Maneuver 当前只有 soft-cost authority，不能恢复成 `u>1 => hard zero`；
- pause 不准重新变成匿名 bonus；
- State Trigger 属 prey+state local value，不修改 fish-global Motivation threshold。

这些内容必须进入新的 Working Closure。

## 7. 当前判断

### 可保留

当前 Proposal C 的最近一轮修改方向总体合理：

- 从“虚构具体鱼点”改为 latent-angle 概率积分；
- 把绝对鱼距从首版 Intercept 中撤出；
- 将折线/逃逸运动拆成正向 prey-state trigger 与负向 capture/prediction consequence；
- 将 State Trigger 限定为小预算、prey-local；
- 将 prey support 保持为非概率解释强度；
- 默认 `C_prey = support × C_conditional`，不另造无证据的非线性 recognition curve；
- alternative prey interpretations 默认 max，不求和、不做概率 union。

### 不能升格

以下仍是 Working Hypothesis / Candidate，不应写成 Current：

- `R = support` 的 production calibration；
- State Trigger 的生产预算；
- TaskCost 的生产函数与参数；
- Response Projection 的 `M0/M1`；
- 各 prey family 的完整 escape-state feature set；
- Feeding 之外其他 response family 的最终 aggregation；
- runtime hot-path representation。

## 8. 下一步

新增一份单一 `Feeding Response Working Closure`，只承接当前仍有效的承重规则、公式拓扑、typed boundaries、已知 OPEN 与 Current/Candidate 边界。

旧 probe 与窄主题文档保留作证据和回归夹具，不把它们全部拼进正文。
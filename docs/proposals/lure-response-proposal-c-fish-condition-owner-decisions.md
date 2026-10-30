# Proposal C｜Fish Condition 七项：Owner 裁定记录（2026-10-30）

状态：Owner Decided（2026-10-30）。Owner 已在 Issue #161 评论中裁定七项；本文保留问题与选项作为记录，执行结果写回鱼况契约与开放决策。

> 下面各节保留裁定前的问题原文与选项，供追溯。当前执行状态以[裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md) 第 3 节、[Fish Condition Production Contract](lure-response-proposal-c-fish-condition-production-contract.md) 与[开放决策](lure-response-proposal-c-open-decisions.md)为准；正文中“尚未 Contract 化”“owner 未指定”等表述属于当时的缺口描述。

基线：`futou-/exciting-payne-95a562`，提交 `9d4ed83e`。裁决原文见[裁决记录](lure-response-proposal-c-fish-condition-rulings-2026-10-30.md)。追踪 Issue：[#161](https://github.com/futouyiba/HitFish-Up/issues/161)。

## 1. 路径 B 是否正式 Contract 化

现状：裁决采用「Bake 基线 + 受限运行时更新」，当前只有 Wariness 有累积依据；路径 B 尚未 Contract 化。

- A. 接受路径 B，写入 Fish Condition 契约：Bake 出基线，运行时只更新机制授权维度。
- B. 回到 bake-only：需要同时处理 Wariness「随过程累积变化」的语义冲突。
- C. 维持 Candidate，不 Contract 化；第一版只做 Bake 基线。

影响：A 需要后续补 Wariness 机制；B 需要改术语或说明 Wariness 的累积只发生在 Bake 内部。

## 2. Wariness 累积的 owner

现状：裁决只定「归 Fish Condition / 动态机制」，没有指定 owner。

- A. 指定现有鱼况 / Bake 线承接，并命名具体职责线。
- B. 新设独立机制 owner。
- C. 维持待指定，第一版不实现累积。

影响：没有 owner 时，Wariness 只能作为 Bake 基线，真实警戒玩法无法闭合。

## 3. 过期状态协议

现状：裁决建议过期、越界或缺来源转 `Unknown`，但未正式确认。

- A. 采用：过期即 `Unknown`，不允许沿用最后值。
- B. 允许沿用最后值，但标记 `stale`，由消费者决定。
- C. 其它协议。

影响：A 最安全；B 需要每个消费者处理 `stale`，容易与「Unknown 不等于零」重复。

## 4. Activity 是否需要生产上界

现状：裁决不设上界，也不新增 runtime cap；只保留非负与 Working 1.0。

- A. 维持：不设上界。
- B. 设生产上界，并给出来源与稳定性理由。
- C. 先只做分档占位，不讨论上界。

## 5. `TackleConspicuousness` 的字段与 owner

现状：方向已定，字段、数据 owner 与 schema 未定；实现前 `RiskCost=0`。

- A. 指定 owner 并立项最小字段：线径 / 前导 / 钩与连接件等已声明事实，派生可见 / 侵入程度。
- B. 暂不投入，继续 `RiskCost=0`，接受 Wariness 暂无真实消费方。
- C. 只做静态装备代理，不做呈现级耦合。

若选 A 或 C，请给出最小事实清单与可接受来源。

## 6. DEF 中 Fish Condition 的载体

现状：只有候选粒度 `ConditionGroup × Mode`，没有字段、版本或有效区间载体。

- A. 在 DEF 条件组下增加 Fish Condition 字段：值、来源、版本、有效区间、状态。
- B. 独立 Fish Condition 表，按条件组与模式关联。
- C. 暂不定，第一版只用内存占位。

## 7. 四个 Condition 的生成来源与审核职责

现状：生成公式、上游数据来源与审核职责均为缺口。

- A. 归 Bake 线统一生成与审核。
- B. 每个 Condition 各自归属，另立文档。
- C. 暂不指定，只保留占位与 `Unknown`。

## 8. 输出格式

每项给出：

```text
裁定：A / B / C
依据：
作用域：
重开条件：
影响文件或字段：
```

最后给一张总表：项目 | 裁定 | 是否阻塞第一版 | 需要谁执行。

## 9. 约束

- 不把裁决记录写成 Owner 批；
- 不给生产数值；
- 不为方便实现新增机制；
- 所有选择都要能落回现有文档或明确标为缺口。

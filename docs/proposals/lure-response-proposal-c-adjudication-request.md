# Proposal C｜第一轮玩法闭合：裁定请求

状态：Decision Record。本文是 2026-10-30 提交的问题单，五项已由 Owner 在 [Issue #152](https://github.com/futouyiba/HitFish-Up/issues/152) 裁定；保留作来源记录，不再作为待办。

基线：`futou-/exciting-payne-95a562`，提交 `3b7b2332`。追踪 Issue：[#152](https://github.com/futouyiba/HitFish-Up/issues/152)。

## 1. 请求

请只依据本文与链接的仓内文档作判断，不从旧对话、记忆或标题补造规则。

每条裁定给出：结论、依据、作用域、重开条件、影响的文档或字段；没有把握时写“不足以判断，缺 X”。

## 2. 已闭合，不要重开

1. 第一版主体是五项加性出手余量：食物价值 + 攻击诱因 - 追赶负担 - 风险顾虑 - 摄食意愿门槛。
2. Prediction 不在第一版主体；只有独立策略价值证据才重开。
3. Activity 只调制追赶负担，不改物理速度能力；与摄食动机正交。
4. Closing 只解释水平径向分离；`u_close >= 1` 不 hard-zero；垂直运动归 Opportunity。
5. 机会接入是 `q = L × C`，只乘一次；`L` 由 Spatial / Opportunity 提供；Response 不建 ExposureRate。
6. `Reject` 是 typed hard zero；`Unknown`、`NotConfigured`、`NoMatch`、`ResolutionIncomplete` 分开。
7. 攻击诱因第一版只准入 Escape-like；Injured / Struggling 与 imbalance-like vulnerability 是 `CandidateUnresolved`；pause 本身不得作为 Trigger。
8. sibling 用有界部分解析：区间收敛才输出标量。
9. 投影 Working：`M0=0`、`M1=0.40`；动机门槛：`M<=0.8` 时 `0.60-0.40M`，`M>0.8` 再减 `0.50(M-0.8)`。
10. Risk 当前没有生产输入，`RiskCost` 退化为 0；不补造代理字段。

## 3. 事实与 probe 结果

不是生产标定。

- 仓内无 tackle / entry / pose 运行时字段；Fixed Bake 参考实现排除 Response / Presentation，且它消费的 `time_period_activity_coefficient` 不是 Fish Condition 的 Activity。
- 冻结验证基线只有 `cue.contact_disturbance`（限定 moving contact with world geometry）与 `sound_amplitude` 瞬态；术语表只有「线透明度 / 线颜色」作为派生条件的语义，没有字段。
- 策略 probe（Working：`K_close=0.76`、`TriggerBudget=0.10`、`K_wary=1.0`）：
  - Case A：Activity 倍率 0.8→1.6，快搜响应从 0.509 降到 0.466（约 8.5%）；`K_close` 0.50~1.00 下快/慢比值 0.75~0.77。
  - Case B：高 Motivation 普通口 0.991；低 Motivation 0.324；合法 Trigger 拉回 0.574；高速反应口 0.419。
  - Case C：高警戒把直接方案压到 0，隐蔽保留 0.47；低警戒时隐蔽也更高，因为 probe 没给隐蔽建模成本。
- 机会量玩具模型（`L=D/(D+q)`、`R=q/(1+q/Q_cap)`、`D=0.8`、`Q_cap=1.0`）：
  - 高活性最优 `q≈0.49`，低活性 `≈0.39`；方向正确但幅度小。
  - 所有 Activity 下快速都不如中等速度：该模型没有买出快搜。
  - 隐蔽 `coverage=0.55` 时，低警戒直接占优（0.089 vs 0.058），高警戒隐蔽占优（0.043 vs 0）。

## 4. 当时待裁定（已由 #152 裁定）

### 4.1 探索 / 信息覆盖收益是否立项

现状：快搜的真实收益是单位时间覆盖更多水体、更快收敛鱼位判断，不在单次响应；塞进 `C` 或单颗粒 `L` 都会算错。

- A. 不立项：快搜只作为搜索效率，不进入 Response 或 Candidate 的任何数值路径。
- B. 立项为 Opportunity 侧的独立信息收益项，只回答“单位时间找到更多有效条件”，不改 `C`。
- C. 先 playtest / 录制数据，不设计机制。

请回答：选哪个；若 B，最小可测形式、owner、拒绝条件是什么。

### 4.2 Risk MVP 是否给字段和 owner

现状：`TackleConspicuousness` 与 `EntryDisturbance` 都没有生产输入。

- A. 不立项：第一版 `RiskCost=0`，保留接口。
- B. 只立项 `EntryDisturbance`：用 sound / contact 线索与时间窗。
- C. 只立项 `TackleConspicuousness`：需要装备 / 线组字段。
- D. 两者都立项。

若立项，请给出最小 cue 定义、可接受的数据来源、防重复计权判据（fishing pressure 不得二次进入 `SuspicionLoad`；`visual_contrast` 已吸收的视觉原因不得再读 `context.light`）。

### 4.3 CapacityModifier 的去留

现状：列为 optional Candidate；没有独立消费需求或失败案例。

- A. 保持 optional；
- B. 提升为 Fish Condition；
- C. 删除。

请给出触发重开的证据条件。

### 4.4 Prediction 的重开条件

现状：第一版不含。请确认该立场，并写清什么证据才算“独立策略价值”。

### 4.5 `L` 的正式 owner

现状：Proposal C 只定义 seam；`L` 由 Spatial / Opportunity 提供，但仓内没有正式 Current Owner。

- A. 沿用现有 Opportunity / Spatial owner；
- B. 新设 owner；
- C. 保持 seam，不指定，直到有生产需求。

请说明对 `q = L × C` 的影响。

## 5. 输出格式

对每个 4.x：

```text
裁定：
依据：
作用域：
重开条件：
不确定性：
```

最后给一张总表：项目 | 裁定 | 是否阻塞第一版 | 需要谁执行。

## 6. 约束

- 不把 Candidate 写成 Current，不给生产数值。
- 不因为“现实里可能有”就新增机制。
- 不合并 PR，不改仓库。
- 所有建议必须能落回现有文档，或明确标为缺口。

## 7. 相关文件

- [设计骨架](lure-response-proposal-c-design-spine.md)
- [语义契约](lure-response-proposal-c-semantic-contract.md)
- [呈现解释与状态契约](lure-response-proposal-c-presentation-interpretation.md)
- [五评价项契约](lure-response-proposal-c-evaluation-items.md)
- [响应与机会契约](lure-response-proposal-c-response-opportunity.md)
- [第一轮玩法闭合审查](lure-response-proposal-c-first-round-closure.md)
- [Escape-like Trigger v1](lure-response-proposal-c-escape-trigger-v1.md)
- [机会量支持](lure-response-proposal-c-opportunity-support.md)
- [工作案例](lure-response-proposal-c-worked-cases.md)
- [开放决策](lure-response-proposal-c-open-decisions.md)
- [策略 probe](../../prototypes/lure-response/proposal_c_strategy_probe.py)
- [逃逸触发 probe](../../prototypes/lure-response/proposal_c_escape_trigger_probe.py)
- [机会量 probe](../../prototypes/lure-response/proposal_c_opportunity_support_probe.py)

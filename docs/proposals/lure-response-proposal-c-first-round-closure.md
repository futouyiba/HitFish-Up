# Proposal C｜第一轮玩法闭合审查

状态：Working Review / Candidate。不是 Current Contract，不是生产参数。本文回答“当前机制能否买出目标玩法”，不扩展新机制。

## 1. 范围与判据

本轮只做四件事：AttackTrigger 准入、Risk MVP 输入实证、三个策略排序 probe、机制与标定的判断。

所有数值标为 Working / Probe。判定依据：

- 玩家能否用可理解的操作制造该状态；
- 系统当前是否有实际事实识别它；
- 它是否被 FoodValue / Closing / Risk / Prediction（若启用）已有的路径解释；
- 它是否带来自然代价、是否重复计权；
- 当前数据与配置是否足够生产。

## 2. A. AttackTrigger 第一版准入

| 候选 | 玩家操作 | 当前可识别事实 | 独立性 | 自然代价 | 重复计权风险 | 数据充分性 | 建议 |
|---|---|---|---|---|---|---|---|
| Escape-like / 逃逸样 | 抽停、急抽、darting / slashing | 轨迹转向强度、burst 强度；经 prey-conditioned interpreter 判断 | 是：FoodValue 回答值不值得吃，Closing 回答难不难追，都不回答“现在是否触发攻击” | 速度上升 → 追赶负担；强动作 → 风险顾虑（若 cue 存在）；局部窗口可能缩短 | 中：burst 速度同时进入 Closing 是不同问题，允许；但不能再加 erratic bonus | 轨迹事实在设计层可用；无生产采集 | **准入（唯一）** |
| Injured / Struggling / 受伤挣扎样 | 慢速翻滚、失稳下沉、濒死抖动 | 需要侧翻角、持续失衡、局部动作；也可来自 prey-conditioned 的 struggle 序列（如蛙类踢水） | 概念上独立，但缺生产闭合的识别映射 | 慢速通常降低追赶负担；长时间停留抬高机会量 | 若用航迹不规则替代姿态，会与 prey support / prediction 重复 | 无生产闭合的 struggle / vulnerability 输入映射 | **CandidateUnresolved**，等 cue-only holdout；不是仅因缺姿态字段否决 |
| Vulnerable Pause / 虚弱停顿样 | burst 后停顿 | 位移分段可识别停顿 | pause 本身不成立：已由 attention / temporal / prediction 承接 | 没有独立代价；收益已在机会量中 | 高：把 `burst → pause` 再算 Trigger 会与 temporal support 重复 | 分段可用，但 pause 语义重复；imbalance-like vulnerability 另属未决候选 | **pause 本身不得作为 Trigger**；imbalance-like vulnerability 保持 **CandidateUnresolved** |

### 为什么只留 Escape-like

- 它有独立策略价值：低摄食意愿时，普通呈现过不了线，合法逃逸样呈现可能跨线；
- 它可低成本识别：转向与 burst 来自轨迹，不需要新硬件输入；
- 它不能被已有项替代：Closing 只说“难追”，Risk 只说“可疑”，FoodValue 只说“值不值得吃”。

其余两项不是被否决，而是仍未闭合：

- Injured / Struggling 与 imbalance-like vulnerability 在 joint 来源中都是 `CandidateUnresolved`，需要 cue-only holdout（控制物理轨迹、capture geometry、prey support、Perception、TaskDemand、dwell、Motivation，只改可感知的 vulnerability cue）；本仓目前没有生产闭合的输入映射。
- pause 本身不单独进入 Trigger；这不等于否定 vulnerability 候选。

### 第一版边界

```text
TriggerIntensity_p ∈ [0,1]
StateTriggerValue_p = 0.10 × TriggerIntensity_p
```

- 只按 prey interpretation 解释后的状态计算；
- 不允许 `a × turn + b × burst + c × event_count`；
- 不允许 pause 进入 Trigger；
- 领地、护巢、烦躁不进入 Feeding。

## 3. B. Risk MVP 输入实证

对照仓内实际内容：

| 风险语义 | 当前配置 / 字段 | 数据来源 | 分类 | 第一版建议 |
|---|---|---|---|---|
| TackleConspicuousness | `TackleConspicuousness` 只存在于 Proposal C 文档；术语表把「线透明度、线颜色」列为派生条件，没有字段或 schema | 语义 | 缺失（语义已有，产物缺） | 不启用；等 owner 与字段 |
| EntryDisturbance | 冻结验证基线有 `cue.contact_disturbance`（限定为 moving contact with world geometry，按 cause / motion / duration 分轴）与 `sound_amplitude` 瞬态；holdout 把入水 splash 映射为 sound spike + apparent_size 瞬态 | baseline 线索 | 存在可复用底层 cue 线索，尚不能推出 EntryDisturbance 生产量 | 不启用；不拿「刚抛投」冒充风险 |
| Wariness | 术语表与鱼况定义存在；无 runtime 产出字段 | 语义 | 缺失 | 不生产 |
| Activity / FeedingMotivation / DietShift | 同上，有语义，无运行时 schema | 语义 | 缺失 | 不生产 |
| 装配 / 呈现 | 只有 Proposal C 文档与 5 个 probe；probe 输入为手填特征 | prototype | 仅设计层 | 不当作生产输入 |
| Fixed Bake 参考实现 | `reference/0340-fixed-bake/` 明确排除 Response / Presentation，并消费的是 `time_period_activity_coefficient`（环境查表键），不是 Fish Condition 的 Activity | 参考实现 | 不覆盖 | 不能作为 Response 输入 |

补充核对：

- `cue.visual_contrast` 已吸收的视觉原因，Response 不能再读 `context.light` 做第二次视觉加权（baseline R2 规则）；
- R3 基线禁止 raw rig identity / SKU / Technique ID / source_count / lure_count 进入呈现事实，因此不能用饵型号冒充 conspicuousness；
- 没有其它字段表达同一语义；
- `SuspicionLoad` 不应由 `1 - prey_support`、高速、高频转向生成；
- fishing pressure 若已提高 Wariness，不再进入 `SuspicionLoad`。

### 结论

Risk MVP 当前只能实现退化路径：

```text
无已解析 cue → SuspicionLoad = 0 → RiskCost = 0
```

这不是“风险机制已可用”，而是“没有输入时不处罚”。第一版要么保留接口并明确不生产 RiskCost，要么等 cue owner 落地；本轮不补造代理字段（例如用饵体积冒充 conspicuousness，或把入水动作直接当 EntryDisturbance）。

## 4. C. 三个策略排序 Probe

可执行入口：`prototypes/lure-response/proposal_c_strategy_probe.py`。

方法：720 个 latent bearing；每个 bearing 先算成本与 Margin，再投影，最后平均；`M0=0 / M1=0.40`，`K_close=0.76`，`TriggerBudget=0.10`，`K_wary=1.0`（probe 值）。support 固定为 1，不模拟机会量与覆盖。

### Case A：快搜 vs 慢速 finesse

| Activity 倍率 | q=0.45（慢） | q=0.90（快） |
|---|---|---|
| 0.8 | 0.673 | 0.509 |
| 1.0 | 0.654 | 0.493 |
| 1.3 | 0.625 | 0.477 |
| 1.6 | 0.596 | 0.466 |

- `ClosingLoad ≈ 0` 时，Activity 0.8 与 1.6 的响应完全相同（0.750），低 Activity 未凭空降分；
- 快搜仍有非零响应，但与慢速差距稳定在约 0.75 倍；
- **Activity 从 0.8 升到 1.6，快搜只从 0.509 降到 0.466（约 8.5%）**，没有出现“明显恶化”。

原因不是 `K_close` 太小：`K_close` 从 0.50 到 1.00，快/慢比值稳定在 0.75–0.77。原因是水平径向成本只作用于一半方位，且有利方位的响应已饱和。要让“不适合追时高速明显恶化”，需要机会量 `L`（覆盖与有效窗口）或更高的成本结构参与，Response 单独做不到。

### Case B：普通口 vs 反应口

| Motivation | 普通（T=0, q=0.4） | 反应口（T=0.10, q=0.4） | 反应口高速（T=0.10, q=0.9） |
|---|---|---|---|
| 0.9 | 0.991 | 1.000 | 0.798 |
| 0.5 | 0.624 | 0.874 | 0.646 |
| 0.2 | 0.324 | 0.574 | 0.419 |

- 高 Motivation 时普通优质呈现已接近满响应；
- 低 Motivation 时普通口明显变弱（0.324）；
- 合法 Trigger 能把边缘机会拉回（0.574），但高速反应口掉到 0.419，低于中速反应口；
- 反应口没有超过高 Motivation 的普通口（0.574 < 0.991），不是固定最优；
- 代价来自追赶负担，没有新增匿名刺激惩罚。

### Case C：直接 vs 隐蔽

| Wariness | 直接（E=0.50） | 隐蔽（E=0.10） |
|---|---|---|
| 0.1 | 0.549 | 0.649 |
| 0.2 | 0.424 | 0.624 |
| 0.4 | 0.179 | 0.574 |
| 0.6 | 0.000 | 0.524 |
| 0.8 | 0.000 | 0.474 |

- 低警戒时直接方案仍可用（0.549 > 0）；
- 高警戒时同一暴露把直接方案压到 0，隐蔽方案仍保留 0.47；
- **但隐蔽方案在低警戒时也更高（0.649 > 0.549）**，因为本 probe 没有给隐蔽方案建模任何代价。真实交换必须来自 Response 之外：更窄的猎物匹配、更大的覆盖损失或更慢的搜索。否则隐蔽是固定最优。

### 敏感度

| 参数 | 观察 |
|---|---|
| `M1` 0.30 / 0.40 / 0.50 | 同一 Margin 下响应从 1.00 / 0.75 / 0.60，变化最大；选项间排序不变 |
| `K_close` 0.50 / 0.76 / 1.00 | 在本 probe fixture（`food=0.70`、`activity=1.0`、`M=0.5`）下，快/慢比值 0.77 / 0.75 / 0.76；只改水平，不改该 fixture 的排序，不能外推为普遍性质 |
| Trigger budget 0.05 / 0.10 / 0.15 | 低 Motivation 反应口从 0.449 / 0.574 / 0.699，直接决定反应口能否跨线 |

### Probe 限制

- 不模拟机会量 `L`、覆盖收益或隐蔽方案成本；
- support 固定为 1，不检查 support 与响应的交互；
- 不是生产标定，只证明机制在给定 Working 值下的排序能力。

## 5. D. 判断

### 5.1 五评价项是否足够产生四类策略差异

部分足够：

| 策略 | Response 内是否成立 | 备注 |
|---|---|---|
| 食物价值（选什么） | 是 | 通过与 lower-value 目标的 Margin 差直接体现 |
| 摄食动机（普通口 / 反应口） | 是 | Case B 成立，Trigger 有边界 |
| 追赶（快搜 / 慢速） | 只成立一半 | Response 只惩罚快搜约 8.5%；覆盖收益与完整恶化需要机会侧 |
| 警戒（直接 / 隐蔽） | 只成立一半 | 直接会被压到 0，但隐蔽没有内建成本，需要外部代价 |

### 5.2 机制缺口

1. **Closing 的角度平均削弱高速惩罚**：一半方位成本为零、有利方位响应饱和。这不是调 `K_close` 能解决的。
2. **Risk 没有输入**：TackleConspicuousness 与 EntryDisturbance 在仓内都没有字段，MVP 只能输出零。
3. **Injured / Struggling 没有生产闭合的输入映射**：不是单一姿态字段缺失，也没有可用的 cue-only 识别证据；不能用航迹不规则冒充。
4. **Vulnerable Pause 与时间机会重复**：pause 本身不能作为 Trigger；imbalance-like vulnerability 仍是 `CandidateUnresolved`，需要 cue-only holdout。

### 5.3 只是标定问题

- `M1` 决定绝对响应水平；
- Trigger budget 决定反应口能否跨线；
- `K_wary` 决定警戒翻转位置；
- `K_close` 只改变水平，不改变快/慢排序。

### 5.4 CapacityModifier

本轮没有找到独立消费需求或失败案例。维持 optional Candidate，不引入。

### 5.5 Prediction

维持“第一版主体不含”。重开条件：控制 Trigger / Closing / Risk 后，Prediction 仍产生稳定、独立、玩家可学习的排序差异。

## 6. E. 文档联动

本轮只改动被结果影响的 Candidate / alignment 文档：

- `lure-response-proposal-c-open-decisions.md`：更新 AttackTrigger、Risk、Prediction 的当前状态；
- `lure-response-proposal-c-evaluation-items.md`：AttackTrigger 收窄为 Escape-like；Risk 标注当前无输入；
- 会议稿只保留对齐结论，不加入 support 插值、状态阈值和 sweep 表。

## 7. 事实与判断的分界

| 类型 | 内容 |
|---|---|
| 事实 | 仓内无 tackle / entry / pose 运行时字段；Fixed Bake 参考实现不含 Response；probe 输出如本页表格 |
| Candidate 判断 | 只准入 Escape-like；Risk MVP 退化为零；快搜与隐蔽需要外部代价 |
| Working 参数 | `M0/M1`、`K_close`、Trigger budget、`K_wary`、tail 参数 |
| 仍缺证据 | 真实玩家能否稳定制造逃逸样；姿态输入能否落地；机会量 `L` 的覆盖函数；隐蔽方案的实际成本 |

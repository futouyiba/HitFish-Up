# Feeding Event｜一次摄食事件 Candidate

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 权威边界：本页把一次摄食机会拆成可审的机制步骤，不定义 FCF Current Contract、最终 Response 公式或生产概率。

## 1. 事件从哪里开始

`Feeding Event` 是本目录的 Candidate-local 工作词。它不是“配方得分”，而是鱼在某个地点、某个时间对一个实体对象形成的一次处理机会。

事件必须从已有 `Feeding Place State` 开始，而不是从静态配方比例开始：

```text
Feeding Place State(place, t)
  → encounter opportunity
  → feasible action set
  → selected action
  → attempted action
  → capture / retention
  → handling
  → ingestion outcome
```

如果对象没有进入鱼能接触的地点和状态，后面的尺寸和摄食动作都不应凭空产生结果。

## 2. 四个顺序问题

### 2.1 是否形成遇见机会

`Encounter` 处理鱼是否可能在当前地点、时间和线索场中发现或接近对象。它可以读取：

- Feeding Place 的空间位置、水层和对象可接触状态；
- Chemical Cue Field 的暴露；
- 当前 Fish Condition 的 Activity、Feeding Motivation、Wariness；
- 当前 Response Condition / Presentation Signal 的相关输入。

它不应读取对象尺寸来直接宣布对象“更吸引”，也不应把尺寸成功提前算进发现概率。

### 2.2 哪些动作可行

给定已遇见的对象，形成可行路径集合：

```text
F(f, o, p, t) = {m | feasibility_m(f, o, p, t) > 0}
```

可行性读取：

- 鱼的 Body Linear Size / Morphology；
- Feeding Action 的固有能力；
- 当前地点、水层、底质、流态等动作前提；
- 对象的 effective_size、shape、hardness、cohesion、release_state。

`BENTHIC_SUCTION` 的底层前提属于这里；不能再把“底层”塞进同一条尺寸曲线重复计算。

### 2.3 在可行路径中选择动作

如果 `F` 为空，事件不能进入动作成功。若 `F` 不为空，鱼可能：

- 在唯一可行路径上尝试；
- 在多个路径中按策略选择；
- 受到 Fish Condition、对象 Food Identity、Chemical Cue、警戒和动作代价影响。

本页不先决定确定性 `argmax`、随机选择或其它策略。选择概率必须只在可行集合 `F` 内归一化：

```text
Σ_{m ∈ F} P(select m | F, f, o, p, t) = 1
```

不可行路径的选择概率为 `0`。

### 2.4 所选动作能否成功处理对象

动作成功是条件在所选路径上的结果，不等于鱼已经遇见对象：

```text
success_m
  → capture / retain
  → handle
  → ingest
```

尺寸、形状、硬度、团聚状态可以影响这些环节。先把它们命名分开，再决定是否需要独立概率；不能用一条“最佳粒径曲线”同时解释所有失败原因。

## 3. 候选概率分解

以下只作为 Candidate 的逻辑分解，不是已确认公式：

```text
P(effective ingestion | f, o, p, t)
  = P(encounter | f, o, p, t)
  × [F ≠ ∅]
  × Σ_{m ∈ F}
      P(select m | F, f, o, p, t)
      × P(success_m | f, o, p, t)
      × P(handle_and_ingest | success_m, f, o, p, t)
```

为避免把尺寸曲线误当成最终结果，尺寸模型只提供成功链中的一个因子：

```text
size_condition_m
  ⊂ P(success_m | f, o, p, t)
```

在需要表达对象价值时再显式乘上：

```text
expected_ingested_value
  = P(effective ingestion) × value(o)
```

`value(o)` 的单位尚未收口，可以是质量、数量、能量或其它明确声明的价值空间；不能默认为“分”。

## 4. 路径量的职责

| 路径量 | 回答的问题 | 主要输入 | 不负责 |
|---|---|---|---|
| `encounter` | 鱼有没有机会遇到对象 | Place、Cue、Fish Condition | 颗粒处理成功 |
| `feasibility_m` | 动作 m 在当前条件下能不能做 | Fish、Place、Object State | 鱼最终是否选择 |
| `selection_m` | 已可行动作中选哪条 | Fish Condition、Food/Cue、动作代价 | 改变动作固有能力 |
| `success_m` | 所选动作能否捕获/保留/处理 | Action、Object、Fish、Place | 发现对象 |
| `handle_and_ingest` | 成功后是否产生有效摄食 | Object value、状态、鱼况 | 改变线索场 |
| `Effective Ingestion Opportunity` | 一次事件能贡献多少有效机会 | 上述结果 | 直接等于 AdaptationCoeff |

## 5. Edible Size Response 的位置

尺寸响应不再作为一条独立的最终 `EdibleSizeFit` 分数，而是动作路径中的对象约束：

```text
Fish morphology + action capacity
        +
Object effective_size / shape / state
        ↓
feasibility_m and success_m
        ↓
Feeding Event
```

如果为了实现需要使用相对尺寸曲线，它必须被声明为 `size_condition_m` 的近似函数，并保留：

- 适用的动作路径；
- 需要哪些对象状态；
- 哪些地点前提已经在外部处理；
- 它不能解释哪些结果。

`max(path)` 只在“动作总能自由切换、没有选择成本、没有竞争”的简化假设下成为上界。它不应作为默认机制公式，更不应和多个路径直接求和。

## 6. 失败与对象状态

一次事件失败不等于对象消失，也不等于可以在同一事件内免费换动作重试：

| 结果 | 对象状态 | 下一步 |
|---|---|---|
| 未遇见 | 不变 | 等待下一次机会 |
| 无可行动作 | 通常不变 | 下一次机会或离开 / 转态 |
| 动作失败 | 可能不变、受扰动或部分改变 | 由状态转换决定 |
| 部分摄食 | 剩余对象减少或状态改变 | 下一次机会处理剩余部分 |
| 成功摄食 | 对象价值减少 / 对象移除 | 更新 Feeding Place State |
| 成功但未吞下 | 对象可能脱落或受损 | 不能当作完整摄食 |

具体状态更新仍是 OPEN，但“成功后仍保留完整对象价值”不能作为默认。

## 7. 三条硬边界

1. 尺寸不直接决定 encounter、Food Preference 或最终 Response。
2. Chemical Cue 不直接改变对象的尺寸成功；它影响发现、趋近、选择或回避。
3. 一个对象的一次事件只有一条实际动作路径；复制机制、复制路径或复制 Ingredient ID 不能凭空增加结果。

## 8. 最小反例

- **不可行路径**：鱼具备 PICK 能力，但当前对象在底层且 PICK 前提不成立；该路径贡献为零。
- **重复路径**：同一 GULP 路径复制一次，选择集合没有新增语义，结果不得改变。
- **分层隔离**：只改变对象尺寸，不应直接改变 Cue Exposure；只改变 Cue，不应直接改变 size condition。
- **失败状态**：动作失败后对象仍在地点，不能在同一事件内免费再走第二条动作路径。
- **来源拆分**：同一 Ingredient 贡献 Food、Cue 和物理属性，三条路径都可存在，但不能末端合并成一条总分。

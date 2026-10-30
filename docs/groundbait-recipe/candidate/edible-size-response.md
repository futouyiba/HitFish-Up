# Edible Size Response｜可摄食尺寸响应 Candidate

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 权威边界：本页只定义 Feeding Event 中“对象约束如何影响动作路径”的候选接口，不定义独立的最终尺寸分、Response 或生产参数。

## 1. 作用范围

粒径不是鱼的偏好，也不是一个独立 Bonus。它只回答：

> 给定对象已经进入接触机会后，某条摄食动作能否捕获、保留、处理这个对象？

对象是否出现、是否被发现、是否位于该动作可用的水层，由 `Feeding Place State` 和 `Physical Release` 负责。一次事件如何选择动作、如何更新对象状态，由 `feeding-event.md` 负责。

```text
Fish body / morphology + action capacity
        +
ParticleObject effective_size / shape / state
        ↓
feasibility_m / success_m 的尺寸相关部分
```

输入和输出的边界：

- 输入只包含 `Edible Particle Distribution`，即当前地点可接触的可食颗粒。载体、黏结料、泥和不提供营养的颗粒不进入本页。
- 输出是 `EdibleUtilization`，表示可食颗粒中被有效利用的份额。
- 输出不是 Attraction、Retention、Bite Bonus、饱腹或最终 Response。
- Groundbait 与 Hookbait 共享的只是这个鱼侧尺寸约束接口，不共享完整的 Feeding Place、释放或响应机制。

## 2. Fish body 与 action capacity

- `Body Linear Size` 描述个体成长带来的尺度变化。
- `Morphology Profile` 描述同一体尺下口部、过滤结构或身体形态差异。
- 两者共同约束 Feeding Action 的能力范围，但不直接给出“最佳颗粒”。

普通口部路径可以使用线性参考尺度：

```text
reference_size = body_linear_size × morphology_scale
```

这只是生成动作能力坐标的一种候选映射，不是 Runtime 真理，也不是“颗粒小于嘴宽乘常数”的万能公式。重量可以帮助推断体尺或成长阶段，但不能直接与无量纲 Ratio 相乘生成长度。

`FILTER` 可能没有同样的口部参考。它可以由过滤结构、悬浮状态和流量直接提供自己的截留 / 保留约束；不能强行套普通 Mouth Reference。

## 3. Feeding Mechanism 是动作路径

PICK、SUCTION、BENTHIC_SUCTION、GULP、FILTER 不是同一条曲线的倍率，而是不同的动作路径。每条路径要分别说明：

- 动作前提；
- 对象如何被捕获；
- 对细小对象如何保留和处理；
- 对过大对象的入口、吸入或吞咽限制；
- 对水层、底质、流态的依赖。

例如 `BENTHIC_SUCTION` 的“底层”属于动作可行性的地点前提，不属于尺寸本身；否则会把地点约束重复计入尺寸约束。

### 3.1 尺寸约束接口

每条动作路径可以提供尺寸相关的条件项：

```text
size_condition_m(
  effective_size,
  fish_morphology,
  object_state
)
```

它表示对象尺寸、形态与状态如何影响动作 `m` 的捕获、保留和处理。它不是一条必须具有“上升、平台、下降”形状的最终曲线。若实现采用相对尺寸曲线，也必须说明：

- 它只服务哪条动作路径；
- 哪些地点前提已在外部处理；
- 哪些对象状态会改变结果；
- 它不能解释 encounter、Food Preference 或最终 Response。

## 4. 多动作由 Feeding Event 处理

一条鱼可能有多个动作路径。它们是处理同一对象的备选路径，不是多个独立奖励：

```text
Feasible Action Set
        ↓
Action Selection
        ↓
One Attempt
        ↓
Action Success
```

因此本页不再定义 `EdibleSizeFit = max(...)`。`max` 只能在“动作总能自由切换、没有选择成本和竞争”的强假设下作为上界。实际路径选择、可行性、动作成功和失败状态见 `feeding-event.md`。

## 5. 对象状态不是尺寸值

同一有效尺寸的对象，仍可能因状态不同而产生不同动作结果：

- `shape`：影响捕获、入口和保留；
- `hardness`：影响处理和吞咽；
- `cohesion`：影响团聚、解体和一次事件可处理的对象边界；
- `release_state`：影响当前是否仍是可处理实体。

这些属性不能静默编码进 `effective_size`。如果它们影响物理释放，也必须通过 `Feeding Place State` 进入；如果影响动作成功，则通过 `success_m` 的对象约束进入。

## 6. Groundbait 与 Hookbait 的复用边界

Groundbait 输入是随地点和时间变化的对象分布；Hookbait 通常是单对象或小分布。两者可以共用：

```text
fish morphology + action capacity + object constraints
```

但 Hookbait 还要经过入口性、钩体阻碍、持钩、姿态和被识别等约束。复用的是对象约束接口，不是 Groundbait 的完整响应。

## 7. 当前状态

### 事实 / 结构性边界

- 线性体尺与无量纲比例相乘才得到线性尺寸；
- 不同摄食动作不能默认视为同一动作的倍率；
- 一个对象的一次摄食机会不能通过动作数量重复计奖；
- FILTER 的约束可能来自过滤结构，而不是普通口部尺度；
- 粒径对摄食的作用与释放、扩散、沉降是不同环节。

### Working Hypothesis

- 大对象对小鱼的限制通常首先出现在捕获、吸入或处理环节；
- 小对象对大鱼不应仅因体型更大就自动变成强负分；
- Feeding Place 会改变动作路径是否可行，因此尺寸约束不能脱离地点状态单独解释。

### OPEN

- `size_condition_m` 是否需要拆成捕获、保留、处理三个显式因子；
- `capacity_m` 由哪些可取证的形态和行为事实生成；
- 过滤结构的窗口如何与悬浮状态联合；
- 同一尺寸下的形状、硬度和团聚如何进入动作成功；
- 是否需要保留相对尺寸曲线，还是改用动作能力窗口与对象约束的组合。

## 8. 最小验证要求

1. 改变体尺或形态时，改变的是动作能力，不是鱼的偏好标签。
2. 改变 Feeding Place 的水层或底质时，只影响相关动作可行性，不重复修改尺寸约束。
3. 增加重复动作路径不增加同一对象的一次有效收益。
4. 改变释放时间或空间分布时，改变的是鱼遇到对象的分布，不直接改写对象固有尺寸约束。
5. 同一尺寸的不同对象状态可以改变动作成功，但不能伪装成不同粒径。

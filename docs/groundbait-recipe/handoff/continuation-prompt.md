# Continuation Prompt｜台钓窝料 / 配方机制

> 状态：Transient Handoff Context
> 
> 日期：2026-10-28
> 
> 说明：这是一份跨会话接续提示，不是机制 Contract。后续 Agent 应先读取 `../README.md` 指向的 Candidate / Working Decisions；如果本文与那些文件冲突，以 Candidate / Working Decisions 和更高层项目 Authority 为准。

你现在接手「中鱼升级」中的台钓窝料 / 饵料混合机制设计。

这不是从零开始，也不要重新扫描旧聊天。先完成最小 Documentation Rebase：

1. `docs/README.md`
2. `docs/authority-model.md`
3. `docs/groundbait-recipe/README.md`
4. `docs/groundbait-recipe/decisions/working-decisions.md`
5. `docs/groundbait-recipe/candidate/proposal.md`
6. 当前任务若涉及尺寸，再读 `docs/groundbait-recipe/candidate/edible-size-response.md`
7. 只有在做对抗性 Review 或怀疑方案退化时，再读 `docs/groundbait-recipe/rejected/anti-designs.md`

不要把 `rejected/` 当成候选方案列表，也不要把这份 handoff 当作 Current Authority。

## 当前工作位置

目前最新整体方案已经形成，但尚未闭合为正式 Contract。最深入的子模块是：

> `Edible Size Response｜可摄食尺寸响应`

它试图让 Groundbait 粒径筛选和后续 Hookbait / 饵球尺寸筛选复用同一套鱼侧模型。

当前鱼侧骨架：

```text
Body Size
× Morphology Profile
→ Intake Reference

Intake Reference
+ Feeding Mechanism Curve(s)
→ Mode Size Fit

多个替代 Feeding Mechanism
→ Best Available Path
→ Edible Size Fit
```

Groundbait 侧：

```text
Particle Distribution
× Fish Edible Size Response
→ Edible Fraction
```

## 下一项主任务

不要继续扩概念。直接建立 `Edible Size Response` 的第一轮 Gold Fixture，并攻击当前结构。

建议至少覆盖六类角色：

- 小型啄食鱼
- 大型底吸鱼
- 小型底吸鱼
- 大口吞食鱼
- 滤食鱼
- 双摄食模式鱼

可以先使用一组 Working Test Size：

```text
0.2 / 0.5 / 1 / 2 / 5 / 10 / 20 mm
```

这些数字只用于检验结构行为，不是生产定值。

Fixture 必须验证：

1. 同物种长大后 Size Response 整体向更大尺寸移动。
2. 同体长鱼可以因 Morphology Ratio 不同而不同。
3. PICK / SUCTION / GULP 的区别来自曲线形状，不只是倍率。
4. FILTER 使用独立 Reference Source 仍能成立。
5. 多 Feeding Mechanism 不因数量多而叠加获利。
6. 粗颗粒能明显降低小鱼的可利用份额。
7. 细颗粒不会无依据地强烈排斥大鱼。

## 你需要特别警惕的设计惯性

不要为了让模型“看起来完整”而立刻增加参数。优先问：这个参数购买了什么玩家策略？有没有现有参数已经能表达？

尤其不要重新引入：

- 每鱼手填最佳毫米数；
- 万能 `particle < mouth × constant`；
- 多 Feeding Mechanism 求和；
- 大鱼因为嘴大就自动强烈讨厌小颗粒；
- Food / Flavor / Particle / Physical 直接相加成 RecipeFit；
- 小药固定 Bonus；
- Weather → Flavor 的简单密码。

详细原因在 `rejected/anti-designs.md`。

## 数据生产问题

当前倾向不是让策划手填完整 Fish × Particle 矩阵，而是建立 Generator：

```text
Evidence
├─ Body-size range
├─ Mouth / gape evidence
├─ Feeding mechanism
├─ Filter structure when needed
└─ Typical natural food / prey size
        ↓
Parameter Generator
        ↓
Morphology Profile
+ Feeding Mechanism Set
        ↓
Generated Size Response
        ↓
Sparse Override
```

建议继续区分 Evidence Level：

```text
DIRECT
INFERRED
ARCHETYPE_DEFAULT
OVERRIDE
```

嘴部 / gape 是重要证据，但不是唯一决定因素。

## Fixture 完成以后

如果 Size Response 通过结构攻击，再依次：

1. 用若干真实代表鱼尝试生成 Morphology / Feeding Mechanism 参数。
2. 接 Groundbait Particle Distribution。
3. 设计 Physical Release：雾化、黏度、解体、沉降如何产生 Release Rate / Spread / Persistence。
4. 回到 Food Target，做同 Target 聚合 + 边际递减的 Fixture。
5. 再做 Flavor Composition / Intensity、小药和 Sparse Avoidance。
6. Groundbait 闭环以后再接 Hookbait。
7. Diet Shift 与最终 Response Aggregation 最后处理。

## 关于 RF4

研究输入：

`futouyiba/programaticHitFish/docs/research/2026-10-27-rf4-recipe-aggregation-design-recommendation.md`

已知研究 blob：`88ac78e33f90cd55ea5c01af90406bbca084b91f`

不要把其算法提案当成 RF4 源码事实。可借鉴的是公开产品结构和已验证的退化风险。

## 交付方式

每推进一个子模块，优先产出：

1. 当前 Candidate 机制；
2. 3–7 个反例 / 退化测试；
3. 一个小型可复算 Fixture；
4. 哪些是事实、推断、Working Hypothesis；
5. 尚未闭合的问题。

不要先写宏大的最终公式，也不要把研究阶段的建议直接晋升为 Current Contract。

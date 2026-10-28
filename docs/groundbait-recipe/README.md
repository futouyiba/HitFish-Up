# 台钓窝料 / 配方机制文档入口

> 状态：Candidate / Working Design  
> 日期：2026-10-28  
> 权威边界：本目录整理当前讨论形成的工作提案、工作决定、已排除方向和交接上下文。它不是 FCF Current Contract，不自动覆盖现有中鱼框架、Response Contract 或术语规范。正式术语与权威关系仍以 `docs/README.md`、`docs/authority-model.md` 和对应 Current 文档为准。

## 目录职责

```text
docs/groundbait-recipe/
├─ README.md                         # 唯一入口
├─ decisions/                        # 工作决定及其成熟度
│  └─ working-decisions.md
├─ candidate/                        # 当前最新工作提案
│  ├─ proposal.md
│  ├─ edible-size-response.md
│  └─ plain-language-explainer.md
├─ rejected/                         # 已排除 / 当前不采用的反设计
│  └─ anti-designs.md
└─ handoff/                          # 跨会话临时上下文，不是长期机制事实
   └─ continuation-prompt.md
```

`decisions/` 区分“已收敛边界”和“仍待 Fixture 验证的算法候选”；`candidate/` 保存当前完整方案；`rejected/` 不参与正常主线读取，避免旧方案与最新方案并肩竞争注意力；`handoff/` 只服务跨会话接续。

## 阅读顺序

后续 Agent 处理台钓窝料、混饵、味型、粒径或小药机制时，按以下顺序读取：

1. [`decisions/working-decisions.md`](decisions/working-decisions.md)：先确认哪些是已收敛边界，哪些仍只是 Active Candidate。
2. [`candidate/proposal.md`](candidate/proposal.md)：当前最新整体提案。
3. [`candidate/edible-size-response.md`](candidate/edible-size-response.md)：目前推得最深入的“可摄食尺寸响应”子模块。
4. [`candidate/plain-language-explainer.md`](candidate/plain-language-explainer.md)：面向人类快速理解当前设计。
5. [`rejected/anti-designs.md`](rejected/anti-designs.md)：只在评审、反例检查或需要理解边界时读取。
6. [`handoff/continuation-prompt.md`](handoff/continuation-prompt.md)：跨会话继续工作用的临时上下文与任务提示。

## 当前设计主旨

台钓配方暂不建模成一个“多个 Ingredient 给鱼加分，再求总分”的公式。当前提案把问题拆成四层：

```text
Ingredient / Recipe Source Facts
        ↓
Food / Flavor / Particle / Physical Facts
        ↓
Groundbait Physical Release
        ↓
Feeding Place：随空间和时间变化的食物、化学线索与颗粒状态
        ↓
Fish Interpretation / Response
        ↓
现有下游 Adaptation Coefficient / 权重链
```

当前最承重的工作边界：

- Food、Flavor、Particle Size、Physical Release 的职责不同，不直接并列成四个 Bonus 相加。
- 小药不作为免费固定 Bonus；状态饵也必须承担固体份额或其它真实成本。
- 雾化、黏度等首先改变释放速度、扩散范围、沉降和持续时间，不直接写成中鱼倍率。
- Particle Size 单独抽成 `Edible Size Response`，目标是让窝料颗粒和后续钩上饵球共享同一套“可摄食尺寸”语言，但 Hookbait 仍有自己的入口性、持钩、姿态等额外因素。
- “天气直接切换味型偏好”目前证据不足，不作为候选规则；天气等环境输入优先进入现有 Fish Condition / Feeding Readiness 语义。
- 最终是否存在单一 `RecipeFit` 尚未决定。Attraction、Retention、Ingestion、Selection 可能需要保留为不同语义。

当前主要算法候选仍需验证：

- Food：同 Target 合并后边际递减。
- Flavor：先按 Chemical Cue Exposure / Potency 混成整体 Flavor Profile，并保留总 Intensity；不是按 Ingredient 质量份额直接当味型百分比。
- Edible Size：用鱼的线性体尺、摄食形态和 Feeding Mechanism 生成尺寸响应；多 Feeding Mechanism 的 best-path 聚合仍需 Fixture 攻击。

## 研究输入

本轮主要设计输入之一：

- `futouyiba/programaticHitFish/docs/research/2026-10-27-rf4-recipe-aggregation-design-recommendation.md`
- 已读取版本 blob：`88ac78e33f90cd55ea5c01af90406bbca084b91f`

该研究明确是 Research / Working Proposal，不是 RF4 内部公式事实，也不是 FCF Current。当前目录只吸收其中经本轮继续推敲后仍保留的设计结论。

## 当前推进顺序

```text
Common Ingredient / Recipe Facts
↓
Edible Size Response
↓
Gold Fixture 攻击与真实代表鱼参数生成
↓
Groundbait Particle Distribution
↓
Physical Release：雾化 / 黏度 / 解体 / 沉降
↓
Food Target
↓
Flavor / 小药 / Sparse Avoidance
↓
Groundbait 完整闭环
↓
Hookbait / 饵球复用 Size Response
↓
最后再收 Response Aggregation 与 Diet Shift
```

不要从最终总公式开始倒推各模块。
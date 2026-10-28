# 台钓窝料 / 配方机制文档入口

> 状态：Candidate / Working Design
> 
> 日期：2026-10-28
> 
> 权威边界：本目录整理当前讨论形成的工作提案、已排除方向和交接上下文。它不是 FCF Current Contract，不自动覆盖现有中鱼框架、Response Contract 或术语规范。正式术语与权威关系仍以 `docs/README.md`、`docs/authority-model.md` 和对应 Current 文档为准。

## 先读什么

后续 Agent 处理台钓窝料、混饵、味型、粒径或小药机制时，按以下顺序读取：

1. [`candidate/proposal.md`](candidate/proposal.md)：当前最新整体提案。优先级最高。
2. [`candidate/edible-size-response.md`](candidate/edible-size-response.md)：目前推得最深入的“可摄食尺寸响应”子模块。
3. [`candidate/plain-language-explainer.md`](candidate/plain-language-explainer.md)：面向人类快速理解当前设计。
4. [`rejected/anti-designs.md`](rejected/anti-designs.md)：已讨论并明确不应重新直接采用的方向。只在评审、反例检查或需要理解边界时读取。
5. [`handoff/continuation-prompt.md`](handoff/continuation-prompt.md)：跨会话继续工作用的临时上下文与任务提示。它不是长期机制事实。

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
下游 Adaptation Coefficient 等现有响应结果
```

当前最承重的工作判断：

- Food、Flavor、Particle Size、Physical Release 的职责不同，不应直接并列成四个 Bonus 相加。
- Food 倾向采用“同 Target 合并后边际递减”，但仍需 Gold Fixture 验证。
- Flavor 倾向采用“整体味型画像 + 强度”，新味型会改变和稀释原有组成，不按味型逐项领取独立 Bonus。
- 小药是高强度的化学线索修改器，不应成为免费固定 Bonus。
- 雾化、黏度等首先改变释放速度、扩散范围和持续时间，不直接写成中鱼加成。
- Particle Size 当前单独抽成 `Edible Size Response`，目标是让窝料颗粒和后续钩上饵球共享同一套鱼侧尺寸响应语言。
- 天气默认先影响 Feeding Readiness；“天气直接切换味型偏好”目前证据不足，不作为现行候选规则。
- 最终是否存在单一 `RecipeFit` 尚未决定。Attraction、Retention、Ingestion、Selection 可能需要保留为不同语义。

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
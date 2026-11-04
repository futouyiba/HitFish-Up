# 圆桌、抽鱼与生成边界

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页只整理响应输出如何进入圆桌候选权重，以及抽鱼、生成和 Fish AI 的边界。它不定义圆桌四件的 Current 规则，也不补造刺鱼或搏鱼算法。

端到端工作算法见 [`end-to-end-algorithm.md`](end-to-end-algorithm.md) §10。本页只保留圆桌、抽鱼、生成和 Fish AI 的职责边界，不替 Current Contract 补造圆桌四件公式。

## 1. 已验证的 Current 语义

`docs/terminology.md` 定义：

- `SpatialDistributionWeight`：基础权重乘环境系数后的未归一化权重。
- `Fish Adaptation Coefficient Set`：鱼种对应中鱼习性模式到适配系数的 map，不含鱼况。
- `Roundtable Weight List`：响应之后、抽鱼和生成之前形成的最终候选权重列表。
- `Crowding-out`：圆桌抽鱼中候选按权重竞争抽取机会的关系。

术语只给出这些定义和位置，没有给出圆桌四件的具体公式。

## 2. 顺序

当前能确认的顺序是：

```text
有效 FishStock 集合
  → 按 FishStock.id 去重
  → 完成实鱼权重前置计算
  → 按 FishStock 汇总实鱼总权重
  → 每个 FishStock 独立计算空鱼权重扩张
  → 实鱼 / 空鱼贡献叠加
  → 现有挤占
  → 现有裁剪 Clipping
  → 圆桌权重表
  → 抽鱼
  → 生成
```

其中空鱼权重扩张来自 `docs/real-fish-weight-anchor-no-fish-expansion-dev-spec.md`：

```text
WΣ,k = Σ_i W_i,k
X_k = max(0, WΣ,k - A_k)
E_e,k = E_0,k + S_k × X_k
E_stack = Σ_k E_e,k
```

该文档是 0.3.4.1 独立开发需求，不是 0.3.4.0-B 的一部分，也不替代现有挤占和裁剪。

## 3. 输入输出

| 阶段 | 输入 | 输出 | 所有权 |
|---|---|---|---|
| 权重组装 | 空间分布权重、适配系数、投鱼配置、圆桌控制规则 | 圆桌权重结果 | 圆桌 |
| 空鱼扩张 | 每个 FishStock 的实鱼总权重、锚点、扩张率、基础空鱼权重 | 扩张后空鱼权重 | 0.3.4.1 dev spec |
| 挤占 | 候选权重 | 竞争后的候选 | 现有圆桌规则 |
| 裁剪 | 候选权重 | 裁剪后的候选 | 现有圆桌规则 |
| 抽鱼 | 圆桌权重表 | 抽取结果 | 抽鱼 |
| 生成 | 抽取结果、投鱼配置、生成规则 | 鱼对象 | 生成 |

## 4. 权重与概率

- `Roundtable Weight List` 仍是候选权重，不是概率。
- 只有进入抽样并归一化后才成为概率。
- 空鱼是同一抽鱼列表中的伪候选：参与抽鱼，不生成鱼对象。
- 中鱼等待时间属于系统输出，但不在响应模块直接产出。

## 5. 与响应的接口

当前保留两条互斥候选接口，具体候选必须携带接口类型：

```text
GenericFCF
  AdaptationCoeff
  → SpatialDistributionWeight × AdaptationCoeff

ProposalCOpportunity
  q = L × C
  → 直接进入候选权重，不再乘 SpatialDistributionWeight
```

接口类型缺失时阻断组装，不把 `q` 当作 `AdaptationCoeff`。

- 适配系数是模式级、鱼种级还是 FishStock 级。
- 多模式如何聚合成鱼种级系数集。
- 权重组装时是否还有其他修正。
- 响应读取空间权重只作为对应接口的只读输入；组装时是否再次相乘由接口类型决定：GenericFCF 必须乘一次，ProposalCOpportunity 不得再乘。

对应冲突登记 C-04a、C-04b。

## 6. 圆桌四件

系统图列出四件事：

```text
品质抽取调整
圆桌权重表构建
硬保底
动态权重调整
```

仓内没有这四件的完整 Current 公式。当前只保留接口问题：

- 品质抽取调整改变权重还是改变品质抽样。
- 圆桌权重表构建的输入：`GenericFCF` 走 `SpatialDistributionWeight × AdaptationCoeff`；`ProposalCOpportunity` 走 `q = L × C`，不再乘空间权重。
- 硬保底是权重下限、概率下限，还是独立控制层；它与归一化如何共存。
- 动态权重调整的规则是什么，是否需要记忆。
- 四件与挤占、裁剪的先后顺序。

## 7. 抽鱼与生成

抽鱼从圆桌权重表抽取候选，生成阶段确定：

- 鱼种 Species；
- 品质 Fish Quality；
- 大小 Size；
- 重量 Weight；
- 鱼对象；
- 中鱼等待时间。

这些字段的生成规则不在本页定义。当前只确认它们发生在圆桌之后。

## 8. Fish AI 边界

刺鱼、搏鱼属于 Fish AI / 下游玩法，明确在中鱼系统范围之外。

本页只记录一条接口：

- `Activity` 可由中鱼系统向刺鱼、搏鱼提供输入。
- 不定义刺鱼时机、钩型、线组、张力、脱钩或上岸模型。
- 不让 Fish AI 的结果反向改写圆桌或响应。

## 9. 未决项

- 圆桌四件的 Current 归属和公式。
- 硬保底与归一化的关系。
- 品质、大小、重量在哪一步抽取。
- `Roundtable Weight List` 是否已经归一化。
- 空鱼候选是否参与响应。
- 刺鱼是否消费 `Effective Ingestion Opportunity` 或 `Candidate retention`。

对应冲突登记 C-09。

## 10. 最小结构反例

- 同一 Collider 命中两次被算两次：FishStock 未去重。
- `WΣ = A` 仍然扩张：边界错误。
- `S = 0` 仍改变空鱼权重：关闭开关失效。
- 前置计算失败被当成 `WΣ = 0` 并转成空鱼：失败语义错误。
- 抽中空鱼后仍生成鱼对象：抽鱼与生成边界错误。
- 圆桌权重在归一化前被当成概率：阶段混用。
- 响应或圆桌反向改写 `SpatialDistributionWeight`：上游越权。

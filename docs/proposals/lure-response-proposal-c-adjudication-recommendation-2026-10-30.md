# Proposal C｜第一轮闭合：顾问建议记录（待 Owner 确认）

状态：Advisor Recommendation，Owner 已于 2026-10-30 确认全部五项，按 Owner 裁定执行。记录保留来源与当时的建议原文，便于追溯。

基线：`futou-/exciting-payne-95a562`，提交 `c8437a91`；对应 Issue #152。

## 1. 五项建议

| 项目 | 建议 | 对第一版的影响 |
|---|---|---|
| 探索 / 信息覆盖收益 | 不新增独立数值机制（A） | 不阻塞 |
| Risk MVP | 只立 `TackleConspicuousness`，可后置实现（C） | 不阻塞 Response 主链；但 Wariness 暂缺真实消费方 |
| CapacityModifier | 从 active candidate 删除（C），保留重开条件 | 不阻塞 |
| Prediction | 降级为 `Deferred Research`，不是当前待设计项 | 不阻塞 |
| `L` owner | 正式归 Opportunity；Spatial 只提供事实 | 实现前需要 |

## 2. 分项理由与重开条件

### 2.1 探索 / 信息覆盖：不立数值机制

理由：Response `C` 加单颗粒 `L` 买不出快搜；快搜的收益是实际扫过更多空间、更快收敛鱼位判断，属于作钓行为自然产生的信息收益，不应再加一个 `FastSearchInformationBonus`。

建议措辞：实际空间覆盖由 Opportunity / 空间遍历保留，但不奖励“快搜”标签。

重开条件：发现当前 Opportunity 架构无法表达“扫过更多空间意味着更多有效试探”时，按 Opportunity 实现缺口处理，不在 Response 加 bonus。

### 2.2 Risk MVP：只立 TackleConspicuousness

理由：玩家能直接选择线径、前导、钩与连接件、终端装配的明显程度；`EntryDisturbance` 是短暂瞬态，且 sound / contact 线索离“鱼视为异常风险”还隔一层解释。

建议：给 `TackleConspicuousness` 一个正式输入方向与 owner；第一版可暂不实现 `EntryDisturbance`。禁止 `SKU → conspicuousness`，应由配置提供可解释事实再派生风险暴露。

若会议完全不投入该开发，则退到 A：`RiskCost=0`，但必须明确 Wariness 暂时没有真实玩家策略消费方。

### 2.3 CapacityModifier：删除 active candidate

理由：没有独立消费需求，也没有现有机制解释不了的失败案例。

建议：当前 active design 不含 `CapacityModifier`，保留重开条件：

```text
species / size 能力基线 + Activity 仍无法解释某类必要玩法差异
且该差异确实是“当前实际运动能力改变”，不是“愿不愿追”
```

### 2.4 Prediction：降级为 Deferred Research

理由：继续列为普通 OPEN 已没有意义。

重开必须同时满足：固定 FoodValue、AttackTrigger、Closing、Risk、Motivation、Opportunity `L`，只改变运动可预测性，仍得到稳定、可复现、玩家能理解且足以改变打法选择的 Response 排序；不能只是统计拟合变好。

### 2.5 `L` owner：Opportunity

理由：`L` 已负责停留、穿越有效区域、垂直可交互窗口、opportunity identity、dedupe、reevaluation 与后续 reduce，超出 Spatial 职责。

建议职责：

```text
Spatial     → 提供空间事实：位置、区域、几何、有效空间窗口
Opportunity → 消费事实，产生 L，管理 identity / duration / dedupe / reducer
```

`q = L × C` 不变。

## 3. Owner 确认后的执行记录

五项已全部执行：

- `open-decisions`：五项从待裁改为已裁，保留重开条件；
- `evaluation-items`：`CapacityModifier` 移出可选聚合，标注删除与重开条件；Risk 只列 `TackleConspicuousness`；
- `response-opportunity` 与 `semantic-contract`：`L` owner 改为 Opportunity，Spatial 只提供空间事实；
- `first-round-closure`：Risk、快搜、CapacityModifier、Prediction 的结论补上裁定状态；
- 图形版同步。

会议稿不在本分支；如需同步，只加裁定结论，不加新机制细节。

## 4. 未决边界

- 本记录保留顾问建议原文与 Owner 确认来源；执行以 Owner 裁定为准；
- 未确认范围以外的事项不随本建议一起翻转。

## 5. 来源

- 用户转述的 ChatGPT 评审（2026-10-30）；
- Issue #152 与本文同源，评论只作留痕，不构成批准。

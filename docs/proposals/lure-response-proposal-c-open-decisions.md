# Proposal C｜开放决策

状态：Working Design / Candidate。这里只列尚未收口、尚未有 owner 或两侧口径冲突的问题。

## 1. 两侧口径冲突

本仓设计包已按 `docs/lure-response-joint-evaluation` 的 Working Closure 更新。旧 10-27 入口里的数字不再作为设计依据。仍存在的冲突只有一项：

| 议题 | 旧口径 | joint 最新口径 | 当前处理 |
|---|---|---|---|
| Prediction 是否进入主体 | 在 `DecisionMargin` 内作为 `-PredictionCost` | 聚合拓扑审查与 10-29 对齐稿把它移出主体 | 第一版主体不含 Prediction；只有出现独立策略价值证据时再重开，不列为下一步首要事项 |
| 机会表达 | `C(t) × exposure → accumulated` | `q = L × C` 一次乘，`L` 由 Spatial / Opportunity 提供 | 已按 joint 口径写入契约 |
| 响应投影 | `Margin / 0.30` | `M0=0, M1=0.40` | 已按 `M1=0.40` 写入 |
| 动机曲线 | `K_mot=0.60` 全轴 | 基准 `0.40` + 高 Motivation tail relief | 已按 tail relief 写入 |

## 2. Owner 缺口

- Opportunity / Spatial 侧 `L` 的正式 Current Owner 与 reducer；
- Feeding、Defense、Investigation 的 Interaction composition；
- `SuspicionLoad` 的生产 cue owner；
- 若未来启用 `ExplicitDirectional` bearing prior，production directional support 的 owner；
- 垂直可交互窗口（vertical opportunity seam）的正式 owner。

## 3. 语义缺口

- Prediction：第一版主体不含；只有控制 Trigger / Closing / Risk 后仍出现稳定、独立、玩家可学习的排序差异时，才重开；
- AttackTrigger：Escape-like 已准入；Injured / Struggling 与 imbalance-like vulnerability 为 `CandidateUnresolved`，等 cue-only holdout；pause 本身不得作为 Trigger（与时间机会重复）；
- 风险顾虑：当前没有任何生产输入，`RiskCost` 退化为 0；等 cue owner 与字段，不补造代理；
- 完整自然度模型；
- 非摄食咬击（护巢、领地、防御、烦躁）如何作为独立 family 组合；
- Fish Condition 名单与生成方式留待专门 Bake / Owner 讨论；本轮沿用现行四个鱼况，不重定名单；
- 装配版本变化时，共用轨迹记忆可以保留到什么边界。

## 4. 标定缺口

- FoodValue relation anchors 的生产来源；
- 动机 tail 的起点的 `0.80` 与额外斜率 `0.50`；
- `StateTrigger` 的最终预算；
- `K_close`、`K_wary`、`tau_recover`、`K_pred`（若启用）；
- `M0 / M1` 的 reference calibration，当前 Working `M1=0.40`；
- prey support、response、opportunity 和 Candidate 的整链分布；
- saturation 和 zero-response guardrails。

## 5. 数据缺口

- 实际水流与相对水体速度的稳定来源；
- 鱼与饵的 encounter geometry、reaction window 和 strike reach；
- 各鱼种 `InterceptSpeedLimit` 与体型缩放来源；
- 猎物解释所需的可见性、遮挡和装配局部数据；
- 机械操控暴露指标的实际采集口径（来源：`lure-response-proposal-c-mechanical-control-exposure-metrics.md`）。

## 6. 本轮不做的事

- 不把 Working seed 升格为 production parameter；
- 不把 Proposal C 研究分支的文件当作当前 Contract；
- 不为缺少 owner 的内容补造公式；
- 不通过新增 runtime cap 掩盖重复计权或标定失败；
- 不在完成语义契约前继续扩展商品类型或实现字段；
- 不在 Response 内增加搜索奖励或单位时间效率模型。

## 7. 下一轮收口顺序

1. 为 Escape-like 选定第一版可生产事实（转向强度、burst 强度）与 prey-conditioned 判定；
2. 决定 Risk cue 是否立项（TackleConspicuousness / EntryDisturbance 需要字段与 owner）；在此之前 `RiskCost` 保持 0；
3. 补机会量 `L` 的覆盖与有效窗口模型，验证快搜与隐蔽方案的外部代价；
4. 用 `proposal_c_strategy_probe.py` 的排序结果检查参数敏感度，再进入生产标定；
5. Prediction 不进入本轮；有独立策略价值证据时再单独开题。

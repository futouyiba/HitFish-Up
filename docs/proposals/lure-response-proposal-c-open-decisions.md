# Proposal C｜开放决策

状态：Working Design / Candidate。这里只列尚未收口、尚未有 owner 或两侧口径冲突的问题。

## 1. 两侧口径冲突

本仓设计包已按 `docs/lure-response-joint-evaluation` 的 Working Closure 更新。旧 10-27 入口里的数字不再作为设计依据。仍存在的冲突只有一项：

| 议题 | 旧口径 | joint 最新口径 | 当前处理 |
|---|---|---|---|
| Prediction 是否进入主体 | 在 `DecisionMargin` 内作为 `-PredictionCost` | 聚合拓扑审查与 10-29 对齐稿把它移出主体，只保留为待证明的局部代价；10-28 的联合回归仍允许双路并行 | 第一版主体不含 Prediction；触发与预测双路机制保留为可选局部实现，是否重入主体待裁定 |
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

- Prediction 是否值得作为独立局部代价重入主体；需要证明它在控制其它因素后仍产生稳定排序；
- 攻击诱因第一版准入哪些具名猎物状态；
- 风险顾虑第一版的最低实现层（装备暴露、呈现异常），以及是否展开完整 Naturalness；
- 完整自然度模型；
- 非摄食咬击（护巢、领地、防御、烦躁）如何作为独立 family 组合；
- Fish Condition 数量应由 Response 与其它消费者反推，当前不按生物学名词先定数量；
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

1. 裁定 Prediction 是否进入主体，或明确保留为可选局部代价；
2. 为攻击诱因选定第一版准入状态；
3. 确认风险顾虑的最低实现层；
4. 用三个对齐案例（追赶、摄食意愿、警惕度）检查策略排序；
5. 再进入生产标定。

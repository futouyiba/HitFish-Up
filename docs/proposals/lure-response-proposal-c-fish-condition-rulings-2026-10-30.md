# Proposal C｜Fish Condition 裁决记录（2026-10-30）

状态：Adjudication Record。由用户指示的 Fable 子代理在基线 `bc79696d` 上裁决，只读完成。本文记录裁决结论与仍需 Owner 决定的事项；裁决不自动写成 Current Contract。

## 1. 裁决总表

| 项目 | 裁决 | 是否阻塞第一版 |
|---|---|---|
| A 更新路径 | Bake 基线 + 运行时更新；当前只有 Wariness 有累积语义依据，其它三项不自动获得运行时更新 | 否，若只做基线或受限 Wariness |
| B 粒度与有效期 | Bake 粒度 `ConditionGroup × EngagementMode`；Diet Shift 加 prey family；过期 / 越界 / 缺来源转 `Unknown`，具体 TTL 待 Owner | 粒度不阻塞；完整 TTL 阻塞生产化 |
| C Activity | 非负 Candidate 值域；1.0 只是 Working reference，不是默认值；无证据不设上界 | 否，阻塞生产标定声明 |
| D Motivation | `[0,1]` 为 Candidate/Working 域；0.5 是参考锚，不是 fallback | 否，阻塞生产标定声明 |
| E Wariness | `[0,1]` 仅为 Candidate；累积归 Fish Condition / 动态机制，owner 待指定；Risk 只消费 | 否，Risk 当前为 0；阻塞真实警戒玩法 |
| F Diet Shift | 按 prey family 的有符号偏移；不加全局分量 | 否 |
| G TackleConspicuousness | 保留语义槽，后置实现；字段 / 数据 owner 待指定；实现前 `RiskCost=0`；禁止代理字段 | 否，主链可退化；阻塞真实 Risk 输入 |
| H 占位 | 允许常量或天气 / 时段分档的 Candidate placeholder；必须显式标注，缺失仍 `Unknown` | 否，若只声称占位 |

## 2. 逐项要点

### A. 更新路径

采用：

```text
Bake 产出 ConditionGroup × EngagementMode 基线
+ 运行时仅更新已有机制 Contract 明确授权的维度
当前仓内只有 Wariness 有“随过程累积变化”的语义依据
```

Response、窝料、Persistent Response Field 与玩家即时操作不得直接写回 Fish Condition。

Activity、Feeding Motivation、Diet Shift 目前只随上游重新求值或 Bake 刷新变化，没有运行时累积证据。

### B. 粒度与失效

- Bake 输出：Activity、Motivation、Wariness 为 `ConditionGroup × Mode`；
- Diet Shift：再按 prey family；
- 值必须携带来源、适用区间与解析状态；
- 过期、越界或缺少必要来源不得沿用最后值，转为 `Unknown`；
- 具体有效期、刷新频率与运行时 Wariness 的事件窗口未定。

### C–F. 数值与职责

- Activity：`ActivityCostMultiplier` 非负；1.0 是 Working reference；Unknown 不默认 1.0；无证据不设上界，不加 runtime cap。
- Motivation：`M ∈ [0,1]`；0.5 是参考锚，不是缺失 fallback；不乘 FoodValue，不复活 Reject。
- Wariness：`[0,1]` 仅为 Candidate；Risk 只消费，不生成；无 cue 时 `RiskCost=0`。
- Diet Shift：prey-family 有符号偏移，只影响对应 family；全局意愿由 Feeding Motivation 表达。

### G. TackleConspicuousness

只钉语义槽：当前目标下，已声明的终端装配事实造成的可见 / 侵入程度。最小可审计边界是能追溯声明事实、目标上下文、来源、有效区间与解析状态；数值范围、字段清单、公式与 owner 均待指定。

在字段与数据 owner 落仓前：

```text
SuspicionLoad = 0 → RiskCost = 0
```

不得用 SKU、饵体积或型号代理。

### H. 占位

允许常量或分档值，但必须标注 `Candidate/Working placeholder`、适用范围（ConditionGroup × Mode，Diet Shift 另含 family）、版本、有效期、来源与未标定状态。placeholder 不得冒充生产参数；无来源、越界或过期仍输出 `Unknown`。

## 3. Owner 裁定（2026-10-30）

七项已由 Owner 在 [Issue #161](https://github.com/futouyiba/HitFish-Up/issues/161) 裁定，摘要：

1. 路径 B Contract 化：Bake baseline + 仅机制授权的 runtime overlay → resolved Fish Condition → Response 只读；V1 可实现 baseline-only；
2. Wariness 累积归 Fish Condition 线下的 `Wariness Runtime Update / Overlay`；V1 不要求实现；
3. 过期、越界或缺来源 → `Unknown`，不引入 `stale-but-usable`；
4. Activity 不设语义生产上界，只要求非负且有限；1.0 是 Working reference；
5. `TackleConspicuousness` 暂不投入字段与 owner，继续 `RiskCost=0`；`EntryDisturbance` 不恢复；
6. Fish Condition baseline 落在 DEF 条件组下，按 snapshot / block 保存，含 value / status / source / version / validity；
7. Bake 负责执行、物化与校验；各 Condition 的语义、曲线、标定仍由对应机制 Contract 承接与审核。

问题与选项的原文见[Owner 决定请求](lure-response-proposal-c-fish-condition-owner-decisions.md)。

## 4. 来源

- 本记录来自用户指示的 Fable 子代理裁决（2026-10-30，基线 `bc79696d`）；
- 依据文件与节见[鱼况/Bake 契约](lure-response-proposal-c-fish-condition-bake-contract.md)、[开放决策](lure-response-proposal-c-open-decisions.md)、[五评价项契约](lure-response-proposal-c-evaluation-items.md)；
- 裁决不等于 Owner 批。第 3 节已由 Owner 在 [Issue #161](https://github.com/futouyiba/HitFish-Up/issues/161) 确认；经 PR 审核合并后才成为 Git Contract。

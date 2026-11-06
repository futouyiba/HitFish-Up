# Proposal C｜风险输入：RF4 与 Fishing Planet 参考（Research Note）

状态：External Research / Candidate。本文汇总《俄罗斯钓鱼 4》与《Fishing Planet》公开资料中的“终端钓组显眼度 → 咬口”设计，用来推导 Proposal C 的 cue 候选。外部游戏机制不是本仓 Current，也不是可直接照搬的生产公式。

来源标注：补丁说明与 Wiki 属官方 / 维护资料；Steam、论坛与攻略站属社区观察。两者在下面的来源列表中分别给出，不把社区经验当成官方机制。

## 1. 为什么看这两款

Proposal C 的 Risk 链条目前是：

```text
TackleConspicuousness（Candidate 字段：clarity，Owner 2026-11-06 立项）
× Wariness
→ RiskCost（解释规则未闭合时仍为 0）
```

缺的是“clarity 如何与直径、颜色、透明度聚合，鱼侧怎么消费”。RF4 与 Fishing Planet 都长期把线径、前导、钩与终端件的可见性当成咬口修正项，可以作为 cue 清单与聚合形状的外部参照。

## 2. Russian Fishing 4 的公开设计事实

- 线径越细、可见度越低，咬口率越好；同强度下线径更细的线更优；
- 材料透明度排序：编织线最显眼，尼龙接近透明，氟碳接近隐形；
- 判定的是“起作用的终端段”：接了前导后，按前导的线径计，不按主线；钢前导因粗显眼明显压低咬口；
- 部分编织前导按水底颜色选择（岩石灰、水草绿、泥底红、沙底沙色），颜色不匹配会出现“死口”；
- 鱼种谨慎度差异大：鲤 / 草鱼高，鲑科中等，鲈低；个体越大越谨慎；
- 官方/社区把它描述为咬口率修正，而不是“鱼真的被吓跑”。

来源：

- [RF4 Wiki：谨慎度](https://wiki.biligame.com/russianfishing4/%E8%B0%A8%E6%85%8E%E5%BA%A6)
- [Steam 讨论：am i scaring fish?](https://steamcommunity.com/app/766570/discussions/9/4138311592810801531)
- [RF4 论坛：Model Two Picker / welche Schnur](https://rf4game.de/forum/index.php?/topic/1822-model-two-picker-welche-schnur/)
- [俄罗斯钓鱼 4：主线推荐说明](https://a.9game.cn/news/10340461.html)

## 3. Fishing Planet 的公开设计事实

- 0.3.0 补丁把“线粗 → 可见度”加入 Fish AI；线材类型是可感知参数；
- 钩号影响咬口：小钩咬口更多、平均鱼更小；大钩提高平均个体但降低咬口；大钩配小饵会提高钩的可见度；
- 底部钓组里前导长度的影响可能大于线径：0.5 m 前导相比 1–2 m 明显掉口；钛前导同时吃“显眼 + 短”双重惩罚；
- 鱼种差异明显：鳟鱼偏好低可见度氟碳，鲶鱼 / 鲑鱼对编织线不敏感。

来源：

- [Fishing Planet Wiki：0.3.0 更新说明](https://wiki.fishingplanet.com/index.php?title=0.3.0/ru&oldid=138435)
- [Steam 讨论：Braid line](https://steamcommunity.com/app/380600/discussions/0/282992646977991094/)
- [Fishing Planet Basic Tips and Tricks](https://gameplay.tips/guides/fishing-planet-basic-tips-and-tricks.html)
- [Fishing Planet Wiki：Float fishing](https://wiki.fishingplanet.com/index.php?title=Float_fishing/ru)

## 4. 推导出的 Candidate cue 清单

```text
终端钓组显眼度
= 1 − Π_i (1 − c_i')

c_i' = c_i × ctx_visibility

c_line     线 / 前导的直径与材料可见度（只看实际起作用的终端段）
c_hook     钩与连接件的尺寸 / 形态显眼度
ctx_visibility  水体透明度与光照，只调制装备 cue，不单独作为一项显眼度
```

- `c_line` 需要直径、材料、是否使用前导、前导长度与颜色；
- `c_hook` 需要钩号、钩型、连接件尺寸与材质；
- `ctx_visibility` 必须调制已有装备 cue：没有 `c_line` / `c_hook` 时它不产生显眼度，避免清水或强光单独造出一个风险值；
- 鱼侧差异放在 `Wariness` baseline：鱼种、个体大小、钓压；
- `SuspicionLoad` 只取以上具名 cue 的聚合，不读取 `1 − prey_support`、速度或转向。

## 5. 与 Proposal C 的边界

- 本文只给 cue 候选与聚合形状；字段、owner 与生产映射未立项，`RiskCost = 0` 保持；
- `EntryDisturbance` 仍不实现；
- 不把 RF4 / Fishing Planet 的具体数值照搬为 FCF 参数；
- 外部资料是设计参照，不是本仓 Current 或 Owner 裁定。

## 6. 未闭口

- `c_i` 的具体映射与阈值（线径、材料、钩号）；
- 前导长度是否作为显眼度因子（Fishing Planet 证据支持，FCF 未验证）；
- 水体透明度与视觉 cue 的 owner，避免与 `cue.visual_contrast` 重复；
- 鱼种 / 体型 `Wariness` 基线表；
- 字段落地前 Risk 玩法的替代方案（是否接受长期 `RiskCost = 0`）。

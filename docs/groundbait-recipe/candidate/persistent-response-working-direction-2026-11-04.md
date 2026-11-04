# 台钓｜配方、持久响应场与实时响应：工作方向

> 状态：Working Synthesis / Candidate（2026-11-04）
> 来源：2026-11-03 至 11-04 对话中的用户明确方向与后续候选推演。
> 权威：此稿供审阅和继续设计，不是已审核的 Current Contract，也不补充生产字段、数值或公式。用户明确的方向要按 `docs/authority-model.md` 处理为待承接 Owner 意图；本稿仍需与现行 Owner 和 Current 合并路径核对。
> 本轮核对基线：`main@d81829778df10bde9c6e129a84bf51c749fb451b`。原有 Groundbait 文档中写的“截至 10-30 PR #130 draft”等属于当时快照，不作为今天的状态判据。

## 1. 要购买的玩家选择

台钓玩家主要选择：用什么配方、什么钩饵、打多少窝、何时补窝、何时换点。系统需要支持“发窝、续窝、过量、衰减、重登后仍有历史”，并允许泛用/专精、主料/主攻/状态/小药之间有真实取舍。

### 本轮目标链

```text
Ingredient facts → 离散槽位配方 → 投放事件 / Physical Release
                                     ↓
                         Persistent Response Field（持续响应条件）
                                     ↓
钩饵 Food / Cue / Size / 当前呈现 → Response C / AdaptationCoeff
                                     ↑
                                Fish Condition（只读）

合法姿态 / 有效机会颗粒 → Opportunity（身份、窗口、去重）→ L

组装时依声明的接口类型二选一：
  GenericFCF          : SpatialDistributionWeight × AdaptationCoeff
  ProposalCOpportunity: q = L × C（此路径不再乘空间权重）
```

**“窝料影响 C、不改 L”是本轮用户指定的台钓方向，不是自动改写 Proposal C 的全域 Opportunity Contract。** Opportunity 负责合法呈现形成的机会支持；窝料不凭空创建合法机会、不直接提高 L、不写回 DEF 或 SpatialDistributionWeight。上层仍需检验：只调 C 是否足以表达期望的“发窝”体验，不能把真实鱼数增加当成已实现事实。

## 2. 当前可承接的边界

### 2.1 原有文档已经收敛的边界

- `Ingredient Facts` 与 `Recipe Role` 分开：原料提供 Food、Chemical Cue、粒径与物理事实；Base/Target/State/Attractant 是配方角色，不能写成固有 `Ingredient.Type`。
- Food Target 是可摄食目标；Chemical Cue 是可感知化学线索；两套字典不混用。同 Target 先合并后饱和是 Active Candidate，多 Target 算子仍 OPEN（C-11b）。
- Physical Release 先改变 Feeding Place 的对象、位置、可用量、持续时间；实体物料有守恒账本，Cue 来源、释放与可食物料不可混同；不直接生成 Bite Bonus。
- `Persistent Response Field` 是持续玩家行为在运行时形成的增量语义，不复制也不写回 DEF；`Fish Condition` 不能被窝料自由写入。
- 当前 Chemical Cue 只准入“类型/签名”分支；连续浓度/强度未获 C-02 Owner 准入，不能借本稿偷偷开启数值 FlavorIntensity。
- `GenericFCF` 与 `ProposalCOpportunity` 是互斥组装路径，不能把 `L × C` 泛化到所有候选，亦不能重复乘空间权重。

### 2.2 用户本轮明确提出的方向（待进入正式审阅承接）

- **窝料持续影响**归 `Persistent Response Field`，当前钩饵对应实时 `Response Condition`。Groundbait Cue 和 Hookbait Cue 可复用化学线索语义，但按来源、作用范围、生命周期分别生产；共同在 Response 消费，禁止双算。
- “发窝、续窝、衰退、过量、恢复”的持久作用**不归 Opportunity**；合法机会颗粒、identity、窗口与去重继续归 Opportunity。
- Overfeeding / feeding pressure 先在持久响应场内研究，不自动成为 `FeedingMotivation` 或其它 Fish Condition 的 runtime overlay，亦不进入 Bake。
- 持久效应需要跨抛竿、跨本次登录、下线再登录后恢复；不以登出清零。具体有效期、离线演化和归属范围待定。

这些属于**Owner 意向及讨论方向**；它们收窄了旧的 C-05、C-07 等 OPEN/“首版后置”建议，却没有回答状态、更新、资源和生产验收问题。CC 不能把“先研究 Overfeeding”转写为“已批准首版必须实现全部鱼群模拟”。

### 2.3 当前仅作为可检验的 Candidate

| 主题 | 工作建议 | 仍需验证 |
| --- | --- | --- |
| Base/Target/State/Attractant | Base 负责主体质量、基础 Food 和物理基底；Target 强化特定 Food；State 调控释放；Attractant 是低用量 Cue contributor | 这些是角色定位，不是固定 Bonus；Ingredient 即使担任 State 仍可能贡献 Food/Cue |
| 配方界面 | 先走 RF4 式离散槽位，不给玩家连续百分比或“淡/标准/浓”滑杆 | RF4 玩家界面≠内部公式；不得据此断言 RF4 没有数量机制 |
| 数量 | 配方组成可以槽位化；投放总量、物料库存、释放、消耗、离线演化仍需可计算量 | 如果“同一种 Cue 多投”只改变时间/覆盖，不得声称其强度影响偏好，除非 C-02 获准 |
| Food 多 Target | 比较“各 Target 先饱和，再总和后全局饱和”作为优先实验分支 | C-11b OPEN；不预先定公式或参数 |
| Overfeeding | 考察物料过量、实际摄食累计与持续负反馈的不同因果来源 | 不能以投放量直接伪造鱼已吃饱；先做反例 |

## 3. 持久响应场的最小模型：先定义问题，不冻结 schema

必须区分三件事：

1. **来源事件**：某人在何处、何时投入哪种配方、投放多少，补窝/移除/替换如何记。
2. **地点随时间的物料和线索状态**：可食/载体余量、位置/层、释放、化学线索及有效期。物料和线索账本不得混为一个“窝强度”。
3. **给 Response 的持续输入**：对指定鱼种/模式/钩饵的可解释持续影响。它可以从上面两层按需派生，不能又作为独立 Bonus 对同一事实重复乘一次。

Candidate `PersistentFieldState` 需要设计的最小语义：scope/owner、place、来源与投放事件、时间戳/版本、物料与 Cue 状态、feeding-pressure 来源、过期/无效状态及重放规则。**这些是待回答的字段职责，不是批准了的字段清单。**

“Local Presence / 招鱼 / 驻留”可以先定义为可观察玩法结果（发窝、咬口变化），**不预设鱼群真的从别处移动、人口增殖或额外生成机会**。若必须表达真实局地鱼数变化，另行提交有状态所有权与守恒依据的 Owner 决策，不把它暗写到 `Persistent Response Field` 或 `L`。

## 4. 六个需要继续闭合的问题

| 顺序 | 问题 | 必须回答的最小结果 |
| --- | --- | --- |
| P1 | 持久场到底保存什么？ | 来源事件/物料状态/响应投影如何分层；谁生产、谁消费、时间与空间身份；缓存与事实来源如何区分 |
| P2 | Food、Cue、Release、FeedingPressure 怎样共同起效？ | 谁影响哪个结果、如何形成非单调“少/适量/过量”；同一事实不在持续层、实时层或 Fish Condition 重复结算 |
| P3 | 多 Food Target 怎么聚合？ | C-11b 对照算子和策略排序，测试专精/混配/拆 Ingredient 套利/全家桶，给 Owner 可选结论 |
| P4 | 窝料背景与钩饵实时响应如何合并？ | 同一 Cue 不双算；钩饵无效/缺失不能被强窝料救活；Size/动作约束、目标鱼差异仍能发挥作用 |
| P5 | 如何发窝、补窝、过量、恢复？ | 最小确定性时间模型、投放与消耗守恒、衰减/记忆、离散步长与离线回放等价性 |
| P6 | 下线再登录如何继承？ | 实例作用域（玩家/钓点/房间/公共水体）、跨人并发与重复计投、服务器权威、过期与存储成本、跨登录可重建性 |

必要的结构反例：

- 同配方换 Ingredient ID 或交换槽位中语义等价的原料，输出不发生非法跃升；角色确有不同预算时需注明来源。
- 固定钩饵与机会条件，先后投放/补窝可改变后续 Response，但绝不能修改 DEF、Fish Condition 或 L。
- 同一时间窗同时有“窝料 GARLIC + 钩饵 GARLIC”，不会因为同一 Cue 源复制而重复获奖；若背景和实时线索各有明确独立后果，应分开可追溯。
- 过量投放不自动等于过量进食；若尚无摄食事实，负反馈来源必须另作假设并标注。
- 在声明的离线时间语义下，连续模拟与“保存时间戳后重登推演”得到同一结果；重登不得重发奖励、复制物料或跳过衰减。
- 空钩/不可摄食对象、被 Reject 的食物目标不能靠强窝料无限救活。
- 对比“只有窝料，没有合法机会颗粒”：不能凭窝料独立制造候选机会；对比两个组装路径：只能走其一。

## 5. 还需要 Owner 决定的内容

- C-02 Chemical Cue 强度是否准入（类型、粗档、连续）；这与是否有玩家“加多加少”按钮正交。
- C-05 持久场独立语义、实例归属、增量与原始状态关系；此前 brief 的推荐不等于 Owner 裁定。
- C-07 Overfeeding、Local Population/Residence 是否首版做，以及它们是事实状态还是仅 Response 的派生效果。
- C-11b 多 Food Target 聚合；多 Response Component、模式聚合及 `GenericFCF` 与 `ProposalCOpportunity` 的具体接口承接。
- 长期保存时的时间语义：现实时间还是游戏时间，玩家私有还是共享，离线恢复上限、过期和服务器权威。

## 6. 阅读依据（固定版本）

- 仓库入口 `docs/README.md` blob `f43c7d59`，权威 `docs/authority-model.md` blob `7bc31c5e`。
- 正式术语 `docs/terminology.md` blob `741248f1`，其中 Persistent Response Field 的职责见 §4。
- Groundbait `docs/groundbait-recipe/README.md` blob `db1fbfc1`；`decisions/working-decisions.md` blob `9107198a`；`decisions/owner-decision-brief.md` blob `56f11545`。
- `candidate/response-aggregation-map.md` blob `ee9a5712`：两种互斥组装路径；`candidate/food-aggregation.md` blob `1c9bf517`：C-11b 仍 OPEN；`candidate/response-stage-mapping.md` blob `6351f12c`：持久与即时响应映射为 Candidate。
- Fish Condition runtime 的授权边界需核对 [Issue #161](https://github.com/futouyiba/HitFish-Up/issues/161) 与目前已合并 Proposal C Candidate，而非复用旧 PR #130 的旧标尺。

下轮推演先核对这些依据的最新状态；本稿是可审核的方向记录，不是后来者可以跳过 authority rebase 的依据。

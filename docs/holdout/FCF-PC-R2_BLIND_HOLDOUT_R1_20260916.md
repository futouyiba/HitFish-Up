# FCF-PC R2 Blind Holdout Round 1｜独立盲测样本 + 泛化审查报告

```text
Round ID:        FCF-PC-BLIND-HOLDOUT-ROUND-1-20260916
Baseline ID:     FCF-PC-BASELINE-R2-20260916
Baseline sha256: e5c7c1e5044b4a4ee943975170277a0399cfd50630c08a9d0d25e85ab1b2e93e
Role:            Independent Holdout Reviewer（未参与 R2 Presentation/Cue 设计）
Round Date:      2026-09-16
Status:          COMPLETE / BLIND DISCIPLINE HELD（本轮零 baseline 修改）
```

---

## 0. Round Validity｜可复现性与冻结验证

**阅读路径合规**（任务指定顺序，全部执行后 Stop）：

```text
FCF Router (3cca4137…9e47)
→ Project State Current (3cca4137…5e49)
→ Design Branch Index (3cda4137…84dd)
→ Simplified Production V0 Working Main (3cda4137…bd41)
→ Response Language Contract Delta R0 (3d0a4137…583c)
→ FROZEN Presentation Adapter Development Set Manifest v1 (3c7a4137…4b6b, 2026-08-25)
→ Presentation Adapter Unseen Holdout Protocol v5 (3c7a4137…1cb92)
→ Stop
```

- Branch 确认：**Simplified Production V0 / Presentation / Cue / Response-input representation**。未切换 FCF V1 或 Mainline authority。
- **Executable parent 验证通过**：`futouyiba/programaticHitFish`，branch `fcf-v0-current-contract-rebase`，head = `9c2beebd2e2b1f5757223149e9c65f16bb200841`（clone 只读验证，未做任何修改）。
- **Baseline sha256**：owner-attested。对该 commit 下全部 `.md/.py/.json/.txt` 文件做 sha256 扫描无匹配——R2 baseline 是冻结的 representation 文档（Notion 合同文本 + 本任务冻结声明），不是 repo 内单一 artifact，故 hash 无法在本环境独立复核。**按任务方冻结声明采信，风险披露于此。**
- **Admitted vocabulary 口径**：以 Response Language Contract Delta R0 §4.1–4.5 为基础，叠加 R2 冻结修订——`cue.displacement` 记 **NOT_ADMITTED / PROVISIONAL**；chemical magnitude（`cue.chemical_intensity` / `cue.odor_concentration`）**不**是 admitted core primitive；`presentation.chemical_signature` 只载 chemical type/identity。据此，admitted typed token 计数：cue 12（13 项列名减去 provisional 的 displacement）+ presentation 3 + relation 4 ≈ **19**。
- **污染边界**：FROZEN Manifest v1（9 dev cases + 3 synthetic fixtures + 已影响设计决策清单）+ 任务 §6 补充条目（Bass jerk-pause、Spawn Guard Bass、Trout match hatch、Walleye low-light、chemical/scent feeder 故事、Carp pressure/cue familiarity 故事）。
- **Blind discipline**：本轮期间未修改任何 cue.* / presentation.* / relation.* / FeedingTarget 语义 / classification protocol / ownership rule；未因 case 结果新增 alias 或调整解释方向。所有 `BASELINE_CHANGE_REQUIRED` 仅作为标记记录，修改留待 Design Owner 在本轮结束后裁决。

---

## A. Sample Manifest｜18 cases

选样独立完成，未与任何设计讨论对齐。案例来自现实钓法（部分以公开资料佐证，资料仅作 case evidence，不构成 semantic authority）。

| ID | Case | 家族 | Unseen class | Contamination check | 建议覆盖轴 |
|----|------|------|--------------|---------------------|-----------|
| H01 | 慢滚单 Colorado 叶片 spinnerbait（冷水浑水鲈） | spinnerbait | IN_FAMILY_UNSEEN | dev set 只消费 fast/steady（光学主导）与 jerk+pause；低速机械主导 config 未被使用 | mechanical-dominant、continuous retrieve |
| H02 | 铸勺垂直 jig：slack 线 flutter 沉降 + 上抽 | spoon | IN_FAMILY_UNSEEN | dev set 消费的是水平 steady/oscillating **retrieve**；垂直沉降循环未使用 | optical-dominant、short-event/temporal |
| H03 | 水面 walker 走狗式连续侧移 | topwater | IN_FAMILY_UNSEEN | dev set 消费 popper pop+pause；连续 zigzag 无停顿 config 未使用 | surface、continuous retrieve |
| H04 | 无配重 wacky 软虫 slack 沉降 | soft-worm | IN_FAMILY_UNSEEN | dev set 消费 bottom drag；水柱沉降相未使用 | stationary/slow、fall phase |
| H05 | 湿蝇/毛钩 swing 横扫流口（steelhead） | fly | IN_FAMILY_UNSEEN | dev set 消费 dead drift + twitch；受张力横扫 config 未使用 | reference-frame、mid-water、flow |
| H06 | 方唇 crankbait 撞障碍偏折回收 | crankbait | CROSS_FAMILY_UNSEEN | crankbait 家族整体未入 dev set | mixed cue、short-event、离散接触 |
| H07 | Umbrella rig（Alabama rig）5 臂拟饵群游 | 多组件复合 | CROSS_FAMILY_UNSEEN + ADVERSARIAL | 未入 dev set | multi-target、multi-component |
| H08 | 自由线活饵 shiner（鲈） | 活饵 | CROSS_FAMILY_UNSEEN | 活饵（self-propelled）未入 dev set；bread/prepared food 是另一支 | live erratic motion、feeding-target |
| H09 | Popping cork + 虾静态悬浮 | shrimp + 声源复合 | IN_FAMILY_UNSEEN | dev set 消费 shrimp bottom hop；静态悬虾 + 独立声源 config 未使用 | multi-source（异构）、stationary、mixed |
| H10 | 夜间 jitterbug 匀速水面爬行 | topwater | IN_FAMILY_UNSEEN | pop+pause 之外的恒定 gurgle config 未使用；夜间光照场景未消费 | sound-dominant、light/visibility |
| H11 | Drop-shot 原地微抖离底定悬 | finesse rig | CROSS_FAMILY_UNSEEN | 未入 dev set | stationary、零位移、displacement 反例 |
| H12 | Bottom bouncer + crawler harness 拖底拖曳（白昼 walleye） | 复合 rig | CROSS_FAMILY_UNSEEN | walleye 污染条目是 low-light 故事；本 config 为白昼结构拖曳，主导通道（底扰/blade/气味）不同，exact config 未使用 | bottom relation、continuous contact（已知缺口轴） |
| H13 | Football jig 沿石底拖磨（smallmouth） | jig | CROSS_FAMILY_UNSEEN | 未入 dev set | bottom relation、continuous contact（已知缺口轴） |
| H14 | Sheepshead 紧贴桩柱蟹型微饵 | 甲壳拟饵 | CROSS_FAMILY_UNSEEN | 未入 dev set | feeding-target-sensitive、结构贴合 |
| H15 | Musky 船边 figure-8 急转 | 大型拟饵 | CROSS_FAMILY_UNSEEN | 未入 dev set；非 Spawn Guard 故事 | non-feeding Mode 候选（Reaction）、short-event |
| H16 | Crankbait 涂 shad 气味凝胶 | 化学辅助 | CROSS_FAMILY_UNSEEN | 未入 dev set；只涉及 chemical **类型**（未触及被推迟的浓度问题） | chemical identity、mixed |
| H17 | 鲶鱼 punch bait 浸泡时间衰减 | 化学主导 | IN_FAMILY_UNSEEN_CONFIG，**POSSIBLE_CONTAMINATION（家族级）** | chemical/scent feeder 故事已参与设计且显式推迟过 odor_concentration；exact config（新鲜度管理策略）未用于调参，但语义问题已被访问 → 按协议**不作为 blind discovery**，作 confirmatory 压力证据 | chemical magnitude（已知推迟项） |
| H18 | Flatline 拖钓深潜 crankbait 匀速定深 | 拖钓 | CROSS_FAMILY_UNSEEN | 未入 dev set | boundary（策略差异在 presentation 之外） |

**主动排除的抽样轴（污染不可回避）**：Carp pressure / cue familiarity；chum/groundbait 区域级化学；Spawn Guard 类护巢故事；Bass jerk-pause；Trout match hatch；Walleye low-light。这些轴本轮**未获得 blind 证据**，见 F 节。

---

## B. Per-case Results

分类集合：`COVERED / ANNOTATION_ONLY / DERIVED_DESCRIPTOR_ONLY / NEW_GENERIC_RULE_REQUIRED / NEW_PRIMITIVE_REQUIRED / NEW_RELATION_REQUIRED / ITEM_SPECIFIC_EXCEPTION / UNRESOLVED / CAUSE_OWNERSHIP_CONFLICT`。

### H01｜慢滚单 Colorado spinnerbait｜COVERED

- **Unseen class**: IN_FAMILY_UNSEEN（spinnerbait；dev set 为 fast/steady 光学主导 + jerk/pause）
- **Real strategy**: 冷水/浑水沿草线慢滚大单叶，靠低频高幅 thump 在低能见度下招募鲈鱼。对玩家实质变化：同一物品家族从"闪光+快"切到"震动+慢"仍成立。
- **Observed facts**: vibration_amplitude HIGH / vibration_frequency LOW / speed LOW / visual_contrast LOW（浑水下 receiver-relative 有效值）/ apparent_size MED。
- **R2 facts available**: 上述通道全部 admitted。
- **Required Response distinction**: 低频高幅震动+低速 vs 高频闪光+快速——同一 Species×Mode Profile 下不同 rule 组合 band。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: MECHANICAL_DOMINANT_CHANNEL_REUSE。
- **Cause ownership**: 浑水对视觉的影响已被 effective receiver-relative `cue.visual_contrast` 单点吸收；Response 不读 context.clarity/light。
- **Double-count**: 无。**Identity-shortcut**: 无（"spinnerbait"不进鱼语义，只消费 resolved kinematics/震动）。
- **Reasoning**: dev set 当年"optical family 复用、不新增 sensory dimension"的判断在机械主导 config 上外推成立。

### H02｜垂直铸勺 flutter 沉降 + 上抽｜COVERED

- **Unseen class**: IN_FAMILY_UNSEEN（spoon；dev set 为水平 retrieve）。
- **Real strategy**: 深水垂直 jig，鱼主要在 slack 线 flutter 摆闪沉降段触发反应口；对玩家的实质变化：以"沉降相"为主激活策略。
- **Observed facts**: 沉降段 vertical_motion SINK + speed LOW + flash HIGH（摆动反光）；上抽段 speed_change HIGH + vertical RISE + 声响 spike。
- **Required Response distinction**: 摆闪沉降 vs 水平稳收——fall 相的 flash+sink 组合提升 band。
- **Primary**: COVERED。**Flags**: SHORT_EVENT_TEMPORAL（分相快照足够，不需 sequence operator）。
- **Cause ownership**: 相切换由上游 molecule 快照承载；`cue.flash` 是沉降段 CurrentFact。**Identity** ✓。
- **Reasoning**: R2 的 CurrentFact / RecentEventFact 合同正确覆盖"fall 触发"模式；印证时序算子未准入的决策。

### H03｜水面 walker 连续走狗｜COVERED

- **Unseen class**: IN_FAMILY_UNSEEN（topwater；dev set 为 popper pop+pause）。
- **Real strategy**: 黎明水面连续侧向走动，恒定细碎水声+连续 zigzag，无长停顿。
- **Observed facts**: direction_change 高频小幅；sound_amplitude LOW 恒定；relation.surface ON；speed LOW-MED 匀。
- **Required Response distinction**: 连续走动 vs 爆停式——`ALL(direction_change HIGH, pause_duration LOW)` 与 popper 的 pause 主导 rule 自然分开。
- **Primary**: COVERED。**Flags**: SURFACE_RELATION_REUSE。
- **Reasoning**: relation.surface + direction_change 组合足够；不需 surface_pop 类 universal feature（与 dev set 反设计一致）。

### H04｜无配重 wacky 软虫 slack 沉降｜COVERED

- **Unseen class**: IN_FAMILY_UNSEEN（soft-worm；dev set 为 bottom drag）。
- **Real strategy**: 水柱中无张力自由沉降，端部 shimmy 微震，触底前完成大部分咬口。
- **Observed facts**: vertical_motion SINK / speed LOW / vibration_amplitude LOW（shimmy）/ apparent_size、visual_contrast 常规。
- **Required Response distinction**: 慢沉降微震 vs 拖底 vs 游动——沉降相主导的 rule。
- **Primary**: COVERED。**Flags**: FALL_PHASE_NO_BOTTOM_CONTACT（已知缺口未被触碰：不接触底）。
- **Reasoning**: 与 H12/H13 对照说明软虫家族的沉降相表达无缺口；缺口专属于连续底接触。

### H05｜湿蝇 swing 横扫流口｜COVERED

- **Unseen class**: IN_FAMILY_UNSEEN（fly；dev set 为 dead drift + twitch）。
- **Real strategy**: steelhead 经典 swing：跨流弧线、线张力持续、饵以略超水流的速度横扫 holding lie。
- **Observed facts**（support-relative）: speed rel. water LOW；direction_change LOW（缓弧）；apparent_size 偏大（broadside 投影由 receiver-relative 自动承载）；relation.flow IN_FLOW。
- **Required Response distinction**: swing vs dead drift（speed rel. support = LOW vs ZERO）vs strip（MED-HIGH）。
- **Primary**: COVERED。**Flags**: REFERENCE_FRAME_RESOLVED_BY_SUPPORT_RELATIVE_RULE。
- **Cause ownership**: 参考系统一取水流支撑系，baseline 明确允许 support-relative geometry——三 config 在同一坐标系内区分，无需 frame 字段。**Double-count**: flow 只经 relation.flow 进入，不重复。**Identity** ✓。
- **Reasoning**: §11 压力点"reference-frame-dependent motion"被现有规则吸收，是 R2 的隐性强项。

### H06｜方唇 crankbait 撞障碍偏折回收｜COVERED

- **Unseen class**: CROSS_FAMILY_UNSEEN（crankbait 家族未入 dev set）。
- **Real strategy**: 故意撞木/撞石，瞬间的偏折+碎裂声触发反应口（"crash bang"）。
- **Observed facts**: 匀速段 vibration_amplitude MED（wobble）+ speed MED；撞击瞬间 direction_change HIGH + speed_change HIGH + sound_amplitude spike（RecentEventFact）。
- **Required Response distinction**: "刚发生强烈偏折事件"提升 Reaction band vs 平稳回收。
- **Primary**: COVERED。**Flags**: DISCRETE_CONTACT_EVENT_EXPRESSIBLE。
- **Cause ownership**: 关键裁决——"撞到木头"这一 cause **不**需要进入语义；鱼响应的是偏折运动学+声音事实本身。因此不需要 `relation.cover / relation.wood`。这是正确的结果，不是偷懒：deflection 的全部可观察结果就是运动学+声学事实。**Double-count** ✓ 无。**Identity** ✓。
- **Reasoning**: 离散触障事件可表达；与 H12/H13 的连续底接触缺口形成精确边界（本报告最重要边界发现之一）。

### H07｜Umbrella rig（Alabama rig）群游拟饵｜NEW_GENERIC_RULE_REQUIRED

- **Unseen class**: CROSS_FAMILY_UNSEEN + ADVERSARIAL（multi-component、多同源源）。
- **Real strategy**（证据：[In-Fisherman](https://www.in-fisherman.com/editorial/umbrella-rigs/154044)、[Wired2Fish](https://www.wired2fish.com/fishing-rigs/alabama-rig-how-to-fish-and-rig-it)）：5 臂各挂小 swimbait 模拟小型饵鱼群；群体的联合闪光/扰动/集群轮廓触发 school-feeding 反应，捕食者攻击"掉队者"。冷水迟钝鱼也反应。
- **What materially changes**: "一群小鱼" vs "单只"是玩家合法且实质不同的策略；远距离群体信号 + 单饵尺寸攻击目标同时存在。
- **R2 facts available**: 每个组件单独都有全套通道；但 **typed snapshot 语义是单一 presentation**——多同源源的合成规则未定义：通道聚合取谁（MAX？物理叠加？）、集群轮廓/群体 shimmer 归哪个字段、以及"本 presentation 实例化了一个群体"这一事实无承载位。
- **Required Response distinction 不可省略**：若不承载 multiplicity，umbrella rig 与单 swimbait 的 Response 不可区分——玩家策略差异被抹平。
- **Primary**: NEW_GENERIC_RULE_REQUIRED。
- **Requested deltas**: 多同源源 snapshot 合成 generic rule（哪些通道合成/取最大、哪些保持 per-target；multiplicity fact 如何进入 typed snapshot）。备选窄路径（记录不裁决）：`presentation.profile` 字典增加 SCHOOL_OF_BAITFISH 值可保类型级差异但丢失 count/spacing 梯度。
- **Flags**: MULTI_TARGET_PRESENTATION / BASELINE_CHANGE_REQUIRED / SINGLE_EVIDENCE_RULE（本轮仅此 case 要求；daisy chain、tandem rig、multi-fly 可预期复用）。
- **Cause ownership**: 合成规则属 Cue Resolver / molecule 层（Presentation-side）；不进 Fish 侧。**Identity** ✓（不形成 SKU 语义）。**Double-count**: 需防物理叠加声音与单饵声音重复计入——合成规则本身要定义唯一性。
- **Reasoning**: 通道词汇本身够（amplitude/flash/size 都在），缺的是多源组合语义——按"最小充分 semantic change"归 NEW_GENERIC_RULE 而非 NEW_PRIMITIVE（count/spacing 梯度需求当前证据不足）。

### H08｜自由线活饵 shiner｜COVERED

- **Unseen class**: CROSS_FAMILY_UNSEEN（self-propelled 活饵未入 dev set）。
- **Real strategy**: 活饵自主游动+挣扎，erratic 自然轨迹，free-line 无浮标约束。
- **Observed facts**: speed 时变（LOW-MED 波动）；direction_change 持续小幅高频 + 偶发挣扎 burst（RecentEventFact speed_change/direction_change HIGH）；无 pause；presentation.prey_stage = 成体饵鱼。
- **Required Response distinction**: "自主持续 erratic 运动" vs 拟饵匀速回收——`direction_change` 频带 + `speed` 波动 + prey_stage 组合足以区分。
- **Primary**: COVERED。**Flags**: NO_LIVE_SEMANTIC_NEEDED。
- **Cause ownership**: **"活"本身不需要语义**——鱼无法直接感知 provenance，感知的是运动学；目标偏好由 Species × FeedingTarget 静态亲和承载。**Identity** ✓（没有 LIVE_BAIT 语义捷径，这是正确缺席）。
- **Reasoning**: 强 counterexample——看似需要新语义的 case 被运动学事实覆盖，验证了 identity-shortcut 禁令的可行性。

### H09｜Popping cork + 虾静态悬浮｜COVERED

- **Unseen class**: IN_FAMILY_UNSEEN（shrimp 家族；dev set 为 bottom hop；且本 config 声源≠攻击目标）。
- **Real strategy**（证据：[Salt Strong](https://www.saltstrong.com/fishing-tip/how-to-rig-popping-corks/)、[Sport Fishing Mag](https://www.sportfishingmag.com/fishing-with-popping-corks/)）：cork 爆音远距离召集（拟捕食搅动声），到访鱼就地吃静态虾；浑水尤其有效。
- **Observed facts**: sound_amplitude HIGH（RecentEventFact pop）@cork；虾: speed ZERO + apparent_size SMALL + vibration LOW；relation.surface（cork 在面）；leader 固定偏移几何。
- **Required Response distinction**: "远处声事件 + 就地静态小目标" vs 声源即目标的 popper。
- **Primary**: COVERED。**Flags**: MULTI_COMPONENT_ROUTINE_ANNOTATION / SOURCE_OFFSET_MINOR（声源与目标 ~2–4 ft 偏移在 opportunity 几何内，不影响 band 表达，仅 debug 层注意）。
- **Reasoning**: 与 H07 的精确界线——**异构组件（各贡献不同通道）→ 事实并集足够；同源集群信号 → 需合成规则**。多组件 item 本身不自动触发缺口。

### H10｜夜间 jitterbug 匀速水面爬行｜COVERED

- **Unseen class**: IN_FAMILY_UNSEEN（topwater；dev set 为 pop+pause；夜间场景未消费）。
- **Real strategy**: 黑夜恒定 gurgle 声轨迹让鱼锁定攻击；黑色低反光体色靠轮廓。
- **Observed facts**: sound_amplitude LOW-MED 恒定 + sound_pattern 匀搅节奏；direction_change ~NONE（直线）；relation.surface ON；visual_contrast effective LOW（夜，receiver-relative）。
- **Required Response distinction**: 声主导 rule（夜间成立）vs 昼间视觉主导。
- **Primary**: COVERED。**Flags**: LIGHT_DOUBLE_COUNT_RESOLVED_BY_EFFECTIVE_RECEIVER_RELATIVE_CUE。
- **Cause ownership**: §11 压力点"light / visibility double count"的实际裁决——`cue.visual_contrast` 是"当前**有效**刺激事实"（receiver-relative），光照已在 Cue Resolver 侧折叠；Response **不**读 context.light，无双算。所有权单点收干净。**Identity** ✓。
- **Reasoning**: R2 succeeds unexpectedly 的代表：光照压力被 receiver-relative 规则恰好化解。

### H11｜Drop-shot 原地微抖离底定悬｜COVERED

- **Unseen class**: CROSS_FAMILY_UNSEEN。
- **Real strategy**: 铅坠坐底、饵离底定悬，持续微抖竿尖——原地颤动、零位移、可无限期持守。
- **Observed facts**: speed ZERO；vibration_amplitude LOW 持续；vertical_motion HOLD；DurationFact VERY_LONG（定悬持续）；组件分工：坠=定锚（world geometry），饵=presentation（离底）。
- **Required Response distinction**: "原地持续微震 + 长时定悬" vs 游动 / 沉降。
- **Primary**: COVERED。**Flags**: ZERO_DISPLACEMENT_EXPRESSIBLE_WITHOUT_cue.displacement。
- **Reasoning**: 重要反例——预期最可能踩 `cue.displacement` 缺口的 case 实际由 speed ZERO + 持续 LOW 震动 + DurationFact 完整表达；**displacement 的 PROVISIONAL 状态在此不构成缺口**，为该 primitive 的准入决策提供了"非必要"证据。

### H12｜Bottom bouncer + crawler harness 拖底拖曳｜NEW_PRIMITIVE_REQUIRED

- **Unseen class**: CROSS_FAMILY_UNSEEN（walleye 物种出现，但污染条目是 low-light 故事；本 config 为白昼结构拖曳，exact config 未被消费）。
- **Real strategy**（证据：[In-Fisherman](https://www.in-fisherman.com/editorial/spinner-rig-bottom-bouncer-walleyes/364997)、[MidWest Outdoors](https://midwestoutdoors.com/fishing/positioning-secrets-crawler-harness-mastery/)）：L 形坠沿底爬行产生连续触底+底质扰动，前置 blade 闪光震动召唤，crawler 拖在底上提供气味；"持续拖 vs 间歇点触"是玩家真实选择变量。
- **What materially changes**: 鱼被**持续移动的底扰动迹**在远距离招募——与点源 blade 震动是两条通道。
- **R2 facts available**: cue.vibration_*（blade）✓；presentation.chemical_signature（crawler 类型）✓；relation.bottom CONTACT（瞬时）；DurationFact 可给接触时长（**部分路径**）。
- **部分路径为何不充分**（不作有利于 baseline 的解释）：
  1. 招募发生在扰动**迹**上：连续接触产生的 bottom disturbance plume（silt/碎屑/底质声）是传播型机械事实，baseline 无承载位；
  2. 仅靠 relation.bottom + DurationFact，"移动中持续接触（拖行）"与"静止持续贴底"不可区分——travel-while-contact 事实缺失；
  3. 这正是 KNOWN_DEV_GAP_CONTINUOUS_BOTTOM_CONTACT_MECHANICAL_CAUSE 所指能力。
- **Primary**: NEW_PRIMITIVE_REQUIRED（continuous-contact / bottom-disturbance mechanical cause——primitive 具体形态由 Design Owner 定：contact-continuity fact、disturbance-trace fact 或 displacement 族，本轮不预设解法）。
- **Requested deltas**: [continuous-contact mechanical signal primitive]。
- **Flags**: REPEATED_PRESSURE_ON_KNOWN_DEV_GAP (#1) / KNOWN_GAP_NOT_NOVEL_DISCOVERY / BASELINE_CHANGE_REQUIRED。
- **Cause ownership**: 底扰动迹属 Presentation/Cue（world-molecule）层，不得塞进 relation.* 硬编码，也不得混入 vibration_amplitude 伪造覆盖（那会把点源与迹两条通道合一，正是 double-count）。**Identity** ✓。
- **Reasoning**: 按 §5，这不是新发现——是已知缺口**首次获得独立 unseen 压力证据**。

### H13｜Football jig 沿石底拖磨（smallmouth）｜NEW_PRIMITIVE_REQUIRED

- **Unseen class**: CROSS_FAMILY_UNSEEN（jig+trailer 拖底未入 dev set）。
- **Real strategy**（证据：[Indiana Fishing Guide](https://www.indianafishing.guide/gear/football-jigs/)、[Coastal Angler](https://coastalanglermag.com/jig-fishing-february/)）：铁头在岩石上拖磨（grind/scrape 声 + 底扰动），trailer 蠕动跟随；**拖（拟小龙虾爬行、自然招募）vs 跳（反应触发）是两条玩家策略**。
- **What materially changes**: "drag vs hop"差异在 R2 现状下部分坍缩：hop 可由 RecentEventFact 表达 ✓；drag 的连续接触+刮磨迹缺事实 ✗。
- **部分可表达成分（诚实记录）**: 刮磨的**声学分量**可落 cue.sound_amplitude / vibration_amplitude（连续 LOW-MED 磨擦带）；但构成策略区分核心的"持续接触行进 + 扰动迹"仍缺。
- **Primary**: NEW_PRIMITIVE_REQUIRED（同 H12 能力族）。
- **Requested deltas**: [continuous-contact mechanical signal primitive]（与 H12 同一 delta，不重复计数）。
- **Flags**: REPEATED_PRESSURE_ON_KNOWN_DEV_GAP (#2) / BASELINE_CHANGE_REQUIRED。
- **Reasoning**: 两个独立真实策略（walleye crawler 拖、smallmouth football 拖）要求同一 semantic capability → 依任务 §5 记录 REPEATED_PRESSURE_ON_KNOWN_DEV_GAP，构成本轮最重要实验发现之一。

### H14｜Sheepshead 紧贴桩柱蟹型微饵｜ANNOTATION_ONLY

- **Unseen class**: CROSS_FAMILY_UNSEEN；feeding-target-sensitive 轴。
- **Real strategy**: 小 crab 拟饵/蟹腿直落桩边缝隙，微沉微动；sheepshead 靠结构+甲壳类食性；咬口极轻（strike detection 属下游）。
- **Observed facts**: apparent_size SMALL；speed LOW；vertical_motion SINK 微相；placement 紧贴结构（玩家技能/世界几何）。
- **Required Response distinction**: 为什么 sheepshead（而非同水域鲈鱼）高响应——由 Species × CRUSTACEAN 静态亲和承载，presentation 只需类型+运动学。
- **Primary**: ANNOTATION_ONLY。**Requested deltas**: [prey_stage/profile 字典新增 CRAB/CRUSTACEAN 值]（fish-neutral 字典 admission；shrimp 已在 dev set，crab 是新值）。
- **Flags**: FEEDING_TARGET_STATIC_AFFINITY_WORKS。
- **Cause ownership**: 结构贴合属 Bake/Opportunity 侧（鱼在哪），非 presentation relation——**不需要** relation.structure。**Identity** ✓。
- **Reasoning**: 静态亲和层分工正确的样板 case；代价仅 1 个字典值。

### H15｜Musky 船边 figure-8 急转｜COVERED

- **Unseen class**: CROSS_FAMILY_UNSEEN；non-feeding Engagement Mode 候选轴。
- **Real strategy**: 收线末端船侧大八字/圆环，跟随的 musky 在急转向瞬间触发攻击（aggression/reaction，非摄食）。
- **Observed facts**: figure-8 段 speed LOW + direction_change HIGH（急转 RecentEventFact）；近场 mid-water。
- **Required Response distinction**: 非摄食 Reaction 招募——R2 的 Response 是 pre-generation weighting：figure-8 的 pre-gen 贡献 = Reaction band 提升；**跟随/转身/攻击属 post-generation AI，出 Response scope（Scope Boundary R0）**。
- **Primary**: COVERED。**Flags**: NON_FEEDING_MODE_VIA_REACTION_CHANNEL / POST_GEN_SCOPE_NOTE。
- **Identity** ✓（"figure-8"是玩家操作名，resolved kinematics 承载语义）。**Ownership**: 不要求新 Engagement Mode——Generic Reaction 通道（R-T2）复用。
- **Reasoning**: 非摄食模式候选不自动升 Mode；与 dev set 的 Reaction 通道设计一致。

### H16｜Crankbait 涂 shad 气味凝胶｜COVERED

- **Unseen class**: CROSS_FAMILY_UNSEEN；chemical identity 轴。
- **Real strategy**: 同一拟饵加/不加饵味凝胶提升咬口——化学**类型**辅助，运动学不变。
- **Observed facts**: presentation.chemical_signature = SHAD_SCENT（有）vs NONE（无）。
- **Required Response distinction**: 有/无气味类型——Response rule: `chemical_signature IN {SHAD_SCENT}` 提升嗅觉主导鱼种的 band。
- **Primary**: COVERED。**Flags**: CHEMICAL_TYPE_BOUNDARY_WORKS。
- **Cause ownership**: 气味**羽流扩散**属 world molecule / Exposure 几何；signature 只载类型——分层干净。**Double-count** ✓。**Identity** ✓（凝胶 SKU 不进语义）。
- **Reasoning**: 证明 R2 刻意收窄的 chemical_signature（只载类型）对类型级使用**足够**；与 H17 形成化学轴的内外边界。

### H17｜鲶鱼 punch bait 浸泡时间衰减｜NEW_PRIMITIVE_REQUIRED（非 blind 发现）

- **Unseen class**: IN_FAMILY_UNSEEN_CONFIG；**Contamination: POSSIBLE_CONTAMINATION（家族级）**——chemical/scent feeder 故事已参与设计，且 Response Language Contract 14.1 显式推迟过 odor_concentration；exact config（新鲜度管理）未用于调参，但语义问题已被设计访问 → 按协议**不作为 blind discovery**，作为 confirmatory 压力证据；结果仍计入本轮。
- **Real strategy**: punch/dip bait 出水时气味浓、随浸泡衰减；玩家策略 = 定期 re-dip 维持新鲜气味羽流——**新鲜度是合法策略变量**。
- **What materially changes**: 同饵、同点，气味**浓度/可用性**梯度实质改变招募；类型不变。
- **R2 facts available**: chemical_signature 类型 ✓；**无浓度通道**（cue.chemical_intensity / cue.odor_concentration 明确未 admitted）。
- **Primary**: NEW_PRIMITIVE_REQUIRED（已具名 deferred candidate：cue.odor_concentration 族）。
- **Requested deltas**: [cue.odor_concentration / chemical magnitude primitive——准入与否是产品决策]。
- **Flags**: KNOWN_DEFERRED_CANDIDATE / POSSIBLE_CONTAMINATION_FAMILY / BASELINE_CHANGE_REQUIRED。
- **Cause ownership**: 羽流几何属 Exposure/Opportunity；到达鱼端的**有效浓度**属 Cue（若准入）——避免与 Exposure 双算。
- **Reasoning**: 确认 §11 压力点"chemical magnitude / availability"存在真实策略需求；非本轮新发现。

### H18｜Flatline 拖钓深潜 crankbait｜COVERED

- **Unseen class**: CROSS_FAMILY_UNSEEN；boundary 轴。
- **Real strategy**: 船速拖带定深泳层长距离覆盖。
- **What materially changes for player**: 覆盖面积/搜索效率（玩家侧）大幅变化；**鱼端感知的 presentation 事实不变**（匀速 wobble、定深）。
- **Observed facts**: speed 匀带 + vibration MED + vertical HOLD——与岸抛匀收同一 fact 组合。
- **Primary**: COVERED。**Flags**: STRATEGY_DIFF_LIVES_OUTSIDE_PRESENTATION_SEMANTICS。
- **Cause ownership**: 船迹/噪声是独立 world 事实，若要模拟船惊鱼属其它 owner（world/Bake 层），不是 presentation cue。**Identity** ✓。
- **Reasoning**: 正确 factorization 的边界证据——trolling vs casting 的策略差异属于搜索/暴露层，R2 **不需要也不应该**在 Presentation/Cue 里区分它们。

---

## C. Aggregate Metrics

### C.1 Classification 分布（18 cases）

```text
COVERED                      13  (H01 H02 H03 H04 H05 H06 H08 H09 H10 H11 H15 H16 H18)
ANNOTATION_ONLY               1  (H14)
DERIVED_DESCRIPTOR_ONLY       0
NEW_GENERIC_RULE_REQUIRED     1  (H07)
NEW_PRIMITIVE_REQUIRED        3  (H12 H13 H17 → 去重后 2 个 unique semantic family)
NEW_RELATION_REQUIRED         0
ITEM_SPECIFIC_EXCEPTION       0
UNRESOLVED                    0
CAUSE_OWNERSHIP_CONFLICT      0
```

**Blind-only 视图**（剔除 H17 的 POSSIBLE_CONTAMINATION 后 17 cases）：COVERED 13 / ANNOTATION_ONLY 1 / NEW_GENERIC_RULE 1 / NEW_PRIMITIVE 2（同一能力族）。blind 覆盖率（COVERED + ANNOTATION_ONLY）= 14/17 ≈ 82%。

### C.2 Vocabulary-growth metrics

```text
new primitive count                2 unique families
                                   ├─ continuous-contact / bottom-disturbance mechanical cause（H12+H13，独立双击）
                                   └─ chemical magnitude（H17，已具名 deferred candidate，非 blind 发现）
new derived descriptor count       0
new relation count                 0（relation.* 完全未被要求扩张——含 relation.cover/structure 的诱惑被正确拒绝）
new generic resolver rule count    1（多同源源 snapshot 合成；本轮单证据，标注 SINGLE_EVIDENCE_RULE）
manual annotation count            1 字典值（prey_stage/profile: CRAB）
item-specific exception count      0
unresolved count                   0
cause ownership conflict count     0（1 次准冲突——光照——被现有 receiver-relative 规则化解）

descriptor token count             baseline ≈19 admitted typed tokens → 请求 +2 primitive +1 rule +1 enum 值 = +4（≈21%）
single-use descriptor count        0；新增合成规则单证据（已 flag）
Fish × Descriptor direct-touch     0
per-descriptor Species/Mode fan-out 无 descriptor 获得 Species/Mode-specific Response rules；
                                   所有 rule 停留在 Species×Mode Profile 内对 typed facts 的通用组合
generic-rule fan-out               既有 rules 零改动；新增 1 rule 预期可跨 umbrella/daisy-chain/tandem 复用
```

### C.3 Kill Signals

```text
Kill Signal A（item count ↑ ≈ token count ↑）：未触发。
    18 个新 item → 4 个新 token 请求（其中 2 个是预先已识别的 deferred 项），
    真正本轮新发现的语义需求 = 1 个 primitive family（连续底接触）+ 1 条合成规则 + 1 个字典值。
Kill Signal B（descriptor 聚集 Species/Mode-specific Response rules）：未触发。
    全部 COVERED cases 经共享 generic 通道表达；无 descriptor 出现按鱼种分裂的响应规则。
```

**结论：无 degeneration 迹象；未出现 Item vocabulary 化或 Fish×Item matrix 回潮。**

---

## D. Counterexamples（最强 5 例）

1. **R2 succeeds unexpectedly — H11 drop-shot（零位移微震）**。最可能踩 `cue.displacement` 缺口的形态（原地抖动、零位移）实际由 speed ZERO + 持续 LOW vibration + DurationFact 完整表达。为 displacement 的 PROVISIONAL 状态提供了"并非普遍必要"的直接证据——准入决策需要比预期更强的理由。
2. **R2 succeeds unexpectedly — H08 活饵 shiner（无 LIVE 语义）**。活饵是现实中差异极大的内容族，R2 正确地不需要任何 "live" 语义：erratic 运动学事实 + prey_stage + 静态 FeedingTarget 亲和完整保留策略差异。identity-shortcut 禁令在真实压力下可行。
3. **R2 fails materially — H07 umbrella rig（集群 multiplicity 无定义）**。单一 presentation snapshot 语义未定义多同源源合成；集群轮廓/联合闪光/"攻击掉队者"的招募差异无法表达。这是本轮唯一**真正新颖**的语义缺口，修复路径窄（合成 rule，或 profile 字典 SCHOOL 值的退化方案）。
4. **Boundary ambiguous — H06 vs H12/H13（离散偏折 COVERED / 连续拖磨 NOT）**。同一"触底/触障"现象族在 R2 内外分界精确落在：**接触连续性 × 行进 × 扰动迹**。H06 的偏折=运动学事件（可表达）；H12/H13 的拖行=持续接触+传播型扰动（不可表达）。此外 DurationFact-on-relation.bottom 的部分路径会使"拖行"与"静止贴底"坍缩为同型——部分修复不充分。
5. **Boundary ambiguous — H16 vs H17（化学类型内 / 浓度外）**。chemical_signature 只载类型的刻意收窄，对类型级使用（涂凝胶）经 H16 验证足够；对浓度级策略（punch bait 新鲜度管理）经 H17 确认存在真实需求。化学轴的边界不是表示缺陷，而是**待产品决策的显式推迟**。

（附加正面证据：H10 显示光照双算压力被 receiver-relative effective contrast 单点化解——未列入前五因未产生实质边界。）

---

## E. Known-gap Repetition｜已知缺口复击报告

```text
KNOWN_DEV_GAP_CONTINUOUS_BOTTOM_CONTACT_MECHANICAL_CAUSE
→ REPEATED_PRESSURE_ON_KNOWN_DEV_GAP：确认（CONFIRMED）
```

- 两个**互相独立**的真实未见策略（H12 walleye bottom-bouncer crawler 拖曳；H13 smallmouth football-jig 拖磨）要求同一 semantic capability——不是等价重述，是不同内容族（live-bait 复合 rig / jig+trailer）独立命中。
- 边界被本轮**收紧**：
  - H04（软虫沉降、无底接触）COVERED——缺口不属于软虫家族本身；
  - H06（离散触障偏折）COVERED——缺口不属于"接触"本身；
  - H11（原地零位移微震）COVERED——缺口不属于微震或位移本身；
  - 精确缺口 = **移动中的持续接触 + 传播型底扰动迹**（recruitment-at-range），且 DurationFact-on-relation.bottom 部分路径不充分（drag vs static-contact 坍缩）。
- 同时记录：H17 确认 chemical magnitude 推迟项存在真实策略压力（非 dev gap，属显式 deferred candidate）。

---

## F. Verdict

```text
HOLDOUT_PASS_WITH_NARROW_DELTA
```

**理由**：

1. **主分解结构经受住盲测**：17 个 blind cases 中 14 个（82%）落在 COVERED / ANNOTATION_ONLY；0 UNRESOLVED、0 ITEM_SPECIFIC_EXCEPTION、0 CAUSE_OWNERSHIP_CONFLICT。presentation/cue/relation/state/context 的 namespace 分工、receiver/support-relative 几何规则、identity-shortcut 禁令、静态 FeedingTarget 亲和、RecentEventFact/DurationFact 时序合同均在未见真实策略上按设计工作。
2. **两个 Kill Signal 均未触发**：18 item → ~4 token（其中 2 个预已知）；无 descriptor 鱼种化。无退化证据。
3. **所需 delta 窄且集中**：
   - `continuous-contact / bottom-disturbance mechanical cause` primitive（已知缺口，本轮获得独立双击证据，边界已收紧）；
   - 多同源源 snapshot 合成 generic rule（本轮唯一真正新颖发现，单证据）；
   - 1 个 prey 字典值（CRAB）；
   - chemical magnitude 维持 deferred，等待产品决策（本轮确认有真实需求）。
4. **不判 HOLDOUT_PASS**：存在一个真实新颖语义缺口（H07）与一个已被独立证据加强的已知缺口（H12/H13），且两者都要求 Presentation/Cue 层 baseline 变更——超出"零 delta"标准。
5. **不判 HOLDOUT_REVISE / FAIL_FACTORIZATION**：缺口数量少、无单点连续击穿、无结构性退化；representation 的复杂度曲线在首回合表现健康。

### BASELINE_CHANGE_REQUIRED 汇总（本轮零修改，全部留待 Design Owner）

```text
H07 → 多同源源合成 rule（或 profile SCHOOL 字典值的退化方案）
H12 + H13 → continuous-contact / bottom-disturbance mechanical cause primitive（同一 delta）
H17 → chemical magnitude primitive（已具名 deferred candidate，产品决策）
H14 → prey_stage/profile 字典 CRAB 值（annotation 级，非语义变更）
```

### 本轮不证明什么（What this round does not prove）

- 不证明 rule resolution / aggregation / sampling / rate / calibration 算法（Language Contract 之外的 Algorithm 层）；
- 不证明数值标定与最终体验；
- 不证明 post-generation 行为（追击/攻击/挂钩）；
- **两个轴因污染被整体排除，仍未获得任何 blind 证据**：Carp pressure / cue familiarity；chum / groundbait 区域级化学（后者同时是潜在的 Presentation-vs-World-State ownership 冲突高风险区）。建议下一轮优先补这两轴；
- 按 Holdout Protocol §8：单轮不构成复杂度斜率证据；泛化主张需要**第二个独立 unseen round**。本轮任何 baseline 修改生效后，本批样本即转为 Development Set。

---

## 附：证据来源（case evidence only，非 semantic authority）

- [In-Fisherman – Umbrella Rigs](https://www.in-fisherman.com/editorial/umbrella-rigs/154044)｜[Wired2Fish – Alabama Rig](https://www.wired2fish.com/fishing-rigs/alabama-rig-how-to-fish-and-rig-it)（H07）
- [In-Fisherman – Spinner-Crawler Rigs on Bottom Bouncers](https://www.in-fisherman.com/editorial/spinner-rig-bottom-bouncer-walleyes/364997)｜[MidWest Outdoors – Crawler Harness Positioning](https://midwestoutdoors.com/fishing/positioning-secrets-crawler-harness-mastery/)（H12）
- [Salt Strong – How to Rig Popping Corks](https://www.saltstrong.com/fishing-tip/how-to-rig-popping-corks/)｜[Sport Fishing Mag – Popping Corks for Redfish & Seatrout](https://www.sportfishingmag.com/fishing-with-popping-corks/)（H09）
- [Indiana Fishing Guide – Football Jigs](https://www.indianafishing.guide/gear/football-jigs/)｜[Coastal Angler – Jig Fishing](https://coastalanglermag.com/jig-fishing-february/)（H13）

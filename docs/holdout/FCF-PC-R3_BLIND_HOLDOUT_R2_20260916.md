# FCF-PC R3 Blind Holdout Round 2｜独立盲测样本 + 泛化审查报告

```text
Round ID:        FCF-PC-BLIND-HOLDOUT-ROUND-2-20260916
Baseline ID:     FCF-PC-BASELINE-R3-20260916
Baseline sha256: f68bac2b78c3d23850478269f679eb9c9847b66168b7a196edf176992dcf6625
Baseline commit: 8221cf633fb9e89f10c8e0d5846bfe25b3e0b0e8 (branch feature/pc-cue-validation-r3-candidate)
Role:            Independent Holdout Reviewer / Sample Agent（未参与 R3 设计与裁决）
Round Date:      2026-09-16
Status:          COMPLETE / BLIND DISCIPLINE HELD（本轮零 baseline / validator / vocabulary 修改）
唯一目标:        检验 R3 窄 Delta（cue.contact_disturbance + cause provenance + composition resolver）在全新 unseen cases 上是否保持低边际复杂度
```

---

## 0. Round Validity｜可复现性与冻结验证

**阅读路径合规**（任务指定顺序，全部执行后 Stop）：

```text
FCF Router (Notion 3cca4137…9e47)
→ Project State Current (3cca4137…5e49)
→ Design Branch Index (3cda4137…84dd)
→ Simplified Production V0 Working Main (3cda4137…bd41)
→ Presentation Adapter Unseen Holdout Protocol v5 (3c7a4137…1cb92)
→ Stop
```

- Branch 确认：**Simplified Production V0 / Presentation / Cue validation**。未切换 FCF V1 或 Mainline authority。
- **Frozen baseline 独立验证通过**：从 `futouyiba/programaticHitFish` 本地 ref `origin/feature/pc-cue-validation-r3-candidate` 读取（网络 fetch 超时，但本地 ref head 逐字等于冻结 commit `8221cf63…`），对 `docs/pc_validation/FCF-PC-BASELINE-R3-20260916.md` 做 sha256：

```text
f68bac2b78c3d23850478269f679eb9c9847b66168b7a196edf176992dcf6625
```

与任务声明及 baseline.json 完全一致。Freeze ID / commit / sha256 三项一致，未触发 `ROUND2_BLOCKED_BY_BASELINE_TRANSPORT`。
- **Admitted vocabulary 口径**：以冻结 commit 的 `fcf_v1/pc_validation.py` 为准——admitted cue facts 13 项（apparent_size / visual_contrast / flash / speed / speed_change / direction_change / pause_duration / vertical_motion / vibration_amplitude / vibration_frequency / sound_amplitude / sound_pattern / **contact_disturbance(R3)**）；NOT_ADMITTED：displacement、source_count、lure_count；candidate：chemical_intensity（"?"）；CONTACT_CAUSE_FAMILY = {contact_disturbance, vibration_amplitude, vibration_frequency, sound_amplitude}（R3 ruling B，无布尔豁免）；lane-local FeedingTarget test vocabulary = {SMALL_BAITFISH, CRUSTACEAN}（ruling D，非 canonical）；composition resolver 禁止 source_count / rig_identity / sum / weighted_average / max / noisy_or（R3 §C + Delta 2）。
- **污染边界**：原 Frozen Development Set（DEV-001..010、DEV-S1..S5）、validator synthetic fixtures（SYN-01..27）、Round 1 全部 18 cases（H01..H18，已转 permanent Development）、R3 targeted / counterfactual fixtures、任何参与 R3 设计与裁决的具体案例、R1 污染清单条目（Bass jerk-pause、Spawn Guard Bass、Trout match hatch、Walleye low-light、chemical/scent feeder 故事、Carp pressure/cue familiarity 故事）。
- **选样独立性**：全部 case 身份由本 Agent 在冻结验证之后独立选定时序下确定，未与任何设计讨论对齐；外部钓法资料仅作 case evidence，不构成 semantic authority。
- **Blind discipline**：从第一例 reveal 到本报告提交，未修改任何 baseline / vocabulary / validator 语义 / annotation dictionary / classification 规则；未发生替换 hard case。本轮 **BASELINE_CHANGE_REQUIRED 计数为零**。
- **批处理披露**：本 run 为单 Agent 执行，选样（seal）与 reveal 在同一会话内按协议顺序完成（先冻结验证与污染清单，后选样，后统一 reveal 与逐案裁决）；无失败换样。

---

## A. Sample Manifest｜16 blind-valid + 2 confirmatory

选样覆盖任务 §6 全部 sampling axes；具体 Item / Species / Presentation 身份独立选择。

| ID | Case | 家族 | Contamination status | 主攻击轴 |
|----|------|------|----------------------|----------|
| HR2-01 | Lipless crankbait 扯穿 submerged grass 后 kill（鲈） | lipless crankbait | BLIND_VALID | Delta 1 泛化：植被接触；disc rip + die |
| HR2-02 | Pitched jig 下落中故意磕撞 standing timber（垂直木击） | jig | BLIND_VALID | Delta 1 泛化：垂直/离散 impulse |
| HR2-03 | Carolina rig 铅沿软泥底拖行（silt puff 迹） | C-rig | BLIND_VALID | Delta 1 泛化：软质底连续拖 + 底质诱惑 |
| HR2-04 | Hollow-body frog 走 matted vegetation（鲈） | topwater frog | BLIND_VALID | target ambiguity + FeedingTarget dictionary 压力 |
| HR2-05 | Chugger 水面 cadence 策略：chug-chug-停 vs 连续 chug | topwater | BLIND_VALID | cue.sound_pattern 盲压（R3 §E） |
| HR2-06 | Dry-dropper 双飞（dry 诱饵+指示器 / nymph 目标） | fly | BLIND_VALID | Delta 2：异构多源 union |
| HR2-07 | Flasher + fly 拖钓（三文鱼） | troll attractor | BLIND_VALID | Delta 2：耦合吸引子；flash 周期性 |
| HR2-08 | Texas rig + brass-and-glass clacker（组件内撞击声） | soft worm | BLIND_VALID | provenance：组件内接触 vs world-geometry scope |
| HR2-09 | Deep-drop rig：glow sleeve + cut squid（600–1200 ft） | 深海底钓 | BLIND_VALID | 混合通道；极端深度光学；glow 诱惑 |
| HR2-10 | 夜间 drift 活鳗（条纹鲈） | 活饵 | BLIND_VALID | partial unknown；live 边界二次验证 |
| HR2-11 | 冰钓 micro-jig 微颤（perch / lake trout） | ice jig | BLIND_VALID | context-sensitive（冰下几何）；IN_FAMILY_UNSEEN vs H02 |
| HR2-12 | Glide bait 缓速 wake（水面Wake+gurgle 同因） | glide/swimbait | BLIND_VALID | cause provenance：单因双感官 |
| HR2-13 | 高压 flats bonefish（安静入水 + 慢爬） | flats fly | BLIND_VALID | state/history 边界（pressure/familiarity 轴，R3 §3 建议） |
| HR2-14 | Dipsey diver / diving planer 前置（拖钓） | 拖钓设备 | BLIND_VALID | Delta 2：设备组件 + rig_identity 诱惑 |
| HR2-15 | Surf pencil popper（浪区背景噪声） | surf topwater | BLIND_VALID | receiver-relative 第二模态（声掩蔽） |
| HR2-16 | 河流底层浸泡 cut herring 钓鲟（化学主导静止） | cut bait | BLIND_VALID | 化学类型 + plume ownership + 零运动负空间 |
| HR2-C1 | Tuna spreader bar（同源集群 teasers + stinger） | 集群拖钓 | **CONFIRMATORY_CONTAMINATED**（H07 umbrella 家族级） | composition 泛化 confirmatory；CF-MULTI-1 复击 |
| HR2-C2 | Berley/chum trail 钓 snapper | 区域化学 | **POSSIBLE_CONTAMINATION**（axis 已被 R1 访问并推迟；R3 §3 点名建议） | plume ownership confirmatory；chemical magnitude 复击 |

主动排除：任何 dev set / Round 1 / SYN fixture case 的轻微改名版本；Spawn Guard、Hot Bass、Front、Trout match hatch、Walleye low-light、Carp、chum（除 C2 显式 confirmatory 外）、Bass jerk-pause 家族 exact config。

---

## B. Per-case Results

分类集合与决策顺序同 Round 1：`CAUSE_OWNERSHIP_CONFLICT → UNRESOLVED → minimal sufficient semantic delta`。

### HR2-01｜Lipless crankbait 扯草 + kill｜COVERED

- **Source evidence**: [Bassmaster – Ripping Traps in Grass](https://www.bassmaster.com/how-to/news/ripping-traps-in-grass/)、[Googan Squad – Rip Lipless Crankbaits Through Grass](https://googansquad.com/blogs/bass-fishing-guide/how-to-rip-lipless-crankbaits-through-spring-grass)、[Kraken Bass – Lipless Crankbait Guide](https://krakenbass.com/lipless-crankbait/)
- **Blind validity**: BLIND_VALID。lipless 家族整体未入 dev set / Round 1；"rip through grass then die" exact config 未被任何 fixture 消费。Flag: DELTA1_AXIS_PRE_VISITED（R3 Delta 1 针对 bottom contact 设计；植被接触是其泛化面）。
- **Real player strategy**: 让无唇拟饵穿行草顶，故意挂草后瞬间爆发扯离（reaction 触发），随后 kill 停摆（fleeing/trapped baitfish 模拟）——"挂-扯-死"三段式是独立于匀速回收的真实策略。
- **Observed presentation facts**: 穿行段 speed MED-HIGH（LOCAL_WATER）+ vibration_amplitude HIGH（rattle）+ flash MED；挂草段 contact_disturbance MED-HIGH（lure-grass contact，sustained 短程）+ speed_change HIGH + direction_change HIGH（RecentEventFact 扯离爆发）；kill 段 speed ZERO + pause_duration LONG + vibration/flash 归零。
- **Relevant R3 facts**: cue.contact_disturbance（植被接触）——R3 ruling A 的负空间检查：case 不要求 contact_disturbance_type / scrape_pattern / vegetation_rub；movement 由 motion facts、duration 由 DurationFact 承载，与冻结语义一致。
- **Required gameplay distinction**: 扯草循环 vs 干净匀速回收 vs 单纯 kill——contact_disturbance 事件 + RecentEventFact + pause 组合区分三态。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: DELTA1_GENERALIZES_TO_VEGETATION / RULING_A_NEGATIVE_SPACE_RESPECTED。
- **Cause ownership**: grass contact（contact_disturbance + 草摩擦声）与 rattle（内部机构声）是**两个独立 cause**——同一 rule 若同时消费 sound_amplitude 与 contact_disturbance 必须以 cause identity 声明独立性；正确 authoring 是 rattle→vibration、grass→contact_disturbance 分开。**Double-count** ✓ 无。**Identity-shortcut** ✓（"lipless/rattle"不入鱼语义）。
- **Reasoning**: R3 新事实在植被介质上即取即用，未诱发任何植被子词汇；撕扯爆发与 kill 由既有时序合同承载。这是 Delta 1 泛化的第一个正向证据。

### HR2-02｜Pitched jig 磕撞 timber｜COVERED

- **Blind validity**: BLIND_VALID。jig 家族在 H13（拖磨）入 Development，但"pitch 入立木、下落中垂直磕撞"exact config 未被消费。Flag: DELTA1_AXIS_PRE_VISITED。
- **Real player strategy**: 向立木/桥柱精准 pitch，让饵在下落中撞木头发出 knock——离散撞击是招募信号本身，不是意外。
- **Observed facts**: 下落段 vertical_motion SINK（WORLD_VERTICAL）+ speed LOW-MED；撞击瞬间 contact_disturbance HIGH（离散 spike）+ sound_amplitude spike + direction_change MED（偏转）（RecentEventFact）；撞击间隙 pause/fall。
- **Relevant R3 facts**: contact_disturbance 离散 impulse。R3 ruling A 明确不冻结 composite temporal enum（CONTINUOUS_WHILE_MOVING / MOMENTARY_IMPULSE / STATIC_CONTACT 未准入）——本 case 是对该裁决的直接压力：离散/连续差异由 magnitude + DurationFact + 既有 motion facts 表达，**不需要** MOMENTARY_IMPULSE 枚举。
- **Required gameplay distinction**: 有磕撞 vs 干净下落——contact_disturbance spike + RecentEventFact 区分。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: DISCRETE_IMPULSE_NO_TEMPORAL_ENUM_NEEDED（冻结裁决 A 的确认证据）。
- **Cause ownership**: knock 的 contact_disturbance 与 knock 声**同一 cause**（木击）→ CONTACT_CAUSE_FAMILY 纪律：rule 只消费其一（contact_disturbance），声作为其可观察伴随不二次计权。**Double-count**：若无 provenance 纪律会自然双算——机制正确强制单消费。**Identity** ✓。
- **Reasoning**: H06（R1）证明离散偏折不需要新能力是在无 contact_disturbance 时代；本 case 证明加入 R3 事实后离散撞击**同样不诱发枚举词汇**，冻结裁决被盲例确认。

### HR2-03｜Carolina rig 软泥拖行（silt puff）｜COVERED

- **Source evidence**: [Game & Fish – Crash Course: Carolina Rig](https://www.gameandfishmag.com/editorial/crash-course-carolina-rig-bass-fishing/549323)、[Wired2Fish – The Carolina Rig](https://www.wired2fish.com/fishing-rigs/the-carolina-rig-how-to-rig-and-fish)
- **Blind validity**: BLIND_VALID。C-rig（pegged 铅 + leader + 浮性软饵）整体未入 dev/Round 1；与 H12（bottom bouncer + crawler）、H13（football jig）无相同 item/config。Flag: DELTA1_AXIS_PRE_VISITED。
- **Real player strategy**: 重铅贴底低姿慢拖，在软泥/黏土底犁出 silt puff 迹，鱼被扰动迹招募而来，就地吃 leader 后端的浮性软饵——"拖 vs 跳"与 H13 同构但介质（软泥）与组件分工不同。
- **Observed facts**: 铅：contact_disturbance MED continuous（temporal_scope 拖行时段）+ speed LOW（ground-relative，frame 已声明）；软饵：speed LOW + vertical_motion BOTTOM/HOLD + apparent_size MED；异构组件各自 source-local facts。
- **Relevant R3 facts**: 本 case 直击任务 §7 禁止清单的 `substrate_specific_disturbance / mud_disturbance` 诱惑——**未触发**：游戏区分（软泥犁行 vs 硬底点触 vs 跳跃）由 contact_disturbance 的 magnitude × DurationFact × motion facts 表达；底质身份（mud/rock）只影响 debug/annotation 层，不是鱼独立可解析语义。扰动迹的远距招募 = medium_propagation 几何折叠（GEOMETRY_INPUT_TOKENS 允许），cue 侧保持 at-source fact。
- **Required gameplay distinction**: 拖行（连续扰动迹）vs 跳跃（离散脉冲）vs 纯静止——已由 H13→R3 路径覆盖；软泥不新增语义。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: SUBSTRATE_DESCRIPTOR_TEMPTATION_DECLINED / DELTA1_GENERALIZES_TO_SOFT_SUBSTRATE / HETEROGENEOUS_COMPONENT_UNION。
- **Cause ownership**: 铅扰动与软饵运动学独立 cause，分属不同 source，无同 rule 重复消费。**Double-count** ✓。**Identity** ✓。
- **Reasoning**: 这是 Delta 1 泛化最重要的证据之一——R3 恰好购买"moving contact generates resolved disturbance"这一句话，软泥 puff 场景零扩展词汇即被吸收；`mud_disturbance` 类 descriptor 的准入请求在盲压下未成立。

### HR2-04｜Hollow-body frog 走 mat｜ANNOTATION_ONLY

- **Source evidence**: [Game & Fish – Topwater Froggin' Game Plan](https://www.gameandfishmag.com/editorial/bass-crash-course-frog-baits/496259)、[Major League Fishing – Froggin' Tips](https://majorleaguefishing.com/tips/become-a-frog-prince-with-these-hot-froggin-tips/)、[Tackle Warehouse – Hollow Body Frogs](https://www.tacklewarehouse.com/bass-fishing/gear-guides/hollow-body-frog-patterns-techniques-for-bass-fishing.html)
- **Blind validity**: BLIND_VALID。frog/mat config 未入任何 fixture；Spawn Guard / 其它 dev 故事无重叠。FeedingTarget 字典压力轴是 R3 §D 作用域声明的直接测试面。
- **Real player strategy**: 无配重 frog 直拖过草垫顶层，walk-the-dog 小幅走动；鱼从垫下 attacking 穿垫攻击。目标身份高度歧义（frog/rat/落水小鱼皆可）——玩家真正在意的差异是"垫顶扰动 + 鱼是否对两栖/陆源猎物有静态亲和"。
- **Observed facts**: relation.surface ON（垫顶层）；contact_disturbance LOW-MED continuous（lure-mat 顶部接触，与 HR2-01 植被接触同族但持续型）；speed LOW + direction_change MED（walk）；sound_amplitude LOW-MED（穿垫闷响）；visual_contrast effective LOW（鱼经垫观察，receiver-relative 折叠）；apparent_size MED。
- **Relevant R3 facts**: TargetResolutionStatus = HYPOTHESES（多类型猎物假设并存）；响应不需要消歧——静态 Species × FeedingTarget 亲和承载身份偏好。
- **Required gameplay distinction**: 为什么鲈（而非同水域只吃鲫鱼的鱼）高响应——亲和轴承载；垫顶扰动行为由既有通道表达。
- **Primary**: ANNOTATION_ONLY。**Deltas**: [FeedingTarget dictionary 值 AMPHIBIAN（或等价两栖/陆源小型脊椎动物值）——fish-neutral 字典 admission，canonical 权威在 FeedingTarget dictionary contract，不属本 lane 语义变更]。
- **Flags**: FEEDING_TARGET_DICTIONARY_PRESSURE / CRUSTACEAN_REUSE_NOT_DEFENSIBLE / TARGET_AMBIGUITY_ABSORBED_BY_AFFINITY / DELTA1_REUSED_SUSTAINED_VARIANT。
- **Cause ownership**: contact_disturbance（垫摩擦）与 sound（闷响）同 cause（垫上拖动）→ 单消费纪律。**Identity** ✓。**Double-count** ✓。
- **Reasoning**: 与 H14 的关键差异：R3 ruling D 让 crab 复用 CRUSTACEAN，但 frog 复用 CRUSTACEAN 是语义失真——字典压力真实且不可复用规避。按 R3 §D 分工，这是 annotation 级请求（进 canonical 字典 admission 流程），不是 lane baseline 语义变更。H13 之后的第二个植被接触变体（sustained 型）同时确认 temporal enum 未被需要。

### HR2-05｜Chugger cadence：chug-chug-停 vs 连续 chug｜COVERED

- **Source evidence**: [Megabass – How to Fish Walking Topwater Lures](https://megabassusa.com/how-to-fish-walking-topwater-lures/)、[Game & Fish – Chuggers](https://www.gameandfishmag.com/editorial/chugger-still-one-of-the-best-topwaters-for-bass/333642)、[BassResource – Topwater Cadence](https://www.bassresource.com/bass-fishing-videos/topwater-cadence.html)
- **Blind validity**: BLIND_VALID。chugger 家族未入 dev/Round 1（dev 有 popper pop DEV-009、H03 walker、H10 jitterbug；chugger 的 cadence-dial config 未消费）。
- **Real player strategy**: 同一支 chugger，cadence 是玩家主旋钮：浑水/消极鱼用 chug-chug-长停（单点轰炸），清水/_active 鱼用连续高频 chug 覆盖搜索——**幅度相同、节奏不同**。
- **Observed facts**: 爆停式：sound_pattern = 节奏（burst 频带）+ sound_amplitude MED（spike ×3）+ pause_duration LONG；连续式：sound_pattern = 稳态 + sound_amplitude LOW-MED 恒定 + pause_duration LOW。speed / direction_change / relation.surface 两侧相同。
- **Relevant R3 facts**: cue.sound_pattern 的独立盲压（R3 §E：当前仅 EXERCISED_BY_DEVELOPMENT_CASE / H10）。对抗性自查：能否用 pause_duration + sound_amplitude 表达？不能——段内节奏（3 快 chug 后停 vs 单 chug 后停；pop 3 Hz vs 1 Hz）在 amplitude、pause、speed 全同时仍不同，**只有 sound_pattern 承载**。
- **Required gameplay distinction**: 节奏拨盘不等于幅度或停顿拨盘——sound_pattern 的必要性证据。
- **Primary**: COVERED（sound_pattern 已 admitted）。**Deltas**: 无。**Flags**: SOUND_PATTERN_BLIND_EXERCISE（首个独立盲压证据，支持但不足以单案宣判 NECESSITY_VALIDATED）。
- **Cause ownership**: chug 声与 wake 视觉同 cause（水面排水）；本 case 的 rule 只消费声学通道，无双算。**Identity** ✓。
- **PROVENANCE_SCOPE_NOTE（上报，非修改）**: 冻结 validator 的 CONTACT_CAUSE_FAMILY = {contact_disturbance, vibration_amplitude, vibration_frequency, sound_amplitude}，**不含 sound_pattern**。若某 rule 同 rule 消费 sound_amplitude + sound_pattern（同一声学事件的幅度与节奏），family 检查不会提示声明 cause identity。本 case 正确 authoring 将二者视为一个声学通道的一次读取，无实际冲突；此为 family 清单的 scope 观察，留 Design Owner 裁决，本轮不做任何修改。
- **Reasoning**: sound_pattern 从"开发集使用过"升级为"盲策略差异独立命中"——正是 R3 §E 要求的第二轮证据形态。

### HR2-06｜Dry-dropper 双飞｜COVERED

- **Blind validity**: BLIND_VALID。fly 家族 dev 消费 dead drift（DEV-007）+ twitch；H05 swing 已转 Development。双飞 rig（dry=诱饵/指示器 + nymph=目标）exact config 未消费。Flag: 多源异构语义问题曾在 H09 访问（异构→并集），披露为 SEMANTIC_QUESTION_PRE_VISITED_R1。
- **Real player strategy**: 干式浮飞同时承担诱饵与咬口指示，nymph 在下水层 dead drift——两条 source-local 表现并存，鱼可分别攻击任一。
- **Observed facts**: dry source：relation.surface ON + visual_contrast MED + speed ~ZERO（water-relative，frame 声明）+ twitch 时 speed_change spike；nymph source：vertical_motion HOLD/SINK + speed ~ZERO（water-relative）+ apparent_size SMALL。
- **Required gameplay distinction**: 双机会并存 vs 单飞——并集即可，两 source 各自成为独立 opportunity，无需知道它们物理相连。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: MULTI_SOURCE_HETEROGENEOUS_UNION / NO_RIG_IDENTITY_NEEDED（连线是 angler mechanics，非鱼语义）。
- **Cause ownership**: 两 source 完全独立 cause；无双算。**Identity** ✓。
- **Reasoning**: composition resolver（R3 §C）的确定性 per-source 解析在此直接适用：0..N source-local facts → canonical snapshot，不触发 source_count 也不触发聚合规则。H09 的"异构→并集"结论在 fly 介质上盲复现。

### HR2-07｜Flasher + fly 拖钓｜COVERED

- **Source evidence**: [Ace Charters – Keys to Fishing Flasher Flies](https://www.acecharters.com/fishing/fishing-flasher-flies/)、[Island Fisherman – Choosing a Flasher](https://islandfishermanmagazine.com/choosing-the-right-flasher/)、[Fish Hawk – Mastering Flasher-Fly Programs](https://fishhawkelectronics.com/blog/mastering-flasherfly-programs-for-great-lakes-salmon-with-captain-chris-ingalls/)
- **Blind validity**: BLIND_VALID。flasher/attractor 组件与"机械耦合驱动尾饵"结构未入任何 fixture。Flag: SEMANTIC_QUESTION_PRE_VISITED_R1（H09 异构并集）。
- **Real player strategy**: 旋转 flasher 产生周期性 flash + 低频 thump 远距招募，尾随 fly 被其涡流带动做 erratic 动作——吸引子与攻击目标分工明确，玩家拨盘 = flasher 旋转速度/尺寸。
- **Observed facts**: flasher source：flash HIGH（旋转周期性）+ vibration_amplitude MED + vibration_frequency（随旋转速度走）+ direction_change LOW periodic；fly source：speed MED erratic + direction_change MED + apparent_size SMALL + visual_contrast LOW。
- **Required gameplay distinction**: 有/无吸引子（flash 全 0 vs HIGH）；旋转速度拨盘 → **vibration_frequency + flash 幅度组合承载**，不需要 visual_pattern 类新 descriptor。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: HETEROGENEOUS_COUPLED_COMPONENTS_UNION / ROTATION_PERIODICITY_ABSORBED_BY_VIBRATION_FREQUENCY / CAUSAL_COUPLING_NOT_NEEDED_FISH_SIDE。
- **Cause ownership**: flasher 的 flash 与 vibration **同 cause**（旋转板）——flash 不在 CONTACT_CAUSE_FAMILY，validator 不强制提示；正确 authoring 将二者以同一 cause identity 声明、各模态计权一次（多模态整合 ≠ 双算）。**Identity** ✓。
- **OBSERVATION（非请求）**: 纯视觉周期性且无声学伴随的场景（如频闪 LED 拟饵）未被本轮真实策略命中，`visual_pattern` 负空间保持未压状态，仅记录。
- **Reasoning**: 耦合组件的因果链（flasher 使 fly 动）对鱼不可感知也无需感知——resolver 侧 per-source 事实已完整；玩家拨盘经已 admitted 的频率/幅度通道表达，零词汇增长。

### HR2-08｜Texas rig + brass-and-glass clacker｜COVERED

- **Source evidence**: [BassResource – Texas Rigged Worm](https://www.bassresource.com/fishing/worm-fishing-1.html)、[r/bassfishing – brass & glass clicking](https://www.reddit.com/r/bassfishing/comments/bg7pvs/most_versatile_bait_in_my_opinion/)
- **Blind validity**: BLIND_VALID。soft worm 家族 dev 消费 bottom drag（H04 沉降）；brass-and-glass 组件音未消费。
- **Real player strategy**: 铅与玻璃珠在抽动/跳底时互击发出 crawdad 式 click， stained 水中用声招募——**组件内部接触**产生的声音，与底接触无关。
- **Observed facts**: worm：speed LOW hop + vertical_motion + apparent_size SMALL-MED；clack：sound_amplitude MED spike + vibration spike（RecentEventFact，伴随每次 hop）；铅触底：contact_disturbance LOW spike（world-geometry contact）。
- **Relevant R3 facts**: **scope 边界验证**——contact_disturbance 的语义是"moving contact with **world geometry**"；bead strike 是组件-组件接触，其表达正确落入 sound/vibration 通道而非 contact_disturbance。若 authoring 误用 contact_disturbance 表达组件内撞击即越界，本 case 提供了清晰的负空间标定。
- **Required gameplay distinction**: 有 clacker vs 无声配重——sound/vibration 事件差异。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: COMPONENT_INTERNAL_CONTACT_OUT_OF_CONTACT_DISTURBANCE_SCOPE / PROVENANCE_MECHANISM_EXERCISED。
- **Cause ownership**: clack 的 sound + vibration **同一 cause**（珠击），二者均在 CONTACT_CAUSE_FAMILY → 机制强制单消费（rule 只读其一），正确表达一次声-机刺激。底触的 contact_disturbance + 触底声同理单消费。**Double-count**：被 provenance 纪律干净阻断。**Identity** ✓。
- **Reasoning**: R3 Delta 1 + ruling B 的组合在本 case 上同时展示了"该用的地方"（底触）与"不该用的地方"（组件内击）——scope 纪律在盲压下自洽。

### HR2-09｜Deep-drop glow sleeve + cut squid｜COVERED

- **Source evidence**: [Sport Fishing Mag – Deep-Drop Fishing with Electric Reels](https://www.sportfishingmag.com/deep-drop-fishing-with-electric-reels/)
- **Blind validity**: BLIND_VALID。深海 electric-reel 底钓、glow 附件、600–1200 ft 场景均未入任何 fixture。
- **Real player strategy**: 近零光深度的光学策略：glow sleeve 余晖 + cut squid 化学类型 + 铅触底机械提示，三通道混合招募；玩家拨盘 = glow 充能状态（收线回充，随时间衰减）。
- **Observed facts**: visual_contrast effective HIGH（自发光在暗背景，receiver-relative + background 折叠），随 glow 衰减降到 MED/LOW（按时间快照取值）；chemical_signature = SQUID/CUT_BAIT 类型；铅触底 contact_disturbance + sound spike（同 cause，单消费）；speed ZERO（静置）+ DurationFact。
- **Required gameplay distinction**: glow vs 无 glow、新充能 vs 将耗尽——**同一字段的取值时间序列**，无新字段。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: GLOW_ABSORBED_BY_EFFECTIVE_RECEIVER_RELATIVE_CONTRAST / NO_LIGHT_INTENSITY_PRIMITIVE_NEEDED / MIXED_CHANNEL_UNION。
- **Cause ownership**: 三通道三 cause，独立声明；触底机械对单消费。**Identity** ✓（glow 套管 SKU 不入语义）。**Double-count** ✓。
- **Reasoning**: H10 的 receiver-relative 光学折叠在极端深度环境盲复现；"glow"这个表面像新 primitive 的属性被证明是 effective visual_contrast 的取值——derived descriptor temptation 被拒绝的样板。

### HR2-10｜夜间 drift 活鳗｜COVERED

- **Source evidence**: [The Fisherman – Nighttime Stripers: Live Eeling Done Right](https://www.thefisherman.com/article/nighttime-stripers-live-eeling-done-right/)、[The Tackle Room – How to Fish a Live Eel](https://thetackleroom.com/blogs/news/how-to-fish-a-live-eel-for-striped-bass-rigging-presentation-and-night-tactics)、[On The Water – Monster Bass Tactics](https://onthewater.com/monster-bass-tactics)
- **Blind validity**: BLIND_VALID。活鳗 night drift config 未消费。Flags: LIVE_QUESTION_PRE_VISITED_R1（H08 已裁"live 无需语义"）；NIGHT_CONTEXT_PRE_EXERCISED_H10。
- **Real player strategy**: 上流 drift 1.5–2.5 kn，鳗自主蛇行游动；玩家的拨盘是漂速与结构线选择，活物确切运动在 authoring 时**部分不可知**。
- **Observed facts**: speed LOW-MED（water-relative，band 声明）+ direction_change HIGH intermittent（蛇行，band 表达，非精确轨迹）；apparent_size MED（细长 profile）；chemical_signature = EEL_SLIME 类型；visual_contrast effective LOW（夜）。
- **Relevant R3 facts**: partial unknown 的合法表达：typed band facts（不硬猜精确值）+ TargetResolutionStatus 机制；未知部分保持 UNKNOWN，不压 0（Protocol §9 Unknown intolerance 红线）。
- **Required gameplay distinction**: 活饵 erratic vs 拟饵匀速——运动学 band + 化学类型区分，无需 "live" 语义（H08 边界在第二个活饵物种上复现）。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: PARTIAL_UNKNOWN_EXPRESSIBLE_VIA_TYPED_BANDS / LIVE_PROVENANCE_AGAIN_NOT_NEEDED。
- **Cause ownership**: 蛇行尾流（Exposure 侧）与黏液羽流（Exposure 侧）不入 cue rule。**Identity** ✓。
- **Reasoning**: typed missing / band 化是 baseline 的既有能力，本 case 验证其在"上游数据天然不可完全解析"场景的诚实退化路径。

### HR2-11｜冰钓 micro-jig 微颤｜COVERED

- **Source evidence**: [In-Fisherman – Ice Fishing Lake Trout](https://www.in-fisherman.com/editorial/ice-fishing-lake-trout/153710)、[Mack's Lure – Ice Fishing Jigging](https://mackslure.com/blogs/mack-attack/ice-fishing-how-to-locate-fish-and-effective-jigging-techniques)
- **Blind validity**: BLIND_VALID。ice 场景与 micro-quiver config 未消费（H02 是开阔水垂直勺）。Flags: IN_FAMILY_UNSEEN_CONFIG vs H02；DARK_WATER_CONTEXT 与 H10 光轴相邻（披露）。
- **Real player strategy**: 冰孔内垂直微颤（quiver）+ 死停交替，glow/亮片在暗水承担光学；鱼只能从下方/侧方接近（几何约束）。
- **Observed facts**: vibration_amplitude LOW 恒定（quiver）+ vertical_motion SINK/HOLD（WORLD_VERTICAL）+ speed LOW + flash LOW-MED + visual_contrast effective + pause_duration（死停）。
- **Required gameplay distinction**: 微颤 vs 大抽停 vs 匀沉降——amplitude/speed_change/pause 组合区分（H02 既有路径）。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: CONTEXT_OUT_OF_LANE_GEOMETRY（冰下仅垂直接近属 Bake/Opportunity 层，非 presentation 语义）。
- **Cause ownership**: 无多因叠加。**Identity** ✓。
- **Reasoning**: 轻量证据：context-sensitive 轴的"正确失格"样本——环境几何约束留在世界层，presentation 快照无缺口。

### HR2-12｜Glide bait 缓速 wake｜COVERED

- **Blind validity**: BLIND_VALID。glide/wake config 未入任何 fixture（H15 musky 是 figure-8，不同 case；物种重叠不构成污染，R1 H12 先例）。
- **Real player strategy**: 黎明浅水缓速直拖大 glide，体表推开水面形成连续 wake + gurgle——**同一物理过程**产生视觉尾波与声响，招募 + 触发并行。
- **Observed facts**: relation.surface ON + speed LOW-MED steady + direction_change LOW（S 弯）+ sound_amplitude LOW-MED continuous gurgle + apparent_size 偏大（wake 放大的水面投影，receiver-relative）。
- **Required gameplay distinction**: 水面 wake vs 水下直拖 vs 抽停——surface + 声 + 投影组合区分。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: SINGLE_CAUSE_DUAL_ASPECT_FORCES_SINGLE_CHANNEL_CONSUMPTION / PROVENANCE_MECHANISM_EXERCISED / KILL_SIGNAL_C_OBSERVATION_POINT。
- **Cause ownership**: wake 视觉畸变与 gurgle 声**同一 cause identity**（体表排水）。对抗性检查：一个"wake profile rule"同时计权 sound + visual 是否构成双算？——按 R3 ruling B 属同一 cause 二次计权，**正确 authoring 只消费其一**（声）+ relation.surface + speed 承载几何；游戏区分度无损失。apparent_size 不在 family 清单内，其 wake 放大属于几何投影而非"事件重复计权"，无冲突。**Identity** ✓。
- **Reasoning**: 本 case 是 Kill Signal C 的核心观察点：单因双感官场景是否迫使每个 item 发明专属 cause taxonomy？实测不需要——cause identity 就是平凡的物理事件描述（"lure body displacing surface water"），一行 provenance，零 taxonomy 增长。

### HR2-13｜高压 flats bonefish｜COVERED

- **Blind validity**: BLIND_VALID。bonefish flats 与 pressure/familiarity 轴的具体 case 未入任何 fixture。该轴是 R3 §3 显式留给 Sample Agent 的建议轴；R1 的 Carp pressure/familiarity **故事**是污染条目，本 case 是不同物种/不同 config 的独立内容，且裁决结论不同（见下）。
- **Real player strategy**: 高钓压 flat 上的骨鱼需要 40+ ft 远投、长 leader、入水无声、超慢爬——策略差异同时存在于 presentation（更安静/更慢/更远）与**鱼侧状态**（警觉阈值升高）。
- **Observed facts**: 入水 splash：sound_amplitude LOW-MED 瞬态 spike（RecentEventFact）+ 慢爬 speed LOW + visual_contrast effective LOW（长 leader 小饵）+ support-relative 前置距离（geometry 输入）。
- **Required gameplay distinction**: presentation 侧：安静 vs 常规入水、慢 vs 快——全部可表达。鱼侧：警觉/习惯化改变响应阈值——**不属 Presentation/Cue lane**（鱼侧 state owner；同 H18 边界先例）。
- **Primary**: COVERED（对 lane 而言）。**Deltas**: 无。**Flags**: PRESSURE_FAMILIARITY_OUT_OF_LANE_SCOPE / R3_S3_AXIS_ATTACKED（给出盲证据：presentation 层不需要 pressure/familiarity admission；鱼侧是否需要属其它 owner，lane 不裁决）。
- **Cause ownership**: 无叠加。**Identity** ✓。
- **Reasoning**: R3 §1"Pressure / cue familiarity 未验证"在 presentation 侧获得第一个盲边界证据：该语义**正确缺席**——警觉是鱼-世界历史，不是 bait 的感官事实；把它塞进 cue vocabulary 正是 identity-shortcut 反模式。

### HR2-14｜Dipsey diver 前置拖钓｜COVERED

- **Blind validity**: BLIND_VALID。diving planer 组件未入任何 fixture。
- **Real player strategy**: 潜水板把线带到侧向与深度，自身产生持续 planing 震动与水流痕迹，有的鱼会攻击 diver 本体；后方才是目标饵。
- **Observed facts**: diver source：vibration_amplitude MED（planing）+ direction_change MED（侧向恒偏，frame 声明）+ speed trolling band；lure source：speed + flash + 常规通道；两 source 空间偏移（leader 几何）。
- **Required gameplay distinction**: 有/无 diver、diver 自身信号强弱——per-source facts 并集。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: NO_RIG_IDENTITY_NEEDED（"diver"不入语义，resolved facts 全承载）。
- **Cause ownership**: diver 与 lure 独立 cause。**Identity** ✓。
- **Reasoning**: 与 HR2-06/07 构成 composition 的三个结构变体（纯并集 / 耦合吸引子 / 带自身信号的设备）：同一 resolver 契约三种实例化，零 per-case 规则——Delta 2 的 fan-out 正向证据。

### HR2-15｜Surf pencil popper｜COVERED

- **Blind validity**: BLIND_VALID。surf 场景与浪区背景噪声未入任何 fixture。
- **Real player strategy**: 破浪区远投重 pencil，入水大水花 + 抽拉水柱；环境浪噪声抬高声学地板，玩家赌的是"比噪声更响 + 更大的轮廓"。
- **Observed facts**: 入水 splash：sound_amplitude HIGH 瞬态 + apparent_size 瞬态放大（水花）；抽拉段 sound_amplitude MED spike 序列；relation.surface ON；**环境浪噪 = background 输入**（GEOMETRY_INPUT_TOKENS 允许），resolver 侧折出有效声刺激带。
- **Required gameplay distinction**: 浪区 vs 静水同一饵——有效声/视觉刺激差异；**不需要** signal-to-noise ratio 类新字段。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: RECEIVER_RELATIVE_EXTENDS_TO_ACOUSTIC_MASKING / NO_SN_RATIO_DESCRIPTOR_NEEDED / UPSTREAM_DATA_READINESS_NOTE。
- **Cause ownership**: splash 与抽拉声独立 cause（入水 vs 操作），无叠加。**Identity** ✓。
- **Reasoning**: receiver-relative 教义（H10 光学先例）在第二感官模态盲复现；实现侧需上游提供背景噪声输入（data readiness，非语义缺口，按 Protocol §14 归 INPUT_DATA_SIDE 而非 SEMANTIC_GAP）。

### HR2-16｜河流底浸 cut herring 钓鲟｜COVERED

- **Blind validity**: BLIND_VALID。sturgeon、cut bait 静浸 config 均未入 fixture；R1 污染清单的 Bottom Feeder 分支故事不属 PC lane 边界（R1 清单未列）。Flag: CHEMICAL_MAGNITUDE_ECHO（若继续追问"新鲜度衰减"即 H17 已推迟问题——本 case 主问不在此，见下）。
- **Real player strategy**: 重坠静浸切块鲱鱼于河底主流带，纯化学招募、零运动；玩家拨盘 = 位置（主流带羽流下游可达性）与换饵节奏。
- **Observed facts**: speed ZERO + DurationFact VERY_LONG + chemical_signature = CUT_HERRING 类型 + **contact_disturbance / vibration / sound 全零**（负空间：静浸不得声明任何接触扰动）；羽流几何 = Exposure/Opportunity 侧（current 输运）。
- **Required gameplay distinction**: 化学静饵 vs 运动拟饵——类型 + 运动学差异，无需浓度语义即可表达"有/无有效化学源"；**换饵节奏若要求表达浓度衰减，落回 H17 的 DEFERRED candidate（cue.chemical_intensity），本轮维持推迟**。
- **Primary**: COVERED。**Deltas**: 无。**Flags**: PLUME_GEOMETRY_OUT_OF_CUE_SIDE / ZERO_MOTION_NEGATIVE_SPACE / CHEMICAL_MAGNITUDE_ECHO_CONFIRMATORY_ONLY。
- **Cause ownership**: 单化学源。**Identity** ✓。
- **Reasoning**: 化学类型通道（H16 验证）在"零运动纯化学"极端上外推成立；接触扰动事实在静止场景的**正确缺席**为 Delta 1 提供了反向标定。

### HR2-C1｜Tuna spreader bar｜CONFIRMATORY（不入盲统计）

- **Contamination**: CONFIRMATORY_CONTAMINATED——spreader bar 与 H07 umbrella rig 是同源集群信号的直系变体（任务 §4"轻微改名版本"规则适用；集群 multiplicity 语义问题在 R1/R3 设计中被访问并导致 CF-MULTI-1 保持 OPEN）。
- **Analysis**: 5–8 同源 swimbait teasers + stinger。R3 §C 契约下：per-source facts 并集可表达；"集群联合信号 vs 单饵"的 multiplicity 差异仍无承载位（source_count 禁令 + 聚合禁令）。**MULTIPLICITY_ADMISSION_PRESSURE 独立家族重复命中（#2）**——R1 H07（bass umbrella）之外的第二个内容族（saltwater tuna）要求同一 capability。CF-MULTI-1 **维持 OPEN_PENDING_EVIDENCE**，证据强度上升，admission 决策仍归 Design Owner。
- **Flags**: CONFIRMATORY_CONTAMINATED / MULTIPLICITY_ADMISSION_PRESSURE_REPEAT / CF_MULTI_1_EVIDENCE_STRENGTHENED。

### HR2-C2｜Berley/chum trail 钓 snapper｜CONFIRMATORY（不入盲统计）

- **Contamination**: POSSIBLE_CONTAMINATION——chum/groundbait 区域化学轴在 R1 被显式排除（区域级化学 = Presentation-vs-World-State ownership 高风险区），R3 §3 点名为 Round 2 建议轴；语义问题已被访问。
- **Analysis**: 碎饵粒 + 油膜顺流扩散形成**区域级**化学场：不是一次 presentation instance，而是 world-state 字段——owner 在 World/Exposure 侧（Bake/Opportunity 消费其几何），**不要求 presentation 层 admission**。到达鱼端的"有效化学浓度"若产品需要，落回 candidate `cue.chemical_intensity`（H17 同一 DEFERRED 项）——chum 为其提供了第二个消费场景（区域招募 vs 饵新鲜度），仍属产品决策。本轮维持推迟。
- **Flags**: POSSIBLE_CONTAMINATION / OWNERSHIP_ROUTING_TO_WORLD_EXPOSURE / CHEMICAL_INTENSITY_CANDIDATE_SECOND_SCENARIO。

---

## C. Aggregate Metrics

### C.1 Classification 分布

```text
Blind-valid（16 cases，进入主统计）:
COVERED                      15  (HR2-01 02 03 05 06 07 08 09 10 11 12 13 14 15 16)
ANNOTATION_ONLY               1  (HR2-04)
DERIVED_DESCRIPTOR_ONLY       0
NEW_GENERIC_RULE_REQUIRED     0
NEW_PRIMITIVE_REQUIRED        0
NEW_RELATION_REQUIRED         0
ITEM_SPECIFIC_EXCEPTION       0
UNRESOLVED                    0
CAUSE_OWNERSHIP_CONFLICT      0

Confirmatory（2 cases，不计入）:
CONFIRMATORY_CONTAMINATED     1  (HR2-C1)
POSSIBLE_CONTAMINATION        1  (HR2-C2)

Blind 覆盖率（COVERED + ANNOTATION_ONLY） = 16/16 = 100%
```

### C.2 Vocabulary-growth metrics（与 Round 1 并列）

```text
                                Round 1 (18 cases)      Round 2 (16 blind)
ΔPrimitiveCount                 2 unique families       0
ΔDerivedDescriptorCount         0                       0
ΔRelationCount                  0                       0
ΔGenericRuleCount               1（多同源源合成）        0
ΔManualAnnotationCount          1（CRAB 请求）           1（AMPHIBIAN 请求；同级别 fish-neutral 字典值）
ΔItemSpecificExceptionCount     0                       0
ΔUnresolvedCount                0                       0
ΔCauseConflictCount             0（1 准冲突被化解）      0

admitted token 请求合计         +2 primitive +1 rule +1 enum = +4
                                → 本轮 +1 enum = +1（annotation 级，非 lane 语义变更）

single-use descriptor count     0                       0
contact_disturbance reuse       —                       5 case 直接复用（HR2-01 02 03 08 12）
                                                        + 1 反向标定（HR2-16 零）+ 1 误用边界（HR2-08 组件内接触禁用）
composition resolver reuse      —                       3 结构变体共用同一契约（HR2-06 07 14），0 per-case rule
Species/Mode fan-out            无 descriptor 鱼种化     无（AMPHIBIAN 值为字典层，不触发任何 Species 专属 rule）
generic-rule fan-out            既有 rules 零改动        既有 rules 零改动；新增规则 0
cause-provenance authoring 负担 —                       4 case 行使 provenance（HR2-01 02 08 12），
                                                        每 case 1–2 条平凡物理 cause 声明，0 专属 taxonomy 条目
```

### C.3 Kill Signals

```text
Kill Signal A（new content ↑ ≈ semantic token ↑）：未触发，且边际显著收敛。
    Round 1：18 cases → 4 token 请求。
    Round 2：18 cases → 1 annotation 级字典值（0 semantic token）。
Kill Signal B（descriptor 聚集 Species×Mode-specific rules）：未触发。
    全部 COVERED case 经共享 generic 通道表达；AMPHIBIAN 字典值不产生任何鱼种规则。
Kill Signal C（本轮新增：cause provenance authoring 复杂度 ≈ Item/rule 线性增长）：未触发。
    4 个 provenance 行使点全部使用平凡物理事件描述（"lure-grass contact"、
    "bead strike"、"wood strike"、"body displacing surface water"），
    无 cause ID registry、无 per-item taxonomy、无为了防 double count 而手工
    发明的新登记结构——complexity 未从 semantic vocabulary 位移到
    provenance authoring。
    1 条 scope 观察（sound_pattern 不在 CONTACT_CAUSE_FAMILY 清单内，
    见 HR2-05）作为 watch item 上报，非修改请求。
```

**结论：无 degeneration；未出现 Item vocabulary 化、Fish×Item matrix 回潮，也未出现 complexity displacement。**

---

## D. R3 Delta 专项发现

### D.1 Delta 1（cue.contact_disturbance : OrderedBand）

```text
泛化面           盲例          结果
植被接触         HR2-01        COVERED，无植被子词汇
垂直木击/离散    HR2-02        COVERED，未诱发 composite temporal enum
软泥连续拖行     HR2-03        COVERED，未诱发 substrate_specific_disturbance
垫顶持续拖动     HR2-04        COVERED（sustained 变体，DurationFact 承载）
组件内接触       HR2-08        正确禁用（scope = world geometry only）
静止零接触       HR2-16        正确缺席（反向标定）
```

任务 §7 列举的诱惑词汇（contact_disturbance_type / substrate_specific_disturbance / scrape_pattern / impact_pattern / mud_disturbance / vegetation rub）在全部盲例中**均未获得成立请求**。冻结语义"contact cause → provenance; movement → motion facts; duration → DurationFact"的分轴在 6 个独立配置上自洽。**Delta 1 泛化通过。**

### D.2 Delta 2（composition resolver）

```text
结构变体                 盲例          结果
异构并集（近距双组件）   HR2-06 08     并集即表达，无 rig identity
耦合吸引子（旋转板+尾饵）HR2-07        因果耦合对鱼不可感知，无需表达
设备组件（diver 本体）   HR2-14        设备名不入语义，resolved facts 全承载
同源集群（confirmatory） HR2-C1        MULTIPLICITY_ADMISSION_PRESSURE 重复（#2 家族），
                                       CF-MULTI-1 维持 OPEN_PENDING_EVIDENCE
```

任务 §8 的检查成立：未出现 aggregate 语义相同但 multiplicity 必须改变 Response 的 **blind** case（唯一命中者为 family 级污染的 confirmatory case）。`source_count / lure_count / rig_identity / SKU` 禁令未受盲压挑战。**Delta 2 泛化通过；CF-MULTI-1 证据增强但状态不变。**

### D.3 Cause ownership / provenance 机制（R3 ruling B）

- 4 个盲侧行使了 provenance 纪律（HR2-01 独立双因、HR2-02/08 同因单消费、HR2-12 单因双感官单消费），全部以平凡物理事件描述完成，无 CAUSE_OWNERSHIP_CONFLICT、无 CAUSE_PROVENANCE_REQUIRED 阻塞、无作者发明 cause taxonomy。
- **Kill Signal C 观察：未触发**。complexity 未位移到 provenance authoring。
- **1 条 scope 上报（非修改）**：`cue.sound_pattern` 未列入冻结 validator 的 CONTACT_CAUSE_FAMILY；同 rule 消费 sound_amplitude + sound_pattern 时 family 检查不提示声明 cause identity。本 round 无实际冲突成立，但该清单位与 ruling B 的"同因二次计权"判据存在形式缝隙，留 Design Owner 裁决（R4 候选，不阻塞）。

### D.4 cue.sound_pattern（R3 §E）

HR2-05 提供了它的**第一个独立盲压证据**：节拍拨盘在 amplitude / pause_duration / speed 全同下仍是真实策略差异，仅 sound_pattern 可承载。证据等级建议从 `EXERCISED_BY_DEVELOPMENT_CASE` 上调为 `EXERCISED_BY_DEVELOPMENT_AND_ONE_BLIND_CASE`——按 R3 §E 标准（使用过 ≠ 证明必须），单盲案不自动宣判 NECESSITY_VALIDATED，但必要性方向获得独立支持。

---

## E. Counterexamples / 边界（最强 5 例）

1. **R3 succeeds broadly — HR2-03 C-rig 软泥拖行**。表面最像"需要 substrate-specific descriptor"的 case，实际由 contact_disturbance magnitude × DurationFact 完整表达；`mud_disturbance` 请求未成立。Delta 1 的泛化宽度的正面证据。
2. **Scope boundary — HR2-08 clacker（组件内接触）**。提供了 contact_disturbance"该用/不该用"的精确分界：world geometry contact ∈；component-internal contact ∉（走 sound/vibration）。语义边界在盲压下自洽，未发现灰色地带。
3. **R2 succeeds unexpectedly — HR2-15 surf 声掩蔽**。环境噪声抬升声学地板的最强候选缺口，被"effective receiver-relative fact + background 几何输入"吸收，无 SNR 字段请求——receiver-relative 教义从光学到声学的免费外推。
4. **Boundary reconfirmed — HR2-13 pressured bonefish**。pressure / cue familiarity 轴（R3 §3 留给本轮的建议轴）：presentation 侧完整表达策略差异，警觉属鱼侧 state owner。lane 的 NOT_ADMITTED 是正确缺席而非缺口；R3 §1 该条目获得盲边界证据。
5. **Confirmatory echo — HR2-C1/C2**。两个 confirmatory case 分别复击 CF-MULTI-1（第二个独立内容族）与 chemical intensity candidate（第二个消费场景）：都不是新缺口，但都提高了已 OPEN/DEFERRED 项的证据强度，供 Design Owner 做 admission 裁决。

---

## F. Round 1 → Round 2 边际复杂度比较

```text
维度                       R1 (R2 baseline)        R2 (R3 baseline)        趋势
primitive family growth    2（连续底接触、          0                       ↓ 收敛
                           化学量级-deferred）
generic-rule growth        1（多同源源合成）        0                       ↓ 收敛
annotation growth          1（CRAB）               1（AMPHIBIAN）          → 持平（同级）
exception growth           0                       0                       → 持平
unresolved growth          0                       0                       → 持平
cause-provenance burden    n/a（机制未冻结）        4 case × 平凡声明，      新增机制零边际成本
                                                   0 taxonomy 增长
blind COVERED+ANNOT        14/17 ≈ 82%             16/16 = 100%            ↑（与上三项共同
                                                                           表明 R3 窄 Delta
                                                                           恰好补中 R1 缺口）
```

- **曲线判断**：R1 的两个 semantic 缺口（连续底接触、多同源源合成）被 R3 窄 Delta 补中后，本轮 18 个新 case 的 semantic token 边际成本从 +4 降到 +1（且为字典 annotation 级）。**R3 的窄 Delta 使边际复杂度曲线稳定下来**——没有出现补丁之后的新缺口连锁。
- 同一缺口未重复盲命中：本轮盲统计内 0 个 NEW_PRIMITIVE / NEW_GENERIC_RULE；唯二重复压力（C1 multiplicity、C2 chemical）均为污染标记的 confirmatory，指向**已经 OPEN/DEFERRED 的同一项**，非新缺口。
- 按 Protocol §8：两个独立 unseen round 的斜率已可读——R1 建立基线（4 token），R2 验证斜率下降（1 annotation）。泛化主张的证据形态满足"第二轮比第一轮更强信号"。

---

## G. Verdict

```text
HOLDOUT_PASS
```

**理由**：

1. **16 个盲例零 semantic delta**：无新 primitive、无新 generic rule、无新 relation、无 item-specific exception、无 unresolved、无 cause conflict；唯一请求是 1 个 fish-neutral 字典值（AMPHIBIAN，annotation 级，canonical 权威在 FeedingTarget dictionary contract，非本 lane baseline 变更）。
2. **R3 两个 Delta 在盲压下泛化**：contact_disturbance 以 6 个独立配置复用且零子词汇诱发（含 2 个正确禁用/缺席的负空间标定）；composition resolver 以 3 个结构变体实例化且零 per-case 规则。任务 §7/§8 的全部诱惑路径（子词汇、temporal enum、substrate descriptor、multiplicity primitive、rig identity）均未在盲例中成立。
3. **Kill Signal A / B / C 全部未触发**：token 边际成本 R1 +4 → R2 +1（annotation 级）；无 descriptor 鱼种化；provenance authoring 零 taxonomy 增长（无 complexity displacement）。
4. **不判 HOLDOUT_PASS_WITH_NARROW_DELTA**：本轮不存在需要 baseline 语义变更的盲发现；字典值 admission 按冻结 R3 §D 分工本就属 lane 外的 canonical 流程，"NARROW_DELTA" 措辞应保留给需要改 baseline 语义的轮次。
5. **不判 REVISE / FAIL**：无单点击穿、无退化、无位移；结构在第二个独立轮次上保持健康斜率。

### 四项 §17 声明

```text
是否出现新的 semantic family        否（0 新 family）
是否重复命中同一缺口                盲统计内否；confirmatory 层复击两项
                                   已 OPEN/DEFERRED（CF-MULTI-1、chemical intensity），
                                   证据增强、状态不变
是否出现 factorization degeneration 否
是否出现 complexity displacement    否（Kill Signal C 观察点实测未触发；
                                   1 条 family 清单 scope 观察上报，非位移）
```

### BASELINE_CHANGE_REQUIRED 汇总

```text
（无——本轮零 baseline 修改请求）
上报备查（非修改请求）：
- CONTACT_CAUSE_FAMILY 清单未含 cue.sound_pattern 的 scope 观察（HR2-05，R4 候选议题）
- FeedingTarget 字典 AMPHIBIAN 值 admission 请求（HR2-04，canonical 流程，非 lane 语义）
- CF-MULTI-1 证据增强（第二个独立内容族 HR2-C1，维持 OPEN_PENDING_EVIDENCE）
- cue.chemical_intensity 候选获得第二个消费场景（HR2-C2，维持 DEFERRED）
- cue.sound_pattern 证据等级建议上调为 EXERCISED_BY_DEVELOPMENT_AND_ONE_BLIND_CASE（HR2-05）
```

### 本轮不证明什么（What this round does not prove）

- 不证明 rule resolution / aggregation / sampling / rate / calibration 算法与数值标定；
- 不证明 post-generation 行为（追击 / 攻击 / 挂钩 / fish-side state machinery——HR2-13 只划界不裁决鱼侧）；
- 不证明 production runtime 实现；
- 16 个盲例全部落在 COVERED / ANNOTATION_ONLY **不等于**"vocabulary 已完备"——纯视觉周期性（HR2-07 OBSERVATION）、SNR 字段、temporal enum 等负空间本轮未被真实策略命中，它们的缺席证据是"暂无需求"，不是"永久无需求"；
- CF-MULTI-1 与 chemical magnitude 的 admission 决策仍完全归 Design Owner，本轮只增强证据不关闭议题；
- 按 Holdout Protocol §8 / Promotion Gate C：本轮与 Round 1 构成两个独立 unseen round 的斜率证据，但 Presentation/Cue 语义的任何 promotion 仍需 Design Owner 在完整揭盲后 adjudication。

---

## 附：证据来源（case evidence only，非 semantic authority）

- [Bassmaster – Ripping Traps in Grass](https://www.bassmaster.com/how-to/news/ripping-traps-in-grass/)｜[Googan Squad – Ripping Lipless Crankbaits](https://googansquad.com/blogs/bass-fishing-guide/how-to-rip-lipless-crankbaits-through-spring-grass)｜[Kraken Bass – Lipless Crankbait Guide](https://krakenbass.com/lipless-crankbait/)（HR2-01）
- [Game & Fish – Carolina Rig Crash Course](https://www.gameandfishmag.com/editorial/crash-course-carolina-rig-bass-fishing/549323)｜[Wired2Fish – The Carolina Rig](https://www.wired2fish.com/fishing-rigs/the-carolina-rig-how-to-rig-and-fish)（HR2-03）
- [Game & Fish – Topwater Froggin' Game Plan](https://www.gameandfishmag.com/editorial/bass-crash-course-frog-baits/496259)｜[Major League Fishing – Froggin' Tips](https://majorleaguefishing.com/tips/become-a-frog-prince-with-these-hot-froggin-tips/)（HR2-04）
- [Megabass – Walking Topwater Lures](https://megabassusa.com/how-to-fish-walking-topwater-lures/)｜[Game & Fish – Chuggers](https://www.gameandfishmag.com/editorial/chugger-still-one-of-the-best-topwaters-for-bass/333642)（HR2-05）
- [Ace Charters – Flasher Flies](https://www.acecharters.com/fishing/fishing-flasher-flies/)｜[Island Fisherman – Choosing a Flasher](https://islandfishermanmagazine.com/choosing-the-right-flasher/)（HR2-07）
- [BassResource – Texas Rigged Worm](https://www.bassresource.com/fishing/worm-fishing-1.html)（HR2-08）
- [Sport Fishing Mag – Deep-Drop with Electric Reels](https://www.sportfishingmag.com/deep-drop-fishing-with-electric-reels/)（HR2-09）
- [The Fisherman – Live Eeling Done Right](https://www.thefisherman.com/article/nighttime-stripers-live-eeling-done-right/)｜[On The Water – Monster Bass Tactics](https://onthewater.com/monster-bass-tactics)（HR2-10）
- [In-Fisherman – Ice Fishing Lake Trout](https://www.in-fisherman.com/editorial/ice-fishing-lake-trout/153710)｜[Mack's Lure – Ice Jigging](https://mackslure.com/blogs/mack-attack/ice-fishing-how-to-locate-fish-and-effective-jigging-techniques)（HR2-11）

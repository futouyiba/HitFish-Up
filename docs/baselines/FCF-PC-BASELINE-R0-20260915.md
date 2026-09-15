<!-- Archived verbatim 2026-09-15 from author-provided candidate text. No wording edits. Freeze candidate, NOT promoted. -->

# FCF Presentation / Cue Validation Baseline Candidate R0

Status: EXPERIMENT FREEZE CANDIDATE / NOT PROMOTED
Candidate Freeze ID: `FCF-PC-BASELINE-R0-20260915`

## 1. Purpose

本 Baseline 不是完整设计 Presentation Runtime,也不是建立新的 Stimulus / Perception Domain。
它只冻结足够用于下一轮 Authorability / Vocabulary Generalization 实验的最小语义边界:

```text
Item / Rig / Technique / Player Motion / World-Physics
                    ↓
          Presentation Realization
                    ↓
 fish-independent Presentation / Cue Facts
                    ↓
      small typed Derived Relations
                    ↓
      Species × Engagement Mode
              Response DSL
                    ↓
              ResponseBand

```

实验目标不是证明该 Vocabulary 能描述现实中的所有鱼饵,而是攻击以下主张:
新 Item / Presentation / strategy story 进入系统时,大部分内容应能复用有限的 canonical facts、derived descriptors 与 relation resolvers,而不是线性制造新的 semantic token、Fish × Descriptor rule 或 item-specific exception。

## 2. Ownership Invariants

### 2.1 Presentation / Cue 必须 Fish-independent

同一组 Presentation / Cue Facts 不得因为当前评估 Species 或 Engagement Mode 不同而变化。

禁止 Presentation/Cue resolver 读取:

```text
Species preference
Engagement Mode valuation
Fish-specific attractiveness
Fish sensory preference
ResponseBand
SelectionWeight

```

Species-specific 解释只能发生在下游 Relation / Response。

### 2.2 Item / Technique Identity 不是 Response Semantic

以下内容不能直接成为 Response 输入:

```text
Lure SKU
ItemId
TechniqueId
UI Action Name
Merchandise Category

```

它们只能作为上游 cause,经 realization / semantic projection 生成可复用事实。

### 2.3 Existing Owner Truth 不重复配置

FCF 不建立第二套:

```text
Item physics table
Rig physics table
World environment table

```

已有 Owner 的 geometry / material / rig / motion / World facts优先引用。
只有确实缺少且经 admission 的 sparse semantic annotation 才允许新增 authoring truth。

## 3. Baseline Input Namespaces

### 3.1 `presentation.*`

表示 fish-independent representation / semantic descriptor。
当前只冻结“允许这种角色存在”,不冻结完整 taxonomy。
候选示例:

```text
presentation.profile?
presentation.prey_stage?
presentation.chemical_signature?

```

合法 descriptor 必须满足:

```text
Fish-independent
Cross-item reusable
Not a SKU alias
Not a response judgment
Preferably derivable/provenanced from realized facts

```

`MINNOW_LIKE`、`CRUSTACEAN_LIKE` 等可以作为 descriptor candidate,但它们本身没有 Fish preference setter 权。

### 3.2 `cue.*`

定义为:
在当前 Response evaluation semantic support 上已经解析出的、fish-independent physical / presentation stimulus facts。
它可以是 source-local,也可以包含 fish-independent World / Physics propagation;但不得已经包含 Fish sensory interpretation。

当前 Candidate Basis:

```text
cue.apparent_size
cue.visual_contrast
cue.flash

cue.speed
cue.speed_change
cue.direction_change
cue.pause_duration
cue.vertical_motion

cue.displacement
cue.vibration_amplitude
cue.vibration_frequency

cue.sound_amplitude
cue.sound_pattern

```

Candidate extension,仅作为实验候选、不是已批准 primitive:

```text
cue.chemical_intensity?

```

重要边界:

```text
Source fact
+ fish-independent geometry / propagation
→ cue.*

cue.*
+ Fish sensory capability / valuation
→ downstream Response interpretation

```

不得把 `cue.*` 定义为:

```text
fish_visibility
perceived_attractiveness
injuredness
provocation

```

## 4. Feeding Target Contract

`DynamicFeedingPreference` 所使用的 Target 不得绑定:

```text
Lure SKU
Bait product
presentation.profile directly

```

实验中使用抽象角色:

```text
FeedingTargetKey

```

其语义是:
一个版本化、低基数、稳定、可跨 Item 复用的 feeding-target domain concept。
概念示例仅用于解释,不冻结 taxonomy:

```text
SMALL_BAITFISH
CRUSTACEAN
AQUATIC_INSECT
SURFACE_INSECT
WORM_LIKE_FOOD
PREPARED_FOOD

```

链路:

```text
Presentation Evidence / Descriptor
            ↓
Target Interpretation
            ↓
0..N FeedingTarget hypotheses
            ↓
Static Fish Target Affinity
× Dynamic Feeding Preference
            ↓
relation.feeding_target_affinity

```

Response DSL 默认消费:

```text
relation.feeding_target_affinity

```

而不是直接查 Target table。
`relation.feeding_target_affinity` 只表达:
当前 Presentation 被解释成的 feeding target,相对于当前 Species / Engagement Mode / current feeding preference 是否合适。

它不得吞并:

```text
motion quality
drift quality
pause timing
flash fit
vibration fit
general Presentation quality

```

因此以下情况必须合法:

```text
feeding_target_affinity = BEST
但 motion / drift 不合适
→ Response LOW

```

以及:

```text
feeding_target_affinity = GOOD
但某些 response-relevant cues 非常匹配
→ Response HIGH

```

Deliberately OPEN
多个 FeedingTarget hypotheses 同时成立时如何 resolve,本轮不冻结。
禁止 Coding Agent自行引入:

```text
sum
weighted average
max
Noisy-OR

```

若实验遇到该问题,记录为 `UNRESOLVED` 或 semantic delta request。

## 5. Derived Relation Contract

`relation.*` 不是 universal Meaning Layer。
准入标准是:
Response 如果要得到某个事实,是否必须跨 Owner 做 lookup / join / history resolution / current-state resolution?
若不需要,优先直接使用 primitive facts。

当前 Candidate Relations:

```text
relation.feeding_target_affinity
relation.cue_familiarity

```

以及已经存在的空间/情境关系,例如:

```text
relation.bottom
relation.surface
relation.nest
relation.flow

```

典型链:

```text
CueSignature
× local History / Pressure
→ relation.cue_familiarity

```

Response:

```text
relation.cue_familiarity >= HIGH
→ CAP_RESPONSE_BAND ...

```

## 6. No Mandatory Meaning Layer

Baseline 不要求:

```text
PreyMatch
FeedingMatch
PresentationMatch
StimulusScore
Attractiveness
MotivationScore
Meaning Resolver

```

它们只有在后续实验发现大量重复 predicate、且新增一个 derived semantic 能明显压缩 exception / authoring complexity 时,才允许提出 admission。

默认优先:

```text
primitive typed facts
+ field-to-field comparison
+ ALL / ANY / NOT

```

直接表达 Response。

## 7. Explicitly Forbidden Canonical Fields

Baseline 默认拒绝:

```text
presentation.injured_prey
presentation.vulnerable
presentation.easy_opportunity

presentation.good_for_bass
presentation.attractive_to_*
presentation.catchability
presentation.presentation_quality

presentation.rapala_xrap
presentation.spinnerbait_product_123

cue.perceived_attractiveness
cue.fish_visibility

FeedingMatch
PresentationMatch
Universal AttractionScore

```

`reaction_bait`、`injured-like` 等词默认视为高风险 Explain/Interpretation vocabulary,不准自动进入 Canonical Basis。

## 8. Cause Ownership / Double-count Rule

每个 derived fact 应保存最小 causal provenance。
例如:

```text
Turbidity
+ background
+ geometry
→ cue.visual_contrast

```

如果 Response 已消费 `cue.visual_contrast`,则不得在没有独立语义理由的情况下再次:

```text
context.turbidity
→ second visual penalty

```

Harness 不需要自动证明完整因果图,但必须能够记录并报告明显的:

```text
CAUSE_OWNERSHIP_CONFLICT

```

## 9. Vocabulary Admission Principle

新增真正 semantic degree of freedom 前至少检查:

```text
能否由已有 primitive 表达?
能否由已有 primitive 确定性 derived?
是否跨多个 Item / Technique 复用?
是否购买真实 downstream strategy distinction?
是否减少更多 exception?
是否会制造新的 Fish × Token response surface?

```

核心 Kill Signals:

```text
new Item count ↑
≈ semantic token count 线性 ↑

```

或:

```text
一个新 descriptor
→ 大量 Species 都需要新增专门 Response rule

```

出现上述趋势,视为 factorization degeneration,而不是成功扩展 vocabulary。

## 10. Validation Classification

每个测试 Case 在不修改冻结 Baseline 的情况下,必须先归类为:

```text
COVERED
ANNOTATION_ONLY
DERIVED_DESCRIPTOR_ONLY
NEW_GENERIC_RULE_REQUIRED
NEW_PRIMITIVE_REQUIRED
NEW_RELATION_REQUIRED
ITEM_SPECIFIC_EXCEPTION
UNRESOLVED
CAUSE_OWNERSHIP_CONFLICT

```

不得看到单个失败 Case 后立即修改 Baseline 并把该 Case 重新记为 PASS。
一旦根据某 Case 调整 Baseline,该 Case 从此属于 Development Set。

## 11. Required Metrics

至少输出:

```text
case count by classification

Δ primitive requests
Δ derived descriptor requests
Δ relation requests
Δ generic resolver rule requests
Δ manual annotation
Δ item-specific exception
Δ unresolved
Δ cause ownership conflict

descriptor token count
single-use descriptor count
Fish × Descriptor direct-touch count
per-descriptor Species/Mode fan-out
generic rule fan-out

```

不要压缩成一个综合分。

## 12. Development vs Holdout Boundary

已经参与过旧 Presentation / FCF 设计的案例只能作为 Regression / Development Set,不得宣称 unseen:

```text
Spinnerbait steady
Spinnerbait jerk-pause
Bread / prepared-food passive
Shrimp-like bottom hop
Spoon steady / oscillating
Fly dead drift / twitch
Topwater popper pop-pause
Soft worm bottom drag

以及已经参与 FCF Strategy Story 设计的 Bass / Trout / Carp 等具体故事

```

真正 Blind Holdout 的具体 Item × Presentation 身份必须在 Baseline Freeze 后由独立 Reviewer / Sample Agent 选择。
Coding Agent 本轮不得自行挑选一批案例、调模型、再用同一批案例报告 generalized PASS。

## 13. What This Freeze Does NOT Decide

本轮故意不冻结:

```text
complete presentation.* taxonomy
complete cue.* taxonomy
FeedingTarget dictionary exact members
multi-target hypothesis aggregation
ResponseBand numeric mapping
SET/CAP final resolution algorithm
final chemical cue model
Production physics / propagation implementation
Human editor UX
post-generation Fish AI / pursuit / bite / hook

```

这些不是 Coding Agent 可以暗中闭合的问题。

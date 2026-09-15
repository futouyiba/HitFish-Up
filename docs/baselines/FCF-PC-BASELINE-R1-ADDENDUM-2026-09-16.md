<!-- FCF-PC-BASELINE-R1: Addendum to R0. R0 archive remains unmodified at docs/baselines/FCF-PC-BASELINE-R0-20260915.md. This document records Design Owner adjudication 2026-09-16. -->

# FCF Presentation / Cue Validation Baseline R1 — Addendum to R0

Candidate Freeze ID: `FCF-PC-BASELINE-R1-2026-09-16`
Status: FREEZE CANDIDATE / DESIGN OWNER ADJUDICATED / NOT PROMOTED

## 0. 与 R0 的关系

- R1 = R0(原样存档于 [FCF-PC-BASELINE-R0-20260915.md](FCF-PC-BASELINE-R0-20260915.md),不回写、不修改)+ 本 Addendum。
- R0 中未被本文修改的章节全部继续有效;本文只做裁决级澄清与边界修补。
- 裁决来源:Design Owner 2026-09-16 裁决,闭合自审 [报告](../reviews/FCF-PC-BASELINE-R0-SELFREVIEW-2026-09-15.md) 的 P1-1~P1-4、P2-5、P2-9(CueSignature 部分)。
- 本文不晋升任何未经裁决的 proposal;见 §3「维持 open / proposal 的项」。

## A1. Fish-independent 不等于 geometry-independent(解决 P1-1)

`presentation.* / cue.*` 的 fish-independent 定义为:

```text
在相同 canonical evaluation support / geometry / World 状态下，
其值不得因当前 Species 或 Engagement Mode 身份不同而变化。
```

因此允许:

- canonical support-relative distance / angle / geometry;
- fish-independent medium propagation;
- background / turbidity / flow 等 World/Physics 对物理信号的影响。

禁止:

- Fish sensory capability;
- Species-specific detection threshold;
- attractiveness / valuation / preference;
- spawned individual Fish AI / geometry state。

`cue.apparent_size`、`cue.visual_contrast` 因而可以是 receiver/support-relative、但必须保持 Species/Mode-independent。
如果某字段需要具体 spawned Fish 才能求出,则不属于当前 pre-generation baseline。

对 R0 §2.1 的效力:不变式的正确读法即上述定义;§2.1 禁止读取清单原样有效。

## A2. Kinematic facts 不允许隐含 Reference Frame(解决 P1-2)

不要替 Design Owner 强行选择一个 universal speed frame。
Validation schema 应要求所有存在 reference-frame ambiguity 的 kinematic fact 显式记录 semantic metadata,例如:

```text
reference_frame
temporal_scope / summary_semantics
```

- `cue.speed / speed_change / direction_change` 不得靠字段名暗示 ground-relative 或 local-water-relative。
- `pause_duration` 是 upstream 已解析 pause-state 的 DurationFact。
- `vertical_motion` 可使用明确 gravity/world vertical semantic。
- `cue.displacement` 暂标 `PROVISIONAL`:net displacement 与 path length 尚未裁定。在没有明确 semantic definition 的 fixture 中,不得用 `cue.displacement` 把 Case 判成 `COVERED`;应标 `UNRESOLVED` 或避免依赖该字段。

Harness 本轮只需能验证 reference-frame / temporal metadata 是否存在,不需要实现生产级 motion resolver。

## A3. Feeding Target axis(解决 P1-3)

第一版固定:

```text
StaticTargetAffinity:
    Species × FeedingTargetKey
```

不带 Engagement Mode。
Dynamic Feeding Preference 也不得因为 ResponseProfile 是 `Species × EngagementMode` 就自动复制成 Mode-specific target table。

链路:

```text
Species × FeedingTargetKey
        ↓
Static Target Affinity
        +
current Dynamic Feeding Preference
        ↓
relation.feeding_target_affinity
```

然后当前:

```text
ResponseProfile = Species × Engagement Mode
```

可以选择消费、忽略或以不同 Response rules 使用这个 relation。
如果将来出现真实反例证明:同一 Species 对 FeedingTargetKey 的基础/当前排序本身因 Engagement Mode 改变,将其报告为新的 semantic admission request,不要提前扩大表轴。

## A4. Classification protocol(解决 P1-4)

每个 Case 必须有:

```text
primary_classification: exactly one
requested_deltas: zero or more
flags: zero or more
```

Primary 判定程序:

```text
CAUSE_OWNERSHIP_CONFLICT
→ 若当前表达首先违反 owner / double-count

UNRESOLVED
→ 若必须先做尚未冻结的 semantic decision

否则寻找“使 Case 可合法表达的最小充分改动”：

COVERED
ANNOTATION_ONLY
DERIVED_DESCRIPTOR_ONLY
NEW_GENERIC_RULE_REQUIRED
NEW_PRIMITIVE_REQUIRED
NEW_RELATION_REQUIRED
ITEM_SPECIFIC_EXCEPTION
```

若 Case 同时需要多种 Delta:

- primary = 最先不可缺少的最小充分 semantic change;
- 其它需求进入 `requested_deltas[]`;
- aggregate metrics 分别计数,不丢失多 Delta 信息。

`DERIVED_DESCRIPTOR_ONLY` 的「确定性派生」要求:
只读取当前已 admitted fish-independent facts,并且相同输入必须唯一地产生相同 descriptor;不得读取 Species / Mode / response / hidden SKU identity。

## B1. CueSignature must not become SKU memory(解决 P2-9 之 CueSignature 部分)

`CueSignature` 必须是 versioned semantic signature,只允许由已 admitted:

```text
presentation.*
cue.*
以及必要的 canonical relation-independent presentation facts
```

构成。

禁止包含:

```text
SKU
ItemId
TechniqueId
merchandise category
raw UI action identity
```

如果两个不同 SKU 解析成同一 canonical CueSignature,则 baseline 默认视为同一 familiarity identity。
如果产品未来需要 item-specific learning,这是新的 semantic/state admission,不得通过 CueSignature 偷渡。

## B2. Zero target hypothesis is typed(解决 P2-5)

必须区分:

```text
NO_SUPPORTED_TARGET
```

与

```text
UNKNOWN / RESOLUTION_INCOMPLETE
```

后者不得当作 zero / bad affinity。
Harness 只需保留 typed status;本轮不要自行决定它如何映射 ResponseBand。

## 1. 对 R0 的修改效力表

| R0 章节 | R1 效力 |
|---|---|
| §2.1 | A1 澄清读法:fish-independent ≠ geometry-independent;禁止清单不变 |
| §3.2 | A2:kinematic fact 须显式 `reference_frame` / temporal metadata;`cue.displacement` 标 `PROVISIONAL` |
| §4 | A3:`StaticTargetAffinity = Species × FeedingTargetKey`(无 Mode 轴);B2:typed zero-target status |
| §5 | B1:CueSignature 组成约束(versioned、仅 admitted facts、无 item identity) |
| §10 | A4:分类记录结构(primary/requested_deltas/flags)与判定程序 |
| 其余章节 | 不变,继续有效 |

## 2. 悬挂引用的裁决外备注(非 normative)

R0 §5/§13 引用的 `SET_RESPONSE_BAND / CAP_RESPONSE_BAND`、单一 ordered `ResponseBand`、`Species × Engagement Mode` ResponseProfile 语义,其权威出处为 Notion「FCF Simplified V0|Response Language Contract Delta R0|接口优先,算法延后」(WORKING / NOT PROMOTED)。R0 §13 不冻结 SET/CAP 终局算法的立场与该页一致。

## 3. 维持 open / proposal 的项(本裁决未覆盖)

- R0 §13 全部 open 项不变:multi-target aggregation、ResponseBand 数值映射、SET/CAP 终局、chemical cue model、production physics 等。
- 自审 P2-6(§11 度量口径操作化)、P2-7(conflict 豁免载体 `CAUSE_JUSTIFIED`)、P2-8(holdout 抽样框钉住)、P3-10~P3-14、WATCH-15/16:维持 proposal / open,不因本文晋升。
- 实施位置裁定(Design Owner 裁决 C 节,2026-09-16):harness 实现于 `futouyiba/programaticHitFish`(在其既有 authoring compiler / deterministic pre-generation harness / fixture-test infra 上增加 Presentation/Cue Contract Validation Lane,不平行建第二套 execution framework);HitFish-Up 本仓文档为 preflight working artifacts,不冒充实现完成。
- Blind holdout 案例选择权仍在独立 Reviewer / Sample Agent;implementation lane 可执行且 regression PASS 之前不启动 holdout 选择。

## 4. 记录要求

- 本文件的 sha256 在实现 lane 的 baseline 记录与 run 报告中登记;R1 镜像入 `programaticHitFish` 仓 `docs/pc_validation/` 并保留同一 hash。
- 任何基于 case 的进一步修订 → 形成 R2 候选;R0/R1 不回写;被用于修订的 case 归入 Development Set(R0 §10 纪律)。

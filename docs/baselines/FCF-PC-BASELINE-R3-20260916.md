<!-- FCF-PC-BASELINE-R3-20260916: FROZEN after the Design Owner's REVISE_NARROWLY_BEFORE_FREEZE review (rulings A-F). Supersedes FCF-PC-BASELINE-R3-CANDIDATE-20260916 (kept as provenance, unchanged). Freeze != Promotion: WORKING VALIDATION BASELINE / NOT PROMOTED. -->

# FCF Presentation / Cue Validation Baseline R3 — Frozen

Freeze ID: `FCF-PC-BASELINE-R3-20260916`

```text
ROUND1 = HISTORICAL BLIND EVIDENCE(已闭合)
R3     = WORKING VALIDATION BASELINE(FROZEN / NOT PROMOTED)
ROUND2 = NOT_YET_AUTHORIZED
```

## 0. 冻结链与修订记录

- 链:R0 → R1 Addendum → R2(D1–D6)→ **R3(本文件)**;R0/R1/R2 与 R3-CANDIDATE 均不回写,保留为 provenance。
- 本文件 = R3-CANDIDATE 经 Design Owner `REVISE_NARROWLY_BEFORE_FREEZE`(裁决 A–F)收缩后的冻结版;收缩仅限 A–E 所列,无其它 semantic delta。
- 稳定读取位置:本文件(HitFish-Up `docs/baselines/`)+ `programaticHitFish` 分支 `feature/pc-cue-validation-r3-candidate` 上的逐字节镜像 `docs/pc_validation/FCF-PC-BASELINE-R3-20260916.md`(sha256 一致);分支 hash 见 `pc_validation/baseline.json`。

## A. Contact disturbance(冻结版 schema)

Round 1 真正购买的 capability 只有一句:**moving contact with world geometry generates a fish-independent resolved disturbance fact.**

```text
cue.contact_disturbance : OrderedBand
```

- 正交事实分解:contact cause → 本 cue / provenance;movement → 既有 motion facts;duration / sustained → 既有 DurationFact / `temporal_scope`。
- **不冻结任何 composite temporal enum**:候选期的 `CONTINUOUS_WHILE_MOVING / MOMENTARY_IMPULSE / STATIC_CONTACT` 未获独立 admission evidence,不进入 vocabulary(H06 等 Development 证据已表明 discrete impulse 不需要新能力)。
- 字段名不含 `surface_`,避免与既有 `relation.surface`(水面)歧义。
- 防 double-count:与 `vibration_*` / `sound_*` 的同类物理成因禁止同一 rule 重复计权——依据 **cause provenance / cause identity**(见 B)。
- `cue.displacement` 维持 NOT_ADMITTED;strategy token(`mechanical_scrape` 等)维持拒绝。

## B. Cause ownership(冻结版机制)

- `CAUSE_JUSTIFIED` **不进入** frozen contract、Response DSL、production schema、author-facing semantic——它在本 baseline 中不存在为正式机制;validator 逻辑中亦无布尔豁免。
- 防 double-count 唯一依据:cause provenance / cause identity 证明被消费 facts 来自独立 cause。
- 同一 cause identity 被同一 rule 二次计权 ⇒ `CAUSE_OWNERSHIP_CONFLICT`,无条件。
- 同 cause-family 成员被同 rule 消费但缺 cause identity 声明 ⇒ `CAUSE_PROVENANCE_REQUIRED`(须补 provenance 证明独立性)。

## C. Multi-source composition(冻结版契约)

```text
0..N source-local Presentation / Cue facts
→ deterministic composition resolver
→ canonical fish-independent snapshot
→ Response
```

继续禁止:raw rig identity / SKU / Technique ID / `source_count` / `lure_count`。
`CF-MULTI-1`(single vs multi-source 等聚合对照)**保持 `OPEN_PENDING_EVIDENCE`**,不因 Freeze 强行关闭;只有明确 yes 才重开 multiplicity primitive admission request。

## D. FeedingTarget dictionary(作用域声明)

- H14 裁决:复用 `CRUSTACEAN`,不新增 enum value、不新增维度。
- 实现 lane 中的 `FEEDING_TARGET_TEST_VOCABULARY = {SMALL_BAITFISH, CRUSTACEAN}` **仅是 validation fixture 的局部 test vocabulary**,不是 canonical FeedingTarget dictionary;canonical 成员权威仍在 FeedingTarget dictionary contract 及其 admission 流程。

## E. `cue.sound_pattern` 状态

使用状态仅为:`EXERCISED_BY_DEVELOPMENT_CASE`(H10)。**不是** `NECESSITY_VALIDATED`——使用过 ≠ 已证明必须存在;留待 blind Round 2+ 提供进一步证据。

## 1. 维持不准入(不变)

```text
chemical magnitude / odor concentration   DEFERRED / NOT_ADMITTED(H17 confirmatory only)
cue.displacement                          NOT_ADMITTED
item-specific strategy tokens             拒绝
raw source count(source_count/lure_count)拒绝
new Meaning layer                         拒绝
Pressure / cue familiarity                未验证(Round 1 主动排除)
```

## 2. Freeze Gate 执行记录(2026-09-16)

```text
full regression            215 passed / 1 skipped(169 Current baseline + 46 PC-specific)
PC test inventory          46(真实 collected inventory,未为数字调测试)
33-case Development Reg.   COVERED 29 / ANNOTATION_ONLY 3 / NEW_PRIMITIVE_REQUIRED 1(H17)/ UNRESOLVED 0
无新增 semantic delta      收缩仅限 A–E
frozen hash                见本文件 sha256(baseline.json 与 run 报告同值)
```

## 3. 剩余 OPEN

```text
CF-MULTI-1 counterfactual(OPEN_PENDING_EVIDENCE)
H17 chemical magnitude(DEFERRED,产品决策)
multi-target aggregation / ResponseBand numeric mapping / SET-CAP 终局(R0 §13)
metric spot-check ratio 与 §6 度量口径(协议 proposal,未裁决)
Round 2 采样轴建议(Carp pressure / cue familiarity;chum / groundbait)——由独立 Sample Agent 决定
```

## 4. 纪律

Freeze ≠ Promotion:本 baseline 是 WORKING VALIDATION BASELINE,不是 Working Main promotion;Working Main 状态不变。后续修订 → R4;R0–R3 不回写。

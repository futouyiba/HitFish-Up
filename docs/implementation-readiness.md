# 0.3.4.0-B Fixed Bake — Implementation Readiness

Result of one real vertical implementation (`reference/0340-fixed-bake/`) against the
Current 0.3.4.0-B contract. **REFERENCE / VALIDATION — not promoted.**

**Answer in one line:** the main chain is **uniquely implementable**; the numbers, the
gates, the aggregation and the floor are unambiguous and reproduce the P0 goldens
exactly. What was blocking a *formal* engineer was **not algorithm** but **two schema
questions** — resolved profile payload key names (GAP-001) and the Trace key set
(GAP-002) — plus two readings needing an owner line (GAP-003, GAP-004). **All four were
adjudicated on 2026-09-18 and are now closed** (see `implementation-gap.md` → *Rulings
applied*). Eight non-blocking edge items remain.

---

## 1. Authority used

Read from Notion on **2026-09-18**. The task prompt's stated entry points turned out to be
**historical**; the Current tree used instead is recorded below.

### Current (used)

| Page | ID | Role |
| --- | --- | --- |
| FCF Prototype Validation Router (bootstrap router) | `3cca4137d2368152bcd4dadaa0ab9e47` | entry |
| FCF Documentation Governance L0 | `3cca4137d23681599731d974a9cd4f89` | hard rules |
| 中鱼0.3.4.0-B｜中鱼因子聚合逻辑化（Fixed Template Bake） | `3dda4137d236812e89b5cf846c528b6c` | branch root |
| 中鱼0.3.4.0-B｜开发需求 | `3dda4137d23681c68ec3fb1944573af4` | **canonical**: Role/Gate §3.3 §4.5, aggregation §3.4, goldens §7, validation §8 |
| 0.3.4.0-B｜Bake Runtime Algorithm & Authoring Contract | `3dca4137d236815c88a0e56e15ceaf85` | W4B Current runtime spine (§ lines 1–61) |
| 0.3.4.0-B｜Bake Authoring Schema & Validator Contract | `3dca4137d23681e28c5bc2f29c63dc16` | W4B Current schema, validator, trace §3.8 |
| 0.3.4.0-B｜Authoring & Resolve Contract | `3dda4137d23681408e4fe0f35ced39d9` | W4B Current authoring / resolve / preview |
| 0.3.4.0-B｜Bass NORMAL Fixed Template Vertical Slice | `3dda4137d236818c9b61e6bc7fc348a7` | P0 golden fixture, validator assertions V1–V13 |
| 0.3.4.0-B｜Bake Authoring / 条件开关 Working | `3dca4137d236816ab0add70228a80d51` | role annotation method, profile names |
| 0.3.4.0-B｜Executable Delta Spec | `3dca4137d236819e98e2eebf67aaae68` | migration delta package (delta 1–7) |
| Checkpoint｜0.3.4.0-B Main Agent Control §25.6 / §26 | `3dda4137d2368109aa54ec4f7acbab26` | owner rulings: output name, 9 code deltas |
| 0.3.4.0-B｜时辰模板数值调研（昼行型） | `3dea4137d23681de95ded1b7e05311c9` | time-period template values (not consumed by Bass) |

### Prompt targets that are now Historical (authority drift)

| Prompt said | Actual current title | Status |
| --- | --- | --- |
| `3dda4137d23681bc9bcbcf9ded8da0ee` = "0.3.4.0 Fixed Bake 当前入口" | `Historical｜0.3.4.0 Fixed Template Transition｜2026-09-16` | **HISTORICAL**; content superseded by the sibling `0.3.4.0-B` root |
| `3dda4137d23681f5bc1ac72641c0597a` = "0.3.4.0 固定模板烘焙开发需求" | `Historical｜0.3.4.0 Fixed Template｜开发需求 R0` | **HISTORICAL** |
| `3dda4137d2368197955be725038ca786` = "参数组件计算机制 R1｜Fixed Template" | `Historical｜0.3.4.0 Fixed Template｜参数组件计算机制 R1` | **HISTORICAL** |

### Superseded premises carried by the prompt (deliberately NOT implemented)

| Prompt premise | Current contract |
| --- | --- |
| `ConditionRole`, `GatePolicy` (`HARD_EXCLUDE/TRACE_RESIDUAL/LOW_RESIDUAL`) | `AggregationRole = CORE \| SECONDARY \| IGNORED`; **no GatePolicy field** — gate is automatic for CORE |
| Gate "Failure Cap": `min(RawEnvCoeff, min(failedGateCaps))`, "cap 只能降低不能抬高" | replaced by a **failure branch**: background → `envCoeffMin`, non-background → `0`; the aggregate is not computed |
| `SpatialOpportunityIntensity` | `SpatialDistributionWeight` (Main Control §25.6) |
| `ConditionGroupSnapshot` | `ConditionGroup` |
| Secondary "total loss budget / 超预算行为", `1/6` scaling, cap `0.2554` | `SecondaryFactor = 1 − (1 − SecondaryProduct)/4`, range `[0.75, 1.0]` — no budget, no cap constant |
| Hard Exclude as a separate feature | expressed by authoring a discrete affinity of exactly `0` |

### Local repo

`docs/` in this repository is the **FCF Presentation / Cue validation lane**
(`FCF-PC-BASELINE-R*`), a different lane — it contains **no** Fixed Bake authority. No
local mirror of the Fixed Bake contract exists, so Notion was the sole authority.

---

## 2. Main chain status

### SPEC_CLEAR / IMPLEMENTED

- **Resolved Bake Subject** — `ResolvedSpatialOpportunitySubject { fishQualityRef,
  resolvedComponentProfiles, resolvedSpatialOpportunityBindings, provenance }`; own-pond
  truth must not appear; identity survives as `FishQualityRef`.
- **Base Opportunity input** — `ResolvedOpportunitySeed { fishPondRef, fishQualityRef,
  baseOpportunityIntensity, isBackgroundFish, envCoeffMin? }`, flat shape, floor only when
  `isBackgroundFish = true`, `envCoeffMin ∈ (0, 0.30]`, `baseOpportunityIntensity ≥ 0`.
- **ConditionRole** — three states, legacy `OFF`/`EXCLUDED` read as migration aliases.
- **Gate** — automatic for CORE, fixed criteria (discrete = coefficient exactly `0`;
  temperature = `PointFit < temp_threshold`), no authoring order, no combination step.
- **Gate evaluation → failure branch** — single-valued: `envCoeffMin` (background) / `0`
  (non-background); the aggregate is not applied; the floor cannot override it.
- **Atomic factor evaluation** — all four P0 components: temperature midpoint → PointFit
  with LINEAR/SMOOTHSTEP; structure table lookup; feeding layer `max` over the array;
  time-period table lookup. IGNORED conditions run no evaluator and need no profile.
- **Core aggregation** — `CoreProduct = Π CORE fits`; commutative; multiplicative loss.
- **Secondary aggregation** — `SecondaryProduct = Π SECONDARY fits` then
  `SecondaryFactor = 1 − (1 − SecondaryProduct)/4`; mathematically bounded to `[0.75, 1.0]`
  so "all secondary conditions together cost at most 25%" is a *structural* property, not
  a clamp; no per-factor operator, strength or budget is authorable.
- **RawEnvCoeff** — `CoreProduct × SecondaryFactor`.
- **Background floor** — `max(RawEnvCoeff, envCoeffMin)`, applied **only** when no gate
  failed.
- **FinalEnvCoeff / output** — `SpatialDistributionWeight = BaseOpportunityIntensity ×
  FinalEnvCoeff`, base multiplied exactly once, no normalisation, no cap.
- **Input validation (main-chain-consumed subset)** — seed missing `fishPondRef`,
  subject/seed `fishQualityRef` mismatch, non-finite/negative base, non-explicit
  `isBackgroundFish`, background without floor, floor out of range, non-background with a
  floor, unknown/duplicate condition keys, missing active profile, missing table entry.
- **Missing vs ignored** — a missing binding row / missing active profile is an error; an
  ignored condition is legal and silent.

### RESOLVED 2026-09-18

- **GAP-001** — resolved: the four component profiles use the 开发需求 §4.0 / §4.3
  snake_case key names in the resolved payload (delta 7 already pinned Temperature to
  that spelling; the 条件开关 page's camelCase is stale).
- **GAP-002** — resolved: `gateFailureCap` / `secondaryLossRaw` / `secondaryLossApplied`
  are **deleted** (not kept as null) and `gateFailureBranch {applied, branch,
  failedConditions}` is added; `importance` → `aggregationRole`. No legacy data, no
  implemented consumer, no information loss.
- **GAP-003** — resolved: an explicit `"aggregationRole": null` is an explicit IGNORED;
  only a wholly absent binding row is a resolve error.
- **GAP-004** — resolved: `gatePolicy` never shipped, so there is no legacy payload and
  no read-through channel; any occurrence is an error.

### SPEC_GAP

- **GAP-005** — runtime handling of an out-of-`[0,1]` authored fit is defined nowhere
  (only in an explicitly non-Current implementation history). Partially blocking.
- **GAP-006** — empty `feedingEcologyLayers[]`: `max()` over an empty set is undefined.
- **GAP-007** — a fish with **no** CORE binding: the empty-product convention is not stated.
- **GAP-008** — degenerate temperature bands (`accept_min == fav_min`) are legal by the
  stated constraint but their meaning is unstated (the value is derivable; the legality is
  not).

### NON_BLOCKING_AMBIGUITY

- **GAP-009** — what the Trace shows on the gate-failure branch.
- **GAP-010** — SECONDARY Temperature is required to carry `temp_threshold` /
  `falloff_shape` it can never use.
- **GAP-011** — `ConditionGroup` vs `ConditionGroupSnapshot`.
- **GAP-012** — `temp_threshold = 0` is legal and makes the gate permanently pass; a CORE
  fit of `0` then yields `CoreProduct = 0` with `CoreLoss = -inf`.

### DEFERRED_BY_SCOPE

Activity · Functional Capacity · Feeding Readiness · Fish Condition (Activity /
FeedingMotivation / Wariness) · Response / bait / posture / length · Presentation /
Exposure · Quality Selection · Engagement Mode routing, share, per-Mode
`BakeProgramRef` · Fish materialisation · any authorable Bake DSL / AST / expression
language · Editor UI and Figma frames · persistence / XLSX mappings · `TimePeriod →
Fish Condition` migration and its double-count audit · `ComponentDefinition` catalog
admission of Joint/Derived/Anchor definitions (`ACCESSIBLE_BENTHIC_FORAGE`,
`SPAWN_SITE_ANCHOR`) · `envCoeffMin` Floor-Impact Preview.

---

## 3. What was implemented

`reference/0340-fixed-bake/` — reference/validation only, stdlib Python 3.9.

```text
fixed_bake.py                the vertical slice (≈330 lines, no dependencies)
fixtures/bass_q3.json        P0 golden fixture + mutation cases
test_fixed_bake.py           semantic cases + contract-derived property tests
README.md                    scope, run instructions, authority pointer
```

The slice deliberately stops at the defined boundary: it validates only the invariants the
main chain consumes, and it takes **no decision** on any GAP. Where a GAP is unavoidable to
run at all, the chosen reading is labelled in code and in §4 of `implementation-gap.md`.

## 4. Tests

```text
runner      python3 -m pytest test_fixed_bake.py   and   python3 -m unittest test_fixed_bake
total       39
passed      39
failed      0
skipped     0
```

- **Fixture goldens (8 cases)** — CG-01 `1.0000000000`, CG-02 `0.3190909091`,
  CG-03 `0.1125000000`, temperature-gate failure (non-background `0` / background
  `0.10`), background floor `0.0306818182 → 0.10`, and two Base-scaling cases. The goldens
  were reproduced a second time by an independent script that applies the §3.4 / §4.3
  formulas without importing the reference.
- **Semantic cases (20)** — the task's Case 1–15 re-expressed against the Current contract
  (Case 7 "residual gate" is now "a near-zero nonzero coefficient is not a gate failure";
  Case 9 "multiple failed gates" collapses to one branch because there is no cap to
  combine), plus a dead-key-absence case added by the GAP-002 ruling.
- **Migration / legacy (3)**, **validation (7)**, **property invariants (8)**. The
  migration class was rewritten by the GAP-004 ruling: "any `gatePolicy` occurrence is
  rejected" replaced the old "inert value read through / non-inert rejected" pair.
- **Property tests** run seeded loops of 100–300 iterations over randomised condition
  groups: determinism, `EnvCoeff` bounds, background floor lower bound, monotonicity under
  a worsening CORE fit (including across the gate threshold), extra-SECONDARY-factor
  never raising, binding-order invariance, `SecondaryFactor ∈ [0.75, 1.0]`, empty-Core
  identity. This is the "small fuzz" round; no separate fuzzing harness was added.
- No regression suite was run in this repository: it contains no code. The production
  suite lives in `futouyiba/programaticHitFish` and was not touched.

### Invariants verified

| Invariant | Result |
| --- | --- |
| Gate failure never yields a value above the gate-passing path for the same fits | holds |
| An extra loss-only (SECONDARY) condition never raises the result | holds |
| `SecondaryFactor ∈ [0.75, 1.0]` structurally, without any clamp | holds |
| `FinalEnvCoeff ∈ [0, 1]` for all legal inputs | holds (violable only by GAP-005 input) |
| A background fish's result is never below `envCoeffMin` | holds |
| Binding order does not change the result | holds |
| Same input ⇒ identical output, and the Trace is byte-identical | holds |
| `BaseOpportunityIntensity` multiplies exactly once and never enters the aggregate | holds |
| IGNORED conditions run no evaluator and require no profile | holds |
| Missing ≠ ignored (absent active binding/profile is an error) | holds |
| Legacy `OFF + non-inert GatePolicy` is never silently coerced | holds |

## 5. Code-derived hidden decisions

Cases where the reference has to behave in a way no Current page states — all disclosed,
none silently absorbed. Full detail in `implementation-gap.md`.

**Now backed by a ruling** (so no longer hidden — the contract says what to do):

1. **Superseded trace keys.** Now deleted outright rather than kept as `null`, with a
   negative-knowledge note. (GAP-002 ✅)
2. **`null` role → IGNORED, absent row → error.** Now the ruled contract. (GAP-003 ✅)
3. **Any `gatePolicy` key is rejected.** The earlier inert-value read-through path was
   removed once it was established the field never shipped. (GAP-004 ✅)

**Still open — deliberately un-decided:**

4. **Gate failure → `None` aggregate.** On the failure branch the Trace reports `null` for
   `coreProduct` / `secondaryProduct` / `secondaryFactor` / `rawEnvCoeff` while still
   reporting per-condition fits (which had to be computed to evaluate the gate). The text
   only says the formula "is not computed". (GAP-009)
5. **No runtime clamp, no runtime range check.** An out-of-`[0,1]` authored value passes
   through unchanged and can push `FinalEnvCoeff` above `1`. Deliberate: taking no decision
   keeps GAP-005 visible rather than hidden behind a clamp.
6. **`coreLoss = None` when any CORE fit is 0** — avoids emitting `-inf`. Only reachable
   when `temp_threshold = 0`. (GAP-012)
7. **Empty product = 1.** Used twice: empty SECONDARY (explicitly authorised) and empty
   CORE (not authorised anywhere). (GAP-007)

**Not a decision at all:**

8. **`appliedFit == rawFit`.** The trace keeps both keys for shape fidelity, but the
   Current contract applies no `≥ 0.05` clamp, so they are always equal. This is a
   statement about the contract, not a choice.

## 6. Production readiness assessment

**Is the main chain already implementable by a formal engineer?**
Almost. The *behaviour* is: aggregation, gate semantics, failure branch, floor, base
multiplication, temperature curve and all four evaluators are specified tightly enough to
implement with no guessing, and the P0 goldens reproduce exactly. An engineer can build a
numerically correct Fixed Bake evaluator today from 开发需求 §3.3/§3.4/§4.3/§7 alone.

**What contracts are still missing?** As of the 2026-09-18 rulings: **none that block.**
The four items that previously did are now closed —

1. ~~resolved profile payload key names~~ (GAP-001 ✅ canonicalised to the 开发需求
   snake_case set);
2. ~~Trace key set~~ (GAP-002 ✅ dead keys deleted, `gateFailureBranch` added);
3. ~~`null` vs missing~~ (GAP-003 ✅ explicit `null` = IGNORED);
4. ~~legacy `gatePolicy`~~ (GAP-004 ✅ never shipped ⇒ any occurrence is an error).

Nothing in the remaining list (GAP-005 … GAP-012) blocks a legal configuration.

**Is there an architecture blocker?** No. Nothing found while building the slice required a
Bake DSL, an expression language, authorable ordering, early return, a Factor Tree, a
third role tier, or a per-mode program. The `CORE | SECONDARY | IGNORED` plus
automatic-gate model was sufficient for every case exercised, including all the boundary
cases the task nominated. The gaps were naming and edge-case ownership, never shape.

**Caveat that must not be lost:** the *production* line (`programaticHitFish`, W6 head
`0d94319`, 62 B-module tests green / 231 total) still carries the **pre-2026-09-17**
semantics listed in Main Control §26.4 deltas 1–9 — in particular the deleted `gatePolicy`
field, the removed `1/6` secondary loss with its `0.25541281188299536` cap, the old output
name, and the `0.30` ACCEPTABLE anchor. That code has **not** been migrated. This reference
implements the post-delta contract; the two will disagree until the migration lands.

**One caveat on the rulings themselves:** they currently live in this repository plus the
two edited Notion pages. Recorded project decisions belong in Main Control
(§26-style ruling section) — that page was outside this session's two-page write scope, so
**the ruling trace is still outstanding.**

## 7. Write-back status

**Done 2026-09-18** — the two authorised authority pages were edited and each read
back in full:

| Page | Edit | Verified |
| --- | --- | --- |
| Schema & Validator (`3dca4137d23681e28c5bc2f29c63dc16`) | new §1.1 canonical `resolvedComponentProfiles` key table; §3.8 `BakeEvaluationTrace` rewritten to the post-2026-09-17 key set; 2026-09-17 field-name note replaced by the 2026-09-18 ruling + negative-knowledge warning | headings §1–§11 intact, new §1.1 present, no `****` corruption |
| Bake Authoring / 条件开关 Working (`3dca4137d236816ab0add70228a80d51`) | §6.2 Feeding Layer keys and §6.3 Structure key → snake_case, plus a one-line ruling note | §6.1–§6.4 and the historical tail intact |

Both pages had a `last_edited_time` of 2026-09-17 (≈24h stale) before the edit, so no
concurrent writer was active. Writes were narrow `update_content` deltas with distinct
anchors, then read back whole-page.

**Still outstanding (both outside the authorised two-page scope):**

1. **Ruling trace.** Recorded project decisions belong in Main Control
   (`3dda4137d2368109aa54ec4f7acbab26`, §26-style section). The four adjudications
   currently live in this repository plus the two edited pages, but not in the branch's
   ruling log. Append one narrow section.
2. **One residual string.** 开发需求 §4.1's inline example writes
   `time_period_coefficient[DAWN]` while §4.0's own table writes
   `time_period_activity_coefficient[DAWN]`. Under the GAP-001 ruling the §4.0 spelling
   wins, so that example should be corrected.

**Also noticed but not touched:** the 条件开关 page's *title* still reads
`…｜AggregationRole constrains GatePolicy`, which references the deleted field. Renaming a
page changes its link/URL, so it was left alone — worth a separate decision.

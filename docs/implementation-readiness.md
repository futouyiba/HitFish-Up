# 0.3.4.0-B Fixed Bake — Implementation Readiness

Result of one real vertical implementation (`reference/0340-fixed-bake/`) against the
Current 0.3.4.0-B contract. **REFERENCE / VALIDATION — not promoted.**

**Answer in one line:** the main chain is **~90% uniquely implementable**; the numbers,
the gates, the aggregation and the floor are unambiguous and reproduce the P0 goldens
exactly. What still blocks a *formal* engineer is **not algorithm** — it is **two schema
questions**: the resolved profile payload key names (GAP-001) and the Trace key names
(GAP-002). Two further readings require an owner adjudication (GAP-003, GAP-004).

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

### SPEC_GAP

- **GAP-001** — component profile payload key names are not canonicalised
  (Structure / Feeding Layer / Time Period each have 2–3 spellings across Current pages).
  **Blocking.**
- **GAP-002** — the Trace schema was annotated but never rewritten after the 2026-09-17
  deltas; output key, failure-branch representation and dead keys are undefined.
  **Blocking for trace conformance, not for the number.**
- **GAP-005** — runtime handling of an out-of-`[0,1]` authored fit is defined nowhere
  (only in an explicitly non-Current implementation history). Partially blocking.
- **GAP-006** — empty `feedingEcologyLayers[]`: `max()` over an empty set is undefined.
- **GAP-007** — a fish with **no** CORE binding: the empty-product convention is not stated.
- **GAP-008** — degenerate temperature bands (`accept_min == fav_min`) are legal by the
  stated constraint but their meaning is unstated (the value is derivable; the legality is
  not).

### DESIGN_CHOICE_REQUIRED

- **GAP-003** — does an explicit `"aggregationRole": null` mean IGNORED (Bass fixture
  reading) or "configured but missing" = error (`Missing ≠ Ignore`)?
- **GAP-004** — a serialized legacy `gatePolicy` key: hard error (Bass slice V6) or
  read-through when inert (Schema §5.1)? Two Current clauses disagree.

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
total       38
passed      38
failed      0
skipped     0
```

- **Fixture goldens (8 cases)** — CG-01 `1.0000000000`, CG-02 `0.3190909091`,
  CG-03 `0.1125000000`, temperature-gate failure (non-background `0` / background
  `0.10`), background floor `0.0306818182 → 0.10`, and two Base-scaling cases. The goldens
  were reproduced a second time by an independent script that applies the §3.4 / §4.3
  formulas without importing the reference.
- **Semantic cases (19)** — the task's Case 1–15 re-expressed against the Current contract
  (Case 7 "residual gate" is now "a near-zero nonzero coefficient is not a gate failure";
  Case 9 "multiple failed gates" collapses to one branch because there is no cap to
  combine).
- **Migration / legacy (3)**, **validation (7)**, **property invariants (8)**.
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

1. **Gate failure → `None` aggregate.** On the failure branch the Trace reports `null` for
   `coreProduct` / `secondaryProduct` / `secondaryFactor` / `rawEnvCoeff` while still
   reporting per-condition fits (which had to be computed to evaluate the gate). The text
   only says the formula "is not computed". (GAP-009)
2. **No runtime clamp, no runtime range check.** An out-of-`[0,1]` authored value passes
   through unchanged and can push `FinalEnvCoeff` above `1`. Deliberate: taking no decision
   keeps GAP-005 visible rather than hidden behind a clamp. (GAP-005)
3. **`appliedFit == rawFit`.** The trace keeps both keys for shape fidelity with Schema
   §3.8, but the Current contract applies no `≥ 0.05` clamp, so they are always equal.
4. **Superseded trace keys retained as `null`.** `secondaryLossRaw`, `secondaryLossApplied`
   and the cap concept are dead under the new aggregation; the keys are kept as `null`
   purely so the Trace shape still matches the published schema. (GAP-002)
5. **`coreLoss = None` when any CORE fit is 0** — avoids emitting `-inf`. Only reachable
   when `temp_threshold = 0`. (GAP-012)
6. **Empty product = 1.** Used twice: empty SECONDARY (explicitly authorised) and empty
   CORE (not authorised anywhere). (GAP-007)
7. **`null` role → IGNORED, absent row → error.** A split reading of the two authorities
   that speak to this. (GAP-003)
8. **Legacy `gatePolicy` with an inert value is read through, other values rejected.** Picks
   one side of two disagreeing Current clauses. (GAP-004)

## 6. Production readiness assessment

**Is the main chain already implementable by a formal engineer?**
Almost. The *behaviour* is: aggregation, gate semantics, failure branch, floor, base
multiplication, temperature curve and all four evaluators are specified tightly enough to
implement with no guessing, and the P0 goldens reproduce exactly. An engineer can build a
numerically correct Fixed Bake evaluator today from 开发需求 §3.3/§3.4/§4.3/§7 alone.

**What contracts are still missing?** Precisely two, plus two readings:

1. the **resolved profile payload key names** for Structure / Feeding Layer / Time Period
   (GAP-001) — this is a *serialization* contract, and without it two correct
   implementations still cannot interoperate;
2. the **Trace key names** after the 2026-09-17 deltas (GAP-002) — the schema page was
   annotated, not rewritten;
3. an owner line on **`null` vs missing** (GAP-003);
4. an owner line on **legacy `gatePolicy`** handling (GAP-004).

Nothing in the remaining list (GAP-005 … GAP-012) blocks a legal configuration.

**Is there an architecture blocker?** No. Nothing found while building the slice required a
Bake DSL, an expression language, authorable ordering, early return, a Factor Tree, a
third role tier, or a per-mode program. The `CORE | SECONDARY | IGNORED` plus
automatic-gate model was sufficient for every case exercised, including all the boundary
cases the task nominated. The gaps are naming and edge-case ownership, not shape.

**Caveat that must not be lost:** the *production* line (`programaticHitFish`, W6 head
`0d94319`, 62 B-module tests green / 231 total) still carries the **pre-2026-09-17**
semantics listed in Main Control §26.4 deltas 1–9 — in particular the deleted `gatePolicy`
field, the removed `1/6` secondary loss with its `0.25541281188299536` cap, the old output
name, and the `0.30` ACCEPTABLE anchor. That code has **not** been migrated. This reference
implements the post-delta contract; the two will disagree until the migration lands.

## 7. Next minimal action

**One page, one table:** add a canonical *resolved payload key-name table* to
Schema & Validator §1/§3 (Structure, Feeding Layer, Time Period profile keys — GAP-001) and
rewrite its §3.8 `BakeEvaluationTrace` block to the post-2026-09-17 key set (GAP-002). Both
are documentation-only edits on one existing page, and together they convert the two
blocking gaps into fixed contracts. Everything else in this report can wait.

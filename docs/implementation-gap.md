# 0.3.4.0-B Fixed Bake — Implementation Gap Log

Real engineering problems found while building the executable reference in
`reference/0340-fixed-bake/`. Only gaps that actually block or dilute a unique
implementation are listed; phrasing improvements are not.

Authority read 2026-09-18 (Notion). Page IDs are given so each claim is checkable.

**Status: GAP-001 … GAP-004 were adjudicated on 2026-09-18 — all four are RESOLVED.**
Eight non-blocking items remain (GAP-005 … GAP-012).

| ID | Area | Status | Blocking |
| --- | --- | --- | --- |
| GAP-001 | Atomic factor evaluation (input shape) | **RESOLVED** — canonicalised to the 开发需求 snake_case set | was YES |
| GAP-002 | Debug Trace | **RESOLVED** — dead keys deleted, `gateFailureBranch` added | was YES |
| GAP-003 | ConditionRole / input validation | **RESOLVED** — explicit `null` = IGNORED | was DESIGN_CHOICE |
| GAP-004 | Legacy migration / invalid config | **RESOLVED** — GatePolicy never shipped; any occurrence is an error | was DESIGN_CHOICE |
| GAP-005 | Atomic factor evaluation (numeric domain) | SPEC_GAP | Partial |
| GAP-006 | ConditionGroupSnapshot | SPEC_GAP | NO |
| GAP-007 | Core aggregation | SPEC_GAP | NO |
| GAP-008 | Temperature evaluator (degenerate bands) | SPEC_GAP | NO |
| GAP-009 | Debug Trace / Gate evaluation | NON_BLOCKING_AMBIGUITY | NO |
| GAP-010 | Gate evaluation / validation layering | NON_BLOCKING_AMBIGUITY | NO |
| GAP-011 | Naming | NON_BLOCKING_AMBIGUITY | NO |
| GAP-012 | Temperature gate edge value | NON_BLOCKING_AMBIGUITY | NO |

---

## Rulings applied 2026-09-18

Decided by the Design Owner in the readiness-validation session; applied to the
reference implementation, and written back to the two authority pages
(Schema & Validator; Bake Authoring / 条件开关 Working).

| ID | Ruling | Rationale |
| --- | --- | --- |
| GAP-001 | The four component profiles use the **开发需求 §4.0 / §4.3 snake_case key names** in the resolved payload (`structure_affinity`, `foraging_surface_affinity` / `_middle_` / `_bottom_`, `time_period_activity_coefficient`). The camelCase spellings on the 条件开关 page are stale. | Not a free choice: §26.4 delta 7 already pinned the Temperature profile to that spelling in the resolved payload, so the other three follow the same layer. 条件开关's §6.2/§6.3 are annotation-method text and were written before that pin. |
| GAP-002 | **Delete** `gateFailureCap` / `secondaryLossRaw` / `secondaryLossApplied` from the Trace; add `gateFailureBranch {applied, branch, failedConditions}`; rename `factorResults[].importance` → `aggregationRole`. Leave a negative-knowledge note saying they were removed and must not be re-added. | No legacy data (new requirement), no implemented consumer (production not migrated, Bake Preview not built), and no information loss — the dead keys' content is fully expressed by `secondaryProduct` / `secondaryFactor` / `gateFailureBranch`. A schema whose only job is explainability must not advertise concepts that no longer exist. |
| GAP-003 | An explicit `"aggregationRole": null` is an **explicit IGNORED**. Only a wholly absent binding row is a resolve error. | Satisfies both Current clauses at once: the Bass fixture's `null` reads as IGNORED, and 开发需求 §4.5's "missing ≠ ignored" still governs absent rows. |
| GAP-004 | `gatePolicy` **never shipped**, so there is no legacy payload and no read-through channel. Any occurrence of the key is an error (Bass slice §8 V6, read literally). Docs that still describe it as current are to be made consistent with the spec. | Owner 2026-09-18: it is a new feature with no historical/stock data, so there is nothing to migrate. A role edit (e.g. CORE → SECONDARY) is ordinary authoring — bake always uses the *current* role; no migration logic is involved. |

**Written back 2026-09-18** to the two authority pages — Schema & Validator
(`3dca4137d23681e28c5bc2f29c63dc16`: new §1.1 key table + rewritten §3.8 Trace block +
ruling note) and Bake Authoring / 条件开关 Working
(`3dca4137d236816ab0add70228a80d51`: §6.2 / §6.3 profile keys → snake_case + ruling
note). Both were read back in full and verified. Two items remain outside that scope: the
Main Control ruling trace, and 开发需求 §4.1's `time_period_coefficient` example string.

**Consequences for the reference implementation:** `role_of()` rejects any
`gatePolicy` key outright (the inert-value read-through path was removed);
the Trace no longer emits the three dead keys; `spatial_distribution_weight`
follows §26.4 delta 6. Test count went 38 → 39 (the old "OFF + NONE normalises"
test was replaced by "any gatePolicy is rejected", plus a dead-key-absence test).

**Residual (not covered by these rulings, needs one more edit):** 开发需求 §4.1's
inline example writes `time_period_coefficient[DAWN]` while §4.0's own table
writes `time_period_activity_coefficient[DAWN]`. Under the GAP-001 ruling the
§4.0 spelling wins, so §4.1's example string should be corrected — that is a
**third page** and was outside the two-page write scope of this session.

---

## GAP-001

**Area:** Atomic factor evaluation — resolved component profile payload key names
**Status:** RESOLVED 2026-09-18 (see Rulings above)

**Authority:**
- 中鱼0.3.4.0-B｜开发需求 §4.0 / §4.1–§4.4 (`3dda4137d23681c68ec3fb1944573af4`) uses
  snake_case config-table column names.
- 0.3.4.0-B｜Bake Authoring / 条件开关 Working §6.2 / §6.3
  (`3dca4137d236816ab0add70228a80d51`) uses camelCase names for the same things.

**What is known:** the six **Temperature** keys *are* canonical and identical on both
pages: `temp_accept_min / temp_fav_min / temp_fav_max / temp_accept_max /
temp_threshold / falloff_shape` (开发需求 §4.3; Main Control §26.4 delta 7 pins this).
The temperature curve and gate formulas are fully specified.

**What is missing:** the canonical key names for the other three profiles:

| Component | 开发需求 §4.0 | 条件开关 §6.2/§6.3 |
| --- | --- | --- |
| Structure | `structure_affinity[StructureType]` | `structureAffinity[CanonicalStructureType]` |
| Feeding Layer | `foraging_surface_affinity` / `foraging_middle_affinity` / `foraging_bottom_affinity` | `surfaceAffinity` / `midAffinity` / `bottomAffinity` |
| Time Period | `time_period_activity_coefficient[DAWN]` | (unnamed); and 开发需求 §4.1's own example writes `time_period_coefficient[DAWN]` |

**Why code cannot uniquely decide:** the numeric semantics are identical, so every
candidate produces the same numbers — but `ResolvedSpatialOpportunitySubject` is a
*serialized* payload. Two implementations using different key names cannot exchange
subjects, cannot share fixtures, and cannot both be "the" contract. There is no
authority statement that one spelling wins.

**Candidate A:** adopt 开发需求 §4.0 config-table names verbatim (this reference does).
**Candidate B:** adopt 条件开关 §6.2/§6.3 camelCase names as the resolved-payload shape,
treating §4.0 names as raw table columns only (i.e. resolved payload ≠ table column).

**Affected code/tests:** `fixed_bake.evaluate_fit`, `fixtures/bass_q3.json`, every
fixture and any serializer/deserializer pair.
**Blocking:** YES.
**Do not decide:** this reference uses Candidate A so the slice can run at all; it is
not a recommendation.

---

## GAP-002

**Area:** Debug Trace
**Status:** RESOLVED 2026-09-18 (see Rulings above)

**Authority:** 0.3.4.0-B｜Bake Authoring Schema & Validator Contract §3.8
(`3dca4137d23681e28c5bc2f29c63dc16`) defines `BakeEvaluationTrace`. Its own
2026-09-17 note states that in that structure `spatialOpportunityIntensity` is a
**historical** key and `gateFailureCap?` is superseded by the failure branch, "gateResults[]
保留为展示位". Main Control §25.6 / §26.4 delta 6 (`3dda4137d2368109aa54ec4f7acbab26`)
require the *code* field and trace key to become `spatial_distribution_weight`.

**What is known:** the value is `SpatialDistributionWeight = BaseOpportunityIntensity ×
FinalEnvCoeff` (开发需求 §3.5), and the trace must expose per-condition lookup/curve
values, role, reduction, and gate firing (开发需求 §3.5, §8).

**What is missing:** the trace schema was *annotated*, never rewritten, so the canonical
names are undefined for: (a) the output key, (b) the representation of the gate-failure
branch, (c) whether `factorResults[].importance` is renamed to `aggregationRole`,
(d) whether the now-dead `secondaryLossRaw / secondaryLossApplied / gateFailureCap` keys
are deleted or retained as `null`.

**Why code cannot uniquely decide:** an engineer writing a trace consumer cannot match
keys against a schema that still describes the superseded model. No candidate is
excluded by the text.

**Candidate A:** `spatialDistributionWeight`; replace the cap key with
`gateFailureBranch {applied, branch, failedConditions}`; keep the dead keys as `null`
for shape compatibility (this reference does this).
**Candidate B:** snake_case `spatial_distribution_weight`; delete superseded keys; express
the branch only through `gateResults[].passed`.

**Affected code/tests:** the whole Trace surface; any Bake Preview / inspector;
`test_case15_trace_explains_the_result`.
**Blocking:** YES for exact trace conformance; NO for the numeric contract (every
candidate yields the same weight).
**Do not decide:** the reference picks A to be runnable, not as a ruling.

---

## GAP-003

**Area:** ConditionRole resolution / input validation
**Status:** RESOLVED 2026-09-18 — explicit `null` = IGNORED (see Rulings above)

**Authority:** 0.3.4.0-B｜Bass NORMAL Fixed Template Vertical Slice §5
(`3dda4137d236818c9b61e6bc7fc348a7`) serializes
`{"conditionKey":"TIME_PERIOD","aggregationRole":null}` and annotates
"`TIME_PERIOD` 的 `null` = IGNORED（自动不消费）". But 开发需求 §4.5 guardrail 2 and
Schema & Validator §5 require the opposite distinction: "忽略 = 作者显式决定，与
「缺配置 / 应配而缺」不同——后者仍是错误，不得静默当作忽略".

**What is known:** an explicit author decision to ignore is legal and costs nothing at
runtime; a *required* binding that is simply absent is an error.

**What is missing:** which side an explicit `null` falls on.

**Why code cannot uniquely decide:** the golden P0 fixture (Bass slice §5) cannot be
read at all until this is settled, and both readings are supported by a Current page.

**Candidate A:** `"aggregationRole": null` → IGNORED; only a wholly absent binding row is
an error (this reference does this, so the Bass fixture compiles).
**Candidate B:** `null` → ERROR; only the explicit token `"IGNORED"` is legal, because an
explicit author decision is being claimed.

**Affected code/tests:** `fixed_bake.role_of` / `_binding_rows`; `test_case14_*`;
every serialized subject.
**Blocking:** NO for the Bass fixture under A; the choice is unavoidable for any other
payload.
**Do not decide:** the reference follows A only because the P0 fixture demands it.

---

## GAP-004

**Area:** Legacy migration / invalid config handling
**Status:** RESOLVED 2026-09-18 — GatePolicy never shipped; any occurrence is an error (see Rulings above)

**Authority conflict — two Current clauses disagree:**
- Schema & Validator §5.1: `legacy OFF（GatePolicy NONE / absent）→ IGNORED（自动不消费）`.
- Bass Vertical Slice §8 **V6**: `序列化中出现 gatePolicy 字段 → ERROR（legacy 字段，仅 migration 读入）`.
- Executable Delta Spec delta 2: the `gatePolicy` field is deleted, "含 fixture 四处".

**What is known:** the field is gone from the Current model; gate is automatic for CORE.

**What is missing:** whether a serialized `gatePolicy` key with an inert value (`NONE`) is
a hard error (V6) or an accepted migration read-in (§5.1).

**Why code cannot uniquely decide:** §5.1 says `GatePolicy NONE / absent` is fine; V6 says
any occurrence is an error. Both are Current pages of the same branch.

**Candidate A:** any `gatePolicy` key at all → ERROR (V6 / delta 2 reading).
**Candidate B:** `gatePolicy` absent or `NONE` → inert; any other value → migration
diagnostic requiring an explicit content decision (this reference does this).

**Affected code/tests:** `fixed_bake.role_of`; `TestMigrationAndLegacy`.
**Blocking:** NO — both readings agree on the important case (a non-NONE policy must never
be silently coerced).
**Do not decide:** needs one adjudication line in §26 or the Schema page.

---

## GAP-005

**Area:** Atomic factor evaluation — numeric domain
**Status:** SPEC_GAP

**Authority:** 开发需求 §8 lists "习性表数值超出 `[0,1]`" as a **publish-time** blocker,
i.e. config-validator-owned. The only statement about *runtime* behaviour is Bass Vertical
Slice §10: "离散 authored affinity 不允许 Runtime 静默 clamp ... 直接报错" — but §10 is
explicitly stamped "**NOT W4B Current Contract**" and is implementation history.

**What is known:** legal authored values are `[0,1]`; `1` means "no loss" and `>1` is never
a bonus (AFLA §第一刀 数值域). The validator is supposed to stop out-of-range values
before they reach Runtime.

**What is missing:** what the runtime does if such a value arrives anyway — clamp, raise,
or pass through — and whether that differs between authored discrete values and
evaluator-produced continuous values (the historical note distinguishes them).

**Why code cannot uniquely decide:** "validator owns it upstream" is not a runtime
specification. Silently clamping is explicitly forbidden by the task's own rules, and so
is inventing a default.

**Candidate A:** runtime raises (fail-closed), matching the config validator and preserving
the `[0,1]` EnvCoeff invariant.
**Candidate B:** runtime clamps to `[0,1]` (the historical `clamp01` in the AFLA doc).
**Candidate C:** pass through unmodified (pure formula, no decision taken).

**Affected code/tests:** `fixed_bake.evaluate_fit`; `test_case13_out_of_range_authored_fit`
(which is a *characterisation* test, not a contract assertion — it pins 1.5 → EnvCoeff 1.5).
**Blocking:** Partial. It does not block any legal configuration; it blocks the
"undefined input" contract and it is the only way `FinalEnvCoeff <= 1.0` can be violated.
**Do not decide:** the reference takes Candidate C on purpose, so that the gap stays
visible instead of being papered over.

---

## GAP-006

**Area:** ConditionGroupSnapshot
**Status:** SPEC_GAP

**Authority:** 开发需求 §3.2 specifies Feeding Layer evaluation as "含多个水层时取其中
最大亲和"; §3.1 defines the field as `feedingEcologyLayers // 觅食水层集合（可多选…）`.

**What is known:** with ≥1 layer the fit is `max(affinity[layer])`.

**What is missing:** whether an **empty** layer set is a legal `ConditionGroup`, and if so
what the fit is. `max()` over an empty set has no value.

**Why code cannot uniquely decide:** `max(∅)` could legitimately map to 0 (nothing
available), 1 (no constraint), or be rejected as a malformed condition group. Authority
says nothing.

**Candidate A:** empty set is illegal — raise (this reference does this).
**Candidate B:** legal; fit = 0 (consistent with "no suitable layer here").
**Candidate C:** legal; fit = 1 (treated as "the condition does not constrain").

**Affected code/tests:** `fixed_bake.evaluate_fit`; `test_empty_layer_set_is_undefined`.
Bears on the ConditionGroup validator: §8 lists "条件组必要事实缺失" as blocking but does
not say whether "a set field present but empty" counts as missing.
**Blocking:** NO.
**Do not decide.**

---

## GAP-007

**Area:** Core aggregation
**Status:** SPEC_GAP

**Authority:** 开发需求 §3.4 defines `CoreProduct = Π_CORE 适配值` and requires only that
conditions configured as CORE/SECONDARY have complete profiles; §4.5 says the four slots
"不必配满" but frames that about leaving some IGNORED, not about leaving *all* IGNORED.

**What is known:** for ≥1 CORE binding the product is unambiguous, and the empty product of
SECONDARY is explicitly covered (`SecondaryProduct = 1` ⇒ `SecondaryFactor = 1`).

**What is missing:** whether a fish with **no** CORE binding is legal, and if so whether
`CoreProduct` is the multiplicative identity `1` or the config is rejected.

**Why code cannot uniquely decide:** the Executable Delta Spec's **superseded** test list
contains `A12 empty Core / Secondary set has identity 1`, but that list also contains
`A5/A6/A9/A10` which delta 7 explicitly invalidates — so it cannot be cited as current
contract. Current pages never state the empty-Core convention.

**Candidate A:** identity `1` — such a fish gets no core environmental differentiation and
its weight is driven only by SECONDARY and the floor (this reference does this).
**Candidate B:** at least one CORE binding is mandatory — compile error.

**Affected code/tests:** `fixed_bake._product`; `test_p8_no_core_bindings_yields_multiplicative_identity`.
**Blocking:** NO.
**Do not decide.**

---

## GAP-008

**Area:** Temperature evaluator — degenerate bands
**Status:** SPEC_GAP

**Authority:** 开发需求 §4.3 hard constraint is `temp_accept_min ≤ temp_fav_min ≤
temp_fav_max ≤ temp_accept_max` — equality is therefore allowed. The falloff formula divides
by `temp_fav_min − temp_accept_min` and by `temp_accept_max − temp_fav_max`.

**What is known:** the intended shape (0 outside accept, 1 inside fav, ramp between).

**What is missing:** what a zero-width transition band means, and whether such a profile is
legal at all. A zero-width band makes the divisor 0.

**Why code cannot uniquely decide:** a naive implementation divides by zero and produces
`NaN`; nothing in the authority forbids equality, and §8's validation list does not include
this shape.

**Candidate A:** equality is legal and the band is simply empty (this reference does this —
correct branch ordering makes the division unreachable, so no NaN occurs).
**Candidate B:** forbid equality in validation to keep the formula total.

**Affected code/tests:** `fixed_bake.point_fit`.
**Blocking:** NO — the value is derivable, the input legality is not.
**Do not decide.**

---

## GAP-009

**Area:** Debug Trace content on the gate-failure branch
**Status:** NON_BLOCKING_AMBIGUITY

**Authority:** 开发需求 §3.4: "若任一 CORE 门控失败 → 走 §3.3 失败分支，**不计算上式**".
The W4B runtime spine orders gate evaluation before factor evaluation.

**What is known:** the final value is exactly `envCoeffMin` (background) or `0`
(non-background), and the aggregate is not applied.

**What is missing:** what the Trace reports on that branch — per-condition fits (necessarily
computed in order to evaluate the gate), and whether `rawEnvCoeff` / `coreProduct` /
`secondaryFactor` appear, are `null`, or are absent.

**Why it is non-blocking:** no candidate changes the weight, and all candidates explain the
result equally well. It only affects trace consumers' expectations.

**Candidate A:** report fits; `null` the aggregate products and `rawEnvCoeff` (this
reference does this).
**Candidate B:** report nothing but the branch, since the formula "is not computed".

**Affected code/tests:** `fixed_bake.evaluate`; `TestFixtureGoldens` (asserts
`rawEnvCoeff is None` on gate failure).
**Blocking:** NO.
**Do not decide.**

---

## GAP-010

**Area:** Gate evaluation / validation layering
**Status:** NON_BLOCKING_AMBIGUITY

**Authority:** Schema & Validator §5.2: "温度门控参数（`temp_threshold` / `falloff_shape`）
只对绑定为 **CORE / SECONDARY** 的 Temperature Profile 要求完整". 开发需求 §3.3 and
Schema §4 make the temperature gate fire **only** for CORE.

**What is known:** a SECONDARY Temperature binding never evaluates a gate.

**What is missing:** why SECONDARY is required to carry gate parameters it can never use.

**Why it is non-blocking:** it is a validation-scope statement, not a runtime requirement; it
costs an author a few numbers and changes no result.

**Candidate A:** intentional — the requirement keeps a later role change SECONDARY→CORE from
invalidating the profile (recommended reading).
**Candidate B:** carry-over from the deleted GatePolicy era; should be CORE-only.

**Affected code/tests:** nothing in this reference (profile completeness is validator-owned
here).
**Blocking:** NO.
**Do not decide.**

---

## GAP-011

**Area:** Naming
**Status:** NON_BLOCKING_AMBIGUITY

**Authority:** the W4B spine and Schema & Validator §2 name the runtime input
`ConditionGroup`. The Executable Delta Spec's Current constraints also say `ConditionGroup`,
but the same page's historical API sketch declares
`class ConditionGroupSnapshot` and `BakeEvaluationResult`.

**What is missing:** whether `ConditionGroupSnapshot` is the serialized/protocol name of
`ConditionGroup` or was simply an implementation-era name.

**Why it is non-blocking:** one concept, two labels; no behavioural consequence.

**Candidate A:** `ConditionGroup` is canonical (Current sections win over the historical
sketch) — this reference uses this.
**Candidate B:** keep both: `ConditionGroup` for the authoring/reference language,
`ConditionGroupSnapshot` for the boundary payload.

**Affected code/tests:** parameter naming only.
**Blocking:** NO.
**Do not decide.**

---

## GAP-012

**Area:** Temperature gate edge value
**Status:** NON_BLOCKING_AMBIGUITY

**Authority:** 开发需求 §4.3 constrains `temp_threshold ∈ 0..1`; §3.3 defines the gate as
failing when the fit is **below** `temp_threshold`.

**What is known:** with `temp_threshold > 0`, `fit == 0` always fails the gate for a CORE
Temperature binding.

**What is missing:** whether `temp_threshold = 0` is meant as "never gate" (it is legal by
the stated range) and whether the resulting `CoreProduct = 0` — whose logarithm is `-inf` —
is acceptable, or whether some minimum should exist.

**Why it is non-blocking:** the weight is well defined (`0`); only the reported loss is
undefined. This reference guards `coreLoss` to `None` when a CORE fit is 0 and therefore
never emits `-inf`.

**Candidate A:** `0` means "no gate" and is a legal authoring choice.
**Candidate B:** require `temp_threshold > 0` (or a documented minimum) so a CORE fit of 0
always implies a gate failure.

**Affected code/tests:** `fixed_bake.gate_failed`, `fixed_bake.evaluate` (`core_loss` guard).
**Blocking:** NO.
**Do not decide.**

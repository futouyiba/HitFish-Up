# 0.3.4.0-B Fixed Bake — Executable Reference

**STATUS: REFERENCE / VALIDATION — NOT the production implementation.**
Nothing in this directory is promoted, frozen, or authoritative. The production
implementation lives in `futouyiba/programaticHitFish` and is owned by that line;
this directory is a read-only-model reference built to answer one question:

> Can an engineer implement the Current 0.3.4.0-B Fixed Bake contract without
> guessing — and if not, exactly where must they stop and ask?

## Files

| File | What it is |
| --- | --- |
| `fixed_bake.py` | The vertical slice: `evaluate(subject, seed, conditionGroup) -> weight + Trace`. Stdlib only. |
| `fixtures/bass_q3.json` | The P0 golden fixture (Bass Q3, CG-01/02/03 + gate/floor/base mutation cases). |
| `test_fixed_bake.py` | Semantic cases (§十 of the task) + contract-derived property tests. |

## Run

```bash
cd reference/0340-fixed-bake
python3 -m pytest test_fixed_bake.py -q     # or: python3 -m unittest test_fixed_bake
python3 fixed_bake.py                        # print one full Trace for CG-01
```

## Scope of this slice

In: `ResolvedSpatialOpportunitySubject` + `ResolvedOpportunitySeed` + `ConditionGroup`
→ Gate evaluation → Atomic factor evaluation → Core/Secondary aggregation →
gate-failure branch / background floor → `FinalEnvCoeff` → `SpatialDistributionWeight`
+ Trace.

Out (deliberately): Activity, Functional Capacity, Feeding Readiness, Fish Condition,
Response, Presentation/Exposure, Quality Selection, Engagement Mode routing, Fish
materialisation, any Bake DSL / expression language, Editor UI, persistence,
performance work.

## Authority

Read from Notion on 2026-09-18. Full list, plus the superseded premises this
reference deliberately does **not** implement, is in
[`docs/implementation-readiness.md`](../../docs/implementation-readiness.md) §1.
Open contract gaps found by building this slice are in
[`docs/implementation-gap.md`](../../docs/implementation-gap.md).

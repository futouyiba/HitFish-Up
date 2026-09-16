# DEVSET-REGISTRY — Development Set 注册表(R0/R1/R2/R3 + Round 1)

- 状态:**EXECUTED UNDER R3 CANDIDATE(2026-09-16)**——Design Owner Development Review(D1–D6)后,在 `programaticHitFish` `feature/pc-cue-validation-r2-clean` 以 R2 契约执行;fixture 见该仓 `pc_validation/fixtures/devset_r2_backfilled.json`;R1 回填版本保留为 provenance
- 来源:baseline [R0 §12](../baselines/FCF-PC-BASELINE-R0-20260915.md) 枚举 + Design Owner 2026-09-16 裁决(新增 Walleye)+ 回填材料:
  - Presentation Adapter Development Set Manifest v1(frozen 2026-08-25,Notion `3c7a4137d23681b7adc7cafa9f444b6b`)
  - Response Language Contract Delta R0 §14 Expression Pressure Test(2026-09-05,Notion `3d0a4137d2368168b678ccfafc85583c`)
- 纪律:本表不发明语义;来源未定值标 `UNKNOWN_FROM_SOURCE`;无任何 ResponseBand 数字;DEV regression 证明事实需求/可表达性/所需 delta/ownership 结果,不证明 HIGH=多少。
- 据本表任何 case 修改 baseline 时,该 case 永久保持 Development 身份(R0 §10)。

## Presentation 案例

| case_id | Presentation | classification | requested_deltas | ownership | 备注 |
|---|---|---|---|---|---|
| DEV-001 | Spinnerbait steady | COVERED | — | NO_DOCUMENTED_CONFLICT | optical motion + flash + mechanical;frame metadata 照 A2 |
| DEV-002 | Spinnerbait jerk-pause | COVERED | — | NO_DOCUMENTED_CONFLICT | 14.1 判定:speed_change + pause_duration + ALL 足够 |
| DEV-003 | Bread / prepared-food passive | ANNOTATION_ONLY | chemical_signature values;PREPARED_FOOD member | NO_DOCUMENTED_CONFLICT | CHEMICAL_INTENSITY_GAP_WATCH;species UNKNOWN_FROM_SOURCE |
| DEV-004 | Shrimp-like bottom hop | COVERED | — | NO_DOCUMENTED_CONFLICT | relation.bottom;不新增 bottom_disturbance |
| DEV-005 | Spoon steady | COVERED | — | NO_DOCUMENTED_CONFLICT | Optical family 复用 |
| DEV-006 | Spoon oscillating | **COVERED**(D2 重分类) | — | NO_DOCUMENTED_CONFLICT | 复用 admitted cues(flash/direction_change/speed_change/speed);displacement 依赖已移除(D1) |
| DEV-007 | Fly dead drift | COVERED | — | NO_DOCUMENTED_CONFLICT | LOCAL_WATER 为 fixture 级声明(A2 不选 universal frame) |
| DEV-008 | Fly twitch | COVERED | — | NO_DOCUMENTED_CONFLICT | 同 representation 换 kinematics,复用 item-side 语义 |
| DEV-009 | Topwater popper pop-pause | COVERED | — | NO_DOCUMENTED_CONFLICT | relation.surface;不升级 surface_pop;sound_pattern 未用 |
| DEV-010 | Soft worm bottom drag | **UNRESOLVED** | D3 问题:relation.bottom + 常规 motion facts 是否足够;缺的是 continuous-contact cue / temporal summary / 其它 reusable primitive | NO_DOCUMENTED_CONFLICT | flag `KNOWN_DEV_GAP_CONTINUOUS_BOTTOM_CONTACT_MECHANICAL_CAUSE`;不阻塞 holdout;永不做 blind evidence |

## Strategy Story 案例(回填后重构编号;旧表 S1–S4 作废)

| case_id | Story | classification | requested_deltas | ownership | 备注 |
|---|---|---|---|---|---|
| DEV-S1 | Bass jerk-pause(14.1) | COVERED | — | NO_DOCUMENTED_CONFLICT | Profile=Species×Mode;affinity 值 UNKNOWN_FROM_SOURCE |
| DEV-S2 | Bass Spawn Guard(14.1) | COVERED | — | NO_DOCUMENTED_CONFLICT | relation.nest;NestThreat 非 mandatory 层 |
| DEV-S3 | Trout Match Hatch(14.1) | ANNOTATION_ONLY | prey_stage values | NO_DOCUMENTED_CONFLICT | field-to-field compare 已在语言契约 |
| DEV-S4 | Walleye low-light / hydro-acoustic(14.1;Owner 2026-09-16 加入) | COVERED | — | **LINT_WATCH_DOUBLE_COUNT**(D5) | light 已被 visual 因果链消费时 Response 不得再匿名读 context.light 二次计;独立因果作用例外且须 provenance |
| DEV-S5 | Scent feeder(R0 §12 Carp story;物种归属 UNKNOWN_FROM_SOURCE) | ANNOTATION_ONLY | chemical_signature values | NO_DOCUMENTED_CONFLICT | CHEMICAL_INTENSITY_GAP_WATCH;浓度 primitive 保持 candidate |

## Round 1 盲测案例纳入(2026-09-16,R3 裁决)

[Blind Holdout Round 1 报告](../holdout/FCF-PC-R2_BLIND_HOLDOUT_R1_20260916.md)(18 cases,H01–H18)经 Design Owner adjudication(`HOLDOUT_PASS_WITH_NARROW_DELTA`)后**全部转为永久 Development 材料**;fixture 见 `programaticHitFish` `pc_validation/fixtures/holdout_round1_devset.json`(保留 historical R2 分类 + R3 重分类)。

R3 重分类(仅限授权 delta):

| case | R2 盲测分类 | R3 分类 | 依据 |
|---|---|---|---|
| H12 / H13 | NEW_PRIMITIVE_REQUIRED | COVERED | Delta 1(contact disturbance primitive) |
| H07 | NEW_GENERIC_RULE_REQUIRED | COVERED(+`COUNTERFACTUAL_PENDING_MULTIPLICITY`) | Delta 2(composition contract;multiplicity 未准入,CF-MULTI-1 挂起) |
| H14 | ANNOTATION_ONLY | COVERED | Delta 3(复用 CRUSTACEAN,不加值不加维度) |
| H17 | NEW_PRIMITIVE_REQUIRED | NEW_PRIMITIVE_REQUIRED(维持) | chemical magnitude DEFERRED / NOT_ADMITTED(H17 仅 confirmatory) |
| 其余 14 | COVERED | COVERED | 不变 |

## 分布与特别报告(2026-09-16,R3 candidate run)

```text
Development 总集 33 = 原有 15 + Round 1 18
COVERED 29 / ANNOTATION_ONLY 3 / NEW_PRIMITIVE_REQUIRED 1(H17)/ UNRESOLVED 0
DEV-010 KNOWN_DEV_GAP 经 Delta 1 关闭(RESOLVED_BY_R3_DELTA_1;永久 Development 身份保留)
H10 首次行使 cue.sound_pattern(D6 UNEXERCISED 解除;combined dev set unused basis = 空)
chemical 缺口维持:DEV-003、DEV-S5(D4)
ownership lint watch 维持:DEV-S4(D5)
open counterfactual:CF-MULTI-1(OPEN_PENDING_EVIDENCE)——single vs multi-source 等聚合对照,
  只有明确 yes 才重开 multiplicity primitive admission request
```

```text
ROUND1 = HISTORICAL BLIND EVIDENCE
R3     = DEVELOPMENT CANDIDATE(NOT YET FROZEN / NOT_PROMOTED)
ROUND2 = NOT YET STARTED
```

完整机器可读结果:`programaticHitFish` `pc_validation/reports/pc_validation_report.json`(development_regression + open_counterfactuals 段)。

## 回填记录

| 日期 | 回填人 | 覆盖 case | 来源标注 | 冲突处理 |
|---|---|---|---|---|
| 2026-09-16 | Coding Agent | DEV-001..010, S1..S5 | Manifest v1 + Pressure Test 14.1 + R0 §12 + Owner 裁决 | 无来源冲突;未定值均标 UNKNOWN_FROM_SOURCE |
| 2026-09-16 | Design Owner → Coding Agent | D1–D6 裁决后 R2 重执行 | Owner Development Review 2026-09-16 | DEV-006 重分类 COVERED;DEV-010 钉 KNOWN_DEV_GAP |
| 2026-09-16 | Independent Reviewer → Coding Agent | H01–H18 转入 | Round 1 报告(独立盲测)+ Owner R3 裁决 | 历史分类保留;重分类仅限授权 delta |

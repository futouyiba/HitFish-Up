<!-- FCF-PC-BASELINE-R3-CANDIDATE: Narrow Delta over frozen R2, authorized by Design Owner adjudication of Blind Holdout Round 1 (HOLDOUT_PASS_WITH_NARROW_DELTA). R2 and earlier archives remain unchanged. Exactly three deltas; nothing else is admitted by this document. -->

# FCF Presentation / Cue Validation Baseline R3 — Candidate(窄 Delta)

Candidate Freeze ID: `FCF-PC-BASELINE-R3-CANDIDATE-20260916`

```text
ROUND1 = HISTORICAL BLIND EVIDENCE(FCF-PC-BLIND-HOLDOUT-ROUND-1-20260916)
R3     = DEVELOPMENT CANDIDATE(NOT YET FROZEN / NOT PROMOTED)
ROUND2 = NOT YET STARTED
```

## 0. 与 R2 的关系

- R3 = R2(全文有效)+ 本文档的**恰好三个** delta;除此之外任何语义变更均未获授权。
- 裁决来源:Design Owner 对 [Blind Holdout Round 1 报告](../holdout/FCF-PC-R2_BLIND_HOLDOUT_R1_20260916.md) 的 adjudication(`HOLDOUT_PASS_WITH_NARROW_DELTA / R3_DELTA_AUTHORIZED / R3_NOT_YET_FROZEN / NOT_PROMOTED`,2026-09-16)。
- Round 1 全部 18 cases 自此转为 Development Set(永久;不得再作 blind evidence)。

## Delta 1|Contact-generated disturbance capability

采纳 H12/H13 对已知 DEV gap(`KNOWN_DEV_GAP_CONTINUOUS_BOTTOM_CONTACT_MECHANICAL_CAUSE`)的独立双击压力。**不新增任何 strategy-specific token**(`mechanical_scrape / bottom_drag / football_jig_drag` 等一律不准入)。

最小 schema(单一 primitive,不因命名方便购买多个):

```text
cue.surface_contact_disturbance
  语义:Presentation / rig 与 world surface 持续接触并移动时产生、
       经 World / Physics 解析的 fish-independent mechanical disturbance。
  magnitude        OrderedBand          当前幅值(与时长分离)
  temporal_scope   必填                 A2 风格元数据
  summary_semantics 必填 Enum:
       CONTINUOUS_WHILE_MOVING   拖行(连续接触且行进)
       MOMENTARY_IMPULSE         瞬时触障(离散事件)
       STATIC_CONTACT            静止贴底(接触但不行进)
```

约束:

- generic world-surface semantic:该 fact **不命名具体表面**;世界语境由既有 `relation.*`(bottom/surface/structure)等提供,不硬编码 bottom;
- fish-independent(World/Physics 解析,不读 Species/Mode);
- current magnitude 与 duration / temporal semantics 经 `magnitude` 与 `summary_semantics`/`temporal_scope` 可区分;
- **不与 `vibration_*` / `sound_*` 对同一 physical cause 重复计权**:surface-contact cause family(`cue.surface_contact_disturbance` + `cue.vibration_amplitude/frequency` + `cue.sound_amplitude`)内,同一 Response rule 无 `CAUSE_JUSTIFIED` 不得消费 ≥2 成员;
- **不恢复 `cue.displacement`**(维持 NOT_ADMITTED)。

先行 schema、后以 Development fixtures 验证(含 DEV-010 重评估与 H12/H13 重分类)。

## Delta 2|Multi-source composition resolver contract

采纳 H07 暴露的上游 generic rule 缺口:

```text
0..N source-local Presentation / Cue facts
→ deterministic composition resolver
→ canonical Presentation / Cue snapshot
→ Response
```

- resolver 必须 deterministic、fish-independent、不读 raw identity;
- 禁止:`raw UmbrellaRig identity` / `SKU` / `Technique ID` / `rig_identity` 等任何 item/component identity 进入 sources 或 resolver 输入;
- 第一版**不增加** `source_count / lure_count` 类 Response fact(列入 R3 NOT_ADMITTED);
- **强制 development counterfactual**(CF-MULTI-1):single-source 与 multi-source 在 aggregate cue / target semantics 被控制为相同时,是否仍存在必须保留的策略差异?状态 `OPEN_PENDING_EVIDENCE`;只有答案明确为 **yes**,才重新提交 multiplicity primitive admission request;答案为 no 则关闭。

## Delta 3|Crab-like dictionary annotation

H14 只作为现有 semantic axis 的 annotation。字典核查结果:

- 既有 FeedingTarget 字典中 `CRUSTACEAN`(DEV-004 先例使用)对 crab-like 目标解释**足够**;
- 裁决:**reuse existing value**,不新增 enum value、不新增维度;
- `PREPARED_FOOD`(DEV-003 请求)与其它新字典值仍走 admission request,不在本 delta 内授予。

## 本轮明确不准入(维持)

```text
chemical magnitude / odor concentration   DEFERRED / NOT_ADMITTED(Round 1 H17 系 POSSIBLE_CONTAMINATION,
                                          仅 confirmatory evidence,不构成准入依据)
cue.displacement                          NOT_ADMITTED(维持 R2 D1)
item-specific strategy tokens             不准入(mechanical_scrape / bottom_drag / football_jig_drag 等)
raw source count                          不准入(source_count / lure_count)
new Meaning layer                         不准入
Pressure / cue familiarity                维持未验证(Round 1 主动排除,未获 blind 证据)
```

## 1. 对 R2 的效力表

| R2 条款 | R3 效力 |
|---|---|
| D3 DEV-010 KNOWN_DEV_GAP | 经 Delta 1 关闭:DEV-010 重评估为可表达(保持永久 Development 身份) |
| 其余 D1–D6 | 不变 |
| CUE_BASIS(12) | +`cue.surface_contact_disturbance` = 13 |
| FeedingTarget 字典 | 核查记录 + `CRUSTACEAN` 复用裁决;成员准入流程不变 |

## 2. 执行要求(Owner 指定)

1. 运行全部旧 regression;
2. Round 1 全部 cases 纳入 Development Regression;
3. 三个 R3 delta 建 targeted fixtures;
4. 生成 R3 Candidate hash;
5. 不选择任何新 Blind Holdout case(ROUND2 = NOT YET STARTED;registry 保持 SEALED_EMPTY);
6. 不 promotion Working Main;
7. 回报 Design Owner。

## 3. 记录要求

- 本文件 sha256 在实现 lane 的 baseline 记录与 run 报告登记;镜像入 `programaticHitFish` `docs/pc_validation/` 保持同一 hash;
- R3 冻结(升级为本实验 baseline)需 Design Owner 在 Development fixtures 验证后裁决;任何后续修订 → R4;R0/R1/R2/R3 不回写。

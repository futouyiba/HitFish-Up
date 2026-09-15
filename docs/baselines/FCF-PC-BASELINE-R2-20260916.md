<!-- FCF-PC-BASELINE-R2: Development Review Delta over R1. R0 and R1 archives and their hashes remain unchanged (Historical freeze provenance). This document supersedes R1 only where the delta below says so. -->

# FCF Presentation / Cue Validation Baseline R2 — Development Review Delta

Candidate Freeze ID: `FCF-PC-BASELINE-R2-20260916`
Status: FREEZE CANDIDATE / DESIGN OWNER ADJUDICATED (Development Review 2026-09-16)

## 0. 与 R0 / R1 的关系

- R2 = R1 全部已裁决内容(A1–A4 / B1–B2)+ 本 Development Review Delta(D1–D6)。
- R0、R1 原文件与 hash 保持不变,作 Historical freeze provenance;R1 与本 Delta 冲突之处,以本 Delta 为准。
- 裁决来源:Design Owner 对 Development Regression(15 case,2026-09-16 run)的 review。
- Implementation parent 同步修正:Current clean head = `9c2beebd2e2b1f5757223149e9c65f16bb200841`(`fcf-v0-current-contract-rebase`);`b8bcf778…` 降为 `PRIOR_CLEAN_BASELINE_PROVENANCE`。

## D1. `cue.displacement`:从 core vocabulary 移除

R2 不再把 `cue.displacement` 视为 admitted canonical core fact。状态:

```text
PROVISIONAL / NOT_ADMITTED
```

原因:不是在 net displacement 与 path length 之间择一,而是 Development evidence 尚不足以证明需要一个名为 `displacement` 的独立 semantic dimension,且该名称混合了多个不同物理量。潜在未来概念(不预先裁决、不预先拆字段):

```text
net spatial displacement
path length
hydrodynamic / water displacement
continuous contact travel
```

Harness 若发现新 case 使用它,不得判 `COVERED`;应要求 case 改用已 admitted facts,或返回 semantic admission request。

## D2. DEV-006(Spoon oscillating):去除 displacement 依赖后重分类

历史 Development judgement 是:Spoon steady / oscillating 复用已有 Optical / motion vocabulary,不因新品类新增 sensory dimension。因此 DEV-006 不得再因 `cue.displacement` 判 `UNRESOLVED`;优先使用:

```text
cue.flash
cue.direction_change
cue.speed_change
cue.speed
```

及必要的已 admitted motion facts。重新执行后,`primary_classification` 按是否仍需已有-schema annotation,在 `COVERED` 与 `ANNOTATION_ONLY` 之间确定。

## D3. DEV-010(Soft-worm bottom drag):Known Development Gap

不得因本轮压力测试新增 `mechanical_scrape / continuous_drag / bottom_scrape` 等 setter/primitive。记录为:

```text
UNRESOLVED
flag: KNOWN_DEV_GAP_CONTINUOUS_BOTTOM_CONTACT_MECHANICAL_CAUSE
```

问题具体化:`relation.bottom + ordinary motion facts` 是否足以表达产品需要的 bottom-drag strategy;若不足,缺失的是 continuous-contact physical cue、temporal summary,还是别的 reusable primitive——本轮不回答。该 Known Development Gap **不阻塞 blind holdout**;DEV-010 已是 Development case,后续不得作为 blind evidence;holdout 只测试冻结 R2 之外是否产生新的 marginal semantic growth。

## D4. Chemical intensity:暂不准入

`cue.chemical_intensity` / `cue.odor_concentration` 保持候选,不进入 R2 core。`presentation.chemical_signature` 仍只表达 chemical type / identity 类事实。仅当未来 unseen case 证明「相同 chemical signature 下,浓度/availability 变化构成独立、可学习、可重复利用的玩家策略差异」时,再申请 `NEW_PRIMITIVE_REQUIRED` 或对应 relation。不得因 DEV-003 / DEV-S5 提前加入。

## D5. Walleye low-light:保持 LINT_WATCH,不产生新 semantic

DEV-S4 保持:

```text
LINT_WATCH_DOUBLE_COUNT
```

规则:若 `local light → propagation / visibility resolution → cue.visual_contrast` 已消费该 visual cause,则 Response 不得再匿名读取 `context.light` 对同一视觉效果做第二次 penalty/bonus;只有 `context.light` 对 Response 具有另一条独立因果作用时才可同时读取,且必须能解释 provenance。这不是新 primitive,也不是 confirmed conflict。

## D6. `cue.sound_pattern`:UNEXERCISED

当前 15 个 DEV case 未使用 `cue.sound_pattern`。仅记录:

```text
UNEXERCISED_BY_CURRENT_DEVSET
```

本轮既不删除,也不据此证明必要;由 blind holdout 提供进一步证据。

## 1. 对 R1 的效力表

| R1 条款 | R2 效力 |
|---|---|
| A2 中 `cue.displacement` PROVISIONAL(net vs path 未决) | 升级为 D1 `NOT_ADMITTED`(更强:整个 dimension 移出 core;未来概念另行申请) |
| A1 / A3 / A4 / B1 / B2 及 A2 其余部分 | 不变,继续有效 |
| R0 §3.2 Candidate Basis 含 `cue.displacement` | R2 起 basis 为其余 12 项 + candidate extension `cue.chemical_intensity?`(NOT_ADMITTED) |

## 2. 不阻塞本轮 Blind Holdout 的 OPEN 项(维持,不得由 Harness 自行闭合)

```text
multi-target aggregation
ResponseBand numeric mapping
final SET/CAP resolution
CAUSE_JUSTIFIED formal carrier
metric spot-check ratio
DEV-S5 exact species attribution
```

## 3. Blind Holdout 授权条件(裁决原文)

9c2 rebase 后同时满足则状态更新为 `BLIND_HOLDOUT_AUTHORIZED`:

```text
full regression PASS
PC-specific tests PASS
DEV regression PASS
DEV-006 no longer blocked by displacement
DEV-010 correctly pinned as KNOWN_DEV_GAP
R2 hash frozen
holdout registry still SEALED_EMPTY
```

此后由独立 Sample / Reviewer Agent 选择真正 unseen cases;Coding Agent 不得看到或挑选具体 holdout case。

## 4. 记录要求

- 本文件 sha256 在实现 lane 的 baseline 记录与 run 报告登记;R2 镜像入 `programaticHitFish` `docs/pc_validation/` 并保持同一 hash。
- 任何后续修订 → R3;R0/R1/R2 不回写。

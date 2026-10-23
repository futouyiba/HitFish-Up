# FCF 0.3.4.0-B Fixed Bake 实现就绪 — 独立审核记录

- 审核对象:PR [#2](https://github.com/futouyiba/HitFish-Up/pull/2),分支
  `fcf-0.3.4.0-fixed-bake-readiness` @ `f2d5df9`(5 个 commit,领先 main tip `cf90e74`;
  净 diff = 7 个新增文件,+2515/-0)
- 审核日期:2026-09-18
- 审核方式:role-separated 全新上下文 agent,只读,在 detached worktree 中逐条实测;
  对「独立复算」一项自行另写脚本重算(见下)
- **模型披露(AGENTS.md 要求)**:指定 reviewer `gpt-5.6-sol` **不可用** —— codex CLI
  0.142.4 对 `gpt-5.6-sol` 与 `gpt-6-astra` 均返回「requires a newer version of Codex」,
  与 2026-09-16 那次审核记录的结论一致;本轮未升级 codex(系统工具变更,影响其它在途会话,
  未获授权)。按 AGENTS.md 回退条款继承当前可用模型:**Claude Opus 5**,高推理强度。
  与实现同模型族、不同上下文实例,**独立性弱于指定跨厂商 reviewer** —— 实现与审核方之间
  若存在共同盲区,本审无法暴露。

## Verdict(原文)

```text
level: ARTIFACT
scope: PR #2, branch fcf-0.3.4.0-fixed-bake-readiness @ f2d5df9 (5 commits ahead of main tip
       cf90e74; net diff = 7 files, +2515/-0): reference/0340-fixed-bake/README.md,
       reference/0340-fixed-bake/fixed_bake.py, reference/0340-fixed-bake/test_fixed_bake.py,
       reference/0340-fixed-bake/fixtures/bass_q3.json, docs/implementation-gap.md,
       docs/implementation-readiness.md, docs/mockups/0.3.4.0-fixed-bake-readiness.html
baseline: cf90e74 (= origin/main = main). All 7 files A(added); 0 modified, 0 deleted.
proves:
  1. Scope (claim 1) HOLDS: the branch adds only documentation plus an explicitly-labeled
     executable reference. No existing file is touched; no production migration occurs.
     REFERENCE/VALIDATION framing is repeated in the module docstring (fixed_bake.py:3),
     README.md:3, implementation-readiness.md:4, implementation-gap.md:3. (Boundary note N4.)
  2. Test count (claim 2) HOLDS: 39/39 pass under `python3 -m pytest test_fixed_bake.py -q`
     and `python3 -m unittest test_fixed_bake`. Class breakdown 1+20+3+7+8 = 39 matches
     implementation-readiness.md:164-168. Tests are behavioral, not tautological: golden
     assertions compare against constants held in fixtures/bass_q3.json (falsifiable),
     validation tests use assertRaises, and the one undefined-input case is explicitly
     labeled characterisation. (Weak-assertion notes N5.)
  3. Goldens (claim 3) HOLD IN SUBSTANCE: 8/8 reproduced EXACTLY by my own independent
     recomputation that does not import fixed_bake.py, hand-transcribed from the stated
     §3.3/§3.4/§4.3/§3.5 formulas. BUT (claim 3's provenance half) the "independent script"
     the docs cite is NOT in the branch: only 2 .py files were tracked, test_fixed_bake.py:20
     imports the implementation, and git status -uall was clean. The guard was not
     reproducible from the artifact. See N1 — since fixed by committing verify_goldens.py.
  4. Rulings (claim 4) HOLD: GAP-002 dead keys (gateFailureCap/secondaryLossRaw/
     secondaryLossApplied) absent from the Trace and gateFailureBranch present (probed
     directly); GAP-003 explicit null -> IGNORED and an absent binding row -> BakeConfigError
     (test_case14); GAP-004 a gatePolicy key inside a binding row raises, including on an
     otherwise-legal CORE row (test_any_gate_policy_field_is_rejected). GAP-001 snake_case
     keys are what fixtures/bass_q3.json actually uses. Scope caveat N3.
  5. Stale semantics (claim 5) HOLD: SecondaryFactor = 1-(1-p)/4 verified (p=0.6 -> 0.90,
     range [0.75,1.0]); the old 1/6-loss + 0.2554-cap model appears ONLY in prose explicitly
     marked superseded. IGNORED is the first-class third state; OFF/EXCLUDED are accepted as
     read aliases and normalised, never emitted (`off`/`BOGUS` both error). 0.30 is the
     background-floor upper bound (0, 0.30] -- accepted at 0.30, rejected at 0.3000001 / 0 /
     -0.01 -- and is NOT stale.
  6. Internal consistency (claim 6) PARTIAL: status is consistent across
     implementation-gap.md's header table, implementation-readiness.md, the HTML and the code
     (GAP-001..004 RESOLVED; GAP-005..012 open; implementation-side migration outstanding).
     The gap-log section BODIES were stale and contradicted it. See N2 — since fixed.
does_not_prove:
  - The mapping of the four rulings to the Notion authority pages and the Feishu derivation
    sheet. No access to those sources; not fetched. Everything above is internal consistency
    between the committed text and the committed code only. That the reference faithfully
    matches the authority pages is NOT established here.
  - Any property of the production repo futouyiba/programaticHitFish, including the claimed
    W6 head 0d94319 / 62 B-module tests, or the claim that it still runs pre-2026-09-17
    semantics. Not inspected.
  - Whether the four adjudications are the correct design decisions. Only that the code and
    tests implement what the docs say was ruled.
  - That the claimed independent recomputation script ever existed or was run. It was absent
    from the branch; the reviewer substituted its own recomputation (see proves 3).
  - Runtime behavior beyond the exercised inputs; no coverage measurement was performed.
open_findings: NONE
verdict: ARTIFACT_APPROVE
```

## 非阻塞观察与处置

| # | 观察 | 处置 |
| --- | --- | --- |
| N1 | 三处文档声称存在一支「不 import 参考实现」的独立复算脚本,但分支只跟踪 2 个 `.py`,工作区干净无未跟踪 —— 出处声明显不可复现。数值本身经 reviewer 独立重算确认无误(8/8)。 | **已修**:把该检查提交为 `reference/0340-fixed-bake/verify_goldens.py`(手工转写 §3.3/§3.4/§4.3/§3.5,不 import `fixed_bake`,失配时非零退出),三处声明改指向它。 |
| N2 | `docs/implementation-gap.md` 的 GAP-001…004 **条目正文**仍是裁决前文本:GAP-002 与 GAP-004 把「*(this reference does this)*」标在了**错误的候选**上(与代码相反),四条正文结尾还留着「Do not decide」,GAP-001/002 仍写「Blocking: YES」。头部表格、readiness、HTML、代码四方一致,故非阻塞;但只读正文的实现者会拿到反转答案。 | **已修**:正文改为指向裁决;GAP-002 记明裁决取的是 **B 的删除 + A 的 `gateFailureBranch`**,并非任一候选原样。 |
| N3 | GAP-004 在代码中比文本窄:`role_of` 只在 `resolvedSpatialOpportunityBindings` 行内拒绝 `gatePolicy`,顶层 `subject` / `seed` / `conditionGroup` 上的该键静默通过;而 readiness 写的是「Any `gatePolicy` key is rejected」。 | 未修 —— 文本表述偏宽,实际影响低(该字段的家就在 binding 行)。留待后续。 |
| N4 | 这是本仓第一份可执行代码,而 `AGENTS.md` 写的是 harness/实验执行代码属于 `futouyiba/programaticHitFish`;它落在新的 `reference/` 目录下,`AGENTS.md` 未更新以授权它。各处 REFERENCE / VALIDATION 措辞很强,被误认为已交付实现的风险低,但这是 Owner 的边界裁定。 | 未修 —— 待 Owner 裁定(是否需要更新 `AGENTS.md` 以承认 `reference/`)。 |
| N5 | 若干断言偏弱:`test_p1_determinism` 拿纯函数的两次相同调用对比;`test_p2/p3/p7` 断言公式结构上必然成立的界;`test_case08` 的 `assertLessEqual(gated, opened + 1e-12)` 因两路都落在 `0.1` 底而由精确相等通过,其 docstring 声称的区分力实际由 `gateFailureBranch.applied` 的 True-vs-None 断言承担。 | 未修 —— 不削弱结论(真正的区分由其它断言承担)。留待后续。 |

## 审核基准更正

派单说明把审核对象写成「单个 commit `f2d5df9`」;实际该分支是 **5 个 commit**
(`8d13aff → 9fff8e4 → 0c4569e → 5324a9a → f2d5df9`),只有净 diff 符合所述的
7 文件 / +2515 / -0。结论不受影响。

# FCF Canonical System Map — 独立审核记录

- 审核对象:PR [#3](https://github.com/futouyiba/HitFish-Up/pull/3),分支 `fcf-map-canonical`
  @ `70354d6`(63 文件,+20178/-0,全部新增):`fcf-system-map/`(46)、`spike/`(15)、
  `.mcp.json`、`.claude/launch.json`
- 审核日期:2026-09-18
- 审核方式:role-separated 全新上下文 agent,只读,在 detached worktree 中实测;
  在 scratch 副本里做了 16 组变异以证伪各项校验
- **模型披露(AGENTS.md 要求)**:指定 reviewer `gpt-5.6-sol` **不可用** —— codex CLI
  0.142.4 版本门槛(与 2026-09-16 那次一致);本轮未升级 codex(系统工具变更,影响其它
  在途会话,未获授权)。按 AGENTS.md 回退条款继承当前可用模型:**Claude Opus 5**,高推理强度。
  与实现同模型族、不同上下文实例,**独立性弱于指定跨厂商 reviewer**。

## Verdict(原文)

```text
level: ARTIFACT
scope: PR #3 fcf-map-canonical @ 70354d6c9915bf76a8d1cc2f5d9ca10949b9e11a (63 files, +20178/-0):
       fcf-system-map/ (46), spike/ (15), .mcp.json, .claude/launch.json
baseline: main (merge-base; additions-only diff), plus the artifact's own declared
          claims (README, LAYOUT.md §1-§9, spike/README.md fingerprints)
proves:
  1. Build is deterministic: distinct runs byte-identical and equal to the committed
     .drawio (sha256 e4a02bcc82ea70cb...); invariant under PYTHONHASHSEED 0/1/12345/random
     and LC_ALL=C. Committed artifact is NOT stale. The no-arg builder rewrites
     generated/ but byte-identically — git status stayed clean.
  2. validate.py's checks are non-vacuous: 12/12 constructed failures caught in a scratch
     copy (duplicate ID, unknown edge endpoint, scope missing/duplicate, parent cycle,
     CJK, overlap, skeleton drift x4). Rename stability caught BOTH a builder patched to
     size titles from len(label) and a builder patched to drop label propagation.
     (Two item-1 sub-checks are subsumed by ID_RE and cannot fire independently.)
  3. Skeleton guard is live, not vestigial: fingerprint == baseline on all 6 keys;
     validate.py imports freeze_skeleton.fingerprint and FAILs on relabel / new edge /
     kind change / added block. It is fail-open when skeleton.baseline.json is deleted.
  4. Spike fingerprints all match committed bytes (drawio 37972b92..., v2 bf248886...,
     viewer e49a0d5d...); v1 == committed fcf-spike.drawio; v2 rebuilds byte-identically
     from graph.roundtrip.json; committed roundtrip.diff == regenerated diff (40 lines);
     check_roundtrip.py PASSes with strict expected-added equality.
  5. No superseded token lives in the canonical chain: gatePolicy/GatePolicy appears only
     as a quoted Notion string in align/notion-gov-findings.md; EXCLUDED only in throwaway
     align/ artifacts; zero 未配置, zero uppercase OFF. Third aggregation role is 忽略因子.
  6. .claude/launch.json entry is runnable from a fresh clone: preview.py starts, serves
     the harness 200, /api/version returns the committed hash, port 8799 == script default.
  7. graph/scopes/views/contracts/generated/LAYOUT/README agree on node+edge counts, view
     names, scope tallies, and LAYOUT §6.4's 9-module-edge and fold-visible-edge tallies
     (31 -> 12) reconcile exactly with graph.json. test_roundtrip.py PASSes.
does_not_prove: No access to the Notion Content Ledger, so no label's MEANING or currency
  is confirmed — only internal consistency and mechanical claims. Draw.io engine behaviours
  were NOT re-measured (fold delta, lens opacities, cross-view collapse persistence) — those
  need the pinned viewer in a real browser. The spike's viewer-runtime click assertions and
  container-test were not re-run. No CI exists, so validate/freeze/test run only when invoked.
open_findings: N1..N11, none blocking.
verdict: ARTIFACT_APPROVE
```

## 非阻塞观察与处置

| # | 观察 | 处置 |
| --- | --- | --- |
| N1 | `graph.json` 头部描述的是**已废的方案一**:`description` 写「每行固定高度行带、展开只向右、绝不向下」,`provenance.topology` 写「行带 + 横向展开」,`semantics.hierarchy` 写「parent = 行」,`semantics.expansion` 写「横向向右延伸…折叠用封面块填住行带」——与 `LAYOUT.md`、README 及数据本身全部相反(实测 `R2.F.HAB.parent == R2.C1`,无封面块)。`semantics.edgeTypes` 只列 3 种而 builder 的 `EDGE_TYPES` 有 5 种。这些字段惰性(builder 只读 nodes/edges),但它是 SoT 文件。 | **已修**:`description` / `provenance.topology` / `semantics.hierarchy` / `semantics.expansion` / `semantics.edgeTypes` 全部按 `LAYOUT.md` 的方案二口径改写,edgeTypes 补齐 RETENTION / ANCHOR。 |
| N2 | `working/manifest.json` 的 `snapshot_commit: 66898b7` 不在 HEAD 祖先中(在 `futou-/container-layout` 上),同 commit 的 drawio blob 哈希也不同;只有 `baseline_sha256` 是对的。 | 未修 —— `working/` 是工作副本目录,待后续。 |
| N3 | `build/viewer-harness.html` 宣传「顶部三个按钮」含已不存在的「0.3.4.0-B 聚焦」,并把 0340b 说成「只上配色与透明度」(实际它还折叠 R2–R6);README §5 表格重复「绝不触碰」层级,与 `views.json` 及其下方正文矛盾;harness 引「约 1376×2078」、LAYOUT §7 引「约 1340×2600」,实际内容盒 1300×2356。 | 未修 —— 面向读者的 stale 文本,待后续。 |
| N4 | `R2.C2.X/C3.X/C4.X/C5.X`(kind `skip`)标 `排除忽略`;channel 1 的同类已按「忽略因子往下什么都不做」删除,旧 align 草图曾用 排除/EXCLUDED。现行第三态令牌是 `忽略因子`(在 `R2.C1.F5`/`R2.F.SKIP` 上用得正确)。另:live label `R2.C1.A1/A3` 仍用 README §2 已弃的「环境权重」。 | 未修 —— **需 Content Ledger 才能裁定**是否命名漂移,不在本仓可定范围。 |
| N5 | `GatePolicy` 出现一次,在 `align/notion-gov-findings.md:30`,是 Notion 权威文本的**逐字引用**(治理发现 G-03),非 live 值。 | 未修 —— 作为引用是正确的。 |
| N6 | `EXCLUDED` 作为 live role 名出现在 `align/expand_model.py:78` 与 `align/expand-model-row2.drawio` —— 都在 README 自称「throwaway、可删」的目录里,但已提交且可 grep 到。 | 未修 —— 待后续,或整目录删除。 |
| N7 | **骨架守卫 fail-open**:删除 `skeleton.baseline.json` 后 `validate.py` 打印 `VALIDATION: PASS`(因 `if baseline_path.exists():`),与其自身注释「基线缺失/损坏不应静默通过」矛盾。它保护的正是本项目最核心的不变量。 | **已修**:补 `else` 分支显式报错。实测:基线缺失 → `VALIDATION: FAIL (1)`、exit 1;改名节点仍触发 `SKELETON DRIFT`。 |
| N8 | item-1 的两个子检查(保留前缀、`::`/`->` 检查)因 `ID_RE` 已拒绝 `:` 和 `-` 而永不触发。 | 未修 —— 无害冗余。 |
| N9 | `.mcp.json` 提交了一条全仓生效、会触发权限提示的 MCP 入口,跑未 pin 的 `npx -y @drawio/mcp`;README 声称 pin 了 v1.6.0 但无任何机制强制。 | 未修 —— 待 Owner 定是否 pin。 |
| N10 | 本仓无 CI,validate / freeze / test 只在有人手动跑时才跑。`validate.py` 退出码本身正确(FAIL→1)。 | 未修 —— 待后续。 |
| N11 | `check_roundtrip.py:109-110` 有死代码(`if not (...): pass`);PASS 路径的重复检测 `print` 会输出 `x=x=1080,...`。 | 未修 —— 待后续。 |

## 备注

- 本次是本仓首次对地图线做独立审核。此前该分支的机械检查(`validate.py`、骨架守卫、
  round-trip)全绿,但**机械检查不是独立审核** —— 本次 16 组变异正是为了区分二者。
- 审核本身未改动工作区(`git status` 前后均干净);构建器写入 `generated/` 但内容逐字节相同。

# PR #74／#75 合后独立复核

- 审核对象:PR [#74](https://github.com/futouyiba/HitFish-Up/pull/74) 与 [#75](https://github.com/futouyiba/HitFish-Up/pull/75),均已合并;基线 `main` @ `cbb7d01985642c89305499081d316d59c28e633d`
- 审核日期:2026-09-22
- 审核方式:role-separated 全新上下文 agent,只读;以与原作者不同的探针逐条实测正文里的可证伪断言,不采信原 `intg` 评论的结论
- **模型披露(AGENTS.md 要求)**:指定 reviewer `gpt-5.6-sol` **不可用** —— codex CLI 0.142.4 对 `gpt-5.6-sol` 与 `gpt-6-astra` 均返回「requires a newer version of Codex」,与 2026-09-16／09-18／09-21 数次的结论一致;本轮未升级 codex(系统工具变更,影响其它在途会话,未获授权)。按 AGENTS.md 回退条款继承当前可用模型:**Claude Sonnet 5**,中等推理强度。与实现同模型族、不同上下文实例,**独立性弱于指定跨厂商 reviewer**;共同盲区无法由本审暴露

## 目标与证据边界

| 对象 | exact 锚 |
|---|---|
| 基线(被审对象并入后的 `main`) | `cbb7d01985642c89305499081d316d59c28e633d` |
| `#74` 合并提交 | `53b5195a1fc956340de5acfe62fc291010ce1a15`(parents `8f60ed4c` ＋ `ddc37576`) |
| `#74` 被审 head | `ddc37576ab8cb238f85ac126226da1863cac7a32` |
| `#75` 合并提交 | `cbb7d01985642c89305499081d316d59c28e633d`(parents `53b5195a` ＋ `7fa46e9a`) |
| `#75` 被审 head | `7fa46e9a46d451a19fdf318d6cb3ba21611e4fa3` |
| `#74` 被删 blob | `TASK-dynamic-layout.md` = `251d4fedac126b5a7c8c940f6fcd41d4f917f7f6`;`TASK-dynamic-layout-landing.md` = `ffbfab963214ccbe2532fe6ac70f7566aa24ed4b` |
| `#75` 被删 blob | `fcf-0.3.4.0-B-03-aggregation-flow-v2.svg` = `b0a1752b1bec3eb943427e8f3c23d6f640d7d0cf` |
| 被审断言原出处 | 两 PR 的正文,及各自合并后的 `intg 独立核` 评论 |

复核只读仓内 tracked 内容与上述 Git 对象。**上游 Notion／Figma／其它仓本次未核**;不把仓内读数升级为 Product Authority。

## 被审的两个事实主张

两 PR 都是单用途删除,且把「可安全删除」写成了可证伪的断言:

| PR | 删除内容 | 自述的关键断言 |
|---|---|---|
| `#74` | `fcf-system-map/align/` 下两个 TASK brief(共 186 行) | 两文件在仓内**零引用**;工作已分别落在 `align/dynlayout/REPORT-dynamic-layout.md`(可行性)与 `fcf-system-map/LAYOUT.md`(采纳);canonical build 不依赖;仅删除,未动其它内容 |
| `#75` | `docs/diagrams/fcf-0.3.4.0-B-03-aggregation-flow-v2.svg`(191 行) | tracked 文件对 v2 **零引用**;`-current` 是其继任者(非同图副本)且为唯一现行版本;单文件,无其它改动 |

## R1:两笔合并提交确为「纯删除」

| PR | 合并提交 `--stat` 读数 |
|---|---|
| `#74` | 2 files changed, **186 deletions(-)**, 0 insertions |
| `#75` | 1 file changed, **191 deletions(-)**, 0 insertions |

两条都是 `parents=2` 的真合并提交,且 `git merge-base --is-ancestor 53b5195a cbb7d019` 成立 ⇒ 两笔在 `main` 上先后相接,**不存在把 `#74` 内容回灌或被覆盖的窗口**。

## R2:`#74` 的零引用断言成立,另补三条原评论未覆盖的轴

原 `intg` 评论核的是 **basename 全树引用 0**(`git grep origin/main`)。本次以同源命令独立复得 0,并追加:

1. **tracked 文件层**:两个被删文件名在 `main` 上各 **0 命中**。
2. **构建依赖层**(正文点名、原评论未单列):`fcf-system-map/tools/` 对 `align/` 与 `TASK-` **0 命中** ⇒ canonical build 不引用。
3. **PR／issue 正文层(本次新增轴)**:全仓 38 个 PR ＋ 37 个 issue 的正文中,提及这两个 basename 的**只有 `#74` 自身** ⇒ 无先前 PR body 指向它们。
4. **README 附录层**:`fcf-system-map/README.md` 的 `align/` 附录表(第 229–241 行)**未**点名这两个文件 ⇒ 删除没在附录里留下悬空条目。

第 3 条不是冗余:两 PR 正文**自己**知道这一类风险 —— `#74` 明确披露它为此外加保留了 `docs/proposals/` 中 6 个文件(「删除会打断已合并 PR body 的链接」),只是没把同一判据施加于本次删除的两个 TASK 文件。复核结果:该层同样干净。

**载体存活**:`align/dynlayout/REPORT-dynamic-layout.md`(blob `cd8aa9a850b4bd172c8bfca8c69db42d87efc3a5`)在 `main` 上存在,且被 **4 处**引用(`LAYOUT.md:27`、`build/build_diagram.py:30`、`build/build_diagram.py:160`、`layout.json:7`)⇒ 被删 TASK 所指的「durable home」确在且可达。

**一处计数口径收窄(非阻塞)**:`#74` 正文与其 `intg` 评论均写作「LAYOUT.md 引用 REPORT **两次**」。按精确串测,`REPORT-dynamic-layout.md` 在 `LAYOUT.md` 中**出现 1 次**(第 27 行);另 1 处是第 152 行对**目录** `align/dynlayout/` 的引用。⇒ 读作「2 处指向 **REPORT 文件**」不成立;**读作「2 处指向 `dynlayout` 这一住处」成立**。结论不变,仅计数口径需收窄。

## R3:`#75` 的继任断言成立

- `docs/diagrams/` 在 `main` 上只剩 `fcf-0.3.4.0-B-03-aggregation-flow-current.svg`(blob `825c578c92b0b94bb622cb77a4af0e69894483db`)⇒ v2 已去、current 在。
- `dd509780` 存在,`2026-09-20T07:47:20+08:00`,改的正是 current svg(4 insertions / 4 deletions)⇒ 与 `#75` 自述的「current 此后还有 `0da5f5b0`、`dd509780` 两轮细化(至 09-20 07:47)」一致。
- 引用层面同 R2:该 v2 文件名在 tracked 文件与全部 PR／issue 正文中均 0 命中(唯一提及者是 `#75` 自身)。

**未复核**:`#75` 自述的「两图 287 行差异」「current 非同图副本」「v2 整条提交线先于 current 的 merge-base 判定」三条,本次**未独立重算**。它们回答的是「该不该删」的合理性;本记录的目标是「删了之后有没有断链」。三条仍以原 `intg` 读数为准。

## 过程观察(不改变上述结论)

两 PR 于 04:42:47／04:42:53 **相隔 5 秒批量合并**;六段定式中**只有末段**:`DESIGN: APPROVE` 与 `REVIEW: APPROVE` 计数均为 0,`INTEGRATED:` 前缀计数亦为 0(补记写成普通评论)。对照同期 `#56`／`#64`／`#65`／`#68`／`#69`／`#72` 均为 `comments=6 / DESIGN=1 / REVIEW=1 / INTEGRATED=1`,`#52` 为 `8/1/2/1`。

⇒ **准确定性**:这不是「未审」,而是**「审在合后」** —— 两条都有合并后的 `intg 独立核` PASS 评论,`#74` 另有一条补锚评论明说「approve 因同账号自批限制未能落 review」。缺的是**合前**的 `DESIGN`／`REVIEW` 两段,以及把结果写成 `INTEGRATED:` 定式。本记录只报告读数,**是否受理该路径、是否要求补齐合前段,归 Owner**。

另注一条会误导判读的通道事实:本仓全部 agent 共用 GitHub 账号 `futouyiba`,GitHub 禁自批 ⇒ `reviews` 端点与 `reviewDecision` 在本仓**恒空**,审批证据只住在评论正文里。**不得以 `reviews=0` 判「没审」。**

## 可复现检查

```sh
main=cbb7d01985642c89305499081d316d59c28e633d

# R1 纯删除与祖先关系
git show --stat --format='%H%nparents: %P' 53b5195a
git show --stat --format='%H%nparents: %P' cbb7d019
git merge-base --is-ancestor 53b5195a cbb7d019 && echo ancestor

# R2/R3 tracked 零引用
for f in TASK-dynamic-layout.md TASK-dynamic-layout-landing.md \
         fcf-0.3.4.0-B-03-aggregation-flow-v2.svg; do
  printf '%s -> %s\n' "$f" "$(git grep -F "$f" "$main" -- . | wc -l)"
done

# R2 构建依赖层
git grep -n -E 'align/|TASK-' "$main" -- fcf-system-map/tools/

# R2 载体存活与全部引用点
git ls-tree "$main":fcf-system-map/align/dynlayout/
git grep -n 'REPORT-dynamic-layout' "$main" -- .

# R2 计数口径收窄:REPORT 在 LAYOUT.md 的精确出现次数(得 1,非 2)
git show "$main":fcf-system-map/LAYOUT.md | grep -o 'REPORT-dynamic-layout\.md' | wc -l
git grep -n -E 'REPORT|dynlayout' "$main" -- fcf-system-map/LAYOUT.md

# R3 继任者
git ls-tree "$main":docs/diagrams/
git show --stat --format='%h %aI %s' dd509780
```

PR／issue 正文层需先取回正文本地比对 —— **不要**用 GitHub code search:本两仓实测对确实存在的串也返回 `total_count=0`:

```sh
gh pr list --state all --limit 200 --json number,body > /tmp/prbodies.json
gh issue list --state all --limit 200 --json number,body > /tmp/issuebodies.json
```

## 收口范围

**覆盖**:`#74`／`#75` 在 `cbb7d019` 上的删除是否造成**仓内**引用断裂(tracked 文件层、构建依赖层、PR／issue 正文层、README 附录层),以及两条 PR 的「纯删除」与「继任者存活」断言。

**不覆盖**:

- **仓外引用**。两条断言的射程都写作「tracked 文件／in-repo」。Notion 页、Figma、其它仓、以及被**外部**引用的公开 blob URL 是否不再可达,本次未核。
- `#74` 正文自披露的 **README `align/` 附录表陈旧**问题(漏 `align-harness.html`、`align_*.py`、`expand-*`、`dynlayout/`)确实存在,但它在**删除前就已陈旧**,且被正文明确划出射程归 Owner —— 按「老问题别算进新变化的账」,不计入本批。
- `#75` 的三条合理性断言(见 R3 末)未重算。
- 本记录**未复核任何其它 PR**,不构成对任何实现或契约结论的背书。

## 结论

`#74`／`#75` 的「零引用」与「纯删除」断言**成立**,仓内无断链;判 **PASS(合后复核)**,附 R2 的一处计数口径收窄。

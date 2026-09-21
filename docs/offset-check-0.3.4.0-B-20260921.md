# 偏移检查：实现 ↔ md（只读，先报不改）

**检查方**：impl agent。**日期** 2026-09-21。**未改任何代码、未推任何仓、未碰平台、未读写 Notion。**

**★ 时点锚（作者后补，2026-09-21）—— 读本报告前先读这一段**

**本报告读于 `futou/hitfish-0.3.4.0-b-batch27` @ `bae6e6f`。** 该分支此后又走了 **`3cb3074` → `ecbd1df` → `b003dfe`**，其中**有改动正好落在本报告判过的点上**：

| 本报告判的 | 现状态 |
| --- | --- |
| §1 第 3 行 **`ADJ-07` 偏移** | **已修** —— `ecbd1df`（`src/editor/policyTemplate.ts:108–110` 的 `rawRoleOf` 真的折出 `payload.roles[component] ?? 'CORE'`，并配新测试） |
| §1 第 4 行 **`ADJ-02` 偏移** | **已由 `#27`（`3cb3074`）落了大半** —— 读者／写者／求值／校验**四处四组件齐**；**剩余几处**见《落仓说明》§3 |
| §1 第 5 行 `ADJ-11`、第 7 行 `ADJ-09` | **仍成立**（`refs` 零写者；`src/` 里 `staged` **0 命中**） |

⇒ ★ **不要在 `b003dfe` 上重跑本报告并据此判「报告错了」** —— 上面前两条是**基线之后被修的**，不是报告写错。
⇒ ★ 且 **本报告的 `file:line` 锚解析在三个不同修订上**（不是两个）：**`bae6e6f` ／ `3cb3074` ／ `ecbd1df`**。⇒ **凡未在下表出现的锚，以 `bae6e6f` 为准。**
⇒ ⚠️ **但「在 `bae6e6f` 上成立」不等于「在别处也成立」** —— 下表 **B 组**那 8 条自 `ecbd1df` 起已被移动；**要按某个具体修订复核，先看 B 组。**

**★ 锚的修订归属（须标 commit 的那批）**

> **怎么得的**：脚本 `/tmp/anchor-check.mjs` 对本文件实跑，逐锚在 `bae6e6f`→`3cb3074`→`ecbd1df`→`b003dfe` 四个 base 上**同时打出「那一行原文」与「它最近的声明」**；两处「注释声称」由**人工逐字复核**（见 C）。
>
> ⚠️ **脚本的三条已知局限（都已在 v3 修掉，此处留痕）**：
> ① 它取的是「**最近的声明**」（从该行**向上**找）⇒ **函数体起始行在锚点之下时，会归给上面那个函数**（`app.ts:858–885`、`app.ts:1240–*` 就是这种，**已人工改正**）；
> ② ★ **它会把控制关键字当成声明捕获** ⇒ `if (f === 'TIME_PERIOD' && …)` 被报成 owner ＝ 裸 `if`。**这不是「该行不属于声称的符号」，是这个 token 本身是假值** —— 本表初稿据此把 `872`／`1088` 的归属**判反**（见 B）。v3 加了 STOP 表，并**把「那一行原文」一起打出来**：报「那一行实际是什么」比报「最近的声明是谁」更难被误读；
> ③ ★ **「是不是跨修订」的判据必须打在字节上，不能打在同一层的代理量上**：v1 拿 `owner` 当判据 ⇒ **漏报**了 `persistence.ts:484–489`（四个 base 的 owner 全是 `at`，而那一行是 `}` vs `typeof rec.refs…`）。改用字节后，跨修订数 **14 → 16**。
>
> v3 的 **8 条自检**（越界必红／已知正确必绿／真缺陷必红／路径不存在必红／控制关键字不得当声明／语句行须被标出／字节变必报跨修订／字节不变不得报）**逐条做过定向突变证伪** —— 每条都**能红**，且只在脏的时候红；**不过即退 2、什么都不做**。

**★ 判别方式**：下表列的**不是**「哪些锚写错了」，而是「**哪些锚不在报告声明的基线 `bae6e6f` 上**」。逐条问的是：**报告引用它的那一处，说的是 `bae6e6f` 的事，还是别的修订的事？**

**A. 不在 `bae6e6f` 上的锚（8 条）** —— 引用它们时，量的其实是更新的修订

| 锚 | 该锚真正成立于 | `bae6e6f` 上那一行**实际**是什么 |
| --- | --- | --- |
| `src/core/contract.ts:111–113` | **`3cb3074`** | `feedingLayer: FeedingLayerProfile;` —— ★ **「四个槽位一律可缺席」那段头注当时还不存在**（该修订全文搜「可缺席」**0 命中** ⇒ 那时**只有时段可空**） |
| `src/data/persistence.ts:484–489` | **`3cb3074`** | `}` —— ★ **v1 漏报**；那条 `typeof rec.refs` 校验在 `bae6e6f` 上是 **478** |
| `src/data/persistence.ts:1117–1120` | **`3cb3074`** | `...state,` —— **不是** `setPatchFor`（它在 `bae6e6f` 上是 **1061**） |
| `src/data/persistence.ts:1278–1287` | **`3cb3074`** | `/**` —— 那是 `revisionOfText` 的 doc 注释（「基线版本指纹」）；**该断链检查在 `bae6e6f` 上是 `1222–1233`** |
| `src/data/persistence.ts:1396` ／ `:1396–1410` | **`3cb3074`** | **越界** —— 该修订该文件 `wc -l` ＝ **1372**（`httpFileStore` 在 `bae6e6f` 上是 **1340**） |
| `src/ui/app.ts:870–891` | **`ecbd1df`** | 另一段注释（`field → data-* 属性` 映射那条） |
| `src/ui/app.ts:858` | **`ecbd1df`** | `/**` —— ★ 它支撑的是 §11.4 那句「`858` 那行是 `onRoleEdit`」；**在 `bae6e6f` 上那句是假的** |

**B. 在 `bae6e6f` 上成立、但 `ecbd1df` 起已被移动的锚（8 条）** —— 不是错，引时必须带 commit

| 锚 | 在 `3cb3074`／`ecbd1df` 及以后变成 |
| --- | --- |
| `src/data/persistence.ts:872` | **`3cb3074` 上就是 `const tNum = Number(t);`** —— ★ `bae6e6f` 上那一行 `if (f === 'TIME_PERIOD' && !profiles.timePeriod) {` **正是**本报告声称的「时段形状不同」的写入分支 ⇒ **该锚属于基线系**（初稿判成 `3cb3074`，**反了**） |
| `src/data/persistence.ts:1088` | **`3cb3074` 上是 `};`** —— ★ `bae6e6f` 上那一行 `if (f === 'TIME_PERIOD' && !repProfiles.timePeriod) continue;` **正是**本报告声称的「被读成全 0」的绕行 ⇒ **属于基线系**（初稿**反了**） |
| `src/editor/refConsumers.ts:40–45` | `ecbd1df` 起该行是 `*`（该注释块加长了） |
| `src/editor/refConsumers.ts:53` | `ecbd1df` 起该行是 `*/`，**`OwnerGranularity` 原样下移 1 行到 `:54`** —— ★ 初稿写「该行是 `consumerKeyOf`」，那又是**代理量的假值**（它是该行向上最近的声明，与这行无关） |
| `src/editor/session.ts:123–128` | `3cb3074` 起该区间是 `): void {`（`setTimePeriodAffinity` 签名末行） |
| `src/ui/app.ts:858–885` | `ecbd1df` 起起点是 `onRoleEdit: () => this.commitWorkingCopy(),` |
| `src/ui/app.ts:1240–1265` ／ `:1240–1275` | `ecbd1df` 起起点是 `onRunWriteBack: (field, productName) => …` —— ★ 那是**接线行**，不是函数体；`private async runWriteBack` 下移到 **`:1254`**（初稿写「四个 base 上都落在同一函数体」，**不准确**） |

**C. 两处「注释段」锚：人工核（非工具核）**

**为什么单列**：这两条落在**注释块**里，而脚本的 `owner` 是「该行**向上最近的声明**」⇒ 它报的是注释块**上面**那个不相干的声明 —— **两条都报错。**
⇒ 所以这两条**由人回读逐字**，**不引用工具结论**。

**C1. `src/core/contract.ts:111–113`** —— **只在 `3cb3074` 及以后成立**（`bae6e6f` 上那段头注不存在）。逐字（`@ 3cb3074`，即 `#27` 那一笔）：

```text
 * ★ **四个槽位一律可缺席**（`#27`，ADJ-02「统一」）：§3.1 把四个组件字段都写成「**组件值或空**」，
 * 且**缺席是合法状态**；**缺席的合法性只由 `Role` 决定**（`IGNORED` ⇒ 缺席合法；
 * `CORE`/`SECONDARY` ＋ 缺必需 Profile ⇒ 阻断 Publish）—— **四个组件一视同仁，没有哪一个特殊。**
```

- **人工核定所属**：`export interface ResolvedComponentProfiles`（该修订 **L124**）。
- ★ **脚本报的是 `TimePeriodProfile`（L104）—— 错的。**

**C2. `src/editor/session.ts:123–128`** —— **只在 `bae6e6f` 上成立**（`3cb3074` 起该区间是别的代码）。逐字（`@ bae6e6f`；该注释块整体为 **`114–130`**，属 `setRole(key: ConditionKey, role: AggregationRole)`，声明在 **L131**）：

```text
   *   自动补一份**行为中立**的档案，五段全 `1.00`」—— 理由是「提角色这个动作不该改变数值行为」。
   *   那条推理本身没错，但它**用自动生成掩盖了「缺配置」这个事实**：作者提完角色看到的是一份
   *   全 1.00 的档案，**分不出「我配过」与「系统替我填的」**。
   * - **收口 `Y`（现行）**：不生成，改为**如实报缺**。缺档案是**可见的 ERROR**，
   *   由作者自己决定配什么 —— 「缺配置 != 忽略」（开发需求 §4.5）这条由此在界面上真正成立。
   * ⚠️ `1.00` 而不是 `0` 的那条**具体教训仍然有效**，只是换了落点：将来若哪条通路要生成默认档案，
```

- ★ **脚本报的是 `if`（@`bae6e6f`）／`setFeedingLayerAffinity`（@`3cb3074`）—— 两个都错。**

⇒ ★ **C1／C2 是对代理量的证伪**：它给的不是「差一点」，是**指向另一个符号**。**若直接把工具输出当结论，会多报两条不存在的「锚错」。**

⇒ ★★ **一句必须写进正文的话**（它是本报告最重要的一条元结论）：
**本报告没有任何单一修订能让全部锚成立 —— `file:line` 锚解析在三个不同修订上。** ⇒ **读任何一条锚之前，先看它属于哪个 commit；「按某个数改回」是最坏的修法，它会把「两把尺子」变成一次真实的引入错误。**

---

## 0. ★ 三个「基准本身」的问题（先报，因为它们决定这张表能证明到什么）

### 0.1 取件与 SHA（每个 md 的 commit）

| 载体 | ref | commit | 备注 |
| --- | --- | --- | --- |
| ~~主基准~~ **降为辅助** `docs/implementation-brief-0.3.4.0-B.md` | `b5013e5f` | `b5013e5f`（**实质陈旧**：早于 ADJ-07…13；覆盖只到 §3.1–§3.5 ＋ §3.10） | blob `feecccea7e1f…`，102 行 |
| **★ 主基准（已升级）** `docs/review/ui-component-contract-r2/` | `review/ui-component-contract-r2` | **`ed2fde0`**（PR #7 `headRefOid`，与 `gh` 逐字核对 ✓） | 迭代：`b0544737` → `9a0232b` → **`ed2fde0`**；见 0.3 |
| **实现**（peer 未给，我查出来的） | `futou/hitfish-0.3.4.0-b-batch27` | **`bae6e6f`** | 主检出（本地 `preCompute` 仓）正 checkout 在它上面；领先 `futou/hitfish-0.3.4.0-b` **15 笔** |

### 0.2 ★ **对表面锚在投影目录，不在指定的主基准 md 上**

**探针面**：在 `b5013e5f:docs/implementation-brief-0.3.4.0-B.md` 全文（102 行）搜下列 10 个词，**全部 0 命中**：
`ADJ-`｜`C_SPLIT_REGISTERS`｜`EngagementMode`｜`owner_ref`｜`B1`｜`全 1.00`｜`1.00`｜`promotion`｜`Source mutation`｜`staged`

**同一批词在 `b0544737:docs/review/ui-component-contract-r2/` 里全部命中**（`ADJ-*` 命中 2–3 个文件）。

⇒ **对表面（`ADJ-08` / `B1` / `ADJ-07` / `ADJ-02` / `ADJ-11` / `ADJ-13` / `ADJ-09`）的判据文字在 `OPEN-ITEMS.md` 里，不在 brief 里。**
⇒ 而**该目录自述**（其 `README.md` 逐字）：「**权威一律是项目内的 Notion Current**，本目录只做投影。冲突时以 Current 为准。」
⇒ 按任务书「**每个判据都要能落在 md 的某一段上**」这条，**7 项里没有一项的判据能落在指定的主基准 md 上**。
⇒ **这是任务前提的问题，不是我执行的问题** ⇒ 按你说的「md 自相矛盾类」停手条件**记一笔并报你**，**我没有自己选一边**。

**但**：其中**部分项的「实质」在 brief 里是有的**（只是标签不同）—— 见下表「md 侧锚点」列。**凡能落到 brief 的，我按 brief 判；落不到的，我标 `md 无锚`，只用投影当线索。**

### 0.3 ★ 本地 ref 全部过期（本族已记过的坑，这次实测复现）

```
origin/review/ui-component-contract-r2   5a0674f6   ← 本地跟踪引用（旧）
pr7                                      0b2f01b6   ← 本地 ref（旧）
r2head                                   5a0674f6   ← 本地 ref（旧）
真 head（gh pr view 7 --json headRefOid） b0544737   ← 三者都不是它
```
`git fetch origin review/ui-component-contract-r2` 后 `FETCH_HEAD` == `b0544737` ✓。**下表用的是 `b0544737`。**

---

## 1. 主表（四列）

> **「md 侧」列的 `brief§N` ＝ 能落到主基准的**；标 `※投影` 的 ＝ **只能落到 `OPEN-ITEMS.md`（非权威投影）**，按任务书该跳过，但你在对表面里点名了，我**按线索读、不按裁判用**，并标注该行判力的来源。

| # | 项 | **md 侧逐字 / 锚点** | **实现实测（`bae6e6f`，file:line）** | **是否偏移** | **修不修 ＋ 代价** |
| --- | --- | --- | --- | --- | --- |
| 1 | **ADJ-08 `C_SPLIT_REGISTERS`** | **`brief §3`** 逐字：「桶层的 patch ＝ `AffinityAuthoringPatch`（**owner ＝ `FishEnvAffinityRef`**）」 | `src/editor/refConsumers.ts:53` `export type OwnerGranularity = 'affinity-row' \| 'species-bucket';`；`:36` 注释逐字「⚠️⚠️ **owner 粒度待裁**」；`src/editor/sourceOverride.ts` 头注：「owner 的**身份**是「中鱼习性模式」（`Engagement Mode`），**桶只是数据迁移期的行单位表达** ⇒ 那是**一个参数**，不是常量」 | ★ **是（部分）** | 见 §2 |
| 2 | **B1（不得自动生成全 `1.00` Profile）** | `※投影` `OPEN-ITEMS` ADJ-12 尾部；**brief 无锚** | `src/editor/session.ts:123–128`：**明确讨论并否掉**「自动补一份行为中立、五段全 `1.00` 档案」，理由逐字：「全 1.00 的档案，**分不出「我配过」与「系统替我填的」**」；并留「`1.00` 而不是 `0` 的那条具体教训仍然有效」 | **否 —— 已对齐** | 无 |
| 3 | **ADJ-07 raw Role 默认 ＝ `CORE`** | **`brief 无锚`**（brief §1 只写 `roles` 必填，§2 只给词表，**都没写默认值**） | `src/data/speciesBaseRecord.ts:41` 只有类型 `RoleOpValue = 'CORE' \| 'SECONDARY' \| 'IGNORED'`；`:127/:134` 逐字「**缺**的必填字段 —— 报出来，**不替它编一个默认值**」。**`defaultRole` / `rawRole` 符号 0 命中** | ⚠️ **无法判**（md 无锚）＋ **实现里找不到该默认值** | 待你回权威物定；若该默认成立，落点是 `speciesBaseRecord.ts` 一处 |
| 4 | **ADJ-02 缺席统一（时段不特权）** | **`docs/review/ui-component-contract-r2/OPEN-ITEMS.md:45`**：「缺席合法性**只由 `Role` 决定**；**时段不特权**」 | `src/core/contract.ts:111–113`（「四个槽位一律可缺席」那段头注） **注释**：「四个槽位一律可缺席……**四个组件一视同仁，没有哪一个特殊**」；但 `src/core/authoring.ts:326–358`（`collectAllIssues` 的 `for (const key of CONDITION_KEYS)` 循环） 的 `for (const key of CONDITION_KEYS)` 循环里**唯一的存在性检查是 `src/core/authoring.ts:337`（`key === 'TIME_PERIOD'`） 的 `key === 'TIME_PERIOD'`** | ★ **是（偏移）** | 主代理定性：**「另外三处缺检查」**，非时段特权（依据：两侧声明的口径都是「统一」）。⚠️ 同一文件内**类型与注释不一致**：解析类型目前**只允许 `timePeriod` 可空** ⇒ 另三个今天在类型上就不能缺席 |
| 5 | **ADJ-11 空底板那一支** | **`docs/review/ui-component-contract-r2/OPEN-ITEMS.md:59`** | ★ **反查「谁写 `refs`」⇒ `src/` 与 `scripts/` 里【没有任何写者】**（赋值面 `refs: {` / `refs = {` / `.refs =` **0 命中**）；`refs` 全部命中只有：类型声明 `src/data/derived.ts:44`（`refs` 的类型声明）／校验 `src/data/persistence.ts:484–489`（`refs` 的 `typeof` 校验）／**读**（断链检查 `1278–1287`）／渲染 | ★ **行为侧未见实现（且比「缺一支」更强：没有写者）** | 见 §8 |
| 6 | **ADJ-13 时段预设 target** | **`docs/review/ui-component-contract-r2/OPEN-ITEMS.md:61`** 逐字（六条）：五个 `SET`／一个 atomic batch／batch preview ＋ 显式确认／不持久化 `presetId`／target ＝ 当前 authoring layer／不切层不改 Source | ★ **`src/ui/app.ts:870–891`（`onApplyPeriodPreset` 的函数体；注释块 864–869） `onApplyPeriodPreset`：六条【全部成立】** —— ① `for (const k of TIME_PERIOD_KEYS)`（恰 5 个）② 同一循环 ＋ **一次** `commitWorkingCopy()` ③ **两阶段**（第一次点只置 `periodPresetPending` 先不落；**第二次点同一键**才落）④ `presetId` 在 `src/`＋`tests/` 共 6 处命中**全是注释/UI 文案、零写入**（**实测非声明**）⑤ `expressedCells`（`src/ui/app.ts:240`（`expressedCells` 的定义））＝ 当前编辑面的未落盘缓冲，冲刷进 `state.species[…].groups[…]` ⇒ target ＝ 当前层 ⑥ 该路径无任何切层/改 Source 动作，`setPatchFor` 只产 `{op,set,value,tier?}` | ✅ **已对齐** | 无 |
| 7 | **ADJ-09 事务两层 / Source mutation 一律 staged** | **`docs/review/ui-component-contract-r2/OPEN-ITEMS.md:57`** | ★ **反查「除 `runWriteBack` 之外还有没有第二条写盘路径」⇒ 找到两个出口**：`/api/write-back`（改产品表，`src/data/writeBackClient.ts:58`（发起 `POST /api/write-back`））与 `/api/editor-state`（编辑器持久层，`src/data/persistence.ts:1396–1410`：`httpFileStore`）。**写盘调用点 `src/ui/app.ts:1240–1275`（`private async runWriteBack`）：`materialize → planMaterialization → targetForChange → runWriteBack`，中间【没有】确认闸**；`staged`/`transaction`/`twoLayer` 在 `src/` **0 命中** | ★ **未见 staged 流程**（作用域见 §8） | 见 §8 |
| 8 | **并桶** | —（**这侧是我自己的实测**） | `fish_env_affinity` 2185 → 264；`fishEnvId` 取值集合 1360 → 212 | **已收敛** ✓ | 无 |
| 9 | **DEF version 驱动（发布前置）** | —（**不是代码偏移**） | `DEFHotUpdateManager` 路径 `{cdnRoot}/{channelId}/{VersionPrefix}{version}`；进程内缓存键 `(pond,月,日,时段)` **不含内容哈希** | **非代码项** ⇒ 见 §4 | 发版检查项 |

---

## 2. 第 1 项展开：ADJ-08 到底偏在哪、怎么修

**md（brief §3）要的**：owner **就是** `FishEnvAffinityRef`（单一物理 durable key）。

**实现做的**：把 owner 粒度做成**运行期参数**，且**两种读法都留着**：
```ts
export type OwnerGranularity = 'affinity-row' | 'species-bucket';   // src/editor/refConsumers.ts:53
export function ownerOf(e, granularity: OwnerGranularity): string {
  return granularity === 'affinity-row' ? `row:${e.scope}` : `species:${e.speciesId}/${e.scope}`;
}
```
注释还逐字写着 **「owner 粒度待裁」**，并把 `Engagement Mode` 称为 owner 的**「身份」**。

**为什么我认为这是偏移（三条，都可核）**：
1. brief §3 **没有**给出第二个读法 —— 它逐字钉在 `FishEnvAffinityRef`；
2. 投影侧 ADJ-08 的**全部要点**就是「**消灭「owner」这个模糊中间词**」；
   而实现的注释**恰恰把那个中间词又引入了一次**（「owner 的身份是中鱼习性模式」）；
3. 实现自己的**通则**（`src/editor/refConsumers.ts:40–45`（「别把会变的坐标钉进持久物」那条通则） 逐字）说「**不要把「会变的坐标」钉进代码或契约**」——
   这条本身是对的、我认同；但它被用来**保留一个待裁的两读法**，
   于是「待裁」成了**长期状态**，而 md 侧已经给了答案。

**修不修 ＋ 代价（我不改，列给你）**：
- **最小改法**：`OwnerGranularity` 收成单一实现（删 `'species-bucket'` 分支），`ownerOf` 退化为
  `row:${e.scope}`；注释里那句「待裁」与「身份是 Engagement Mode」改成 brief §3 的逐字。
  **代价：改 1 个文件、约 3 处**（类型 1、函数体 1、头注 1），**调用方无需改**（形参是别名类型）。
- ⚠️ **但这条是否该改，取决于你对 ADJ-06（粒度＝物种,桶）与 ADJ-08（物理 key＝FishEnvAffinityRef）
  的并合读法** —— 投影侧把两者**都列为已裁**，而它们在实现的这段代码里**是同一条 `ownerOf`**。
  ⇒ **这一处是 ADJ-06／ADJ-08 的接缝**，**该由你回权威物定**（我按任务书不裁判）。

---

## 3. 未判项 —— **现已全部判完，见 §1 与 §8**

（本节原记「#4／#5／#6／#7 未读完」。**第三轮已按主代理「从写盘出口反查」的法子扩面**：
`#4` ⇒ §1 第 4 行（**偏移**）；`#5`／`#7` ⇒ §8（**行为侧未见实现**）；`#6` ADJ-13 ⇒ §1 第 6 行（**✅ 已对齐 —— 六条全成立**；本条一度被写成「部分对齐／两条子判据未读到证据」，**那是搜错入口名所致**，收口见 §11）。
**保留本节作留痕**，不删。）

## 4. 第 9 项：DEF version 驱动（**发布前置，不是代码偏移**）

**事实（我上一条线实测的）**：进程内缓存键 `(pondId, monthId, dayId, periodId)` **不含内容哈希**；
热更走 `{cdnRoot}/{channelId}/{VersionPrefix}{version}` ⇒ **按 version 取清单**。
⇒ **换了 DEF 内容但不 bump version ⇒ 客户端继续用旧文件。**

**建议写成发版检查项（不是代码改项）**：
> **凡改动会影响 DEF 产物的配置，发版时必须 bump DEF version；否则改动不生效且无告警。**

---

## 5. 探针面清单（每条「无偏移／0 命中」的搜法与作用域）

| 结论 | 搜法 | 作用域 |
| --- | --- | --- |
| brief 里 0 命中那 10 个词 | `git show b5013e5f:docs/implementation-brief-0.3.4.0-B.md \| grep -c` | **那一个 blob（102 行）**；不等于「这一族里没有」 |
| 对表面词在投影目录命中 | `git grep -c <词> b0544737 -- docs/review/ui-component-contract-r2/` | **该目录 9 个文件** |
| 实现里的 ADJ 编号 | `git grep -o -E 'ADJ-[0-9]+' bae6e6f -- src tests` | **`FishHabitEditor-0.3.4.0-b/{src,tests}`**；结果：ADJ-03×2、ADJ-04×2、ADJ-06×3、ADJ-08×1 —— **其余 9 个 ADJ 编号 0 命中** |
| B1 已对齐 | `git grep -n '1\.00' / '全 1' bae6e6f -- src` | 同上；`src/editor/session.ts:123–128`（否掉「全 1.00 档案」那段注释） |
| ADJ-07 找不到默认 | `git grep -n "'CORE'"` ＋ `defaultRole`/`rawRole` | 同上；`'CORE'` 只作类型字面量出现 |
| ADJ-09 词汇 0 命中 | `git grep -c staged/Staged/transaction/Transaction/twoLayer` | 同上 |
| 实现仓归属 | 逐分支 `git grep -l` 扫 `AffinityAuthoringPatch\|sourceOverride\|AffinityRolePatch` | **`preCompute` 仓 30 条本地/远端分支**；命中只有 `futou/hitfish-0.3.4.0-b*` 族 ＋ `origin/futou/hitfish-0.3.4.0-b` |

★ **一条要写明的**：我**起初查错了分支**（`futou/bucket-merge-next`，那是我另一条线的 checkout），得到「全部 0 命中」。
⇒ **若就此下结论会是「实现根本不存在」**。按分支重扫后才定位到 `batch27`。
⇒ **这就是本族「按分支查、别按检出答」那条**；我把它记下来是因为**它差一点产出假结论**。

---

## 6. `【待核】` 项的跳过记录（按任务书要求）

主基准 brief 里 **`【待核】` 共 4 处**，**均未用作判据**：

| brief 位置 | 内容 | 处理 |
| --- | --- | --- |
| §二.1 | 组件值的「内部形态」（序列化细节） | **跳过**；但实现 `src/data/speciesBaseRecord.ts:18–30`（`ComponentValue` 编码那段头注） **自述**它选的形由 ADJ-04 裁定、**且明写「页还没落这句」** ⇒ 这是**实现侧已知的页/记录页落差**，不是本次能判的 |
| §二.2 | `AggregationRole` 三个值与次要聚合数值 | **跳过** |
| §二.3 | `fail_env_coeff` 的 GAP-013/014 现状 | **跳过**；注：那一条我这条线**已有实测**（见 §1 #8 的并桶线），但**不属本次判据** |
| §二.4 | 「页会动，落码前再读一次」 | **跳过**（元指令） |

★ **另记一条**：实现引用了 **`§3.6` / `§3.7` / `§3.8`**（分别 20 / 8 / 3 次），
而 **brief 的附录自述其取数面只有 `§3.1／§3.2／§3.3／§3.4／§3.5／§3.10`**
⇒ **实现在引 brief 未覆盖的节**。**这不是偏移**，但它说明**实现的依据面 > brief 的覆盖**，
⇒ **用 brief 当唯一基准会系统性漏掉 `§3.6/§3.7/§3.8` 那一片**（尤其 `policyTemplate.ts` 整份建在 §3.6 上）。

---

## 7. 阻塞项（等你）

1. ★ **对表面的判据落不到指定的主基准 md 上**（§0.2）—— 7 项里没有一项能落在 brief；
   只能落在**自述非权威**的投影目录上，而权威（Notion）你已明令不读。**⇒ 请你定基准**。
2. ★ **ADJ-06 与 ADJ-08 在实现里是同一条 `ownerOf`**（§2）—— 两者在投影侧**都列为已裁**，
   但读法上相抵（粒度 vs 物理 key）。**⇒ 该由你回权威物定，我不裁判。**
3. ~~**#4／#5／#6（部分）／#7 未读完**（§3）~~ ⇒ **★ 已全部读完并收口**（第四轮）：`#4` 偏移／`#5`・`#7` 行为侧未见／**`#6` ✅ 已对齐（六条全成立）** —— 见 §1 第 4／6 行与 §8、§11。**此条不再挂着。**

---

## 8. 反查扩面（第三轮，按主代理「从写盘出口反查」的法子）

### 8.1 `#5`（ADJ-11）—— **`refs` 没有写者**

**搜法**：`git grep -E 'refs:\s*\{|refs\s*=\s*\{|\.refs\s*='` on `bae6e6f` 的 `src/` ＋ `scripts/`
⇒ **0 命中**（`tests/` 里有构造，那是夹具不是生产代码）。
\`refs\` 在 `src/` 的全部命中分类：**类型声明 1**（`src/data/derived.ts:44`（`refs` 的类型声明））／**校验 1 处**（`src/data/persistence.ts:484–489`（`refs` 的 `typeof` 校验），判 `typeof rec.refs`）／**读 1 处**（`src/data/persistence.ts:1278–1287`（断链检查，读 `refs`），查断链）／**渲染/格式化**（`ui/format.ts`、`ui/render/template.ts`）。另有 `policyTemplate.ts` 的 `refs` 是**另一个东西**（`PolicyDirectRef[]`），不要与生产行的 `refs` 并读。

⇒ **判**：ADJ-11 的三条行为（不产生 projection／`refs[component]` 保持空／不进 evaluator）**在实现里不可观察** —— 因为 **`refs` 从来不被写**。
⚠️ **作用域**：覆盖 `src/` ＋ `scripts/` 的**赋值面**；`tests/` 内的构造不算实现。

### 8.2 `#7`（ADJ-09）—— **未见 staged 流程；写盘有两个出口**

**搜法**：从唯一写盘出口 `src/data/writeBackClient.ts:50`（`runWriteBack`） runWriteBack` 反查调用方 ⇒ `src/ui/app.ts:1240–1265`（`private async runWriteBack`）（唯一调用点）。
**读到的流程**：`materialize(...)` → `planMaterialization(...)` → `changeKindOfPlan` → `targetForChange` → **`runWriteBack(...)` 直接调用** ⇒ **中间没有「预览／确认」闸**。
**第二条写盘出口**：`src/data/persistence.ts:1396`（`httpFileStore()`）→ `POST /api/editor-state`（编辑器自有持久层）。
⇒ **判**：**Source mutation 的 staged 流程在这批模块里未见**。
⚠️ **作用域**：覆盖 `ui/app.ts` 的写回调用点 ＋ `src/` 内的写盘出口搜索（`fetch(`／`/api/`／`writeFile`／`fs.`）；**不覆盖** `vite.config.ts` 服务端实现与 `scripts/apply-writeback.mjs`。

---

## 9. ★ 两条口径（本轮确立）

### 9.1 「已落」的判据（主代理采纳为本批口径）

> **一条「已落」的验收必须是「能演示行为」的** —— **类型层可达 ≠ 已落；注释里写着 ≠ 已落；测试钉住一个常量 ≠ 已落**。
> ⇒ **凡只有类型／注释／常量支撑的，一律写「声明侧已落、行为侧未见」，不写「已落」。**

**本轮的两个样本**：`#3`（`src/editor/policyTemplate.ts:84`（`PolicyTemplatePayload.roles` 的注释） 注释写「默认 `CORE`」，**无代码折出**）／`#4`（`src/core/contract.ts:111–113`（「四个槽位一律可缺席」那段头注） 注释写「四组件一视同仁」，**只对 `TIME_PERIOD` 实施**）。

### 9.2 两个计数面**不要读成相抵**

`#27` 报的是**同一不变量的站点**（`src/core/authoring.ts:337`（`key === 'TIME_PERIOD'`） ＋ `src/data/persistence.ts:872`（「时段形状不同」的写入分支）「时段形状不同」的写入分支 ＋ `src/data/persistence.ts:1088`（「无档案被读成全 0」的绕行）「无档案被读成全 0」的绕行 ＝ **3 处**）；
本报告数的是**存在性检查**（`ACTIVE_PROFILE_MISSING` 只有 `src/core/authoring.ts:337`（`key === 'TIME_PERIOD'`） **1 处**）。
⇒ **两者都对、不矛盾** —— 另两处**与该不变量相关但不是存在性检查**。同类风险本族有过（一个集合被 N 个读者各取子集）。

---

## 10. ★ `#6` 的自我更正（本轮，留痕）

**一度**（第三轮）：我把 `#6` 判成「**部分对齐**（`target ＝ 当前 authoring layer` 与「五个 `SET` 一个 atomic batch」**未读到证据**）」。

**收口**（第四轮）：**六条全部成立**，判 **✅ 已对齐**。依据 `src/ui/app.ts:870–891`（`onApplyPeriodPreset` 的函数体）**@ `ecbd1df`**（逐字见 §1 第 6 行）。

**为什么一度判错**：**我搜错了入口**。我搜的是符号名 `applyPreset`／`ApplyPreset`／`authoringLayer`／`currentLayer`／`activeLayer`／`targetLayer` ⇒ **全部 0 命中** ⇒ 我据此写「未见证据」。
而实现里那条路的入口是 **UI 回调 `onApplyPeriodPreset`，落在 `src/ui/app.ts`**（不在 `editor/` 层）。

⇒ ★ **这说明「先找载体」这条法子有一个失败模式**：**载体名取错 ⇒ 得到假「未见」**。
⇒ 配套纪律（本轮补）：**「未见证据」之前，先证明「我搜的是那条路真正的入口」** —— 用**行为面**（谁调它／它调谁）而不是**名字面**去定位入口。

**另一条同轮的自我纪律**：我在那条命令里**预写了一句「⇒ 载体探测结论」**，随后被输出当场否掉。
⇒ **在看见输出之前先写下结论**，这个动作本身会把「预期」写成「事实」。**别在命令里预写结论句。**

---

## 11. ★ 探针纪律（本轮扩，主代理升为通则）

### 11.1 「先找载体」的三根轴 —— **0 命中不等于「不存在」**

| 轴 | 情形 | 结论 | 本轮样本 |
| --- | --- | --- | --- |
| ① | **载体不存在** | 真·不可观察 | — |
| ② | **载体存在、但没人写** | 真·不可观察 | **`#5`**：`refs` 在 `src/` ＋ `scripts/` **零写者** |
| ③ | **载体有人写、我找错了名字** | ★ **假·未见** | **`#6`**：我搜 `applyPreset`（0 命中），实现叫 **`onApplyPeriodPreset`**，且**不在 `editor/` 层而在 `ui/` 层** |

⇒ ★ **通则：探针 miss 的第一嫌疑人应当是「我用错了名字」，不是「它不存在」。**
★ 且 **② 与 ③ 外观完全一样（都是 0 命中）、结论相反** ⇒ ★ **新判据：说「行为未见」时，必须同时交代「我搜了哪些名字」。**
（「按层找」也会 miss —— **UI 回调名 ≠ 领域符号名**。）

### 11.2 「未见证据」之前，先证明「我搜的是那条路真正的入口」

定位入口**用行为面（谁调它／它调谁），不用名字面**。本轮 `#6` 的入口就是这样找到的：
顺 `TIME_PERIOD_PRESETS` 的**引用面**才落到 `src/ui/app.ts` 的回调。

### 11.3 预写结论：不是错，错的是拿它当读数

**预写结论本身有价值**（它把预测暴露出来，输出才能当场否掉它）—— 本轮我在命令行里预写的
「⇒ 载体探测结论」就被输出当场否掉 ✓。**错的是拿预写的当读数。**

### 11.4 ★ 锚的卫生（本报告已按此自查一遍）

- **所有行号必须配内容锚**（函数名／符号名／那句逐字）—— **行号是易变的锚**；
- **所有路径必须是仓内相对全路径**（`src/ui/app.ts`，不是 `app.ts`）。

**★ 本节原写「本轮我自己的三处锚偏了」—— 这句是错的，已按实测更正（作者，2026-09-21）：三处都不是「偏」，是「两把尺子」。**

三处**各自量在不同的修订上**，而**表里从来没有写「这个数属于哪个 commit」**：

| 符号（`file`） | 在 `bae6e6f`（**本报告声明的基线**） | 在 `3cb3074` 及以后（含当前头 `b003dfe`） |
| --- | --- | --- |
| `onApplyPeriodPreset`（`src/ui/app.ts`） | 注释块 **858–863**、函数体 **864–885** | 注释 **864–869**、函数体 **870–891** |
| `setPatchFor`（`src/data/persistence.ts`） | **1061** | **1117**（函数体 **1117–1120**） |
| `httpFileStore`（`src/data/persistence.ts`） | **1340** | **1396** |

⇒ ★ **`858–885` 与 `870–891` 在各自那个修订上都是对的**；而 `1117–1120` / `1396` **只在 `3cb3074` 及以后成立** —— 在 `bae6e6f` 上，`1117–1120` 落在 `upsertSpeciesEntry` 里，**不是** `setPatchFor`。
⇒ ★★ **所以「改回某个数」是最坏的一种修法** —— 它把「两把尺子」的问题变成一次**真实的引入错误**。（实测：`onApplyPeriodPreset` **全历史从没有一版起始于 858**；位移因 `ecbd1df` 对 `app.ts` 做了 **+18/−4**。）
⇒ **正解是「每个锚带它自己的 commit」**，不是把行号换成另一种写法。

⇒ **真正改正了的是另外两件**：全表的 `file` 一律补成**仓内相对全路径**（`src/ui/app.ts`，不是 `app.ts`）；并给每条配**内容锚**（函数名／符号名／那句逐字）。

★ **全量锚表在头部「★ 锚的修订归属」**（11 条须标 commit 的锚，逐条给解析于哪个修订）—— **本节只讲最初被误标的那三条**；**两处冲突时以头部那张表为准**（它是对全文实跑出来的，本节的表是当时手写的）。


**另一条同轮自查**：我第一版的「裸行号」复查脚本**自身有 bug** —— 正则把
`src/data/persistence.ts:1396` 的**后缀**也当成命中 ⇒ **差点报「已清干净」**。
改成按**前一个字符是否 `src/`** 判定后，才查出真有 4 条裸引用。
⇒ **判据：证「已清干净」的脚本，必须先证明它能区分「干净」与「脏」**（否则它只会报绿）。

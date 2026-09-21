# REVISION 12 — packet 侧五处文本修正（**不动图、不动 Notion**）（2026-09-21）

对齐 head：`5591f24`（REVISION 11）。

**本版只改文本**：图仍是 REVISION 11 那三张（现行）；Notion 侧四处**不在本版**（见末节）。

---

## 一、⚠️ 撤回一句**过早的 CLOSED**（这条最要紧）

`REVISION-10.md` §六 写着 **「Persistence Contract: CLOSED / READBACK PASSED」**。
**它已被推翻**：`Species Component Recipe` 的物理 schema **与** `AffinityAuthoringPatch.sourceOverride` 的物理落点**都仍未闭** ——

- **§3.1** 的字段表对四个组件仍写 `组件值或空`，**没有** source binding、**也没有** Species 每字段 `ADD/SET` 的 durable shape；
- **§3.3** 的表里**没有 `sourceOverride` 行**（它只出现在表后的散文里）；
- 更硬的一处：**§3.3 的表被钉在 bucket 级**（`scope_kind` 类型是 **literal `bucket`、必填**，说明逐字「Current 固定为 `bucket`；**numeric override 不允许 row-level**」；`scope_key` 是 `young`/`mature`）⇒ **那条记录结构上不可能同时承担 species 级 Recipe**。

⇒ **处置**：`REVISION-10` §六 的那句**作废**；`README` 的 `REVISION-10` 行已加 ⚠️ 并写明**在它真闭之前，不得再写未加限定的「Persistence CLOSED」**。

## 二、`Role 恒为 row-level` 收窄（`contract-cards.md`）

原句是**全称句**，而物种侧本来就有 Role op（`INHERIT / SET`）⇒ 全称不成立；**在 Component Recipe 正在 reopen 的当口留着它，很容易让实现为「统一粒度」反向把 `Species Policy Recipe` 删掉**。

**改成**：**两条 patch 轨道（`AffinityRolePatch` / `AffinityFailEnvCoeffPatch`）恒为 row-level**；**物种层的 Role op（`INHERIT` / `SET`）不是 override，而是决定该物种的 `Effective Default Role`**，住在 §3.1 —— **与本节两条 patch 轨道并存；不得为「统一粒度」把它删掉**。

（出处：`Effective Default Role` ＝ **记录页 §331 ④**，Owner 亲裁原话。）

## 三、Affinity 缺省支：把「两个寄存器」写开（`component-contract-consolidated.md`）

汇编原有三条说的是**显示层**（行内必须给具体串、不显示泛称）。但**读起来像"泛称被禁"**。
⇒ 补一条：**「沿用物种操作」是这一支的「名字」（概念层，保留）**；**行内「显示」必须给具体串** ⇒ **名字 ≠ 显示，两者不矛盾**；且「沿用物种操作」与「仅使用当前来源」**不得合并成「恢复」**。

## 四、`figma-current.md` §六 的字节数更正（**我们自己造成的陈旧**）

§六 表里 `108:311` 那张仍写 **`174828`** —— 那是 REVISION 6 的数；REVISION 11 换图后是 **`175020`**。⇒ 已改。**这正是「改了画布／换了图，引用它的那一处没跟上」的同一种病**，记一笔。

## 五、`README` 去重

`REVISION-10` 曾被**列两次**（两个写者各加一行），且第二条自称「**现行 closure**」并写「**Persistence readback 完成**」（与第一节相抵）⇒ **合并为一行**（保留其可用内容：Source＝前层＋Card、Role＝Card＋Policy 双入口单 Truth、卡 2 恢复、annotation 去留痕、保留那条 UI 缺口），并加 ⚠️ 与第一节的撤回。
⇒ 并**核实「现行」只有一处**（现在只有 `REVISION-11` 那行）✓。

---

## 六、不在本版、仍在飞的四项（Notion 侧，等时机）

1. **两寄存器句**落《编辑器界面》§1.2 与《心智模型与 IA》§2；
2. **§3.4 的粒度不变量收窄**（逐字已定，引号保留页上原形）；
3. **`AffinityRolePatch.species_key` 的那条不变量**（`== ProductionRowLedger[row_key].species_key`；不一致 ⇒ diagnostic / reconcile error；**冗余 `species_key` 不得成为第二份 owner truth、不得反向覆盖 ledger**）；
4. **§3.1／§3.3 的 schema 重构**（Component Recipe 与 `sourceOverride` 的物理落点）。

⇒ 这四项**都要先过页写入者的手**，且按已定的序**排在契约 gate 之后**。**本版不把它们写成已闭合。**

**通过判据**见 `REVIEW-PROMPT.md` §六（两层门）。

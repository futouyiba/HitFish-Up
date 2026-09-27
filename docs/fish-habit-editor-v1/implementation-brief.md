# Fish Habit Editor V1｜Implementation Brief

> Status: Current Implementation Entry for V1  
> Product Authority: [product-contract.md](product-contract.md)  
> Semantic Authority: [common-semantics.md](common-semantics.md)  
> Surface Contracts: [authoring-surface.md](authoring-surface.md), [shared-assets.md](shared-assets.md), [secondary-surfaces.md](secondary-surfaces.md)  
> Scope: [版本范围与阶段路线](../review/fish-habit-editor-version-scope.md)

本文只列 V1 最小生产闭环的实现切面与尚需工程落点，不重新定义产品语义。

本文按“单机单写者、已有 Fish Habit、非破坏性 Publish”组织。Coding Agent 不需要实现多人 revision 协议、Species Base fresh-create、legacy adjudication UI、Production ownership graph / GC 或 Git 客户端。

## 1. V1 最小闭环

```text
existing Editor Species Base / Compat Subject
→ Component Source（Shared Template / Authoring compatibility data）
→ Authoring
→ Validation / Resolve
→ Publish
→ local Production working tree
```

V1 不实现：

- 新 Species identity；
- 用户创建任意 Mode；
- Family / Species Preset；
- Quality / StockRelease / FishRelease authoring；
- Bake；
- Production reverse reconcile。

## 2. Existing Subject integration

Fish Habit Editor 只读 authoritative Fish Basic，用于已有 Subject 的 Species identity / display：

- `species_key` 使用 Fish Basic 稳定 ID；
- display name 只用于 UI；
- Habit Editor 不写 Fish Basic；
- 已有 Species Base 的 `species_key` 若失效，产生 `BROKEN_SPECIES_REF` 并阻断 Publish；
- V1.0 不提供 Species Base creation / “开始配置其他鱼种”。

普通 Authoring 的输入前提：

- Species Base 已经存在于 authoring working tree；
- system-default Affinity identity 已经存在并能映射；
- existing Compat 若属于 `young / mature` slot，可进入“小个体 / 大个体 [兼容]”Subject；
- unmapped legacy row 不要求 Coding Agent 在 Editor 内 adjudicate，可留给 Editor 外部的数据准备脚本。

## 3. Source catalog / picker

Component Source 统一支持：

```text
Shared Template
Authoring compatibility data   # UI：已有数据 · 兼容
```

实现要求：

- Source catalog 从当前 Authoring persistence 读取；
- 对兼容数据只按 Component Kind / schema legality 枚举候选；
- 不按当前 Species / Quality 推导 owner；
- 若现有 Authoring 数据已经保留原 Production 英文 `name`，UI 直接显示；
- durable binding 沿用当前 Authoring persistence 已有的 Source reference / key；
- **不新增 ImportedSourceSnapshot aggregate、snapshot id、provenance schema 或 lifecycle**；
- 如果当前实现已经使用冻结 input snapshot / JSON 输入层，继续通过现有 adapter 消费即可，不为本轮另造持久化模型；
- Production 文件变化不会自动改变普通 Source catalog；
- 若需要从旧 Production 重新准备 Authoring 输入，属于 Editor 外的数据准备工作，不是 V1.0 Editor flow。

中鱼习性模式还允许 `FOLLOW_SPECIES`，并与 explicit Template / compatible-data pin 保持正交。

## 4. Existing System Default Affinity

system-default Affinity 不是第二个 Authoring Subject，也不是业务 Mode。

V1.0 的前提是该 identity 已经存在并能映射到 Species Base。Editor 只需要：

- 识别稳定 existing Affinity identity / row mapping；
- 不把它当成 `young` / `mature`；
- ordinary UI 不显示为中鱼习性模式；
- Species Base Authoring 改变后，Publish 更新它所引用 / materialize 的 Profile 与 Policy 结果；
- StockRelease / FishRelease 可以继续在自己的配置中引用该 EnvAffinity；
- Habit Editor 不写 Quality / StockRelease 关联。

如果现有数据无法无歧义识别 system-default Affinity，属于进入 V1.0 前的数据准备问题，不在 Editor UI 中设计 migration / create flow。

V1.0 不实现 Species Base / system-default Affinity Create / Archive / Delete。

## 5. Existing Compat Mode

V1 只编辑已存在、且 ingress 已无歧义映射到 `young / mature` physical slot 的 Compat FishEnvAffinity。产品 UI 将这些 rows 放在“中鱼习性模式”下展示：`young → 小个体`，`mature → 大个体`。

- 一个 UI Mode 对应一条既有 Affinity row；
- 该 Affinity row identity 必须保留；即使 Mode 最终完全跟随 Species、所有 Component/Profile payload 与 Species 相同，也只能复用下层 Profile projection，不能把 Compat Affinity row 本身折叠掉；
- Source / numeric operation / Role / coeff 继续按 V1 Common Semantics；
- V1 不创建额外 Mode。

V1.0.1 才补缺失 fixed slot 的按需创建：

```text
小个体    → young
大个体    → mature
```

两个 slot 不要求成对存在；Species Base / 基础习性始终是默认入口。

## 6. Shared Template

实现 [shared-assets.md](shared-assets.md) 的最小能力：

- blank create；
- extract from Effective Component / Policy；
- clone；
- metadata autosave；
- complete-value multi-field candidate；
- impact recompute；
- Archive / Restore；
- Hard Delete guard；
- Replace References。

Template create 与 Fish binding 必须是两笔独立 mutation：

> Create Source ≠ Bind Source.

## 7. Resolve

Resolve 只消费最近一次成功保存的 durable state。

输出：

- Resolved Overview；
- 最短充分因果说明；
- partial resolve；
- shared diagnostics。

不得在 UI 内实现第二套 resolver。

## 8. Publish

Publish 是单机全局动作：

```text
flush / verify saved Authoring state
→ full validation
→ read current Production working tree
→ materialize
→ create / update 明确目标 rows
→ keep all other rows unchanged
→ reread touched rows/files
→ verify
→ success
```

V1.0 使用**非破坏性 patch**：

- 不删除 Editor 不认识的 row；
- 不做 orphan GC / obsolete-row cleanup；
- 不做 managed-vs-pass-through ownership graph；
- 不做 whole-generation concurrent baseline protocol；
- touched output reread + verify 是 success 必要条件。

Materializer 仍必须区分 Affinity identity row 与可复用的 Component/Profile row：system-default / Compat Affinity identity 不因 payload 相同而合并；Profile projection 才可以按明确 lineage 复用。

如果 materialization 需要新建 Production row 并取得 `row_id`：

```text
create → reread → unique row_id → local mapping → verify
```

未完成这条链路不宣告成功，不 blind recreate。

## 9. 推荐实现顺序

```text
1. load existing Authoring working tree
2. Fish Basic + existing Species Base / Compat loading
3. Species Base / Compat Authoring
4. Source catalog：Shared Template + Authoring compatibility data
5. Shared Template create / edit / propagation
6. Resolve
7. Web Dev Server 下完成 Non-destructive Publish + touched-output verify
8. Electron Host Shell + portable ZIP packaging
9. V1.0.1 fixed Compat slot create
```

先完成 Domain / Authoring / Publish 核心闭环，再包 Electron；不要让桌面壳阻塞核心开发。

其中 1–8 构成 V1.0；9 不阻塞 V1.0 Freeze。

Workspace / Electron 物理边界见 [workspace-and-delivery.md](workspace-and-delivery.md)。

## 10. V1 验收最小样例

至少覆盖：

1. 从 authoring working tree 载入已有 Species Base / Compat Subject；
2. default Affinity 不作为第二个业务 Subject；
3. `young / mature` UI 显示“小个体 / 大个体”，缺任一 slot 都合法；
4. Shared Template 与合法同 Kind Authoring compatibility data 都可以成为 Component Source；
5. Source Picker 不扫描 Production working tree；兼容数据若已保留原 Production 英文 `name` 则直接显示，不推导 Fish ownership；
6. 不为兼容数据新增 snapshot identity / provenance persistence contract；
7. Source Change Candidate 正确展示 before / after，原有 Operation 不被偷偷清理；
8. 普通字段 Autosave 到本地 Authoring state；
9. Extract / Template edit / propagation 可用；
10. Resolve 解释最近一次成功保存的 Authoring Truth；
11. Publish 只 create / update 明确目标 row，其它 Production row 保持不变；
12. Publish 后 reread touched output 并 verify；
13. Production working tree 可由外部 Git 直接 diff / commit / merge；Editor 不实现 Git merge；
14. save / Production write failure 不冒充成功；
15. V1.0 没有 Species Base fresh-create / migration adjudication UI / Production GC；
16. Electron ZIP 保持 app / authoring / production sibling，mutable data 不进 `app.asar`。

V1.0 不以 arbitrary Mode creation、Family、Quality、Bake、多人协作、reconcile 或 Production GC 作为验收前提。

## 11. Closure Status

### 11.1 Product / semantic closure

V1.0 已冻结的最小语义：

- 只编辑已有 Species Base / existing Compat；
- Species identity 来自 Fish Basic，只读；
- system-default Affinity 是已有 Species Base 的 Production projection，不是第二个 Authoring Subject；
- `young / mature` 是 existing Compat physical slots，UI 映射为“小个体 / 大个体”；
- Component Source = Shared Template 或 Authoring persistence 中同 Kind compatible data；Compat 还可 Follow Species；
- compatible data 只从 Authoring persistence 读取；若已有原 Production 英文 `name` 则直接显示，不推导 Fish ownership，也不新增 snapshot object model；
- Source / ADD / SET / CLEAR / Policy / Resolve 语义保持现行 Contract；
- Shared Template create / extract / propagation / lifecycle 保留；
- Publish = 单机非破坏性 create/update + touched-output reread/verify；
- 多人协作、Git merge、Production GC、reverse reconcile 不属于 V1.0。

### 11.2 Remaining engineering gates

只保留真正会阻塞落码的物理问题。

**G1｜Existing Fish / Species adapter**

- 确认 Fish Basic 稳定 Species ID 与 display / canonical English name 来源；
- 确认已有 Species Base / system-default Affinity / Compat 的读取映射；
- 只读 Fish Basic，不实现 Species Base fresh-create。

**G2｜Source catalog adapter**

- 为每个 Component Kind 从当前 Authoring persistence 枚举合法 compatibility source data；
- 复用当前已有 Source reference / key 与 typed payload；
- 若现有数据已有原 Production 英文 `name`，将其用于 UI；
- 不新增 snapshot identity / provenance schema / lifecycle；
- 不在普通 Source catalog 阶段读取 Production working tree；
- 不实现 current-Species ownership 推断；
- 与 Shared Template 一起提供统一 Source Picker 数据。

**G3｜Production materialization / naming**

- 固定各 Profile / Affinity 子表的真实 lookup key、name collision domain 与 normalization；
- Shared Template English name 如何派生 Production Profile name；
- Existing row 能否原地 update、何时必须 create 新 row；
- 新 row 若有 `row_id`，完成 create → reread → mapping → verify；
- Publish 采用非破坏性 patch，不承担旧 row cleanup。

完成 G1–G3 后，V1.0 不需要新的产品裁决即可实现。

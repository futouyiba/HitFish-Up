# Fish Habit Editor V1｜Implementation Brief

> Status: Working Implementation Baseline  
> Product Authority: [product-contract.md](product-contract.md)  
> Semantic Authority: [common-semantics.md](common-semantics.md)  
> Surface Contracts: [authoring-surface.md](authoring-surface.md), [shared-assets.md](shared-assets.md), [secondary-surfaces.md](secondary-surfaces.md)  
> Scope: [版本范围与阶段路线](../review/fish-habit-editor-version-scope.md)

本文只列 V1 最小生产闭环的实现切面与尚需工程落点，不重新定义产品语义。

## 1. V1 最小闭环

```text
Fish Basic
→ 选择已有 Species
→ 若无 Habit：创建 Species Base + 系统默认 Affinity projection
→ Species Base / 已有 Compat Mode Authoring
→ Shared Template
→ Validation / Resolve
→ Publish
```

V1 不实现：

- 新 Species identity；
- 用户创建任意 Mode；
- Family / Species Preset；
- Quality / StockRelease / FishRelease authoring；
- Bake；
- Production reverse reconcile。

## 2. Species Catalog integration

Fish Habit Editor 读取 authoritative Fish Basic：

- `species_key` 使用 Fish Basic 稳定 ID；
- display name 只用于 UI；
- Habit Editor 不写 Fish Basic；
- 已有 Habit Species进入正常左栏；
- 尚无 Habit Species 通过“开始配置其他鱼种”搜索选择。

必须保证同一 `species_key` 不能重复创建 Species Base。

## 3. Species Base creation transaction

创建输入只有五个 binding：

```text
Temperature Source
Structure Source
Feeding Layer Source
Time Period Source
Policy Template
```

提交前校验：

- 五个 binding 都存在且当前可选；
- 四个 Component 可以 Resolve 完整 Profile；
- Policy 可以 Resolve 完整 Effective Policy；
- `species_key` 尚无 Species Base。

一次 atomic transaction 同时创建：

1. Species Base Record；
2. 一个系统默认 Affinity projection record / ledger entry。

初始化 transaction 不写：

- ADD / SET / CLEAR；
- Role override；
- fail_env_coeff override；
- Quality / StockRelease binding。

创建成功后直接进入普通 Species Base Authoring。

## 4. System Default Affinity projection

系统默认 Affinity 不是第二个 Authoring Subject，也不是业务 Mode。

固定语义：

```text
4 Component Source = FOLLOW_SPECIES
numeric operation  = absent
Role patch         = absent
fail_env_coeff     = absent
```

因此它完全跟随 Species Base。

实现必须满足：

- 有稳定 Editor identity / row key；
- Publish 前可以处于未物化状态；
- Publish 后得到 Production row identity；
- ordinary UI 不把它列为“中鱼习性模式” child；
- StockRelease / FishRelease 可以在自己的配置中引用其 Production EnvAffinity；
- Habit Editor 不写这条外部关联。

### 4.1 仍需落码前确认的窄点

不要在产品文档中发明新字段；实现前只需确认：

- 当前 ProductionRowLedger 用哪个既有字段 / bucket 表达系统默认 Affinity；
- 默认 Affinity 的 production human-readable name 如何沿现有规则生成；
- collision 的 lookup domain；
- 新 row 的 `row_key → row_id` 回填路径。

如果现有 schema 已能无歧义表达，就复用；只有无法表达时才提交 schema delta。

## 5. Existing Compat Mode

V1 只编辑已存在的 Compat Mode / FishEnvAffinity：

- 一个 UI Mode 对应一条既有 Affinity row；
- Source / numeric operation / Role / coeff 继续按 V1 Common Semantics；
- V1 不创建额外 Mode。

V1.0.1 才补固定：

```text
幼年
成年及以上
```

的缺失 Compat Mode 创建。

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

Resolve 只消费最近成功 durable revision。

输出：

- Resolved Overview；
- 最短充分因果说明；
- partial resolve；
- shared diagnostics。

不得在 UI 内实现第二套 resolver。

## 8. Publish

Publish 是 Editor-global transaction。

Preflight：

1. Editor durable state；
2. full validation / materialization readiness；
3. Production generation baseline。

Executor 必须：

```text
revision check
→ generation check
→ write
→ whole Production reread
→ verify
→ success
```

只有 reread + verify 成功才算 Publish success。

Partial / unverifiable write 不自动建立新 baseline。

## 9. 推荐实现顺序

```text
1. Fish Basic read + Species Base lookup
2. Species Base create + default Affinity ledger shell
3. existing Species Base Authoring
4. existing Compat Mode Authoring
5. Shared Template create / edit / propagation
6. Resolve
7. Publish
8. V1.0.1 fixed Compat Mode create
```

其中 1–7 构成 V1；8 不阻塞 V1 Freeze。

## 10. V1 验收最小样例

至少覆盖：

1. 选择 Fish Basic 中尚无 Habit 的 Species；
2. 用五个既有 Source / Policy 创建 Species Base；
3. 默认 Affinity 不出现在 Mode 列表；
4. 修改 Species Base 字段并 Autosave；
5. 从当前 Component 提取 Shared Template；
6. 将 Fish Source 改绑到模板并经过 Candidate；
7. Resolve 解释最终值；
8. Publish 创建 / 更新需要的 Production projection；
9. reread / verify 成功；
10. StockRelease 域可以使用默认 EnvAffinity identity，但 Habit Editor 本身没有创建任何 StockRelease 关联。

V1 不以 arbitrary Mode creation、Family、Quality、Bake 或 reconcile 作为验收前提。

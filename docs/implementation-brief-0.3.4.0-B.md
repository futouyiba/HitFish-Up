# 0.3.4.0-B 开发 brief —— 实现入口与边界

本 brief 是实现导航和依赖清单，不另定义产品契约。权威仍是本项目 Current 文档与 Owner 裁定；[审阅包](review/ui-component-contract-r2/README.md)是仓内投影。落码前回读对应 Current 小节；原取证的权威顺序为记录页 > 设计页；遇真实冲突先按来源报告，不自行调和。

**来源边界**：本次回读《编辑器持久层契约》v16（`Last Updated 2026-09-21 14:34 +08:00`），核对下列持久层入口与 Source 事务；没有重新核实其它 Current、实时 Figma 或实现代码。原 brief 的逐字取证、【画布】、【待核】及【裁定·未落页】标签见[固定基线全文](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/implementation-brief-0.3.4.0-B.md)（更早来源为其引用的 PR #10）。标签只说明当时取证，不代表今天仍未落页，也不自动成为当前已核结论。

**审查状态入口**：[OPEN-ITEMS 当前审查项](review/ui-component-contract-r2/OPEN-ITEMS.md#active-review-items)是唯一问题台账；Species Role UI 查[对应条目](review/ui-component-contract-r2/OPEN-ITEMS.md#species-role-ui)，实际画面查[图像登记](review/ui-component-contract-r2/figma-current.md#image-evidence)。本 brief 不复制动态完成状态；图像、产品依据与独立审核分别判读。

## 一、实现范围、顺序与依赖

视觉／交互依赖与 annotation 职责按[投影维护边界](review/ui-component-contract-r2/README.md#projection-maintenance)判断。

1. **先落记录与 schema**：按《编辑器持久层契约》§3.1–3.4、§3.6、§3.8 和 §5 实现物种记录、生产行台账、各自独立的 patch 与模板清单；本文件第二节保留尚无完整仓内替代的细节。序列化格式归实现线，不改变字段／类型／必填／键。
2. **打通 Structure 竖切**：按[汇编 §2](review/ui-component-contract-r2/component-contract-consolidated.md#structure-slice)与[执行卡](review/ui-component-contract-r2/contract-cards.md)实现 Species → 共享模板 → Species ADD → Affinity sourceOverride → SET／CLEAR → autosave → Resolve Preview → materialize。卡片的冻结依据和依赖在卡片文件维护，不在此复制阶段状态。
3. **接 Source 与模板传播**：Source 选择器用[汇编 §8](review/ui-component-contract-r2/component-contract-consolidated.md#source-transaction)和[卡1](review/ui-component-contract-r2/contract-cards.md#source-selector)；模板生命周期／换绑用[汇编 §14](review/ui-component-contract-r2/component-contract-consolidated.md#template-lifecycle)与卡8–12。先具备 candidate、Resolve 及 revision 检测，再连接确认提交；不得把候选当已落盘数据。
4. **按域补齐 Policy 与其它组件**：Policy 用[§9](review/ui-component-contract-r2/component-contract-consolidated.md#policy-profile)、[§10](review/ui-component-contract-r2/component-contract-consolidated.md#policy-clear)及[RoleControl](review/ui-component-contract-r2/contract-cards.md#role-control)；组件特有能力用[§12](review/ui-component-contract-r2/component-contract-consolidated.md#component-specifics)。TimePeriod Preset 的覆盖确认走[Batch Overwrite Guard](review/ui-component-contract-r2/component-contract-consolidated.md#timeperiod-batch-guard)，不能套用 Source 事务。
5. **最后验保存、物化与往返**：按[汇编 §15](review/ui-component-contract-r2/component-contract-consolidated.md#cross-layer-guards)及《编辑器持久层契约》§3.7、§6.3–6.5 验证。Production → Bootstrap → Editor → 不编辑 → Publish → Production 的逐位往返是本版验收入口；Publish 只读已成功持久化 revision。实现／图证据尚未核的部分按台账区分，不借设计包批准宣称运行通过。

## 二、记录与实现护栏

以下细节在原 brief 有明确来源，但现有仓内投影尚未逐项完整覆盖，因此保留；完整 schema 仍以所引 Current 小节为准，不能把这份摘要当字段全集。

### 1. 记录入口与保留字段

| 对象 | 完整定义／现有投影 | 本 brief 保留的实现限定 |
|---|---|---|
| Species Base Record | 《编辑器持久层契约》§3.1；整条 aggregate 与两条子结构的区分见 [RoleControl](review/ui-component-contract-r2/contract-cards.md#role-control) | `schema_version`；键 `species_key` 为物种 id，不是 name；`name_cache` 仅作比对基线、不作键、不导出。`policy_source_binding` 与 `roles` 必填，`fail_env_coeff` 为 op。组件值可空，表示该物种尚未配置。 |
| 生产行台账 | 《编辑器持久层契约》§3.2 | 每个既有 `FishEnvAffinity` 行一条、不折叠，常驻编辑器耐久层。`row_key` 为键：既有行用其行 id，新造未写回行用编辑器稳定键；`row_id` 空表示尚未写回；`species_key` 为属性，另有 `bucket`、四组件子表行标识 `refs`。 |
| 两条 row-level patch | 《编辑器持久层契约》§3.4；[RoleControl 的 Durable mutation](review/ui-component-contract-r2/contract-cards.md#role-control) | 按所引 RoleControl 实现并验收；此处只登记依赖。 |
| Numeric patch 与 Source binding | 《编辑器持久层契约》§3.3；[汇编 §3](review/ui-component-contract-r2/component-contract-consolidated.md#component-clear)、[身份边界 §16](review/ui-component-contract-r2/component-contract-consolidated.md#identity-boundaries) | numeric 的 `scope_kind` 恒为 literal `bucket`，带 `scope_kind=row` 必须由 Validator 按不合 Current Schema 报错，不静默接受。组件级 `sourceOverride` 的物理键与 authoring 粒度按 §16 分开，不把它当逐字段 patch 字段。 |
| 模板清单与别名 | 《编辑器持久层契约》§3.6；[卡8](review/ui-component-contract-r2/contract-cards.md#template-list) | `kind = TemplateKind = TEMPERATURE / STRUCTURE / FEEDING_LAYER / TIME_PERIOD / SPATIAL_OPPORTUNITY_POLICY`。`template_key` 为生产子表行标识（时段为组名）；唯一约束分别为 `kind + template_key` 或 `kind + editor_key`。别名、追溯及未物化记录的交互／展示按所引卡8。 |

底板不进生产表，Species Base Record 不含任何子表行引用。其初值导入时取配置表中该物种最频繁画像的代表行，不能初始为空；这是一次性种子，此后以编辑器为准，不是持续 Production → Editor 覆盖（《编辑器持久层契约》§3.1）。它与作者随后将某组件配置为空是两件事。

第五类模板的边界按所引定义；实现落点仍为 `FishEnvAffinity` 角色列及 `fail_env_coeff`。完整机制见[汇编 §9](review/ui-component-contract-r2/component-contract-consolidated.md#policy-profile)；identity／生命周期规则对五类一并适用（《编辑器持久层契约》§3.6、§3.10）。

### 2. 操作、引用与物化入口

- **字段操作与 CLEAR**：组件按[汇编 §3](review/ui-component-contract-r2/component-contract-consolidated.md#component-clear)、[层 × 字段 allowlist §13](review/ui-component-contract-r2/component-contract-consolidated.md#component-operation-allowlist)；Policy 按[§10](review/ui-component-contract-r2/component-contract-consolidated.md#policy-clear)；无值动作落盘例外按[§4](review/ui-component-contract-r2/component-contract-consolidated.md#field-value-control)。操作名字与行内作者显示串是两个层次，按 §4 映射，不合并；不以最终值差推断记录意图。
- **Source identity／生命周期／引用集**：完整定义在《编辑器持久层契约》§3.10；仓内动作投影为[汇编 §14](review/ui-component-contract-r2/component-contract-consolidated.md#template-lifecycle)，只读两集展示为[卡12](review/ui-component-contract-r2/contract-cards.md#reference-list)。两集定义、用途、Hard Delete 清点范围及 Policy direct refs 均在该 §14 完整投影，不在 brief 另列一份。断链来源的诊断码、加载／Publish 规则完整见[§8](review/ui-component-contract-r2/component-contract-consolidated.md#source-transaction)。
- **生产投影复用**：完整算法在《编辑器持久层契约》§3.7，lineage／同值 SET 与纯 source pin 的仓内判定见[汇编 §15](review/ui-component-contract-r2/component-contract-consolidated.md#cross-layer-guards)，空底板且 IGNORED 的合取分支见[§11](review/ui-component-contract-r2/component-contract-consolidated.md#profile-lifecycle)。

  **仍须保留的算法限定**：对每条生产行、每组件、每项，有 numeric override 取 override，否则取底板；无可复用的上游 Profile 才新增一行并写回引用；Role 有行级 override 取它，否则取物种默认。零覆盖生产行也落完整值。`SPECIES_CONCRETE` 即使无 op 也属物种自有 projection。

  编辑器使用／导出按 lineage 复用，**数据迁移另走按完整最终值复用同值行**；两套路径分开，不把迁移规则套到作者意图上。

### 3. Schema、版本与载体

《编辑器持久层契约》§3.8、§5 的实现检查项：
- 版本字段逐记录携带；不符报错，不猜、不静默升级。升级是显式的一次性迁移，旧文件由 Git 保留。
- 空文件／结构由 schema 生成；生成器拒绝覆盖已有作者数据，不提供单旗标绕过；清空必须显式双旗标。schema 与生成件有 parity 测试，未同步重生成即报错。
- 序列化格式由实现线选择；必须逐条可 diff、可人工比对与 merge、由 schema 生成且有 parity 测试。**不得将嵌套结构塞进单个单元格或单个标量字段**。这不放松字段／类型／必填／键的契约。

### 4. 原裁定中尚需独立保留的限定

下列沿用[固定基线第一节第10项](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/implementation-brief-0.3.4.0-B.md#L100-L115)的 ED-15／ED-13／ED-20，属于当时 Owner 裁定的转录。本次未重读裁定记录，不声称全部已经落 Current，也不撤销已裁内容；落码前核对应 Current。

- **ED-15**：Species Base 为主要 Authoring Truth；young／mature 是稀疏 exception scope，大部分不产生 bucket patch，不是每桶完整 Profile。

  不加钓场维；mature 内 quality 差异本期接受压平，不新增 quality override 或第三／第四 bucket；

  Bootstrap／Migration 必须报告 lossy collapse，它是 migration diagnostic，不是新 authoring dimension。

- **ED-13**：内部稳定寻址、XLSX 仍写 `targetRow.name`、重名 BLOCK 不 silent suffix 等完整边界见[汇编 §15](review/ui-component-contract-r2/component-contract-consolidated.md#cross-layer-guards)。

  保留该处未逐字列出的命名形态：`<Kind>_<Template>`／`<Kind>_<Species>`／`<Kind>_<Species>_<Bucket>`，沿用主前缀 `Cover_ / FeedLayer_ / Temp_ / period_`；已有模板 production row 直接复用；不把完整 inheritance／provenance 链塞进 name。

- **ED-20**：Role／缺 Profile 中间态／Setup 的完整机制按[Profile 生命周期](review/ui-component-contract-r2/component-contract-consolidated.md#profile-lifecycle)，记录与交互按[RoleControl](review/ui-component-contract-r2/contract-cards.md#role-control)。

  独立保留 `composeEntry` 护栏：各 lane 独立 compose／resolve，最后统一 validation；numeric base 缺失不能连带丢 Role patch、fail_env_coeff 或其它独立 durable patch。旧自动补全规则的撤回与执行顺序沿本节固定历史，不在 brief 另维护一份。

## 三、验收与证据使用

- **实现验收**：第一节的竖切、保存冲突、Resolve／物化及无编辑往返；CLEAR／同值意图按各域入口，Source 的同值 FOLLOW_PARENT 按卡1验收；Preset 按 Batch Overwrite Guard 核无覆盖／有覆盖两个分支。测试结果与设计裁定分别登记。
- **原 brief 待核事项的处置入口**：见[台账](review/ui-component-contract-r2/OPEN-ITEMS.md#brief-source-verification)。本文件不另维护动态状态；历史读数不得直接作为现行数值或验收判据。
- **Figma 核验方法**：统一引用[项目 figma-mockup-write 技能](../.claude/skills/figma-mockup-write/SKILL.md)的回读判据及 §5 分层对拍；本文件不维护第二份 API／时间戳／导出教程。原 annotation 字数、sha12 与画面取证在[固定基线附录](https://github.com/futouyiba/HitFish-Up/blob/807cef92f75e660cae820ccd48996f7e0c922e18/docs/implementation-brief-0.3.4.0-B.md#L140-L150)保留，仅证明当时该通路所读内容，不代替新取证；画布是目标态投影，不代表已实现。

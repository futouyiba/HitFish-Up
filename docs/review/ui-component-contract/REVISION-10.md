# REVISION 10 — Cross-layer Contract Closure｜Persistence × UI Topology × Figma Hygiene（2026-09-21）

本版不新增机制。目标是把本轮已经裁定并落入 Current 的内容同步回 review packet / Figma projection，关闭“Current 已变、执行包仍停在旧状态”的裂缝。

## 一、Persistence Contract closure 已回读

《编辑器持久层契约》当前已经落成：

```text
Species Base Record
key = species_key
├─ Component Recipes
└─ Species Policy Recipe
   ├─ policy_source_binding
   ├─ Role op × 4
   └─ fail_env_coeff op

AffinityAuthoringPatch
→ Component sourceOverride + numeric operationPatches

AffinityRolePatch
key = (row_key, component)
→ CLEAR | SET

AffinityFailEnvCoeffPatch
key = row_key
→ CLEAR | ADD | SET
```

边界保持：
- `Species Policy Recipe` 是 `Species Base Record` 的子结构，不是整条 Base Record 的改名；
- numeric Component patch 与 Policy patch 并列、不合并；
- numeric override = bucket-level；Role override = row-level；
- 不引入 `layer` discriminator、`scope_key="*"`、nullable generic scope 或万能 Policy patch record。

## 二、Source / Role UI topology 已冻结并落 Current

### Source

```text
前层 Source Selector
↕ same truth
Component Card Source / Template dropdown
→ Component Recipe Source binding
```

- 两处都是合法 mutation entry；
- Component Card 不是只读卡；
- Focus / Contextual Editor **不提供第三个 Source mutation selector**，只显示当前 Source 上下文并编辑逐字段 Value / Operation / Provenance / Diagnostic。

### Role

```text
Component Card Role dropdown
↕ same truth
Spatial Opportunity Policy Role row
→ Policy Authoring Truth
```

- Role 仍是 Card + Policy 双入口单 Truth；
- `fail_env_coeff` 只在 Policy 面编辑，不塞进某一 Component Card；
- Source binding 不属于 Policy payload。

上述口径已同步进《编辑器界面》与《编辑器心智模型与 IA》。

## 三、冻结卡状态恢复

`A①-卡2 Operation Control` 先前被降级的唯一理由是：其用户语言 / CXR-04 基准尚未完整落 Current。

该前提现已消失：
- ADD 基准已统一为**当前来源值**，覆盖 `SHARED_TEMPLATE` 与合法 `SPECIES_CONCRETE`；
- 层 × 字段类型四格用户语言已落 Current；
- `absent` 与 `CLEAR` 的语义区分已落 Current。

因此 `contract-cards.md` 当前恢复为：

> **批次①七张均已冻结 v1.1，可作为当前执行投影。**

不再保留“Card2 暂不作为无条件执行依据”的旧状态词。

## 四、Figma Current 与 annotation hygiene

当前主作者帧已满足 Source topology：
- `108:314 templateRow` = 前层 Source Selector；
- `108:335 componentCards` = Card 内 Source / Template 快速下拉；
- `108:495 Contextual Editor · Structure` = Focus Editor，无第三个 Source selector。

因此 `R3-FIG-01` 不需要重画 Focus Editor；正确修法是 contract text 对齐 Top/Front + Card，这一项已完成。

本轮同时清理：
- `108:335` annotation：只保留 Source / Role 当前读图规则；
- `108:364` annotation：只保留 Species default / row override 与 persistence shape；
- 删除“谁提出 / 哪轮 review / 为什么回应”等审阅留痕；
- 两组回读均为 1 条 annotation，`&` 计数 0。

`figma-current.md` §七已同步为上述 Current 摘要。

## 五、仍保留的窄 UI gap｜不在本版擅自造形

Policy 当前已经把：
- **物种层默认**
- **本行覆盖**

视觉分组分开；但物种层 Role operation 的 **`INHERIT / SET` 如何作为作者动作呈现**，Current 只定义了 durable / resolve 语义，尚未给出稳定用户交互形态。

因此本版：
- **不**擅自添加新的下拉 / chip / 用户词；
- **不**把“物种层 Role op 已有 UI”写成事实；
- 保留为窄范围 UI projection gap，后续只需裁交互形态，不重开 Persistence / Role semantics。

这不是 `R3-F-05` persistence gap 的残留；Persistence 已闭合。它是 persistence closure 后显露出的一个**纯 UI 表征问题**。

## 六、收口状态

本轮四项结果：

1. Persistence Contract：**CLOSED / READBACK PASSED**
2. Cross-page semantic consistency scan：**PASSED，发现并隔离 1 个纯 UI residual**
3. Source / Role UI topology：**FROZEN AND APPLIED TO CURRENT**
4. Figma / execution cards：**机械同步已完成；annotation hygiene 已完成；物种层 Role op UI residual 明确保留，不伪闭合**


# Fish Habit Editor V1｜Current Product Entry

> Status: V1 Product Contract Candidate  
> Scope boundary: [版本范围与阶段路线](../review/fish-habit-editor-version-scope.md)  
> Current shared semantics: [common-semantics.md](common-semantics.md)  
> Historical predecessor / evidence: [UI Component Contract R2](../review/ui-component-contract-r2/README.md)（V0.2，非 Current Authority）。

本目录承接 **Fish Habit Editor V1 的产品层 Current**：作者看到什么、如何理解对象、如何导航、哪些交互属于普通编辑、哪些需要候选预览，以及 V1 各 Surface 如何组成一个完整生产工具。

V1 当前最小生产闭环包括：从 Fish Basic 选择已有 Species，为尚无 Habit 的 Species 原子创建完整 Species Base + 系统默认 Affinity projection，然后进入同一套 Authoring / Resolve / Publish；V1 不创建新的 Species identity，也不接管 StockRelease / FishRelease 关联。

V1 当前需要的共用语义暂时与产品文档共址在 `common-semantics.md`。R2 只保留历史版本、裁定来源与证据，不再作为 V1 的最终语义解释入口。未来当这些语义稳定跨越多个版本后，再从 V1 提取到独立 common 目录。

## 阅读顺序

1. [product-contract.md](product-contract.md)  
   V1 Mental Model、IA、Workspace、Truth/Derived 边界、交互分类与 Golden Path。
2. [common-semantics.md](common-semantics.md)  
   V1 当前消费的公共语义：Source / Operation / Resolve / Policy / Validation / staged mutation / Template / Publish materialization。
3. [authoring-surface.md](authoring-surface.md)  
   Fish Subject 的核心一屏：Subject Navigation、Context Header、Component Overview、Focus Editor、Inline Field Authoring、Source Change。
4. [shared-assets.md](shared-assets.md)  
   V1 Shared Template：创建、提取、值编辑传播、引用、Archive / Restore / Replace References。
5. [secondary-surfaces.md](secondary-surfaces.md)  
   V1 的次级产品面；当前已闭合 Resolve Preview 与 Publish。
6. [implementation-brief.md](implementation-brief.md)  
   V1 最小生产闭环的实现顺序、Species Base + default Affinity 创建、Shared Template、Resolve 与 Publish 工程落点。

## Authority relationship

```text
Version Scope
    ↓
V1 Product Contract ───────┐
                          ├→ V1 Surface / Interaction Contract
V1 Common Semantics ──────┘
                          ↓
              implementation brief / Figma projection
```

- **Version Scope** 回答“V1 做什么 / 不做什么”。
- **V1 Product Contract** 回答“V1 作为一个产品如何工作”。
- **Surface Contract** 回答“具体一屏如何交互”。
- **V1 Common Semantics** 拥有当前 V1 使用的 Source / Operation / Policy / Validation / lifecycle / materialization 共用语义。R2 只作为 V0.2 历史版本与证据。
- **Implementation / Figma** 是产品 Contract 的实现与视觉投影，不反向成为产品语义 Authority。

普通修订历史由 Git / PR 保存；本目录只维护当前有效产品状态。

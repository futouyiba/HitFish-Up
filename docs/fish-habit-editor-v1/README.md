# Fish Habit Editor V1｜Current Product Entry

> Status: V1 Product Contract Candidate  
> Scope boundary: [版本范围与阶段路线](../review/fish-habit-editor-version-scope.md)  
> Low-level semantic / persistence owners remain in [UI Component Contract R2](../review/ui-component-contract-r2/README.md) until explicitly migrated.

本目录承接 **Fish Habit Editor V1 的产品层 Current**：作者看到什么、如何理解对象、如何导航、哪些交互属于普通编辑、哪些需要候选预览，以及 V1 各 Surface 如何组成一个完整生产工具。

本目录不复制已有低层 Contract。`ADD / SET / CLEAR`、Source binding、Role、Template lifecycle、Validator、Persistence shape 等底层语义继续由现有审阅包中的 canonical owner 维护；V1 产品文档只引用并投影这些语义。

## 阅读顺序

1. [product-contract.md](product-contract.md)  
   V1 Mental Model、IA、Workspace、Truth/Derived 边界、交互分类与 Golden Path。
2. [authoring-surface.md](authoring-surface.md)  
   Fish Subject 的核心一屏：Subject Navigation、Context Header、Component Overview、Focus Editor、Inline Field Authoring、Source Change。
3. [secondary-surfaces.md](secondary-surfaces.md)  
   V1 的次级产品面；当前已闭合 Resolve Preview 与 Publish，Shared Assets 在真正进入收敛时追加。

## Authority relationship

```text
Version Scope
    ↓
V1 Product Contract
    ↓
V1 Surface / Interaction Contract
    ↓
existing semantic / persistence contracts
    ↓
implementation brief / Figma projection
```

- **Version Scope** 回答“V1 做什么 / 不做什么”。
- **V1 Product Contract** 回答“V1 作为一个产品如何工作”。
- **Surface Contract** 回答“具体一屏如何交互”。
- **现有 low-level contracts** 继续拥有字段语义、持久层 token、生命周期与校验规则。
- **Implementation / Figma** 是产品 Contract 的实现与视觉投影，不反向成为产品语义 Authority。

普通修订历史由 Git / PR 保存；本目录只维护当前有效产品状态。

# 设计护栏

本目录记录跨多个机制文档都必须遵守的负向边界和防重复计权规则。

## 权威边界

- 护栏不是第二套机制规范，也不重复维护生产公式。
- 具体公式、字段、状态与生产参数仍以对应机制 Contract 为 owner。
- 本目录负责回答“哪些重复计权、偷换语义或越层结算不允许发生”。
- 若护栏与更高 Authority 或已合并的机制 Contract 冲突，以更高 Authority / 对应 Contract 为准，并在后续 PR 中修正本目录。

## 当前入口

| 主题 | 文档 |
|---|---|
| 路亚姿态响应的跨模块负向边界、重复计权与重开条件 | [路亚响应设计护栏](lure-response.md) |
| Feature → Owner 的逐项责任分配 | [Proposal C Feature Ownership Matrix](../proposals/lure-response-proposal-c-feature-ownership-matrix.md) |

普通历史推导、被否掉的公式与旧 probe 不在本目录重复保存；从 Git history / PR 查阅。
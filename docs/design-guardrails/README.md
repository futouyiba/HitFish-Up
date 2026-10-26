# Design Guardrails

本目录记录仍然有效、后续设计不应静默回退的负向设计边界。

这些材料不是 Current Contract，也不是失败方案流水账。Current Authority 仍由对应 Owner / Current 文档持有；本目录只保存已经被明确反例、Owner 边界或可执行 probe 击穿，而且具有跨局部方案复用价值的设计护栏。

一条内容进入本目录，至少应满足：

1. 已有明确反例、契约边界或可执行验证依据；
2. 重犯会造成真实的语义、数值或 ownership 错误；
3. 结论不只依赖某一版临时参数或单个 Proposal 的实现细节；
4. 能说明什么新证据出现时允许 reopen。

这里不保存：

- 仅仅“曾经考虑但没选”的备选方案；
- 已完成计划、讨论流水账或模型工作日志；
- 被新设计完全 supersede、且不再具有防回退价值的历史材料；
- 应由 Current Contract 直接拥有的现行产品规则。

使用关系：

```text
Current Contract
→ 定义现行产品事实与 Owner 边界

Design Guardrails
→ 防止重新引入已经知道会出错的设计

Proposal / Probe
→ 探索尚未冻结的解法
```

## 当前入口

| 主题 | 护栏 |
|---|---|
| 路亚 Feeding / Interaction Response | [Lure Response Guardrails](lure-response.md) |

新增或修改 Guardrail 时，应保留其依据、影响与重开条件；不能把 Working 建议静默升级为 Current Rule。

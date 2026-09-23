# Authoring Archetype Clustering Probe

本目录是独立的 FCF / 中鱼机制 0.3.4 数据验证 Prototype，不修改 Runtime、Bake DSL 或正式 Editor。

## 结论先行（当前状态）

**数据已足够做全量字段级 Probe，但不足以宣称正式生产 Archetype。** 飞书 V3 鱼总表表格 2 实测有 267 条完整行、温度/8 时段/3 水层/推荐结构等字段；然而这些字段是源表策划参考/派生数据，不是已经 Resolve 成 0.3.4 `ResolvedBakeSubjectConfig` 的生产配置。四类输入中，结构推荐是标签集合而非正式约 25 类 `StructureType` affinity，时段仍为旧 8 档（0.3.4 要求 5 档且明确不自动迁移），温度字段缺少 `falloff_shape` 与逐鱼 `temp_threshold` 的正式配置口径。因此本 Probe 对转换部分标记 `DERIVED`，不能作为 Current 配置写回。

## 运行

```bash
python3 prototypes/authoring-archetype-clustering/scripts/clustering.py
```

输出：

- `outputs/metrics.json`：数据覆盖、距离、压缩曲线、ARI/NMI、outlier 与 authoring proxy
- `outputs/metrics.csv`：压缩曲线表
- `outputs/cases.md`：3 个稳定 cluster、2 个边界 cluster、3–5 个 outlier 的回读
- `outputs/cluster_assignments.csv`：每条鱼的 component/joint cluster 和异常信息
- `report.md`：最终中文报告

## 数据来源

- `data/raw/feishu_v3_selected_fields.csv`：飞书表格直读，267 行 × 34 列，来源字段；由本任务调查导出。
- `data/raw/fish_reference_267.csv`：Notion 公共资料库 2026-09-08 snapshot 的 267 条辅助字段。
- `data/raw/fish_db_page{1,2,3}.json`（Notion 库原始导出）**不随公开仓分发**：含内部页面 id，按公开仓红线（Owner 2026-09-23 裁定）已移出公开树；如需从原始导出复现 `fish_reference_267.csv`，须另行提供授权/脱敏数据。脚本对缺失的输入会显式退出并说明原因，不会静默产出。

源表/参考资料均保留 provenance；空白不是 0。除非文件明确写 `SOURCE-LINKED`，不要把推导结果当正式 0.3.4 配置。

## 方法摘要

1. Temperature：按 0.3.4 Core Spec 的 `range_fit` 计算 0–40°C / 0.5°C 网格 Effect Signature；acceptable 边界来自源表，comfort 区间由最喜欢温度推导（规则见 `input_schema.md`）。
2. Structure：`FG推荐结构体` 多选集合转为 53 维 presence signature；这是结构标签相似度，不是正式 `StructureType × float` affinity。
3. Time：8 个 `period*` 源表系数归一到最大值；同时报告“源表 8 档”而非伪造 5 档 Contract。
4. Feeding Layer：`表层/中层/底层亲和系数` 1–10 归一到 0–1；它是源表数值，但其与 0.3.4 affinity scale 的对应关系仍需确认。
5. `D_component` = Signature 各维平均绝对差；`D_joint` = 四组件等权平均（本 Probe 的透明 proxy）。
6. Hierarchical average-linkage cuts + deterministic greedy radius cover；补充 PAM-style k-medoids用于固定 K 对照。
7. 压缩曲线的 `epsilon` 是平均 effect/affinity 差；覆盖表示距某个 archetype medoid 不超过 epsilon。它不是抽象 ML score，可回溯至每个 Signature 维度。

## 重要边界

- 不使用自然生物学 Family 命名，不把 cluster 名当 Runtime identity。
- 不强行指定 K；重点看允许误差到覆盖率的曲线和 override 成本。
- `Archetype` 在本 Probe 中仅表示一次性 Starter Recipe 候选，不表示持续继承。
- 因为没有真实 0.3.4 Species Shared / FishQuality / Engagement Mode 配置、ResolvedBakeSubjectConfig 和 BakeInputSnapshot provenance，本结果不能证明正式机制已准备好。

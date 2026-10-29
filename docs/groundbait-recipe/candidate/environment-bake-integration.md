# 环境烘焙与空间分布权重接入

> 状态：Candidate / Working Design
> 日期：2026-10-29
> 边界：本页只说明窝料与中鱼候选如何消费环境烘焙结果，不复制、改写或补造 Fixed Bake Current Contract。

## 1. 为什么先推这一段

空间侧是响应和圆桌的上游。如果先写窝料或响应，再回头补环境权重，很容易把同一环境事实算两次，或者把 `SpatialDistributionWeight` 当成概率使用。

本页只固定三件事：

- 环境事实经过什么结构变成空间分布权重；
- 哪些量可以被下游读取；
- 哪些量不能被下游重新计算或改写。

## 2. 已验证的结构

以下结构来自仓内术语与总图，是 Current 术语层的事实：

```text
环境实体 / 地形 / 材质
  → 原始条件 Raw Condition
  → 派生条件 Derived Condition
  → 因子 Factor
  → 环境习性组件 Environment Component
  → 门控结果 GateResult / 适配值 Fit
  → 通道聚合
  → 中鱼习性模式空间结果
  → 派生环境场 DEF
  → 空间分布权重 SpatialDistributionWeight
```

关键定义：

- `SpatialDistributionWeight = Base Weight × FinalEnvCoeff`，仍未归一化，不是概率。
- `DEF` 按条件组归并，不按每个空间坐标重复保存。
- 条件组下的结果属于中鱼习性模式，不直接属于单条鱼。
- `Base Weight` 只在这个乘法中出现一次。

出处：`docs/terminology.md` §2.1、§2.2、§3.1、§4、§5.1；`fcf-system-map/README.md` §1、§2。

## 3. 可执行参考与 Current 的区别

仓内 `reference/0340-fixed-bake/` 提供可运行的 Fixed Bake 参考，用于验证结构和 golden 读数。它是 REFERENCE / VALIDATION，不是生产实现，也不是本仓 Current Contract 本体。

使用时必须：

- 记录具体 `contract_ref`，不能只写 `main`；
- 把参考公式和 golden 当作证据，不当作生产参数；
- 发现实现与 Current 冲突时，先按 Current，再在实现仓开 issue 或发起契约修订。

出处：`docs/authority-model.md`、`reference/0340-fixed-bake/README.md`、`docs/implementation-readiness.md`。

## 4. 下游可以读什么

以下内容可以进入响应或圆桌：

| 量 | 读取方 | 用途 | 限制 |
|---|---|---|---|
| `SpatialDistributionWeight` | 响应、圆桌 | 候选权重的空间侧输入 | 不重新乘 `Base Weight`，不提前归一化 |
| `DEF` 条件组结果 | 响应、圆桌 | 查询当前地点对应的模式结果 | 只读，不写回 |
| 模式空间结果 | 响应 | 模式级候选权重 | 不把模式结果当成鱼种最终概率 |
| Fish Condition（若 DEF 携带） | 响应 | 鱼况条件输入 | 更新公式归对应机制，不由窝料写 |

## 5. 下游不能做什么

1. 不在响应阶段重新计算环境系数。
2. 不把 `SpatialDistributionWeight` 和 `Base Weight` 再乘一次。
3. 不把 DEF 当作可随意修改的运行时对象。
4. 不把条件组级权重当成坐标级权重；逐地点差异应通过派生条件表达。
5. 不把参考 golden 升级为生产参数。
6. 不自行裁决 `fail_env_coeff` 与 `envCoeffMin` 的口径漂移。

以上第 6 项对应 `docs/terminology.md` §3.1 与参考实现之间的命名差异，已登记在 `decisions/conflict-register.md`。

## 6. 当前未决项

- `SpatialDistributionWeight` 的 Current 归属页仍未登记。
- Fixed Bake 的 Current 契约本体不在本仓 Markdown。
- `fail_env_coeff` 与 `envCoeffMin` 的适用范围需要 Owner / Current 收口。
- DEF 是否同时携带 Fish Condition，以及按什么键保存，仍待对应 Contract 确认。

## 7. 最小结构反例

- 同一温度既进环境系数又进 Fish Condition，且两处都乘最终权重：重复计权。
- 响应阶段重新乘 `Base Weight`：基础权重被计算两次。
- 参考 golden 被写进生产配置：证据被当成参数。
- 条件组权重被当作坐标级权重：空间分辨率错误。
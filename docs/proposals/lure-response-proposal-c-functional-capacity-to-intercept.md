# Proposal C｜Functional Capacity → Intercept Capacity

状态：Superseded Working。仅保留历史索引，不代表当前 Proposal C 推荐结构。

本页原路线尝试用：

```text
FunctionalCapacity
→ LocomotorCapacityRetention
→ EffectiveInterceptCapacity
```

承接动态 Fish Condition 对 Closing 的影响。

该路线已被后续设计替代。当前 Proposal C 不再把 `FunctionalCapacity` 作为必要 Bake 输出，也不再让动态 Fish Condition 修改物种/体型决定的物理追赶上限。

当前结构见：

- `lure-response-proposal-c-activity-bake-contract.md`
- `lure-response-proposal-c-activity-closing-ownership.md`

当前推荐主链：

```text
species × size cohort config
→ InterceptSpeedLimit
→ hard Closing feasibility

Fish Condition Bake
→ Activity
→ physically-feasible Closing 的 soft-cost multiplier

Fish Condition Bake
→ FeedingMotivation
→ WillingnessThreshold
```

原文仍可从 Git history 查阅，用于理解为什么放弃 `FunctionalCapacity → speed limit` 路线。

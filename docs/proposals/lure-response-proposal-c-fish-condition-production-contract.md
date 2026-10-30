# Proposal C｜鱼况（Fish Condition）生产契约（Candidate）

状态：Working Contract Draft / Candidate。按 2026-10-30 Owner 裁定（Issue #161）编写，尚未审核合并，不冒充 Current Contract。

本文只定义 Fish Condition 的载体、状态、来源与校验；各 Condition 的生成语义、曲线与标定仍归对应机制 Contract。

## 1. 架构

```text
各 Condition 机制 Contract
→ 语义、合法 cause、curve / reducer、标定依据

Bake
→ 统一执行、物化 baseline、校验

DEF / ConditionGroup × EngagementMode
→ Fish Condition Baseline block

可选 Runtime Overlay
→ 仅被明确授权的 Condition
→ 当前只有 Wariness 有语义依据；V1 可暂不实现

Baseline + authorized overlay
→ resolved Fish Condition

Response / 其它消费者
→ 只读
```

## 2. 键与载体

Fish Condition baseline 存在 DEF 的条件组下，不另开独立表。

```text
Block key = ConditionGroupId × EngagementModeId
DietShift 额外按 preyFamily 分项
```

Block 必须声明版本、生成时刻与有效期；不同版本的 block 不能拼接使用。

## 3. Block 结构

```text
FishConditionBlock {
  key { conditionGroupId, engagementModeId }
  version
  producedAt
  validity { from, to }
  source { bakeRunId, inputs[] }
  status
  conditions {
    activity        { value, status, sourceRef }
    feedingMotivation { value, status, sourceRef }
    wariness        { value, status, sourceRef, layer }
    dietShift       { [preyFamily]: { value, status, sourceRef } }
  }
}
```

`layer` 区分 `baseline` 与 `overlay`；`overlay` 不写回 DEF，只在消费前与 baseline 合成 resolved 值。

## 4. 值与范围

| 字段 | 范围 | 说明 |
|---|---|---|
| Activity | 有限、非负 | `1.0` 是 Working reference，不是默认值；不设语义上界 |
| FeedingMotivation | `[0,1]`（Candidate 域） | 0.5 是参考锚，不是 fallback |
| Wariness | `[0,1]`（Candidate 域） | 仅表示鱼侧警觉；不是 SuspicionLoad |
| DietShift[family] | 与 FoodValue 同标尺的有符号偏移 | 只影响对应 family；无全局分量 |

范围之外的值按 `InvalidInput` / `Unknown` 处理，不截断后继续用，见第 6 节。

## 5. 状态

| 状态 | 含义 |
|---|---|
| `Resolved` | 值、来源、有效期齐全，可直接消费 |
| `Unknown` | 必要事实缺失、过期、越界或无来源 |
| `NotConfigured` | 该 Condition 或 family 没有适用规则 / 配置 |
| `ResolutionIncomplete` | 归约阶段仍不能形成最终值 |

规则：

- 每个值独立带状态；一个字段 `Unknown` 不抹掉其它已知字段；
- block 的 `status` 只作汇总提示，最终是否可消费由消费方按自己需要的字段判断；
- 不引入 `stale-but-usable`；过期即 `Unknown`。

## 6. 解析规则

```text
resolved(condition) =
  baseline.value          status = Resolved，且无 overlay 或 overlay 已过期
  baseline + delta        overlay 被授权、在有效期内、结果在范围内
  Unknown                 baseline 过期 / 越界 / 缺来源
  InvalidInput            overlay 指向未授权 Condition，或合并结果越界
```

- overlay 必须声明来源、适用区间与规则版本；
- overlay 只能修改被机制 Contract 明确授权的 Condition；越权 overlay 是配置错误，标 `InvalidInput`，不能静默应用；
- 过期 overlay 回落到 baseline，不沿用旧增量；
- 当前只有 Wariness 具备 runtime 语义依据；V1 可只消费 baseline；
- Response 不得写回任何 Fish Condition。

## 7. 写入者与消费者

| 角色 | 权限 |
|---|---|
| Bake | 写 baseline；负责执行、物化与校验 |
| Wariness Runtime Overlay | 仅在机制 Contract 授权后写 overlay |
| Response | 只读 resolved 值 |
| Groundbait / Feeding Event | 不写 Fish Condition；如需消费 Wariness，必须有自己的消费者语义，不能沿用 Risk 的权限 |
| Roundtable / Candidate | 只读，不反向修改 |

## 8. 校验

- 字段值必须有限、在范围内、带来源与有效期；
- `version`、`validity`、`source` 缺失即不可用；
- 不允许用 SKU、饵体积、速度、转向、`1 - prey_support` 等代理字段填充；
- 不允许在 Unknown 时回填 1.0、0.5 或最后值；
- block 校验失败时整块标为不可用，而不是部分字段静默降级。

## 9. 与 main 的待对齐点

`main` 的窝料端到端 Candidate（`docs/groundbait-recipe/candidate/end-to-end-algorithm.md`）有三处需要按 #161 重新核对，尚未在本分支改写：

1. §4 对任意 `[0,1]` 状态使用通用一阶 runtime 更新；#161 只授权 Wariness，且 Activity 不在 `[0,1]` 上界内；
2. §8.2 的 `w_wary × Wariness` 让 Feeding Event 直接消费 Wariness，属于新的 consumer 语义，不能用 Risk 的权限顺带继承；
3. §9 的 `w_*` 加权和、顶层 `EIO` 项与 sigmoid 投影不是 Proposal C 已闭合的五评价项公式，只能作为 Groundbait 自己的 Candidate 接口。

这些点在 main 侧核对前，不进入 Proposal C 的规则。

## 10. 未决

- 各 Condition 的机制 Contract 与曲线；
- Wariness overlay 的事件、粒度、衰减、有效期与会话边界；
- DEF block 的序列化与版本迁移；
- 各 Condition 的 TTL 与刷新频率；
- `TackleConspicuousness` 的字段与 owner（已后置）；
- main 窝料文档的三处对齐。

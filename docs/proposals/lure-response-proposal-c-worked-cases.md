# Proposal C｜工作案例

状态：Working Design / Candidate。以下案例用于检查语义契约，不是生产标定结果。

## 1. 同一呈现支持两种解释

**事实：** 一件裙丝 Jig 加鱼形 T 尾，鱼形轮廓可见，实际运动接近底部并有局部展开变化。

**应得结果：**

- 小鱼解释保留鱼形证据；
- 小龙虾解释保留近底和局部动态证据；
- 两套解释读取同一份实际记录；
- TemporalOpportunity owner 使用同一 `presentation_segment_id`、局部机会窗口和 Feeding route 创建一条机会记录，并在 sibling 聚合前去重；
- 两套解释不生成两次独立机会；
- 食物偏好不改变猎物解释。

**反例：** 仅因为鱼更爱吃小鱼，就把同一呈现改写成小鱼身份。该推导不成立。

## 2. 缺失历史不等于停留

**事实：** 记录从低位移开始，前面没有有效轨迹。

**应得结果：**

```text
current_state = low_displacement
prior_movement = Unknown
move_to_pause = Unknown
```

不能把记录起点当作移动结束，也不能给停留增加额外 bonus。

## 3. NoMatch 与 Unknown

**事实 A：** 小龙虾近底规则已配置，所需数据完整，但近底条件不成立。

**结果：** `NoMatch` 或规则定义的零结果。

**事实 B：** 小龙虾近底规则已配置，但局部展开记录缺失，缺失可能改变匹配程度。

**结果：** 支持区间或 `Unknown`，不能写成零。

## 4. Poor 与 Reject

**事实 A：** `CurrentFoodValue=0`，Motivation 极高，合法 Trigger 达到上限，负担接近零。

**结果：** Poor 可以进入窄的弱响应窗口。

**事实 B：** `Reject`，其他条件相同。

**结果：** typed hard zero，不能复活。

## 5. 同一 sudden turn 的双路消费

**事实：** 呈现发生一次突然改向。

**结果：**

```text
prey-state evidence → StateTriggerValue (+)
prediction disruption → PredictionCost (-)
```

两条路径可以同时存在，因为它们回答不同问题。不能再加一个 generic erratic bonus 或 penalty。

## 6. Unknown sibling 的替代聚合

**事实：**

```text
baitfish response = 0.45
crayfish response = Unknown
```

**结果：**

- 若小龙虾允许的上界高于 0.45，保持 `ResolutionIncomplete`；
- 若小龙虾上界已被证据压到不超过 0.45，才可输出 0.45；
- 不把 Unknown 当作 0 后直接输出 0.45。

## 7. 时间机会

**事实：** 两次呈现的瞬时响应相同，第二次在有效局部机会中持续更久。

**结果：** 第二次 accumulated opportunity 可以更高。

**限制：** 停留时长不直接增加 `DecisionMargin`，也不产生 `DwellBonus`。如果 exposure 未配置，结果是 `ResolutionIncomplete`，不是零机会。

## 8. Closing 的职责

**事实：** 饵相对潜在鱼的水平径向远离速度提高。

**结果：** ClosingCost 增加，可能降低 DecisionMargin。

**限制：** 在没有 encounter geometry、reaction window 等 owner 时，不能仅因 `u_close >= 1` 宣称整个交互不可能，也不能把高速自动写成 SuspicionLoad。

## 9. 装配变化与记忆

**事实：** 呈现过程中更换拖尾。

**结果：**

- 新装配重新绑定证据；
- 仅与旧装配绑定的局部计时和事件失效；
- 同一主体的共用轨迹是否可保留，按规则决定；
- 不把旧装配的猎物解释和状态事件直接带入新装配。

## 10. 设计案例的验收方式

每个案例必须记录：

```text
facts
→ applicable rule
→ intermediate state/value
→ final status/value
→ forbidden alternative
```

案例只验证语义区分和状态传播，不证明生产参数、现实鱼类行为或最终玩法效果。

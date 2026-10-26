# 方案 C｜Step 4 Probe：大口黑鲈 × 小型饵鱼

日期：2026-10-26  
状态：Working Probe，不是 Current，不规定最终 response aggregation。

## 1. 本轮只问一个问题

固定：

- Fish：大口黑鲈（Largemouth Bass / Micropterus salmoides）
- Prey interpretation：小型饵鱼
- Step 2 prey support：相同，例如 0.90
- 基本环境与鱼的内部状态：相同

只改变 Step 3 的呈现状态：

A. 持续移动  
B. 移动后停留  
C. 下落，并可选带有“失衡样下沉”线索

目标不是决定哪一个“更好”，而是检查这些状态究竟应该改变 Step 4 的什么。

## 2. 先排除一个错误抽象：State Bonus

不要建立：

```text
response = preySupport × stateBonus × motivation × ...
```

原因：Step 3 的状态不是同一种因果量。

- 当前速度、鱼饵相对位置会改变捕获任务；
- 侧翻姿态可能只是 target / vulnerability cue；
- “移动后停留”只是时序关系，本身未证明有独立作用；
- feeding motivation 是鱼的内部状态，不应由饵刚刚停下来重新创造。

因此 Step 4 必须先按因果角色路由，再决定是否进入某个 Complete Response Mode。

## 3. 第一轮路由结果

| Step 3 信息 | 首选去向 | 当前判断 |
|---|---|---|
| 当前世界速度 / 相对鱼速度 | TaskDemand | 直接影响追赶、截获、定位要求 |
| 当前鱼-饵距离 / 相对几何 | TaskDemand | 决定需要多少 reposition / closing |
| 方向变化、垂直移动 | TaskDemand | 只有确实改变捕获动作要求时进入 |
| 当前低位移 | TaskDemand | 通过降低当前运动要求起作用，不另加“停顿奖励” |
| recent_move_then_pause | Explain / Candidate Mechanism | 默认不加分；只有证明存在独立的 attention / trigger 机制才进入 valuation |
| burst_then_pause | Explain / Candidate Mechanism | 同上；不能仅因被识别就奖励 |
| imbalance_like_sinking | Target / Valuation Candidate | 可作为“易损/异常样呈现”的证据候选；不能自动等价于真实受伤 |
| 实际下沉速度 | TaskDemand + Geometry evolution | 它是真实运动；与侧翻 cue 分开结算 |
| prey support 0.90 | Target interpretation input | 保持原值，不乘进每个状态字段 |
| fish feeding motivation | Interaction 内部状态 | 来自 fish current context；不是 Step 3 输出 |

## 4. 三个受控案例

### A. 持续移动

假设小型饵鱼支持仍为 0.90，当前呈现持续以较高速度移动。

Step 4 首先看到的是更高的捕获任务要求：鱼需要完成更大的 closing / interception / positioning。大口黑鲈的 prey capture 本身包含明显的 locomotor positioning，并能随 prey capture condition 调整 ram / suction 与接近运动。

因此首轮语义：

```text
prey support = unchanged
food identity/value = unchanged unless other evidence changes
TaskDemand = higher than otherwise-same paused case
feeding motivation = unchanged
```

是否最终 response 更低，不能仅凭“运动更快”断言；如果鱼的 FunctionalCapacity 足够，可能仍是 Feasible，只是 demand / cost 不同。

### B. 移动后停留

当前实际速度已经进入低位移状态。

首轮不要做：

```text
recent_move_then_pause => +30% response
```

已经有一个足够直接的因果变化：当前捕获任务变容易，追赶 / 截获要求下降。

因此先结算：

```text
lower current motion
→ lower TaskDemand
→ compare with same ResolvedFunctionalCapacity
→ TaskAffordance may improve
```

`recent_move_then_pause` 暂时保留为 Explain / Candidate Mechanism。只有未来证据证明“刚刚运动后停住”相对于“同样速度、同样位置、但已经静止很久”仍会稳定改变大口黑鲈的攻击倾向，才 admission 一条独立的 temporal valuation mechanism。

这提供了一个很干净的未来 ablation：

```text
B1 刚停 0.2 s
B2 已静止 5 s

保持当前速度、位置、prey support、fish state 全部相同。
若 B1 / B2 没有可靠 ranking difference，recent_move_then_pause 不获得独立数值自由度。
```

### C. 下落 / 失衡样下沉

这里必须拆成两个事实：

1. **实际下沉运动**：改变鱼饵未来位置、相对距离和截获几何，因此属于 TaskDemand / geometry evolution；
2. **持续侧翻等失衡样线索**：可能让鱼将其解释为更易损的 prey presentation，但这是 valuation candidate，不是物理捕获难度本身。

不能写成：

```text
imbalance_like_sinking = injured = easier = +response
```

因为这连续跨了三次尚未证明的推断。

首轮更安全的结构是：

```text
actual sinking motion
    → ResolvedTaskDemand

imbalance-like cue
    → candidate vulnerability interpretation
    → only if supported: Feeding-mode valuation effect
```

如果最终发现“侧翻”除了已经由真实速度 / 轨迹表达的捕获任务之外，并没有独立且稳定的玩家策略效果，就删除 valuation 分支，只保留 Explain。

## 5. Step 4 最小结构

这一轮不建立一个新的 universal scalar pipeline。按照当前 Interaction Contract，建议只保留下列概念关系：

```text
Step 2 Target / Prey interpretation
+ Step 3 current presentation facts
+ fish-relative geometry
+ ResolvedFunctionalCapacity
        ↓
ResolvedTaskDemand
        ↓ compare
TaskAffordance
  = Feasible | Constrained | Infeasible(reason) | Unknown

同时：
Target / prey value
+ optional evidence-backed vulnerability / opportunity valuation
+ current fish-side Feeding motivation
        ↓
Feeding-mode Valuation

TaskAffordance + Feeding-mode Valuation + Perception / Target outcome
        ↓
Complete Feeding Response Mode
        ↓
C_mode
```

这里只规定语义角色，不规定三项必须相乘，也不规定它们一定各自输出 scalar。

## 6. 第一轮最小 TaskDemand，不要过度参数化

暂时不要马上建立 speed / acceleration / turn / vertical / pursuit stamina 五六维向量。

优先从能够制造 ranking reversal 的最少变量开始：

1. **fish-to-target geometry**：距离与相对位置；
2. **relative motion demand**：当前需要鱼进行多少 closing / interception；
3. **必要的 maneuver / vertical reposition**：只有案例证明单靠前两项无法解释差异时再 admission。

Fish 侧同样不直接配置一堆“最大速度”。先由现有 ResolvedFunctionalCapacity 与具体 TaskDemand 比较；只有某个能力维度能独立决定 Feasible / Constrained / Infeasible，才增加 DOF。

## 7. 外部证据怎样支持、又不支持本设计

现有生物力学研究支持以下较弱但可靠的结论：

- 大口黑鲈捕食需要主动 locomotor positioning；
- 面对 evasive 与 non-evasive prey，其 capture kinematics 会改变；
- 感知条件改变时，它们也会调整 ram / suction feeding modality；
- 因此 prey motion / geometry 进入 TaskDemand 是合理的。

这些研究**不直接证明**：

- 路亚“停顿”应该获得固定 bonus；
- “移动后停留”拥有独立的吸引系数；
- 侧翻软饵必然被理解为受伤鱼；
- 某个速度阈值应是多少；
- 最终 response 应采用乘法、加法或其它固定公式。

参考入口：

- Higham 2007, *Feeding, fins and braking maneuvers: locomotion during prey capture in centrarchid fishes*, J Exp Biol, doi:10.1242/jeb.02634
- Holzman et al. 2014, *Modelled three-dimensional suction accuracy predicts prey capture success in three species of centrarchid fishes*, PMCID: PMC4006267
- Gardiner & Motta 2012, *Largemouth bass switch feeding modalities in response to sensory deprivation*, PMID: 22285791

## 8. 下一组真正有信息量的验收案例

Step 4 下一轮不要扩大鱼种，先攻击以下反事实：

### Q1 当前速度反转

同一大口黑鲈、同一距离、同一 prey support：

- Q1a target 速度低；
- Q1b target 速度高到刚好让捕获任务进入 constrained；
- Q1c 再高到超过当前 FunctionalCapacity。

目标：验证 TaskAffordance 是否能自然形成 Feasible → Constrained → Infeasible，而不需要“快饵惩罚系数”。

### Q2 刚停 vs 久停

当前所有物理状态完全相同，仅 temporal history 不同。

目标：攻击 `recent_move_then_pause` 是否真的需要独立作用。默认预期是**没有额外作用**，除非证据或体验目标证明 ranking reversal。

### Q3 同样下沉，姿态不同

下沉速度、位置、prey support 相同：

- Q3a roll 0°；
- Q3b roll 75°。

目标：如果两者 TaskDemand 相同，那么任何差异都必须明确来自 target / valuation interpretation；不能再伪装成 capture feasibility。

这三组通过后，再决定 Step 4 是否需要新增独立 `Vulnerability` 语义，还是 `Actual motion → TaskDemand` 已经购买了大部分需要的表达能力。
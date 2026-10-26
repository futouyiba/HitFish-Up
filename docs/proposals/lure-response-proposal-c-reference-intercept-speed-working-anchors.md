# Proposal C｜ReferenceInterceptSpeed Working Anchors

状态：Working Calibration Seed / Candidate。不是 Current，不是生产参数。

## 1. 结论

第一版先不直接冻结三个 locomotor archetype 的绝对 `m/s`，而是相对于一个项目内可测的 Normal Steady reference lure speed 建立无量纲 calibration anchor。

定义：

```text
V_ref
= 选定 Normal Steady reference lure basket
  的 horizontal water-relative speed 中位数
```

在 reference fish length、reference Activity 下，Working seed：

```text
HighClosing    q_ref = 0.45
GeneralClosing q_ref = 0.65
LowClosing     q_ref = 0.90
```

其中：

```text
q_ref = V_ref / ReferenceInterceptSpeed
```

所以等价的 speed anchor 为：

```text
HighClosing
ReferenceInterceptSpeed ≈ 2.22 × V_ref

GeneralClosing
ReferenceInterceptSpeed ≈ 1.54 × V_ref

LowClosing
ReferenceInterceptSpeed ≈ 1.11 × V_ref
```

这些比例只是一组用于联合标定 Closing 的 Working seed，不宣称对应真实鱼类绝对游速。

## 2. 为什么先用相对 anchor，而不是直接写 m/s

当前仓内尚无生产 lure telemetry 能证明 Normal Steady 的绝对 horizontal water-relative speed 分布。

若现在直接写：

```text
GeneralClosing = 1.8 m/s
```

这个数字会同时混入：

- lure motion implementation；
- reel / rod 操作速度；
- water-relative reference frame；
- fish locomotor calibration。

因此第一版先把鱼侧能力相对于项目自身的 reference presentation 定标：

```text
project lure-speed telemetry
→ V_ref
→ q_ref target
→ ReferenceInterceptSpeed
```

等生产 telemetry 可用后，再把上述比例解析成绝对 `m/s`。

## 3. 为什么选择 0.45 / 0.65 / 0.90

这组值不是按等距美学选择，而是为了满足已有 lure-speed basket 的行为要求。

### Normal Steady

```text
HighClosing    q = 0.45
GeneralClosing q = 0.65
LowClosing     q = 0.90
```

三档都仍低于 hard feasibility boundary `q=1`，但 LowClosing 已明显接近边界。

这样 Normal Steady 不会把 LowClosing 直接普遍打成 hard-zero，同时能让三档 Closing burden 明显分离。

### Slow，示例取 0.5 × V_ref

```text
HighClosing    q = 0.225
GeneralClosing q = 0.325
LowClosing     q = 0.450
```

三档都应保持低 Closing burden，支持“慢下来可以恢复弱追赶鱼种 response”的策略故事。

### Fast Search，示例取 1.5 × V_ref

```text
HighClosing    q = 0.675
GeneralClosing q = 0.975
LowClosing     q = 1.350
```

于是：

- HighClosing 仍主要处于 soft-cost 区；
- GeneralClosing 已非常接近能力边界；
- LowClosing 开始出现 angle-local hard-infeasible。

在 Isotropic2D 下：

```text
LowClosing @ q=1.35
P_hard ≈ 0.234
```

### Burst Peak，示例取 2.0 × V_ref

```text
HighClosing    q = 0.900
GeneralClosing q = 1.300
LowClosing     q = 1.800
```

在 Isotropic2D 下：

```text
GeneralClosing @ q=1.30
P_hard ≈ 0.221

LowClosing @ q=1.80
P_hard ≈ 0.313
```

这符合当前 basket 目标：Burst 不造成 whole-mode hard-zero，但不同 locomotor archetype 的局部不可行比例明显分开。

## 4. 与 K_close 的联合 seed

当前 combined-burden stress test 为 ordinary Closing 预留的参考量级约为 `0.08`。

在：

```text
Isotropic2D
reference Activity multiplier = 1
GeneralClosing q_ref = 0.65
```

且 `q<=1` 时：

```text
E[u_close²] = q² / 4
```

若令：

```text
E[ClosingCost] ≈ 0.08
```

可反推 Working：

```text
K_close ≈ 0.76
```

该值只用于这一组 seed 的联合 sanity check，不是 production 参数。

在同一个 `K_close≈0.76` 下，Normal Steady 的 reference average Closing burden 约为：

```text
HighClosing    ≈ 0.038
GeneralClosing ≈ 0.080
LowClosing     ≈ 0.153
```

这形成清晰的三档 separation，并让 GeneralClosing 正好落在 ordinary reference burden 附近。

## 5. Fast / Burst 下不要只看平均 cost

一旦 `q>1`，部分 bearing 进入 hard infeasible：

```text
u_close(theta) >= 1
→ C_conditional(theta) = 0
```

因此 Fast / Burst 的诊断不能只把 `q²/4` 延伸过去。

至少同时记录：

```text
hard_infeasible_share
E[C_conditional]
E[ClosingCost | feasible]
Good response retention
Preferred response retention
```

不能把 hard-zero bearing 重新折算成更大的 soft ClosingCost。

## 6. 这组 anchor 不拥有的语义

这些值不表达：

- Activity；
- sustained pursuit duration；
- acceleration capability；
- maneuverability；
- Prediction；
- Wariness；
-真实鱼类最高游速。

`ReferenceInterceptSpeed` 仍只表达 Proposal C 当前模型中的结构性短时 Closing 边界。

## 7. 何时允许改这三个 q_ref

拿到生产 telemetry 后，应以真实 basket 重算：

```text
lure family × regime
→ horizontal water-relative speed distribution
→ q distribution by archetype / cohort
```

若发现：

- Normal Steady 下 GeneralClosing 大量接近 `q>=1`；
- Fast Search 下 HighClosing 与 GeneralClosing 几乎无 separation；
- Slow 下 LowClosing 仍大量高 burden；
- Burst 下所有 archetype 都几乎同样 hard-zero；

则优先调整 archetype anchor 或 reference basket，不用 `K_close` 去修正错误的 hard-feasibility ordering。

## 8. 生产化前的最低验证

至少需要：

1. 确定 Normal Steady reference lure family；
2. 取得 `V_ref` 的真实 horizontal water-relative telemetry；
3. 把三个相对 anchor 转成绝对 `m/s`；
4. 跑 Slow / Normal / Fast / Burst basket；
5. 检查 hard-infeasible share 与 Good / Preferred retention；
6. 再结合 Activity multiplier 做 full Closing calibration。

Activity multiplier 的具体实现与参数由其独立 owner / Cowork 工作流承接，本页不修改 Activity contract。

## 9. 当前 Working seed 汇总

```text
RelativeBearingPrior = Isotropic2D

HighClosing    q_ref = 0.45
GeneralClosing q_ref = 0.65
LowClosing     q_ref = 0.90

ReferenceInterceptSpeed / V_ref:
HighClosing    ≈ 2.22
GeneralClosing ≈ 1.54
LowClosing     ≈ 1.11

K_close sanity-check seed ≈ 0.76
```

本页只建立一组联合 calibration seed，用于后续 probe / telemetry 对照；不把这些数字晋升为 Current 或 production authority。

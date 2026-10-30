# Proposal C｜Vertical Motion Ownership

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

Proposal C 第一版继续保留 Horizontal2D Closing，不把垂直速度强行并入 `u_close`。

职责切分：

```text
vertical position / rise / fall
→ Spatial / Opportunity eligibility
→ valid vertical encounter window
→ exposure duration / opportunity amount

horizontal relative lure motion
→ latent horizontal bearing
→ radial separation load
→ ClosingCost
```

因此 vertical jigging、rapid lift、rapid fall 等 presentation 的垂直运动，不通过一个虚构的 3D fish bearing 进入 Closing；它主要通过“多久处在可发生 interaction 的垂直区域”影响机会量。

当前仓未找到已合并 Current Markdown Contract 明确拥有这一 vertical opportunity seam，因此这里只冻结 Response 的边界，不补造生产公式。

---

## 2. 为什么不直接改成 Isotropic3D

如果改为：

```text
latent fish direction ~ Isotropic3D
```

并让完整 3D lure velocity 进入 Closing，会隐含：

- 潜在鱼在垂直方向也等概率分布；
- fish-lure depth relation 未被上游 Spatial / Candidate 限制；
- Response 可以自行决定鱼在拟饵上方还是下方。

这些都不是当前已知事实。

鱼在什么深度、水层是否适宜、presentation 是否正在穿过该鱼的局部机会区域，本应由 Spatial / Opportunity 一侧拥有。

因此 3D isotropic prior 会把垂直空间分布重新偷回 Response，存在重复计权风险。

---

## 3. 为什么不直接用 `abs(vertical_speed)` 处罚

禁止：

```text
ClosingCost += K_vertical * abs(v_vertical)
```

因为同样的垂直速度可能代表完全不同的 encounter 后果：

```text
鱼在拟饵下方，拟饵上升
→ 可能正在远离

鱼在拟饵上方，拟饵上升
→ 可能正在接近
```

没有 fish-lure vertical relation 时，`abs(v_vertical)` 不能告诉我们是接近还是逃离。

使用绝对值只会把“运动快”错误等价成“追赶难”。

---

## 4. Vertical motion 应该买到什么玩法效果

第一版更合理的系统故事是：

```text
快速 vertical lift
→ 更快穿过某个有效 depth / layer region
→ 有效 exposure window 变短
→ accumulated opportunity 下降
```

同时：

```text
vertical rise / fall / dart
→ prey-conditioned state
→ 可能改变 StateTrigger / prey interpretation
```

所以同一 vertical motion 可以合法有两条不同后果：

1. **空间/时间后果**：在局部有效区域停留多久；
2. **猎物状态后果**：当前像不像 rise / fall / escape / distressed prey。

它不自动产生第三条匿名 `VerticalClosingPenalty`。

---

## 5. 条件化理解 Horizontal2D Closing

Horizontal2D Closing 的完整语义应理解为：

> 在上游已经给出“当前存在一个局部 interaction opportunity”的条件下，拟饵的水平运动是否正在沿潜在鱼→拟饵方向增加径向分离负担。

因此：

```text
C_response(t)
```

不是对任意世界位置上的鱼计算的 response；它是**条件于局部 opportunity 已成立**的 response strength。

这也是为什么 vertical distance 不应再由 Response 自行重建。

---

## 6. Vertical-dominant presentation 是否 NotApplicable

第一版不把 vertical-dominant presentation 标成 Feeding Response `NotApplicable`。

原因：

- FoodValue、Motivation、StateTrigger、Prediction、Risk 仍然合法；
- Horizontal2D Closing 仍可对水平分量求值；
- 缺失的是完整系统层的 vertical opportunity / exposure，而不是整个 Feeding Response 无法计算。

因此状态应区分：

```text
Feeding Response
→ 可以计算局部 conditional response

Full-system opportunity / candidate result
→ 若 vertical opportunity owner 未提供必要输入，可能 ResolutionIncomplete
```

不能因为 full-system seam 缺失，就把 Response 自身宣告 NotApplicable。

---

## 7. 需要 Opportunity Owner 提供的最小语义

后续正式 owner 至少需要回答：

```text
当前 presentation 是否处于该 candidate / prey route 的有效垂直机会区域？
```

以及：

```text
在该区域内持续了多久？
```

不要求第一版拥有具体鱼点。

可以是更抽象的输出，例如：

```text
vertical_eligibility(t) ∈ {0,1}
```

或：

```text
vertical_opportunity_support(t) ∈ [0,1]
```

再与姿态颗粒 / temporal exposure 结合。

具体输出形态由 Opportunity / Spatial Owner 决定，Proposal C 不冻结。

---

## 8. Acceptance stories

### A. Horizontal steady retrieve

```text
vertical eligibility stable
horizontal speed > 0
→ Closing 主导运动负担
```

### B. Vertical jig through a narrow feeding layer

```text
horizontal speed ≈ 0
→ horizontal Closing≈0

rapid vertical traversal
→ short valid-layer exposure
→ lower accumulated opportunity
```

不会因为 `Closing≈0` 就得到无限优势。

### C. Slow vertical hover in valid layer

```text
horizontal Closing≈0
vertical eligibility sustained
→ longer exposure
```

如果 prey state / FoodValue 合适，累计 opportunity 可以较高。

### D. Vertical movement outside valid layer

```text
Feeding response local formula may be well-defined
but vertical eligibility = 0
→ no effective opportunity contribution
```

时间不能凭空制造 candidate opportunity。

---

## 9. 当前裁定

第一版冻结：

```text
Horizontal2D Closing 保留
完整 3D lure speed 不进入 Closing
不新增 abs(vertical_speed) penalty
vertical motion 的空间后果归 Spatial / Opportunity
vertical motion 的 prey-state 后果归 prey interpretation / StateTrigger
vertical-dominant presentation 不把 Feeding Response 标 NotApplicable
full-system vertical result 在 Opportunity seam 缺失时仍可 ResolutionIncomplete
```

这关闭的是 Response 对 vertical motion 的职责边界，不宣称 Vertical Opportunity 的生产机制已经闭合。

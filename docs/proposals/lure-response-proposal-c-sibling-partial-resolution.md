# Proposal C｜Sibling Prey Partial Resolution

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

同一 physical target 的 sibling prey interpretations 使用替代关系：

```text
C_feed = max(C_1, C_2, ...)
```

但 `Unknown / ResolutionIncomplete` 不能被静默当成 0，也不能因为存在一个已解析 sibling 就直接忽略。

第一版采用 **bounded partial resolution**：每条 sibling path 不只携带一个 scalar，而是携带当前可证明的 response 区间：

```text
C_i ∈ [L_i, U_i]
```

聚合后：

```text
L_feed = max_i(L_i)
U_feed = max_i(U_i)
```

只有：

```text
L_feed == U_feed
```

时，Feeding composition 才得到最终 scalar：

```text
C_feed = L_feed = U_feed
```

否则保持：

```text
ResolutionIncomplete
response_bounds = [L_feed, U_feed]
not rollable
```

这样 Unknown 不等于 0，但已知信息仍能继续压缩不确定范围。

---

## 2. 为什么不能简单采用“有 Unknown 就全部 Unknown”

例如：

```text
baitfish = resolved 0.80
crayfish = unresolved, known upper bound 0.60
```

虽然 crayfish 尚未完整解析，但它已经不可能超过 baitfish。

因此：

```text
max(0.80, crayfish≤0.60) = 0.80
```

最终 winner 已经确定，没有必要阻断整条 Feeding route。

反过来：

```text
baitfish = resolved 0.45
crayfish = unresolved [0, 1]
```

则不能输出：

```text
C_feed = 0.45
```

因为 crayfish 后续可能解析为更高值。

此时应输出：

```text
ResolutionIncomplete
bounds = [0.45, 1.00]
```

---

## 3. Sibling set 必须先确定

`max` 只能作用于**已声明属于同一 physical target、同一 Feeding route 的 sibling alternative set**。

不能运行时把整个 prey catalog 都塞进 sibling set，否则所有未配置 prey family 都会变成永久 Unknown。

第一版要求上游配置先声明本次需要评价的 sibling set，例如：

```text
SiblingSet
= {baitfish, crayfish, frog}
```

然后分别解析。

没有进入该 declared sibling set 的 prey family：

```text
NotParticipating
```

不参与本次 `max`，也不构成 Unknown。

进入 sibling set 后却缺少必要配置或输入，则是：

```text
NotConfigured / ResolutionIncomplete
```

不能从集合中偷偷删除。

因此必须区分：

```text
NotParticipating
≠ NotConfigured
≠ NoMatch
```

---

## 4. 各状态如何映射到区间

### 4.1 ResolvedResponsive

```text
C_i = c, 0 < c <= 1
→ [c, c]
```

### 4.2 ResolvedNonResponsive

```text
C_i = 0
→ [0, 0]
```

### 4.3 Reject

Reject 是 hard semantic zero：

```text
Reject
→ [0, 0]
```

它不是 Unknown。

### 4.4 NoMatch

当该 sibling interpretation 已完整评价，且当前 presentation 对该 prey interpretation 明确无匹配支持：

```text
NoMatch
→ [0, 0]
```

`NoMatch` 表示已知没有这条解释贡献，不是缺数据。

### 4.5 ResolutionIncomplete / Unknown

若当前只能证明合法范围：

```text
C_i ∈ [L_i, U_i]
```

则保留该区间。

若没有任何更窄信息，而 `C_prey` 的合法域为 `[0,1]`：

```text
Unknown
→ [0, 1]
```

但只要已有部分信息，就应使用更窄 bound，而不是退回 `[0,1]`。

### 4.6 NotConfigured

如果某 prey interpretation 已被声明进入 sibling set，但必要规则 / 数据配置不存在：

```text
NotConfigured
→ ResolutionIncomplete
```

其区间由当前还能证明的上下界决定；若没有其它约束，则为 `[0,1]`。

不能把 `NotConfigured` 当 `NoMatch=0`。

---

## 5. Prey support 与 fish-side response 的部分解析

当前：

```text
C_prey
= prey_support × R_prey
```

其中：

```text
R_prey = E_theta[C_conditional,p(theta)]
```

两者合法域均为非负 `[0,1]`。

因此如果：

```text
support ∈ [S_L, S_U]
response ∈ [R_L, R_U]
```

则可安全传播：

```text
C_prey
∈ [S_L × R_L,
   S_U × R_U]
```

因为所有量均非负。

例：support 已知为 `0.60`，fish-side response 尚未解析：

```text
support = [0.60, 0.60]
response = [0, 1]
→ C_prey = [0, 0.60]
```

此时另一个 sibling 若已解析为 `0.75`，就已经可以安全胜出：

```text
max(0.75, unknown≤0.60)
→ C_feed = 0.75
```

这比把所有 Unknown 一律扩成 `[0,1]` 更有信息量。

---

## 6. Max aggregation

给定 sibling set：

```text
S = {1,2,...,n}
```

每条 path：

```text
C_i ∈ [L_i, U_i]
```

聚合：

```text
L_feed = max_i L_i
U_feed = max_i U_i
```

### 已闭合

若：

```text
L_feed == U_feed
```

则：

```text
ResolvedResponsive, if C_feed > 0
ResolvedNonResponsive, if C_feed = 0
```

### 未闭合

若：

```text
L_feed < U_feed
```

则：

```text
ResolutionIncomplete
not rollable
```

但 Explain 应保留：

```text
known_lower_bound
possible_upper_bound
current_leading_sibling(s)
unresolved_competitor(s)
```

---

## 7. Winner 已确定但 sibling 仍 Unknown

这是 bounded resolution 的主要价值。

例如：

```text
baitfish = [0.80, 0.80]
crayfish = [0.10, 0.60]
frog     = [0.00, 0.30]
```

则：

```text
L_feed = 0.80
U_feed = 0.80
```

因此：

```text
C_feed = 0.80
ResolvedResponsive
```

虽然 crayfish / frog 自己仍未完全解析，但它们已经没有改变 `max` 结果的可能。

这不是把 Unknown 当 0，而是证明 Unknown 已不影响当前 operator 的结果。

---

## 8. Tie

若多个 sibling 最终同值：

```text
baitfish = 0.70
crayfish = 0.70
```

则：

```text
C_feed = 0.70
```

数值上已闭合。

Explain 可记录：

```text
winning_siblings = {baitfish, crayfish}
```

不需要人为选唯一 prey identity。

这与 prey support 本来就允许多重解释一致。

---

## 9. 不能做的事

禁止：

```text
Unknown → 0
```

禁止：

```text
max(known siblings only)
```

如果 declared sibling set 中仍有未解析 path，除非它的 upper bound 已证明不会改变 winner。

禁止：

```text
Unknown → default prey support / default response
```

禁止为了得到 scalar 随机选择 prey identity。

禁止把 entire prey catalog 当 sibling set。

---

## 10. Acceptance cases

### A. 全部已解析

```text
0.60, 0.35, 0
→ C_feed = 0.60
```

### B. Unknown 可能改变 winner

```text
baitfish = [0.45, 0.45]
crayfish = [0, 1]
→ feed = [0.45, 1]
→ ResolutionIncomplete
```

### C. Unknown 已无法改变 winner

```text
baitfish = [0.75, 0.75]
crayfish = [0, 0.60]
→ feed = [0.75, 0.75]
→ C_feed = 0.75
```

### D. NoMatch

```text
baitfish = 0.40
frog = NoMatch
→ max(0.40, 0)
→ 0.40
```

### E. Declared but NotConfigured

```text
baitfish = 0.40
crayfish = NotConfigured [0,1]
→ [0.40,1]
→ ResolutionIncomplete
```

### F. Not participating

```text
SiblingSet={baitfish, crayfish}
frog not in set
```

frog 不参加 max，也不导致 incomplete。

---

## 11. 当前裁定

第一版冻结以下 Candidate 边界：

```text
Sibling set 先声明
Unknown != 0
NoMatch = resolved zero
Reject = hard resolved zero
NotConfigured inside declared set = ResolutionIncomplete
partial information 使用 bounds 传播
max operator 对 bounds 做 max
只有聚合 bounds 收敛才输出最终 scalar
未收敛时不可 roll，但 Explain 保留 bounds
```

该规则只闭合同一 Feeding route 内 sibling alternative 的 partial-resolution semantics，不扩展到 Feeding / Defense / Investigation 等 Complete Modes 的跨 family composition。跨 family operator 仍由 Interaction contract 决定。

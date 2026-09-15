# FCF-PC-BASELINE-R0 冻结前自审报告

- 审查对象:[FCF-PC-BASELINE-R0-20260915](../baselines/FCF-PC-BASELINE-R0-20260915.md)(EXPERIMENT FREEZE CANDIDATE / NOT PROMOTED)
- 审查日期:2026-09-15
- 审查者角色:Coding Agent 自审。本报告**不构成** AGENTS.md 定义的独立审核,不输出 PASS/BLOCK;独立审核与晋升决定仍归 `gpt-5.6-sol` / Owner。
- 审查方法:仅做内部一致性、可实现性、度量可计算性检查。**未**对照 Notion 中鱼库与飞书推导表(本轮未授权该范围);涉及既有术语出处的问题见 P2-9。
- 纪律声明:本报告所有「建议」均**未**应用于冻结文本;是否进入 R1 修订由 Owner 决定。未澄清前遇到的相关 case,应记 `UNRESOLVED` / semantic delta request,不得自行选定一种解释实现(遵循 §4 同款纪律)。

## 总评

- 未发现根本性架构矛盾:fish-independent 边界(§2.1)、§3.2 边界公式、§7 禁用字段、§4 不吞并约束、§8 双计规则、§9 kill signals 互相咬合良好(见文末「结构稳健点」)。
- 主要风险集中在两类:(a) **参考系与表轴未定义**(P1-1/P1-2/P1-3);(b) **分类与度量程序未定义**(P1-4/P2-6)。都不动摇架构,但会在首轮实验中制造实现分歧,导致 run 之间不可比、结论可被实现选择改写。
- 建议冻结前以「一句话级别增补」澄清 P1-1..P1-4;P2 或澄清、或显式进 §13 open 清单;P3 随 R1 顺带处理;WATCH 项进 run 报告。

## 发现索引

| ID | 位置 | 级别 | 摘要 |
|---|---|---|---|
| P1-1 | §2.1, §3.2 | 必须澄清 | 观察者相对 cue(apparent_size / visual_contrast)的参考系未定义,与 §2.1 不变式的字面表述冲突 |
| P1-2 | §3.2 | 必须澄清 | 运动学 cue 的参考系/时间窗未定义;cue.displacement 度量语义未定义 |
| P1-3 | §4 | 必须澄清 | Static Fish Target Affinity 表轴未定义;Engagement Mode 进入路径图与文字不一致 |
| P1-4 | §10 | 必须澄清 | 分类缺判定程序:单/多标签、优先序、边界判定、抽查机制 |
| P2-5 | §4 | 建议澄清 | FeedingTarget hypotheses N=0 时 affinity 的缺席语义未定义 |
| P2-6 | §11 | 建议澄清 | 度量缺 dev/holdout 分组、首轮绝对值口径、逐项操作化定义 |
| P2-7 | §8 | 建议澄清 | CAUSE_OWNERSHIP_CONFLICT 缺声明/豁免载体;共享成因双 cue 消费未声明为 open |
| P2-8 | §12 | 建议澄清 | holdout 抽样框(sampling frame)来源与钉住方式未定义 |
| P2-9 | 全文, §5 | 建议澄清 | 悬挂引用(SET/CAP、ResponseBand 等)无出处;CueSignature 身份语义未钉死 |
| P3-10 | §3.1/§3.2/§4 | 编辑性 | `?` 后缀约定未说明 |
| P3-11 | §4 | 编辑性 | 「默认消费」的例外路径未定义 |
| P3-12 | §3.2 | 编辑性 | cue.sound_pattern 作为 primitive 但域未定义 |
| P3-13 | §11/§13 | 编辑性 | cue/presentation schema 的 run 间版本钉住缺失 |
| P3-14 | §1 vs §3 | 编辑性 | 图中单层 "Presentation / Cue Facts" 与 §3 双 namespace 术语漂移 |
| WATCH-15 | §3.1 vs §4 | 观察 | descriptor↔FeedingTarget 恒等映射退化风险 |
| WATCH-16 | §8 | 观察 | 共享成因的两个 cue 被同一 rule 消费的隐性双计 |

级别定义:P1 = 冻结前必须澄清,否则首轮实验产生实现分歧;P2 = 冻结前建议澄清,影响度量或流程可信度;P3 = 编辑性改进;WATCH = 开放观察项,不阻塞。

## 详细发现

### P1-1 `cue.*` 观察者参考系未定义,与 §2.1 不变式的字面表述冲突

引文:§2.1「同一组 Presentation / Cue Facts 不得因为当前评估 Species 或 Engagement Mode 不同而变化。」;§3.2 Candidate Basis 含 `cue.apparent_size`、`cue.visual_contrast`。

问题:apparent_size / visual_contrast 是观察者相对量。若以评估鱼的位置/朝向为几何参考,同一 Presentation 在不同评估距离/角度下取值不同;当不同 Species 的典型评估几何不同时,cue 值会 de facto 随 Species 漂移——尽管 resolver 并未读取任何 §2.1 禁止项。字面不变式与观察者相对 cue 不能同时严格成立,除非二选一:(a) 明确 cue 允许以评估上下文的**纯几何量**(位置/距离/视角)为参考,禁止的只是 Species/Mode 的 valuation 属性;(b) cue 一律世界系(此时 apparent_size 语义需重定义)。

失败场景:两个实现者分别按 (a)/(b) 实现,同一 dev case(如 Topwater popper pop-pause 的水面视角对比度)得出不同 `cue.visual_contrast`,classification 与 §8 冲突判定随之不同,run 之间不可比。

建议(未应用):在 §2.1 增补参考系条款(明确选 a 或 b),并给每个观察者相对 cue 标注参考系。

### P1-2 运动学 cue 的参考系、窗口与 displacement 度量未定义

引文:§3.2 `cue.speed`、`cue.speed_change`、`cue.direction_change`、`cue.pause_duration`、`cue.vertical_motion`、`cue.displacement`。

问题:(i) 未定义水局部参考系 vs 地面参考系——dead drift(地面速度≈流速,水相对速度≈0)两种取值截然不同;(ii) `cue.displacement` 未定义是净位移还是路径长度、时间窗多长——Spoon steady 与 oscillating 的区分正落在这个差值上(振荡收线:路径长度大、净位移小);(iii) speed_change / direction_change 的微分窗口未定义。

失败场景:dev set 首轮就会同时遇到 Fly dead drift(DEV-007)与 Spoon oscillating(DEV-006);参考系选择直接决定这两个 case 是 COVERED 还是需要 exception——未定义项会直接改写实验结论与 kill-signal 读数。

建议(未应用):冻结「水局部参考系 + 显式时间窗」;displacement 定义为窗口净位移或路径长度(二选一),另一个留作候选派生量。

### P1-3 Static Fish Target Affinity 的轴定义缺失,Engagement Mode 进入路径图文不一致

引文:§4 链路图为 `Static Fish Target Affinity × Dynamic Feeding Preference`;relation 语义句为「相对于当前 Species / Engagement Mode / current feeding preference 是否合适」。

问题:Static Affinity 的表轴未定义——是 Species × FeedingTargetKey 还是 Species × Mode × Target?Mode 是经 DynamicFeedingPreference 进入还是独立维度?链路图未画 Mode,文字却含 Mode。该轴定义直接决定 §11 的 `Fish × Descriptor direct-touch count` 与 `per-descriptor Species/Mode fan-out` 的计数单位,即 §9 kill-signal 的分母。

失败场景:同一 run 按两种轴口径统计 fan-out,数值差一个 Mode 因子,kill-signal 判定不可复现。

建议(未应用):明确 Static Affinity = Species × FeedingTargetKey,Mode 只经 Dynamic Feeding Preference 与 Response 层进入(或另行声明),并同步修链路图。

### P1-4 §10 分类缺判定程序

引文:§10 九类标签清单。

问题:未定义 (i) 单标签还是多标签;(ii) 多类同时适用时的主标签规则;(iii) COVERED 与 DERIVED_DESCRIPTOR_ONLY 的边界(谁判定「确定性派生」、判据是什么);(iv) 分类由 Coding Agent 初判时的自利归类风险(borderline 记 COVERED)如何抽查。

失败场景:分类是 §11 全部度量的输入;判定程序缺失 → run 间分类漂移,所有 Δ 指标失去可比性。

建议(未应用):见 [EXP-PROTOCOL-FCF-PC-R0](../experiments/EXP-PROTOCOL-FCF-PC-R0.md) §5 的提案判定树(标注 [PROPOSAL-R0]),含正交 flag 设计与 Reviewer 抽查比例。

### P2-5 FeedingTarget hypotheses N=0 的缺席语义未定义

问题:§4 的 0..N 中 N=0(presentation 不被解释成任何 feeding target,如纯 reaction / territorial 情形)时 `relation.feeding_target_affinity` 取什么、Response DSL 如何消费 absence,未定义。实验遇及时最易被自行发明一个 "NONE" 底元——这是一个隐蔽的 vocabulary 擅自扩张点。

建议(未应用):明确 absence 为合法取值并在 DSL 消费语义中声明,或显式归 UNRESOLVED。

### P2-6 §11 度量口径缺口

问题:(i) 无 dev/holdout 分组要求——不分组则 dev 调出的规则会混进 holdout 口径;(ii) 首轮没有 Δ,需绝对值口径;(iii) 各指标缺一行操作化定义(`direct-touch`、`fan-out`、`single-use` 的计数单位);(iv) Δ requests 未区分 admitted/rejected。

建议(未应用):见协议 §6 的指标定义表提案。

### P2-7 CAUSE_OWNERSHIP_CONFLICT 缺声明载体与豁免记录

问题:§8 允许「有独立语义理由」时共消费,但理由在哪里、以什么形式声明未定义——harness 报出 conflict 后没有消解路径,报告会持续挂起。另外,两个 cue 共享成因(如 apparent_size 与 visual_contrast 共享 geometry/turbidity 成因)造成的隐性双计不在 §8 规则覆盖内,且未像 §13 那样被显式声明为 open。

建议(未应用):定义 rule 级 `CAUSE_JUSTIFIED` 声明载体(理由文本 + 引用);把共享成因双 cue 消费加入 open 清单或 WATCH(WATCH-16)。

### P2-8 holdout 抽样框未定义

问题:§12 把 holdout 选择权交给独立 Reviewer / Sample Agent,但没有定义其抽样总体从哪来、如何钉住版本。没有钉住的 frame,Sample Agent 无法开始,事后也无法检查是否存在 frame 缩小(frame-gaming)。

建议(未应用):见 [HOLDOUT-HANDOFF-R0](../experiments/HOLDOUT-HANDOFF-R0.md) 的输入契约(Owner 提供 pinned 快照)。

### P2-9 悬挂引用与 CueSignature 身份语义

问题:SET/CAP、`CAP_RESPONSE_BAND`(§5 例)、ResponseBand、SelectionWeight(§2.1 禁读列表)、DynamicFeedingPreference、Engagement Mode、CueSignature(§5)均在本文使用但未定义、未给出处。R0 要「独立可审」,需要一节 assumed prior contracts。其中 **CueSignature 的身份语义**尤其要钉死:其 key 必须由 `cue.*` 内容派生,不得含 item identity——否则 §2.2 会被 familiarity 链路绕过(按 SKU 记熟悉度)。

建议(未应用):增加「Assumed Prior Contracts」一节列出处;CueSignature 身份语义单独一句话钉死;其余无出处的机制归入 §13 open 清单。

### P3-10 `?` 后缀约定未说明

`presentation.profile?`、`cue.chemical_intensity?` 等的 `?` 可推断为「candidate / not frozen」,建议一句话明说,避免被实现者当作 token 命名的一部分。

### P3-11 「默认消费」的例外路径未定义

§4「Response DSL 默认消费 relation.feeding_target_affinity」——「默认」暗示存在直接查 Target 表的例外,但例外准入未定义。建议注明:直接消费 Target 表需走 §9 admission。

### P3-12 `cue.sound_pattern` 域未定义

「pattern」不是标量;作为 primitive 冻结但域(枚举/签名/模板)未定义。建议降为 candidate(加 `?`)或定义其类型域。

### P3-13 schema / run 版本钉住缺失

Freeze ID 钉住的是文档文本;cue/presentation schema 若在 run 之间变化,Δ 指标失去可比性。建议每 run 记录 schema 版本(协议 §4 已留检查位)。

### P3-14 §1 图与 §3 术语漂移

§1 图把 "Presentation / Cue Facts" 画为单层,§3 拆成准入语义不同的两个 namespace(`presentation.*` / `cue.*`)。建议在图注说明该层含两个 namespace。

### WATCH-15 descriptor↔FeedingTarget 恒等映射退化

`MINNOW_LIKE`(§3.1)与 `SMALL_BAITFISH`(§4 示例)语义近重叠。若 Target Interpretation 长期退化为恒等映射,两层 vocabulary 有一层冗余,按 §9 应裁掉一层。建议 run 报告增加「descriptor→target 非恒等映射率」观察指标(不阻塞)。

### WATCH-16 共享成因双 cue 消费

见 P2-7 后半。实验期观察同一 rule 消费共享成因 cue 对的频率,为未来扩展 §8 积累证据。

## 结构稳健点(正向确认)

- fish-independent 边界(§2.1)与 §3.2 边界公式、§7 禁用字段互相咬合,未发现内部矛盾(P1-1 属措辞级歧义,非主张冲突)。
- §4 两个「必须合法」反例(BEST affinity + 坏 motion → LOW;GOOD affinity + 匹配 cue → HIGH)有效阻止 affinity 吞并 presentation quality。
- §6 默认表达式(primitive + field-to-field + ALL/ANY/NOT)与 §9 kill signals、§11 fan-out 指标构成闭环。
- §10 的 development-set 吸收规则是防 case-driven 改基线的关键机制,方向正确(P1-4 只需补判定程序)。
- §13 open 清单诚实,把 multi-target aggregation、SET/CAP 终局算法等明确挡在 Coding Agent 自行闭合之外。

## 处置建议汇总

P1-1..P1-4 建议冻结前以最小增补澄清(不动架构);P2 可澄清或显式进 §13 open 清单;P3 随 R1 顺带处理;WATCH 进 run 报告。所有处置由 Owner 决定;澄清前相关 case 一律记 `UNRESOLVED`,不得自行选择解释实现。

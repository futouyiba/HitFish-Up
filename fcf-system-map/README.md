# FCF Canonical System Map — Production Pilot v0.1

日期:2026-09-17 · 分支:`futou-/trusting-lehmann-70328f` · 前置:draw.io capability spike 已 PASS(`../spike/`)

**目标回顾**:第一版真实 `FCF Canonical System Map / 中鱼机制总图`。semantic source 是事实源;`.drawio` 是确定性生成产物;全程 AI/code authoring;支持展开/折叠、Version Scope、stable semantic ID,并预留 Contract / Notion Authority 关联。本轮不测试 draw.io、不重设计 FCF。

---

## 1. Source files(semantic source,唯一允许编辑的输入)

| 文件 | 职责 |
|---|---|
| `graph.json` | 25 个节点(stable ID + display label + 语义层级 parent + layout lane)+ 19 条显式语义边(`DATA_FLOW` / `CONTROL_OR_SELECTION` / `REFERENCE_OR_CONFIG`) |
| `scopes.json` | Scope 维度:`OVERALL`(无 lens)与 `0.3.4.0`(lens),三分类 `ACTIVE / BOUNDARY / OUT`,每个节点恰好归入一类 |
| `views.json` | View 维度:三个视图预设(Overall / 0.3.4.0 / Spatial Bake Detail),声明式定义各自动哪个维度、绝不动另一个 |
| `contracts.json` | 薄关联层:`semanticId → authorityRef / status / note`;只引用外部权威(飞书 / Notion),不复制内容 |

**三维度正交**(本轮的硬约束):

- **Hierarchy** = `graph.json` 的 `parent`(progressive disclosure;`collapsible` 节点的子树可折叠);
- **Scope** = `scopes.json` 的分类,实现为对**同一批 cell** 的原生 `style` action 着色——**单实例,零复制**,不存在 `Spatial_Detail_0340` 这类 scope × view 层组合(spike 时代的 `::view` 灰副本方案被明确废弃,连带消除了 spike 审查发现的 stable-ID↔scope 耦合);
- **View** = `views.json` 的预设,只动可见性或只动配色,二者互不覆盖。

## 2. Generated artifacts

```
generated/fcf-system-map.drawio      # 构建产物,禁止手工编辑;sha256 见下
build/build_diagram.py               # 确定性构建器(Python 3 stdlib,无依赖)
build/validate.py                    # 静态验证套件(见 §7)
build/viewer-harness.html            # 测试脚手架(仅验证用,可整体删除)
```

构建:

```bash
python3 build/build_diagram.py       # 4 个 source JSON -> generated/fcf-system-map.drawio
python3 build/validate.py            # 全部静态检查 + 确定性 + rename 稳定性
```

- `fcf-system-map.drawio` sha256 = `5f8ba3bd7a29225f`…(完整值 `shasum -a 256 generated/fcf-system-map.drawio`)
- 消费表面 = 官方 diagrams.net viewer(pinned `viewer-static.min.js`,sha256 `e49a0d5d…`,与 spike 共用 `spike/verify/vendor/`);交互全部为原生 custom action(`show/hide/toggle/style`),词汇表已在 spike 阶段从 viewer 源码逐条核实。

## 3. Stable-ID count

**25 个 stable semantic ID**(构建后 cell id == node id,1:1 单实例):

```
SYS.CONTEXT            OPPORTUNITY.BASE      MODE.ROUTING          CANDIDATE.RESOLVED
SPATIAL                CONDITION             PRESENTATION.EXPOSURE RESPONSE
SELECTION              MATERIALIZATION
SPATIAL.SUBJECT        SPATIAL.SNAPSHOT      SPATIAL.BASE          SPATIAL.TEMPLATE
SPATIAL.GATE           SPATIAL.FACTOR        SPATIAL.CORE_LOSS     SPATIAL.SECONDARY_LOSS
SPATIAL.AGGREGATE      SPATIAL.ENV_COEFF     SPATIAL.INTENSITY     SPATIAL.DEBUG
CONDITION.ACTIVITY     CONDITION.FUNCTIONAL_CAPACITY   CONDITION.FEEDING_READINESS
```

Display label 可随时改名而不动 ID(validate.py 每次全量改名回归)。ID 语法受校验:禁 `::`、`->`、`:` 与保留前缀(`E:`/`EX:`/`BTN:`/`CTRL:`/`LEG:`/`Layer:`),防止 spike 审查指出的字符串解析暗通道。

## 4. Views

| 视图 | 动 Hierarchy? | 动 Scope 配色? | 语义 |
|---|---|---|---|
| **Overall**(默认) | 收起全部 detail 子树 | 清除 lens,恢复中性配色 | 复位预设:一眼主链 |
| **0.3.4.0** | **绝不触碰** | 应用 0.3.4.0 lens | 只回答"这个版本负责什么" |
| **Spatial Bake Detail** | 展开 SPATIAL 子树 | **绝不触碰** | 只改变阅读粒度,可与 0.3.4.0 配色自由叠加 |

另有手动操作:点击 `Spatial Opportunity` / `Fish Condition` 节点本身 toggle 其子树(toggle 语义),与任何按钮状态组合。预设用幂等 `hide/show` 集合而非 toggle,保证"按钮不动手动展开状态"。

## 5. Scope behavior(0.3.4.0)

- **ACTIVE(13)**:SPATIAL + 全部 12 个 SPATIAL.* 细节节点——正常分支色。
- **BOUNDARY(3)**:`SYS.CONTEXT`、`OPPORTUNITY.BASE`、`CANDIDATE.RESOLVED`——保持本色、**虚线边框 + 加粗**,表达"被当前 Bake 消费、本任务不负责其内部"。这是按规范"只标记必要边界,不扩大 Scope"的最小集合(bake 的三类输入:resolved subject / environment snapshot / base opportunity)。判定规则:被当前 Bake 消费且非本任务实现。
- **OUT(9)**:`MODE.ROUTING`、`CONDITION` + 3 子节点、`PRESENTATION.EXPOSURE`、`RESPONSE`、`SELECTION`、`MATERIALIZATION`——**置灰(#f5f5f5 / #a6a6a6 / #8f8f8f)但永不隐藏**,上下文可读。
- 边的 lens 规则:target ∈ OUT → 边灰;source ∈ BOUNDARY 且 target ∈ ACTIVE(跨边界消费,如 `CANDIDATE.RESOLVED→SPATIAL.SUBJECT`)→ 边虚线。
- 实测(viewer 运行时断言):lens 只改 `fillColor/strokeColor/fontColor/dashed/strokeWidth`,展开状态在 lens 切换前后逐 cell 一致;OUT 节点全部保持 rendered。

## 6. Expand/collapse behavior

- `SPATIAL` 子树 = 12 节点 + 全部关联边(结构边、内部流边、跨边界输入边);`CONDITION` 子树 = 3 节点 + 结构边。点击节点 toggle,视图按钮用幂等 show/hide。
- 初始态 = Overall 视图(detail 子树以 `visible="0"` 烘焙,官方 viewer 加载即遵守)。
- 实测正交性矩阵:lens 开 → 展开 SPATIAL(12 节点全渲染、lens 仍在)→ 收起(子树消失、lens 仍在)→ Overall(配色还原、子树保持收起)→ Spatial Bake Detail(仅展开、配色保持中性)→ 点击 CONDITION 展开/收起(与 Detail 视图共存,主链边不受影响)。
- 已知原生行为:可见性变化后 viewer 会 auto-crop 重新取景(spike 已记录);折叠不引发周边重排(draw.io 无全局 reflow)。

## 7. Validation result

`python3 build/validate.py` → **PASS**(规范 Validation 1–6 + schema):

```
stable IDs:        25 (unique, syntax-safe)
edges:             19 semantic + 15 structural, endpoints ok
scope 0.3.4.0:     13 ACTIVE / 3 BOUNDARY / 9 OUT, all nodes classified once
views:             overall, 0340, spatial-detail (default overall)
contracts:         13 entries (refs valid)
determinism:       consecutive builds byte-identical; committed artifact fresh
rename stability:  cell ID set and geometry invariant under label rename
```

规范 Validation 7–10(viewer 运行时,官方 `viewer-static.min.js` + 程序化断言):

- **7 Overall / 0.3.4.0 切换**:PASS(§5 全部断言);
- **8 Spatial expand/collapse**:PASS(§6 正交性矩阵);
- **9 OUT 只置灰不删除**:PASS(cell 存在于 model、rendered、灰色三元组);
- **10 生成文件零人工修补**:PASS(viewer 直接加载、console 无 warn/error、全部交互由生成的 action 完成)。

> harness 备注:开发面板把 1400px 模拟视口缩进 362px 物理面板时,**合成**(JS 派发)鼠标事件的坐标簿记会失真,自动化断言改经 `customLinkClicked()`(viewer 点击回调的同一入口)执行;真实鼠标不受影响。普通环境:`python3 ../spike/verify/serve.py` 后打开 `http://127.0.0.1:8799/fcf-system-map/build/viewer-harness.html`(预览沙箱读不了 `/Volumes`,需按 spike README 的方式镜像到 /tmp)。

## 8. SEMANTIC_OPEN(只记录,不填补)

| ID | 缺口 | 当前图上的忠实表达 |
|---|---|---|
| SEMANTIC_OPEN-001 | 五个 bake stage(Gate / Atomic Factor / Core Loss / Secondary Loss / Aggregation)之间的内部顺序与数据流 | 按 Pilot 规范图渲染为 TEMPLATE 下的**无序兄弟**(├─ 列表),不画内部顺序边 |
| SEMANTIC_OPEN-002 | Spatial × Condition 在 `PRESENTATION.EXPOSURE` 的汇合语义 | 两条边只表达"职责域进入后续链路",不暗示任何 combine 数学(规范明令禁止自行发明) |
| SEMANTIC_OPEN-003 | Activity 是否进入 0.3.4.0(源文档标注"讨论") | `CONDITION.ACTIVITY` 为结构占位,scope=OUT;contracts.json 标 pending |
| SEMANTIC_OPEN-004 | `SPATIAL.DEBUG` 的消费契约(读什么) | 按规范图画在 INTENSITY 下游;具体消费未确认 |
| SEMANTIC_OPEN-005 | `MODE.ROUTING` 的 scope 归类 | 按"被当前 Bake 消费才设 BOUNDARY"规则定为 OUT(路由只产出 resolved candidate,其内部不被 bake 消费);待 Design Owner 确认 |

依据标注(AGENTS.md 纪律):ACTIVE/BOUNDARY/OUT 划分依据 = 本轮 Pilot 指令原文;bake 输入/输出结构依据 = 用户提供的烘焙逻辑文档(飞书 `RgWQdLKQkoYmf1xCP14cHMnondh`);组件计算依据 = 飞书 `VUdJdinA3oHTQsx0SP7cmCHfnkh`;权重聚合依据 = Notion `3dca4137d23681309a7cf6b43216c036`。以上仅以 contracts.json 引用,未改动任何 Notion/飞书权威。Notion 中鱼库本轮未读取(本轮未涉及权威修改,不伪称已读)。

## 9. Commit

见本次提交 `fcf-system-map: Production Pilot v0.1`(SHA 在会话最终报告给出;`git log --oneline -- fcf-system-map` 可查)。

## 本轮不做的事(合规确认)

未重设计 Activity;未裁 Functional Capacity / Feeding Readiness;未重开 DSL;未改 Notion Authority / 机制 Contract;未并入 P哥原图;未开发独立 Web App(verify 脚手架仅加载 pinned 官方 viewer);未扩展通用 Diagram Platform。

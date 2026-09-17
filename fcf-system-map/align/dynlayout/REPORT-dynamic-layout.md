# 实验报告：展开/折叠时的动态重排（方案二）是否可行

日期：2026-09-17 · 分支：`futou-/dynlayout-experiment`（自 `fcf-map-canonical` 开出）
viewer：`spike/verify/vendor/viewer-static.min.js`
sha256 `e49a0d5d1eac05351c3d21a22d5278fcab5d20066bdbdf074edc0b9989c611cd`（与 spike 报告一致）
产物：`probe.drawio` / `probe-tc.drawio` / `probe-layers.drawio`（由 `probe_build.py` 生成，连续两次构建逐字节一致）

## 复现

```bash
python3 fcf-system-map/align/dynlayout/probe_build.py
# 在仓库根起静态服务（App 的预览沙箱读不了 /Volumes，普通终端可以）
cd "$(git rev-parse --show-toplevel)" && python3 -m http.server 8801
# 打开 http://localhost:8801/fcf-system-map/align/dynlayout/probe.html
```

`probe.html` 用官方 pinned viewer 加载 probe，暴露 `window.P`，用**合成鼠标事件真实点击**
（`mousedown/mouseup/click` 打在 `state.shape.node` 上），并回读每个 cell 的
`geometry` / `state` / `visible` / `collapsed`。

## 可交互 demo：三层嵌套容器逐级展开

`demo.html` + `demo-nested.drawio`（`python3 demo_build.py` 生成，逐字节确定）：

- 结构：L1 ×2（并排两列）→（每个 L1）L2 ×3 →（每个 L2）L3 ×3 →（每个 L3）内容块 ×3，
  即 **26 个真容器（2 / 6 / 18）+ 54 个内容块**，全部 drawio 原生 `childLayout=stackLayout`。
- 初始全折叠（只有 2 条 L1 标题条）。**点图里任意一条标题条**展开那一层，再点收起。
- 每个容器的子块顺序是 `[标题条（永不隐藏，携带 toggle） , 内容子块…]`。
  标题条做成子块而不是容器自己的标题栏，是因为栈布局在「没有可见子块」时不会重排父容器——
  那样收起后会留一条空档；标题条常驻可见就保证了收起时容器精确缩到 `标题 18 + 2×border 5 = 28`。

**两个版面决定（都是实测倒逼出来的）：**

1. **两列 L1 各自独立，不共用一个外层栈。** 单列 27 层纵排全展开是 340×2213，
   在常规面板里只能缩到 ×0.36、字看不清；分成两列后全展开是 720×1099，可以缩到 ×0.5~0.7。
   顶层兄弟间的重排由 `probe.drawio` 单独覆盖。
2. **viewer 必须 `resize:false`。** `resize:true` 时 viewer 会把**图的内容尺寸**写成容器的
   inline 高度（全展开时实测写成了 `height: 4458px`），于是页面被撑长、图不缩放 ——
   这正是「显示不全」的直接原因。`resize:false` + 页面自己定容器高度 + 每次编辑事务后重新取景，
   才是「永远看得全」的组合。

**实测（合成鼠标事件真实点击图里的标题条，每步都检查是否落在面板内）：**

| 操作 | 可见容器 L1/L2/L3/内容块 | 可见内容框 | 缩放 | 是否整幅可见 |
|---|---|---|---|---|
| 加载（全折叠） | 2 / 0 / 0 / 0 | 720×28 | ×1.61 | ✓ |
| 点 L1-A | 2 / 3 / 0 / 0 | 720×127 | ×1.61 | ✓ |
| 点 L2-A2 | 2 / 3 / 3 / 0 | 720×226 | ×1.61 | ✓ |
| 点 L3-A21 | 2 / 3 / 3 / 3 | 720×301 | ×1.61 | ✓ |
| 收回 L3 → L2 → L1 | 2 / 0 / 0 / 0 | 720×28 | ×1.61 | ✓（逐字节回到初值） |
| 全部展开 | 2 / 6 / 18 / 54 | 720×1099 | ×0.51 | ✓ |
| 全部收起 | 2 / 0 / 0 / 0 | 720×28 | ×1.61 | ✓ |

全程空档检查 0 处 FAIL（每个收起容器的高度都正好是 28），全程 `fits` 全为 true。

页面自带两项自检（加载后直接显示在状态栏，也可点「跑一次自检」重跑）：
① 初始折叠坐标 = `.drawio` 里写死的坐标（点开前零位移）；
② 4 个层级各做一次「展开 → 全收起 → 再展开」，可见几何逐字节一致。


---

## 结论速览

| 问题 | 答案 |
|---|---|
| Q1 整行重排能不能跑起来 | **能**，但不是在"加载"或"折叠"上触发，而是在**任何一个完成的 model 编辑事务**上触发 |
| Q2 能不能接到点击上 | **能**，不需要新动词：现成的 `hide` / `show` / `toggle` 就够（正文说明为什么） |
| Q3 确定性 | **整数精确、与窗口尺寸无关、跨页面加载逐字节一致** |
| Q4 位置记忆 | **精确回到原位，40 次循环零漂移**；唯一例外见 §Q4.4 |
| Q5 第三种做法 | **有，而且比"整行折叠"更好**：标题与内容作为**并列的 stack 子块**交错排（§Q5a） |

**判断：值得用，但只值得做成一个可回退的 A/B，范围限在"行带"这一层，先用行二对照方案一。**
理由与代价见文末「判断」。

---

## Q1 让它重排：机制与触发点

**实验**：`probe.drawio` 里 `OUTER` 是一个 `childLayout=stackLayout;horizontalStack=0;stackSpacing=10;stackBorder=10;`
的容器，5 个可折叠行容器 `R1..R5` 是它的直接子块，故意都摆在同一个 y（重叠）。

**实测 1 — 加载时不跑。**

| | 每个行容器的绝对 y | 高度 |
|---|---|---|
| 加载后（未调用任何布局） | R1..R5 全是 **130**（互相重叠） | 100 |

**实测 2 — 显式调用布局就排好。**

| 触发 | R1 / R2 / R3 / R4 / R5 的 y | 行距 | OUTER 高 |
|---|---|---|---|
| `graph.executeAllChildLayouts(root)` | 70 / 180 / 290 / 400 / 510 | 110 = 100 + 10 | 560 |
| `layoutManager.executeLayout(OUTER)` | 同上 | 同上 | 560 |

**实测 3 — 触发点在哪：栈追踪。**

```
lm.executeLayoutForCells([OUTER])
  at mxLayoutManager.beforeUndo      (viewer-static.min.js:1508)
  at mxLayoutManager.<anonymous>     (viewer-static.min.js:1504)   <- bound to model BEFORE_UNDO
  at mxGraphModel.<anonymous>        (viewer-static.min.js:70)
  at mxEventSource.fireEvent
  at mxGraphModel.endUpdate          (viewer-static.min.js:935)
```

对应源码（去 minify 后）：

```js
// mxGraphModel.prototype.endUpdate
if(this.endingUpdate && !this.currentEdit.isEmpty()){
  this.fireEvent(new mxEventObject(mxEvent.BEFORE_UNDO, "edit", this.currentEdit));   // ← 每个非空编辑事务都会发
  ...
}
// mxLayoutManager.setGraph
model.addListener(mxEvent.BEFORE_UNDO, this.undoHandler)
```

**所以触发条件是"任何一次完成的、非空的 model 编辑事务"**，不是折叠、不是加载：

1. `endUpdate()` 发 `BEFORE_UNDO`；
2. `mxLayoutManager.beforeUndo` → `executeLayoutForCells(getCellsForChanges(changes))`；
3. `getCellsForChange` 收录 `mxChildChange / mxValueChange / mxTerminalChange / mxGeometryChange / mxVisibleChange / mxStyleChange`；
4. `addAncestorsWithLayout` 从被改的 cell **向上冒泡**，把所有带 `childLayout` 的祖先收进来 → 逐个重跑布局。

三条被证实的效果（全部无需手动调用布局）：

- **折叠** `graph.foldCells(true,false,[R3])`：R3 高 100→26、`collapsed=1`；**R4 400→326、R5 510→436**；OUTER 560→486。
- **改几何**：把 R2 高改成 33、R4 改成 27（包在 `beginUpdate/endUpdate` 里）→ 位置自动重算成
  `10 / 120 / 163 / 273 / 310`。
- **改可见性**：`setVisible(R3,false)` → R4 400→290、R5 510→400。

**重排范围 = 那个 `childLayout` 容器，仅此而已。** 全程 `SIB`（OUTER 之外、位于其下方的兄弟块）
一直停在 y=660 不动 —— 与任务里第 1 条探针的结论一致。

### 1.5 谁动了、谁没动（补充实测，绝对 y）

场景：`OUTER` 是 stack 容器，`R1..R5` 是它的直接子块，`R1a/R1b…` 是各行的内容块
（即 OUTER 的孙节点）。布局排好后，点击隐藏 `R3`：

| 层级 | cell | 隐藏 R3 前 → 后 |
|---|---|---|
| **重排容器的直接子块** | R1 | 70 → 70（在 R3 之上，不动） |
| | R2 | 180 → 180 |
| | R3 | 290 → 隐藏 |
| | **R4** | **400 → 290** ← 动了 |
| | **R5** | **510 → 400** ← 动了 |
| **孙节点（行内内容块）** | R1a / R1b | 170 → 170 |
| | R2a / R2b | 280 → 280 |
| | R3a / R3b | 390 → 隐藏 |
| | **R4a / R4b** | **500 → 390** ← 跟着父容器一起动了 |
| **容器自己** | OUTER | 位置固定在 (60,60)；**高度** 560 → 450 |
| **容器之外** | SIB | 660 → 660（不动） |

**要点：子容器与子节点的位置确实会变，这正是这项能力的全部意义。** 精确的说法是：

1. **只有重排容器的「直接子块」的几何被重写**（这里是 R1..R5）；
2. 但孙节点的坐标是相对父容器的，**父一动，整棵子树跟着平移**（R4a/R4b 500→390）——
   所以观感上"整行连同内容一起让位"，正是方案二想要的效果；
3. **容器自己的位置不变**，只有尺寸会跟着 `resizeParent` 变；
4. **边界在容器上**：容器之外的东西一个都不动（SIB 660→660）。

也就是说，"能不能改变子容器/子节点的位置"——**能，而且是逐像素精确的**（见 Q3/Q4）。
不能动的是容器自身的位置、以及容器之外的元素；这也是为什么重排的作用域必须靠
构建期的容器划分来界定（见 Q5b）。


---

## Q2 接到点击上：不需要新动词

从 pinned bundle 里**逐条核实**的 custom action 动词表（`Graph.prototype.executeCustomActions`）：
`open / wait / opacity / fadeIn / fadeOut / fadeTo / flow / wipeIn / wipeOut / popIn / popOut /
toggle / show / hide / toggleStyle / style / select / highlight / scroll / viewbox / explore / tags`。
**确实没有 fold / relayout 动词**，而且 `style {key:"collapsed",value:"1"}` 只写了样式串——
`graph.isCellCollapsed()` 仍是 `false`，不渲染折叠态（实测），所以 `style` 也不是后门。

**但是不需要后门。** 因为 Q1 的触发点是「任何非空编辑事务」，而 `hide`/`show`/`toggle`
本来就走事务。点击链：

```
click → graph.customLinkClicked → handleCustomLink → executeCustomActions
      → 非 transient 时 fa() = model.beginUpdate()
      → setCellsVisible / toggleCells
      → X() = model.endUpdate() → BEFORE_UNDO → mxLayoutManager → stack.execute(OUTER)
```

（真实点击时 `transient` 默认为 `false`；canonical builder 现在发的裸 `{"toggle":{"cells":[...]}}`
就是这个形状，实测同样触发重排——**payload 形状不用改**。）

**实测（合成鼠标事件真实点击）**，基线 `R1..R5 = 70/180/290/400/510`，`OUTER=560`：

| 点击的 action | 结果 |
|---|---|
| `hide {cells:["R3"]}` | R3 消失；**R4 400→290、R5 510→400**；OUTER 560→450 |
| `show {cells:["R3"]}` | **精确回到原基线**（逐字节相等） |
| 裸 `toggle {cells:["R3"]}` | 同上，重排 + 精确还原 |
| `toggle {cells:["R2a","R2b"]}`（只隐藏行内子块，行容器尺寸不变） | 不移动（正确：stack 子块尺寸没变） |
| `style {key:"fillColor"}` | 不移动（布局确实重跑了，但结果是幂等的） |
| `style {key:"collapsed",value:"1"}` | 不折叠、不移动 |
| `viewbox {cells:["R3","R4","R5"]}` | 只改视口（scale 1→2.55），cell 不动 |

**一个必须注意的约束**：被隐藏的 cell 同时也失去了点击目标。所以"点行标题折叠它自己"
在这条路上不成立——需要标题与内容分离，见 Q5a。

---

## Q3 确定性

| 检验 | 方法 | 结果 |
|---|---|---|
| 跨页面加载 | 同一份 `probe.drawio`、同一段点击序列（布局→隐藏 R3→显示 R3→toggle R3 两次），3 次独立加载 | 序列 JSON **长度 2159、hash 938101579，三次完全相同** |
| 窗口尺寸 | 其中一次在容器 `2061×971`、一次 `0×870`、一次移动端仿真下跑 | **同上，逐字节一致** |
| 无网格吸附 | 把行高设成 33 / 27（非 10 的倍数） | 位置 `163 / 273 / 310` —— 精确整数和，**没有取整** |

原因：`mxStackLayout.execute` 的位置是 `Σ(height + spacing)` 的整数累加，
`snap()` 只在 `allowGaps=1` 时才有 `gridSize`（这里没设，是 no-op）；
父容器尺寸取自容器**自身的 geometry**（`getParentSize`），与窗口无关。
`gridSize=10` 在这条路径上不起作用。

---

## Q4 位置记忆

| 检验 | 结果 |
|---|---|
| hide R3 → show R3，**40 次循环** | `drift: null`，最终 JSON 与基线逐字节相等 |
| toggle T2 + T3，**40 次循环**（交错布局） | `drift: null` |
| fold R3 → unfold R3 | R1..R5 精确回到 70/180/290/400/510，OUTER 560 |
| 同时收起 T2/T3/T5 再全放 | 精确还原 |

**偏差量：0（整数，无浮点累积、无 padding 取整）。**

**4.4 唯一的例外：加载后的第一次重排。**

构建期按 `LANES` 摆的坐标**不是** stack 布局的不动点（probe 里初始 y=130，第一次布局后变成 70/180/…）。
所以采用方案二时，**builder 必须直接吐"已经 stack 过的坐标"**，否则读者第一次点任何东西，
整批行会跳一下。这是构建期约束，不是运行时问题。

---

## Q5 第三种做法

### 5a（推荐）：标题与内容作为**并列的 stack 子块**交错排

`probe-tc.drawio`：`OUTER2` 的 `childLayout=stackLayout`，子块按 `T1,C1,T2,C2,T3,C3,T4,C4,T5,C5`
排列——标题条（高 28，**永不隐藏**，带 toggle 自己内容的 action）与内容块（高 72）平级。

**这解决了 Q2 的"点击目标会消失"问题：标题和内容一起位移，既不错位，也一直可点。**

实测（基线 `T1..T5 = 68/180/292/404/516`，`C1..C5 = 102/214/326/438/550`，OUTER2 高 570）：

| 点击 | 结果 |
|---|---|
| T2（收起行二内容） | C2 消失；T3 292→214、C3 326→248、T4 404→326、C4 438→360、T5 516→438、C5 550→472；OUTER2 570→492 |
| T2 再点 | **精确还原**（逐字节） |
| T4 | C4 消失、T5 516→438、C5 550→472；其它行不受影响 |
| T2 + T4 同时收起 | 两者独立叠加，结果自洽（OUTER2 = 414） |
| 40 次 toggle 循环 | 零漂移 |

**代价**：一行从"1 个标题 + N 个方块"变成"2 个 cell（标题 + 内容容器）"，且必须真的嵌进容器里。

### 5b：有界重排（只动相邻几行）

重排的**作用域恒等于那个 `childLayout` 容器**。所以"有界"只能靠**构建期选择哪些 cell 进哪个容器**，
不能靠运行时。把 7 行拆成嵌套的容器（例如外层 stack = `[R1][R2][R3..R7 内层 stack]`）确实能缩小
一次重排的范围，但**断点是构建期钉死的**，不跟着"这次展开的是哪一行"走。
没有"把下方 N 行整体平移固定量"这个中间档——除非自己写运行时（本任务明确排除）。

### 5c：预烘焙多态 + layer 切换（不碰布局引擎）

`probe-layers.drawio`：`Layer:StateA`（全收起坐标）与 `Layer:StateB`（行二展开、下方行已下移的坐标）
各存一份完整行集，按钮用 `hide/show {layers:[...]}` 切换。

实测：点 STATE_A → `A=true, B=false`，几何就是预置值（StateB 里 R2 高 120、R3 y=250）；
点 STATE_B → 翻转正确。**引擎完全不参与，几何永远精确。**

代价：**每个状态复制一整套 cell**（5 行状态 = 15 个 cell），且**不能组合**——
"行一 + 行三同时展开"要另一个状态。全自由 = 2^7 = 128 个状态；只允许一行展开 = 8 个。
本质上这是"方案一多准备几套行带"，不是动态布局。

---

## 判断：值不值得用？用在什么范围？

**值得——机制是真的、干净的、确定的，而且不需要任何新平台代码、新动词或构建期随机性。**
但它的成本不在 viewer 侧，而在**构建/校验管线**和**语义**上，所以**现在不要全图替换方案一**。

支持做的证据：Q2 的点击路径完全落在现有能力内（`toggle` 就够，payload 形状都不用改）；
Q3/Q4 的确定性达到"可以继续对几何做校验"的标准（整数精确、跨加载一致、40 次循环零漂移）。

必须一起处理的代价（按重要性排）：

1. **`validate.py` 的顶点重叠检查会直接 FAIL。** 它把生成 XML 里**所有**带 geometry 的
   vertex 两两比对（`validate.py:235-253`），而容器**必然**和自己的子块重叠。
   这条护栏是专门负向测试过的，改它是一次治理事件，不是顺手改。
2. **builder 要真的吐嵌套结构**（行标题/内容块挂到 stack 容器下），并且**必须吐已经排好的坐标**
   （§Q4.4），否则首次点击会跳。
3. **骨架护栏不受影响**——`freeze_skeleton.fingerprint` 只读 `graph.json`，从不看 `.drawio`。
   只要不改 `graph.json` 里的 `parent` 字段、只在 emit 阶段加容器，就不会触发骨架漂移。
   （反过来说：如果为了嵌套去改 `graph.json` 的层级，那就真的漂移了。）
4. **行从"一条带"变成"两个 cell"**：现有的 `subtree_cells` 会按 id 列表隐藏"方块 + 所连箭头"，
   换成 5a 结构后，折叠语义变成"toggle 一个内容容器的 id"。箭头要跟着内容容器走。

**建议范围**：只做**行带这一层**，用 **5a 交错结构**，先在**行二（烘焙）**上做一个和方案一的
并排 A/B，让 Design Owner 看过再决定要不要铺到七行。理由正是骨架护栏那条注释写的：
"往①行加一块条件组、把图例换成三态，每一步单看都合理，合起来就把已对齐的结构改掉了"——
这次的两项改动（重叠护栏 + builder 嵌套）正好属于同一类。

如果 Design Owner 要的只是"收起时不留空档"而不在意"展开的动画感"，**5c 更便宜也更安全**
（不碰引擎、不动护栏），代价是 cell 数量随状态数线性增长且不能组合。

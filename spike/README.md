# FCF Canonical System Map — draw.io AI-carrier Spike

日期:2026-09-17 · 状态:**完成,Stop Rule 未触发**

**结论(一句话):draw.io / diagrams.net 可以作为 FCF Canonical System Map 的
AI-only carrier**——Source JSON → 代码生成 → 原生 Layer + custom action 交互,
全程零手工 `.drawio` 编辑,构建字节级确定,Round-trip 稳定;交互能力依赖
diagrams.net **viewer** 表面(嵌入 viewer 或 viewer.diagrams.net lightbox),
静态导出(PNG/SVG/PDF)无交互,这是唯一的实质限制。

---

## 交付物

```
spike/
├─ graph.json                 # Source of Truth①:节点 + 层级(唯一允许人改的输入之一)
├─ scopes.json                # Source of Truth②:View / scope 规则(同上)
├─ build_diagram.py           # 确定性构建器(Python 3 stdlib,无依赖)
├─ fcf-spike.drawio           # 构建产物 —— 永远不要手工编辑,改 JSON 后重新生成
├─ README.md                  # 本报告
└─ verify/                    # 测试脚手架(可整体删除,不影响 carrier)
   ├─ viewer-harness.html     #   官方 viewer 本地加载页(仅测试用)
   ├─ serve.py                #   测试静态服务器
   ├─ vendor/viewer-static.min.js   # 官方 viewer,2026-09-17 固定版本
   └─ roundtrip/              #   Round-trip 证据(v1/v2/diff/断言脚本/变更后源)
```

> harness 说明:本会话的预览启动器沙箱拒绝读取 `/Volumes/…` 卷,故测试时把
> `fcf-spike.drawio + verify/{viewer-harness.html, serve.py, vendor/}` 镜像到
> `/tmp/fcf-spike-preview/` 再起服务。普通环境下直接
> `python3 spike/verify/serve.py` 后打开
> `http://127.0.0.1:8799/spike/verify/viewer-harness.html` 即可。

快速开始:

```bash
python3 build_diagram.py        # graph.json + scopes.json -> fcf-spike.drawio
python3 verify/roundtrip/check_roundtrip.py   # 重跑 Round-trip 断言(需先重跑下方命令)
```

Round-trip 复现(生成 verify/roundtrip/ 下的 v1/v2/diff):

```bash
cp fcf-spike.drawio verify/roundtrip/fcf-spike.v1.drawio
python3 build_diagram.py --graph verify/roundtrip/graph.roundtrip.json \
  --out verify/roundtrip/fcf-spike.v2.drawio
diff -u verify/roundtrip/fcf-spike.v1.drawio verify/roundtrip/fcf-spike.v2.drawio
python3 verify/roundtrip/check_roundtrip.py
```

指纹:

| 文件 | sha256 |
|---|---|
| fcf-spike.drawio | `37972b927894bc0ce68fa199646ea28d737a343de946ae7bb4eeaeca0d27709b` |
| fcf-spike.v2.drawio(round-trip 后) | `bf248886617927c56e11ab00295dc90da087d7e73226ebe3ea92643f3c047f36` |
| viewer-static.min.js(官方 viewer) | `e49a0d5d1eac05351c3d21a22d5278fcab5d20066bdbdf074edc0b9989c611cd` |

---

## 必须测试项结果(全部 PASS)

测试方式:XML 结构断言 + **官方 viewer 运行时断言**(`verify/viewer-harness.html`
用 viewer.diagrams.net 的 `viewer-static.min.js` 原样加载生成的 `.drawio`,
对 mxGraph model/view 做程序化断言,并用合成鼠标事件真实点击触发 custom action)。

| # | 要求 | 结果 | 证据 |
|---|---|---|---|
| 1 | 完全通过代码生成 .drawio | PASS | 构建器 501 行纯 stdlib;`.drawio` 126 行未压缩 XML,无任何手工编辑 |
| 2 | 图元有稳定 ID | PASS | cell id == node id(`SPATIAL.BASE` 等);跨视图灰色副本带 `::0.3.4.0` 后缀 |
| 3 | Spatial Opportunity 可展开/收起 | PASS | 点击 SPATIAL 框:4 子节点 + 4 边全部 not-rendered;再点击全部恢复;viewer model 中 per-cell visible 翻转 |
| 4 | Overall / 0.3.4.0 两个交互 View | PASS | 两个 view 按钮(native custom action);layer 可见性精确翻转(见下) |
| 5 | 0.3.4.0 中 Spatial 正常、其余置灰保留 | PASS | 运行时:灰色副本 rendered,彩色副本 not-rendered;灰样式 `fillColor=#f5f5f5 / stroke=#a6a6a6 / fontColor=#8f8f8f`;SPATIAL 子树与 SYS.FCF 不受影响 |
| 6 | 尽量用原生 Layer / custom action / viewer interaction | PASS | 仅用:native layers(4 层)、layer 初始 `visible="0"`、`data:action/json` 链接、viewer 的 chromeless 点击执行链 |
| 7 | 不允许用户手工绑 Action | PASS | action 链接由构建器以 `<UserObject link=…>` 自动注入;用户零操作 |

### 关键运行时断言(官方 viewer,逐字摘录)

初始(Overall,默认视图):

```
layers: { overall: true, v034: false }          # XML 里的初始 layer 可见性被尊重
CONDITION / RESPONSE / SELECTION: rendered      # 彩色版
CONDITION::0.3.4.0 等: not-rendered            # 灰副本未渲染
graphEnabled: false                             # chromeless 模式 → 点击执行 custom action
```

点击 `0.3.4.0` 按钮后:

```
layers: { overall: false, v034: true }
CONDITION/RESPONSE/SELECTION: not-rendered; *::0.3.4.0: rendered
SPATIAL.BASE / SPATIAL.FACTOR / SYS.FCF: rendered   # Spatial 相关不受影响
灰副本 state.style: fillColor=#f5f5f5, strokeColor=#a6a6a6, fontColor=#8f8f8f
```

点击 SPATIAL 框(在 0.3.4.0 视图内)后,再切回 Overall:

```
afterCollapse: 4 个子节点 + 边 not-rendered,SPATIAL 框本身 rendered
afterSwitchBack: layers 翻转正确;彩色版恢复 rendered;灰版 not-rendered;
                子节点仍 not-rendered   ← 折叠状态跨视图保持(layer 翻转与
                                          per-cell 折叠正交,这是本设计的核心性质)
```

---

## Round-trip 测试:PASS

源变更(`verify/roundtrip/graph.roundtrip.json`):

- `SPATIAL.FACTOR` label:`Factor Evaluate` → `Atomic Factor Evaluation`
- 追加节点 `SPATIAL.DEBUG / Debug Trace`(scopes.json 未改)

重新生成后 `check_roundtrip.py` 输出:

```
ROUND-TRIP: PASS
  stable ids: 41/41 survived unchanged
  new ids (expected only): ['E:SPATIAL->SPATIAL.DEBUG', 'SPATIAL.DEBUG']
  SPATIAL.DEBUG auto-placed on layer: Layer:ViewOverall
  SPATIAL.DEBUG slot (appended, nothing moved): x=1080,y=360,width=200,height=50
  label mutation: SPATIAL.FACTOR -> 'Atomic Factor Evaluation' (id/geometry untouched)
```

即:未修改节点 Stable ID 不变;布局零移动(DEBUG 落在追加槽位);Scope 规则自动
生效(DEBUG 按 prefix 规则只进 Overall 层,viewer 里实测:Overall 渲染、
0.3.4.0 隐藏);SPATIAL 的折叠 payload 自动纳入新节点;全程无人工改 `.drawio`。
diff 全文仅 40 行:1 处 label、3 行新节点、3 行新边、1 行折叠 payload 追加。

## Determinism 测试:PASS(字节级一致)

同一 Source 连续构建 2 次 + 与在位产物比对 + round-trip 源重建比对,
`cmp` 全部通过,无任何 metadata diff——构建器不写时间戳/UUID/随机数,
`mxfile` 的 `host/agent/version` 与 `mxGraphModel` 的 `dx/dy` 等均为固定常量。

注意:若有人用 draw.io **App** 打开并保存,App 会重写文件(压缩、`modified`/
`agent` 时间戳)。这不影响本管线——`.drawio` 是一次性产物,永远从 JSON 重建。

---

## draw.io 原生能做到什么(本 spike 实测 + 源码确认)

以下均从官方 `viewer-static.min.js` 源码逐条核实,非文档转述:

1. **Layer 即视图载体**:layer cell 持久化 `visible="0"`;viewer 加载时尊重;
   原生 Layers 面板(嵌入 viewer 的 `toolbar:'layers'`)可手动切换——备用的
   无代码交互路径。
2. **Custom actions**:`<UserObject link="data:action/json,{…}">` 挂在任意图元上,
   chromeless viewer 中**单击即执行**(`click → getClickableLinkForCell →
   customLinkClicked → handleCustomLink → executeCustomActions`,viewer 还会在
   bounds 变化后自动 re-crop 重新取景)。
   已核实的 action 动词:`show / hide / toggle / style / toggleStyle / select /
   highlight / scroll / viewbox / tags / explore / open / wait / opacity /
   fadeIn / fadeOut / fadeTo / wipeIn / wipeOut / popIn / popOut / flow`;
   选择器键:`cells / layers / tags / descendants / excludeCells`(按 cell id 精确匹配)。
3. **`show/hide` 一个 layer cell id 只翻转该 layer 自身可见性**,与逐 cell 的
   `toggle`(折叠)正交组合——本 spike 的双视图 + 折叠共存正是靠这一点。
4. **`viewbox` action** 可点击后自动缩放到某组 cells/layers/tags——未来做
   "聚焦某分支"不需要任何新机制。
5. **`tags` + `tagsMatch`**:还有一套基于标签的可见性机制(hiddenTags),
   可作为 layer 之外的另一条 scope 路线(spike 未用,记录备查)。
6. **页面导航**:`open: "data:page/id,…"` 可从 custom action 跳页——多页
   (每视图一页)方案原生可行,本 spike 选了单页 + layer(切换不换页,状态共享)。

## 做不到 / 限制(如实)

1. **交互只活在 viewer 表面**:嵌入 viewer-static / viewer.diagrams.net
   lightbox(及基于同一 viewer 的 Confluence/Jira/Drive 预览)有效;
   **导出 PNG/SVG/PDF 后交互消失**(灰化副本方案可让静态导出按当前激活层
   导出对应视图,算部分缓解)。
2. **draw.io 编辑器 App 里普通点击是选中**,不是执行 action(editor 需通过
   link 覆盖角标/Ctrl+点击)。但本管线的用户根本不打开编辑器,只看 viewer,
   所以不构成阻碍——只是不能把"编辑器当播放器"用。
3. **交互状态不持久**:视图切换/折叠是会话态,刷新回到默认视图(Overall)。
   对"AI 生成、人只读"的定位反而正确:状态不回写,产物永不脏。
4. **灰化 = 重复实例**:置灰视图为每个灰节点生成 `::view` 后缀副本(同坐标、
   灰样式)。图很大时副本线性增长;原生 `style` action 可原地改样式、免副本,
   spike 未启用(保持"绝对状态切换"语义,避免 style 叠加还原问题)。
5. **手动把两层同时打开**(原生 Layers 面板)会出现彩色版与灰版同坐标重叠
   ——面板允许任意组合,这是 feature 的副作用;按按钮切换单视图永远干净。
6. **布局是固定容量网格**:每个分支区 5 个子槽;追加稳定(本轮实测),但
   "在中间插入"会把后续兄弟右移一格;超过容量构建器会 warning。

## 是否仍需要人工 UI?

**不需要。**
- 查看/交互:打开 viewer(嵌入页或 viewer.diagrams.net)即可,点击即用;
- 修改:改 `graph.json` / `scopes.json` → `python3 build_diagram.py`,AI 或人
  都可以,产物不入库手工修改;
- 唯一的"人工"是可选的:原生 Layers 面板手动切层(备用路径,非必需)。

## Source → Build → Diagram 是否稳定?

**稳定,且是本 spike 最强的结论**:字节级确定性构建 + Stable ID + 追加式
布局稳定 + scope 规则自动重排,Round-trip diff 最小化(40 行,全部可解释)。
`.drawio` 在本管线中的角色与编译产物 `.o` 相同。

## 补充实验:原生容器(section/group)在 viewer 里的折叠性

问题:折叠是否只适用于"脑图/树状"布局?把元素放进真正的 drawio
section/group(`swimlane` / `container=1;collapsible=1`,子图元 parent 挂组下)
能否在 viewer 里直接点折叠?

实测(`verify/container-test.drawio` + `verify/container-test.html`,官方 viewer):

| 操作 | 结果 |
|---|---|
| 单击 / 双击 swimlane 标题(chromeless viewer) | **不折叠**(`isCollapsed` 保持 false) |
| 单击 collapsible rect group 标题 | **不折叠** |
| 编程调用 `foldCells(true)`(等价于 XML 预置 `collapsed="1"`) | **正常渲染折叠态**:容器缩成标题条(260→32px),子元素隐藏,可恢复 |

结论:折叠机制与布局形态无关——本 spike 的折叠是 custom action 按**任意
cell ID 集合**切换可见性,不要求树状、不要求 mxGraph 父子关系;drawio 原生
容器折叠只在**编辑器**里可交互,viewer 的点击只走 custom action 链,而
action 动词表(见上)没有 fold 动词,故原生容器折叠无法在 viewer 里被点击
触发(viewer 的渲染管线本身支持折叠态,可用 XML 预置)。若正式图要
section 化:builder 生成 section 背景框(可选真容器)+ 折叠统一走 toggle
custom action;树形 `shape=tree` 是 viewer 里支持点击折叠的原生例外
(源码证据 `foldTreeCell`,未实测)。另注意:任何机制折叠后**周边元素都不会
自动让位**(无全局 reflow),"收拢"效果需 builder 预排或用 `viewbox` action
联动缩放视口。

## Stop Rule 检查

**未触发。** 为实现 Scope Toggle,零行平台代码:`verify/` 只是加载**官方**
viewer 的测试脚手架(harness 页 ~60 行,引 pinned 的 viewer-static.min.js),
可整体删除而不影响 carrier。没有任何"为了让测试通过"而开发的 Diagram Platform。

## 是否适合 FCF 正式图?

**适合,附带三个前提:**

1. **消费表面锁定 viewer 系**(嵌入 viewer-static 或 viewer.diagrams.net),
   并 pin viewer 版本(本报告 sha256 已 pin;action 能力集随版本演进,
   升级需回归本 spike 的断言);
2. **SoT 永远是 JSON**(`graph.json` + `scopes.json`),`.drawio` 永远是产物,
   任何人不经管线直接改 `.drawio` 视为违规(文件头部的 CTRL:TITLE 也写了);
3. 图规模显著增长时,评估用原生 `style` action 替代灰化副本(去重实例),
   以及用 `viewbox` action 做"分支聚焦"——都在原生能力内,不需要新平台。

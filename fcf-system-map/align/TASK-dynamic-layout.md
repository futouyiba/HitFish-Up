# 任务：探索「展开/折叠时的动态重排」是否可行 —— draw.io 布局引擎实验

## 背景

我们在做 **FCF Canonical System Map（中鱼机制总图）**，用 draw.io 作为载体，
source 是 JSON、`.drawio` 是确定性构建产物。仓库与基础设施见文末。

图的骨架是 **7 行**（六步 + 范围外），自上而下。每行是一个可折叠单元，
点行标题可以收起/展开该行内容。现在要往里加**中下层细节**，于是出现一个矛盾：

- **当前做法（方案一，已选定为主线）**：每行预留固定的"行带"，展开只是切换可见性。
  好处：**任何位置永不移动**。代价：折叠起来时行带里空着，页面显得稀疏
  （我们打算用一块大的"封面块"填住行带缓解）。
- **待验证做法（方案二，本任务）**：用 draw.io 的布局引擎做动态重排——
  展开一行时，下面的行自动下移；收起时自动上移。好处：没有空档。
  代价：每次展开/收起都有整体位移。

**Design Owner 想看方案二到底能不能做、做得干不干净**，再决定要不要采用或部分采用。

## 我已经做过的探针（不要重复做）

1. **真容器 + `childLayout=stackLayout` + `collapsible=1`，在 chromeless viewer 里
   用 `graph.foldCells(true,false,[cell])` 折叠** →
   - 容器自身从 260 高缩到 26，它的**直接子块自动重排**（子块 state 变为 null，被隐藏）；
   - 但**容器之外、位于它下方的另一个模块 y 坐标完全没动**（400 → 400）。
   结论：布局引擎只整理容器自己的内部，不会让整张图重排。

2. **viewer 里点击容器不会折叠**（早前探针）：viewer 的点击走 custom action 链，
   而 action 动词表里没有 fold 动词。所以要让用户能触发折叠，只能靠 custom action
   切可见性，或者找到一个把 `foldCells` 接进点击路径的办法。

3. **画布是无界的**：在 x=4200（页宽只有 1700）注入方块，正常渲染，图形边界扩到 4342。
   `pageVisible=false`。页只是打印/导出参考矩形。

## 请你验证的问题

**Q1｜能不能让"展开一行 → 下面的行自动让位"在 viewer 里跑起来？**
外层容器 + `childLayout`（stackLayout / 其它）能否让 7 个行容器作为一个整体重排？
如果能，是**在什么事件上触发**的（BEGIN_UPDATE？折叠？还是必须手动跑布局）？

**Q2｜触发路径能不能接到用户点击上？**
viewer 的 custom action 词汇表里没有 fold/relayout 动词。有没有别的路子——
比如 `open` 一个 `data:page/...`、`tags` 隐藏、或者某种能间接触发 model 变更的动作，
会被 `mxLayoutManager` 捕获并重排？

**Q3｜重排的确定性如何？**
同一份 `.drawio`、同一个 viewer 版本，两次展开同一行，位置是否逐像素一致？
不同窗口尺寸下呢？这关系到我们能不能继续对几何做校验。

**Q4｜重排会不会破坏"折叠态"的位置记忆？**
具体说：展开 A、再收起 A，其它块是否精确回到原位？如果只是近似（比如浮点累积、
或者 stackLayout 的 padding 取整），请给出实测的偏差量。

**Q5｜有没有第三种做法？**
比如：只重排**相邻的两行**而不是全部；或者用"展开时把自己下方 N 行整体平移一个固定量"
这类**有界**的动态布局——既避免空档，又不让整图抖动。请一并评估。

## 约束（务必遵守）

- **不要为这件事开发新的画图平台 / Web App。** 这是能力验证，不是产品开发。
- 现有产物是**确定性构建**的（无时间戳 / UUID / 随机数，同 source 两次构建逐字节一致）。
  任何方案如果要求构建期引入随机性或时间依赖，直接判为不可行。
- 图上的**中文字段是硬要求**；英文只作副标题。
- 骨架冻结在最初对齐草图 v1（见 `fcf-system-map/skeleton.baseline.json`）。
  你可以做实验副本，但**不要改 canonical 的 `graph.json` 拓扑**。

## 交付

一份简短报告，回答 Q1–Q5，每条附**可复现的实验步骤与实测数据**（不要只给结论）。

明确给出判断：**方案二值不值得用？如果值得，用在什么范围？如果不值得，卡在哪一步？**

## 仓库与基础设施

分支：**`fcf-map-canonical`**（无 remote，直接从本仓取该分支即可）

```
fcf-system-map/
├─ graph.json / scopes.json / views.json / contracts.json   # source（勿改拓扑）
├─ skeleton.baseline.json      # 冻结的骨架指纹
├─ build/
│  ├─ build_diagram.py         # 确定性构建器（JSON -> .drawio）
│  ├─ validate.py              # 校验：ID唯一/边端点/scope归类/无环/确定性/改名稳定/
│  │                           #       中文标签/顶点重叠/骨架漂移/页面容纳
│  ├─ freeze_skeleton.py       # 需要改骨架时才运行
│  └─ viewer-harness.html      # 官方 viewer 加载页（自带稳健适配，可作模板）
├─ tools/preview.py            # 常驻预览：改 source 后自动重建 + 页面自动刷新
├─ generated/fcf-system-map.drawio
└─ align/                      # 对齐草图与本次的方案二草图（throwaway）
```

跑起来：

```bash
python3 fcf-system-map/build/build_diagram.py
python3 fcf-system-map/build/validate.py
python3 fcf-system-map/tools/preview.py        # 然后浏览器打开它打印的地址
```

viewer 是**官方 pinned 版本**：`spike/verify/vendor/viewer-static.min.js`。
早前对它的 custom action 词汇表的核实结论在 `spike/README.md`。

## 参考：方案一在这张图上的样子

行 2「烘焙」的三层展开模型（三块面板对照 L0 / L1 / L2）：
`fcf-system-map/align/expand-view.html` + `expand_model.py`。

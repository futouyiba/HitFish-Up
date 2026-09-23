#!/usr/bin/env python3
"""FCF Canonical System Map — deterministic draw.io builder (Production Pilot v0.1).

Inputs (semantic source, hand/AI-editable):
    graph.json     nodes (stable IDs, hierarchy, lanes) + explicit semantic edges
    layout.json    版面：容器包纳树（C: 前缀的容器 + graph.json 节点作叶子）
    scopes.json    lens scopes (OVERALL / 0.3.4.0) with ACTIVE/BOUNDARY/OUT classes
    views.json     view presets (expansion granularity + optional scope lens)
    contracts.json thin diagram-node -> authority links (validated only)

Output (build artifact, never hand-edit):
    generated/fcf-system-map.drawio

Design invariants (Production Pilot v0.1):
  * ONE cell per semantic node, ever. Scope coloring is a native `style`
    custom-action pass on those same cells — no duplicated instances, no
    scope x view layer multiplication (`::-suffixed` copies are banned).
  * Three orthogonal dimensions:
      Hierarchy  — 版面容器（layout.json）互相包纳，由 draw.io 的布局引擎在
                   每次编辑事务后重排：展开一层，下面的层自动让位。
      Scope      — per-node ACTIVE/BOUNDARY/OUT class; applied only as
                   fillColor/strokeColor/fontColor/dashed style changes.
                   OUT nodes are grayed, never hidden.
      View       — expansion presets; buttons that change visibility never
                   change styles and vice versa.
  * 版面硬规则（探针 P3 实测 + 后续独立复核）：引擎从不重算**水平**容器的高度，
    也不会让它自己定宽 —— 宽度只能有一个来源（父容器的 fill），否则两边互相覆盖，
    发出来的坐标就不是不动点了。所以「展开时要推动下方」的东西必须是垂直容器里的
    兄弟；水平容器的高度与宽度都在发射时按父容器定死。
    见 align/dynlayout/REPORT-dynamic-layout.md 的探针 P3。
  * Deterministic: fixed constants, fixed emission order, no timestamps,
    uuids or randomness. Same sources -> byte-identical output.
  * Only native draw.io mechanisms: layers (controls/main), custom-action
    links (`data:action/json,{...}`) verified against the pinned official
    viewer (see spike/README.md for the verified action vocabulary).

Regenerate:
    python3 build/build_diagram.py
Validate:
    python3 build/validate.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


GRAY_FILL, GRAY_STROKE, GRAY_FONT = "#f5f5f5", "#a6a6a6", "#8f8f8f"

# 形状 / 配色按节点的 kind 字段决定（回到 v1 的图例）：
#   数据 / 配置   -> 平行四边形
#   派生数据      -> 立方体（派生环境场的专用图例）
#   过程 / 模块   -> 圆角矩形
#   范围外        -> 灰色虚线圆角矩形
KIND_STYLE = {
    "data":    ("shape=parallelogram;perimeter=parallelogramPerimeter;size=18;", "#dae8fc", "#6c8ebf"),
    "cube":    ("shape=cube;size=20;", "#dae8fc", "#6c8ebf"),
    "process": ("rounded=1;", "#ffe6cc", "#d79b00"),
    "l1":      ("rounded=1;", "#fff7e6", "#d79b00"),
    "core":    ("rounded=1;strokeWidth=2;", "#d5e8d4", "#2d6a4f"),
    "sec":     ("rounded=1;dashed=1;", "#fff2cc", "#d6b656"),
    "skip":    ("rounded=1;dashed=1;", "#f5f5f5", "#aaaaaa"),
    "gate":    ("rhombus;whiteSpace=wrap;html=1;", "#f8cecc", "#b85450"),
    "end":     ("rounded=1;arcSize=50;strokeWidth=2;", "#dae8fc", "#6c8ebf"),
    "factor":  ("rounded=0;", "#dae8fc", "#6c8ebf"),
    # 因子：**形状代表类别**（照 Design Owner 2026-09-23 给的参照 SVG），
    # 名字写回框上。所以这三个不再是"图标"，而是带形状样式的普通格子。
    "fcore":   ("shape=hexagon;perimeter=hexagonPerimeter;size=26;", "#dbeafe", "#2563eb"),
    "fsec":    ("shape=ellipse;", "#dcfce7", "#16a34a"),
    "fskip":   ("rounded=1;dashed=1;", "#f8fafc", "#94a3b8"),
    "outside": ("rounded=1;dashed=1;", "#f5f5f5", "#a6a6a6"),
    "group":   ("rounded=1;dashed=1;strokeWidth=1;", "#fcfcfc", "#bbbbbb"),
    "gtitle":  ("rounded=0;", "#eeeeee", "#999999"),
}
DEFAULT_KIND = "process"
# kind 基线里自带描边宽度的那些（clear 还原时要按它写回去，不能一律写成 1）。
# 从 KIND_STYLE 推出来，避免两处各写一份而漂移。
KIND_STROKE_W = {}
for _k, (_base, _fill, _stroke) in KIND_STYLE.items():
    _i = _base.find("strokeWidth=")
    KIND_STROKE_W[_k] = _base[_i + 12:].split(";")[0] if _i >= 0 else "1"
# 版面容器：**按嵌套深度给深浅不同的实线边**，让"谁包着谁"一眼看得见。
# 不留底色，避免盖住方块。深度从 0（根）往下。
CONTAINER_STROKE_BY_DEPTH = (
    "none",      # 根：不画
    "#9fb4c7",   # 行
    "#b9c9d8",   # 行内带
    "#d0dbe5",   # 更深一层
)
CONTAINER_STROKE_DEEP = "#dde5ec"
# 标题条（行标题 / 分组标题）：左对齐加粗，压低体量，便于一眼看出这是可点的把手。
TITLE_FILL, TITLE_STROKE, TITLE_FONT = "#f6f9fc", "#a8bccd", "#2b4a63"
TITLE_EXTRA = ("align=center;verticalAlign=middle;fontSize=12;fontStyle=1;")

EDGE_BASE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;jettySize=auto;orthogonalLoop=1;strokeWidth=1.5;"
)
EDGE_TYPES = {
    "DATA_FLOW": {"dashed": "", "arrow": "block", "dashPattern": ""},
    "CONTROL_OR_SELECTION": {"dashed": "dashed=1;", "arrow": "block", "dashPattern": ""},
    "REFERENCE_OR_CONFIG": {"dashed": "dashed=1;", "arrow": "open", "dashPattern": "dashPattern=1 4;"},
    "RETENTION": {"dashed": "", "arrow": "block", "dashPattern": "", "color": "#2d6a4f"},
    "ANCHOR": {"dashed": "dashed=1;", "arrow": "open", "dashPattern": "dashPattern=1 3;", "color": "#b03a2e"},
}

DIRS = {
    "N": (0.5, 0), "S": (0.5, 1), "E": (1, 0.5), "W": (0, 0.5),
    # 四个角也给出来：多路汇进同一个框时（如两个因子汇进门控、两路汇进聚合），
    # 各自钉在框的一个角上，线才不会叠在最后一段上。
    "NW": (0, 0), "NE": (1, 0), "SW": (0, 1), "SE": (1, 1),
}

LENS_EDGE_GRAY = "#a6a6a6"


def xesc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def style_of(kind):
    return KIND_STYLE.get(kind, KIND_STYLE[DEFAULT_KIND])


def node_style(kind, role=None):
    if role == "title":
        return ("rounded=0;whiteSpace=wrap;html=1;fontColor=%s;"
                "fillColor=%s;strokeColor=%s;strokeWidth=2;%s"
                % (TITLE_FONT, TITLE_FILL, TITLE_STROKE, TITLE_EXTRA))
    base, fill, stroke = style_of(kind)
    extra = ""
    if kind == "group":
        extra = "align=center;verticalAlign=middle;fontSize=12;fontColor=#555555;"
    elif kind == "gtitle":
        extra = "fontSize=11;fontColor=#555555;fontStyle=1;"
    return (base + "whiteSpace=wrap;html=1;fontSize=12;fontColor=#000000;"
            "fillColor=%s;strokeColor=%s;%s" % (fill, stroke, extra))


def action_link(payload):
    return "data:action/json," + json.dumps(payload, separators=(",", ":"))


# ---------------------------------------------------------------- loading ----

def load_sources(root):
    src = {}
    for name in ("graph", "scopes", "views", "contracts"):
        with open(root / ("%s.json" % name), "r", encoding="utf-8") as f:
            src[name] = json.load(f)
    return src


# ---------------------------------------------------------------- layout ----
# 版面来自 layout.json 的「包纳树」：内部节点是容器（C: 前缀，带 childLayout），
# 叶子是 graph.json 的节点。几何必须与 mxStackLayout 的首轮结果逐像素一致，
# 否则首次点击时整批行会跳（见 align/dynlayout/REPORT-dynamic-layout.md）。
#
# 硬规则（探针 P3 实测）：引擎从不重算**水平**容器的高度，也不让它自己定宽。
# 宽度只能有一个来源 —— 父容器的 fill —— 所以水平容器一律 resizeParent=0、
# 按父容器内宽发射；重排只能沿「垂直容器的连续链」向上传播。

# 矢量图标：layout.json 里写 {"icon": "triangle"}，发成一个无文字的图形 cell。
# 用图形代替"方块/三角/六边形/圆"这些**文字**——那本来就是形状，写名字反而绕。
ICON_SHAPES = {
    "square":   ("rectangle;", "#dae8fc", "#6c8ebf"),
    "triangle": ("triangle;direction=north;", "#dae8fc", "#6c8ebf"),
    "hexagon":  ("hexagon;", "#d5e8d4", "#82b366"),
    "circle":   ("ellipse;", "#d5e8d4", "#82b366"),
    "hexagon-off": ("hexagon;dashed=1;", "#f5f5f5", "#aaaaaa"),
}
ICON_SIZE = 30
ICON_PREFIX = "I:"

LEAF_W = {
    "data": 260, "l1": 250, "process": 260, "cube": 260, "outside": 260,
    "group": 300, "core": 190, "sec": 190, "skip": 190, "gate": 130,
    "end": 300, "factor": 40, "fcore": 210, "fsec": 150, "fskip": 200,
}
DEFAULT_LEAF_W = 240
ROOT_X, ROOT_Y = 40, 150
# 控件区硬编码坐标占用的最小页宽（图例 y=底部那排，最右一格到 x=1370）。
CONTROLS_MIN_W = 1410
# 绕行边的"先纵向挪出横带"留白（像素）。
ROUTE_GUTTER = 20


def load_layout(root):
    with open(root / "layout.json", "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_layout(lay, nodes):
    """把 layout.json 的 ref 展开成实树，并校验「每个节点恰好出现一次」。"""
    by_id = {n["id"]: n for n in nodes}
    containers = lay["containers"]

    def build(spec, cid, parent, axis):
        kids = []
        for ch in spec.get("children", []):
            # `"node"` 先判：`{"node": "R2.C1.F1", "icon": "square"}` 是「把某个
            # **语义节点**画成图形」，而 `{"icon": "square"}` 是纯装饰图形。
            if "node" in ch:
                if ch["node"] not in by_id:
                    sys.exit("error: layout.json 引用了 graph.json 里没有的节点 %r"
                             % ch["node"])
                leaf = {"kind": "leaf", "id": ch["node"], "spec": ch,
                        "parent": cid}
                if ch.get("icon"):
                    # 形状即因子：cell id 仍是节点 id，所以边照样能接上去，
                    # 只是不写字。
                    if ch["icon"] not in ICON_SHAPES:
                        sys.exit("error: layout.json 用了未知图标 %r" % ch["icon"])
                    leaf["icon"] = ch["icon"]
                kids.append(leaf)
            elif "icon" in ch:
                if ch["icon"] not in ICON_SHAPES:
                    sys.exit("error: layout.json 用了未知图标 %r" % ch["icon"])
                icon = {"kind": "leaf", "id": ICON_PREFIX + cid + "/" + str(len(kids)),
                        "spec": ch, "parent": cid, "icon": ch["icon"]}
                kids.append(icon)
            elif "ref" in ch:
                if ch["ref"] not in containers:
                    sys.exit("error: layout.json 引用了未定义的容器 %r" % ch["ref"])
                spec2 = containers[ch["ref"]]
                sub = build(spec2, ch["ref"], cid, spec2.get("axis", "v"))
                sub["spec"] = spec2                  # 容器自己的定义
                sub["when"] = ch.get("when")         # 引用处决定的可见性
                kids.append(sub)
            else:
                sys.exit("error: layout.json 的子项既非 node 也非 ref: %r" % (ch,))
        node = {"kind": "container", "id": cid, "axis": axis,
                "indent": spec.get("indent", 0), "spec": spec,
                "children": kids, "parent": parent}
        if "border" in spec:          # 容器可自带 border（贴边壳是 0）
            node["border"] = spec["border"]
        return node

    root = build(lay["root"], "C:ROOT", None, lay["root"].get("axis", "v"))

    # 垂直栈会把**每个子块撑满容器内宽**（引擎的 fill 行为；它和 resizeParent 由
    # 同一个开关控制，没法单独关掉）。所以想保住块自己的宽度，就不能让它当垂直栈的
    # 直接子块：给它套一层「贴边壳」—— border=0、不画边、不重算尺寸的水平容器。
    # 壳被撑满（无所谓，它没有边），块在壳里按自身宽度左对齐；壳高 = 块高，所以
    # 父容器算出来的高度一点没变，重排链也不受影响。
    # 例外：`role: title` 的标题条本来就要通栏；`fill: true` 是显式要求撑满；
    # `pin` 的侧钉子块不进栈，压根不会被撑。
    def wrap(node):
        if node["kind"] != "container":
            return
        for c in node["children"]:
            wrap(c)
        if node["axis"] != "v":
            return
        out = []
        for c in node["children"]:
            if (c["kind"] == "leaf" and not c["spec"].get("skip")
                    and not c["spec"].get("fill")
                    and not c["spec"].get("pin")):
                wid = "C:W:" + c["id"]
                if wid in containers:
                    sys.exit("error: 贴边壳 id %r 与 layout.json 里声明的容器重名，"
                             "请给那个容器改个 id" % wid)
                c["parent"] = wid
                out.append({"kind": "container", "id": wid, "axis": "h",
                            "indent": 0, "border": 0, "bare": True,
                            "spec": {"when": when_of(c)},
                            "children": [c], "parent": node["id"]})
            else:
                out.append(c)
        node["children"] = out
    wrap(root)
    seen = {}

    def count(n):
        # 每个叶子都登记一次 —— 包括画成矢量图形的**语义节点**（它们也是叶子，
        # 只是不写字）。纯装饰图标（`I:` 前缀）登记进来无害：`miss` 只查 graph
        # 里的节点 id，`dup` 也只会被真正出现两次的 id 触发。
        if n["kind"] == "leaf":
            seen[n["id"]] = seen.get(n["id"], 0) + 1
        for c in n.get("children", []):
            count(c)
    count(root)
    dup = sorted(k for k, v in seen.items() if v > 1)
    miss = sorted(n["id"] for n in nodes if n["id"] not in seen)
    if dup or miss:
        sys.exit("error: layout.json 覆盖不全 —— 重复 %r / 缺失 %r" % (dup, miss))
    return root


def layout_ctx(lay, graph, views, root):
    """可见性 + 尺寸上下文。

    容器的折叠态由 default view 决定：它的**标题节点**出现在 expansion.expand 里
    就是展开态，否则折叠态。子项的 `when` 与之匹配时才在初态可见。
    """
    spec = next(v for v in views["views"] if v["id"] == views["defaultView"])
    expanded = set((spec.get("expansion") or {}).get("expand", []))

    by_cid = {}

    def index(n):
        by_cid[n["id"]] = n
        for c in n.get("children", []):
            index(c)
    index(root)

    def state_of(cid):
        """容器当前的折叠态 = **最近的、有标题的**祖先的状态。

        自己没标题的容器（比如贴边壳）不构成一个折叠层，态要沿祖先链找上去；
        否则它的子块 `when` 永远匹配不上，会被当成不可见。
        """
        node = by_cid.get(cid)
        while node is not None:
            t = title_leaf_of(node)
            if t is not None:
                return "expanded" if t["id"] in expanded else "collapsed"
            node = by_cid.get(node["parent"]) if node["parent"] else None
        return None

    def visible(child):
        if child["spec"].get("skip"):
            return False
        """一个子块只有在**自己与全部祖先**的折叠态都匹配时才可见。
        只查自己那一层是不够的：被收起的容器里的子孙虽然没写 `when`，
        也一起不可见，否则它们会按展开态坐标发出去。"""
        node = child
        while node is not None:
            when = when_of(node)
            if when is not None and when != state_of(node["parent"]):
                return False
            node = by_cid.get(node["parent"]) if node["parent"] else None
        return True

    return {
        "border": lay["border"], "spacing": lay["spacing"],
        "titleH": lay["titleH"], "titleW": lay["titleW"], "leafH": lay["leafH"],
        "kinds": {n["id"]: n.get("kind", DEFAULT_KIND) for n in graph["nodes"]},
        "labels": {n["id"]: n.get("label", "") for n in graph["nodes"]},
        "visible": visible, "state_of": state_of, "expanded": expanded,
    }


def natural_w(node, ctx):
    if node["kind"] == "leaf":
        kind = ctx["kinds"].get(node["id"], DEFAULT_KIND)
        return (node["spec"].get("w") or LEAF_W.get(kind, DEFAULT_LEAF_W))
    b, sp = border_of(node, ctx), ctx["spacing"]
    laid = [c for c in node.get("children", [])
            if ctx["visible"](c) and not c["spec"].get("pin")]
    if not laid:
        return 2 * b + node["indent"]
    if node["axis"] == "h":
        return (2 * b + node["indent"] + sum(natural_w(c, ctx) for c in laid)
                + sp * (len(laid) - 1))
    return 2 * b + node["indent"] + max(natural_w(c, ctx) for c in laid)


def title_leaf_of(container):
    """容器的标题叶子。标题也会被套进贴边壳（它不再通栏了），所以要看穿那一层。"""
    for c in container.get("children", []):
        if c["kind"] == "leaf" and c["spec"].get("role") == "title":
            return c
        if c.get("bare"):
            for g in c.get("children", []):
                if g["kind"] == "leaf" and g["spec"].get("role") == "title":
                    return g
    return None


def when_of(node):
    """子块在引用/定义处的可见性条件。叶子把 spec 存成子项对象，容器存成容器定义，
    引用处还可能覆盖 —— 两处都要认。"""
    return node.get("when") or node["spec"].get("when")


def border_of(node, ctx):
    return node.get("border", ctx["border"])


def measure(node, forced_w, ctx):
    """自底向上算尺寸、自顶向下落局部坐标（相对父容器左上角）。

    容器的高度/宽度只由**初态可见**的子块决定（发射出来的几何就是布局引擎的
    首轮不动点）。初态不可见的子块照样要发出去（带 visible="0"），所以也得给
    它们一组坐标 —— 顺排在可见内容之后，仅供存储，引擎在它们变可见时会重排。
    """
    b, sp = border_of(node, ctx), ctx["spacing"]
    if node["kind"] == "leaf":
        if node["spec"].get("role") == "title":
            # 标题条只占固定宽度，不再被父容器的 fill 撑成横贯整行的长色框。
            # **不能用字数推算宽度** —— 那样改一个 label 就会改几何，
            # 重命名稳定性检查（cell 几何在改名后不得变动）会立刻报错。
            # 容器可以显式再收窄（如「环境聚合」：宽了会横在进聚合的连线前面）。
            node["_w"] = node["spec"].get("w") or ctx["titleW"]
            node["_h"] = ctx["titleH"]
            return
        if node.get("icon"):
            node["_w"] = ICON_SIZE
            node["_h"] = ICON_SIZE
            return
        kind = ctx["kinds"].get(node["id"], DEFAULT_KIND)
        node["_w"] = (forced_w or node["spec"].get("w")
                      or LEAF_W.get(kind, DEFAULT_LEAF_W))
        node["_h"] = (node["spec"].get("h")
                      or (ctx["titleH"] if node["spec"].get("role") == "title"
                          else ctx["leafH"].get(kind, 44)))
        return
    kids = [c for c in node["children"] if not c["spec"].get("pin")]
    vis = [c for c in kids if ctx["visible"](c)]
    hid = [c for c in kids if not ctx["visible"](c)]
    ind = node["indent"]
    if node["axis"] == "h":
        # 贴边壳（wrap() 造的那层，border=0、无边框）：只有一个子块。壳的宽度由父容器
        # 给（引擎也会把它撑满，实测 `C:W:R2.C1.A1` 被撑到 1220），子块按自身宽度放在
        # 壳里 —— 声明 `center` 就居中，否则靠左。壳的 stackBorder 必须写成同一个偏移，
        # 否则引擎会把子块放到 x=0，发出来的坐标就不再是首轮不动点。
        if node.get("bare") and len(vis) <= 1:
            c = vis[0] if vis else None
            pad = 0
            if c is None:
                node["_w"] = forced_w or 0
                node["_h"] = 0
            else:
                measure(c, None, ctx)
                inner_w = (forced_w or c["_w"]) - 2 * b - ind
                if c["spec"].get("center"):
                    pad = max(0, (inner_w - c["_w"]) // 2)
                c["_x"], c["_y"] = ind + b + pad, b
                node["_w"] = forced_w if forced_w else (2 * b + ind + pad + c["_w"])
                node["_h"] = c["_h"] + 2 * b
                c["_h"] = node["_h"] - 2 * b
            node["_pad"] = pad
            for c in hid:
                measure(c, None, ctx)
                c["_x"], c["_y"] = ind + b, b
            return
        # `even`：把可用内宽**均分**给可见子块，让每行的块左右两边对齐成一个格子阵。
        # 硬编码块宽在内容一变就得重算，而且行与行的块宽不齐看着就乱。
        # 算出来的宽度只作为 forced_w 往下传，**不改写 spec** —— 改写会让几何依赖
        # 调用顺序，破坏"发射坐标 = 引擎首轮不动点"。
        each = None
        if node["spec"].get("even") and forced_w and vis:
            each = (forced_w - 2 * b - ind - sp * (len(vis) - 1)) // len(vis)
        # 水平容器：子块保留自己的宽度；容器宽向上汇总，高发射时钉死。
        # 引擎会给**叶子**子块按 fill 拉平高度（容器子块则用自己的内容高度，
        # 见探针 P3），所以叶子的发射高度必须写成容器内高，否则首次点击会跳。
        off = ind + b
        for c in vis:
            # 声明了 `w` 的子块自己定宽（`even` 只决定它占哪个格子）。
            measure(c, None if c["spec"].get("w") else each, ctx)
            # `even` 均分的是**格子**；块比格子窄时在格内居中 —— 图标尤其需要，
            # 否则一排形状会全挤在各自格子的左边。
            slot = each if each else c["_w"]
            pad = 0
            if each and (c.get("icon") or c["spec"].get("center")):
                pad = max(0, (slot - c["_w"]) // 2)
            c["_x"], c["_y"] = off + pad, b
            off += slot + sp
        # 水平容器的宽度**只有一个来源**：父容器的 fill。它自己如果也去 resizeParent，
        # 两边会互相覆盖，哪次布局跑赢就取哪个值 —— 那样发出来的坐标就不是不动点了
        # （独立复核实测过：行一的行内横带在 824 与 1336 之间来回跳）。所以水平容器
        # 一律 resizeParent=0、按父容器内宽发射；没有父容器（根）时才按内容定宽。
        node["_w"] = forced_w if forced_w else (
            ((off - sp) + b) if vis else (2 * b + ind))
        node["_h"] = 2 * b + max([c["_h"] for c in vis] or [0])
        for c in vis:
            if c["kind"] == "leaf":
                c["_h"] = node["_h"] - 2 * b
        for c in hid:
            measure(c, None, ctx)
            c["_x"], c["_y"] = ind + b, b
    else:
        # 根没有父容器，宽度只能自己声明（layout.json 的 root.w）。
        # 不声明就会退化成 natural_w，而 natural_w 对 `even` 横带只能拿叶子默认宽
        # 去估，估出来的数会一路放大到根 —— 实测把根从 1300 撑到 1904。
        node["_w"] = forced_w or node["spec"].get("w") or natural_w(node, ctx)
        inner = node["_w"] - 2 * b - ind
        y = b
        for c in vis:
            # 子块默认被撑满（forced_w = inner）；声明 `w` 或 `center` 的子块自己定宽
            # ——「汇聚漏斗」（AGG）就靠这个：否则一个 260 宽的菱形放进 1240 宽的
            # 列里只能左对齐，看着像掉到边上去了。
            own = c["spec"].get("w") or c["spec"].get("center")
            measure(c, None if own else inner, ctx)
            c["_x"] = (ind + b + max(0, (inner - c["_w"]) // 2)
                       if c["spec"].get("center") else ind + b)
            c["_y"] = y
            y += c["_h"] + sp
        node["_h"] = ((y - sp) + b) if vis else (2 * b)
        for c in hid:
            own = c["spec"].get("w") or c["spec"].get("center")
            measure(c, None if own else inner, ctx)
            c["_x"], c["_y"] = ind + b, b
    # 侧钉（movable=0）：不进栈、不计入父高，坐标由声明给定。
    for c in node.get("children", []):
        if c["spec"].get("pin"):
            measure(c, c["spec"].get("w"), ctx)
            c["_x"], c["_y"] = c["spec"]["pin"]


def layout(lay, graph, views):
    """递归版面 → 发射计划。坐标是**父相对**的（mxGeometry 语义）。"""
    root = resolve_layout(lay, graph["nodes"])
    ctx = layout_ctx(lay, graph, views, root)
    measure(root, None, ctx)
    root["_x"], root["_y"] = ROOT_X, ROOT_Y

    order, parent_of = [], {}

    def walk(n, depth=0):
        n["_depth"] = depth
        order.append(n["id"])
        for c in n.get("children", []):
            parent_of[c["id"]] = n["id"]
            walk(c, depth + 1)
    walk(root)

    # 结构边（行 → 该行顶层块）：**不再画**。
    # 容器嵌套已经把"谁包着谁"画出来了，再叠一层线反而是本图最主要的"挡内容"来源：
    # 实测 27 条结构边里，行一/行五/行六/行七 那几条中心连中心，正好横穿各自行内的
    # 方块（如 行六→鱼侧透传 穿过 抽鱼和生成）。Design Owner 2026-09-17 反馈
    # "好多箭头上上下下，把内容都挡住了" —— 删掉这一层是最大的一笔。
    semantic = []
    for e in graph["edges"]:
        semantic.append({"from": e["from"], "to": e["to"], "type": e["type"],
                         "exit": e.get("exit"), "entry": e.get("entry"),
                         "exitDx": e.get("exitDx"), "exitDy": e.get("exitDy"),
                         "entryDx": e.get("entryDx"), "entryDy": e.get("entryDy"),
                         "points": e.get("points"),
                         "route": e.get("route"), "lane": e.get("lane"),
                         "via": e.get("via"), "gutter": e.get("gutter"),
                         "id": "E:%s->%s" % (e["from"], e["to"])})

    by_cid = {}

    def index(n):
        by_cid[n["id"]] = n
        for c in n.get("children", []):
            index(c)
    index(root)

    # 边的默认出入口：按源/目标的相对位置给一组（下→上 / 右→左 …）。
    # 不设默认的话线是**中心连中心** —— 一条斜线从源方块拉到目标方块，中途压过
    # 挡在中间的所有方块（实测 `BAKE→DEF` 一条就穿过十几个）。钉住出入口之后，
    # 线从边上出去、从边上进来，只在方块的间隙里走。
    # graph.json 里显式写了 exit/entry 的边不被覆盖。
    def _abs(n):
        x = y = 0
        cur = n
        while cur is not None:
            x += cur["_x"]
            y += cur["_y"]
            cur = by_cid.get(cur["parent"]) if cur["parent"] else None
        return x, y

    for e in semantic:
        s, t = by_cid.get(e["from"]), by_cid.get(e["to"])
        if s is None or t is None:
            continue
        sx, sy = _abs(s)
        tx, ty = _abs(t)
        tcx, tcy = tx + t["_w"] / 2, ty + t["_h"] / 2

        # 「绕行」：跨行的长边不走中间（中间横着好几行），改为沿页面左右空白走廊绕。
        # 走廊 x 由页面几何算出来、不写死 —— 版面改了它跟着改。
        # 为什么非要途经点：**平行四边形（kind=data）会忽略 exitX/exitY**（实测：
        # 圆角矩形、立方体都认，"从左边出去"对行一的三个数据块完全不生效），
        # 那条线于是从方块正中往下扎，横穿行一的细节带。见 memory 的布局硬规则。
        if e.get("route") == "gap":
            # 走「列与列之间的缝」。有些边两侧都被堵死：往下走撞自己那一列下面的
            # fit，往左走撞左边那一列的门控 —— 只剩这条缝可走。
            # 缝的横坐标 = **源所在那一列**的左缘减半个间距（不写死）。
            col_x, n = None, s
            while n is not None:
                par = by_cid.get(n.get("parent")) if n.get("parent") else None
                if par is not None and par["spec"].get("even"):
                    for c in par.get("children", []):
                        if c is n:
                            col_x = _abs(c)[0]
                            break
                    break
                n = par
            mx = round((col_x if col_x is not None else sx) - ctx["spacing"] / 2)
            e["points"] = [[mx, round(sy + s["_h"] / 2)],
                           [mx, round(ty + t["_h"] / 2)]]
            e["exit"] = e["entry"] = None
            continue

        if e.get("route") in ("left", "right"):
            lane = e.get("lane") or 0
            mx = (8 + lane * 9 if e["route"] == "left"
                  else ROOT_X + root["_w"] + 12 + lane * 9)
            mid_y = round(ty + t["_h"] / 2)
            if e.get("via") == "S":
                # 先纵向挪出自己那一条横带再横穿：同行邻居会挡住直着过去的路
                # （行一的「投放与机会强度」要往右走，正撞上右边的「习性配置的构成」）。
                # 留白逐边可调：默认 20 挪不出"方块 + 间隔"那么高的一行（门控要挪过
                # 自己那一列的 fit，得 70）。
                y = round(sy + s["_h"] + (e.get("gutter") or ROUTE_GUTTER))
                e["points"] = [[round(sx + s["_w"] / 2), y], [mx, y], [mx, mid_y]]
            else:
                e["points"] = [[mx, round(sy + s["_h"] / 2)], [mx, mid_y]]
            e["exit"] = e["entry"] = None
            continue

        def _frac(v, lo, span):
            # 目标中线**落在源的那条边上**才把出点挪过去；落在边外就保持中分。
            # （否则"从左边出去"会被算成 y=1.0，变成从**下边**出去 —— 实测过：
            #   行一→烘焙 的三条边因此横穿行一的细节带。）
            if not span:
                return None
            f = (v - lo) / span
            return round(f, 4) if 0.0 <= f <= 1.0 else None

        # 没写方向的边：按相对位置定方向（下→上 / 右→左 …）。
        if not (e["exit"] or e["entry"]):
            dx = tcx - (sx + s["_w"] / 2)
            dy = tcy - (sy + s["_h"] / 2)
            if abs(dy) >= abs(dx):
                e["exit"], e["entry"] = ("S", "N") if dy > 0 else ("N", "S")
            else:
                e["exit"], e["entry"] = ("E", "W") if dx > 0 else ("W", "E")

        # 出点对准目标中线 —— 于是"下→上"是一条**竖直直线**，不会先斜着走一段
        # 再拐（那一段上的方块会被整片压掉）。四角（NW/NE/…）是显式钉点，不参与。
        ex = e["exit"]
        if len(ex) == 1:
            if ex in ("N", "S"):
                f = _frac(tcx, sx, s["_w"])
                e["exitX"] = f if f is not None else 0.5
                e["exitY"] = 0.0 if ex == "N" else 1.0
            else:
                f = _frac(tcy, sy, s["_h"])
                e["exitX"] = 0.0 if ex == "W" else 1.0
                e["exitY"] = f if f is not None else 0.5
        # 入口用 draw.io 的默认：那条边的中点。四角同理。
        en = e["entry"]
        if len(en) == 1:
            if en in ("N", "S"):
                e["entryX"], e["entryY"] = 0.5, (0.0 if en == "N" else 1.0)
            else:
                e["entryX"], e["entryY"] = (0.0 if en == "W" else 1.0), 0.5

    titles = {n["id"] for n in by_cid.values()
              if n["kind"] == "leaf" and n["spec"].get("role") == "title"}
    # 控件区（标题 / 提示 / 视图按钮 / 图例）是硬编码坐标，图例最右到 x=1370。
    # 版面收起时根容器会变窄，页宽不能跟着一路缩到装不下控件。
    page_w = max(int(ROOT_X + root["_w"] + 120), CONTROLS_MIN_W)
    page_h = int(ROOT_Y + root["_h"] + 220)
    return {"root": root, "by_cid": by_cid, "order": order,
            "parent_of": parent_of, "ctx": ctx, "titles": titles,
            "page_w": page_w, "page_h": page_h}, semantic


def subtree_cell_ids(node):
    """版面树里某个节点下面的全部 cell id：graph.json 节点 **和** 容器 id。
    隐藏一个子树时要按这个集合标记 —— 只标节点的话，容器本身仍会发成可见。"""
    out = set()

    def walk(n):
        out.add(n["id"])
        for c in n.get("children", []):
            walk(c)
    walk(node)
    return out


def subtree_node_ids(node):
    """版面树里某个节点下面的全部 graph.json 节点 id（含自身若是叶子）。"""
    out = set()

    def walk(n):
        if n["kind"] == "leaf":
            out.add(n["id"])
        for c in n.get("children", []):
            walk(c)
    walk(node)
    return out


def edges_touching(ids, semantic):
    out = []
    for e in semantic:
        if e["from"] in ids or e["to"] in ids:
            out.append(e["id"])
    return sorted(out)


def container_toggles(plan, semantic):
    """每个可折叠容器要 toggle 的 cell 列表，键 = 它的**标题节点 id**
    （与 views.json 的 expansion 对齐）。

    折叠态 = 只留标题条（Design Owner 2026-09-17 的决定：不再有「占满整条行带」
    的封面块）。所以只需要一条 `toggle` 动作作用在这组内容 cell 上 —— 隐藏一个
    容器 id 会级联到它的子孙（探针 P6），而 toggle 动词本身双向可用，一个链接
    展开/收起都管。边不是容器的子孙，必须显式列进来。
    """
    toggles = {}
    for node in plan["by_cid"].values():
        if node["kind"] != "container":
            continue
        title = title_leaf_of(node)
        if title is None:
            continue
        cells = []
        for c in node.get("children", []):
            # 侧钉的子块（如行三 gutter 里的 DEF）虽然没有进栈，但**属于**这个容器：
            # 收起时必须一起隐藏，否则它会挂着压在下一行上（独立复核抓到过这一条）。
            if c is title or not when_of(c):
                continue
            cells.append(c["id"])
            cells.extend(edges_touching(subtree_node_ids(c), semantic))
        if cells:
            toggles[title["id"]] = sorted(set(cells))
    return toggles


def class_of(node_id, assignment):
    for cls, members in assignment.items():
        if node_id in members:
            return cls
    return None


def lens_actions(scope, nodes, kinds, semantic, mode, titles=()):
    """Style + opacity actions for a scope lens.

    mode='apply' -> colour the three classes AND dim out-of-scope cells
    mode='clear' -> neutral colours AND full opacity

    Opacity uses the native viewer action {"opacity": {"value": v, "cells": [...]}}.
    Dimming rather than hiding is deliberate: out-of-scope elements stay legible as
    context and the geometry never moves, so spatial memory survives the switch.
    """
    assignment = scope["assignment"]
    op = scope.get("opacity", {})
    acts = []

    def style(key, value, cells):
        cells = sorted(set(cells))
        if cells:
            acts.append({"style": {"key": key, "value": value,
                                   "cells": cells, "transient": False}})

    def set_opacity(value, cells):
        cells = sorted(set(cells))
        if cells:
            acts.append({"opacity": {"value": value, "cells": cells}})

    by_class = {c: sorted(assignment.get(c, [])) for c in ("ACTIVE", "BOUNDARY", "OUT")}
    all_nodes = [n["id"] for n in nodes]
    all_edges = [e["id"] for e in semantic]

    gray_edges, dash_edges = [], []
    for e in semantic:
        tcls = class_of(e["to"], assignment)
        scls = class_of(e["from"], assignment)
        if tcls == "OUT":
            gray_edges.append(e["id"])
        elif scls == "BOUNDARY" and tcls == "ACTIVE":
            dash_edges.append(e["id"])

    if mode == "clear":
        for cls in ("OUT", "BOUNDARY"):
            for nid in by_class[cls]:
                if nid in titles:
                    # 标题条有一套自己的样式，clear 必须还原成它，而不是 kind 色。
                    style("fillColor", TITLE_FILL, [nid])
                    style("strokeColor", TITLE_STROKE, [nid])
                    style("fontColor", TITLE_FONT, [nid])
                    style("strokeWidth", "2", [nid])
                    continue
                _, fill, stroke = style_of(kinds.get(nid, DEFAULT_KIND))
                style("fillColor", fill, [nid])
                style("strokeColor", stroke, [nid])
                style("fontColor", "#000000", [nid])
        style("dashed", "0", by_class["BOUNDARY"])
        # 还原时按 kind 自己的描边宽度走，不要一律写成 1 —— 否则像 core 这种
        # 本来就 strokeWidth=2 的节点会被 clear 改细（当前没有这种 BOUNDARY 节点，
        # 但这是一类会随内容变化而复现的坑）。
        for nid in by_class["BOUNDARY"]:
            if nid not in titles:
                style("strokeWidth", KIND_STROKE_W.get(kinds.get(nid, DEFAULT_KIND), "1"),
                      [nid])
        by_eid = {e["id"]: e for e in semantic}
        for eid in gray_edges:
            _, fill, stroke = style_of(kinds.get(by_eid[eid]["from"], DEFAULT_KIND))
            style("strokeColor", stroke, [eid])
        style("dashed", "0", dash_edges)
        set_opacity(1, all_nodes + all_edges)
        return acts

    style("fillColor", GRAY_FILL, by_class["OUT"])
    style("strokeColor", GRAY_STROKE, by_class["OUT"])
    style("fontColor", GRAY_FONT, by_class["OUT"])
    style("dashed", "1", by_class["BOUNDARY"])
    style("strokeWidth", "2", by_class["BOUNDARY"])
    style("strokeColor", LENS_EDGE_GRAY, gray_edges)
    style("dashed", "1", dash_edges)

    set_opacity(op.get("ACTIVE", 1.0), by_class["ACTIVE"])
    set_opacity(op.get("BOUNDARY", 0.75), by_class["BOUNDARY"])
    set_opacity(op.get("OUT", 0.30), by_class["OUT"])
    set_opacity(op.get("BOUNDARY", 0.75), dash_edges)
    set_opacity(op.get("OUT", 0.30), gray_edges)
    return acts


# ---------------------------------------------------------------- easing ----

def view_button_payload(view, scope_by_id, nodes, kinds, semantic,
                        toggles, titles=()):
    acts = []
    lens_id = view.get("scopeLens", "keep")
    if lens_id == "clear":
        for s in scope_by_id.values():
            if s.get("lens"):
                acts.extend(lens_actions(s, nodes, kinds, semantic,
                                         "clear", titles))
    elif lens_id not in (None, "keep"):
        acts.extend(lens_actions(scope_by_id[lens_id], nodes, kinds,
                                 semantic, "apply", titles))
    exp = view.get("expansion") or {}
    for key in ("collapse", "expand"):
        for nid in exp.get(key, []):
            if nid not in toggles:
                sys.exit("error: view %s tries to %s %r, which is not a "
                         "collapsible node in layout.json" % (view["id"], key, nid))
    for nid in exp.get("collapse", []):
        acts.append({"hide": {"cells": toggles[nid]}})
    for nid in exp.get("expand", []):
        acts.append({"show": {"cells": toggles[nid]}})
    return {"actions": acts}


# ---------------------------------------------------------------- emit ----

def vertex(cid, value, style, x, y, w, h, layer, link=None, visible=True):
    vis = "" if visible else ' visible="0"'
    geo = ('            <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" />\n'
           % (x, y, w, h))
    if link:
        return ('        <UserObject label="%s" link="%s" id="%s">\n'
                '          <mxCell style="%s" vertex="1" parent="%s"%s>\n%s'
                '          </mxCell>\n        </UserObject>\n'
                % (xesc(value), xesc(link), xesc(cid), xesc(style), xesc(layer), vis, geo))
    return ('        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s"%s>\n%s'
            '        </mxCell>\n'
            % (xesc(cid), xesc(value), xesc(style), xesc(layer), vis, geo))


def edge(eid, estyle, layer, src, tgt, visible=True, value="", points=None):
    vis = "" if visible else ' visible="0"'
    if points:
        # 显式途经点（绝对页面坐标）。**这是最后的逃生口**：这个 viewer build
        # 完全忽略 exitX/exitY（实测：改 exitX、换 edgeStyle 都不动），所以
        # "这条线要绕左边空白走"只能靠点把它钉住。
        body = ('            <mxGeometry relative="1" as="geometry">\n'
                '              <Array as="points">\n'
                + "".join('                <mxPoint x="%d" y="%d" />\n' % (int(px), int(py))
                          for px, py in points)
                + '              </Array>\n'
                  '            </mxGeometry>\n')
    else:
        body = '            <mxGeometry relative="1" as="geometry" />\n'
    return ('        <mxCell id="%s" value="%s" style="%s" edge="1" parent="%s" source="%s" target="%s"%s>\n'
            '%s'
            '        </mxCell>\n'
            % (xesc(eid), xesc(value), xesc(estyle), xesc(layer), xesc(src), xesc(tgt), vis, body))


def text_cell(cid, value, style, x, y, w, h):
    return vertex(cid, value, style, x, y, w, h, "Layer:Controls")


def emit(graph, scopes, views, plan, semantic, default_view):
    kinds = {n["id"]: n.get("kind", DEFAULT_KIND) for n in graph["nodes"]}
    gby = {n["id"]: n for n in graph["nodes"]}
    toggles = container_toggles(plan, semantic)
    ctx = plan["ctx"]
    PAGE_W, PAGE_H = plan["page_w"], plan["page_h"]
    out = []
    a = out.append
    a('<?xml version="1.0" encoding="UTF-8"?>\n')
    a('<mxfile host="fcf-system-map" agent="build_diagram.py" version="26.0.0" type="device">\n')
    a('  <diagram id="fcf-canonical-system-map" name="FCF System Map">\n')
    a('    <mxGraphModel dx="1422" dy="796" grid="1" gridSize="10" guides="1" tooltips="1" '
      'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" '
      'pageHeight="%d" math="0" shadow="0">\n' % (PAGE_W, PAGE_H))
    a('      <root>\n')
    a('        <mxCell id="0" />\n')
    a('        <mxCell id="1" parent="0" />\n')
    a('        <mxCell id="Layer:Controls" value="Controls" parent="0" />\n')
    a('        <mxCell id="Layer:Main" value="System Map" parent="0" />\n')

    # ---- controls（全部中文；英文仅作副标题） ---------------------------
    a(text_cell("CTRL:TITLE",
                "中鱼机制总图｜FCF Canonical System Map",
                "text;html=1;align=left;verticalAlign=middle;fontSize=16;fontStyle=1;",
                700, 56, 640, 30))
    a(text_cell("CTRL:HINT",
                "本图停在『整体框架』级别：只表达流向、模块边界与输入输出边界，不表达具体参数如何算出下一层。"
                "七大层自上而下；每行是一个容器，点标题条上的 ⇕ 收起／展开 —— 收起时只留标题条，"
                "下方的行自动上移；展开时整行恢复、下方的行下移。层内再展开同样会让位。",
                "text;html=1;align=left;verticalAlign=top;fontSize=10;fontColor=#666666;",
                80, 92, 1080, 28))

    for i, v in enumerate(views["views"]):
        payload = view_button_payload(v, {s["id"]: s for s in scopes["scopes"]},
                                      graph["nodes"], kinds, semantic,
                                      toggles, plan["titles"])
        is_default = v["id"] == default_view
        x, y, w, h = 80 + i * 190, 54, 175, 34
        extra = "strokeWidth=2;fontStyle=1;" if is_default else "strokeWidth=1;"
        fill, stroke = ("#dae8fc", "#6c8ebf") if is_default else ("#d5e8d4", "#82b366")
        a(vertex("BTN:VIEW:%s" % v["id"], v["label"],
                 "rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=%s;strokeColor=%s;%s"
                 % (fill, stroke, extra),
                 x, y, w, h, "Layer:Controls",
                 link=action_link(payload)))

    # 图例：Scope 三态（右下侧栏，避开各行方块）
    legend = [
        ("LEG:DATA", "数据 / 配置",
         "shape=parallelogram;perimeter=parallelogramPerimeter;size=18;", "#dae8fc", "#6c8ebf"),
        ("LEG:CUBE", "派生数据（环境场）", "shape=cube;size=20;", "#dae8fc", "#6c8ebf"),
        ("LEG:PROC", "过程 / 模块", "rounded=1;", "#ffe6cc", "#d79b00"),
        ("LEG:OUT2", "范围外", "rounded=1;dashed=1;", GRAY_FILL, GRAY_STROKE),
    ]
    ly = PAGE_H - 128
    lx = 340
    for cid, label, base, fill, stroke in legend:
        a(vertex(cid, label,
                 base + "whiteSpace=wrap;html=1;fontSize=11;fontColor=#333333;"
                 "fillColor=%s;strokeColor=%s;" % (fill, stroke),
                 lx, ly, 250, 34, "Layer:Controls"))
        lx += 260
    a(text_cell("LEG:EDGES",
                "——▶  数据 / 权重流向　　– –▶  选择 · 控制　　┄┄  层属查询（非因果主张）",
                "text;html=1;align=left;verticalAlign=middle;fontSize=10;fontColor=#666666;",
                350, ly + 48, 900, 30))

    # ---- nodes: 容器 + 叶子，按版面树 DFS 顺序（父先于子） -----------------
    hidden_nodes, hidden_edges = set(), set()
    for node in plan["by_cid"].values():
        for c in node.get("children", []):
            if not ctx["visible"](c):
                hidden_nodes |= subtree_cell_ids(c)
    hidden_edges = set(edges_touching(hidden_nodes, semantic))

    for cid in plan["order"]:
        n = plan["by_cid"][cid]
        parent = plan["parent_of"].get(cid, "Layer:Main")
        x, y, w, h = n["_x"], n["_y"], n["_w"], n["_h"]
        if n["kind"] == "container":
            indent = ("marginLeft=%d;" % n["indent"]) if n["indent"] else ""
            d = n.get("_depth", 99)
            stroke = "none" if n.get("bare") else (
                CONTAINER_STROKE_BY_DEPTH[d] if d < len(CONTAINER_STROKE_BY_DEPTH)
                else CONTAINER_STROKE_DEEP)
            style = ("rounded=0;html=1;fillColor=none;strokeColor=%s;strokeWidth=1;"
                     "childLayout=stackLayout;resizeParent=%d;resizeParentMax=0;"
                     "horizontalStack=%d;stackSpacing=%d;stackBorder=%d;%s"
                     % (stroke, 0 if n["axis"] == "h" else 1,
                        1 if n["axis"] == "h" else 0,
                        ctx["spacing"], n.get("_pad", border_of(n, ctx)), indent))
            a(vertex(cid, "", style, x, y, w, h, parent,
                     visible=cid not in hidden_nodes))
            continue
        if n["spec"].get("skip"):
            continue                      # 留在语义模型里，但不画（总图框＝页面标题已表达）
        if n.get("icon"):
            base, fill, stroke = ICON_SHAPES[n["icon"]]
            a(vertex(cid, "", base + "fillColor=%s;strokeColor=%s;" % (fill, stroke),
                     x, y, w, h, parent, visible=cid not in hidden_nodes))
            continue
        gn = gby[n["id"]]
        kind = gn.get("kind", DEFAULT_KIND)
        style = node_style(kind, n["spec"].get("role"))
        if n["spec"].get("pin"):
            style += "movable=0;"
        value = gn["label"]
        if n["id"] in toggles:
            value = "⇕ " + value      # 折叠把手：⇕ = 可收起 / 展开
        if gn.get("caption"):
            value += ("<br><font style='font-size:10px;color:#444444'>%s</font>"
                      % gn["caption"])
        link = None
        if n["id"] in toggles:
            link = action_link({"actions": [
                {"toggle": {"cells": toggles[n["id"]], "transient": False}}]})
        a(vertex(n["id"], value, style, x, y, w, h, parent, link=link,
                 visible=n["id"] not in hidden_nodes))

    # ---- edges: 只有语义边（层级关系由容器嵌套表达，不另画线） -----------
    for e in semantic:
        kind = kinds.get(e["from"], DEFAULT_KIND)
        _, fill, stroke = style_of(kind)
        t = EDGE_TYPES[e["type"]]
        stroke = t.get("color", stroke)
        style = (EDGE_BASE + t["dashed"] + t["dashPattern"] +
                 "endArrow=%s;strokeColor=%s;" % (t["arrow"], stroke))
        if e.get("label"):
            style += "fontSize=10;fontColor=%s;" % stroke
        for key in ("exit", "entry"):
            val = e.get(key)
            fx, fy = e.get(key + "X"), e.get(key + "Y")
            if fx is None and fy is None:
                if not val:
                    continue
                fx, fy = DIRS[val]
            style += "%sX=%s;%sY=%s;%sDx=%s;%sDy=%s;" % (
                key, fx, key, fy, key, e.get(key + "Dx", 0) or 0,
                key, e.get(key + "Dy", 0) or 0)
        a(edge(e["id"], style, "Layer:Main", e["from"], e["to"],
               visible=e["id"] not in hidden_edges, value=e.get("label", ""),
               points=e.get("points")))

    a('      </root>\n')
    a('    </mxGraphModel>\n')
    a('  </diagram>\n')
    a('</mxfile>\n')
    return "".join(out)


# ---------------------------------------------------------------- main ----

def build(root):
    src = load_sources(root)
    graph, scopes, views = src["graph"], src["scopes"], src["views"]

    plan, semantic = layout(load_layout(root), graph, views)
    xml = emit(graph, scopes, views, plan, semantic,
               views["defaultView"])
    out_path = root / "generated" / "fcf-system-map.drawio"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    digest = hashlib.sha256(xml.encode("utf-8")).hexdigest()
    n_cont = sum(1 for n in plan["by_cid"].values() if n["kind"] == "container")
    n_cells = len(graph["nodes"]) + n_cont + len(semantic)
    print("wrote %s: %d nodes + %d containers, %d semantic edges, "
          "%d cells total, sha256=%s" % (out_path, len(graph["nodes"]), n_cont,
                                         len(semantic), n_cells, digest[:16]))
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(ROOT),
                    help="fcf-system-map root directory (contains the source JSONs)")
    ap.add_argument("--out", default=None,
                    help="override output path (default <root>/generated/fcf-system-map.drawio)")
    args = ap.parse_args()
    root = Path(args.root)
    if args.out:
        src = load_sources(root)
        graph, scopes, views = src["graph"], src["scopes"], src["views"]
        plan, semantic = layout(load_layout(root), graph, views)
        xml = emit(graph, scopes, views, plan, semantic,
                   views["defaultView"])
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(xml)
        print("wrote %s" % args.out)
    else:
        build(root)


if __name__ == "__main__":
    main()

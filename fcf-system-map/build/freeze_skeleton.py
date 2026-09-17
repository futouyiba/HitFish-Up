#!/usr/bin/env python3
"""冻结 / 更新总图骨架基线。

原则（见 memory: fcf-map-topology-invariant）：总图的**拓扑骨架**冻结在最初对齐的
草图 v1；后续只允许往骨架里加中下层内容、以及细化 JSON 与格式处理。

骨架 = 行结构 + 每行并列方块 + 方块间连接 + 形状语义 + 行/方块的名字。
内容 = caption、scope 归类、view 预设、contracts 关联、provenance。

`validate.py` 会拿当前 graph.json 的骨架指纹和本基线比对；一旦骨架变了就报错。

**只有在明确决定要改骨架时**（那是一次需要与 Design Owner 重新对齐的事件）才运行：

    python3 build/freeze_skeleton.py          # 覆盖基线
    python3 build/freeze_skeleton.py --show   # 只打印当前指纹，不写
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GRAPH = ROOT / "graph.json"
BASELINE = ROOT / "skeleton.baseline.json"


def fingerprint(graph):
    """骨架指纹：只含结构与命名，不含 caption / scope / view。"""
    nodes = graph["nodes"]
    rows = [n for n in nodes if n.get("lane") == "main" and n.get("parent") is not None]
    blocks = {}
    for n in nodes:
        p = n.get("parent")
        if p is not None:
            blocks.setdefault(p, []).append(n["id"])
    root = next(n["id"] for n in nodes if n.get("parent") is None)
    return {
        "root": root,
        "rows": [{"id": r["id"], "label": r["label"],
                  "collapsible": bool(r.get("collapsible"))} for r in rows],
        "blocks": {k: sorted(v) for k, v in sorted(blocks.items())},
        "shapes": {n["id"]: n.get("kind", "process") for n in nodes},
        "labels": {n["id"]: n["label"] for n in nodes},
        "edges": sorted("%s->%s:%s" % (e["from"], e["to"], e["type"])
                        for e in graph["edges"]),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--show", action="store_true", help="只打印，不写基线")
    args = ap.parse_args()

    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    fp = fingerprint(graph)

    if args.show:
        print(json.dumps(fp, ensure_ascii=False, indent=2))
        return

    BASELINE.write_text(json.dumps(fp, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print("已冻结骨架基线 -> %s" % BASELINE)
    print("  行 %d 个 / 方块 %d 个 / 连接 %d 条"
          % (len(fp["rows"]), len(fp["labels"]), len(fp["edges"])))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""FCF 总图 · 常驻预览器（改完就能看到）。

为什么需要它：App 的 preview 启动器跑在沙箱里，读不了 /Volumes 卷，所以
必须把文件镜像到 /tmp 再服务。用你**自己的终端**起这个脚本就没有那个限制，
可以直接服务工作区、每次请求自动重建，而且活得比任何一次会话都长。

用法（在你自己的终端里跑，一次即可）：

    python3 fcf-system-map/tools/preview.py            # 默认 8799
    python3 fcf-system-map/tools/preview.py --port 9000

然后浏览器打开它打印的地址。之后我改完 source，你**刷新页面**（或它自动刷新）
就能看到最新图 —— 不需要你我之间传文件。

自动刷新：页面会轮询 /api/version；一旦 generated/*.drawio 的 mtime 变了，
页面自动重新加载 viewer。
"""

from __future__ import annotations

import argparse
import hashlib
import http.server
import json
import os
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAP_ROOT = HERE.parent                      # fcf-system-map/
REPO_ROOT = MAP_ROOT.parent                 # 工作区根（harness 要引用 ../spike/...）
BUILDER = MAP_ROOT / "build" / "build_diagram.py"
DRAWIO = MAP_ROOT / "generated" / "fcf-system-map.drawio"
SOURCES = [MAP_ROOT / n for n in ("graph.json", "layout.json", "scopes.json",
                                  "views.json", "contracts.json")]
HARNESS = "/fcf-system-map/build/viewer-harness.html"

_build_lock = threading.Lock()


def rebuild_if_stale() -> bool:
    """source 比产物新就重建一次。返回是否重建。"""
    with _build_lock:
        if not DRAWIO.exists():
            stale = True
        else:
            produced = DRAWIO.stat().st_mtime
            stale = any(s.exists() and s.stat().st_mtime > produced for s in SOURCES)
        if not stale:
            return False
        r = subprocess.run([sys.executable, str(BUILDER)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write("[preview] 构建失败:\n%s\n" % (r.stderr or r.stdout))
            return False
        sys.stderr.write("[preview] 已重建 %s\n" % DRAWIO.name)
        return True


def version() -> str:
    if not DRAWIO.exists():
        return "missing"
    data = DRAWIO.read_bytes()
    return hashlib.sha256(data).hexdigest()[:16]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO_ROOT), **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path == "/api/version":
            # 必须在这里也重建：页面靠轮询本端点来发现变化，
            # 若只有 .drawio 请求才重建，轮询就永远看不到新版本。
            rebuild_if_stale()
            payload = json.dumps({"version": version()}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)
            return

        if path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", HARNESS)
            self.end_headers()
            return

        # 任何取图的请求都先确保产物是最新的
        if path.endswith("fcf-system-map.drawio"):
            rebuild_if_stale()

        super().do_GET()

    def end_headers(self):
        # 图上永不缓存，避免浏览器拿旧的
        if self.path.endswith(".drawio") or self.path.endswith(".html"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("[preview] %s\n" % (fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8799)
    ap.add_argument("--no-initial-build", action="store_true")
    args = ap.parse_args()

    if not args.no_initial_build:
        rebuild_if_stale()

    url = "http://127.0.0.1:%d%s" % (args.port, HARNESS)
    print("服务目录: %s" % REPO_ROOT)
    print("打开:     %s" % url)
    print("(改完 source 后刷新页面即可；页面也会自动刷新)")
    with Server(("127.0.0.1", args.port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止。")


if __name__ == "__main__":
    main()

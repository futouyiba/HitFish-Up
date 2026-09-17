#!/usr/bin/env python3
"""Test-only static server for the spike viewer harness.

Serves the worktree root (so the harness can fetch ../fcf-spike.drawio).
Avoids `python3 -m http.server`, which calls os.getcwd() at argument-parser
construction and fails under the sandboxed preview launcher.
"""
import http.server
import os
import socketserver

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PORT = 8799
HARNESS = "/spike/verify/viewer-harness.html"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/spike", "/spike/"):
            self.send_response(302)
            self.send_header("Location", HARNESS)
            self.end_headers()
            return
        super().do_GET()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


def main():
    with Server(("127.0.0.1", PORT), Handler) as httpd:
        print("serving %s at http://127.0.0.1:%d/ -> %s" % (ROOT, PORT, HARNESS), flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()

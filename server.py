#!/usr/bin/env python3
"""pref-sub 后端：静态文件服务 + sb-onekey 节点 API"""
import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

SB_NODES = "/etc/sing-box/nodes"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/nodes":
            self.send_nodes()
        else:
            super().do_GET()

    def send_nodes(self):
        """读取 sb-onekey 的 VLESS+WS+TLS 节点"""
        nodes = []
        if os.path.isdir(SB_NODES):
            for fn in sorted(os.listdir(SB_NODES)):
                if not fn.endswith(".json"):
                    continue
                try:
                    with open(os.path.join(SB_NODES, fn)) as f:
                        meta = json.load(f)
                    # 只要 vless-ws-tls 节点
                    if meta.get("proto") not in ("vless-ws-tls", "vless-ws"):
                        continue
                    nodes.append({
                        "tag": meta.get("tag"),
                        "name": meta.get("name"),
                        "proto": meta.get("proto"),
                        "uuid": meta.get("uuid"),
                        "port": meta.get("port"),
                        "path": meta.get("path"),
                        "host": meta.get("sni_v4") or meta.get("domain"),
                        "created": meta.get("created"),
                    })
                except Exception:
                    continue
        # 按创建时间排序
        nodes.sort(key=lambda x: x.get("created") or "")
        body = json.dumps({"nodes": nodes, "sb_installed": os.path.isdir(SB_NODES)}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "13530"))
    print(f"pref-sub serving on port {port}, sb-onekey nodes: {SB_NODES}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

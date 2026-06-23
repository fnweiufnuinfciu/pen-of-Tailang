"""
太郎的笔 Server
Serves the web UI and proxies API calls to LLM providers.
Usage: python server.py
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import json, os, sys, signal, urllib.request, traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8765
LOG_FILE = os.path.join(BASE_DIR, "server.log")

PAGES = {"/": "novel.html", "/novel.html": "novel.html"}


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        page = PAGES.get(self.path)
        if page:
            path = os.path.join(BASE_DIR, page)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self._respond(200, content.encode("utf-8"), "text/html; charset=utf-8")
        else:
            self._respond(404, b"Not Found", "text/plain")

    def do_POST(self):
        if self.path == "/api":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length))
                url = body["_url"]
                headers = {k: v for k, v in body.get("_headers", {}).items()}
                payload = json.dumps(body.get("_body", {})).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
                try:
                    with urllib.request.urlopen(req, timeout=180) as resp:
                        self._respond(resp.status, resp.read(), "application/json")
                except urllib.request.HTTPError as e:
                    err_body = e.read().decode("utf-8", errors="replace")
                    self._respond(e.code, json.dumps(
                        {"error": f"API Error: {e.code}", "detail": err_body[:500]},
                        ensure_ascii=False).encode("utf-8"), "application/json")
            except Exception as e:
                log(f"API Error: {e}")
                self._respond(500, json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8"), "application/json")
        else:
            self._respond(404, b"Not Found", "text/plain")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _respond(self, code, data, mime="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def signal_handler(sig, frame):
    log("Server shutting down...")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    log(f"太郎的笔 started on http://127.0.0.1:{PORT}")
    try:
        HTTPServer(("127.0.0.1", PORT), Server).serve_forever()
    except KeyboardInterrupt:
        pass
    log("Server stopped")

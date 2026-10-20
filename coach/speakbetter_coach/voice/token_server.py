"""Local HTTP server: LiveKit token + minimal voice web UI (no API secret to browser)."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from speakbetter_coach.env_config import load_local_env
from speakbetter_coach.voice.config import load_livekit_config
from speakbetter_coach.voice.tokens import create_participant_token

WEB_ROOT = Path(__file__).resolve().parents[2] / "voice_web"


class TokenHandler(BaseHTTPRequestHandler):
    server_version = "SpeakBetterVoice/0.1"

    def log_message(self, format: str, *args) -> None:
        # Avoid logging query strings that might contain sensitive data
        super().log_message(format, *args)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self._serve_index()
            return
        if parsed.path == "/health":
            self._json(200, {"status": "ok"})
            return
        if parsed.path == "/token":
            self._serve_token(parsed)
            return
        self.send_error(404, "Not found")

    def _serve_index(self) -> None:
        index = WEB_ROOT / "index.html"
        if not index.is_file():
            self.send_error(404, "index.html missing")
            return
        data = index.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _serve_token(self, parsed) -> None:
        try:
            config = load_livekit_config()
        except RuntimeError as err:
            self._json(503, {"error": str(err)})
            return
        qs = parse_qs(parsed.query)
        identity = qs.get("identity", ["speakbetter-user"])[0]
        try:
            jwt = create_participant_token(config, identity=identity)
        except Exception:
            self._json(500, {"error": "Could not create token"})
            return
        self._json(
            200,
            {
                "token": jwt,
                "url": config.url,
                "room": config.room,
            },
        )

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(host: str = "127.0.0.1", port: int = 8787) -> None:
    load_local_env()
    httpd = HTTPServer((host, port), TokenHandler)
    print(f"Voice UI + token server: http://{host}:{port}/")
    print("Browser receives a short-lived token only; LIVEKIT_API_SECRET stays on the server.")
    httpd.serve_forever()


def main() -> None:
    host = os.environ.get("VOICE_HTTP_HOST", "127.0.0.1")
    port = int(os.environ.get("VOICE_HTTP_PORT", "8787"))
    run_server(host, port)


if __name__ == "__main__":
    main()

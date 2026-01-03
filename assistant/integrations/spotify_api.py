from __future__ import annotations

import base64
import hashlib
import http.server
import json
import os
import secrets
import socketserver
import time
import urllib.parse
import urllib.request
import webbrowser
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, List

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"

DEFAULT_SCOPES = [
    "user-read-playback-state",
    "user-modify-playback-state",
]

TOKEN_DIR = os.path.join(os.path.expanduser("~"), ".vera")
TOKEN_PATH = os.path.join(TOKEN_DIR, "spotify_tokens.json")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _sha256(s: str) -> bytes:
    return hashlib.sha256(s.encode("utf-8")).digest()


def _now() -> int:
    return int(time.time())


def _load_json(path: str) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _save_json(path: str, obj: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    os.replace(tmp, path)


def _http_request(url: str, method: str = "GET", headers: Optional[dict] = None, data: Optional[bytes] = None) -> Tuple[int, dict, bytes]:
    req = urllib.request.Request(url, method=method, data=data)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()
    except Exception as e:
        raise RuntimeError(f"HTTP request failed: {e}")


@dataclass
class SpotifyTokens:
    access_token: str
    refresh_token: Optional[str]
    expires_at: int  # unix timestamp

    @classmethod
    def from_dict(cls, d: dict) -> "SpotifyTokens":
        return cls(
            access_token=str(d.get("access_token") or ""),
            refresh_token=d.get("refresh_token"),
            expires_at=int(d.get("expires_at") or 0),
        )

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
        }


class SpotifyAPI:
    """
    Product-grade behavior:
    - PKCE OAuth (no client secret required)
    - Token cache in ~/.vera/spotify_tokens.json
    - Automatic refresh if refresh_token exists
    """

    def __init__(
        self,
        client_id: str,
        redirect_uri: str = "http://127.0.0.1:8888/callback",
        scopes: Optional[List[str]] = None,
    ) -> None:
        self.client_id = client_id.strip()
        self.redirect_uri = redirect_uri.strip()
        self.scopes = scopes or DEFAULT_SCOPES
        self._tokens: Optional[SpotifyTokens] = None

    @property
    def configured(self) -> bool:
        return bool(self.client_id)

    def load_cached_tokens(self) -> bool:
        data = _load_json(TOKEN_PATH)
        if not data:
            return False
        tok = SpotifyTokens.from_dict(data)
        if not tok.access_token:
            return False
        self._tokens = tok
        return True

    def _save_tokens(self, tok: SpotifyTokens) -> None:
        self._tokens = tok
        _save_json(TOKEN_PATH, tok.to_dict())

    def _needs_refresh(self) -> bool:
        if not self._tokens:
            return True
        # refresh 60s early
        return _now() >= (self._tokens.expires_at - 60)

    def ensure_auth(self) -> None:
        if not self.configured:
            raise RuntimeError("Spotify client_id not configured (set SPOTIFY_CLIENT_ID).")

        if self._tokens is None:
            self.load_cached_tokens()

        if self._tokens and not self._needs_refresh():
            return

        # Try refresh first
        if self._tokens and self._tokens.refresh_token:
            ok = self._refresh()
            if ok and self._tokens and not self._needs_refresh():
                return

        # Otherwise run interactive OAuth
        self._interactive_pkce_auth()

    def _refresh(self) -> bool:
        assert self._tokens is not None
        assert self._tokens.refresh_token is not None
        form = {
            "grant_type": "refresh_token",
            "refresh_token": self._tokens.refresh_token,
            "client_id": self.client_id,
        }
        body = urllib.parse.urlencode(form).encode("utf-8")
        status, _, raw = _http_request(
            SPOTIFY_TOKEN_URL,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=body,
        )
        if status != 200:
            return False
        data = json.loads(raw.decode("utf-8"))
        access = data.get("access_token")
        expires_in = int(data.get("expires_in") or 0)
        if not access or not expires_in:
            return False
        # refresh may not return refresh_token; keep existing
        tok = SpotifyTokens(
            access_token=access,
            refresh_token=self._tokens.refresh_token,
            expires_at=_now() + expires_in,
        )
        self._save_tokens(tok)
        return True

    def _interactive_pkce_auth(self) -> None:
        # PKCE verifier/challenge
        verifier = _b64url(secrets.token_bytes(32))
        challenge = _b64url(_sha256(verifier))
        state = _b64url(secrets.token_bytes(16))

        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "code_challenge_method": "S256",
            "code_challenge": challenge,
            "state": state,
            "show_dialog": "true",
        }
        url = SPOTIFY_AUTH_URL + "?" + urllib.parse.urlencode(params)

        code_holder: Dict[str, str] = {}

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):  # noqa: N802
                parsed = urllib.parse.urlparse(self.path)
                if parsed.path != urllib.parse.urlparse(self.server.redirect_uri).path:
                    self.send_response(404)
                    self.end_headers()
                    return
                q = urllib.parse.parse_qs(parsed.query)
                if "error" in q:
                    code_holder["error"] = q["error"][0]
                if "state" in q and q["state"][0] != self.server.state:
                    code_holder["error"] = "state_mismatch"
                if "code" in q:
                    code_holder["code"] = q["code"][0]

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<html><body><h3>VERA connected to Spotify. You can close this tab.</h3></body></html>")

            def log_message(self, format, *args):  # noqa: A003
                return  # silence

        # start local server
        parsed = urllib.parse.urlparse(self.redirect_uri)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 8888

        with socketserver.TCPServer((host, port), Handler) as httpd:
            httpd.redirect_uri = self.redirect_uri
            httpd.state = state

            webbrowser.open(url)

            # wait up to 90s
            deadline = time.time() + 90
            while time.time() < deadline:
                httpd.handle_request()
                if "code" in code_holder or "error" in code_holder:
                    break

        if "error" in code_holder:
            raise RuntimeError(f"Spotify auth failed: {code_holder['error']}")
        if "code" not in code_holder:
            raise RuntimeError("Spotify auth timed out (no code received).")

        code = code_holder["code"]
        form = {
            "client_id": self.client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": verifier,
        }
        body = urllib.parse.urlencode(form).encode("utf-8")
        status, _, raw = _http_request(
            SPOTIFY_TOKEN_URL,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=body,
        )
        if status != 200:
            raise RuntimeError(f"Token exchange failed: HTTP {status} {raw[:200]!r}")

        data = json.loads(raw.decode("utf-8"))
        access = data.get("access_token")
        refresh = data.get("refresh_token")
        expires_in = int(data.get("expires_in") or 0)
        if not access or not expires_in:
            raise RuntimeError("Token response missing access_token/expires_in.")
        tok = SpotifyTokens(access_token=access, refresh_token=refresh, expires_at=_now() + expires_in)
        self._save_tokens(tok)

    def _auth_header(self) -> dict:
        assert self._tokens is not None
        return {"Authorization": f"Bearer {self._tokens.access_token}"}

    def get_devices(self) -> List[dict]:
        self.ensure_auth()
        status, _, raw = _http_request(f"{SPOTIFY_API_BASE}/me/player/devices", headers=self._auth_header())
        if status != 200:
            return []
        data = json.loads(raw.decode("utf-8"))
        return data.get("devices") or []

    def _pick_device_id(self) -> Optional[str]:
        devices = self.get_devices()
        if not devices:
            return None
        # prefer active device
        for d in devices:
            if d.get("is_active"):
                return d.get("id")
        return devices[0].get("id")

    def search(self, query: str, types: List[str], limit: int = 5) -> dict:
        self.ensure_auth()
        q = urllib.parse.quote(query)
        t = ",".join(types)
        url = f"{SPOTIFY_API_BASE}/search?q={q}&type={t}&limit={limit}"
        status, _, raw = _http_request(url, headers=self._auth_header())
        if status != 200:
            return {}
        return json.loads(raw.decode("utf-8"))

    def play(self, *, uris: Optional[List[str]] = None, context_uri: Optional[str] = None) -> Tuple[bool, str]:
        self.ensure_auth()
        device_id = self._pick_device_id()
        if not device_id:
            return False, "No active Spotify device found. Open Spotify and start playing something once."

        url = f"{SPOTIFY_API_BASE}/me/player/play?device_id={urllib.parse.quote(device_id)}"
        payload: Dict[str, Any] = {}
        if context_uri:
            payload["context_uri"] = context_uri
        if uris:
            payload["uris"] = uris

        body = json.dumps(payload).encode("utf-8")
        status, _, raw = _http_request(
            url,
            method="PUT",
            headers={**self._auth_header(), "Content-Type": "application/json"},
            data=body,
        )
        # Spotify returns 204 No Content on success
        if status in (200, 204):
            return True, ""
        return False, f"Spotify play failed: HTTP {status} {raw[:200]!r}"

    def search_and_play(self, query: str) -> Tuple[bool, str]:
        """
        Strategy:
        - If query sounds like "lofi/work/focus", prefer a playlist context
        - Otherwise try track first, then playlist
        """
        q = (query or "").strip() or "lofi work music"
        prefer_playlist = any(k in q.lower() for k in ["lofi", "focus", "work", "study", "beats", "mix"])

        if prefer_playlist:
            data = self.search(q, ["playlist"], limit=5)
            items = (((data.get("playlists") or {}).get("items")) or [])
            if items:
                uri = items[0].get("uri")
                if uri:
                    return self.play(context_uri=uri)
            # fallback to track
            data = self.search(q, ["track"], limit=5)

        else:
            data = self.search(q, ["track"], limit=5)

        tracks = (((data.get("tracks") or {}).get("items")) or [])
        if tracks:
            uri = tracks[0].get("uri")
            if uri:
                return self.play(uris=[uri])

        # last fallback to playlist
        data = self.search(q, ["playlist"], limit=5)
        items = (((data.get("playlists") or {}).get("items")) or [])
        if items:
            uri = items[0].get("uri")
            if uri:
                return self.play(context_uri=uri)

        return False, "No Spotify results found for that query."

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import requests


TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
DEFAULT_TOKEN_FILE = "~/.codex/secrets/google/google-business-token.json"


class AuthError(RuntimeError):
    pass


def load_env_file(path: str | None = None) -> None:
    env_path = Path(path or os.environ.get("GOOGLE_BUSINESS_MCP_ENV", "~/.codex/secrets/google/google-business-mcp.env")).expanduser()
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def token_file() -> Path:
    return Path(os.environ.get("GOOGLE_OAUTH_TOKEN_FILE", DEFAULT_TOKEN_FILE)).expanduser()


def load_token() -> dict[str, Any]:
    path = token_file()
    if not path.exists():
        raise AuthError(f"OAuth token file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_token(token: dict[str, Any]) -> None:
    path = token_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(token, indent=2, sort_keys=True), encoding="utf-8")
    path.chmod(0o600)


def refresh_access_token(token: dict[str, Any]) -> dict[str, Any]:
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    refresh_token = token.get("refresh_token")

    if not client_id or not client_secret:
        raise AuthError("GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET are required.")
    if not refresh_token:
        raise AuthError("OAuth token file does not contain a refresh_token.")

    response = requests.post(
        TOKEN_ENDPOINT,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    response.raise_for_status()
    refreshed = response.json()

    token.update(refreshed)
    token["expires_at"] = int(time.time()) + int(refreshed.get("expires_in", 3600)) - 60
    save_token(token)
    return token


def access_token() -> str:
    load_env_file()
    token = load_token()
    if not token.get("access_token") or int(token.get("expires_at", 0)) <= int(time.time()):
        token = refresh_access_token(token)
    return str(token["access_token"])


def auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token()}", "Accept": "application/json"}

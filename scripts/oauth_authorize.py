from __future__ import annotations

import json
import os
import secrets
import sys
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from time import monotonic

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from google_business_mcp.auth import TOKEN_ENDPOINT, load_env_file, save_token


AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
REDIRECT_PATH = "/oauth2callback"
DEFAULT_SCOPES = " ".join(
    [
        "https://www.googleapis.com/auth/content",
        "https://www.googleapis.com/auth/webmasters.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/calendar.calendarlist.readonly",
        "https://www.googleapis.com/auth/calendar.events.readonly",
        "https://www.googleapis.com/auth/calendar.events.freebusy",
        "https://www.googleapis.com/auth/directory.readonly",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/contacts.readonly",
    ]
)


class CallbackHandler(BaseHTTPRequestHandler):
    code: str | None = None
    error: str | None = None
    expected_state: str | None = None

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if parsed.path != REDIRECT_PATH:
            self.send_response(404)
            self.end_headers()
            return
        state = params.get("state", [""])[0]
        if state != self.expected_state:
            type(self).error = "OAuth state did not match."
        elif "error" in params:
            type(self).error = params["error"][0]
        else:
            type(self).code = params.get("code", [None])[0]

        self.send_response(200 if type(self).code else 400)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"You can close this browser tab and return to Codex.\n")

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    load_env_file()
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    scopes = os.environ.get("GOOGLE_BUSINESS_MCP_SCOPES", DEFAULT_SCOPES)
    login_hint = os.environ.get("GOOGLE_OAUTH_LOGIN_HINT")
    if not client_id or not client_secret:
        raise SystemExit("Set GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET in the env file first.")

    server = HTTPServer(("127.0.0.1", 0), CallbackHandler)
    redirect_uri = f"http://127.0.0.1:{server.server_port}{REDIRECT_PATH}"
    state = secrets.token_urlsafe(24)
    CallbackHandler.expected_state = state

    auth_params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scopes,
            "access_type": "offline",
            "prompt": "consent select_account",
            "state": state,
    }
    if login_hint:
        auth_params["login_hint"] = login_hint
        auth_params["hd"] = login_hint.split("@", 1)[1]

    auth_url = AUTH_ENDPOINT + "?" + urllib.parse.urlencode(auth_params)

    print(f"Opening OAuth URL:\n{auth_url}\n")
    webbrowser.open(auth_url)
    deadline = monotonic() + 300
    while not CallbackHandler.code and not CallbackHandler.error and monotonic() < deadline:
        server.timeout = 5
        server.handle_request()

    if CallbackHandler.error:
        raise SystemExit(CallbackHandler.error)
    if not CallbackHandler.code:
        raise SystemExit("No authorization code received.")

    response = requests.post(
        TOKEN_ENDPOINT,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": CallbackHandler.code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
        timeout=30,
    )
    response.raise_for_status()
    token = response.json()
    save_token(token)
    print(json.dumps({"saved_token_file": os.environ.get("GOOGLE_OAUTH_TOKEN_FILE")}, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

from typing import Any

import requests

from .auth import auth_headers


class GoogleApiError(RuntimeError):
    pass


def request_json(method: str, url: str, **kwargs: Any) -> dict[str, Any]:
    headers = kwargs.pop("headers", {})
    merged_headers = {**auth_headers(), **headers}
    response = requests.request(method, url, headers=merged_headers, timeout=60, **kwargs)
    if response.status_code >= 400:
        raise GoogleApiError(f"{response.status_code} {response.reason}: {response.text[:1000]}")
    if not response.text:
        return {}
    return response.json()


from __future__ import annotations

import base64
from typing import Any
from urllib.parse import quote

import requests

from .auth import auth_headers
from .google_api import request_json


BASE = "https://www.googleapis.com/drive/v3"

DEFAULT_FIELDS = (
    "id,name,mimeType,kind,description,webViewLink,webContentLink,"
    "createdTime,modifiedTime,size,owners(displayName,emailAddress),"
    "lastModifyingUser(displayName,emailAddress),trashed,shared,starred"
)
LIST_FIELDS = f"nextPageToken,files({DEFAULT_FIELDS})"
PERMISSION_FIELDS = "id,type,role,emailAddress,domain,displayName,allowFileDiscovery,deleted"
EXPORT_MIME_TYPES = {
    "application/vnd.google-apps.document": "text/plain",
    "application/vnd.google-apps.spreadsheet": "text/csv",
    "application/vnd.google-apps.presentation": "text/plain",
    "application/vnd.google-apps.drawing": "image/png",
}


def _normalize_order_by(order_by: str | None) -> str:
    return order_by or "modifiedTime desc"


def list_recent_files(page_size: int = 20, page_token: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {
        "pageSize": page_size,
        "orderBy": "modifiedTime desc",
        "fields": LIST_FIELDS,
    }
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{BASE}/files", params=params)


def search_files(
    query: str,
    page_size: int = 20,
    page_token: str | None = None,
    order_by: str | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "q": query,
        "pageSize": page_size,
        "orderBy": _normalize_order_by(order_by),
        "fields": LIST_FIELDS,
    }
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{BASE}/files", params=params)


def get_file_metadata(file_id: str, fields: str = DEFAULT_FIELDS) -> dict[str, Any]:
    return request_json("GET", f"{BASE}/files/{quote(file_id, safe='')}", params={"fields": fields})


def get_file_permissions(file_id: str, page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {
        "pageSize": page_size,
        "fields": f"nextPageToken,permissions({PERMISSION_FIELDS})",
    }
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{BASE}/files/{quote(file_id, safe='')}/permissions", params=params)


def read_file_content(file_id: str, mime_type: str | None = None, max_bytes: int = 200_000) -> dict[str, Any]:
    metadata = get_file_metadata(file_id=file_id, fields="id,name,mimeType,size")
    source_mime_type = metadata.get("mimeType")
    export_mime_type = mime_type or EXPORT_MIME_TYPES.get(str(source_mime_type))

    if str(source_mime_type).startswith("application/vnd.google-apps."):
        if not export_mime_type:
            raise RuntimeError(f"No default export MIME type for {source_mime_type}; pass mime_type explicitly.")
        url = f"{BASE}/files/{quote(file_id, safe='')}/export"
        params = {"mimeType": export_mime_type}
    else:
        url = f"{BASE}/files/{quote(file_id, safe='')}"
        params = {"alt": "media"}
        export_mime_type = source_mime_type

    response = requests.get(url, headers=auth_headers(), params=params, timeout=60)
    if response.status_code >= 400:
        raise RuntimeError(f"{response.status_code} {response.reason}: {response.text[:1000]}")

    content = response.content[:max_bytes]
    truncated = len(response.content) > max_bytes
    try:
        text = content.decode(response.encoding or "utf-8")
        return {
            "metadata": metadata,
            "mimeType": export_mime_type,
            "encoding": "text",
            "content": text,
            "truncated": truncated,
        }
    except UnicodeDecodeError:
        return {
            "metadata": metadata,
            "mimeType": export_mime_type,
            "encoding": "base64",
            "content": base64.b64encode(content).decode("ascii"),
            "truncated": truncated,
        }


def download_file_content(file_id: str, mime_type: str | None = None, max_bytes: int = 2_000_000) -> dict[str, Any]:
    result = read_file_content(file_id=file_id, mime_type=mime_type, max_bytes=max_bytes)
    result["note"] = "Content is returned inline as text or base64, capped by max_bytes."
    return result

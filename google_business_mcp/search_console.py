from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .google_api import request_json


BASE = "https://searchconsole.googleapis.com/webmasters/v3"
INSPECTION_BASE = "https://searchconsole.googleapis.com/v1"


def list_sites() -> dict[str, Any]:
    return request_json("GET", f"{BASE}/sites")


def search_analytics(site_url: str, start_date: str, end_date: str, dimensions: list[str] | None = None, row_limit: int = 1000, start_row: int = 0) -> dict[str, Any]:
    body: dict[str, Any] = {
        "startDate": start_date,
        "endDate": end_date,
        "rowLimit": row_limit,
        "startRow": start_row,
    }
    if dimensions:
        body["dimensions"] = dimensions
    return request_json("POST", f"{BASE}/sites/{quote(site_url, safe='')}/searchAnalytics/query", json=body)


def inspect_url(site_url: str, inspection_url: str, language_code: str = "en-US") -> dict[str, Any]:
    return request_json(
        "POST",
        f"{INSPECTION_BASE}/urlInspection/index:inspect",
        json={"siteUrl": site_url, "inspectionUrl": inspection_url, "languageCode": language_code},
    )


def list_sitemaps(site_url: str) -> dict[str, Any]:
    return request_json("GET", f"{BASE}/sites/{quote(site_url, safe='')}/sitemaps")


def get_sitemap(site_url: str, feedpath: str) -> dict[str, Any]:
    return request_json("GET", f"{BASE}/sites/{quote(site_url, safe='')}/sitemaps/{quote(feedpath, safe='')}")


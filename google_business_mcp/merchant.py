from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .google_api import request_json


BASE = "https://merchantapi.googleapis.com"


def list_accounts(page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"pageSize": page_size}
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{BASE}/accounts/v1/accounts", params=params)


def list_products(account: str, page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"pageSize": page_size}
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{BASE}/products/v1/{quote(account, safe='/')}/products", params=params)


def get_product(product_name: str) -> dict[str, Any]:
    return request_json("GET", f"{BASE}/products/v1/{quote(product_name, safe='/')}")


def list_product_statuses(account: str, page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"pageSize": page_size}
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{BASE}/issueresolution/v1/{quote(account, safe='/')}/aggregateProductStatuses", params=params)


def list_product_issues(account: str, language_code: str = "en-US", page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    statuses = list_product_statuses(account=account, page_size=page_size, page_token=page_token)
    issues: list[dict[str, Any]] = []
    for status in statuses.get("aggregateProductStatuses", []):
        for issue in status.get("itemLevelIssues", []):
            issues.append(
                {
                    **issue,
                    "aggregateProductStatus": status.get("name"),
                    "reportingContext": status.get("reportingContext"),
                    "country": status.get("country"),
                }
            )
    return {"productIssues": issues, "nextPageToken": statuses.get("nextPageToken")}


def query_reports(account: str, query: str, page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {"query": query, "pageSize": page_size}
    if page_token:
        body["pageToken"] = page_token
    return request_json("POST", f"{BASE}/reports/v1/{quote(account, safe='/')}/reports:search", json=body)

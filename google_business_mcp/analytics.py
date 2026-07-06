from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .google_api import request_json


ADMIN_BASE = "https://analyticsadmin.googleapis.com/v1beta"
DATA_BASE = "https://analyticsdata.googleapis.com/v1beta"


def _property_path(property_id: str) -> str:
    name = property_id if property_id.startswith("properties/") else f"properties/{property_id}"
    return quote(name, safe="/")


def list_account_summaries(page_size: int = 200, page_token: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"pageSize": page_size}
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{ADMIN_BASE}/accountSummaries", params=params)


def list_properties(filter: str, page_size: int = 200, page_token: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"filter": filter, "pageSize": page_size}
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{ADMIN_BASE}/properties", params=params)


def get_property(property_id: str) -> dict[str, Any]:
    return request_json("GET", f"{ADMIN_BASE}/{_property_path(property_id)}")


def get_metadata(property_id: str) -> dict[str, Any]:
    return request_json("GET", f"{DATA_BASE}/{_property_path(property_id)}/metadata")


def run_report(
    property_id: str,
    metrics: list[str],
    start_date: str,
    end_date: str,
    dimensions: list[str] | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "metrics": [{"name": name} for name in metrics],
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
    }
    if dimensions:
        body["dimensions"] = [{"name": name} for name in dimensions]
    if limit is not None:
        body["limit"] = limit
    if offset is not None:
        body["offset"] = offset
    return request_json("POST", f"{DATA_BASE}/{_property_path(property_id)}:runReport", json=body)


def run_realtime_report(
    property_id: str,
    metrics: list[str],
    dimensions: list[str] | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"metrics": [{"name": name} for name in metrics]}
    if dimensions:
        body["dimensions"] = [{"name": name} for name in dimensions]
    if limit is not None:
        body["limit"] = limit
    return request_json("POST", f"{DATA_BASE}/{_property_path(property_id)}:runRealtimeReport", json=body)

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .google_api import request_json


GMAIL_BASE = "https://gmail.googleapis.com/gmail/v1/users/me"
CALENDAR_BASE = "https://www.googleapis.com/calendar/v3"
PEOPLE_BASE = "https://people.googleapis.com/v1"


def gmail_list_labels() -> dict[str, Any]:
    return request_json("GET", f"{GMAIL_BASE}/labels")


def gmail_search_threads(query: str, max_results: int = 10, page_token: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"q": query, "maxResults": max_results}
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{GMAIL_BASE}/threads", params=params)


def gmail_get_thread(thread_id: str, fmt: str = "metadata", metadata_headers: list[str] | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"format": fmt}
    if metadata_headers:
        params["metadataHeaders"] = metadata_headers
    return request_json("GET", f"{GMAIL_BASE}/threads/{quote(thread_id, safe='')}", params=params)


def calendar_list_calendars(max_results: int = 50, page_token: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"maxResults": max_results}
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{CALENDAR_BASE}/users/me/calendarList", params=params)


def calendar_list_events(
    calendar_id: str = "primary",
    time_min: str | None = None,
    time_max: str | None = None,
    max_results: int = 10,
    single_events: bool = True,
    order_by: str = "startTime",
    page_token: str | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "maxResults": max_results,
        "singleEvents": str(single_events).lower(),
        "orderBy": order_by,
    }
    if time_min:
        params["timeMin"] = time_min
    if time_max:
        params["timeMax"] = time_max
    if page_token:
        params["pageToken"] = page_token
    return request_json("GET", f"{CALENDAR_BASE}/calendars/{quote(calendar_id, safe='')}/events", params=params)


def calendar_get_event(calendar_id: str, event_id: str) -> dict[str, Any]:
    return request_json(
        "GET",
        f"{CALENDAR_BASE}/calendars/{quote(calendar_id, safe='')}/events/{quote(event_id, safe='')}",
    )


def people_get_user_profile() -> dict[str, Any]:
    return request_json(
        "GET",
        f"{PEOPLE_BASE}/people/me",
        params={"personFields": "names,emailAddresses,photos,organizations"},
    )


def people_search_contacts(query: str, page_size: int = 10) -> dict[str, Any]:
    return request_json(
        "GET",
        f"{PEOPLE_BASE}/people:searchContacts",
        params={
            "query": query,
            "pageSize": page_size,
            "readMask": "names,emailAddresses,phoneNumbers,organizations",
        },
    )


def people_search_directory(query: str, page_size: int = 10) -> dict[str, Any]:
    return request_json(
        "GET",
        f"{PEOPLE_BASE}/people:searchDirectoryPeople",
        params={
            "query": query,
            "pageSize": page_size,
            "readMask": "names,emailAddresses,phoneNumbers,organizations",
            "sources": "DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE",
        },
    )

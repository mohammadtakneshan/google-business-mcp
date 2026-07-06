from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from . import analytics, drive, merchant, search_console, workspace


mcp = FastMCP("google-business")


@mcp.tool(name="google.help_overview")
def google_help_overview() -> dict[str, Any]:
    """Return local usage guidance for the Google Business MCP."""
    return {
        "mcp": "google_business",
        "purpose": "Read-only MCP for Google business data and Google Workspace access.",
        "readOnlyPolicy": "This MCP exposes only read-only Merchant Center, Search Console, and Drive tools. No write or mutation tools are registered.",
        "accounts": {
            "merchant": {
                "name": os.environ.get("GOOGLE_BUSINESS_MERCHANT_ACCOUNT", "accounts/YOUR_MERCHANT_ACCOUNT_ID"),
                "displayName": os.environ.get("GOOGLE_BUSINESS_MERCHANT_DISPLAY_NAME", "Your merchant account"),
            },
            "searchConsole": {"siteUrl": os.environ.get("GOOGLE_BUSINESS_SEARCH_CONSOLE_SITE", "https://example.com/")},
            "analytics": {"propertyId": os.environ.get("GOOGLE_ANALYTICS_PROPERTY_ID", "properties/YOUR_PROPERTY_ID")},
            "googleCloudProjectNumber": os.environ.get("GOOGLE_CLOUD_PROJECT_NUMBER", "YOUR_PROJECT_NUMBER"),
        },
        "liveTools": {
            "merchant": [
                "merchant.list_accounts",
                "merchant.list_products",
                "merchant.get_product",
                "merchant.list_product_statuses",
                "merchant.list_product_issues",
                "merchant.query_reports",
            ],
            "searchConsole": [
                "gsc.list_sites",
                "gsc.search_analytics",
                "gsc.inspect_url",
                "gsc.list_sitemaps",
                "gsc.get_sitemap",
            ],
            "drive": [
                "drive.list_recent_files",
                "drive.search_files",
                "drive.get_file_metadata",
                "drive.get_file_permissions",
                "drive.read_file_content",
                "drive.download_file_content",
            ],
            "workspace": [
                "gmail.list_labels",
                "gmail.search_threads",
                "gmail.get_thread",
                "calendar.list_calendars",
                "calendar.list_events",
                "calendar.get_event",
                "people.get_user_profile",
                "people.search_contacts",
                "people.search_directory",
            ],
            "analytics": [
                "analytics.list_account_summaries",
                "analytics.list_properties",
                "analytics.get_property",
                "analytics.get_metadata",
                "analytics.run_report",
                "analytics.run_realtime_report",
            ],
        },
        "authNotes": [
            "OAuth credentials are loaded from GOOGLE_BUSINESS_MCP_ENV.",
            "Merchant API requires the broad https://www.googleapis.com/auth/content scope, but this MCP exposes read-only tools only.",
            "Drive tools use https://www.googleapis.com/auth/drive.readonly.",
            "Analytics tools use https://www.googleapis.com/auth/analytics.readonly and require the Google Analytics Admin API and Data API to be enabled.",
            "Workspace tools are intentionally read-only and are separate from Claude.ai Google connectors.",
            "Google Ads and Google Business Profile are not exposed yet; they require a developer token and API allowlisting respectively.",
        ],
    }


@mcp.tool(name="google.docs_links")
def google_docs_links() -> dict[str, Any]:
    """Return official documentation links relevant to this MCP."""
    return {
        "merchantApi": "https://developers.google.com/merchant/api",
        "merchantReports": "https://developers.google.com/merchant/api/guides/reports/overview",
        "merchantApiDeveloperRegistration": "https://developers.google.com/merchant/api/guides/quickstart/direct-api-calls#step_1_register_as_a_developer",
        "searchConsoleApi": "https://developers.google.com/webmaster-tools/v1/api_reference_index",
        "urlInspectionApi": "https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect",
        "driveApi": "https://developers.google.com/drive/api/reference/rest/v3",
        "analyticsDataApi": "https://developers.google.com/analytics/devguides/reporting/data/v1/rest",
        "analyticsAdminApi": "https://developers.google.com/analytics/devguides/config/admin/v1/rest",
        "googleWorkspaceMcp": "https://developers.google.com/workspace/guides/configure-mcp-servers",
        "gmailApi": "https://developers.google.com/gmail/api/reference/rest",
        "calendarApi": "https://developers.google.com/workspace/calendar/api/v3/reference",
        "peopleApi": "https://developers.google.com/people/api/rest",
        "codexMcp": "https://developers.openai.com/codex/mcp",
    }


@mcp.tool(name="merchant.query_examples")
def merchant_query_examples() -> dict[str, Any]:
    """Return known-good Merchant Center report query examples."""
    return {
        "notes": [
            "Merchant reports use lowercase MCQL view names.",
            "Use account resource names like accounts/YOUR_MERCHANT_ACCOUNT_ID.",
        ],
        "examples": {
            "last7DaysPerformance": (
                "SELECT date, impressions, clicks "
                "FROM product_performance_view "
                "WHERE date DURING LAST_7_DAYS "
                "LIMIT 5"
            ),
            "last30DaysProductPerformance": (
                "SELECT offer_id, title, impressions, clicks "
                "FROM product_performance_view "
                "WHERE date DURING LAST_30_DAYS "
                "LIMIT 20"
            ),
        },
    }


@mcp.tool(name="merchant.list_accounts")
def merchant_list_accounts(page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    """List Merchant Center accounts visible to the authenticated user."""
    return merchant.list_accounts(page_size=page_size, page_token=page_token)


@mcp.tool(name="merchant.list_products")
def merchant_list_products(account: str, page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    """List products for a Merchant API account resource such as accounts/123."""
    return merchant.list_products(account=account, page_size=page_size, page_token=page_token)


@mcp.tool(name="merchant.get_product")
def merchant_get_product(product_name: str) -> dict[str, Any]:
    """Get one Merchant product by full resource name."""
    return merchant.get_product(product_name=product_name)


@mcp.tool(name="merchant.list_product_statuses")
def merchant_list_product_statuses(account: str, page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    """List read-only product status resources for a Merchant API account."""
    return merchant.list_product_statuses(account=account, page_size=page_size, page_token=page_token)


@mcp.tool(name="merchant.list_product_issues")
def merchant_list_product_issues(account: str, language_code: str = "en-US", page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    """List read-only product issues for a Merchant API account."""
    return merchant.list_product_issues(account=account, language_code=language_code, page_size=page_size, page_token=page_token)


@mcp.tool(name="merchant.query_reports")
def merchant_query_reports(account: str, query: str, page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    """Run a Merchant reports search query."""
    return merchant.query_reports(account=account, query=query, page_size=page_size, page_token=page_token)


@mcp.tool(name="gsc.list_sites")
def gsc_list_sites() -> dict[str, Any]:
    """List Search Console sites visible to the authenticated user."""
    return search_console.list_sites()


@mcp.tool(name="gsc.search_analytics")
def gsc_search_analytics(site_url: str, start_date: str, end_date: str, dimensions: list[str] | None = None, row_limit: int = 1000, start_row: int = 0) -> dict[str, Any]:
    """Query Search Console Search Analytics for a site."""
    return search_console.search_analytics(
        site_url=site_url,
        start_date=start_date,
        end_date=end_date,
        dimensions=dimensions,
        row_limit=row_limit,
        start_row=start_row,
    )


@mcp.tool(name="gsc.inspect_url")
def gsc_inspect_url(site_url: str, inspection_url: str, language_code: str = "en-US") -> dict[str, Any]:
    """Inspect Google index status for a URL in Search Console."""
    return search_console.inspect_url(site_url=site_url, inspection_url=inspection_url, language_code=language_code)


@mcp.tool(name="gsc.list_sitemaps")
def gsc_list_sitemaps(site_url: str) -> dict[str, Any]:
    """List Search Console sitemaps for a site."""
    return search_console.list_sitemaps(site_url=site_url)


@mcp.tool(name="gsc.get_sitemap")
def gsc_get_sitemap(site_url: str, feedpath: str) -> dict[str, Any]:
    """Get one Search Console sitemap by feed path."""
    return search_console.get_sitemap(site_url=site_url, feedpath=feedpath)


@mcp.tool(name="drive.list_recent_files")
def drive_list_recent_files(page_size: int = 20, page_token: str | None = None) -> dict[str, Any]:
    """List recently modified Google Drive files visible to the authenticated user."""
    return drive.list_recent_files(page_size=page_size, page_token=page_token)


@mcp.tool(name="drive.search_files")
def drive_search_files(query: str, page_size: int = 20, page_token: str | None = None, order_by: str | None = None) -> dict[str, Any]:
    """Search Google Drive files using Drive API v3 query syntax."""
    return drive.search_files(query=query, page_size=page_size, page_token=page_token, order_by=order_by)


@mcp.tool(name="drive.get_file_metadata")
def drive_get_file_metadata(file_id: str, fields: str = drive.DEFAULT_FIELDS) -> dict[str, Any]:
    """Get Google Drive file metadata by file ID."""
    return drive.get_file_metadata(file_id=file_id, fields=fields)


@mcp.tool(name="drive.get_file_permissions")
def drive_get_file_permissions(file_id: str, page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
    """List permissions for a Google Drive file."""
    return drive.get_file_permissions(file_id=file_id, page_size=page_size, page_token=page_token)


@mcp.tool(name="drive.read_file_content")
def drive_read_file_content(file_id: str, mime_type: str | None = None, max_bytes: int = 200_000) -> dict[str, Any]:
    """Read Google Drive file content inline as text or base64."""
    return drive.read_file_content(file_id=file_id, mime_type=mime_type, max_bytes=max_bytes)


@mcp.tool(name="drive.download_file_content")
def drive_download_file_content(file_id: str, mime_type: str | None = None, max_bytes: int = 2_000_000) -> dict[str, Any]:
    """Download Google Drive file content inline as text or base64, capped by max_bytes."""
    return drive.download_file_content(file_id=file_id, mime_type=mime_type, max_bytes=max_bytes)


@mcp.tool(name="gmail.list_labels")
def gmail_list_labels() -> dict[str, Any]:
    """List Gmail labels visible to the authenticated user."""
    return workspace.gmail_list_labels()


@mcp.tool(name="gmail.search_threads")
def gmail_search_threads(query: str, max_results: int = 10, page_token: str | None = None) -> dict[str, Any]:
    """Search Gmail threads with Gmail query syntax. Read-only."""
    return workspace.gmail_search_threads(query=query, max_results=max_results, page_token=page_token)


@mcp.tool(name="gmail.get_thread")
def gmail_get_thread(thread_id: str, fmt: str = "metadata", metadata_headers: list[str] | None = None) -> dict[str, Any]:
    """Get one Gmail thread. Defaults to metadata to avoid pulling full email bodies unless requested."""
    return workspace.gmail_get_thread(thread_id=thread_id, fmt=fmt, metadata_headers=metadata_headers)


@mcp.tool(name="calendar.list_calendars")
def calendar_list_calendars(max_results: int = 50, page_token: str | None = None) -> dict[str, Any]:
    """List calendars visible to the authenticated user."""
    return workspace.calendar_list_calendars(max_results=max_results, page_token=page_token)


@mcp.tool(name="calendar.list_events")
def calendar_list_events(
    calendar_id: str = "primary",
    time_min: str | None = None,
    time_max: str | None = None,
    max_results: int = 10,
    single_events: bool = True,
    order_by: str = "startTime",
    page_token: str | None = None,
) -> dict[str, Any]:
    """List read-only calendar events for a calendar."""
    return workspace.calendar_list_events(
        calendar_id=calendar_id,
        time_min=time_min,
        time_max=time_max,
        max_results=max_results,
        single_events=single_events,
        order_by=order_by,
        page_token=page_token,
    )


@mcp.tool(name="calendar.get_event")
def calendar_get_event(calendar_id: str, event_id: str) -> dict[str, Any]:
    """Get one calendar event by calendar ID and event ID."""
    return workspace.calendar_get_event(calendar_id=calendar_id, event_id=event_id)


@mcp.tool(name="people.get_user_profile")
def people_get_user_profile() -> dict[str, Any]:
    """Get the authenticated user's Google profile."""
    return workspace.people_get_user_profile()


@mcp.tool(name="people.search_contacts")
def people_search_contacts(query: str, page_size: int = 10) -> dict[str, Any]:
    """Search the authenticated user's Google contacts. Read-only."""
    return workspace.people_search_contacts(query=query, page_size=page_size)


@mcp.tool(name="people.search_directory")
def people_search_directory(query: str, page_size: int = 10) -> dict[str, Any]:
    """Search Google Workspace directory people. Read-only."""
    return workspace.people_search_directory(query=query, page_size=page_size)


@mcp.tool(name="analytics.list_account_summaries")
def analytics_list_account_summaries(page_size: int = 200, page_token: str | None = None) -> dict[str, Any]:
    """List GA4 account summaries (accounts and their properties). Read-only."""
    return analytics.list_account_summaries(page_size=page_size, page_token=page_token)


@mcp.tool(name="analytics.list_properties")
def analytics_list_properties(filter: str, page_size: int = 200, page_token: str | None = None) -> dict[str, Any]:
    """List GA4 properties matching a filter such as parent:accounts/123. Read-only."""
    return analytics.list_properties(filter=filter, page_size=page_size, page_token=page_token)


@mcp.tool(name="analytics.get_property")
def analytics_get_property(property_id: str) -> dict[str, Any]:
    """Get one GA4 property by id or resource name (properties/123). Read-only."""
    return analytics.get_property(property_id=property_id)


@mcp.tool(name="analytics.get_metadata")
def analytics_get_metadata(property_id: str) -> dict[str, Any]:
    """Get available GA4 dimensions and metrics for a property. Read-only."""
    return analytics.get_metadata(property_id=property_id)


@mcp.tool(name="analytics.run_report")
def analytics_run_report(
    property_id: str,
    metrics: list[str],
    start_date: str,
    end_date: str,
    dimensions: list[str] | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any]:
    """Run a GA4 Data API report for a property. Read-only.

    Dates accept YYYY-MM-DD or relative values like 7daysAgo/today.
    """
    return analytics.run_report(
        property_id=property_id,
        metrics=metrics,
        start_date=start_date,
        end_date=end_date,
        dimensions=dimensions,
        limit=limit,
        offset=offset,
    )


@mcp.tool(name="analytics.run_realtime_report")
def analytics_run_realtime_report(
    property_id: str,
    metrics: list[str],
    dimensions: list[str] | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Run a GA4 Data API realtime report for a property. Read-only."""
    return analytics.run_realtime_report(
        property_id=property_id,
        metrics=metrics,
        dimensions=dimensions,
        limit=limit,
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()

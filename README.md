# Google Business MCP

Read-only MCP server for Google Merchant Center, Google Search Console, Google Drive, Google Analytics (GA4), and selected Google Workspace surfaces.

Use `google_business` as the only enabled day-to-day Google business MCP in
Codex. Separate docs MCPs and the Google Ads MCP can stay configured but
disabled unless they are needed later.

## Setup

1. Create OAuth credentials in Google Cloud for a desktop app.
2. Enable these APIs in the same project:
   - Merchant API
   - Search Console API
   - Google Drive API
   - Gmail API
   - Google Calendar API
   - People API
   - Google Analytics Admin API
   - Google Analytics Data API
3. Create `~/.codex/secrets/google/google-business-mcp.env` from `.env.example`.
4. Run the OAuth helper:

```bash
python3 scripts/oauth_authorize.py
```

The helper writes a refresh token to the token path configured in the env file.

Merchant API currently requires the `https://www.googleapis.com/auth/content`
OAuth scope. The MCP only exposes read-only tools, but Google does not provide a
separate Merchant API read-only OAuth scope.

Analytics tools use the read-only `https://www.googleapis.com/auth/analytics.readonly`
scope and require both the Google Analytics Admin API and the Google Analytics
Data API to be enabled in the project.

## Local account labels

Optional local labels can be set in your private env file. Keep real account
IDs, project numbers, login hints, and token paths out of git.

- `GOOGLE_BUSINESS_MERCHANT_ACCOUNT`
- `GOOGLE_BUSINESS_MERCHANT_DISPLAY_NAME`
- `GOOGLE_BUSINESS_SEARCH_CONSOLE_SITE`
- `GOOGLE_ANALYTICS_PROPERTY_ID`
- `GOOGLE_CLOUD_PROJECT_NUMBER`

## Merchant notes

- Product status and product issue data comes from
  `issueresolution/v1/{account}/aggregateProductStatuses`.
- `merchant.list_product_issues` flattens the `itemLevelIssues` returned by
  aggregate product statuses.
- Valid Merchant reports queries use lowercase MCQL view names, for example:

```sql
SELECT date, impressions, clicks
FROM product_performance_view
WHERE date DURING LAST_7_DAYS
LIMIT 5
```

## Read-only tools

- `google.help_overview`
- `google.docs_links`
- `merchant.list_accounts`
- `merchant.list_products`
- `merchant.get_product`
- `merchant.list_product_statuses`
- `merchant.list_product_issues`
- `merchant.query_reports`
- `merchant.query_examples`
- `gsc.list_sites`
- `gsc.search_analytics`
- `gsc.inspect_url`
- `gsc.list_sitemaps`
- `gsc.get_sitemap`
- `drive.list_recent_files`
- `drive.search_files`
- `drive.get_file_metadata`
- `drive.get_file_permissions`
- `drive.read_file_content`
- `drive.download_file_content`
- `gmail.list_labels`
- `gmail.search_threads`
- `gmail.get_thread`
- `calendar.list_calendars`
- `calendar.list_events`
- `calendar.get_event`
- `people.get_user_profile`
- `people.search_contacts`
- `people.search_directory`
- `analytics.list_account_summaries`
- `analytics.list_properties`
- `analytics.get_property`
- `analytics.get_metadata`
- `analytics.run_report`
- `analytics.run_realtime_report`

## Google Workspace MCP note

Google's official Workspace MCP servers are live as a Developer Preview as of
July 2026. This local MCP remains a durable Codex-side, read-only Google
business and Workspace surface for Merchant Center, Search Console, Drive,
Gmail, Calendar, and People.

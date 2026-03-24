---
name: google-sheets
version: 1.0.0
tier: business-ops
description: "Spreadsheet operations for small businesses. Sales tracking, inventory management, expense reports, simple dashboards, and data import/export. Built on the gws CLI."
requires:
  bins: ["gws"]
  skills: ["google-workspace"]
---

# Google Sheets

**Spreadsheet operations built for how small businesses actually track data.**

Uses the [gws CLI](https://github.com/googleworkspace/cli) for all Sheets operations. See the `google-workspace` skill for setup.

## Triggers

- "read the spreadsheet"
- "update the sheet"
- "add a row to..."
- "create a spreadsheet"
- "pull data from sheets"
- "log this to a spreadsheet"
- Any request involving spreadsheet read/write operations

## Prerequisites

- `gws` CLI installed and authenticated with Sheets + Drive scope
- Run `gws auth login -s sheets,drive` if not already done

## Core Commands

```bash
gws sheets +read                   # Read values from a spreadsheet
gws sheets +append                 # Append a row to a spreadsheet
gws sheets spreadsheets create     # Create a new spreadsheet
gws sheets spreadsheets get        # Get spreadsheet metadata
```

## Common Operations

### Read data from a sheet

```bash
# Read a range
gws sheets +read
# When prompted: spreadsheet ID + range (e.g., "Sheet1!A1:D10")

# Read via API directly
gws sheets spreadsheets values get --params '{
  "spreadsheetId": "SPREADSHEET_ID",
  "range": "Sheet1!A1:D100"
}'

# Read entire sheet
gws sheets spreadsheets values get --params '{
  "spreadsheetId": "SPREADSHEET_ID",
  "range": "Sheet1"
}'
```

### Append a row

```bash
# Append a single row
gws sheets +append
# When prompted: spreadsheet ID, range, values

# Append via API directly
gws sheets spreadsheets values append --params '{
  "spreadsheetId": "SPREADSHEET_ID",
  "range": "Sheet1!A:D",
  "valueInputOption": "USER_ENTERED"
}' --json '{
  "values": [["2025-01-15", "Widget A", "50", "$12.50"]]
}'
```

### Write / Update cells

```bash
# Update a specific range
gws sheets spreadsheets values update --params '{
  "spreadsheetId": "SPREADSHEET_ID",
  "range": "Sheet1!B2",
  "valueInputOption": "USER_ENTERED"
}' --json '{
  "values": [["updated value"]]
}'

# Batch update multiple ranges
gws sheets spreadsheets values batchUpdate --params '{
  "spreadsheetId": "SPREADSHEET_ID"
}' --json '{
  "valueInputOption": "USER_ENTERED",
  "data": [
    {"range": "Sheet1!A1", "values": [["Revenue"]]},
    {"range": "Sheet1!B1", "values": [["Date"]]},
    {"range": "Sheet1!A2", "values": [["$1,250"]]}
  ]
}'
```

### Create a new spreadsheet

```bash
gws sheets spreadsheets create --json '{
  "properties": {"title": "Q1 2025 Sales Tracker"},
  "sheets": [
    {"properties": {"title": "Daily Sales"}},
    {"properties": {"title": "Summary"}},
    {"properties": {"title": "By Product"}}
  ]
}'
```

## SMB Spreadsheet Patterns

### Daily Sales Log

Track daily revenue with a simple append workflow:

```bash
# Append today's sales data
gws sheets spreadsheets values append --params '{
  "spreadsheetId": "SALES_SHEET_ID",
  "range": "Daily Sales!A:E",
  "valueInputOption": "USER_ENTERED"
}' --json '{
  "values": [["2025-01-15", "Store 1", "$2,450", "87 transactions", "Wednesday"]]
}'
```

### Inventory Tracking

```bash
# Read current inventory levels
gws sheets spreadsheets values get --params '{
  "spreadsheetId": "INVENTORY_SHEET_ID",
  "range": "Current Stock!A:D"
}' --format json | jq '.values[] | select(.[2] | tonumber < 10)'
# Find items with less than 10 units
```

### Expense Tracking

```bash
# Log an expense
gws sheets spreadsheets values append --params '{
  "spreadsheetId": "EXPENSE_SHEET_ID",
  "range": "Expenses!A:E",
  "valueInputOption": "USER_ENTERED"
}' --json '{
  "values": [["2025-01-15", "Office Supplies", "Staples", "$47.32", "Receipt in Drive"]]
}'
```

### Simple Reporting

```bash
# Read summary data for a report
gws sheets spreadsheets values get --params '{
  "spreadsheetId": "REPORT_SHEET_ID",
  "range": "Summary!A1:C12"
}' --format table
```

## Data Export

```bash
# Export sheet as CSV (via Drive export)
gws drive files export --params '{
  "fileId": "SPREADSHEET_ID",
  "mimeType": "text/csv"
}' -o ./export.csv

# Export as Excel
gws drive files export --params '{
  "fileId": "SPREADSHEET_ID",
  "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}' -o ./export.xlsx
```

## Finding Spreadsheets

```bash
# List all spreadsheets
gws drive files list --params '{
  "q": "mimeType=\"application/vnd.google-apps.spreadsheet\"",
  "pageSize": 20,
  "orderBy": "modifiedTime desc"
}' --format table

# Search by name
gws drive files list --params '{
  "q": "mimeType=\"application/vnd.google-apps.spreadsheet\" and name contains '\''sales'\''",
  "pageSize": 10
}'
```

## Integration with Other Skills

- **`autoresearch`** — Track experiment results in sheets; use sheet data as eval input
- **`google-drive`** — Sheets are Drive files; use Drive for search and permissions
- **`gmail`** — Email sheet data as reports
- **`morning-briefing`** — Pull KPIs from sheets for daily briefing
- **`semantic-layer-audit`** — Document sheet data sources in your semantic layer

## Tips

- Use `valueInputOption: "USER_ENTERED"` to let Sheets parse dates, numbers, and formulas
- Use `valueInputOption: "RAW"` when you want exact text (no parsing)
- Spreadsheet IDs are in the URL: `docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
- Use named ranges in your sheets for more readable API calls
- For large datasets, consider BigQuery instead of Sheets (Sheets has a 10M cell limit)
- `--format csv` output from `gws` can be piped directly into other tools

## Related Skills

- `google-workspace` — Required setup (install and auth)
- `google-drive` — File-level operations on spreadsheets
- `autoresearch` — Use sheets as parameter/experiment tracking
- `morning-briefing` — Pull sheet KPIs into daily digest

---

*Sheets are the swiss army knife of small business data. Simple, flexible, and accessible.*

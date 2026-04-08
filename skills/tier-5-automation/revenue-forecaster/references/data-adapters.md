# Data Adapters — Bring Your Own History

The forecaster reads a **single CSV** with three columns: `week_start`, `entity`, `revenue`. This page shows how to produce that CSV from the most common data sources. Pick the one that matches your stack.

## Expected Format

```csv
week_start,entity,revenue
2025-10-06,Main Street,48350.00
2025-10-06,Downtown,32110.00
2025-10-13,Main Street,51200.00
2025-10-13,Downtown,34780.00
2025-10-20,Main Street,47980.00
2025-10-20,Downtown,33450.00
```

Rules:

- `week_start` is the **Monday** of the week (ISO week start). If your source uses Sundays or arbitrary week boundaries, you'll need to re-align.
- `entity` is a free-form label — location name, product line, store number, region, anything. Use the same label consistently across rows.
- `revenue` is the total revenue for that entity for that week, as a number (no currency symbol, no thousands separator).
- **Minimum usable history:** 8 weeks per entity. **Good:** 6+ months. **Great:** 1+ year (unlocks YoY blending).

## Adapter 1 — Google Sheets

If your historical revenue lives in a sheet, use the [`google-sheets`](../../tier-3-business-ops/google-sheets/) skill to pull it down as CSV.

```bash
# Pull the range into a CSV
gws sheets spreadsheets values get --params '{
  "spreadsheetId": "YOUR_SHEET_ID",
  "range": "Weekly Sales!A:C"
}' --format csv > data/history.csv

# Feed it to the forecaster
python3 scripts/forecast.py --data data/history.csv --params config/parameters.json
```

If your sheet has headers in row 1 that don't match `week_start,entity,revenue`, either rename them in the sheet or pipe through a quick `awk`/`sed` to rewrite the header row before passing to `forecast.py`.

## Adapter 2 — BigQuery

For data warehoused in BigQuery:

```bash
bq query --use_legacy_sql=false --format=csv '
  SELECT
    DATE_TRUNC(DATE(transaction_date), WEEK(MONDAY)) AS week_start,
    location_name                                   AS entity,
    SUM(revenue)                                    AS revenue
  FROM `your-project.your_dataset.daily_sales`
  WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 24 MONTH)
  GROUP BY week_start, entity
  ORDER BY week_start, entity
' > data/history.csv

python3 scripts/forecast.py --data data/history.csv
```

**Cost note:** `bq query` bills by bytes scanned. For large tables, add a partition filter (`WHERE _PARTITIONDATE >= ...`) to avoid a full scan.

## Adapter 3 — Square POS (via Square Connect API)

If you're on Square, the most authoritative source for "what hit the bank" is the Payouts endpoint, not raw transactions (which can include refunds and disputes).

```bash
# Prerequisite: Square access token in your secrets manager
export SQUARE_TOKEN=$(gcloud secrets versions access latest --secret=square-access-token)

# Pull 52 weeks of payouts for a specific location
curl -sS -H "Authorization: Bearer $SQUARE_TOKEN" \
  -H "Square-Version: 2024-10-17" \
  "https://connect.squareup.com/v2/payouts?location_id=LXXXXXXXXXXXX&begin_time=2025-04-01T00:00:00Z&limit=100" \
  | jq -r '
      .payouts[] |
      [
        (.created_at | sub("T.*"; "") | strptime("%Y-%m-%d") | mktime |
          . - ((.  / 86400 % 7) * 86400) | strftime("%Y-%m-%d")),
        "Main Street",
        (.amount_money.amount / 100)
      ] | @csv
    ' \
  > data/history.csv

# Add the header row
sed -i '' '1i\
week_start,entity,revenue
' data/history.csv
```

The `jq` filter rounds each payout date down to the preceding Monday. If you have multiple locations, run the curl once per location and concat the CSVs (or use a loop).

**Gotchas:**

- Square's Payouts API is paginated — for 52+ weeks you'll need to follow the `cursor` field.
- The `amount` field is in cents; divide by 100 for dollars.
- If you want to use *sales* instead of payouts (e.g., to include tips or exclude chargebacks), query `v2/orders/search` instead — but sales won't match what actually hit your bank.

## Adapter 4 — Shopify

```bash
# Prerequisite: Shopify admin API token
export SHOPIFY_TOKEN=$(gcloud secrets versions access latest --secret=shopify-admin-token)

# Shopify GraphQL — pull weekly revenue aggregated client-side
curl -sS -X POST \
  -H "X-Shopify-Access-Token: $SHOPIFY_TOKEN" \
  -H "Content-Type: application/json" \
  "https://YOUR_SHOP.myshopify.com/admin/api/2024-10/graphql.json" \
  -d '{
    "query": "{ orders(first: 250, query: \"created_at:>=2025-04-01 financial_status:paid\") { edges { node { createdAt totalPriceSet { shopMoney { amount } } } } } }"
  }' \
  | jq -r '
      .data.orders.edges[].node |
      [
        (.createdAt | sub("T.*"; "") | strptime("%Y-%m-%d") | mktime |
          . - ((. / 86400 % 7) * 86400) | strftime("%Y-%m-%d")),
        "Online Store",
        (.totalPriceSet.shopMoney.amount | tonumber)
      ] | @csv
    ' \
  | awk -F, '{gsub(/"/, "", $1); gsub(/"/, "", $2); sum[$1","$2]+=$3} END{for(k in sum) print k","sum[k]}' \
  | sort \
  > data/shopify_weekly.csv

sed -i '' '1i\
week_start,entity,revenue
' data/shopify_weekly.csv
```

For multi-store Shopify setups, change the `entity` label per shop and concatenate.

## Adapter 5 — QuickBooks Online

QBO's Profit & Loss report is the easiest source of weekly revenue. Use the QBO API's `reports/ProfitAndLoss` endpoint with `summarize_column_by=Week`.

```bash
export QBO_TOKEN=$(gcloud secrets versions access latest --secret=qbo-access-token)
export QBO_REALM=$(gcloud secrets versions access latest --secret=qbo-realm-id)

curl -sS -H "Authorization: Bearer $QBO_TOKEN" \
  -H "Accept: application/json" \
  "https://quickbooks.api.intuit.com/v3/company/$QBO_REALM/reports/ProfitAndLoss?start_date=2025-04-01&end_date=2026-04-01&summarize_column_by=Week" \
  > data/qbo_pnl.json

# Parse the response — QBO's report format is nested and ugly.
# You'll want a small Python script to walk the ColData tree and emit CSV.
```

QBO's report endpoint is the right call for aggregated weekly revenue, but the response format is deeply nested. A small helper script is easier to maintain than a jq one-liner.

## Adapter 6 — Plain CSV From a Spreadsheet

If all you have is a manually-maintained spreadsheet in Excel or Google Sheets, just export it as CSV directly. The important thing is that the columns match the expected format — rename them if the original sheet uses different labels.

```bash
# Assumes you have a file downloaded from Excel or Google Sheets
# Rename columns to match the expected format
awk -F, 'BEGIN {OFS=","}
  NR==1 {print "week_start,entity,revenue"; next}
  {print $1, $2, $3}
' ~/Downloads/weekly_sales.csv > data/history.csv
```

## Adapter 7 — Writing Your Own

If your data source isn't covered above, the fastest path is usually:

1. Get the raw data in whatever format the source provides (JSON, XML, Excel, SQL result set).
2. Write a 20-line Python or shell script that walks the rows and emits the 3-column CSV.
3. Run the forecaster against the CSV.

Keep the adapter script in `data/adapters/` alongside the CSV it produces. Commit both. If the data changes upstream, you regenerate the CSV; the forecaster doesn't need to know.

**Minimal Python adapter skeleton:**

```python
#!/usr/bin/env python3
"""Adapter: your-source → history.csv"""
import csv, sys
from datetime import date, timedelta

def monday_of(d):
    return d - timedelta(days=d.weekday())

def fetch_rows():
    # ...query your source here, yielding (datetime, entity, revenue) tuples
    yield date(2025, 10, 8), "Main Street", 48350.00
    yield date(2025, 10, 11), "Downtown", 32110.00

by_week = {}
for d, entity, rev in fetch_rows():
    key = (monday_of(d).isoformat(), entity)
    by_week[key] = by_week.get(key, 0) + rev

w = csv.writer(sys.stdout)
w.writerow(["week_start", "entity", "revenue"])
for (week, entity), rev in sorted(by_week.items()):
    w.writerow([week, entity, f"{rev:.2f}"])
```

Run with `python3 adapter.py > data/history.csv` and you're ready to forecast.

## Data Quality Checklist

Before you spend time tuning parameters, make sure your data is clean:

- [ ] **No duplicate `(week_start, entity)` rows.** The forecaster assumes one row per entity per week.
- [ ] **Week boundaries consistent.** All `week_start` values are Mondays.
- [ ] **Complete weeks only.** Don't include the current partial week in the history — the forecaster handles that separately.
- [ ] **Zero-revenue weeks are labeled, not missing.** If a location was closed for a week, include it as a `0` row. The forecaster can filter these out via `data_filters.min_weekly_revenue`, but it can't re-create them if they're missing.
- [ ] **Entity names stable over time.** "Main Street" and "main street" and "Main St." are three different entities to the model.
- [ ] **Numbers are numbers.** No `$1,234.56` — use `1234.56`.

A 10-minute data-quality pass is usually worth more than an hour of parameter tuning.

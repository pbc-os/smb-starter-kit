---
name: semantic-layer-audit
description: Audit and maintain a data semantic layer for AI agents. Scans BigQuery datasets, GCP APIs, secrets, and service accounts to keep your data catalog current. Essential for any agent that needs to know "what data do I have access to?"
---

# Semantic Layer Audit

> **Why this matters:** AI agents can only use data they know about. This skill maintains a living data catalog so you never lose track of available datasets, APIs, or credentials.

## Prerequisites

- **GCP Project** with BigQuery enabled
- **gcloud CLI** authenticated (`gcloud auth login`)
- **bq CLI** (comes with gcloud)
- **Environment variable:** `GCP_PROJECT_ID` set to your project

```bash
# Set your project
export GCP_PROJECT_ID="your-project-id"

# Verify access
gcloud config set project $GCP_PROJECT_ID
bq ls --project_id=$GCP_PROJECT_ID
```

## Quick Start

```bash
# Run full infrastructure audit
python3 scripts/audit_infrastructure.py > audit-results.json

# Review and update your semantic layer doc
# (see templates/SEMANTIC-LAYER-TEMPLATE.md)
```

## When to Run

| Trigger | Action |
|---------|--------|
| "What data do we have?" | Full audit |
| "Audit data sources" | Full audit |
| After creating views | Document with full schema + usage guidance |
| After new integrations | Infrastructure scan |
| Weekly maintenance | Cron: catch schema changes |
| Before complex analysis | Verify sources exist |

---

## Documentation Standards

### The Problem

Most data catalogs are just lists of table names. This leads to:
- Agents querying wrong tables
- Missing context about when to use what
- No guidance on data source transitions
- Confusion when numbers don't match between sources

### The Solution: Documentation Levels

#### Level 1: Table Documentation (Minimum)

Every table needs these fields:

| Field | Required | Example |
|-------|----------|---------|
| Name | ✅ | `orders` |
| Description | ✅ | "All completed orders" |
| Key Fields | ✅ | `order_id`, `created_at`, `total` |
| Granularity | ✅ | Per-order |
| Source | ✅ | "Synced from Shopify API" |

#### Level 2: View Documentation (Full Detail)

Views require MORE documentation because users need to know when to use them vs raw tables:

```markdown
#### `daily_sales_summary` (VIEW)

**Purpose:** Pre-aggregated daily sales metrics. Faster than aggregating raw orders.

**When to use:**
- Daily/weekly/monthly revenue trends
- High-level reporting dashboards
- Quick "how did yesterday go?" questions

**When NOT to use:**
- Need individual order details → use `orders`
- Need customer-level data → use `orders` joined with `customers`

| Column | Type | Description |
|--------|------|-------------|
| `date` | DATE | Sales date |
| `total_revenue` | FLOAT64 | Sum of order totals (dollars) |
| `order_count` | INT64 | Number of orders |
| `avg_order_value` | FLOAT64 | Revenue / orders |

**Example:**
\`\`\`sql
-- Last 30 days revenue trend
SELECT date, total_revenue, order_count
FROM `project.dataset.daily_sales_summary`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY date
\`\`\`
```

#### Level 3: Decision Tables

When multiple tables/views could answer similar questions, add a decision table:

```markdown
### Choosing the Right Sales Data Source

| Question | Use This | Why |
|----------|----------|-----|
| "Total revenue last month?" | `daily_sales_summary` | Pre-aggregated, fast |
| "Revenue by product category?" | `order_items` | Has product details |
| "Specific customer's orders?" | `orders` | Has customer_id |
| "Hour-by-hour sales today?" | `orders` + aggregate | Summary is daily only |
```

#### Level 4: Source System Transitions

Document when underlying systems changed (critical for historical analysis):

```markdown
### 🚨 SYSTEM TRANSITION

| Entity | Old System | New System | Cutover Date |
|--------|------------|------------|--------------|
| Orders | Legacy POS | Shopify | Jan 2024 |

**Implications:**
- YoY comparisons spanning the cutover need both systems
- Pre-Jan-2024 data in `legacy_orders`, post in `orders`
- Some fields don't exist in legacy (e.g., `discount_code`)
```

#### Level 5: Data Reconciliation Notes

When different sources show different numbers, explain WHY:

```markdown
### 💡 Why Shopify Revenue ≠ Accounting Revenue

**Observation:** Shopify shows $100k, QuickBooks shows $94k for same month.

**Explanation:** 
- Shopify = Gross merchandise value (what customers paid)
- QuickBooks = Net revenue (after refunds, chargebacks, payment fees)

**Neither is wrong.** Use Shopify for customer-facing metrics, QuickBooks for P&L.
```

---

## Audit Process

### 1. Infrastructure Scan

```bash
python3 scripts/audit_infrastructure.py
```

The script scans:
- **BigQuery:** All datasets, tables, views, and row counts
- **Secrets:** All Secret Manager secrets (credential inventory)
- **APIs:** All enabled Google Cloud APIs
- **Service Accounts:** All service accounts in the project

Output is JSON for easy processing.

### 2. Memory Pattern Discovery

Search your agent's memory for data access patterns not yet documented:

```bash
# Find BigQuery queries in recent sessions
memory_search "BigQuery query SELECT FROM"

# Find new views or tables created
memory_search "CREATE VIEW CREATE TABLE"

# Find API usage patterns  
memory_search "API endpoint curl"
```

Look for:
- Tables queried but not in your semantic layer doc
- Views created that need documentation
- API endpoints used successfully
- Join patterns between datasets
- Explanations of data discrepancies you've figured out

### 3. Gap Analysis

Compare audit results against your `SEMANTIC-LAYER.md`:

**Completeness:**
- [ ] New BigQuery tables/views documented
- [ ] New secrets/credentials listed
- [ ] New APIs documented

**Quality (the important part):**
- [ ] Views have full schema + "When to use" guidance
- [ ] Decision tables exist for related data sources
- [ ] Source transitions documented
- [ ] Data reconciliation notes where numbers differ
- [ ] Deprecated items marked with replacement pointers

### 4. Update Semantic Layer

Update your data catalog with:
- New tables (Level 1 minimum)
- New views (Level 2 - full detail)
- Decision tables (Level 3)
- System transitions (Level 4)
- Reconciliation notes (Level 5)
- Updated Quick Reference routing table
- Deprecated items marked with ⚠️

### 5. Track Discoveries

Log ad-hoc discoveries for future audits:

```markdown
## Discovery Log

| Date | Discovery | Source | Added |
|------|-----------|--------|-------|
| 2024-01-15 | Tips not in revenue | Debug session | ✅ |
| 2024-01-18 | New product_prices view | Created for analysis | ✅ |
```

---

## Quick Reference Table Standards

Maintain a routing table at the TOP of your semantic layer doc:

```markdown
| Data Need | Source | Notes |
|-----------|--------|-------|
| **Daily Sales** | `daily_sales_summary` | Preferred - pre-aggregated |
| **Order Details** | `orders` | Full order records |
| **Product Prices** | `product_prices` (VIEW) | Use this! |
| **Legacy Orders** | `legacy_orders` | Pre-2024 only |
```

Use "Preferred" or "Use this!" to guide agents to the right source.

---

## Deprecation Standards

When a table/view is superseded:

**In the table listing:**
```markdown
| `old_table` | ⚠️ **Use `new_view` instead** - Legacy | ... |
```

**Add a deprecation section:**
```markdown
## ⚠️ Deprecated Sources

| Old Source | Use Instead | Reason |
|------------|-------------|--------|
| `order_line_items` | `product_sales` view | Better schema, faster |
| `sales_raw` | `orders` | Renamed, same data |
```

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GCP_PROJECT_ID` | Yes | Your GCP project ID |
| `SEMANTIC_LAYER_PATH` | No | Path to your doc (default: `docs/SEMANTIC-LAYER.md`) |

### Customizing the Script

Edit `scripts/audit_infrastructure.py` to:
- Skip certain datasets (add to `SKIP_DATASETS`)
- Add custom API checks
- Adjust row count timeout

---

## Files

| File | Purpose |
|------|---------|
| `scripts/audit_infrastructure.py` | Infrastructure scanner |
| `templates/SEMANTIC-LAYER-TEMPLATE.md` | Starter template |

---

## Cron Schedule (Recommended)

Weekly audit to catch schema changes:

```
0 6 * * 0
```

Text: "Run semantic layer audit - check for new BigQuery tables, views, API changes, and undocumented data patterns"

---

## Post-Audit Checklist

After each audit:
- [ ] All tables documented (Level 1)
- [ ] All views have full documentation (Level 2)
- [ ] Decision tables for related sources (Level 3)
- [ ] System transitions noted (Level 4)
- [ ] Reconciliation notes where needed (Level 5)
- [ ] Quick Reference routing table updated
- [ ] Deprecated items marked with replacements
- [ ] Changes committed to git
- [ ] User notified of significant changes

---

## Example Output

```json
{
  "project_id": "your-project",
  "audit_time": "2024-01-15T10:30:00",
  "bigquery": {
    "datasets": [
      {
        "dataset_id": "sales_data",
        "tables": [
          {"table_id": "orders", "type": "TABLE", "row_count": 50000},
          {"table_id": "daily_summary", "type": "VIEW"}
        ]
      }
    ]
  },
  "secrets": ["api-key-service-a", "oauth-token-service-b"],
  "apis": ["bigquery.googleapis.com", "secretmanager.googleapis.com"]
}
```

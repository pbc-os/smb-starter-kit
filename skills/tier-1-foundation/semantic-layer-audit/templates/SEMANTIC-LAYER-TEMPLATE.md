# Semantic Layer - Data Catalog

> Your AI agent's single source of truth for available data.

**Last Updated:** YYYY-MM-DD  
**GCP Project:** `your-project-id`

---

## 🗺️ Quick Reference: Where Does This Data Live?

| Data Need | Source | Access | Notes |
|-----------|--------|--------|-------|
| **Daily Sales** | `sales.daily_summary` | BigQuery | Preferred - pre-aggregated |
| **Order Details** | `sales.orders` | BigQuery | Individual transactions |
| **Product Sales** | `sales.product_sales` (VIEW) | BigQuery | **Use this!** |
| **Customer Info** | `customers.profiles` | BigQuery | |
| **Real-time Orders** | Orders API | REST API | For live data |
| **Credentials** | Secret Manager | gcloud | |

---

## 📍 Location/Entity Reference (if applicable)

| ID | Name | Aliases |
|----|------|---------|
| `LOC001` | Main Store | Downtown, Store 1 |
| `LOC002` | Mall Store | Mall, Store 2 |

⚠️ **Always verify entity IDs before running queries.**

---

## 🚨 System Transitions (if applicable)

| Entity | Old System | New System | Cutover Date |
|--------|------------|------------|--------------|
| Orders | Legacy POS | Shopify | Jan 2024 |

**Implications:**
- Pre-Jan-2024 data in `legacy_orders`, post in `orders`
- YoY comparisons spanning cutover need both tables
- Some fields don't exist in legacy

---

## 🗄️ BigQuery: `your_dataset`

**Project:** `your-project-id`  
**Dataset:** `sales` (primary business data)

### Core Tables

| Table | Description | Key Fields | Granularity |
|-------|-------------|------------|-------------|
| `orders` | All completed orders | `order_id`, `customer_id`, `total`, `created_at` | Per order |
| `order_items` | Line items within orders | `order_id`, `product_id`, `quantity`, `price` | Per item |
| `daily_summary` | Pre-aggregated daily metrics | `date`, `revenue`, `order_count` | Daily |
| `customers` | Customer profiles | `customer_id`, `email`, `created_at` | Per customer |
| `legacy_orders` | ⚠️ **Pre-2024 only** - Old POS data | `order_id`, `total` | Per order |

---

### 📦 Views (Analyst-Friendly)

Views transform raw data into analyst-friendly formats. **Use views instead of complex joins when available.**

#### `product_sales` (VIEW)

**Purpose:** Flat product sales data. One row per line item per order.

**When to use:**
- Individual transaction analysis
- Finding specific orders for a product
- Revenue by product queries

**When NOT to use:**
- Need order-level totals only → use `orders`
- Need pre-aggregated daily data → use `product_sales_daily`

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | STRING | Order identifier |
| `order_date` | DATE | Date of order |
| `product_name` | STRING | Product name |
| `category` | STRING | Product category |
| `quantity` | INT64 | Units sold |
| `unit_price` | FLOAT64 | Price per unit (dollars) |
| `line_total` | FLOAT64 | Total for line (dollars) |

**Example:**
```sql
-- Find all Widget sales in January
SELECT order_date, product_name, quantity, line_total
FROM `project.sales.product_sales`
WHERE product_name LIKE '%Widget%'
  AND order_date BETWEEN '2024-01-01' AND '2024-01-31'
ORDER BY order_date
```

#### `product_price_history` (VIEW)

**Purpose:** Track how product prices change over time using actual transaction data.

**When to use:**
- Price change analysis
- Margin calculations with real selling prices
- Historical price lookups

| Column | Type | Description |
|--------|------|-------------|
| `date` | DATE | Transaction date |
| `product_name` | STRING | Product name |
| `avg_price` | FLOAT64 | Average price that day |
| `min_price` | FLOAT64 | Lowest price seen |
| `max_price` | FLOAT64 | Highest price seen |
| `transactions` | INT64 | Number of sales |

**Example:**
```sql
-- Track Widget price changes over 2024
SELECT date, avg_price, transactions
FROM `project.sales.product_price_history`
WHERE product_name = 'Widget Pro'
  AND date >= '2024-01-01'
ORDER BY date
```

---

### Choosing the Right Source

| Question | Use This | Why |
|----------|----------|-----|
| "Total revenue last month?" | `daily_summary` | Pre-aggregated, fast |
| "Revenue by product?" | `product_sales` → aggregate | Has product detail |
| "Every order for Widget?" | `product_sales` | Line item detail |
| "How has Widget price changed?" | `product_price_history` | Price tracking |
| "Customer's order history?" | `orders` | Has customer_id |

---

## 💡 Data Reconciliation Notes

### Why Source A ≠ Source B

*(Document when different sources show different numbers)*

**Example: POS Total ≠ Accounting Revenue**

| Source | Shows | Includes |
|--------|-------|----------|
| POS System | $100,000 | Gross sales (what customers paid) |
| Accounting | $94,000 | Net revenue (after refunds, fees) |

**Both are correct.** POS for customer metrics, Accounting for P&L.

---

## 🔌 API Integrations

### Orders API

- **Docs:** https://docs.example.com/api/orders
- **Auth:** API key in Secret Manager (`orders-api-key`)
- **Base URL:** `https://api.example.com/v1`
- **Rate Limits:** 100 req/min

| Endpoint | Method | Use Case |
|----------|--------|----------|
| `/orders` | GET | List orders (paginated) |
| `/orders/{id}` | GET | Single order detail |
| `/orders/search` | POST | Search by criteria |

---

## 🔐 Credentials Inventory

All credentials in GCP Secret Manager.

| Secret Name | Service | Notes |
|-------------|---------|-------|
| `orders-api-key` | Orders API | Production |
| `analytics-sa-key` | BigQuery | Service account JSON |
| `webhook-secret` | Webhooks | HMAC validation |

**Access:**
```bash
gcloud secrets versions access latest --secret="secret-name" --project=your-project
```

---

## ⚠️ Deprecated Sources

| Old Source | Use Instead | Reason |
|------------|-------------|--------|
| `raw_order_items` | `product_sales` view | Better schema, includes names |
| `sales_v1` | `orders` | Renamed |

---

## 📊 Data Freshness

| Source | Update Frequency | Typical Lag |
|--------|------------------|-------------|
| `orders` | Real-time | < 1 min |
| `daily_summary` | Daily 2am UTC | ~24 hrs |
| `product_price_history` | Daily | ~24 hrs |

---

## 🚫 Known Limitations

- **Historical data:** Orders before 2023 may be incomplete
- **Timezone:** All timestamps in UTC unless noted
- **PII:** Customer emails available but use carefully

---

## 📝 Discovery Log

Track new data patterns found during ad-hoc work.

| Date | Discovery | Source | Added |
|------|-----------|--------|-------|
| 2024-01-15 | Tips not included in revenue totals | Debug session | ✅ |
| 2024-01-18 | Created product_price_history view | Analysis need | ✅ |

---

## 🔄 Maintenance Schedule

- **Weekly:** Run `audit_infrastructure.py` to catch schema changes
- **Monthly:** Review deprecated items, prune if unused
- **Quarterly:** Deep audit of all integrations, verify credentials

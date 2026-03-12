# SMB Spreadsheet Templates

Common spreadsheet structures for small businesses. Use these as starting points when creating new tracking sheets.

## Daily Sales Tracker

### Columns
| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Date | Location | Revenue | Transactions | Avg Ticket | Day of Week | Notes |

### Example data
```
2025-01-13 | Store 1 | $2,150 | 73 | $29.45 | Monday | Holiday weekend recovery
2025-01-14 | Store 1 | $2,890 | 95 | $30.42 | Tuesday | Normal
2025-01-14 | Store 2 | $1,940 | 68 | $28.53 | Tuesday | Short staffed
```

### Useful formulas (put in a Summary tab)
- **MTD Revenue:** `=SUMIFS(C:C, A:A, ">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))`
- **Avg Daily Revenue:** `=AVERAGEIF(A:A, ">="&TODAY()-30, C:C)`
- **Best Day:** `=INDEX(A:A, MATCH(MAX(C:C), C:C, 0))`

---

## Inventory Tracker

### Columns
| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| SKU | Product Name | Category | Current Stock | Reorder Point | Unit Cost | Supplier |

### Conditional formatting rules
- **Red:** Current Stock < Reorder Point (needs reorder)
- **Yellow:** Current Stock < Reorder Point * 1.5 (getting low)
- **Green:** Current Stock >= Reorder Point * 2 (well stocked)

---

## Expense Tracker

### Columns
| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Date | Category | Vendor/Description | Amount | Payment Method | Receipt Link |

### Categories for SMBs
- COGS (Cost of Goods Sold)
- Rent / Lease
- Utilities
- Payroll
- Insurance
- Marketing / Advertising
- Supplies
- Equipment
- Professional Services
- Miscellaneous

### Summary formulas
- **Monthly total by category:** `=SUMIFS(D:D, B:B, "Marketing", A:A, ">="&DATE(2025,1,1), A:A, "<"&DATE(2025,2,1))`

---

## Vendor Contact List

### Columns
| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Vendor | Contact Name | Email | Phone | Products | Payment Terms | Account # | Notes |

---

## Customer Order Log

### Columns
| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Order Date | Customer | Items | Total | Status | Pickup/Delivery | Fulfillment Date | Notes |

### Status values
- Received
- In Progress
- Ready
- Completed
- Cancelled

---

## Simple P&L (Profit & Loss)

### Structure
```
Row 1:  | Month | Jan | Feb | Mar | ... | YTD |
Row 2:  REVENUE
Row 3:  | Sales        | $X | $X | $X |
Row 4:  | Other Income | $X | $X | $X |
Row 5:  | Total Revenue| $X | $X | $X |
Row 6:
Row 7:  COST OF GOODS SOLD
Row 8:  | Materials    | $X | $X | $X |
Row 9:  | Labor        | $X | $X | $X |
Row 10: | Total COGS   | $X | $X | $X |
Row 11:
Row 12: GROSS PROFIT   | $X | $X | $X |
Row 13: Gross Margin   | X% | X% | X% |
Row 14:
Row 15: OPERATING EXPENSES
Row 16: | Rent         | $X | $X | $X |
Row 17: | Utilities    | $X | $X | $X |
Row 18: | Marketing    | $X | $X | $X |
Row 19: | Insurance    | $X | $X | $X |
Row 20: | Other        | $X | $X | $X |
Row 21: | Total OpEx   | $X | $X | $X |
Row 22:
Row 23: NET PROFIT     | $X | $X | $X |
Row 24: Net Margin     | X% | X% | X% |
```

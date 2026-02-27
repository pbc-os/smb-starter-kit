# Google Ads Browser Automation Workflows

When API access isn't available, browser automation works well for Google Ads management. This guide covers the key workflows.

## Why Browser Mode?

**Use browser automation when:**
- API credentials aren't set up
- Quick one-off checks
- Client accounts you can't get API access to
- Teaching/demonstrating to someone

**Limitations:**
- Slower than API
- Requires user to be logged in
- Can't schedule/automate reliably
- UI changes can break workflows

---

## Prerequisites

1. User logged into ads.google.com
2. Browser automation tool connected (Playwright, Puppeteer, or similar)
3. Correct account selected (check top-right account switcher)

---

## URL Structure

All Google Ads URLs follow this pattern:

```
https://ads.google.com/aw/{section}?ocid={account_id}
```

### Main Sections

| Section | URL | Description |
|---------|-----|-------------|
| Overview | /aw/overview | Account dashboard |
| Campaigns | /aw/campaigns | All campaigns |
| Ad Groups | /aw/adgroups | All ad groups |
| Keywords | /aw/keywords | Search keywords |
| Ads | /aw/ads | All ads |
| Search Terms | /aw/searchterms | Matched search queries |
| Conversions | /aw/conversions | Conversion tracking |
| Settings | /aw/settings | Account settings |

---

## Core Workflows

### 1. Check Campaign Performance

**Goal:** See cost, conversions, and status for all campaigns

**Steps:**
```
1. Navigate: ads.google.com/aw/campaigns
2. Wait for table to load (look for campaign rows)
3. Set date range:
   - Click date picker (top right)
   - Select: Last 7 days / Last 30 days / Custom
   - Click Apply
4. Read table columns:
   - Campaign name
   - Status (Enabled/Paused/Removed)
   - Budget
   - Cost
   - Conversions
   - Cost/conv
```

**What to look for:**
- High cost + low/no conversions = problem
- Paused campaigns with budget = review if intentional
- Status warnings (yellow icons)

---

### 2. Find Zero-Conversion Keywords

**Goal:** Identify keywords eating budget without results

**Steps:**
```
1. Navigate: ads.google.com/aw/keywords
2. Add filter:
   - Click "Add filter" button
   - Select "Conversions"
   - Choose "Less than"
   - Enter "1"
   - Apply
3. Add second filter:
   - Click "Add filter" again
   - Select "Cost"
   - Choose "Greater than"
   - Enter your threshold (e.g., 500 for $500)
   - Apply
4. Sort by Cost (descending):
   - Click "Cost" column header
   - Click again if needed to sort high→low
5. Review results:
   - Keywords with high spend, zero conversions = candidates for pause
```

**Filter URL shortcut:**
```
ads.google.com/aw/keywords?filter=metrics.conversions<1,metrics.cost_micros>500000000
```

---

### 3. Review Search Terms

**Goal:** See what people actually searched for

**Steps:**
```
1. Navigate: ads.google.com/aw/searchterms
2. Set date range (last 30 days recommended)
3. Sort by Cost descending
4. Look for:
   - Irrelevant terms (add as negative keywords)
   - Good terms without exact match (add as keywords)
   - Competitor names (usually add as negatives)
```

**Action patterns:**
- Irrelevant term → Add to negative keyword list
- Relevant term converting well → Add as exact match keyword
- Relevant term not converting → Monitor or add as negative

---

### 4. Pause Campaigns/Keywords

**Goal:** Stop spend on underperformers

**Steps:**
```
1. Navigate to campaigns or keywords view
2. Check the boxes next to items to pause
   - Checkbox is in the first column
3. Click "Edit" button (appears in toolbar)
4. Select "Pause" from dropdown
5. Confirm if prompted
```

**Bulk pause:**
- Use filters to show only items you want to pause
- Click checkbox in header row to select all visible
- Edit → Pause

---

### 5. Change Budgets

**Goal:** Increase/decrease campaign spend

**Single campaign:**
```
1. Navigate: ads.google.com/aw/campaigns
2. Find the campaign
3. Click on the budget number (it's editable)
4. Type new value
5. Press Enter or click away to save
```

**Multiple campaigns:**
```
1. Select campaign checkboxes
2. Click "Edit" → "Change budgets"
3. Choose: Set to / Increase by % / Decrease by %
4. Enter value
5. Apply
```

---

### 6. Check Conversion Tracking

**Goal:** Verify conversions are recording

**Steps:**
```
1. Navigate: ads.google.com/aw/conversions (or Goals → Conversions)
2. Check status column:
   - "Recording conversions" = ✅ Working
   - "No recent conversions" = ⚠️ May need review
   - "Inactive" = ❌ Broken, needs fixing
3. Click any conversion action to see:
   - Last conversion date
   - Conversion count
   - Attribution settings
```

---

## UI Element Selectors

For browser automation scripts, these selectors help locate elements:

### Tables
```css
/* Main data table */
[role="grid"]
table.ess-table

/* Table rows */
[role="row"]
tbody tr

/* Cells */
[role="gridcell"]
td

/* Headers (clickable for sorting) */
[role="columnheader"]
th
```

### Buttons
```css
/* Primary action buttons */
button[data-color="primary"]

/* Dropdown triggers */
[aria-haspopup="listbox"]
[aria-haspopup="menu"]
```

### Filters
```css
/* Filter toolbar */
[role="toolbar"]

/* Add filter button */
/* Usually contains text "Add filter" */

/* Active filter chips */
[role="listitem"]
```

### Dialogs
```css
/* Modal dialogs */
[role="dialog"]

/* Close button */
[aria-label="Close"]
```

---

## Tips for Reliable Automation

### 1. Wait for Table Data
Tables load asynchronously. Wait for rows to appear:
```javascript
// Wait for at least one data row
await page.waitForSelector('tbody tr', { timeout: 10000 });
```

### 2. Handle Pagination
Large accounts may paginate. Look for:
- "Show more" button at bottom
- Page numbers
- "1-100 of 500" indicator

### 3. Always Verify Date Range
The date range persists across sessions but may not be what you expect. Always set it explicitly before reading data.

### 4. Check Account Context
Top-right shows the current account. Verify you're in the right one before making changes.

### 5. Wait for Saves
After editing (budgets, pausing, etc.), wait for the save confirmation before moving on. Look for:
- Checkmark/success indicators
- Spinner disappearing
- Value updating in the UI

---

## Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Empty table | Wrong account | Check account selector |
| "No data" | Date range issue | Expand date range |
| Can't click elements | UI still loading | Add longer waits |
| Filters not applying | Wrong filter logic | Clear all, start fresh |
| Actions grayed out | No items selected | Select items first |

---

## When to Switch to API

Browser automation works, but consider API if you're:
- Running these checks daily
- Managing multiple accounts
- Building automated workflows
- Doing bulk operations (100+ items)

See `api-setup.md` for the API path.

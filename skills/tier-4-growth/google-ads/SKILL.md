---
name: google-ads
description: "Create, query, audit, and optimize Google Ads campaigns. Supports both API mode (google-ads Python SDK) and browser automation. Use for campaign management, performance analysis, keyword optimization, and ad creation."
---

# Google Ads Management Skill

Comprehensive skill for managing Google Ads accounts via API or browser automation.

## Why This Skill Exists

**The Problem:**  
Google Ads management requires precise, methodical work. Missed settings cause wasted spend. Forgotten fields cause API rejections. Small mistakes compound into big losses.

**The Solution:**  
This skill provides battle-tested checklists, query templates, and workflows for common Google Ads operations. It captures lessons learned from real production use — the gotchas that aren't in the official docs.

**What it prevents:**
- Campaign creation with broken landing pages ($$ wasted on 404s)
- RSA text rejections (character limits are strict)
- Missing required fields that cause API errors
- Pausing the wrong campaigns
- Forgetting to set end dates on promotional campaigns

---

## When to Use This Skill

| Task | Use This Skill |
|------|---------------|
| Check campaign performance | ✅ Yes |
| Create new campaigns/ads | ✅ Yes |
| Find wasted spend | ✅ Yes |
| Pause underperforming keywords | ✅ Yes |
| Adjust budgets | ✅ Yes |
| Audit account health | ✅ Yes |
| Billing/payment issues | ❌ No (use Google support) |

---

## Mode Selection

This skill supports two modes. Choose based on what's available:

### API Mode (Power Users)
**Best for:** Automation, programmatic changes, bulk operations  
**Requires:** Developer token, OAuth credentials, `google-ads` Python SDK

```bash
# Check if API mode is available
ls ~/.google-ads.yaml 2>/dev/null && echo "API config found" || echo "No API config"
python -c "from google.ads.googleads.client import GoogleAdsClient; print('SDK installed')" 2>/dev/null
```

### Browser Mode (Universal)
**Best for:** Quick checks, one-off changes, no API setup needed  
**Requires:** User logged into ads.google.com in browser

If no API config exists, ask: *"I don't see Google Ads API credentials. Should I use browser automation instead?"*

---

## Campaign Creation Checklist

**⚠️ COMPLETE THIS BEFORE CREATING ANY CAMPAIGN**

This checklist exists because every item has caused real-world failures:

### 1. Pre-Flight Verification

```bash
# ALWAYS verify landing page is live
curl -sI "https://your-landing-page.com/path" | head -2
# Must return: HTTP/2 200 or HTTP/1.1 200 OK

# Why? We've seen campaigns launch with 404 landing pages. 
# All ad spend went to a broken page. Verify FIRST.
```

### 2. Plan Structure Before Code

Before writing any campaign creation code, document:

| Element | Your Plan | Character Limit |
|---------|-----------|-----------------|
| Campaign name | | — |
| Campaign type | Search / PMax / Display / etc. | — |
| Daily budget | | — |
| Ad group names | | — |
| Keywords per group | | — |
| Headlines (3-15) | | ≤30 chars each |
| Descriptions (2-4) | | ≤90 chars each |
| Final URL | | Must return 200 |
| Location targeting | | — |
| End date? | | (if promotional) |

**Why plan first?** Iterating campaign structure via API is slow and error-prone. Get it right on paper first.

### 3. Required API Fields (Easy to Forget)

```python
# EU Political Advertising field (REQUIRED even for non-political ads)
campaign.contains_eu_political_advertising = (
    client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
)
# Why? Without this, the API rejects the campaign with a confusing error.

# RSA character limits (STRICT)
# Headlines: exactly ≤30 characters (not "about 30")
# Descriptions: exactly ≤90 characters (not "about 90")
# Why? The API rejects over-length text, doesn't truncate it.
```

### 4. Post-Creation Verification

- [ ] Campaign status shows ENABLED (not PAUSED or ERROR)
- [ ] Ads show "Eligible" or "Under review" (not "Disapproved")
- [ ] Conversion tracking is connected
- [ ] Location targeting is correct
- [ ] Budget is what you intended
- [ ] End date set (if time-limited)

---

## Account Audit Checklist

Quick health check for any Google Ads account:

| Check | Where to Look | Red Flags |
|-------|---------------|-----------|
| Zero-conversion keywords | Keywords → Filter: Conv<1, Cost>$X | High spend, no results |
| Empty ad groups | Ad Groups → Filter: Ads=0 | Budget allocated, no creative |
| Policy violations | Campaigns → Status column | Yellow warning icons |
| Optimization Score | Overview page (top right) | Below 70% |
| Conversion tracking | Tools → Conversions | "Inactive" or no recent data |
| Wasted spend | Search Terms report | Irrelevant queries |
| Landing page status | Ads → Final URL column | Any 404s or redirects |

---

## Common Queries (API Mode)

### Campaign Performance (Last 30 Days)

```python
query = """
    SELECT 
        campaign.id,
        campaign.name,
        campaign.status,
        campaign_budget.amount_micros,
        metrics.cost_micros,
        metrics.conversions,
        metrics.cost_per_conversion
    FROM campaign
    WHERE segments.date DURING LAST_30_DAYS
      AND campaign.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
    LIMIT 50
"""

# Parse results
for row in response:
    cost = row.metrics.cost_micros / 1_000_000
    conv = row.metrics.conversions
    cpa = row.metrics.cost_per_conversion / 1_000_000 if conv > 0 else 0
    print(f"{row.campaign.name}: ${cost:.2f} | {conv:.1f} conv | ${cpa:.2f} CPA")
```

### Find Wasted Spend (Zero-Conversion Keywords)

```python
query = """
    SELECT 
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        campaign.name,
        metrics.cost_micros,
        metrics.clicks,
        metrics.impressions
    FROM keyword_view
    WHERE metrics.conversions = 0
      AND metrics.cost_micros > 500000000  /* $500 in micros */
      AND segments.date DURING LAST_90_DAYS
      AND ad_group_criterion.status = 'ENABLED'
    ORDER BY metrics.cost_micros DESC
    LIMIT 100
"""

# Why 90 days? Short windows miss slow converters.
# Why $500 threshold? Adjust based on your CPA expectations.
```

### Search Terms Report (Find Bad Matches)

```python
query = """
    SELECT 
        search_term_view.search_term,
        campaign.name,
        metrics.cost_micros,
        metrics.conversions,
        metrics.clicks
    FROM search_term_view
    WHERE segments.date DURING LAST_30_DAYS
    ORDER BY metrics.cost_micros DESC
    LIMIT 200
"""

# Look for irrelevant searches eating budget.
# Add them as negative keywords.
```

---

## Common Mutations (API Mode)

### Pause Campaigns

```python
from google.ads.googleads.client import GoogleAdsClient

def pause_campaigns(client, customer_id, campaign_ids):
    """Pause one or more campaigns."""
    campaign_service = client.get_service("CampaignService")
    operations = []
    
    for campaign_id in campaign_ids:
        operation = client.get_type("CampaignOperation")
        campaign = operation.update
        campaign.resource_name = campaign_service.campaign_path(
            customer_id, campaign_id
        )
        campaign.status = client.enums.CampaignStatusEnum.PAUSED
        
        # Set field mask
        client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, campaign._pb)
        )
        operations.append(operation)
    
    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=operations
    )
    return response
```

### Pause Keywords

```python
def pause_keywords(client, customer_id, keyword_resource_names):
    """Pause specific keywords by resource name."""
    service = client.get_service("AdGroupCriterionService")
    operations = []
    
    for resource_name in keyword_resource_names:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.update
        criterion.resource_name = resource_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
        
        client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, criterion._pb)
        )
        operations.append(operation)
    
    return service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations
    )
```

---

## Browser Automation (Universal Mode)

When API isn't available, use browser automation at ads.google.com.

### URL Quick Reference

```
Base: https://ads.google.com/aw/
├── overview          # Account dashboard
├── campaigns         # All campaigns
├── adgroups          # All ad groups
├── keywords          # All keywords
├── ads               # All ads
├── searchterms       # Search terms report
└── conversions       # Conversion tracking
```

### Common Workflows

**Check Campaign Performance:**
1. Navigate to ads.google.com/aw/campaigns
2. Set date range (top-right picker)
3. Read the table: Campaign, Status, Budget, Cost, Conversions

**Find Zero-Conversion Keywords:**
1. Navigate to ads.google.com/aw/keywords
2. Click "Add filter" → Conversions → Less than → 1
3. Click "Add filter" → Cost → Greater than → [threshold]
4. Sort by Cost descending

**Pause Items:**
1. Check boxes next to items
2. Click "Edit" dropdown → "Pause"

For detailed browser selectors, see `references/browser-workflows.md`

---

## Output Format

When reporting findings, use clear tables:

```markdown
## Campaign Performance (Last 30 Days)
| Campaign | Cost | Conv | CPA | Status |
|----------|------|------|-----|--------|
| Branded  | $5K  | 50   | $100| ✅ Strong |
| Generic  | $10K | 5    | $2K | ⚠️ Review |
| Test     | $2K  | 0    | N/A | ❌ Pause |

## Recommended Actions
1. **PAUSE**: Test campaign ($2K spent, 0 conversions)
2. **REVIEW**: Generic campaign (CPA too high)
3. **INCREASE**: Branded budget (efficient performer)
```

---

## Troubleshooting

### API Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthenticationError` | Bad credentials | Regenerate refresh token |
| `DEVELOPER_TOKEN_NOT_APPROVED` | Using test token in prod | Apply for token approval |
| `CUSTOMER_NOT_FOUND` | Wrong customer ID | Use 10-digit ID, no dashes |
| `proto-plus CopyFrom errors` | Wrong assignment syntax | Use direct assignment, not CopyFrom |
| `INVALID_STRING_LENGTH` | Text too long | Headlines ≤30, descriptions ≤90 |

### Browser Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Can't see data | Wrong account | Check account selector (top right) |
| Slow loading | Heavy UI | Wait for tables to fully render |
| Session expired | Timeout | User re-login to ads.google.com |
| Wrong date range | Default range | Always set date range before reading |

---

## Why This Belongs in Tier 4 (Growth)

This skill directly drives revenue growth:

- **Tier 1** = Foundation (secrets, setup)
- **Tier 2** = Communication (email, Slack)
- **Tier 3** = Business Ops (POS, accounting)
- **Tier 4** = Growth (advertising, marketing, SEO)

Google Ads is one of the primary paid growth channels for SMBs. This skill helps you manage it without the expensive mistakes that eat into margins.

---

## Files Included

```
google-ads/
├── SKILL.md                    # This documentation
└── references/
    ├── api-setup.md            # Full API setup guide
    └── browser-workflows.md    # Browser automation details
```

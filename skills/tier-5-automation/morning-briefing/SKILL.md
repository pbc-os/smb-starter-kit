---
name: morning-briefing
version: 1.1.0
tier: automation
description: "Automated daily digest for small business owners. Combines email triage, calendar agenda, open tasks, and business KPIs into a single morning briefing. Composable — works with whatever data sources are available."
requires:
  bins: ["gws"]
  skills: ["google-workspace"]
---

# Morning Briefing

**Wake up to everything you need to know about your business in one place.**

This is the "killer app" for AI agents — a composable daily digest that pulls from every connected data source and gives you a single, prioritized briefing before your day starts.

## Triggers

- "morning briefing"
- "daily digest"
- "what do I need to know today"
- "brief me"
- "standup"
- First interaction of the day with the agent

## Prerequisites

- `gws` CLI installed and authenticated (see `google-workspace` skill)
- At minimum: Gmail + Calendar scopes (`gws auth login -s gmail,calendar`)
- More data sources = better briefing

## What Gets Included

The briefing is **composable** — it includes whatever data sources are available. Not everything is required.

### Always included (if available):

| Section | Source | What It Shows |
|---------|--------|--------------|
| **Calendar** | `gws calendar +agenda` | Today's meetings, who you're meeting with, prep needed |
| **Email** | `gws gmail +triage` | Unread count, urgent messages, key senders |
| **Tasks** | `gws workflow +standup-report` | Open tasks, overdue items |

### Included if connected:

| Section | Source | What It Shows |
|---------|--------|--------------|
| **Business KPIs** | Google Sheets, BigQuery, or POS system | Yesterday's revenue, vs forecast, trends |
| **Drive Activity** | `gws drive` | Recently shared or modified documents needing attention |
| **Chat** | `gws chat` | Unread messages in key spaces |

### Included if relevant skills are installed:

| Section | Source | What It Shows |
|---------|--------|--------------|
| **Forecast** | Revenue forecaster / autoresearch | Today's forecast, confidence, model changes |
| **Ads Performance** | Google Ads skill | Spend, ROAS, anomalies |
| **Alerts** | Health monitor / anomaly detection | Anything that needs immediate attention |

## The Briefing Flow

### Step 1: Gather data

Run these in parallel (all are read-only):

```bash
# Calendar — today's events
gws calendar +agenda --format json

# Email — unread inbox summary
gws gmail +triage --max 15 --format json

# Tasks — open items
gws workflow +standup-report --format json
```

If additional data sources are available:

```bash
# Weekly digest context
gws workflow +weekly-digest --format json

# Recent Drive activity
gws drive files list --params '{"pageSize": 5, "orderBy": "modifiedTime desc"}' --format json
```

### Step 2: Analyze and prioritize

Process the gathered data into priority buckets:

**Urgent (handle before anything else):**
- Calendar conflicts or meetings starting within 1 hour
- Emails flagged as urgent or from key contacts (boss, biggest customer, critical vendor)
- Overdue tasks
- Anomalous business metrics (revenue down 30%+, ad spend spike, etc.)

**Important (handle today):**
- Meetings that need prep
- Unread emails from known contacts
- Tasks due today
- Business metrics outside normal range

**Informational (know but don't act yet):**
- Email volume and categories
- This week's calendar overview
- Business metric trends
- Recently shared documents

### Step 3: Compose the briefing

Present in this structure:

```markdown
# Morning Briefing — [Day, Month Date, Year]

## Urgent
- [Anything that needs immediate attention]
- [If nothing urgent: "Nothing urgent — clear to focus."]

## Today's Schedule
| Time | Event | Prep Needed |
|------|-------|-------------|
| 9:00 AM | Team standup | None |
| 11:00 AM | Vendor meeting — Acme Corp | Review latest invoice |
| 2:00 PM | Customer call — Smith Co | Pull order history |

## Email (X unread)
- **From [key contact]:** [subject] — [needs response / FYI]
- **From [vendor]:** [subject] — [action needed / informational]
- [X other unread messages in categories: Y vendors, Z promotions]

## Open Tasks (X items)
- [ ] [Task 1] — due [date]
- [ ] [Task 2] — due [date]
- [X overdue items need attention]

## Business Snapshot (if available)
- Yesterday's revenue: $X,XXX (vs forecast: $X,XXX)
- [Trend: up/down X% vs same day last week]
- [Any anomalies or alerts]

## This Week
- [Key meetings or deadlines coming up]
- [X emails to process]
- [Any scheduled reports or deliverables]
```

### Step 4: Deliver

Options for delivery:
- **Direct response** — Display in the current conversation
- **Google Chat** — Post to a dedicated #briefing space
- **Email** — Send as a digest email to yourself
- **Slack** — Post to a channel (if using `slack-directory` skill)

## Setting Up Automated Daily Briefing

### As a cron job

Set up a cron that runs the briefing every morning:

```bash
# Run at 7:30 AM every weekday
# The cron should:
# 1. Gather all data sources
# 2. Compose the briefing
# 3. Post to your preferred channel
```

The agent should use whatever cron mechanism is available (Claude Code cron, system crontab, Cloud Scheduler, etc.).

### Manual invocation

Just say "morning briefing" or "brief me" to get an on-demand briefing at any time.

## Configuration Template

A starter config is provided at `templates/briefing-config.yaml`. Copy it to your agent's workspace and customize:

- Toggle sections on/off based on what data sources you have connected
- Set delivery method (console, Slack, Google Chat, email)
- Configure schedule, key contacts, and alert thresholds
- Start simple (calendar + email) and enable more sections as you connect more tools

The agent reads this config to know what to gather and how to format the output.

## Customization

The briefing should adapt to the business over time:

- **Key contacts:** Learn which senders are highest priority (boss, top customers, critical vendors)
- **Business hours:** Adjust meeting prep timing based on when you start your day
- **Quiet days:** On slower days (e.g., Sunday for retail), reduce the briefing to essentials
- **Season:** During busy seasons, add more detail on inventory/order status

## Example Briefing

```
# Morning Briefing — Wednesday, January 15, 2026

## Urgent
- Customer complaint from Sarah Miller (email, 11pm last night) — needs response
- Cooler #2 temp alert from overnight monitoring

## Today's Schedule
| Time | Event | Prep Needed |
|------|-------|-------------|
| 9:00 AM | Team standup (30 min) | None |
| 11:00 AM | Vendor call — Fresh Farms (30 min) | Review Q1 pricing sheet in Drive |
| 2:30 PM | Staff 1:1 with Mike (30 min) | Check his task completions |

## Email (23 unread)
- **Sarah Miller:** "Issue with my order" — needs response (urgent)
- **Fresh Farms:** "Updated price list for Q1" — review before 11am call
- **Square:** Daily sales summary — FYI
- 20 others: 8 vendor, 5 newsletter, 7 promotions

## Open Tasks (6 items)
- [ ] Submit quarterly tax docs — due Jan 17 ⚠️
- [ ] Update employee schedule for next week — due Jan 16
- [ ] Order packaging supplies — due Jan 18
- [ ] Follow up with landlord re: lease renewal — overdue ⚠️
- 2 other items due this week

## Business Snapshot
- Yesterday: $2,450 revenue (forecast: $2,200) — +11% vs forecast ✅
- Week-to-date: $4,890 (tracking 8% above weekly target)
- Google Ads: $40 spent, 12 clicks, 2 conversions — ROAS 2.8x

## This Week
- Thursday: Payroll deadline
- Friday: Vendor delivery — Fresh Farms
- 3 more meetings scheduled
```

## Integration with Other Skills

- **`gmail`** — Email triage data
- **`google-calendar`** — Calendar agenda
- **`google-tasks`** — Open task list
- **`google-drive`** — Recently shared documents
- **`google-sheets`** — Business KPI data
- **`autoresearch`** — Report overnight experiment results
- **`google-ads`** — Ad performance snapshot
- **`playbook-discovery`** — Surface new automation opportunities

## Tips

- Start with just email + calendar — add more data sources over time
- The briefing should take 2 minutes to read, not 20
- Focus on what needs ACTION, not just information
- Run it at the same time every day for consistency
- The agent should learn your priorities over time and adjust accordingly

## Related Skills

- `google-workspace` — Required setup (install and auth)
- `gmail` — Email data source
- `google-calendar` — Calendar data source
- `google-tasks` — Task data source
- `autoresearch` — Overnight experiment results

---

*Know your day before it starts. The best operators don't react — they anticipate.*

---
name: morning-briefing
version: 1.3.1
tier: automation
description: "Automated daily digest for small business owners. Combines email triage, calendar agenda, open tasks, and business KPIs into a single morning briefing. Composable — works with whatever data sources are available. Urgent emails require body inspection and explicit escalation signals — never classified from sender/timing metadata alone."
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

## Setup Verification

**Run this before composing the briefing.** If any required check fails, route the user to the [`google-workspace`](../../tier-1-foundation/google-workspace/) skill to complete setup, then come back to this skill. Do not silently proceed with a partial briefing on the first run — the user should know what's missing.

### Required checks (must pass to run the briefing)

1. **`gws` CLI is installed.**
    ```bash
    which gws && gws --version
    ```
    **If not found:** Stop. Route to `google-workspace` skill and ask the user to complete the install step. Do not try to install `gws` from inside this skill.

2. **`gws` is authenticated.**
    ```bash
    gws auth status
    ```
    **If not authenticated:** Stop. Route to `google-workspace` skill — its setup walkthrough handles the OAuth flow.

3. **At minimum, Gmail + Calendar scopes are present.**
    ```bash
    gws auth status | grep -E "(gmail|calendar)"
    ```
    **If either scope is missing:** Run `gws auth login -s gmail,calendar` and re-check. If that still fails, route to `google-workspace`.

### Recommended checks (warn but don't block)

4. **Tasks scope** (for the Open Tasks section):
    ```bash
    gws auth status | grep tasks
    ```
    **If missing:** Note in the briefing that "Tasks scope not authorized — run `gws auth login -s tasks` to enable the Open Tasks section." Continue with the rest of the briefing. Do not block on this.

5. **Drive scope** (for the Recent Activity section):
    ```bash
    gws auth status | grep drive
    ```
    **If missing:** Skip the Recent Activity section silently. It's optional.

### Cache the result

Once verification has passed for a given session, don't re-check on subsequent runs in the same session — it adds latency for no value. The agent should re-run verification only at the start of a fresh session, after a known auth change, or if a `gws` command returns `PERMISSION_DENIED` mid-run.

## Prerequisites

- `gws` CLI installed and authenticated — verified by the Setup Verification step above
- At minimum: Gmail + Calendar scopes
- More data sources = better briefing (Tasks, Drive, Chat, Sheets, etc.)

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
| **Forecast** | `revenue-forecaster` (weekly mode) | This week's point estimate, confidence range, component breakdown |
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

Process the gathered data into priority buckets.

**Urgent (handle before anything else):**
- Calendar conflicts or meetings starting within 1 hour
- Overdue tasks
- Anomalous business metrics (revenue down 30%+, ad spend spike, etc.)
- **Emails — only after the body has been read AND it contains an explicit escalation signal (see below)**

**Important (handle today):**
- Meetings that need prep
- Unread emails from known contacts that don't escalate to "urgent"
- Tasks due today
- Business metrics outside normal range
- Vendor invoices and statements (route to AP)

**Informational (know but don't act yet):**
- Email volume and categories
- This week's calendar overview
- Business metric trends
- Recently shared documents

### Email urgency rules — read the body, don't guess from metadata

**Sender + timing metadata is not enough to classify an email as urgent.** A vendor replying on a thread, a key contact sending a routine status update, or two replies on one thread within an hour are all common patterns that look urgent from the outside but are usually not. The agent must **open the message body** before flagging anything as urgent and look for an actual escalation signal.

#### How to read the body

```bash
# Read a single message body (plain text, no HTML noise)
gws gmail +read --id <MESSAGE_ID>

# Read with headers included
gws gmail +read --id <MESSAGE_ID> --headers

# JSON output for programmatic checking
gws gmail +read --id <MESSAGE_ID> --format json
```

The `gws gmail +read` helper handles HTML→text conversion, base64 decoding, and multipart messages automatically. Use it on any candidate-urgent email before classifying.

#### Required escalation signals

Promote an email to **Urgent** ONLY if its body contains at least one of:

| Signal | What it looks like |
|---|---|
| **Direct address** | The recipient's first name in a salutation or mid-sentence ask: "Hey Corey...", "Corey, can you...", "@corey" |
| **Explicit ask pointed at the recipient** | A direct question or request the recipient is the only one who can answer |
| **Deadline language** | "by EOD", "before tomorrow", "needs to ship today", "by Friday", a date that's < 24 hours away |
| **Problem requiring a decision** | "we're stuck on...", "I need your call on...", "blocked on...", "can you approve..." |
| **Escalation language** | "urgent", "ASAP", "second time asking", "still no response", "this is blocking us" |
| **Money or risk on the line** | Stated dollar amount + a decision needed, account at risk, contract expiring, customer threatening to leave |

If none of those signals are in the body, the email is **Important** (route to AP, log for follow-up, or surface in the Email section) — not Urgent. The same applies to emails from "key contacts": being from the boss or a top customer doesn't automatically make a message urgent. The body decides.

#### The false-urgency failure mode

The most common briefing bug is flagging an email as urgent because of the *pattern* (key sender, recent reply, active thread) rather than the *content*. This produces noisy briefings that the user learns to distrust. Examples of patterns that look urgent but usually aren't:

- A vendor sending a routine status update or "thanks, will look at this" reply
- Two participants on one thread replying within an hour of each other (normal business pace)
- A monthly statement from a vendor that's been monthly for years
- A "FYI" or "no action needed" that uses an urgent-sounding subject line
- An automated system message with the word "Important" in the subject (CC of a boilerplate notice — e.g., utility "you have a new letter" notifications)
- A thread between two other people that doesn't address or @-mention the user — it's their conversation, not the user's
- **A CI / build / deploy failure where the actual deploy step succeeded.** Modern pipelines run non-blocking audit, security-scan, and customer-install jobs alongside the main build. A failure in one of those with `Deploy: succeeded` in the same run means the release went out — this is a code-quality follow-up, not a production incident. Only flag as urgent if the failed job is on the critical path (the build itself, the deploy itself, or a job marked as required for merge). Read the body for the per-job status before classifying.

When in doubt, the agent should **demote** the item from Urgent to Important. Important items still appear in the briefing — they just don't claim the user's attention before everything else. A briefing with no Urgent items and 6 Important items is more useful than a briefing with 6 false-urgent items the user has to triage themselves.

#### Calendar and metric urgency rules (unchanged)

Calendar events and business metrics don't have a body to read, so the urgency rule for those is mechanical:
- Calendar event starting within 60 minutes → Urgent
- Calendar event in next 4 hours that needs prep → Important
- Business metric outside its normal range (e.g., revenue down >30% vs forecast, ROAS halved, error rate spiked) → Urgent
- Business metric trending in the wrong direction but still in range → Important

### Step 3: Compose the briefing

Present in this structure. **Urgent items must include sub-bullets with context AND a link to the source content** (the actual email, calendar event, task, etc.) so the user can click straight through to act on it. A bare one-line urgent item is not acceptable — the briefing's job is to make action one click away.

```markdown
# Morning Briefing — [Day, Month Date, Year]

## Urgent

**[Bold one-line headline of the urgent item]** — [link to source]
- [Sub-bullet: who, when, what context — the "why this is urgent"]
- [Sub-bullet: the specific action needed and any deadline]
- [Sub-bullet: anything else the user needs to decide before acting]

**[Next urgent headline]** — [link to source]
- [Same sub-bullet structure]

If nothing is urgent: "Nothing urgent — clear to focus."

## Today's Schedule
| Time | Event | Prep Needed |
|------|-------|-------------|
| 9:00 AM | Team standup | None |
| 11:00 AM | Vendor meeting — Acme Corp | Review latest invoice |
| 2:00 PM | Customer call — Smith Co | Pull order history |

## Email (X unread)
- **From [key contact]:** [subject] — [needs response / FYI] — [link]
- **From [vendor]:** [subject] — [action needed / informational] — [link]
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

### How to build the source links

The agent should produce real URLs the user can click. Use the underlying Google IDs already in the gws JSON output:

| Source | URL pattern | Example |
|---|---|---|
| **Gmail message** | `https://mail.google.com/mail/u/0/#inbox/{message_id}` | `https://mail.google.com/mail/u/0/#inbox/19d6d6ef3590984d` |
| **Gmail thread** | `https://mail.google.com/mail/u/0/#inbox/{thread_id}` | (use the `threadId` from gmail JSON if available) |
| **Calendar event** | `https://calendar.google.com/calendar/event?eid={base64url(event_id + " " + calendar_id)}` | Or just link to `https://calendar.google.com/calendar/u/0/r/day/{YYYY}/{MM}/{DD}` for the day view if you don't want to compute the eid |
| **Drive file** | `https://drive.google.com/file/d/{file_id}/view` | From `gws drive files list` JSON |
| **Google Doc / Sheet / Slide** | The `webViewLink` field returned by `gws drive files list` | Use it directly |
| **Tasks** | `https://tasks.google.com/embed/list/{task_list_id}` | (Tasks doesn't have per-task deep links) |
| **External (Bill.com, Stripe, etc.)** | Use the link from the email body if you parsed it | Or skip if there's no canonical URL |

For email links specifically, the message ID from `gws gmail +triage --format json` (the `id` field) plugs directly into the Gmail web URL. No transformation needed.

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

```markdown
# Morning Briefing — Wednesday, January 15, 2026

## Urgent

**Customer complaint from Sarah Miller** — [Open in Gmail](https://mail.google.com/mail/u/0/#inbox/19d6d6ef3590984d)
- Sent 11:14pm last night, subject: "Issue with my order #4521"
- Order shipped Tuesday, arrived damaged. Sarah is one of our top-10 customers (12 orders YTD).
- Action: Reply with refund + replacement before 11am vendor call so it doesn't slip.

**Cooler #2 temperature alert** — [Open in Sensor Dashboard](https://sensors.example.com/cooler-2)
- Tripped at 3:42am, current reading 38°F (target 34°F).
- Auto-acknowledged but not resolved. Could be a door left open or compressor.
- Action: Have a staff member check before opening; flag for service if still warm by 9am.

## Today's Schedule
| Time | Event | Prep Needed |
|------|-------|-------------|
| 9:00 AM | Team standup (30 min) | None |
| 11:00 AM | Vendor call — Fresh Farms (30 min) | Review Q1 pricing sheet in Drive |
| 2:30 PM | Staff 1:1 with Mike (30 min) | Check his task completions |

## Email (23 unread)
- **Sarah Miller:** "Issue with my order" — needs response — [Open](https://mail.google.com/mail/u/0/#inbox/19d6d6ef3590984d)
- **Fresh Farms:** "Updated price list for Q1" — review before 11am call — [Open](https://mail.google.com/mail/u/0/#inbox/19d6c39a56a7094f)
- **Square:** Daily sales summary — FYI — [Open](https://mail.google.com/mail/u/0/#inbox/19d6b9d9b14196ea)
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

Notice how every urgent item has:
1. A bold one-line headline
2. A clickable link to the source so the user can act in one click
3. 2-3 sub-bullets explaining the why, the action, and any deadline

A bare urgent line ("Customer complaint — needs response") forces the user to go hunt for the email. The structured version puts the action one click away.

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

# SMB Team Messaging Best Practices

> **Canonical location:** This file has moved to `skills/shared/smb-team-messaging.md`. This copy is kept for backwards compatibility. The shared version is the source of truth.

Platform-agnostic best practices for small business team communication. Applies to Slack, Google Chat, Discord, Teams, or any team messaging tool.

## The Problem

Most small businesses either:
1. **Under-communicate** — everything is verbal, nothing is documented, the next shift has no idea what happened
2. **Over-communicate** — every channel is noisy, nobody reads anything, important messages get buried

The goal is **structured communication**: the right information, in the right place, at the right time.

## Channel Design for Small Businesses

### The "3 Channel" Minimum (< 5 people)

| Channel | Purpose | Volume |
|---------|---------|--------|
| **#general** | Everything | Medium |
| **#alerts** | Urgent items, automated alerts | Low |
| **#daily-briefing** | Agent-posted daily digest | 1-2x/day |

### The "8 Channel" Standard (5-20 people)

| Channel | Purpose | Who Reads | Agent Posts |
|---------|---------|-----------|------------|
| **#general** | Announcements, company-wide | Everyone | Major alerts |
| **#daily-briefing** | Morning briefing, EOD summary | Everyone | Automated daily |
| **#orders** | Order status, fulfillment | Ops team | Order alerts |
| **#sales** | Revenue, transactions, wins | Leadership | Daily numbers |
| **#inventory** | Stock levels, vendor orders | Purchasing + ops | Low stock alerts |
| **#marketing** | Ads, campaigns, content | Marketing | Performance reports |
| **#ops-log** | Shift notes, equipment, facilities | Ops team | Shift reminders |
| **#random** | Non-work, team bonding | Everyone | Never |

### Rules for Adding Channels

- **Add a channel when:** A topic generates 5+ messages/day in #general and those messages are only relevant to some people
- **Don't add a channel when:** You're trying to organize theoretically. Unused channels are worse than a busy #general
- **Archive channels that go quiet** for 30+ days
- **Never duplicate information** across channels — post once, cross-link if needed

## What to Automate (Agent Posts)

### Daily (post to #daily-briefing)

**Morning briefing (7-8am):**
- Today's calendar / schedule
- Unread email summary
- Yesterday's revenue vs forecast
- Open tasks / action items
- Deliveries expected today
- Staffing notes (who's in, who's out)

**End-of-day summary (6-7pm):**
- Today's final revenue
- Orders completed / pending
- Issues that came up
- Shift handoff notes (if applicable)

### On-demand (post to #alerts)

**Trigger-based alerts — only when something needs attention:**
- Revenue significantly below forecast (>20% miss)
- Inventory below reorder point
- Customer complaint received
- Equipment alert (temp, uptime, etc.)
- Ad spend anomaly
- Large order placed

### Weekly (post to #sales or #daily-briefing)

**Friday PM or Monday AM:**
- Week's total revenue vs target
- Best/worst day
- Key wins and issues
- Next week's priorities

## What NOT to Automate

- **Don't post if there's nothing to say.** A "nothing to report" message is noise.
- **Don't duplicate email.** If it went to email, don't also post it to Slack/Chat unless it's urgent.
- **Don't alert on every metric.** Only alert when something is outside normal range.
- **Don't use @channel / @here for routine posts.** Reserve notifications for genuinely urgent items.
- **Don't post raw data dumps.** Format data into readable summaries with context.

## Message Formatting

### Good bot message anatomy

```
[Emoji] *Title — Context*

*Key metric:* Value (vs benchmark)
*Key metric:* Value (vs benchmark)

*What this means:* [One sentence interpretation]
*Action needed:* [What someone should do, or "None — informational only"]
```

### Example: Sales update (good)

```
📊 *Daily Sales — Wednesday, Jan 15*

*Revenue:* $2,450 (+11% vs forecast)
*Transactions:* 87 (avg ticket: $28.16)
*Top seller:* NY Strip (23 units)

Strong day. No action needed.
```

### Example: Sales update (bad — too much noise)

```
DAILY SALES REPORT FOR JANUARY 15 2026

Total revenue today was $2,450.00 which is $250 above our forecasted amount of $2,200.00, representing an 11.36% positive variance from the forecast. We processed a total of 87 individual transactions throughout the day with an average transaction value of $28.16 per transaction...

[continues for 500 more words]
```

**Rule: If it takes longer to read the message than to check the dashboard, the message is too long.**

### Example: Alert (good)

```
🚨 *Low Stock: Ground Beef*

Current: 8 lbs (reorder point: 15 lbs)
Estimated depletion: Tomorrow by 2pm
Suggested: Order from Fresh Farms today for Thursday delivery.
```

### Example: Alert (bad — not actionable)

```
Inventory update: Ground beef is at 8 lbs.
```

(So what? What should I do about it?)

## Threading Best Practices

- **Start a thread** for discussions. Keep the main channel as a feed of discrete updates.
- **Don't reply in the main channel** to a bot post — thread it.
- **Pin threads** that contain decisions or reference information.
- **Summarize long threads** with a main-channel message when a decision is reached.

## Notification Etiquette

| Urgency | How to Post | Example |
|---------|-------------|---------|
| **Urgent** | @channel + main message | Fire alarm, data breach, system down |
| **Important** | Main message, no mention | Revenue miss, customer complaint |
| **Informational** | Main message, formatted | Daily briefing, sales update |
| **FYI** | Thread or low-priority channel | Meeting notes, minor update |

**Rule: If you @channel more than once a week, you're doing it too much.** People will start ignoring notifications.

## Small Team Communication Cadence

### Daily rhythm

| Time | What | Where |
|------|------|-------|
| 7:30 AM | Morning briefing posted | #daily-briefing |
| 9:00 AM | Team reads + responds in thread | #daily-briefing (thread) |
| Throughout day | Issues and updates | Relevant channels |
| 6:00 PM | EOD summary / shift handoff | #daily-briefing or #ops-log |

### Weekly rhythm

| Day | What | Where |
|-----|------|-------|
| Monday AM | Week preview + priorities | #daily-briefing |
| Wednesday | Midweek check-in (optional) | #general |
| Friday PM | Week recap + wins | #sales or #daily-briefing |

### Monthly

- Channel cleanup (archive dead channels)
- Review which automated posts are actually useful
- Adjust alert thresholds based on noise level

## Platform-Specific Notes

### Slack

- Use **Blocks API** for structured messages (tables, sections, buttons)
- **Slack Connect** for vendor/partner communication (keeps them out of internal channels)
- **Canvas** for pinned reference docs within channels
- **Workflow Builder** for simple automations without code
- Bot needs to be **invited to each channel** it posts to

### Google Chat

- Use **cards** for structured messages (similar to Slack blocks)
- **Spaces** = channels. Create dedicated spaces for each topic area.
- Chat works best when your team is already in Google Workspace
- Use `gws chat +send` for simple messages, API for rich cards
- No equivalent of Slack Connect — use email for external comms

### For either platform

- **Consolidate bot posts.** One daily briefing > 10 separate automated messages
- **Name channels/spaces consistently.** Use lowercase, hyphens, descriptive names
- **Set descriptions/topics** on every channel so new team members understand the purpose
- **Review quarterly.** Are these channels still useful? Is the cadence right?

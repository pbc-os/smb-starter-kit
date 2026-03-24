---
name: google-chat
version: 1.0.0
tier: communication
description: "Google Chat messaging for small business teams. Send messages, post automated updates, manage spaces, run daily standups, and coordinate your team. Built on the gws CLI."
requires:
  bins: ["gws"]
  skills: ["google-workspace"]
---

# Google Chat

**Team messaging for small businesses using Google Workspace.**

Uses the [gws CLI](https://github.com/googleworkspace/cli) for all Chat operations. See the `google-workspace` skill for setup. For platform-agnostic team messaging best practices, see [SMB Team Messaging](../../shared/smb-team-messaging.md) — it applies to both Google Chat and Slack.

## Triggers

- "send a chat message"
- "post to [space/channel]"
- "message the team"
- "set up chat spaces"
- "post an update"
- Any request involving Google Chat spaces or messages

## Prerequisites

- `gws` CLI installed and authenticated with Chat scope
- Run `gws auth login -s chat` if not already done
- Google Workspace account (Chat is not available on free Gmail)

## Core Commands

```bash
# Send a message to a space
gws chat +send

# List spaces you're in
gws chat spaces list

# Get space details
gws chat spaces get --params '{"name": "spaces/SPACE_ID"}'

# List messages in a space
gws chat spaces messages list --params '{"parent": "spaces/SPACE_ID"}'

# Create a message
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "Your message here"}'

# Reply in a thread
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "Thread reply", "thread": {"name": "spaces/SPACE_ID/threads/THREAD_ID"}}'
```

## SMB Space Structure

### Recommended spaces for small businesses

| Space | Purpose | Who's In | Agent Posts |
|-------|---------|----------|------------|
| **Daily Briefing** | Morning digest + EOD summary | Everyone | Automated daily |
| **General** | Company-wide announcements | Everyone | Major alerts only |
| **Orders** | Order updates, fulfillment | Ops team | Order alerts |
| **Sales** | Revenue, transactions, wins | Leadership | Daily numbers |
| **Inventory** | Stock levels, vendor orders | Purchasing + ops | Low stock alerts |
| **Ops Log** | Shift notes, equipment, facilities | Ops team | Shift reminders |

### For very small teams (< 5 people)

Start with just 2-3 spaces:

| Space | Purpose |
|-------|---------|
| **General** | Everything |
| **Daily Briefing** | Automated agent posts |
| **Alerts** | Urgent items only |

### Create spaces

```bash
# Create a new space
gws chat spaces create --json '{
  "displayName": "Daily Briefing",
  "spaceType": "SPACE",
  "externalUserAllowed": false
}'
```

## SMB Messaging Patterns

### Morning standup post

```bash
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "*Daily Standup — Wednesday, Jan 15*\n\n*Yesterday:*\n• Revenue: $2,450 (forecast: $2,200, +11%)\n• 87 transactions, avg ticket $28.16\n• Vendor delivery received from Fresh Farms\n\n*Today:*\n• 3 deliveries scheduled\n• 2 customer pickups\n• Mike out — Sarah covering\n\n*Blockers:*\n• Cooler #2 running warm (38°F, target 34°F)"}'
```

### Shift handoff

```bash
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "*Shift Handoff — 3:00 PM*\n\n*Completed:*\n• Morning delivery received and checked in\n• Inventory count done for deli case\n• Customer order #4521 prepped for pickup\n\n*Needs attention:*\n• Paper towel supply low — reorder needed\n• Register 2 jamming on receipts\n\n*Heads up:*\n• Evening delivery from Sysco expected at 5pm\n• VIP customer (Johnson) pickup at 6pm"}'
```

### Automated sales report

```bash
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "📊 *Daily Sales — Wednesday, Jan 15*\n\n*Revenue:* $2,450 (+11% vs forecast)\n*Transactions:* 87 (avg ticket: $28.16)\n*Top seller:* NY Strip (23 units)\n\nStrong day. No action needed."}'
```

### Alert — needs attention

```bash
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "🚨 *Low Stock: Ground Beef*\n\nCurrent: 8 lbs (reorder point: 15 lbs)\nEstimated depletion: Tomorrow by 2pm\nSuggested: Order from Fresh Farms today for Thursday delivery."}'
```

### Weekly recap

```bash
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "*Weekly Recap — Week of Jan 13*\n\n*Revenue:* $12,450 (target: $11,500, +8.3%)\n*Best day:* Tuesday ($2,890)\n*Transactions:* 423 total, avg ticket $29.43\n\n*Highlights:*\n• New catering client signed\n• Google Ads ROAS improved to 3.2x\n\n*Issues:*\n• Cooler #2 still warm — repair Monday\n• 2 customer complaints (both resolved)\n\n*Next week:*\n• Vendor negotiation (Tuesday)\n• Monthly inventory count (Thursday)"}'
```

### Announce a file from Drive

```bash
# Built-in workflow
gws workflow +file-announce
```

## Rich Cards (Structured Messages)

For formatted messages with sections and buttons:

```bash
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{
    "cardsV2": [{
      "cardId": "daily-sales",
      "card": {
        "header": {
          "title": "Daily Sales Report",
          "subtitle": "Wednesday, January 15"
        },
        "sections": [{
          "widgets": [{
            "columns": {
              "columnItems": [
                {"widgets": [{"decoratedText": {"topLabel": "Revenue", "text": "$2,450"}}]},
                {"widgets": [{"decoratedText": {"topLabel": "vs Forecast", "text": "+11%"}}]}
              ]
            }
          }]
        }]
      }
    }]
  }'
```

## Communication Cadence

### Daily rhythm

| Time | What | Where |
|------|------|-------|
| 7:30 AM | Morning briefing | Daily Briefing space |
| 9:00 AM | Team reads + responds in thread | Daily Briefing (thread) |
| Throughout day | Issues and updates | Relevant spaces |
| 6:00 PM | EOD summary / shift handoff | Daily Briefing or Ops Log |

### Weekly

| Day | What | Where |
|-----|------|-------|
| Monday AM | Week preview + priorities | Daily Briefing |
| Friday PM | Week recap + wins | Sales or Daily Briefing |

## Notification Rules

| Urgency | How to Post | When |
|---------|-------------|------|
| **Urgent** | @all mention + message | System down, safety issue |
| **Important** | Direct message, no @all | Revenue miss, complaint |
| **Informational** | Space message | Daily briefing, updates |
| **FYI** | Thread reply | Meeting notes, minor updates |

**Rule: If you @all more than once a week, you're doing it too much.**

## Integration with Other Skills

- **`morning-briefing`** — Post the daily briefing to a Chat space
- **`gmail`** — Forward important emails as Chat messages
- **`google-drive`** — Share files in Chat spaces via `gws workflow +file-announce`
- **`google-sheets`** — Pull KPI data for automated reports
- **`autoresearch`** — Post overnight experiment results
- **`google-ads`** — Post ad performance summaries
- **`slack`** — Alternative for Slack-based teams (same patterns, different platform)

## Slack vs Google Chat?

| If your team... | Use |
|----------------|-----|
| Already uses Google Workspace for email/calendar/docs | **Google Chat** — it's integrated |
| Uses Slack for other projects or prefers it | **Slack** — see the `slack` skill |
| Is split or undecided | **Pick one and commit** — don't split communication across both |

Both platforms work. The patterns in [SMB Team Messaging](../../shared/smb-team-messaging.md) apply to either. The worst choice is using both — consolidate.

## Tips

- Use `gws chat spaces list` to find space IDs
- Use `--dry-run` before sending to preview the request
- Use threads for discussions — keep the main space as a clean feed
- Set space descriptions so everyone knows what each space is for
- Consolidate bot posts into 1-2 spaces, not every space
- Archive spaces nobody uses

## Related Skills

- `google-workspace` — Required setup (install and auth)
- `slack` — Alternative for Slack-based teams
- `morning-briefing` — Daily digest that can post to Chat

---

*Keep your team in sync. One update, one place, one time.*

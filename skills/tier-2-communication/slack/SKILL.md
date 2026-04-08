---
name: slack
version: 1.0.0
tier: communication
description: "Slack team messaging for small businesses. Send messages, manage channels, post automated updates, run daily standups, and coordinate your team. Includes SMB channel structure and team communication best practices."
requires:
  bins: ["curl", "jq"]
  skills: ["secrets-manager", "slack-directory"]
  secrets: ["slack-bot-token"]
---

# Slack

**Team messaging built for how small businesses actually communicate.**

For user lookups and directory management, see the `slack-directory` skill. This skill covers everything else: sending messages, managing channels, posting automated updates, and organizing your team's communication.

## Triggers

- "send a slack message"
- "post to #channel"
- "message the team"
- "set up slack channels"
- "slack standup"
- "post an update to slack"
- Any request involving Slack messaging, channels, or team communication

## Prerequisites

- **Slack Bot Token** with appropriate scopes (see Setup below)
- **jq** installed for JSON parsing
- `slack-directory` skill for user lookups
- `secrets-manager` skill for secure token storage

## Setup

### Required Bot Token Scopes

| Scope | What It Enables |
|-------|----------------|
| `chat:write` | Send messages to channels and DMs |
| `channels:read` | List and get info about public channels |
| `channels:manage` | Create and archive public channels |
| `groups:read` | List private channels the bot is in |
| `im:write` | Send direct messages |
| `users:read` | Look up users (for slack-directory) |
| `files:write` | Upload files to channels |
| `reactions:write` | Add emoji reactions |

### Getting Your Bot Token

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app (or use existing)
3. Go to **OAuth & Permissions** → add the scopes above
4. Install to your workspace
5. Copy the **Bot User OAuth Token** (`xoxb-...`)
6. Store securely:
   ```bash
   # GCP Secret Manager (recommended)
   echo -n "xoxb-your-token" | gcloud secrets create slack-bot-token --data-file=-

   # Or set as environment variable
   export SLACK_BOT_TOKEN="xoxb-your-token"
   ```

### Retrieving Your Token

```bash
# From GCP Secret Manager
TOKEN=$(gcloud secrets versions access latest --secret="slack-bot-token")

# From environment
TOKEN="$SLACK_BOT_TOKEN"
```

## Core Operations

### Send a message to a channel

```bash
TOKEN=$(gcloud secrets versions access latest --secret="slack-bot-token")

curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0XXXXXXX",
    "text": "Morning update: 3 deliveries scheduled, 2 pickups. Full details in the daily brief."
  }' | jq '.ok'
```

### Send a DM to someone

```bash
# First, look up the user ID (use slack-directory skill)
# Then send a DM
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "U09ABC123",
    "text": "Hey — vendor delivery moved to 3pm today. Can you be there to receive it?"
  }' | jq '.ok'
```

### Send a rich message (blocks)

```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0XXXXXXX",
    "blocks": [
      {
        "type": "header",
        "text": {"type": "plain_text", "text": "Daily Sales Report"}
      },
      {
        "type": "section",
        "fields": [
          {"type": "mrkdwn", "text": "*Revenue:*\n$2,450"},
          {"type": "mrkdwn", "text": "*vs Forecast:*\n+11%"},
          {"type": "mrkdwn", "text": "*Transactions:*\n87"},
          {"type": "mrkdwn", "text": "*Avg Ticket:*\n$28.16"}
        ]
      },
      {
        "type": "context",
        "elements": [
          {"type": "mrkdwn", "text": "Generated automatically by your AI agent"}
        ]
      }
    ]
  }'
```

### List channels

```bash
curl -s "https://slack.com/api/conversations.list" \
  -H "Authorization: Bearer $TOKEN" \
  -G -d "types=public_channel,private_channel" -d "limit=100" | \
  jq -r '.channels[] | "\(.id)\t\(.name)\t\(.num_members) members"'
```

### Create a channel

```bash
curl -s -X POST "https://slack.com/api/conversations.create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "daily-briefing",
    "is_private": false
  }' | jq '.channel.id'
```

### Upload a file

```bash
# Upload a report or document to a channel
curl -s -X POST "https://slack.com/api/files.uploadV2" \
  -H "Authorization: Bearer $TOKEN" \
  -F "channel_id=C0XXXXXXX" \
  -F "title=Weekly Sales Report" \
  -F "file=@./report.pdf"
```

### Set channel topic

```bash
curl -s -X POST "https://slack.com/api/conversations.setTopic" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0XXXXXXX",
    "topic": "Daily ops updates. Agent posts briefings at 7:30am."
  }'
```

### Thread a reply

```bash
# Reply in a thread (use ts from the parent message)
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0XXXXXXX",
    "thread_ts": "1705300000.000100",
    "text": "Update: delivery confirmed for 3pm."
  }'
```

## SMB Channel Structure

### Recommended channels for small businesses

| Channel | Purpose | Who's In | Bot Posts |
|---------|---------|----------|----------|
| `#general` | Company-wide announcements | Everyone | Major alerts only |
| `#daily-briefing` | Morning briefing + end-of-day summary | Everyone | Daily automated briefing |
| `#orders` | Order updates, fulfillment status | Operations team | Order alerts |
| `#inventory` | Stock levels, reorder alerts | Operations + purchasing | Low stock alerts |
| `#sales` | Revenue updates, daily numbers | Leadership + sales | Daily sales report |
| `#marketing` | Ad performance, campaign updates | Marketing team | Ad spend alerts |
| `#ops-log` | Shift handoffs, equipment issues | Operations team | Shift change reminders |
| `#vendor-comms` | Vendor updates, delivery tracking | Purchasing + ops | Delivery confirmations |

### For very small teams (< 5 people)

Don't over-channel. Start with:

| Channel | Purpose |
|---------|---------|
| `#general` | Everything that doesn't fit elsewhere |
| `#daily-briefing` | Automated morning briefing |
| `#alerts` | Anything that needs immediate attention |

Add channels only when a topic generates enough noise to warrant its own space.

## SMB Messaging Patterns

### Morning standup post

Post a structured daily standup every morning:

```
*Daily Standup — Wednesday, Jan 15*

*Yesterday:*
• Revenue: $2,450 (forecast: $2,200, +11%)
• 87 transactions, avg ticket $28.16
• Vendor delivery received from Fresh Farms

*Today:*
• 3 deliveries scheduled (UPS, Fresh Farms, Packaging Co)
• 2 customer pickups
• Mike out — Sarah covering his shift

*Blockers:*
• Cooler #2 running warm (38°F, target 34°F) — monitoring
• Waiting on quote from new packaging vendor

*Action items:*
• [ ] Follow up with landlord re: lease renewal (Owner)
• [ ] Submit Q1 tax docs by Friday (Owner)
```

### Shift handoff

Post at shift change so the next crew knows what's happening:

```
*Shift Handoff — 3:00 PM*

*Completed:*
• Morning delivery received and checked in
• Inventory count done for deli case
• Customer order #4521 prepped and ready for pickup

*In progress:*
• Cooler reorganization (about 60% done)

*Needs attention:*
• Customer called about catering for Saturday — details in #orders
• Paper towel supply low — reorder needed
• Register 2 jamming on receipts (works if you open/close the paper door)

*Heads up:*
• Evening delivery from Sysco expected at 5pm
• VIP customer (Johnson) picking up at 6pm — special order in walk-in, labeled
```

### Automated alerts

Post alerts when metrics cross thresholds:

```
🚨 *Alert: Revenue significantly below forecast*
Today's revenue: $1,200 (forecast: $2,100)
Shortfall: -43%
Time: 4:30 PM

Possible causes to investigate:
• Weather impact? (check conditions)
• Foot traffic? (compare to normal)
• Missing transactions? (check POS)
```

```
📦 *Low Stock Alert*
The following items are below reorder point:
• Ground Beef (8 lbs remaining, reorder at 15)
• Chicken Breast (12 lbs remaining, reorder at 20)

Suggested: Place order with Fresh Farms by EOD for Thursday delivery.
```

### Weekly recap

Post a weekly summary every Friday afternoon or Monday morning:

```
*Weekly Recap — Week of Jan 13*

*Revenue:* $12,450 (target: $11,500, +8.3%)
*Best day:* Tuesday ($2,890)
*Transactions:* 423 total, avg ticket $29.43

*Highlights:*
• New catering client signed (Johnson Corp, $800/week)
• Google Ads ROAS improved to 3.2x (was 2.5x)

*Issues:*
• Cooler #2 still running warm — repair scheduled Monday
• 2 customer complaints (both resolved same-day)

*Next week:*
• Vendor price negotiation with Fresh Farms (Tuesday)
• Monthly inventory count (Thursday)
• Payroll deadline (Friday)
```

## Integration with Other Skills

- **`slack-directory`** — Look up user IDs for DMs and mentions
- **`morning-briefing`** — Post the daily briefing to `#daily-briefing`
- **`gmail`** — Forward important emails as Slack messages
- **`google-sheets`** — Pull KPI data for automated reports
- **`google-drive`** — Share Drive links in channels
- **`autoresearch`** — Post overnight experiment results
- **`google-ads`** — Post ad performance summaries

## Tips

- **Don't over-notify.** Every bot message should be actionable or informational — never both at once.
- **Use threads** for follow-ups. Keep the main channel clean.
- **Use blocks** for structured data (sales reports, KPIs). Plain text for quick updates.
- **Pin important messages** — delivery schedules, SOPs, emergency contacts.
- **Set channel topics** to explain what the channel is for and what the bot posts there.
- **Respect DND.** Don't send non-urgent DMs outside business hours.
- **One channel for bot posts.** Consolidate automated messages into `#daily-briefing` or `#alerts` rather than spraying every channel.
- **Archive dead channels.** If nobody's posted in 30 days, archive it.

## API Reference

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `chat.postMessage` | POST | Send a message |
| `chat.update` | POST | Edit a message |
| `chat.delete` | POST | Delete a message |
| `conversations.list` | GET | List channels |
| `conversations.create` | POST | Create a channel |
| `conversations.invite` | POST | Add someone to a channel |
| `conversations.setTopic` | POST | Set channel topic |
| `conversations.setPurpose` | POST | Set channel purpose |
| `files.uploadV2` | POST | Upload a file |
| `reactions.add` | POST | Add an emoji reaction |
| `users.list` | GET | List users (see slack-directory) |

Full docs: [api.slack.com/methods](https://api.slack.com/methods)

## Related Skills

- `slack-directory` — User lookup and caching (prerequisite)
- `google-chat` — Alternative for Google Workspace teams
- `morning-briefing` — Daily digest that can post to Slack
- `secrets-manager` — Secure token storage

---

*Your team channel is your operational heartbeat. Keep it structured and it keeps you informed.*

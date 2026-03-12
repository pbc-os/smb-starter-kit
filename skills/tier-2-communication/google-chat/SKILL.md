---
name: google-chat
version: 1.0.0
description: "Google Chat messaging for small business teams. Send messages, post updates, and manage spaces. Built on the gws CLI."
metadata:
  openclaw:
    category: "communication"
    requires:
      bins: ["gws"]
      skills: ["google-workspace"]
---

# Google Chat

**Team messaging for small businesses using Google Workspace.**

Uses the [gws CLI](https://github.com/googleworkspace/cli) for all Chat operations. See the `google-workspace` skill for setup.

## Triggers

- "send a chat message"
- "post to [space/channel]"
- "message the team"
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

# List messages in a space
gws chat spaces messages list --params '{"parent": "spaces/SPACE_ID"}'
```

## Common Workflows

### Post a team update

```bash
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "Morning update: Today we have 3 deliveries scheduled and 2 customer pickups. Full details in the daily brief."}'
```

### Announce a file from Drive

```bash
# Built-in workflow for sharing Drive files in Chat
gws workflow +file-announce
```

### Post automated alerts

```bash
# Example: Post a sales alert
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "📊 Daily sales hit $2,450 — 15% above forecast. Strong Tuesday."}'
```

### Find your spaces

```bash
# List all spaces with their IDs
gws chat spaces list --format table
```

## SMB Team Patterns

### Morning standup post
Combine with other skills to post a daily standup:
```bash
# Get standup data, then post to team chat
gws workflow +standup-report --format json
```

### Shift handoff
Post end-of-shift notes for the next team:
```bash
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "Shift handoff:\n- 2 pending orders need pickup\n- Cooler #3 temp logged at 38°F\n- Vendor delivery expected at 2pm"}'
```

## Integration with Other Skills

- **`morning-briefing`** — Post the daily briefing to a Chat space
- **`gmail`** — Forward important emails as Chat messages
- **`google-drive`** — Share files in Chat spaces

## Tips

- Use `gws chat spaces list` to find space IDs — you'll need them for all message operations
- Use `--dry-run` before sending to preview the message
- For Slack-based teams, use the `slack-directory` skill instead

## Related Skills

- `google-workspace` — Required setup (install and auth)
- `slack-directory` — Alternative for Slack-based teams
- `morning-briefing` — Daily digest that can post to Chat

---

*Keep your team in sync without leaving the terminal.*

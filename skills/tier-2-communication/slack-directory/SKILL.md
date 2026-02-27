---
name: slack-directory
description: Look up Slack users by name with fuzzy matching. Caches discoveries for instant future lookups.
---

# Slack Directory Lookup

## Why This Skill Exists

**The Problem:**  
When someone says "DM Sarah about the budget" or "add Mike to the channel," you need a Slack user ID — not a name. Slack's API requires IDs for all user operations, but humans think in names.

**The Solution:**  
This skill lets you search Slack users by partial name (first, last, display name, or username), handles multiple matches gracefully, and builds a local cache so you never look up the same person twice.

**Real-world example:**  
> "Hey, message the new hire about onboarding"  
> → "What's their name?"  
> → "Jamie something... started last week"  
> → Run lookup for "Jamie" → Find Jamie Chen (U09ABC123)  
> → Cache the mapping → Send the message

---

## When to Use This Skill

| Situation | Use This Skill |
|-----------|---------------|
| Need to DM someone by name | ✅ Yes |
| Need to @mention someone | ✅ Yes |
| Adding users to channels | ✅ Yes |
| Building a people directory | ✅ Yes |
| You already have the Slack ID | ❌ No (just use it) |

---

## How It Works

### Step 1: Check Your Cache First

Before calling the API, check if you already have the mapping cached (in TOOLS.md, a JSON file, or wherever you store local state):

```markdown
### People Directory
| Name | Slack ID | Notes |
|------|----------|-------|
| Sarah Chen | U09ABC123 | Engineering |
| Mike Brown | U07XYZ789 | Sales lead |
```

**Why cache?** Slack API calls cost time and rate limits. Most workspaces have the same 20-50 people you interact with regularly. Cache them once, use forever.

### Step 2: Fuzzy Search via API

If not cached, run the lookup:

```bash
./lookup.sh "jamie"
```

The script searches across:
- `real_name` (e.g., "Jamie Chen")
- `display_name` (e.g., "Jamie C")  
- `username` (e.g., "jamie.chen")

Case-insensitive, partial match.

### Step 3: Handle Results

**Single match → Use it and cache it:**
```
✅ Single match found:
| Jamie Chen | U09ABC123 | jamie.chen@company.com |
```

**Multiple matches → Clarify with the user:**
```
⚠️ Multiple matches for 'jamie' (2 found):
1. Jamie Chen (U09ABC123) - jamie.chen@company.com
2. Jamie Rodriguez (U08DEF456) - jamie.r@company.com

Which one did you mean?
```

**No matches → Help troubleshoot:**
```
❌ No matches found for 'jamie'

Suggestions:
- Check spelling
- Try first or last name only
- They may not be in this workspace
```

### Step 4: Update Cache

After finding someone new, add them to your local cache for next time.

---

## Setup

### Requirements

1. **Slack Bot Token** with `users:read` scope
2. **jq** installed for JSON parsing
3. **curl** for API calls

### Getting Your Bot Token

If using Clawdbot with Slack channel configured, your token is already available. Otherwise:

1. Create a Slack App at api.slack.com/apps
2. Add Bot Token Scopes: `users:read`, `users:read.email` (optional)
3. Install to workspace
4. Copy the Bot User OAuth Token (`xoxb-...`)

### Token Storage Options

The included `lookup.sh` expects the token in an environment variable or secrets manager. Modify line 13 for your setup:

```bash
# Option 1: Environment variable
TOKEN="${SLACK_BOT_TOKEN}"

# Option 2: GCP Secret Manager
TOKEN=$(gcloud secrets versions access latest --secret="slack-bot-token" --project=YOUR_PROJECT)

# Option 3: AWS Secrets Manager  
TOKEN=$(aws secretsmanager get-secret-value --secret-id slack-bot-token --query SecretString --output text)

# Option 4: File (less secure, but simple)
TOKEN=$(cat ~/.slack-token)
```

---

## API Details

**Endpoint:** `https://slack.com/api/users.list`  
**Auth:** `Authorization: Bearer xoxb-...`  
**Rate limit:** Tier 2 (~20 requests/minute) — safe for occasional lookups

### Useful User Object Fields

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Slack user ID (what you need) | U09ABC123 |
| `name` | Username/handle | jamie.chen |
| `real_name` | Full name | Jamie Chen |
| `profile.display_name` | Custom display name | Jamie |
| `profile.email` | Email (if visible) | jamie@co.com |
| `deleted` | Deactivated account? | false |
| `is_bot` | Bot account? | false |

### Manual API Call (if script unavailable)

```bash
TOKEN="xoxb-your-token"

# List all active users
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://slack.com/api/users.list" | \
  jq '.members[] | select(.deleted == false and .is_bot == false) | {id, name, real_name}'

# Filter for a name
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://slack.com/api/users.list" | \
  jq --arg q "jamie" '.members[] | select(.deleted == false) | select((.real_name // "" | ascii_downcase | contains($q)))'
```

---

## Common Patterns

### "DM [name] about [topic]"
1. Check cache for name
2. If not found → Run lookup
3. If single match → Cache it, send DM
4. If multiple → Ask "Which [name]?"
5. If none → Ask for clarification

### "Add [name] to #channel"
Same flow, then use the ID with `conversations.invite`

### "Who is [name]?"
Run lookup, display full profile info (name, email, title if available)

### Building Initial Directory
For new workspaces, you can bulk-cache everyone:

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://slack.com/api/users.list" | \
  jq -r '.members[] | select(.deleted == false and .is_bot == false) | "| \(.real_name) | \(.id) | |"'
```

This outputs a markdown table you can paste into your cache file.

---

## Why This Belongs in Tier 2 (Communication)

This skill is foundational to Slack communication:

- **Tier 1** is infrastructure (secrets, auth, basic setup)
- **Tier 2** is communication (email, calendar, Slack, messaging)
- **Tier 3+** is business operations

If your agent uses Slack, it will eventually need to look up users. This skill solves that cleanly, with caching to make it fast and reliable over time.

---

## Files Included

```
slack-directory/
├── SKILL.md      # This documentation
└── lookup.sh     # Bash script for fuzzy user search
```

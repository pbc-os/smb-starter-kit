#!/bin/bash
# Slack Directory Lookup - Fuzzy search for users by name
# Usage: ./lookup.sh "search term"
#
# WHY THIS EXISTS:
# Slack's API requires user IDs for all operations, but humans think in names.
# This script bridges that gap with fuzzy name matching.

set -e

QUERY="${1:-}"
if [[ -z "$QUERY" ]]; then
    echo "Usage: $0 <name>"
    echo "Example: $0 'Jamie'"
    echo ""
    echo "Searches real_name, display_name, and username (case-insensitive)"
    exit 1
fi

# ============================================================
# TOKEN CONFIGURATION - Modify this section for your setup
# ============================================================

# Option 1: Environment variable (recommended for dev)
TOKEN="${SLACK_BOT_TOKEN:-}"

# Option 2: GCP Secret Manager (uncomment and modify)
# TOKEN=$(gcloud secrets versions access latest --secret="slack-bot-token" --project=YOUR_PROJECT 2>/dev/null)

# Option 3: AWS Secrets Manager (uncomment and modify)
# TOKEN=$(aws secretsmanager get-secret-value --secret-id slack-bot-token --query SecretString --output text 2>/dev/null)

# Option 4: File-based (simple but less secure)
# TOKEN=$(cat ~/.slack-token 2>/dev/null)

# ============================================================

if [[ -z "$TOKEN" ]]; then
    echo "Error: Could not retrieve Slack bot token"
    echo ""
    echo "Configure your token by editing this script (lines 16-28)"
    echo "or set the SLACK_BOT_TOKEN environment variable:"
    echo ""
    echo "  export SLACK_BOT_TOKEN='xoxb-your-token-here'"
    exit 1
fi

# Normalize query to lowercase for matching
QUERY_LOWER=$(echo "$QUERY" | tr '[:upper:]' '[:lower:]')

# Fetch users and filter
# WHY: We pull all users and filter locally because Slack's users.list
# doesn't support server-side name filtering. For large workspaces,
# consider caching the full user list and searching locally.

RESULTS=$(curl -s -H "Authorization: Bearer $TOKEN" \
    "https://slack.com/api/users.list" | \
    jq --arg q "$QUERY_LOWER" '
        .members[] 
        | select(.deleted == false and .is_bot == false and .id != "USLACKBOT")
        | select(
            ((.real_name // "") | ascii_downcase | contains($q)) or
            ((.profile.display_name // "") | ascii_downcase | contains($q)) or
            ((.name // "") | ascii_downcase | contains($q))
        )
        | {
            id,
            name,
            real_name,
            display_name: .profile.display_name,
            email: .profile.email,
            title: .profile.title
        }
    ')

COUNT=$(echo "$RESULTS" | jq -s 'length')

if [[ "$COUNT" -eq 0 ]]; then
    echo "❌ No matches found for '$QUERY'"
    echo ""
    echo "Suggestions:"
    echo "  - Check spelling"
    echo "  - Try first or last name only"
    echo "  - Use a nickname or username"
    echo "  - They may not be in this workspace"
    exit 1
elif [[ "$COUNT" -eq 1 ]]; then
    echo "✅ Single match found:"
    echo ""
    echo "$RESULTS" | jq -r '"  Name:  \(.real_name)\n  ID:    \(.id)\n  Email: \(.email // "not visible")"'
    echo ""
    echo "Cache this mapping (markdown table format):"
    NAME=$(echo "$RESULTS" | jq -r '.real_name')
    ID=$(echo "$RESULTS" | jq -r '.id')
    echo "| $NAME | $ID | |"
else
    echo "⚠️  Multiple matches for '$QUERY' ($COUNT found):"
    echo ""
    echo "$RESULTS" | jq -rs '
        to_entries[] | 
        "\(.key + 1). \(.value.real_name) (\(.value.id))\n   \(.value.email // "no email visible")"
    '
    echo ""
    echo "Specify more precisely, or pick one to cache."
fi

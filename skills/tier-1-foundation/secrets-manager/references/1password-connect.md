# 1Password Connect — Full Setup Guide

## Table of Contents
- [1. Account Setup](#1-account-setup)
- [2. CLI Installation](#2-cli-installation)
- [3. Authentication](#3-authentication)
- [4. Creating Your First Secret](#4-creating-your-first-secret)
- [5. Granting AI Agent Access](#5-granting-ai-agent-access)
- [6. Gateway Wrapper Script](#6-gateway-wrapper-script)
- [7. Common Issues & Troubleshooting](#7-common-issues--troubleshooting)

---

## 1. Account Setup

### Prerequisites
- A 1Password account on **Business** or **Teams** plan: https://1password.com/business
- Admin access to your 1Password organization

> **Note:** 1Password's CLI (`op`) works with Individual plans too, but Connect Server (for server-side automation) requires Business/Teams.

### Option A: CLI-Only (Simplest)
Use the `op` CLI directly. No Connect Server needed. Best for single-machine setups.

### Option B: 1Password Connect Server (For Production)
Deploy a Connect Server for multi-machine or headless access.

1. Log into https://my.1password.com
2. Go to **Integrations** → **Directory**
3. Click **1Password Connect Server** → **Set Up**
4. Download the `1password-credentials.json` file
5. Create an access token and save it

**What you should see:** A credentials file and a token string. Store both securely.

---

## 2. CLI Installation

### Install 1Password CLI

**macOS (Homebrew):**
```bash
brew install --cask 1password-cli
```

**Linux (amd64):**
```bash
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
  sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/amd64 stable main" | \
  sudo tee /etc/apt/sources.list.d/1password.list
sudo apt update && sudo apt install 1password-cli
```

**Linux (arm64):**
```bash
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
  sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
echo "deb [arch=arm64 signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/arm64 stable main" | \
  sudo tee /etc/apt/sources.list.d/1password.list
sudo apt update && sudo apt install 1password-cli
```

### Verify Installation

```bash
op --version
```

**What you should see:** Version number like `2.26.1`

---

## 3. Authentication

### Sign In (Interactive)

```bash
op account add --address YOUR_TEAM.1password.com --email you@example.com
op signin
```

**What you should see:** You'll be prompted for your Secret Key and Master Password. After signing in, you get a session token.

### Enable Biometric Unlock (macOS — Optional)

If you have 1Password desktop app with biometric:
```bash
op signin --account YOUR_TEAM
```

Uses Touch ID instead of typing the master password every time.

### Service Account Token (For Automation)

1. Go to https://my.1password.com → **Developer** → **Service Accounts**
2. Click **New Service Account**
3. Name it (e.g., "clawdbot-agent")
4. Grant access to specific vaults
5. Copy the token

Set the token as an environment variable:
```bash
export OP_SERVICE_ACCOUNT_TOKEN="your-service-account-token"
```

### Verify Authentication

```bash
op vault list
```

**What you should see:** A table of vaults you have access to:
```
ID                            NAME
xxxxxxxxxxxxxxxxxxxxxxxxxxxx  Personal
xxxxxxxxxxxxxxxxxxxxxxxxxxxx  Shared
```

---

## 4. Creating Your First Secret

### 1Password uses Items, not raw key-value secrets. Create an item:

### Create a Secret Item

```bash
op item create \
  --category=login \
  --title="my-first-secret" \
  --vault="Shared" \
  --generate-password \
  "credential=my-super-secret-value"
```

**What you should see:** JSON output with the created item details.

### Simpler: Create a Secure Note

```bash
op item create \
  --category="Secure Note" \
  --title="my-api-key" \
  --vault="Shared" \
  "notesPlain=my-super-secret-value"
```

### Read a Secret

Using secret references (recommended):
```bash
op read "op://Shared/my-first-secret/credential"
```

**What you should see:** `my-super-secret-value`

### List Items in a Vault

```bash
op item list --vault="Shared" --format=json | jq '.[].title'
```

**What you should see:** A list of item titles.

### Update a Secret

```bash
op item edit "my-first-secret" --vault="Shared" "credential=updated-value"
```

### Delete a Secret

```bash
op item delete "my-first-secret" --vault="Shared"
```

**What you should see:** No output (success is silent). Verify with `op item list`.

---

## 5. Granting AI Agent Access

### Service Accounts (Recommended for Automation)

1. Go to **Developer** → **Service Accounts** in the web UI
2. Create a new service account named "clawdbot-agent"
3. Grant it read-only access to the vault containing your secrets
4. Copy the service account token

### Set Up on the Agent Machine

```bash
# Set the service account token (add to your shell profile or wrapper script)
export OP_SERVICE_ACCOUNT_TOKEN="your-token-here"

# Verify it works
op vault list
```

### Security Notes
- Service account tokens don't expire by default, but you can revoke them anytime
- Grant access to specific vaults only — not the entire account
- Use read-only access unless the agent needs to create/modify secrets

---

## 6. Gateway Wrapper Script

Create `~/.clawdbot/gateway-wrapper.sh`:

```bash
#!/bin/bash
set -euo pipefail

# Set your service account token
export OP_SERVICE_ACCOUNT_TOKEN="your-service-account-token"

fetch_secret() {
  op read "op://Shared/$1/credential" 2>/dev/null
}

export SLACK_BOT_TOKEN=$(fetch_secret "slack-bot-token")
export SQUARE_ACCESS_TOKEN=$(fetch_secret "square-access-token")
# Add more as needed...

exec clawdbot gateway start
```

```bash
chmod +x ~/.clawdbot/gateway-wrapper.sh
```

> **Tip:** Store the service account token itself in a secure location (e.g., a system keychain or a file with `chmod 600`), not hardcoded in the script.

---

## 7. Common Issues & Troubleshooting

### "You are not signed in"

**Cause:** Session expired or no active sign-in.

**Fix (Interactive):**
```bash
op signin
```

**Fix (Service Account):**
```bash
export OP_SERVICE_ACCOUNT_TOKEN="your-token"
```

### "op: command not found"

**Fix (macOS):**
```bash
brew install --cask 1password-cli
```

### "could not find vault"

**Cause:** Vault name is wrong, or the service account doesn't have access.

**Fix:**
```bash
# List available vaults
op vault list

# Check vault name spelling (case-sensitive)
```

### "could not find item"

**Cause:** Item doesn't exist, wrong vault, or wrong field name.

**Fix:**
```bash
# List items in the vault
op item list --vault="Shared"

# Get full item details to find the right field
op item get "item-name" --vault="Shared" --format=json
```

### "service account doesn't have access"

**Fix:** Go to 1Password web UI → **Developer** → **Service Accounts** → Edit the account → Grant access to the needed vault.

### Secret Reference Format

The `op://` reference format is:
```
op://VAULT_NAME/ITEM_TITLE/FIELD_NAME
```

Common field names:
- `credential` — for login items
- `password` — for login items
- `notesPlain` — for secure notes
- Custom field names you've defined

---

**Ask me anything about 1Password Connect. It's the easiest option if you're already a 1Password user.**

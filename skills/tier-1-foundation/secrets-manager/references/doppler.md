# Doppler — Full Setup Guide

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

### Create a Doppler Account

1. Sign up at https://dashboard.doppler.com/register
2. Create a **Workplace** (your organization)
3. Create a **Project** (e.g., `clawdbot`)

**What you should see:** The Doppler dashboard with your project listed. Each project has three default environments: Development, Staging, Production.

### Understand Doppler's Structure

```
Workplace
└── Project (e.g., "clawdbot")
    ├── dev      ← Development config
    ├── stg      ← Staging config
    └── prd      ← Production config
```

Each environment/config has its own set of secrets. This is Doppler's killer feature — same secret names, different values per environment.

### Free Tier Limits
- 5 projects
- Unlimited secrets per project
- Unlimited team members (Community plan)
- No credit card required

---

## 2. CLI Installation

### Install Doppler CLI

**macOS (Homebrew):**
```bash
brew install dopplerhq/cli/doppler
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl gnupg
curl -sLf --retry 3 --tlsv1.2 --proto "=https" \
  'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key' | \
  sudo gpg --dearmor -o /usr/share/keyrings/doppler-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/doppler-archive-keyring.gpg] https://packages.doppler.com/public/cli/deb/debian any-version main" | \
  sudo tee /etc/apt/sources.list.d/doppler-cli.list
sudo apt-get update && sudo apt-get install doppler
```

**Linux (RHEL/Fedora):**
```bash
sudo rpm --import 'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key'
curl -sLf --retry 3 --tlsv1.2 --proto "=https" \
  'https://packages.doppler.com/public/cli/config.rpm.txt' | \
  sudo tee /etc/yum.repos.d/doppler-cli.repo
sudo yum update && sudo yum install doppler
```

**Any platform (npm):**
```bash
npm install -g @dopplerhq/cli
```

### Verify Installation

```bash
doppler --version
```

**What you should see:** Version like `3.68.0`

---

## 3. Authentication

### Login

```bash
doppler login
```

**What you should see:** A browser window opens. Authorize the CLI. Terminal prints "Welcome, [your name]".

### Set Up Your Project

```bash
doppler setup
```

**What you should see:** Interactive prompts to select your project and config (environment). Choose your project (e.g., `clawdbot`) and config (e.g., `prd` for production).

### Verify Authentication

```bash
doppler secrets
```

**What you should see:** A table of all secrets in the selected project/config. If it's a new project, the table will be empty.

---

## 4. Creating Your First Secret

### Create a Secret

```bash
doppler secrets set MY_FIRST_SECRET="my-super-secret-value"
```

**What you should see:**
```
┌───────────────────┬────────────────────────┐
│ NAME              │ VALUE                  │
├───────────────────┼────────────────────────┤
│ MY_FIRST_SECRET   │ my-super-secret-value  │
└───────────────────┴────────────────────────┘
```

### Set Multiple Secrets at Once

```bash
doppler secrets set \
  SLACK_TOKEN="xoxb-..." \
  SQUARE_KEY="sq0atp-..." \
  API_SECRET="my-other-secret"
```

### Read a Secret

```bash
doppler secrets get MY_FIRST_SECRET --plain
```

**What you should see:** `my-super-secret-value`

### List All Secrets

```bash
doppler secrets
```

**What you should see:** A table of all secret names and values.

### Update a Secret

```bash
doppler secrets set MY_FIRST_SECRET="updated-value"
```

### Delete a Secret

```bash
doppler secrets delete MY_FIRST_SECRET
```

**What you should see:** Confirmation prompt, then the secret is removed.

---

## 5. Granting AI Agent Access

### Service Tokens (Recommended for Automation)

Service tokens are scoped to a specific project + config. Perfect for the agent.

1. Go to https://dashboard.doppler.com → Your project → Config (e.g., `prd`)
2. Click **Access** → **Service Tokens**
3. Click **Generate** → Name it "clawdbot-agent"
4. Copy the token

Or via CLI:
```bash
doppler configs tokens create clawdbot-agent \
  --project clawdbot \
  --config prd \
  --plain
```

### Set Up on the Agent Machine

```bash
# Set the service token (one-time)
doppler configure set token dp.st.xxxxxxxxxxxx --scope /path/to/clawdbot
```

Or use it as an environment variable:
```bash
export DOPPLER_TOKEN="dp.st.xxxxxxxxxxxx"
```

### Verify Agent Access

```bash
DOPPLER_TOKEN="dp.st.xxxx" doppler secrets
```

**What you should see:** The same table of secrets, accessed via the service token.

---

## 6. Gateway Wrapper Script

Create `~/.clawdbot/gateway-wrapper.sh`:

### Option A: Doppler Run (Recommended — Simplest)

Doppler can inject ALL secrets as environment variables automatically:

```bash
#!/bin/bash
set -euo pipefail

export DOPPLER_TOKEN="dp.st.your-service-token"

# doppler run injects ALL project secrets as env vars, then runs the command
exec doppler run -- clawdbot gateway start
```

No need to `fetch_secret` one by one — Doppler handles it.

### Option B: Selective Fetch

```bash
#!/bin/bash
set -euo pipefail

export DOPPLER_TOKEN="dp.st.your-service-token"

fetch_secret() {
  doppler secrets get "$1" --plain 2>/dev/null
}

export SLACK_BOT_TOKEN=$(fetch_secret "SLACK_BOT_TOKEN")
export SQUARE_ACCESS_TOKEN=$(fetch_secret "SQUARE_ACCESS_TOKEN")
# Add more as needed...

exec clawdbot gateway start
```

```bash
chmod +x ~/.clawdbot/gateway-wrapper.sh
```

> **Tip:** Option A (`doppler run`) is the Doppler Way™ — it's simpler, injects everything, and auto-restarts on secret changes if configured.

---

## 7. Common Issues & Troubleshooting

### "Unable to fetch secrets"

**Cause:** Invalid or expired service token.

**Fix:**
```bash
# Generate a new service token
doppler configs tokens create clawdbot-agent-v2 \
  --project clawdbot --config prd --plain
```

### "doppler: command not found"

**Fix (macOS):**
```bash
brew install dopplerhq/cli/doppler
```

### "No project or config selected"

**Cause:** `doppler setup` hasn't been run in the current directory.

**Fix:**
```bash
doppler setup
# Select your project and config
```

Or specify inline:
```bash
doppler secrets --project clawdbot --config prd
```

### "Missing required permission"

**Cause:** The service token doesn't have access to the requested config.

**Fix:** Generate a new token scoped to the correct project + config in the Doppler dashboard.

### "Connection refused" or "Network error"

**Cause:** Firewall or proxy blocking Doppler API.

**Fix:**
```bash
# Test connectivity
curl -s https://api.doppler.com/v3/me -H "Authorization: Bearer $DOPPLER_TOKEN"
```

### Secrets Not Updating

**Cause:** Doppler CLI caches responses briefly.

**Fix:**
```bash
# Force refresh
doppler secrets --no-cache
```

---

**Ask me anything about Doppler. It's the most developer-friendly option on this list.**

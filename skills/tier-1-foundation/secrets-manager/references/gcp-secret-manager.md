# GCP Secret Manager — Full Setup Guide

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

### Enable the Secret Manager API

1. Open the GCP Console: https://console.cloud.google.com
2. Select or create a project (e.g., `my-project-123`)
3. Navigate to **APIs & Services → Library**
4. Search for "Secret Manager API"
5. Click **Enable**

**What you should see:** A green checkmark and "API enabled" confirmation. The Secret Manager page becomes accessible.

### Note your Project ID

```bash
# Find your project ID (you'll need this everywhere)
gcloud config get-value project
```

**What you should see:** Your project ID printed, e.g., `my-project-123`

If nothing prints, set it:
```bash
gcloud config set project YOUR_PROJECT_ID
```

---

## 2. CLI Installation

### Install Google Cloud SDK

**macOS (Homebrew):**
```bash
brew install --cask google-cloud-sdk
```

**macOS (Manual):**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Linux (apt):**
```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt cloud-sdk main" | \
  sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
  sudo tee /usr/share/keyrings/cloud.google.asc
sudo apt update && sudo apt install google-cloud-cli
```

**Linux (snap):**
```bash
snap install google-cloud-cli --classic
```

### Verify Installation

```bash
gcloud version
```

**What you should see:** Version info like:
```
Google Cloud SDK 469.0.0
bq 2.0.101
core 2024.03.29
gsutil 5.27
```

---

## 3. Authentication

### Interactive Login (For Development)

```bash
gcloud auth login
```

**What you should see:** A browser window opens. Sign in with your Google account. Terminal prints "You are now logged in as [your-email]."

### Application Default Credentials (For Scripts/Automation)

```bash
gcloud auth application-default login
```

**What you should see:** Browser opens again. After sign-in, credentials are saved to `~/.config/gcloud/application_default_credentials.json`.

### Verify Authentication

```bash
gcloud auth list
```

**What you should see:** Your account listed with an asterisk (*) marking the active account:
```
     ACCOUNT                  STATUS
*    you@example.com          ACTIVE
```

### Required Permissions

The authenticated account needs one of these IAM roles:
- `roles/secretmanager.admin` — Full control (create, read, update, delete)
- `roles/secretmanager.secretAccessor` — Read-only (for production/agent use)

Grant a role:
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:you@example.com" \
  --role="roles/secretmanager.admin"
```

---

## 4. Creating Your First Secret

### Create a Secret

```bash
echo -n "my-super-secret-value" | gcloud secrets create my-first-secret \
  --data-file=- \
  --project=YOUR_PROJECT_ID
```

**What you should see:**
```
Created secret [my-first-secret].
```

### Read a Secret

```bash
gcloud secrets versions access latest --secret="my-first-secret" --project=YOUR_PROJECT_ID
```

**What you should see:** `my-super-secret-value` printed to stdout.

### Update a Secret (Add New Version)

```bash
echo -n "updated-value" | gcloud secrets versions add my-first-secret \
  --data-file=- \
  --project=YOUR_PROJECT_ID
```

**What you should see:**
```
Created version [2] of the secret [my-first-secret].
```

### List All Secrets

```bash
gcloud secrets list --project=YOUR_PROJECT_ID --format="table(name)"
```

**What you should see:** A table listing all secret names in the project.

### Delete a Secret

```bash
gcloud secrets delete my-first-secret --project=YOUR_PROJECT_ID --quiet
```

**What you should see:**
```
Deleted secret [my-first-secret].
```

---

## 5. Granting AI Agent Access

For production, create a dedicated service account so the agent can access secrets without your personal credentials.

### Create a Service Account

```bash
gcloud iam service-accounts create clawdbot-agent \
  --display-name="Clawdbot AI Agent" \
  --project=YOUR_PROJECT_ID
```

### Grant Secret Access

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:clawdbot-agent@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Create and Download a Key (For Non-GCE Machines)

```bash
gcloud iam service-accounts keys create ~/clawdbot-sa-key.json \
  --iam-account=clawdbot-agent@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

**⚠️ Store this key file securely. Do NOT commit it to git.**

### Activate the Service Account

```bash
gcloud auth activate-service-account --key-file=~/clawdbot-sa-key.json
```

### If Running on GCE/Cloud Run

No key file needed. Attach the service account directly to the instance:
```bash
gcloud compute instances set-service-account INSTANCE_NAME \
  --service-account=clawdbot-agent@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform
```

---

## 6. Gateway Wrapper Script

Create `~/.clawdbot/gateway-wrapper.sh`:

```bash
#!/bin/bash
set -euo pipefail

PROJECT_ID="YOUR_PROJECT_ID"

fetch_secret() {
  gcloud secrets versions access latest --secret="$1" --project="$PROJECT_ID" 2>/dev/null
}

# Export each secret as an environment variable
export SLACK_BOT_TOKEN=$(fetch_secret "slack-bot-token")
export SQUARE_ACCESS_TOKEN=$(fetch_secret "square-access-token")
# Add more as needed...

exec clawdbot gateway start
```

```bash
chmod +x ~/.clawdbot/gateway-wrapper.sh
```

---

## 7. Common Issues & Troubleshooting

### "Permission Denied" or "PERMISSION_DENIED"

**Cause:** Account lacks the `secretmanager.secretAccessor` role.

**Fix:**
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:you@example.com" \
  --role="roles/secretmanager.admin"
```

Wait 1-2 minutes for IAM propagation, then retry.

### "gcloud: command not found"

**Cause:** Google Cloud SDK not installed or not in PATH.

**Fix (macOS):**
```bash
# If installed via brew
source "$(brew --prefix)/share/google-cloud-sdk/path.bash.inc"

# Add to ~/.zshrc or ~/.bashrc for persistence
echo 'source "$(brew --prefix)/share/google-cloud-sdk/path.bash.inc"' >> ~/.zshrc
```

### "API not enabled"

**Cause:** Secret Manager API not enabled for the project.

**Fix:**
```bash
gcloud services enable secretmanager.googleapis.com --project=YOUR_PROJECT_ID
```

### "Auth expired" or "Token refresh error"

**Fix:**
```bash
gcloud auth login
gcloud auth application-default login
```

### "Secret not found"

**Cause:** Wrong project or wrong secret name.

**Fix:**
```bash
# List all secrets to find the correct name
gcloud secrets list --project=YOUR_PROJECT_ID

# Check which project is active
gcloud config get-value project
```

---

**Ask me anything about GCP Secret Manager setup. Every step has more detail if you need it.**

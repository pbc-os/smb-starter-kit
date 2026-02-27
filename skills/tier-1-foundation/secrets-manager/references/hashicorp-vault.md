# HashiCorp Vault — Full Setup Guide

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

### Choose Your Deployment Model

| Option | Description | Cost |
|--------|-------------|------|
| **HCP Vault (Managed)** | HashiCorp Cloud Platform hosted | Free tier (1 cluster), then ~$0.03/hr |
| **Self-Hosted (Dev)** | Run locally for development | Free (open source) |
| **Self-Hosted (Prod)** | Run on your own server | Free (open source), you manage infra |

### Option A: HCP Vault (Managed — Easiest for Production)

1. Sign up at https://portal.cloud.hashicorp.com
2. Create an organization
3. Click **Vault** → **Create cluster**
4. Select tier (Development for testing, Starter for production)
5. Choose cloud provider and region
6. Click **Create**

**What you should see:** A running Vault cluster with a public endpoint URL.

### Option B: Self-Hosted Dev Server (For Testing)

Start a dev server locally (data is in-memory, NOT persistent):
```bash
vault server -dev
```

**What you should see:**
```
==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
...
Unseal Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Root Token: hvs.xxxxxxxxxxxxxxxxxxxx

Development mode should NOT be used in production installations!
```

**Save the Root Token.** You'll need it to authenticate.

---

## 2. CLI Installation

### Install Vault CLI

**macOS (Homebrew):**
```bash
brew install hashicorp/tap/vault
```

**Linux (Ubuntu/Debian):**
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vault
```

**Linux (RHEL/Fedora):**
```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum install vault
```

### Verify Installation

```bash
vault version
```

**What you should see:** Version like `Vault v1.16.2`

---

## 3. Authentication

### Set the Vault Address

```bash
# For dev server
export VAULT_ADDR='http://127.0.0.1:8200'

# For HCP Vault (use your cluster URL)
export VAULT_ADDR='https://your-cluster.vault.xxxx.hashicorp.cloud:8200'
```

Add this to your shell profile (`~/.zshrc` or `~/.bashrc`) for persistence.

### Login with Root Token (Dev/Initial Setup)

```bash
export VAULT_TOKEN="hvs.xxxxxxxxxxxxxxxxxxxx"
# Or
vault login hvs.xxxxxxxxxxxxxxxxxxxx
```

**What you should see:**
```
Success! You are now authenticated.
Token:            hvs.xxxxxxxxxxxxxxxxxxxx
Token duration:   ∞
```

### Login with Username/Password (Production)

Enable userpass auth first:
```bash
vault auth enable userpass
vault write auth/userpass/users/clawdbot password="secure-password" policies="clawdbot-policy"
```

Then login:
```bash
vault login -method=userpass username=clawdbot password=secure-password
```

### Enable the KV Secrets Engine

The dev server enables KV v2 at `secret/` by default. For production:
```bash
vault secrets enable -path=secret kv-v2
```

### Verify Authentication

```bash
vault status
```

**What you should see:**
```
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
...
```

If "Sealed" is `true`, the vault needs to be unsealed first (see Troubleshooting).

---

## 4. Creating Your First Secret

### Create a Secret

```bash
vault kv put secret/my-first-secret value="my-super-secret-value"
```

**What you should see:**
```
===== Secret Path =====
secret/data/my-first-secret

======= Metadata =======
Key                Value
---                -----
created_time       2024-01-15T10:30:00.000Z
...
version            1
```

### Store Multiple Key-Value Pairs in One Secret

```bash
vault kv put secret/my-service api-key="abc123" api-secret="xyz789" endpoint="https://api.example.com"
```

### Read a Secret

```bash
vault kv get secret/my-first-secret
```

**What you should see:**
```
===== Secret Path =====
secret/data/my-first-secret

======= Metadata =======
...

====== Data ======
Key      Value
---      -----
value    my-super-secret-value
```

Get just the value:
```bash
vault kv get -field=value secret/my-first-secret
```

**What you should see:** `my-super-secret-value`

### List Secrets

```bash
vault kv list secret/
```

**What you should see:** A list of secret paths.

### Update a Secret

```bash
vault kv put secret/my-first-secret value="updated-value"
```

Creates a new version (previous versions are retained).

### Delete a Secret

```bash
vault kv delete secret/my-first-secret
```

Soft-deletes the latest version. To permanently destroy:
```bash
vault kv destroy -versions=1 secret/my-first-secret
```

---

## 5. Granting AI Agent Access

### Create a Policy

Create a file `clawdbot-policy.hcl`:
```hcl
# Read-only access to all secrets under secret/
path "secret/data/*" {
  capabilities = ["read", "list"]
}

path "secret/metadata/*" {
  capabilities = ["list"]
}
```

Apply the policy:
```bash
vault policy write clawdbot-read clawdbot-policy.hcl
```

### Create an AppRole (Recommended for Automation)

```bash
# Enable AppRole auth
vault auth enable approle

# Create the role
vault write auth/approle/role/clawdbot-agent \
  token_policies="clawdbot-read" \
  token_ttl=1h \
  token_max_ttl=4h

# Get the Role ID
vault read auth/approle/role/clawdbot-agent/role-id

# Generate a Secret ID
vault write -f auth/approle/role/clawdbot-agent/secret-id
```

**Save both the Role ID and Secret ID.** The agent uses them to authenticate.

### Agent Login with AppRole

```bash
vault write auth/approle/login \
  role_id="your-role-id" \
  secret_id="your-secret-id"
```

**What you should see:** A Vault token in the response. Use this token for subsequent operations.

### Create a Periodic Token (Alternative — Simpler)

```bash
vault token create -policy=clawdbot-read -period=24h -display-name="clawdbot-agent"
```

The token auto-renews as long as it's used within the period.

---

## 6. Gateway Wrapper Script

Create `~/.clawdbot/gateway-wrapper.sh`:

### Using AppRole Authentication

```bash
#!/bin/bash
set -euo pipefail

export VAULT_ADDR="http://127.0.0.1:8200"

ROLE_ID="your-role-id"
SECRET_ID="your-secret-id"

# Authenticate and get a token
VAULT_TOKEN=$(vault write -field=token auth/approle/login \
  role_id="$ROLE_ID" \
  secret_id="$SECRET_ID")
export VAULT_TOKEN

fetch_secret() {
  vault kv get -field=value "secret/$1" 2>/dev/null
}

export SLACK_BOT_TOKEN=$(fetch_secret "slack-bot-token")
export SQUARE_ACCESS_TOKEN=$(fetch_secret "square-access-token")
# Add more as needed...

exec clawdbot gateway start
```

### Using a Static Token (Simpler, Less Secure)

```bash
#!/bin/bash
set -euo pipefail

export VAULT_ADDR="http://127.0.0.1:8200"
export VAULT_TOKEN="hvs.your-periodic-token"

fetch_secret() {
  vault kv get -field=value "secret/$1" 2>/dev/null
}

export SLACK_BOT_TOKEN=$(fetch_secret "slack-bot-token")
export SQUARE_ACCESS_TOKEN=$(fetch_secret "square-access-token")

exec clawdbot gateway start
```

```bash
chmod +x ~/.clawdbot/gateway-wrapper.sh
```

---

## 7. Common Issues & Troubleshooting

### "Vault is sealed"

**Cause:** Vault server restarted and needs to be unsealed (production only — dev mode doesn't seal).

**Fix:**
```bash
# You need the unseal keys (distributed during vault init)
vault operator unseal UNSEAL_KEY_1
vault operator unseal UNSEAL_KEY_2
vault operator unseal UNSEAL_KEY_3
# Default threshold is 3 of 5 keys
```

### "vault: command not found"

**Fix (macOS):**
```bash
brew install hashicorp/tap/vault
```

### "permission denied"

**Cause:** Token lacks the required policy.

**Fix:**
```bash
# Check your token's policies
vault token lookup

# Attach the correct policy
vault token create -policy=clawdbot-read
```

### "connection refused"

**Cause:** Vault server isn't running.

**Fix:**
```bash
# Start dev server
vault server -dev

# Or check your production Vault status
systemctl status vault
```

### "token expired"

**Cause:** Token TTL has elapsed.

**Fix:**
```bash
# Renew if within max TTL
vault token renew

# Or re-authenticate
vault write auth/approle/login role_id="..." secret_id="..."
```

### "no handler for route" or "path is not supported"

**Cause:** The secrets engine isn't enabled at that path.

**Fix:**
```bash
# List enabled secrets engines
vault secrets list

# Enable KV v2
vault secrets enable -path=secret kv-v2
```

### Dev Server Data Loss

**This is expected.** The dev server stores everything in memory. When it stops, all data is gone. For persistence, deploy a production Vault with a storage backend (Raft, Consul, etc.).

---

**Ask me anything about HashiCorp Vault. It's the most powerful option — happy to help you tame it.**

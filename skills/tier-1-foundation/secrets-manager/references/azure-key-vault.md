# Azure Key Vault — Full Setup Guide

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
- An Azure account: https://azure.microsoft.com/free/
- An Azure subscription (free tier works)

### Create a Key Vault

1. Open the Azure Portal: https://portal.azure.com
2. Search "Key vaults" in the top search bar
3. Click **+ Create**
4. Fill in:
   - **Resource group:** Create new or select existing
   - **Key vault name:** e.g., `clawdbot-vault` (must be globally unique)
   - **Region:** Select your nearest region
   - **Pricing tier:** Standard
5. Click **Review + create** → **Create**

**What you should see:** "Your deployment is complete" with a "Go to resource" button.

### Note Your Vault Name

Your vault name is used in every command. Example: `clawdbot-vault`
The vault URL will be: `https://clawdbot-vault.vault.azure.net/`

---

## 2. CLI Installation

### Install Azure CLI

**macOS (Homebrew):**
```bash
brew install azure-cli
```

**Linux (Ubuntu/Debian):**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Linux (RHEL/Fedora):**
```bash
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo dnf install azure-cli
```

### Verify Installation

```bash
az version
```

**What you should see:**
```json
{
  "azure-cli": "2.58.0",
  "azure-cli-core": "2.58.0",
  ...
}
```

---

## 3. Authentication

### Interactive Login

```bash
az login
```

**What you should see:** A browser window opens. Sign in with your Microsoft account. Terminal prints your subscription details.

### Set Your Subscription (If Multiple)

```bash
# List subscriptions
az account list --output table

# Set the active one
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### Verify Authentication

```bash
az account show --output table
```

**What you should see:** Your active subscription name, ID, and state "Enabled."

### Required Permissions

Assign the Key Vault role to your account:
```bash
az role assignment create \
  --role "Key Vault Secrets Officer" \
  --assignee "you@example.com" \
  --scope "/subscriptions/YOUR_SUB_ID/resourceGroups/YOUR_RG/providers/Microsoft.KeyVault/vaults/clawdbot-vault"
```

Alternatively, configure the vault's access policy:
```bash
az keyvault set-policy \
  --name clawdbot-vault \
  --upn you@example.com \
  --secret-permissions get list set delete
```

---

## 4. Creating Your First Secret

### Create a Secret

```bash
az keyvault secret set \
  --vault-name clawdbot-vault \
  --name "my-first-secret" \
  --value "my-super-secret-value"
```

**What you should see:** JSON output with `id`, `value`, and `attributes`.

> **Note:** Azure Key Vault secret names can contain alphanumerics and hyphens only. No underscores.

### Read a Secret

```bash
az keyvault secret show \
  --vault-name clawdbot-vault \
  --name "my-first-secret" \
  --query value \
  -o tsv
```

**What you should see:** `my-super-secret-value`

### Update a Secret

```bash
az keyvault secret set \
  --vault-name clawdbot-vault \
  --name "my-first-secret" \
  --value "updated-value"
```

**What you should see:** JSON with a new version ID.

### List All Secrets

```bash
az keyvault secret list --vault-name clawdbot-vault --query "[].name" -o tsv
```

**What you should see:** A list of secret names, one per line.

### Delete a Secret

```bash
az keyvault secret delete --vault-name clawdbot-vault --name "my-first-secret"
```

**What you should see:** JSON confirming the deletion schedule.

> **Note:** Azure uses soft-delete by default (90-day retention). To permanently purge:
```bash
az keyvault secret purge --vault-name clawdbot-vault --name "my-first-secret"
```

---

## 5. Granting AI Agent Access

### Create a Service Principal

```bash
az ad sp create-for-rbac \
  --name "clawdbot-agent" \
  --role "Key Vault Secrets User" \
  --scopes "/subscriptions/YOUR_SUB_ID/resourceGroups/YOUR_RG/providers/Microsoft.KeyVault/vaults/clawdbot-vault"
```

**What you should see:**
```json
{
  "appId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "displayName": "clawdbot-agent",
  "password": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "tenant": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**Save all three values.** The password is shown only once.

### Login as Service Principal (For Automation)

```bash
az login --service-principal \
  --username "APP_ID" \
  --password "PASSWORD" \
  --tenant "TENANT_ID"
```

### If Running on an Azure VM

Use Managed Identity instead (no passwords needed):
1. Enable system-assigned managed identity on the VM
2. Grant the managed identity access to the Key Vault:
```bash
az keyvault set-policy \
  --name clawdbot-vault \
  --object-id "VM_MANAGED_IDENTITY_OBJECT_ID" \
  --secret-permissions get list
```

---

## 6. Gateway Wrapper Script

Create `~/.clawdbot/gateway-wrapper.sh`:

```bash
#!/bin/bash
set -euo pipefail

VAULT_NAME="clawdbot-vault"

fetch_secret() {
  az keyvault secret show \
    --vault-name "$VAULT_NAME" \
    --name "$1" \
    --query value \
    -o tsv 2>/dev/null
}

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

### "Forbidden" or "Access denied"

**Cause:** Account/service principal lacks vault permissions.

**Fix (RBAC):**
```bash
az role assignment create \
  --role "Key Vault Secrets Officer" \
  --assignee "you@example.com" \
  --scope "/subscriptions/YOUR_SUB_ID/resourceGroups/YOUR_RG/providers/Microsoft.KeyVault/vaults/clawdbot-vault"
```

**Fix (Access Policy):**
```bash
az keyvault set-policy \
  --name clawdbot-vault \
  --upn you@example.com \
  --secret-permissions get list set delete
```

### "az: command not found"

**Fix (macOS):**
```bash
brew install azure-cli
```

### "The subscription could not be found"

**Fix:**
```bash
az account list --output table
az account set --subscription "CORRECT_SUBSCRIPTION_ID"
```

### "SecretNotFound"

**Cause:** Wrong vault name, secret name, or the secret was soft-deleted.

**Fix:**
```bash
# List existing secrets
az keyvault secret list --vault-name clawdbot-vault --query "[].name" -o tsv

# Check soft-deleted secrets
az keyvault secret list-deleted --vault-name clawdbot-vault
```

### "Vault is in a deleted state"

**Fix:**
```bash
# Recover a deleted vault
az keyvault recover --name clawdbot-vault
```

---

**Ask me anything about Azure Key Vault. Happy to dig deeper into any step.**

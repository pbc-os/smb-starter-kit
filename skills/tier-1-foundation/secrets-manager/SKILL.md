---
name: secrets-manager
description: Set up and configure cloud secrets management for your AI agent. Use when onboarding a new user, setting up API key storage, configuring secure credential management, or when someone asks about storing secrets, API keys, tokens, or passwords securely. Guides users through platform selection (GCP, AWS, Azure, 1Password, Doppler, HashiCorp Vault), account setup, CLI configuration, and integration with Clawdbot's gateway.
---

# Secrets Manager — Give Your AI Agent Keys to the Kingdom

## 1. The Vision: Why This Changes Everything

Right now you're chatting with an AI. That's 1% of what's possible.

Without secrets management, your AI agent is a brain in a jar — it can think, but it can't *do* anything:

```
┌─────────────────────────────────────────────────────┐
│                  WITHOUT SECRETS                     │
│                                                      │
│   You ──── text ────► [  AI Agent  ] ──── text ───► You
│                        (brain in a jar)              │
│                                                      │
│   ❌ Can't read email        ❌ Can't run ads        │
│   ❌ Can't check inventory   ❌ Can't pull analytics │
│   ❌ Can't manage orders     ❌ Can't post content   │
│   ❌ Can't send invoices     ❌ Can't automate anything│
│                                                      │
│   It's a walkie-talkie. You talk. It talks back.     │
│   That's it.                                         │
└─────────────────────────────────────────────────────┘
```

Now look what happens when you give the agent secure access to your tools:

```
┌──────────────────────────────────────────────────────────────────┐
│                     WITH SECRETS MANAGEMENT                       │
│                                                                   │
│                        ┌──────────┐                               │
│              ┌────────►│  Gmail   │  Read/send email              │
│              │         └──────────┘                               │
│              │         ┌──────────┐                               │
│              ├────────►│  Square  │  POS, inventory, orders       │
│              │         └──────────┘                               │
│              │         ┌──────────┐                               │
│   You ──►[ AI AGENT ]─┼────────►│ Google Ads│  Run campaigns     │
│              │         └──────────┘                               │
│              │         ┌──────────┐                               │
│              ├────────►│Mailchimp │  Email marketing              │
│              │         └──────────┘                               │
│              │         ┌──────────┐                               │
│              ├────────►│QuickBooks│  Accounting                   │
│              │         └──────────┘                               │
│              │         ┌──────────┐                               │
│              └────────►│ Walmart  │  Ecommerce                   │
│                        └──────────┘                               │
│                                                                   │
│   Every API key = a new superpower.                               │
│   Secrets management = the secure vault that holds them all.      │
└──────────────────────────────────────────────────────────────────┘
```

Here's how secrets flow from vault to action:

```
┌─────────────┐    startup    ┌──────────────┐    env vars    ┌──────────┐    API calls    ┌──────────┐
│ Cloud Vault  │─────────────►│   Gateway    │──────────────►│ AI Agent │───────────────►│ Services │
│ (encrypted)  │  fetch keys  │  Wrapper.sh  │  in memory    │          │  authenticated  │ (Gmail,  │
│              │              │              │  (not on disk) │          │                 │  Square, │
└─────────────┘              └──────────────┘               └──────────┘                 │  etc.)   │
                                                                                          └──────────┘
     SECURE                     SECURE                        SECURE                      AUTHORIZED
  at rest, encrypted        fetched once at boot          never written to disk          full API access
```

**Think of it this way:** Secrets management gives your AI agent keys to the building instead of just a walkie-talkie. Every integration you'll ever add — email, POS, ads, ecommerce — starts here.

This is the foundation. Set it up once, and every future integration becomes a 5-minute job instead of an hour of fumbling with `.env` files and hardcoded keys.

---

## 2. Platform Selection

**Ask the user:** "Which secrets platform do you want to use? Here are your options:"

| Platform | Best For | Pricing | Complexity |
|----------|----------|---------|------------|
| **GCP Secret Manager** | Google ecosystem, cost-effective | 6 active secrets free, ~$0.06/secret/mo | Medium |
| **AWS Secrets Manager** | AWS ecosystem, enterprise | $0.40/secret/month | Medium |
| **Azure Key Vault** | Microsoft/Azure ecosystem | $0.03/10k operations | Medium |
| **1Password Connect** | Teams already on 1Password | Business plan required | Low |
| **Doppler** | Developer-focused, multi-env | Free tier available | Low |
| **HashiCorp Vault** | Self-hosted, max control | Free (self-hosted) | High |

### Why each platform:

- **GCP Secret Manager** — Best bang for buck. Generous free tier (6 secrets, 10k access ops/mo). Deeply integrated with Google services. If you use Gmail, Google Ads, or BigQuery, this is the natural choice.
- **AWS Secrets Manager** — Industry standard for enterprise. Pairs perfectly with Lambda, ECS, and the broader AWS ecosystem. More expensive per-secret but rock-solid.
- **Azure Key Vault** — Natural fit for Microsoft shops. Strong RBAC, integrates with Azure AD. Good if you're already running Azure resources.
- **1Password Connect** — Lowest friction if your team already pays for 1Password Business. No new accounts, no new CLI to learn. Just extend what you have.
- **Doppler** — Built specifically for developer secrets. Best DX of any option. Syncs across environments (dev/staging/prod). Free tier covers small projects.
- **HashiCorp Vault** — Maximum control. Self-hosted, open source, infinitely configurable. But also the most complex to set up and maintain. Choose this if you have strong DevOps skills or compliance requirements.

**Not sure?** Ask me to help you decide. Tell me what cloud services you already use, your team size, and your budget. I'll recommend one.

For a detailed side-by-side comparison, load `references/platform-comparison.md`.

**After the user selects a platform, load the corresponding reference file:**

| Selection | Reference File |
|-----------|---------------|
| GCP | `references/gcp-secret-manager.md` |
| AWS | `references/aws-secrets-manager.md` |
| Azure | `references/azure-key-vault.md` |
| 1Password | `references/1password-connect.md` |
| Doppler | `references/doppler.md` |
| HashiCorp Vault | `references/hashicorp-vault.md` |

---

## 3. Setup — Walk Through the Reference

Read the selected platform's reference file and walk the user through it step by step.

**Guidelines for the agent:**
- Go one step at a time. Don't dump the whole guide at once.
- After each command, tell the user what they should see.
- Encourage questions: "Ask me anything about this step."
- If a step fails, troubleshoot before moving on.
- Celebrate small wins: "Secret created! You're almost there."

---

## 4. Integration with Clawdbot

Once the platform is configured, wire secrets into the Clawdbot gateway.

### Step 1: Create the Gateway Wrapper Script

Create `~/.clawdbot/gateway-wrapper.sh`:

```bash
#!/bin/bash
# gateway-wrapper.sh — Fetch secrets at startup, export as env vars
# This script wraps the gateway start command.
# Secrets are held in memory only — never written to disk.

set -euo pipefail

# ------------------------------------------------------------------
# Helper: fetch a single secret (replace with your platform's CLI)
# ------------------------------------------------------------------
# GCP:        gcloud secrets versions access latest --secret="$1" --project=YOUR_PROJECT
# AWS:        aws secretsmanager get-secret-value --secret-id "$1" --query SecretString --output text
# Azure:      az keyvault secret show --vault-name YOUR_VAULT --name "$1" --query value -o tsv
# 1Password:  op read "op://vault/$1/credential"
# Doppler:    doppler secrets get "$1" --plain
# Vault:      vault kv get -field=value secret/"$1"
# ------------------------------------------------------------------
fetch_secret() {
  # Uncomment and customize ONE of the lines above
  echo "REPLACE_ME"
}

# ------------------------------------------------------------------
# Export secrets as environment variables
# ------------------------------------------------------------------
export MY_API_KEY=$(fetch_secret "my-api-key")
export ANOTHER_SECRET=$(fetch_secret "another-secret")
# Add more as needed...

# ------------------------------------------------------------------
# Start the gateway
# ------------------------------------------------------------------
exec clawdbot gateway start
```

```bash
chmod +x ~/.clawdbot/gateway-wrapper.sh
```

### Step 2: Reference Secrets in clawdbot.json

Use `${VAR_NAME}` substitution in your gateway config:

```json
{
  "integrations": {
    "myService": {
      "apiKey": "${MY_API_KEY}"
    }
  }
}
```

The gateway resolves `${VAR_NAME}` from environment variables at startup.

### Step 3: Restart the Gateway

```bash
# Stop the current gateway
clawdbot gateway stop

# Start via wrapper (fetches fresh secrets)
~/.clawdbot/gateway-wrapper.sh
```

**What you should see:** Gateway starts normally, logs show no errors.

### Step 4: Verify the Integration

```bash
# Quick check — can the gateway see the env var?
clawdbot gateway status
```

If the gateway is running and your integrations work, secrets are flowing correctly.

---

## 5. Verification

Run the verification script to confirm everything is wired up:

```bash
bash scripts/verify_access.sh
```

**What you should see:** Green checkmarks for CLI detection, authentication, and secret access.

If any check fails, the script prints exactly what went wrong and how to fix it.

### Optional: Full Round-Trip Test

Run the test script to create, read, and delete a test secret:

```bash
bash scripts/test_secret.sh
```

This creates `clawdbot-test-secret`, reads it back, verifies the value, and cleans up after itself.

---

## 6. What's Next

You now have a secure secrets pipeline. Here's what to do with it:

1. **Add your first real secret** — Start with whatever API key you use most (email, POS, analytics)
2. **Update the wrapper script** — Add a `fetch_secret` + `export` line for each new key
3. **Restart the gateway** — Picks up new secrets automatically
4. **Repeat** — Every new integration is now: get API key → store in vault → add to wrapper → restart

**Every integration you add from here is a 5-minute job.** The hard part is done.

---

## Quick Reference

### Adding a New Secret (Any Platform)

```
1. Store the secret:    <platform-cli> create-secret "secret-name" "secret-value"
2. Update wrapper:      export SECRET_NAME=$(fetch_secret "secret-name")
3. Update config:       Add ${SECRET_NAME} to clawdbot.json if needed
4. Restart gateway:     clawdbot gateway stop && ~/.clawdbot/gateway-wrapper.sh
```

### Security Best Practices

- **Never** store secrets in `.env` files, code, or config files
- **Never** commit secrets to git
- **Always** use the vault as single source of truth
- **Rotate** secrets periodically (quarterly at minimum)
- **Audit** access logs when your platform supports it
- Use **service accounts** with minimum required permissions

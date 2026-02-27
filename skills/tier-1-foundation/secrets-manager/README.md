# Secrets Manager — Give Your AI Agent Keys to the Kingdom

**Without secure secrets, your AI agent is a brain in a jar.**

## What This Is

A guided setup skill that walks you through configuring secure API key storage. Supports:
- Google Cloud Secret Manager (GCP)
- AWS Secrets Manager
- Azure Key Vault
- 1Password Connect
- Doppler
- HashiCorp Vault

## Why This Matters

```
WITHOUT SECRETS                    WITH SECRETS
┌────────────────┐                ┌────────────────┐
│   AI Agent     │                │   AI Agent     │──► Gmail
│ (brain in jar) │                │                │──► Square
│                │                │                │──► Google Ads
│ ❌ Can't read  │                │                │──► QuickBooks
│    email       │                │                │──► Mailchimp
│ ❌ Can't check │                │                │──► Everything
│    inventory   │                │                │
└────────────────┘                └────────────────┘
   Just talks                     Actually DOES things
```

Every API integration your agent will ever use starts here.

## Setup Time

30-60 minutes for first-time setup. After that, adding new secrets takes 2 minutes.

## What You'll Do

1. **Choose a secrets platform** (we help you pick based on your existing stack)
2. **Install the CLI** and authenticate
3. **Create your first secret** (walk-through with verification)
4. **Wire secrets into your agent** (gateway wrapper script)
5. **Test the integration**

## Files

```
secrets-manager/
├── SKILL.md            # Full walkthrough (this is what your agent reads)
├── README.md           # This file
├── references/         # Platform-specific guides
│   ├── gcp-secret-manager.md
│   ├── aws-secrets-manager.md
│   ├── azure-key-vault.md
│   ├── 1password-connect.md
│   ├── doppler.md
│   ├── hashicorp-vault.md
│   └── platform-comparison.md
└── scripts/
    ├── verify_access.sh    # Verify CLI + auth is working
    └── test_secret.sh      # Create/read/delete test secret
```

## Quick Start

Tell your AI agent:
> "I need to set up secrets management. Read the secrets-manager skill and guide me through it."

The SKILL.md will walk both of you through the entire process.

## Platform Recommendations

| Your Stack | Recommended Platform |
|------------|---------------------|
| Google Workspace / Gmail / Google Ads | GCP Secret Manager |
| AWS-heavy infrastructure | AWS Secrets Manager |
| Microsoft / Azure AD | Azure Key Vault |
| Already paying for 1Password | 1Password Connect |
| Multi-environment deploys | Doppler |
| Self-hosted / max control | HashiCorp Vault |

## Security Best Practices

- **Never** store secrets in `.env` files, code, or git
- **Always** use the vault as single source of truth
- **Rotate** secrets periodically (quarterly minimum)
- **Audit** access logs when available
- Use **service accounts** with minimum permissions

---

*This is Tier 1 for a reason. Everything else depends on this.*

# Secrets Management Platform Comparison

## Table of Contents
- [Quick Summary](#quick-summary)
- [Pricing Breakdown](#pricing-breakdown)
- [Feature Comparison](#feature-comparison)
- [Free Tier Details](#free-tier-details)
- [Best Use Cases](#best-use-cases)
- [Limitations](#limitations)
- [Recommendation Matrix](#recommendation-matrix)

---

## Quick Summary

| Platform | Ease of Setup | CLI Quality | Price (10 secrets/mo) | Price (50 secrets/mo) | Price (100 secrets/mo) |
|----------|:------------:|:-----------:|----------------------:|----------------------:|-----------------------:|
| **GCP Secret Manager** | ⭐⭐⭐ | ⭐⭐⭐⭐ | Free | $2.64 | $5.64 |
| **AWS Secrets Manager** | ⭐⭐⭐ | ⭐⭐⭐⭐ | $4.00 | $20.00 | $40.00 |
| **Azure Key Vault** | ⭐⭐⭐ | ⭐⭐⭐ | ~$0.03 | ~$0.15 | ~$0.30 |
| **1Password Connect** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $7.99/user/mo* | $7.99/user/mo* | $7.99/user/mo* |
| **Doppler** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Free | Free | Free |
| **HashiCorp Vault** | ⭐⭐ | ⭐⭐⭐⭐ | Free (self-hosted) | Free (self-hosted) | Free (self-hosted) |

\* 1Password pricing is per-user, not per-secret. Secrets are unlimited on Business plan.

---

## Pricing Breakdown

### GCP Secret Manager
- **6 active secret versions:** Free
- **Per active secret version:** $0.06/month
- **Per 10,000 access operations:** $0.03
- **10 secrets:** Free (under free tier)
- **50 secrets:** 44 × $0.06 = $2.64/mo + negligible access costs
- **100 secrets:** 94 × $0.06 = $5.64/mo + negligible access costs
- **Billing:** Per project, pay-as-you-go

### AWS Secrets Manager
- **Per secret:** $0.40/month
- **Per 10,000 API calls:** $0.05
- **10 secrets:** $4.00/mo
- **50 secrets:** $20.00/mo
- **100 secrets:** $40.00/mo
- **Billing:** Per region, pay-as-you-go
- **Note:** No free tier for Secrets Manager itself

### Azure Key Vault (Standard Tier)
- **Secret operations:** $0.03/10,000 transactions
- **No per-secret charge** — you pay for operations, not storage
- **10 secrets:** ~$0.03/mo (assuming ~10k reads)
- **50 secrets:** ~$0.15/mo
- **100 secrets:** ~$0.30/mo
- **Billing:** Per vault, pay-as-you-go

### 1Password
- **Teams:** $3.99/user/month (limited integrations)
- **Business:** $7.99/user/month (required for Connect Server/Service Accounts)
- **Secrets per se:** Unlimited at any plan
- **10/50/100 secrets:** Same price — per-user, not per-secret
- **Billing:** Monthly or annual per user

### Doppler
- **Community (Free):** Unlimited secrets, 5 projects, unlimited members
- **Team:** $6/seat/month (audit logs, SAML, webhooks)
- **Enterprise:** Custom pricing
- **10/50/100 secrets:** Free on Community plan
- **Billing:** Per seat, monthly

### HashiCorp Vault
- **Self-Hosted (OSS):** Free forever, you manage infrastructure
- **HCP Vault (Managed):**
  - Development: Free (1 small cluster)
  - Starter: ~$0.03/hr (~$22/mo)
  - Standard: ~$0.09/hr (~$65/mo)
  - Plus: ~$0.22/hr (~$160/mo)
- **10/50/100 secrets:** Free if self-hosted

---

## Feature Comparison

| Feature | GCP | AWS | Azure | 1Password | Doppler | Vault |
|---------|:---:|:---:|:-----:|:---------:|:-------:|:-----:|
| Secret versioning | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Auto-rotation | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Audit logging | ✅ | ✅ | ✅ | ✅ | ✅* | ✅ |
| Multi-environment | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Team sharing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Browser UI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Dynamic secrets | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Encryption as a service | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Kubernetes native | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Webhook on change | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Secret references | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |

\* Audit logs on Doppler Team plan and above.

---

## Free Tier Details

### GCP Secret Manager
- 6 active secret versions
- 10,000 access operations/month
- No time limit

### AWS Secrets Manager
- **No free tier** for Secrets Manager
- AWS Free Tier covers other services but not this one
- 30-day trial with first secret when you create an account

### Azure Key Vault
- **No per-secret charge** (you only pay for operations)
- 20,000 vault operations included in free Azure account
- Azure free account: $200 credit for 30 days

### 1Password
- 14-day free trial on Business plan
- No permanent free tier for business features

### Doppler
- **Community plan is permanently free**
- 5 projects, unlimited secrets, unlimited team members
- Generous for small teams and solo developers

### HashiCorp Vault
- **Open source is permanently free** (self-hosted)
- HCP Vault Development tier: 1 free cluster (limited resources)

---

## Best Use Cases

### Choose GCP Secret Manager when:
- You already use Google Cloud services (GKE, Cloud Run, BigQuery)
- You want the best price-to-feature ratio
- You need integration with Google's IAM system
- You're cost-conscious but want enterprise features

### Choose AWS Secrets Manager when:
- You're all-in on AWS (Lambda, ECS, EC2)
- You need automatic secret rotation (built-in for RDS, Redshift, DocumentDB)
- Enterprise compliance requirements (SOC2, HIPAA, PCI)
- You need cross-region replication

### Choose Azure Key Vault when:
- You use Microsoft/Azure ecosystem
- You need the cheapest per-operation pricing
- Azure AD integration matters
- You also need key management and certificate management

### Choose 1Password Connect when:
- Your team already uses 1Password
- You want minimal new tooling
- Non-technical team members need to manage secrets
- You value the 1Password UI/UX

### Choose Doppler when:
- You're a developer or small team
- You need multi-environment management (dev/staging/prod)
- You want the fastest setup experience
- You don't want to manage cloud infrastructure
- You want the best CLI experience

### Choose HashiCorp Vault when:
- You need dynamic secrets (auto-generated, short-lived database credentials)
- Compliance requires self-hosted secrets management
- You need encryption as a service
- You have DevOps expertise to manage it
- You want maximum flexibility and control

---

## Limitations

### GCP Secret Manager
- No native multi-environment support (use separate projects or naming conventions)
- No built-in sync to local `.env` files
- Requires Google Cloud account even for non-GCP workloads

### AWS Secrets Manager
- Most expensive per-secret pricing
- No free tier
- Secret names can't be reused for 7+ days after deletion

### Azure Key Vault
- Secret names limited to alphanumerics and hyphens (no underscores)
- Soft-delete is mandatory (90-day retention)
- Purge protection can prevent cleanup for up to 90 days

### 1Password
- Requires Business plan ($7.99/user/mo) for automation features
- No secret versioning (overwrite replaces the value)
- CLI session tokens expire (30 minutes default)
- Designed for human secrets management first, automation second

### Doppler
- Audit logs only on paid plans
- No secret rotation automation
- Newer platform — smaller ecosystem than cloud providers
- Limited compliance certifications compared to AWS/GCP/Azure

### HashiCorp Vault
- Highest setup complexity by far
- Requires unsealing after server restart (production)
- Dev server loses all data on restart
- Significant operational overhead for self-hosting
- HCP managed offering is expensive at scale

---

## Recommendation Matrix

| Scenario | Recommended | Runner-Up |
|----------|------------|-----------|
| Solo developer, budget-conscious | Doppler | GCP |
| Small team (<10), already on Google Cloud | GCP | Doppler |
| Enterprise, AWS-heavy | AWS | Vault |
| Microsoft shop | Azure | Doppler |
| Team already on 1Password Business | 1Password | Doppler |
| Need multi-environment (dev/staging/prod) | Doppler | Vault |
| Maximum security/compliance | Vault | AWS |
| Fastest possible setup | Doppler | 1Password |
| Lowest ongoing cost (high secret count) | GCP or Azure | Doppler |
| Kubernetes-native workloads | Vault | GCP |

---

**Still not sure? Tell me about your setup — existing cloud provider, team size, budget, and compliance needs — and I'll give you a specific recommendation.**

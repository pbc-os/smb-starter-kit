# What a Secure Data Lake Actually Costs

Short version: at small-business scale, a secured BigQuery data lake usually runs **between $0 and a few dollars a month** — and a lot of businesses stay inside the free tier indefinitely. The lake itself is cheap. What it gives back is the part that used to require a data team.

> Prices below are Google Cloud's published US list prices as of writing. Always confirm current numbers at [cloud.google.com/bigquery/pricing](https://cloud.google.com/bigquery/pricing) — cloud pricing changes. The point isn't the exact cents; it's the order of magnitude.

## The components

| Service | What you pay for | Free tier | List price after free |
|---|---|---|---|
| **BigQuery storage** | Data sitting in your tables | First **10 GB/month free** | ~$0.02/GB active, ~$0.01/GB long-term (90+ days untouched) |
| **BigQuery queries** | Data *scanned* by queries (on-demand) | First **1 TiB/month free** | ~$6.25 per TiB scanned |
| **Secret Manager** | Active secret versions + access | **6 versions free**, 10k access ops free | ~$0.06/version/mo, ~$0.03/10k accesses |
| **Cloud Logging (audit)** | Log storage | **50 GiB/project/month free** | ~$0.50/GiB after |
| **Workload Identity** | Keyless auth | **Free** | Free |
| **Budget alerts** | The guardrail itself | **Free** | Free |

## A realistic SMB month

A two-location shop with several years of POS history, a dozen connected sources, and an agent querying it daily:

| Line item | Typical usage | Cost |
|---|---|---|
| Storage | ~5 GB of business data | **$0** (under 10 GB free) |
| Queries | ~50 GB scanned/month (agent + dashboards) | **$0** (under 1 TiB free) |
| Secrets | ~15 source credentials | ~**$0.60** |
| Audit logs | well under 50 GiB | **$0** |
| **Total** | | **≈ $0–$3 / month** |

Even a data-heavy shop that blows past the free tiers — tens of GB stored, queries scanning a few TiB a month — is generally looking at **single-digit to low-double-digit dollars per month.** That's the cost of *owning your entire data picture*, in one place, queryable in plain English.

## Keeping it cheap (and the guardrail)

The one way to get a surprising BigQuery bill is an inefficient query scanning huge tables in a loop. The scaffold and standard prevent it:

- **Partition and cluster** big tables by date — queries then scan only the days they need, not the whole history.
- **`SELECT` the columns you need**, not `SELECT *` — you're billed on bytes *scanned*.
- **Read the curated `marts` layer**, which is already aggregated and small, instead of raw.
- **The budget alert** ([hardening.md §9](./hardening.md)) emails you the moment spend crosses a threshold you set — so a mistake is a $4 surprise, not a $400 one.
- Optional: set a **per-query bytes-billed cap** so no single query can scan more than you allow.

## The honest framing

This isn't about a business being unable to afford software. It's that the *labor* of unifying data — the data engineer, the warehouse, the pipelines — was the expensive part, and it was priced for companies with a data team. The cloud bill for the storage and compute was never the barrier.

What changed is the labor. An owner with an agent can now stand up and run what used to take that team — and the infrastructure underneath it costs about a coffee a month. Consolidating overlapping tools you're already paying for is a nice bonus; the real win is finally being able to *ask your whole business a question and get an answer.*

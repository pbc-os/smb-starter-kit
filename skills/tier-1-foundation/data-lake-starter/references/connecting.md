# Connecting Your Sources — The Manual Boundary

You built the lake. It's secure, and it's empty. Filling it is your job — and this guide is how to do it safely.

## Why there are no connectors here

This kit deliberately ships **zero pre-baked connectors.** That's not a gap; it's the security model.

Connecting a source means handing over a credential — your Square keys, your Stripe secret, your QuickBooks token. **Every one of those is a trust decision that only you, the owner, should make.** A skill that "just connects Square for you" would have to take your Square keys and decide, on your behalf, what to pull and where it goes. The secure pattern is the exact opposite: *you* mint each credential at the smallest possible scope, *you* put it in your vault, and *you* decide what gets ingested.

So this last step stays manual on purpose. It's the line between "convenient" and "secure," and it's the one place convenience isn't worth it.

The good news: once the lake exists, each connection is a small, repeatable job — and your agent can write most of it *with* you.

---

## The secure connection pattern (every source)

```
1. MINT      Create a credential in the source app.
             → Least scope. Read-only wherever the source allows it.
             → Name it so you know it's for the lake (e.g. "data-lake-readonly").

2. STORE     Put it in Secret Manager — never in code, never in .env, never in git.
             → gcloud secrets create square-access-token --data-file=-
             → See the secrets-manager skill.

3. GRANT     Give ONLY the ingest service account access to ONLY that secret.
             → gcloud secrets add-iam-policy-binding square-access-token \
                 --member="serviceAccount:lake-ingest@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
                 --role="roles/secretmanager.secretAccessor"

4. LAND      Write a small job that pulls from the source and writes into lake_raw.
             → Nothing fancy: call the API, write rows to a raw table. One source, one table.
             → It writes to raw ONLY. Transforms (raw→clean→marts) come later.

5. SCHEDULE  Run it on a cadence (Cloud Scheduler, cron, or a Cloud Run job).
             → Start daily. Tighten to hourly/near-real-time only where it earns its keep.
```

Your agent can scaffold step 4 for any source with a documented API — just be explicit that it writes to `lake_raw` and reads its credential from Secret Manager (never hardcoded).

---

## Per-source checklist (copy for each one)

```
Source: ______________________
[ ] Credential minted at LEAST scope (read-only if possible)
[ ] Scope/permissions written down (what can this key actually do?)
[ ] Stored in Secret Manager as: ______________________
[ ] Only lake-ingest granted secretAccessor on it
[ ] Ingestion job writes to lake_raw.______________________ only
[ ] Scheduled: daily / hourly / other: ____________
[ ] Rotation reminder set (quarterly)
[ ] Verified: rows landing in raw, nothing written outside raw
```

---

## Common SMB sources — what to mint

Guidance only — you create these yourself, in each tool's own settings. Always prefer read-only.

| Source | Credential type | Scope to request | Notes |
|---|---|---|---|
| **Square** | OAuth token / PAT | `ORDERS_READ`, `PAYMENTS_READ`, `ITEMS_READ`, `CUSTOMERS_READ` | Read-only. One token can cover multiple locations. |
| **Stripe** | Restricted API key | Read access to charges, payouts, customers | Use a **restricted** key, not the secret key. |
| **QuickBooks Online** | OAuth 2.0 | Accounting read | Token refresh required; store refresh token in the vault. |
| **Google Ads** | OAuth + developer token | Read | Reuses Google auth; the [google-ads](../../../tier-4-growth/google-ads/) skill covers the credential setup. |
| **Mailchimp** | API key | Read audiences/campaigns | Region is encoded in the key suffix. |
| **Google Business Profile / Reviews** | OAuth | Read | Reviews + search insights. |

> The point isn't this table — it's the *pattern*. Any source with an API connects the same five ways. Pick the one source you'd most like to ask questions about (usually your POS), connect it end-to-end, see rows land in `raw`, then repeat.

---

## What happens after data lands

Once `raw` has data:
1. **Transform** it (raw → clean → marts) with the `lake-transform` identity — normalize, dedupe, build the curated tables and views your agent will actually read.
2. **Catalog** it with the [semantic-layer-audit](../../semantic-layer-audit/) skill so your agent always knows what's queryable and how to use it.
3. **Use** it — every skill in Tiers 2–5 now reads from the same lake.

You're no longer renting someone else's view of your business. You own the whole picture.

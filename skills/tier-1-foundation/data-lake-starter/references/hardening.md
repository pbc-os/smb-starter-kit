# SMB Data Lake Hardening Standard — v1

A small business's data lake holds everything: customer info, sales, finances. It deserves enterprise-grade security — but enterprise-grade *complexity* is a non-starter for a shop owner. This standard is the middle path: **ten controls that a small business can actually hold, every one of them enforced by the [data-lake-starter](../SKILL.md) scaffold.**

The `data-lake-starter` skill (and its Terraform) implements all ten. This doc explains *why* each exists and *how to verify* it — so "secure" is something you can point at, not just hope for.

---

### 1. One project, one purpose
Isolate the lake in its **own dedicated GCP project**. Don't share it with your website, a side app, or test work.

- **Why:** Blast radius. If anything else in a shared project is compromised or misconfigured, your customer data shouldn't be in the same room.
- **Verify:** `gcloud projects describe "$GCP_PROJECT_ID"` — and that nothing unrelated runs in it.

### 2. Least-privilege service accounts
Three identities, each scoped to exactly what it does: **ingest** (write `raw` only), **transform** (raw→clean→marts), **agent** (read `marts` only). Never grant `roles/owner` or `roles/editor` to a service account.

- **Why:** No single leaked identity can do everything. The identity your AI agent uses is read-only and can't see raw PII.
- **Verify:** `gcloud projects get-iam-policy "$GCP_PROJECT_ID" --flatten=bindings --filter="bindings.members:lake-"` — confirm no `owner`/`editor` on any `lake-*` SA.

### 3. No downloadable keys — use Workload Identity
Automation (GitHub Actions, Cloud Run) authenticates via **Workload Identity Federation**, which mints short-lived tokens. Do **not** create or download `.json` service-account keys.

- **Why:** A downloaded key is a permanent password sitting in a file, waiting to leak. WIF tokens expire in minutes and can't be exfiltrated.
- **Verify:** `gcloud iam service-accounts keys list --iam-account=lake-ingest@$GCP_PROJECT_ID.iam.gserviceaccount.com` shows only the Google-managed key (no user-managed keys). Bonus: enforce the `iam.disableServiceAccountKeyCreation` org policy.

### 4. Read-only consumption via authorized views
Agents and dashboards read **only the `marts` layer**, through **authorized views** that query `raw`/`clean` on their behalf. The consumer identity is never granted direct access to raw data.

- **Why:** Your agent can get *answers* (aggregates, curated views) without ever being able to read raw customer rows. PII stays behind a wall.
- **Verify:** the `lake-agent` SA has `READER` on `lake_marts` and **nothing** on `lake_raw`. Query a marts view as the agent SA — it works. Query `lake_raw` directly as the agent SA — it's denied.

### 5. Secrets in a vault — never in code
Every credential lives in **Secret Manager**. Never in `.env` files, never in code, never committed to git. At runtime, secrets are injected as environment variables and held in memory — **the agent never sees a raw secret value on disk.**

- **Why:** Code leaks, laptops get lost, repos go public by accident. A vault is revocable and audited; a hardcoded key is forever.
- **Verify:** `gcloud secrets list` shows your credentials; `git grep -iE "api[_-]?key|secret|token|password"` in any repo returns no real values. See the [secrets-manager](../../secrets-manager/) skill.

### 6. Layered datasets, one-way flow
Data moves **raw → clean → marts** and never backward. Consumers read the end of the pipeline, not the start.

- **Why:** Separation of concerns and of access. Messy/PII-laden landing data is quarantined; only curated, intentional data reaches the things that read it.
- **Verify:** the four datasets exist (`raw`, `clean`, `marts`, `archive`) and only `transform` writes across them.

### 7. Audit logging on
**BigQuery Data Access audit logs** are enabled, so every read and write is recorded.

- **Why:** You can always answer "who queried the customer table, and when?" Detection and accountability both require a trail.
- **Verify:** `gcloud projects get-iam-policy "$GCP_PROJECT_ID"` shows an `auditConfigs` block for `bigquery.googleapis.com` with `DATA_READ`/`DATA_WRITE`. Query logs in Cloud Logging under `protoPayload.serviceName="bigquery.googleapis.com"`.

### 8. Rotate credentials
Rotate every source credential **at least quarterly**, and immediately if anyone with access leaves. WIF tokens rotate themselves (they're short-lived by design).

- **Why:** Limits the useful lifetime of any credential that quietly leaked.
- **Verify:** keep a rotation date per secret (Secret Manager labels work well); review quarterly.

### 9. Budget guardrail
A **billing budget with an email alert** is attached, so cost can never run away unnoticed.

- **Why:** A single accidental full-table scan in a loop is the classic "surprise cloud bill." An alert turns a $400 mistake into a $4 one.
- **Verify:** `gcloud billing budgets list --billing-account=<ID>` shows a budget with a threshold rule. See [cost.md](./cost.md).

### 10. The manual boundary
**No pre-baked connector ever ingests on your behalf.** You mint each source credential yourself, at the smallest scope, and decide what gets ingested. Connecting sources is a deliberate human act — not an automated one.

- **Why:** Every credential is a trust decision. Automating that decision away is the one convenience that isn't worth it. Keeping it manual is what makes "secure" true rather than aspirational. See [connecting.md](./connecting.md).
- **Verify:** every credential in your vault was created by a human, at a documented scope, with a reason.

---

## The 60-second checklist

- [ ] Lake lives in its **own** GCP project
- [ ] Three **least-privilege** SAs (ingest / transform / agent) — no owner/editor
- [ ] **No** user-managed service-account keys (WIF for automation)
- [ ] Agent SA reads **`marts` only**, via authorized views — never `raw`
- [ ] All credentials in **Secret Manager**, none in code or git
- [ ] Datasets layered **raw → clean → marts → archive**, one-way flow
- [ ] **Audit logging** on for BigQuery data access
- [ ] Credential **rotation** schedule in place (quarterly)
- [ ] **Budget** + alert attached to the billing account
- [ ] Every source connected **manually**, at least scope, by a human

If all ten are checked, you meet the standard. The [data-lake-starter](../SKILL.md) scaffold gets you there in one build.

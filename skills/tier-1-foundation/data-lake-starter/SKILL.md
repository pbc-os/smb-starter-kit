---
name: data-lake-starter
version: 1.0.0
tier: foundation
description: "Stand up a secure, empty BigQuery data lake on GCP — layered datasets, least-privilege service accounts, Workload Identity (no downloadable keys), read-only authorized views, audit logging, and a budget alert. Agent-guided or Terraform. You connect your own data sources afterward — on purpose."
requires:
  bins: ["gcloud", "bq"]
  skills: []
  env: ["GCP_PROJECT_ID"]
---

# Data Lake Starter — A Secure Home for All Your Business Data

> **Start here.** This is the first skill in the foundation tier. It builds the secure, empty lake that every other skill in this kit reads from and writes to.

## How to use this skill

> **Don't run these steps by hand. Hand them to an AI agent and let it drive.**

This skill is written to be run *by an agent on your behalf* — **Claude Code** or **Claude Desktop** — not copy-pasted into a terminal by you. That's not just easier; it's how the lake gets set up *securely*: the agent runs each `gcloud` / `terraform` command with judgment, explains every security choice as it goes, checks its own work, and never writes a secret to disk.

**Getting started (about 5 minutes):**

1. **Install an agent.** [Claude Desktop](https://claude.com/download) is the no-terminal option; [Claude Code](https://docs.anthropic.com/en/docs/claude-code) is the CLI version.
2. **Add this skill.** Clone the kit and copy this folder into your agent's skills directory:
   ```bash
   git clone https://github.com/pbc-os/smb-starter-kit.git
   cp -r smb-starter-kit/skills/tier-1-foundation/data-lake-starter ~/.claude/skills/data-lake-starter
   ```
   *(Not comfortable with git? Download the repo as a ZIP from GitHub and copy the folder. On Windows the skills directory is `%APPDATA%\Claude\skills\`.)*
3. **Ask the agent to run it.** Open the agent and say: **"Use the data-lake-starter skill to build my data lake — walk me through it."**

New to all of this? Start with the repo [README](../../../README.md). The rest of this document is written for the agent — you're welcome to read along, but you don't have to run anything yourself.

## 1. The Vision: You Already Have the Data

Every small business is already generating enterprise amounts of data. Your POS, your accounting, your email tool, your ad accounts, your reviews — each one is quietly piling up thousands of rows about your business. The problem was never *having* the data. It's that the data lives in twenty different tools that don't talk to each other, and stitching it together used to require a data team only big companies could afford.

```
┌──────────────────────── BEFORE: data scattered by design ───────────────────────┐
│                                                                                  │
│   [Square]   [Stripe]   [QuickBooks]   [Google Ads]   [Mailchimp]   [Reviews]    │
│      │           │           │             │              │             │        │
│      ▼           ▼           ▼             ▼              ▼             ▼        │
│   locked      locked      locked        locked         locked        locked      │
│                                                                                  │
│   You can see each one alone. You can never ask a question across all of them.   │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────── AFTER: one secure lake you own ──────────────────────────┐
│                                                                                  │
│   [Square]  [Stripe]  [QuickBooks]  [Google Ads]  [Mailchimp]  [Reviews]         │
│      └─────────┴───────────┴─────────────┴─────────────┴───────────┘             │
│                                  │  (you connect these — see §8)                  │
│                                  ▼                                                │
│                       ┌──────────────────────┐                                   │
│                       │   YOUR DATA LAKE      │   one place, your cloud account   │
│                       │   (BigQuery, secured) │   query it in plain English       │
│                       └──────────────────────┘                                   │
│                                                                                  │
│   "How did each location do last weekend vs the same weekend last year?"  ✓      │
│   "Which ads actually drove repeat customers?"                            ✓      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

This skill builds the lake on the right — **empty, secured, and yours.** It does *not* connect your sources (that's your deliberate, manual step — and it's a feature, see §8). It gives your agent a safe place to put data and a safe way to read it back.

---

## 2. What This Builds

A clean, layered BigQuery data lake with a one-way flow and a hard wall between raw data and whatever reads it:

```
                 you connect sources (§8)
                          │
                          ▼
   ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
   │   raw     │──► │   clean   │──► │   marts   │    │  archive  │
   │ landing   │    │ normalized│    │ analytics │    │ retired   │
   │ (has PII) │    │           │    │  (views)  │    │  tables   │
   └───────────┘    └───────────┘    └───────────┘    └───────────┘
        ▲                ▲                 │
        │                │                 │ read-only, via authorized views
   ingest SA        transform SA       agent SA  ◄── your AI agent + dashboards
   (write raw)     (raw→clean→marts)  (reads marts only — never touches raw)
```

| Resource | What it is | Why it matters |
|---|---|---|
| **4 datasets** — `raw`, `clean`, `marts`, `archive` | Layered storage with a one-way flow | Raw landing data (with PII) is isolated; consumers only ever see curated `marts` |
| **3 service accounts** — ingest, transform, agent | Least-privilege identities, scoped per dataset | No single key can do everything; the agent identity is read-only |
| **Workload Identity Federation** | Keyless auth for CI/automation | **No downloadable service-account keys** to leak |
| **Authorized views** | `marts` views read `raw`/`clean` on the agent's behalf | The agent queries answers without ever being granted access to raw PII |
| **Audit logging** | BigQuery data-access logs on | You can always see who queried what |
| **Budget alert** | Billing budget + email threshold | A runaway query can never surprise you |
| **Secret Manager enabled** | The vault your credentials will live in | Sets up the next skill ([secrets-manager](../secrets-manager/)) |

Everything follows the **[SMB Data Lake Hardening Standard](./references/hardening.md)** — the security baseline is the whole point.

---

## 3. Two Paths (pick one)

| Path | Best for | How |
|---|---|---|
| **A — Agent-guided** | Owners who don't live in a terminal | Let the agent run the `gcloud`/`bq` steps in §6, explaining each one |
| **B — Terraform** | Developers, or anyone who wants it reproducible | `terraform apply` the scaffold in [`templates/terraform/`](./templates/terraform/) |

Path A gets you the datasets, identities, and project-level roles by hand; Path B additionally applies the **dataset-scoped data roles and authorized-view wiring** precisely (those are fiddly to do by hand) and is recommended for production. Both enforce the same [hardening standard](./references/hardening.md).

---

## 4. Prerequisites

- **A Google Cloud account** with a billing account attached. (No GCP account yet? Ask the agent — it'll walk you through [console.cloud.google.com](https://console.cloud.google.com) and the free-tier signup. BigQuery's free tier covers a typical SMB; see [cost.md](./references/cost.md).)
- **A dedicated GCP project** for the lake. One project, one purpose — don't share it with other apps. Create one and set it:
  ```bash
  export GCP_PROJECT_ID="your-lake-project-id"
  gcloud config set project "$GCP_PROJECT_ID"
  ```
- **`gcloud` + `bq` CLIs** authenticated. Both ship with the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install). For **Path A** run `gcloud auth login`; for **Path B** also run `gcloud auth application-default login` — Terraform authenticates via Application Default Credentials, which is separate from the gcloud CLI login.
- For Path B only: **Terraform** ≥ 1.5. Tip: `export TF_VAR_project_id="$GCP_PROJECT_ID"` to reuse the same project value as Path A.

## Working With the User — Transparency & Consent

> Read this before running anything in Path A or Path B. It is not optional.

This skill creates real resources in the user's own cloud project — some of which **cost money** (enabling billable APIs, the budget) or **grant access** (service accounts, IAM). The agent must never make those changes silently.

- **Announce before you act.** Before each group of changes — enabling APIs, creating datasets, creating service accounts, granting IAM, attaching the budget, configuring Workload Identity — tell the user in plain language *what* you're about to create, in *which* project, and *why*. Name the exact resources.
- **Surface the implications.** *Cost:* enabling APIs and the budget touch billing — point the user at [cost.md](./references/cost.md) and state the expected range. *Access:* each IAM grant hands an identity power — say which service account gets which role on which dataset (and that `lake-agent` stays read-only on `marts`). *Reversibility:* datasets are created empty and protected from deletion, but identities and IAM grants persist until you remove them.
- **Pause for explicit approval.** After announcing a consequential group, stop and ask the user to confirm before running it. Don't act on an earlier blanket "go ahead" — re-confirm at each create / enable / grant. **Never run a billing-incurring, access-granting, or destructive command silently.**
- **Prefer dry-runs.** Use `terraform plan` before `apply`, and read-only checks before any create.

## 5. Setup Verification

The agent should confirm these before building:

1. **CLI present:** `which gcloud && which bq`
2. **Authenticated:** `gcloud auth list` shows an active account
3. **Project set & billing linked:** `gcloud config get-value project` and `gcloud billing projects describe "$GCP_PROJECT_ID"`
4. **Caller can administer IAM/BigQuery:** the active user needs `roles/owner` (or `bigquery.admin` + `iam.serviceAccountAdmin` + `serviceusage.serviceUsageAdmin`) on the project

If any check fails, fix it before proceeding — don't build half a lake.

---

## 6. Path A — Agent-Guided Build

> These are **guidance, not a rigid script.** Go one step at a time, tell the user what they should see, and adapt commands to their setup. Defaults below: BigQuery location `US`, dataset prefix `lake`.

> **Before each step below**, follow *Working With the User — Transparency & Consent* (above): announce the resources, surface the cost/IAM implications, and get an explicit yes before each create, enable, or grant.

### Step 1 — Enable the APIs
```bash
gcloud services enable \
  bigquery.googleapis.com secretmanager.googleapis.com \
  cloudresourcemanager.googleapis.com iam.googleapis.com \
  sts.googleapis.com iamcredentials.googleapis.com logging.googleapis.com \
  --project="$GCP_PROJECT_ID"
```

### Step 2 — Create the layered datasets
```bash
for ds in raw clean marts archive; do
  bq --location=US mk --dataset \
    --description "Data lake — ${ds} layer" \
    "${GCP_PROJECT_ID}:lake_${ds}"
done
```
*What you should see:* four datasets created. `raw` is your landing zone, `marts` is what gets read.

### Step 3 — Create the three least-privilege service accounts
```bash
gcloud iam service-accounts create lake-ingest    --display-name="Data lake — ingest (write raw)"            --project="$GCP_PROJECT_ID"
gcloud iam service-accounts create lake-transform  --display-name="Data lake — transform (raw→clean→marts)"   --project="$GCP_PROJECT_ID"
gcloud iam service-accounts create lake-agent      --display-name="Data lake — agent (read marts only)"       --project="$GCP_PROJECT_ID"
```

### Step 4 — Grant each one the *minimum* it needs
Everyone needs to run query jobs (project-level), but data access is scoped per dataset:
```bash
PID="$GCP_PROJECT_ID"
for sa in lake-ingest lake-transform lake-agent; do
  gcloud projects add-iam-policy-binding "$PID" \
    --member="serviceAccount:${sa}@${PID}.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser" --condition=None --quiet
done
```
Then dataset-scoped data roles (write only where each identity should write). Dataset-level grants are set on the dataset's access list — the agent can patch it via `bq update`, but **Path B (Terraform) does this more precisely and is recommended for the data roles.** Intent:

| Service account | `lake_raw` | `lake_clean` | `lake_marts` | `lake_archive` |
|---|---|---|---|---|
| `lake-ingest` | **WRITER** | — | — | — |
| `lake-transform` | READER | **WRITER** | **WRITER** | WRITER |
| `lake-agent` | — | — | **READER** | — |

> The `lake-agent` identity — the one your AI agent and dashboards use — can read **only** `marts`. It can never touch `raw`. That wall is the core of the security model.

### Step 5 — Turn on audit logging & a budget alert
Audit logging for BigQuery data access, and a billing budget so nothing surprises you. These are fiddly via CLI — **let Path B handle them**, or follow [hardening.md](./references/hardening.md) §7 and §9. Confirm with the user either way.

### Step 6 — (Recommended) Keyless CI with Workload Identity
If you'll run scheduled ingestion from GitHub Actions or Cloud Run, set up **Workload Identity Federation so you never download a service-account key.** This is involved — use the `wif` block in [Path B](./templates/terraform/) or [hardening.md](./references/hardening.md) §3.

✅ **You now have an empty, secured, layered data lake.**

---

## 7. Path B — Terraform

Everything above, codified and reproducible. **Run `terraform plan` first, show the user the plan, and get explicit approval before `terraform apply`.**

```bash
cd templates/terraform
cp terraform.tfvars.example terraform.tfvars   # then edit: project_id, billing_account, github_repo
terraform init
terraform plan      # read it — it should create datasets, SAs, IAM, audit config, budget
terraform apply
```

See [`templates/terraform/README.md`](./templates/terraform/README.md) for every variable and what each file provisions. The Terraform is the source of truth for the **dataset-scoped IAM and authorized views** — the parts that are awkward to do by hand.

---

## 8. Now Connect Your Sources — On Purpose

The lake is built and empty. Filling it is **your job, and it's meant to be.**

This kit ships **no pre-baked connectors.** Not because it's hard — because **every credential you mint is a trust decision only you should make.** A skill that auto-connected your Square account would need your Square keys; the secure pattern is the opposite — *you* create each credential at the smallest scope, *you* store it in your vault, and *you* decide what gets ingested. That deliberate step is the security boundary, and it stays manual by design.

The secure connection pattern (per source):
```
1. Mint a credential in the source app  →  least scope, read-only where possible
2. Store it in Secret Manager           →  see the secrets-manager skill (next)
3. Grant lake-ingest access to it        →  one secret, one grant
4. Write a small job that lands the data →  into lake_raw, nothing else
5. Schedule it                           →  Cloud Scheduler / cron
```

Full walkthrough + a per-source checklist: **[connecting.md](./references/connecting.md).**

---

## 9. Cost

A secured lake at SMB scale runs for roughly the price of a coffee per month — often **$0** inside the free tier. Honest math, what's free, and when you'd pay more: **[cost.md](./references/cost.md).**

---

## 10. What's Next — Climb the Tiers

You've laid the foundation. The rest of the kit builds on it:

```
data-lake-starter  ──►  secrets-manager  ──►  (you connect sources, §8)  ──►  semantic-layer-audit
   (this skill)          store your keys        fill the lake                  catalog what's in it
        │
        └──►  then Tier 2 (comms) · Tier 3 (ops) · Tier 4 (growth) · Tier 5 (automation)
              read from the same lake — morning briefings, forecasts, dashboards, and more.
```

1. **[secrets-manager](../secrets-manager/)** — your vault is enabled; now store credentials in it securely.
2. **Connect your first source** — start with the one you'd most like to query (usually your POS). See [connecting.md](./references/connecting.md).
3. **[semantic-layer-audit](../semantic-layer-audit/)** — once data is flowing, build a living catalog so your agent always knows what's queryable.
4. **Graduate upward** — every skill in Tiers 2–5 now has a secure place to read and write.

---

## Files

| File | Purpose |
|---|---|
| `references/hardening.md` | The SMB Data Lake Hardening Standard (the security baseline) |
| `references/connecting.md` | The manual boundary — how to securely connect your own sources |
| `references/cost.md` | Honest monthly cost + what's free |
| `templates/terraform/` | The full Terraform scaffold (Path B) |

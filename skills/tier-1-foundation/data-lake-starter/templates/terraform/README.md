# Data Lake Starter — Terraform (Path B)

Codified, reproducible version of the [data-lake-starter](../../SKILL.md) build. `terraform apply` this and you get the exact same secure, empty, layered BigQuery data lake — with the dataset-scoped IAM and audit config that are awkward to do by hand done precisely.

## Prerequisites

- Terraform ≥ 1.5
- A **dedicated** GCP project with a billing account attached
- `gcloud auth application-default login` (Terraform uses your ADC), and your user has `roles/owner` (or `bigquery.admin` + `iam.serviceAccountAdmin` + `serviceusage.serviceUsageAdmin`) on the project

## Use

```bash
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars: project_id (required), billing_account, github_repo

terraform init
terraform plan      # READ IT. Confirm it creates datasets + SAs + IAM + audit, nothing destructive.
terraform apply
```

When it finishes, `terraform output` shows your dataset ids, the three service-account emails, and the read-only `agent_identity` your AI agent should use.

## What each file provisions

| File | Provisions |
|---|---|
| `versions.tf` | Provider + version pins; optional remote state backend (commented) |
| `variables.tf` | All inputs and their defaults/validation |
| `main.tf` | Project lookup, shared locals (layers, SAs), and API enablement |
| `datasets.tf` | The four datasets (`raw`/`clean`/`marts`/`archive`) + a commented authorized-view example |
| `iam.tf` | The three service accounts + project-level `jobUser` + dataset-scoped data roles (the security model) |
| `security.tf` | BigQuery data-access **audit logging** (always) + **Workload Identity** for keyless CI (optional) |
| `budget.tf` | Billing budget + 50/90/100% alerts (only if `billing_account` is set) |
| `outputs.tf` | Dataset ids, SA emails, the agent identity, and the WIF provider name |

## The security model, in one table

| Service account | `raw` | `clean` | `marts` | `archive` | Project |
|---|---|---|---|---|---|
| `lake-ingest` | **dataEditor** | — | — | — | jobUser |
| `lake-transform` | dataViewer | **dataEditor** | **dataEditor** | dataEditor | jobUser |
| `lake-agent` | — | — | **dataViewer** | — | jobUser |

The `lake-agent` identity — used by your AI agent and dashboards — can read **only `marts`**, never `raw`. Curated `marts` views read `raw` via [authorized views](https://cloud.google.com/bigquery/docs/authorized-views) (the commented example in `datasets.tf`), so the agent gets answers without ever touching raw PII.

## Notes

- **Nothing destructive.** Datasets use `delete_contents_on_destroy = false`; a `terraform destroy` won't wipe data you've loaded.
- **No keys.** There are deliberately no `google_service_account_key` resources. CI uses Workload Identity; humans use their own `gcloud` auth. See the [hardening standard](../../references/hardening.md) §3.
- **Authorized views** depend on tables that don't exist in an empty lake, so they ship commented in `datasets.tf` — uncomment once you've connected a source. The IAM wall (agent can't read `raw`) holds regardless.
- This builds the lake. **Connecting sources is your deliberate next step** — see [connecting.md](../../references/connecting.md).

# ---------------------------------------------------------------------------
# Security controls: audit logging (always on) + keyless CI via Workload
# Identity Federation (optional). No downloadable service-account keys, ever.
# ---------------------------------------------------------------------------

# --- Audit logging: record every BigQuery data read and write ----------------
resource "google_project_iam_audit_config" "bigquery" {
  project = var.project_id
  service = "bigquery.googleapis.com"

  audit_log_config {
    log_type = "DATA_READ"
  }
  audit_log_config {
    log_type = "DATA_WRITE"
  }
  # ADMIN_READ is enabled by default and can't be disabled.
}

# --- Workload Identity Federation for GitHub Actions (optional) ---------------
# Lets CI authenticate as the ingest/transform SAs using short-lived tokens.
# No .json key is ever created or downloaded.

resource "google_iam_workload_identity_pool" "github" {
  count = var.enable_github_wif ? 1 : 0

  project                   = var.project_id
  workload_identity_pool_id = "github-pool"
  display_name              = "GitHub Actions"
  description               = "Keyless auth for CI (data-lake-starter)"

  depends_on = [google_project_service.apis]
}

resource "google_iam_workload_identity_pool_provider" "github" {
  count = var.enable_github_wif ? 1 : 0

  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github[0].workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub OIDC"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
  }

  # Hard-scope the provider to exactly one repo — nothing else can use it.
  attribute_condition = "assertion.repository == '${var.github_repo}'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Allow the named GitHub repo to impersonate the ingest + transform SAs (not agent).
resource "google_service_account_iam_member" "github_impersonation" {
  for_each = var.enable_github_wif ? toset(["ingest", "transform"]) : toset([])

  service_account_id = google_service_account.lake[each.value].name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github[0].name}/attribute.repository/${var.github_repo}"
}

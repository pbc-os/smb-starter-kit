# ---------------------------------------------------------------------------
# Least-privilege service accounts + dataset-scoped data roles.
# This is the part that's awkward to do by hand — Terraform makes it exact.
# ---------------------------------------------------------------------------

resource "google_service_account" "lake" {
  for_each = local.service_accounts

  project      = var.project_id
  account_id   = "lake-${each.key}"
  display_name = each.value

  depends_on = [google_project_service.apis]
}

locals {
  sa_emails = { for k, sa in google_service_account.lake : k => sa.email }

  # Project-level: every identity may RUN query jobs (but not read data it isn't granted).
  job_users = keys(local.service_accounts)

  # Dataset-scoped DATA access. This is the security model in one table:
  #   ingest    -> writes raw only
  #   transform -> reads raw, writes clean/marts/archive
  #   agent     -> reads marts only (never raw)
  # Map key is a stable, unique string so for_each is deterministic.
  dataset_grants = {
    "ingest-raw"        = { sa = "ingest", layer = "raw", role = "roles/bigquery.dataEditor" }
    "transform-raw"     = { sa = "transform", layer = "raw", role = "roles/bigquery.dataViewer" }
    "transform-clean"   = { sa = "transform", layer = "clean", role = "roles/bigquery.dataEditor" }
    "transform-marts"   = { sa = "transform", layer = "marts", role = "roles/bigquery.dataEditor" }
    "transform-archive" = { sa = "transform", layer = "archive", role = "roles/bigquery.dataEditor" }
    "agent-marts"       = { sa = "agent", layer = "marts", role = "roles/bigquery.dataViewer" }
  }
}

resource "google_project_iam_member" "job_user" {
  for_each = toset(local.job_users)

  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${local.sa_emails[each.value]}"
}

resource "google_bigquery_dataset_iam_member" "data_access" {
  for_each = local.dataset_grants

  project    = var.project_id
  dataset_id = google_bigquery_dataset.layer[each.value.layer].dataset_id
  role       = each.value.role
  member     = "serviceAccount:${local.sa_emails[each.value.sa]}"
}

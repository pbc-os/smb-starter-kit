# ---------------------------------------------------------------------------
# Data Lake Starter — core: project lookup, API enablement, shared locals.
# Part of the SMB Starter Kit. Builds a secure, EMPTY BigQuery data lake.
# ---------------------------------------------------------------------------

data "google_project" "this" {
  project_id = var.project_id
}

locals {
  # The four layers of the lake. One-way flow: raw -> clean -> marts. archive is cold storage.
  layers = ["raw", "clean", "marts", "archive"]

  dataset_ids = { for l in local.layers : l => "${var.lake_prefix}_${l}" }

  # The three least-privilege identities.
  service_accounts = {
    ingest    = "Data lake — ingest (write raw only)"
    transform = "Data lake — transform (raw -> clean -> marts)"
    agent     = "Data lake — agent (read marts only)"
  }

  # APIs the lake needs.
  services = [
    "bigquery.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "sts.googleapis.com",
    "iamcredentials.googleapis.com",
    "logging.googleapis.com",
    "billingbudgets.googleapis.com",
  ]
}

resource "google_project_service" "apis" {
  for_each = toset(local.services)

  project = var.project_id
  service = each.value

  disable_on_destroy = false
}

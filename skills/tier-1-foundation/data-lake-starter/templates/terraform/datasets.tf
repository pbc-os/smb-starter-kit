# ---------------------------------------------------------------------------
# The four layered datasets. Created empty. delete_contents_on_destroy = false
# so you can never accidentally `terraform destroy` your data away.
# ---------------------------------------------------------------------------

resource "google_bigquery_dataset" "layer" {
  for_each = local.dataset_ids

  project       = var.project_id
  dataset_id    = each.value
  friendly_name = "Data lake — ${each.key}"
  description   = "Data lake ${each.key} layer. Managed by data-lake-starter (SMB Starter Kit)."
  location      = var.bq_location

  delete_contents_on_destroy = false

  labels = {
    managed_by = "data-lake-starter"
    layer      = each.key
  }

  depends_on = [google_project_service.apis]
}

# ---------------------------------------------------------------------------
# AUTHORIZED VIEW — example (commented).
#
# An authorized view lets the `agent` identity read a curated view in `marts`
# that itself selects from `raw`/`clean`, WITHOUT granting the agent any access
# to raw data. The agent gets answers; raw PII stays behind the wall.
#
# You can't authorize a view over tables that don't exist yet — so this is a
# template to uncomment once you've connected a source and have raw tables.
#
# 1. Create the curated view in marts:
#
# resource "google_bigquery_table" "daily_sales" {
#   project    = var.project_id
#   dataset_id = google_bigquery_dataset.layer["marts"].dataset_id
#   table_id   = "daily_sales"
#   view {
#     use_legacy_sql = false
#     query = <<-SQL
#       SELECT DATE(created_at) AS day, COUNT(*) AS orders, SUM(total) AS revenue
#       FROM `${var.project_id}.${local.dataset_ids.raw}.square_orders`
#       GROUP BY day
#     SQL
#   }
#   deletion_protection = false
# }
#
# 2. Authorize that view to read the raw dataset:
#
# resource "google_bigquery_dataset_access" "marts_view_reads_raw" {
#   project    = var.project_id
#   dataset_id = google_bigquery_dataset.layer["raw"].dataset_id
#   view {
#     project_id = var.project_id
#     dataset_id = google_bigquery_dataset.layer["marts"].dataset_id
#     table_id   = google_bigquery_table.daily_sales.table_id
#   }
# }
#
# NOTE: iam.tf already manages raw's access list via google_bigquery_dataset_iam_member.
# Manage raw's access with ONE mechanism only — do NOT also add a
# google_bigquery_dataset_access resource to the raw dataset. (Mixing
# _iam_member and _dataset_access on the same dataset is a documented provider
# conflict: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_access )
# And do NOT silence it with lifecycle { ignore_changes = [access] } — that
# blinds Terraform to the very access controls this skill exists to enforce.
# If you want authorized views, move ALL of raw's grants into dataset_access
# entries here and remove them from iam.tf — never run both.
# ---------------------------------------------------------------------------

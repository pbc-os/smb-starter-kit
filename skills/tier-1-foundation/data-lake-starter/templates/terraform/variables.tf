variable "project_id" {
  type        = string
  description = "The dedicated GCP project that will hold the data lake. One project, one purpose."
}

variable "gcp_region" {
  type        = string
  description = "Default region for regional resources (not BigQuery's location)."
  default     = "us-central1"
}

variable "bq_location" {
  type        = string
  description = "BigQuery location for all datasets. Use a multi-region ('US', 'EU') or a single region. Pick once — it can't be changed later."
  default     = "US"
}

variable "lake_prefix" {
  type        = string
  description = "Prefix for the four dataset names (e.g. 'lake' -> lake_raw, lake_clean, lake_marts, lake_archive)."
  default     = "lake"

  validation {
    condition     = can(regex("^[a-z][a-z0-9_]{0,20}$", var.lake_prefix))
    error_message = "lake_prefix must be lowercase letters, digits, and underscores, starting with a letter."
  }
}

# --- Budget guardrail (optional) ---------------------------------------------
variable "billing_account" {
  type        = string
  description = "Billing account ID (e.g. 000000-AAAAAA-BBBBBB). If set, a budget + alert is created. Leave empty to skip."
  default     = ""
}

variable "budget_amount_usd" {
  type        = number
  description = "Monthly budget amount in USD for the alert thresholds."
  default     = 50
}

# --- Keyless CI with Workload Identity Federation (optional) ------------------
variable "enable_github_wif" {
  type        = bool
  description = "Create a Workload Identity pool/provider so GitHub Actions can authenticate WITHOUT a downloadable key."
  default     = false
}

variable "github_repo" {
  type        = string
  description = "GitHub repo allowed to impersonate the ingest/transform SAs, as 'owner/repo'. Required if enable_github_wif = true."
  default     = ""

  validation {
    condition     = var.github_repo == "" || can(regex("^[^/]+/[^/]+$", var.github_repo))
    error_message = "github_repo must be in 'owner/repo' form."
  }
}

# ---------------------------------------------------------------------------
# Budget guardrail (optional). Created only if you set var.billing_account.
# Emails billing admins at 50% / 90% / 100% of the monthly amount so a
# runaway query can never become a surprise bill.
# ---------------------------------------------------------------------------

resource "google_billing_budget" "lake" {
  count = var.billing_account != "" ? 1 : 0

  billing_account = var.billing_account
  display_name    = "Data Lake — ${var.project_id}"

  budget_filter {
    projects               = ["projects/${data.google_project.this.number}"]
    calendar_period        = "MONTH"
    credit_types_treatment = "INCLUDE_ALL_CREDITS"
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = tostring(var.budget_amount_usd)
    }
  }

  threshold_rules {
    threshold_percent = 0.5
  }
  threshold_rules {
    threshold_percent = 0.9
  }
  threshold_rules {
    threshold_percent = 1.0
  }

  depends_on = [google_project_service.apis]
}

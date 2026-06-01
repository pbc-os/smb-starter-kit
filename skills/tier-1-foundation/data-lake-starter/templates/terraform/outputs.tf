output "datasets" {
  description = "The four lake datasets, by layer."
  value       = { for k, ds in google_bigquery_dataset.layer : k => ds.dataset_id }
}

output "service_accounts" {
  description = "The three least-privilege service-account emails."
  value       = local.sa_emails
}

output "agent_identity" {
  description = "The read-only identity your AI agent / dashboards should use. Reads marts only."
  value       = local.sa_emails["agent"]
}

output "workload_identity_provider" {
  description = "Full WIF provider resource name for GitHub Actions (null unless enabled). Use as workload_identity_provider in google-github-actions/auth."
  value       = var.enable_github_wif ? google_iam_workload_identity_pool_provider.github[0].name : null
}

output "next_steps" {
  description = "Where to go from here."
  value       = "Lake is built and empty. Next: store credentials with the secrets-manager skill, then connect your first source (references/connecting.md), then catalog it with semantic-layer-audit."
}

terraform {
  required_version = ">= 1.5"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0, < 7.0"
    }
  }

  # Recommended for real use: store state remotely so it isn't only on your laptop.
  # Create a bucket first, then uncomment and set it.
  # backend "gcs" {
  #   bucket = "your-tf-state-bucket"
  #   prefix = "data-lake"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.gcp_region
}

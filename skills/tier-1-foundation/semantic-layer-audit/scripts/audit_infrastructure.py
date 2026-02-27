#!/usr/bin/env python3
"""
Semantic Layer Infrastructure Audit

Scans GCP project for:
- BigQuery datasets and tables (with row counts)
- Enabled APIs
- Secret Manager secrets
- Service accounts

Outputs structured JSON for semantic layer updates.

Requirements:
- gcloud CLI authenticated
- bq CLI (comes with gcloud)
- GCP_PROJECT_ID environment variable set

Usage:
    export GCP_PROJECT_ID="your-project-id"
    python3 audit_infrastructure.py > audit-results.json
"""

import subprocess
import json
import sys
import os
from datetime import datetime

# Configuration
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
SKIP_DATASETS = []  # Add dataset IDs to skip (e.g., ["temp_data", "staging"])
ROW_COUNT_TIMEOUT = 30  # Seconds per table


def run_cmd(cmd: list[str], timeout: int = 120) -> str:
    """Run command and return output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out"
    except Exception as e:
        return f"ERROR: {e}"


def get_bigquery_datasets() -> list[dict]:
    """Get all BigQuery datasets with their tables."""
    datasets = []
    
    # List datasets
    output = run_cmd(["bq", "ls", f"--project_id={PROJECT_ID}", "--format=json"])
    if output.startswith("ERROR"):
        return [{"error": output}]
    
    try:
        dataset_list = json.loads(output)
    except json.JSONDecodeError:
        return [{"error": f"Failed to parse datasets: {output[:200]}"}]
    
    for ds in dataset_list:
        ds_id = ds.get("datasetReference", {}).get("datasetId", "unknown")
        
        # Skip configured datasets
        if ds_id in SKIP_DATASETS:
            continue
            
        dataset_info = {
            "dataset_id": ds_id,
            "tables": []
        }
        
        # List tables in dataset
        tables_output = run_cmd([
            "bq", "ls", f"--project_id={PROJECT_ID}", 
            "--format=json", f"{PROJECT_ID}:{ds_id}"
        ])
        
        try:
            tables = json.loads(tables_output) if tables_output and not tables_output.startswith("ERROR") else []
            for t in tables:
                table_ref = t.get("tableReference", {})
                table_info = {
                    "table_id": table_ref.get("tableId", "unknown"),
                    "type": t.get("type", "TABLE"),
                    "creation_time": t.get("creationTime"),
                }
                
                # Get row count for tables (not views)
                if t.get("type") == "TABLE":
                    count_output = run_cmd([
                        "bq", "query", "--nouse_legacy_sql", "--format=json",
                        f"SELECT COUNT(*) as cnt FROM `{PROJECT_ID}.{ds_id}.{table_ref.get('tableId')}`"
                    ], timeout=ROW_COUNT_TIMEOUT)
                    try:
                        count_data = json.loads(count_output)
                        if count_data:
                            table_info["row_count"] = int(count_data[0].get("cnt", 0))
                    except (json.JSONDecodeError, IndexError, KeyError, TypeError):
                        table_info["row_count"] = "unknown"
                
                dataset_info["tables"].append(table_info)
        except json.JSONDecodeError:
            dataset_info["tables_error"] = tables_output[:200]
        
        datasets.append(dataset_info)
    
    return datasets


def get_enabled_apis() -> list[str]:
    """Get list of enabled GCP APIs."""
    output = run_cmd([
        "gcloud", "services", "list", "--enabled",
        f"--project={PROJECT_ID}", "--format=value(config.name)"
    ])
    if output.startswith("ERROR"):
        return [output]
    return sorted(output.split("\n")) if output else []


def get_secrets() -> list[str]:
    """Get list of secrets in Secret Manager."""
    output = run_cmd([
        "gcloud", "secrets", "list",
        f"--project={PROJECT_ID}", "--format=value(name)"
    ])
    if output.startswith("ERROR"):
        return [output]
    return sorted(output.split("\n")) if output else []


def get_service_accounts() -> list[dict]:
    """Get list of service accounts."""
    output = run_cmd([
        "gcloud", "iam", "service-accounts", "list",
        f"--project={PROJECT_ID}", "--format=json"
    ])
    if output.startswith("ERROR"):
        return [{"error": output}]
    try:
        accounts = json.loads(output)
        # Return simplified list
        return [
            {
                "email": a.get("email", "unknown"),
                "display_name": a.get("displayName", ""),
                "disabled": a.get("disabled", False)
            }
            for a in accounts
        ]
    except (json.JSONDecodeError, TypeError):
        return [{"error": f"Failed to parse: {output[:200]}"}]


def main():
    if not PROJECT_ID:
        print("ERROR: GCP_PROJECT_ID environment variable not set", file=sys.stderr)
        print("Usage: export GCP_PROJECT_ID='your-project-id' && python3 audit_infrastructure.py", file=sys.stderr)
        sys.exit(1)
    
    print(f"🔍 Semantic Layer Infrastructure Audit", file=sys.stderr)
    print(f"   Project: {PROJECT_ID}", file=sys.stderr)
    print(f"   Time: {datetime.now().isoformat()}", file=sys.stderr)
    print("", file=sys.stderr)
    
    audit = {
        "project_id": PROJECT_ID,
        "audit_time": datetime.now().isoformat(),
        "bigquery": {},
        "apis": [],
        "secrets": [],
        "service_accounts": []
    }
    
    # BigQuery (this is slow due to row counts)
    print("📊 Scanning BigQuery datasets...", file=sys.stderr)
    audit["bigquery"]["datasets"] = get_bigquery_datasets()
    dataset_count = len([d for d in audit["bigquery"]["datasets"] if "error" not in d])
    print(f"   Found {dataset_count} datasets", file=sys.stderr)
    
    # APIs
    print("🔌 Listing enabled APIs...", file=sys.stderr)
    audit["apis"] = get_enabled_apis()
    print(f"   Found {len(audit['apis'])} APIs", file=sys.stderr)
    
    # Secrets
    print("🔐 Listing secrets...", file=sys.stderr)
    audit["secrets"] = get_secrets()
    print(f"   Found {len(audit['secrets'])} secrets", file=sys.stderr)
    
    # Service accounts
    print("👤 Listing service accounts...", file=sys.stderr)
    audit["service_accounts"] = get_service_accounts()
    sa_count = len([a for a in audit["service_accounts"] if "error" not in a])
    print(f"   Found {sa_count} service accounts", file=sys.stderr)
    
    print("\n✅ Audit complete", file=sys.stderr)
    
    # Output JSON to stdout
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()

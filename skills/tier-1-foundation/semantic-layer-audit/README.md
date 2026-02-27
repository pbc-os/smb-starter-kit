# Semantic Layer Audit

**Tier 1 - Foundation**

Maintain a living data catalog so your AI agent always knows what data is available.

## Why This Matters

AI agents can only use data they know about. Without a maintained semantic layer:
- Agents forget about useful tables
- New integrations go undocumented
- Agents make up data sources that don't exist
- Knowledge degrades over time

This skill solves that by providing:
1. **Discovery process** to identify where data lives
2. **Automated scanning** for supported platforms (GCP/BigQuery)
3. **Structured audit process** to catch changes
4. **Template** for documenting your data catalog

## Supported Platforms

| Platform | Automation | Manual Guidance |
|----------|------------|-----------------|
| **GCP/BigQuery** | ✅ Full script | — |
| **Snowflake** | — | ✅ SQL snippets |
| **Redshift** | — | ✅ SQL snippets |
| **Databricks** | — | ✅ SQL snippets |
| **PostgreSQL** | — | ✅ SQL snippets |

The included Python script scans GCP infrastructure. For other platforms, the skill provides SQL snippets and guides you through manual documentation.

## What the GCP Script Scans

- **BigQuery:** All datasets, tables, row counts
- **Secret Manager:** All credentials (inventory only, not values)
- **APIs:** All enabled Google Cloud APIs
- **Service Accounts:** All service accounts in project

## Quick Start

```bash
# 1. Set your project
export GCP_PROJECT_ID="your-project-id"

# 2. Run audit
python3 scripts/audit_infrastructure.py > audit-results.json

# 3. Review results and update your semantic layer doc
cat audit-results.json | jq .
```

## Installation

```bash
npx skills add smb-pbc/agent-skills-public@semantic-layer-audit -g -y
```

## Requirements

- gcloud CLI authenticated
- BigQuery API enabled
- Secret Manager API enabled (optional)

## Files

```
semantic-layer-audit/
├── SKILL.md                              # Agent instructions
├── README.md                             # This file
├── scripts/
│   └── audit_infrastructure.py           # Infrastructure scanner
└── templates/
    └── SEMANTIC-LAYER-TEMPLATE.md        # Starter template
```

## Recommended Schedule

Weekly cron to catch schema changes:
```
0 6 * * 0  # Sunday 6am
```

## License

MIT

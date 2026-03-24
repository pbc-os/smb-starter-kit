---
name: google-drive
version: 1.0.0
tier: business-ops
description: "File management for small businesses. Organize invoices, contracts, SOPs, product photos, and team documents. Search, upload, share, and manage permissions. Built on the gws CLI."
requires:
  bins: ["gws"]
  skills: ["google-workspace"]
---

# Google Drive

**File management built for how small businesses actually organize documents.**

Uses the [gws CLI](https://github.com/googleworkspace/cli) for all Drive operations. See the `google-workspace` skill for setup.

## Triggers

- "find a file"
- "upload to drive"
- "share this document"
- "organize files"
- "list my drive files"
- Any request involving file storage, sharing, or organization

## Prerequisites

- `gws` CLI installed and authenticated with Drive scope
- Run `gws auth login -s drive` if not already done

## Core Commands

```bash
gws drive +upload                    # Upload a file with metadata
gws drive files list                 # List files
gws drive files get                  # Get file metadata
gws drive files create               # Create a file/folder
gws drive files export               # Export Google Docs/Sheets to PDF, etc.
```

## Common Operations

### List recent files

```bash
# Last 10 files, newest first
gws drive files list --params '{"pageSize": 10, "orderBy": "modifiedTime desc"}' --format table

# Search by name
gws drive files list --params '{"q": "name contains '\''invoice'\''", "pageSize": 20}'
```

### Upload a file

```bash
# Upload with automatic MIME type detection
gws drive +upload

# Upload to a specific folder
gws drive files create \
  --params '{"uploadType": "multipart"}' \
  --json '{"name": "Q1-Report.pdf", "parents": ["FOLDER_ID"]}' \
  --upload ./Q1-Report.pdf
```

### Download / Export

```bash
# Download a file
gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' -o ./downloaded-file.pdf

# Export a Google Doc as PDF
gws drive files export --params '{"fileId": "FILE_ID", "mimeType": "application/pdf"}' -o ./document.pdf

# Export a Google Sheet as CSV
gws drive files export --params '{"fileId": "FILE_ID", "mimeType": "text/csv"}' -o ./data.csv
```

### Create a folder

```bash
gws drive files create --json '{
  "name": "2025 Invoices",
  "mimeType": "application/vnd.google-apps.folder",
  "parents": ["PARENT_FOLDER_ID"]
}'
```

### Share a file

```bash
# Share with a specific person (editor access)
gws drive permissions create --params '{"fileId": "FILE_ID"}' --json '{
  "role": "writer",
  "type": "user",
  "emailAddress": "person@example.com"
}'

# Share with view-only access
gws drive permissions create --params '{"fileId": "FILE_ID"}' --json '{
  "role": "reader",
  "type": "user",
  "emailAddress": "person@example.com"
}'

# Share via link (anyone with the link can view)
gws drive permissions create --params '{"fileId": "FILE_ID"}' --json '{
  "role": "reader",
  "type": "anyone"
}'
```

### Search with Drive query syntax

```bash
# Find PDFs
gws drive files list --params '{"q": "mimeType=\"application/pdf\""}'

# Find files in a specific folder
gws drive files list --params '{"q": "'\''FOLDER_ID'\'' in parents"}'

# Find files modified in last 7 days
gws drive files list --params '{"q": "modifiedTime > '\''2025-01-08T00:00:00'\''", "orderBy": "modifiedTime desc"}'

# Find shared files
gws drive files list --params '{"q": "sharedWithMe = true", "pageSize": 10}'

# Find large files (for storage cleanup)
gws drive files list --params '{"q": "quotaBytesUsed > 10000000", "orderBy": "quotaBytesUsed desc", "pageSize": 20, "fields": "files(name,size,quotaBytesUsed,modifiedTime)"}'
```

## SMB File Organization

### Recommended folder structure

```
My Drive/
├── Business Operations/
│   ├── SOPs/                    # Standard operating procedures
│   ├── Checklists/              # Opening/closing, inventory, etc.
│   └── Policies/                # Employee handbook, safety, etc.
├── Finance/
│   ├── Invoices/
│   │   ├── 2025/
│   │   │   ├── January/
│   │   │   └── February/
│   │   └── 2024/
│   ├── Receipts/
│   ├── Tax Documents/
│   └── Reports/
├── Customers/
│   ├── Contracts/
│   ├── Correspondence/
│   └── Orders/
├── Vendors/
│   ├── Agreements/
│   ├── Price Lists/
│   └── Invoices Received/
├── Marketing/
│   ├── Photos/
│   ├── Ad Creatives/
│   └── Campaigns/
└── Team/
    ├── Meeting Notes/
    ├── Schedules/
    └── Training Materials/
```

### Create this structure automatically

```bash
# Create top-level folders
for folder in "Business Operations" "Finance" "Customers" "Vendors" "Marketing" "Team"; do
  gws drive files create --json "{\"name\": \"$folder\", \"mimeType\": \"application/vnd.google-apps.folder\"}"
done
```

## Integration with Other Skills

- **`gmail`** — Save email attachments to Drive
- **`google-sheets`** — Drive is where sheets live
- **`google-docs`** — Drive is where docs live
- **`google-chat`** — Share Drive files in Chat spaces
- **`morning-briefing`** — Reference important docs in daily briefing

## Tips

- Use `--format json` and pipe to `jq` for extracting specific fields
- Always use `--dry-run` before delete operations
- Use `--page-all` for complete file listings (auto-paginates)
- Google Drive search syntax is powerful — use `q` parameter for precise queries
- Export Google-native files (Docs, Sheets) before downloading — they have no binary content

## Related Skills

- `google-workspace` — Required setup (install and auth)
- `google-sheets` — Spreadsheet operations
- `google-docs` — Document operations
- `gmail` — Email attachment management

---

*Your Drive is your filing cabinet. Keep it organized and your agent can find anything.*

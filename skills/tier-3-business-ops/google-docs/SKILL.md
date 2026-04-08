---
name: google-docs
version: 1.0.0
tier: business-ops
description: "Document creation and management for small businesses. SOPs, proposals, contracts, meeting notes, and templates. Built on the gws CLI."
requires:
  bins: ["gws"]
  skills: ["google-workspace"]
---

# Google Docs

**Document management built for small business needs — SOPs, proposals, contracts, and meeting notes.**

Uses the [gws CLI](https://github.com/googleworkspace/cli) for all Docs operations. See the `google-workspace` skill for setup.

## Triggers

- "create a document"
- "write a doc"
- "draft a proposal"
- "create an SOP"
- "meeting notes"
- Any request involving document creation or editing

## Prerequisites

- `gws` CLI installed and authenticated with Docs + Drive scope
- Run `gws auth login -s docs,drive` if not already done

## Core Commands

```bash
gws docs +write                   # Create or update a document
gws docs documents create         # Create an empty document
gws docs documents get             # Get document content
```

## Common Operations

### Create a document

```bash
# Create with the helper command
gws docs +write

# Create via API
gws docs documents create --json '{
  "title": "Weekly Meeting Notes — 2026-01-15"
}'
```

### Write content to a document

```bash
# Insert text at the beginning
gws docs documents batchUpdate --params '{"documentId": "DOC_ID"}' --json '{
  "requests": [
    {
      "insertText": {
        "location": {"index": 1},
        "text": "Meeting Notes\n\nDate: January 15, 2026\nAttendees: Team\n\nAgenda:\n1. Review last week\n2. This week priorities\n3. Blockers\n\nNotes:\n"
      }
    }
  ]
}'
```

### Read a document

```bash
# Get full document content
gws docs documents get --params '{"documentId": "DOC_ID"}'
```

### Export as PDF

```bash
gws drive files export --params '{
  "fileId": "DOC_ID",
  "mimeType": "application/pdf"
}' -o ./document.pdf
```

## SMB Document Types

### Standard Operating Procedures (SOPs)

Structure for any SOP:
1. **Title** — What this procedure covers
2. **Purpose** — Why it exists
3. **When to use** — Triggers for this procedure
4. **Steps** — Numbered, clear, actionable
5. **What to do if something goes wrong** — Edge cases
6. **Last updated** — Date and who updated it

### Proposals / Quotes

Structure for client proposals:
1. **Executive summary** — What you're proposing, the price
2. **Scope of work** — Exactly what's included
3. **Timeline** — When it starts, milestones, completion
4. **Pricing** — Line items, total, payment terms
5. **Terms** — Validity period, cancellation, warranty

### Meeting Notes

Structure for meeting notes:
1. **Date, time, attendees**
2. **Agenda items discussed**
3. **Decisions made**
4. **Action items** — Who does what by when
5. **Next meeting date**

## Finding Documents

```bash
# List recent docs
gws drive files list --params '{
  "q": "mimeType=\"application/vnd.google-apps.document\"",
  "pageSize": 10,
  "orderBy": "modifiedTime desc"
}' --format table

# Search by name
gws drive files list --params '{
  "q": "mimeType=\"application/vnd.google-apps.document\" and name contains '\''SOP'\''",
  "pageSize": 10
}'
```

## Integration with Other Skills

- **`google-drive`** — Docs are Drive files; use Drive for search/permissions
- **`gmail`** — Email documents or draft emails from doc content
- **`google-calendar`** — Create meeting notes docs linked to calendar events
- **`playbook-discovery`** — Turn discovered playbooks into SOP documents

## Tips

- Use `gws docs +write` for the simplest document creation workflow
- For complex formatting, create a template in the Google Docs UI and duplicate it via Drive API
- Export to PDF for sharing with external parties who don't need edit access
- Keep SOPs in a shared Drive folder so the whole team has access

## Related Skills

- `google-workspace` — Required setup (install and auth)
- `google-drive` — File-level operations
- `google-calendar` — Meeting-linked documents

---

*Document your processes. If it's not written down, it doesn't exist.*

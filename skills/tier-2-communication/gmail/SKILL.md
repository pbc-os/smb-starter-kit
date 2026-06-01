---
name: gmail
version: 1.0.0
tier: communication
description: "Email management for small businesses. Daily triage, vendor communication, customer replies, templates, and inbox automation. Built on the gws CLI."
requires:
  bins: ["gws"]
  skills: ["google-workspace"]
---

# Gmail

**Email management built for how small businesses actually use email.**

Uses the [gws CLI](https://github.com/googleworkspace/cli) for all Gmail operations. See the `google-workspace` skill for setup.

## Triggers

- "check my email"
- "triage inbox"
- "send an email to..."
- "reply to..."
- "email summary"
- "set up email filters"
- Any request involving reading, sending, or managing email

## Prerequisites

- `gws` CLI installed and authenticated with Gmail scope
- Run `gws auth login -s gmail` if not already done

## Core Commands

```bash
gws gmail +triage              # Unread inbox summary (sender, subject, date)
gws gmail +triage --max 10     # Limit to 10 messages
gws gmail +send                # Send a new email
gws gmail +reply               # Reply to a message (handles threading)
gws gmail +reply-all           # Reply-all
gws gmail +forward             # Forward a message
gws gmail +watch               # Stream new emails as NDJSON (real-time)
```

> **Sending and filters are consequential.** Draft every outbound email and show it to the user for approval before `+send` / `+reply` / `+forward`. Before creating a filter (which silently diverts or archives future mail), run it with `--dry-run`, show the user what it would match, and get a yes.

## Daily Triage Workflow

The most valuable email workflow for an SMB owner. Run this every morning.

### Step 1: Get the inbox snapshot

```bash
gws gmail +triage --max 20 --format table
```

### Step 2: Categorize by priority

When triaging, sort emails into these buckets:

| Priority | What Goes Here | Action |
|----------|---------------|--------|
| **Urgent** | Customer complaints, payment issues, time-sensitive vendor requests | Handle immediately |
| **Today** | Orders, supplier confirmations, employee questions | Handle before end of day |
| **This week** | Marketing emails, partnership inquiries, non-urgent vendor comms | Batch process |
| **Archive** | Newsletters, notifications, FYI-only | Label and archive |

### Step 3: Process urgent items first

```bash
# Reply to a specific message
gws gmail +reply

# Forward something that needs delegation
gws gmail +forward
```

### Step 4: Batch-archive the noise

```bash
# Find and label promotional emails
gws gmail users messages list --params '{"q": "category:promotions is:unread", "maxResults": 50}' --format json
```

## SMB Email Patterns

### Vendor Communication

Common patterns for small businesses dealing with suppliers:

```bash
# Find all emails from a specific vendor
gws gmail +triage --query 'from:vendor@example.com'

# Find purchase orders
gws gmail +triage --query 'subject:(purchase order OR PO OR invoice)'

# Find delivery notifications
gws gmail +triage --query 'subject:(delivery OR shipping OR tracking)'
```

### Customer Service

```bash
# Find customer questions (unread)
gws gmail +triage --query 'is:unread -category:promotions -category:social'

# Find emails mentioning orders or complaints
gws gmail +triage --query '(order OR complaint OR refund OR return) is:unread'
```

### Financial / Accounting

```bash
# Find invoices and receipts
gws gmail +triage --query 'subject:(invoice OR receipt OR payment OR statement)'

# Find emails from your bank
gws gmail +triage --query 'from:*@yourbank.com'
```

## Setting Up Filters

Filters automate email organization. Essential for any SMB:

### Priority vendor filter
```bash
# Create a filter that labels emails from key vendors
gws gmail users settings filters create --json '{
  "criteria": {"from": "vendor1@example.com OR vendor2@example.com"},
  "action": {"addLabelIds": ["Label_vendors"], "removeLabelIds": ["INBOX"]}
}'
```

### Customer inquiry filter
```bash
# Label and star customer inquiries
gws gmail users settings filters create --json '{
  "criteria": {"query": "from:(-@yourdomain.com) subject:(order OR question OR help)"},
  "action": {"addLabelIds": ["Label_customers"], "markImportant": true}
}'
```

### Archive noise
```bash
# Auto-archive marketing newsletters
gws gmail users settings filters create --json '{
  "criteria": {"query": "unsubscribe category:promotions"},
  "action": {"removeLabelIds": ["INBOX"], "addLabelIds": ["Label_newsletters"]}
}'
```

## Email Templates

### Replying to common questions

Instead of typing the same response repeatedly, use templates:

**Order status inquiry:**
> Thanks for reaching out! Your order is [status]. Expected delivery is [date]. Let me know if you have any other questions.

**Vendor payment confirmation:**
> Payment for invoice #[number] has been processed. Please confirm receipt. Thanks.

**Meeting request:**
> Thanks for reaching out. I'm available [times]. Would any of those work for you? Here's my calendar link: [link]

The agent should adapt these templates to match the business's tone and the specific context of each email.

## Monitoring & Alerts

### Watch for new emails in real-time

```bash
# Stream new emails as they arrive (NDJSON)
gws gmail +watch
```

### Set up push notifications

```bash
# Watch for new messages (requires Pub/Sub topic)
gws gmail users watch --json '{
  "topicName": "projects/YOUR_PROJECT/topics/gmail-notifications",
  "labelIds": ["INBOX"]
}'
```

## Advanced Queries

Gmail search syntax works with all `--query` flags:

| Query | What It Finds |
|-------|--------------|
| `is:unread` | Unread messages |
| `is:starred` | Starred messages |
| `has:attachment` | Messages with attachments |
| `newer_than:7d` | Last 7 days |
| `from:name@domain.com` | From specific sender |
| `to:me` | Sent directly to you (not CC/BCC) |
| `subject:(keyword)` | Subject contains keyword |
| `label:vendors` | Messages with specific label |
| `larger:5M` | Larger than 5MB |
| `filename:pdf` | Has PDF attachment |

Combine with AND/OR:
```bash
gws gmail +triage --query 'is:unread has:attachment newer_than:3d'
```

## Email Templates

Ready-to-adapt templates for common SMB emails (customer replies, vendor follow-ups, payment reminders, appointment confirmations) live in [`references/email-templates.md`](references/email-templates.md). Load the file when the user asks for copy, not when they ask for operations.

## Integration with Other Skills

- **`morning-briefing`** — Email triage is part of the daily briefing
- **`playbook-discovery`** — Analyze 6 months of email to find automation opportunities
- **`google-drive`** — Save attachments to Drive
- **`google-tasks`** — Convert emails to tasks
- **`google-calendar`** — Find meeting-related emails

## Tips

- Run triage at the same time every day — consistency matters more than frequency
- Use `--format table` for quick visual scans, `--format json` for programmatic processing
- Create labels that match your business categories (vendors, customers, accounting, team)
- Don't try to reach inbox zero — triage and prioritize instead
- Use `--dry-run` before creating filters to preview what they'd match

## Related Skills

- `google-workspace` — Required setup (install and auth)
- `google-calendar` — Calendar events referenced in emails
- `google-drive` — Attachment management
- `morning-briefing` — Daily digest including email triage
- `playbook-discovery` — Discover email-based workflows to automate

---

*Your inbox is your business's nervous system. Triage it, don't fight it.*

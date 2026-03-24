---
name: google-workspace
version: 1.0.0
tier: foundation
description: "Set up the gws CLI to give your agent access to Gmail, Calendar, Drive, Sheets, Docs, Chat, Tasks, and every Google Workspace API. Foundation skill that enables all Google-powered communication, business ops, and automation skills."
requires:
  bins: ["node"]
---

# Google Workspace

**Give your agent access to all of Google Workspace through one CLI.**

This skill sets up [gws](https://github.com/googleworkspace/cli) — a command-line tool that wraps every Google Workspace API (Gmail, Calendar, Drive, Sheets, Docs, Chat, Tasks, Meet, Forms, and more). It outputs structured JSON, making it ideal for AI agents.

> **Attribution:** The `gws` CLI was created by [Justin Poehnelt](https://github.com/jpoehnelt), Developer Relations Engineer at Google. It's the foundation that makes the entire Google Workspace skill tier possible.

> `gws` doesn't ship a static list of commands. It reads Google's Discovery Service at runtime and builds its command surface dynamically. When Google adds an API endpoint, `gws` picks it up automatically.

## Triggers

- "set up google workspace"
- "connect gmail / calendar / drive / sheets"
- "install gws"
- "I need to read my email"
- "I need to manage my calendar"
- Any request that requires Google Workspace access and `gws` isn't installed yet

## What This Enables

Once `gws` is set up, these skills become available:

| Tier | Skill | What It Does |
|------|-------|-------------|
| 2 | `gmail` | Send, read, triage, reply, forward email |
| 2 | `google-calendar` | Manage events, check availability, meeting prep |
| 2 | `google-chat` | Send messages to Google Chat spaces |
| 3 | `google-drive` | Manage files, folders, shared drives |
| 3 | `google-sheets` | Read, write, create spreadsheets |
| 3 | `google-docs` | Create and edit documents |
| 3 | `google-tasks` | Manage task lists and to-dos |
| 5 | `morning-briefing` | Daily digest combining email, calendar, and business data |

## Prerequisites

- **Node.js 18+** — check with `node --version`
- **A Google Cloud project** — `gws auth setup` can create one, or use an existing project
- **A Google account** with access to Google Workspace (works with personal Gmail too)

## Installation

### Option 1: npm (recommended)

```bash
npm install -g @googleworkspace/cli
```

### Option 2: Pre-built binary

Download from [GitHub Releases](https://github.com/googleworkspace/cli/releases).

### Option 3: Build from source

```bash
cargo install --git https://github.com/googleworkspace/cli --locked
```

### Verify installation

```bash
gws --version
```

## Authentication

### Fastest Path (if you have `gcloud`)

```bash
gws auth setup     # Creates Cloud project, enables APIs, logs you in
```

This is the recommended path. It handles everything in one command.

### If you don't have `gcloud`

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or use an existing one)
3. Go to **APIs & Services → Credentials**
4. Configure OAuth consent screen:
   - App type: **External** (testing mode is fine)
   - Add your email under **Test users**
5. Create an **OAuth client** (type: Desktop app)
6. Download the client JSON → save as `~/.config/gws/client_secret.json`
7. Run:
   ```bash
   gws auth login
   ```

### Scope Selection

Google limits unverified apps to ~25 scopes. Don't select all — pick what you need:

```bash
# Just email
gws auth login -s gmail

# Email + calendar
gws auth login -s gmail,calendar

# Email + calendar + drive + sheets
gws auth login -s gmail,calendar,drive,sheets

# Common SMB setup (email, calendar, drive, sheets, docs, tasks, chat)
gws auth login -s gmail,calendar,drive,sheets,docs,tasks,chat
```

**Recommended for SMBs:** Start with `gmail,calendar,drive,sheets` — this covers 90% of small business needs. Add more services later with another `gws auth login -s <additional-services>`.

### Headless / Server / CI

1. Complete interactive auth on a machine with a browser
2. Export credentials:
   ```bash
   gws auth export --unmasked > credentials.json
   ```
3. On the headless machine:
   ```bash
   export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/credentials.json
   gws drive files list   # just works
   ```

### Service Account (server-to-server)

```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/service-account.json
gws drive files list
```

### Using an existing token

If another tool (e.g., `gcloud`) already manages tokens:

```bash
export GOOGLE_WORKSPACE_CLI_TOKEN=$(gcloud auth print-access-token)
```

## Verify Everything Works

After auth, test each service you enabled:

```bash
# Gmail — show unread count
gws gmail +triage --max 3

# Calendar — today's events
gws calendar +agenda

# Drive — list recent files
gws drive files list --params '{"pageSize": 5}'

# Sheets — list spreadsheets
gws drive files list --params '{"q": "mimeType=\"application/vnd.google-apps.spreadsheet\"", "pageSize": 5}'
```

## CLI Patterns

### Global Flags

| Flag | Description |
|------|-------------|
| `--format <FORMAT>` | `json` (default), `table`, `yaml`, `csv` |
| `--dry-run` | Preview without calling the API |
| `--page-all` | Auto-paginate (NDJSON output) |
| `--page-limit <N>` | Max pages (default: 10) |

### Command Structure

```bash
gws <service> <resource> <method> [flags]
gws <service> +<helper-command> [flags]
```

### Discovering Commands

```bash
# What services are available?
gws --help

# What can I do with gmail?
gws gmail --help

# What parameters does this method take?
gws schema gmail.users.messages.list

# Preview a request without executing
gws gmail users messages list --params '{"maxResults": 5}' --dry-run
```

### Helper Commands (shortcuts)

`gws` includes high-level helper commands prefixed with `+` that simplify common tasks:

```bash
gws gmail +triage           # Unread inbox summary
gws gmail +send             # Send an email
gws gmail +reply            # Reply to a message
gws calendar +agenda        # Today's events
gws calendar +insert        # Create an event
gws drive +upload            # Upload a file
gws sheets +read             # Read spreadsheet values
gws sheets +append           # Append a row
gws workflow +standup-report # Today's meetings + tasks
gws workflow +meeting-prep   # Prep for next meeting
gws workflow +weekly-digest  # Week summary
```

### Built-in Workflows

`gws` includes cross-service workflows that combine multiple APIs:

```bash
gws workflow +standup-report    # Calendar agenda + open tasks
gws workflow +meeting-prep      # Attendees + agenda + linked docs
gws workflow +weekly-digest     # Week's meetings + unread count
gws workflow +email-to-task     # Convert email → task
gws workflow +file-announce     # Share Drive file in Chat
```

### Built-in Recipes (40+)

For common multi-step operations:

```bash
# See all available recipes
gws --help | grep recipe
```

Examples: batch-invite-to-event, create-gmail-filter, find-large-files, save-email-attachments, create-doc-from-template, sync-contacts-to-sheet, and many more.

## Security Rules

- **Never** output secrets (API keys, tokens) directly
- **Always** confirm with the user before executing write/delete commands
- Prefer `--dry-run` for destructive operations
- Use `--format json` for programmatic processing — don't parse table output
- Credentials are encrypted at rest (AES-256-GCM) with OS keyring

## Credential Storage

| Method | Where Stored | Best For |
|--------|-------------|----------|
| Interactive OAuth | `~/.config/gws/` (encrypted) | Local development, personal use |
| Service Account | Wherever you put the JSON key | Servers, CI/CD, automation |
| Environment variable | `GOOGLE_WORKSPACE_CLI_TOKEN` | Short-lived sessions |
| Exported credentials | Your chosen path | Headless servers |

For production/server use, consider storing the service account key or exported credentials in your secrets manager (see `secrets-manager` skill).

## Troubleshooting

### "Access blocked" on login
- You need to add your email as a **Test user** in the OAuth consent screen
- Go to: Google Cloud Console → APIs & Services → OAuth consent screen → Test users → Add

### Scope errors
- Your app may be in testing mode with limited scopes
- Use `-s service1,service2` to select only what you need
- Or publish the app for broader scope access

### "gws: command not found"
- Ensure Node.js 18+ is installed: `node --version`
- Try: `npx @googleworkspace/cli --version`
- Check your PATH includes npm global bin: `npm config get prefix`

### Rate limits
- Use `--page-delay <MS>` to slow down pagination
- Use `--page-limit <N>` to cap pages
- For bulk operations, add delays between calls

## What's Next

After setup, install the skills that match your needs:

- **Need email management?** → `gmail` skill
- **Need scheduling?** → `google-calendar` skill
- **Need file management?** → `google-drive` skill
- **Need reporting/tracking?** → `google-sheets` skill
- **Want a daily briefing?** → `morning-briefing` skill

## Related Skills

- `secrets-manager` — Store `gws` credentials securely for server deployments
- `gmail` — Email management for SMBs
- `google-calendar` — Calendar management for SMBs
- `google-drive` — File management for SMBs
- `google-sheets` — Spreadsheet operations for SMBs
- `morning-briefing` — Daily digest combining all Google Workspace data

---

*Powered by [gws](https://github.com/googleworkspace/cli) by [Justin Poehnelt](https://justin.poehnelt.com) — one CLI for all of Google Workspace.*

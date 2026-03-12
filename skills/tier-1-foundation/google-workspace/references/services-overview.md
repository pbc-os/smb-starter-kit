# Google Workspace Services Overview

Quick reference for which `gws` service covers what.

## Core Services

| Service | Command | What It Does | Common SMB Use |
|---------|---------|-------------|----------------|
| **Gmail** | `gws gmail` | Send, read, triage, label, filter email | Customer comms, vendor management, daily triage |
| **Calendar** | `gws calendar` | Events, scheduling, free/busy, agenda | Staff scheduling, customer appointments, meetings |
| **Drive** | `gws drive` | Files, folders, shared drives, permissions | Document storage, invoices, SOPs, product photos |
| **Sheets** | `gws sheets` | Read, write, create spreadsheets | Sales tracking, inventory, expense reports |
| **Docs** | `gws docs` | Create and edit documents | SOPs, proposals, contracts, meeting notes |
| **Chat** | `gws chat` | Send messages to Spaces | Team communication, alerts, announcements |
| **Tasks** | `gws tasks` | Task lists, to-dos | Daily checklists, project tracking |

## Additional Services

| Service | Command | What It Does |
|---------|---------|-------------|
| **Forms** | `gws forms` | Create and manage forms |
| **Slides** | `gws slides` | Create and manage presentations |
| **Meet** | `gws meet` | Manage meeting spaces |
| **Keep** | `gws keep` | Notes and lists |
| **Classroom** | `gws classroom` | Course management (education) |
| **Admin** | `gws admin` | Directory, users, groups (Workspace admin) |
| **People** | `gws people` | Contacts management |

## Helper Commands by Service

### Gmail
| Command | Description |
|---------|-------------|
| `gws gmail +send` | Send an email |
| `gws gmail +triage` | Unread inbox summary |
| `gws gmail +reply` | Reply to a message |
| `gws gmail +reply-all` | Reply-all to a message |
| `gws gmail +forward` | Forward a message |
| `gws gmail +watch` | Stream new emails as NDJSON |

### Calendar
| Command | Description |
|---------|-------------|
| `gws calendar +agenda` | Show upcoming events |
| `gws calendar +insert` | Create a new event |

### Drive
| Command | Description |
|---------|-------------|
| `gws drive +upload` | Upload a file with metadata |

### Sheets
| Command | Description |
|---------|-------------|
| `gws sheets +read` | Read values from a spreadsheet |
| `gws sheets +append` | Append a row to a spreadsheet |

### Cross-Service Workflows
| Command | Description |
|---------|-------------|
| `gws workflow +standup-report` | Calendar + tasks summary |
| `gws workflow +meeting-prep` | Attendees + agenda + docs |
| `gws workflow +weekly-digest` | Week's meetings + unread email |
| `gws workflow +email-to-task` | Convert email → task |
| `gws workflow +file-announce` | Share Drive file in Chat |

## Recommended Scope Sets for SMBs

### Minimal (email only)
```bash
gws auth login -s gmail
```

### Standard (most SMBs)
```bash
gws auth login -s gmail,calendar,drive,sheets
```

### Full (all communication + ops)
```bash
gws auth login -s gmail,calendar,drive,sheets,docs,tasks,chat
```

### With admin (Workspace organizations)
```bash
gws auth login -s gmail,calendar,drive,sheets,docs,tasks,chat,admin
```

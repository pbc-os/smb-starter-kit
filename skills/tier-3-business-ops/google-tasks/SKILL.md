---
name: google-tasks
version: 1.0.0
tier: business-ops
description: "Task management for small businesses. Daily to-dos, project tracking, meeting action items, and team checklists. Built on the gws CLI."
requires:
  bins: ["gws"]
  skills: ["google-workspace"]
---

# Google Tasks

**Simple task management integrated with Gmail and Calendar.**

Uses the [gws CLI](https://github.com/googleworkspace/cli) for all Tasks operations. See the `google-workspace` skill for setup.

## Triggers

- "create a task"
- "add to my to-do list"
- "what are my tasks"
- "mark as done"
- "show open tasks"
- Any request involving to-do items or task management

## Prerequisites

- `gws` CLI installed and authenticated with Tasks scope
- Run `gws auth login -s tasks` if not already done

## Core Commands

```bash
gws tasks tasklists list                    # List all task lists
gws tasks tasks list                        # List tasks in a list
gws tasks tasks insert                      # Create a new task
gws tasks tasks patch                       # Update a task (complete, rename, etc.)
gws tasks tasks delete                      # Delete a task
```

## Common Operations

### List all task lists

```bash
gws tasks tasklists list --format table
```

### List open tasks

```bash
# List tasks in a specific list
gws tasks tasks list --params '{
  "tasklist": "TASKLIST_ID",
  "showCompleted": false
}' --format table
```

### Create a task

```bash
# Simple task
gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{
  "title": "Follow up with vendor about delivery"
}'

# Task with due date
gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{
  "title": "Submit quarterly tax filing",
  "due": "2025-03-31T00:00:00Z",
  "notes": "Documents in Drive > Finance > Tax Documents"
}'
```

### Complete a task

```bash
gws tasks tasks patch --params '{
  "tasklist": "TASKLIST_ID",
  "task": "TASK_ID"
}' --json '{"status": "completed"}'
```

### Create a task list

```bash
gws tasks tasklists insert --json '{"title": "Weekly Store Checklist"}'
```

### Convert email to task

```bash
# Built-in workflow
gws workflow +email-to-task
```

## SMB Task Patterns

### Daily Operations Checklist

Create a recurring checklist for opening/closing:

```bash
# Create a task list for daily ops
gws tasks tasklists insert --json '{"title": "Daily Opening Checklist"}'

# Add checklist items
for task in "Check cooler temperatures" "Review today'\''s orders" "Confirm staff schedule" "Check inventory levels" "Review yesterday'\''s sales"; do
  gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json "{\"title\": \"$task\"}"
done
```

### Meeting Action Items

After a meeting, quickly capture action items:

```bash
gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{
  "title": "Send updated pricing to vendor — from Jan 15 meeting",
  "due": "2025-01-17T00:00:00Z"
}'
```

### Review overdue tasks

```bash
# Built-in recipe for reviewing overdue items
gws tasks tasks list --params '{
  "tasklist": "TASKLIST_ID",
  "showCompleted": false,
  "dueMax": "2025-01-15T23:59:59Z"
}'
```

## Integration with Other Skills

- **`gmail`** — Convert emails to tasks with `gws workflow +email-to-task`
- **`google-calendar`** — Tasks appear alongside calendar events
- **`morning-briefing`** — Open tasks are part of the daily standup report
- **`google-docs`** — Link task notes to relevant documents

## Tips

- Use `gws workflow +standup-report` to see tasks alongside today's calendar
- Set due dates on tasks so they surface in your calendar
- Keep task lists organized by context (daily ops, projects, follow-ups)
- Use task notes to link to relevant emails, docs, or sheets

## Related Skills

- `google-workspace` — Required setup (install and auth)
- `gmail` — Email-to-task conversion
- `google-calendar` — Task/calendar integration
- `morning-briefing` — Daily task review

---

*Capture it or forget it. Tasks bridge the gap between intention and execution.*

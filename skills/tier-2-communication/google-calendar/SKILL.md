---
name: google-calendar
version: 1.0.0
tier: communication
description: "Calendar management for small businesses. Schedule meetings, check availability, prep for meetings, manage staff schedules, and coordinate with customers. Built on the gws CLI."
requires:
  bins: ["gws"]
  skills: ["google-workspace"]
---

# Google Calendar

**Calendar management built for how small businesses actually schedule.**

Uses the [gws CLI](https://github.com/googleworkspace/cli) for all Calendar operations. See the `google-workspace` skill for setup.

## Triggers

- "what's on my calendar"
- "schedule a meeting"
- "check availability"
- "meeting prep"
- "cancel / reschedule a meeting"
- "block time for..."
- Any request involving scheduling, events, or availability

## Prerequisites

- `gws` CLI installed and authenticated with Calendar scope
- Run `gws auth login -s calendar` if not already done

## Core Commands

```bash
gws calendar +agenda             # Today's upcoming events
gws calendar +agenda --week      # This week's events
gws calendar +insert             # Create a new event
gws workflow +meeting-prep       # Prep for next meeting (attendees, docs, agenda)
gws workflow +standup-report     # Today's meetings + open tasks
```

## Daily Scheduling Workflow

### Morning: Know your day

```bash
# What's on today?
gws calendar +agenda --format table

# Full week view (Monday planning)
gws calendar +agenda --week --format table
```

### Before each meeting: Prep

```bash
# Get attendees, description, linked docs for next meeting
gws workflow +meeting-prep
```

### Scheduling: Create events

```bash
# Quick event from natural language
gws calendar events quickAdd --params '{"calendarId": "primary", "text": "Team standup tomorrow at 9am for 30 minutes"}'

# Structured event with attendees
gws calendar +insert
```

### Check availability before scheduling

```bash
# Check free/busy for specific people
gws calendar freebusy query --json '{
  "timeMin": "2026-01-15T09:00:00-05:00",
  "timeMax": "2026-01-15T17:00:00-05:00",
  "items": [
    {"id": "person1@example.com"},
    {"id": "person2@example.com"}
  ]
}'
```

## SMB Scheduling Patterns

### Staff Meetings

```bash
# Create a recurring weekly team meeting
gws calendar events insert --params '{"calendarId": "primary"}' --json '{
  "summary": "Weekly Team Standup",
  "start": {"dateTime": "2026-01-20T09:00:00-05:00", "timeZone": "America/New_York"},
  "end": {"dateTime": "2026-01-20T09:30:00-05:00", "timeZone": "America/New_York"},
  "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=MO"],
  "attendees": [
    {"email": "team-member@example.com"}
  ]
}'
```

### Customer Appointments

```bash
# Schedule a customer meeting
gws calendar events insert --params '{"calendarId": "primary"}' --json '{
  "summary": "Meeting with [Customer Name]",
  "description": "Discuss: [agenda items]",
  "start": {"dateTime": "2026-01-20T14:00:00-05:00", "timeZone": "America/New_York"},
  "end": {"dateTime": "2026-01-20T15:00:00-05:00", "timeZone": "America/New_York"},
  "attendees": [
    {"email": "customer@example.com"}
  ],
  "reminders": {
    "useDefault": false,
    "overrides": [
      {"method": "email", "minutes": 60},
      {"method": "popup", "minutes": 15}
    ]
  }
}'
```

### Focus Time / Deep Work Blocks

```bash
# Block focus time so meetings don't eat your day
gws calendar events insert --params '{"calendarId": "primary"}' --json '{
  "summary": "Focus Time — Do Not Schedule",
  "start": {"dateTime": "2026-01-20T08:00:00-05:00", "timeZone": "America/New_York"},
  "end": {"dateTime": "2026-01-20T10:00:00-05:00", "timeZone": "America/New_York"},
  "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=TU,TH"],
  "transparency": "opaque"
}'
```

### Vendor / Supplier Meetings

```bash
# Find all events with a specific vendor this month
gws calendar events list --params '{
  "calendarId": "primary",
  "timeMin": "2026-01-01T00:00:00Z",
  "timeMax": "2026-01-31T23:59:59Z",
  "q": "vendor name"
}'
```

## Managing Events

### Reschedule

```bash
# Update an event's time (need the eventId)
gws calendar events patch --params '{"calendarId": "primary", "eventId": "EVENT_ID"}' --json '{
  "start": {"dateTime": "2026-01-21T14:00:00-05:00", "timeZone": "America/New_York"},
  "end": {"dateTime": "2026-01-21T15:00:00-05:00", "timeZone": "America/New_York"}
}'
```

### Cancel

```bash
# Delete an event
gws calendar events delete --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'
```

### Add notes / agenda to existing meeting

```bash
gws calendar events patch --params '{"calendarId": "primary", "eventId": "EVENT_ID"}' --json '{
  "description": "Agenda:\n1. Review last week\n2. Discuss Q1 goals\n3. Action items"
}'
```

## Weekly Planning (Monday Routine)

A good Monday routine for any small business owner:

1. **Review the week:**
   ```bash
   gws calendar +agenda --week --format table
   ```

2. **Identify conflicts:** Look for overlapping events or back-to-back meetings without breaks

3. **Block focus time:** Protect at least 2 hours/day for deep work

4. **Prep for key meetings:**
   ```bash
   gws workflow +meeting-prep
   ```

5. **Check for missing follow-ups:** Are there meetings from last week that need follow-up emails?

## Integration with Other Skills

- **`morning-briefing`** — Calendar is part of the daily briefing
- **`gmail`** — Meeting-related emails, sending agendas
- **`google-tasks`** — Convert meeting action items to tasks
- **`google-docs`** — Meeting notes and agendas
- **`playbook-discovery`** — Analyze calendar for recurring meeting patterns

## Tips

- Always check free/busy before proposing times to external contacts
- Use `quickAdd` for fast event creation with natural language
- Set up recurring events for regular meetings — don't recreate them each week
- Use `--dry-run` before creating/modifying events to preview the request
- Keep event descriptions structured: agenda items, links, prep notes

## Related Skills

- `google-workspace` — Required setup (install and auth)
- `gmail` — Email coordination around meetings
- `google-tasks` — Action items from meetings
- `morning-briefing` — Daily calendar + email + business digest

---

*Your calendar is your commitment log. Protect it.*

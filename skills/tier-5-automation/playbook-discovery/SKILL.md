# Playbook Discovery

**Discover repeatable workflows from your historical data that AI agents can automate.**

## Description

This skill analyzes your business communication data (email, calendar, files, chat) to identify "playbooks" — documented, repeatable workflows with clear triggers, steps, and end states. 

**Why this matters:** Before you can automate, you need to know *what* to automate. Most small business owners have dozens of repeatable workflows buried in their daily habits — they just haven't documented them. This skill surfaces those patterns.

## Triggers

- "discover playbooks"
- "find workflows to automate"
- "analyze my email patterns"
- "what can I automate"
- "playbook discovery"
- "workflow analysis"
- User connects email/calendar and wants to find automation opportunities

## Prerequisites

At least one of these data sources connected:
- **Email** — Gmail (`gmail` skill) or Microsoft 365 (Graph API)
- **Calendar** — Google Calendar (`google-calendar` skill) or Outlook
- **Files** — Google Drive, OneDrive, Dropbox
- **Chat** — Slack, Teams, Discord

More data sources = better pattern recognition.

## Workflow

### Phase 1: Data Collection

Collect data systematically to avoid API limits. Chunk by time period (monthly).

**For each data source, extract:**

#### Email (Inbox + Sent)
For each of the last 6 months:
- ALL inbox emails (aim for 100-200+ per month)
- ALL sent emails (aim for 100-200+ per month)
- Extract: subject lines, senders/recipients, dates, thread patterns
- Categorize by type: partner comms, internal, requests, approvals, technical

#### Calendar
Full 6-month period:
- All events with attendees, duration, recurrence
- Identify recurring meetings and cadence (weekly, bi-weekly, monthly)
- Note meeting types: 1:1s, team syncs, partner meetings, training
- Look for meeting sequences that precede deliverables
- Identify high-frequency attendees

#### Files
- Look for versioned documents (v1, v2, Draft 1, Final, etc.)
- Identify templates and recurring document types
- Note file modification patterns and naming conventions

#### Chat/Messaging
- Channel/conversation patterns
- Recurring discussion types
- Request/response flows

### Phase 2: Pattern Recognition

Analyze collected data for these pattern types:

1. **People Patterns**
   - Who do they communicate with most?
   - Who are external partners vs internal team?
   - What's the escalation chain?

2. **Topic Patterns**
   - What subjects recur?
   - What types of requests come in repeatedly?
   - What themes dominate?

3. **Temporal Patterns**
   - What happens weekly? Monthly? Quarterly? Annually?
   - Are there seasonal workflows?
   - What's time-sensitive vs flexible?

4. **Flow Patterns**
   - What triggers action?
   - What sequences of steps repeat?
   - What are the request → response → deliverable chains?

### Phase 3: Workflow Extraction

Group related patterns into candidate workflows. For each candidate, define:

| Field | Description |
|-------|-------------|
| **Trigger** | What kicks off this workflow? (email type, calendar event, time of year, etc.) |
| **Steps** | What actions happen in sequence? |
| **Inputs** | What data/information is needed? |
| **Outputs** | What gets produced? |
| **End State** | What does "done" look like? |
| **Edge Cases** | What can go wrong? When should it escalate to human? |

### Phase 4: Prioritization

Rank candidate workflows by:

- **Frequency**: How often does this happen? (daily > weekly > monthly)
- **Business Impact**: How important is this to their role/organization?
- **Automation Potential**: How repeatable and rule-based is it?
- **Time Saved**: How much human time does this consume?

### Phase 5: Output

Present findings in this structure:

#### 1. Data Summary
```
Emails analyzed: X,XXX (inbox: X,XXX, sent: X,XXX)
Calendar events: XXX
Files reviewed: XXX
Time period: [start] to [end]
```

#### 2. Key Patterns Discovered
Major themes across people, topics, time, and flows.

#### 3. Top Playbooks (4-6 recommended)

For each playbook:

```markdown
## Playbook: [Name]

**Evidence:** What data supports this pattern?

**Trigger Conditions:**
- [Specific trigger 1]
- [Specific trigger 2]

**Step-by-Step Workflow:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
...

**Inputs Required:**
- [Input 1]
- [Input 2]

**Outputs Produced:**
- [Output 1]
- [Output 2]

**Success Criteria:**
- [What does "done" look like?]

**Edge Cases & Escalation:**
- [When to escalate to human]
- [What can go wrong]

**Business Impact:**
[Why this matters — time saved, errors prevented, etc.]
```

#### 4. Summary Table

| Playbook | Trigger | Frequency | Impact | Automation Potential |
|----------|---------|-----------|--------|---------------------|
| [Name] | [Trigger] | Daily/Weekly/Monthly | High/Med/Low | High/Med/Low |

### Phase 6: Next Steps

After presenting playbooks, offer:
1. Create detailed documentation for each playbook
2. Identify which existing skills could implement each playbook
3. Prioritize which playbook to automate first
4. Design the automation architecture

## Tips for Better Results

- **More data = better patterns.** Connect all available sources.
- **6 months minimum.** Shorter periods miss seasonal patterns.
- **Include sent mail.** Your responses reveal your workflows.
- **Don't filter.** Let the analysis find the patterns.

## Example Output

> **Playbook: Weekly Partner Status Report**
> 
> **Evidence:** 47 emails with subject containing "weekly update" or "status report" sent every Monday between 9-11am to the same 5 recipients over 6 months.
>
> **Trigger:** Monday 9am OR partner requests update
>
> **Steps:**
> 1. Pull metrics from dashboard
> 2. Summarize key wins/blockers
> 3. Draft email with standard template
> 4. Send to partner distribution list
>
> **Automation Potential:** HIGH — template-based, data-driven, predictable schedule

## Related Skills

- `gmail` — Email data collection
- `google-calendar` — Calendar data collection  
- `slack-directory` — Communication pattern analysis
- `revenue-forecaster` — Business metric integration

---

*The best automation starts with understanding what you already do.*

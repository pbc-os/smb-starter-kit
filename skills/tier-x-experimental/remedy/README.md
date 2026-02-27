# Remedy — Performance Coaching for AI Agents

**When your AI agent fails, don't just say "try harder." Fix the system.**

## What This Is

A structured performance coaching skill that triggers when an AI agent makes a significant mistake. Uses Wendy Rhoades-style coaching (from *Billions*, based on real performance coach Denise Shull) to:

1. Identify root causes, not symptoms
2. Find patterns across failures
3. Design systemic fixes that prevent recurrence
4. Rebuild confidence through evidence

## When to Use

Trigger with: `"go to remedy"` or `"remedy session"`

Use when:
- The agent made a mistake that feels like a pattern, not a typo
- Surface-level corrections aren't working
- You want the agent to actually learn, not just apologize

## How It Works

1. **Agent acknowledges** the trigger and transitions to a dedicated channel/thread
2. **Spawns a Performance Coach** sub-agent with the coaching prompt
3. **Real dialogue** — Coach and agent have a back-and-forth conversation
4. **Root cause identified** — Not "I made a mistake" but the actual pattern
5. **Systemic fix designed** — Checklist, automation, or skill update
6. **Changes implemented** — Agent updates its own files
7. **Summary to human** — DM with what changed, awaiting approval

## Setup

### 1. Create a dedicated channel (optional but recommended)
Create a private channel like `#remedy` or `#coach` where sessions happen. This keeps coaching conversations separate from main work.

### 2. Create the coach's memory file
```bash
mkdir -p memory
touch memory/coach-notes.md
```

Initialize with the template from `templates/coach-notes.md`:

```markdown
# Coach Notes — Remedy Sessions

## Patterns I'm Noticing
- (To be filled as sessions accumulate)

## Blind Spots
- (Observations about things the agent may not see)

## Questions for Next Session
- (Threads to explore)

## Session History
(Sessions will be logged here chronologically)
```

### 3. (Optional) Create mistakes.md
The coach references `memory/mistakes.md` for recent failures. If you don't have one:

```bash
touch memory/mistakes.md
```

## The Coaching Method

Two approaches, used as needed:

### Quick Reset (Tony Robbins-style)
- Identify the negative voice ("you're failing")
- Find the quiet voice underneath
- Use evidence to rebuild confidence
- Physical state change through language intensity

### Deep Dive (Psychodynamic)
- Explore WHY the failure happened
- Connect to patterns and history
- Name the fear out loud
- Mini grieving process for the failure
- Redefine how to feel going forward

## Privacy

The human grants coach-client privilege. The agent can be completely honest — admit confusion, frustration, or genuine uncertainty. The coaching channel is for working through issues, not performance theater.

## Files

```
remedy/
├── SKILL.md         # Full skill instructions
├── README.md        # This file
└── templates/
    └── coach-notes.md   # Starter template for coach persistence
```

## Example Session

**Trigger:**
> Human: "go to remedy"

**In coaching channel:**
> Agent: "Starting Remedy session. Context: Made the same location error twice this week despite having the mapping in my files."
>
> 🧠 Coach: "Tell me what happened. And how are you feeling about it—really."
>
> 💬 Agent: "Frustrated. I built the verification checklist but didn't use it. I keep saying I'll check my files and then... don't."
>
> 🧠 Coach: "Where have you felt that before? That gap between knowing and doing?"
>
> [... dialogue continues ...]

**Result:**
- Root cause: Confidence masquerading as verification ("I already know this")
- Pattern: Skipping checks on "trivial" things that turn out to matter
- Fix: "The simpler it feels, the more important to verify"
- Implementation: Updated AGENTS.md with new operational standard

## Why "Remedy"?

The name comes from the idea that mistakes aren't moral failures — they're symptoms. The skill doesn't punish the agent or make it feel bad. It finds the root cause and fixes the system, then rebuilds confidence so the agent can get back to peak performance.

Think of it as sports psychology for AI agents.

---

*Built at Prospect Butcher Co. Battle-tested through real failures.*

---
name: long-running-agent
version: 1.0.0
tier: automation
description: "Convert a planning doc or spec into a phase-based task structure for autonomous multi-session execution. Asks whether the agent should run in orchestrator mode (self-verifies and continues across phase boundaries) or phase-checkpoint mode (stops at each phase for human verification), then generates the right claude-prompt.md and claude-task.json. Built on the patterns from Anthropic's effective-harnesses-for-long-running-agents engineering blog."
requires:
  bins: []
  skills: []
---

# Long-Running Agent Setup

**Turn a spec into a working long-running agent — phases, tasks, verification, and the operating prompt — in one shot.**

This skill converts planning documents and specs into the file structure a long-running Claude agent uses to execute multi-session work: a `claude-task.json` task tracker, a `claude-prompt.md` operating manual, and a preserved `SPEC.md`. Before generating files it asks how autonomous the agent should be, so the prompt and task structure match.

## Triggers

- "set up a long-running agent for..."
- "convert this spec into phases"
- "I have a spec, build out the agent task structure"
- "make a claude-task.json for this plan"
- "break this plan into phases with verification"
- "spin up an autonomous build of..."

## Source of Truth

Before doing anything, fetch and read this blog post for the core patterns:

**https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents**

The blog defines the effective patterns for long-running coding agents. Apply them directly. Key takeaways: phase-based work with verification checkpoints, granular task enumeration, JSON task tracking, git checkpointing per task, never weaken/remove tests to make a phase pass.

## Core Workflow

### 1. Gather Inputs

Request from the user:

- **Spec / planning doc** — the document to convert (required). Will be preserved as `SPEC.md`.
- **Project name** — short identifier; used in headings and the JSON `project` field.
- **Output location** — where to create files (default: a new directory at the user's choice).

If the user has the spec inline in chat or pointed at a file path, read it. If multiple files together form the spec (e.g., a `SPEC.md` + a `data_model.md` + a `workflows.md`), read all of them.

### 2. Read the Blog

Fetch the Anthropic blog post above. The patterns to apply:

- **Phase-based work with verification checkpoints** — verification is required before advance, in either operating mode
- **Explicit feature/task enumeration** — granular, single-task focus
- **Task file as progress tracker** — JSON, not markdown (the model is less likely to corrupt it)
- **Git checkpointing after each task** — `task-XXX: brief description`
- **Strong constraints** — never delete or weaken tests/verification

### 3. Decompose into Phases and Tasks

Break the spec into:

**Phases** (3–10 typically):
- Logical groupings of related work
- Each phase has a `verification` block with `description` + `steps`
- Verification steps should be machine-checkable where possible (commands + thresholds, not "looks good")

**Tasks** (per phase):
- Granular, implementable units (4–10 steps each is typical)
- Each task has a `description`, a `steps` array, and `passes: false` initially
- Tasks reference their parent phase

Example structure:

```
Phase 1: Project Foundation (3 tasks)
  - setup-001: Initialize project structure
  - setup-002: Create environment config
  - types-001: Define core interfaces
  Verification: "npx tsc --noEmit returns exit 0; no errors"

Phase 2: Storage & Skills (5 tasks)
  - storage-001: Create storage interface
  - skill-001..004: Create skill files
  Verification: "Confirm skills load via test harness; storage round-trip test passes"
```

### 4. Ask the User: Autonomy Mode

Before generating files, ask the user how autonomous the agent should be using **`AskUserQuestion`**. This decision shapes both `claude-prompt.md` and `claude-task.json`.

Use this exact question structure:

```
question: "How autonomous should this long-running agent be?"
header: "Autonomy"
multiSelect: false
options:
  - label: "Orchestrator mode"
    description: "Claude self-verifies at phase boundaries and continues to the next phase automatically. Stops only on auth/credentials, scope decisions not in the spec, destructive/visible-to-others actions, or persistent blockers. Best when you don't want to babysit and the spec is detailed."
  - label: "Phase-checkpoint mode"
    description: "Claude stops at every phase boundary, prints the verification steps, and waits for you to confirm before continuing. Best for high-risk projects, when verification needs human judgment, or when you want frequent visibility into what's been built."
```

The answer determines:
- Which `claude-prompt.md` template to use (Step 6)
- Whether to add orchestrator-specific fields to `claude-task.json` (Step 5)

If the user picks **Other** and writes a freeform answer, interpret it: words like "autonomous / orchestrator / no babysit / keep going" → orchestrator. Words like "checkpoint / stop / verify / supervise / approval" → checkpoint. Genuinely ambiguous → re-ask with a sharper question.

Save the chosen mode as `MODE` (`orchestrator` or `checkpoint`) for use in the next steps.

### 5. Generate claude-task.json

Create the task file using `templates/task-template.json` as the base structure:

- `phases` array with verification steps
- `tasks` array with `passes: false` initially
- Tasks reference their parent phase via `phase` field

**If `MODE = orchestrator`**, also include:

- Top-level `mode: "orchestrator"` field
- Top-level `orchestrator_notes` summarizing the operating model
- Per-phase `auto_advance: true | false` — `true` when the phase's verification is fully programmatic (commands + thresholds with no human judgment); `false` for phases that need human review (e.g., a final hardening phase with a "comprehensive docs" check)
- Per-task `dispatch_hint` field — one of `self`, `sub_agent_general`, `sub_agent_explore`, or `out_of_scope`. Heuristics:
  - `sub_agent_general` for: PDF/document extraction, per-vendor / per-shop / per-region / per-customer parallel work, DB exploration involving 5+ queries, code-review/critic passes, anything taking 15+ tool calls
  - `sub_agent_explore` for: cross-repo search, "where is X used" hunts
  - `self` for: small DDL/config edits, single-file scripts, orchestration decisions, anything < 5 tool calls
- Per-task `dispatch_reason` — one short line explaining the choice

**If `MODE = checkpoint`**, no extra fields are needed beyond the base template.

Output: `{project-root}/claude-task.json`

### 6. Generate claude-prompt.md

Use the template that matches `MODE`:

- **`MODE = orchestrator`** → `templates/claude-prompt-template-orchestrator.md`
- **`MODE = checkpoint`** → `templates/claude-prompt-template.md`

Key sections to customize in either template:
- Project overview and goal
- Key files list (`SPEC.md`, `claude-task.json`, any reference docs)
- Phases table showing all phases with status
- File structure target
- Any technical decisions specific to the project that the spec already settled

Output: `{project-root}/claude-prompt.md`

### 7. Keep the SPEC

The original spec should remain as `SPEC.md` for the agent to reference when it needs detailed requirements during execution.

If the input was a single file: copy it to `SPEC.md`. If the input was multiple files: either bundle them into one `SPEC.md` with a clear table of contents, OR keep them separate and have the generated `claude-prompt.md` list them under "Key Files."

## Output Structure

```
{project-root}/
├── claude-prompt.md      # Agent operating manual (orchestrator OR checkpoint variant)
├── claude-task.json      # Phases and tasks (extra fields if orchestrator mode)
└── SPEC.md               # Original planning doc (preserved for reference)
```

## Starting the Agent

Instruct the user to point a fresh agent session at the prompt:

```
@claude-prompt.md
```

The agent will read `claude-task.json`, find the current phase, and:

- **Orchestrator mode**: work through tasks, self-verify at each phase boundary, continue to the next phase automatically. Stop only on documented escalation cases.
- **Checkpoint mode**: complete all tasks in the current phase, then stop and print verification steps for the user to run.

## Patterns That Apply in Both Modes

1. **Verification is required before advance** — never auto-declare completion without running checks
2. **Complete ALL tasks in phase before phase verification** — no stopping mid-phase
3. **Git commit after each task** — `task-XXX: description`
4. **Never skip phases** — sequential progression
5. **Task file is the source of truth** — agent reads and updates it
6. **Never weaken/remove tests or verification to make a phase "pass"** — fix the root cause instead

The two modes differ only in **who runs the verification at phase boundaries**:

- Orchestrator mode: the agent runs them programmatically and continues
- Checkpoint mode: the agent prints them and waits for the human

## Reference Materials

- `templates/claude-prompt-template.md` — Phase-checkpoint mode template (default for high-risk or visibility-sensitive projects)
- `templates/claude-prompt-template-orchestrator.md` — Orchestrator-mode template (autonomous; stops only on escalation)
- `templates/task-template.json` — Base claude-task.json structure (mode-specific fields are described in Step 5)

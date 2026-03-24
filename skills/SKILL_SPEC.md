# Skill Specification

Every skill in this repository follows a standard structure. This document defines the schema so that AI agents and tooling can programmatically discover, validate, and install skills.

## SKILL.md Frontmatter

Each `SKILL.md` file begins with YAML frontmatter. The frontmatter is the machine-readable manifest for the skill.

### Schema

```yaml
---
# Required
name: skill-name                    # Unique identifier (lowercase, hyphens)
description: "Short description"    # What the skill does (1-2 sentences)

# Recommended
version: 1.0.0                      # Semver — update when the skill changes materially
tier: foundation                    # One of: foundation, communication, business-ops, growth, automation, experimental

# Optional — declares what the skill needs
requires:
  bins: ["gws", "curl"]            # CLI tools that must be available on PATH
  skills: ["google-workspace"]      # Other skills this skill depends on
  secrets: ["slack-bot-token"]      # Named secrets the skill expects (from any secret manager)
  env: ["GCP_PROJECT_ID"]          # Environment variables the skill reads

# Optional — additional metadata
metadata:
  category: "communication"         # Freeform category tag
  agent_agnostic: true              # Default true — skill works with any AI agent
---
```

### Field Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Unique skill identifier. Lowercase, hyphens only. |
| `description` | Yes | string | One-to-two sentence summary of what the skill does. |
| `version` | Recommended | string | Semantic version (MAJOR.MINOR.PATCH). |
| `tier` | Recommended | string | Skill tier: `foundation`, `communication`, `business-ops`, `growth`, `automation`, `experimental`. |
| `requires.bins` | Optional | string[] | CLI tools that must be installed. The agent should check availability before proceeding. |
| `requires.skills` | Optional | string[] | Skill names that should be set up first. |
| `requires.secrets` | Optional | string[] | Named secrets the skill expects to exist. |
| `requires.env` | Optional | string[] | Environment variables the skill reads at runtime. |
| `metadata` | Optional | object | Freeform metadata for tooling or platform-specific config. |

### Version Guidelines

- **1.0.0** — Initial stable release
- **Bump PATCH** (1.0.1) — Typo fixes, clarifications, example improvements
- **Bump MINOR** (1.1.0) — New sections, new workflows, additional references
- **Bump MAJOR** (2.0.0) — Breaking changes to prerequisites, restructured skill, removed sections

## Directory Structure

Each skill lives in its own directory under the appropriate tier:

```
skills/
├── tier-1-foundation/
│   └── skill-name/
│       ├── SKILL.md                 # Main skill document (required)
│       ├── references/              # Supporting docs, API references (optional)
│       ├── templates/               # Config templates, starter files (optional)
│       ├── examples/                # Example outputs, sample data (optional)
│       └── scripts/                 # Helper scripts (optional, keep portable)
├── tier-2-communication/
├── tier-3-business-ops/
├── tier-4-growth/
├── tier-5-automation/
├── tier-x-experimental/
└── shared/                          # Cross-skill resources referenced by multiple skills
```

## Setup Verification Pattern

Skills should NOT ship rigid install scripts that assume specific system configurations. Instead, include a **Setup Verification** section in the SKILL.md that the agent can follow:

```markdown
## Setup Verification

The agent should verify the following before using this skill:

1. **Check CLI availability:** `which gws` (or equivalent for the required tool)
2. **Check authentication:** Run a lightweight read-only command to confirm credentials work
3. **Check secrets:** Verify required secrets are accessible from the configured secret manager
4. **Check dependencies:** Confirm prerequisite skills are installed

If any check fails, guide the user through setup rather than failing silently.
```

This approach works across agents (Claude Code, Codex, Gemini CLI, etc.) without assuming a specific runtime.

## Agent Agnosticism

Skills in this repository are designed to work with **any AI agent** that can read markdown and execute shell commands. While examples may reference specific agents, the underlying instructions are portable:

- Use standard CLI tools and APIs, not agent-specific features
- Write instructions as guidance the agent interprets, not rigid scripts
- Avoid hardcoding paths, versions, or platform-specific assumptions
- When a skill needs something installed, describe what's needed and let the agent figure out the best way for the user's system

## Machine-Readable Index

See `index.json` for a complete, parseable listing of all skills with their metadata. Agents can read this file to discover available skills, check dependencies, and plan installation order.

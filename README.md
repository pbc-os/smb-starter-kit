# SMB Agent Skills

**Turn your AI from a chatbot into a business operator.**

*Part of [PBC OS](https://github.com/pbc-os) — open-source AI infrastructure for small business.*

---

## What this is

A collection of **skills** — pre-built instructions that teach an AI agent how to actually run parts of a small business. Read your email. Pull your sales numbers. Pause a wasteful ad. Send a vendor reminder. Generate creative for a campaign. Forecast next week's revenue.

Not "talk about" any of those things. *Do* them.

If you've only ever used AI in a chat window, this is the part you've been missing. ChatGPT and Claude in a browser are smart, but they can't touch anything outside the chat. An AI **agent** is the same intelligence with hands — it runs on your computer (or in your Anthropic account), it can read files and call APIs, and skills are how you teach it to do specific jobs well.

## Who this is for

Small business owners who already feel like AI is useful for thinking and writing, and now want it to actually take work off their plate. You don't need to be technical. You don't need to use a terminal. You need about 5 minutes to set up the agent, and another 5 to drop in the first skill.

If you're a developer who already runs Claude Code or another CLI agent, skip to [the skill catalog](./skills/) — you know what to do.

---

## Setup

### Default path: Claude Desktop *(5 minutes, no terminal)*

The fastest way to get an agent that can actually run skills is to install **Claude Desktop**. It's the native Mac/Windows app from Anthropic, and it bundles Claude chat, Claude Cowork, and Claude Code in one place — meaning it can read files, run commands, and use skills, all from a chat interface. No terminal.

1. **Download Claude Desktop:** [claude.com/download](https://claude.com/download)
2. **Install and sign in** with your Anthropic account (or create one — there's a free tier).
3. **Add a skill.** Skills go in `~/.claude/skills/<skill-name>/` on Mac (`%APPDATA%\Claude\skills\<skill-name>\` on Windows). The easiest way to add one from this repo is to `git clone` the repo and copy the folder for the skill you want, e.g.:

   ```bash
   git clone https://github.com/pbc-os/agent-skills-public.git
   cp -r agent-skills-public/skills/tier-2-communication/gmail ~/.claude/skills/gmail
   ```

   *(If you're not comfortable with git, you can also download the repo as a ZIP from the GitHub page and copy the folder manually.)*

4. **Use the skill.** Open Claude Desktop and ask the agent to do the thing the skill is for — e.g., "give me a morning briefing" or "read my unread email." The agent will load the skill and follow its instructions.

That's it. Most skills also need credentials for the service they connect to (a Gmail token, a Square API key, etc.) — the [secrets-manager](./skills/tier-1-foundation/secrets-manager/) skill walks you through storing those securely once, and then every other skill that needs them just works.

### Power-user path: any CLI agent

These skills are agent-agnostic — they work with any AI agent that can read markdown and execute shell commands. If you already run one of these, just point it at the skills directory:

| Tool | Notes |
|---|---|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | The CLI version. Same skill loader as Desktop (`~/.claude/skills/`) |
| [Codex CLI](https://github.com/openai/codex) | OpenAI's terminal agent |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google's terminal agent |
| [Goose](https://github.com/block/goose) | Local-first, extensible |

For Codex / Gemini / Goose, check each tool's docs for where its skills directory lives. The `SKILL.md` file inside each skill folder is the entry point — frontmatter declares dependencies, the body is the instructions.

> **Need to onboard a non-technical user from inside ChatGPT or another browser chatbot?** There's an advanced "chatbot bridge" pattern that uses [`LLM.txt`](./LLM.txt) and [`CONTINUE.md`](./CONTINUE.md) to walk a beginner through installation from inside any chat window, then hand them off to a freshly-installed CLI agent with full context. See [`docs/advanced-onboarding.md`](./docs/advanced-onboarding.md). Most users won't need this — Claude Desktop is simpler.

---

## Agents, skills, and tools — the 30-second version

Think of an AI agent like a really smart employee.

- **The agent** is the employee — their brain, judgment, and memory. You hire one, they stick around, they learn how you like things.
- **Skills** are the training manuals you hand them. "Here's how we run a morning briefing." "Here's how we handle a vendor invoice." Each skill is a focused playbook for one job.
- **Tools** are the things the employee uses to do the work — your inbox, your spreadsheet, your accounting software, your ad platform. The agent already has access to tools through Claude Desktop or its CLI; what it doesn't have is the *playbook* for how to use them well in your business.

**This repo gives your agent skills.** One agent with twenty skills is almost always better than twenty separate agents with one skill each — because the agent remembers your preferences across everything, sees the whole picture, and chains skills together naturally (the secrets-manager skill enables Gmail, which enables the morning briefing, which uses the revenue forecaster).

---

## What Your First Week Could Look Like

**Day 1-2: Connect your email**

Once AI can read your inbox, something magical happens — it can actually SEE your business. Not in theory. Actually see what you deal with every day.

**Day 3-5: AI observes**

You don't do anything. AI reads 2 weeks of your emails and learns:
- Who emails you most
- What questions keep coming up
- What's taking your time

**Day 5-7: AI tells YOU what to automate**

Instead of you guessing what would help, AI shows you:

> "You answered 23 emails about delivery times last week. Want me to create an auto-reply?"
>
> "You have 5 vendors you email every Monday. Want me to track those and remind you?"
>
> "You got 8 customer complaints about the same issue. Want me to flag those instantly?"

**You pick which automations to try.** AI suggests based on your actual patterns. You decide.

---

## You Control the Access

This is important: **you decide how much access AI gets.**

| Level | What AI Can Do | Good For |
|-------|----------------|----------|
| **Read-only** | See your emails, can't send | Starting out, observing |
| **Draft** | Write emails, but you approve before sending | Testing automations |
| **Full** | Send on your behalf | After you trust it |

Start with read-only. Expand later. You're always in control.

---

## Available Skills (22 skills)

Each skill is a self-contained `SKILL.md` file (plus optional references, scripts, and templates) that teaches your agent how to do one job well. Skills compose — set up Tier 1 once and everything above it becomes a 5-minute install.

### Tier 1 — Foundation *(start here)*

These enable everything else. Set up once, forget about it.

| Skill | What it does |
|---|---|
| [secrets-manager](./skills/tier-1-foundation/secrets-manager/) | Secure API key storage across GCP, AWS, Azure, 1Password, Doppler, or Vault — with a startup wrapper pattern that keeps secrets in memory only |
| [google-workspace](./skills/tier-1-foundation/google-workspace/) | Install and authenticate the [gws CLI](https://github.com/googleworkspace/cli) — the gateway to every Google-powered skill in Tier 2 and 3 |
| [semantic-layer-audit](./skills/tier-1-foundation/semantic-layer-audit/) | Discover and document every data source your agent can touch. A living data catalog with reconciliation notes for the things only humans know |
| [mcp-guide](./skills/tier-1-foundation/mcp-guide/) | When to build an MCP server vs. when a CLI + skill is enough. Links to [Anthropic's mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) |

### Tier 2 — Communication

Connect your agent to the people in your business.

| Skill | What it does |
|---|---|
| [gmail](./skills/tier-2-communication/gmail/) | Daily triage, vendor comms, customer replies, filters, and templates |
| [google-calendar](./skills/tier-2-communication/google-calendar/) | Scheduling, availability, meeting prep, and staff schedules |
| [google-chat](./skills/tier-2-communication/google-chat/) | Team updates, shift handoffs, standups, alerts |
| [slack](./skills/tier-2-communication/slack/) | Messages, channels, automated updates, standups, rich blocks — pairs with `slack-directory` for name→ID lookups |
| [slack-directory](./skills/tier-2-communication/slack-directory/) | Fuzzy name-to-user-ID lookup for Slack, with local caching |

> **Slack or Google Chat?** Pick whichever your team already uses. Both skills share the same SMB patterns (standups, shift handoffs, alerts, weekly recaps) via the [shared messaging reference](./skills/shared/smb-team-messaging.md).

### Tier 3 — Business Ops

Your agent's eyes on the actual business: files, data, documents, tasks.

| Skill | What it does |
|---|---|
| [google-drive](./skills/tier-3-business-ops/google-drive/) | File management with an opinionated SMB folder taxonomy — invoices, contracts, SOPs, product photos |
| [google-sheets](./skills/tier-3-business-ops/google-sheets/) | Sales logs, inventory, expenses, and ready-to-adapt SMB sheet templates (Daily Sales / Inventory / P&L) |
| [google-docs](./skills/tier-3-business-ops/google-docs/) | SOPs, proposals, contracts, meeting notes |
| [google-tasks](./skills/tier-3-business-ops/google-tasks/) | Daily to-dos, project tracking, meeting action items |

### Tier 4 — Growth

Drive revenue through ads, creative, and brand.

| Skill | What it does |
|---|---|
| [google-ads](./skills/tier-4-growth/google-ads/) | Campaigns, audits, and wasted-spend detection via the official Google Ads API — with pre-flight checklists that prevent expensive launch mistakes |
| [nano-banana](./skills/tier-4-growth/nano-banana/) | Image generation, editing, and a 4-pass pipeline for truly transparent PNGs via Google Gemini |
| [creative-matrix](./skills/tier-4-growth/creative-matrix/) | 27-concept Meta/Facebook ad creative matrix (3 angles × 3 formats × 3 funnel stages), with nano-banana-powered asset generation |
| [brand-identity](./skills/tier-4-growth/brand-identity/) | 18-deliverable agency-grade brand system — strategy, logo, W3C design tokens, SVG vectors, and a printable HTML brand guide |

### Tier 5 — Automation

Discover and automate the repeatable work.

| Skill | What it does |
|---|---|
| [morning-briefing](./skills/tier-5-automation/morning-briefing/) | The "killer app" — composable daily digest that pulls email, calendar, tasks, and KPIs from whichever skills you've installed |
| [revenue-forecaster](./skills/tier-5-automation/revenue-forecaster/) | Weekly / 13-week / daily / stress-test revenue forecasting for multi-entity SMBs, with per-entity holiday and week-of-month tuning. Ships with an autoresearch-compatible eval so you can self-tune on your own history |
| [playbook-discovery](./skills/tier-5-automation/playbook-discovery/) | Mine 6 months of email, calendar, and files to surface the repeatable workflows hiding in your daily work |
| [autoresearch](./skills/tier-5-automation/autoresearch/) | Three-agent autonomous optimization loop (researcher + critic + meta-reviewer). Extends [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) with holdout validation, coverage-driven exploration, and metacognitive self-modification ([HyperAgents](https://arxiv.org/abs/2603.19461)) |

### Tier X — Experimental

Niche or in-development skills that don't fit the main tiers yet.

| Skill | What it does |
|---|---|
| [patent-figure](./skills/tier-x-experimental/patent-figure/) | Generate USPTO-style patent figure drawings from provisional patent markdown, with targeted single-fix iteration. Built on `nano-banana`. |

### Skill Dependency Map

```
secrets-manager ───────────────────────────────┐
                                               │
google-workspace ─┬── gmail ─────────┐         │
                  ├── google-calendar │         │
                  ├── google-chat ────┤         │
                  ├── google-drive    ├── morning-briefing
                  ├── google-sheets ──┤         │
                  ├── google-docs     │         │
                  └── google-tasks ───┘         │
                                               │
slack-directory ──── slack ────────────────────┤
                                               │
                  playbook-discovery            │
                           │                    │
                           ▼                    │
                   revenue-forecaster ◀─── autoresearch
                                               │
google-ads ────────────────────────────────────┘

nano-banana ──┬── creative-matrix
              ├── brand-identity
              └── patent-figure
```

### Coming Soon

- **Tier 3 — Business Ops:** Square POS, QuickBooks, BigQuery analytics
- **Tier 4 — Growth:** Mailchimp, Instagram
- **Tier 5 — Automation:** Workflow builder, health monitor, anomaly detection

---

## For AI Agents Reading This

These skills are portable across runtimes. The `SKILL.md` file in each folder is the entry point — frontmatter for dependencies, body for instructions. See [`skills/SKILL_SPEC.md`](./skills/SKILL_SPEC.md) for the standard schema.

If you're a chat-based AI walking a non-technical user through installation, see [`docs/advanced-onboarding.md`](./docs/advanced-onboarding.md) — it documents the chatbot-bridge pattern (`LLM.txt` → handoff packet → `CONTINUE.md`) for the rare case where the user can't or won't install Claude Desktop directly.

---

## Contributing

Have a skill that's been battle-tested and could help other SMBs? Open a PR!

**Quality bar:**
- Skill must be proven through real use (not theoretical)
- Documentation must be clear and complete
- Skills must follow the [Skill Spec](./skills/SKILL_SPEC.md) (frontmatter schema, directory structure)
- No hardcoded secrets or personal info
- Generalized for any agent/human pair

**Resources:**

| Resource | What It Is |
|----------|------------|
| [Skill Spec](./skills/SKILL_SPEC.md) | Standard schema for skill frontmatter, directory structure, and conventions |
| [Skills Index](./skills/index.json) | Machine-readable index of all skills — agents can parse this for discovery and dependency resolution |
| [Shared Resources](./skills/shared/) | Cross-skill references used by multiple skills (e.g., SMB team messaging patterns) |
| [Changelog](./CHANGELOG.md) | What changed and when |

---

## The Story

These skills were built at [Prospect Butcher Co](https://prospectbutcher.co), a premium butcher shop in Brooklyn. We use AI agents to:
- Forecast daily revenue
- Manage Google Ads ($40/day, fully autonomous)
- Track inventory across locations
- Generate product content for Walmart Marketplace
- Run morning briefings

Everything here was battle-tested on a real business before being published.

---

## Part of PBC OS

This repo is one piece of **[PBC OS](https://github.com/pbc-os)** — open-source AI infrastructure for small businesses.

**The vision:** PBC OS is your backoffice AI. It helps you make informed decisions faster — and then *acts on those decisions for you*. It's entirely dedicated to your business with no other biases.

| Repo | What It Does |
|------|--------------|
| **[agent-skills-public](https://github.com/pbc-os/agent-skills-public)** | Reusable AI agent skills (this repo) |
| **[pbc-x402-api](https://github.com/pbc-os/pbc-x402-api)** | Accept payments from AI agents |

**Coming soon: PBC by PBC** — Pre-configured Raspberry Pi 5 hardware (~$100) with everything ready to go. Run your own AI, on your own hardware, for your own business.

---

## License

MIT — Use freely, build on it, share improvements.

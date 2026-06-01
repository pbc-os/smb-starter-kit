# SMB Starter Kit

**Stand up a secure data lake, then turn your AI from a chatbot into a business operator.**

*Part of [PBC OS](https://github.com/pbc-os) — open-source AI infrastructure for small business.*

*Built and battle-tested by [Prospect Butcher Co](https://prospectbutcher.co), an **Anthropic education partner**.*

---

## What this is

A **starter kit** that takes a small business from zero to an AI-run backoffice — as a path you climb one step at a time.

It's two things that work together:

1. **A secure data lake you own.** The [data-lake-starter](./skills/tier-1-foundation/data-lake-starter/) skill stands up a hardened BigQuery lake in *your* cloud account — the one secure place all your business data can finally live together. You connect your own sources; nothing is pre-baked, because every credential is a trust decision only you should make.
2. **Skills that run on it** — pre-built instructions that teach an AI agent to actually do the work. Read your email. Pull your sales numbers. Pause a wasteful ad. Send a vendor reminder. Forecast next week's revenue.

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
   git clone https://github.com/pbc-os/smb-starter-kit.git
   cp -r smb-starter-kit/skills/tier-2-communication/gmail ~/.claude/skills/gmail
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

## Available Skills (24 skills)

The kit is a **path**, not just a pile. You start by building your data lake, then climb the tiers — each one reads from and writes to the same lake you own.

```
data-lake-starter ──► secrets-manager ──► (connect your sources) ──► semantic-layer-audit
  build the lake       store your keys         fill it                catalog what's in it
        │
        └──► then Tier 2 (comms) · Tier 3 (ops) · Tier 4 (growth) · Tier 5 (automation)
```

Each skill is a self-contained `SKILL.md` file (plus optional references, scripts, and templates) that teaches your agent how to do one job well. Skills compose — set up Tier 1 once and everything above it becomes a 5-minute install.

### Tier 1 — Foundation *(start here)*

These enable everything else. Set up once, forget about it.

| Skill | What it does |
|---|---|
| [data-lake-starter](./skills/tier-1-foundation/data-lake-starter/) | **Start here.** Build a secure, empty BigQuery data lake in your own cloud — layered datasets, least-privilege identities, no downloadable keys, audit logging, and a budget alert. Agent-guided or Terraform. You connect your own sources |
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
| [long-running-agent](./skills/tier-5-automation/long-running-agent/) | Turn a plan or spec into a phase-based task structure for autonomous multi-session execution — orchestrator mode (self-verifies across phases) or phase-checkpoint mode (stops for human review). Built on Anthropic's long-running-agents patterns |

### Tier X — Experimental

Niche or in-development skills that don't fit the main tiers yet.

| Skill | What it does |
|---|---|
| [patent-figure](./skills/tier-x-experimental/patent-figure/) | Generate USPTO-style patent figure drawings from provisional patent markdown, with targeted single-fix iteration. Built on `nano-banana`. |

### Skill Dependency Map

```
FOUNDATION (Tier 1) — set up once
  data-lake-starter · secrets-manager · semantic-layer-audit · google-workspace

BUILT ON secrets-manager
  slack-directory ──▶ slack    ·    google-ads    ·    nano-banana

BUILT ON google-workspace
  gmail · google-calendar · google-chat · google-drive · google-sheets · google-docs · google-tasks

nano-banana ──┬── creative-matrix
              ├── brand-identity
              └── patent-figure

AUTOMATION — composes the skills above
  morning-briefing    ◀── gmail · calendar · tasks
  playbook-discovery  ◀── gmail
  revenue-forecaster  ◀── autoresearch
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

This kit was built at [Prospect Butcher Co](https://prospectbutcher.co) — a premium butcher shop in Brooklyn and an **Anthropic education partner** — and it's exactly what the shop runs on: a secure data lake holding millions of rows of its own sales, finance, and marketing data, with AI agents that:
- Query the whole business in plain English
- Forecast daily revenue
- Manage Google Ads fully autonomously on a small daily budget
- Track inventory across locations
- Run morning briefings

Everything here was battle-tested on a real business before being published — starting with the data lake the rest is built on.

---

## Part of PBC OS

This repo is one piece of **[PBC OS](https://github.com/pbc-os)** — open-source AI infrastructure for small businesses.

**The vision:** PBC OS is your backoffice AI. It helps you make informed decisions faster — and then *acts on those decisions for you*. It's entirely dedicated to your business with no other biases.

| Repo | What It Does |
|------|--------------|
| **[smb-starter-kit](https://github.com/pbc-os/smb-starter-kit)** | Build a secure data lake, then run your business on agent skills (this repo) |

**Coming soon: PBC by PBC** — Pre-configured Raspberry Pi 5 hardware (~$100) with everything ready to go. Run your own AI, on your own hardware, for your own business.

---

## License

MIT — Use freely, build on it, share improvements.

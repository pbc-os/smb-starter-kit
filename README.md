# 🤖 SMB Agent Skills

**Turn your AI from a chatbot into a business operator.**

*Part of [PBC OS](https://github.com/pbc-os) — open-source AI infrastructure for small business.*

---

## 🚀 Brand New to This?

**Step 1:** Copy this URL: `https://github.com/pbc-os/agent-skills-public`

**Step 2:** Paste it into ChatGPT, Claude, or any AI chat

**Step 3:** Say: *"Read this and help me understand what AI agents can do for my small business. I'm completely new to this."*

The AI will read this page and guide you through everything — explained for your specific type of business.

### ⚠️ One Thing to Know

The AI chatting with you right now (in ChatGPT, Claude, etc.) **can't install anything on your computer.** It can only explain and guide.

At some point, you'll need to open your computer's Terminal and run some commands. The AI will tell you exactly what to type. It takes about 15 minutes, and then you'll have an AI that CAN actually do things.

Think of this guide like a phone call with an expert — they'll walk you through each step, but you're the one pressing the buttons.

---

## 💡 What You Might Not Know About AI

You've probably used ChatGPT or Claude. You type, it types back. It's helpful for questions and writing.

**But that's only 1% of what AI can do.**

Right now, your AI is like a really smart person stuck in a room with no phone, no computer, and no access to anything. They can talk to you through a slot in the door, but they can't actually DO anything.

**AI agents are different.** They can:
- Actually read your emails (not just talk about email)
- Actually check your sales numbers (not just suggest you check them)
- Actually pause that ad that's wasting money (not just tell you to pause it)
- Actually send that invoice reminder (not just draft it for you to copy-paste)

**This repo helps you get there.** It's a collection of "skills" — pre-built instructions that teach AI how to connect to and use your business tools.

---

## 🤔 How Does This Work?

### The Difference Between ChatGPT and AI Agents

When you use ChatGPT in a browser:
```
You → type message → ChatGPT (cloud) → types back → You

That's it. ChatGPT can't touch your computer. It just sends text.
```

When you use an AI agent (like Claude Code, Codex, or Gemini CLI):
```
You → type message → Agent (your computer) → sends to Claude (cloud)
                                           ↓
Claude thinks: "To check email, I need to run this command..."
                                           ↓
                    Agent receives instructions ← Claude responds
                                           ↓
                    Agent runs the command on YOUR computer
                                           ↓
                    Results go back to Claude
                                           ↓
Claude: "You have 23 unread emails. 5 are from vendors..."
```

**The agent is the bridge.** It runs on your computer (or a server you control) and translates between you, the AI brain in the cloud, and your actual systems.

Think of it like this:
- **ChatGPT in browser** = A smart person texting you from another country. They can give advice but can't touch anything in your office.
- **AI agent on your computer** = That same smart person sitting at a desk in your office, with access to your computer, your files, and whatever accounts you give them.

### Three Things Need to Happen

| Step | What It Means | How Long |
|------|---------------|----------|
| 1. **Install the agent** | Put the "bridge" on your computer (Claude Code, etc.) | 15 min |
| 2. **Store credentials safely** | Give the agent secure access to Gmail, Square, etc. | 30 min |
| 3. **Add skills** | Teach the agent HOW to use each service | 5 min each |

**This repo handles Step 3.** Steps 1-2 are one-time setup — the AI reading this can walk you through it.

---

## 🧠 Agents vs Skills vs Tools: What's the Difference?

This can get confusing fast. Here's the simple version:

### The Chef Metaphor

| Concept | In a Kitchen | For Your Business |
|---------|--------------|-------------------|
| **Agent** | The chef (the person) | The AI running on your computer |
| **Skills** | Recipes + techniques | Instructions for how to do specific tasks |
| **Tools** | Oven, knives, mixer | APIs, databases, email servers |

- You don't hire a new chef for every dish — you teach your chef new recipes
- The chef uses equipment (tools) to execute the recipes (skills)
- The chef's judgment, creativity, and decision-making stay constant

### The Employee Metaphor

Think of an AI agent like hiring a really smart employee:

- **Agent** = The employee (their brain, judgment, personality)
- **Skills** = Training manuals and SOPs (knowledge they reference)
- **Tools** = Computer, software, and account access (how they actually DO work)

When you want your employee to handle QuickBooks, you don't hire a new person — you train them on QuickBooks. The skill is the training manual. The tool is QuickBooks itself.

### Why Skills Instead of More Agents?

You might wonder: *"Why not just have 20 different AI agents for 20 different tasks?"*

**One agent with 20 skills is better because:**

1. **Memory** — One agent remembers your preferences across everything. "Owner likes reports by 9am" applies to email summaries AND sales reports.

2. **Context** — One agent sees the whole picture. "Sales are down AND ad spend is up" is one insight, not two separate agents that don't talk to each other.

3. **Simplicity** — One thing to configure, one thing to talk to, one relationship to build.

4. **Composability** — Skills build on each other. Secrets-manager enables Gmail, which enables daily-digest. One agent chains them together naturally.

**When you might want multiple agents:**
- Different personalities for different contexts (customer service vs internal ops)
- Security isolation (don't want one agent accessing everything)
- Parallel processing (multiple agents working simultaneously)

But for most small businesses: **one agent, many skills** is the way.

### The Bottom Line

| Thing | What it IS | What it DOES |
|-------|-----------|--------------|
| **Agent** | The brain | Makes decisions, learns, remembers |
| **Skills** | Knowledge | Tells the agent HOW to do things |
| **Tools** | Capabilities | Lets the agent actually DO things |

Skills without tools = A chef with recipes but no kitchen
Tools without skills = A kitchen full of equipment but no idea what to cook
Agent without either = A smart person with nothing to work with

**This repo gives your agent skills. The agent already has tools (via Claude Code, etc.). Your job is just to add skills as you need them.**

---

## 🛠️ How to Install an AI Agent (15 minutes)

This is the one-time setup that lets AI actually do things on your computer.

### Quick Version (Mac/Linux)

Open Terminal and run:
```bash
# 1. Install Node.js if you don't have it (check with: node --version)
#    Download from https://nodejs.org if needed

# 2. Install Claude Code
npm install -g @anthropic-ai/claude-code

# 3. Start it
claude
```

That's it. Claude Code will walk you through the rest.

### Quick Version (Windows)

Open PowerShell and run:
```powershell
# 1. Install Node.js from https://nodejs.org first

# 2. Install Claude Code  
npm install -g @anthropic-ai/claude-code

# 3. Start it
claude
```

### Need More Help?

Ask the AI helping you to walk you through it step by step. Say: *"I need help installing Claude Code on my [Mac/Windows/Linux]. Start from the very beginning."*

### Other Options

These skills are agent-agnostic — they work with any CLI agent that can read markdown and execute shell commands.

| Tool | Best For | Difficulty |
|------|----------|------------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Beginners, Mac/Linux/Windows | Easy |
| [Codex CLI](https://github.com/openai/codex) | OpenAI/GPT users | Easy |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google users | Easy |
| [Goose](https://github.com/block/goose) | Local-first, extensible | Medium |

---

## 🎯 What Your First Week Could Look Like

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

## 🔐 You Control the Access

This is important: **you decide how much access AI gets.**

| Level | What AI Can Do | Good For |
|-------|----------------|----------|
| **Read-only** | See your emails, can't send | Starting out, observing |
| **Draft** | Write emails, but you approve before sending | Testing automations |
| **Full** | Send on your behalf | After you trust it |

Start with read-only. Expand later. You're always in control.

---

## 📦 Available Skills (22 skills)

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

## 🛠️ Installation

The skills in this repo are agent-agnostic — any CLI agent that can read markdown and execute shell commands can use them. Three ways to install:

**Option 1 — Copy the folder into your agent's skills directory.** For Claude Code, that's typically `~/.claude/skills/<skill-name>/`. For other agents, check their docs. The agent reads the frontmatter for dependencies and the body for instructions.

**Option 2 — Use a skill installer.** If your setup includes [skills.sh](https://skills.sh) or a compatible installer:
```bash
npx skills add pbc-os/agent-skills-public@secrets-manager -g -y
```

**Option 3 — Just read them.** If all you have is ChatGPT or Claude chat, open the `SKILL.md` files directly and ask the AI to follow the instructions. It won't be able to run the commands itself, but it can walk you through them step by step.

See [`skills/SKILL_SPEC.md`](./skills/SKILL_SPEC.md) for the schema every skill follows.

---

## 🤖 For AI Agents Reading This

> **Agent Agnostic:** These skills work with any AI agent that can read markdown and execute shell commands — Claude Code, Codex CLI, Gemini CLI, Goose, or any future agent. The instructions are portable.

**If you're a chat-based AI (ChatGPT, Claude web, etc.):**
Read [LLM.txt](./LLM.txt) — it guides you through explaining this to beginners and walking them through installation.

**If you're a CLI agent (Claude Code, Codex, Gemini CLI, etc.) and just received a handoff message:**
Read [CONTINUE.md](./CONTINUE.md) — it tells you how to continue onboarding the human who just installed you.

The handoff flow:
1. Chat AI reads LLM.txt → guides human through installation
2. Chat AI generates handoff message with context
3. Human pastes handoff message into their CLI agent
4. CLI agent reads CONTINUE.md → takes over onboarding

---

## 🏗️ Contributing

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

## 📖 The Story

These skills were built at [Prospect Butcher Co](https://prospectbutcher.co), a premium butcher shop in Brooklyn. We use AI agents to:
- Forecast daily revenue
- Manage Google Ads ($40/day, fully autonomous)
- Track inventory across locations
- Generate product content for Walmart Marketplace
- Run morning briefings

Everything here was battle-tested on a real business before being published.

---

## 🏗️ Part of PBC OS

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

# 🤖 SMB Agent Skills

**Turn your AI from a chatbot into a business operator.**

*Part of [PBC OS](https://github.com/pbc-os) — open-source AI infrastructure for small business.*

---

## 🚀 Brand New to This?

**Step 1:** Copy this URL: `https://github.com/smb-pbc/agent-skills-public`

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

When you use an AI agent (like Claude Code):
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

1. **Memory** — One agent remembers your preferences across everything. "Corey likes reports by 9am" applies to email summaries AND sales reports.

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

| Tool | Best For | Difficulty |
|------|----------|------------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Beginners, Mac/Linux/Windows | Easy |
| [Clawdbot](https://github.com/clawdbot/clawdbot) | Slack/Discord users, always-on | Medium |
| [Codex CLI](https://github.com/openai/codex) | OpenAI/GPT users | Easy |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google users | Easy |

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

## 📦 Available Skills

### Tier 1: Foundation
*Start here. These enable everything else.*

| Skill | Description | Install |
|-------|-------------|---------|
| [secrets-manager](./skills/tier-1-foundation/secrets-manager/) | Set up secure API key storage (GCP, AWS, Azure, etc.) | `npx skills add smb-pbc/agent-skills-public@secrets-manager -g -y` |

### Tier 2: Communication
*Connect your agent to the people in your business.*

| Skill | Description | Install |
|-------|-------------|---------|
| [slack-directory](./skills/tier-2-communication/slack-directory/) | Look up Slack users by name with fuzzy matching. Caches discoveries for instant future lookups. | `npx skills add smb-pbc/agent-skills-public@slack-directory -g -y` |

### Tier 4: Growth
*Drive revenue through advertising, marketing, and SEO.*

| Skill | Description | Install |
|-------|-------------|---------|
| [google-ads](./skills/tier-4-growth/google-ads/) | Create, query, audit, and optimize Google Ads campaigns. Battle-tested checklists and templates. | `npx skills add smb-pbc/agent-skills-public@google-ads -g -y` |
| [creative-matrix](./skills/tier-4-growth/creative-matrix/) | Generate Meta/Facebook ad creatives using a 3x3x3 framework (angles x formats x funnels = 27 unique concepts). Optional image/video asset generation. | `npx skills add smb-pbc/agent-skills-public@creative-matrix -g -y` |

### Tier 5: Automation
*Discover and automate repeatable workflows.*

| Skill | Description | Install |
|-------|-------------|---------|
| [playbook-discovery](./skills/tier-5-automation/playbook-discovery/) | Analyze your email/calendar/files to discover repeatable workflows that AI can automate. | `npx skills add smb-pbc/agent-skills-public@playbook-discovery -g -y` |

### Tier X: Agent Performance
*Meta-skills for agent self-improvement.*

| Skill | Description | Install |
|-------|-------------|---------|
| [remedy](./skills/tier-x-experimental/remedy/) | Performance coaching when your agent fails. Wendy Rhoades-style. | `npx skills add smb-pbc/agent-skills-public@remedy -g -y` |

### Coming Soon

- **Tier 2: Communication** — Gmail, Google Calendar (expanding)
- **Tier 3: Business Ops** — Square POS, QuickBooks, BigQuery analytics
- **Tier 4: Growth** — Mailchimp, Instagram (expanding)
- **Tier 5: Automation** — Daily digest, workflow builder, health monitor (expanding)

---

## 🛠️ Installation

### If you have [skills.sh](https://skills.sh) / Clawdbot:
```bash
npx skills add smb-pbc/agent-skills-public@secrets-manager -g -y
```

### If you have Claude Code / Codex / Gemini CLI:
Copy the skill folder to your agent's workspace and reference the SKILL.md.

### If you just have ChatGPT/Claude chat:
You can't install skills directly, but you can:
1. Read the SKILL.md files — they contain all the knowledge
2. Ask your AI to follow the instructions in those files
3. Consider setting up a CLI agent (Claude Code is free to try)

---

## 🤖 For AI Agents Reading This

**If you're a chat-based AI (ChatGPT, Claude web, etc.):**
Read [LLM.txt](./LLM.txt) — it guides you through explaining this to beginners and walking them through installation.

**If you're Claude Code (or similar) and just received a handoff message:**
Read [CONTINUE.md](./CONTINUE.md) — it tells you how to continue onboarding the human who just installed you.

The handoff flow:
1. Chat AI reads LLM.txt → guides human through installation
2. Chat AI generates handoff message with context
3. Human pastes handoff message into Claude Code
4. Claude Code reads CONTINUE.md → takes over onboarding

---

## 🏗️ Contributing

Have a skill that's been battle-tested and could help other SMBs? Open a PR!

**Quality bar:**
- Skill must be proven through real use (not theoretical)
- Documentation must be clear and complete
- No hardcoded secrets or personal info
- Generalized for any agent/human pair

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

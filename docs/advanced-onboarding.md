# Advanced Onboarding: The Chatbot Bridge Pattern

> **Most users should not need this page.** The default install path in the [README](../README.md) (download Claude Desktop, drop a skill folder into `~/.claude/skills/`) is simpler, faster, and works for ~95% of small business owners.
>
> This document exists for the remaining 5%: someone who is interacting with you (an AI) inside a browser chatbot like ChatGPT or Claude.ai, and who has never opened a terminal in their life. The chatbot bridge pattern is how you walk that person through installing a real CLI agent and hand them off with full context, without losing the relationship you've built in the chat.

## When this pattern applies

Use the chatbot bridge when **all** of these are true:

- The user is talking to you in a browser-based chatbot (ChatGPT, Claude.ai, Gemini, etc.) — not a CLI, not Claude Desktop
- They want to use one of the skills in this repo
- They are not technical enough to follow a "download this app, drag this folder" instruction unaided
- They cannot or will not install Claude Desktop (which would be the simpler path)

If the user is on a Mac or Windows machine and willing to download an app, **just point them at the [Claude Desktop install path](../README.md#default-path-claude-desktop-5-minutes-no-terminal)** in the README and skip this entirely.

## Why the bridge exists

A chat-based AI in a browser tab cannot install software, run commands, or touch the user's filesystem. It can only send text. So if a non-technical user shows up in ChatGPT and says "I want this morning briefing thing on my computer," the chatbot needs a way to:

1. **Explain what's about to happen** in plain terms, at the user's level
2. **Walk them through installing a CLI agent** (Claude Code, Codex, Gemini CLI, etc.) one step at a time, with checkpoints
3. **Generate a handoff message** that captures the entire context of the conversation
4. **Hand the user off** to the freshly-installed CLI agent so they don't have to start over

The two files that make this work are at the repo root:

- [`LLM.txt`](../LLM.txt) — Instructions for the **chatbot** doing the onboarding. Tells it how to assess the user's level, explain agents in plain terms, walk them through installation step-by-step, and generate a handoff packet.
- [`CONTINUE.md`](../CONTINUE.md) — Instructions for the **CLI agent** receiving the handoff. Tells it how to read the handoff packet, greet the user by name, prove it can actually do things, and pick up where the chatbot left off.

## The flow

```
┌────────────────────────────────────────────────────────┐
│  1. User opens ChatGPT/Claude.ai                       │
│  2. User pastes this repo URL and asks for help        │
│  3. Chatbot fetches README + LLM.txt                   │
│  4. Chatbot follows LLM.txt:                           │
│       a. Asks user about their business + AI level     │
│       b. Explains agents in language they understand   │
│       c. Walks them through installing a CLI agent     │
│          (one command at a time, with checkpoints)     │
│       d. Verifies the CLI agent is working             │
│       e. Generates a handoff packet with full context  │
│  5. User copies the handoff packet                     │
│  6. User pastes it into the new CLI agent              │
│  7. CLI agent reads CONTINUE.md                        │
│  8. CLI agent greets user by name, addresses concerns, │
│     and continues onboarding from where chatbot left   │
└────────────────────────────────────────────────────────┘
```

## What's in the handoff packet

The handoff packet is a structured message the chatbot generates near the end of the install conversation. It captures:

- **About this person** — name, business type, computer type, experience level
- **What they want** — in their own words, the goal that brought them here
- **Their concerns** — any hesitations or worries the chatbot picked up on
- **What we completed** — installation steps that are already done
- **Next steps** — the recommended onboarding path
- **How to treat them** — tone guidance, what to do, what to avoid, specific concerns to address

The full packet template lives in [`LLM.txt`](../LLM.txt) under "Step 8: Generate the Handoff Packet."

## Why this matters less than it used to

When this pattern was originally designed, CLI agents were the only way to get a real AI agent on a user's computer, and the install was non-trivial — Node.js, npm, OAuth, etc. The chatbot bridge was the only way to get a non-technical SMB owner over that hump.

Claude Desktop now ships with the same execution capabilities (read files, run commands, use skills) inside a regular consumer app — no terminal, no Node, no install ceremony. For nearly every user, that's the right answer.

The chatbot bridge is preserved here because:

1. Some users genuinely won't install Claude Desktop (privacy preference, IT restrictions, Linux, etc.)
2. The handoff-packet pattern is itself a useful technique — it works for *any* multi-tool agent flow where context needs to survive across tool boundaries
3. `LLM.txt` is a load-bearing file that real chatbots fetch via raw URL when a user pastes the repo link, so removing it would break that path

## When to fall back to the bridge from the default path

If a user is going through the Claude Desktop install and gets stuck (Mac too old, Windows version unsupported, IT blocks the download, etc.), it's reasonable to fall back to the chatbot bridge as a Plan B. The same skills work either way — only the agent runtime is different.

## Files

- [`LLM.txt`](../LLM.txt) — Chatbot-side instructions
- [`CONTINUE.md`](../CONTINUE.md) — CLI agent-side instructions
- [`README.md`](../README.md) — Default install path (Claude Desktop) — **start here unless you have a specific reason not to**

---
name: mcp-guide
version: 1.0.0
description: "Educational guide to MCP (Model Context Protocol) — what it is, when you need it, when you don't, and how to build your own. Helps agents and humans understand when an MCP server adds value vs when a CLI + skill is enough."
metadata:
  openclaw:
    category: "foundation"
---

# MCP Guide

**Understand MCP so you can decide if you need one — and build one if you do.**

This is an educational skill. It doesn't install anything. It teaches agents and humans what MCP (Model Context Protocol) is, when it's the right tool, and when simpler alternatives (CLIs + skills) are better.

## Triggers

- "what is MCP"
- "should I build an MCP server"
- "MCP vs CLI"
- "how do MCPs work"
- "build an MCP"
- "connect [service] to my agent"
- When an agent is trying to figure out how to integrate an external service

## What Is MCP?

**MCP (Model Context Protocol)** is an open standard that lets AI agents talk to external services through a structured interface. Think of it as a universal adapter between your AI agent and the tools it uses.

### The Restaurant Metaphor

| Without MCP | With MCP |
|-------------|----------|
| You walk into every restaurant and shout your order in English, hoping someone understands | Every restaurant has the same ordering kiosk with the same interface — you always know how to order |

Without MCP, every integration is custom. With MCP, there's a standard way for agents to discover tools, understand their inputs/outputs, and call them.

### How It Works

```
Your Agent (Claude Code, etc.)
    ↕ MCP Protocol (JSON-RPC)
MCP Server (runs locally or remotely)
    ↕ API calls
External Service (Gmail, Slack, Square, etc.)
```

An MCP server:
1. **Advertises tools** — "I can send emails, read inbox, create filters"
2. **Describes each tool** — "send_email takes: to, subject, body. Returns: message_id"
3. **Executes tool calls** — Agent says "call send_email with these params" → server makes the API call → returns the result
4. **Handles auth** — Server manages API keys, OAuth tokens, etc.

The agent never touches the raw API. It just calls structured tools.

## When Do You Need an MCP?

### You probably DON'T need an MCP if:

| Situation | Better Alternative |
|-----------|-------------------|
| There's already a good CLI for the service | **CLI + skill** (like `gws` + our Google Workspace skills) |
| You're doing simple CRUD operations | **Direct API calls** via curl/scripts in a skill |
| Your agent only needs read access | **CLI + skill** with read-only commands |
| You're the only user | **Scripts + skill** — less infra to maintain |
| The service has a well-designed REST API | **Skill with curl patterns** — teach the agent to call it directly |

**This repo's approach:** We use CLIs + skills wherever possible. `gws` for Google Workspace, `stripe` for payments, `gcloud` for GCP. The skill provides the domain knowledge; the CLI provides the tool. No MCP needed.

### You probably DO need an MCP if:

| Situation | Why MCP Helps |
|-----------|---------------|
| **No good CLI exists** for the service | MCP gives you a structured interface where none exists |
| **Multiple agents** need the same integration | MCP server is shared infrastructure, not per-agent scripts |
| **Real-time data** — webhooks, streaming, subscriptions | MCPs handle persistent connections; CLIs are request/response |
| **Complex auth** — OAuth flows, token refresh, multi-tenant | MCP server manages auth centrally |
| **You want tool discovery** — agent should see what's available | MCP's `tools/list` lets agents discover capabilities dynamically |
| **Structured I/O** — you want typed inputs and outputs | MCP enforces schemas; CLI output is often unstructured text |
| **You're building for others** — distributing an integration | MCP is a standard; your custom scripts are not |

### The Decision Flowchart

```
Does a good CLI already exist for this service?
├── Yes → Use CLI + skill. Done.
└── No
    ├── Is it a simple REST API with < 10 endpoints?
    │   ├── Yes → Write curl patterns in a skill. Done.
    │   └── No
    │       ├── Do multiple agents/users need this?
    │       │   ├── Yes → Build an MCP server.
    │       │   └── No
    │       │       ├── Do you need real-time data (webhooks/streaming)?
    │       │       │   ├── Yes → Build an MCP server.
    │       │       │   └── No → Write a script + skill. Probably enough.
    │       │       └──
    │       └──
    └──
```

## MCP Architecture (for the curious)

### Components

| Component | What It Does | Example |
|-----------|-------------|---------|
| **MCP Client** | Your agent's MCP integration | Built into Claude Code, Cline, etc. |
| **MCP Server** | Wraps an external service | `slack-mcp-server`, `github-mcp-server` |
| **Transport** | How client and server communicate | stdio (local) or Streamable HTTP (remote) |
| **Tools** | Individual operations the server exposes | `slack_send_message`, `github_create_issue` |
| **Resources** | Data the server can provide | File contents, database records |
| **Prompts** | Pre-built prompt templates | "Summarize this repo", "Triage inbox" |

### Transport Options

| Transport | When to Use | How It Works |
|-----------|-------------|-------------|
| **stdio** | Local servers, single user | Server runs as a subprocess, communicates via stdin/stdout |
| **Streamable HTTP** | Remote servers, multi-user | Server runs as an HTTP service, clients send JSON-RPC over HTTP |

For most SMBs, **stdio** is fine — the MCP server runs on the same machine as your agent.

### Tool Anatomy

Every MCP tool has:

```json
{
  "name": "slack_send_message",
  "description": "Send a message to a Slack channel or DM",
  "inputSchema": {
    "type": "object",
    "properties": {
      "channel": {"type": "string", "description": "Channel ID or user ID"},
      "text": {"type": "string", "description": "Message text (supports Slack markdown)"}
    },
    "required": ["channel", "text"]
  },
  "annotations": {
    "readOnlyHint": false,
    "destructiveHint": false
  }
}
```

The agent sees this schema, knows what inputs are needed, and can call the tool without knowing anything about the Slack API underneath.

## Building Your Own MCP Server

If you've decided you need one, here's the path:

### Recommended Stack

| Choice | Recommendation | Why |
|--------|---------------|-----|
| **Language** | TypeScript | Best SDK support, good for AI-generated code, static typing |
| **Transport** | stdio (local) or Streamable HTTP (remote) | Avoid SSE (deprecated) |
| **Schema** | Zod (TypeScript) or Pydantic (Python) | Type safety for tool inputs |

### The Build Process

1. **Research the API** — Understand endpoints, auth, data models
2. **Plan your tools** — List operations to expose, prioritize by usage
3. **Set up the project** — Scaffold with the MCP SDK
4. **Implement tools** — One at a time, with proper error handling
5. **Test** — Use MCP Inspector to verify tools work
6. **Create evals** — Write test questions to verify LLMs can use your tools effectively

### Official Build Guide

Anthropic maintains a comprehensive MCP builder skill with templates, best practices, and language-specific guides:

**[Anthropic MCP Builder Skill](https://github.com/anthropics/skills/tree/main/skills/mcp-builder)**

This includes:
- Step-by-step implementation guides for TypeScript and Python
- MCP best practices (naming, pagination, error handling, response formats)
- Evaluation creation guide (test that LLMs can actually use your server)
- Project structure templates
- Quality checklists

**To use it with Claude Code:**
```bash
# Add the official MCP builder skill
npx skills add anthropics/skills@mcp-builder -g -y
```

Or just tell your agent: *"I want to build an MCP server for [service]. Use the mcp-builder skill."*

### Naming Conventions

| Language | Pattern | Example |
|----------|---------|---------|
| TypeScript | `{service}-mcp-server` | `slack-mcp-server` |
| Python | `{service}_mcp` | `slack_mcp` |

### Tool Naming

- Use `snake_case` with service prefix: `slack_send_message`, `github_create_issue`
- Be action-oriented: start with verbs (get, list, search, create, update, delete)
- Be specific: `slack_send_message` not `send_message` (avoids conflicts with other MCPs)

### Key Best Practices

1. **Tool descriptions must be precise.** The agent reads these to decide which tool to use. Vague descriptions = wrong tool choices.

2. **Return structured data.** JSON for programmatic use, Markdown for human readability. Support both when possible.

3. **Pagination is mandatory** for any tool that lists things. Default to 20-50 items. Return `has_more` and `next_offset`.

4. **Error messages must be actionable.** Not "Error 403" but "Permission denied — the bot token needs the `chat:write` scope. Add it at api.slack.com/apps → OAuth & Permissions."

5. **Annotate your tools.** Mark read-only vs destructive. This helps agents (and humans) understand the risk of each operation.

6. **Don't over-build.** Start with the 5-10 most common operations. Add more based on actual usage, not speculation.

## Finding Existing MCP Servers

Before building your own, check if one already exists:

- **[MCP Server Registry](https://github.com/modelcontextprotocol/servers)** — Official directory of community MCP servers
- **[Smithery](https://smithery.ai/)** — MCP server marketplace
- **npm** — Search for `mcp-server-{service}` or `{service}-mcp`
- **PyPI** — Search for `{service}-mcp` or `{service}_mcp`

Common existing servers: GitHub, Slack, Google Drive, Postgres, SQLite, Brave Search, Puppeteer, and many more.

## MCP vs Other Integration Patterns

| Pattern | Complexity | Flexibility | Best For |
|---------|-----------|-------------|----------|
| **CLI + Skill** | Low | High | Services with good CLIs (`gws`, `stripe`, `gh`) |
| **curl + Skill** | Low | Medium | Simple REST APIs (< 10 endpoints) |
| **MCP Server** | Medium | Very High | Complex integrations, multi-agent, real-time |
| **Custom Code** | High | Highest | Unique workflows that don't fit patterns |

**This repo's philosophy:** Start simple (CLI + skill), upgrade to MCP only when you hit a wall. Most SMB needs are well-served by CLIs and skills.

## Related Skills

- `google-workspace` — Example of CLI + skill pattern (uses `gws` CLI, no MCP needed)
- `secrets-manager` — Secure credential storage (needed by MCP servers too)
- `slack` — Example of API + skill pattern (curl calls, no MCP needed)

## External Resources

- [MCP Specification](https://modelcontextprotocol.io/) — The official protocol spec
- [Anthropic MCP Builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) — Official skill for building MCP servers
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers) — Directory of existing servers
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) — Official TypeScript implementation
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk) — Official Python implementation

---

*Understand the tool before you reach for it. Sometimes a screwdriver is better than a power drill.*

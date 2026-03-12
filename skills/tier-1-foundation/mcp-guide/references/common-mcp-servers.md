# Common MCP Servers for SMBs

Before building your own, check if one of these existing servers covers your need. These are well-maintained, widely-used MCP servers from the community.

## Official / High-Quality Servers

### Communication
| Service | MCP Server | Install |
|---------|-----------|---------|
| Slack | `@modelcontextprotocol/server-slack` | `npx @modelcontextprotocol/server-slack` |
| Google Maps | `@modelcontextprotocol/server-google-maps` | `npx @modelcontextprotocol/server-google-maps` |

### Data & Databases
| Service | MCP Server | Install |
|---------|-----------|---------|
| PostgreSQL | `@modelcontextprotocol/server-postgres` | `npx @modelcontextprotocol/server-postgres` |
| SQLite | `@modelcontextprotocol/server-sqlite` | `npx @modelcontextprotocol/server-sqlite` |

### Development
| Service | MCP Server | Install |
|---------|-----------|---------|
| GitHub | `@modelcontextprotocol/server-github` | `npx @modelcontextprotocol/server-github` |
| Git | `@modelcontextprotocol/server-git` | `npx @modelcontextprotocol/server-git` |

### Web & Search
| Service | MCP Server | Install |
|---------|-----------|---------|
| Brave Search | `@modelcontextprotocol/server-brave-search` | `npx @modelcontextprotocol/server-brave-search` |
| Puppeteer | `@modelcontextprotocol/server-puppeteer` | `npx @modelcontextprotocol/server-puppeteer` |
| Fetch | `@modelcontextprotocol/server-fetch` | `npx @modelcontextprotocol/server-fetch` |

### File Systems
| Service | MCP Server | Install |
|---------|-----------|---------|
| Filesystem | `@modelcontextprotocol/server-filesystem` | `npx @modelcontextprotocol/server-filesystem` |
| Google Drive | `@modelcontextprotocol/server-gdrive` | `npx @modelcontextprotocol/server-gdrive` |

## Finding More

- **Official Registry:** [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- **Smithery Marketplace:** [smithery.ai](https://smithery.ai/)
- **npm search:** `npm search mcp-server`
- **PyPI search:** Search for `mcp` on pypi.org

## When to Use a Community MCP vs CLI + Skill

| Situation | Recommendation |
|-----------|---------------|
| Good CLI exists (gws, stripe, gh) | **CLI + skill** — simpler, less infra |
| Community MCP server exists and is well-maintained | **Community MCP** — saves you building from scratch |
| No CLI, no MCP, simple API | **curl + skill** — write API patterns in a skill |
| No CLI, no MCP, complex API | **Build your own MCP** — use the mcp-builder skill |

## Configuring MCP Servers in Claude Code

Add to your Claude Code settings (`~/.claude/settings.json` or project `.claude/settings.json`):

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost/dbname"]
    }
  }
}
```

## Configuring MCP Servers in Other Agents

Each agent has its own MCP configuration format. Check your agent's docs:
- **Cline:** `.cline/mcp_settings.json`
- **Cursor:** Settings → MCP
- **Windsurf:** Similar to Cursor
- **Custom agents:** Use the MCP TypeScript or Python SDK to build a client

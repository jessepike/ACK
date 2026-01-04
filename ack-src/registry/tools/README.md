---
doc_id: "doc-001"
slug: "mcp-inventory"
title: "MCP Servers Inventory"
type: "artifact_registry"
tier: "tier1"
status: "active"
authority: "binding"
version: "0.2.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-02"
owner: "human"
depends_on: []
---

# MCP Servers Inventory

Comprehensive inventory of MCP servers for the Claude Registry.

## Currently Configured

| Server | Source | Purpose | Config Type |
|--------|--------|---------|-------------|
| Railway | `railwayapp/railway-mcp-server` | Deployment management | URL |
| Supabase | `supabase-community/supabase-mcp` | Database/Auth/RLS | HTTP |
| Context7 | `upstash/context7` | Library documentation | stdio |
| Playwright | `@anthropic/mcp-playwright` | Browser testing | stdio |

## Available Servers (To Add)

### Development & Deployment

| Server | Repo | Purpose |
|--------|------|---------|
| **GitHub** | `github/github-mcp-server` | Repos, PRs, Issues, Actions |
| **Vercel** | (check registry) | Deployment, serverless |

### Database & Storage

| Server | Repo | Purpose |
|--------|------|---------|
| **PostgreSQL** | `stuzero/pg-mcp-server` | Direct Postgres access |
| **ChromaDB** | `meloncafe/chromadb-remote-mcp` | Vector database |
| **SQLite Memory** | `Daichi-Kudo/mcp-memory-sqlite` | Persistent memory |

### Web & Scraping

| Server | Repo | Purpose |
|--------|------|---------|
| **Firecrawl** | `firecrawl/firecrawl-mcp-server` | Web scraping, crawling |
| **Claude in Chrome** | Anthropic built-in | Browser automation agent |

### Productivity

| Server | Repo | Purpose |
|--------|------|---------|
| **Google Tasks** | `arpitbatra123/mcp-googletasks` | Task management |

### API & Integration

| Server | Repo | Purpose |
|--------|------|---------|
| **FastAPI** | `tadata-org/fastapi_mcp` | FastAPI integration |
| **Magic MCP** | `21st-dev/magic-mcp` | UI component generation |

## MCP Server Registries

Official and community registries to discover more servers:

| Registry | URL |
|----------|-----|
| **Official MCP Registry** | https://registry.modelcontextprotocol.io |
| **Awesome MCP Servers** | https://github.com/wong2/awesome-mcp-servers |
| **Reference Implementations** | https://github.com/modelcontextprotocol/servers |

## Configuration Templates

### URL-based (OAuth flow)
```json
{
  "mcpServers": {
    "Railway": {
      "type": "url",
      "url": "https://mcp.railway.com/sse"
    }
  }
}
```

### HTTP-based (OAuth flow)
```json
{
  "mcpServers": {
    "supabase": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp"
    }
  }
}
```

### stdio-based (local npx)
```json
{
  "mcpServers": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

### stdio-based (local binary)
```json
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "github-mcp-server",
      "args": [],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## Full Template (.mcp.json)

```json
{
  "mcpServers": {
    "Railway": {
      "type": "url",
      "url": "https://mcp.railway.com/sse"
    },
    "supabase": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp"
    },
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@anthropic/mcp-playwright"]
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## Claude in Chrome

Per Anthropic documentation:
- https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome
- Browser automation agent
- Appears in MCP list when Chrome extension connected
- Used for web browsing tasks

## MCP vs CLI Decision Guide

| Use MCP When | Use CLI When |
|--------------|--------------|
| Querying data | Local development |
| Real-time operations | Streaming logs |
| OAuth-protected APIs | File operations |
| Structured responses | Complex shell pipelines |
| Direct API access | Offline/air-gapped |

## Adding New Servers

1. Find server in registry or awesome-mcp-servers
2. Determine config type (url, http, stdio)
3. Add to project `.mcp.json`
4. Test connection with `/mcp` command
5. Document in this inventory

---

## Review & Change History

**Current Version:** 0.2.0
**Review Status:** draft

### Changes Since Last Review
- Added comprehensive server inventory from user research
- Added MCP registries
- Added configuration templates
- Added Claude in Chrome reference

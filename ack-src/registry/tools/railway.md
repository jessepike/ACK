# Railway Tool Spec

## MCP Server (Primary)

type: mcp
name: railway
source: Built-in to Claude Code (via gateway)

### Configuration
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

### Capabilities via MCP
- List projects and services
- View deployment status
- Read logs
- Manage environment variables
- Trigger deployments
- View metrics

### Authentication
OAuth flow — Claude will prompt to connect your Railway account on first use.

---

## CLI (Supplementary)

type: cli
name: railway-cli
binary: railway
install: npm install -g @railway/cli
docs: https://docs.railway.app/guides/cli

### When to Use CLI vs MCP

| Task | Use |
|------|-----|
| View deployments | MCP |
| Read logs | MCP (or CLI for streaming) |
| Set env variables | MCP |
| Trigger deploy | MCP |
| Local development with Railway env | CLI (`railway run`) |
| Link project locally | CLI (`railway link`) |

### CLI Commands (When MCP Unavailable)
```bash
railway login               # Auth
railway link                # Link project
railway up                  # Deploy
railway logs                # Stream logs
railway variables           # List env vars
railway run <cmd>           # Run with Railway env
```

---

## Scripts

Location: `skills/railway/scripts/` (if needed)

Example diagnostic script:
```bash
#!/bin/bash
# scripts/railway-diagnose.sh
railway status
railway deployments list --limit 3
railway logs --latest | tail -50
```

---

## Documentation Sources

When stuck, reference:
- Official docs: https://docs.railway.app
- CLI reference: https://docs.railway.app/guides/cli
- Deployment troubleshooting: https://docs.railway.app/guides/deployments
- Nixpacks (builder): https://nixpacks.com/docs

Use Context7 MCP or WebFetch to pull current documentation when needed.

---
type: domain
description: "Railway Domain Package"
version: 0.1.0
updated: "2026-01-04T09:26:12"
---

# Railway Domain Package

**Purpose:** Deploy, debug, and manage Railway services

## Components

### Agent: `railway-expert`
Senior Railway specialist. Knows deployment patterns, debugging workflows, Nixpacks builds. Uses MCP first, CLI fallback.

**Invoked when:** Deployment fails, need to check logs, manage services, configure environments.

### Skill: `railway/SKILL.md`
Procedural knowledge:
- CLI command reference
- Debugging decision tree (build vs runtime vs network failures)
- Configuration templates (`railway.json`, `railway.toml`)
- Common fixes (port binding, health checks, database connections)

### Tool: `railway.md`
- **MCP Server:** `https://mcp.railway.com/sse` — Primary. Query deployments, logs, variables directly.
- **CLI:** `railway` — For local dev (`railway run`), linking projects, streaming logs.
- **Scripts:** Diagnostic scripts if needed.

### Command: `railway-debug`
Trigger: `/railway-debug` or "railway deploy failing"

Workflow:
1. Check MCP connection
2. List recent deployments
3. Pull logs from failed deployment
4. Analyze against known patterns
5. Apply fix
6. Verify deployment succeeds

## Quick Start

```bash
# In your project
ln -s ~/code/tools/claude-registry/agents/railway-expert.md .claude/agents/
ln -s ~/code/tools/claude-registry/commands/railway-debug.md .claude/commands/

# Add to .mcp.json
{
  "mcpServers": {
    "Railway": {
      "type": "url",
      "url": "https://mcp.railway.com/sse"
    }
  }
}
```

## Documentation Sources
- https://docs.railway.app
- https://docs.railway.app/guides/cli
- https://docs.railway.app/guides/deployments
- https://nixpacks.com/docs

## When to Use
- Deployment failed
- Need to check service logs
- Configure environment variables
- Debug build errors
- Set up custom domains
- Scale services

# Claude Registry

Central repository for AI agent primitives.

**Location:** `~/code/tools/claude-registry`

## Quick Start

```bash
# In any project
mkdir -p .claude/agents .claude/commands
ln -s ~/code/tools/claude-registry/agents/*.md .claude/agents/
ln -s ~/code/tools/claude-registry/commands/*.md .claude/commands/
cp ~/code/tools/claude-registry/templates/mcp-base.json .mcp.json
```

## Current Inventory

### Domains (Complete Packages)

| Domain | Agent | Skill | Tool | Command |
|--------|-------|-------|------|---------|
| Railway | ✅ railway-expert | ✅ railway/SKILL.md | ✅ MCP + CLI | ✅ /railway-debug |
| Supabase | ✅ supabase-expert | ✅ supabase/SKILL.md | ✅ MCP + CLI | ✅ /supabase-debug |
| Next.js | ✅ nextjs-expert | ✅ nextjs/SKILL.md | ✅ CLI only | ✅ /nextjs-debug |

See `domains/` folder for human-readable summaries of each package.

### MCP Servers

| Server | URL/Command |
|--------|-------------|
| Railway | `https://mcp.railway.com/sse` |
| Supabase | `https://mcp.supabase.com/mcp` |
| Context7 | `npx @context7/mcp-server` |
| Playwright | `npx @anthropic/mcp-playwright` |

See `docs/MCP_INVENTORY.md` for full details.

## Directory Structure

```
claude-registry/
├── agents/           # Domain experts (WHO)
├── skills/           # Procedural knowledge (HOW)
├── tools/            # MCP/CLI/Script specs (WHAT)
├── commands/         # Slash triggers (WHEN)
├── prompts/          # Reusable templates
├── policies/         # Constraints/guards
├── domains/          # Human-readable package summaries
├── docs/             # Reference documentation
│   ├── PRIMITIVES.md # Primitive types explained
│   └── MCP_INVENTORY.md # All MCP servers
└── templates/        # Project scaffolds
    ├── mcp-base.json # Starter MCP config
    └── PROJECT_INTEGRATION.md
```

## When to Use What

| I need to... | Use |
|--------------|-----|
| Debug Railway deploy | `/railway-debug` |
| Debug Supabase query | `/supabase-debug` |
| Debug Next.js build | `/nextjs-debug` |
| Design database schema | Ask supabase-expert |
| Understand App Router | Ask nextjs-expert |
| Know exact CLI commands | Check skill or tool spec |

## Documentation

- `docs/PRIMITIVES.md` — What agents, skills, tools, commands are
- `docs/MCP_INVENTORY.md` — All MCP servers and configs
- `domains/*.md` — Human-readable domain summaries

## Adding New Domains

1. Create agent: `agents/{domain}-expert.md`
2. Create skill: `skills/{domain}/SKILL.md`
3. Create tool spec: `tools/{domain}.md`
4. Create command: `commands/{domain}-debug.md`
5. Create domain summary: `domains/{DOMAIN}.md`
6. Update MCP inventory if needed

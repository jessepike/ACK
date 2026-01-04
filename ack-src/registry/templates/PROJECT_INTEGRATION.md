# Project Integration Guide

How to use the central registry in your projects.

## Quick Start

```bash
# In your project root
mkdir -p .claude/agents .claude/commands

# Symlink Railway stack
ln -s ~/code/tools/registry/agents/railway-expert.md .claude/agents/
ln -s ~/code/tools/registry/commands/railway-debug.md .claude/commands/

# Copy MCP config (modify as needed)
cp ~/code/tools/registry/templates/mcp-base.json .mcp.json
```

## Directory Structure in Project

```
your-project/
├── .claude/
│   ├── agents/
│   │   └── railway-expert.md -> ~/code/tools/registry/agents/railway-expert.md
│   ├── commands/
│   │   └── railway-debug.md -> ~/code/tools/registry/commands/railway-debug.md
│   └── settings.json        # Project-specific settings
├── .mcp.json                 # MCP server configuration
├── CLAUDE.md                 # Project-specific context
└── ... your code
```

## CLAUDE.md Template

```markdown
# Project: {name}

## Stack
- Framework: Next.js 14
- Database: Supabase PostgreSQL
- Hosting: Railway
- Auth: Supabase Auth

## Active Agents
- railway-expert: Deployment and debugging

## Key Commands
- /railway-debug: Debug deployment failures

## Project-Specific Context
{Add project-specific notes here}
```

## Symlink vs Copy

**Symlink (Recommended):**
- Updates automatically when registry changes
- Single source of truth
- Use for stable primitives

**Copy:**
- Project-specific modifications
- Isolated from registry changes
- Use when customization needed

## Verify Integration

```bash
# Check Claude Code sees your agents
claude --print-agents

# Check commands
claude --print-commands

# Test MCP servers
claude /mcp status
```

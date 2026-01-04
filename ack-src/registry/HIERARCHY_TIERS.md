---
doc_id: "guide-002"
slug: "hierarchy-tiers"
title: "Agent Context Registry Hierarchy"
type: "research_note"
tier: "tier1"
status: "active"
authority: "binding"
version: "0.1.0"
review_status: "draft"
created: "2026-01-02"
updated: "2026-01-02"
owner: "human"
depends_on: []
---

# Agent Context Registry Hierarchy

Defines which primitives (MCP servers, agents, skills, tools) live at which level.

## Three-Tier Hierarchy

Mirrors Claude Code's CLAUDE.md hierarchy and Mem0 tier structure.

```
┌─────────────────────────────────────────────────────────┐
│ GLOBAL (User Level)                                     │
│ ~/.claude/ or ~/.config/agent-context-registry/         │
│ Every project inherits these                            │
├─────────────────────────────────────────────────────────┤
│ DOMAIN (Shared)                                         │
│ ~/code/tools/agent-context-registry/domains/            │
│ Opt-in per project via symlinks                         │
├─────────────────────────────────────────────────────────┤
│ PROJECT (Local)                                         │
│ project/.claude/ or project/.agent-context/             │
│ Project-specific only                                   │
└─────────────────────────────────────────────────────────┘
```

## Tier Definitions

### Global Tier (Every Project)

**Criteria:** Used in 90%+ of projects, universal utility.

**MCP Servers:**
| Server | Why Global |
|--------|------------|
| Context7 | Library docs — every project needs references |
| Claude in Chrome | Browser automation — universal capability |
| Sequential Thinking | Reasoning enhancement — always beneficial |
| GitHub | Version control — every project uses git |

**Agents:** None at global (too project-specific)

**Skills:** 
- Code review patterns
- Commit message standards
- Documentation templates

**Tools:**
- Git CLI patterns
- Common shell utilities

### Domain Tier (Opt-In Shared)

**Criteria:** Used by multiple projects sharing a technology stack.

**Domains Defined:**
| Domain | Projects Using |
|--------|----------------|
| Railway | Any Railway-deployed project |
| Supabase | Any Supabase-backed project |
| Next.js | Any Next.js frontend |
| LangChain | Any LangChain/LangGraph project |
| Python | Any Python project |
| TypeScript | Any TS project |

**Per Domain Package:**
- 1 Agent (domain expert)
- 1 Skill (procedural knowledge)
- 1 Tool (MCP or CLI spec)
- N Commands (domain-specific workflows)

**Integration:** Symlink domain folder into project `.claude/`

### Project Tier (Local Only)

**Criteria:** Specific to one project, not reusable.

**Examples:**
- Project-specific agents (e.g., "RiskTools Expert")
- Custom skills for proprietary workflows
- Environment-specific tool configs
- Project policies and constraints

## MCP Server Placement

### Global MCP Config (~/.claude/mcp.json)

```json
{
  "mcpServers": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "claude-in-chrome": {
      "note": "Configured via Chrome extension"
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

### Project MCP Config (project/.mcp.json)

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
    }
  }
}
```

## Directory Structure

### Global Registry

```
~/code/tools/agent-context-registry/
├── global/                    # Global tier primitives
│   ├── mcp-global.json        # Global MCP config
│   ├── skills/
│   │   ├── code-review/
│   │   └── commit-standards/
│   └── prompts/
│       ├── commit-message.md
│       └── pr-description.md
├── domains/                   # Domain tier packages
│   ├── railway/
│   │   ├── RAILWAY.md
│   │   ├── agents/railway-expert.md
│   │   ├── skills/railway/SKILL.md
│   │   ├── tools/railway.md
│   │   └── commands/railway-debug.md
│   ├── supabase/
│   ├── nextjs/
│   ├── github/
│   └── langchain/
├── docs/                      # Reference documentation
├── templates/                 # Project setup templates
└── scripts/                   # Utility scripts
```

### Project Integration

```
project/
├── .claude/
│   ├── CLAUDE.md
│   ├── settings.json
│   └── domains/              # Symlinks to registry
│       ├── railway -> ~/code/tools/agent-context-registry/domains/railway
│       └── supabase -> ~/code/tools/agent-context-registry/domains/supabase
└── .mcp.json                 # Project MCP config (extends global)
```

## Integration Commands

### Add Domain to Project

```bash
# Create symlink
ln -s ~/code/tools/agent-context-registry/domains/railway project/.claude/domains/railway

# Or use a setup script (future)
acr add-domain railway
```

### List Available Domains

```bash
ls ~/code/tools/agent-context-registry/domains/
```

### Check What's Active

```bash
ls -la project/.claude/domains/
```

## Decision Guide

| Question | Answer → Tier |
|----------|---------------|
| Does every project need this? | Global |
| Is this technology-stack specific? | Domain |
| Is this only for this one project? | Project |
| Will I reuse this in similar projects? | Domain |
| Is this a universal best practice? | Global |

## Migration Path

1. **Current state:** Everything in flat registry
2. **Next:** Reorganize into global/domains structure
3. **Then:** Create project integration tooling
4. **Finally:** Document onboarding for new projects

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation defining three-tier hierarchy

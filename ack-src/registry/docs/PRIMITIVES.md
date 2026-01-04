---
type: guide
description: "Primitives Reference"
version: 0.1.0
updated: "2026-01-04T09:26:12"
---

# Primitives Reference

Quick reference for understanding and using the Claude Registry.

## The Six Primitives

| Primitive | What It Is | File Location | When It's Used |
|-----------|-----------|---------------|----------------|
| **Agent** | Domain expert identity with personality and decision-making | `agents/{name}.md` | Invoked by name or auto-matched by Claude |
| **Skill** | Procedural how-to knowledge (steps, commands, patterns) | `skills/{domain}/SKILL.md` | Agent loads it, or matches task keywords |
| **Tool** | External system Claude can invoke (MCP, CLI, or Script) | `tools/{name}.md` | When agent/skill needs to execute actions |
| **Command** | Slash-triggered workflow | `commands/{name}.md` | User types `/command-name` |
| **Prompt** | Reusable instruction template | `prompts/{name}.md` | Command or agent references it |
| **Policy** | Constraint/guard rules | `policies/{name}.md` | Always active, limits behavior |

## Tool Types

Tools can be:

| Type | Example | How Claude Uses It |
|------|---------|-------------------|
| **MCP Server** | Supabase, Railway | Direct API calls via MCP protocol |
| **CLI** | `railway`, `supabase`, `npm` | Via Bash tool |
| **Script** | `scripts/diagnose.sh` | Via Bash tool |

## Hierarchy

```
User invokes Command
    ↓
Command activates Agent
    ↓
Agent loads relevant Skill(s)
    ↓
Skill references Tool(s)
    ↓
Tool executes (MCP/CLI/Script)
```

Or directly:
- User asks question → Claude matches Agent → Agent uses Skills/Tools
- User runs `/command` → Command orchestrates everything

## File Format

### Agent (agents/example-expert.md)
```markdown
---
name: example-expert
description: One line for Claude to match on
tools: Read, Write, Edit, Bash, Grep, Glob, mcp__toolname
---

You are a [role] specialist with expertise in...

## Context Gathering
[What to check first]

## Common Patterns
[Typical solutions]

## Debugging Workflow
[Step-by-step approach]

## Communication Protocol
[How to report findings]
```

### Skill (skills/example/SKILL.md)
```markdown
---
name: example
description: What procedures this contains
version: 1.0.0
---

# Skill Name

## Prerequisites
[What's needed before using]

## Quick Reference
[Command cheatsheet]

## Decision Trees
[If X then Y logic]

## Common Fixes
[Code templates]
```

### Tool (tools/example.md)
```markdown
# Tool Name

## MCP Server (if available)
type: mcp
url: https://...

## CLI (if available)
type: cli
binary: command-name
install: npm install -g ...

## When to Use MCP vs CLI
[Decision guide]

## Documentation Sources
[URLs for reference]
```

### Command (commands/example.md)
```markdown
---
name: example-command
triggers:
  - /example-command
  - natural language trigger
description: What this workflow does
---

# Command Name

## Workflow
[High-level steps]

## Execution Steps
[Detailed procedure]

## Output Format
[Expected output structure]
```

## Quick Decision Guide

**I need to...**

| Task | Use |
|------|-----|
| Debug a deployment | Command (e.g., `/railway-debug`) |
| Ask about design patterns | Agent (e.g., "ask supabase-expert") |
| Know exact steps for X | Skill (procedures) |
| Know what commands exist | Tool spec |
| Trigger a multi-step workflow | Command |
| Apply constraints to all tasks | Policy |

## Adding to Projects

```bash
# Create Claude directory
mkdir -p .claude/agents .claude/commands

# Symlink from registry
ln -s ~/code/tools/claude-registry/agents/railway-expert.md .claude/agents/
ln -s ~/code/tools/claude-registry/commands/railway-debug.md .claude/commands/

# Add MCP servers to .mcp.json
```

Claude Code auto-discovers:
- `.claude/agents/*.md`
- `.claude/commands/*.md`
- `.mcp.json` (if `enableAllProjectMcpServers: true`)

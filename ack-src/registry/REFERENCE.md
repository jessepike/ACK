# Claude Registry Reference

Quick reference for primitives, conventions, and usage patterns.

## Primitive Definitions

| Primitive | What It Is | When It's Used | Example |
|-----------|-----------|----------------|---------|
| **Agent** | Domain expert with personality, decision-making, context awareness | Invoked by name or auto-matched by Claude based on task | `railway-expert`, `supabase-expert` |
| **Skill** | Procedural knowledge — steps, commands, decision trees, patterns | Agent loads it, or matches task keywords in description | `railway/SKILL.md`, `supabase/SKILL.md` |
| **Tool** | System boundary Claude can invoke (MCP server, CLI, or script) | When agent/skill needs to execute actions outside Claude | `Railway MCP`, `supabase-cli`, `deploy.sh` |
| **Command** | Slash-triggered workflow that orchestrates agent + skill + tool | User types `/railway-debug` or similar trigger | `/railway-debug`, `/supabase-debug` |
| **Prompt** | Reusable instruction template for specific outputs | Command or agent references it for consistent output format | `commit-message.md`, `pr-description.md` |
| **Policy** | Constraint rules, guard rails, behavioral limits | Always active — limits what agents can/cannot do | `no-force-push.md`, `require-tests.md` |

## Tool Types

| Type | Description | How Claude Uses It |
|------|-------------|-------------------|
| **MCP Server** | Model Context Protocol — direct integration | Claude calls tools directly via MCP protocol |
| **CLI** | Command-line interface | Claude executes via Bash tool |
| **Script** | Custom automation (bash, python, etc.) | Claude executes via Bash tool |

## Hierarchy: How Primitives Compose

```
User invokes Command (/railway-debug)
    │
    ▼
Command activates Agent (railway-expert)
    │
    ▼
Agent loads relevant Skill (railway/SKILL.md)
    │
    ▼
Skill references Tool (Railway MCP or CLI)
    │
    ▼
Tool executes action (deploy, get logs, etc.)
    │
    ▼
Agent reports back using Prompt template (if defined)
```

## File Naming Conventions

| Primitive | Location | Naming Pattern |
|-----------|----------|----------------|
| Agent | `agents/` | `{domain}-expert.md` or `{role}.md` |
| Skill | `skills/{domain}/` | `SKILL.md` (with optional `scripts/`) |
| Tool | `tools/` | `{tool-name}.md` |
| Command | `commands/` | `{action}.md` or `{domain}-{action}.md` |
| Prompt | `prompts/` | `{output-type}.md` |
| Policy | `policies/` | `{constraint}.md` |

## Agent Manifest Format

```markdown
---
name: domain-expert
description: One line for Claude to match on (keep concise)
tools: Read, Write, Edit, Bash, Grep, Glob, mcp__toolname
---

You are a [role] specialist with expertise in...

## Context Gathering
What to check before starting work

## Common Patterns
Reusable solutions for frequent tasks

## Debugging Workflow
Step-by-step troubleshooting approach

## Communication Protocol
How to report findings and verify fixes
```

## Skill Format

```markdown
---
name: skill-name
description: What procedures this contains
version: 1.0.0
---

# Skill Name

## Prerequisites
What must be installed/configured

## Quick Reference
Common commands and patterns

## Decision Trees
If X then Y flowcharts for troubleshooting

## Common Fixes
Code snippets for frequent issues
```

## Command Format

```markdown
---
name: command-name
triggers:
  - /command-name
  - natural language trigger phrase
description: What this workflow does
---

# Command Name

## Workflow
High-level steps this command performs

## Execution Steps
Detailed step-by-step instructions

## Output Format
Template for how to report results
```

## Documentation Lookup Pattern

When an agent needs current documentation:

1. **Context7 MCP** (preferred): `"Use Context7 to look up [topic]"`
2. **WebFetch**: Direct URL fetch if you know the docs location
3. **WebSearch**: Search for documentation if URL unknown

Add to agent's Context Gathering section:
```markdown
## Context Gathering
...
If stuck or need current docs:
- Use Context7: "Look up [framework] [topic] documentation"
- Or fetch directly: https://docs.[framework].com/[topic]
```

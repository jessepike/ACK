# IPE Minimal Structure
## Bare Minimum Files and Folders

**Philosophy:** Just enough structure to stay organized. No bureaucracy.

---

## Folder Structure

```
project/
├── CLAUDE.md                 # Agent memory - loaded automatically
├── agents.md                 # Agent-specific instructions (optional, can merge into CLAUDE.md)
│
├── .context/                 # Project context (human + agent readable)
│   ├── intent.md             # What we're building and why
│   ├── decisions.md          # Key decisions with rationale
│   ├── constraints.md        # Technical and business constraints
│   └── current-focus.md      # What we're working on NOW
│
├── .environment/             # Project environment configuration
│   ├── manifest.md           # What agents, tools, dependencies this project needs
│   └── setup.md              # Setup steps (manual for now)
│
├── .agents/                  # Agent configurations and skills (simple folder)
│   ├── skills/               # Reusable prompts/skills
│   │   └── [skill-name].md
│   └── configs/              # Agent-specific configs if needed
│       └── [agent-name].md
│
├── .drift/                   # Drift detection (future - can ignore for MVP)
│   └── baseline.md           # What "correct" looks like
│
└── scripts/                  # Helper scripts (optional)
    └── inject-context.sh     # Combines context for non-IDE agents
```

---

## Core Files

### CLAUDE.md (Required)

This is your agent memory. Auto-loaded by Claude Code, Cursor, etc.

```markdown
# Project: [Name]

## What This Is
[1-2 sentences: what we're building]

## Current Status
[What phase we're in, what's in progress]

## Key Decisions
- [Decision 1]: [rationale]
- [Decision 2]: [rationale]

## Constraints
- [Technical constraint]
- [Business constraint]
- [Scope constraint]

## How to Work on This Project
- [Instruction 1]
- [Instruction 2]
- [Instruction 3]

## What NOT to Do
- [Anti-pattern 1]
- [Anti-pattern 2]

## Current Focus
[What we're working on RIGHT NOW - update frequently]

---
Last updated: [date]
```

### .context/intent.md

The "why" document. Rarely changes after initial definition.

```markdown
# Intent: [Project Name]

## The Problem
[What problem are we solving? Why does it matter?]

## The Solution
[High-level: what are we building to solve it?]

## Success Looks Like
[How do we know when we've succeeded?]

## Non-Goals
[What are we explicitly NOT doing?]
```

### .context/decisions.md

Append-only log of key decisions.

```markdown
# Decisions Log

## [Date]: [Decision Title]
**Decision:** [What we decided]
**Rationale:** [Why]
**Alternatives Considered:** [What else we looked at]
**Status:** Active | Superseded by [link]

---

## [Date]: [Decision Title]
...
```

### .context/constraints.md

Boundaries the project operates within.

```markdown
# Constraints

## Technical
- [e.g., Must run on Node 20+]
- [e.g., No external API dependencies for MVP]

## Business
- [e.g., Must be usable by non-technical users]
- [e.g., Budget: $0 for infrastructure initially]

## Scope
- [e.g., Solo developer only - no team features]
- [e.g., MVP in 4 weeks]

## Dependencies
- [e.g., Requires Supabase account]
- [e.g., Depends on Anthropic API access]
```

### .context/current-focus.md

What's happening NOW. Update frequently (daily or per session).

```markdown
# Current Focus

**Updated:** [date/time]

## Working On
[What you're actively building/solving]

## Blocked By
[Anything stopping progress]

## Next Up
[What comes after current task]

## Recent Completions
- [x] [Thing done]
- [x] [Thing done]
```

### .environment/manifest.md

What this project needs to run.

```markdown
# Environment Manifest: [Project Name]

## Agents
| Agent | Purpose | Required? |
|-------|---------|-----------|
| Claude Sonnet | Primary coding | Yes |
| Claude Opus | Complex reasoning, review | No |
| GPT-4 | Alternative perspective | No |

## Tools / MCP Servers
| Tool | Purpose | Required? |
|------|---------|-----------|
| mcp-filesystem | File operations | Yes |
| mcp-github | Repo management | Yes |
| mcp-postgres | Database access | No |

## Skills Needed
| Skill | Location | Notes |
|-------|----------|-------|
| spec-driven-dev | .agents/skills/spec-driven.md | Core workflow |
| code-review | .agents/skills/review.md | PR reviews |

## Dependencies
| Type | Name | Version | Notes |
|------|------|---------|-------|
| Runtime | Node.js | >=20 | Required |
| Package Manager | pnpm | >=8 | Preferred |
| Database | Supabase | - | Cloud hosted |
| Framework | Next.js | 14 | App router |

## Setup Checklist
- [ ] Clone repo
- [ ] Run `pnpm install`
- [ ] Copy `.env.example` to `.env.local`
- [ ] Configure Supabase connection
- [ ] Enable MCP servers in Claude
```

### .environment/setup.md

Detailed setup steps if manifest checklist isn't enough.

```markdown
# Setup Guide: [Project Name]

## Prerequisites
[What you need before starting]

## Step-by-Step Setup

### 1. [Step Name]
[Detailed instructions]

### 2. [Step Name]
[Detailed instructions]

## Verification
[How to confirm everything is working]

## Troubleshooting
[Common issues and fixes]
```

---

## Agent/Skill Selection Framework

When starting a project, answer these questions:

### 1. What kind of project is this?
- [ ] Web app (frontend + backend)
- [ ] CLI tool
- [ ] Library/package
- [ ] Data pipeline
- [ ] Automation/scripts
- [ ] Documentation
- [ ] Other: ___

### 2. What's the complexity?
- [ ] Simple (single component, well-defined)
- [ ] Medium (multiple components, some unknowns)
- [ ] Complex (many components, significant unknowns)
- [ ] Exploratory (figuring it out as we go)

### 3. What agents do I need?
| Need | Agent | Why |
|------|-------|-----|
| Primary coding | Claude Sonnet | Fast, capable, cost-effective |
| Complex reasoning | Claude Opus | When Sonnet isn't enough |
| Research | Gemini/Perplexity | Web search, deep research |
| Alternative view | GPT-4 | Second opinion on architecture |
| Code review | [Any] | Catch what you missed |

### 4. What tools/integrations?
- [ ] File system access (mcp-filesystem)
- [ ] Git/GitHub (mcp-github)
- [ ] Database (mcp-postgres, mcp-supabase)
- [ ] Web search (built-in or mcp)
- [ ] Browser automation (mcp-puppeteer)
- [ ] Other: ___

### 5. What skills/workflows?
- [ ] Spec-driven development
- [ ] Test-driven development
- [ ] PR-based workflow
- [ ] Documentation-first
- [ ] Other: ___

---

## What You DON'T Need Yet

- Drift detection automation
- Memory database
- Formal gates or stages
- Change orders
- Version hashing
- Plugins

Add these when you feel the pain, not before.

---

## Quick Start

1. Create the folder structure
2. Fill in CLAUDE.md with project basics
3. Fill in intent.md with the "why"
4. Fill in manifest.md with what you need
5. Start working

Update current-focus.md and decisions.md as you go. That's it.

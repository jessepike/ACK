---
doc_id: "doc-002"
slug: "builtin-commands-reference"
title: "Built-in vs Custom Commands Reference"
type: "research_note"
tier: "tier2"
status: "active"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "2026-01-02"
updated: "2026-01-02"
owner: "human"
depends_on: []
---

# Built-in vs Custom Commands Reference

Reference for understanding what Claude Code provides natively vs what requires custom commands.

## Built-in Commands (Don't Recreate)

| Command | Purpose |
|---------|---------|
| `/add-dir` | Add additional working directories |
| `/agents` | Manage custom AI subagents |
| `/bashes` | List and manage background tasks |
| `/bug` | Report bugs |
| `/clear` | Clear conversation history |
| `/compact` | Compact conversation |
| `/config` | Open Settings |
| `/context` | Visualize context usage |
| `/cost` | Show token usage |
| `/doctor` | Check installation health |
| `/exit` | Exit REPL |
| `/export` | Export conversation |
| `/help` | Get usage help |
| `/hooks` | Manage hook configurations |
| `/ide` | Manage IDE integrations |
| `/init` | Initialize project with CLAUDE.md |
| `/install-github-app` | Set up GitHub Actions |
| `/login` / `/logout` | Account management |
| `/mcp` | Manage MCP connections |
| `/memory` | Edit CLAUDE.md memory files |
| `/model` | Select AI model |
| `/output-style` | Set output style |
| `/permissions` | View/update permissions |
| `/plugin` | Manage plugins |
| `/pr-comments` | View PR comments |
| `/privacy-settings` | Privacy settings |
| `/release-notes` | View release notes |
| `/resume` | Resume conversation |
| `/review` | **Request code review** |
| `/rewind` | Rewind conversation/code |
| `/sandbox` | Enable sandboxed bash |
| `/security-review` | **Security review of changes** |
| `/status` | Show version, model, account |
| `/statusline` | Set up status line UI |
| `/terminal-setup` | Install key bindings |
| `/todos` | List todo items |
| `/usage` | Show plan usage limits |
| `/vim` | Enter vim mode |

## Custom Commands (Add Value)

Commands we created that are NOT built-in:

| Command | Purpose | Status |
|---------|---------|--------|
| `/commit` | Generate conventional commit message | ✅ Active |
| `/pr` | Generate PR description | ✅ Active |
| `/branch` | Generate branch name | ✅ Active |
| `/railway-debug` | Debug Railway deployments | ✅ Active |
| `/supabase-debug` | Debug Supabase issues | ✅ Active |
| `/nextjs-debug` | Debug Next.js builds | ✅ Active |

## Deprecated Commands

Commands that overlap with built-ins:

| Command | Reason | Alternative |
|---------|--------|-------------|
| `/review` (custom) | Built-in `/review` exists | Use built-in `/review` |

## Key Insight from Community

> "Commands were removed for things Claude already does well"
> — hikarubw/claude-commands

Focus custom commands on:
1. Domain-specific workflows (railway-debug, supabase-debug)
2. Standardized formats (commit, pr, branch with your conventions)
3. Multi-step orchestration Claude can't do natively

## Skills vs Slash Commands

| Use Slash Commands | Use Skills |
|--------------------|------------|
| Quick, frequent prompts | Complex capabilities |
| Single .md file | Directory with resources |
| Explicit invocation | Automatic discovery |
| Simple templates | Scripts, validation, multi-file |

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation based on Claude Code docs research

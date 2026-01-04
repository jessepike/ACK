---
type: tool
description: "GitHub Tool"
version: 0.1.0
updated: 2026-01-02
status: active
depends_on: []
doc_id: tool-004
slug: github
title: "GitHub Tool"
tier: tier1
authority: binding
review_status: draft
created: 2026-01-02
owner: human
---

# GitHub Tool

GitHub integration via MCP server and CLI.

## MCP Server (Primary)

**Server:** `@modelcontextprotocol/server-github`  
**Tier:** Global (every project)

### Configuration

```json
{
  "mcpServers": {
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

### Setup

1. Create GitHub Personal Access Token (PAT)
   - Settings → Developer settings → Personal access tokens
   - Scopes needed: `repo`, `workflow`, `read:org`

2. Set environment variable:
   ```bash
   export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
   ```

3. Add to global MCP config: `~/.claude/mcp.json`

### Available Tools

| Tool | Description |
|------|-------------|
| `list_repositories` | List repos for user/org |
| `get_repository` | Get repo details |
| `create_repository` | Create new repo |
| `list_pull_requests` | List PRs |
| `get_pull_request` | PR details |
| `create_pull_request` | Create PR |
| `list_issues` | List issues |
| `get_issue` | Issue details |
| `create_issue` | Create issue |
| `list_branches` | List branches |
| `get_file_contents` | Read file from repo |

## CLI Fallback

**Tool:** GitHub CLI (`gh`)  
**Docs:** https://cli.github.com/manual/

### Installation

```bash
# macOS
brew install gh

# Authenticate
gh auth login
```

### Common Commands

```bash
# Repos
gh repo view
gh repo clone owner/repo
gh repo create name --public

# PRs
gh pr create --title "title" --body "body"
gh pr list
gh pr view 123
gh pr checkout 123
gh pr merge 123 --squash

# Issues
gh issue create --title "title"
gh issue list
gh issue view 123

# Actions
gh workflow list
gh run list
gh run view 12345 --log
```

## When to Use Which

| Scenario | Use |
|----------|-----|
| Query repo/PR/issue data | MCP |
| Create PR with complex body | CLI |
| Bulk operations | MCP |
| Interactive review | CLI |
| Check workflow status | Either |
| Trigger workflow | CLI |

## Authentication

### MCP
Requires `GITHUB_TOKEN` environment variable with PAT.

### CLI
```bash
gh auth login
gh auth status
```

## Rate Limits

- **Authenticated:** 5,000 requests/hour
- **GraphQL:** 5,000 points/hour (queries cost 1+ points)

Check status:
```bash
gh api rate_limit
```

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation

---
name: github
description: >
  GitHub workflow procedures for repository management, pull requests, issues, 
  and Actions CI/CD. Use when performing GitHub operations, setting up repos,
  configuring workflows, or managing PRs and issues.

doc_id: "skill-004"
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

# GitHub Skill

Procedural knowledge for GitHub operations.

## Repository Setup

### New Repo Checklist

1. Create repo with appropriate visibility
2. Add `.gitignore` for stack
3. Configure branch protection on `main`
4. Set up required status checks
5. Add CODEOWNERS if team project
6. Create initial README

### Branch Protection Rules

```bash
# Via CLI (requires admin)
gh api repos/{owner}/{repo}/branches/main/protection -X PUT -F required_status_checks='{"strict":true,"contexts":["ci"]}' -F enforce_admins=false -F required_pull_request_reviews='{"required_approving_review_count":1}'
```

**Standard rules:**
- Require PR before merge
- Require status checks to pass
- Require conversation resolution
- Do not allow force pushes

## Pull Request Workflow

### Create PR

```bash
# Feature PR
gh pr create --title "feat: add user auth" --body-file .github/PULL_REQUEST_TEMPLATE.md

# With reviewers
gh pr create --title "feat: add user auth" --reviewer @username

# Draft PR
gh pr create --draft --title "WIP: user auth"
```

### PR Description Template

```markdown
## Summary
Brief description of changes.

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests pass
- [ ] Manual testing done

## Related
- Closes #123
```

### Review PR

```bash
# View PR
gh pr view 123

# Check out PR locally
gh pr checkout 123

# Approve
gh pr review 123 --approve

# Request changes
gh pr review 123 --request-changes --body "Need to fix X"
```

### Merge Strategies

| Strategy | When to Use |
|----------|-------------|
| Squash | Feature branches, clean history |
| Merge | Release branches, preserve commits |
| Rebase | Linear history preference |

```bash
gh pr merge 123 --squash --delete-branch
```

## Issue Management

### Create Issue

```bash
gh issue create --title "Bug: login fails" --body "Steps to reproduce..." --label bug
```

### Issue Templates

Store in `.github/ISSUE_TEMPLATE/`:
- `bug_report.md`
- `feature_request.md`

### Link PR to Issue

In PR body:
```
Closes #123
Fixes #456
Resolves #789
```

## GitHub Actions

### Basic Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
```

### Common Triggers

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    types: [opened, synchronize, reopened]
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:  # Manual trigger
```

### Workflow Commands

```bash
# List workflows
gh workflow list

# View workflow runs
gh run list

# Trigger workflow
gh workflow run ci.yml

# View run logs
gh run view 12345 --log
```

## GitHub API via MCP

### Available Operations

The GitHub MCP server provides:
- `list_repositories` — List user/org repos
- `get_repository` — Repo details
- `create_pull_request` — Create PR
- `list_pull_requests` — List PRs
- `get_issue` — Issue details
- `create_issue` — Create issue

### When to Use MCP vs CLI

| Use MCP | Use CLI |
|---------|---------|
| Queries, listings | Complex mutations |
| Status checks | Interactive operations |
| Bulk operations | Local repo operations |

## Troubleshooting

### PR Checks Failing

1. Check workflow logs: `gh run view --log-failed`
2. Re-run failed jobs: `gh run rerun 12345 --failed`
3. Check branch is up to date with base

### Merge Conflicts

```bash
# Update branch
git fetch origin main
git rebase origin/main
# or
gh pr merge --rebase
```

### Actions Not Triggering

- Check workflow file syntax
- Verify trigger conditions match
- Check repo Actions permissions
- Review workflow run history

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation

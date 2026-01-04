---
doc_id: "cmd-008"
slug: "github-debug"
title: "GitHub Debug Command"
type: "command"
tier: "tier2"
status: "active"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "2026-01-02"
updated: "2026-01-02"
owner: "human"
depends_on: ["agent-004", "skill-004", "tool-004"]
triggers:
  - /github-debug
  - github not working
  - PR failing
  - actions failing
  - workflow error
---

# GitHub Debug Command

Diagnose GitHub issues: auth, PRs, Actions, API.

## Workflow

### 1. Identify Problem Category

Ask: What's failing?
- Authentication / permissions
- Pull request issues
- Actions / workflow failures  
- API rate limits
- Repository access

### 2. Run Diagnostics

**Auth Check:**
```bash
gh auth status
gh api user
```

**Rate Limit Check:**
```bash
gh api rate_limit --jq '.resources.core'
```

**Repo Access:**
```bash
gh repo view --json name,visibility,permissions
```

**PR Status:**
```bash
gh pr status
gh pr checks
```

**Actions Status:**
```bash
gh run list --limit 5
gh run view --log-failed
```

### 3. Common Fixes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| 401 Unauthorized | Token expired/invalid | `gh auth login` |
| 403 Forbidden | Missing scope | Regenerate PAT with required scopes |
| 404 Not Found | Wrong repo/no access | Check repo name, permissions |
| Rate limited | Too many requests | Wait or use authenticated requests |
| PR checks failing | CI error | `gh run view --log-failed` |
| Actions not running | Workflow disabled | Check repo Actions settings |

### 4. Escalation

If basic diagnostics don't resolve:

1. Check GitHub Status: https://githubstatus.com
2. Review audit log (org): Settings → Audit log
3. Check webhook deliveries: Settings → Webhooks
4. Contact repo admin for permission issues

## Output

Provide:
1. Diagnosis summary
2. Root cause identified
3. Specific fix commands
4. Verification steps

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation

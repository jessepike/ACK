---
doc_id: "cmd-006"
slug: "branch"
title: "Branch Command"
type: "command"
tier: "tier2"
status: "active"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: ["prompt-005"]
triggers:
  - /branch
  - create branch
  - new branch name
---

# Branch Command

Generate consistent, descriptive branch name.

## Workflow

1. Get task description
2. Identify type and ticket
3. Apply branch-name prompt template
4. Output formatted name and optionally create

## Execution

Ask for:
- What are you working on?
- Is there a ticket number?

## Apply Prompt

Reference: `prompts/branch-name.md`

## Output Format

```
Suggested branch: feat/42-user-profile-page

Create it? (y/n)
```

If yes:
```bash
git checkout -b <branch-name>
```

## Examples

Input: "Add user profile page, ticket #42"
Output: `feat/42-user-profile-page`

Input: "Fix the null pointer bug in API response"
Output: `fix/null-response-handling`

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation

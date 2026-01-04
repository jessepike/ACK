---
type: prompt
description: "Branch Name Prompt"
version: 0.1.0
updated: 2026-01-01
status: active
depends_on: []
doc_id: prompt-005
slug: branch-name
title: "Branch Name Prompt"
tier: tier2
authority: guidance
review_status: draft
created: 2026-01-01
owner: human
---

# Branch Name Prompt

Generate consistent, descriptive branch names.

## Format

```
<type>/<ticket>-<short-description>
```

## Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructure |
| `docs` | Documentation |
| `test` | Test additions |
| `chore` | Maintenance |

## Rules

1. Lowercase only
2. Use hyphens, not underscores
3. Include ticket number if exists
4. Keep description to 3-5 words
5. Be specific, not generic

## Examples

```
feat/42-user-profile-page
fix/87-null-response-handling
refactor/api-error-handling
docs/setup-instructions
chore/upgrade-nextjs-14
feat/AUTH-123-oauth-login
```

## Anti-patterns

```
❌ feature-branch
❌ my-changes
❌ fix_stuff
❌ FEAT-42-Add-User-Profile-Page
❌ feat/42
```

## Instructions for Claude

1. Ask for ticket number if not provided
2. Determine type from task description
3. Extract 3-5 key words
4. Combine in format: `type/ticket-key-words`

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation

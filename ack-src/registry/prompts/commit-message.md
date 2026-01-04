---
doc_id: "prompt-001"
slug: "commit-message"
title: "Commit Message Prompt"
type: "prompt"
tier: "tier2"
status: "active"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: []
---

# Commit Message Prompt

Generate a commit message following Conventional Commits format.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `perf` | Performance improvement |
| `test` | Adding/fixing tests |
| `chore` | Build, config, dependencies |

## Rules

1. Subject line ≤50 characters
2. Use imperative mood ("add" not "added")
3. No period at end of subject
4. Scope is optional but helpful
5. Body explains what/why, not how
6. Reference issues in footer

## Examples

```
feat(auth): add OAuth2 login flow

Implement Google and GitHub OAuth providers using NextAuth.
Includes session management and token refresh.

Closes #42
```

```
fix(api): handle null response from external service

External API occasionally returns null instead of empty array.
Added defensive check to prevent runtime error.

Fixes #87
```

```
chore(deps): upgrade Next.js to 14.1.0
```

## Instructions for Claude

1. Run `git diff --staged` to see changes
2. Analyze what changed and why
3. Determine appropriate type and scope
4. Write subject line (imperative, ≤50 chars)
5. Add body if changes need explanation
6. Reference related issues if known

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation

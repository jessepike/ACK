---
type: artifact
stage: setup
artifact: git-workflow
description: "Git branching strategy and PR workflow (support artifact)"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Git Workflow

## Purpose

<!-- Document git branching strategy and PR workflow -->

This document captures the git workflow, branching strategy, and pull request process for [Project Name].

**Git hosting:** [GitHub / GitLab / Bitbucket]

**Primary branch:** `main`

---

## Branching Strategy

### Branch Types

| Branch Type | Pattern | Purpose | Lifetime |
|-------------|---------|---------|----------|
| Main | `main` | Production-ready code | Permanent |
| Develop | `develop` | Integration branch | Permanent |
| Feature | `feature/[name]` | New features | Until merged |
| Fix | `fix/[name]` | Bug fixes | Until merged |
| Chore | `chore/[name]` | Maintenance tasks | Until merged |
| Release | `release/[version]` | Release preparation | Until merged |
| Hotfix | `hotfix/[name]` | Emergency fixes | Until merged |

### Branch Flow

```
main ─────────────────────────────────────────▶
       │                    ▲
       │                    │ (merge release)
       ▼                    │
develop ──────────────────────────────────────▶
       │        ▲     ▲     │
       │        │     │     │
       ▼        │     │     ▼
feature/x ──────┘     │
                      │
fix/y ────────────────┘
```

### Simple Flow (Alternative)

For smaller projects, use trunk-based development:

```
main ─────────────────────────────────────────▶
       │        ▲     │        ▲
       │        │     │        │
       ▼        │     ▼        │
feature/x ──────┘     fix/y ───┘
```

---

## Branch Naming Convention

### Format

```
[type]/[short-description]
```

### Examples

| Type | Example | When to Use |
|------|---------|-------------|
| feature | `feature/user-authentication` | New functionality |
| fix | `fix/login-validation-error` | Bug fixes |
| chore | `chore/update-dependencies` | Maintenance |
| refactor | `refactor/user-service` | Code restructuring |
| docs | `docs/api-documentation` | Documentation only |
| test | `test/user-api-coverage` | Test additions |

### Naming Rules

- Use lowercase letters
- Use hyphens for spaces (not underscores)
- Keep names concise but descriptive
- Include ticket ID if applicable: `feature/PROJ-123-user-auth`

---

## Commit Messages

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |

### Examples

```bash
# Simple commit
feat(auth): add password reset functionality

# With body
fix(api): handle null user in profile endpoint

The profile endpoint was throwing an error when user was not found.
Added null check and proper 404 response.

Fixes #123

# Breaking change
feat(api)!: change user response format

BREAKING CHANGE: User object now returns `fullName` instead of `name`
```

---

## Pull Request Process

### PR Template

**File:** `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Summary

<!-- Brief description of changes -->

## Changes

- [ ] Change 1
- [ ] Change 2

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update

## Testing

<!-- How has this been tested? -->

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist

- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have commented hard-to-understand areas
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] Tests pass locally
```

### PR Workflow

```
1. Create branch from develop/main
   └── git checkout -b feature/my-feature

2. Make changes and commit
   └── git commit -m "feat: add new feature"

3. Push branch
   └── git push -u origin feature/my-feature

4. Open PR
   └── Fill out PR template
   └── Assign reviewers

5. Address feedback
   └── Make requested changes
   └── Push updates

6. Merge
   └── Squash and merge (preferred)
   └── Delete branch
```

### PR Requirements

| Requirement | Required? | Notes |
|-------------|-----------|-------|
| Approval from reviewer | Yes | At least 1 approval |
| All checks passing | Yes | CI must be green |
| Up to date with base | Yes | Must merge/rebase |
| Linked issue | Recommended | Reference issue number |
| Description complete | Yes | Explain what and why |

---

## Code Review Guidelines

### For Authors

1. **Keep PRs small** - Aim for < 400 lines changed
2. **Self-review first** - Check your own code before requesting review
3. **Write good descriptions** - Explain context and decisions
4. **Respond promptly** - Address feedback quickly
5. **Don't take it personally** - Feedback is about code, not you

### For Reviewers

1. **Be timely** - Review within 24 hours
2. **Be constructive** - Suggest improvements, don't just criticize
3. **Ask questions** - If unclear, ask rather than assume
4. **Approve when ready** - Don't block on nitpicks
5. **Use suggestions** - GitHub suggestions make fixes easy

### Review Checklist

- [ ] Code is readable and well-structured
- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] Tests cover changes
- [ ] No security issues
- [ ] No performance concerns
- [ ] Documentation updated if needed

---

## Merge Strategy

### Options

| Strategy | When to Use | Result |
|----------|-------------|--------|
| Squash and merge | Most PRs | Single commit on target |
| Merge commit | Large features | Preserves commit history |
| Rebase and merge | Clean history needed | Linear history |

### Recommended: Squash and Merge

- Creates clean, linear history
- Each PR = one commit
- Easy to revert if needed

---

## Conflict Resolution

### Resolving Conflicts

```bash
# Update your branch with latest from base
git fetch origin
git checkout feature/my-feature
git rebase origin/develop

# Or merge approach
git merge origin/develop

# Resolve conflicts in files
# Then continue
git add .
git rebase --continue  # or git commit

# Push (force if rebased)
git push --force-with-lease
```

### Prevention

- Keep branches short-lived
- Communicate about shared files
- Merge/rebase frequently from base branch

---

## Branch Protection

### Main Branch Rules

```yaml
# GitHub branch protection settings
branches:
  main:
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
        dismiss_stale_reviews: true
      required_status_checks:
        strict: true
        contexts:
          - lint
          - test
          - build
      enforce_admins: true
      restrictions: null
```

### Develop Branch Rules (if used)

```yaml
branches:
  develop:
    protection:
      required_status_checks:
        strict: true
        contexts:
          - lint
          - test
```

---

## Release Process

### Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR - Breaking changes
MINOR - New features (backward compatible)
PATCH - Bug fixes (backward compatible)
```

### Release Workflow

```bash
# 1. Create release branch
git checkout develop
git pull
git checkout -b release/v1.2.0

# 2. Update version
npm version 1.2.0 --no-git-tag-version
# Update CHANGELOG.md

# 3. Create PR to main
git push -u origin release/v1.2.0
# Create PR: release/v1.2.0 → main

# 4. After merge, tag release
git checkout main
git pull
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# 5. Merge back to develop
git checkout develop
git merge main
git push
```

---

## Hotfix Process

```bash
# 1. Create hotfix from main
git checkout main
git pull
git checkout -b hotfix/critical-bug

# 2. Fix and commit
git commit -m "fix: resolve critical bug"

# 3. Create PR to main (expedited review)
git push -u origin hotfix/critical-bug

# 4. After merge, tag and deploy
git checkout main
git pull
git tag -a v1.2.1 -m "Hotfix v1.2.1"
git push origin v1.2.1

# 5. Merge to develop
git checkout develop
git merge main
git push
```

---

## Git Hooks (Optional)

### Pre-commit Hook

**File:** `.husky/pre-commit`

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm run lint-staged
```

### Commit-msg Hook

**File:** `.husky/commit-msg`

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx --no -- commitlint --edit "$1"
```

### Setup

```bash
npm install husky lint-staged @commitlint/cli @commitlint/config-conventional -D
npx husky install
```

---

## Git Workflow Checklist

### Initial Setup

- [ ] Repository created
- [ ] Branch protection configured
- [ ] PR template added
- [ ] Team access configured

### Daily Workflow

- [ ] Pull latest before starting work
- [ ] Create feature branch with proper naming
- [ ] Make atomic commits with good messages
- [ ] Push regularly
- [ ] Open PR when ready

### PR Process

- [ ] Fill out PR template completely
- [ ] Request appropriate reviewers
- [ ] Address feedback promptly
- [ ] Ensure CI passes
- [ ] Merge using agreed strategy

---

## Related Documents

- [ci-cd.md](ci-cd.md) - CI/CD pipeline
- [repo-init.md](repo-init.md) - Repository setup
- [tasks-*.md](tasks-product.md) - Task management (commit after each task)

---
type: artifact
stage: setup
artifact: git-workflow
description: "Branch strategy, PR process, and code review guidelines"
version: "1.0.0"
status: draft
---

# [Project Name] - Git Workflow

## Branch Strategy

### Model: [GitHub Flow / Git Flow / Trunk-Based]

**Rationale:** [Why this model was chosen]

---

## Branch Types

| Branch Pattern | Purpose | Base Branch | Merge Target |
|----------------|---------|-------------|--------------|
| `main` | Production-ready code | - | - |
| `develop` | Integration branch (if using Git Flow) | `main` | `main` |
| `feature/[name]` | New features | `[main/develop]` | `[main/develop]` |
| `fix/[name]` | Bug fixes | `[main/develop]` | `[main/develop]` |
| `hotfix/[name]` | Production hotfixes | `main` | `main` |
| `release/[version]` | Release preparation (if using Git Flow) | `develop` | `main` + `develop` |

---

## Branch Naming Convention

```
[type]/[ticket-id]-[short-description]
```

**Examples:**
- `feature/ACK-123-add-user-auth`
- `fix/ACK-456-login-redirect`
- `hotfix/ACK-789-critical-security-patch`

### Naming Rules
- Use lowercase
- Use hyphens (not underscores)
- Keep descriptions short but meaningful
- Include ticket/issue ID when applicable

---

## Commit Messages

### Format

```
[type]([scope]): [short description]

[optional body]

[optional footer]
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code refactoring |
| `test` | Adding/updating tests |
| `chore` | Build, config, tooling |

### Examples

```
feat(auth): add OAuth2 login support

Implements Google and GitHub OAuth providers.
Closes #123

---

fix(api): handle null response from payment gateway

Previously would throw TypeError. Now returns empty array.
```

---

## Pull Request Process

### 1. Before Creating PR

- [ ] Branch is up to date with base branch
- [ ] All tests pass locally
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if needed)

### 2. PR Title Format

```
[Type]: [Short description] (#[ticket-id])
```

**Examples:**
- `feat: Add user authentication (#123)`
- `fix: Resolve login redirect loop (#456)`

### 3. PR Description Template

```markdown
## Summary
[Brief description of changes]

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
- [ ] Other: [describe]

## Changes Made
- [Change 1]
- [Change 2]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Related Issues
Closes #[issue-number]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

---

## Code Review Guidelines

### For Reviewers

**Review for:**
- [ ] Correctness - Does the code do what it's supposed to?
- [ ] Clarity - Is the code readable and well-documented?
- [ ] Security - Are there any security concerns?
- [ ] Performance - Are there obvious performance issues?
- [ ] Testing - Is the code adequately tested?

**Review etiquette:**
- Be constructive and specific
- Ask questions rather than make demands
- Distinguish between required changes and suggestions
- Approve when satisfied, don't block on nitpicks

### For Authors

- Respond to all comments
- Mark conversations resolved when addressed
- Re-request review after changes
- Keep PRs focused and reasonably sized

---

## Merge Rules

### Required Before Merge

- [ ] Minimum [X] approving review(s)
- [ ] All CI checks pass
- [ ] No unresolved conversations
- [ ] Branch is up to date with base
- [ ] [Additional requirements]

### Merge Strategy

**Primary:** [Squash and merge / Merge commit / Rebase and merge]

**Rationale:** [Why this strategy]

### After Merge

- [ ] Delete feature branch
- [ ] Verify deployment (if auto-deploy)
- [ ] Close related issues
- [ ] Update project board/tracker

---

## Branch Protection Rules

### `main` Branch

- [ ] Require pull request before merging
- [ ] Require [X] approval(s)
- [ ] Require status checks to pass
- [ ] Require branches to be up to date
- [ ] Require conversation resolution
- [ ] No force pushes
- [ ] No deletions

### `develop` Branch (if applicable)

- [ ] Require pull request before merging
- [ ] Require [X] approval(s)
- [ ] Require status checks to pass

---

## Release Process

### Version Numbering

**Scheme:** [Semantic Versioning (MAJOR.MINOR.PATCH)]

- **MAJOR:** Breaking changes
- **MINOR:** New features, backward compatible
- **PATCH:** Bug fixes, backward compatible

### Release Steps

1. [ ] Create release branch (if using Git Flow)
2. [ ] Update version number
3. [ ] Update CHANGELOG
4. [ ] Create PR to main
5. [ ] Merge after approval
6. [ ] Create GitHub release/tag
7. [ ] Deploy to production
8. [ ] Announce release

### Tagging

```bash
git tag -a v[X.Y.Z] -m "Release v[X.Y.Z]"
git push origin v[X.Y.Z]
```

---

## Hotfix Process

For critical production issues:

1. [ ] Create `hotfix/[name]` from `main`
2. [ ] Implement fix
3. [ ] Create PR directly to `main`
4. [ ] Fast-track review (expedited approval)
5. [ ] Merge and deploy
6. [ ] Back-merge to `develop` (if applicable)

---

## Setup Checklist

### Phase 1: Branch Protection
- [ ] Configure `main` branch protection
- [ ] Configure `develop` protection (if applicable)
- [ ] Set required reviewers

### Phase 2: Templates
- [ ] Create PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
- [ ] Create issue templates (optional)

### Phase 3: Documentation
- [ ] Document workflow in README or CONTRIBUTING.md
- [ ] Share with team

---

## Open Questions

- [ ] [Git workflow question 1]
- [ ] [Git workflow question 2]

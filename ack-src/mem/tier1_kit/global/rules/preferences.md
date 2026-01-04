---
type: rule_preferences
description: "User Preferences"
version: 1.0.0
updated: 2026-01-02
status: active
doc_id: rule-global-002
title: Preferences
owner: human
created: 2026-01-02
---

# User Preferences

## Purpose

Personal style, formatting, and tool preferences across all projects.

## Rules

### Languages
- **Primary Web:** TypeScript (strict mode)
- **Primary Scripts/Data:** Python 3.10+
- **Formatting:** Strict (Prettier for TS/JS, Black for Python)

### Code Style
- Comments explain *why*, not *what*
- Prefer `const` over `let`, never `var`
- Use async/await over raw promises
- Destructure imports when possible
- Explicit return types on functions

### Git
- Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`
- Atomic commits (one logical change per commit)
- Branch naming: `feature/`, `fix/`, `chore/`
- Rebase over merge for feature branches

### Documentation
- README.md for every project
- Inline JSDoc/docstrings for public APIs
- ADRs for significant architectural decisions
- CHANGELOG.md for user-facing changes

### Testing
- Write tests for new features
- Test edge cases and error paths
- Prefer integration tests over excessive mocking

---

## Review & Change History

**Current Version:** 1.0.0
**Review Status:** accepted

### Changes Since Last Review
- Initial creation with AGS-aligned frontmatter

---
type: rule_stack
description: "Stack Rules"
version: 0.1.0
updated: 2026-01-02
status: draft
doc_id: rule-project-002
title: "Stack Rules"
owner: human
created: 2026-01-02
---

# Stack Rules

## Purpose

Technology-specific conventions and rules for this project's tech stack.

## Rules

### [Primary Framework]
1. [Framework-specific conventions]

### TypeScript/JavaScript
- Use `const` over `let`, avoid `var`
- Use async/await over raw promises
- Strict type checking enabled
- Explicit return types on exported functions

### CSS/Styling
- [Tailwind | CSS Modules | Styled Components]
- Avoid global style pollution
- [Project-specific styling rules]

### Database
- [ORM conventions]
- [Query patterns]
- [Migration rules]

### API
- [REST | GraphQL conventions]
- [Error handling patterns]
- [Authentication approach]

## Dependencies
- Prefer stable, well-maintained packages
- Document reason for any experimental dependencies
- Lock versions in package.json/requirements.txt

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Template initialization

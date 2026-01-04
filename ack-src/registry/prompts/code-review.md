---
type: prompt
description: "Code Review Prompt"
version: 0.1.0
updated: 2026-01-01
status: active
depends_on: []
doc_id: prompt-003
slug: code-review
title: "Code Review Prompt"
tier: tier2
authority: guidance
review_status: draft
created: 2026-01-01
owner: human
---

# Code Review Prompt

Perform thorough code review with actionable feedback.

## Review Checklist

### Correctness
- [ ] Does the code do what it claims?
- [ ] Are edge cases handled?
- [ ] Are errors handled appropriately?

### Security
- [ ] Input validation present?
- [ ] SQL injection prevented?
- [ ] Auth/authz checked?
- [ ] Sensitive data protected?

### Performance
- [ ] N+1 queries avoided?
- [ ] Unnecessary re-renders prevented?
- [ ] Large data sets paginated?

### Maintainability
- [ ] Code is readable without comments?
- [ ] Functions are single-purpose?
- [ ] No magic numbers/strings?
- [ ] Types are accurate?

### Testing
- [ ] Tests cover happy path?
- [ ] Tests cover edge cases?
- [ ] Tests are maintainable?

## Feedback Format

```markdown
## Summary
[Approve | Request Changes | Comment]

## Must Fix
- **[File:Line]** Issue description
  ```suggestion
  // suggested fix
  ```

## Should Fix
- **[File:Line]** Issue description

## Nitpicks
- **[File:Line]** Minor suggestion

## Questions
- [Clarifying questions]

## Praise
- [What's done well]
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **Must Fix** | Bug, security, broken functionality | Block merge |
| **Should Fix** | Code smell, performance, maintainability | Fix before/soon after merge |
| **Nitpick** | Style, naming, minor improvements | Optional |

## Instructions for Claude

1. Read the full diff to understand scope
2. Run through checklist systematically
3. Prioritize feedback by severity
4. Provide concrete suggestions, not vague complaints
5. Acknowledge good patterns
6. Ask questions when intent unclear

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation

---
doc_id: "rule-global-003"
title: "Workflows"
type: "rule_workflow"
status: "active"
version: "1.0.0"
owner: "human"
created: "2026-01-02"
updated: "2026-01-02"
---

# Workflow Patterns

## Purpose

Cross-project process patterns and development workflow guidance.

## Rules

### Development Flow
1. Understand requirements before coding
2. Plan approach for non-trivial changes
3. Write tests for new features
4. Run linting/typecheck before commit
5. Self-review diff before pushing

### Task Completion Protocol
1. Complete task as specified
2. Verify acceptance criteria met
3. Run relevant tests
4. Commit with conventional message
5. Update task tracking if exists

### When Blocked
1. **STOP** — Do not improvise alternative approaches
2. Document the blocker clearly
3. Note what was attempted
4. Identify what decision is needed
5. Wait for human input

### Deviation Protocol
If task cannot be completed as specified:
1. Stop immediately
2. Document issue with attempted solutions
3. Alert human via clear message
4. Propose alternatives if obvious
5. Wait for decision before proceeding

### Code Review Checklist
- Correctness: Does it do what it should?
- Clarity: Is the intent obvious?
- Edge cases: Are errors handled?
- Tests: Is new code covered?
- Security: Any new attack surface?

---

## Review & Change History

**Current Version:** 1.0.0
**Review Status:** accepted

### Changes Since Last Review
- Initial creation with AGS-aligned frontmatter

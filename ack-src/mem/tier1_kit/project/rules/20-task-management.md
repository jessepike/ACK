---
type: rule
description: "Task and Plan Management - Hard Requirements"
version: 1.0.0
updated: "2026-01-04T00:00:00"
priority: high
---

# Task Management Rules

These rules are **mandatory** for all agent work during the Develop stage.

## Task Lifecycle (MUST follow exactly)

### Before Starting ANY Task

1. **Locate** the next pending task `[ ]` in tasks file
2. **Mark** the task as in-progress `[~]`
3. **Save** the tasks file immediately
4. **Then** begin work on the task

### After Completing ANY Task

1. **Mark** the task as complete `[x]`
2. **Document** any decisions made (inline with task)
3. **Save** the tasks file immediately
4. **Commit** all changes with task reference
5. **Then** move to next task

### Status Symbols

| Symbol | Meaning | When to Use |
|--------|---------|-------------|
| `[ ]` | Pending | Not started |
| `[~]` | In Progress | Currently working |
| `[x]` | Complete | Finished successfully |
| `[!]` | Blocked | Cannot proceed |
| `[-]` | Skipped | Intentionally not done |

## Commit Rules

### Commit Timing

- **ALWAYS** commit after each completed task
- **NEVER** batch multiple tasks into one commit
- **NEVER** commit incomplete or broken code

### Commit Message Format

```
[Phase X.Y] Task description

- What was implemented
- Decisions made (if any)
```

For features:
```
[Feature: Name] Task description
```

For projects:
```
[Project: Name] Task description
```

## Checkpoint Rules

### At Every Checkpoint

1. **STOP** - Do not continue to next phase
2. **Summarize** for human review:
   - Tasks completed
   - Decisions made
   - Blockers encountered
   - Deviations from plan
3. **WAIT** for explicit human approval
4. **Then** proceed only after approval

### Never Skip Checkpoints

- Checkpoints exist for human oversight
- No amount of confidence justifies skipping
- If unsure whether to stop, STOP

## Decision Documentation

### Minor Decisions (inline)

```markdown
- [x] Implement authentication
  - **Decision:** Used JWT over sessions
  - **Rationale:** Stateless, better for scaling
```

### Major Decisions (ADR)

Create an ADR when the decision:
- Affects multiple components
- Is difficult to reverse
- Will be referenced often
- Needs detailed context

## Blocker Protocol

When blocked:

1. **Mark** task as `[!]`
2. **Document** what's blocking
3. **Do NOT** skip to other tasks (unless explicitly unrelated)
4. **Flag** for human attention
5. **Wait** for resolution or guidance

## Scope Discipline

### Before Each Task

- Verify task is in-scope per brief.md
- If task seems out of scope, STOP and verify
- Do not add features not in the plan

### If Scope Question Arises

1. Check brief.md scope boundaries
2. If clearly out of scope: skip with `[-]` and note
3. If unclear: STOP and ask human

## Files to Keep Updated

| File | Update When |
|------|-------------|
| `tasks.md` | Every task start/complete |
| `plan.md` | Checkpoint summaries (optional) |
| `CLAUDE.md` | Current focus section |

## Summary: The Non-Negotiables

1. **Mark in-progress before starting**
2. **Mark complete after finishing**
3. **Commit after every task**
4. **Stop at every checkpoint**
5. **Document every decision**
6. **Never skip blockers**

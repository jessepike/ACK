---
type: artifact
stage: setup
artifact: tasks
scope: project
description: "Task breakdown for administrative, documentation, or meta work"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Project Tasks

## Scope

**Type:** Project (administrative, documentation, or organizational work)

**Plan reference:** [plan-project.md](plan-project.md)

---

## Hard Requirements

These rules are **mandatory** and must be followed exactly.

### Task Lifecycle

```
BEFORE starting a task:
  1. Find the next pending task [ ]
  2. Mark it in-progress [~]
  3. Save the file
  4. Begin work

AFTER completing a task:
  1. Mark it complete [x]
  2. Add decision notes if any decisions were made
  3. Save the file
  4. Commit changes (if files were modified)
  5. Move to next task
```

### Status Symbols

| Symbol | Meaning | When to Use |
|--------|---------|-------------|
| `[ ]` | Pending | Task not yet started |
| `[~]` | In Progress | Currently working on this task |
| `[x]` | Complete | Task finished successfully |
| `[!]` | Blocked | Cannot proceed - document why |
| `[-]` | Skipped | Intentionally not done - document why |

### Commit Requirement

**Commit after EVERY completed task that changes files.**

```bash
# Format
git commit -m "[Project: Name] Task description"
```

Note: Unlike product/feature tasks, project tasks may not always produce file changes. Only commit when files are actually modified.

### Decision Documentation

When making a decision during a task, add it inline:

```markdown
- [x] Define naming convention
  - **Decision:** Used {artifact}-{scope}.md pattern
  - **Rationale:** Consistent, scannable, groups related files
```

---

## Progress Summary

| Area | Total | Complete | In Progress | Blocked |
|------|-------|----------|-------------|---------|
| [Area 1] | 0 | 0 | 0 | 0 |
| [Area 2] | 0 | 0 | 0 | 0 |
| [Area 3] | 0 | 0 | 0 | 0 |
| **Total** | **0** | **0** | **0** | **0** |

---

## Area 1: [Work Area Name]

**Goal:** [What this area accomplishes]

**Deliverables:** [What gets created]

### Tasks

- [ ] [Task 1 - specific action]
- [ ] [Task 2 - specific action]
- [ ] [Task 3 - specific action]
- [ ] [Task 4 - specific action]

### Area 1 Complete

- [ ] All tasks finished
- [ ] Deliverables verified

---

## Area 2: [Work Area Name]

**Goal:** [What this area accomplishes]

**Deliverables:** [What gets created]

### Tasks

- [ ] [Task 1 - specific action]
- [ ] [Task 2 - specific action]
- [ ] [Task 3 - specific action]
- [ ] [Task 4 - specific action]

### Area 2 Complete

- [ ] All tasks finished
- [ ] Deliverables verified

---

## Area 3: [Work Area Name]

**Goal:** [What this area accomplishes]

**Deliverables:** [What gets created]

### Tasks

- [ ] [Task 1 - specific action]
- [ ] [Task 2 - specific action]
- [ ] [Task 3 - specific action]
- [ ] [Task 4 - specific action]

### Area 3 Complete

- [ ] All tasks finished
- [ ] Deliverables verified

---

## Checkpoint

**STOP here for human review.**

- [ ] **All tasks complete**
- [ ] **All deliverables created**
- [ ] **Quality verified**
- [ ] **Documentation clear**

---

## Blocked Tasks

| Task | Area | Blocked By | Resolution Needed |
|------|------|------------|-------------------|
| | | | |

---

## Decisions Log

### [YYYY-MM-DD] - [Decision Topic]

**Context:** [Why decision was needed]

**Chosen:** [What was decided and why]

---

## Completion Checklist

Before marking project complete:

- [ ] All tasks marked `[x]` or `[-]` (with reason)
- [ ] All blocked tasks resolved
- [ ] All deliverables created and verified
- [ ] Checkpoint approved by human

---

## Related Documents

- [plan-project.md](plan-project.md) - Project plan
- [Other relevant documents]

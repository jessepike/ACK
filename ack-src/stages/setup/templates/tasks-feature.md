---
type: artifact
stage: setup
artifact: tasks
scope: feature
description: "Task breakdown for single feature implementation"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Feature Name] - Feature Tasks

## Scope

**Type:** Feature (single capability within existing product)

**Plan reference:** [plan-feature.md](plan-feature.md)

**Parent product:** [Product name if applicable]

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
  4. Commit changes with task reference
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

**Commit after EVERY completed task.**

```bash
# Format
git commit -m "[Feature: Name] Task description"
```

### Decision Documentation

When making a decision during a task, add it inline:

```markdown
- [x] Implement caching layer
  - **Decision:** Used Redis over in-memory
  - **Rationale:** Persists across restarts, scales horizontally
```

---

## Progress Summary

| Step | Total | Complete | In Progress | Blocked |
|------|-------|----------|-------------|---------|
| 1 - Setup | 0 | 0 | 0 | 0 |
| 2 - Implementation | 0 | 0 | 0 | 0 |
| 3 - Integration | 0 | 0 | 0 | 0 |
| **Total** | **0** | **0** | **0** | **0** |

---

## Step 1: Setup & Preparation

**Goal:** Prepare for feature implementation

### 1.1 Research & Planning

- [ ] Review existing code that feature will integrate with
- [ ] Identify components to modify
- [ ] Identify new components to create
- [ ] Confirm approach (or document decision)

### 1.2 Setup

- [ ] Create feature branch (if using branches)
- [ ] Set up any new dependencies
- [ ] Create placeholder files/structure

---

## Step 2: Core Implementation

**Goal:** Build the feature functionality

### 2.1 [Component/Layer 1]

- [ ] Implement [specific piece]
- [ ] Implement [specific piece]
- [ ] Add unit tests

### 2.2 [Component/Layer 2]

- [ ] Implement [specific piece]
- [ ] Implement [specific piece]
- [ ] Add unit tests

### 2.3 [Component/Layer 3] (if needed)

- [ ] Implement [specific piece]
- [ ] Implement [specific piece]
- [ ] Add unit tests

---

## Step 3: Integration & Testing

**Goal:** Integrate with existing system and verify

### 3.1 Integration

- [ ] Connect to existing components
- [ ] Update any affected existing code
- [ ] Verify no regressions

### 3.2 Testing

- [ ] Write integration tests
- [ ] Test edge cases
- [ ] Test error scenarios
- [ ] Manual testing of user flow

### 3.3 Cleanup

- [ ] Remove any debug code
- [ ] Clean up comments
- [ ] Update documentation (if needed)

---

## Checkpoint

**STOP here for human review.**

- [ ] **All tasks complete**
- [ ] **Feature works as specified**
- [ ] **Tests pass**
- [ ] **No regressions**
- [ ] **Ready for merge**

---

## Blocked Tasks

| Task | Step | Blocked By | Resolution Needed |
|------|------|------------|-------------------|
| | | | |

---

## Decisions Log

### [YYYY-MM-DD] - [Decision Topic]

**Context:** [Why decision was needed]

**Chosen:** [What was decided and why]

---

## Completion Checklist

Before marking feature complete:

- [ ] All tasks marked `[x]` or `[-]` (with reason)
- [ ] All blocked tasks resolved
- [ ] Feature works as specified
- [ ] Tests written and passing
- [ ] No regressions in existing functionality
- [ ] Checkpoint approved by human

---

## Related Documents

- [plan-feature.md](plan-feature.md) - Feature plan
- [Parent product tasks] - If part of larger product

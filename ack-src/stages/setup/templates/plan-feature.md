---
type: artifact
stage: setup
artifact: plan
scope: feature
description: "Implementation plan for a single feature within an existing product"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Feature Name] - Feature Plan

## Scope

**Type:** Feature (single capability within existing product)

**What this plan covers:**
- One specific feature or capability
- Fits within existing architecture
- Limited, focused scope

**Parent product:** [Product name if applicable]

---

## Hard Requirements

These rules are **mandatory** and must be followed exactly.

### Agent Behavior

| Requirement | Rule |
|-------------|------|
| **Task start** | Mark task `[~]` in-progress BEFORE starting work |
| **Task complete** | Mark task `[x]` complete IMMEDIATELY after finishing |
| **Commits** | Commit after EACH completed task, not batched |
| **Checkpoints** | STOP at checkpoints and wait for human review |
| **Decisions** | Document ALL decisions inline with the task |
| **Blockers** | Mark task `[!]` blocked and explain; do NOT skip |

### Commit Rules

```
# Commit message format
[Feature: Name] Task description

- What was implemented
- Decisions made (if any)
```

### Checkpoint Rules

- Never skip a checkpoint
- Summarize: tasks completed, decisions made, blockers hit
- Wait for explicit human approval before continuing

---

## Overview

<!-- Brief summary of the feature -->

**Feature:** [Feature name]

**Purpose:** [What problem this feature solves]

**User story:** As a [user type], I want to [action] so that [benefit].

---

## Success Criteria

- [ ] [Criterion 1 - measurable outcome]
- [ ] [Criterion 2 - measurable outcome]
- [ ] [Criterion 3 - measurable outcome]

---

## Implementation Steps

Features typically don't need full phases. Use steps instead:

### Step 1: [Setup/Preparation]

**Goal:** [What this step accomplishes]

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

**Done when:** [Clear completion criteria]

---

### Step 2: [Core Implementation]

**Goal:** [What this step accomplishes]

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

**Done when:** [Clear completion criteria]

---

### Step 3: [Integration & Testing]

**Goal:** [What this step accomplishes]

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

**Done when:** [Clear completion criteria]

---

### Checkpoint

**STOP here for human review.**

Review focus:
- [ ] Feature works as specified
- [ ] Integrates with existing code
- [ ] Tests adequate
- [ ] No regressions introduced
- [ ] Ready for merge/deployment

---

## Boundaries

### In Scope

- [Specific capability 1]
- [Specific capability 2]

### Out of Scope

- [Related thing NOT included]
- [Future enhancement NOT included]

---

## Integration Points

<!-- How this feature connects to existing system -->

| Touches | Component | Change Type |
|---------|-----------|-------------|
| [ ] | [Component 1] | [New/Modify/Read-only] |
| [ ] | [Component 2] | [New/Modify/Read-only] |

---

## Risks

| Risk | Mitigation |
|------|------------|
| [Risk 1] | [How to handle] |
| [Risk 2] | [How to handle] |

---

## Flexible Elements

| Element | Default | For Features |
|---------|---------|--------------|
| Number of steps | 3 | Adjust as needed (usually 2-5) |
| Checkpoints | 1 at end | Add mid-point if complex |
| Phases | Not used | Use "steps" instead |
| Duration estimates | Optional | Usually not needed |

---

## Related Documents

- [tasks-feature.md](tasks-feature.md) - Detailed task breakdown
- [Parent product plan] - If feature is part of larger product
- [architecture.md](../../design/templates/architecture.md) - System structure

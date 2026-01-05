---
type: artifact
stage: setup
artifact: plan
scope: project
description: "Implementation plan for administrative, documentation, or meta work"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Project Plan

## Scope

**Type:** Project (administrative, documentation, or organizational work)

**What this plan covers:**
- Non-software or meta work
- Documentation, templates, processes
- Reorganization, cleanup, improvements

**Examples:**
- Reorganizing project structure
- Creating documentation templates
- Defining workflows and processes
- Research and analysis work

---

## Hard Requirements

These rules are **mandatory** and must be followed exactly.

### Agent Behavior

| Requirement | Rule |
|-------------|------|
| **Task start** | Mark task `[~]` in-progress BEFORE starting work |
| **Task complete** | Mark task `[x]` complete IMMEDIATELY after finishing |
| **Commits** | Commit after EACH completed task (if files changed) |
| **Checkpoints** | STOP at checkpoints and wait for human review |
| **Decisions** | Document ALL decisions inline with the task |
| **Blockers** | Mark task `[!]` blocked and explain; do NOT skip |

### Commit Rules

```
# Commit message format (when applicable)
[Project: Name] Task description

- What was created/changed
- Decisions made (if any)
```

### Checkpoint Rules

- Never skip a checkpoint
- Summarize: tasks completed, decisions made, blockers hit
- Wait for explicit human approval before continuing

---

## Overview

<!-- Brief summary of the project -->

**Project:** [Project name]

**Purpose:** [Why this work needs to be done]

**Outcome:** [What exists when this is complete]

---

## Success Criteria

- [ ] [Criterion 1 - what's true when done]
- [ ] [Criterion 2 - what's true when done]
- [ ] [Criterion 3 - what's true when done]

---

## Work Breakdown

Projects are organized by work area, not phases:

### Area 1: [Work Area Name]

**Goal:** [What this area accomplishes]

**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

**Done when:** [Clear completion criteria]

---

### Area 2: [Work Area Name]

**Goal:** [What this area accomplishes]

**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

**Done when:** [Clear completion criteria]

---

### Area 3: [Work Area Name]

**Goal:** [What this area accomplishes]

**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

**Done when:** [Clear completion criteria]

---

### Checkpoint

**STOP here for human review.**

Review focus:
- [ ] All deliverables created
- [ ] Quality meets expectations
- [ ] Work is complete and coherent
- [ ] Documentation clear

---

## Constraints

| Constraint | Impact |
|------------|--------|
| [Constraint 1] | [How it affects the work] |
| [Constraint 2] | [How it affects the work] |

---

## Dependencies

| Dependency | Needed For | Status |
|------------|------------|--------|
| [Dependency 1] | [Area] | [ ] Pending |
| [Dependency 2] | [Area] | [ ] Pending |

---

## What's Different About Project Scope

| Aspect | Product/Feature | Project |
|--------|-----------------|---------|
| Output | Working software | Documents, templates, processes |
| Phases | Foundation → Core → Features → Polish | Work areas (parallel OK) |
| CI/CD | Required | Usually not applicable |
| Testing | Required | Review-based validation |
| Deployment | To production environment | To repository/documentation |
| Commits | After each task | After each task (when files change) |

---

## Flexible Elements

| Element | Default | For Projects |
|---------|---------|--------------|
| Work areas | 3 | Adjust as needed |
| Checkpoints | 1 at end | Add if multi-session |
| Commit requirement | Every task | Only when files change |
| CI/CD checks | Skip | Not applicable |

---

## Related Documents

- [tasks-project.md](tasks-project.md) - Detailed task breakdown
- [Project-specific references as needed]

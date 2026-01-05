---
type: artifact
stage: setup
artifact: plan
scope: product
description: "Implementation plan for full product/MVP with multiple features"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Product Name] - Product Plan

## Scope

**Type:** Product (full MVP with multiple features)

**What this plan covers:**
- Complete product from foundation to deployment
- Multiple features and capabilities
- Full development lifecycle

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
[Phase X.Y] Task description

- What was implemented
- Decisions made (if any)
```

### Checkpoint Rules

- Never skip a checkpoint
- Summarize: tasks completed, decisions made, blockers hit
- Wait for explicit human approval before continuing
- Do not proceed on ambiguity - ask

---

## Overview

<!-- Brief summary of the product and implementation approach -->

[Product Name] is [brief description]. This plan breaks implementation into [X] phases, building from foundation to complete MVP.

**Success criteria (from brief):**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## Phase Summary

| Phase | Focus | Milestone | Duration Est. |
|-------|-------|-----------|---------------|
| 1 | Foundation | Infrastructure operational | [X days/weeks] |
| 2 | Core | Primary workflow functional | [X days/weeks] |
| 3 | Features | All MVP features complete | [X days/weeks] |
| 4 | Polish | Production-ready | [X days/weeks] |

**Total estimated duration:** [X weeks]

---

## Phase 1: Foundation

**Goal:** Establish infrastructure, project structure, and core patterns.

**Depends on:** Setup stage complete (repo initialized, deps installed, CI working)

### What Gets Built

- [ ] Database schema and connections
- [ ] Project structure per architecture
- [ ] Core utilities and shared code
- [ ] Base configuration
- [ ] Development workflow verified

### Milestone: "Foundation Operational"

Definition of done:
- [ ] Project builds without errors
- [ ] Database connects and migrations run
- [ ] Core utilities are tested
- [ ] CI pipeline passes

### Checkpoint 1

**STOP here for human review.**

Review focus:
- [ ] Structure matches architecture.md
- [ ] Schema matches data-model.md
- [ ] Code quality acceptable
- [ ] Ready for core development

---

## Phase 2: Core Functionality

**Goal:** Implement the primary user workflow end-to-end.

**Depends on:** Phase 1 complete and approved

### What Gets Built

- [ ] User authentication (if applicable)
- [ ] Primary API endpoints
- [ ] Core business logic
- [ ] Basic error handling
- [ ] Tests for critical paths

### Milestone: "Core Loop Working"

Definition of done:
- [ ] User can complete primary workflow
- [ ] Data persists correctly
- [ ] API contracts honored
- [ ] Core tests passing

### Checkpoint 2

**STOP here for human review.**

Review focus:
- [ ] Core workflow functions correctly
- [ ] Code follows established patterns
- [ ] Test coverage adequate
- [ ] Performance acceptable
- [ ] Ready for feature development

---

## Phase 3: Features

**Goal:** Implement all MVP features defined in scope.

**Depends on:** Phase 2 complete and approved

### What Gets Built

- [ ] [Feature A] - [brief description]
- [ ] [Feature B] - [brief description]
- [ ] [Feature C] - [brief description]
- [ ] Feature integration
- [ ] Feature tests

### Milestone: "Feature Complete"

Definition of done:
- [ ] All in-scope features implemented
- [ ] Features work together correctly
- [ ] Edge cases handled
- [ ] Feature tests passing

### Checkpoint 3

**STOP here for human review.**

Review focus:
- [ ] All scope items from brief addressed
- [ ] No scope creep (nothing out-of-scope built)
- [ ] Features integrated properly
- [ ] Ready for polish phase

---

## Phase 4: Polish & Deploy

**Goal:** Production-ready quality and deployment.

**Depends on:** Phase 3 complete and approved

### What Gets Built

- [ ] Comprehensive error handling
- [ ] Logging and monitoring
- [ ] Documentation updates
- [ ] Performance optimization (if needed)
- [ ] Production deployment

### Milestone: "MVP Complete"

Definition of done:
- [ ] All success criteria met
- [ ] No critical bugs
- [ ] Documentation complete
- [ ] Successfully deployed
- [ ] Smoke tests pass in production

### Checkpoint 4 (Final)

**STOP here for human review.**

Review focus:
- [ ] Success criteria from brief verified
- [ ] Production stable
- [ ] Documentation adequate
- [ ] Ready for users

---

## Dependencies

| Dependency | Needed By | Status | Owner |
|------------|-----------|--------|-------|
| [External API keys] | Phase 2 | [ ] Pending | [Name] |
| [Third-party account] | Phase 3 | [ ] Pending | [Name] |
| [Production hosting] | Phase 4 | [ ] Pending | [Name] |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Action] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Action] |

---

## Flexible Elements

These can be adjusted based on project needs:

| Element | Default | Can Adjust |
|---------|---------|------------|
| Number of phases | 4 | Yes - combine or split as needed |
| Checkpoint frequency | End of each phase | Yes - add mid-phase if risky |
| Duration estimates | Include | Optional - remove if not helpful |
| Risk section | Include | Optional for low-risk projects |

---

## Related Documents

- [tasks-product.md](tasks-product.md) - Detailed task breakdown
- [brief.md](../../discover/templates/brief.md) - What we're building
- [architecture.md](../../design/templates/architecture.md) - How it's structured

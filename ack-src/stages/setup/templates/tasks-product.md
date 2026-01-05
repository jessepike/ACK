---
type: artifact
stage: setup
artifact: tasks
scope: product
description: "Task breakdown for full product/MVP implementation"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Product Name] - Product Tasks

## Scope

**Type:** Product (full MVP with multiple features)

**Plan reference:** [plan-product.md](plan-product.md)

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
git commit -m "[Phase X.Y] Task description"
```

### Decision Documentation

When making a decision during a task, add it inline:

```markdown
- [x] Implement user authentication
  - **Decision:** Used JWT over sessions
  - **Rationale:** Stateless, better for API-first architecture
```

---

## Progress Summary

| Phase | Total | Complete | In Progress | Blocked |
|-------|-------|----------|-------------|---------|
| 1 - Foundation | 0 | 0 | 0 | 0 |
| 2 - Core | 0 | 0 | 0 | 0 |
| 3 - Features | 0 | 0 | 0 | 0 |
| 4 - Polish | 0 | 0 | 0 | 0 |
| **Total** | **0** | **0** | **0** | **0** |

---

## Phase 1: Foundation

**Milestone:** Foundation Operational
**Checkpoint:** End of phase - STOP for human review

### 1.1 Project Structure

- [ ] Create directory structure per architecture.md
- [ ] Set up base configuration files
- [ ] Configure TypeScript/linting/formatting
- [ ] Verify build succeeds

### 1.2 Database Setup

- [ ] Configure database connection
- [ ] Create initial schema migration
- [ ] Implement core entity models
- [ ] Verify database operations work
- [ ] Add seed data (if applicable)

### 1.3 Core Utilities

- [ ] Implement logging utility
- [ ] Create error handling patterns
- [ ] Set up common type definitions
- [ ] Add shared helper functions

### Phase 1 Checkpoint

- [ ] **All Phase 1 tasks complete**
- [ ] **STOP and summarize for human review**

---

## Phase 2: Core Functionality

**Milestone:** Core Loop Working
**Checkpoint:** End of phase - STOP for human review

### 2.1 Authentication (if applicable)

- [ ] Implement user registration endpoint
- [ ] Implement login endpoint
- [ ] Implement logout endpoint
- [ ] Add token/session management
- [ ] Create auth middleware
- [ ] Write auth tests

### 2.2 Core API Endpoints

- [ ] Implement [Resource 1] CRUD
  - [ ] Create endpoint
  - [ ] Read endpoint(s)
  - [ ] Update endpoint
  - [ ] Delete endpoint
- [ ] Implement [Resource 2] CRUD
  - [ ] Create endpoint
  - [ ] Read endpoint(s)
  - [ ] Update endpoint
  - [ ] Delete endpoint
- [ ] Add input validation
- [ ] Add error responses

### 2.3 Core Business Logic

- [ ] Implement [Core operation 1]
- [ ] Implement [Core operation 2]
- [ ] Add business validation rules
- [ ] Write tests for core paths

### Phase 2 Checkpoint

- [ ] **All Phase 2 tasks complete**
- [ ] **STOP and summarize for human review**

---

## Phase 3: Features

**Milestone:** Feature Complete
**Checkpoint:** End of phase - STOP for human review

### 3.1 [Feature A Name]

- [ ] Implement [Feature A component 1]
- [ ] Implement [Feature A component 2]
- [ ] Integrate with core system
- [ ] Write Feature A tests

### 3.2 [Feature B Name]

- [ ] Implement [Feature B component 1]
- [ ] Implement [Feature B component 2]
- [ ] Integrate with core system
- [ ] Write Feature B tests

### 3.3 [Feature C Name]

- [ ] Implement [Feature C component 1]
- [ ] Implement [Feature C component 2]
- [ ] Integrate with core system
- [ ] Write Feature C tests

### 3.4 UI/Frontend (if applicable)

- [ ] Implement [UI component 1]
- [ ] Implement [UI component 2]
- [ ] Add styling
- [ ] Test user flows

### Phase 3 Checkpoint

- [ ] **All Phase 3 tasks complete**
- [ ] **STOP and summarize for human review**

---

## Phase 4: Polish & Deploy

**Milestone:** MVP Complete
**Checkpoint:** End of phase (Final) - STOP for human review

### 4.1 Error Handling

- [ ] Add comprehensive error messages
- [ ] Implement error logging
- [ ] Add user-friendly error displays
- [ ] Test error scenarios

### 4.2 Documentation

- [ ] Update README with setup instructions
- [ ] Document API endpoints
- [ ] Add code comments where helpful
- [ ] Update architecture docs if changed

### 4.3 Performance (if needed)

- [ ] Profile critical paths
- [ ] Optimize identified bottlenecks
- [ ] Add caching if needed
- [ ] Verify performance acceptable

### 4.4 Deployment

- [ ] Configure production environment
- [ ] Set up production database
- [ ] Configure production secrets
- [ ] Deploy application
- [ ] Run smoke tests
- [ ] Verify production functionality

### Phase 4 Checkpoint (Final)

- [ ] **All Phase 4 tasks complete**
- [ ] **All success criteria verified**
- [ ] **STOP and summarize for human review**

---

## Blocked Tasks

<!-- Move blocked tasks here with context -->

| Task | Phase | Blocked By | Resolution Needed |
|------|-------|------------|-------------------|
| | | | |

---

## Decisions Log

<!-- Major decisions made during implementation -->

### [YYYY-MM-DD] - [Decision Topic]

**Context:** [Why decision was needed]

**Options:**
1. [Option A]
2. [Option B]

**Chosen:** [Which option and why]

---

## Completion Checklist

Before marking product complete:

- [ ] All tasks marked `[x]` or `[-]` (with reason)
- [ ] All blocked tasks resolved
- [ ] All checkpoints reviewed and approved
- [ ] All decisions documented
- [ ] Success criteria from brief verified
- [ ] Final checkpoint approved

---

## Related Documents

- [plan-product.md](plan-product.md) - Implementation phases
- [brief.md](../../discover/templates/brief.md) - Success criteria
- [architecture.md](../../design/templates/architecture.md) - System structure

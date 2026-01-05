---
type: prompt
stage: develop
prompt: validate
description: "Checkpoint and milestone validation for Develop stage"
version: 1.0.0
updated: "2026-01-04T00:00:00"
---

# Develop Stage Validation

Validate checkpoint completion, milestone achievement, and task tracking compliance.

## Instructions

This validation is used at **checkpoints** and **milestones** during the Develop stage. Unlike planning stages that validate documents, this validates execution compliance.

Use this prompt to verify:
- Checkpoint requirements are met
- Milestone criteria are achieved
- Task management rules were followed
- Ready to proceed to next phase

---

## Task Tracking Validation

### Status Compliance

- [ ] **All started tasks marked:** No work without `[~]` status recorded
- [ ] **All finished tasks marked:** No complete work still showing `[ ]`
- [ ] **No stale in-progress:** Tasks marked `[~]` are actually being worked
- [ ] **Blocked tasks explained:** All `[!]` tasks have documented reason
- [ ] **Skipped tasks justified:** All `[-]` tasks have documented reason

### Commit Compliance

- [ ] **Commits exist:** Each `[x]` task has corresponding commit(s)
- [ ] **Commit messages proper:** Follow format `[Phase X.Y] Description`
- [ ] **No batched commits:** Tasks weren't combined into single commits
- [ ] **No uncommitted work:** All completed work is committed

### Decision Documentation

- [ ] **Decisions captured:** All choices documented inline
- [ ] **Format correct:** Uses `**Decision:**` and `**Rationale:**` format
- [ ] **ADRs created:** Major decisions have ADR files (if applicable)

---

## Checkpoint Validation

### Checkpoint Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| Agent stopped at checkpoint | [ ] Pass / Fail | |
| Summary provided | [ ] Pass / Fail | |
| Awaited human approval | [ ] Pass / Fail | |
| All phase tasks addressed | [ ] Pass / Fail | |

### Checkpoint Summary Completeness

The agent's checkpoint summary must include:

- [ ] **Tasks completed:** List of finished tasks
- [ ] **Tasks remaining:** List of pending tasks (if any)
- [ ] **Decisions made:** Summary of decisions
- [ ] **Blockers encountered:** Any blocking issues
- [ ] **Deviations from plan:** Any changes to planned approach

---

## Milestone Validation

### Milestone Criteria Check

From the plan.md milestone definition:

| Criterion | Met? | Evidence |
|-----------|------|----------|
| [Criterion 1 from plan] | [ ] Yes / No | [How verified] |
| [Criterion 2 from plan] | [ ] Yes / No | [How verified] |
| [Criterion 3 from plan] | [ ] Yes / No | [How verified] |

### Deliverables Check

| Deliverable | Exists? | Works? |
|-------------|---------|--------|
| [Deliverable 1] | [ ] Yes / No | [ ] Yes / No |
| [Deliverable 2] | [ ] Yes / No | [ ] Yes / No |

---

## Phase Completion Validation

### Phase Task Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Complete `[x]` | X | X% |
| In Progress `[~]` | X | X% |
| Pending `[ ]` | X | X% |
| Blocked `[!]` | X | X% |
| Skipped `[-]` | X | X% |
| **Total** | **X** | **100%** |

### Phase Exit Criteria

- [ ] **All required tasks complete:** No pending required tasks
- [ ] **No unresolved blockers:** All `[!]` tasks resolved or escalated
- [ ] **Skips justified:** All `[-]` tasks have valid reasons
- [ ] **Milestone achieved:** Phase milestone criteria met
- [ ] **Tests pass:** Automated tests succeed
- [ ] **No broken builds:** CI pipeline passes

---

## Compliance Summary

### Task Management Compliance

| Rule | Compliant? | Issues |
|------|------------|--------|
| Mark in-progress before starting | [ ] Yes / No | [If no, list issues] |
| Mark complete after finishing | [ ] Yes / No | [If no, list issues] |
| Commit after each task | [ ] Yes / No | [If no, list issues] |
| Document decisions inline | [ ] Yes / No | [If no, list issues] |
| Stop at checkpoints | [ ] Yes / No | [If no, list issues] |

### Checkpoint Protocol Compliance

| Rule | Compliant? | Issues |
|------|------------|--------|
| Provided summary | [ ] Yes / No | |
| Listed completed tasks | [ ] Yes / No | |
| Listed decisions | [ ] Yes / No | |
| Listed blockers | [ ] Yes / No | |
| Waited for approval | [ ] Yes / No | |

---

## Validation Output

### Results Summary

| Category | Status | Issues |
|----------|--------|--------|
| Task Tracking | Valid / Invalid | [Count of issues] |
| Commit Compliance | Valid / Invalid | [Count of issues] |
| Decision Documentation | Valid / Invalid | [Count of issues] |
| Checkpoint Protocol | Valid / Invalid | [Count of issues] |
| Milestone Criteria | Valid / Invalid | [Count of issues] |
| Phase Exit Criteria | Valid / Invalid | [Count of issues] |

### Issues Found

| Issue | Category | Severity | How to Fix |
|-------|----------|----------|------------|
| [Issue 1] | [Category] | Blocking / Warning | [Fix] |
| [Issue 2] | [Category] | Blocking / Warning | [Fix] |

### Verdict

**[ ] VALID** - Checkpoint/milestone requirements met, approved to continue

**[ ] INVALID** - Issues must be resolved before proceeding

---

## Final Milestone Validation (MVP Complete)

Use this section only for the final checkpoint:

### Success Criteria Verification

From brief.md:

| Success Criterion | Achieved? | Evidence |
|-------------------|-----------|----------|
| [Criterion 1] | [ ] Yes / No | [How verified] |
| [Criterion 2] | [ ] Yes / No | [How verified] |
| [Criterion 3] | [ ] Yes / No | [How verified] |

### Production Readiness

| Check | Status |
|-------|--------|
| All tests pass | [ ] Yes / No |
| No critical bugs | [ ] Yes / No |
| Documentation complete | [ ] Yes / No |
| Deployed successfully | [ ] Yes / No |
| Smoke tests pass | [ ] Yes / No |

### MVP Verdict

**[ ] MVP COMPLETE** - All success criteria met, product ready

**[ ] NOT COMPLETE** - Issues must be resolved

---

## Quick Validation Checklist

For fast checkpoint validation:

1. [ ] All phase tasks marked `[x]` or have valid `[-]`/`[!]` status
2. [ ] Each completed task has a corresponding commit
3. [ ] Decisions documented inline with tasks
4. [ ] Agent provided checkpoint summary
5. [ ] Milestone criteria from plan.md are met
6. [ ] Tests pass, build succeeds

If all 6 pass, checkpoint is valid.

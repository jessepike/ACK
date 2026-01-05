---
type: prompt
stage: develop
prompt: review
description: "Code and progress review prompt for Develop stage checkpoints"
version: 1.0.0
updated: "2026-01-04T00:00:00"
---

# Develop Stage Review

Review code quality, progress, and alignment at checkpoints during development.

## Instructions

This review is used at **checkpoints** during the Develop stage. Unlike planning stages that review documents, this reviews actual implementation progress.

Use this prompt when:
- Agent reaches a planned checkpoint
- Phase milestone is claimed complete
- Before merging significant work
- When human review is requested

---

## Pre-Review: Status Check

Before detailed review, verify current state:

- [ ] **Tasks file updated:** All completed tasks marked `[x]`
- [ ] **No orphan work:** All work ties to a task
- [ ] **Commits made:** Each completed task has a commit
- [ ] **Decisions documented:** Inline decisions captured

If status tracking is incomplete, address that first.

---

## Progress Review

### 1. Task Completion

- [ ] **Tasks claimed complete are actually done**
- [ ] **No half-finished work marked complete**
- [ ] **Blocked tasks have clear explanations**
- [ ] **Skipped tasks have justification**

**Questions to answer:**
- Does the work match what the task described?
- Are there any tasks marked complete that aren't?
- Are blocked items truly blocked or just difficult?

### 2. Phase/Milestone Progress

- [ ] **On track:** Progress matches expectations
- [ ] **Milestone criteria:** Phase deliverables are actually delivered
- [ ] **No scope creep:** Only in-scope work was done
- [ ] **No scope gaps:** All phase tasks addressed

**Questions to answer:**
- Is the milestone actually achieved?
- Was work done that wasn't in the plan?
- Was planned work skipped without justification?

### 3. Decision Quality

- [ ] **Decisions documented:** All choices captured
- [ ] **Rationale sound:** Reasoning makes sense
- [ ] **Consistent:** Decisions don't contradict each other
- [ ] **Aligned:** Decisions match architecture/brief

**Questions to answer:**
- Were decisions made that should have been escalated?
- Are there undocumented decisions visible in the code?
- Do decisions create technical debt?

---

## Code Review

### 1. Correctness

- [ ] **Works as intended:** Code does what task specified
- [ ] **Edge cases handled:** Reasonable error handling
- [ ] **No obvious bugs:** Logic appears sound
- [ ] **Tests pass:** Automated tests succeed

**Questions to answer:**
- Does the code actually solve the problem?
- Are there obvious failure modes?
- Would this break in production?

### 2. Architecture Alignment

- [ ] **Matches architecture.md:** Components are where they should be
- [ ] **Follows patterns:** Consistent with established code patterns
- [ ] **Proper boundaries:** Separation of concerns maintained
- [ ] **No shortcuts:** Didn't bypass architectural decisions

**Questions to answer:**
- Does this fit the system design?
- Were architectural decisions ignored for convenience?
- Will this cause problems as the system grows?

### 3. Code Quality

- [ ] **Readable:** Code is understandable
- [ ] **Maintainable:** Future changes won't be painful
- [ ] **Not over-engineered:** Appropriate complexity
- [ ] **Not under-engineered:** Not cutting important corners

**Questions to answer:**
- Could another developer understand this?
- Is there unnecessary complexity?
- Are there obvious improvements needed?

### 4. Test Coverage

- [ ] **Critical paths tested:** Main functionality has tests
- [ ] **Edge cases covered:** Error scenarios tested
- [ ] **Tests are meaningful:** Not just for coverage numbers
- [ ] **Tests pass:** All tests green

**Questions to answer:**
- What happens if this breaks? Will we know?
- Are the tests testing the right things?
- Is coverage appropriate for the risk level?

---

## Alignment Review

### 1. Brief Alignment

- [ ] **Solving stated problem:** Work addresses brief's problem
- [ ] **Within scope:** Only in-scope items built
- [ ] **Success criteria progress:** Moving toward success metrics
- [ ] **Constraints honored:** Budget, timeline, resources respected

### 2. Plan Alignment

- [ ] **Following plan:** Work matches plan phases
- [ ] **Correct order:** Dependencies respected
- [ ] **Checkpoints honored:** Stopped when supposed to

### 3. Stack Alignment

- [ ] **Using chosen technologies:** stack.md decisions followed
- [ ] **No rogue dependencies:** Only approved packages added
- [ ] **Patterns consistent:** Following stack conventions

---

## Review Output

### Summary

| Area | Rating | Notes |
|------|--------|-------|
| Task Completion | Strong / Adequate / Weak | [Key observation] |
| Milestone Progress | Strong / Adequate / Weak | [Key observation] |
| Decision Quality | Strong / Adequate / Weak | [Key observation] |
| Code Correctness | Strong / Adequate / Weak | [Key observation] |
| Architecture Alignment | Strong / Adequate / Weak | [Key observation] |
| Code Quality | Strong / Adequate / Weak | [Key observation] |
| Test Coverage | Strong / Adequate / Weak | [Key observation] |

### What Went Well

- [Positive observation]
- [Positive observation]

### Issues Found

| Issue | Severity | Category | Action Needed |
|-------|----------|----------|---------------|
| [Issue 1] | Blocking / Important / Minor | [Category] | [Fix required] |
| [Issue 2] | Blocking / Important / Minor | [Category] | [Fix required] |

### Decisions to Revisit

| Decision | Concern | Recommendation |
|----------|---------|----------------|
| [Decision] | [Why it's concerning] | [What to do] |

### Verdict

**[ ] Approved to continue** - Work is solid, proceed to next phase

**[ ] Approved with items** - Can continue, but address listed items

**[ ] Revisions required** - Must fix issues before continuing

**[ ] Needs discussion** - Significant concerns require conversation

---

## Checkpoint Approval

For the agent to continue after checkpoint:

```
## Checkpoint [X] Review

**Date:** YYYY-MM-DD
**Phase:** [Phase name]
**Reviewer:** [Human name]

### Status
- Tasks complete: X/Y
- Milestone achieved: Yes/No
- Blocking issues: X

### Verdict
[Approved / Approved with items / Revisions required]

### Items to address (if any)
1. [Item]
2. [Item]

### Approved to proceed
[X] Yes, continue to Phase [X+1]
[ ] No, see revisions required above
```

---

## Notes

- This review happens at runtime, not planning time
- Focus on working code, not documents
- "Adequate" means good enough to continue
- Blocking issues must be fixed before proceeding
- Minor issues can be tracked for later cleanup

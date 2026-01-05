---
type: prompt
stage: setup
prompt: review
description: "Content analysis prompt for Setup stage deliverables"
version: 1.0.0
updated: "2026-01-04T00:00:00"
---

# Setup Stage Review

Review the implementation plan and task breakdown for completeness and actionability.

## Instructions

You are reviewing the Setup stage deliverables to assess whether they're ready to advance to the Develop stage. Focus on **plan soundness and task actionability**.

Read both documents, then evaluate each area below.

---

## Pre-Review: Environment Verification

Before reviewing documents, verify the environment is ready:

- [ ] **Repository exists:** Git repo initialized and accessible
- [ ] **Dependencies install:** Package install completes without errors
- [ ] **Project runs:** Dev server or build succeeds
- [ ] **Tests run:** Test framework executes (even if minimal tests)
- [ ] **CI/CD works:** Pipeline completes (build + test at minimum)

If environment isn't ready, note as blocking issue before continuing.

---

## Plan Review (plan.md)

### 1. Phase Structure

- [ ] **Phases defined:** Implementation broken into logical phases
- [ ] **Sequence logical:** Phases build on each other appropriately
- [ ] **Dependencies clear:** What must complete before each phase can start
- [ ] **No gaps:** All architecture components have a phase

**Questions to answer:**
- Do phases follow a logical progression (foundation → core → features)?
- Are there implicit dependencies not documented?
- Could phases be parallelized, and is that noted?

### 2. Milestones

- [ ] **Milestones defined:** Each phase has a clear completion point
- [ ] **Milestones verifiable:** Can objectively determine if milestone is reached
- [ ] **Milestones valuable:** Each milestone delivers something meaningful
- [ ] **Not too granular:** Milestones are significant, not every small step

**Questions to answer:**
- Would you know when each phase is "done"?
- Do milestones align with brief's success criteria?
- Are milestones too ambitious or too trivial?

### 3. Checkpoints

- [ ] **Human checkpoints exist:** Points where human reviews agent work
- [ ] **Checkpoint frequency appropriate:** Not too sparse, not excessive
- [ ] **Checkpoint criteria clear:** What gets reviewed at each checkpoint
- [ ] **Critical points covered:** Checkpoints before risky or irreversible work

**Questions to answer:**
- How long can agents work unsupervised?
- Are checkpoints at natural boundaries (not mid-feature)?
- Do checkpoints catch issues before they compound?

### 4. Scope Alignment

- [ ] **Covers in-scope items:** All brief scope items have a plan
- [ ] **Excludes out-of-scope:** Nothing planned that's out of scope
- [ ] **Constraints respected:** Plan fits timeline/resource constraints
- [ ] **Architecture aligned:** Plan implements the designed architecture

**Questions to answer:**
- Is anything in the brief missing from the plan?
- Is anything in the plan not in the brief?
- Does the plan seem achievable given constraints?

---

## Tasks Review (tasks.md)

### 1. Task Clarity

- [ ] **Tasks are specific:** Each task describes a concrete action
- [ ] **Tasks are scoped:** Can be completed in a reasonable session
- [ ] **No ambiguity:** Clear what "done" looks like for each task
- [ ] **Context included:** Enough detail to start without research

**Questions to answer:**
- Could someone start this task immediately?
- Is the task small enough to complete in one session?
- Would two people interpret the task the same way?

### 2. Task Coverage

- [ ] **Derives from plan:** Every plan phase has corresponding tasks
- [ ] **Complete coverage:** No phases missing task breakdown
- [ ] **No orphan tasks:** Every task maps to a plan phase
- [ ] **Dependencies noted:** Task order reflects dependencies

**Questions to answer:**
- Are there plan phases without any tasks?
- Are there tasks that don't connect to the plan?
- Is the task ordering logical?

### 3. Task Granularity

- [ ] **Appropriately sized:** Not too big (unclear), not too small (overhead)
- [ ] **Consistent sizing:** Tasks are roughly similar effort
- [ ] **Complex tasks split:** Large tasks broken into sub-tasks
- [ ] **Trivial tasks grouped:** Very small items combined sensibly

**Questions to answer:**
- Are any tasks that would take multiple days? (Should be split)
- Are any tasks that take minutes? (Should be grouped)
- Could you estimate effort for each task?

### 4. Actionability

- [ ] **No research required:** Tasks don't require decisions first
- [ ] **Blockers identified:** Known blockers/unknowns are called out
- [ ] **Resources linked:** Relevant docs/files referenced if needed
- [ ] **Acceptance criteria:** Know when task is complete

**Questions to answer:**
- Which tasks require decisions before starting?
- Are there hidden unknowns that will block progress?
- Could an agent execute these tasks autonomously?

---

## Cross-Document Review

### 1. Plan ↔ Tasks Alignment

- [ ] **Complete mapping:** Every plan phase has tasks
- [ ] **Every task traces:** Each task maps to a phase
- [ ] **Effort reasonable:** Task volume matches plan ambition
- [ ] **Order consistent:** Task sequence matches plan phases

### 2. Design ↔ Plan Alignment

- [ ] **Architecture covered:** All architecture components planned
- [ ] **Data model covered:** Schema implementation planned
- [ ] **Stack used:** Planned work uses chosen technologies

### 3. Brief ↔ Plan Alignment

- [ ] **Scope matched:** Plan delivers what brief promises
- [ ] **Success criteria achievable:** Plan leads to success metrics
- [ ] **Constraints honored:** Plan fits within stated constraints

---

## Review Output

### Summary

| Area | Rating | Notes |
|------|--------|-------|
| Plan - Phases | Strong / Adequate / Weak | [Key observation] |
| Plan - Milestones | Strong / Adequate / Weak | [Key observation] |
| Plan - Checkpoints | Strong / Adequate / Weak | [Key observation] |
| Plan - Scope Alignment | Strong / Adequate / Weak | [Key observation] |
| Tasks - Clarity | Strong / Adequate / Weak | [Key observation] |
| Tasks - Coverage | Strong / Adequate / Weak | [Key observation] |
| Tasks - Granularity | Strong / Adequate / Weak | [Key observation] |
| Tasks - Actionability | Strong / Adequate / Weak | [Key observation] |
| Cross-Document Alignment | Strong / Adequate / Weak | [Key observation] |

### Strengths

- [What's working well]
- [What's working well]

### Issues to Address

| Issue | Severity | Document | Recommendation |
|-------|----------|----------|----------------|
| [Issue 1] | Blocking / Important / Minor | plan.md | [How to fix] |
| [Issue 2] | Blocking / Important / Minor | tasks.md | [How to fix] |

### Verdict

**[ ] Ready to advance** - Plan and tasks are solid, proceed to Develop stage

**[ ] Revise and re-review** - Address issues above, then review again

**[ ] Needs significant work** - Fundamental gaps require rethinking

---

## Notes

- Both documents must pass review to advance
- Environment must be verified before advancing
- "Adequate" means good enough to start development
- Tasks can be refined during Develop; don't over-plan
- Blocking issues must be resolved before advancing

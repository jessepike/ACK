---
type: "stage_guide"
stage: "develop"
description: "Stage 4: Execute the implementation plan (runtime stage)"
version: "1.0.0"
updated: "2026-01-04T00:00:00"
---

# Develop Stage

## Overview

**Purpose:** Execute the implementation plan. Build the software with agent assistance and human oversight.

**Key Question:** Is it built correctly?

**When to enter:** Setup complete, environment ready, plan and tasks defined.

**When to exit:** MVP complete per success criteria in brief.

---

## This Stage Is Different

Unlike Stages 1-3 (Discover, Design, Setup), the Develop stage is a **runtime stage**:

| Planning Stages (1-3) | Runtime Stage (4) |
|----------------------|-------------------|
| Produce artifacts | Consume artifacts |
| One-time completion | Ongoing execution |
| Clear exit criteria | Exit = MVP complete |
| Templates guide creation | Plan guides execution |

There are no new artifacts to create. Instead:
- Execute tasks from `tasks.md`
- Update task status as work completes
- Capture decisions inline with tasks
- Create ADRs for major architectural decisions

---

## Inputs

From Setup stage:
- `plan.md` - Implementation phases, milestones, checkpoints
- `tasks.md` - Actionable work breakdown

From Design stage:
- `architecture.md` - System structure (reference during implementation)
- `data-model.md` - Database schema (reference during implementation)
- `stack.md` - Technology choices (use specified technologies)

From Discover stage:
- `brief.md` - Success criteria, scope boundaries (verify alignment)

---

## Outputs

No new deliverables. Instead, this stage produces:

| Output | Description |
|--------|-------------|
| **Working software** | The actual implementation |
| **Updated tasks.md** | Tasks marked complete, decisions captured |
| **ADRs** (if needed) | Major architectural decisions documented |
| **Git commits** | Incremental, well-documented changes |

---

## Execution Model

### Agent-Driven Development

Agents execute tasks from `tasks.md` with these guardrails:

1. **Work in phases** - Follow plan.md phase sequence
2. **Complete tasks** - Mark tasks done as completed
3. **Pause at checkpoints** - Human review at defined points
4. **Capture decisions** - Document choices inline with tasks
5. **Commit incrementally** - Small, focused commits

### Human Oversight

Humans intervene at:
- **Checkpoints** defined in plan.md
- **Blockers** when agents can't proceed
- **Decisions** that require judgment
- **Reviews** of completed work

---

## Workflow

### Starting a Work Session

1. **Load context**
   - Read `plan.md` - current phase, next milestone
   - Read `tasks.md` - next uncompleted task
   - Read relevant Design artifacts if needed

2. **Identify work**
   - Find next task in current phase
   - Verify no blockers
   - Confirm task is actionable

3. **Execute task**
   - Implement the task
   - Commit changes with clear message
   - Update task status in `tasks.md`

4. **Check for checkpoint**
   - If checkpoint reached, pause for human review
   - If phase complete, verify milestone achieved

### Task Lifecycle

```
[ ] Pending     → Task not yet started
[~] In Progress → Currently being worked on
[x] Complete    → Task finished
[!] Blocked     → Cannot proceed (document why)
[-] Skipped     → Intentionally not done (document why)
```

### Decision Capture

When making decisions during implementation:

**Minor decisions** - Capture inline with the task:
```markdown
- [x] Implement user authentication
  - Decision: Used JWT over sessions for stateless auth
  - Rationale: Simpler scaling, matches API-first architecture
```

**Major decisions** - Create an ADR:
```markdown
docs/adr/
└── 001-jwt-authentication.md
```

Use ADRs for decisions that:
- Affect multiple components
- Are hard to reverse
- Will be referenced often
- Need detailed rationale

---

## Checkpoints

### What Happens at a Checkpoint

1. **Agent pauses** - Stops executing tasks
2. **Agent summarizes** - Reports progress, decisions, blockers
3. **Human reviews** - Examines work, provides feedback
4. **Human approves** - Gives go-ahead to continue
5. **Agent continues** - Proceeds to next phase

### Checkpoint Review Criteria

| Area | Questions |
|------|-----------|
| **Progress** | Are tasks being completed as expected? |
| **Quality** | Does the code meet standards? |
| **Alignment** | Is work matching the plan and architecture? |
| **Decisions** | Are decisions documented and reasonable? |
| **Blockers** | Are there issues that need resolution? |

### Suggested Checkpoint Timing

- After foundation/scaffolding complete
- After core functionality works
- Before external integrations
- Before any irreversible actions
- At phase boundaries

---

## Handling Common Situations

### Task is Unclear

```markdown
1. Do NOT guess - ambiguity causes drift
2. Document the ambiguity inline
3. Mark task as blocked
4. Flag for human clarification
```

### Task Needs to be Split

```markdown
1. Mark original task as blocked
2. Add sub-tasks below it
3. Continue with sub-tasks
4. Mark original complete when sub-tasks done
```

### Unexpected Decision Needed

```markdown
1. Document the decision point
2. List options considered
3. Make a reasonable choice (or ask human)
4. Document chosen option and rationale
5. Continue with implementation
```

### Bug Found During Development

```markdown
1. Assess severity (blocking vs. minor)
2. If blocking current task: fix first
3. If not blocking: add as new task
4. Document in commit message
```

### Scope Creep Detected

```markdown
1. Check brief.md scope boundaries
2. If out of scope: note and skip
3. If in scope but not in tasks: add task
4. If unclear: flag for human decision
```

---

## Quality Practices

### Code Standards

- Follow conventions established in codebase
- Match patterns in existing code
- Write tests for new functionality
- Keep functions focused and readable

### Commit Practices

- Commit after each completed task (or logical sub-unit)
- Write clear commit messages
- Reference task in commit message
- Don't commit broken code

### Documentation

- Update code comments where helpful
- Keep README current if setup changes
- Document API endpoints as created
- Update tasks.md with decisions

---

## Progress Tracking

### In tasks.md

```markdown
## Phase 1: Foundation

- [x] Initialize project structure
- [x] Set up database connection
  - Decision: Used connection pooling for performance
- [~] Implement user model
- [ ] Add authentication endpoints
- [ ] Set up test framework

**Status:** 2/5 complete
**Milestone:** Foundation operational
```

### Metrics to Track

| Metric | How to Measure |
|--------|---------------|
| Tasks complete | Count [x] vs total |
| Phase progress | Current phase / total phases |
| Blockers | Count [!] tasks |
| Decisions made | Count inline decisions + ADRs |

---

## Prompts

- [Review Prompt](prompts/review.md) - Code and progress review
- [Validation Prompt](prompts/validate.md) - Milestone and checkpoint validation

---

## Exit Criteria

The Develop stage completes when:

| Criterion | Check |
|-----------|-------|
| All tasks complete | No pending tasks for MVP scope |
| Tests pass | Test suite passes |
| Success criteria met | brief.md criteria achieved |
| No critical blockers | All blocking issues resolved |
| Code reviewed | Human has reviewed implementation |
| Deployed (if applicable) | MVP accessible in target environment |

---

## Common Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Ignoring checkpoints | Never skip human review points |
| Silent decisions | Always document decisions inline |
| Scope drift | Refer back to brief.md boundaries |
| Large commits | Commit after each task, not at day end |
| Skipping tests | Write tests as part of task completion |
| Over-engineering | Build what's in scope, nothing more |

---

## Stage Flow

```
plan.md + tasks.md (from Setup)
    ↓
┌─────────────────────────────────┐
│  Development Loop               │
│                                 │
│  1. Pick next task              │
│  2. Implement                   │
│  3. Commit                      │
│  4. Update tasks.md             │
│  5. Repeat until checkpoint     │
│                                 │
└─────────────────────────────────┘
    ↓
Human checkpoint review
    ↓
Continue loop until MVP complete
    ↓
Exit: Working software
```

---

## Previous Stage

**Setup** - Initialize environment and create implementation plan.

## After Develop

The Develop stage doesn't "advance" to another stage. Instead, the project is **complete** when:

- MVP is built and working
- Success criteria are met
- Deliverables are in `/docs`
- Software is deployed (if applicable)

For ongoing work after MVP:
- Return to Discover for new features
- Return to Design for architectural changes
- Continue in Develop for enhancements within current architecture

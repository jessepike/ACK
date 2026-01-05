---
type: "stage_guide"
stage: "setup"
description: "Stage 3: Initialize environment and create implementation plan"
version: "1.0.0"
updated: "2026-01-04T00:00:00"
---

# Setup Stage

## Overview

**Purpose:** Initialize the development environment and repository. Front-load all configuration. Create an implementation plan and task breakdown before coding begins.

**Key Question:** Are we ready to start coding?

**When to enter:** Design reviewed, architecture finalized, stack decisions made.

**When to exit:** Repo initialized, CI/CD configured, plan complete, tasks defined.

---

## Inputs

From Design stage:
- `architecture.md` - System structure and components
- `data-model.md` - Database schema and relationships
- `stack.md` - Technology choices with rationale

From Discover stage:
- `brief.md` - What we're building, success criteria, constraints

---

## Deliverables

Required outputs to advance to Develop stage:

| Artifact | Purpose |
|----------|---------|
| `plan.md` | Phased implementation sequence with milestones |
| `tasks.md` | Work breakdown with actionable items |

Both deliverables must be complete before advancing. The plan and tasks are the "contract" for the Develop stage.

---

## Support Artifacts

Working documents that capture setup decisions. Archived at Setup completion.

| Artifact | Purpose | When to Use |
|----------|---------|-------------|
| `repo-init.md` | Git repository and initial structure | Always - documents repo setup |
| `scaffolding.md` | Initial code structure and boilerplate | Complex projects with significant scaffolding |
| `ci-cd.md` | Pipeline configuration notes | When CI/CD is non-trivial |
| `testing.md` | Test strategy and configuration | When test approach needs documentation |
| `git-workflow.md` | Branch strategy and PR process | Team projects or complex workflows |

Not all support artifacts are required. Use what's needed based on project complexity.

---

## Checklist

### Phase 1: Repository Initialization
- [ ] Create git repository
- [ ] Set up initial directory structure
- [ ] Configure .gitignore
- [ ] Create initial README
- [ ] Document setup in `repo-init.md`

### Phase 2: Project Scaffolding
- [ ] Initialize project (npm init, cargo init, etc.)
- [ ] Install core dependencies from stack.md
- [ ] Create configuration files
- [ ] Set up base project structure
- [ ] Verify project builds/runs
- [ ] Document in `scaffolding.md` (if complex)

### Phase 3: Development Environment
- [ ] Configure linting and formatting
- [ ] Set up editor/IDE configuration
- [ ] Configure environment variables
- [ ] Document local setup steps

### Phase 4: CI/CD Configuration
- [ ] Set up CI pipeline (build, test, lint)
- [ ] Configure deployment pipeline (if applicable)
- [ ] Set up environment secrets
- [ ] Verify pipeline runs successfully
- [ ] Document in `ci-cd.md`

### Phase 5: Testing Setup
- [ ] Configure test framework
- [ ] Set up test directory structure
- [ ] Create initial test configuration
- [ ] Verify tests run
- [ ] Document in `testing.md` (if complex)

### Phase 6: Git Workflow
- [ ] Define branch naming convention
- [ ] Create PR template (if needed)
- [ ] Set up branch protection (if needed)
- [ ] Document in `git-workflow.md`

### Phase 7: Implementation Planning
- [ ] Break architecture into implementation phases
- [ ] Define milestones for each phase
- [ ] Identify dependencies between phases
- [ ] Set human oversight checkpoints
- [ ] Document in `plan.md`

### Phase 8: Task Breakdown
- [ ] Derive tasks from plan phases
- [ ] Ensure tasks are actionable (can be started and completed)
- [ ] Estimate effort where helpful
- [ ] Identify blockers and dependencies
- [ ] Document in `tasks.md`

### Phase 9: Review & Validate
- [ ] Run content review (prompts/review.md)
- [ ] Address review feedback
- [ ] Run structural validation (prompts/validate.md)
- [ ] Confirm ready for Develop stage

---

## Templates

### Deliverables
- [plan.md](templates/plan.md) - **Deliverable** - Implementation plan
- [tasks.md](templates/tasks.md) - **Deliverable** - Task breakdown

### Support Artifacts
- [repo-init.md](templates/repo-init.md) - Repository setup
- [scaffolding.md](templates/scaffolding.md) - Project scaffolding
- [ci-cd.md](templates/ci-cd.md) - CI/CD configuration
- [testing.md](templates/testing.md) - Test strategy
- [git-workflow.md](templates/git-workflow.md) - Git workflow

---

## Prompts

- [Review Prompt](prompts/review.md) - Content analysis of plan and tasks
- [Validation Prompt](prompts/validate.md) - Structural completeness check

---

## Exit Criteria

Before advancing to Develop:

| Criterion | Check |
|-----------|-------|
| Repository exists | Git repo initialized with proper structure |
| Dependencies install | `npm install` (or equivalent) succeeds |
| Project runs | Dev server or build completes without errors |
| Tests run | Test framework configured, at least 1 test passes |
| CI/CD works | Pipeline runs and completes (even if minimal) |
| Plan complete | Phases defined with milestones and checkpoints |
| Tasks actionable | Each task can be started without ambiguity |
| Validation passed | Structural check passes |

---

## Common Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Skipping CI/CD | Even minimal CI saves time later; set it up now |
| Vague tasks | Tasks should be completable in one session; if not, break down further |
| No checkpoints | Plan should have human review points; don't let agents run unsupervised |
| Over-planning | Plan enough to start; adjust as you learn |
| Missing dependencies | Verify all stack.md dependencies are actually installed |
| Untested setup | Someone else (or future you) should be able to clone and run |

---

## Planning Principles

### 1. Front-Load Configuration
Get all setup, config, and environment work done before coding. Discovering missing config mid-implementation is disruptive.

### 2. Phases Over Features
Organize by implementation phase (foundation → core → features → polish), not by feature. This ensures dependencies are built first.

### 3. Checkpoint Often
Plan human oversight points. Agents should not run indefinitely without review. Key checkpoints:
- After foundation/scaffolding
- After core functionality
- Before any external integrations
- Before deployment

### 4. Actionable Tasks
A good task can be started immediately without further clarification. If a task requires research or decisions, split it: "Research X options" → "Decide X approach" → "Implement X".

### 5. Capture Decisions Inline
When making decisions during Setup, document them in the relevant artifact. Don't create a separate decisions file—context matters.

---

## Stage Flow

```
Design artifacts (architecture, data-model, stack)
    ↓
Repository initialization
    ↓
Project scaffolding
    ↓
CI/CD + Testing setup
    ↓
plan.md (phases, milestones, checkpoints)
    ↓
tasks.md (actionable work breakdown)
    ↓
Review (content) → Fix → Validate (structure)
    ↓
Advance to Develop
```

---

## Archive Trigger

**Setup completion triggers archiving:**

When Setup is complete and validated:
1. **Deliverables** (plan.md, tasks.md) move to `/docs`
2. **All support artifacts** from Discover, Design, Setup move to `~/.ack/archives/[project-name]/`
3. **Working directory** (`.ack/`) is cleaned except for `archives-manifest.md`

This is the only archive trigger in the ACK workflow. All planning artifacts are preserved for reference but removed from the active project to prevent agent confusion.

---

## Relationship to Other Stages

```
Discover          Design              Setup              Develop
─────────────────────────────────────────────────────────────────
brief.md    →    architecture.md  →   plan.md      →    (execute)
                 data-model.md    →   tasks.md     →    (update)
                 stack.md         →   [repo setup]
```

- **Plan** translates architecture phases into implementation order
- **Tasks** breaks plan phases into actionable work items
- **Develop** executes tasks, updating `tasks.md` as work completes

---

## Previous Stage

**Design** - Define how the solution will work technically.

## Next Stage

**Develop** - Execute the implementation plan.

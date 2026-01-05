# ACK Artifact Inventory

## Overview

This document catalogs all artifacts in the ACK (Agent Context Kit) system, organized by stage. Each stage has deliverables (required outputs) and support artifacts (working documents that get archived).

**Last updated:** 2025-01-04

---

## Stage Structure

```
stages/
├── discover/           # Stage 1: What & Why
├── design/             # Stage 2: How (technical)
├── setup/              # Stage 3: Ready to execute
└── develop/            # Stage 4: Doing (runtime)
```

Each stage contains:
- `README.md` - Stage overview and checklist
- `templates/` - Artifact templates
- `prompts/` - Review and validation prompts

---

## Artifact Classification

| Type | Description | Final Location |
|------|-------------|----------------|
| **Deliverable** | Required output to advance to next stage | `/docs` in project |
| **Support** | Working documents, research, notes | Archived to `~/.ack/archives/` |

---

## Stage 1: Discover

**Purpose:** Define what we're building and why

### Deliverables

| Artifact | Template | Description |
|----------|----------|-------------|
| Brief | `stages/discover/templates/brief.md` | Problem, solution, scope, success criteria |

### Support Artifacts

| Artifact | Template | Description |
|----------|----------|-------------|
| Concept | `stages/discover/templates/concept.md` | Working concept for iteration |
| Research | `stages/discover/templates/research.md` | Market and competitive research |
| Validation | `stages/discover/templates/validation.md` | Problem and solution validation |

### Prompts

| Prompt | Path | Purpose |
|--------|------|---------|
| Review | `stages/discover/prompts/review.md` | Content analysis of brief |
| Validate | `stages/discover/prompts/validate.md` | Structural check of brief |

---

## Stage 2: Design

**Purpose:** Define how the solution will work technically

### Deliverables

| Artifact | Template | Description |
|----------|----------|-------------|
| Architecture | `stages/design/templates/architecture.md` | System structure, components, data flow |
| Data Model | `stages/design/templates/data-model.md` | Database schema, entities, relationships |
| Stack | `stages/design/templates/stack.md` | Technology choices with rationale |

### Support Artifacts

| Artifact | Template | Description |
|----------|----------|-------------|
| Context Schema | `stages/design/templates/context-schema.md` | Agent context structure definition |
| Dependencies | `stages/design/templates/dependencies.md` | Package evaluation and selection |

### Prompts

| Prompt | Path | Purpose |
|--------|------|---------|
| Review | `stages/design/prompts/review.md` | Technical soundness review |
| Validate | `stages/design/prompts/validate.md` | Structural check of design docs |

---

## Stage 3: Setup

**Purpose:** Prepare environment and plan for execution

### Deliverables

Deliverables are scope-specific. Choose based on project type:

#### Plan Templates

| Scope | Template | When to Use |
|-------|----------|-------------|
| Product | `stages/setup/templates/plan-product.md` | Full MVP with multiple features |
| Feature | `stages/setup/templates/plan-feature.md` | Single capability addition |
| Project | `stages/setup/templates/plan-project.md` | Administrative/meta work |

#### Tasks Templates

| Scope | Template | When to Use |
|-------|----------|-------------|
| Product | `stages/setup/templates/tasks-product.md` | Task breakdown by phase |
| Feature | `stages/setup/templates/tasks-feature.md` | Task breakdown by step |
| Project | `stages/setup/templates/tasks-project.md` | Task breakdown by work area |

### Support Artifacts

| Artifact | Template | Description |
|----------|----------|-------------|
| Repo Init | `stages/setup/templates/repo-init.md` | Repository initialization documentation |
| Scaffolding | `stages/setup/templates/scaffolding.md` | Code scaffolding patterns and boilerplate |
| CI/CD | `stages/setup/templates/ci-cd.md` | Pipeline configuration |
| Testing | `stages/setup/templates/testing.md` | Test strategy and configuration |
| Git Workflow | `stages/setup/templates/git-workflow.md` | Branch strategy and PR process |

### Prompts

| Prompt | Path | Purpose |
|--------|------|---------|
| Review | `stages/setup/prompts/review.md` | Plan soundness and task actionability |
| Validate | `stages/setup/prompts/validate.md` | Environment verification |

---

## Stage 4: Develop

**Purpose:** Execute the plan and build the solution

### Deliverables

No new deliverables - updates `tasks.md` from Setup stage.

### Support Artifacts

Created during development as needed:
- Decision logs
- Debug notes
- Spike results

### Prompts

| Prompt | Path | Purpose |
|--------|------|---------|
| Review | `stages/develop/prompts/review.md` | Code and progress review at checkpoints |
| Validate | `stages/develop/prompts/validate.md` | Checkpoint and milestone validation |

---

## Template Summary

### By Stage

| Stage | Deliverables | Support | Prompts |
|-------|--------------|---------|---------|
| Discover | 1 | 3 | 2 |
| Design | 3 | 2 | 2 |
| Setup | 6 (3 plan + 3 tasks) | 5 | 2 |
| Develop | 0 | - | 2 |
| **Total** | **10** | **10** | **8** |

### Complete File List

```
stages/
├── discover/
│   ├── README.md
│   ├── templates/
│   │   ├── brief.md            # Deliverable
│   │   ├── concept.md          # Support
│   │   ├── research.md         # Support
│   │   └── validation.md       # Support
│   └── prompts/
│       ├── review.md
│       └── validate.md
│
├── design/
│   ├── README.md
│   ├── templates/
│   │   ├── architecture.md     # Deliverable
│   │   ├── data-model.md       # Deliverable
│   │   ├── stack.md            # Deliverable
│   │   ├── context-schema.md   # Support
│   │   └── dependencies.md     # Support
│   └── prompts/
│       ├── review.md
│       └── validate.md
│
├── setup/
│   ├── README.md
│   ├── templates/
│   │   ├── plan-product.md     # Deliverable
│   │   ├── plan-feature.md     # Deliverable
│   │   ├── plan-project.md     # Deliverable
│   │   ├── tasks-product.md    # Deliverable
│   │   ├── tasks-feature.md    # Deliverable
│   │   ├── tasks-project.md    # Deliverable
│   │   ├── repo-init.md        # Support
│   │   ├── scaffolding.md      # Support
│   │   ├── ci-cd.md            # Support
│   │   ├── testing.md          # Support
│   │   └── git-workflow.md     # Support
│   └── prompts/
│       ├── review.md
│       └── validate.md
│
└── develop/
    ├── README.md
    └── prompts/
        ├── review.md
        └── validate.md
```

---

## Hard Requirements

All plan and tasks templates include mandatory agent behavior rules:

| Requirement | Rule |
|-------------|------|
| **Task start** | Mark task `[~]` in-progress BEFORE starting work |
| **Task complete** | Mark task `[x]` complete IMMEDIATELY after finishing |
| **Commits** | Commit after EACH completed task, not batched |
| **Checkpoints** | STOP at checkpoints and wait for human review |
| **Decisions** | Document ALL decisions inline with the task |
| **Blockers** | Mark task `[!]` blocked and explain; do NOT skip |

These rules are also documented in Tier 1 memory: `mem/tier1_kit/project/rules/20-task-management.md`

---

## Status Symbols

Used across all task documents:

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Pending - not started |
| `[~]` | In progress - currently working |
| `[x]` | Complete - finished |
| `[!]` | Blocked - cannot proceed |
| `[-]` | Skipped - intentionally not doing |

---

## Related Documents

- Stage READMEs provide detailed guidance for each stage
- Prompts are used by `/review-stage` and `/validate-stage` skills
- Plan file: `~/.claude/plans/luminous-sparking-wilkes.md`

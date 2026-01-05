---
type: "stage_guide"
stage: "design"
description: "Stage 2: Define how the solution will work technically"
version: "1.0.0"
updated: "2026-01-04T00:00:00"
---

# Design Stage

## Overview

**Purpose:** Define how the solution will work technically. Translate the brief into architecture, data models, and technology decisions.

**Key Question:** How will the solution work?

**When to enter:** Brief approved, problem validated, ready for technical design.

**When to exit:** Architecture reviewed, data model defined, stack decisions finalized.

---

## Inputs

From Discover stage:
- `brief.md` - What we're building and why
- Problem statement and success criteria
- Scope boundaries and constraints

---

## Deliverables

Required outputs to advance to Setup stage:

| Artifact | Purpose |
|----------|---------|
| `architecture.md` | System structure, components, and data flow |
| `data-model.md` | Database schema, entities, and relationships |
| `stack.md` | Technology choices with rationale |

All three deliverables must be complete and reviewed before advancing.

---

## Support Artifacts

Working documents that inform deliverables. Archived at Setup completion.

| Artifact | Purpose | When to Use |
|----------|---------|-------------|
| `context-schema.md` | Agent context structure | When building AI/agent features |
| `dependencies.md` | Package evaluation and research | When selecting libraries/frameworks |

Not all support artifacts are required. Use what's needed based on project complexity.

---

## Checklist

### Phase 1: Architecture Design
- [ ] Review brief constraints and success criteria
- [ ] Identify major system components
- [ ] Define component boundaries and responsibilities
- [ ] Map data flow between components
- [ ] Design API contracts (if applicable)
- [ ] Address security considerations
- [ ] Document in `architecture.md`

### Phase 2: Data Modeling
- [ ] Identify core entities from brief
- [ ] Define entity attributes and types
- [ ] Map relationships between entities
- [ ] Consider query patterns and access patterns
- [ ] Plan migration strategy (if applicable)
- [ ] Document in `data-model.md`

### Phase 3: Stack Selection
- [ ] Evaluate technology options against constraints
- [ ] Research dependencies (`dependencies.md` if needed)
- [ ] Select frontend stack (if applicable)
- [ ] Select backend stack (if applicable)
- [ ] Select database/storage solution
- [ ] Document decisions with rationale in `stack.md`

### Phase 4: Agent/AI Design (if applicable)
- [ ] Define context structure
- [ ] Design prompt templates
- [ ] Plan context injection strategy
- [ ] Document in `context-schema.md`

### Phase 5: Review & Validate
- [ ] Run content review (prompts/review.md)
- [ ] Address review feedback
- [ ] Run structural validation (prompts/validate.md)
- [ ] Confirm ready for Setup stage

---

## Templates

- [architecture.md](templates/architecture.md) - **Deliverable** - System architecture
- [data-model.md](templates/data-model.md) - **Deliverable** - Database schema
- [stack.md](templates/stack.md) - **Deliverable** - Technology choices
- [context-schema.md](templates/context-schema.md) - Agent context design
- [dependencies.md](templates/dependencies.md) - Package evaluation

---

## Prompts

- [Review Prompt](prompts/review.md) - Content analysis of design quality
- [Validation Prompt](prompts/validate.md) - Structural completeness check

---

## Exit Criteria

Before advancing to Setup:

| Criterion | Check |
|-----------|-------|
| Architecture complete | All major components defined with clear boundaries |
| Data model complete | Core entities, attributes, and relationships documented |
| Stack decided | All technology choices made with rationale |
| Constraints honored | Design fits within brief's constraints |
| Scalability considered | Design can handle expected load/growth |
| Security addressed | Authentication, authorization, data protection planned |
| Validation passed | Structural check passes |

---

## Common Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Over-engineering | Design for current scope, not hypothetical future |
| Analysis paralysis | Time-box research, make decisions, move forward |
| Ignoring constraints | Revisit brief constraints before finalizing |
| Skipping data model | Even "simple" projects benefit from entity definition |
| Undocumented decisions | Capture WHY, not just WHAT, in stack.md |
| Premature optimization | Focus on correctness first, optimize later |

---

## Design Principles

### 1. Trace to Brief
Every design decision should connect to something in the brief. If it doesn't serve a stated goal, question whether it's needed.

### 2. Simplest Thing That Works
Choose boring technology. Prefer proven solutions. Add complexity only when required.

### 3. Document the Why
Future you (or an agent) needs to understand not just what was decided, but why. Capture the reasoning.

### 4. Design for Change
Requirements will evolve. Prefer loose coupling, clear interfaces, and modular components.

### 5. Security by Default
Build security in from the start. It's harder to add later.

---

## Stage Flow

```
brief.md (from Discover)
    ↓
architecture.md (system design)
    ↓
data-model.md (entities & relationships)
    ↓
stack.md (technology choices)
    ↓
Review (content) → Fix → Validate (structure)
    ↓
Advance to Setup
```

---

## Relationship to Other Artifacts

```
brief.md (Discover)
    │
    ├── architecture.md ─────┐
    │       │                │
    │       ▼                │
    │   data-model.md        │
    │       │                │
    │       ▼                │
    └── stack.md ◄───────────┘
            │
            ▼
    plan.md (Setup)
```

- **Architecture** defines what components exist
- **Data model** defines what data those components work with
- **Stack** defines what technologies implement the components
- All three inform the implementation **plan** in Setup

---

## Previous Stage

**Discover** - Understand what we're building and why.

## Next Stage

**Setup** - Initialize environment and create implementation plan.

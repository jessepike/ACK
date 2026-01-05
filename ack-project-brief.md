---
type: "project_brief"
description: "ACK concept, scope, stages, artifact hierarchy, and MVP approach"
version: "0.3.0"
updated: "2025-01-04T00:00:00"

depends_on: ["ack-intent.md"]
---

# ACK Project Brief

## Executive Summary

ACK (Agent Context Kit) is a meta-project that produces reusable templates, workflows, and orchestration patterns for AI-assisted software development. It solves the fundamental problem of managing ephemeral AI agents that start cold every session.

**Core outcome:** Better results, faster, more consistent, higher quality at higher velocity.

---

## The Problem (Why)

AI agents are ephemeral. They spin up, do work, and disappear. This creates three interconnected problems:

| Problem | Symptom | Impact |
|---------|---------|--------|
| **Context Management** | Cold starts, re-explanation tax | Time waste, inconsistency, fatigue |
| **Drift** | Agents diverge from intent | Rework, quality issues, trust erosion |
| **No Structure** | Ad-hoc workflows, no repeatability | Inconsistency, missing steps, cognitive load |

**Root cause:** No systematic context management for ephemeral agents.

---

## The Solution (What)

A structured system with three parts:

### 1. Set Context
Define what context exists through hierarchical artifacts:
- Intent (North Star)
- Principles (framework/guardrails)
- Brief (concept + high-level tech)
- Architecture (technical master)
- Derivatives (progressive detail)

### 2. Feed Context
Load the right amount at the right time:
- Source artifacts (read occasionally, maintained carefully)
- Derivative artifacts (loaded every session - CLAUDE.md, rules/)
- Goldilocks priming - not too much, not too little

### 3. Validate Context
Catch drift before it causes damage:
- Intent as anchor for all work
- Agent rules and principles
- Validation mechanisms (MVP: manual; Future: automated)

---

## Stage Model (How)

Work flows through 4 sequential stages with iteration back as needed:

| # | Stage | Purpose | Key Question | Deliverables |
|---|-------|---------|--------------|--------------|
| 1 | **Discover** | What & Why | What problem are we solving? | `brief.md` |
| 2 | **Design** | How (technical) | How will the solution work? | `architecture.md`, `data-model.md`, `stack.md` |
| 3 | **Setup** | Ready to execute | Are we ready to start coding? | `plan.md`, `tasks.md` |
| 4 | **Develop** | Doing (runtime) | Is it built correctly? | (updates `tasks.md`) |

**Key insight:** Stages 1-3 are planning/front-loading (before code). Stage 4 is doing (runtime).

### Stage 1: Discover
**Intent:** Validate and flesh out a concept
**Process:** Iterative refinement + content review cycles
**Deliverable:** `brief.md` (flexible format adapting to feature/product/project scope)
**Support Artifacts:** concept.md, research.md, validation.md (archived after Setup)
**Exit:** Brief reviewed and validated

### Stage 2: Design
**Intent:** Define HOW we're building technically
**Process:** Architecture design + content review
**Deliverables:** `architecture.md`, `data-model.md`, `stack.md`
**Support Artifacts:** context-schema.md, dependencies-research.md (archived after Setup)
**Exit:** Technical design reviewed and validated

### Stage 3: Setup
**Intent:** Initialize everything needed for development + create execution plan
**Process:** Scaffold project, configure CI/CD, create implementation plan
**Deliverables:** `plan.md`, `tasks.md`
**Support Artifacts:** ci-cd-config.md, testing-strategy.md, git-workflow.md (archived)
**Exit:** Repo initialized, plan complete, tasks broken down, ready to code

### Stage 4: Develop
**Intent:** Execute the implementation plan
**Process:** Agents code against plan/tasks with human oversight checkpoints
**Output:** Working software (updates `tasks.md` as work progresses)
**Exit:** MVP complete per success criteria

---

## Stage Structure

Each stage follows a consistent structure:

```
stages/
├── discover/
│   ├── README.md          # Overview, artifacts, deliverables, checklist
│   ├── templates/         # Artifact templates (concept.md, brief.md, etc.)
│   └── prompts/           # Stage-specific prompts
│       ├── review.md      # Content analysis prompt
│       └── validate.md    # Structural check prompt
├── design/
├── setup/
└── develop/
```

### Two Quality Gates Per Stage

| Gate | Purpose | What it checks |
|------|---------|----------------|
| **Review** | Content analysis | Is the brief clear? Is architecture sound? Quality of thinking |
| **Validation** | Structural check | YAML frontmatter correct? All sections present? Format right? |

**Stage flow:** Work → Review (content) → Fix → Validate (structure) → Advance

### Stage Workflow Skills

| Skill | Purpose |
|-------|---------|
| `/init-project` | Initialize `.ack/` structure, set stage to Discover |
| `/review-stage <stage>` | Run content analysis on deliverables |
| `/validate-stage <stage>` | Run structural check on deliverables |
| `/advance-stage <to>` | Validate current stage, move deliverables to `docs/`, advance |
| `/archive-planning` | Archive support artifacts to `~/.ack/archives/` |

**Full workflow:**
```
/init-project → work → /review-stage → /validate-stage → /advance-stage → repeat
```

---

## Working Directory & Archives

**During Planning (Stages 1-3):**
- Working directory: `.ack/` in project root
- Contains stage subdirectories with work-in-progress artifacts
- Add to `.gitignore`

**After Setup Completes:**
- Deliverables move to `/docs` in final repo
- Support artifacts archived to `~/.ack/archives/[project-name]/`
- Archive lives outside project so agents don't accidentally read old research

**Final repo structure:**
```
project/
├── docs/              # Deliverables only
│   ├── brief.md
│   ├── architecture.md
│   ├── data-model.md
│   ├── stack.md
│   ├── plan.md
│   └── tasks.md
├── src/               # Application code
├── tests/             # Test files
└── .ack/              # Minimal - just archives-manifest.md
```

---

## Artifact Hierarchy

```
Intent (North Star - outcome focused)
    └── Principles (framework to work within)
        └── Brief (concept + high-level tech rolled up)
            ├── Architecture.md (master technical)
            │   ├── Frontend design
            │   ├── Backend design
            │   └── Schemas, data models
            └── Other derivatives (ICP, etc.)
```

**Key relationships:**
- Each level increases specificity
- Lower levels are derivatives of higher levels
- Source artifacts → Derivative artifacts (for agent consumption)
- ADRs are cross-cutting support artifacts (decision log)

---

## Artifact Classification

### Deliverables (Go to /docs)
Required outputs that must be complete to advance. Persist in final repo.

| Stage | Deliverable | Purpose |
|-------|-------------|---------|
| Discover | `brief.md` | What & why we're building |
| Design | `architecture.md` | System structure and data flow |
| Design | `data-model.md` | Database schema and relationships |
| Design | `stack.md` | Technology choices with rationale |
| Setup | `plan.md` | Phased implementation plan |
| Setup | `tasks.md` | Work breakdown (updated during Develop) |

### Support Artifacts (Archived)
Working documents that inform deliverables but don't advance to next stage.

| Stage | Support Artifact | Purpose |
|-------|------------------|---------|
| Discover | concept.md | Working concept iteration |
| Discover | research.md | Market/competitive research |
| Discover | validation.md | User interviews, problem validation |
| Design | context-schema.md | Agent context structure |
| Design | dependencies-research.md | Package evaluation |
| Setup | ci-cd-config.md | Pipeline configuration notes |
| Setup | testing-strategy.md | Test approach documentation |
| Setup | git-workflow.md | Branch/PR process notes |

### System Artifacts (Always Loaded)

| Artifact | Type | Purpose |
|----------|------|---------|
| Intent | Source | North Star anchor |
| CLAUDE.md | Derivative | Loaded every session |
| rules/* | Derivative | Agent guardrails |
| ADRs | Supporting | Decision log (cross-cutting) |

---

## MVP Scope

### In Scope (MVP)
- Clear structure and artifacts defined
- Intent document as anchor
- 4-stage model with consistent structure (README, templates, prompts per stage)
- Artifact hierarchy established (deliverables vs support)
- Two quality gates: Review (content) + Validation (structural)
- Agent rules and principles
- Tier-1 memory (context priming)
- Working directory (`.ack/`) and archive (`~/.ack/archives/`) pattern
- Stage workflow skills (all complete):
  - `/init-project` - Initialize ACK project structure
  - `/review-stage` - Content analysis of deliverables
  - `/validate-stage` - Structural check for completion
  - `/advance-stage` - Move to next stage (validates first)
  - `/archive-planning` - Archive support artifacts after Setup

### Deferred (Backlog)
- Automated enforcement (hooks)
- Tier-2 memory (state tracking database)
- Automated drift detection
- Advanced CLI tooling
- Self-running validation agents

---

## Technical Approach

### File-First Architecture
- All artifacts are markdown + YAML frontmatter
- Version controlled with git
- Progressive disclosure through hierarchy
- Machine-readable structure, human-readable content

### Context Management
- Source artifacts maintained carefully, read occasionally
- Derivative artifacts (CLAUDE.md, rules/) loaded every session
- Clear separation: system definition vs project instance

### Validation Model (MVP)
- Manual external review loops
- Human judgment for stage exits
- Enforcement through clear documentation, not automation

---

## Success Criteria

- **Zero re-explanation tax:** Sessions start with context auto-loaded
- **Drift caught early:** Divergence flagged during generation, not after
- **Artifacts as specification:** Documents are executable by AI
- **Reusable patterns:** Each project improves the system

---

## Constraints

- **Solo developer optimized:** Built for one person, not teams
- **Incremental adoption:** Each stage independently usable
- **File-first:** No databases for MVP (except future Tier-2 memory)
- **Manual before automated:** Prove the workflow works before automating

---

## Open Questions

### Resolved
- ~~What's the exact structure for Plan and Tasks artifacts?~~ → Defined in Setup stage templates
- ~~What validation is needed at each stage exit?~~ → Two gates: Review (content) + Validation (structural)
- ~~Where do support artifacts go?~~ → Archived to `~/.ack/archives/` at Setup completion
- ~~Stage names?~~ → Discover, Design, Setup, Develop

### Still Open
1. Should Principles be a separate artifact or part of Intent?
2. How do we handle iteration back up the stack (updating higher artifacts)?
3. How do tasks relate to features from scope?
4. How do artifacts feed into CLAUDE.md context?
5. Should artifacts auto-update memory tier?

---

## Supporting Documents

- `ack-intent.md` - North Star anchor
- `ack-src/gov/` - Artifact Governance System (AGS)
- `ack-src/mem/` - Tier-1 Memory Kit
- `ack-src/registry/` - Agent primitives

---

## Next Steps

### Completed
1. ~~Review and validate this Brief~~ → Updated with new stage structure
2. ~~Create stage README.md files~~ → 4 files created (discover, design, setup, develop)
3. ~~Create stage prompts~~ → 8 prompts (review.md + validate.md per stage)
4. ~~Create `brief.md` template~~ → Discover deliverable template
5. ~~Create all stage templates~~ → 20 templates across all stages
6. ~~Update ARTIFACT_INVENTORY.md~~ → Complete catalog of artifacts
7. ~~Create `/review-stage` skill~~ → Content analysis
8. ~~Create `/validate-stage` skill~~ → Structural check
9. ~~Create `/advance-stage` skill~~ → Stage transitions
10. ~~Create `/init-project` skill~~ → Project initialization
11. ~~Create `/archive-planning` skill~~ → Archive support artifacts

### Remaining
1. Update project CLAUDE.md with stage workflow
2. Clean up old stage directories (1-discovery/, 4-implementation/)
3. Test the full workflow on a real project
4. Document onboarding guide for new projects

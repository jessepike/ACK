---
type: "project_brief"
description: "ACK concept, scope, stages, artifact hierarchy, and MVP approach"
version: "0.1.0"
updated: "2026-01-03T00:00:00"

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

### Stage 1: Discovery
**Intent:** Validate and flesh out a concept
**Process:** Iterative refinement + external agent review cycles
**Output:** Project Brief
**Exit:** Human judgment ("good enough")

### Stage 2: Design
**Intent:** Define WHAT we're building technically
**Process:** Architecture design + external validation
**Output:** Architecture.md + derivatives (data model, schemas, component designs)
**Exit:** Technical design validated

### Stage 3: Setup (Environment + Workflow)
**Intent:** Initialize everything needed for implementation
**Process:** Scaffold project, configure agents, set up harness
**Output:** Fully configured project ready for agents
**Exit:** All tooling and context in place

### Stage 4: Implementation Planning
**Intent:** Create structured plan agents execute against
**Process:** Work with Planning Agent to create phases, milestones, tasks
**Output:** Plan + Tasks (separate artifacts)
**Exit:** Agents can begin execution with clear what/why/how

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

| Artifact | Type | Readability | Handoff? |
|----------|------|-------------|----------|
| Intent | Source | Human + Machine | Referenced, not passed |
| Principles | Source | Human + Machine | Distilled into rules |
| Brief | Source/Deliverable | Human + Machine | Stage 1 → Stage 2 |
| Architecture | Source | Human + Machine | Stage 2 → Stage 3 |
| CLAUDE.md | Derivative | Machine | Loaded every session |
| rules/* | Derivative | Machine | Loaded every session |
| Plan | Deliverable | Human + Machine | Stage 4 → Execution |
| Tasks | Deliverable | Machine | Agent consumption |
| ADRs | Supporting | Human | Reference/log |
| Research docs | Supporting | Human | Archived |

---

## MVP Scope

### In Scope (MVP)
- Clear structure and artifacts defined
- Intent document as anchor
- 4-stage model documented
- Artifact hierarchy established
- Agent rules and principles
- Tier-1 memory (context priming)
- Manual validation workflows
- External review prompts/templates

### Deferred (Backlog)
- Automated enforcement (hooks)
- Tier-2 memory (state tracking database)
- Automated drift detection
- CLI tooling
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

1. Should Principles be a separate artifact or part of Intent?
2. What's the exact structure for Plan and Tasks artifacts?
3. How do we handle iteration back up the stack (updating higher artifacts)?
4. What validation is needed at each stage exit?

---

## Supporting Documents

- `ack-intent.md` - North Star anchor
- `ack-src/gov/` - Artifact Governance System (AGS)
- `ack-src/mem/` - Tier-1 Memory Kit
- `ack-src/registry/` - Agent primitives

---

## Next Steps

1. Review and validate this Brief (external agent review)
2. Define canonical directory structure
3. Clean up inbox (dedupe against existing folders)
4. Enhance Intent document with learnings
5. Begin Design stage (Architecture)

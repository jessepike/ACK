---
type: "stage_guide"
stage: "discover"
description: "Stage 1: Understand what we're building and why"
version: "1.0.0"
updated: "2026-01-04T00:00:00"
---

# Discover Stage

## Overview

**Purpose:** Understand what we're building and why. Validate the problem and opportunity.

**Key Question:** What problem are we solving?

**When to enter:** Starting a new project, feature, or initiative.

**When to exit:** Problem validated, brief complete, ready for technical design.

---

## Inputs

- Initial idea, request, or problem statement
- Stakeholder input (if available)
- Market context or competitive landscape (if known)

---

## Deliverable

Required output to advance to Design stage:

| Artifact | Purpose |
|----------|---------|
| `brief.md` | What & why we're building (single flexible format) |

The brief captures the validated problem, solution concept, success criteria, and scope boundaries. It's the single source of truth for "what are we building and why."

---

## Support Artifacts

Working documents that inform the brief. Archived at Setup completion.

| Artifact | Purpose | When to Use |
|----------|---------|-------------|
| `concept.md` | Working concept iteration | Early exploration, before validation |
| `research.md` | Market/competitive research | When market context matters |
| `validation.md` | User interviews, problem validation | When validating assumptions |

Not all support artifacts are required for every project. Use what's needed based on scope and risk.

---

## Checklist

### Phase 1: Explore
- [ ] Capture initial idea or problem statement
- [ ] Identify target users/customers
- [ ] Draft initial concept in `concept.md`
- [ ] List key assumptions to validate

### Phase 2: Research (if needed)
- [ ] Analyze market landscape
- [ ] Identify competitors and alternatives
- [ ] Document findings in `research.md`
- [ ] Identify differentiation opportunity

### Phase 3: Validate (if needed)
- [ ] Define validation approach
- [ ] Conduct user interviews or research
- [ ] Document findings in `validation.md`
- [ ] Confirm problem exists and is worth solving

### Phase 4: Synthesize
- [ ] Consolidate learnings into `brief.md`
- [ ] Define success criteria
- [ ] Set scope boundaries (in/out)
- [ ] Identify constraints and risks

### Phase 5: Review & Validate
- [ ] Run content review (prompts/review.md)
- [ ] Address review feedback
- [ ] Run structural validation (prompts/validate.md)
- [ ] Confirm ready for Design stage

---

## Templates

- [concept.md](templates/concept.md) - Working concept document
- [research.md](templates/research.md) - Market/competitive research
- [validation.md](templates/validation.md) - Problem validation findings
- [brief.md](templates/brief.md) - **Deliverable** - Final brief

---

## Prompts

- [Review Prompt](prompts/review.md) - Content analysis of brief quality
- [Validation Prompt](prompts/validate.md) - Structural completeness check

---

## Exit Criteria

Before advancing to Design:

| Criterion | Check |
|-----------|-------|
| Problem clarity | Can articulate the problem in one sentence |
| User identification | Know who we're building for |
| Differentiation | Understand why this solution vs alternatives |
| Success definition | Have measurable success criteria |
| Scope boundaries | Clear on what's in/out of scope |
| Brief complete | All required sections filled in |
| Validation passed | Structural check passes |

---

## Common Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Skipping validation | At minimum, validate core assumptions |
| Scope creep | Define boundaries early, push back on additions |
| Solution-first thinking | Start with problem, not implementation |
| Missing success criteria | Define how you'll know it worked |
| Vague target user | Be specific about who benefits |

---

## Stage Flow

```
Initial Idea
    ↓
concept.md (iterate)
    ↓
research.md + validation.md (as needed)
    ↓
brief.md (synthesize)
    ↓
Review (content) → Fix → Validate (structure)
    ↓
Advance to Design
```

---

## Next Stage

**Design** - Define how the solution will work technically.

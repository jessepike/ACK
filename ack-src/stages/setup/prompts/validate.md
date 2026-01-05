---
type: prompt
stage: setup
prompt: validate
description: "Structural validation prompt for Setup stage deliverables"
version: 1.0.0
updated: "2026-01-04T00:00:00"
---

# Setup Stage Validation

Validate plan and tasks documents for structural completeness.

## Instructions

You are validating Setup stage deliverables for **structural completeness**. This is NOT a content review - you're checking that all required elements exist and are properly formatted.

Both documents must pass validation to advance.

---

## Pre-Validation: Environment Checks

Before validating documents, verify environment setup:

| Check | Command/Method | Status |
|-------|---------------|--------|
| Repository exists | `git status` succeeds | [ ] Pass / Fail |
| Dependencies install | `npm install` or equivalent succeeds | [ ] Pass / Fail |
| Project builds/runs | Build or dev server starts | [ ] Pass / Fail |
| Tests run | Test command executes | [ ] Pass / Fail |
| CI/CD configured | Pipeline file exists and runs | [ ] Pass / Fail |

If any environment check fails, note as blocking issue.

---

## Document 1: plan.md

### 1.1 YAML Frontmatter

```yaml
---
type: artifact
stage: setup
artifact: plan
description: "[non-empty string]"
version: [valid semver]
updated: "[valid ISO date]"
status: [draft|review|approved|locked]
---
```

- [ ] Frontmatter exists and is valid YAML
- [ ] `type` is "artifact"
- [ ] `stage` is "setup"
- [ ] `artifact` is "plan"
- [ ] Required fields present and valid

### 1.2 Required Sections

| Section | Required | Check |
|---------|----------|-------|
| Overview/Summary | Yes | [ ] Exists with plan summary |
| Phases | Yes | [ ] At least 2 phases defined |
| Milestones | Yes | [ ] At least 1 milestone per phase |
| Checkpoints | Yes | [ ] At least 1 human checkpoint defined |
| Dependencies | No | [ ] Exists if phases have dependencies |
| Timeline | No | [ ] Exists if time estimates provided |

### 1.3 Content Completeness

For each phase:
- [ ] Phase has a name/title
- [ ] Phase has a description of what gets built
- [ ] Phase has a milestone (completion criteria)

For checkpoints:
- [ ] At least 1 checkpoint defined
- [ ] Checkpoint specifies when it occurs
- [ ] Checkpoint specifies what gets reviewed

Minimum requirements:
- [ ] At least 2 phases defined
- [ ] At least 2 milestones total
- [ ] At least 1 human checkpoint

### 1.4 No Placeholders

- [ ] No `[Phase Name]` placeholders
- [ ] No `[Description]` placeholders
- [ ] No `[Milestone]` placeholders
- [ ] No template instructions remaining

---

## Document 2: tasks.md

### 2.1 YAML Frontmatter

```yaml
---
type: artifact
stage: setup
artifact: tasks
description: "[non-empty string]"
version: [valid semver]
updated: "[valid ISO date]"
status: [draft|review|approved|locked]
---
```

- [ ] Frontmatter exists and is valid YAML
- [ ] `type` is "artifact"
- [ ] `stage` is "setup"
- [ ] `artifact` is "tasks"
- [ ] Required fields present and valid

### 2.2 Required Sections

| Section | Required | Check |
|---------|----------|-------|
| Overview | No | [ ] Exists if context helpful |
| Task List | Yes | [ ] Tasks organized by phase or category |
| Status Legend | No | [ ] Exists if custom statuses used |
| Blockers | No | [ ] Exists if blockers identified |

### 2.3 Task Format

Each task should have:
- [ ] Task identifier or checkbox (`- [ ]` format)
- [ ] Task description (what to do)
- [ ] Phase/category association (explicit or via grouping)

Minimum requirements:
- [ ] At least 5 tasks defined
- [ ] Tasks use consistent format (checkboxes or numbered)
- [ ] Tasks grouped by phase/category

### 2.4 Task Completeness

- [ ] Every plan phase has at least 1 task
- [ ] No duplicate tasks
- [ ] Tasks are specific actions (not vague goals)

### 2.5 No Placeholders

- [ ] No `[Task description]` placeholders
- [ ] No `[Phase]` placeholders
- [ ] No template instructions remaining

---

## Cross-Document Validation

### Plan ↔ Tasks Alignment

- [ ] **Phase coverage:** Every phase in plan.md has tasks in tasks.md
- [ ] **No orphan tasks:** Every task group maps to a plan phase
- [ ] **Naming consistent:** Phase names match between documents

### Plan ↔ Design Alignment

- [ ] **Architecture covered:** Phases address architecture components
- [ ] **Data model covered:** Database/schema work included
- [ ] **Stack aligned:** Plan uses technologies from stack.md

### Quantity Checks

| Metric | Minimum | Actual | Status |
|--------|---------|--------|--------|
| Phases | 2 | [count] | Pass/Fail |
| Milestones | 2 | [count] | Pass/Fail |
| Checkpoints | 1 | [count] | Pass/Fail |
| Tasks | 5 | [count] | Pass/Fail |
| Tasks per phase | 1 | [min count] | Pass/Fail |

---

## Validation Output

### Environment Results

| Check | Status | Notes |
|-------|--------|-------|
| Repository | Pass / Fail | [Issue if fail] |
| Dependencies | Pass / Fail | [Issue if fail] |
| Build/Run | Pass / Fail | [Issue if fail] |
| Tests | Pass / Fail | [Issue if fail] |
| CI/CD | Pass / Fail | [Issue if fail] |

### Document Results

| Document | Frontmatter | Sections | Content | Placeholders | Status |
|----------|-------------|----------|---------|--------------|--------|
| plan.md | Pass/Fail | Pass/Fail | Pass/Fail | Pass/Fail | Valid/Invalid |
| tasks.md | Pass/Fail | Pass/Fail | Pass/Fail | Pass/Fail | Valid/Invalid |

### Cross-Document Results

| Check | Status | Issue |
|-------|--------|-------|
| Phase ↔ Task alignment | Pass/Fail | [If fail, describe mismatch] |
| Plan ↔ Design alignment | Pass/Fail | [If fail, what's missing] |
| Quantity checks | Pass/Fail | [If fail, what's short] |

### Issues Found

| Issue | Document/Area | Category | How to Fix |
|-------|---------------|----------|------------|
| [Issue 1] | [doc] | [Category] | [Specific fix] |
| [Issue 2] | [doc] | [Category] | [Specific fix] |

### Verdict

**[ ] VALID** - All checks pass, Setup stage can advance to Develop

**[ ] INVALID** - Issues must be fixed before advancing

---

## Quick Checklist

For fast validation:

1. [ ] Environment: repo exists, deps install, project runs, tests run, CI works
2. [ ] plan.md: valid frontmatter, 2+ phases, 2+ milestones, 1+ checkpoint
3. [ ] tasks.md: valid frontmatter, 5+ tasks, every phase has tasks
4. [ ] No placeholder text in either document
5. [ ] Phase names consistent between plan and tasks
6. [ ] All architecture components have corresponding plan phases

If all 6 pass, the Setup stage is structurally valid.

---

## Archive Readiness

If validation passes, confirm readiness for archive:

- [ ] All deliverables (plan.md, tasks.md) ready to move to `/docs`
- [ ] Support artifacts identified for archive
- [ ] `.ack/archives-manifest.md` will be created

Setup completion triggers archiving of all Discover, Design, and Setup support artifacts.

---

## Validation vs. Review

| Validation (This Prompt) | Review (review.md) |
|--------------------------|-------------------|
| Checks structure exists | Checks plan soundness |
| Checks environment ready | Checks task actionability |
| Binary pass/fail | Qualitative assessment |
| "Is everything in place?" | "Is the plan good?" |

Both documents must pass BOTH validation AND review to advance.

---
type: prompt
stage: discover
prompt: validate
description: "Structural validation prompt for Discover stage deliverables"
version: 1.0.0
updated: "2026-01-04T00:00:00"
---

# Discover Stage Validation

Validate the brief for structural completeness and format correctness.

## Instructions

You are validating a project brief for **structural completeness**. This is NOT a content review - you're checking that all required elements exist and are properly formatted.

Run through each check below. A brief must pass ALL required checks to advance.

---

## Validation Checks

### 1. YAML Frontmatter

```yaml
---
type: artifact
stage: discover
artifact: brief
description: "[non-empty string]"
version: [valid semver]
updated: "[valid ISO date]"
status: [draft|review|approved|locked]
---
```

- [ ] Frontmatter exists and is valid YAML
- [ ] `type` is "artifact"
- [ ] `stage` is "discover"
- [ ] `artifact` is "brief"
- [ ] `description` is non-empty
- [ ] `version` follows semver (e.g., 1.0.0)
- [ ] `updated` is valid ISO date
- [ ] `status` is one of: draft, review, approved, locked

---

### 2. Required Sections

Check that these sections exist and are non-empty:

| Section | Required | Check |
|---------|----------|-------|
| Summary | Yes | [ ] Exists and has content |
| Problem | Yes | [ ] Exists with Problem Statement subsection |
| Problem > Who Has This Problem | Yes | [ ] Has at least 1 user type identified |
| Solution | Yes | [ ] Exists with Core Concept subsection |
| Solution > Key Capabilities | Yes | [ ] Has at least 1 capability listed |
| Scope > In Scope | Yes | [ ] Has at least 1 item |
| Scope > Out of Scope | Yes | [ ] Section exists (can be empty if genuinely nothing deferred) |
| Success Criteria | Yes | [ ] Has at least 1 must-have criterion |
| Constraints | No | [ ] Section exists if constraints apply |
| Risks | No | [ ] Section exists if risks identified |
| Validation | Yes | [ ] Exists with Problem Validation subsection |
| Open Questions | No | [ ] Section exists (can be empty) |

---

### 3. Content Completeness

These checks verify minimum content thresholds:

- [ ] **Summary** is a complete paragraph (not just a placeholder)
- [ ] **Problem Statement** is 2+ sentences describing the problem
- [ ] **At least 1 user** identified with pain point and workaround
- [ ] **At least 2 capabilities** listed with descriptions
- [ ] **At least 2 in-scope items** for MVP
- [ ] **At least 1 success criterion** that is measurable
- [ ] **At least 1 form of validation** (evidence problem/solution are real)

---

### 4. No Placeholder Text

Check that template placeholders have been replaced:

- [ ] No `[Project Name]` remaining (should be actual name)
- [ ] No `[Description]` placeholders
- [ ] No `[User 1]` or `[User 2]` placeholders
- [ ] No `[Capability 1]` placeholders
- [ ] No `YYYY-MM-DD` date placeholders (should be real dates)
- [ ] No `<!-- comment -->` instructions remaining in content areas

---

### 5. Internal Consistency

- [ ] Project name in title matches references throughout
- [ ] Users mentioned in Problem appear in Solution (we're solving for them)
- [ ] Capabilities in Solution connect to items in Scope
- [ ] Success criteria relate to stated problem/solution

---

### 6. Format Standards

- [ ] Markdown renders correctly (no broken syntax)
- [ ] Tables are properly formatted
- [ ] Checkboxes use `- [ ]` format
- [ ] Headers follow hierarchy (no skipped levels)
- [ ] Links are valid (if any internal links exist)

---

## Validation Output

### Results

| Check Category | Status | Issues |
|----------------|--------|--------|
| YAML Frontmatter | Pass / Fail | [List any failures] |
| Required Sections | Pass / Fail | [List missing sections] |
| Content Completeness | Pass / Fail | [List incomplete areas] |
| No Placeholders | Pass / Fail | [List remaining placeholders] |
| Internal Consistency | Pass / Fail | [List inconsistencies] |
| Format Standards | Pass / Fail | [List format issues] |

### Issues Found

| Issue | Category | How to Fix |
|-------|----------|------------|
| [Issue 1] | [Category] | [Specific fix] |
| [Issue 2] | [Category] | [Specific fix] |

### Verdict

**[ ] VALID** - All required checks pass, brief can advance to Design

**[ ] INVALID** - Issues must be fixed before advancing

---

## Validation vs. Review

| Validation (This Prompt) | Review (review.md) |
|--------------------------|-------------------|
| Checks structure exists | Checks content quality |
| Binary pass/fail | Qualitative assessment |
| Can be automated | Requires judgment |
| "Is the form filled out?" | "Is the thinking sound?" |

A brief must pass BOTH validation AND review to advance.

---

## Quick Checklist

For fast validation, confirm:

1. [ ] YAML frontmatter is valid with correct type/stage/artifact
2. [ ] Summary, Problem, Solution, Scope, Success Criteria sections exist
3. [ ] At least 1 user, 2 capabilities, 2 scope items, 1 success criterion
4. [ ] No placeholder text remaining
5. [ ] Markdown renders correctly

If all 5 pass, the brief is structurally valid.

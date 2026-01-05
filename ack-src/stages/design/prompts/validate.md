---
type: prompt
stage: design
prompt: validate
description: "Structural validation prompt for Design stage deliverables"
version: 1.0.0
updated: "2026-01-04T00:00:00"
---

# Design Stage Validation

Validate architecture, data model, and stack documents for structural completeness.

## Instructions

You are validating three Design stage deliverables for **structural completeness**. This is NOT a content review - you're checking that all required elements exist and are properly formatted.

All three documents must pass validation to advance.

---

## Document 1: architecture.md

### 1.1 YAML Frontmatter

```yaml
---
type: artifact
stage: design
artifact: architecture
description: "[non-empty string]"
version: [valid semver]
updated: "[valid ISO date]"
status: [draft|review|approved|locked]
---
```

- [ ] Frontmatter exists and is valid YAML
- [ ] `type` is "artifact"
- [ ] `stage` is "design"
- [ ] `artifact` is "architecture"
- [ ] Required fields present and valid

### 1.2 Required Sections

| Section | Required | Check |
|---------|----------|-------|
| Overview/Summary | Yes | [ ] Exists with system description |
| Components | Yes | [ ] At least 2 components defined |
| Data Flow | Yes | [ ] Flow between components documented |
| API Design | Conditional | [ ] Exists if system has APIs |
| Security | Yes | [ ] Authentication and/or authorization addressed |
| Diagrams/Visuals | No | [ ] If present, renders correctly |

### 1.3 Content Completeness

- [ ] Each component has: name, responsibility, interfaces
- [ ] Data flow shows: source → transformation → destination
- [ ] Security section addresses: auth method, data protection

### 1.4 No Placeholders

- [ ] No `[Component Name]` placeholders
- [ ] No `[Description]` placeholders
- [ ] No template instructions remaining

---

## Document 2: data-model.md

### 2.1 YAML Frontmatter

```yaml
---
type: artifact
stage: design
artifact: data-model
description: "[non-empty string]"
version: [valid semver]
updated: "[valid ISO date]"
status: [draft|review|approved|locked]
---
```

- [ ] Frontmatter exists and is valid YAML
- [ ] `type` is "artifact"
- [ ] `stage` is "design"
- [ ] `artifact` is "data-model"
- [ ] Required fields present and valid

### 2.2 Required Sections

| Section | Required | Check |
|---------|----------|-------|
| Overview | Yes | [ ] Exists with model summary |
| Entities | Yes | [ ] At least 1 entity defined |
| Relationships | Yes | [ ] Entity relationships documented |
| Schema/ERD | Conditional | [ ] Visual or detailed schema if complex |
| Query Patterns | No | [ ] Exists if performance-critical |
| Migration Strategy | No | [ ] Exists if evolving existing system |

### 2.3 Content Completeness

For each entity:
- [ ] Entity name defined
- [ ] At least 2 attributes/fields listed
- [ ] Field types specified (string, number, date, etc.)
- [ ] Primary key identified

For relationships:
- [ ] At least 1 relationship defined (if multiple entities)
- [ ] Cardinality specified (one-to-one, one-to-many, etc.)

### 2.4 No Placeholders

- [ ] No `[Entity Name]` placeholders
- [ ] No `[field_name]` placeholders
- [ ] No template instructions remaining

---

## Document 3: stack.md

### 3.1 YAML Frontmatter

```yaml
---
type: artifact
stage: design
artifact: stack
description: "[non-empty string]"
version: [valid semver]
updated: "[valid ISO date]"
status: [draft|review|approved|locked]
---
```

- [ ] Frontmatter exists and is valid YAML
- [ ] `type` is "artifact"
- [ ] `stage` is "design"
- [ ] `artifact` is "stack"
- [ ] Required fields present and valid

### 3.2 Required Sections

| Section | Required | Check |
|---------|----------|-------|
| Overview | Yes | [ ] Exists with stack summary |
| Frontend | Conditional | [ ] Exists if project has frontend |
| Backend | Conditional | [ ] Exists if project has backend |
| Database | Yes | [ ] Database choice documented |
| Infrastructure | Yes | [ ] Deployment target specified |
| Dependencies | No | [ ] Key dependencies listed |

### 3.3 Content Completeness

For each technology choice:
- [ ] Technology/tool named
- [ ] Version specified (or "latest" with date)
- [ ] Rationale provided (why this choice)

Minimum requirements:
- [ ] At least 1 language/framework specified
- [ ] Database type and product specified
- [ ] Hosting/deployment target specified

### 3.4 No Placeholders

- [ ] No `[Technology]` placeholders
- [ ] No `[Rationale]` placeholders
- [ ] No template instructions remaining

---

## Cross-Document Validation

### Consistency Checks

- [ ] **Project name matches** across all three documents
- [ ] **Components in architecture** align with **stack choices**
- [ ] **Entities in data model** align with **components in architecture**
- [ ] **Database in stack** is appropriate for **data model** complexity

### Completeness Checks

- [ ] All three documents exist
- [ ] All three documents have valid frontmatter
- [ ] All three documents have required sections filled

---

## Validation Output

### Document Results

| Document | Frontmatter | Sections | Content | Placeholders | Status |
|----------|-------------|----------|---------|--------------|--------|
| architecture.md | Pass/Fail | Pass/Fail | Pass/Fail | Pass/Fail | Valid/Invalid |
| data-model.md | Pass/Fail | Pass/Fail | Pass/Fail | Pass/Fail | Valid/Invalid |
| stack.md | Pass/Fail | Pass/Fail | Pass/Fail | Pass/Fail | Valid/Invalid |

### Cross-Document Results

| Check | Status | Issue |
|-------|--------|-------|
| Consistency | Pass/Fail | [If fail, describe mismatch] |
| Completeness | Pass/Fail | [If fail, what's missing] |

### Issues Found

| Issue | Document | Category | How to Fix |
|-------|----------|----------|------------|
| [Issue 1] | [doc] | [Category] | [Specific fix] |
| [Issue 2] | [doc] | [Category] | [Specific fix] |

### Verdict

**[ ] VALID** - All documents pass, Design stage can advance to Setup

**[ ] INVALID** - Issues must be fixed before advancing

---

## Quick Checklist

For fast validation across all three documents:

1. [ ] All three files exist with valid YAML frontmatter
2. [ ] architecture.md has components + data flow + security
3. [ ] data-model.md has entities with fields + relationships
4. [ ] stack.md has technology choices with rationale
5. [ ] No placeholder text in any document
6. [ ] Terminology consistent across documents

If all 6 pass, the Design stage is structurally valid.

---

## Validation vs. Review

| Validation (This Prompt) | Review (review.md) |
|--------------------------|-------------------|
| Checks structure exists | Checks technical soundness |
| Binary pass/fail | Qualitative assessment |
| Can be automated | Requires judgment |
| "Are the docs complete?" | "Is the design good?" |

All three documents must pass BOTH validation AND review to advance.

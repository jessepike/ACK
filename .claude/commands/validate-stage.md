# Validate Stage

Perform structural validation on stage deliverables to verify format, completeness, and readiness to advance.

## Usage

```
/validate-stage <stage>
```

**Stages:**
- `discover` - Validate brief.md structure
- `design` - Validate architecture.md, data-model.md, stack.md structure
- `setup` - Validate plan.md, tasks.md structure + environment
- `develop` - Validate checkpoint/milestone completion

---

## What This Does

**Validation = Structural Check**

This skill verifies the *format and completeness* of deliverables:
- Does the file exist?
- Is YAML frontmatter present and valid?
- Are required sections present?
- Is the checklist complete?

This is different from `/review-stage` which analyzes *content quality*.

**No content analysis** - Validation doesn't judge whether decisions are good, only whether they're documented.

---

## Process

### Step 1: Identify Stage

Parse the stage argument. Valid values:
- `discover`, `design`, `setup`, `develop`

If invalid, show usage and exit.

### Step 2: Load Validation Prompt

Read the validation prompt for the specified stage:
```
ack-src/stages/{stage}/prompts/validate.md
```

### Step 3: Locate Deliverables

Find deliverables in the project's `.ack/` working directory or `docs/` folder:

| Stage | Required Deliverables |
|-------|----------------------|
| discover | `brief.md` |
| design | `architecture.md`, `data-model.md`, `stack.md` |
| setup | `plan-{scope}.md`, `tasks-{scope}.md` |
| develop | `tasks.md` (updated), checkpoint artifacts |

Search order:
1. `.ack/{stage}/` (working directory)
2. `docs/` (finalized deliverables)
3. Root directory (legacy placement)

### Step 4: Run Validation Checks

For each deliverable, check:

#### A. File Existence
- [ ] File exists at expected location

#### B. YAML Frontmatter
- [ ] Frontmatter block present (`---` delimiters)
- [ ] `type` field present and from controlled vocabulary
- [ ] `description` field present
- [ ] `version` field present (SemVer format)
- [ ] `updated` field present (ISO 8601 format)
- [ ] `status` field present (draft/review/final)

#### C. Required Sections
Check against stage-specific requirements:

**Discover (brief.md)**:
- [ ] Problem Statement section
- [ ] Target Users section
- [ ] Solution Overview section
- [ ] Success Criteria section
- [ ] Scope section (In Scope / Out of Scope)

**Design (architecture.md)**:
- [ ] System Overview section
- [ ] Components section
- [ ] Data Flow section
- [ ] API Design section (if applicable)
- [ ] Security Considerations section

**Design (data-model.md)**:
- [ ] Entities section
- [ ] Relationships section
- [ ] Schema Definition section

**Design (stack.md)**:
- [ ] Technology Choices section
- [ ] Rationale for each choice

**Setup (plan.md)**:
- [ ] Phases/Steps section
- [ ] Checkpoints defined
- [ ] Hard Requirements section

**Setup (tasks.md)**:
- [ ] Task breakdown present
- [ ] Status symbols used correctly
- [ ] Hard Requirements section

#### D. Checklist Completion
- [ ] All checklist items checked or explicitly skipped
- [ ] No unchecked blocking items

### Step 5: Generate Validation Report

Output a structured validation report:

```markdown
## Stage Validation: {Stage Name}

**Date**: {YYYY-MM-DD}
**Result**: PASS / FAIL

---

### Deliverables

| Deliverable | Exists | Frontmatter | Sections | Checklist | Status |
|-------------|--------|-------------|----------|-----------|--------|
| {name} | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | PASS/FAIL |

---

### Detailed Results

#### {Deliverable 1}

**Frontmatter Validation**:
- [✓] type: {value}
- [✓] description: present
- [✓] version: {value}
- [✓] updated: {value}
- [✓] status: {value}

**Section Validation**:
- [✓] {Section 1}: present
- [✗] {Section 2}: MISSING
- [✓] {Section 3}: present

**Checklist Status**:
- {X} of {Y} items complete
- Blocking items incomplete: {list if any}

---

### Validation Summary

**Overall Result**: {PASS/FAIL}

**Blocking Issues** (must fix to advance):
- {Issue 1}
- {Issue 2}

**Warnings** (recommended to fix):
- {Warning 1}

---

### Next Steps

If PASS:
- Ready to advance to {next stage}
- Run `/advance-stage {next-stage}` to proceed

If FAIL:
- Fix blocking issues listed above
- Run `/validate-stage {stage}` again
```

### Step 6: Return Result

- If all checks pass: Report PASS, suggest advancing
- If any blocking checks fail: Report FAIL, list issues to fix

---

## Validation Rules by Stage

### Discover Stage

**Required for PASS:**
- brief.md exists
- Valid YAML frontmatter
- Problem statement clearly articulated
- Target users defined
- Success criteria are measurable (not vague)
- Scope boundaries set

### Design Stage

**Required for PASS:**
- All 3 deliverables exist (architecture, data-model, stack)
- Valid YAML frontmatter on all
- Architecture components listed
- Data entities defined
- Technology choices documented with rationale

### Setup Stage

**Required for PASS:**
- Plan and tasks documents exist (any scope variant)
- Valid YAML frontmatter
- Tasks are granular (not just high-level bullets)
- Hard Requirements section present
- Checkpoints defined in plan
- Environment ready (can verify with checklist)

### Develop Stage

**Required for PASS (at checkpoint):**
- Tasks being updated (in-progress/complete markers)
- Decisions documented inline
- No stale in-progress tasks (started but abandoned)
- Code compiles/runs (if applicable)
- Tests pass (if applicable)

---

## Examples

```
/validate-stage discover
```
Checks brief.md exists, has valid frontmatter, and required sections.

```
/validate-stage design
```
Checks all 3 design deliverables for structure and completeness.

```
/validate-stage setup
```
Checks plan and tasks documents, plus environment readiness.

---

## Related Commands

- `/review-stage <stage>` - Content analysis (quality, soundness)
- `/advance-stage <stage>` - Move to next stage (runs validation first)

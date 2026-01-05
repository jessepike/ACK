# Review Stage

Perform content analysis on stage deliverables to assess quality, completeness, and soundness.

## Usage

```
/review-stage <stage>
```

**Stages:**
- `discover` - Review brief.md
- `design` - Review architecture.md, data-model.md, stack.md
- `setup` - Review plan.md, tasks.md
- `develop` - Review at checkpoint (code + progress)

---

## What This Does

**Review = Content Analysis**

This skill analyzes the *substance* of deliverables:
- Is the content clear and complete?
- Are decisions well-reasoned?
- Are there gaps or inconsistencies?
- Is the quality sufficient to proceed?

This is different from `/validate-stage` which checks *structure* (format, YAML, completeness checklist).

---

## Process

### Step 1: Identify Stage

Parse the stage argument. Valid values:
- `discover`, `design`, `setup`, `develop`

If invalid, show usage and exit.

### Step 2: Load Review Prompt

Read the review prompt for the specified stage:
```
ack-src/stages/{stage}/prompts/review.md
```

### Step 3: Locate Deliverables

Find deliverables in the project's `.ack/` working directory or `docs/` folder:

| Stage | Deliverables |
|-------|--------------|
| discover | `brief.md` |
| design | `architecture.md`, `data-model.md`, `stack.md` |
| setup | `plan-{scope}.md`, `tasks-{scope}.md` |
| develop | Current task + related code |

Search order:
1. `.ack/{stage}/` (working directory)
2. `docs/` (finalized deliverables)
3. Root directory (legacy placement)

### Step 4: Read Deliverables

Load all deliverables for the stage. If any are missing:
- Note which are missing
- Continue with available deliverables
- Include missing items in the review output

### Step 5: Execute Review

Apply the review prompt to analyze each deliverable. The review prompt contains stage-specific criteria.

### Step 6: Generate Review Report

Output a structured review report:

```markdown
## Stage Review: {Stage Name}

**Date**: {YYYY-MM-DD}
**Reviewer**: Claude (automated)

---

### Deliverables Reviewed

| Deliverable | Found | Status |
|-------------|-------|--------|
| {name} | Yes/No | Reviewed / Missing |

---

### {Deliverable 1 Name}

**Overall Assessment**: Strong / Acceptable / Needs Work / Incomplete

**Strengths**:
- {Strength 1}
- {Strength 2}

**Issues**:
- {Issue 1} - {Severity: Critical/Major/Minor}
- {Issue 2} - {Severity}

**Recommendations**:
- {Recommendation 1}
- {Recommendation 2}

---

### {Deliverable 2 Name}
...

---

### Summary

**Ready to proceed?** Yes / Yes with minor fixes / No - requires rework

**Critical issues (must fix)**:
- {Issue if any}

**Suggested improvements (optional)**:
- {Improvement if any}

---

### Next Steps

1. {Action item 1}
2. {Action item 2}
```

### Step 7: Await User Response

After presenting the review, ask:
- "Would you like me to help address any of these issues?"
- "Ready to run `/validate-stage {stage}` for structural check?"

---

## Review Criteria by Stage

### Discover Stage

Focus on:
- Problem clarity - Is the problem well-defined?
- User understanding - Are target users identified?
- Solution fit - Does the solution address the problem?
- Scope boundaries - Is scope clear and reasonable?
- Success criteria - Are they measurable?

### Design Stage

Focus on:
- Technical soundness - Are decisions defensible?
- Completeness - Are all components addressed?
- Consistency - Do documents align with each other?
- Tradeoffs - Are alternatives considered?
- Feasibility - Can this be built as designed?

### Setup Stage

Focus on:
- Plan coherence - Do phases build logically?
- Task actionability - Are tasks specific enough?
- Scope alignment - Does plan match brief?
- Risk awareness - Are blockers identified?
- Checkpoints - Are review points defined?

### Develop Stage

Focus on:
- Code quality - Does it match design?
- Progress tracking - Are tasks being updated?
- Decision documentation - Are choices recorded?
- Test coverage - Are changes tested?
- Checkpoint readiness - Ready for human review?

---

## Examples

```
/review-stage discover
```
Reviews the brief.md for problem clarity, user understanding, and solution fit.

```
/review-stage design
```
Reviews architecture.md, data-model.md, and stack.md for technical soundness and consistency.

```
/review-stage setup
```
Reviews plan and tasks documents for actionability and scope alignment.

---

## Related Commands

- `/validate-stage <stage>` - Structural check (format, YAML, completeness)
- `/advance-stage <stage>` - Move to next stage (runs validation first)

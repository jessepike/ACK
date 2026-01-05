# Advance Stage

Move to the next stage in the ACK workflow after validating current stage completion.

## Usage

```
/advance-stage <to-stage>
```

**Target stages:**
- `design` - Advance from Discover → Design
- `setup` - Advance from Design → Setup
- `develop` - Advance from Setup → Develop

---

## What This Does

1. **Validates current stage** - Runs `/validate-stage` on the previous stage
2. **Checks for blockers** - Ensures no critical issues
3. **Moves deliverables** - Copies finalized deliverables to `docs/`
4. **Updates state** - Records stage transition
5. **Prepares next stage** - Creates working directory for new stage

**Advancement is blocked if validation fails.** Fix issues and retry.

---

## Stage Transitions

```
Discover ──▶ Design ──▶ Setup ──▶ Develop
   │           │          │          │
   ▼           ▼          ▼          ▼
brief.md   arch.md    plan.md    (runtime)
           data.md    tasks.md
           stack.md
```

| Command | From | To | Validates | Moves to /docs |
|---------|------|-----|-----------|----------------|
| `/advance-stage design` | Discover | Design | brief.md | brief.md |
| `/advance-stage setup` | Design | Setup | arch, data, stack | architecture.md, data-model.md, stack.md |
| `/advance-stage develop` | Setup | Develop | plan, tasks | plan.md, tasks.md |

---

## Process

### Step 1: Identify Transition

Parse the target stage. Determine current stage:

| Target | Current Stage | Validation Required |
|--------|---------------|---------------------|
| `design` | discover | `/validate-stage discover` |
| `setup` | design | `/validate-stage design` |
| `develop` | setup | `/validate-stage setup` |

If target is `discover`, error: "Cannot advance to Discover - it's the first stage."

### Step 2: Run Validation

Execute validation for the current stage:

```
/validate-stage {current-stage}
```

**If validation FAILS:**
```markdown
## Cannot Advance

Validation failed for {current-stage} stage.

**Blocking issues:**
- {Issue 1}
- {Issue 2}

Fix these issues and run `/advance-stage {target}` again.
```

Stop here. Do not proceed.

**If validation PASSES:** Continue to Step 3.

### Step 3: Confirm Advancement

Ask for user confirmation:

```markdown
## Ready to Advance: {Current Stage} → {Target Stage}

**Validation:** PASSED ✓

**What will happen:**
1. Deliverables moved to `docs/`:
   - {deliverable 1}
   - {deliverable 2}

2. Working directory prepared:
   - `.ack/{target-stage}/` created

3. Stage state updated

**Proceed with advancement?** (yes/no)
```

Wait for user confirmation. If "no", abort.

### Step 4: Move Deliverables

Copy deliverables from working directory to `docs/`:

| From Stage | Files to Move |
|------------|---------------|
| discover | `.ack/discover/brief.md` → `docs/brief.md` |
| design | `.ack/design/architecture.md` → `docs/architecture.md` |
| | `.ack/design/data-model.md` → `docs/data-model.md` |
| | `.ack/design/stack.md` → `docs/stack.md` |
| setup | `.ack/setup/plan-*.md` → `docs/plan.md` |
| | `.ack/setup/tasks-*.md` → `docs/tasks.md` |

**Note:** For setup, rename scope-specific files to generic names in docs.

If `docs/` doesn't exist, create it.

### Step 5: Prepare Next Stage

Create working directory for the target stage:

```bash
mkdir -p .ack/{target-stage}
```

### Step 6: Update State

Update `.ack/state.json` (create if doesn't exist):

```json
{
  "currentStage": "{target-stage}",
  "stageHistory": [
    {
      "stage": "{previous-stage}",
      "completedAt": "YYYY-MM-DDTHH:MM:SS",
      "deliverables": ["file1.md", "file2.md"]
    }
  ],
  "startedAt": "YYYY-MM-DDTHH:MM:SS"
}
```

### Step 7: Report Success

```markdown
## Stage Advanced: {Current} → {Target}

**Completed:** {timestamp}

**Deliverables in `docs/`:**
- {file 1}
- {file 2}

**Next steps for {Target} stage:**
- {Step 1 from stage README}
- {Step 2 from stage README}

**Templates available:**
- `ack-src/stages/{target}/templates/`

**When ready:**
- `/review-stage {target}` - Review deliverables
- `/validate-stage {target}` - Check completion
- `/advance-stage {next}` - Move to next stage
```

---

## Special Case: Advance to Develop

When advancing to Develop (from Setup), additional actions:

### Archive Trigger

At Setup → Develop transition, offer to archive support artifacts:

```markdown
## Archive Support Artifacts?

Support artifacts from planning stages can be archived to keep the repo clean.

**Would be archived:**
- `.ack/discover/concept.md`
- `.ack/discover/research.md`
- `.ack/discover/validation.md`
- `.ack/design/context-schema.md`
- `.ack/design/dependencies.md`
- `.ack/setup/repo-init.md`
- `.ack/setup/scaffolding.md`
- `.ack/setup/ci-cd.md`
- `.ack/setup/testing.md`
- `.ack/setup/git-workflow.md`

**Archive location:** `~/.ack/archives/{project-name}/`

**Archive now?** (yes/no/later)
```

If "yes": Run archive process (see `/archive-planning`).
If "no" or "later": Skip, leave in `.ack/`.

### Development Ready Check

Before completing advancement to Develop:

```markdown
## Development Environment Check

- [ ] Repository initialized
- [ ] Dependencies installed
- [ ] Dev server runs
- [ ] Tests pass
- [ ] CI/CD configured

**All checks passing?** (yes/skip)
```

If issues, note them but don't block advancement.

---

## Error Handling

### Invalid Target Stage

```
/advance-stage foo
```

```markdown
## Invalid Stage

`foo` is not a valid stage.

Valid targets: `design`, `setup`, `develop`

Usage: `/advance-stage <to-stage>`
```

### Already at Target Stage

If `.ack/state.json` shows current stage equals target:

```markdown
## Already at {Stage}

You're already in the {Stage} stage.

**To advance further:**
- `/advance-stage {next-stage}`

**To re-validate current stage:**
- `/validate-stage {stage}`
```

### No Working Directory

If `.ack/{current-stage}/` doesn't exist:

```markdown
## No Working Directory Found

Expected `.ack/{current-stage}/` but it doesn't exist.

**Options:**
1. Create working directory and add deliverables
2. Check if deliverables are in `docs/` already
3. Run `/init-project` to set up ACK structure
```

---

## Examples

### Advance from Discover to Design

```
/advance-stage design
```

1. Validates brief.md exists and is complete
2. Moves brief.md to docs/
3. Creates .ack/design/
4. Updates state to "design"
5. Shows Design stage next steps

### Advance from Setup to Develop

```
/advance-stage develop
```

1. Validates plan and tasks documents
2. Moves plan.md and tasks.md to docs/
3. Offers to archive support artifacts
4. Runs development environment check
5. Updates state to "develop"
6. Shows Develop stage guidance

---

## Related Commands

- `/validate-stage <stage>` - Check stage completion (run automatically)
- `/review-stage <stage>` - Content analysis (run before advancing)
- `/archive-planning` - Archive support artifacts manually
- `/init-project` - Initialize ACK project structure

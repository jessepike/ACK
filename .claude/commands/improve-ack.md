# Improve ACK

Analyze backlog insights and apply improvements to ACK stages. This command bridges the gap between curated tips and actual implementation.

## Usage

```
/improve-ack [action] [args]
```

**Actions:**
- `analyze` (default) - Sweep backlog, map tips to stages, create improvement plan
- `preview <title>` - Show what would change for a specific tip (no changes made)
- `apply <title>` - Apply tip to relevant stages, mark as implemented
- `quick-wins` - List tips that are low effort + high impact + affect single stage

---

## Action: `analyze` (Default)

Perform a project-wide analysis of the backlog to identify improvement opportunities.

### Step 1: Load Context

Read these files:
- `/Users/jessepike/code/ack/tips.backlog.md` - The insights backlog
- `/Users/jessepike/code/ack/ack-project-brief.md` - Current ACK structure

### Step 2: Filter Candidates

From the backlog, select insights where:
- Priority: High
- Status: `backlog` (not implemented, rejected, or in-progress)

### Step 3: Map Tips to Stages

For each candidate tip, analyze which ACK stages it affects:

| Stage | Affected If... |
|-------|----------------|
| **Discover** | Changes concept→brief process, research methods, validation approach |
| **Design** | Changes architecture patterns, data modeling, stack decisions |
| **Setup** | Changes repo init, CI/CD, testing, planning, task breakdown |
| **Develop** | Changes runtime workflow, task execution, oversight patterns |
| **All Stages** | Changes review process, validation criteria, or cross-cutting concerns |

Also determine the **change type**:
- `process` - Changes how the stage is executed (affects README.md)
- `template` - Changes artifact structure (affects templates/)
- `review` - Changes content analysis (affects prompts/review.md)
- `validation` - Changes structural checks (affects prompts/validate.md)
- `new-artifact` - Adds a new artifact type
- `new-skill` - Requires a new skill/command to be created

### Step 4: Output Improvement Plan

```markdown
## ACK Improvement Analysis

**Date**: {{YYYY-MM-DD}}
**Candidates analyzed**: X high-priority tips

### Stage Impact Matrix

| Tip | Discover | Design | Setup | Develop | Change Type |
|-----|----------|--------|-------|---------|-------------|
| Shared Mistakes Log | ✓ | ✓ | ✓ | ✓ | new-artifact |
| Subagents for Tasks | | | ✓ | ✓ | new-skill |
| Drift Detection | ✓ | ✓ | ✓ | ✓ | validation |
| ... | | | | | |

### Quick Wins (Low Effort + High Impact)

Tips that can be implemented quickly:
1. [CATEGORY] Title - affects: Stage(s) - change: type
2. ...

### Recommended Implementation Order

Based on dependencies and impact:

1. **First**: [Tip] - Foundation for others
2. **Second**: [Tip] - Builds on #1
3. **Third**: [Tip] - Independent quick win
...

### Complex Items (Needs Planning)

Tips requiring significant work:
- [Tip] - Reason it's complex
- ...

### Not Applicable

Tips reviewed but not applicable to current ACK direction:
- [Tip] - Why it doesn't fit
```

### Step 5: Suggest Next Action

```
Ready to improve? Try:
- /improve-ack preview "Tip Title"  # See proposed changes
- /improve-ack apply "Tip Title"    # Implement a tip
- /improve-ack quick-wins           # Focus on easy wins
```

---

## Action: `preview <title>`

Show exactly what would change for a specific tip without making any modifications.

### Step 1: Find the Tip

Search `tips.backlog.md` for the tip by title (fuzzy match OK).

If not found, output:
```
Tip not found: "{{title}}"

Did you mean one of these?
- [Similar title 1]
- [Similar title 2]
```

### Step 2: Analyze Impact

Determine:
- Which stages are affected
- What type of changes are needed
- Specific files that would be modified

### Step 3: Generate Proposed Changes

For each affected stage, show the proposed modifications:

```markdown
## Preview: [CATEGORY] {{Tip Title}}

**Source**: {{tip source}}
**Description**: {{tip description}}
**Application**: {{tip application}}

---

### Affected Stages

#### Stage: Discover
**Files to modify:**
- `stages/discover/README.md`
- `stages/discover/prompts/validate.md`

**Proposed changes:**

**README.md** - Add to Checklist section:
```diff
+ - [ ] Check mistakes.md for known pitfalls before finalizing brief
```

**prompts/validate.md** - Add validation criterion:
```diff
+ - [ ] No patterns from mistakes.md repeated in deliverable
```

---

#### Stage: Design
**Files to modify:**
- `stages/design/prompts/review.md`

**Proposed changes:**

**prompts/review.md** - Add review question:
```diff
+ - Have we avoided the architectural mistakes documented in mistakes.md?
```

---

### New Files to Create

- `docs/mistakes.md` - Shared mistakes log template

**Template content:**
```markdown
# Mistakes Log

Patterns to avoid, learned from experience.

## Format

### [Date] Category: Brief Title
- **What happened**: Description
- **Why it was wrong**: Impact
- **Correct approach**: What to do instead
```

---

### Summary

| Change | Count |
|--------|-------|
| Files modified | X |
| New files | Y |
| Stages affected | Z |

**Ready to apply?** Run: `/improve-ack apply "{{Tip Title}}"`
```

---

## Action: `apply <title>`

Apply a tip's improvements to the relevant ACK stages.

### Step 1: Find and Validate

1. Find the tip in backlog (fuzzy match OK)
2. Verify status is `backlog` (not already implemented)
3. If tip not found or already implemented, report and exit

### Step 2: Generate Changes

Run the same analysis as `preview` to determine all changes.

### Step 3: Present for Approval

Show the full preview and ask:

```
## Ready to Apply: [CATEGORY] {{Tip Title}}

The following changes will be made:
- Modify X files across Y stages
- Create Z new files

Proceed with these changes? (yes/no)
```

**Do not proceed without explicit user approval.**

### Step 4: Apply Changes

For each proposed change:

1. **Existing files**: Use Edit tool to make modifications
2. **New files**: Use Write tool to create with proposed content
3. **Track all changes made**

### Step 5: Update Backlog

After successful application:

1. Mark tip as implemented:
   - Change `- **Status**: backlog` to `- **Status**: implemented`
   - Add `- **Implemented**: {{YYYY-MM-DD}}`

2. Add changelog entry:
```markdown
### {{YYYY-MM-DD}} (Implementation)
- **Implemented**: [CATEGORY] {{Tip Title}}
- **Stages affected**: List of stages
- **Files modified**: Count
```

3. Update frontmatter counts

### Step 6: Report Success

```markdown
## Implementation Complete

**Tip**: [CATEGORY] {{Tip Title}}
**Date**: {{YYYY-MM-DD}}

### Changes Applied

| Stage | Files Modified | Changes |
|-------|----------------|---------|
| Discover | 2 | Added checklist item, validation criterion |
| Design | 1 | Added review question |
| ... | | |

### New Files Created
- `docs/mistakes.md`

### Backlog Updated
- Status: backlog → implemented
- Changelog entry added

### Next Steps
- Review the changes in affected stage files
- Test the new workflow/validation
- Run `/improve-ack analyze` for next improvement
```

---

## Action: `quick-wins`

List tips that are easy to implement: low effort, high impact, minimal stage overlap.

### Criteria

A "quick win" is a tip where:
- Effort: `low`
- Impact: `high`
- Status: `backlog`
- Affects 1-2 stages (not all stages)

### Output

```markdown
## Quick Wins

Low effort, high impact improvements ready to implement.

| # | Tip | Stages | Change Type |
|---|-----|--------|-------------|
| 1 | [CATEGORY] Title | Setup | template |
| 2 | [CATEGORY] Title | Design, Setup | validation |
| 3 | [CATEGORY] Title | Develop | process |

**Total quick wins**: X

### Recommended First

**[CATEGORY] {{Title}}**
- Effort: low | Impact: high
- Affects: {{Stage}}
- Change: {{type}}

Preview: `/improve-ack preview "{{Title}}"`
Apply: `/improve-ack apply "{{Title}}"`
```

---

## Stage File Locations

When applying changes, use these paths:

| Stage | README | Templates | Review Prompt | Validation Prompt |
|-------|--------|-----------|---------------|-------------------|
| Discover | `stages/discover/README.md` | `stages/discover/templates/` | `stages/discover/prompts/review.md` | `stages/discover/prompts/validate.md` |
| Design | `stages/design/README.md` | `stages/design/templates/` | `stages/design/prompts/review.md` | `stages/design/prompts/validate.md` |
| Setup | `stages/setup/README.md` | `stages/setup/templates/` | `stages/setup/prompts/review.md` | `stages/setup/prompts/validate.md` |
| Develop | `stages/develop/README.md` | `stages/develop/templates/` | `stages/develop/prompts/review.md` | `stages/develop/prompts/validate.md` |

**Note**: If stage directories don't exist yet, create them as part of the improvement.

---

## Cross-Cutting Changes

Some tips affect all stages or create new shared resources:

### New Shared Artifacts
Location: `docs/` or `templates/shared/`
- `mistakes.md` - Shared mistakes log
- `decisions.md` - Cross-stage decision log

### New Skills/Commands
Location: `.claude/commands/`
- Create new command file following existing patterns
- Update `.claude/commands/README.md` to include new command

### Memory Tier Changes
Location: `ack-src/mem/`
- Changes to CLAUDE.md templates
- Changes to rules/ structure

---

## Example Workflow

```bash
# Weekly improvement cycle

# 1. Check what's ready to improve
/improve-ack analyze

# 2. Preview a specific improvement
/improve-ack preview "Shared Mistakes Log"

# 3. Apply if it looks good
/improve-ack apply "Shared Mistakes Log"

# 4. Or focus on quick wins
/improve-ack quick-wins
/improve-ack apply "First Quick Win"
```

---

## Integration with Other Commands

| Command | Relationship |
|---------|--------------|
| `/extract-insights` | Feeds tips into backlog for later improvement |
| `/curate-backlog` | Prioritizes which tips to improve first |
| `/backlog-stats` | Shows improvement candidates count |
| `/improve-ack` | Actually applies improvements to ACK |

**Full cycle:**
```
/extract-insights URL → /curate-backlog → /improve-ack analyze → /improve-ack apply
```

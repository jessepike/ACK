---
type: "guide"
description: "ACK slash commands for stage workflow, backlog management, and maintenance"
version: "1.3.0"
updated: "2025-01-04T00:00:00"
---

# ACK Skills Package

Slash commands for AI-assisted development workflows.

## Skills Overview

### Stage Workflow

| Skill | Purpose |
|-------|---------|
| `/review-stage` | Content analysis of stage deliverables |
| `/validate-stage` | Structural check for stage completion |
| `/advance-stage` | Move to next stage (validates first) |

### Backlog Management

| Skill | Purpose |
|-------|---------|
| `/extract-insights` | Add insights from URLs or files to backlog |
| `/curate-backlog` | Review and maintain backlog priorities |
| `/backlog-stats` | Quick dashboard and analytics |
| `/improve-ack` | Apply insights to ACK stages |

### Project Maintenance

| Skill | Purpose |
|-------|---------|
| `/doc-check` | Check documentation accuracy and structure |
| `/repo-check` | Check repository organization |

---

## Stage Workflow

Skills for the 4-stage ACK workflow: Discover → Design → Setup → Develop.

### Two Quality Gates

Each stage has two quality gates before advancing:

1. **Review** (`/review-stage`) - Content analysis
   - Is the content clear and complete?
   - Are decisions well-reasoned?
   - Is quality sufficient to proceed?

2. **Validate** (`/validate-stage`) - Structural check
   - Does the file exist?
   - Is YAML frontmatter valid?
   - Are required sections present?

### `/review-stage <stage>`

Perform content analysis on stage deliverables.

**Stages:** `discover`, `design`, `setup`, `develop`

**What it reviews:**

| Stage | Deliverables | Focus |
|-------|--------------|-------|
| discover | brief.md | Problem clarity, user understanding, solution fit |
| design | architecture.md, data-model.md, stack.md | Technical soundness, consistency |
| setup | plan.md, tasks.md | Plan coherence, task actionability |
| develop | current work | Code quality, progress tracking |

**Output:** Review report with strengths, issues, recommendations, and go/no-go assessment.

**Usage:**
```bash
/review-stage discover    # Review the brief
/review-stage design      # Review all design docs
/review-stage setup       # Review plan and tasks
```

---

### `/validate-stage <stage>`

Perform structural validation on stage deliverables.

**Stages:** `discover`, `design`, `setup`, `develop`

**What it checks:**

| Check | Description |
|-------|-------------|
| File existence | Required deliverables present |
| YAML frontmatter | type, description, version, updated, status |
| Required sections | Stage-specific sections present |
| Checklist completion | All items checked or skipped |

**Output:** Validation report with PASS/FAIL status and blocking issues.

**Usage:**
```bash
/validate-stage discover  # Check brief structure
/validate-stage design    # Check all design docs
/validate-stage setup     # Check plan, tasks, environment
```

---

### `/advance-stage <to-stage>`

Move to the next stage after validating current stage completion.

**Target stages:** `design`, `setup`, `develop`

**What it does:**

1. Runs `/validate-stage` on current stage
2. If PASS: moves deliverables to `docs/`
3. Creates working directory for next stage
4. Updates `.ack/state.json`

**Transitions:**

| Command | From → To | Moves to docs/ |
|---------|-----------|----------------|
| `/advance-stage design` | Discover → Design | brief.md |
| `/advance-stage setup` | Design → Setup | architecture.md, data-model.md, stack.md |
| `/advance-stage develop` | Setup → Develop | plan.md, tasks.md |

**Special:** When advancing to Develop, offers to archive support artifacts.

**Usage:**
```bash
/advance-stage design   # Move from Discover to Design
/advance-stage setup    # Move from Design to Setup
/advance-stage develop  # Move from Setup to Develop
```

---

### Stage Workflow Example

```bash
# 1. Complete work on Discover stage deliverables
#    (create brief.md)

# 2. Review content quality
/review-stage discover
#    → Fix any issues identified

# 3. Validate structure
/validate-stage discover
#    → Must PASS to advance

# 4. Move to Design stage
/advance-stage design
#    → Moves brief.md to docs/, creates .ack/design/
```

---

## Backlog Management

A system for capturing, prioritizing, and maintaining actionable insights from external sources.

### Files

| File | Purpose |
|------|---------|
| `tips.backlog.md` | The backlog itself (root directory) |
| `/extract-insights` | Add insights from URLs or files |
| `/curate-backlog` | Review and maintain priorities |
| `/backlog-stats` | Quick dashboard and analytics |
| `/improve-ack` | Apply insights to ACK stages |

---

## Quick Start

```bash
# Add insights from a URL
/extract-insights https://example.com/article

# Add insights from a local file
/extract-insights ~/notes/conference-notes.md

# View dashboard
/backlog-stats

# Review stale items
/curate-backlog review

# Analyze improvements and apply to ACK
/improve-ack analyze
/improve-ack apply "Tip Title"
```

---

## Skills Reference

### `/extract-insights <source>`

Extract actionable insights from URLs or local files and append to backlog.

**What it does:**
1. Fetches/reads source content
2. Extracts up to 7 ACK-relevant insights
3. Filters duplicates against existing entries
4. Appends new insights with today's date
5. Updates frontmatter counts
6. Adds changelog entry

**Output:** Summary of added/skipped insights with new totals.

---

### `/curate-backlog [action] [args]`

Review and maintain backlog health.

**Actions:**

| Action | Usage | Description |
|--------|-------|-------------|
| `review` | `/curate-backlog review` | Full curation with recommendations |
| `promote` | `/curate-backlog promote "Title"` | Move medium → high priority |
| `demote` | `/curate-backlog demote "Title"` | Move high → medium priority |
| `implement` | `/curate-backlog implement "Title"` | Mark as implemented |
| `reject` | `/curate-backlog reject "Title" reason` | Mark as rejected |
| `stale` | `/curate-backlog stale` | List items >30 days old |
| `merge` | `/curate-backlog merge "A" + "B"` | Combine similar items |

**Review process:**
1. Analyzes staleness (>30 days in backlog)
2. Evaluates priority accuracy
3. Detects potential duplicates
4. Presents recommendations
5. Awaits approval before changes

---

### `/backlog-stats [view]`

Quick analytics and health indicators.

**Views:**

| View | Usage | Shows |
|------|-------|-------|
| (default) | `/backlog-stats` | Full dashboard |
| `by-source` | `/backlog-stats by-source` | Breakdown by source |
| `by-category` | `/backlog-stats by-category` | Breakdown by category |
| `by-age` | `/backlog-stats by-age` | Fresh/aging/stale items |
| `by-status` | `/backlog-stats by-status` | Backlog/implemented/rejected |
| `recent` | `/backlog-stats recent` | Last 7 days activity |

**Dashboard includes:**
- Total counts and health indicators
- Staleness warnings
- Category distribution
- Effort/impact matrix
- Quick wins count (low effort + high impact)

---

### `/improve-ack [action] [args]`

Apply backlog insights to ACK stages.

**Actions:**

| Action | Usage | Description |
|--------|-------|-------------|
| `analyze` | `/improve-ack analyze` | Map tips to stages, create improvement plan |
| `preview` | `/improve-ack preview "Title"` | Show proposed changes (no modifications) |
| `apply` | `/improve-ack apply "Title"` | Apply tip to stages, mark implemented |
| `quick-wins` | `/improve-ack quick-wins` | List low-effort, high-impact tips |

**Analyze output:**
- Stage impact matrix (which tips affect which stages)
- Quick wins identification
- Recommended implementation order
- Complex items needing more planning

**Apply process:**
1. Finds tip in backlog
2. Determines affected stages
3. Proposes changes to README, templates, prompts
4. Awaits approval before making changes
5. Updates backlog status to implemented

---

## Backlog Format

### YAML Frontmatter

```yaml
---
total_insights: 39
high_priority: 22
medium_priority: 17
last_updated: 2026-01-04
last_curated: 2026-01-04
sources_count: 5
---
```

### Entry Format

```markdown
### [CATEGORY] Title Here
- **Source**: URL or description
- **Added**: YYYY-MM-DD
- **Description**: What it is (2-3 sentences)
- **Application**: How to apply to ACK (specific)
- **Effort**: low | **Impact**: high
- **Status**: backlog
```

### Categories

| Category | Use For |
|----------|---------|
| `WORKFLOW` | Process improvements, task sequences |
| `PATTERN` | Reusable approaches, best practices |
| `TECHNIQUE` | Specific methods, tricks |
| `INTEGRATION` | External tools, APIs, connections |
| `ARCHITECTURE` | System design, structure |
| `TOOL` | Specific tools to build or use |

### Statuses

| Status | Meaning |
|--------|---------|
| `backlog` | Not started |
| `in-progress` | Currently being worked on |
| `implemented` | Done and shipped |
| `rejected` | Won't do (with reason) |

### Optional Fields

Added during curation:
- `**Demoted**: YYYY-MM-DD - reason`
- `**Promoted**: YYYY-MM-DD - reason`
- `**Implemented**: YYYY-MM-DD`
- `**Rejected**: YYYY-MM-DD - reason`

---

## Recommended Workflow

### Weekly

1. `/backlog-stats` - Check health indicators
2. `/curate-backlog stale` - Review old items
3. `/improve-ack analyze` - See what's ready to implement
4. `/improve-ack quick-wins` - Pick an easy improvement
5. `/improve-ack apply "Title"` - Implement it

### When Finding Good Content

1. `/extract-insights <url>` - Capture insights
2. Review the summary output
3. Optionally promote key items immediately

### Before Starting Work

1. `/backlog-stats by-category` - See what's available
2. Pick from "quick wins" (low effort + high impact)
3. `/improve-ack preview "Title"` - See what would change
4. `/improve-ack apply "Title"` - Apply the improvement

### Monthly

1. `/curate-backlog review` - Full priority review
2. Apply recommended promotions/demotions
3. Reject items that no longer apply
4. Merge any duplicates found
5. `/improve-ack analyze` - Plan next month's improvements

---

## Changelog Location

The changelog lives at the bottom of `tips.backlog.md` with newest entries first:

```markdown
## Changelog

### 2026-01-04 (Curation)
- **Reviewed**: 7 items
- **Demoted**: Item A
- **Rejected**: Item B

### 2026-01-04
- **Source**: https://example.com
- **Added**: 2 high priority, 4 medium priority
```

This provides a complete audit trail of all backlog changes.

---

## Project Maintenance

Skills for keeping documentation accurate and repository organized.

### `/doc-check [action] [category]`

Check documentation accuracy and structure.

**Actions:**

| Action | Usage | Description |
|--------|-------|-------------|
| (default) | `/doc-check` | Full scan and report |
| `scan` | `/doc-check scan` | Quick structural scan only |
| `review` | `/doc-check review` | Deep accuracy review with suggestions |
| `apply` | `/doc-check apply` | Apply approved changes |
| `tech` | `/doc-check tech` | Check tech docs only |
| `product` | `/doc-check product` | Check product docs only |
| `user` | `/doc-check user` | Check user docs only |

**Checks performed:**
- Frontmatter compliance (type, version, updated, description)
- Required sections present per doc type
- Internal link verification
- Staleness detection (based on configurable thresholds)
- Source of truth comparison (for tech/user docs)

**Workflow:**
1. Run deterministic scan (`doc-health.py`)
2. Analyze issues with agent reasoning
3. Report findings with suggestions
4. Apply fixes with user approval
5. Record results to audit log

---

### `/repo-check [action]`

Check repository structure against canonical layout.

**Actions:**

| Action | Usage | Description |
|--------|-------|-------------|
| (default) | `/repo-check` | Full scan and report |
| `scan` | `/repo-check scan` | Quick check for violations |
| `fix` | `/repo-check fix` | Interactive cleanup (move files) |
| `rules` | `/repo-check rules` | Show current placement rules |

**Checks performed:**
- Files at root match allowed list
- Docs in correct stage directories
- Source code in `src/`
- Tests in `tests/`
- No orphaned files

**Rules source:** `.claude/rules/repo-structure.md`

**Workflow:**
1. Run deterministic scan (`repo-structure.py`)
2. Analyze violations with agent reasoning
3. Report findings with move suggestions
4. Fix with user approval (uses `git mv`)
5. Record results to audit log

---

## Audit Logs

Maintenance actions are logged to:

| Log | Purpose |
|-----|---------|
| `.claude/logs/doc-maintenance.log` | Documentation check history |
| `.claude/logs/repo-maintenance.log` | Repository structure check history |

Log entries include timestamps, actions taken, files modified, and files skipped with reasons.

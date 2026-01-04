# ACK Skills Package

Slash commands for AI-assisted development workflows.

## Backlog Management

A system for capturing, prioritizing, and maintaining actionable insights from external sources.

### Files

| File | Purpose |
|------|---------|
| `tips.backlog.md` | The backlog itself (root directory) |
| `/extract-insights` | Add insights from URLs or files |
| `/curate-backlog` | Review and maintain priorities |
| `/backlog-stats` | Quick dashboard and analytics |

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
3. Address any items >30 days without progress

### When Finding Good Content

1. `/extract-insights <url>` - Capture insights
2. Review the summary output
3. Optionally promote key items immediately

### Before Starting Work

1. `/backlog-stats by-category` - See what's available
2. Pick from "quick wins" (low effort + high impact)
3. `/curate-backlog implement "Title"` when done

### Monthly

1. `/curate-backlog review` - Full priority review
2. Apply recommended promotions/demotions
3. Reject items that no longer apply
4. Merge any duplicates found

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

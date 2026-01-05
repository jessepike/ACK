---
type: "command"
description: "Documentation health checker - validates accuracy and structure"
version: "1.0.0"
updated: "2026-01-04T00:00:00"
---

# /doc-check

Validates documentation for accuracy and structural compliance. Uses a hybrid approach: fast deterministic script for structure checks, agent reasoning for content accuracy.

## Usage

```bash
/doc-check                 # Full scan and report
/doc-check scan            # Quick structural scan only (fast)
/doc-check review          # Deep accuracy review (agent reasoning)
/doc-check apply           # Apply approved changes
/doc-check tech            # Check tech docs only
/doc-check product         # Check product docs only
/doc-check user            # Check user docs only
```

## Document Categories

| Category | Location | Examples | Source of Truth |
|----------|----------|----------|-----------------|
| **Tech** | `docs/design/` | architecture.md, data-model.md, stack.md | `src/`, `schema/` |
| **Product** | `docs/discover/`, `docs/setup/`, root | brief.md, plan.md, tasks.md | None (human-driven) |
| **User** | `docs/guides/` | user-guide.md, API docs | `src/cli/`, `src/api/` |

## Workflow

### Step 1: Run Health Scan

Run the deterministic checker script:

```bash
python ack-src/scripts/doc-health.py --json > /tmp/doc-health-report.json
```

Parse the JSON output to identify:
- Frontmatter issues
- Missing sections
- Broken links
- Stale documents

### Step 2: Analyze Issues

For each document with issues:

1. **Frontmatter errors** - Missing or invalid required fields
2. **Missing sections** - Required sections not present
3. **Broken links** - Internal references that don't resolve
4. **Staleness** - Document older than threshold, source files newer

### Step 3: Content Accuracy (for `review` action)

For tech and user docs flagged as stale:

1. Read the document content
2. Read the source of truth files (from `source_of_truth` field or convention)
3. Compare: Does the doc accurately reflect current code?
4. Generate specific suggestions:
   - What's missing from the doc?
   - What's outdated?
   - What should be updated?

### Step 4: Generate Report

Display to user:

```
┌─────────────────────────────────────────────┐
│ Doc Health Report - {date}                  │
├─────────────────────────────────────────────┤
│ Scanned: {total} docs                       │
│ Current: {valid} | Stale: {stale} | Issues: {issues} │
├─────────────────────────────────────────────┤
│ ERRORS:                                      │
│ • {path} [{category}]                       │
│   ✗ Missing frontmatter: version            │
│                                              │
│ STALE:                                       │
│ • docs/design/architecture.md               │
│   → Source files in src/ modified after doc │
│   → Suggestion: Update to reflect new auth  │
│                                              │
│ WARNINGS:                                    │
│ • docs/guides/user-guide.md                 │
│   ⚠ Missing section: ## API Reference       │
└─────────────────────────────────────────────┘

Apply fixes? [Y/n/select]
```

### Step 5: Apply Fixes (with approval)

For each approved fix:

1. **Frontmatter fixes** - Add missing fields, correct format
2. **Section additions** - Add skeleton for missing sections
3. **Content updates** - Apply suggested content changes
4. **Version bump** - Increment patch version
5. **Update timestamp** - Set `updated` to current datetime

### Step 6: Record Results

Append to `.claude/logs/doc-maintenance.log`:

```markdown
## {ISO timestamp}
- **Action:** scan | review | apply
- **Scanned:** {count} documents
- **By category:**
  - Tech: {count} ({issues} issues)
  - Product: {count} ({issues} issues)
  - User: {count} ({issues} issues)
- **Updated:**
  - docs/design/architecture.md (added auth section, bumped to 1.0.1)
- **Skipped:**
  - docs/setup/plan.md (user declined)
```

## Checks Performed

### Frontmatter Compliance

| Field | Required | Format |
|-------|----------|--------|
| `type` | Yes | From controlled vocabulary |
| `description` | Yes | One-line string |
| `version` | Yes | SemVer (X.Y.Z) |
| `updated` | Yes | ISO 8601 datetime |

### Required Sections (by type)

| Type | Required Sections |
|------|-------------------|
| `architecture` | ## Overview, ## Components, ## Data Flow |
| `data_model` | ## Entities, ## Relationships |
| `plan` | ## Phases, ## Milestones |
| `tasks` | ## Tasks |
| `guide` | ## Overview |
| `project_brief` | ## Problem, ## Solution |

### Staleness Thresholds

Default thresholds (configurable via `.claude/settings.yaml`):

| Category | Days | Rationale |
|----------|------|-----------|
| Tech | 7 | Code changes frequently |
| Product | 30 | Requirements change slowly |
| User | 14 | Features ship periodically |

### Source of Truth Mapping

Convention-based (can be overridden via frontmatter):

| Doc Type | Default Source |
|----------|----------------|
| `architecture` | `src/` |
| `data_model` | `src/models/`, `schema/` |
| `stack` | `package.json`, `pyproject.toml` |
| `guide` | `src/cli/`, `src/api/` |

Override in frontmatter:
```yaml
---
type: "architecture"
source_of_truth: ["src/auth/", "src/api/"]
---
```

## Configuration

Projects can customize via `.claude/settings.yaml`:

```yaml
doc_maintenance:
  staleness_days: 14          # Default for all categories
  categories:
    tech: 7                   # Override per category
    product: 30
    user: 14
```

## Examples

### Quick Structural Scan
```
/doc-check scan
```
Runs fast checks (frontmatter, sections, links) without content analysis.

### Deep Review with Suggestions
```
/doc-check review
```
Analyzes content accuracy, compares against source code, generates suggestions.

### Check Only Tech Docs
```
/doc-check tech
```
Focuses on `docs/design/` with comparison against `src/`.

### Apply All Fixes
```
/doc-check apply
```
After a scan/review, applies approved fixes to documents.

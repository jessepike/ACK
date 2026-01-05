---
type: "command"
description: "Repository structure checker - validates file placement"
version: "1.0.0"
updated: "2026-01-04T00:00:00"
---

# /repo-check

Validates repository structure against the canonical layout defined in `.claude/rules/repo-structure.md`.

## Usage

```bash
/repo-check              # Full scan and report
/repo-check scan         # Quick structural scan (no fixes)
/repo-check fix          # Interactive cleanup (move files with approval)
/repo-check rules        # Show current placement rules
```

## Workflow

### Step 1: Run Structure Scan

Run the deterministic checker script:

```bash
python ack-src/scripts/repo-structure.py --json > /tmp/repo-structure-report.json
```

Read the JSON output and parse the results.

### Step 2: Analyze Violations

For each violation in the report:

1. **Errors (severity: error)** - Must be fixed
   - Source code at root
   - Unknown files at root
   - Files in disallowed locations

2. **Warnings (severity: warning)** - Should be fixed
   - Docs in wrong stage directory
   - Files in unknown directories

### Step 3: Generate Report

Display to user:

```
┌─────────────────────────────────────────────┐
│ Repo Structure Report - {date}              │
├─────────────────────────────────────────────┤
│ Scanned: {total} files                      │
│ Valid: {valid} | Errors: {errors} | Warnings: {warnings} │
├─────────────────────────────────────────────┤
│ ERRORS (must fix):                          │
│ • {filename} at {location}                  │
│   → {suggestion}                            │
│                                             │
│ WARNINGS (should fix):                      │
│ • {filename} at {location}                  │
│   → {suggestion}                            │
└─────────────────────────────────────────────┘
```

### Step 4: Offer Fixes (if `fix` action)

For each violation:
1. Show the proposed move
2. Ask: "Move {file} to {destination}? [Y/n]"
3. If approved:
   - Use `git mv {source} {destination}` to preserve history
   - If git mv fails, use regular mv
4. If declined, note the skip reason

### Step 5: Record Results

Append to `.claude/logs/repo-maintenance.log`:

```markdown
## {ISO timestamp}
- **Action:** scan | fix
- **Scanned:** {count} files
- **Violations found:** {count}
- **Fixed:**
  - {file} → {destination}
- **Skipped:**
  - {file} (user declined)
```

## Rules Reference

The canonical structure is defined in `.claude/rules/repo-structure.md`.

### Allowed Root Files

- README.md, intent.md, brief.md (required)
- LICENSE, .gitignore (optional)
- Config files: package.json, pyproject.toml, Makefile, Dockerfile, etc.

### Directory Structure

| Directory | Purpose |
|-----------|---------|
| `docs/discover/` | Problem validation artifacts |
| `docs/design/` | Technical specifications |
| `docs/setup/` | Implementation planning |
| `docs/develop/` | Runtime artifacts (ADRs) |
| `docs/guides/` | User-facing documentation |
| `src/` | Source code |
| `tests/` | Test files |
| `scripts/` | Automation scripts |
| `inbox/` | Incoming files for review |
| `tmp/` | Temporary files |
| `_archive/` | Archived work |

### Extending Rules

Projects can add to the allowed files via `.claude/settings.yaml`:

```yaml
repo_structure:
  allowed_root:
    - "CHANGELOG.md"
    - "CONTRIBUTING.md"
  additional_dirs:
    - "lib/"
  ignore:
    - "vendor/"
```

## Examples

### Quick Scan
```
/repo-check scan
```
Shows violations without offering fixes.

### Interactive Fix
```
/repo-check fix
```
For each violation, asks before moving:
- "Move utils.py to src/utils.py? [Y/n]"
- Uses git mv to preserve history
- Logs all actions

### Show Rules
```
/repo-check rules
```
Displays the current placement rules from `.claude/rules/repo-structure.md`.

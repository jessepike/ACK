---
type: "rule_architecture"
description: "File placement rules for repository organization"
version: "1.0.0"
updated: "2026-01-04T00:00:00"
---

# Repository Structure Rules

This file defines the canonical project structure for ACK-based projects. The `/repo-check` skill uses this as the source of truth.

## Root Level (Locked)

Only these files are allowed at project root:

| File | Required | Purpose |
|------|----------|---------|
| `README.md` | Yes | Project overview |
| `intent.md` | Yes | North Star - WHY we're building this |
| `brief.md` | Yes | WHAT we're building |
| `LICENSE` | No | License file |
| `.gitignore` | No | Git ignore rules |
| `package.json` | No | Node.js config |
| `pyproject.toml` | No | Python config |
| `requirements.txt` | No | Python dependencies |
| `Makefile` | No | Build automation |
| `Dockerfile` | No | Container config |
| `docker-compose.yml` | No | Container orchestration |

**Any other file at root requires explicit user approval.**

## Directory Structure

### Documentation (`docs/`)

Stage-aligned structure matching ACK workflow:

| Directory | Purpose | Allowed Files |
|-----------|---------|---------------|
| `docs/discover/` | Problem validation | concept.md, research.md, validation.md |
| `docs/design/` | Technical specification | architecture.md, data-model.md, stack.md |
| `docs/setup/` | Implementation planning | plan.md, tasks.md |
| `docs/develop/` | Runtime artifacts | ADRs, post-mortems |
| `docs/guides/` | User-facing documentation | *.md |

### Source Code

| Directory | Purpose | Allowed Files |
|-----------|---------|---------------|
| `src/` | Application source code | .py, .ts, .js, .go, etc. |
| `tests/` | Test files (mirrors src/) | test_*.py, *.test.ts, *_test.go |
| `scripts/` | Automation and utilities | .py, .sh, .js |

### Working Directories

| Directory | Purpose | Allowed Files |
|-----------|---------|---------------|
| `inbox/` | Incoming files for review | any |
| `tmp/` | Temporary files | any |
| `_archive/` | Archived/superseded work | any |

### Claude Code Configuration

| Directory | Purpose | Allowed Files |
|-----------|---------|---------------|
| `.claude/` | Claude Code config root | - |
| `.claude/commands/` | Slash command skills | .md |
| `.claude/rules/` | Behavioral rules | .md |
| `.claude/logs/` | Maintenance logs | .log, .md |

## Enforcement Rules

### Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| `error` | Violation that must be fixed | Block or require move |
| `warning` | Should be fixed | Warn but allow |
| `info` | Informational | Log only |

### Violation Types

| Violation | Severity | Example |
|-----------|----------|---------|
| Source code at root | error | `utils.py` in `/` |
| Unknown file at root | error | `notes.md` in `/` |
| Doc in wrong stage dir | warning | `architecture.md` in `docs/discover/` |
| Test outside tests/ | warning | `test_foo.py` in `src/` |
| Orphan in unknown dir | warning | File in unlisted directory |

### Agent Behavior

When creating a new file:

1. **Check allowed locations** - Is the target path in a known directory?
2. **If at root** - STOP and ask user for approval
3. **If in docs/** - Verify correct stage subdirectory
4. **If unknown location** - STOP and ask user for approval

When moving files:

1. Use `git mv` to preserve history
2. Update any internal references
3. Log the move to `.claude/logs/repo-maintenance.log`

## Configuration

Projects can extend these rules via `.claude/settings.yaml`:

```yaml
repo_structure:
  # Additional allowed root files
  allowed_root:
    - "CHANGELOG.md"
    - "CONTRIBUTING.md"

  # Additional directories
  additional_dirs:
    - "lib/"
    - "vendor/"

  # Directories to ignore
  ignore:
    - "node_modules/"
    - ".venv/"
    - "__pycache__/"
```

## Audit Trail

All structure violations and fixes are logged to:
- `.claude/logs/repo-maintenance.log`

Log entry format:
```
## YYYY-MM-DDTHH:MM:SS
- **Action:** scan | fix | move
- **Violations:** N found
- **Fixed:** list of files moved
- **Skipped:** list of files not moved (reason)
```

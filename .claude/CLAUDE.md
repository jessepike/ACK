# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ACK (Agent Context Kit) is a meta-framework for AI-assisted software development. It produces reusable templates, workflows, and orchestration patterns that solve the problem of stateless AI agents losing context between sessions.

**Core Philosophy:** Context is explicit. If an agent needs it, it's written down.

## 4-Stage Workflow

ACK enforces sequential stages - do not skip ahead:

| Stage | Purpose | Deliverable |
|-------|---------|-------------|
| 1. Discover | What & why | `brief.md` |
| 2. Design | Technical how | `architecture.md`, `data-model.md`, `stack.md` |
| 3. Setup | Ready to execute | `plan.md`, `tasks.md` |
| 4. Develop | Runtime execution | Working software |

Each stage has templates in `ack-src/stages/{stage}/templates/` and validation prompts in `ack-src/stages/{stage}/prompts/`.

### Stage Workflow Skills

| Skill | Purpose |
|-------|---------|
| `/init-project` | Initialize `.ack/` structure, set stage to Discover |
| `/review-stage <stage>` | Content analysis of deliverables |
| `/validate-stage <stage>` | Structural check for completion |
| `/advance-stage <to>` | Validate current stage, move to next |
| `/archive-planning` | Archive support artifacts after Setup |

**Workflow:**
```
/init-project → work → /review-stage → /validate-stage → /advance-stage → repeat
```

### Working Directory

During planning (Stages 1-3):
- Working directory: `.ack/` in project root
- Contains stage subdirectories with work-in-progress
- Add to `.gitignore`

After advancing to Develop:
- Deliverables move to `docs/`
- Support artifacts archived to `~/.ack/archives/{project}/`
- Archive lives outside project so agents don't read stale research

## Frontmatter Requirements

Every ACK artifact MUST have YAML frontmatter with these required fields:

```yaml
---
type: "project_brief"           # From controlled vocabulary
description: "One-line purpose"
version: "1.0.0"                # SemVer
updated: "2026-01-03T14:30:00"  # ISO 8601
---
```

**Type vocabulary:** intent, project_brief, architecture, data_model, schema, plan, tasks, memory_global, memory_project, rule_constitution, rule_preferences, rule_workflows, rule_architecture, rule_stack, rule_domain, adr, research, review, guide

See `ack-src/schemas/FRONTMATTER_SCHEMA.md` for full specification.

## Project Structure

```
ack-src/                    # THE PRODUCT (reusable templates)
├── gov/                    # Artifact Governance System
├── mem/                    # Memory Kit (Tier-1 CLAUDE.md + rules/)
├── registry/               # Agent/skill/tool registry
├── schemas/                # FRONTMATTER_SCHEMA.md
├── scripts/                # Setup and validation scripts
├── stages/                 # Stage guides and templates
│   ├── discover/
│   ├── design/
│   ├── setup/
│   └── develop/
└── templates/              # Artifact templates

.claude/commands/           # Slash commands for backlog management
tips.backlog.md            # Insights backlog (managed by slash commands)
```

## File Placement Rules (Enforced)

**IMPORTANT:** Do not create files outside the defined structure without explicit user approval.

### Allowed Locations

| Location | What Goes Here |
|----------|----------------|
| Root | ONLY: README.md, intent.md, brief.md, LICENSE, .gitignore, config files |
| `docs/discover/` | Problem validation: concept.md, research.md, validation.md |
| `docs/design/` | Technical specs: architecture.md, data-model.md, stack.md |
| `docs/setup/` | Planning: plan.md, tasks.md |
| `docs/develop/` | Runtime artifacts: ADRs |
| `docs/guides/` | User-facing: guides, tutorials, API docs |
| `src/` | Source code |
| `tests/` | Test files |
| `scripts/` | Automation scripts |
| `inbox/` | Incoming files for review |
| `tmp/` | Temporary files |
| `_archive/` | Archived work |

### Before Creating Any File

1. Check if location matches the table above
2. If creating at root or unknown location → **ASK USER FIRST**
3. If user approves non-standard location → document why in the file

### Enforcement

- Run `/repo-check` to scan for violations
- Run `/doc-check` to verify documentation health
- See `.claude/rules/repo-structure.md` for full rules

## Available Slash Commands

### Stage Workflow

| Command | Purpose |
|---------|---------|
| `/init-project [name]` | Initialize ACK project with `.ack/` structure |
| `/review-stage <stage>` | Content analysis of stage deliverables |
| `/validate-stage <stage>` | Structural check for stage completion |
| `/advance-stage <to>` | Move to next stage (validates first) |
| `/archive-planning` | Archive support artifacts to `~/.ack/archives/` |

### Backlog Management

| Command | Purpose |
|---------|---------|
| `/extract-insights <url>` | Extract actionable insights from URLs or files |
| `/curate-backlog` | Review and maintain backlog priorities |
| `/backlog-stats` | Quick dashboard and analytics |
| `/improve-ack` | Apply insights to ACK stages |

### Project Maintenance

| Command | Purpose |
|---------|---------|
| `/doc-check` | Check documentation accuracy and structure |
| `/repo-check` | Check repository organization |

## Validation Scripts

Located in `ack-src/scripts/`:

- `fix-frontmatter.py` - Fix YAML frontmatter across documents
- `doc-health.py` - Check documentation health (used by `/doc-check`)
- `repo-structure.py` - Check repository structure (used by `/repo-check`)
- `validate-claude-md.sh` - Validate CLAUDE.md structure
- `check-cycles.py` - Detect circular dependencies in artifacts
- `check-structure.sh` - Validate file placement

## Key Artifacts

| File | Purpose |
|------|---------|
| `ack-intent.md` | North Star - why ACK exists |
| `ack-project-brief.md` | What we're building, how |
| `ack-src/ARTIFACT_INVENTORY.md` | Complete catalog of templates and prompts |
| `ack-src/mem/TIER1_KIT_SPEC.md` | Memory system specification |
| `ack-src/registry/REGISTRY_INVENTORY.md` | Complete capabilities inventory |

## Working Conventions

- **Stages are sequential** - Complete Discovery before Design, etc.
- **Two quality gates per stage** - Review (content) then Validate (structure)
- **Deliverables persist in /docs** - Support artifacts get archived
- **Version control everything** - All artifacts are markdown + YAML frontmatter
- **Manual before automated** - Prove patterns work before scripting them

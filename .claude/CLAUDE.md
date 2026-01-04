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

## Available Slash Commands

| Command | Purpose |
|---------|---------|
| `/extract-insights <url>` | Extract actionable insights from URLs or files |
| `/curate-backlog` | Review and maintain backlog priorities |
| `/backlog-stats` | Quick dashboard and analytics |
| `/improve-ack` | Apply insights to ACK stages |

## Validation Scripts

Located in `ack-src/scripts/`:

- `fix-frontmatter.py` - Fix YAML frontmatter across documents
- `validate-claude-md.sh` - Validate CLAUDE.md structure
- `check-cycles.py` - Detect circular dependencies in artifacts
- `check-structure.sh` - Validate file placement

## Key Artifacts

| File | Purpose |
|------|---------|
| `ack-intent.md` | North Star - why ACK exists |
| `ack-project-brief.md` | What we're building, how |
| `ack-src/mem/TIER1_KIT_SPEC.md` | Memory system specification |
| `ack-src/registry/REGISTRY_INVENTORY.md` | Complete capabilities inventory |

## Working Conventions

- **Stages are sequential** - Complete Discovery before Design, etc.
- **Two quality gates per stage** - Review (content) then Validate (structure)
- **Deliverables persist in /docs** - Support artifacts get archived
- **Version control everything** - All artifacts are markdown + YAML frontmatter
- **Manual before automated** - Prove patterns work before scripting them

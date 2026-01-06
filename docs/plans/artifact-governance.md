---
type: plan
description: "Artifact creation and governance system with config-driven validation"
version: 0.1.0
updated: "2026-01-04T10:15:00"
status: planned
---

# Plan: Artifact Creation & Governance System

## Overview

Build a comprehensive, portable artifact creation and validation system with:
1. Config-driven scope (`.frontmatter.yaml`)
2. `/create-artifact` skill with full workflow
3. Pre-commit validation hook
4. Template migrations to match schema

---

## Phase 1: Foundation

### 1.1 Create `.frontmatter.yaml`

**File:** `/.frontmatter.yaml`

```yaml
version: "1.0.0"

scope:
  include:
    - "**/*.md"
  exclude:
    - "_archive/**"
    - "**/node_modules/**"
    - "**/.venv/**"
    - ".git/**"
    - "misc/**"
    - "inbox/**"
    - "**/README.md"
    - "tips.backlog.md"

validation:
  required_fields: [type, description, version, updated]
  type_vocabulary:
    - intent
    - project_brief
    - architecture
    - data_model
    - schema
    - plan
    - tasks
    - memory_global
    - memory_project
    - rule_constitution
    - rule_preferences
    - rule_workflows
    - rule_architecture
    - rule_stack
    - rule_domain
    - adr
    - research
    - review
    - guide
    - artifact_registry

templates:
  path: "ack-src/templates/artifacts"

registry:
  path: "ack-src/registry/ARTIFACT_REGISTRY.md"
  auto_update: true
```

### 1.2 Update `fix-frontmatter.py`

Modify to read config from `.frontmatter.yaml` instead of hardcoded patterns.

---

## Phase 2: Template Migrations

### 2.1 Create migration script

**File:** `ack-src/scripts/migrate-templates.py`

Map artifact names to schema types:
- `concept` → `project_brief`
- `research` → `research`
- `scope` → `project_brief`
- `validation` → `review`
- `architecture` → `architecture`
- `data-model` → `data_model`
- `stack` → `architecture`
- `dependencies` → `architecture`
- `context-schema` → `schema`
- `repo-init` → `guide`
- `scaffolding` → `guide`

Remove non-schema fields: `stage`, `artifact`, `status`

### 2.2 Files to migrate

All 11 templates in `ack-src/templates/artifacts/`:
- ack-design-architecture.md
- ack-design-context-schema.md
- ack-design-data-model.md
- ack-design-dependencies.md
- ack-design-stack.md
- ack-discovery-concept.md
- ack-discovery-research.md
- ack-discovery-scope.md
- ack-discovery-validation.md
- ack-setup-repo-init.md
- ack-setup-scaffolding.md

---

## Phase 3: Pre-commit Hook

### 3.1 Create hook script

**File:** `ack-src/scripts/validate-frontmatter-hook.py`

Features:
- Read scope from `.frontmatter.yaml`
- Get staged `.md` files from git
- Validate against required fields
- Check type vocabulary
- Validate semver and ISO 8601 formats
- Block commit on failure

### 3.2 Configure pre-commit

**Option A:** `.pre-commit-config.yaml`
```yaml
repos:
  - repo: local
    hooks:
      - id: validate-frontmatter
        name: Validate Frontmatter
        entry: python ack-src/scripts/validate-frontmatter-hook.py
        language: python
        types: [markdown]
```

**Option B:** `.git/hooks/pre-commit`
```bash
#!/bin/bash
python ack-src/scripts/validate-frontmatter-hook.py
```

---

## Phase 4: `/create-artifact` Skill

### 4.1 Create skill file

**File:** `.claude/commands/create-artifact.md`

### 4.2 Workflow

```
1. Parse arguments or prompt for type
2. Load .frontmatter.yaml config
3. Present template selection by stage
4. Gather: name, description, version, dependencies
5. Generate from template with placeholders filled
6. Validate frontmatter before write
7. Write to stage-appropriate directory
8. Update artifact registry (if auto_update)
9. Set up depends_on relationships
10. Run validation checklist for sections
11. Output summary with next steps
```

### 4.3 Template selection menu

**Discovery Stage:**
- concept (→ project_brief)
- research
- scope (→ project_brief)
- validation (→ review)

**Design Stage:**
- architecture
- data_model
- stack (→ architecture)
- dependencies (→ architecture)
- context_schema (→ schema)

**Setup Stage:**
- repo_init (→ guide)
- scaffolding (→ guide)

---

## Phase 5: Artifact Registry

### 5.1 Create registry

**File:** `ack-src/registry/ARTIFACT_REGISTRY.md`

Sections:
- Summary table (stage counts)
- Discovery artifacts table
- Design artifacts table
- Setup artifacts table
- Implementation artifacts table
- Dependency graph (Mermaid)
- Changelog

---

## Implementation Order

| Step | Task | Files |
|------|------|-------|
| 1 | Create `.frontmatter.yaml` | `.frontmatter.yaml` |
| 2 | Update fix-frontmatter.py to use config | `ack-src/scripts/fix-frontmatter.py` |
| 3 | Create migration script | `ack-src/scripts/migrate-templates.py` |
| 4 | Run migrations | `ack-src/templates/artifacts/*.md` |
| 5 | Create pre-commit hook | `ack-src/scripts/validate-frontmatter-hook.py` |
| 6 | Configure pre-commit | `.pre-commit-config.yaml` or `.git/hooks/` |
| 7 | Create artifact registry | `ack-src/registry/ARTIFACT_REGISTRY.md` |
| 8 | Create /create-artifact skill | `.claude/commands/create-artifact.md` |
| 9 | Test end-to-end | Create sample artifact |

---

## Critical Files Reference

- `ack-src/schemas/FRONTMATTER_SCHEMA.md` - Authoritative schema
- `ack-src/scripts/fix-frontmatter.py` - Existing validation patterns
- `.claude/commands/extract-insights.md` - Skill format example
- `ack-src/registry/REGISTRY_INVENTORY.md` - Registry format reference

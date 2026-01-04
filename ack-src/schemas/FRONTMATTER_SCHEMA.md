---
type: "schema"
description: "Definitive YAML frontmatter schema for all ACK artifacts"
version: "1.0.0"
updated: "2026-01-03T00:00:00"
---

# ACK Frontmatter Schema

**Status:** Final
**Applies to:** All ACK artifacts (briefs, architecture, memory, rules, plans, etc.)

---

## Required Fields

Every ACK artifact MUST include these four fields:

```yaml
---
type: "project_brief"
description: "One-line human-readable purpose of this document"
version: "1.0.0"
updated: "2026-01-03T14:30:00"
---
```

| Field | Format | Purpose |
|-------|--------|---------|
| `type` | Controlled vocabulary | Document category (see Type Vocabulary below) |
| `description` | String (one line) | Human-readable purpose; disambiguates files with same name |
| `version` | SemVer `X.Y.Z` | Track meaning changes to the document |
| `updated` | ISO 8601 datetime | Last modification timestamp |

---

## Optional Fields

Add these when applicable to the document type:

```yaml
---
type: "rule_architecture"
description: "Structural decisions and boundaries for this project"
version: "1.0.0"
updated: "2026-01-03T14:30:00"

# Optional
scope: "project"
paths: "src/api/**/*.ts"
depends_on: ["ack-intent.md", "architecture.md"]
---
```

| Field | When to Use |
|-------|-------------|
| `scope` | CLAUDE.md files to disambiguate level: `global`, `project`, `local` |
| `paths` | Conditional loading - file/glob patterns this document applies to |
| `depends_on` | List of artifacts this document references or derives from |

---

## Type Vocabulary

### Core Artifacts
- `intent` — North Star outcome document
- `project_brief` — Concept, scope, constraints, high-level approach
- `architecture` — System architecture and boundaries
- `data_model` — Conceptual/logical data domains
- `schema` — Physical schema definitions
- `plan` — Implementation plan with phases and milestones
- `tasks` — Task breakdown for execution

### Memory Artifacts
- `memory_global` — Global CLAUDE.md entry point
- `memory_project` — Project CLAUDE.md entry point

### Rule Artifacts
- `rule_constitution` — Non-negotiable invariants (security, safety, integrity)
- `rule_preferences` — Code style, formatting preferences
- `rule_workflows` — Process patterns and protocols
- `rule_architecture` — Structural decisions
- `rule_stack` — Technology-specific rules
- `rule_domain` — Business rules, terminology

### Supporting Artifacts
- `adr` — Architecture Decision Record
- `research` — Research notes and findings
- `review` — External review feedback
- `guide` — How-to documentation

### Governance Artifacts
- `schema` — Schema definition documents (like this one)
- `artifact_registry` — Index of all artifacts

---

## Versioning Rules

Follow Semantic Versioning:

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking changes that invalidate downstream work | Major (X) | 1.0.0 → 2.0.0 |
| Non-breaking additions or modifications | Minor (Y) | 1.0.0 → 1.1.0 |
| Corrections, clarifications, typo fixes | Patch (Z) | 1.0.0 → 1.0.1 |

---

## Examples

### Intent Document
```yaml
---
type: "intent"
description: "North Star outcome and success criteria for ACK"
version: "1.0.0"
updated: "2026-01-03T00:00:00"
---
```

### Project Brief
```yaml
---
type: "project_brief"
description: "ACK concept, scope, and high-level technical approach"
version: "0.1.0"
updated: "2026-01-03T00:00:00"

depends_on: ["ack-intent.md"]
---
```

### Architecture Document
```yaml
---
type: "architecture"
description: "System architecture for the Acme API"
version: "1.0.0"
updated: "2026-01-03T00:00:00"

depends_on: ["project-brief.md"]
---
```

### Project CLAUDE.md
```yaml
---
type: "memory_project"
description: "Project context and current working state"
version: "1.0.0"
updated: "2026-01-03T14:30:00"

scope: "project"
---
```

### Rule File
```yaml
---
type: "rule_architecture"
description: "Structural patterns and boundaries for this project"
version: "1.0.0"
updated: "2026-01-03T00:00:00"

depends_on: ["architecture.md"]
---
```

---

## Validation Rules

1. All four required fields must be present
2. `type` must be from the controlled vocabulary
3. `version` must be valid SemVer (X.Y.Z)
4. `updated` must be valid ISO 8601 datetime
5. `depends_on` entries must reference existing files

---

## Supersedes

This schema supersedes:
- `gov/ags_template_v1.0.0/schemas/TIER1_FRONTMATTER_SCHEMA.md`
- `inbox/ACK_Artifact_Schema_Specification.md` (frontmatter section)

Those documents should be updated to reference this schema or archived.

---
doc_id: "spec-002"
slug: "adr-yaml-schema"
title: "ADR Canonical Record Schema (YAML)"
type: "schema"
tier: "tier1"
status: "active"
authority: "binding"
version: "0.1.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: []
---

# ADR canonical record schema (YAML)

This is the *exact* minimum schema for Tier 1 ADR records. It is designed to be:
- human-authored
- machine-validated
- merge-gatable

Store each ADR as `adrs/ADR-###.yaml`.

## File naming

- `adrs/ADR-001.yaml`, `adrs/ADR-002.yaml`, …
- `adr_id` must match the filename prefix.

## ADR YAML (Tier 1) — exact schema

```yaml
adr_id: "ADR-001"              # required; unique; matches filename
slug: "switch-to-openai"       # required; stable, human-readable
title: "Switch inference provider to OpenAI"   # required

status: "accepted"             # required; one of: proposed|accepted|rejected|deprecated
date: "2026-01-01"             # required; ISO-8601 YYYY-MM-DD


impacts:                       # required; list of artifact_ids impacted by this decision
  - "arch-001"                 # e.g., the Tier 1 architecture doc id

context: >                     # required; why this decision exists (problem/trigger)
  Brief description of the situation and constraints.

decision: >                    # required; the decision statement (what we will do)
  Clear, testable statement of the decision.

consequences:                  # required; explicit tradeoffs
  positive:
    - "Lower latency"
  negative:
    - "Vendor dependency"
  followups:
    - "Update ARCHITECTURE.md stack section"

alternatives:                  # optional; list of considered alternatives
  - name: "Provider X"
    reason_rejected: "Did not meet reliability targets"

supersedes: []                 # optional; ADR IDs this replaces (e.g., ["ADR-009"])
references:                    # optional; pointers to evidence, PRs, issues, docs
  - kind: "pr"
    ref: "PR-123"
  - kind: "doc"
    ref: "arch-001"
```

## Validation rules (enforceable)

A validator can enforce these checks:
- `adr_id`, `slug`, `title`, `status`, `date`, `type`, `authority`, `impacts`, `context`, `decision`, `consequences` are present
- `status` ∈ {proposed, accepted, rejected, deprecated}
- `type` ∈ {architecture, data, security, scope, process}
- `authority` ∈ {binding, guidance}
- `impacts` references valid `artifact_id`s in the registry
- if `status: accepted`, then at least one Tier 1 artifact in `impacts` must be updated in the same PR **or** the PR must include a linked reconciliation task (your choice of strictness)

## Notes

- Keep ADRs short. If the context becomes long, link to a supporting `research_note`.
- Treat ADR YAML as canonical; generate any Markdown view from this file.

---

## Review & Change History

**Current Version:** 0.1.0  
**Review Status:** draft

### Changes Since Last Review
- Initial packaging cleanup; standardized frontmatter and review section.

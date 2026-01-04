---
doc_id: "spec-003"
slug: "artifact-type-vocabulary"
title: "Controlled Vocabulary for Artifact Type"
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

# Controlled vocabulary for `type`

`type` identifies *what kind of artifact this is* so tools can apply the right rules (drift detection, required fields, gates, indexing, retention).

## Tier 1 (canonical) `type` values

These should be a small, stable set.

- `project_brief` — Outcome, scope, constraints, success metrics (the “why/what” contract)
- `architecture` — System architecture and boundaries (the “how” at system level)
- `data_model` — Conceptual/logical data domains, entities, relationships
- `security_baseline` — Non-negotiable security requirements and defaults
- `tasks_plan` — Execution contract: work items + acceptance criteria (can be `TASKS.md` or `PLAN.md`)
- `adr` — Individual Architecture Decision Record (canonical record)
- `adr_index` — Decision index / decision log (links + status summary)
- `artifact_registry` — Registry/index of all artifacts (DB-lite)
- `drift_rules` — Rules that map repo diffs to “impacted artifacts” + severity

## Tier 2 (supporting) `type` values

Use these when you want structure but not Tier 1 ceremony.

- `api_spec` — OpenAPI/GraphQL/etc.
- `schema` — Physical schema definition(s) (often generated)
- `runbook` — Operational instructions (deploy, rollback, incident steps)
- `threat_model` — Threat analysis artifact(s)
- `validation_plan` — Assumption tests / validation approach
- `research_note` — Curated research write-up (not raw logs)
- `test_strategy` — Testing approach and coverage intent
- `observability_plan` — Logging/metrics/tracing design
- `release_notes` — Human-facing change summaries for releases

## Tier 3 (ephemeral) `type` values

Mostly generated, short-lived, or not governed.

- `change_summary` — Machine summary of diffs for a PR/run
- `drift_report` — Impact analysis output (JSON canonical + optional MD view)
- `agent_run` — Agent execution transcript/summary
- `validation_result` — Output of a validation run (pass/fail + evidence pointers)
- `build_artifact` — CI artifacts, logs, binaries (usually stored outside git)

## Rules for extending the vocabulary

- Prefer **adding a subtype field** (e.g., `type: runbook`, `subtype: deploy`) before adding a brand-new `type`.
- Only promote a `type` into Tier 1 after it proves it is:
  - required across most projects, and
  - gate-relevant (affects enforcement and drift detection).

---

## Review & Change History

**Current Version:** 0.1.0  
**Review Status:** draft

### Changes Since Last Review
- Initial packaging cleanup; standardized frontmatter and review section.

---
doc_id: gov-011
slug: document-versioning-policy
title: Document Versioning Policy
type: runbook
tier: tier1
status: active
authority: binding
version: 1.0.0
review_status: accepted
created: '2026-01-01'
updated: '2026-01-01'
owner: human
depends_on: []
---
# GOVERNANCE_DOCUMENT_VERSIONING.md

---

## Purpose

This policy defines **how Tier 1 documents are versioned and reviewed** so they remain durable systems of record.

It exists because **humans and AI agents are inconsistent**. Document authority must not depend on memory or discipline. It must be:
- explicit
- reviewable
- auditable
- enforceable

This policy applies regardless of whether edits are made inside or outside Git workflows.

---

## Scope

### In scope
- **Tier 1 artifacts only** (canonical systems of record)

### Out of scope (by default)
- Tier 2 supporting artifacts
- Tier 3 ephemeral artifacts (logs, generated reports)

Tier 2/3 may adopt this policy later via an explicit governance decision.

---

## Definitions

- **Meaningful change**: a change that alters scope, constraints, architecture intent, data intent, security requirements, execution contract, or authority boundaries.
- **Review cycle**: the unit of governance maturity. A document is “reviewed” when it is shared as current truth and accepted for use.
- **Reconciliation**: the act of bringing off-workflow changes back under governance control (version + review notes + optional ADR).

---

## Tier 1 Required Metadata (Frontmatter)

Every Tier 1 Markdown artifact must include:

```yaml
version: "0.0.0"          # required; semver-style (recommended)
review_status: "draft"    # required; draft|reviewed|accepted
```

Guidance:
- `version` is the document’s **meaning version**, not the repo version.
- `review_status` communicates authority readiness.

---

## Tier 1 Required Bottom Section (Progressive Disclosure)

Tier 1 documents must end with the following section (at the bottom of the body):

```markdown
---

## Review & Change History

**Current Version:** 0.0.0  
**Review Status:** draft

### Changes Since Last Review
- (none)
```

Rules:
- This section MUST exist.
- It SHOULD be short.
- It MAY be empty (e.g., “(none)”).

Rationale:
- Keeps governance metadata out of the primary narrative.
- Enables humans and agents to locate review deltas consistently.
- Optimizes context windows (progressive disclosure).

---

## Version Increment Rules (Good Enough)

Increment `version` when any of the following is true:
- The document is shared as **current truth** for review.
- The document’s meaning changes (scope/constraints/decisions/invariants).
- The document is referenced as an input to implementation planning or validation.
- The document authority changes (e.g., `draft → reviewed`, `reviewed → accepted`).

Do NOT increment `version` for:
- typos and formatting
- purely editorial wording with unchanged meaning
- link fixes

If unsure: increment.

---

## Review Status Transitions

Allowed transitions:
- `draft → reviewed` (review occurred; document considered usable input)
- `reviewed → accepted` (treated as stable system-of-record for the current phase)
- `accepted → reviewed` (re-opened due to significant change)
- any state → `draft` (only when explicitly re-baselining; should be rare)

Review status is a governance signal, not a badge.

---

## Off-Workflow Edits (Edge Case Handling)

Edits will occur outside standard Git/PR workflows (workshops, chat sessions, emergency fixes). This is expected.

Rule:
- Any Tier 1 document updated off-workflow MUST be reconciled upon re-entry by:
  1) incrementing `version` if meaning changed
  2) updating “Changes Since Last Review”
  3) creating an ADR if the change modifies architecture/data/security/authority decisions

No blame. The objective is normalization and traceability.

---

## Enforcement via Git (Reference)

Git enforcement rules are defined in `GOVERNANCE_GIT.md`.

At merge boundary, required checks SHOULD enforce:
- If a Tier 1 document changes meaning, `version` or `review_status` must change.
- The “Review & Change History” section must exist.
- If drift indicates Tier 1 impact, reconciliation (ADR and/or doc update) must be present.

This document defines the policy. Git provides enforcement.

---

## Backlog

Deferred (not day 1):
- reviewer identity fields
- timestamps (`last_reviewed`)
- automated “meaning change” detection heuristics
- release/tag alignment between Git tags and document versions


---

## Operational Definitions

- **Reviewed** = the change is approved in a PR/MR by **≥ 1 human with write access**.
- **Accepted** = the artifact is explicitly promoted to be relied on as a stable input for downstream work (e.g., implementation planning), typically after a reviewed PR and (if applicable) ADRs are filed.


- **Reviewed** = PR/MR approved by **≥ 1 human with write access**.

## System Version vs Document Version

AGS uses SemVer in two places:

1. **System version (AGS itself)**  
   - Declared in `AGS_VERSION.md`  
   - Tagged as `ags-vX.Y.Z`

2. **Document version (Tier 1 artifacts)**  
   - Stored in frontmatter `version:`
   - Used to indicate “safe to build from” for planning/execution

### SemVer guidance

- **MAJOR**: breaking schema changes, tier model changes, validator behavior changes that would break existing docs
- **MINOR**: new validator capabilities, new drift-rule primitives, new artifact types
- **PATCH**: bug fixes, doc corrections, wiring fixes

### Operational definition

- `review_status: accepted` means “usable input to planning/execution.”
- `review_status: reviewed` means “PR approved by ≥1 human with write access.”

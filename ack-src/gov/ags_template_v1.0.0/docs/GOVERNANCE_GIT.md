---
doc_id: gov-010
slug: governance-git
title: Governance via Git
type: runbook
tier: tier1
status: active
authority: binding
version: 1.0.0
review_status: accepted
created: '2026-01-01'
updated: '2026-01-01'
owner: human
depends_on:
- gov-011
---
# GOVERNANCE_GIT.md

---

## Purpose

## Enforcement Actor (Round 2)

The minimal enforcement actor is:

- `scripts/validate_ags.py`

It MUST run at the enforcement boundary (PR/MR merge) in team mode.
In solo-dev mode, it SHOULD run locally before push (pre-commit or manual), and MAY run in CI later.

**Non-negotiable:** `ARTIFACT_REGISTRY.json` is derived output from frontmatter. Do not hand-edit it.



This document defines **how Git functions as the governance and enforcement system** for AI‑augmented development.

It exists because **humans and AI agents are both inconsistent**. Memory, discipline, and good intent are unreliable. Governance must therefore be:
- explicit
- objective
- continuously enforced

Git is the neutral arbiter that turns intent into accepted reality.

---

## First Principles

- Intent must be externalized into artifacts.
- Artifacts must be governed, not advisory.
- Drift between intent and execution is inevitable.
- Silent drift is unacceptable.
- Governance must apply equally to humans and agents.
- Friction is proportional to impact.

---

## Authority Model

- The `main` branch represents accepted system reality.
- Direct commits to `main` are prohibited.
- All changes enter through Pull Requests (PRs).
- A merged PR is the **only** mechanism by which intent becomes reality.

---

## Governance Boundaries

### Pre‑Commit (Advisory Boundary)

- Runs locally.
- Fast, low‑latency checks.
- Produces warnings and early signals.
- Bypassable by design.

Purpose: habit formation and early drift visibility.

---

### Merge Boundary (Authoritative Boundary)

- Executed via CI on every PR.
- Full diff visibility.
- Non‑bypassable.
- Required checks must pass before merge.

Purpose: enforcement, reconciliation, auditability.

---

## Drift Detection Contract

- Drift is detected by analyzing repository diffs.
- Drift rules map changes to impacted artifacts.
- Detection is automated and objective.
- Output is a generated drift report (machine‑canonical).

Drift rules are defined in `drift_rules.yaml`.

---

## Reconciliation Rules

When drift impacts **Tier 1 artifacts**:
- An ADR must be created **and/or**
- The impacted artifact must be updated in the same PR.

Merges are blocked until reconciliation occurs.
Silent divergence is not permitted.

---

## Decision Recording

- Architecture Decision Records (ADRs) are canonical decision artifacts.
- ADRs explain *why* a change exists.
- ADRs reference impacted artifacts.
- ADRs are versioned and merge‑gated.

Git history + ADRs constitute the audit trail.

---

## Artifact Authority & Lifecycle

- Tier 1 artifacts are systems of record.
- Tier 2 artifacts are supporting and promotable.
- Tier 3 artifacts are ephemeral and non‑authoritative.
- The Artifact Registry defines what exists and its status.

---

## Enforcement Philosophy

- Trust is allowed.
- Verification is mandatory.
- Enforcement applies equally to humans and agents.
- Governance evolves via backlog and iteration, not speculation.

---

## Review & Change History

**Current Version:** 0.2.0  
**Review Status:** draft

### Changes Since Last Review
- Initial packaging cleanup; standardized frontmatter and review section.



## Emergency Override

Governance enforcement is **merge-gated**, but incidents happen.

- Force-push / bypass is permitted only during an incident (break-glass).
- Within **48 hours**, the bypasser MUST:
  - file an ADR in `docs/adrs/` explaining what was bypassed and why, and
  - reconcile Tier 1 artifacts affected by the bypass.

This keeps the system honest: bypass is allowed, but never silent.



## Authority (Minimum Viable)

- Any **human with write access** may approve Tier 1 changes.
- Agent-submitted changes require **human approval** before merge.
- In solo-dev mode, the human owner is the final authority.


## Recommended Validation Command (Pre-commit / CI)

For teams, the recommended enforcement command is:

```bash
python3 scripts/validate_ags.py --profile strict --write-registry --check-registry --auto-check-drift --diff-range --cached
```

For solo-dev rapid iteration:

```bash
python3 scripts/validate_ags.py --profile minimal --write-registry --check-registry
```

## Releases and System Version

AGS has a **system version** (not just per-document versions):

- System version declaration: `AGS_VERSION.md`
- Release boundary: git tag `ags-vX.Y.Z`

### Release procedure (minimum)

```bash
python3 scripts/validate_ags.py --profile strict --check-registry --check-drift
python3 scripts/validate_ags.py --profile strict --write-registry
git commit -am "release(ags): vX.Y.Z"
git tag -a ags-vX.Y.Z -m "AGS vX.Y.Z"
git push --tags
```

A release is “good enough” when the validator passes strict and the derived registry is current.

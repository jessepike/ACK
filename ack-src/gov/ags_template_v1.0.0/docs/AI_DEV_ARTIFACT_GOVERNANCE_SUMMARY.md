---
type: runbook
description: "AI-DEV Artifact Governance – Summary & First Principles"
version: 1.0.0
updated: 2026-01-01
status: active
depends_on: []
doc_id: gov-001
slug: artifact-governance-summary
title: "AI-DEV Artifact Governance \u2013 Summary & First Principles"
tier: tier1
authority: binding
review_status: accepted
created: 2026-01-01
owner: human
---
# AI-DEV Artifact Governance – Summary & First Principles

## Purpose
This document summarizes the decisions made around **artifact governance for AI‑augmented development**.  
Its goal is to align humans and AI agents around shared sources of truth, reduce drift, and enforce intent through structure, not discipline.

This is written for **review and iteration** by the team.

---

## Core Insight (First Principle)

> **Humans are at least as inconsistent as AI agents.**

Therefore, governance must not rely on:
- memory
- discipline
- best intentions

It must rely on:
- explicit artifacts
- clear rules
- objective detection
- enforced gates

The system must apply equally to humans *and* agents.

---

## Problem We Are Solving

AI-assisted development fails at scale because:
- agents drift from intent
- humans drift even more
- documentation is passive and unenforced
- decisions are made without reconciliation to system-of-record artifacts

**We are externalizing intent into durable, governed artifacts.**

---

## Artifact Philosophy

Artifacts are **first-class system actors**, not documentation byproducts.

Each artifact must have:
- explicit purpose
- known authority level
- defined lifecycle
- traceability to outcomes

Governance effort is proportional to impact.

---

## Artifact Tiers

### Tier 1 — Canonical (System of Record)
- Few (≈10–15)
- Versioned
- Merge-gated
- Drift‑relevant
- Binding authority

Examples:
- Project Brief
- Architecture
- Data Model (conceptual/logical)
- Security Baseline
- Tasks / Plan
- ADRs
- Artifact Registry
- Drift Rules

### Tier 2 — Supporting
- Important but lower ceremony
- Versioned
- May be promoted/demoted

Examples:
- API specs
- Threat models
- Runbooks
- Validation plans

### Tier 3 — Ephemeral
- Generated or exploratory
- Not owned
- Not governed long-term

Examples:
- Change summaries
- Drift reports
- Agent run outputs

---

## Formats & Rationale

| Format | Role |
|------|-----|
| Markdown | Human-first narrative, progressive disclosure |
| YAML | Human-authored structured records & metadata |
| JSON | Machine-generated, canonical outputs |

Rule:
- **Human reads → Markdown**
- **Human writes structured data → YAML**
- **Machine writes/consumes → JSON**

---

## ADR Design (Key Decision)

- ADRs are **canonical YAML records**
- Enforceable, machine-validated
- Human-readable without ceremony
- Optional Markdown views can be generated

ADRs exist to:
- reconcile intent with reality
- explain *why* Tier 1 artifacts changed
- prevent silent drift

---

## Drift Detection & Enforcement

- Drift is detected objectively via repo diffs
- Changes are summarized automatically
- Drift rules map changes → impacted artifacts
- Enforcement happens at the **merge boundary (PR)**

Pre-commit:
- fast, local warnings
- bypassable

Merge checks:
- non-bypassable
- block merges until reconciliation occurs

---

## Artifact Registry (DB‑lite)

A single registry indexes all artifacts with:
- identity
- type
- tier
- authority
- status
- format
- path

This enables:
- traceability
- impact analysis
- automation
- future UI/DB expansion

---

## Guiding Constraints

- Intent must be durable
- Reality must be reconciled
- Drift must be detectable
- Enforcement must be objective
- Friction must be proportional

---

## Status

This system is:
- intentionally minimal
- backlog-driven for expansion
- designed to build governance muscle gradually

Feedback and iteration are expected.

---

## Operationalization

### Repeatable across projects

- Use this repository as a **template harness**.
- Recommended pattern: place AGS under `.ags/` and treat project docs as governed work products.
- New projects start with AGS pre-installed; existing projects adopt in phases (minimal → canonical subset → strict+CI).

### System version control

- AGS has a **system version** declared in `AGS_VERSION.md` and tagged in git as `ags-vX.Y.Z`.
- Tier 1 documents also carry `version:` and `review_status:` to indicate “safe input” for planning/execution.
- The validator is the enforcement boundary; releases are “good enough” when strict validation passes and the derived registry is current.

### Durable execution

Use the provided targets and scripts:
- `make ags-validate`
- `make ags-registry`
- `scripts/ags_init.sh` (new projects)
- `scripts/ags_adopt_existing.sh` (existing projects)

---
type: system_map
description: "TIER 1 SYSTEM MAP"
version: 1.0.0
updated: 2026-01-01
status: active
depends_on: 
doc_id: gov-030
slug: tier1-system-map
title: "Tier 1 System Map"
tier: tier1
authority: binding
review_status: accepted
created: 2026-01-01
owner: human
---
# TIER 1 SYSTEM MAP

---

## Purpose

This document provides a **single, authoritative map of all Tier 1 artifacts** and how they relate.

It answers:
- What artifacts are canonical?
- What role does each play?
- How do they interact?

---

## Tier 1 Artifact Set

### Intent & Direction
- **PROJECT_BRIEF.md**
  - Defines outcome, scope, constraints, success criteria
  - Root of intent

### Governance & Enforcement
- **GOVERNANCE_GIT.md**
  - Defines how Git enforces governance
- **GOVERNANCE_BACKLOG.md**
  - Captures deferred governance rigor

### Architecture & Constraints
- **ARCHITECTURE.md**
  - System structure and boundaries
- **DATA_MODEL.md**
  - Conceptual/logical data architecture
- **SECURITY_BASELINE.md**
  - Non-negotiable security requirements

### Execution Contract
- **TASKS.md / PLAN.md**
  - Work items and acceptance criteria

### Decision System
- **ADR_INDEX.md**
  - Index of all decisions
- **adrs/ADR-###.yaml**
  - Canonical decision records

### Control Plane
- **ARTIFACT_REGISTRY.(json|yaml)**
  - Index of all artifacts
- **drift_rules.yaml**
  - Defines drift detection logic

---

## Relationship Model (Conceptual)

Outcome
  → Project Brief
    → Architecture
      → Data Model
        → Schema (Tier 2)
    → Security Baseline
    → Tasks / Plan
      → Code

Changes
  → Drift Detection
    → ADR
      → Artifact Update
        → Merge

---

## Authority Rules

- Tier 1 artifacts are binding systems of record.
- Changes require reconciliation.
- ADRs explain why changes occur.
- Git merge is the acceptance gate.

---

## Status

This map defines the **minimum viable governance system**.
Additions require governance review or ADR.

---

## Review & Change History

**Current Version:** 0.2.0  
**Review Status:** draft

### Changes Since Last Review
- Initial packaging cleanup; standardized frontmatter and review section.

- `docs/ARTIFACT_REGISTRY.md` — Defines the registry as a derived control-plane artifact.

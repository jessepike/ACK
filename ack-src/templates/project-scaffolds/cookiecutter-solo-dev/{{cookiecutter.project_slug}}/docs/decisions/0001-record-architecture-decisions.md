---
type: template
description: "ADR 0001: Record architecture decisions"
version: 0.1.0
updated: "2026-01-04T09:26:12"
---

# ADR 0001: Record architecture decisions

## Status
Accepted

## Context
We want lightweight decision logging that survives context loss.

## Decision
Use `docs/decisions/` with sequential ADRs.

## Consequences
- Faster onboarding for future maintainers.
- Small overhead to write decisions when they matter.

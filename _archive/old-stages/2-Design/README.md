---
type: "guide"
description: "Design stage overview and artifact inventory"
version: "1.0.0"
updated: "2026-01-03T00:00:00"
---

# Stage 2: Design

## Intent

Define WHAT we're building technically (not HOW to implement it).

## Process

1. Start with validated Project Brief
2. Design architecture iteratively
3. External validation (review architecture with other agents)
4. Progressive detail: Architecture → Data Model → Schemas → Components
5. Update Brief with technical decisions

## Inputs

| Artifact | From |
|----------|------|
| Project Brief | Stage 1 (Discovery) |

## Outputs

| Artifact | Type | Description |
|----------|------|-------------|
| **Architecture.md** | Deliverable | Master technical artifact |
| Data Model | Derivative | Conceptual/logical data domains |
| Schema(s) | Derivative | Physical schema definitions |
| Frontend Design | Derivative | Frontend component structure |
| Backend Design | Derivative | Backend service structure |
| Updated Brief | Deliverable | Brief enhanced with tech decisions |

## Exit Criteria

- Architecture validated externally
- All necessary derivatives created
- Technical design is clear enough for implementation planning

## Artifacts in This Directory

- `architecture.md` - Master technical document
- `data-model.md` - Data domains and relationships
- `schemas/` - Physical schema definitions
- `frontend/` - Frontend design artifacts
- `backend/` - Backend design artifacts
- `reviews/` - External review feedback

## Note

This stage produces CONTEXT documents ("here IS the schema"), not implementation specs ("here's HOW to build the schema"). Implementation specs come in Stage 4.

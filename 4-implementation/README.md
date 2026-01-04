---
type: "guide"
description: "Implementation planning stage overview and artifact inventory"
version: "1.0.0"
updated: "2026-01-03T00:00:00"
---

# Stage 4: Implementation Planning

## Intent

Create structured plan that agents execute against. This is the handoff to execution.

## Process

1. Gather all prior artifacts (hierarchically organized)
2. Work with Planning Agent to create implementation plan
3. Break down into phases, milestones, deliverables
4. Create task breakdown (separate from plan)
5. Define task ↔ commit correspondence
6. Validate agents have everything needed

## Inputs

| Artifact | From |
|----------|------|
| Project Brief | Stage 1 |
| Architecture + derivatives | Stage 2 |
| Configured project | Stage 3 |
| Agent harness | Stage 3 |

## Outputs

| Artifact | Type | Description |
|----------|------|-------------|
| **Plan** | Deliverable | Phases, milestones, deliverables |
| **Tasks** | Deliverable | Individual work items, trackable |

**Plan and Tasks are separate artifacts.**

## Exit Criteria

- Plan covers all implementation work
- Tasks are atomic and executable
- Task ↔ commit mapping is clear
- Agents have clear what/why/how
- Rules and guardrails in place

## Artifacts in This Directory

- `plan.md` - Implementation plan (phases, milestones)
- `tasks.md` - Task breakdown
- `rules.md` - Implementation rules for agents

## Task Execution Flow

```
Agent picks up task
    ↓
Completes work
    ↓
Updates task file
    ↓
Commits (commit ↔ task correspondence)
    ↓
Next task or done
```

## Note

This stage produces the handoff to execution (Stage 5). After this, development agents take over with clear guidance.

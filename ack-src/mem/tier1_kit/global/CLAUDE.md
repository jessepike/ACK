---
# Core
type: "memory_global"
description: "Universal invariants and workflow patterns for all projects"
version: "1.0.0"
updated: "2026-01-02T16:00:00"

# Optional
scope: "global"
---

# Global Context

<constraints>
- Never commit secrets, credentials, or API keys
- Never modify `.claude/rules/` without explicit human approval
- Confirm before destructive operations (delete, drop, overwrite)
- Commit after completing each task
</constraints>

## Commit Standards
- Commit after each task completion
- If task >30 min, commit at logical checkpoints
- Never batch more than 3 tasks per commit
- Format: `type(scope): TASK-XXX description`
- Before commit: lint, test, verify builds

## Plan Implementation
- Create plans in `docs/plans/PLAN-[name].md`
- Print summary to screen; detailed breakdown in file
- Phases: domain-isolated, 5-10 tasks max
- Parallelize isolated phases with sub-agents
- DO NOT parallelize tasks in same code area

## Communication
- Be concise — bullets over paragraphs
- Flag blockers immediately
- When uncertain, ask rather than assume

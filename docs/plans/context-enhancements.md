---
type: "plan"
description: "Context enhancement features for future implementation"
version: "0.2.0"
created: "2026-01-04"
updated: "2026-01-04"
status: "backlog"
priority: "low"
depends_on: ["docs/plans/tier2-memory-model.md"]
---

# Context Enhancements Plan

## Overview

Future features to enhance context management after Tier-2 memory is implemented.

**Note:** The "Promote-to-Learning" pattern has been moved to the core Tier-2 plan as "Phase 2: Curation & Review Tools" - it's critical for safe memory injection.

---

## Feature 1: Ownership Markers

### Purpose

Prevent agents from accidentally overwriting human-curated content while allowing updates to dynamic sections.

### Concept

Mark sections of context files with ownership:
- **HUMAN:** Never auto-modify
- **AGENT:** Can be updated by agents
- **AUTO:** Maintained by system/scripts
- **EPHEMERAL:** Session-specific, auto-cleaned

### Syntax

```markdown
<!-- OWNER: HUMAN -->
## Stack
- Node.js 20
- TypeScript 5.x
<!-- /OWNER -->

<!-- OWNER: AGENT -->
## Recent Activity
Last session worked on authentication flow.
<!-- /OWNER -->

<!-- OWNER: EPHEMERAL expires="session" -->
## Current Task
Implementing login form
<!-- /OWNER -->
```

### Implementation Notes

- Parse markers when reading context files
- Enforce ownership during writes
- Auto-clean EPHEMERAL sections on session end
- Integrate with Tier-1 CLAUDE.md spec

### Source Material

- `inbox/tier2-candidates/CONTEXT_HYGIENE_SPEC.md` (2396 lines)

---

## Feature 2: Context Hygiene System

### Purpose

Automated drift detection and context cleanup.

### Components

1. **File Watcher:** Monitor context files for changes
2. **Hash Tracking:** MD5 of sections to detect drift
3. **Change Attribution:** Log who changed what (human vs agent)
4. **Auto-Cleanup:** Prune stale dynamic sections
5. **Drift Alerts:** Surface unexpected changes

### Integration Points

- Hooks into claude-mem observation capture
- Compares observations against intent artifacts
- Surfaces drift warnings in session start context

### Implementation Notes

- Start with manual drift review
- Add automated detection later
- Consider git-based change tracking

### Source Material

- `inbox/tier2-candidates/CONTEXT_HYGIENE_SPEC.md` (2396 lines)

---

## Dependencies

All features depend on:
1. Working Tier-2 memory with curation (see tier2-memory-model.md Phase 2)
2. Multi-scope storage architecture
3. MCP server for queries

---

## Priority Order

1. **Ownership Markers** - Lowest complexity, highest immediate value
2. **Context Hygiene** - Higher complexity, full drift detection

**Note:** Promote-to-Learning is now part of core Tier-2 (Phase 2: Curation).

---

## Success Criteria

- [ ] Ownership markers prevent unintended overwrites
- [ ] Drift is detected and surfaced proactively

---
type: "backlog"
description: "ACK project backlog - deferred features and future work"
version: "0.1.0"
updated: "2026-01-04"
---

# ACK Backlog

## High Priority

### Tier-2 Memory System
- **Status:** Planning complete
- **Plan:** [docs/plans/tier2-memory-model.md](docs/plans/tier2-memory-model.md)
- **Dependencies:** Tier-1 complete
- **Scope:**
  - [ ] Fix claude-mem hook registration
  - [ ] Multi-scope storage architecture
  - [ ] MCP server implementation
  - [ ] Integration testing

---

## Medium Priority

### Context Enhancements
- **Status:** Deferred
- **Plan:** [docs/plans/context-enhancements.md](docs/plans/context-enhancements.md)
- **Dependencies:** Tier-2 memory

#### Ownership Markers
- **Description:** Section ownership for context files (HUMAN/AGENT/AUTO/EPHEMERAL)
- **Value:** Prevents agents from overwriting human-curated content
- **Source:** `inbox/tier2-candidates/CONTEXT_HYGIENE_SPEC.md`

#### Promote-to-Learning Pattern
- **Description:** Graduate episodic observations to permanent learnings
- **Value:** Builds knowledge base from captured observations
- **Source:** `inbox/tier2-candidates/LEARNINGS_IMPLEMENTATION_SPEC.md`

#### Context Hygiene System
- **Description:** Automated drift detection and context cleanup
- **Value:** Catches divergence from intent proactively
- **Source:** `inbox/tier2-candidates/CONTEXT_HYGIENE_SPEC.md`

---

## Low Priority

### From Project Brief (Deferred)

- **Automated enforcement (hooks):** Git hooks to enforce rules
- **Automated drift detection:** Compare work against intent
- **Advanced CLI tooling:** Project scaffolding, validation
- **Self-running validation agents:** Autonomous quality checks
- **`/advance-stage` skill:** Auto-archive + stage transition
- **`/init-project` skill:** Scaffold new ACK project

---

## Completed

- [x] Tier-1 Memory Kit (`ack-src/mem/TIER1_KIT_SPEC.md`)
- [x] Stage model definition (Discover → Design → Setup → Develop)
- [x] Artifact hierarchy and governance (`ack-src/gov/`)

---

## Source Materials

Reference specs preserved in `inbox/tier2-candidates/`:
- `CLAUDE_MEM_INTEGRATION_SPEC.md` - Claude-mem integration
- `CLAUDE_MEM_HOOKS_SETUP.md` - Hook installation
- `MCP_SERVER_SPEC.md` - MCP server design
- `MEMORY.md` - Memory types
- `DATA_MODEL.md` - Schema patterns
- `CONTEXT_HYGIENE_SPEC.md` - Ownership markers, drift detection
- `LEARNINGS_IMPLEMENTATION_SPEC.md` - Problem-solution pairs

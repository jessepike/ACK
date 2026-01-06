---
type: backlog
description: "Memory System Backlog"
version: 0.2.0
updated: 2026-01-04
status: active
doc_id: mem-backlog-001
title: "Memory System Backlog"
owner: human
created: 2026-01-02
---

# Memory System Backlog

## Purpose

Captured ideas and deferred decisions for the two-tier memory system.

---

## Tier-2 Implementation Queue

Active implementation tracked in [TIER2_STATUS.md](./TIER2_STATUS.md).

### Priority: CRITICAL

#### Phase 2: Curation & Review Tools
- **Spec:** [CURATION_SPEC.md](./tier2_kit/CURATION_SPEC.md)
- **Blocks:** Phase 5 (Injection)
- **Items:**
  - [ ] Add `status` column to memories table
  - [ ] Implement `claude-mem list --status`
  - [ ] Implement `claude-mem promote <id>`
  - [ ] Implement `claude-mem reject <id>`
  - [ ] Build TUI browser (`claude-mem browse`)
  - [ ] Add quality indicators (confidence, duplicates)
  - [ ] Implement bulk operations with safety guards

### Priority: HIGH

#### Phase 3: ACK-Specific MCP Server
- **Spec:** [MCP_SERVER_SPEC.md](./tier2_kit/MCP_SERVER_SPEC.md)
- **Items:**
  - [ ] Create MCP server project structure
  - [ ] Implement `query_memories` tool
  - [ ] Implement `get_memory` tool
  - [ ] Implement `list_scopes` tool
  - [ ] Implement `get_context` tool
  - [ ] Register with Claude Code

### Priority: MEDIUM

#### Phase 4: Multi-Scope Architecture
- **Spec:** See [tier2-memory-model.md](../docs/plans/tier2-memory-model.md)
- **Items:**
  - [ ] Design `~/.ack-mem/` structure
  - [ ] Create scope management CLI
  - [ ] Implement scope isolation (separate DBs)
  - [ ] Add scope auto-detection from project path

### Priority: LOW (After Curation Works)

#### Phase 5: Enable Injection
- [ ] Re-enable SessionStart hook
- [ ] Configure to only inject APPROVED memories
- [ ] Add injection controls (max tokens, recency filters)
- [ ] Monitor for drift issues

---

## Tier-2 Future Enhancements

### Promote-to-Tier-1 Workflow
- Generate markdown drafts in `rules/learnings/`
- Capture problem/solution pairs with tags
- Track source memory for provenance
- **Status:** Designed in CURATION_SPEC.md, implement after Phase 2

### Memory Analytics
- Most common tags/concepts
- Learning trends over time
- Session productivity metrics
- **Status:** Deferred until stable data collection

### AI-Assisted Review
- Auto-approve high-confidence memories
- Suggest duplicates during capture
- Quality scoring refinement
- **Status:** Evaluate after manual curation proves effective

---

## Deferred: Option B Granularity (Fine-Grained Rules Files)

**Context:** When designing Tier-1 kit, we chose Option A (fewer, denser files) over Option B (more, focused files).

**Option B Structure:**
```
~/.claude/rules/
├── 00-security.md         # ~80 lines
├── 10-code-style.md       # ~60 lines
├── 20-testing.md          # ~50 lines
├── 30-git-workflow.md     # ~40 lines
└── 40-documentation.md    # ~40 lines
```

**When to revisit:**
- Any single file exceeds 200-line limit
- Need conditional `paths:` loading for specific file types
- Content becomes hard to navigate in combined files
- Team scaling requires finer-grained ownership

**Advantages of Option B:**
- Easier to assign ownership per topic
- Cleaner git blame/history per concern
- Enables conditional loading via `paths:` frontmatter
- Better for teams with specialized reviewers

**Migration path:** Split files by topic, update numbering prefix to maintain load order.

---

## Future Ideas

### Cross-Project Learning Mechanism
- Pattern: Agent proposes rules in `.claude/proposed-global.md`
- Human reviews at project end, promotes to `~/.claude/rules/`
- Status: Deferred until Option A proves stable

### Symlink-Based Rule Sharing
- Official Claude Code feature: rules/ supports symlinks
- Could share common rules across repos via central location
- Status: Evaluate after establishing base patterns

### Conditional Rules via `paths:` Frontmatter
- Load rules only when working with matching files
- Example: API rules only for `src/api/**/*.ts`
- Status: Implement when specific use case emerges

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation with Option B documentation

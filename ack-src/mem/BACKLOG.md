---
type: backlog
description: "Memory System Backlog"
version: 0.1.0
updated: 2026-01-02
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

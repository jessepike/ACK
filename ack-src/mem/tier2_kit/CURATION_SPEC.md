---
type: spec
description: "Memory Curation and Review Workflow Specification"
version: 0.1.0
created: 2026-01-04
updated: 2026-01-04
status: draft
doc_id: curation-spec
title: "Curation & Review Specification"
owner: human
depends_on: ["tier2_kit/CLAUDE_MEM_SPEC.md"]
priority: critical
---

# Curation & Review Specification

## Overview

This specification defines the **critical** curation workflow for Tier-2 memories. Without curation, AI-captured memories cannot be safely injected into sessions.

**Status:** Phase 2 of Tier-2 implementation. BLOCKING for injection (Phase 5).

## Why Curation Matters

### The Problem

Without curation, blindly injecting AI-curated memories could cause:
- **Outdated information** influencing new sessions
- **Wrong decisions** being reinforced
- **Context pollution** with noise
- **Incorrect patterns** propagating across projects

### The Solution

Human review before injection:

```
Capture → STAGING → Human Review → APPROVED → Available for Injection
              ↓
           REJECTED (archived or deleted)
```

---

## Workflow States

### Memory Status Lifecycle

```
┌─────────┐     ┌─────────┐     ┌──────────┐
│ STAGING │────▶│ APPROVED│────▶│ PROMOTED │
└────┬────┘     └─────────┘     └──────────┘
     │                              │
     │         ┌──────────┐         │
     └────────▶│ REJECTED │◀────────┘
               └──────────┘
```

| Status | Description | Available for Injection |
|--------|-------------|------------------------|
| `staging` | Newly captured, awaiting review | No |
| `approved` | Human-reviewed and accepted | Yes |
| `promoted` | Elevated to Tier-1 (CLAUDE.md, rules/) | Via Tier-1 |
| `rejected` | Archived or deleted | No |

### Default Behavior

- **New memories** → `staging`
- **Injection** → Only `approved` memories
- **MCP queries** → `approved` by default (can include `staging` with flag)

---

## Database Schema Changes

### Add Status Column

```sql
ALTER TABLE memories ADD COLUMN status TEXT DEFAULT 'staging';
ALTER TABLE memories ADD COLUMN reviewed_at TEXT;
ALTER TABLE memories ADD COLUMN reviewed_by TEXT;  -- 'human' or 'bulk'

CREATE INDEX idx_memories_status ON memories(status);
```

### Migration Script

```sql
-- Migrate existing memories to 'staging'
UPDATE memories SET status = 'staging' WHERE status IS NULL;
```

---

## CLI Commands

### Browse/List

```bash
# Interactive TUI browser
claude-mem browse

# List memories for project
claude-mem list --project ack

# List with status filter
claude-mem list --status staging

# List recent (last 7 days)
claude-mem list --since 7d

# Search memories
claude-mem search "authentication"
```

### View Details

```bash
# Show full memory details
claude-mem show <id>

# Show with session context
claude-mem show <id> --context
```

### Review Workflow

```bash
# Start interactive review session
claude-mem review

# Promote single memory
claude-mem promote <id>

# Promote with note
claude-mem promote <id> --note "Verified accurate"

# Reject single memory
claude-mem reject <id>

# Reject with reason
claude-mem reject <id> --reason "Outdated information"

# Bulk promote (with confirmation)
claude-mem bulk-promote --since 7d

# Bulk promote by project
claude-mem bulk-promote --project ack --since 7d
```

### Promotion to Tier-1

```bash
# Promote to Tier-1 learning (creates draft in rules/)
claude-mem promote-to-tier1 <id>

# Preview what would be added
claude-mem promote-to-tier1 <id> --preview
```

---

## Interactive Review Interface

### TUI Design (claude-mem review)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Memory Review                                    [3/15 pending]    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ack_abc123_2026-01-04_001                                         │
│  ───────────────────────────────────────────────────────────────── │
│                                                                     │
│  Title: Railway env vars need NIXPACKS_ prefix                     │
│                                                                     │
│  Subtitle: Build-time env vars require NIXPACKS_ prefix for        │
│            Nixpacks builds                                          │
│                                                                     │
│  Facts:                                                             │
│  • NIXPACKS_ prefix required for build-time env vars               │
│  • Runtime vars work without prefix                                 │
│  • Check Railway docs for buildpack-specific requirements          │
│                                                                     │
│  Concepts: [railway] [deployment] [env-vars]                       │
│  Files: railway.toml, .env.example                                 │
│                                                                     │
│  Session: Railway Deployment Setup (2026-01-04)                    │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  Quality Indicators:                                                │
│  Confidence: 0.87  |  Tokens: 156  |  Concepts: 3  |  Duplicate: No│
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [a] Approve   [r] Reject   [s] Skip   [e] Edit   [q] Quit         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `a` | Approve memory |
| `r` | Reject memory |
| `s` | Skip (review later) |
| `e` | Edit memory (title, facts, etc.) |
| `t` | Edit tags/concepts |
| `p` | Promote to Tier-1 |
| `n` | Next memory |
| `b` | Previous memory |
| `q` | Quit |

---

## Quality Indicators

### Metrics to Display

| Indicator | Source | Purpose |
|-----------|--------|---------|
| **Confidence** | AI filter score | How certain the AI was about storage |
| **Token count** | Fact/subtitle length | Density of information |
| **Concept density** | Number of concepts | Categorization breadth |
| **Duplicate score** | Vector similarity | Potential duplicate detection |
| **Age** | created_at | How old the memory is |
| **Session context** | Parent session | What was being worked on |

### Duplicate Detection

Before approving, check for similar existing memories:

```sql
SELECT id, title,
       (SELECT MAX(similarity) FROM chroma_similar WHERE id = m.id) as similarity
FROM memories m
WHERE status = 'approved'
ORDER BY similarity DESC
LIMIT 5;
```

Flag if similarity > 0.85 (likely duplicate).

---

## Promote to Tier-1

### When to Promote

Promote memories that are:
- **Stable patterns** that won't change
- **Cross-project** applicable
- **Verified** through repeated use
- **Foundational** decisions

### Promotion Output

Creates a draft in `~/.claude/rules/` or project rules:

```markdown
---
type: learning
source: tier2-memory
source_id: ack_abc123_2026-01-04_001
promoted_at: 2026-01-04
---

# Railway Environment Variables

## Problem
Railway couldn't see env vars set in dashboard. App failed to start.

## Solution
Railway with Nixpacks requires `NIXPACKS_` prefix for build-time env vars.
Runtime vars work without prefix.

## Tags
railway, deployment, env-vars
```

---

## Bulk Operations

### Bulk Promote

```bash
# Promote all staging memories from last 7 days
claude-mem bulk-promote --since 7d

# Preview first
claude-mem bulk-promote --since 7d --dry-run

# With project filter
claude-mem bulk-promote --project ack --since 7d
```

### Bulk Reject

```bash
# Reject all staging memories older than 30 days
claude-mem bulk-reject --older-than 30d

# Reject by low confidence
claude-mem bulk-reject --confidence-below 0.5
```

### Safety Guards

- All bulk operations require `--confirm` or interactive confirmation
- Dry-run available with `--dry-run`
- Maximum 100 items per batch
- Audit log of bulk actions

---

## Audit Trail

### Log All Curation Actions

```sql
CREATE TABLE curation_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  memory_id TEXT NOT NULL,
  action TEXT NOT NULL,         -- 'approve', 'reject', 'promote', 'edit'
  previous_status TEXT,
  new_status TEXT,
  reason TEXT,
  actor TEXT DEFAULT 'human',   -- 'human', 'bulk', 'auto'
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_curation_log_memory ON curation_log(memory_id);
CREATE INDEX idx_curation_log_action ON curation_log(action);
```

---

## Integration Points

### With MCP Server

MCP queries respect status:

```typescript
// Default: only approved
query_memories({ query: "deployment" })

// Include staging
query_memories({ query: "deployment", status: "all" })

// Only staging (for review)
query_memories({ status: "staging" })
```

### With Injection (Phase 5)

SessionStart hook only injects approved memories:

```typescript
const memories = await db.query(`
  SELECT * FROM memories
  WHERE status = 'approved'
  AND project = ?
  ORDER BY created_at DESC
  LIMIT 10
`, [project])
```

### With Tier-1

Promoted memories create drafts in:
- `~/.claude/rules/learnings/` (global)
- `.claude/rules/learnings/` (project-specific)

---

## Implementation Phases

### Phase 2a: Schema & CLI Basics

1. Add `status` column to memories table
2. Implement `claude-mem list --status`
3. Implement `claude-mem show <id>`
4. Implement `claude-mem promote <id>`
5. Implement `claude-mem reject <id>`

### Phase 2b: Interactive Review

1. Build TUI browser (`claude-mem browse`)
2. Implement review mode (`claude-mem review`)
3. Add quality indicators
4. Add duplicate detection

### Phase 2c: Bulk Operations

1. Implement `bulk-promote`
2. Implement `bulk-reject`
3. Add safety guards
4. Add audit logging

### Phase 2d: Tier-1 Promotion

1. Implement `promote-to-tier1`
2. Generate markdown drafts
3. Integrate with rules/ structure

---

## Exit Criteria

Phase 2 is complete when:

- [ ] Can browse/list/search memories via CLI
- [ ] Staging area separates new from approved
- [ ] Can promote or reject individual memories
- [ ] Quality indicators visible during review
- [ ] Bulk operations work with safety guards
- [ ] Audit trail captures all curation actions

---

## Risk Mitigation

### Over-Approval

Risk: Approving too many memories → context pollution

Mitigation:
- Quality indicators highlight low-confidence items
- Duplicate detection warns of redundancy
- Regular cleanup prompts for old approved items

### Under-Approval

Risk: Valuable memories stuck in staging → lost knowledge

Mitigation:
- Weekly reminder for unreviewed items
- Bulk approve with confidence threshold
- Session-end prompt to review new memories

### Inconsistent Curation

Risk: Different standards over time

Mitigation:
- Document curation guidelines
- Audit log for review patterns
- Periodic consistency checks

---

## Related Documents

- [Tier-2 README](./README.md)
- [Claude-mem Spec](./CLAUDE_MEM_SPEC.md)
- [MCP Server Spec](./MCP_SERVER_SPEC.md)
- [Implementation Status](../TIER2_STATUS.md)
- [Implementation Plan](../../docs/plans/tier2-memory-model.md)

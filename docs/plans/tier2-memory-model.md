---
type: "plan"
description: "Tier-2 Memory System implementation plan"
version: "0.2.0"
created: "2026-01-04"
updated: "2026-01-04"
status: "active"
priority: "high"
depends_on: ["ack-src/mem/TIER1_KIT_SPEC.md"]
---

# Tier-2 Memory Model Implementation Plan

## Overview

Implement the three-layer memory architecture for ACK:
1. **Tier-1:** Curated guidance (CLAUDE.md, rules/) - DONE
2. **Tier-2:** Episodic observations (claude-mem) - THIS PLAN
3. **MCP:** Agent access layer (read-only) - THIS PLAN
4. **Curation:** Human review before injection - THIS PLAN (CRITICAL)

## Current State

### Claude-Mem Status (as of 2026-01-04)

| Component | Status | Notes |
|-----------|--------|-------|
| CLI | ✅ Installed | `claude-mem` available globally |
| Database | ✅ Has data | SQLite + Chroma operational |
| Hooks | ✅ Registered | In `~/.claude/settings.json` |
| Capture | ✅ Active | PostToolUse, UserPromptSubmit, Stop |
| Injection | ❌ Disabled | SessionStart hook removed for safety |

### Capture-Only Mode

Currently running in **capture-only mode**:
- Observations ARE being captured and stored
- Context is NOT being injected at session start
- This allows reviewing what's captured before trusting it

**To re-enable injection later**, add to `~/.claude/settings.json`:
```json
"SessionStart": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "/Users/jessepike/.claude-mem/hooks/session-start.js",
        "timeout": 180
      }
    ]
  }
]
```

### How Capture Works

```
Tool Use (Read, Write, Bash, etc.)
        ↓
PostToolUse hook receives response
        ↓
Sonnet 4.5 API call analyzes it (separate from your session)
        ↓
AI decides: Store or Skip based on criteria
        ↓
If store → Decomposes into: Title, Subtitle, Facts, Concepts
        ↓
Stored to SQLite + Chroma vector DB
```

**What Gets Stored:** File contents with logic, search results, build errors, architecture decisions, git diffs
**What Gets Skipped:** Simple status checks, trivial edits, repeated operations, binary data

---

## Architecture

### Three-Layer Model

```
Tier-1: Curated guidance (CLAUDE.md, rules/)
   ↓ promotes stable items
Tier-2: Episodic observations (claude-mem)
   ↓ queries
MCP: Agent access layer (read-only)
```

### Multi-Scope Storage

Support multiple memory instances (dev, personal, per-project):

```
~/.ack-mem/
├── config.json              # Global config, scope registry
├── scopes/
│   ├── dev/                 # Development memory
│   │   ├── memory.db        # SQLite (sessions, observations, learnings)
│   │   └── chroma/          # Vector embeddings
│   ├── personal/            # Personal knowledge base
│   │   ├── memory.db
│   │   └── chroma/
│   └── [project-name]/      # Project-specific memories
│       ├── memory.db
│       └── chroma/
└── mcp-server/              # MCP server routes to scopes
```

**Key Decisions:**
- Each scope = isolated SQLite + Chroma instance
- Common schema across all scopes
- MCP server provides unified query interface
- Scope selection via project context or explicit flag

---

## MCP Server Design

### Core Tools

| Tool | Purpose |
|------|---------|
| `query_memories` | Search across memories by text/tags/scope |
| `get_memory` | Retrieve specific memory by ID |
| `list_scopes` | Show available memory scopes |
| `get_context` | Get relevant context for current project |

### Access Pattern

```
Claude Code Agent
       ↓ MCP query
   MCP Server
       ↓ routes to scope
   SQLite/Chroma
       ↓ results
   Agent Context
```

### Tool Schemas

```typescript
// query_memories
{
  query: string,      // Search text
  scope?: string,     // Scope name (default: auto-detect from project)
  tags?: string[],    // Filter by tags
  limit?: number,     // Max results (default: 10)
  type?: "session" | "observation" | "learning"
}

// get_memory
{
  id: string,
  scope?: string
}

// list_scopes
{} // No params

// get_context
{
  project_path?: string  // Default: current working directory
}
```

---

## Implementation Phases

### Phase 1: Capture Validation ✅ DONE

1. ~~Diagnose hook registration in Claude Code settings~~
2. ~~Register hooks (PostToolUse, UserPromptSubmit, Stop)~~
3. ~~Disable SessionStart for capture-only mode~~
4. Run sessions and verify data is being stored

**Exit criteria:** New sessions and observations appear in database

### Phase 2: Curation & Review Tools (CRITICAL - DO FIRST)

Build tools to review and curate captured memories BEFORE enabling injection.

#### 2a. Memory Browser CLI
```bash
claude-mem browse                    # Interactive TUI browser
claude-mem list --project ack        # List memories for project
claude-mem show <id>                 # View full memory details
claude-mem search "authentication"   # Semantic search
```

#### 2b. Staging Area
Memories go to staging first, not directly to "approved":
```
Capture → STAGING → Human Review → APPROVED → Available for Injection
              ↓
           REJECTED (deleted or archived)
```

#### 2c. Promote/Reject Commands
```bash
claude-mem review                    # Start interactive review session
claude-mem promote <id>              # Move from staging to approved
claude-mem reject <id>               # Archive or delete
claude-mem bulk-promote --since 7d   # Approve recent memories
```

#### 2d. Quality Indicators
- Confidence score from AI filter
- Token count / size
- Concept density
- Duplicate detection

**Exit criteria:** Can review, promote, and reject memories before they're injected

### Phase 3: MCP Server

1. Create MCP server project structure
2. Implement core tools (query, get, list, context)
3. **Only serve APPROVED memories** (not staging)
4. Add scope routing logic
5. Register MCP server with Claude Code

**Exit criteria:** Can query approved memories via MCP from Claude Code

### Phase 4: Multi-Scope Architecture

1. Design config.json schema for scope registry
2. Create scope management CLI commands
3. Implement scope isolation (separate DBs)
4. Add scope auto-detection from project path

**Exit criteria:** Can create and switch between scopes (dev, personal, project)

### Phase 5: Enable Injection (Only After Curation Works)

1. Re-enable SessionStart hook
2. Configure to only inject from APPROVED memories
3. Add injection controls (max tokens, recency filters)
4. Monitor for drift issues

**Exit criteria:** Context injection working with curated memories only

### Phase 6: Integration Testing

1. End-to-end test: capture → staging → review → approve → inject
2. Multi-scope queries
3. Drift detection: compare injected context against intent
4. Performance testing with larger datasets

---

## Source Materials

Located in `inbox/tier2-candidates/`:

| File | Use |
|------|-----|
| `CLAUDE_MEM_INTEGRATION_SPEC.md` | Claude-mem integration patterns |
| `CLAUDE_MEM_HOOKS_SETUP.md` | Hook installation guide |
| `MCP_SERVER_SPEC.md` | MCP server design reference |
| `MEMORY.md` | Memory types (sessions/decisions/learnings) |
| `DATA_MODEL.md` | Schema design patterns |

---

## Open Questions

1. Should we use existing `~/.claude-mem/` or create new `~/.ack-mem/`?
2. How to handle scope conflicts when project matches multiple scopes?
3. What's the retention policy for staging vs approved memories?
4. Should rejected memories be deleted or archived for potential recovery?
5. How aggressive should duplicate detection be?

---

## Success Criteria

### Phase 1 (Capture) ✅
- [x] Claude-mem hooks registered in settings.json
- [x] Capture-only mode enabled (no injection)
- [ ] Verify observations appearing in database after sessions

### Phase 2 (Curation) - BLOCKING
- [ ] Can browse/list/search memories via CLI
- [ ] Staging area separates new from approved
- [ ] Can promote or reject individual memories
- [ ] Quality indicators visible during review

### Phase 3 (MCP)
- [ ] MCP server queryable from Claude Code
- [ ] Only approved memories served
- [ ] Semantic search working

### Phase 4 (Multi-Scope)
- [ ] Multiple scopes working (dev, personal, project)
- [ ] Scope auto-detection from project path

### Phase 5 (Injection)
- [ ] SessionStart hook re-enabled
- [ ] Only approved memories injected
- [ ] No drift observed in test sessions

---

## Risk: Memory Drift

Without curation, blindly injecting AI-curated memories could cause:
- Outdated information influencing new sessions
- Wrong decisions being reinforced
- Context pollution with noise

**Mitigation:** Phase 2 (Curation) MUST complete before Phase 5 (Injection).

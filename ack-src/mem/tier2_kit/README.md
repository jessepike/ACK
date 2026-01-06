---
type: spec
description: "Tier-2 Memory System Overview"
version: 0.1.0
created: 2026-01-04
updated: 2026-01-04
status: active
doc_id: tier2-readme
title: "Tier-2 Memory System"
owner: human
---

# Tier-2 Memory System

## Overview

Tier-2 is the **episodic observation layer** of ACK's memory architecture. It captures what happens during Claude Code sessions and makes that knowledge retrievable for future sessions.

```
┌─────────────────────────────────────────────────────────────────┐
│  Tier-1: Curated Guidance (CLAUDE.md, rules/)                  │
│  ────────────────────────────────────────────────────────────── │
│  Human-maintained, always loaded, stable knowledge             │
└───────────────────────────┬─────────────────────────────────────┘
                            │ promotes stable items
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Tier-2: Episodic Observations (claude-mem)        ← THIS LAYER│
│  ────────────────────────────────────────────────────────────── │
│  AI-captured, requires curation, session-specific knowledge    │
└───────────────────────────┬─────────────────────────────────────┘
                            │ queries
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  MCP: Agent Access Layer (read-only)                           │
│  ────────────────────────────────────────────────────────────── │
│  On-demand queries, token-efficient, cross-project search      │
└─────────────────────────────────────────────────────────────────┘
```

## What Gets Captured

Tier-2 captures **observations** from Claude Code sessions:

| Type | Example | Value |
|------|---------|-------|
| Architecture decisions | "Chose SQLite over PostgreSQL for local-first" | Prevents re-debating |
| Bug fixes | "Fixed race condition in async handler" | Searchable solutions |
| Code patterns | "Implemented retry logic with exponential backoff" | Reusable patterns |
| Build errors | "Railway needs NIXPACKS_ prefix for build-time env vars" | Deployment gotchas |
| Discovery | "Found undocumented API behavior in library X" | Tribal knowledge |

## How Capture Works

```
Claude Code Session
        │
        ▼
┌───────────────────┐
│ Tool Use          │  (Read, Write, Bash, etc.)
│ (in your session) │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ PostToolUse Hook  │  (registered in ~/.claude/settings.json)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ AI Filter         │  (SEPARATE Sonnet 4.5 API call)
│ Decides: Store    │  Criteria: semantic value, not trivial
│ or Skip?          │
└─────────┬─────────┘
          │ if store
          ▼
┌───────────────────┐
│ Decompose into:   │
│ - Title (3-8 words)
│ - Subtitle (max 24 words)
│ - Facts (3-7 atomic statements)
│ - Concepts (2-5 tags)
│ - Files touched
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Storage           │
│ - SQLite (metadata)
│ - Chroma (vectors)
└───────────────────┘
```

**Key Point:** The AI filter runs as a **separate API call** (not your current session). This means:
- Extra API cost per session
- Filter decisions are independent of your conversation
- You don't see filter activity in your session

## Storage Structure

```
~/.claude-mem/
├── claude-mem.db          # SQLite: sessions, memories, overviews
├── chroma/                # Vector embeddings for semantic search
├── hooks/                 # Hook scripts (PostToolUse, Stop, etc.)
└── settings.json          # Claude-mem configuration
```

### Database Schema

**memories** table (hierarchical structure):
```sql
CREATE TABLE memories (
  id TEXT PRIMARY KEY,        -- project_session_date_seq
  project TEXT NOT NULL,
  session TEXT NOT NULL,
  date TEXT NOT NULL,
  title TEXT NOT NULL,        -- 3-8 words
  subtitle TEXT,              -- max 24 words
  facts TEXT,                 -- JSON array of atomic facts
  concepts TEXT,              -- JSON array of tags
  files TEXT,                 -- JSON array of file paths
  created_at TEXT
);
```

**streaming_sessions** table:
```sql
CREATE TABLE streaming_sessions (
  id INTEGER PRIMARY KEY,
  claude_session_id TEXT,     -- Claude Code session ID
  project TEXT,
  title TEXT,
  subtitle TEXT,
  status TEXT                 -- active, completed, failed
);
```

## Current Status

See [TIER2_STATUS.md](../TIER2_STATUS.md) for implementation progress.

**What Works:**
- Hooks registered and capturing
- Memories being stored to SQLite + Chroma
- Basic MCP queries via chroma-mcp

**What's Missing:**
- Curation workflow (review/approve/reject)
- Staging area (memories go straight to "approved")
- ACK-specific MCP tools
- Multi-scope storage

## Files in This Directory

| File | Purpose |
|------|---------|
| README.md | This overview |
| [CLAUDE_MEM_SPEC.md](./CLAUDE_MEM_SPEC.md) | Claude-mem integration details |
| [MCP_SERVER_SPEC.md](./MCP_SERVER_SPEC.md) | MCP tool design for querying |
| [CURATION_SPEC.md](./CURATION_SPEC.md) | Review workflow (Phase 2) |

## Related Documents

- [Tier-2 Implementation Plan](../../docs/plans/tier2-memory-model.md)
- [Tier-1 Kit Spec](../TIER1_KIT_SPEC.md)
- [Memory System Backlog](../BACKLOG.md)

## Quick Reference

### Query Memories (via MCP)

```javascript
// Semantic search (always include project name)
mcp__claude-mem__chroma_query_documents(["ack authentication bug"])

// Get specific memory
mcp__claude-mem__chroma_get_documents(ids: ["memory_id"])
```

### CLI Commands

```bash
# Check status
claude-mem status

# View logs
claude-mem logs

# Store memory (used by hooks)
claude-mem store-memory --title "..." --facts '[...]' --project "..."
```

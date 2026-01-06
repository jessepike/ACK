---
type: spec
description: "Claude-mem Integration Specification"
version: 0.1.0
created: 2026-01-04
updated: 2026-01-04
status: active
doc_id: claude-mem-spec
title: "Claude-mem Integration"
owner: human
depends_on: []
---

# Claude-mem Integration Specification

## Overview

Claude-mem is a Claude Code plugin that provides automatic memory capture and compression. This document specifies how ACK integrates with claude-mem for Tier-2 episodic observations.

## What Claude-mem Does

- Automatically captures tool usage (file reads, writes, bash commands)
- Compresses observations via AI summarization
- Stores sessions, observations, summaries in SQLite + Chroma
- Provides search via SQLite + Chroma vector DB
- (Optional) Injects relevant context at session start

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLAUDE CODE                               │
│  ┌─────────────┐                                                │
│  │ Your Session│ ← Tool calls (Read, Write, Bash, etc.)        │
│  └──────┬──────┘                                                │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐                                                │
│  │ Hooks       │ ← Registered in ~/.claude/settings.json       │
│  │ (PostToolUse, UserPromptSubmit, Stop)                       │
│  └──────┬──────┘                                                │
└─────────┼───────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CLAUDE-MEM HOOKS                             │
│                                                                 │
│  PostToolUse:                                                   │
│  1. Receives tool response                                      │
│  2. Calls Sonnet 4.5 API (separate session)                    │
│  3. AI decides: Store or Skip                                   │
│  4. If store → Decompose into hierarchical memory              │
│  5. Write to SQLite + Chroma                                    │
│                                                                 │
│  Stop:                                                          │
│  1. Generate session overview                                   │
│  2. Store final summary                                         │
└─────────┬───────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│  ~/.claude-mem/                                                  │
│  ├── claude-mem.db      # SQLite database                       │
│  └── chroma/            # Vector embeddings                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hook System

### Registered Hooks

Located in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/jessepike/.claude-mem/hooks/post-tool-use.js",
            "timeout": 180
          }
        ],
        "matcher": "*"
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/jessepike/.claude-mem/hooks/user-prompt-submit.js",
            "timeout": 60
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/jessepike/.claude-mem/hooks/stop.js",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Hook Descriptions

| Hook | Trigger | Purpose |
|------|---------|---------|
| PostToolUse | After each tool call | Analyze tool response, store if valuable |
| UserPromptSubmit | User sends message | Record user prompts for context |
| Stop | Session ends | Generate session overview |
| SessionStart | Session begins | Inject relevant context (DISABLED) |

### SessionStart (Currently Disabled)

SessionStart is **intentionally disabled** for capture-only mode. This prevents injecting uncurated memories into sessions.

To re-enable later (after Phase 2 Curation is complete):

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

---

## AI Filter System

The PostToolUse hook uses a **separate Sonnet 4.5 API call** to analyze tool responses.

### Filter Configuration

From `~/.claude-mem/hooks/shared/hook-prompt-renderer.js`:

```javascript
var HOOK_CONFIG = {
  maxUserPromptLength: 200,
  maxToolResponseLength: 20000,
  sdk: {
    model: "claude-sonnet-4-5",
    allowedTools: ["Bash"],
    maxTokensSystem: 8192,
    maxTokensTool: 8192,
    maxTokensEnd: 2048
  }
}
```

### What Gets Stored

The AI filter stores observations with semantic value:

- File contents with logic, algorithms, or patterns
- Search results revealing project structure
- Build errors or test failures with context
- Code revealing architecture or design decisions
- Git diffs with significant changes
- Command outputs showing system state

### What Gets Skipped

- Simple status checks (git status with no changes)
- Trivial edits (one-line config changes)
- Repeated operations
- Binary data or noise
- Anything without semantic value

### Memory Decomposition

When the AI decides to store, it decomposes into:

| Component | Size | Purpose |
|-----------|------|---------|
| Title | 3-8 words | Scannable headline |
| Subtitle | max 24 words | Concise summary |
| Facts | 3-7 items, 50-150 chars each | Atomic, searchable statements |
| Concepts | 2-5 tags | Broad categories |
| Files | List | Actual file paths touched |

---

## Database Schema

### Location

```
~/.claude-mem/claude-mem.db
```

### Tables

#### streaming_sessions

Tracks active and completed sessions:

```sql
CREATE TABLE streaming_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  claude_session_id TEXT UNIQUE NOT NULL,
  sdk_session_id TEXT,
  project TEXT NOT NULL,
  title TEXT,
  subtitle TEXT,
  user_prompt TEXT,
  started_at TEXT NOT NULL,
  started_at_epoch INTEGER NOT NULL,
  updated_at TEXT,
  updated_at_epoch INTEGER,
  completed_at TEXT,
  completed_at_epoch INTEGER,
  status TEXT NOT NULL CHECK(status IN ('active', 'completed', 'failed'))
);
```

#### memories

Hierarchical memory storage:

```sql
CREATE TABLE memories (
  id TEXT PRIMARY KEY,
  project TEXT NOT NULL,
  session TEXT NOT NULL,
  date TEXT NOT NULL,
  title TEXT NOT NULL,
  subtitle TEXT,
  facts TEXT,           -- JSON array
  concepts TEXT,        -- JSON array
  files TEXT,           -- JSON array
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  session_id TEXT
);
```

#### overviews

Session summaries:

```sql
CREATE TABLE overviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project TEXT NOT NULL,
  session TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  session_id TEXT,
  UNIQUE(project, session)
);
```

#### observations (Legacy)

Older observation format:

```sql
CREATE TABLE observations (
  id TEXT PRIMARY KEY,
  session_id TEXT,
  type TEXT,
  concept TEXT,
  narrative TEXT,
  file_path TEXT,
  created_at TEXT,
  tokens INTEGER
);
```

---

## CLI Commands

### Status & Diagnostics

```bash
# Check installation status
claude-mem status

# Run diagnostics
claude-mem doctor

# View operation logs
claude-mem logs
```

### Storage Commands (Used by Hooks)

```bash
# Store a memory
claude-mem store-memory \
  --id "project_session_date_001" \
  --title "Memory Title" \
  --subtitle "Concise description" \
  --facts '["Fact 1", "Fact 2"]' \
  --concepts '["concept1", "concept2"]' \
  --files '["path/to/file.ts"]' \
  --project "project-name" \
  --session "session-id" \
  --date "2026-01-04"

# Store session overview
claude-mem store-overview \
  --project "project-name" \
  --session "session-id" \
  --content "2-3 sentence summary"

# Update session metadata
claude-mem update-session-metadata \
  --project "project-name" \
  --session "session-id" \
  --title "Session Title" \
  --subtitle "What was accomplished"
```

### Installation

```bash
# Install/reinstall hooks
claude-mem install --force --skip-mcp

# Uninstall hooks
claude-mem uninstall
```

---

## Querying Memories

### Direct SQLite

```bash
# List memories
sqlite3 ~/.claude-mem/claude-mem.db \
  "SELECT id, title, date FROM memories ORDER BY created_at DESC LIMIT 10;"

# Search by project
sqlite3 ~/.claude-mem/claude-mem.db \
  "SELECT title, subtitle FROM memories WHERE project = 'ack';"

# Get full memory
sqlite3 -line ~/.claude-mem/claude-mem.db \
  "SELECT * FROM memories WHERE id = 'memory_id';"
```

### Via MCP (chroma-mcp)

```javascript
// Semantic search (include project name for isolation)
mcp__claude-mem__chroma_query_documents(["ack authentication bug fix"])

// Get specific document
mcp__claude-mem__chroma_get_documents(ids: ["document_id"])
```

### Search Tips

1. **Always include project name** in queries for isolation
2. **Include dates** for temporal search: `"ack 2026-01-04 bug fix"`
3. **Intent-based queries** work better than keyword matching
4. **Multiple queries** with different phrasings improve coverage

---

## Memory ID Format

Memories use a structured ID format:

```
{project}_{session}_{date}_{sequence}

Example: ack_5846fad1-1b22-4d9b-b98e-8e253c19322e_2026-01-04_001
```

Components:
- `project`: Project name (directory name)
- `session`: Claude session ID
- `date`: ISO date (YYYY-MM-DD)
- `sequence`: Sequential number (001, 002, etc.)

---

## Integration Points

### With Tier-1

Tier-2 observations can be promoted to Tier-1:
- Stable patterns → Add to `rules/`
- Project decisions → Document in `CLAUDE.md`
- Cross-project learnings → Add to global rules

### With MCP Server

The MCP server (Phase 3) will provide:
- `query_memories` - Search with filters
- `get_memory` - Retrieve by ID
- `list_scopes` - Show available scopes
- `get_context` - Project-relevant context

### With Curation (Phase 2)

Memories will flow through staging:
```
Capture → STAGING → Human Review → APPROVED → Available for Injection
              ↓
           REJECTED
```

---

## Troubleshooting

### Hooks Not Capturing

1. Check registration: `grep -A5 "PostToolUse" ~/.claude/settings.json`
2. Check hook exists: `ls ~/.claude-mem/hooks/post-tool-use.js`
3. View logs: `claude-mem logs`
4. Run diagnostics: `claude-mem doctor`

### Database Issues

```bash
# Check database exists
ls -la ~/.claude-mem/claude-mem.db

# Check schema
sqlite3 ~/.claude-mem/claude-mem.db ".schema"

# Check record counts
sqlite3 ~/.claude-mem/claude-mem.db "SELECT 'memories', count(*) FROM memories;"
```

### API Key Issues

The AI filter requires an Anthropic API key. Check:
```bash
echo $ANTHROPIC_API_KEY
```

---

## Related Documents

- [Tier-2 README](./README.md)
- [MCP Server Spec](./MCP_SERVER_SPEC.md)
- [Curation Spec](./CURATION_SPEC.md)
- [Implementation Status](../TIER2_STATUS.md)

---
type: spec
description: "MCP Server Specification for Tier-2 Memory Access"
version: 0.1.0
created: 2026-01-04
updated: 2026-01-04
status: draft
doc_id: mcp-server-spec
title: "MCP Server Specification"
owner: human
depends_on: ["tier2_kit/CLAUDE_MEM_SPEC.md"]
---

# MCP Server Specification

## Overview

An MCP (Model Context Protocol) server that exposes Tier-2 memories to Claude Code agents. Enables on-demand access to learnings, decisions, and project context without bloating static files.

## Why MCP

| Approach | Token Cost | User Effort | Freshness |
|----------|------------|-------------|-----------|
| **MCP Tools** | ~50 schema + results on-demand | Zero | Always current |
| claude.md injection | 500-5000+ always in context | Manual updates | Stale quickly |
| Manual copy/paste | Variable | High | Point-in-time |

MCP is optimal because:
- **On-demand** — Agent queries only when needed
- **Searchable** — Filter by tags, project, text
- **Cross-project** — Works from any repo
- **Automated** — No manual intervention
- **Token-efficient** — Results only when called

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLAUDE CODE                               │
│                                                                 │
│  Agent: "I'm hitting a deployment issue..."                    │
│         → calls query_memories(tags: ["deployment"])           │
│         → receives relevant learnings                          │
│         → applies solution                                     │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │ stdio (JSON-RPC)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     MCP SERVER                                   │
│                                                                 │
│  Tools:                                                         │
│  • query_memories     Search with filters                       │
│  • get_memory         Get full details by ID                    │
│  • list_scopes        Show available memory scopes              │
│  • get_context        Get project-relevant context              │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │ reads from
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  ~/.claude-mem/                                                  │
│  ├── claude-mem.db      # SQLite (metadata, relationships)     │
│  └── chroma/            # Vector embeddings (semantic search)   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Current State

### What Exists

Generic `chroma-mcp` server registered in `~/.mcp.json`:

```json
{
  "mcpServers": {
    "claude-mem": {
      "command": "uvx",
      "args": ["chroma-mcp", "--client-type", "persistent", "--data-dir", "/Users/jessepike/.claude-mem/chroma"]
    }
  }
}
```

This provides basic Chroma operations:
- `chroma_query_documents` - Vector similarity search
- `chroma_get_documents` - Get by ID

### What's Missing

ACK-specific tools that understand:
- Memory structure (title, subtitle, facts, concepts)
- Project/scope filtering
- Staging vs approved status
- Cross-table queries (memories + sessions + overviews)

---

## Tool Definitions

### 1. query_memories

Search memories with filters.

```typescript
{
  name: "query_memories",
  description: "Search memories from Tier-2 storage. Use when you encounter a problem or need guidance on a specific technology, pattern, or gotcha.",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Free text search across title, subtitle, facts"
      },
      tags: {
        type: "array",
        items: { type: "string" },
        description: "Filter by concept tags (e.g., ['deployment', 'railway'])"
      },
      project: {
        type: "string",
        description: "Filter by project name. Omit to search all projects."
      },
      scope: {
        type: "string",
        description: "Memory scope: 'dev', 'personal', or project name"
      },
      status: {
        type: "string",
        enum: ["staging", "approved", "all"],
        description: "Filter by curation status (default: approved)"
      },
      limit: {
        type: "number",
        description: "Max results (default: 10, max: 50)"
      }
    }
  }
}
```

**Example Usage:**

```javascript
// Search for deployment issues
query_memories({ tags: ["deployment", "railway"] })

// Text search within a project
query_memories({ query: "authentication bug", project: "ack" })

// Cross-project search
query_memories({ query: "pydantic validation" })
```

**Example Response:**

```json
{
  "results": [
    {
      "id": "ack_abc123_2026-01-04_001",
      "title": "Railway env vars need NIXPACKS_ prefix",
      "subtitle": "Build-time env vars require NIXPACKS_ prefix for Nixpacks builds",
      "facts": [
        "NIXPACKS_ prefix required for build-time env vars",
        "Runtime vars work without prefix",
        "Check Railway docs for buildpack-specific requirements"
      ],
      "concepts": ["railway", "deployment", "env-vars"],
      "project": "ack",
      "created_at": "2026-01-04T10:30:00Z"
    }
  ],
  "total": 1
}
```

### 2. get_memory

Get full details of a specific memory.

```typescript
{
  name: "get_memory",
  description: "Get full details of a memory by ID. Use after query_memories to get complete context.",
  inputSchema: {
    type: "object",
    properties: {
      id: {
        type: "string",
        description: "Memory ID (e.g., 'ack_abc123_2026-01-04_001')"
      },
      scope: {
        type: "string",
        description: "Memory scope if known"
      }
    },
    required: ["id"]
  }
}
```

**Example Response:**

```json
{
  "id": "ack_abc123_2026-01-04_001",
  "title": "Railway env vars need NIXPACKS_ prefix",
  "subtitle": "Build-time env vars require NIXPACKS_ prefix for Nixpacks builds",
  "facts": [
    "NIXPACKS_ prefix required for build-time env vars",
    "Runtime vars work without prefix",
    "Check Railway docs for buildpack-specific requirements"
  ],
  "concepts": ["railway", "deployment", "env-vars"],
  "files": ["railway.toml", ".env.example"],
  "project": "ack",
  "session": "abc123",
  "date": "2026-01-04",
  "created_at": "2026-01-04T10:30:00Z",
  "session_context": {
    "title": "Railway Deployment Setup",
    "overview": "Configured Railway deployment with proper env vars..."
  }
}
```

### 3. list_scopes

Show available memory scopes.

```typescript
{
  name: "list_scopes",
  description: "List available memory scopes and their statistics.",
  inputSchema: {
    type: "object",
    properties: {}
  }
}
```

**Example Response:**

```json
{
  "scopes": [
    {
      "name": "dev",
      "path": "~/.ack-mem/scopes/dev",
      "memory_count": 53,
      "last_updated": "2026-01-04T15:00:00Z"
    },
    {
      "name": "ack",
      "path": "~/.ack-mem/scopes/ack",
      "memory_count": 7,
      "last_updated": "2026-01-04T21:11:58Z"
    }
  ],
  "current_scope": "ack"
}
```

### 4. get_context

Get relevant context for current project.

```typescript
{
  name: "get_context",
  description: "Get context for current project including recent memories, decisions, and learnings. Use at session start.",
  inputSchema: {
    type: "object",
    properties: {
      project_path: {
        type: "string",
        description: "Repository path. Defaults to current working directory."
      },
      include_cross_project: {
        type: "boolean",
        description: "Include cross-project learnings (default: true)"
      },
      max_memories: {
        type: "number",
        description: "Max memories to include (default: 5)"
      }
    }
  }
}
```

**Example Response:**

```json
{
  "project": {
    "name": "ack",
    "path": "/Users/jessepike/code/ack"
  },
  "recent_memories": [
    {
      "id": "ack_abc123_2026-01-04_001",
      "title": "Tier-2 Memory System Setup",
      "concepts": ["memory", "claude-mem", "hooks"]
    }
  ],
  "recent_sessions": [
    {
      "id": "5846fad1-1b22-4d9b-b98e-8e253c19322e",
      "title": "ACK Project Initialization",
      "date": "2026-01-04"
    }
  ],
  "cross_project_learnings": [
    {
      "id": "global_xyz_001",
      "title": "Railway NIXPACKS_ prefix",
      "concepts": ["railway", "deployment"]
    }
  ]
}
```

---

## Access Patterns

### Read-Only Access

MCP server opens database in read-only mode:

```typescript
const db = new Database(dbPath, { readonly: true })
```

This ensures:
- No accidental writes
- Safe concurrent access
- No interference with capture hooks

### Query Priority

1. **Approved memories first** - Only curated content by default
2. **Semantic search** - Vector similarity via Chroma
3. **Metadata filters** - Tags, project, date range
4. **Full-text fallback** - SQLite LIKE queries

---

## Implementation Phases

### Phase 3a: Core Tools

1. Create MCP server project structure
2. Implement `query_memories` with SQLite + Chroma
3. Implement `get_memory` with session context
4. Register with Claude Code

### Phase 3b: Scope Routing

1. Implement `list_scopes`
2. Add scope routing logic
3. Auto-detect scope from project path

### Phase 3c: Context Tool

1. Implement `get_context`
2. Aggregate memories, sessions, learnings
3. Add cross-project support

---

## Configuration

### Claude Code Registration

Add to `~/.mcp.json`:

```json
{
  "mcpServers": {
    "ack-memory": {
      "command": "node",
      "args": ["/path/to/ack-mcp-server/dist/index.js"],
      "env": {
        "ACK_MEM_PATH": "~/.ack-mem"
      }
    }
  }
}
```

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `ACK_MEM_PATH` | `~/.ack-mem` | Root memory directory |
| `ACK_MEM_SCOPE` | auto-detect | Current scope |
| `ACK_MEM_DB` | `${ACK_MEM_PATH}/claude-mem.db` | Database path |

---

## Error Handling

### Database Not Found

```typescript
if (!fs.existsSync(dbPath)) {
  return {
    error: "Memory database not found",
    message: "Run claude-mem to start capturing memories",
    path: dbPath
  }
}
```

### No Results

```typescript
if (results.length === 0) {
  return {
    results: [],
    suggestions: [
      "Try broader search terms",
      "Use list_scopes to check available scopes",
      "Recent sessions may not be indexed yet"
    ]
  }
}
```

---

## Testing

### Verification Commands

```bash
# List available tools
/mcp

# Test query
query_memories({ query: "test" })

# Check scopes
list_scopes()
```

### Expected Behavior

- [ ] Server starts without errors
- [ ] Database connection works (read-only)
- [ ] `query_memories` returns results
- [ ] `query_memories` filters by tags
- [ ] `query_memories` filters by project
- [ ] `get_memory` returns full details
- [ ] `list_scopes` shows available scopes
- [ ] `get_context` aggregates relevant data
- [ ] Error handling works for missing DB

---

## Related Documents

- [Tier-2 README](./README.md)
- [Claude-mem Spec](./CLAUDE_MEM_SPEC.md)
- [Curation Spec](./CURATION_SPEC.md)
- [Implementation Status](../TIER2_STATUS.md)

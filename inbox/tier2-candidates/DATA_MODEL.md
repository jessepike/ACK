# Project Studio — Data Model & Build Plan

**Version:** 1.1
**Date:** December 2024
**Updated:** 2025-12-28
**Status:** Implemented

---

## Part 1: Data Model

### Storage Strategy: Hybrid (SQLite + Files)

| Storage | What | Why |
|---------|------|-----|
| **SQLite** | Metadata, relationships, indexes | Fast queries, ACID, single-file backup |
| **Files** | Content (markdown, JSON) | Human-readable, git-friendly, inspectable |

```
~/.project-studio/
├── studio.db                    # SQLite database
├── projects/
│   └── {project-id}/
│       ├── context/
│       │   ├── claude.md        # Canonical context files
│       │   ├── constitution.md
│       │   ├── architecture.md
│       │   └── ...
│       └── sessions/
│           └── {session-id}.md  # Session summaries
├── registry/
│   ├── skills/
│   │   └── {skill-id}.md
│   ├── agents/
│   │   └── {agent-id}.json
│   ├── tools/
│   │   └── {tool-id}.json
│   ├── templates/
│   │   └── {template-id}/
│   │       └── ...
│   └── prompts/
│       └── {prompt-id}.md
└── backups/
    └── studio-{timestamp}.db
```

---

### SQLite Schema

#### Core Tables

```sql
-- ============================================================
-- PROJECTS
-- ============================================================
CREATE TABLE projects (
    id              TEXT PRIMARY KEY,           -- uuid
    name            TEXT NOT NULL,
    description     TEXT,
    repo_path       TEXT,                       -- local filesystem path
    template_id     TEXT,                       -- from registry
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    archived_at     DATETIME                    -- soft delete
);

CREATE INDEX idx_projects_name ON projects(name);
CREATE INDEX idx_projects_archived ON projects(archived_at);

-- ============================================================
-- CYCLES
-- ============================================================
CREATE TABLE cycles (
    id              TEXT PRIMARY KEY,           -- uuid
    project_id      TEXT NOT NULL REFERENCES projects(id),
    name            TEXT NOT NULL,
    description     TEXT,
    cycle_type      TEXT NOT NULL,              -- feature, spike, bugfix, research
    phase           TEXT NOT NULL DEFAULT 'brainstorm',
                                                -- brainstorm, define, refine, implement, test, complete
    intent          TEXT,                       -- what we're trying to accomplish
    success_criteria TEXT,                      -- how we know it's done (JSON array)
    started_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at    DATETIME,
    due_at          DATETIME,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cycles_project ON cycles(project_id);
CREATE INDEX idx_cycles_phase ON cycles(phase);
CREATE INDEX idx_cycles_active ON cycles(project_id, completed_at);

-- ============================================================
-- TASKS
-- ============================================================
CREATE TABLE tasks (
    id              TEXT PRIMARY KEY,
    cycle_id        TEXT NOT NULL REFERENCES cycles(id),
    title           TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',
                                                -- pending, in_progress, complete
    sort_order      INTEGER NOT NULL DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_cycle ON tasks(cycle_id);

-- ============================================================
-- SESSIONS (metadata only - content in files)
-- ============================================================
CREATE TABLE sessions (
    id              TEXT PRIMARY KEY,
    project_id      TEXT NOT NULL REFERENCES projects(id),
    cycle_id        TEXT REFERENCES cycles(id), -- optional
    title           TEXT NOT NULL,
    summary         TEXT,                       -- brief, for list views
    duration_minutes INTEGER,
    files_changed   TEXT,                       -- JSON array of file paths
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_project ON sessions(project_id);
CREATE INDEX idx_sessions_cycle ON sessions(cycle_id);
CREATE INDEX idx_sessions_created ON sessions(created_at DESC);

-- Full session content stored in:
-- ~/.project-studio/projects/{project-id}/sessions/{session-id}.md

-- ============================================================
-- DECISIONS
-- ============================================================
CREATE TABLE decisions (
    id              TEXT PRIMARY KEY,
    project_id      TEXT NOT NULL REFERENCES projects(id),
    cycle_id        TEXT REFERENCES cycles(id), -- optional
    title           TEXT NOT NULL,              -- headline
    rationale       TEXT,                       -- why this decision
    alternatives    TEXT,                       -- JSON array of alternatives considered
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_decisions_project ON decisions(project_id);
CREATE INDEX idx_decisions_cycle ON decisions(cycle_id);
CREATE INDEX idx_decisions_created ON decisions(created_at DESC);

-- ============================================================
-- LEARNINGS (problem/solution pairs for reuse)
-- ============================================================
CREATE TABLE learnings (
    id              TEXT PRIMARY KEY,           -- uuid
    project_id      TEXT REFERENCES projects(id) ON DELETE SET NULL,
    cycle_id        TEXT REFERENCES cycles(id) ON DELETE SET NULL,
    session_id      TEXT REFERENCES sessions(id) ON DELETE SET NULL,
    title           TEXT NOT NULL,              -- short description
    problem         TEXT NOT NULL,              -- what was the problem/challenge
    solution        TEXT NOT NULL,              -- how it was solved
    tags            TEXT,                       -- JSON array of tags for categorization
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_learnings_project ON learnings(project_id);
CREATE INDEX idx_learnings_created ON learnings(created_at DESC);

-- ============================================================
-- CONTEXT FILES (metadata - content in files)
-- ============================================================
CREATE TABLE context_files (
    id              TEXT PRIMARY KEY,
    project_id      TEXT NOT NULL REFERENCES projects(id),
    filename        TEXT NOT NULL,              -- e.g., "claude.md"
    file_path       TEXT NOT NULL,              -- relative to project context dir
    sync_status     TEXT NOT NULL DEFAULT 'unknown',
                                                -- synced, stale, diverged, unknown
    last_sync_at    DATETIME,
    last_checked_at DATETIME,
    canonical_hash  TEXT,                       -- hash of Studio version
    repo_hash       TEXT,                       -- hash of Repo version (last check)
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_id, filename)
);

CREATE INDEX idx_context_files_project ON context_files(project_id);
CREATE INDEX idx_context_files_status ON context_files(sync_status);

-- ============================================================
-- DRIFT RECORDS
-- ============================================================
CREATE TABLE drift_records (
    id              TEXT PRIMARY KEY,
    context_file_id TEXT NOT NULL REFERENCES context_files(id),
    detected_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at     DATETIME,
    resolution      TEXT,                       -- accepted_repo, kept_studio, merged, dismissed
    canonical_content TEXT,                     -- snapshot at detection
    repo_content    TEXT,                       -- snapshot at detection
    diff_summary    TEXT                        -- e.g., "+4 lines, -2 lines"
);

CREATE INDEX idx_drift_context ON drift_records(context_file_id);
CREATE INDEX idx_drift_unresolved ON drift_records(resolved_at);

-- ============================================================
-- TECH STACK (per project)
-- ============================================================
CREATE TABLE tech_stack (
    id              TEXT PRIMARY KEY,
    project_id      TEXT NOT NULL REFERENCES projects(id),
    category        TEXT NOT NULL,              -- backend, frontend, database, deployment
    name            TEXT NOT NULL,              -- e.g., "FastAPI"
    version         TEXT,                       -- e.g., "3.11"
    sort_order      INTEGER NOT NULL DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_id, category, name)
);

CREATE INDEX idx_tech_stack_project ON tech_stack(project_id);
```

#### Registry Tables

```sql
-- ============================================================
-- REGISTRY: SKILLS
-- ============================================================
CREATE TABLE registry_skills (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    description     TEXT,
    file_path       TEXT NOT NULL,              -- relative to registry/skills/
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- REGISTRY: AGENTS
-- ============================================================
CREATE TABLE registry_agents (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    description     TEXT,
    file_path       TEXT NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- REGISTRY: TOOLS
-- ============================================================
CREATE TABLE registry_tools (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    description     TEXT,
    tool_type       TEXT,                       -- mcp, cli, api
    file_path       TEXT NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- REGISTRY: TEMPLATES
-- ============================================================
CREATE TABLE registry_templates (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    description     TEXT,
    template_type   TEXT,                       -- project, doc, cycle
    dir_path        TEXT NOT NULL,              -- directory in registry/templates/
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- REGISTRY: PROMPTS
-- ============================================================
CREATE TABLE registry_prompts (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    description     TEXT,
    file_path       TEXT NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- MAPPINGS: Tech Stack → Registry Items
-- ============================================================
CREATE TABLE tech_mappings (
    id              TEXT PRIMARY KEY,
    tech_stack_id   TEXT NOT NULL REFERENCES tech_stack(id) ON DELETE CASCADE,
    registry_type   TEXT NOT NULL,              -- skill, agent, tool
    registry_id     TEXT NOT NULL,              -- id in respective registry table
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(tech_stack_id, registry_type, registry_id)
);

CREATE INDEX idx_tech_mappings_stack ON tech_mappings(tech_stack_id);

-- ============================================================
-- DEPENDENCIES
-- ============================================================
CREATE TABLE dependencies (
    id              TEXT PRIMARY KEY,
    project_id      TEXT NOT NULL REFERENCES projects(id),
    name            TEXT NOT NULL,              -- e.g., "python", "node", "docker"
    required_version TEXT,                      -- e.g., ">= 3.11"
    detected_path   TEXT,                       -- e.g., "/usr/bin/python3"
    detected_version TEXT,                      -- e.g., "3.11.4"
    status          TEXT NOT NULL DEFAULT 'unknown',
                                                -- installed, not_installed, version_mismatch, unknown
    last_checked_at DATETIME,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_id, name)
);

CREATE INDEX idx_dependencies_project ON dependencies(project_id);
```

#### Activity & Settings

```sql
-- ============================================================
-- ACTIVITY LOG (for Recent Activity feed)
-- ============================================================
CREATE TABLE activity_log (
    id              TEXT PRIMARY KEY,
    project_id      TEXT REFERENCES projects(id),
    activity_type   TEXT NOT NULL,              -- session_captured, decision_recorded, 
                                                -- cycle_started, cycle_completed,
                                                -- drift_detected, drift_resolved,
                                                -- context_updated
    title           TEXT NOT NULL,
    reference_type  TEXT,                       -- session, decision, cycle, context_file, drift
    reference_id    TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activity_project ON activity_log(project_id);
CREATE INDEX idx_activity_created ON activity_log(created_at DESC);
CREATE INDEX idx_activity_type ON activity_log(activity_type);

-- ============================================================
-- USER SETTINGS
-- ============================================================
CREATE TABLE settings (
    key             TEXT PRIMARY KEY,
    value           TEXT NOT NULL,              -- JSON
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Default settings:
-- theme: "dark"
-- sidebar_collapsed: false
-- default_project_id: null
-- keyboard_shortcuts: {...}
```

---

### File Content Formats

#### Context Files (Markdown)

```markdown
# Claude Instructions

## Project Overview
Risk Workbench is a full-stack application for...

## Tech Stack
- Backend: FastAPI (Python 3.11)
- Frontend: React 18 + TypeScript
- Database: PostgreSQL 15

## Coding Standards
...
```

#### Session File (Markdown)

`~/.project-studio/projects/{project-id}/sessions/{session-id}.md`

```markdown
# Auth middleware implementation

**Date:** 2024-12-22 10:42 AM
**Duration:** 45 minutes
**Cycle:** Auth Flow (CYC-102)

## Summary
Implemented JWT validation middleware with refresh token rotation logic.

## Files Changed
- `src/auth/middleware.ts` (+45 -12)
- `src/config/schema.ts` (+8 -0)

## Decisions Made
- Use JWT for stateless authentication
- Set token expiration to 15 minutes

## Open Questions
- Should we support multiple concurrent sessions?
- Token revocation strategy for logout?

## Notes
Major changes to the JWT validation logic to support multi-tenant schemas.
```

#### Registry Skill (Markdown)

`~/.project-studio/registry/skills/python-api-skill.md`

```markdown
# Python API Skill

## Description
FastAPI development patterns including request validation, error handling, 
async operations, dependency injection, and OpenAPI documentation.

## Patterns

### Request Validation
Use Pydantic for all request/response validation:
```python
from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    email: str
    name: str
```

### Error Handling
...

## Tech Stack Compatibility
- FastAPI
- Python 3.11+
```

#### Registry Agent (JSON)

`~/.project-studio/registry/agents/backend-agent.json`

```json
{
  "name": "backend-agent",
  "description": "Specialized agent for backend API development",
  "model": "claude-3-5-sonnet",
  "system_prompt": "You are a backend development specialist...",
  "skills": ["python-api-skill", "sql-skill"],
  "tools": ["openapi-tool", "pytest-tool"],
  "constraints": {
    "max_file_changes": 10,
    "require_tests": true
  }
}
```

#### Registry Tool (JSON)

`~/.project-studio/registry/tools/openapi-tool.json`

```json
{
  "name": "openapi-tool",
  "description": "Generate and validate OpenAPI specifications",
  "tool_type": "cli",
  "command": "openapi-generator",
  "install_command": "npm install -g @openapitools/openapi-generator-cli",
  "version_check": "openapi-generator version"
}
```

---

### Key Queries

```sql
-- Dashboard: Drift alerts
SELECT cf.*, p.name as project_name
FROM context_files cf
JOIN projects p ON cf.project_id = p.id
WHERE cf.sync_status IN ('stale', 'diverged')
  AND p.archived_at IS NULL
ORDER BY cf.updated_at DESC;

-- Dashboard: Active cycles across projects
SELECT c.*, p.name as project_name
FROM cycles c
JOIN projects p ON c.project_id = p.id
WHERE c.completed_at IS NULL
  AND p.archived_at IS NULL
ORDER BY c.updated_at DESC;

-- Dashboard: Pending decisions
SELECT d.*, p.name as project_name, cy.name as cycle_name
FROM decisions d
JOIN projects p ON d.project_id = p.id
LEFT JOIN cycles cy ON d.cycle_id = cy.id
WHERE d.created_at > datetime('now', '-7 days')
ORDER BY d.created_at DESC;

-- Dashboard: Recent activity
SELECT * FROM activity_log
WHERE created_at > datetime('now', '-7 days')
ORDER BY created_at DESC
LIMIT 20;

-- Project view: Context files with status
SELECT * FROM context_files
WHERE project_id = ?
ORDER BY filename;

-- Cycle view: Tasks ordered
SELECT * FROM tasks
WHERE cycle_id = ?
ORDER BY sort_order, created_at;

-- Memory browser: Search sessions
SELECT s.*, p.name as project_name, c.name as cycle_name
FROM sessions s
JOIN projects p ON s.project_id = p.id
LEFT JOIN cycles c ON s.cycle_id = c.id
WHERE (s.title LIKE ? OR s.summary LIKE ?)
  AND (? IS NULL OR s.project_id = ?)
  AND (? IS NULL OR s.cycle_id = ?)
ORDER BY s.created_at DESC;

-- Memory browser: Search learnings
SELECT l.*, p.name as project_name, c.name as cycle_name
FROM learnings l
LEFT JOIN projects p ON l.project_id = p.id
LEFT JOIN cycles c ON l.cycle_id = c.id
WHERE (l.title LIKE ? OR l.problem LIKE ? OR l.solution LIKE ?)
  AND (? IS NULL OR l.project_id = ?)
  AND (? IS NULL OR l.tags LIKE ?)
ORDER BY l.created_at DESC;

-- Get all unique tags with counts
SELECT tag, COUNT(*) as count
FROM (
  SELECT json_each.value as tag
  FROM learnings, json_each(learnings.tags)
)
GROUP BY tag
ORDER BY count DESC;

-- Registry: Items by type with usage count
SELECT rs.*, COUNT(tm.id) as project_count
FROM registry_skills rs
LEFT JOIN tech_mappings tm ON tm.registry_type = 'skill' AND tm.registry_id = rs.id
GROUP BY rs.id
ORDER BY rs.name;
```


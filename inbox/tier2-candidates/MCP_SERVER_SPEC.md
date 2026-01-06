# Project Studio MCP Server — Implementation Spec

**Status:** Ready for Implementation  
**Priority:** High  
**Target:** Project Studio Phase 1  
**Date:** December 2024

---

## 1. Overview

### Purpose

An MCP (Model Context Protocol) server that exposes Project Studio data to Claude Code agents. Enables on-demand access to learnings, decisions, and project context without bloating static files.

### Why MCP

| Approach | Token Cost | User Effort | Freshness |
|----------|------------|-------------|-----------|
| MCP Tools | ~50 schema + results on-demand | Zero | Always current |
| claude.md injection | 500-5000+ always in context | Manual updates | Stale quickly |
| Manual copy/paste | Variable | High | Point-in-time |

MCP is optimal because:
- **On-demand** — Agent queries only when needed
- **Searchable** — Filter by tags, project, text
- **Cross-project** — Works from any repo
- **Automated** — No manual intervention
- **Token-efficient** — Results only when called

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      PROJECT STUDIO                              │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Learnings  │  │   Sessions   │  │  Decisions   │          │
│  │   (SQLite)   │  │   (SQLite)   │  │  (SQLite)    │          │
│  └──────────────┴──┴──────────────┴──┴──────────────┘          │
│                            │                                    │
│                    studio.db                                    │
│                            │                                    │
│              ┌─────────────▼─────────────┐                     │
│              │     MCP Server (stdio)    │                     │
│              │                           │                     │
│              │  Tools:                   │                     │
│              │  • query_learnings        │                     │
│              │  • get_learning           │                     │
│              │  • list_tags              │                     │
│              │  • get_project_context    │                     │
│              └─────────────┬─────────────┘                     │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             │ stdio (JSON-RPC)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CLAUDE CODE                               │
│                                                                 │
│  Agent: "I'm hitting a Railway deployment issue..."            │
│         → calls studio:query_learnings(tags: ["railway"])      │
│         → receives relevant learnings                          │
│         → applies solution                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Project Structure

```
project-studio/
├── src/                          # Electron app (existing)
├── electron/                     # Main process (existing)
├── mcp-server/                   # NEW: MCP server package
│   ├── src/
│   │   ├── index.ts              # Entry point
│   │   ├── server.ts             # MCP server setup
│   │   ├── db.ts                 # Database connection
│   │   └── tools/
│   │       ├── index.ts          # Tool registry
│   │       ├── queryLearnings.ts
│   │       ├── getLearning.ts
│   │       ├── listTags.ts
│   │       └── getProjectContext.ts
│   ├── package.json              # Separate package
│   ├── tsconfig.json
│   └── README.md
├── package.json                  # Root package (workspaces)
└── ...
```

### Package Configuration

**Root `package.json`** (add workspaces):

```json
{
  "name": "project-studio",
  "private": true,
  "workspaces": [
    ".",
    "mcp-server"
  ]
}
```

**`mcp-server/package.json`**:

```json
{
  "name": "project-studio-mcp",
  "version": "0.1.0",
  "description": "MCP server for Project Studio - exposes learnings and context to Claude Code",
  "main": "dist/index.js",
  "bin": {
    "project-studio-mcp": "./dist/index.js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.6.0",
    "better-sqlite3": "^9.4.3"
  },
  "devDependencies": {
    "@types/better-sqlite3": "^7.6.9",
    "@types/node": "^20.11.0",
    "typescript": "^5.3.3"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "files": [
    "dist"
  ]
}
```

**`mcp-server/tsconfig.json`**:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## 3. Database Connection

**`mcp-server/src/db.ts`**:

```typescript
import Database from 'better-sqlite3'
import path from 'path'
import os from 'os'
import fs from 'fs'

let db: Database.Database | null = null

/**
 * Get the path to Project Studio's database
 */
function getDbPath(): string {
  // Check environment variable first (for custom locations)
  if (process.env.STUDIO_DB_PATH) {
    return process.env.STUDIO_DB_PATH.replace('~', os.homedir())
  }

  // Default locations by platform
  const platform = process.platform
  let basePath: string

  if (platform === 'darwin') {
    // macOS: ~/Library/Application Support/project-studio
    basePath = path.join(os.homedir(), 'Library', 'Application Support', 'project-studio')
  } else if (platform === 'win32') {
    // Windows: %APPDATA%/project-studio
    basePath = path.join(process.env.APPDATA || os.homedir(), 'project-studio')
  } else {
    // Linux: ~/.config/project-studio
    basePath = path.join(os.homedir(), '.config', 'project-studio')
  }

  return path.join(basePath, 'studio.db')
}

/**
 * Initialize database connection (read-only)
 */
export function initDb(): Database.Database {
  if (db) return db

  const dbPath = getDbPath()

  if (!fs.existsSync(dbPath)) {
    throw new Error(
      `Project Studio database not found at: ${dbPath}\n` +
      `Make sure Project Studio is installed and has been run at least once.\n` +
      `You can also set STUDIO_DB_PATH environment variable to a custom location.`
    )
  }

  db = new Database(dbPath, { readonly: true })
  return db
}

/**
 * Get database instance
 */
export function getDb(): Database.Database {
  if (!db) {
    return initDb()
  }
  return db
}

/**
 * Close database connection
 */
export function closeDb(): void {
  if (db) {
    db.close()
    db = null
  }
}
```

---

## 4. MCP Server Setup

**`mcp-server/src/server.ts`**:

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ErrorCode,
  McpError,
} from '@modelcontextprotocol/sdk/types.js'

import { initDb, closeDb } from './db.js'
import { tools, executeTool } from './tools/index.js'

export async function createServer(): Promise<Server> {
  // Initialize database
  try {
    initDb()
  } catch (error) {
    console.error('Failed to initialize database:', error)
    process.exit(1)
  }

  const server = new Server(
    {
      name: 'project-studio',
      version: '0.1.0',
    },
    {
      capabilities: {
        tools: {},
      },
    }
  )

  // Handle tool listing
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools }
  })

  // Handle tool execution
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params

    try {
      const result = await executeTool(name, args || {})
      return {
        content: [
          {
            type: 'text',
            text: typeof result === 'string' ? result : JSON.stringify(result, null, 2),
          },
        ],
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error'
      throw new McpError(ErrorCode.InternalError, message)
    }
  })

  // Cleanup on exit
  process.on('SIGINT', () => {
    closeDb()
    process.exit(0)
  })

  process.on('SIGTERM', () => {
    closeDb()
    process.exit(0)
  })

  return server
}

export async function runServer(): Promise<void> {
  const server = await createServer()
  const transport = new StdioServerTransport()
  await server.connect(transport)
  
  // Log to stderr (stdout is for MCP protocol)
  console.error('Project Studio MCP server started')
}
```

**`mcp-server/src/index.ts`**:

```typescript
#!/usr/bin/env node

import { runServer } from './server.js'

runServer().catch((error) => {
  console.error('Fatal error:', error)
  process.exit(1)
})
```

---

## 5. Tool Definitions

**`mcp-server/src/tools/index.ts`**:

```typescript
import { Tool } from '@modelcontextprotocol/sdk/types.js'

import { queryLearnings, queryLearningsSchema } from './queryLearnings.js'
import { getLearning, getLearningSchema } from './getLearning.js'
import { listTags, listTagsSchema } from './listTags.js'
import { getProjectContext, getProjectContextSchema } from './getProjectContext.js'

// Tool definitions for MCP
export const tools: Tool[] = [
  {
    name: 'query_learnings',
    description: 
      'Search learnings from Project Studio. Use this when you encounter a problem ' +
      'or need guidance on a specific technology, pattern, or gotcha. ' +
      'Learnings contain solutions to problems previously encountered.',
    inputSchema: queryLearningsSchema,
  },
  {
    name: 'get_learning',
    description: 
      'Get the full details of a specific learning by ID. ' +
      'Use after query_learnings to get complete problem/solution details.',
    inputSchema: getLearningSchema,
  },
  {
    name: 'list_tags',
    description: 
      'List all available tags used in learnings. ' +
      'Use to discover what categories of learnings are available.',
    inputSchema: listTagsSchema,
  },
  {
    name: 'get_project_context',
    description: 
      'Get context for a Project Studio project including tech stack, ' +
      'active priorities, and constraints. Use at session start or when ' +
      'you need to understand project-specific rules.',
    inputSchema: getProjectContextSchema,
  },
]

// Tool executor
type ToolExecutor = (args: Record<string, unknown>) => Promise<unknown>

const executors: Record<string, ToolExecutor> = {
  query_learnings: queryLearnings,
  get_learning: getLearning,
  list_tags: listTags,
  get_project_context: getProjectContext,
}

export async function executeTool(
  name: string, 
  args: Record<string, unknown>
): Promise<unknown> {
  const executor = executors[name]
  if (!executor) {
    throw new Error(`Unknown tool: ${name}`)
  }
  return executor(args)
}
```

---

## 6. Tool Implementations

### query_learnings

**`mcp-server/src/tools/queryLearnings.ts`**:

```typescript
import { getDb } from '../db.js'

export const queryLearningsSchema = {
  type: 'object' as const,
  properties: {
    tags: {
      type: 'array',
      items: { type: 'string' },
      description: 'Filter by tags (e.g., ["railway", "deployment"]). Returns learnings matching ANY tag.',
    },
    project_id: {
      type: 'string',
      description: 'Filter by project ID. Omit to search across all projects.',
    },
    search: {
      type: 'string',
      description: 'Free text search across title, problem, and solution fields.',
    },
    limit: {
      type: 'number',
      description: 'Maximum number of results (default: 10, max: 50)',
    },
  },
}

interface QueryLearningsArgs {
  tags?: string[]
  project_id?: string
  search?: string
  limit?: number
}

interface LearningResult {
  id: string
  title: string
  problem: string
  solution: string
  tags: string[]
  project_id?: string
  project_name?: string
  created_at: string
}

export async function queryLearnings(args: QueryLearningsArgs): Promise<LearningResult[]> {
  const db = getDb()
  const limit = Math.min(args.limit || 10, 50)
  
  let query = `
    SELECT 
      l.id,
      l.title,
      l.problem,
      l.solution,
      l.tags,
      l.project_id,
      p.name as project_name,
      l.created_at
    FROM learnings l
    LEFT JOIN projects p ON l.project_id = p.id
    WHERE 1=1
  `
  const params: unknown[] = []

  // Filter by project
  if (args.project_id) {
    query += ` AND l.project_id = ?`
    params.push(args.project_id)
  }

  // Filter by tags (match ANY tag)
  if (args.tags && args.tags.length > 0) {
    const tagConditions = args.tags.map(() => `l.tags LIKE ?`).join(' OR ')
    query += ` AND (${tagConditions})`
    for (const tag of args.tags) {
      params.push(`%${tag}%`)
    }
  }

  // Free text search
  if (args.search) {
    query += ` AND (l.title LIKE ? OR l.problem LIKE ? OR l.solution LIKE ?)`
    const searchTerm = `%${args.search}%`
    params.push(searchTerm, searchTerm, searchTerm)
  }

  query += ` ORDER BY l.created_at DESC LIMIT ?`
  params.push(limit)

  const rows = db.prepare(query).all(...params) as Array<{
    id: string
    title: string
    problem: string
    solution: string
    tags: string
    project_id: string | null
    project_name: string | null
    created_at: string
  }>

  return rows.map(row => ({
    id: row.id,
    title: row.title,
    problem: row.problem,
    solution: row.solution,
    tags: JSON.parse(row.tags || '[]'),
    project_id: row.project_id || undefined,
    project_name: row.project_name || undefined,
    created_at: row.created_at,
  }))
}
```

### get_learning

**`mcp-server/src/tools/getLearning.ts`**:

```typescript
import { getDb } from '../db.js'

export const getLearningSchema = {
  type: 'object' as const,
  properties: {
    id: {
      type: 'string',
      description: 'The learning ID (e.g., "L-023")',
    },
  },
  required: ['id'],
}

interface GetLearningArgs {
  id: string
}

interface LearningDetail {
  id: string
  title: string
  problem: string
  solution: string
  tags: string[]
  project_id?: string
  project_name?: string
  cycle_id?: string
  cycle_name?: string
  session_id?: string
  created_at: string
  updated_at: string
}

export async function getLearning(args: GetLearningArgs): Promise<LearningDetail | null> {
  const db = getDb()
  
  const row = db.prepare(`
    SELECT 
      l.id,
      l.title,
      l.problem,
      l.solution,
      l.tags,
      l.project_id,
      p.name as project_name,
      l.cycle_id,
      c.name as cycle_name,
      l.session_id,
      l.created_at,
      l.updated_at
    FROM learnings l
    LEFT JOIN projects p ON l.project_id = p.id
    LEFT JOIN cycles c ON l.cycle_id = c.id
    WHERE l.id = ?
  `).get(args.id) as {
    id: string
    title: string
    problem: string
    solution: string
    tags: string
    project_id: string | null
    project_name: string | null
    cycle_id: string | null
    cycle_name: string | null
    session_id: string | null
    created_at: string
    updated_at: string
  } | undefined

  if (!row) {
    return null
  }

  return {
    id: row.id,
    title: row.title,
    problem: row.problem,
    solution: row.solution,
    tags: JSON.parse(row.tags || '[]'),
    project_id: row.project_id || undefined,
    project_name: row.project_name || undefined,
    cycle_id: row.cycle_id || undefined,
    cycle_name: row.cycle_name || undefined,
    session_id: row.session_id || undefined,
    created_at: row.created_at,
    updated_at: row.updated_at,
  }
}
```

### list_tags

**`mcp-server/src/tools/listTags.ts`**:

```typescript
import { getDb } from '../db.js'

export const listTagsSchema = {
  type: 'object' as const,
  properties: {
    project_id: {
      type: 'string',
      description: 'Filter tags by project. Omit to get tags across all projects.',
    },
  },
}

interface ListTagsArgs {
  project_id?: string
}

interface TagCount {
  tag: string
  count: number
}

export async function listTags(args: ListTagsArgs): Promise<TagCount[]> {
  const db = getDb()
  
  // Get all learnings (optionally filtered by project)
  let query = `SELECT tags FROM learnings WHERE 1=1`
  const params: unknown[] = []

  if (args.project_id) {
    query += ` AND project_id = ?`
    params.push(args.project_id)
  }

  const rows = db.prepare(query).all(...params) as Array<{ tags: string }>

  // Count tag occurrences
  const tagCounts = new Map<string, number>()
  
  for (const row of rows) {
    const tags = JSON.parse(row.tags || '[]') as string[]
    for (const tag of tags) {
      tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1)
    }
  }

  // Sort by count (descending)
  const result: TagCount[] = Array.from(tagCounts.entries())
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count)

  return result
}
```

### get_project_context

**`mcp-server/src/tools/getProjectContext.ts`**:

```typescript
import { getDb } from '../db.js'

export const getProjectContextSchema = {
  type: 'object' as const,
  properties: {
    project_id: {
      type: 'string',
      description: 'The project ID',
    },
    repo_path: {
      type: 'string',
      description: 'The repository path. Use if you don\'t know the project ID.',
    },
  },
}

interface GetProjectContextArgs {
  project_id?: string
  repo_path?: string
}

interface ProjectContext {
  project: {
    id: string
    name: string
    description?: string
    repo_path?: string
    tech_stack?: Record<string, string>
    status: string
  }
  active_cycle?: {
    id: string
    name: string
    intent?: string
    status: string
  }
  recent_learnings: Array<{
    id: string
    title: string
    tags: string[]
  }>
  recent_decisions: Array<{
    id: string
    title: string
    decision?: string
  }>
}

export async function getProjectContext(args: GetProjectContextArgs): Promise<ProjectContext | null> {
  const db = getDb()

  // Find project
  let project: {
    id: string
    name: string
    description: string | null
    repo_path: string | null
    tech_stack: string | null
    status: string
  } | undefined

  if (args.project_id) {
    project = db.prepare(`
      SELECT id, name, description, repo_path, tech_stack, status
      FROM projects WHERE id = ?
    `).get(args.project_id) as typeof project
  } else if (args.repo_path) {
    project = db.prepare(`
      SELECT id, name, description, repo_path, tech_stack, status
      FROM projects WHERE repo_path = ? OR repo_path LIKE ?
    `).get(args.repo_path, `%${args.repo_path}%`) as typeof project
  }

  if (!project) {
    return null
  }

  // Get active cycle
  const activeCycle = db.prepare(`
    SELECT id, name, intent, status
    FROM cycles
    WHERE project_id = ? AND status IN ('active', 'in_progress')
    ORDER BY created_at DESC
    LIMIT 1
  `).get(project.id) as {
    id: string
    name: string
    intent: string | null
    status: string
  } | undefined

  // Get recent learnings for this project
  const recentLearnings = db.prepare(`
    SELECT id, title, tags
    FROM learnings
    WHERE project_id = ?
    ORDER BY created_at DESC
    LIMIT 5
  `).all(project.id) as Array<{
    id: string
    title: string
    tags: string
  }>

  // Get recent decisions for this project
  const recentDecisions = db.prepare(`
    SELECT id, title, decision
    FROM decisions
    WHERE project_id = ?
    ORDER BY created_at DESC
    LIMIT 5
  `).all(project.id) as Array<{
    id: string
    title: string
    decision: string | null
  }>

  return {
    project: {
      id: project.id,
      name: project.name,
      description: project.description || undefined,
      repo_path: project.repo_path || undefined,
      tech_stack: project.tech_stack ? JSON.parse(project.tech_stack) : undefined,
      status: project.status,
    },
    active_cycle: activeCycle ? {
      id: activeCycle.id,
      name: activeCycle.name,
      intent: activeCycle.intent || undefined,
      status: activeCycle.status,
    } : undefined,
    recent_learnings: recentLearnings.map(l => ({
      id: l.id,
      title: l.title,
      tags: JSON.parse(l.tags || '[]'),
    })),
    recent_decisions: recentDecisions.map(d => ({
      id: d.id,
      title: d.title,
      decision: d.decision || undefined,
    })),
  }
}
```

---

## 7. Claude Code Configuration

### User Setup

Users configure the MCP server in Claude Code's settings.

**Location:** `~/.claude/mcp_servers.json` (or Claude Code's config location)

```json
{
  "mcpServers": {
    "project-studio": {
      "command": "npx",
      "args": ["project-studio-mcp"],
      "env": {}
    }
  }
}
```

**Alternative (if installed globally):**

```json
{
  "mcpServers": {
    "project-studio": {
      "command": "project-studio-mcp",
      "env": {}
    }
  }
}
```

**With custom database path:**

```json
{
  "mcpServers": {
    "project-studio": {
      "command": "npx",
      "args": ["project-studio-mcp"],
      "env": {
        "STUDIO_DB_PATH": "/custom/path/to/studio.db"
      }
    }
  }
}
```

### Verification

After configuration, verify in Claude Code:

```
> /mcp

Available MCP servers:
- project-studio (connected)
  Tools: query_learnings, get_learning, list_tags, get_project_context
```

---

## 8. Usage Examples

### Example 1: Query Learnings by Tag

Agent encounters a Railway deployment issue:

```
Agent: I'm getting a build error on Railway. Let me check for learnings.

Tool call: query_learnings({ tags: ["railway", "deployment"] })

Response:
[
  {
    "id": "L-023",
    "title": "Railway env vars need NIXPACKS_ prefix",
    "problem": "Build-time env vars not accessible during build",
    "solution": "Prefix environment variables with NIXPACKS_ for build-time access",
    "tags": ["railway", "deployment", "env-vars"],
    "created_at": "2024-12-20T10:30:00Z"
  },
  {
    "id": "L-041",
    "title": "Railway health check required",
    "problem": "Deployment fails without health endpoint",
    "solution": "Add /health endpoint returning 200 OK",
    "tags": ["railway", "deployment", "health-check"],
    "created_at": "2024-12-22T14:15:00Z"
  }
]

Agent: I see I need to add NIXPACKS_ prefix. Let me check the env vars...
```

### Example 2: Free Text Search

Agent debugging a Pydantic issue:

```
Tool call: query_learnings({ search: "pydantic validation" })

Response:
[
  {
    "id": "L-015",
    "title": "Use Pydantic v2 syntax",
    "problem": "model.parse_obj() not working",
    "solution": "Pydantic v2 uses model_validate() instead of parse_obj()",
    "tags": ["python", "pydantic", "fastapi"],
    "created_at": "2024-12-18T09:00:00Z"
  }
]
```

### Example 3: Get Project Context

Agent starting a new session:

```
Tool call: get_project_context({ repo_path: "/Users/jess/code/risk-workbench" })

Response:
{
  "project": {
    "id": "proj-001",
    "name": "Risk Workbench",
    "tech_stack": {
      "backend": "FastAPI",
      "frontend": "React",
      "database": "PostgreSQL",
      "deploy": "Railway"
    },
    "status": "active"
  },
  "active_cycle": {
    "id": "cycle-042",
    "name": "API Error Handling",
    "intent": "Add consistent error handling middleware to all API endpoints",
    "status": "in_progress"
  },
  "recent_learnings": [
    { "id": "L-023", "title": "Railway env vars need NIXPACKS_ prefix", "tags": ["railway"] },
    { "id": "L-015", "title": "Use Pydantic v2 syntax", "tags": ["pydantic"] }
  ],
  "recent_decisions": [
    { "id": "D-008", "title": "JWT over session cookies", "decision": "Use JWT for stateless auth" }
  ]
}

Agent: I'm working on the API Error Handling cycle. Let me focus on the middleware...
```

### Example 4: Discover Available Tags

Agent wants to see what learnings exist:

```
Tool call: list_tags({})

Response:
[
  { "tag": "fastapi", "count": 12 },
  { "tag": "railway", "count": 8 },
  { "tag": "react", "count": 7 },
  { "tag": "deployment", "count": 6 },
  { "tag": "pydantic", "count": 5 },
  { "tag": "auth", "count": 4 },
  { "tag": "postgresql", "count": 3 }
]

Agent: There are 8 Railway learnings. Let me query those before deploying...
```

---

## 9. Build & Distribution

### Build Commands

```bash
# From project root
cd mcp-server
npm install
npm run build

# Test locally
node dist/index.js
```

### Local Development

For development, link the package locally:

```bash
cd mcp-server
npm link

# Now "project-studio-mcp" is available as a command
project-studio-mcp
```

### Publishing (Future)

When ready to publish:

```bash
cd mcp-server
npm publish
```

Users can then install globally:

```bash
npm install -g project-studio-mcp
```

Or use via npx (no install required):

```bash
npx project-studio-mcp
```

---

## 10. Error Handling

### Database Not Found

```typescript
// In db.ts
if (!fs.existsSync(dbPath)) {
  throw new Error(
    `Project Studio database not found at: ${dbPath}\n` +
    `Make sure Project Studio is installed and has been run at least once.\n` +
    `You can also set STUDIO_DB_PATH environment variable to a custom location.`
  )
}
```

### Tool Errors

```typescript
// In server.ts
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const result = await executeTool(name, args || {})
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] }
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error'
    
    // Log to stderr for debugging
    console.error(`Tool error [${name}]:`, error)
    
    throw new McpError(ErrorCode.InternalError, message)
  }
})
```

### Graceful Degradation

If a query returns no results, return helpful context:

```typescript
// In queryLearnings.ts
if (rows.length === 0) {
  return {
    results: [],
    message: args.tags 
      ? `No learnings found with tags: ${args.tags.join(', ')}. Try list_tags to see available tags.`
      : args.search
        ? `No learnings found matching "${args.search}".`
        : 'No learnings found.',
  }
}
```

---

## 11. Testing

### Manual Testing

```bash
# Start the server manually (will read from stdin, write to stdout)
cd mcp-server
node dist/index.js

# Send a JSON-RPC request (in another terminal, or pipe in)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | node dist/index.js
```

### Test Script

**`mcp-server/test/manual-test.ts`**:

```typescript
import { createServer } from '../src/server.js'
import { queryLearnings } from '../src/tools/queryLearnings.js'
import { listTags } from '../src/tools/listTags.js'
import { initDb } from '../src/db.js'

async function test() {
  console.log('Initializing database...')
  initDb()

  console.log('\n--- Testing list_tags ---')
  const tags = await listTags({})
  console.log('Tags:', tags)

  console.log('\n--- Testing query_learnings (all) ---')
  const allLearnings = await queryLearnings({ limit: 5 })
  console.log('Learnings:', allLearnings)

  console.log('\n--- Testing query_learnings (by tag) ---')
  const taggedLearnings = await queryLearnings({ tags: ['railway'] })
  console.log('Railway learnings:', taggedLearnings)

  console.log('\n--- Testing query_learnings (search) ---')
  const searchResults = await queryLearnings({ search: 'env' })
  console.log('Search results:', searchResults)

  console.log('\nAll tests passed!')
}

test().catch(console.error)
```

### Testing Checklist

- [ ] Server starts without errors
- [ ] Database connection works (read-only)
- [ ] `query_learnings` returns results
- [ ] `query_learnings` filters by tags
- [ ] `query_learnings` filters by project_id
- [ ] `query_learnings` searches text
- [ ] `get_learning` returns full details
- [ ] `get_learning` returns null for unknown ID
- [ ] `list_tags` returns tag counts
- [ ] `get_project_context` returns project details
- [ ] `get_project_context` finds by repo_path
- [ ] Error handling works (missing DB, invalid queries)
- [ ] Claude Code can connect to server
- [ ] Tools appear in Claude Code `/mcp` list
- [ ] Tool calls work from Claude Code

---

## 12. Files Summary

| File | Description |
|------|-------------|
| `mcp-server/package.json` | Package configuration |
| `mcp-server/tsconfig.json` | TypeScript configuration |
| `mcp-server/src/index.ts` | Entry point (shebang for CLI) |
| `mcp-server/src/server.ts` | MCP server setup |
| `mcp-server/src/db.ts` | Database connection |
| `mcp-server/src/tools/index.ts` | Tool registry and executor |
| `mcp-server/src/tools/queryLearnings.ts` | Search learnings tool |
| `mcp-server/src/tools/getLearning.ts` | Get learning detail tool |
| `mcp-server/src/tools/listTags.ts` | List tags tool |
| `mcp-server/src/tools/getProjectContext.ts` | Get project context tool |

---

## 13. Phase 2 Enhancements

Not in this spec, but planned:

| Tool | Purpose |
|------|---------|
| `capture_learning` | Agent writes a learning back to Studio |
| `capture_decision` | Agent records a decision |
| `get_cycle_intent` | Get current cycle's full intent and constraints |
| `update_state` | Agent updates project state (bidirectional) |
| `query_observations` | Search claude-mem observations via Studio |

---

## 14. Integration with Other Specs

This MCP server integrates with:

**LEARNINGS_IMPLEMENTATION_SPEC.md**
- Reads from `learnings` table
- Exposes learnings to agents

**CONTEXT_HYGIENE_SPEC.md**
- `get_project_context` provides what would otherwise bloat claude.md
- Enables lean static files + rich on-demand context

**CLAUDE_MEM_INTEGRATION_SPEC.md**
- Future: Could expose claude-mem observations through Studio MCP
- Unified interface for all memory/context queries

---

*End of Specification*

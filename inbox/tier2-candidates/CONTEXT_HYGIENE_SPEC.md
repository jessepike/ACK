# Context Hygiene System — Implementation Spec

**Status:** Ready for Implementation  
**Priority:** High  
**Target:** Project Studio Phase 1  
**Date:** December 2024

---

## 1. Overview

### Problem

Claude Code agents add to claude.md but never clean up. Over time:
- Content becomes stale (references completed work)
- Duplicates accumulate (same info stated multiple ways)
- Signal drowns in noise (500+ token files that should be <300)
- No visibility into what changed or when

### Solution

A layered hygiene system:
1. **Change Detection** — Watch claude.md, flag every change in Studio
2. **Change Logging** — CHANGELOG.md in repo + UI to browse
3. **Section Ownership** — Clear boundaries: human vs agent vs auto sections
4. **Optimization Pass** — LLM-assisted periodic cleanup

### Goals

- claude.md stays lean (<500 tokens target)
- Every change is visible and logged
- Stale content is identified and removed
- You maintain awareness without manual effort

---

## 2. CHANGELOG.md Pattern

### Constitution Addition

Add to the base constitution template. This instructs agents to log their changes.

**File:** `templates/constitution/base.md`

Add this section:

```markdown
## Change Logging

When you modify any Studio-managed file (claude.md, architecture.md, data-model.md), you MUST append an entry to CHANGELOG.md in the project root.

### Format

\`\`\`markdown
## [YYYY-MM-DD HH:MM] <file> | <session/cycle>

### Changed
- <section>: <what changed>

### Added
- <section>: <what was added>

### Removed
- <section>: <what was removed>

### Why
<brief rationale - 1-2 sentences>
\`\`\`

### Example

\`\`\`markdown
## [2024-12-28 14:32] claude.md | AUTH-001

### Changed
- Current State: Auth flow 60% → 80% complete

### Added
- Gotchas: "JWT refresh requires httpOnly cookie"

### Why
Completed refresh token implementation. Discovered cookie requirement during testing.
\`\`\`

### Rules

1. One entry per file modified (if you change multiple files, multiple entries)
2. Keep entries concise — this is a log, not documentation
3. Always include "Why" — future you needs context
4. If CHANGELOG.md doesn't exist, create it with a header:

\`\`\`markdown
# Project Changelog

Changes to Studio-managed files (claude.md, architecture.md, etc.)

---
\`\`\`
```

### CHANGELOG.md Template

**File:** `templates/files/CHANGELOG.md`

```markdown
# Project Changelog

Changes to Studio-managed files (claude.md, architecture.md, data-model.md).

This file is maintained by Claude Code agents and Project Studio.

---

<!-- Entries are prepended below this line -->
```

---

## 3. claude.md Template with Section Ownership

### Section Types

| Type | Marker | Who Updates | How Updated |
|------|--------|-------------|-------------|
| **HUMAN** | `<!-- HUMAN -->` | You only | Edit in Studio, push to repo |
| **AGENT** | `<!-- AGENT -->` | Claude Code | Agent writes during sessions |
| **AUTO** | `<!-- AUTO -->` | Project Studio | Learnings, optimizations, injections |
| **EPHEMERAL** | `<!-- EPHEMERAL -->` | Project Studio | Injected at session start, cleared after |

### Base Template

**File:** `templates/claude-md/base.md`

```markdown
# {{PROJECT_NAME}}

<!--
  STUDIO MANAGED FILE
  
  Section Ownership:
  - HUMAN: Only you edit these sections (via Studio)
  - AGENT: Claude Code updates during sessions
  - AUTO: Project Studio maintains automatically
  - EPHEMERAL: Injected per-session, auto-cleared
  
  Target size: <500 tokens
  Last optimized: {{LAST_OPTIMIZED}}
-->

## Intent
<!-- HUMAN: What are we building? Why does it matter? Keep to 2-3 sentences. -->
{{INTENT_PLACEHOLDER}}

## Tech Stack
<!-- HUMAN: Core technologies. Rarely changes after init. -->
- Backend: {{BACKEND}}
- Frontend: {{FRONTEND}}
- Database: {{DATABASE}}
- Deploy: {{DEPLOY}}

## Active Priorities
<!-- HUMAN: What matters NOW. Max 3-5 items. Update per cycle. -->
1. {{PRIORITY_1}}
2. {{PRIORITY_2}}
3. {{PRIORITY_3}}

## Constraints
<!-- HUMAN: Hard rules. Things agent must NOT do. -->
- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}

## Current State
<!-- AGENT: Brief status of major components. AUTO-CLEANED periodically. -->
- {{COMPONENT_1}}: {{STATUS_1}}
- {{COMPONENT_2}}: {{STATUS_2}}

## Gotchas
<!-- AUTO: Populated from learnings. Keep only what's actively relevant. -->
<!-- Format: "- <gotcha> (added: YYYY-MM-DD)" -->

## Session Context
<!-- EPHEMERAL: Injected at session start. Cleared after session. -->
<!-- DO NOT EDIT MANUALLY -->
```

### Tech-Stack Layers

These get appended to base.md during project initialization.

**File:** `templates/claude-md/layer-fastapi.md`

```markdown
## FastAPI Patterns
<!-- AUTO: Standard patterns for this stack. -->
- Use Pydantic v2 syntax (model_validate, not parse_obj)
- Async endpoints for I/O operations
- Dependency injection for DB sessions
- HTTPException for error responses
```

**File:** `templates/claude-md/layer-react.md`

```markdown
## React Patterns
<!-- AUTO: Standard patterns for this stack. -->
- Functional components only
- Use React Query for server state
- Zustand for client state
- Tailwind for styling (no CSS modules)
```

**File:** `templates/claude-md/layer-railway.md`

```markdown
## Railway Deployment
<!-- AUTO: Railway-specific gotchas. -->
- Env vars need NIXPACKS_ prefix for build-time access
- Use Railway's internal networking for service-to-service
- Health check endpoint required at /health
```

### Assembled Example

For a FastAPI + React + Railway project:

```markdown
# Risk Workbench

<!--
  STUDIO MANAGED FILE
  
  Section Ownership:
  - HUMAN: Only you edit these sections (via Studio)
  - AGENT: Claude Code updates during sessions
  - AUTO: Project Studio maintains automatically
  - EPHEMERAL: Injected per-session, auto-cleared
  
  Target size: <500 tokens
  Last optimized: 2024-12-28
-->

## Intent
<!-- HUMAN: What are we building? Why does it matter? Keep to 2-3 sentences. -->
Risk assessment tool for financial portfolios. Enables analysts to evaluate 
position risk across multiple asset classes.

## Tech Stack
<!-- HUMAN: Core technologies. Rarely changes after init. -->
- Backend: FastAPI + PostgreSQL
- Frontend: React + Tailwind
- Database: PostgreSQL
- Deploy: Railway

## Active Priorities
<!-- HUMAN: What matters NOW. Max 3-5 items. Update per cycle. -->
1. Complete auth flow (JWT + refresh)
2. API error handling middleware
3. DO NOT touch deployment config

## Constraints
<!-- HUMAN: Hard rules. Things agent must NOT do. -->
- No new dependencies without approval
- No breaking changes to API v1
- Stay within /src directory

## Current State
<!-- AGENT: Brief status of major components. AUTO-CLEANED periodically. -->
- Auth: Complete (JWT + refresh tokens)
- API: v1 stable, v2 in progress (3/8 endpoints)
- Frontend: Component library integrated

## Gotchas
<!-- AUTO: Populated from learnings. Keep only what's actively relevant. -->
- Railway env vars need NIXPACKS_ prefix (added: 2024-12-20)
- React Query v5 changed useQuery API (added: 2024-12-22)

## FastAPI Patterns
<!-- AUTO: Standard patterns for this stack. -->
- Use Pydantic v2 syntax (model_validate, not parse_obj)
- Async endpoints for I/O operations
- Dependency injection for DB sessions

## React Patterns
<!-- AUTO: Standard patterns for this stack. -->
- Functional components only
- Use React Query for server state
- Zustand for client state

## Railway Deployment
<!-- AUTO: Railway-specific gotchas. -->
- Env vars need NIXPACKS_ prefix for build-time access
- Health check endpoint required at /health

## Session Context
<!-- EPHEMERAL: Injected at session start. Cleared after session. -->
- Cycle: API-002 - Error handling middleware
- Focus: /src/api/middleware.py, /src/api/errors.py
- Recent learnings: FastAPI exception handlers (L-047)
```

---

## 4. Data Model

### ContextChange Entity

Add to `src/types/index.ts`:

```typescript
// ============================================================
// Context Hygiene System
// ============================================================

export type ContextFileType = 
  | 'claude.md' 
  | 'constitution.md' 
  | 'architecture.md' 
  | 'data-model.md' 
  | 'CHANGELOG.md'
  | string  // Allow custom files

export type ChangeSource = 
  | 'agent'      // Claude Code made this change
  | 'auto'       // Studio made this change (learning injection, optimization)
  | 'manual'     // Human made this change in Studio
  | 'optimize'   // Optimization pass made this change

export type ChangeAction = 'add' | 'update' | 'delete' | 'consolidate'

export interface ContextChange {
  id: string
  project_id: string
  file: ContextFileType
  section?: string                    // "Current State", "Gotchas", etc.
  source: ChangeSource
  action: ChangeAction
  before: string                      // Previous content (for diff)
  after: string                       // New content (for diff)
  reason?: string                     // Why this change was made
  source_reference?: {                // What triggered this change
    type: 'learning' | 'session' | 'observation' | 'optimization' | 'human'
    id?: string
    label?: string                    // "Learning #L-047", "Session AUTH-001"
  }
  tokens_before?: number              // Token count before change
  tokens_after?: number               // Token count after change
  created_at: string
}

export interface ContextFileState {
  project_id: string
  file: ContextFileType
  content_hash: string                // For detecting changes
  token_count: number
  last_modified: string
  last_optimized?: string
  health: 'healthy' | 'warning' | 'alert'  // Based on token count
}

export interface OptimizationSuggestion {
  id: string
  project_id: string
  file: ContextFileType
  section: string
  suggestion_type: 'remove' | 'consolidate' | 'verify' | 'archive'
  before: string
  after: string
  reason: string
  confidence: 'high' | 'medium' | 'low'
  status: 'pending' | 'accepted' | 'rejected' | 'deferred'
  created_at: string
  resolved_at?: string
}
```

### Database Schema

Add to `electron/ipc/index.ts` migrations:

```typescript
// Context Changes table
db.exec(`
  CREATE TABLE IF NOT EXISTS context_changes (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    file TEXT NOT NULL,
    section TEXT,
    source TEXT NOT NULL,
    action TEXT NOT NULL,
    before TEXT,
    after TEXT,
    reason TEXT,
    source_reference_type TEXT,
    source_reference_id TEXT,
    source_reference_label TEXT,
    tokens_before INTEGER,
    tokens_after INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
  )
`);

// Index for efficient queries
db.exec(`
  CREATE INDEX IF NOT EXISTS idx_context_changes_project 
  ON context_changes(project_id, created_at DESC)
`);

db.exec(`
  CREATE INDEX IF NOT EXISTS idx_context_changes_file 
  ON context_changes(file, created_at DESC)
`);

// Context File State table (tracks current state of each file)
db.exec(`
  CREATE TABLE IF NOT EXISTS context_file_states (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    file TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    token_count INTEGER NOT NULL,
    last_modified TEXT NOT NULL,
    last_optimized TEXT,
    health TEXT NOT NULL DEFAULT 'healthy',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE(project_id, file)
  )
`);

// Optimization Suggestions table
db.exec(`
  CREATE TABLE IF NOT EXISTS optimization_suggestions (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    file TEXT NOT NULL,
    section TEXT NOT NULL,
    suggestion_type TEXT NOT NULL,
    before TEXT,
    after TEXT,
    reason TEXT,
    confidence TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
  )
`);
```

---

## 5. Change Detection Service

### FileWatcher Service

Create `electron/services/contextWatcher.ts`:

```typescript
import fs from 'fs'
import path from 'path'
import crypto from 'crypto'
import { EventEmitter } from 'events'

interface WatchedFile {
  path: string
  projectId: string
  file: string
  lastHash: string
  lastModified: number
}

interface FileChangeEvent {
  projectId: string
  file: string
  filePath: string
  previousHash: string
  currentHash: string
  previousContent: string
  currentContent: string
}

export class ContextWatcher extends EventEmitter {
  private watchedFiles: Map<string, WatchedFile> = new Map()
  private watchers: Map<string, fs.FSWatcher> = new Map()
  private pollInterval: NodeJS.Timeout | null = null
  private pollMs: number = 5000  // Check every 5 seconds

  /**
   * Start watching a project's context files
   */
  watchProject(projectId: string, repoPath: string): void {
    const filesToWatch = [
      'claude.md',
      'CLAUDE.md',  // Case variation
      'constitution.md',
      'CHANGELOG.md',
      'docs/architecture.md',
      'docs/data-model.md',
    ]

    for (const file of filesToWatch) {
      const filePath = path.join(repoPath, file)
      
      if (fs.existsSync(filePath)) {
        this.watchFile(projectId, file, filePath)
      }
    }
  }

  /**
   * Watch a specific file
   */
  private watchFile(projectId: string, file: string, filePath: string): void {
    const key = `${projectId}:${file}`
    
    // Read initial state
    const content = fs.readFileSync(filePath, 'utf-8')
    const hash = this.hashContent(content)
    const stat = fs.statSync(filePath)

    this.watchedFiles.set(key, {
      path: filePath,
      projectId,
      file,
      lastHash: hash,
      lastModified: stat.mtimeMs,
    })

    // Set up fs.watch (real-time, but can be unreliable)
    try {
      const watcher = fs.watch(filePath, (eventType) => {
        if (eventType === 'change') {
          this.checkFile(key)
        }
      })
      this.watchers.set(key, watcher)
    } catch (error) {
      console.warn(`Could not watch ${filePath}:`, error)
    }
  }

  /**
   * Start polling (backup for when fs.watch misses events)
   */
  startPolling(intervalMs: number = 5000): void {
    this.pollMs = intervalMs
    this.pollInterval = setInterval(() => {
      for (const key of this.watchedFiles.keys()) {
        this.checkFile(key)
      }
    }, this.pollMs)
  }

  /**
   * Stop polling
   */
  stopPolling(): void {
    if (this.pollInterval) {
      clearInterval(this.pollInterval)
      this.pollInterval = null
    }
  }

  /**
   * Check a file for changes
   */
  private checkFile(key: string): void {
    const watched = this.watchedFiles.get(key)
    if (!watched) return

    try {
      const stat = fs.statSync(watched.path)
      
      // Skip if not modified
      if (stat.mtimeMs <= watched.lastModified) return

      const currentContent = fs.readFileSync(watched.path, 'utf-8')
      const currentHash = this.hashContent(currentContent)

      // Skip if content unchanged (timestamp changed but content same)
      if (currentHash === watched.lastHash) {
        watched.lastModified = stat.mtimeMs
        return
      }

      // Content changed - emit event
      const previousContent = this.getPreviousContent(watched)
      
      const event: FileChangeEvent = {
        projectId: watched.projectId,
        file: watched.file,
        filePath: watched.path,
        previousHash: watched.lastHash,
        currentHash,
        previousContent,
        currentContent,
      }

      this.emit('change', event)

      // Update state
      watched.lastHash = currentHash
      watched.lastModified = stat.mtimeMs

    } catch (error) {
      // File might have been deleted
      console.warn(`Error checking ${watched.path}:`, error)
    }
  }

  /**
   * Get previous content (from cache or reconstruct)
   */
  private getPreviousContent(watched: WatchedFile): string {
    // In a real implementation, you might cache previous content
    // For now, return empty string (diff will show as all additions)
    return ''
  }

  /**
   * Hash content for comparison
   */
  private hashContent(content: string): string {
    return crypto.createHash('md5').update(content).digest('hex')
  }

  /**
   * Stop watching a project
   */
  unwatchProject(projectId: string): void {
    for (const [key, watched] of this.watchedFiles.entries()) {
      if (watched.projectId === projectId) {
        const watcher = this.watchers.get(key)
        if (watcher) {
          watcher.close()
          this.watchers.delete(key)
        }
        this.watchedFiles.delete(key)
      }
    }
  }

  /**
   * Stop all watching
   */
  stopAll(): void {
    this.stopPolling()
    for (const watcher of this.watchers.values()) {
      watcher.close()
    }
    this.watchers.clear()
    this.watchedFiles.clear()
  }

  /**
   * Count tokens (simple approximation: words * 1.3)
   */
  static countTokens(content: string): number {
    const words = content.split(/\s+/).filter(w => w.length > 0).length
    return Math.ceil(words * 1.3)
  }
}
```

### IPC Handlers

Add to `electron/ipc/index.ts`:

```typescript
import { ContextWatcher } from '../services/contextWatcher'

let contextWatcher: ContextWatcher | null = null

// Initialize watcher
function initContextWatcher(db: Database.Database) {
  contextWatcher = new ContextWatcher()
  
  contextWatcher.on('change', async (event) => {
    // Log the change
    const changeId = crypto.randomUUID()
    const tokensBefore = ContextWatcher.countTokens(event.previousContent)
    const tokensAfter = ContextWatcher.countTokens(event.currentContent)
    
    db.prepare(`
      INSERT INTO context_changes (
        id, project_id, file, source, action, before, after,
        tokens_before, tokens_after, created_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
      changeId,
      event.projectId,
      event.file,
      'agent',  // Assume agent until we can determine otherwise
      'update',
      event.previousContent,
      event.currentContent,
      tokensBefore,
      tokensAfter,
      new Date().toISOString()
    )

    // Update file state
    db.prepare(`
      INSERT OR REPLACE INTO context_file_states (
        id, project_id, file, content_hash, token_count, last_modified, health
      ) VALUES (?, ?, ?, ?, ?, ?, ?)
    `).run(
      `${event.projectId}:${event.file}`,
      event.projectId,
      event.file,
      event.currentHash,
      tokensAfter,
      new Date().toISOString(),
      tokensAfter > 1000 ? 'alert' : tokensAfter > 750 ? 'warning' : 'healthy'
    )

    // Notify renderer
    BrowserWindow.getAllWindows().forEach(win => {
      win.webContents.send('context:changed', {
        projectId: event.projectId,
        file: event.file,
        tokenCount: tokensAfter,
      })
    })
  })

  contextWatcher.startPolling(5000)
}

// IPC Handlers
ipcMain.handle('context:watchProject', async (_event, projectId: string, repoPath: string) => {
  if (!contextWatcher) return false
  contextWatcher.watchProject(projectId, repoPath)
  return true
})

ipcMain.handle('context:unwatchProject', async (_event, projectId: string) => {
  if (!contextWatcher) return
  contextWatcher.unwatchProject(projectId)
})

ipcMain.handle('context:getChanges', async (_event, filters: {
  projectId?: string
  file?: string
  source?: string
  limit?: number
  offset?: number
}) => {
  let query = 'SELECT * FROM context_changes WHERE 1=1'
  const params: any[] = []

  if (filters.projectId) {
    query += ' AND project_id = ?'
    params.push(filters.projectId)
  }
  if (filters.file) {
    query += ' AND file = ?'
    params.push(filters.file)
  }
  if (filters.source) {
    query += ' AND source = ?'
    params.push(filters.source)
  }

  query += ' ORDER BY created_at DESC'
  query += ` LIMIT ? OFFSET ?`
  params.push(filters.limit || 50, filters.offset || 0)

  return db.prepare(query).all(...params)
})

ipcMain.handle('context:getFileStates', async (_event, projectId: string) => {
  return db.prepare(`
    SELECT * FROM context_file_states WHERE project_id = ?
  `).all(projectId)
})

ipcMain.handle('context:getFileState', async (_event, projectId: string, file: string) => {
  return db.prepare(`
    SELECT * FROM context_file_states WHERE project_id = ? AND file = ?
  `).get(projectId, file)
})
```

### Preload Exposure

Add to `electron/preload.ts`:

```typescript
context: {
  watchProject: (projectId: string, repoPath: string) => 
    ipcRenderer.invoke('context:watchProject', projectId, repoPath),
  unwatchProject: (projectId: string) => 
    ipcRenderer.invoke('context:unwatchProject', projectId),
  getChanges: (filters: any) => 
    ipcRenderer.invoke('context:getChanges', filters),
  getFileStates: (projectId: string) => 
    ipcRenderer.invoke('context:getFileStates', projectId),
  getFileState: (projectId: string, file: string) => 
    ipcRenderer.invoke('context:getFileState', projectId, file),
  onChanged: (callback: (data: any) => void) => {
    ipcRenderer.on('context:changed', (_event, data) => callback(data))
    return () => ipcRenderer.removeAllListeners('context:changed')
  },
},
```

---

## 6. Frontend Store

Create `src/stores/contextStore.ts`:

```typescript
import { create } from 'zustand'
import { ContextChange, ContextFileState, OptimizationSuggestion } from '@/types'

interface ContextFilters {
  projectId?: string
  file?: string
  source?: string
}

interface ContextStore {
  // State
  changes: ContextChange[]
  fileStates: ContextFileState[]
  suggestions: OptimizationSuggestion[]
  isLoading: boolean
  error: string | null
  filters: ContextFilters

  // Actions
  loadChanges: (filters?: ContextFilters) => Promise<void>
  loadFileStates: (projectId: string) => Promise<void>
  setFilters: (filters: ContextFilters) => void
  watchProject: (projectId: string, repoPath: string) => Promise<void>
  unwatchProject: (projectId: string) => Promise<void>
  
  // Computed
  getHealthSummary: () => { healthy: number; warning: number; alert: number }
  getRecentChanges: (limit?: number) => ContextChange[]
}

export const useContextStore = create<ContextStore>((set, get) => ({
  changes: [],
  fileStates: [],
  suggestions: [],
  isLoading: false,
  error: null,
  filters: {},

  loadChanges: async (filters?: ContextFilters) => {
    set({ isLoading: true, error: null })
    try {
      const appliedFilters = filters || get().filters
      const changes = await window.electron.context.getChanges({
        ...appliedFilters,
        limit: 100,
      })
      set({ changes, isLoading: false, filters: appliedFilters })
    } catch (error) {
      set({ isLoading: false, error: String(error) })
    }
  },

  loadFileStates: async (projectId: string) => {
    try {
      const fileStates = await window.electron.context.getFileStates(projectId)
      set({ fileStates })
    } catch (error) {
      console.error('Error loading file states:', error)
    }
  },

  setFilters: (filters: ContextFilters) => {
    set({ filters })
    get().loadChanges(filters)
  },

  watchProject: async (projectId: string, repoPath: string) => {
    await window.electron.context.watchProject(projectId, repoPath)
  },

  unwatchProject: async (projectId: string) => {
    await window.electron.context.unwatchProject(projectId)
  },

  getHealthSummary: () => {
    const states = get().fileStates
    return {
      healthy: states.filter(s => s.health === 'healthy').length,
      warning: states.filter(s => s.health === 'warning').length,
      alert: states.filter(s => s.health === 'alert').length,
    }
  },

  getRecentChanges: (limit = 10) => {
    return get().changes.slice(0, limit)
  },
}))

// Set up listener for real-time changes
if (typeof window !== 'undefined' && window.electron?.context?.onChanged) {
  window.electron.context.onChanged((data) => {
    // Reload changes when a file changes
    useContextStore.getState().loadChanges()
  })
}
```

---

## 7. UI Components

### ContextHealthCard Component

Create `src/components/shared/ContextHealthCard.tsx`:

```typescript
import { useEffect } from 'react'
import { FileText, AlertTriangle, AlertCircle, CheckCircle, ExternalLink } from 'lucide-react'
import { useContextStore } from '@/stores'
import { Card, CardHeader, CardTitle, CardContent, Button } from '@/components/ui'
import { useNavigate } from 'react-router-dom'

interface ContextHealthCardProps {
  projectId?: string  // If provided, show single project. Otherwise, show all.
}

export function ContextHealthCard({ projectId }: ContextHealthCardProps) {
  const navigate = useNavigate()
  const { fileStates, loadFileStates, getHealthSummary, getRecentChanges } = useContextStore()

  useEffect(() => {
    if (projectId) {
      loadFileStates(projectId)
    }
  }, [projectId, loadFileStates])

  const health = getHealthSummary()
  const recentChanges = getRecentChanges(3)

  const getHealthIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="w-4 h-4 text-green-400" />
      case 'warning': return <AlertTriangle className="w-4 h-4 text-yellow-400" />
      case 'alert': return <AlertCircle className="w-4 h-4 text-red-400" />
      default: return <FileText className="w-4 h-4 text-text-muted" />
    }
  }

  const getHealthColor = (tokens: number) => {
    if (tokens > 1000) return 'bg-red-400'
    if (tokens > 750) return 'bg-yellow-400'
    if (tokens > 500) return 'bg-blue-400'
    return 'bg-green-400'
  }

  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const hours = Math.floor(diff / 3600000)
    if (hours < 1) return 'Just now'
    if (hours < 24) return `${hours}h ago`
    return `${Math.floor(hours / 24)}d ago`
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2">
          <FileText className="w-4 h-4" />
          Context Health
        </CardTitle>
        <Button 
          variant="ghost" 
          size="sm"
          onClick={() => navigate('/changelog')}
        >
          View All
          <ExternalLink className="w-3 h-3 ml-1" />
        </Button>
      </CardHeader>
      <CardContent>
        {/* File States */}
        {fileStates.length > 0 && (
          <div className="space-y-2 mb-4">
            {fileStates.map((state) => (
              <div key={state.id} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {getHealthIcon(state.health)}
                  <span className="text-sm">{state.file}</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-24 h-2 bg-elevated rounded-full overflow-hidden">
                    <div 
                      className={`h-full ${getHealthColor(state.token_count)}`}
                      style={{ width: `${Math.min((state.token_count / 1000) * 100, 100)}%` }}
                    />
                  </div>
                  <span className="text-xs text-text-muted w-16 text-right">
                    {state.token_count} tok
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Recent Changes */}
        {recentChanges.length > 0 && (
          <div>
            <h4 className="text-xs font-medium text-text-muted uppercase mb-2">
              Recent Changes
            </h4>
            <div className="space-y-1">
              {recentChanges.map((change) => (
                <div key={change.id} className="text-sm flex items-center justify-between">
                  <div className="flex items-center gap-2 truncate">
                    <span className={`text-xs px-1.5 py-0.5 rounded ${
                      change.source === 'agent' ? 'bg-blue-500/20 text-blue-400' :
                      change.source === 'auto' ? 'bg-purple-500/20 text-purple-400' :
                      change.source === 'manual' ? 'bg-green-500/20 text-green-400' :
                      'bg-gray-500/20 text-gray-400'
                    }`}>
                      {change.source.toUpperCase()}
                    </span>
                    <span className="truncate">{change.file}</span>
                  </div>
                  <span className="text-xs text-text-muted">
                    {formatTime(change.created_at)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {fileStates.length === 0 && recentChanges.length === 0 && (
          <p className="text-sm text-text-muted text-center py-4">
            No context files being tracked yet.
          </p>
        )}
      </CardContent>
    </Card>
  )
}
```

### ChangeLogPage Component

Create `src/pages/ChangeLog.tsx`:

```typescript
import { useEffect, useState } from 'react'
import { FileText, Filter, Search, ChevronDown, ChevronRight } from 'lucide-react'
import { useContextStore, useProjectStore } from '@/stores'
import { ContextChange } from '@/types'
import { 
  Card, CardHeader, CardTitle, CardContent, 
  Button, Input, Select 
} from '@/components/ui'

export function ChangeLogPage() {
  const { changes, isLoading, loadChanges, setFilters, filters } = useContextStore()
  const { projects } = useProjectStore()
  
  const [searchQuery, setSearchQuery] = useState('')
  const [expandedChanges, setExpandedChanges] = useState<Set<string>>(new Set())

  useEffect(() => {
    loadChanges()
  }, [loadChanges])

  const toggleExpanded = (id: string) => {
    const next = new Set(expandedChanges)
    if (next.has(id)) {
      next.delete(id)
    } else {
      next.add(id)
    }
    setExpandedChanges(next)
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    })
  }

  const getSourceBadge = (source: string) => {
    const styles: Record<string, string> = {
      agent: 'bg-blue-500/20 text-blue-400',
      auto: 'bg-purple-500/20 text-purple-400',
      manual: 'bg-green-500/20 text-green-400',
      optimize: 'bg-orange-500/20 text-orange-400',
    }
    return (
      <span className={`text-xs px-2 py-0.5 rounded ${styles[source] || 'bg-gray-500/20'}`}>
        {source.toUpperCase()}
      </span>
    )
  }

  const getActionBadge = (action: string) => {
    const styles: Record<string, string> = {
      add: 'text-green-400',
      update: 'text-blue-400',
      delete: 'text-red-400',
      consolidate: 'text-purple-400',
    }
    return <span className={`text-xs ${styles[action] || ''}`}>{action}</span>
  }

  const filteredChanges = changes.filter(change => {
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      return (
        change.file.toLowerCase().includes(query) ||
        change.section?.toLowerCase().includes(query) ||
        change.after?.toLowerCase().includes(query) ||
        change.reason?.toLowerCase().includes(query)
      )
    }
    return true
  })

  // Group changes by date
  const groupedChanges = filteredChanges.reduce((acc, change) => {
    const date = new Date(change.created_at).toLocaleDateString()
    if (!acc[date]) acc[date] = []
    acc[date].push(change)
    return acc
  }, {} as Record<string, ContextChange[]>)

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold flex items-center gap-2">
          <FileText className="w-6 h-6" />
          Change Log
        </h1>
      </div>

      {/* Filters */}
      <Card className="mb-6">
        <CardContent className="py-4">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" />
                <Input
                  placeholder="Search changes..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            
            <Select
              value={filters.projectId || 'all'}
              onValueChange={(value) => setFilters({ 
                ...filters, 
                projectId: value === 'all' ? undefined : value 
              })}
            >
              <option value="all">All Projects</option>
              {projects.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </Select>

            <Select
              value={filters.file || 'all'}
              onValueChange={(value) => setFilters({ 
                ...filters, 
                file: value === 'all' ? undefined : value 
              })}
            >
              <option value="all">All Files</option>
              <option value="claude.md">claude.md</option>
              <option value="constitution.md">constitution.md</option>
              <option value="architecture.md">architecture.md</option>
              <option value="CHANGELOG.md">CHANGELOG.md</option>
            </Select>

            <Select
              value={filters.source || 'all'}
              onValueChange={(value) => setFilters({ 
                ...filters, 
                source: value === 'all' ? undefined : value 
              })}
            >
              <option value="all">All Sources</option>
              <option value="agent">Agent</option>
              <option value="auto">Auto</option>
              <option value="manual">Manual</option>
              <option value="optimize">Optimize</option>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Changes List */}
      {isLoading ? (
        <div className="text-center py-8 text-text-muted">Loading changes...</div>
      ) : Object.keys(groupedChanges).length === 0 ? (
        <div className="text-center py-8 text-text-muted">No changes found.</div>
      ) : (
        <div className="space-y-6">
          {Object.entries(groupedChanges).map(([date, dayChanges]) => (
            <div key={date}>
              <h3 className="text-sm font-medium text-text-muted mb-3">{date}</h3>
              <div className="space-y-2">
                {dayChanges.map((change) => (
                  <Card key={change.id} className="overflow-hidden">
                    <button
                      className="w-full text-left p-4 hover:bg-elevated/50 transition-colors"
                      onClick={() => toggleExpanded(change.id)}
                    >
                      <div className="flex items-start gap-3">
                        {expandedChanges.has(change.id) ? (
                          <ChevronDown className="w-4 h-4 mt-1 text-text-muted" />
                        ) : (
                          <ChevronRight className="w-4 h-4 mt-1 text-text-muted" />
                        )}
                        
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            {getSourceBadge(change.source)}
                            <span className="font-medium">{change.file}</span>
                            {change.section && (
                              <span className="text-text-muted">→ {change.section}</span>
                            )}
                            {getActionBadge(change.action)}
                          </div>
                          
                          {change.reason && (
                            <p className="text-sm text-text-muted truncate">
                              {change.reason}
                            </p>
                          )}
                          
                          <div className="flex items-center gap-4 mt-2 text-xs text-text-muted">
                            <span>{formatDate(change.created_at)}</span>
                            {change.tokens_before !== undefined && change.tokens_after !== undefined && (
                              <span>
                                {change.tokens_before} → {change.tokens_after} tokens
                                {change.tokens_after < change.tokens_before && (
                                  <span className="text-green-400 ml-1">
                                    (-{change.tokens_before - change.tokens_after})
                                  </span>
                                )}
                                {change.tokens_after > change.tokens_before && (
                                  <span className="text-yellow-400 ml-1">
                                    (+{change.tokens_after - change.tokens_before})
                                  </span>
                                )}
                              </span>
                            )}
                            {change.source_reference && (
                              <span>
                                Source: {change.source_reference.label || change.source_reference.type}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </button>

                    {/* Expanded diff view */}
                    {expandedChanges.has(change.id) && (
                      <div className="px-4 pb-4 pl-11">
                        <div className="bg-elevated rounded p-3 font-mono text-xs overflow-x-auto">
                          {change.before && (
                            <div className="text-red-400 whitespace-pre-wrap">
                              {change.before.split('\n').map((line, i) => (
                                <div key={`before-${i}`}>- {line}</div>
                              ))}
                            </div>
                          )}
                          {change.after && (
                            <div className="text-green-400 whitespace-pre-wrap mt-2">
                              {change.after.split('\n').map((line, i) => (
                                <div key={`after-${i}`}>+ {line}</div>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </Card>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
```

### Add Route

Add to `src/App.tsx` or router config:

```typescript
import { ChangeLogPage } from '@/pages/ChangeLog'

// In routes:
{ path: '/changelog', element: <ChangeLogPage /> }
```

### Navigation

Add to sidebar navigation:

```typescript
{ icon: FileText, label: 'Change Log', path: '/changelog' }
```

---

## 8. Context Editor

The Context Editor is the primary UI for viewing and editing context files (claude.md, constitution.md, etc.). It supports both structured editing (section-by-section) and raw markdown editing.

### Navigation & Routing

**Routes:**

| Route | Purpose |
|-------|---------|
| `/projects/:projectId/context` | Context Editor for a project (default to claude.md) |
| `/projects/:projectId/context/:file` | Context Editor for specific file |
| `/registry/templates` | Template browser |
| `/registry/templates/:templateId` | Template Editor |

**Entry Points:**

```
┌─────────────────────────────────────────────────────────────────┐
│                     NAVIGATION FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. From Project View                                           │
│     Project View → Context tab → [Edit claude.md]               │
│     → /projects/:projectId/context/claude.md                    │
│                                                                 │
│  2. From Dashboard (Context Health Card)                        │
│     Dashboard → Click file in health card                       │
│     → /projects/:projectId/context/:file                        │
│                                                                 │
│  3. From Registry (Templates)                                   │
│     Registry → Templates → [Edit]                               │
│     → /registry/templates/:templateId                           │
│                                                                 │
│  4. Direct URL                                                  │
│     /projects/proj-001/context/claude.md                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Page Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  CONTEXT EDITOR                              Project: Risk Tools │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  [claude.md ●]  [constitution.md]  [architecture.md]  [+]   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌───────────────────────────────────┬─────────────────────────┐│
│  │ STATUS                            │ ACTIONS                 ││
│  │ ● In sync with repo               │ [Push to Repo]          ││
│  │ 423 tokens (healthy)              │ [Pull from Repo]        ││
│  │ Last modified: 2h ago (agent)     │ [View Diff]             ││
│  └───────────────────────────────────┴─────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  [Structured View]  [Raw Markdown]                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                                                             ││
│  │  (Section cards or raw textarea based on view mode)         ││
│  │                                                             ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Edit Modes

The editor uses a **hybrid approach**:

| Section Length | Edit Mode | Behavior |
|----------------|-----------|----------|
| Short (<8 lines) | Inline | Click [Edit] → textarea replaces content → Save/Cancel |
| Long (≥8 lines) | Modal | Click [Edit] → modal with larger editor + tips |
| Any | Raw | Toggle to Raw Markdown → full file textarea |

### Section Ownership Behavior

| Ownership | Badge | Editable in Studio? | Actions |
|-----------|-------|---------------------|----------|
| **HUMAN** 🔓 | Green | Yes | [Edit] button |
| **AGENT** 🤖 | Blue | No (read-only) | [View History] button |
| **AUTO** 🔄 | Purple | No (read-only) | [Remove] for individual items |
| **EPHEMERAL** ⏱️ | Gray | No (read-only) | None (auto-managed) |

### Section Parsing

The editor parses markdown into sections based on `##` headings and ownership comments.

**`src/lib/contextParser.ts`:**

```typescript
export type SectionOwnership = 'human' | 'agent' | 'auto' | 'ephemeral' | 'unknown'

export interface ParsedSection {
  id: string                    // Generated from heading
  heading: string               // "## Active Priorities"
  title: string                 // "Active Priorities"
  ownership: SectionOwnership
  ownershipComment?: string     // Raw comment if present
  content: string               // Content after heading
  startLine: number
  endLine: number
  lineCount: number
}

export interface ParsedContextFile {
  frontmatter?: string          // Content before first ## heading
  sections: ParsedSection[]
  raw: string
}

/**
 * Parse a context file into sections
 */
export function parseContextFile(content: string): ParsedContextFile {
  const lines = content.split('\n')
  const sections: ParsedSection[] = []
  let frontmatter = ''
  let currentSection: Partial<ParsedSection> | null = null
  let currentContent: string[] = []

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    
    // Check for section heading
    if (line.startsWith('## ')) {
      // Save previous section
      if (currentSection) {
        currentSection.content = currentContent.join('\n').trim()
        currentSection.endLine = i - 1
        currentSection.lineCount = currentSection.endLine - currentSection.startLine + 1
        sections.push(currentSection as ParsedSection)
      } else if (currentContent.length > 0) {
        frontmatter = currentContent.join('\n').trim()
      }

      // Start new section
      const title = line.replace('## ', '').trim()
      currentSection = {
        id: title.toLowerCase().replace(/\s+/g, '-'),
        heading: line,
        title,
        ownership: 'unknown',
        startLine: i,
      }
      currentContent = []
    } else {
      // Check for ownership comment
      if (currentSection && line.includes('<!-- ')) {
        const ownershipMatch = line.match(/<!--\s*(HUMAN|AGENT|AUTO|EPHEMERAL)/i)
        if (ownershipMatch) {
          currentSection.ownership = ownershipMatch[1].toLowerCase() as SectionOwnership
          currentSection.ownershipComment = line
        }
      }
      currentContent.push(line)
    }
  }

  // Save last section
  if (currentSection) {
    currentSection.content = currentContent.join('\n').trim()
    currentSection.endLine = lines.length - 1
    currentSection.lineCount = currentSection.endLine - currentSection.startLine + 1
    sections.push(currentSection as ParsedSection)
  } else if (currentContent.length > 0) {
    frontmatter = currentContent.join('\n').trim()
  }

  return { frontmatter, sections, raw: content }
}

/**
 * Reconstruct file from parsed sections
 */
export function reconstructContextFile(parsed: ParsedContextFile): string {
  const parts: string[] = []
  
  if (parsed.frontmatter) {
    parts.push(parsed.frontmatter)
    parts.push('')
  }

  for (const section of parsed.sections) {
    parts.push(section.heading)
    if (section.ownershipComment) {
      parts.push(section.ownershipComment)
    }
    parts.push(section.content)
    parts.push('')
  }

  return parts.join('\n').trim()
}

/**
 * Update a single section's content
 */
export function updateSection(
  parsed: ParsedContextFile, 
  sectionId: string, 
  newContent: string
): ParsedContextFile {
  const sections = parsed.sections.map(section => {
    if (section.id === sectionId) {
      return { ...section, content: newContent }
    }
    return section
  })
  
  return { ...parsed, sections }
}
```

### Structured View Component

**`src/components/context/StructuredView.tsx`:**

```typescript
import { useState } from 'react'
import { Lock, Bot, Zap, Clock, Edit2, History, ChevronDown, ChevronRight } from 'lucide-react'
import { ParsedSection, SectionOwnership } from '@/lib/contextParser'
import { Card, Button, Textarea } from '@/components/ui'
import { SectionEditModal } from './SectionEditModal'

interface StructuredViewProps {
  sections: ParsedSection[]
  onSectionUpdate: (sectionId: string, content: string) => void
  onViewHistory?: (sectionId: string) => void
}

const OWNERSHIP_CONFIG: Record<SectionOwnership, {
  icon: React.ReactNode
  label: string
  color: string
  editable: boolean
}> = {
  human: {
    icon: <Lock className="w-4 h-4" />,
    label: 'HUMAN',
    color: 'border-l-green-400 bg-green-500/5',
    editable: true,
  },
  agent: {
    icon: <Bot className="w-4 h-4" />,
    label: 'AGENT',
    color: 'border-l-blue-400 bg-blue-500/5',
    editable: false,
  },
  auto: {
    icon: <Zap className="w-4 h-4" />,
    label: 'AUTO',
    color: 'border-l-purple-400 bg-purple-500/5',
    editable: false,
  },
  ephemeral: {
    icon: <Clock className="w-4 h-4" />,
    label: 'EPHEMERAL',
    color: 'border-l-gray-400 bg-gray-500/5',
    editable: false,
  },
  unknown: {
    icon: null,
    label: '',
    color: 'border-l-gray-300',
    editable: true,
  },
}

const MODAL_THRESHOLD = 8  // Lines before switching to modal

export function StructuredView({ sections, onSectionUpdate, onViewHistory }: StructuredViewProps) {
  const [editingSection, setEditingSection] = useState<string | null>(null)
  const [editContent, setEditContent] = useState('')
  const [modalSection, setModalSection] = useState<ParsedSection | null>(null)
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set())

  const handleEdit = (section: ParsedSection) => {
    if (section.lineCount > MODAL_THRESHOLD) {
      setModalSection(section)
    } else {
      setEditingSection(section.id)
      setEditContent(section.content)
    }
  }

  const saveInlineEdit = (sectionId: string) => {
    onSectionUpdate(sectionId, editContent)
    setEditingSection(null)
    setEditContent('')
  }

  return (
    <div className="space-y-4">
      {sections.map((section) => {
        const config = OWNERSHIP_CONFIG[section.ownership]
        const isEditing = editingSection === section.id
        const isCollapsed = collapsedSections.has(section.id)

        return (
          <Card key={section.id} className={`border-l-4 ${config.color}`}>
            {/* Section Header */}
            <div className="flex items-center justify-between p-4 pb-2">
              <button
                className="flex items-center gap-2"
                onClick={() => {
                  const next = new Set(collapsedSections)
                  isCollapsed ? next.delete(section.id) : next.add(section.id)
                  setCollapsedSections(next)
                }}
              >
                {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                <h3 className="font-medium">{section.title}</h3>
              </button>
              
              <div className="flex items-center gap-2">
                {config.icon && (
                  <span className={`flex items-center gap-1 text-xs px-2 py-1 rounded ${
                    section.ownership === 'human' ? 'bg-green-500/20 text-green-400' :
                    section.ownership === 'agent' ? 'bg-blue-500/20 text-blue-400' :
                    section.ownership === 'auto' ? 'bg-purple-500/20 text-purple-400' :
                    'bg-gray-500/20 text-gray-400'
                  }`}>
                    {config.icon} {config.label}
                  </span>
                )}
                
                {config.editable && !isEditing && (
                  <Button variant="ghost" size="sm" onClick={() => handleEdit(section)}>
                    <Edit2 className="w-4 h-4" />
                  </Button>
                )}
                
                {!config.editable && onViewHistory && (
                  <Button variant="ghost" size="sm" onClick={() => onViewHistory(section.id)}>
                    <History className="w-4 h-4" />
                  </Button>
                )}
              </div>
            </div>

            {/* Section Content */}
            {!isCollapsed && (
              <div className="px-4 pb-4">
                {isEditing ? (
                  <div className="space-y-2">
                    <Textarea
                      value={editContent}
                      onChange={(e) => setEditContent(e.target.value)}
                      className="font-mono text-sm min-h-[100px]"
                      autoFocus
                    />
                    <div className="flex justify-end gap-2">
                      <Button variant="ghost" size="sm" onClick={() => setEditingSection(null)}>
                        Cancel
                      </Button>
                      <Button size="sm" onClick={() => saveInlineEdit(section.id)}>
                        Save
                      </Button>
                    </div>
                  </div>
                ) : (
                  <pre className="whitespace-pre-wrap font-sans text-sm">
                    {section.content || <span className="text-text-muted italic">No content</span>}
                  </pre>
                )}
              </div>
            )}
          </Card>
        )
      })}

      {modalSection && (
        <SectionEditModal
          section={modalSection}
          onSave={(content) => {
            onSectionUpdate(modalSection.id, content)
            setModalSection(null)
          }}
          onClose={() => setModalSection(null)}
        />
      )}
    </div>
  )
}
```

### Section Edit Modal

**`src/components/context/SectionEditModal.tsx`:**

```typescript
import { useState } from 'react'
import { X } from 'lucide-react'
import { ParsedSection } from '@/lib/contextParser'
import { Button, Textarea } from '@/components/ui'

interface SectionEditModalProps {
  section: ParsedSection
  onSave: (content: string) => void
  onClose: () => void
}

const SECTION_TIPS: Record<string, string> = {
  'active-priorities': 'Keep to 3-5 priorities. Be specific about what "done" looks like.',
  'constraints': 'State what the agent must NOT do. Be explicit.',
  'intent': '2-3 sentences. What are we building and why?',
  'tech-stack': 'List core technologies. This rarely changes after init.',
}

export function SectionEditModal({ section, onSave, onClose }: SectionEditModalProps) {
  const [content, setContent] = useState(section.content)
  const tip = SECTION_TIPS[section.id]

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-surface rounded-lg shadow-xl w-full max-w-2xl max-h-[80vh] flex flex-col">
        <div className="flex items-center justify-between p-4 border-b border-border">
          <h2 className="text-lg font-semibold">Edit: {section.title}</h2>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="w-4 h-4" />
          </Button>
        </div>

        <div className="flex-1 p-4 overflow-auto">
          <Textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="font-mono text-sm w-full min-h-[300px]"
            autoFocus
          />
          {tip && <p className="mt-4 text-xs text-text-muted">Tip: {tip}</p>}
        </div>

        <div className="flex justify-end gap-2 p-4 border-t border-border">
          <Button variant="ghost" onClick={onClose}>Cancel</Button>
          <Button onClick={() => onSave(content)}>Save Changes</Button>
        </div>
      </div>
    </div>
  )
}
```

### Raw Markdown View

**`src/components/context/RawMarkdownView.tsx`:**

```typescript
import { Textarea } from '@/components/ui'

interface RawMarkdownViewProps {
  content: string
  onChange: (content: string) => void
  readOnly?: boolean
}

export function RawMarkdownView({ content, onChange, readOnly }: RawMarkdownViewProps) {
  return (
    <Textarea
      value={content}
      onChange={(e) => onChange(e.target.value)}
      className="font-mono text-sm w-full h-[500px] resize-y"
      readOnly={readOnly}
      placeholder="# Project Name\n\n## Intent\n<!-- HUMAN -->\n..."
    />
  )
}
```

### Context Editor Page

**`src/pages/ContextEditor.tsx`:**

```typescript
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { FileText, Upload, Download, GitCompare, CheckCircle, AlertTriangle } from 'lucide-react'
import { useProjectStore, useContextStore } from '@/stores'
import { parseContextFile, reconstructContextFile, updateSection, ParsedContextFile } from '@/lib/contextParser'
import { Card, CardContent, Button, Tabs, TabsList, TabsTrigger } from '@/components/ui'
import { StructuredView } from '@/components/context/StructuredView'
import { RawMarkdownView } from '@/components/context/RawMarkdownView'

type ViewMode = 'structured' | 'raw'
type SyncStatus = 'synced' | 'modified' | 'conflict'

const CONTEXT_FILES = ['claude.md', 'constitution.md', 'architecture.md', 'data-model.md']

export function ContextEditorPage() {
  const { projectId, file: fileParam } = useParams()
  const navigate = useNavigate()
  const { getProject } = useProjectStore()
  const { fileStates, loadFileStates } = useContextStore()

  const [activeFile, setActiveFile] = useState(fileParam || 'claude.md')
  const [viewMode, setViewMode] = useState<ViewMode>('structured')
  const [parsedContent, setParsedContent] = useState<ParsedContextFile | null>(null)
  const [rawContent, setRawContent] = useState('')
  const [originalContent, setOriginalContent] = useState('')
  const [syncStatus, setSyncStatus] = useState<SyncStatus>('synced')
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)

  const project = projectId ? getProject(projectId) : null
  const fileState = fileStates.find(s => s.file === activeFile)

  // Load file content
  useEffect(() => {
    if (!project?.repo_path) return

    const loadFile = async () => {
      setIsLoading(true)
      try {
        const content = await window.electron.fs.readFile(
          `${project.repo_path}/${activeFile}`
        )
        setOriginalContent(content)
        setRawContent(content)
        setParsedContent(parseContextFile(content))
        setSyncStatus('synced')
      } catch (error) {
        setOriginalContent('')
        setRawContent('')
        setParsedContent(null)
      } finally {
        setIsLoading(false)
      }
    }

    loadFile()
    loadFileStates(projectId!)
  }, [project?.repo_path, activeFile, projectId, loadFileStates])

  // Track modifications
  useEffect(() => {
    setSyncStatus(rawContent !== originalContent ? 'modified' : 'synced')
  }, [rawContent, originalContent])

  // Handle section update (structured view)
  const handleSectionUpdate = (sectionId: string, newContent: string) => {
    if (!parsedContent) return
    const updated = updateSection(parsedContent, sectionId, newContent)
    setParsedContent(updated)
    setRawContent(reconstructContextFile(updated))
  }

  // Handle raw content update
  const handleRawUpdate = (content: string) => {
    setRawContent(content)
    setParsedContent(parseContextFile(content))
  }

  // Push to repo
  const handlePush = async () => {
    if (!project?.repo_path) return
    setIsSaving(true)
    try {
      await window.electron.fs.writeFile(`${project.repo_path}/${activeFile}`, rawContent)
      setOriginalContent(rawContent)
      setSyncStatus('synced')
    } finally {
      setIsSaving(false)
    }
  }

  // Pull from repo
  const handlePull = async () => {
    if (!project?.repo_path) return
    setIsLoading(true)
    try {
      const content = await window.electron.fs.readFile(`${project.repo_path}/${activeFile}`)
      setOriginalContent(content)
      setRawContent(content)
      setParsedContent(parseContextFile(content))
      setSyncStatus('synced')
    } finally {
      setIsLoading(false)
    }
  }

  if (!project) return <div className="p-6">Project not found</div>

  return (
    <div className="p-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-semibold flex items-center gap-2">
          <FileText className="w-6 h-6" /> Context Editor
        </h1>
        <p className="text-text-muted mt-1">{project.name}</p>
      </div>

      {/* File Tabs */}
      <div className="flex items-center gap-2 mb-4 border-b border-border pb-2">
        {CONTEXT_FILES.map((file) => (
          <button
            key={file}
            onClick={() => {
              setActiveFile(file)
              navigate(`/projects/${projectId}/context/${file}`)
            }}
            className={`px-3 py-2 rounded-t text-sm ${
              activeFile === file
                ? 'bg-elevated text-text-primary border-b-2 border-accent'
                : 'text-text-muted hover:text-text-primary'
            }`}
          >
            {file}
            {activeFile === file && syncStatus === 'modified' && (
              <span className="ml-1 text-yellow-400">●</span>
            )}
          </button>
        ))}
      </div>

      {/* Status Bar */}
      <Card className="mb-4">
        <CardContent className="py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                {syncStatus === 'synced' ? (
                  <CheckCircle className="w-4 h-4 text-green-400" />
                ) : (
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                )}
                <span className="text-sm">
                  {syncStatus === 'synced' ? 'In sync with repo' : 'Unsaved changes'}
                </span>
              </div>
              {fileState && (
                <>
                  <span className="text-text-muted">•</span>
                  <span className="text-sm">{fileState.token_count} tokens</span>
                </>
              )}
            </div>

            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm" onClick={handlePull} disabled={isLoading}>
                <Download className="w-4 h-4 mr-1" /> Pull
              </Button>
              <Button variant="ghost" size="sm" disabled={syncStatus === 'synced'}>
                <GitCompare className="w-4 h-4 mr-1" /> Diff
              </Button>
              <Button size="sm" onClick={handlePush} disabled={syncStatus === 'synced' || isSaving}>
                <Upload className="w-4 h-4 mr-1" /> {isSaving ? 'Saving...' : 'Push'}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* View Mode Toggle */}
      <div className="mb-4">
        <Tabs value={viewMode} onValueChange={(v) => setViewMode(v as ViewMode)}>
          <TabsList>
            <TabsTrigger value="structured">Structured View</TabsTrigger>
            <TabsTrigger value="raw">Raw Markdown</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {/* Content */}
      {isLoading ? (
        <div className="text-center py-12 text-text-muted">Loading...</div>
      ) : viewMode === 'structured' && parsedContent ? (
        <StructuredView
          sections={parsedContent.sections}
          onSectionUpdate={handleSectionUpdate}
          onViewHistory={(sectionId) => navigate(`/changelog?file=${activeFile}&section=${sectionId}`)}
        />
      ) : (
        <RawMarkdownView content={rawContent} onChange={handleRawUpdate} />
      )}
    </div>
  )
}
```

### Template Editor

The Template Editor uses the same components but saves to the registry instead of the repo.

**`src/pages/TemplateEditor.tsx`:**

```typescript
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { FileText, Save, ArrowLeft } from 'lucide-react'
import { parseContextFile, reconstructContextFile, updateSection, ParsedContextFile } from '@/lib/contextParser'
import { Card, CardContent, Button, Tabs, TabsList, TabsTrigger } from '@/components/ui'
import { StructuredView } from '@/components/context/StructuredView'
import { RawMarkdownView } from '@/components/context/RawMarkdownView'

type ViewMode = 'structured' | 'raw'

export function TemplateEditorPage() {
  const { templateId } = useParams()
  const navigate = useNavigate()

  const [viewMode, setViewMode] = useState<ViewMode>('structured')
  const [parsedContent, setParsedContent] = useState<ParsedContextFile | null>(null)
  const [rawContent, setRawContent] = useState('')
  const [originalContent, setOriginalContent] = useState('')
  const [isModified, setIsModified] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    const loadTemplate = async () => {
      setIsLoading(true)
      try {
        const template = await window.electron.templates.get(templateId!)
        setOriginalContent(template.content)
        setRawContent(template.content)
        setParsedContent(parseContextFile(template.content))
      } finally {
        setIsLoading(false)
      }
    }
    loadTemplate()
  }, [templateId])

  useEffect(() => {
    setIsModified(rawContent !== originalContent)
  }, [rawContent, originalContent])

  const handleSectionUpdate = (sectionId: string, newContent: string) => {
    if (!parsedContent) return
    const updated = updateSection(parsedContent, sectionId, newContent)
    setParsedContent(updated)
    setRawContent(reconstructContextFile(updated))
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      await window.electron.templates.update(templateId!, { content: rawContent })
      setOriginalContent(rawContent)
      setIsModified(false)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/registry/templates')}>
            <ArrowLeft className="w-4 h-4" />
          </Button>
          <div>
            <h1 className="text-2xl font-semibold flex items-center gap-2">
              <FileText className="w-6 h-6" /> Edit Template
            </h1>
            <p className="text-text-muted mt-1">{templateId}</p>
          </div>
        </div>
        <Button onClick={handleSave} disabled={!isModified || isSaving}>
          <Save className="w-4 h-4 mr-2" /> {isSaving ? 'Saving...' : 'Save Template'}
        </Button>
      </div>

      {isModified && (
        <Card className="mb-4 border-yellow-500/50">
          <CardContent className="py-2">
            <span className="text-sm text-yellow-400">You have unsaved changes</span>
          </CardContent>
        </Card>
      )}

      <div className="mb-4">
        <Tabs value={viewMode} onValueChange={(v) => setViewMode(v as ViewMode)}>
          <TabsList>
            <TabsTrigger value="structured">Structured View</TabsTrigger>
            <TabsTrigger value="raw">Raw Markdown</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-text-muted">Loading...</div>
      ) : viewMode === 'structured' && parsedContent ? (
        <StructuredView sections={parsedContent.sections} onSectionUpdate={handleSectionUpdate} />
      ) : (
        <RawMarkdownView content={rawContent} onChange={(c) => {
          setRawContent(c)
          setParsedContent(parseContextFile(c))
        }} />
      )}
    </div>
  )
}
```

### Routes

Add to `src/App.tsx`:

```typescript
import { ContextEditorPage } from '@/pages/ContextEditor'
import { TemplateEditorPage } from '@/pages/TemplateEditor'

// Routes
{ path: '/projects/:projectId/context', element: <ContextEditorPage /> }
{ path: '/projects/:projectId/context/:file', element: <ContextEditorPage /> }
{ path: '/registry/templates/:templateId', element: <TemplateEditorPage /> }
```

### IPC Handlers for File Operations

Add to `electron/ipc/index.ts`:

```typescript
import fs from 'fs/promises'

ipcMain.handle('fs:readFile', async (_event, filePath: string) => {
  return await fs.readFile(filePath, 'utf-8')
})

ipcMain.handle('fs:writeFile', async (_event, filePath: string, content: string) => {
  await fs.writeFile(filePath, content, 'utf-8')
  return true
})

ipcMain.handle('fs:exists', async (_event, filePath: string) => {
  try {
    await fs.access(filePath)
    return true
  } catch {
    return false
  }
})
```

### Preload Additions

Add to `electron/preload.ts`:

```typescript
fs: {
  readFile: (filePath: string) => ipcRenderer.invoke('fs:readFile', filePath),
  writeFile: (filePath: string, content: string) => ipcRenderer.invoke('fs:writeFile', filePath, content),
  exists: (filePath: string) => ipcRenderer.invoke('fs:exists', filePath),
},

templates: {
  get: (id: string) => ipcRenderer.invoke('templates:get', id),
  update: (id: string, data: any) => ipcRenderer.invoke('templates:update', id, data),
  list: () => ipcRenderer.invoke('templates:list'),
},
```

### Context Editor Files Summary

| File | Action | Description |
|------|--------|-------------|
| `src/lib/contextParser.ts` | Create | Parse markdown into sections |
| `src/components/context/StructuredView.tsx` | Create | Section-based view component |
| `src/components/context/RawMarkdownView.tsx` | Create | Raw textarea view |
| `src/components/context/SectionEditModal.tsx` | Create | Modal for editing longer sections |
| `src/pages/ContextEditor.tsx` | Create | Main context editor page |
| `src/pages/TemplateEditor.tsx` | Create | Template editor page |
| `src/App.tsx` | Update | Add routes |
| `electron/ipc/index.ts` | Update | Add file system handlers |
| `electron/preload.ts` | Update | Expose fs and templates APIs |

### Context Editor Testing Checklist

- [ ] Context Editor loads for a project
- [ ] File tabs switch between files
- [ ] Structured view shows sections with ownership badges
- [ ] HUMAN sections have [Edit] button
- [ ] AGENT/AUTO sections show [View History] button
- [ ] Inline edit works for short sections (<8 lines)
- [ ] Modal edit opens for long sections (≥8 lines)
- [ ] Raw Markdown toggle works
- [ ] Changes in raw mode reflect in structured mode
- [ ] Push saves to repo file
- [ ] Pull loads from repo file
- [ ] Unsaved changes indicator works
- [ ] Token count displays correctly
- [ ] Template Editor loads templates
- [ ] Template Editor saves to registry

---

## 9. Optimization Pass (Phase 2)

> **Note:** This section is designed but deferred to Phase 2. Including here for completeness.

### Optimization Service

Create `electron/services/contextOptimizer.ts`:

```typescript
import Anthropic from '@anthropic-ai/sdk'

interface OptimizationResult {
  suggestions: Array<{
    section: string
    type: 'remove' | 'consolidate' | 'verify' | 'archive'
    before: string
    after: string
    reason: string
    confidence: 'high' | 'medium' | 'low'
  }>
  tokensBefore: number
  tokensAfter: number
}

export class ContextOptimizer {
  private client: Anthropic

  constructor(apiKey: string) {
    this.client = new Anthropic({ apiKey })
  }

  async analyzeClaudeMd(
    content: string, 
    recentSessions: string[]
  ): Promise<OptimizationResult> {
    const prompt = `You are analyzing a claude.md file for optimization. Your goal is to identify:

1. STALE content - references to completed work, outdated status
2. DUPLICATES - same information stated multiple ways
3. CONSOLIDATIONS - multiple lines that could be one
4. VERIFY - content that might be outdated (ask human to confirm)

Current claude.md:
\`\`\`
${content}
\`\`\`

Recent session summaries (for context on what's current):
${recentSessions.map((s, i) => `Session ${i + 1}: ${s}`).join('\n')}

Analyze the claude.md and return JSON with this structure:
{
  "suggestions": [
    {
      "section": "Current State",
      "type": "consolidate",
      "before": "- JWT implemented\\n- Refresh tokens done\\n- Auth testing complete",
      "after": "- Auth: Complete (JWT + refresh)",
      "reason": "Three lines describe completed auth work",
      "confidence": "high"
    }
  ],
  "summary": "Found N issues, estimated token savings: X"
}

Be conservative. Only suggest changes you're confident about. When in doubt, use "verify" type.`

    const response = await this.client.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 2000,
      messages: [{ role: 'user', content: prompt }],
    })

    // Parse response
    const text = response.content[0].type === 'text' ? response.content[0].text : ''
    const json = JSON.parse(text.match(/\{[\s\S]*\}/)?.[0] || '{}')
    
    return {
      suggestions: json.suggestions || [],
      tokensBefore: this.countTokens(content),
      tokensAfter: this.estimateAfterTokens(content, json.suggestions || []),
    }
  }

  private countTokens(content: string): number {
    return Math.ceil(content.split(/\s+/).length * 1.3)
  }

  private estimateAfterTokens(content: string, suggestions: any[]): number {
    let estimate = this.countTokens(content)
    for (const s of suggestions) {
      if (s.type === 'remove') {
        estimate -= this.countTokens(s.before)
      } else if (s.type === 'consolidate') {
        estimate -= this.countTokens(s.before)
        estimate += this.countTokens(s.after)
      }
    }
    return Math.max(estimate, 0)
  }
}
```

---

## 10. Files Summary

| File | Action | Description |
|------|--------|-------------|
| `templates/constitution/base.md` | Create/Update | Add change logging rules |
| `templates/files/CHANGELOG.md` | Create | Template for project changelog |
| `templates/claude-md/base.md` | Create | Base claude.md with section ownership |
| `templates/claude-md/layer-*.md` | Create | Tech-specific layers |
| `src/types/index.ts` | Update | Add ContextChange, ContextFileState types |
| `electron/services/contextWatcher.ts` | Create | File watching service |
| `electron/ipc/index.ts` | Update | Add context-related handlers + migrations |
| `electron/preload.ts` | Update | Expose context API |
| `src/stores/contextStore.ts` | Create | Frontend state for context |
| `src/components/shared/ContextHealthCard.tsx` | Create | Health summary card |
| `src/pages/ChangeLog.tsx` | Create | Change log browser page |
| `src/App.tsx` | Update | Add /changelog route |

---

## 11. Testing Checklist

### Database
- [ ] context_changes table created
- [ ] context_file_states table created
- [ ] optimization_suggestions table created
- [ ] Indexes created

### File Watching
- [ ] Detects claude.md changes
- [ ] Detects constitution.md changes
- [ ] Logs changes to database
- [ ] Updates file state (hash, tokens, health)
- [ ] Emits events to renderer

### UI
- [ ] ContextHealthCard displays file states
- [ ] Health indicators (token bar, icons) work
- [ ] ChangeLogPage loads and displays changes
- [ ] Filters work (project, file, source)
- [ ] Search works
- [ ] Diff expansion works
- [ ] Token delta displayed correctly

### Templates
- [ ] Constitution template includes change logging rules
- [ ] claude.md template has section markers
- [ ] Templates are applied during project init

---

## 12. Future Enhancements (Phase 2+)

- **Optimization Pass UI** — Review and apply suggestions
- **Auto-optimization** — Apply high-confidence suggestions automatically
- **Learning → Gotcha flow** — Auto-add learnings to Gotchas section
- **Session Context injection** — Auto-populate ephemeral section
- **CHANGELOG.md parsing** — Read agent's changelog entries into Studio
- **Revert functionality** — One-click revert from change log
- **Notifications** — Alert when health degrades to warning/alert

---

*End of Specification*

# Claude-Mem Integration — Implementation Spec

**Status:** Ready for Implementation  
**Priority:** High (Experiment)  
**Target:** Project Studio Phase 1.5  
**Date:** December 2024

---

## 1. Overview

### Goal

Integrate claude-mem (Claude Code plugin) with Project Studio to enable real-time visibility into agent work and automatic session capture. Studio becomes the "governance view" of claude-mem data.

### What claude-mem Does

claude-mem is a Claude Code plugin that:
- Automatically captures tool usage (file reads, writes, bash commands)
- Compresses observations via AI summarization (~500 tokens each)
- Stores sessions, observations, summaries in SQLite
- Injects relevant context at session start
- Provides search via SQLite FTS5 + Chroma vector DB

### What Studio Adds

- **Project linking** — observations mapped to Studio projects via repo path
- **Real-time feed** — live view of what agent is doing
- **Governance** — compare observations against intent, flag drift
- **Learning extraction** — promote observations to curated Learnings
- **Cross-project context** — learnings that apply everywhere

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLAUDE CODE                               │
│  ┌─────────────┐                                                │
│  │ claude-mem  │ ← Hooks capture observations automatically     │
│  │  (plugin)   │                                                │
│  └──────┬──────┘                                                │
│         │                                                       │
│         ▼                                                       │
│  ~/.claude-mem/claude-mem.db                                    │
└─────────┬───────────────────────────────────────────────────────┘
          │
          │ File watcher (polls or fs.watch)
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROJECT STUDIO                              │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │ ClaudeMemSync   │───►│ Memory Plane    │                    │
│  │ Service         │    │ (observations,  │                    │
│  │                 │    │  sessions)      │                    │
│  └─────────────────┘    └─────────────────┘                    │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 OBSERVATION FEED (UI)                       ││
│  │  Live stream of agent activity, linked to projects          ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Prerequisites

### Install claude-mem

Before implementation, verify claude-mem is installed and working:

```bash
# In Claude Code terminal
> /plugin marketplace add thedotmack/claude-mem
> /plugin install claude-mem

# Restart Claude Code
# Verify database exists:
ls ~/.claude-mem/claude-mem.db
```

### claude-mem Database Location

- **Default path:** `~/.claude-mem/claude-mem.db`
- **Config file:** `~/.claude-mem/settings.json`
- **Web viewer:** http://localhost:37777 (when worker is running)

---

## 3. claude-mem Schema (Read-Only)

We read from claude-mem's database, never write to it. Key tables:

### sessions
```sql
-- Session represents a Claude Code work session
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  project_path TEXT,           -- Repo path (use for project linking)
  started_at DATETIME,
  ended_at DATETIME,
  summary TEXT,                -- AI-generated session summary
  status TEXT                  -- 'active', 'completed'
);
```

### observations
```sql
-- Observation is a compressed snapshot of tool usage
CREATE TABLE observations (
  id TEXT PRIMARY KEY,
  session_id TEXT,
  type TEXT,                   -- 'decision', 'bugfix', 'feature', 'refactor', 'discovery', 'change'
  concept TEXT,                -- 'problem-solution', 'pattern', 'discovery', etc.
  narrative TEXT,              -- AI-compressed summary
  file_path TEXT,              -- File this observation relates to
  raw_content TEXT,            -- Original tool output (if stored)
  created_at DATETIME,
  tokens INTEGER               -- Estimated token count
);
```

### prompts
```sql
-- User prompts within sessions
CREATE TABLE prompts (
  id TEXT PRIMARY KEY,
  session_id TEXT,
  content TEXT,
  created_at DATETIME
);
```

**Note:** Schema may vary by claude-mem version. Inspect actual schema:
```bash
sqlite3 ~/.claude-mem/claude-mem.db ".schema"
```

---

## 4. Data Model Additions

### New Types

Add to `src/types/index.ts`:

```typescript
// ============================================================
// Claude-Mem Integration
// ============================================================

export type ObservationType = 
  | 'decision' 
  | 'bugfix' 
  | 'feature' 
  | 'refactor' 
  | 'discovery' 
  | 'change'

export type ObservationConcept =
  | 'problem-solution'
  | 'pattern'
  | 'discovery'
  | 'architecture'
  | 'debugging'
  | 'implementation'

export interface ClaudeMemSession {
  id: string
  project_path?: string
  started_at?: string
  ended_at?: string
  summary?: string
  status: 'active' | 'completed'
}

export interface ClaudeMemObservation {
  id: string
  session_id: string
  type: ObservationType
  concept?: ObservationConcept
  narrative: string
  file_path?: string
  created_at: string
  tokens?: number
}

// Linked observation (with Studio project context)
export interface LinkedObservation extends ClaudeMemObservation {
  project_id?: string        // Studio project ID (resolved from project_path)
  project_name?: string      // For display
  session_summary?: string   // From parent session
}
```

### Settings Addition

Add to settings schema in `src/types/index.ts`:

```typescript
export interface StudioSettings {
  // ... existing settings
  claude_mem_db_path?: string        // Override default ~/.claude-mem/claude-mem.db
  claude_mem_sync_enabled: boolean   // Toggle sync on/off
  claude_mem_poll_interval: number   // Milliseconds between polls (default: 5000)
}
```

---

## 5. Sync Service

### ClaudeMemSync Service

Create `electron/services/claudeMemSync.ts`:

```typescript
import Database from 'better-sqlite3'
import path from 'path'
import os from 'os'
import fs from 'fs'

interface ClaudeMemSession {
  id: string
  project_path?: string
  started_at?: string
  ended_at?: string
  summary?: string
  status: string
}

interface ClaudeMemObservation {
  id: string
  session_id: string
  type: string
  concept?: string
  narrative: string
  file_path?: string
  created_at: string
  tokens?: number
}

export class ClaudeMemSync {
  private dbPath: string
  private db: Database.Database | null = null
  private lastSyncTime: string = '1970-01-01T00:00:00Z'
  private pollInterval: NodeJS.Timeout | null = null
  private onChange: ((data: { sessions: ClaudeMemSession[], observations: ClaudeMemObservation[] }) => void) | null = null

  constructor(customDbPath?: string) {
    this.dbPath = customDbPath || path.join(os.homedir(), '.claude-mem', 'claude-mem.db')
  }

  /**
   * Check if claude-mem database exists
   */
  exists(): boolean {
    return fs.existsSync(this.dbPath)
  }

  /**
   * Open connection to claude-mem database (read-only)
   */
  connect(): boolean {
    if (!this.exists()) {
      console.warn('claude-mem database not found at:', this.dbPath)
      return false
    }

    try {
      this.db = new Database(this.dbPath, { readonly: true })
      return true
    } catch (error) {
      console.error('Failed to connect to claude-mem database:', error)
      return false
    }
  }

  /**
   * Close database connection
   */
  disconnect(): void {
    if (this.db) {
      this.db.close()
      this.db = null
    }
    this.stopPolling()
  }

  /**
   * Get sessions updated since last sync
   */
  getNewSessions(): ClaudeMemSession[] {
    if (!this.db) return []

    try {
      // Adjust column names based on actual claude-mem schema
      const sessions = this.db.prepare(`
        SELECT id, project_path, started_at, ended_at, summary, status
        FROM sessions
        WHERE started_at > ? OR ended_at > ?
        ORDER BY started_at DESC
        LIMIT 100
      `).all(this.lastSyncTime, this.lastSyncTime) as ClaudeMemSession[]

      return sessions
    } catch (error) {
      console.error('Error fetching sessions:', error)
      return []
    }
  }

  /**
   * Get observations created since last sync
   */
  getNewObservations(): ClaudeMemObservation[] {
    if (!this.db) return []

    try {
      const observations = this.db.prepare(`
        SELECT id, session_id, type, concept, narrative, file_path, created_at, tokens
        FROM observations
        WHERE created_at > ?
        ORDER BY created_at DESC
        LIMIT 500
      `).all(this.lastSyncTime) as ClaudeMemObservation[]

      return observations
    } catch (error) {
      console.error('Error fetching observations:', error)
      return []
    }
  }

  /**
   * Get all sessions for a specific project path
   */
  getSessionsByPath(projectPath: string): ClaudeMemSession[] {
    if (!this.db) return []

    try {
      return this.db.prepare(`
        SELECT id, project_path, started_at, ended_at, summary, status
        FROM sessions
        WHERE project_path = ? OR project_path LIKE ?
        ORDER BY started_at DESC
        LIMIT 50
      `).all(projectPath, `${projectPath}%`) as ClaudeMemSession[]
    } catch (error) {
      console.error('Error fetching sessions by path:', error)
      return []
    }
  }

  /**
   * Get observations for a specific session
   */
  getObservationsBySession(sessionId: string): ClaudeMemObservation[] {
    if (!this.db) return []

    try {
      return this.db.prepare(`
        SELECT id, session_id, type, concept, narrative, file_path, created_at, tokens
        FROM observations
        WHERE session_id = ?
        ORDER BY created_at ASC
      `).all(sessionId) as ClaudeMemObservation[]
    } catch (error) {
      console.error('Error fetching observations by session:', error)
      return []
    }
  }

  /**
   * Get recent observations across all sessions
   */
  getRecentObservations(limit: number = 50): ClaudeMemObservation[] {
    if (!this.db) return []

    try {
      return this.db.prepare(`
        SELECT id, session_id, type, concept, narrative, file_path, created_at, tokens
        FROM observations
        ORDER BY created_at DESC
        LIMIT ?
      `).all(limit) as ClaudeMemObservation[]
    } catch (error) {
      console.error('Error fetching recent observations:', error)
      return []
    }
  }

  /**
   * Search observations by text
   */
  searchObservations(query: string, limit: number = 50): ClaudeMemObservation[] {
    if (!this.db) return []

    try {
      // Try FTS5 search first, fall back to LIKE
      const searchTerm = `%${query}%`
      return this.db.prepare(`
        SELECT id, session_id, type, concept, narrative, file_path, created_at, tokens
        FROM observations
        WHERE narrative LIKE ? OR file_path LIKE ?
        ORDER BY created_at DESC
        LIMIT ?
      `).all(searchTerm, searchTerm, limit) as ClaudeMemObservation[]
    } catch (error) {
      console.error('Error searching observations:', error)
      return []
    }
  }

  /**
   * Start polling for changes
   */
  startPolling(intervalMs: number = 5000, callback: (data: { sessions: ClaudeMemSession[], observations: ClaudeMemObservation[] }) => void): void {
    this.onChange = callback
    
    this.pollInterval = setInterval(() => {
      if (!this.db) {
        this.connect()
      }

      const sessions = this.getNewSessions()
      const observations = this.getNewObservations()

      if (sessions.length > 0 || observations.length > 0) {
        // Update last sync time
        const now = new Date().toISOString()
        this.lastSyncTime = now

        if (this.onChange) {
          this.onChange({ sessions, observations })
        }
      }
    }, intervalMs)
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
   * Get database path
   */
  getDbPath(): string {
    return this.dbPath
  }
}
```

### IPC Handlers

Add to `electron/ipc/index.ts`:

```typescript
import { ClaudeMemSync } from '../services/claudeMemSync'

let claudeMemSync: ClaudeMemSync | null = null

// In registerIpcHandlers function, add:

// Claude-Mem Integration handlers
ipcMain.handle('claudeMem:exists', async () => {
  if (!claudeMemSync) {
    claudeMemSync = new ClaudeMemSync()
  }
  return claudeMemSync.exists()
})

ipcMain.handle('claudeMem:connect', async () => {
  if (!claudeMemSync) {
    claudeMemSync = new ClaudeMemSync()
  }
  return claudeMemSync.connect()
})

ipcMain.handle('claudeMem:disconnect', async () => {
  if (claudeMemSync) {
    claudeMemSync.disconnect()
  }
})

ipcMain.handle('claudeMem:getRecentObservations', async (_event, limit?: number) => {
  if (!claudeMemSync) return []
  return claudeMemSync.getRecentObservations(limit)
})

ipcMain.handle('claudeMem:getSessionsByPath', async (_event, projectPath: string) => {
  if (!claudeMemSync) return []
  return claudeMemSync.getSessionsByPath(projectPath)
})

ipcMain.handle('claudeMem:getObservationsBySession', async (_event, sessionId: string) => {
  if (!claudeMemSync) return []
  return claudeMemSync.getObservationsBySession(sessionId)
})

ipcMain.handle('claudeMem:searchObservations', async (_event, query: string, limit?: number) => {
  if (!claudeMemSync) return []
  return claudeMemSync.searchObservations(query, limit)
})

ipcMain.handle('claudeMem:getDbPath', async () => {
  if (!claudeMemSync) {
    claudeMemSync = new ClaudeMemSync()
  }
  return claudeMemSync.getDbPath()
})
```

### Preload Exposure

Add to `electron/preload.ts`:

```typescript
// In contextBridge.exposeInMainWorld('electron', { ... })
claudeMem: {
  exists: () => ipcRenderer.invoke('claudeMem:exists'),
  connect: () => ipcRenderer.invoke('claudeMem:connect'),
  disconnect: () => ipcRenderer.invoke('claudeMem:disconnect'),
  getRecentObservations: (limit?: number) => ipcRenderer.invoke('claudeMem:getRecentObservations', limit),
  getSessionsByPath: (projectPath: string) => ipcRenderer.invoke('claudeMem:getSessionsByPath', projectPath),
  getObservationsBySession: (sessionId: string) => ipcRenderer.invoke('claudeMem:getObservationsBySession', sessionId),
  searchObservations: (query: string, limit?: number) => ipcRenderer.invoke('claudeMem:searchObservations', query, limit),
  getDbPath: () => ipcRenderer.invoke('claudeMem:getDbPath'),
},
```

### TypeScript Definitions

Add to `src/types/electron.d.ts`:

```typescript
interface ClaudeMemAPI {
  exists: () => Promise<boolean>
  connect: () => Promise<boolean>
  disconnect: () => Promise<void>
  getRecentObservations: (limit?: number) => Promise<ClaudeMemObservation[]>
  getSessionsByPath: (projectPath: string) => Promise<ClaudeMemSession[]>
  getObservationsBySession: (sessionId: string) => Promise<ClaudeMemObservation[]>
  searchObservations: (query: string, limit?: number) => Promise<ClaudeMemObservation[]>
  getDbPath: () => Promise<string>
}

interface ElectronAPI {
  // ... existing
  claudeMem: ClaudeMemAPI
}
```

---

## 6. Frontend Store

Create `src/stores/claudeMemStore.ts`:

```typescript
import { create } from 'zustand'
import { ClaudeMemObservation, ClaudeMemSession, LinkedObservation } from '@/types'
import { useProjectStore } from './projectStore'

interface ClaudeMemStore {
  // State
  isConnected: boolean
  isAvailable: boolean
  observations: LinkedObservation[]
  sessions: ClaudeMemSession[]
  isLoading: boolean
  error: string | null
  dbPath: string | null

  // Actions
  checkAvailability: () => Promise<boolean>
  connect: () => Promise<boolean>
  disconnect: () => Promise<void>
  loadRecentObservations: (limit?: number) => Promise<void>
  loadSessionsForProject: (projectPath: string) => Promise<void>
  loadObservationsForSession: (sessionId: string) => Promise<ClaudeMemObservation[]>
  searchObservations: (query: string) => Promise<void>
  
  // Helpers
  linkObservationsToProjects: (observations: ClaudeMemObservation[]) => LinkedObservation[]
}

export const useClaudeMemStore = create<ClaudeMemStore>((set, get) => ({
  isConnected: false,
  isAvailable: false,
  observations: [],
  sessions: [],
  isLoading: false,
  error: null,
  dbPath: null,

  checkAvailability: async () => {
    try {
      const exists = await window.electron.claudeMem.exists()
      const dbPath = await window.electron.claudeMem.getDbPath()
      set({ isAvailable: exists, dbPath })
      return exists
    } catch (error) {
      set({ isAvailable: false, error: String(error) })
      return false
    }
  },

  connect: async () => {
    set({ isLoading: true, error: null })
    try {
      const connected = await window.electron.claudeMem.connect()
      set({ isConnected: connected, isLoading: false })
      
      if (connected) {
        // Load initial data
        await get().loadRecentObservations(50)
      }
      
      return connected
    } catch (error) {
      set({ isConnected: false, isLoading: false, error: String(error) })
      return false
    }
  },

  disconnect: async () => {
    await window.electron.claudeMem.disconnect()
    set({ isConnected: false, observations: [], sessions: [] })
  },

  loadRecentObservations: async (limit = 50) => {
    set({ isLoading: true })
    try {
      const observations = await window.electron.claudeMem.getRecentObservations(limit)
      const linked = get().linkObservationsToProjects(observations)
      set({ observations: linked, isLoading: false })
    } catch (error) {
      set({ isLoading: false, error: String(error) })
    }
  },

  loadSessionsForProject: async (projectPath: string) => {
    set({ isLoading: true })
    try {
      const sessions = await window.electron.claudeMem.getSessionsByPath(projectPath)
      set({ sessions, isLoading: false })
    } catch (error) {
      set({ isLoading: false, error: String(error) })
    }
  },

  loadObservationsForSession: async (sessionId: string) => {
    try {
      return await window.electron.claudeMem.getObservationsBySession(sessionId)
    } catch (error) {
      console.error('Error loading observations for session:', error)
      return []
    }
  },

  searchObservations: async (query: string) => {
    set({ isLoading: true })
    try {
      const observations = await window.electron.claudeMem.searchObservations(query, 100)
      const linked = get().linkObservationsToProjects(observations)
      set({ observations: linked, isLoading: false })
    } catch (error) {
      set({ isLoading: false, error: String(error) })
    }
  },

  linkObservationsToProjects: (observations: ClaudeMemObservation[]): LinkedObservation[] => {
    const projects = useProjectStore.getState().projects
    
    return observations.map(obs => {
      // Find matching project by repo_path
      // This requires loading sessions to get project_path, then matching
      // For now, return observation without project link
      // TODO: Implement proper linking via session lookup
      return {
        ...obs,
        project_id: undefined,
        project_name: undefined,
      }
    })
  },
}))
```

Update `src/stores/index.ts`:

```typescript
export { useClaudeMemStore } from './claudeMemStore'
```

---

## 7. UI Components

### ObservationFeed Component

Create `src/components/shared/ObservationFeed.tsx`:

```typescript
import { useEffect, useState } from 'react'
import { Activity, AlertCircle, Bug, Lightbulb, FileCode, GitBranch, Zap, RefreshCw } from 'lucide-react'
import { useClaudeMemStore } from '@/stores'
import { LinkedObservation } from '@/types'
import { Card, CardHeader, CardTitle, CardContent, Button } from '@/components/ui'

const TYPE_ICONS: Record<string, React.ReactNode> = {
  decision: <GitBranch className="w-4 h-4 text-purple-400" />,
  bugfix: <Bug className="w-4 h-4 text-red-400" />,
  feature: <Zap className="w-4 h-4 text-green-400" />,
  refactor: <RefreshCw className="w-4 h-4 text-blue-400" />,
  discovery: <Lightbulb className="w-4 h-4 text-yellow-400" />,
  change: <FileCode className="w-4 h-4 text-gray-400" />,
}

const TYPE_COLORS: Record<string, string> = {
  decision: 'border-l-purple-400',
  bugfix: 'border-l-red-400',
  feature: 'border-l-green-400',
  refactor: 'border-l-blue-400',
  discovery: 'border-l-yellow-400',
  change: 'border-l-gray-400',
}

interface ObservationFeedProps {
  limit?: number
  projectPath?: string
  showHeader?: boolean
  compact?: boolean
}

export function ObservationFeed({ 
  limit = 20, 
  projectPath,
  showHeader = true,
  compact = false 
}: ObservationFeedProps) {
  const { 
    observations, 
    isConnected, 
    isAvailable, 
    isLoading,
    error,
    checkAvailability,
    connect,
    loadRecentObservations 
  } = useClaudeMemStore()
  
  const [initialized, setInitialized] = useState(false)

  useEffect(() => {
    const init = async () => {
      const available = await checkAvailability()
      if (available) {
        const connected = await connect()
        if (connected) {
          await loadRecentObservations(limit)
        }
      }
      setInitialized(true)
    }
    init()
  }, [checkAvailability, connect, loadRecentObservations, limit])

  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    
    if (minutes < 1) return 'Just now'
    if (minutes < 60) return `${minutes}m ago`
    if (hours < 24) return `${hours}h ago`
    return date.toLocaleDateString()
  }

  // Filter by project path if provided
  const filteredObservations = projectPath
    ? observations.filter(o => o.file_path?.startsWith(projectPath))
    : observations

  const displayObservations = filteredObservations.slice(0, limit)

  if (!initialized || isLoading) {
    return (
      <Card>
        <CardContent className="py-8 text-center">
          <Activity className="w-6 h-6 mx-auto mb-2 text-text-muted animate-pulse" />
          <p className="text-sm text-text-muted">Loading observations...</p>
        </CardContent>
      </Card>
    )
  }

  if (!isAvailable) {
    return (
      <Card>
        <CardContent className="py-8 text-center">
          <AlertCircle className="w-6 h-6 mx-auto mb-2 text-text-muted" />
          <p className="text-sm text-text-muted mb-2">claude-mem not installed</p>
          <p className="text-xs text-text-muted">
            Install via Claude Code: <code className="bg-elevated px-1 rounded">/plugin marketplace add thedotmack/claude-mem</code>
          </p>
        </CardContent>
      </Card>
    )
  }

  if (!isConnected) {
    return (
      <Card>
        <CardContent className="py-8 text-center">
          <AlertCircle className="w-6 h-6 mx-auto mb-2 text-status-warning" />
          <p className="text-sm text-text-muted mb-2">Could not connect to claude-mem</p>
          <Button variant="ghost" size="sm" onClick={() => connect()}>
            Retry Connection
          </Button>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardContent className="py-8 text-center">
          <AlertCircle className="w-6 h-6 mx-auto mb-2 text-status-error" />
          <p className="text-sm text-text-muted">{error}</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      {showHeader && (
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-4 h-4" />
            Agent Activity
          </CardTitle>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => loadRecentObservations(limit)}
          >
            <RefreshCw className="w-4 h-4" />
          </Button>
        </CardHeader>
      )}
      <CardContent className={showHeader ? '' : 'pt-4'}>
        {displayObservations.length === 0 ? (
          <p className="text-sm text-text-muted text-center py-4">
            No observations yet. Start a Claude Code session to see activity.
          </p>
        ) : (
          <div className="space-y-2">
            {displayObservations.map((obs) => (
              <div
                key={obs.id}
                className={`border-l-2 ${TYPE_COLORS[obs.type] || 'border-l-gray-400'} pl-3 py-2 ${
                  compact ? '' : 'bg-elevated rounded-r-sm'
                }`}
              >
                <div className="flex items-start gap-2">
                  {TYPE_ICONS[obs.type] || <FileCode className="w-4 h-4 text-text-muted" />}
                  <div className="flex-1 min-w-0">
                    <p className={`text-text-primary ${compact ? 'text-sm' : ''} line-clamp-2`}>
                      {obs.narrative}
                    </p>
                    <div className="flex items-center gap-2 mt-1 text-xs text-text-muted">
                      <span className="capitalize">{obs.type}</span>
                      {obs.file_path && (
                        <>
                          <span>•</span>
                          <span className="truncate max-w-[200px]" title={obs.file_path}>
                            {obs.file_path.split('/').pop()}
                          </span>
                        </>
                      )}
                      <span>•</span>
                      <span>{formatTime(obs.created_at)}</span>
                      {obs.tokens && (
                        <>
                          <span>•</span>
                          <span>{obs.tokens} tokens</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

Update `src/components/shared/index.ts`:

```typescript
export { ObservationFeed } from './ObservationFeed'
```

---

## 8. Dashboard Integration

Update `src/pages/Dashboard.tsx` to include the observation feed:

Add import:
```typescript
import { ObservationFeed } from '@/components/shared'
```

Add to the dashboard layout (suggested placement: right column or below activity feed):

```tsx
{/* Agent Activity Feed */}
<div className="col-span-1">
  <ObservationFeed limit={15} compact />
</div>
```

---

## 9. Project View Integration

Update `src/pages/ProjectView.tsx` to show project-specific observations:

Add to the project view (suggested: new tab or section):

```tsx
{/* Project Observations */}
{project.repo_path && (
  <Card>
    <CardHeader>
      <CardTitle>Recent Agent Activity</CardTitle>
    </CardHeader>
    <CardContent>
      <ObservationFeed 
        projectPath={project.repo_path} 
        limit={10} 
        showHeader={false}
        compact
      />
    </CardContent>
  </Card>
)}
```

---

## 10. Files Summary

| File | Action | Description |
|------|--------|-------------|
| `src/types/index.ts` | Modify | Add ClaudeMemSession, ClaudeMemObservation, LinkedObservation types |
| `src/types/electron.d.ts` | Modify | Add ClaudeMemAPI interface |
| `electron/services/claudeMemSync.ts` | Create | Service to read claude-mem database |
| `electron/ipc/index.ts` | Modify | Add claude-mem IPC handlers |
| `electron/preload.ts` | Modify | Expose claudeMem API |
| `src/stores/claudeMemStore.ts` | Create | Frontend store for claude-mem data |
| `src/stores/index.ts` | Modify | Export claudeMemStore |
| `src/components/shared/ObservationFeed.tsx` | Create | Live observation feed component |
| `src/components/shared/index.ts` | Modify | Export ObservationFeed |
| `src/pages/Dashboard.tsx` | Modify | Add observation feed to dashboard |
| `src/pages/ProjectView.tsx` | Modify | Add project-specific observations |

---

## 11. Testing Checklist

### Prerequisites
- [ ] claude-mem plugin installed in Claude Code
- [ ] claude-mem database exists at `~/.claude-mem/claude-mem.db`
- [ ] claude-mem worker running (check http://localhost:37777)

### Integration Tests
- [ ] Studio detects claude-mem availability
- [ ] Studio connects to claude-mem database (read-only)
- [ ] Recent observations load correctly
- [ ] Observations display with correct type icons
- [ ] Time formatting works (just now, Xm ago, Xh ago)
- [ ] Refresh button reloads observations
- [ ] Project-specific filtering works (when repo_path matches)
- [ ] Search finds observations by narrative text
- [ ] No crashes when claude-mem is not installed
- [ ] Graceful error handling when database is locked

### Performance
- [ ] Initial load < 500ms
- [ ] Refresh < 200ms
- [ ] No memory leaks on repeated refreshes

---

## 12. Future Enhancements (Not in This Spec)

These are deferred for later phases:

- **Real-time polling** — Live updates without manual refresh
- **Drift detection** — Compare observations against project intent
- **Learning extraction** — "Promote to Learning" button on observations
- **Session timeline** — Visual timeline of observations within a session
- **Observation details modal** — Expand to see full context
- **Cross-project search** — Search observations across all projects
- **Export observations** — Export as markdown for documentation
- **Bidirectional sync** — Push context from Studio to claude-mem

---

## 13. Schema Discovery Script

Since claude-mem's schema may vary, include this utility to inspect the actual schema:

```bash
#!/bin/bash
# scripts/inspect-claude-mem-schema.sh

CLAUDE_MEM_DB="${HOME}/.claude-mem/claude-mem.db"

if [ ! -f "$CLAUDE_MEM_DB" ]; then
  echo "claude-mem database not found at $CLAUDE_MEM_DB"
  exit 1
fi

echo "=== claude-mem Schema ==="
echo ""
sqlite3 "$CLAUDE_MEM_DB" ".schema"

echo ""
echo "=== Table Row Counts ==="
for table in $(sqlite3 "$CLAUDE_MEM_DB" ".tables"); do
  count=$(sqlite3 "$CLAUDE_MEM_DB" "SELECT COUNT(*) FROM $table")
  echo "$table: $count rows"
done

echo ""
echo "=== Sample Observation ==="
sqlite3 "$CLAUDE_MEM_DB" "SELECT * FROM observations LIMIT 1" 2>/dev/null || echo "No observations table found"

echo ""
echo "=== Sample Session ==="
sqlite3 "$CLAUDE_MEM_DB" "SELECT * FROM sessions LIMIT 1" 2>/dev/null || echo "No sessions table found"
```

Run this before implementation to confirm actual schema matches spec assumptions.

---

*End of Implementation Spec*

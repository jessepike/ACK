# Learnings Feature — Implementation Spec

**Status:** Ready for Implementation  
**Priority:** High  
**Target:** Project Studio Phase 1.5  
**Date:** December 2024

---

## 1. Overview

### What Are Learnings?

Learnings capture hard-won knowledge from development sessions — gotchas, solutions, patterns that shouldn't be forgotten. Unlike Sessions (work logs) or Decisions (architectural choices), Learnings are **retrievable knowledge** meant to prevent repeated mistakes and surface relevant context for future work.

### Example Learning

```
Title: Railway env vars need NIXPACKS_ prefix
Problem: Railway couldn't see env vars set in dashboard. App failed to start. Spent 2+ hours debugging with no clear error messages.
Solution: Railway with Nixpacks requires NIXPACKS_ prefix for build-time env vars. Runtime vars work without prefix. Check Railway docs for buildpack-specific requirements.
Tags: railway, deployment, env-vars, nixpacks
```

### Why This Matters

- **Human memory gaps:** After painful debugging sessions, knowledge lives only in chat logs or your head
- **Agent context gaps:** New agents don't know what previous agents learned
- **Cross-project value:** Some learnings apply everywhere (deployment gotchas, library quirks)

---

## 2. Data Model

### TypeScript Type

Add to `src/types/index.ts`:

```typescript
export interface Learning {
  id: string
  project_id?: string        // Optional - null for cross-project learnings
  cycle_id?: string          // Optional - which cycle spawned this
  session_id?: string        // Optional - source session reference
  
  // Core content
  title: string              // Short summary (< 100 chars ideal)
  problem: string            // What went wrong / what was hard
  solution: string           // What worked / the actual learning
  
  // Retrieval
  tags: string[]             // Stored as JSON string in DB, parsed on read
  
  // Timestamps
  created_at: string
  updated_at: string
}
```

### Database Schema

Add migration to `electron/ipc/index.ts` in the `runMigrations` function:

```typescript
// Migration: Add learnings table
const learningsTableExists = database.prepare(
  "SELECT name FROM sqlite_master WHERE type='table' AND name='learnings'"
).get()

if (!learningsTableExists) {
  database.exec(`
    CREATE TABLE learnings (
      id TEXT PRIMARY KEY,
      project_id TEXT REFERENCES projects(id) ON DELETE SET NULL,
      cycle_id TEXT REFERENCES cycles(id) ON DELETE SET NULL,
      session_id TEXT REFERENCES sessions(id) ON DELETE SET NULL,
      title TEXT NOT NULL,
      problem TEXT NOT NULL,
      solution TEXT NOT NULL,
      tags TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX idx_learnings_project ON learnings(project_id);
    CREATE INDEX idx_learnings_created ON learnings(created_at);
  `)
  console.log('Migration: Created learnings table')
}
```

---

## 3. Store Implementation

Create `src/stores/learningStore.ts`:

```typescript
import { create } from 'zustand'
import { Learning } from '@/types'

// Helper to generate IDs (same pattern as other stores)
const generateId = () => crypto.randomUUID()

interface LearningFilters {
  projectId?: string
  tags?: string[]
  search?: string
}

interface LearningStore {
  // State
  learnings: Learning[]
  isLoading: boolean
  error: string | null
  
  // Actions
  loadLearnings: (filters?: LearningFilters) => Promise<void>
  getLearningById: (id: string) => Learning | undefined
  getLearningsByProject: (projectId: string) => Learning[]
  getLearningsByTags: (tags: string[]) => Learning[]
  searchLearnings: (query: string) => Learning[]
  
  createLearning: (learning: Omit<Learning, 'id' | 'created_at' | 'updated_at'>) => Promise<Learning>
  updateLearning: (id: string, updates: Partial<Learning>) => Promise<void>
  deleteLearning: (id: string) => Promise<void>
  
  // Tag helpers
  getAllTags: () => string[]
}

export const useLearningStore = create<LearningStore>((set, get) => ({
  learnings: [],
  isLoading: false,
  error: null,

  loadLearnings: async (filters?: LearningFilters) => {
    set({ isLoading: true, error: null })
    try {
      let sql = 'SELECT * FROM learnings'
      const conditions: string[] = []
      const params: unknown[] = []

      if (filters?.projectId) {
        conditions.push('project_id = ?')
        params.push(filters.projectId)
      }

      if (filters?.tags && filters.tags.length > 0) {
        // SQLite JSON search - tags stored as JSON array string
        const tagConditions = filters.tags.map(() => "tags LIKE ?")
        conditions.push(`(${tagConditions.join(' OR ')})`)
        filters.tags.forEach(tag => params.push(`%"${tag}"%`))
      }

      if (filters?.search) {
        conditions.push('(title LIKE ? OR problem LIKE ? OR solution LIKE ?)')
        const searchTerm = `%${filters.search}%`
        params.push(searchTerm, searchTerm, searchTerm)
      }

      if (conditions.length > 0) {
        sql += ' WHERE ' + conditions.join(' AND ')
      }

      sql += ' ORDER BY created_at DESC'

      const rows = await window.electron.db.all(sql, params) as Array<Learning & { tags: string }>
      
      // Parse tags JSON
      const learnings = rows.map(row => ({
        ...row,
        tags: row.tags ? JSON.parse(row.tags) : []
      }))

      set({ learnings, isLoading: false })
    } catch (error) {
      set({ error: String(error), isLoading: false })
    }
  },

  getLearningById: (id: string) => {
    return get().learnings.find(l => l.id === id)
  },

  getLearningsByProject: (projectId: string) => {
    return get().learnings.filter(l => l.project_id === projectId)
  },

  getLearningsByTags: (tags: string[]) => {
    return get().learnings.filter(l => 
      tags.some(tag => l.tags.includes(tag))
    )
  },

  searchLearnings: (query: string) => {
    const lower = query.toLowerCase()
    return get().learnings.filter(l =>
      l.title.toLowerCase().includes(lower) ||
      l.problem.toLowerCase().includes(lower) ||
      l.solution.toLowerCase().includes(lower) ||
      l.tags.some(t => t.toLowerCase().includes(lower))
    )
  },

  createLearning: async (learning) => {
    const id = generateId()
    const now = new Date().toISOString()
    
    const newLearning: Learning = {
      ...learning,
      id,
      created_at: now,
      updated_at: now,
    }

    await window.electron.db.run(
      `INSERT INTO learnings (id, project_id, cycle_id, session_id, title, problem, solution, tags, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        id,
        learning.project_id || null,
        learning.cycle_id || null,
        learning.session_id || null,
        learning.title,
        learning.problem,
        learning.solution,
        JSON.stringify(learning.tags || []),
        now,
        now
      ]
    )

    set(state => ({ learnings: [newLearning, ...state.learnings] }))
    return newLearning
  },

  updateLearning: async (id: string, updates: Partial<Learning>) => {
    const now = new Date().toISOString()
    
    // Build dynamic update query
    const fields: string[] = ['updated_at = ?']
    const params: unknown[] = [now]

    if (updates.title !== undefined) {
      fields.push('title = ?')
      params.push(updates.title)
    }
    if (updates.problem !== undefined) {
      fields.push('problem = ?')
      params.push(updates.problem)
    }
    if (updates.solution !== undefined) {
      fields.push('solution = ?')
      params.push(updates.solution)
    }
    if (updates.tags !== undefined) {
      fields.push('tags = ?')
      params.push(JSON.stringify(updates.tags))
    }
    if (updates.project_id !== undefined) {
      fields.push('project_id = ?')
      params.push(updates.project_id || null)
    }

    params.push(id)

    await window.electron.db.run(
      `UPDATE learnings SET ${fields.join(', ')} WHERE id = ?`,
      params
    )

    set(state => ({
      learnings: state.learnings.map(l =>
        l.id === id ? { ...l, ...updates, updated_at: now } : l
      )
    }))
  },

  deleteLearning: async (id: string) => {
    await window.electron.db.run('DELETE FROM learnings WHERE id = ?', [id])
    set(state => ({
      learnings: state.learnings.filter(l => l.id !== id)
    }))
  },

  getAllTags: () => {
    const tagSet = new Set<string>()
    get().learnings.forEach(l => l.tags.forEach(t => tagSet.add(t)))
    return Array.from(tagSet).sort()
  },
}))
```

Update `src/stores/index.ts` to export the new store:

```typescript
export { useLearningStore } from './learningStore'
```

---

## 4. Memory Search Hook Update

Update `src/hooks/useMemorySearch.ts` to include learnings:

```typescript
import { useState, useEffect, useMemo } from 'react'
import { useSessionStore, useDecisionStore, useLearningStore } from '@/stores'
import { Session, Decision, Learning } from '@/types'

export type MemoryType = 'session' | 'decision' | 'learning'

export interface MemoryItem {
  id: string
  type: MemoryType
  title: string
  timestamp: string
  projectId?: string
  data: Session | Decision | Learning
}

interface MemoryFilters {
  types: MemoryType[]
  projectId?: string
  dateRange: 'week' | 'month' | 'all'
  tags?: string[]  // New: filter by tags (primarily for learnings)
}

export function useMemorySearch() {
  const { sessions, loadSessions } = useSessionStore()
  const { decisions, loadDecisions } = useDecisionStore()
  const { learnings, loadLearnings, getAllTags } = useLearningStore()
  
  const [query, setQuery] = useState('')
  const [filters, setFilters] = useState<MemoryFilters>({
    types: ['session', 'decision', 'learning'],
    dateRange: 'all',
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      setIsLoading(true)
      await Promise.all([
        loadSessions(),
        loadDecisions(),
        loadLearnings(),
      ])
      setIsLoading(false)
    }
    load()
  }, [loadSessions, loadDecisions, loadLearnings])

  const items = useMemo(() => {
    const result: MemoryItem[] = []
    const now = new Date()
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
    const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)

    const isInDateRange = (dateStr: string) => {
      if (filters.dateRange === 'all') return true
      const date = new Date(dateStr)
      if (filters.dateRange === 'week') return date >= weekAgo
      if (filters.dateRange === 'month') return date >= monthAgo
      return true
    }

    const matchesQuery = (item: Session | Decision | Learning) => {
      if (!query) return true
      const lower = query.toLowerCase()
      if ('summary' in item) {
        // Session
        return item.title.toLowerCase().includes(lower) ||
               item.summary?.toLowerCase().includes(lower)
      } else if ('rationale' in item) {
        // Decision
        return item.title.toLowerCase().includes(lower) ||
               item.rationale?.toLowerCase().includes(lower)
      } else if ('problem' in item) {
        // Learning
        return item.title.toLowerCase().includes(lower) ||
               item.problem.toLowerCase().includes(lower) ||
               item.solution.toLowerCase().includes(lower) ||
               item.tags.some(t => t.toLowerCase().includes(lower))
      }
      return false
    }

    const matchesProject = (projectId?: string) => {
      if (!filters.projectId) return true
      return projectId === filters.projectId
    }

    const matchesTags = (item: Session | Decision | Learning) => {
      if (!filters.tags || filters.tags.length === 0) return true
      if ('tags' in item) {
        return filters.tags.some(tag => item.tags.includes(tag))
      }
      return true
    }

    // Sessions
    if (filters.types.includes('session')) {
      sessions
        .filter(s => isInDateRange(s.created_at) && matchesQuery(s) && matchesProject(s.project_id))
        .forEach(s => result.push({
          id: s.id,
          type: 'session',
          title: s.title,
          timestamp: s.created_at,
          projectId: s.project_id,
          data: s,
        }))
    }

    // Decisions
    if (filters.types.includes('decision')) {
      decisions
        .filter(d => isInDateRange(d.created_at) && matchesQuery(d) && matchesProject(d.project_id))
        .forEach(d => result.push({
          id: d.id,
          type: 'decision',
          title: d.title,
          timestamp: d.created_at,
          projectId: d.project_id,
          data: d,
        }))
    }

    // Learnings
    if (filters.types.includes('learning')) {
      learnings
        .filter(l => isInDateRange(l.created_at) && matchesQuery(l) && matchesProject(l.project_id) && matchesTags(l))
        .forEach(l => result.push({
          id: l.id,
          type: 'learning',
          title: l.title,
          timestamp: l.created_at,
          projectId: l.project_id,
          data: l,
        }))
    }

    // Sort by timestamp descending
    return result.sort((a, b) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    )
  }, [sessions, decisions, learnings, query, filters])

  return {
    items,
    isLoading,
    query,
    search: setQuery,
    filters,
    setFilters: (updates: Partial<MemoryFilters>) => 
      setFilters(prev => ({ ...prev, ...updates })),
    availableTags: getAllTags(),
  }
}
```

---

## 5. UI Components

### 5.1 CaptureLearningModal

Create `src/components/modals/CaptureLearningModal.tsx`:

```typescript
import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { Button } from '@/components/ui'
import { useLearningStore, useProjectStore, useCycleStore, useSessionStore } from '@/stores'

interface CaptureLearningModalProps {
  isOpen: boolean
  onClose: () => void
  projectId?: string
  cycleId?: string
  sessionId?: string
  // Pre-fill from session summary if provided
  prefillProblem?: string
  prefillSolution?: string
}

export function CaptureLearningModal({
  isOpen,
  onClose,
  projectId,
  cycleId,
  sessionId,
  prefillProblem = '',
  prefillSolution = '',
}: CaptureLearningModalProps) {
  const { createLearning } = useLearningStore()
  const { projects, loadProjects } = useProjectStore()
  const { cycles, loadCycles } = useCycleStore()
  const { sessions, loadSessions } = useSessionStore()

  const [title, setTitle] = useState('')
  const [problem, setProblem] = useState(prefillProblem)
  const [solution, setSolution] = useState(prefillSolution)
  const [tagsInput, setTagsInput] = useState('')
  const [selectedProjectId, setSelectedProjectId] = useState<string | undefined>(projectId)
  const [selectedCycleId, setSelectedCycleId] = useState<string | undefined>(cycleId)
  const [selectedSessionId, setSelectedSessionId] = useState<string | undefined>(sessionId)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    loadProjects()
    loadCycles()
    loadSessions()
  }, [loadProjects, loadCycles, loadSessions])

  // Reset form when modal opens
  useEffect(() => {
    if (isOpen) {
      setTitle('')
      setProblem(prefillProblem)
      setSolution(prefillSolution)
      setTagsInput('')
      setSelectedProjectId(projectId)
      setSelectedCycleId(cycleId)
      setSelectedSessionId(sessionId)
    }
  }, [isOpen, projectId, cycleId, sessionId, prefillProblem, prefillSolution])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim() || !problem.trim() || !solution.trim()) return

    setIsSaving(true)
    try {
      // Parse tags from comma-separated input
      const tags = tagsInput
        .split(',')
        .map(t => t.trim().toLowerCase())
        .filter(t => t.length > 0)

      await createLearning({
        title: title.trim(),
        problem: problem.trim(),
        solution: solution.trim(),
        tags,
        project_id: selectedProjectId || undefined,
        cycle_id: selectedCycleId || undefined,
        session_id: selectedSessionId || undefined,
      })

      onClose()
    } finally {
      setIsSaving(false)
    }
  }

  // Filter cycles and sessions by selected project
  const filteredCycles = selectedProjectId 
    ? cycles.filter(c => c.project_id === selectedProjectId)
    : cycles
  const filteredSessions = selectedProjectId
    ? sessions.filter(s => s.project_id === selectedProjectId)
    : sessions

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="relative bg-surface border border-border-default rounded-sm w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-4 border-b border-border-default">
          <h2 className="text-lg font-semibold text-text-primary">Capture Learning</h2>
          <button onClick={onClose} className="text-text-muted hover:text-text-primary">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-text-secondary mb-1">
              Title <span className="text-status-error">*</span>
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Railway env vars need NIXPACKS_ prefix"
              className="w-full h-9 px-3 rounded-sm bg-input border border-border-default text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-accent-primary/20 focus:border-border-focus"
              required
            />
            <p className="text-xs text-text-muted mt-1">Short summary of what you learned</p>
          </div>

          {/* Problem */}
          <div>
            <label className="block text-sm font-medium text-text-secondary mb-1">
              What was the problem? <span className="text-status-error">*</span>
            </label>
            <textarea
              value={problem}
              onChange={(e) => setProblem(e.target.value)}
              placeholder="Railway couldn't see env vars set in dashboard. App failed to start. Spent 2+ hours debugging..."
              rows={3}
              className="w-full px-3 py-2 rounded-sm bg-input border border-border-default text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-accent-primary/20 focus:border-border-focus resize-none"
              required
            />
          </div>

          {/* Solution */}
          <div>
            <label className="block text-sm font-medium text-text-secondary mb-1">
              What's the solution / learning? <span className="text-status-error">*</span>
            </label>
            <textarea
              value={solution}
              onChange={(e) => setSolution(e.target.value)}
              placeholder="Railway with Nixpacks requires NIXPACKS_ prefix for build-time env vars. Runtime vars work without prefix."
              rows={3}
              className="w-full px-3 py-2 rounded-sm bg-input border border-border-default text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-accent-primary/20 focus:border-border-focus resize-none"
              required
            />
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-text-secondary mb-1">
              Tags
            </label>
            <input
              type="text"
              value={tagsInput}
              onChange={(e) => setTagsInput(e.target.value)}
              placeholder="railway, deployment, env-vars, nixpacks"
              className="w-full h-9 px-3 rounded-sm bg-input border border-border-default text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-accent-primary/20 focus:border-border-focus"
            />
            <p className="text-xs text-text-muted mt-1">Comma-separated for retrieval</p>
          </div>

          {/* Project (Optional) */}
          <div>
            <label className="block text-sm font-medium text-text-secondary mb-1">
              Project (optional)
            </label>
            <select
              value={selectedProjectId || ''}
              onChange={(e) => {
                setSelectedProjectId(e.target.value || undefined)
                setSelectedCycleId(undefined)
                setSelectedSessionId(undefined)
              }}
              className="w-full h-9 px-3 rounded-sm bg-input border border-border-default text-text-secondary text-sm"
            >
              <option value="">Cross-project (applies everywhere)</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </div>

          {/* Cycle (Optional) */}
          {selectedProjectId && filteredCycles.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">
                From Cycle (optional)
              </label>
              <select
                value={selectedCycleId || ''}
                onChange={(e) => setSelectedCycleId(e.target.value || undefined)}
                className="w-full h-9 px-3 rounded-sm bg-input border border-border-default text-text-secondary text-sm"
              >
                <option value="">None</option>
                {filteredCycles.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Session (Optional) */}
          {selectedProjectId && filteredSessions.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">
                From Session (optional)
              </label>
              <select
                value={selectedSessionId || ''}
                onChange={(e) => setSelectedSessionId(e.target.value || undefined)}
                className="w-full h-9 px-3 rounded-sm bg-input border border-border-default text-text-secondary text-sm"
              >
                <option value="">None</option>
                {filteredSessions.slice(0, 20).map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.title}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-2 pt-4 border-t border-border-default">
            <Button variant="ghost" onClick={onClose} disabled={isSaving}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSaving || !title.trim() || !problem.trim() || !solution.trim()}>
              {isSaving ? 'Saving...' : 'Save Learning'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
```

Update `src/components/modals/index.ts`:

```typescript
export { CaptureLearningModal } from './CaptureLearningModal'
```

### 5.2 Memory.tsx Updates

Update `src/pages/Memory.tsx` to include learnings:

**Key changes:**
1. Add 'learning' checkbox to type filters
2. Add tags filter dropdown (populated from `availableTags`)
3. Add `renderLearningItem` function
4. Add CaptureLearningModal to "+ New" menu
5. Handle learning click (navigate to detail or show modal)

Add this render function alongside the existing ones:

```typescript
const renderLearningItem = (item: MemoryItem) => {
  const learning = item.data as Learning
  return (
    <div className="flex items-start gap-3">
      <div className="w-8 h-8 rounded-full bg-status-success/10 flex items-center justify-center flex-shrink-0">
        <Lightbulb className="w-4 h-4 text-status-success" />
      </div>
      <div className="flex-1 min-w-0">
        <h4 className="font-medium text-text-primary">{learning.title}</h4>
        <p className="text-sm text-text-secondary mt-1 line-clamp-2">{learning.problem}</p>
        <div className="flex items-center gap-2 mt-2 flex-wrap">
          {learning.tags.slice(0, 4).map(tag => (
            <span 
              key={tag}
              className="text-xs px-2 py-0.5 rounded-full bg-elevated text-text-muted"
            >
              {tag}
            </span>
          ))}
          {learning.tags.length > 4 && (
            <span className="text-xs text-text-muted">+{learning.tags.length - 4}</span>
          )}
          <span className="text-xs text-text-muted ml-auto">{formatDate(learning.created_at)}</span>
        </div>
      </div>
    </div>
  )
}
```

Import `Lightbulb` from lucide-react.

---

## 6. Activity Integration

Update `src/stores/activityStore.ts` to add learning activity type:

In the `ActivityType` type (in `src/types/index.ts`):

```typescript
export type ActivityType =
  | 'session_captured'
  | 'decision_recorded'
  | 'learning_captured'  // Add this
  | 'cycle_started'
  | 'cycle_completed'
  | 'drift_detected'
  | 'drift_resolved'
  | 'context_updated'
```

In the `learningStore.createLearning` function, after successfully saving, log activity:

```typescript
// At the end of createLearning, before return:
import { useActivityStore } from './activityStore'

// ... in createLearning:
useActivityStore.getState().logActivity({
  activity_type: 'learning_captured',
  title: `Learning: ${learning.title}`,
  project_id: learning.project_id,
  reference_type: 'learning',
  reference_id: id,
})
```

---

## 7. Files Summary

| File | Action | Description |
|------|--------|-------------|
| `src/types/index.ts` | Modify | Add `Learning` type, add `'learning_captured'` to ActivityType |
| `electron/ipc/index.ts` | Modify | Add migration for `learnings` table |
| `src/stores/learningStore.ts` | Create | Full CRUD store with tag search |
| `src/stores/index.ts` | Modify | Export learningStore |
| `src/hooks/useMemorySearch.ts` | Modify | Add 'learning' type support, tag filtering |
| `src/components/modals/CaptureLearningModal.tsx` | Create | Modal for capturing learnings |
| `src/components/modals/index.ts` | Modify | Export CaptureLearningModal |
| `src/pages/Memory.tsx` | Modify | Add learning type filter, tags filter, render learnings |

---

## 8. Testing Checklist

After implementation, verify:

- [ ] `learnings` table created on app start (check SQLite)
- [ ] Can create learning with all fields
- [ ] Can create cross-project learning (no project selected)
- [ ] Tags stored as JSON, parsed correctly on read
- [ ] Memory page shows learnings alongside sessions/decisions
- [ ] Type filter works (can show only learnings)
- [ ] Tag filter works (filter by selected tags)
- [ ] Search finds learnings by title, problem, solution, tags
- [ ] Activity feed shows "Learning captured" entries
- [ ] Date filter works for learnings
- [ ] Project filter works for learnings
- [ ] Can edit learning (title, problem, solution, tags)
- [ ] Can delete learning

---

## 9. Future Enhancements (Not in This Spec)

These are intentionally deferred:

- **LearningDetail page:** Full page view with edit capability (start with modal view)
- **Context surfacing:** Auto-suggest learnings when starting cycles based on tech stack tags
- **Import from session:** "Extract learnings" button on SessionDetail that pre-fills the modal
- **Tag autocomplete:** Suggest existing tags while typing
- **Learning validation:** LLM-as-judge to rate learning quality
- **Export:** Export learnings as markdown for claude.md injection

---

*End of Implementation Spec*

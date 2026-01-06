# Memory System - Feature Summary

## Overview
Comprehensive knowledge management system that captures and organizes three types of project memory: Sessions (work periods), Decisions (architectural choices), and Learnings (problem-solution pairs). Enables searchable, filterable access to project knowledge with seamless integration with Agent Activity observations.

---

## Capabilities

### Memory Types

#### Sessions 🕐
- **Capture work sessions** with title, summary, duration
- **Track files changed** during the session
- **Link to projects and cycles** for context
- **Navigate to detail view** with full session context

#### Decisions ⚖️
- **Record architectural decisions** with title and rationale
- **Document context** around why choices were made
- **Link to projects and cycles** for traceability
- **Searchable decision history** across all projects

#### Learnings 💡
- **Store problem-solution pairs** with descriptive tags
- **Promote from Agent Activity** via ↑ button on observations
- **"From Agent" badge** for learnings promoted from observations
- **Expandable cards** showing full solution details
- **Cross-project knowledge** searchable and reusable

### Search & Discovery
- **Full-text search** across all memory types
- **Filter by type** (session, decision, learning)
- **Filter by project** or view across all projects
- **Filter by date range** (last 7 days, 30 days, all time)
- **Filter by tags** with multi-select support
- **Clear tag filters** with one click

### Integration with Agent Activity
- **Real-time observations** from claude-mem
- **One-click promotion** to permanent learning
- **Pre-filled learning form** with observation data
- **Source tracking** via `source_observation_id`
- **Bidirectional context** between live activity and permanent knowledge

---

## UI Components

### Memory Card (Project View)
Location: Project View → Memory section

```
┌─────────────────────────────────────┐
│ 🧠 Memory               [View All]  │
├─────────────────────────────────────┤
│ No decisions or sessions recorded   │
│                                     │
│ Capture sessions and decisions to   │
│ build project memory.               │
└─────────────────────────────────────┘
```

### Memory Page
Location: Navigation → Memory

```
┌─────────────────────────────────────────────────────────┐
│ [🔍 Search memory...              ] [+ New ▼]           │
├──────────────┬──────────────────────────────────────────┤
│ Filters      │ Results                                  │
│              │                                          │
│ Type         │ ┌──────────────────────────────────────┐ │
│ ☑ Sessions   │ │ 🕐 Session Title                     │ │
│ ☑ Decisions  │ │    Summary text here...              │ │
│ ☑ Learnings  │ │    Dec 28 • 45m • 3 files            │ │
│              │ └──────────────────────────────────────┘ │
│ Project      │                                          │
│ [All ▼]      │ ┌──────────────────────────────────────┐ │
│              │ │ ⚖️ Decision Title                     │ │
│ Date Range   │ │    Rationale text here...            │ │
│ [Week ▼]     │ │    Dec 27                            │ │
│              │ └──────────────────────────────────────┘ │
│ Tags         │                                          │
│ [bug] [feat] │ ┌──────────────────────────────────────┐ │
│              │ │ 💡 Learning Title [From Agent]       │ │
│              │ │    Problem description...            │ │
│              │ │    [bug] [typescript]  Dec 26        │ │
│              │ └──────────────────────────────────────┘ │
└──────────────┴──────────────────────────────────────────┘
```

### CaptureSessionModal
Triggered by: New → Capture Session

```
┌─────────────────────────────────────────────┐
│ Capture Session                         ✕   │
├─────────────────────────────────────────────┤
│ Project: [Project Studio ▼]                 │
│                                             │
│ Title (required)                            │
│ [                                        ]  │
│                                             │
│ Summary (required)                          │
│ ┌─────────────────────────────────────────┐ │
│ │ What did you work on?                   │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Duration: [45] minutes                      │
│                                             │
│ Files Changed (optional)                    │
│ [src/stores/memoryStore.ts, ...]            │
│                                             │
│ Tags (optional)                             │
│ [feature, bugfix, refactor]                 │
│                                             │
│                    [Cancel] [Capture]       │
└─────────────────────────────────────────────┘
```

### RecordDecisionModal
Triggered by: New → Record Decision

```
┌─────────────────────────────────────────────┐
│ Record Decision                         ✕   │
├─────────────────────────────────────────────┤
│ Project: [Project Studio ▼]                 │
│                                             │
│ Title (required)                            │
│ [                                        ]  │
│                                             │
│ Decision (required)                         │
│ ┌─────────────────────────────────────────┐ │
│ │ What was decided?                       │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Rationale (required)                        │
│ ┌─────────────────────────────────────────┐ │
│ │ Why was this decision made?             │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Context (optional)                          │
│ ┌─────────────────────────────────────────┐ │
│ │ Additional context, constraints...      │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│                    [Cancel] [Record]        │
└─────────────────────────────────────────────┘
```

### CaptureLearningModal
Triggered by: New → Capture Learning OR ↑ button on Agent Activity

```
┌─────────────────────────────────────────────┐
│ Capture Learning                        ✕   │
├─────────────────────────────────────────────┤
│ Project: [Project Studio ▼]                 │
│                                             │
│ Title (required)                            │
│ [                                        ]  │
│                                             │
│ Problem (required)                          │
│ ┌─────────────────────────────────────────┐ │
│ │ What problem did you encounter?         │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Solution (required)                         │
│ ┌─────────────────────────────────────────┐ │
│ │ How did you solve it?                   │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Tags (comma-separated)                      │
│ [typescript, react, hooks]                  │
│                                             │
│                    [Cancel] [Capture]       │
└─────────────────────────────────────────────┘
```

Note: When promoted from Agent Activity, the form is pre-filled:
- Title: observation concept or first line
- Problem: observation narrative
- Tags: observation type (e.g., "bugfix")
- Solution: empty (user fills in)

---

## Technical Implementation

### Database Schema (studio.db)

#### Sessions Table
```sql
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  cycle_id TEXT,
  title TEXT NOT NULL,
  summary TEXT,
  duration_minutes INTEGER,
  files_changed TEXT, -- JSON array
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects(id),
  FOREIGN KEY (cycle_id) REFERENCES cycles(id)
);
```

#### Decisions Table
```sql
CREATE TABLE decisions (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  cycle_id TEXT,
  title TEXT NOT NULL,
  decision TEXT NOT NULL,
  rationale TEXT NOT NULL,
  context TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects(id),
  FOREIGN KEY (cycle_id) REFERENCES cycles(id)
);
```

#### Learnings Table
```sql
CREATE TABLE learnings (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  title TEXT NOT NULL,
  problem TEXT NOT NULL,
  solution TEXT NOT NULL,
  tags TEXT NOT NULL, -- JSON array
  source_observation_id TEXT, -- Links to claude-mem observation
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### IPC Handlers (electron/ipc/index.ts)

| Handler | Parameters | Description |
|---------|------------|-------------|
| `db:sessions:create` | projectId, cycleId?, title, summary, duration, filesChanged | Create session |
| `db:sessions:getAll` | projectId?, limit? | Get all sessions |
| `db:sessions:getById` | id | Get session by ID |
| `db:decisions:create` | projectId, cycleId?, title, decision, rationale, context | Create decision |
| `db:decisions:getAll` | projectId?, limit? | Get all decisions |
| `db:learnings:create` | projectId, title, problem, solution, tags, sourceObservationId? | Create learning |
| `db:learnings:getAll` | projectId?, limit? | Get all learnings |
| `db:learnings:search` | query, filters | Full-text search with filters |

### Custom Hook (src/hooks/useMemorySearch.ts)

```typescript
interface MemoryFilters {
  types: MemoryType[]        // ['session', 'decision', 'learning']
  projectId?: string
  dateRange: 'week' | 'month' | 'all'
  tags?: string[]
}

interface MemoryItem {
  id: string
  type: MemoryType
  data: Session | Decision | Learning
  searchScore?: number
}

useMemorySearch() → {
  items: MemoryItem[]
  isLoading: boolean
  query: string
  filters: MemoryFilters
  availableTags: string[]
  search: (query: string) => void
  setFilters: (filters: Partial<MemoryFilters>) => void
}
```

### Search Algorithm
1. Query sessions, decisions, learnings in parallel
2. Apply filters: types, projectId, dateRange, tags
3. Full-text search on title, summary/rationale/problem/solution
4. Merge results with type discrimination
5. Sort by relevance (search score) then created_at DESC
6. Extract unique tags from all learnings

---

## Integration Points

### Agent Activity → Learning Promotion

**Flow:**
1. User views observation in ObservationFeed
2. Clicks ↑ (promote) button on observation
3. CaptureLearningModal opens with pre-filled data:
   - `title`: observation.concept || first line of narrative
   - `problem`: observation.narrative
   - `tags`: [observation.type]
   - `solution`: empty
4. User fills solution field, adjusts as needed
5. On save, creates learning with `source_observation_id`
6. Learning displays "From Agent" badge in Memory view

**Badge Display:**
```tsx
{learning.source_observation_id && (
  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-accent-primary/10 text-accent-primary text-xs">
    <Activity className="w-3 h-3" />
    From Agent
  </span>
)}
```

### Project View Integration

**Memory Card:**
- Shows count of decisions/sessions for current project
- "View All" link navigates to Memory page with project filter
- Empty state encourages capturing knowledge

**Quick Actions:**
- Capture Session button on Dashboard
- Record Decision available from command palette
- Capture Learning from Agent Activity ↑ button

---

## Files Created/Modified

| File | Purpose |
|------|---------|
| `src/pages/Memory.tsx` | Main memory page with search/filters |
| `src/components/modals/CaptureSessionModal.tsx` | Session capture modal |
| `src/components/modals/RecordDecisionModal.tsx` | Decision recording modal |
| `src/components/modals/CaptureLearningModal.tsx` | Learning capture modal (with promotion support) |
| `src/hooks/useMemorySearch.ts` | Custom hook for unified search |
| `src/types/index.ts` | Session, Decision, Learning types |
| `electron/ipc/index.ts` | IPC handlers for sessions, decisions, learnings |
| `electron/preload.ts` | API methods for memory operations |

---

## User Workflows

### Capturing a Session
1. Click "New" → "Capture Session"
2. Fill title, summary, duration, files changed
3. Optionally link to cycle
4. Click "Capture"
5. Session appears in Memory page, searchable

### Recording a Decision
1. Click "New" → "Record Decision"
2. Fill title, decision, rationale, context
3. Optionally link to cycle
4. Click "Record"
5. Decision appears in Memory page, searchable

### Creating a Learning (Manual)
1. Click "New" → "Capture Learning"
2. Fill title, problem, solution, tags
3. Click "Capture"
4. Learning appears in Memory page, searchable

### Creating a Learning (from Agent Activity)
1. View observation in Agent Activity feed
2. Click ↑ button on valuable observation
3. Review pre-filled problem/title/tags
4. Add solution describing how it was resolved
5. Click "Capture"
6. Learning appears with "From Agent" badge

### Searching Memory
1. Navigate to Memory page
2. Use search bar for text search
3. Filter by type, project, date, tags
4. Click learning to expand and see solution
5. Click session to view full session detail

---

## Future Enhancements

### Planned
- Export memory as markdown
- Session timeline visualization
- Decision detail modal/page
- Bulk tag management
- Memory analytics (most common tags, learning trends)

### Experimental
- AI-assisted learning extraction from sessions
- Automatic tag suggestions
- Similarity detection (duplicate learnings)
- Memory graph visualization (linked decisions/sessions)
- Cross-project learning recommendations

---

## Related Documents
- Feature Spec: `docs/FEATURES.md` (Memory section)
- Implementation Progress: `docs/IMPLEMENTATION_PROGRESS.md`
- Claude Mem Integration: `docs/CLAUDE_MEM_POLLING_IMPLEMENTATION.md`

# System Architecture: ACK

---
status: "Draft"
created: 2025-01-01
author: "jess@pike"
stage: "design"
---

## High-Level Architecture

<!-- 
Big picture system design:
- Major components
- How they interact
- Data flow
- Deployment topology
-->

### Architecture Diagram

```
[Create ASCII or link to diagram]

┌─────────────────────────────────────────────────┐
│                  Browser (Client)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Sidebar  │  │  Editor  │  │   Chat   │      │
│  │  (React) │  │ (Tiptap) │  │  (React) │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│         │              │              │          │
└─────────┼──────────────┼──────────────┼─────────┘
          │              │              │
          └──────────────┴──────────────┘
                         ↓
          ┌──────────────────────────────┐
          │   Next.js Server (Vercel)    │
          │   - API Routes               │
          │   - Server Components        │
          └──────────────────────────────┘
                         ↓
          ┌──────────────┴──────────────┐
          ↓                              ↓
┌────────────────────┐        ┌────────────────────┐
│  Supabase          │        │  Anthropic API     │
│  - PostgreSQL      │        │  - Claude          │
│  - Auth            │        │  - Agent calls     │
│  - Realtime        │        └────────────────────┘
│  - Storage         │
└────────────────────┘
```

### Component Responsibilities

**Client (Browser):**
- 
- 
- 

**Server (Next.js):**
- 
- 
- 

**Database (Supabase):**
- 
- 
- 

**AI (Anthropic):**
- 
- 
- 



## Application Structure

<!-- 
Code organization:
- Directory structure
- Module boundaries
- Component hierarchy
-->

### Directory Layout

```
/ack-mvp/
├── /app/                    # Next.js app directory
│   ├── /projects/           # Projects routes
│   │   └── /[id]/          # Project detail
│   ├── /api/               # API routes
│   └── layout.tsx          # Root layout
│
├── /components/            # React components
│   ├── /ui/               # Reusable UI components
│   ├── /editor/           # Tiptap editor components
│   ├── /sidebar/          # File tree components
│   └── /chat/             # Chat panel components
│
├── /lib/                  # Utilities & helpers
│   ├── /supabase/         # Supabase client & queries
│   ├── /tiptap/           # Tiptap config & extensions
│   └── /agents/           # Agent orchestration
│
├── /types/                # TypeScript types
├── /hooks/                # Custom React hooks
├── /config/               # Configuration files
└── /public/               # Static assets
```

### Module Boundaries

**Editor module:**
- Responsibilities:
- Dependencies:
- Exports:

**Agent module:**
- Responsibilities:
- Dependencies:
- Exports:

**Data module:**
- Responsibilities:
- Dependencies:
- Exports:



## Data Flow

<!-- 
How data moves through the system:
- User actions → state updates
- State updates → database
- Agent responses → UI
- Real-time updates
-->

### User Edit Flow

```
1. User types in editor
   ↓
2. Tiptap onChange fires
   ↓
3. Debounced auto-save (3s)
   ↓
4. Update Supabase (content + metadata)
   ↓
5. Update local state
   ↓
6. UI shows "Saved" indicator
```

### Agent Interaction Flow

```
1. User sends message
   ↓
2. Load artifact context
   ↓
3. Build agent prompt
   ↓
4. Create snapshot (pre-change)
   ↓
5. Call Anthropic API
   ↓
6. Stream response to UI
   ↓
7. Parse agent output
   ↓
8. Update artifact if needed
   ↓
9. Save to database
```

### Real-time Sync Flow

```
1. User A updates artifact
   ↓
2. Supabase UPDATE triggers
   ↓
3. Realtime event broadcasts
   ↓
4. User B receives update
   ↓
5. Local state merges changes
   ↓
6. UI re-renders
```



## State Management

<!-- 
How is application state managed?
- Client state
- Server state
- Sync strategy
- Cache strategy
-->

### Client State

**Tool:** 


**State structure:**
```typescript
{
  currentProject: Project | null,
  currentArtifact: Artifact | null,
  currentSection: string | null,
  unsavedChanges: boolean,
  // ...
}
```

**State update patterns:**
- 
- 


### Server State (Database)

**Cache strategy:**
- What gets cached:
- Cache invalidation:
- Cache duration:


**Optimistic updates:**
- When to use:
- Rollback strategy:



## API Design

<!-- 
API routes and contracts:
- REST endpoints (or GraphQL schema)
- Request/response formats
- Authentication
- Error handling
-->

### Core Endpoints

**Projects:**
```typescript
GET    /api/projects              // List all projects
POST   /api/projects              // Create project
GET    /api/projects/[id]         // Get project
PUT    /api/projects/[id]         // Update project
DELETE /api/projects/[id]         // Delete project
```

**Artifacts:**
```typescript
GET    /api/projects/[id]/artifacts           // List artifacts
POST   /api/projects/[id]/artifacts           // Create artifact
GET    /api/artifacts/[id]                    // Get artifact
PUT    /api/artifacts/[id]                    // Update artifact
PATCH  /api/artifacts/[id]/section/[slug]     // Update section
POST   /api/artifacts/[id]/snapshot           // Create snapshot
```

**Agents:**
```typescript
POST   /api/chat                  // Send message, get response
POST   /api/agents/research       // Trigger research agent
POST   /api/agents/validate       // Validate artifact content
```

### Request/Response Examples

**Update section:**
```typescript
// Request
PATCH /api/artifacts/abc123/section/what-is-it
{
  "content": { /* Tiptap JSON */ },
  "is_done": true
}

// Response
{
  "success": true,
  "artifact": {
    "sections_complete": 3,
    "sections_total": 6,
    "updated_at": "2025-01-01T12:00:00Z"
  }
}
```



## Security Architecture

<!-- 
How is the system secured?
- Authentication
- Authorization
- Data protection
- API security
-->

### Authentication

**Method:**


**Flow:**
1. 
2. 
3. 


### Authorization

**Row Level Security (RLS):**
```sql
-- Example policy
CREATE POLICY "Users can only see their own projects"
ON projects FOR SELECT
USING (auth.uid() = created_by);
```

**API middleware:**
- 
- 


### Data Protection

**Sensitive data:**
- How stored:
- How transmitted:
- Encryption:


**API keys:**
- Where stored:
- Rotation strategy:



## Performance Architecture

<!-- 
Performance optimization strategies:
- Caching
- Lazy loading
- Code splitting
- Database indexes
-->

### Client Performance

**Code splitting:**
- 
- 

**Lazy loading:**
- 
- 

**Bundle size target:**


### Server Performance

**Database optimization:**
- Indexes on:
- Query patterns:
- Connection pooling:


**API response times:**
| Endpoint | Target | Current |
|----------|--------|---------|
| GET artifact | < 100ms | |
| UPDATE artifact | < 200ms | |
| Agent chat | < 5s | |



## Error Handling & Resilience

<!-- 
How does the system handle failures?
- Error boundaries
- Retry logic
- Fallbacks
- User feedback
-->

### Error Boundaries

**Client errors:**
- React error boundaries at:
- Fallback UI:
- Error reporting:


**API errors:**
```typescript
{
  "error": {
    "code": "ARTIFACT_NOT_FOUND",
    "message": "Artifact abc123 not found",
    "details": {}
  }
}
```

### Retry Logic

**Network failures:**
- Auto-retry:
- Backoff strategy:
- Max retries:


**Agent API failures:**
- Fallback provider:
- Rate limit handling:
- Timeout handling:



## Scalability Considerations

<!-- 
How will this scale?
- Bottlenecks identified
- Horizontal vs vertical scaling
- Database scaling
- Cost implications
-->

### Current Bottlenecks

1. **[Bottleneck]:**
   - Impact:
   - Mitigation:
   - Scale threshold:

2. **[Bottleneck]:**
   - Impact:
   - Mitigation:
   - Scale threshold:


### Scaling Strategy

**0-100 users:**
- 

**100-1000 users:**
- 

**1000+ users:**
- 



## Monitoring & Observability

<!-- 
How do we know the system is healthy?
- Metrics
- Logging
- Alerts
- Dashboards
-->

### Key Metrics

**Application:**
- Active users (DAU/WAU/MAU)
- Session duration
- Artifact completion rate
- Error rate


**Infrastructure:**
- API response times
- Database query times
- Memory usage
- CPU usage


### Logging Strategy

**What to log:**
- 
- 
- 

**Log levels:**
- DEBUG:
- INFO:
- WARN:
- ERROR:


### Alerts

**Critical alerts:**
- 
- 
- 

**Warning alerts:**
- 
- 



---

## Architecture Decision Records (ADRs)

<!-- 
Document major architectural decisions:
-->

### ADR-001: Use Next.js App Router
**Date:** 2025-01-01
**Status:** Accepted

**Context:**


**Decision:**


**Consequences:**
- Positive:
- Negative:


### ADR-002: Hybrid Data Model (Content + Metadata)
**Date:** 2025-01-01
**Status:** Accepted

**Context:**


**Decision:**


**Consequences:**



---

**Open questions:**
- [ ] How to handle concurrent edits to same artifact?
- [ ] What happens if agent API is down?
- [ ] How to migrate data model if schema changes?
- [ ]

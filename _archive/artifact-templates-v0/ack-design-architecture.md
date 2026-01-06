---
type: artifact
stage: design
artifact: architecture
description: "System architecture, components, and data flow"
version: 1.0.0
updated: "2026-01-04T09:26:12"
status: draft
---

# [Project Name] - Architecture

## Overview

<!-- High-level system design summary -->

[Brief description of the overall architecture approach and key design decisions]

---

## High-Level Architecture

<!-- Big picture system design -->

### Architecture Diagram

```
[ASCII diagram or link to diagram]

┌─────────────────────────────────────────────────┐
│                  [Layer 1]                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │[Component]│  │[Component]│  │[Component]│    │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘
                         ↓
          ┌──────────────────────────────┐
          │        [Layer 2]              │
          │   - [Responsibility]          │
          │   - [Responsibility]          │
          └──────────────────────────────┘
                         ↓
          ┌──────────────┴──────────────┐
          ↓                              ↓
┌────────────────────┐        ┌────────────────────┐
│  [Service 1]       │        │  [Service 2]       │
│  - [Detail]        │        │  - [Detail]        │
│  - [Detail]        │        │  - [Detail]        │
└────────────────────┘        └────────────────────┘
```

### Component Responsibilities

**[Layer/Component 1]:**
- [Responsibility]
- [Responsibility]
- [Responsibility]

**[Layer/Component 2]:**
- [Responsibility]
- [Responsibility]

**[Layer/Component 3]:**
- [Responsibility]
- [Responsibility]

---

## Application Structure

<!-- Code organization -->

### Directory Layout

```
/[project-name]/
├── /[directory-1]/          # [Purpose]
│   ├── /[subdirectory]/     # [Purpose]
│   └── [file]               # [Purpose]
│
├── /[directory-2]/          # [Purpose]
│   ├── /[subdirectory]/     # [Purpose]
│   └── /[subdirectory]/     # [Purpose]
│
├── /[directory-3]/          # [Purpose]
│   └── /[subdirectory]/     # [Purpose]
│
├── /[directory-4]/          # [Purpose]
└── /[directory-5]/          # [Purpose]
```

### Module Boundaries

**[Module 1]:**
- Responsibilities: [What it does]
- Dependencies: [What it needs]
- Exports: [What it provides]

**[Module 2]:**
- Responsibilities: [What it does]
- Dependencies: [What it needs]
- Exports: [What it provides]

---

## Data Flow

<!-- How data moves through the system -->

### [Flow 1]: [Name]

```
1. [Step 1]
   ↓
2. [Step 2]
   ↓
3. [Step 3]
   ↓
4. [Step 4]
   ↓
5. [Step 5]
```

### [Flow 2]: [Name]

```
1. [Step 1]
   ↓
2. [Step 2]
   ↓
3. [Step 3]
```

---

## State Management

<!-- How is application state managed? -->

### Client State

**Tool:** [State management solution]

**State structure:**
```typescript
{
  [stateKey]: [Type],
  [stateKey]: [Type],
  // ...
}
```

**State update patterns:**
- [Pattern 1]
- [Pattern 2]


### Server State

**Cache strategy:**
- What gets cached: [Items]
- Cache invalidation: [Strategy]
- Cache duration: [Duration]

**Optimistic updates:**
- When to use: [Scenarios]
- Rollback strategy: [Approach]

---

## API Design

<!-- API routes and contracts -->

### Core Endpoints

**[Resource 1]:**
```
GET    /api/[resource]              # List all
POST   /api/[resource]              # Create
GET    /api/[resource]/[id]         # Get one
PUT    /api/[resource]/[id]         # Update
DELETE /api/[resource]/[id]         # Delete
```

**[Resource 2]:**
```
GET    /api/[resource]              # List all
POST   /api/[resource]              # Create
```

### Request/Response Examples

**[Example operation]:**
```typescript
// Request
[METHOD] /api/[endpoint]
{
  "[field]": "[value]"
}

// Response
{
  "success": true,
  "[field]": "[value]"
}
```

---

## Security Architecture

<!-- How is the system secured? -->

### Authentication

**Method:** [Auth method]

**Flow:**
1. [Step 1]
2. [Step 2]
3. [Step 3]


### Authorization

**Access control:**
- [Rule 1]
- [Rule 2]

**API middleware:**
- [Middleware 1]
- [Middleware 2]


### Data Protection

**Sensitive data:**
- How stored: [Method]
- How transmitted: [Method]
- Encryption: [Method]

---

## Performance Architecture

<!-- Performance optimization strategies -->

### Client Performance

**Code splitting:** [Strategy]

**Lazy loading:** [Strategy]

**Bundle size target:** [Target]


### Server Performance

**Database optimization:**
- Indexes on: [Fields]
- Query patterns: [Patterns]
- Connection pooling: [Configuration]

**API response times:**

| Endpoint | Target | Current |
|----------|--------|---------|
| [Endpoint 1] | < [X]ms | |
| [Endpoint 2] | < [X]ms | |
| [Endpoint 3] | < [X]s | |

---

## Error Handling & Resilience

<!-- How does the system handle failures? -->

### Error Boundaries

**Client errors:**
- Error boundaries at: [Locations]
- Fallback UI: [Description]
- Error reporting: [Service]

**API errors:**
```typescript
{
  "error": {
    "code": "[ERROR_CODE]",
    "message": "[Human-readable message]",
    "details": {}
  }
}
```

### Retry Logic

**Network failures:**
- Auto-retry: [Yes/No]
- Backoff strategy: [Strategy]
- Max retries: [Number]

---

## Scalability Considerations

<!-- How will this scale? -->

### Current Bottlenecks

1. **[Bottleneck]:**
   - Impact: [Description]
   - Mitigation: [Strategy]
   - Scale threshold: [When it becomes problem]

### Scaling Strategy

**[X]-[Y] users:** [Strategy]

**[Y]-[Z] users:** [Strategy]

**[Z]+ users:** [Strategy]

---

## Monitoring & Observability

<!-- How do we know the system is healthy? -->

### Key Metrics

**Application:**
- [Metric 1]
- [Metric 2]
- [Metric 3]

**Infrastructure:**
- [Metric 1]
- [Metric 2]


### Logging Strategy

**What to log:**
- [Log type 1]
- [Log type 2]

**Log levels:** DEBUG, INFO, WARN, ERROR


### Alerts

**Critical:**
- [Alert condition]

**Warning:**
- [Alert condition]

---

## Architecture Decision Records

<!-- Document major decisions -->

### ADR-001: [Decision Title]

**Date:** [Date]
**Status:** [Accepted/Proposed/Deprecated]

**Context:** [Why this decision was needed]

**Decision:** [What was decided]

**Consequences:**
- Positive: [Benefits]
- Negative: [Tradeoffs]


### ADR-002: [Decision Title]

**Date:** [Date]
**Status:** [Accepted/Proposed/Deprecated]

**Context:** [Why this decision was needed]

**Decision:** [What was decided]

**Consequences:**
- [Consequence]

---

## Open Questions

- [ ] [Architecture question]
- [ ] [Design decision to make]
- [ ] [Scalability concern to address]
